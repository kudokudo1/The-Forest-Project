import copy
import importlib.util
import sys
import unittest
from pathlib import Path

from runtime.session_store import (
    get_runtime_session_binding,
    set_runtime_session_binding,
)


BINDING = "binding-0001"
NOW = "2026-08-11T00:00:00Z"


# Reuse the already-certified G.6 runtime adapter rather than
# creating another independent fake-runtime implementation.
G6_PATH = Path(__file__).with_name(
    "test_model_form_retry_task_session_integration.py"
)

SPEC = importlib.util.spec_from_file_location(
    "_forest_g6_retry_harness",
    G6_PATH,
)

if SPEC is None or SPEC.loader is None:
    raise RuntimeError(
        "Could not load certified G.6 retry harness."
    )

G6 = importlib.util.module_from_spec(
    SPEC
)

sys.modules[SPEC.name] = G6
SPEC.loader.exec_module(G6)


RetryRuntimeAdapter = G6.RetryRuntimeAdapter
SyntheticStaleSessionError = (
    G6.SyntheticStaleSessionError
)
SyntheticRuntimeFailure = (
    G6.SyntheticRuntimeFailure
)


def bind(
    sessions,
    context_id,
    session_id,
    *,
    previous_session_id=None,
):
    return set_runtime_session_binding(
        sessions,
        context_id,
        BINDING,
        adapter="hermes",
        session_id=session_id,
        previous_session_id=previous_session_id,
        updated_at=NOW,
    )


def lookup(
    sessions,
    context_id,
):
    return get_runtime_session_binding(
        sessions,
        context_id,
        BINDING,
    )


def create_session(
    adapter,
    task_id,
):
    result = adapter.create_session(
        {},
        task_id=task_id,
    )

    if not isinstance(result, dict):
        raise AssertionError(
            "Certified adapter create_session "
            "did not return a mapping."
        )

    session_id = result.get(
        "session_id"
    )

    if not session_id:
        raise AssertionError(
            "Certified adapter returned no session_id."
        )

    return str(session_id)


def send(
    adapter,
    session_id,
):
    return adapter.send_turn(
        session_id,
        "H.4 Colony lifecycle turn",
        {},
        instructions="H.4 lifecycle test",
        reasoning_mode="normal",
    )


class ColonyRuntimeLifecycleTests(
    unittest.TestCase
):

    def test_create_same_binding_keeps_context_sessions_separate(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            []
        )

        sessions = {}

        session_a = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        self.assertNotEqual(
            session_a,
            session_b,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-A",
            )["session_id"],
            session_a,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            )["session_id"],
            session_b,
        )

    def test_reuse_in_a_does_not_change_b(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            ["ok"]
        )

        sessions = {}

        session_a = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        before_b = copy.deepcopy(
            lookup(
                sessions,
                "ctx-B",
            )
        )

        result = send(
            adapter,
            session_a,
        )

        self.assertEqual(
            str(result["session_id"]),
            session_a,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-A",
            )["session_id"],
            session_a,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            ),
            before_b,
        )

        self.assertEqual(
            len(adapter.send_calls),
            1,
        )

        self.assertEqual(
            str(
                adapter.send_calls[0][
                    "session_id"
                ]
            ),
            session_a,
        )

    def test_stale_recovery_in_a_replaces_only_a(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            [
                "stale",
                "ok",
            ]
        )

        sessions = {}

        session_a = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        before_b = copy.deepcopy(
            lookup(
                sessions,
                "ctx-B",
            )
        )

        try:
            send(
                adapter,
                session_a,
            )

        except SyntheticStaleSessionError as exc:
            self.assertTrue(
                adapter.is_stale_session_error(
                    exc
                )
            )

        else:
            self.fail(
                "Expected synthetic stale-session error."
            )

        replacement_a = create_session(
            adapter,
            "task-A",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            replacement_a,
            previous_session_id=session_a,
        )

        retry_result = send(
            adapter,
            replacement_a,
        )

        self.assertEqual(
            str(
                retry_result[
                    "session_id"
                ]
            ),
            replacement_a,
        )

        binding_a = lookup(
            sessions,
            "ctx-A",
        )

        self.assertEqual(
            binding_a["session_id"],
            replacement_a,
        )

        self.assertEqual(
            binding_a["previous_session_id"],
            session_a,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            ),
            before_b,
        )

        self.assertEqual(
            [
                str(call["session_id"])
                for call in adapter.send_calls
            ],
            [
                session_a,
                replacement_a,
            ],
        )

        self.assertEqual(
            len(adapter.classifier_calls),
            1,
        )

    def test_rotation_of_a_binding_does_not_rotate_b(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            []
        )

        sessions = {}

        session_a1 = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a1,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        before_b = copy.deepcopy(
            lookup(
                sessions,
                "ctx-B",
            )
        )

        session_a2 = create_session(
            adapter,
            "task-A",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a2,
            previous_session_id=session_a1,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-A",
            )["session_id"],
            session_a2,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-A",
            )["previous_session_id"],
            session_a1,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            ),
            before_b,
        )

    def test_retiring_obsolete_a_session_never_ends_b(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            []
        )

        sessions = {}

        session_a1 = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a1,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        session_a2 = create_session(
            adapter,
            "task-A",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a2,
            previous_session_id=session_a1,
        )

        adapter.end_session(
            session_a1,
            {},
        )

        ended = [
            str(call["session_id"])
            for call in adapter.end_calls
        ]

        self.assertEqual(
            ended,
            [session_a1],
        )

        self.assertNotIn(
            session_b,
            ended,
        )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            )["session_id"],
            session_b,
        )

    def test_nonstale_failure_in_a_does_not_touch_b(
        self,
    ):
        adapter = RetryRuntimeAdapter(
            ["fail"]
        )

        sessions = {}

        session_a = create_session(
            adapter,
            "task-A",
        )

        session_b = create_session(
            adapter,
            "task-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            session_a,
        )

        sessions = bind(
            sessions,
            "ctx-B",
            session_b,
        )

        before_b = copy.deepcopy(
            lookup(
                sessions,
                "ctx-B",
            )
        )

        try:
            send(
                adapter,
                session_a,
            )

        except SyntheticRuntimeFailure as exc:
            self.assertFalse(
                adapter.is_stale_session_error(
                    exc
                )
            )

        else:
            self.fail(
                "Expected synthetic runtime failure."
            )

        self.assertEqual(
            lookup(
                sessions,
                "ctx-B",
            ),
            before_b,
        )

        self.assertEqual(
            adapter.end_calls,
            [],
        )


if __name__ == "__main__":
    unittest.main()
