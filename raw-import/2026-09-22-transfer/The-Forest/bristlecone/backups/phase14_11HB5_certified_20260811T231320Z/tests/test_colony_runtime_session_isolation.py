import copy
import unittest

from runtime.session_store import (
    get_runtime_session_binding,
    set_runtime_session_binding,
)


NOW = "2026-08-11T00:00:00Z"


def bind(
    sessions,
    context_id,
    binding_id,
    session_id,
    *,
    previous_session_id=None,
):
    return set_runtime_session_binding(
        sessions,
        context_id,
        binding_id,
        adapter="hermes",
        session_id=session_id,
        previous_session_id=previous_session_id,
        updated_at=NOW,
    )


class ColonyRuntimeSessionIsolationTests(
    unittest.TestCase
):

    def test_same_binding_different_contexts_have_separate_sessions(
        self,
    ):
        sessions = {}

        sessions = bind(
            sessions,
            "ctx-ortet",
            "binding-0001",
            "session-ortet",
        )

        sessions = bind(
            sessions,
            "ctx-ramet",
            "binding-0001",
            "session-ramet",
        )

        ortet = get_runtime_session_binding(
            sessions,
            "ctx-ortet",
            "binding-0001",
        )

        ramet = get_runtime_session_binding(
            sessions,
            "ctx-ramet",
            "binding-0001",
        )

        self.assertEqual(
            ortet["session_id"],
            "session-ortet",
        )

        self.assertEqual(
            ramet["session_id"],
            "session-ramet",
        )

        self.assertNotEqual(
            ortet["session_id"],
            ramet["session_id"],
        )

    def test_same_context_different_bindings_have_separate_sessions(
        self,
    ):
        sessions = {}

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-small",
            "session-small",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-big",
            "session-big",
        )

        small = get_runtime_session_binding(
            sessions,
            "ctx-A",
            "binding-small",
        )

        big = get_runtime_session_binding(
            sessions,
            "ctx-A",
            "binding-big",
        )

        self.assertEqual(
            small["session_id"],
            "session-small",
        )

        self.assertEqual(
            big["session_id"],
            "session-big",
        )

        self.assertNotEqual(
            small["session_id"],
            big["session_id"],
        )

    def test_exact_context_and_binding_resolves_canonical_entry(
        self,
    ):
        sessions = {}

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-0001",
            "session-A",
        )

        first = get_runtime_session_binding(
            sessions,
            "ctx-A",
            "binding-0001",
        )

        second = get_runtime_session_binding(
            sessions,
            "ctx-A",
            "binding-0001",
        )

        self.assertEqual(
            first,
            second,
        )

        self.assertEqual(
            first["session_id"],
            "session-A",
        )

    def test_updating_one_identity_does_not_change_neighbors(
        self,
    ):
        sessions = {}

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-0001",
            "session-A1",
        )

        sessions = bind(
            sessions,
            "ctx-B",
            "binding-0001",
            "session-B",
        )

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-0002",
            "session-C",
        )

        before = copy.deepcopy(
            sessions
        )

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-0001",
            "session-A2",
            previous_session_id="session-A1",
        )

        updated = get_runtime_session_binding(
            sessions,
            "ctx-A",
            "binding-0001",
        )

        neighbor_context = (
            get_runtime_session_binding(
                sessions,
                "ctx-B",
                "binding-0001",
            )
        )

        neighbor_binding = (
            get_runtime_session_binding(
                sessions,
                "ctx-A",
                "binding-0002",
            )
        )

        self.assertEqual(
            updated["session_id"],
            "session-A2",
        )

        self.assertEqual(
            updated["previous_session_id"],
            "session-A1",
        )

        self.assertEqual(
            neighbor_context,
            get_runtime_session_binding(
                before,
                "ctx-B",
                "binding-0001",
            ),
        )

        self.assertEqual(
            neighbor_binding,
            get_runtime_session_binding(
                before,
                "ctx-A",
                "binding-0002",
            ),
        )

    def test_set_is_pure_and_does_not_mutate_input_mapping(
        self,
    ):
        original = {}

        result = bind(
            original,
            "ctx-A",
            "binding-0001",
            "session-A",
        )

        self.assertEqual(
            original,
            {},
        )

        self.assertIsNot(
            result,
            original,
        )

        self.assertEqual(
            get_runtime_session_binding(
                result,
                "ctx-A",
                "binding-0001",
            )["session_id"],
            "session-A",
        )

    def test_missing_neighbor_identity_returns_none(
        self,
    ):
        sessions = {}

        sessions = bind(
            sessions,
            "ctx-A",
            "binding-0001",
            "session-A",
        )

        self.assertIsNone(
            get_runtime_session_binding(
                sessions,
                "ctx-B",
                "binding-0001",
            )
        )

        self.assertIsNone(
            get_runtime_session_binding(
                sessions,
                "ctx-A",
                "binding-0002",
            )
        )


if __name__ == "__main__":
    unittest.main()
