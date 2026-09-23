"""Phase 14.11G.5D real TaskSession/Governor integration tests.

These tests exercise the frozen production path:

TaskSessionManager.send_runtime_turn()
    -> Reasoning resolution
    -> Auto eligibility
    -> production Auto router
    -> Model Form freeze
    -> ResourceRequest preparation
    -> Governor
    -> injected fake external runtime adapter

Production source and production bindings are never modified.

The live production registry currently exposes Small only.
Big-path tests therefore use a temporary test-only binding
registry while exercising the exact same TaskSession code.
"""

from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from model_form.automatic_routing_evidence import (
    AutomaticModelFormEvidence,
)
from resources import (
    GovernorDecision,
)
from runtime.task_session import (
    TaskSessionError,
    TaskSessionManager,
)


ROOT = Path(__file__).resolve().parents[1]


class FakeRuntimeAdapter:
    """Harmless external runtime boundary for integration tests."""

    adapter_name = "hermes"

    def __init__(self):
        self.create_calls = []
        self.get_calls = []
        self.send_calls = []
        self.end_calls = []

    def get_active_toolsets(self, state):
        return []

    def create_session(
        self,
        state,
        task_id=None,
    ):
        session_id = (
            f"g5d-session-{len(self.create_calls) + 1}"
        )

        self.create_calls.append(
            {
                "state": state,
                "task_id": task_id,
                "session_id": session_id,
            }
        )

        return {
            "adapter": self.adapter_name,
            "session_id": session_id,
        }

    def get_session(
        self,
        session_id,
        state,
    ):
        self.get_calls.append(
            {
                "session_id": session_id,
                "state": state,
            }
        )

        return {
            "adapter": self.adapter_name,
            "session_id": str(session_id),
        }

    def send_turn(
        self,
        session_id,
        message,
        state,
        instructions=None,
        reasoning_mode=None,
    ):
        self.send_calls.append(
            {
                "session_id": str(session_id),
                "message": message,
                "state": state,
                "instructions": instructions,
                "reasoning_mode": reasoning_mode,
            }
        )

        return {
            "adapter": self.adapter_name,
            "session_id": str(session_id),
            "output": "synthetic integration success",
        }

    def is_stale_session_error(
        self,
        exc,
    ):
        return False

    def end_session(
        self,
        session_id,
        state,
    ):
        self.end_calls.append(
            {
                "session_id": str(session_id),
                "state": state,
            }
        )

        return {
            "adapter": self.adapter_name,
            "session_id": str(session_id),
        }


class RecordingGovernor:
    def __init__(
        self,
        outcome,
    ):
        self.outcome = outcome
        self.requests = []

    def __call__(
        self,
        request,
    ):
        self.requests.append(
            request
        )

        return GovernorDecision(
            request=request,
            outcome=self.outcome,
            source="g5d-integration-governor",
            reasons=(
                f"integration_{self.outcome}",
            ),
        )


def active_state(
    task_id="task-g5d",
):
    """Smallest active in-memory Forest Task state."""

    return {
        "task_session": {
            "id": task_id,
            "status": "active",
            "runtime_sessions": {},
            "task_sticky_skills": [],
            "temporary_capabilities": [],
        },
    }


def big_evidence():
    return (
        AutomaticModelFormEvidence(
            signal="task_complexity",
            value="high",
            producer="g5d-integration-test",
        ),
    )


def runtime_side_effect_count(
    adapter,
):
    return (
        len(adapter.create_calls)
        + len(adapter.send_calls)
        + len(adapter.end_calls)
    )


@contextmanager
def manager_fixture(
    *,
    include_big=False,
):
    adapter = FakeRuntimeAdapter()

    manager = TaskSessionManager(
        forest_root=ROOT,
        runtime_adapter=adapter,
    )

    if not include_big:
        yield manager, adapter
        return

    with tempfile.TemporaryDirectory(
        prefix="forest-g5d-bindings-"
    ) as temp_dir:
        binding_file = (
            Path(temp_dir)
            / "bindings.yaml"
        )

        binding_file.write_text(
            """schema_version: 1
forms:
  small: binding-0001
  big: binding-g5d-big
bindings:
  binding-0001:
    runtime:
      adapter: hermes
      profile: bristlecone
      platform: api_server
  binding-g5d-big:
    runtime:
      adapter: hermes
      profile: bristlecone-g5d-big
      platform: api_server
""",
            encoding="utf-8",
        )

        manager.model_binding_registry_file = (
            binding_file
        )

        yield manager, adapter


def send_governed_turn(
    manager,
    *,
    governor,
    evidence=(),
    task_id="task-g5d",
):
    return manager.send_runtime_turn(
        "G.5D production integration turn",
        state=active_state(
            task_id
        ),
        instructions="G.5D integration test",
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-g5d",
        automatic_model_form_evidence=(
            tuple(evidence)
        ),
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "g5d-integration-test"
        ),
        resource_request_reasons=(
            "production_path_certification",
        ),
        resource_may_defer=True,
    )


class LiveSmallGovernorTests(
    unittest.TestCase
):
    """Use the untouched production Small-only registry."""

    def test_live_small_approve_reaches_runtime(
        self,
    ):
        governor = RecordingGovernor(
            "approve"
        )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            result = send_governed_turn(
                manager,
                governor=governor,
            )

            self.assertEqual(
                len(governor.requests),
                1,
            )

            request = governor.requests[0]

            self.assertEqual(
                request.model_form,
                "small",
            )
            self.assertEqual(
                request.execution_context_id,
                "ctx-g5d",
            )
            self.assertEqual(
                request.task_id,
                "task-g5d",
            )
            self.assertEqual(
                request.reasoning_mode,
                "normal",
            )

            self.assertEqual(
                len(adapter.create_calls),
                1,
            )
            self.assertEqual(
                len(adapter.send_calls),
                1,
            )

            self.assertIsInstance(
                result,
                dict,
            )

    def test_live_small_defer_stops_before_runtime(
        self,
    ):
        governor = RecordingGovernor(
            "defer"
        )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ) as caught:
                send_governed_turn(
                    manager,
                    governor=governor,
                )

            self.assertEqual(
                len(governor.requests),
                1,
            )
            self.assertEqual(
                governor.requests[0].model_form,
                "small",
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

            decision = getattr(
                caught.exception,
                "resource_governor_decision",
                None,
            )

            self.assertIsNotNone(
                decision
            )
            self.assertEqual(
                decision.outcome,
                "defer",
            )
            self.assertIs(
                decision.request,
                governor.requests[0],
            )

    def test_live_small_deny_stops_before_runtime(
        self,
    ):
        governor = RecordingGovernor(
            "deny"
        )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ) as caught:
                send_governed_turn(
                    manager,
                    governor=governor,
                )

            self.assertEqual(
                len(governor.requests),
                1,
            )
            self.assertEqual(
                governor.requests[0].model_form,
                "small",
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

            decision = getattr(
                caught.exception,
                "resource_governor_decision",
                None,
            )

            self.assertIsNotNone(
                decision
            )
            self.assertEqual(
                decision.outcome,
                "deny",
            )
            self.assertIs(
                decision.request,
                governor.requests[0],
            )

    def test_live_big_unavailable_fails_before_governor(
        self,
    ):
        governor = RecordingGovernor(
            "approve"
        )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ):
                send_governed_turn(
                    manager,
                    governor=governor,
                    evidence=big_evidence(),
                )

            # Production Big is not bound.
            # Fail closed before Governor/runtime.
            self.assertEqual(
                governor.requests,
                [],
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )


class TestBoundBigGovernorTests(
    unittest.TestCase
):
    """Use a temporary Big binding without changing production."""

    def test_big_approve_reaches_runtime_as_big(
        self,
    ):
        governor = RecordingGovernor(
            "approve"
        )

        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            send_governed_turn(
                manager,
                governor=governor,
                evidence=big_evidence(),
            )

            self.assertEqual(
                len(governor.requests),
                1,
            )

            request = governor.requests[0]

            self.assertEqual(
                request.model_form,
                "big",
            )
            self.assertIn(
                "high_task_complexity",
                request.reasons,
            )

            self.assertEqual(
                len(adapter.create_calls),
                1,
            )
            self.assertEqual(
                len(adapter.send_calls),
                1,
            )

    def test_big_defer_stays_big_and_never_reaches_runtime(
        self,
    ):
        governor = RecordingGovernor(
            "defer"
        )

        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ) as caught:
                send_governed_turn(
                    manager,
                    governor=governor,
                    evidence=big_evidence(),
                )

            self.assertEqual(
                len(governor.requests),
                1,
            )

            request = governor.requests[0]

            self.assertEqual(
                request.model_form,
                "big",
            )
            self.assertIn(
                "high_task_complexity",
                request.reasons,
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

            decision = (
                caught.exception
                .resource_governor_decision
            )

            self.assertEqual(
                decision.outcome,
                "defer",
            )
            self.assertIs(
                decision.request,
                request,
            )

    def test_big_deny_stays_big_and_never_reaches_runtime(
        self,
    ):
        governor = RecordingGovernor(
            "deny"
        )

        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ) as caught:
                send_governed_turn(
                    manager,
                    governor=governor,
                    evidence=big_evidence(),
                )

            self.assertEqual(
                len(governor.requests),
                1,
            )

            request = governor.requests[0]

            self.assertEqual(
                request.model_form,
                "big",
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

            decision = (
                caught.exception
                .resource_governor_decision
            )

            self.assertEqual(
                decision.outcome,
                "deny",
            )
            self.assertIs(
                decision.request,
                request,
            )


class GovernorFailureBoundaryTests(
    unittest.TestCase
):
    def test_wrong_request_identity_fails_closed(
        self,
    ):
        seen = []

        def wrong_identity_governor(
            request,
        ):
            seen.append(
                request
            )

            replacement = replace(
                request
            )

            self.assertIsNot(
                replacement,
                request,
            )

            return GovernorDecision(
                request=replacement,
                outcome="approve",
                source="g5d-wrong-identity",
                reasons=(
                    "wrong_request_identity",
                ),
            )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ):
                send_governed_turn(
                    manager,
                    governor=(
                        wrong_identity_governor
                    ),
                )

            self.assertEqual(
                len(seen),
                1,
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

    def test_malformed_governor_result_fails_closed(
        self,
    ):
        seen = []

        def malformed_governor(
            request,
        ):
            seen.append(
                request
            )

            return {
                "request": request,
                "outcome": "approve",
            }

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ):
                send_governed_turn(
                    manager,
                    governor=malformed_governor,
                )

            self.assertEqual(
                len(seen),
                1,
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )

    def test_governor_exception_fails_closed(
        self,
    ):
        seen = []

        def exploding_governor(
            request,
        ):
            seen.append(
                request
            )

            raise RuntimeError(
                "synthetic Governor failure"
            )

        with manager_fixture() as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                TaskSessionError
            ):
                send_governed_turn(
                    manager,
                    governor=exploding_governor,
                )

            self.assertEqual(
                len(seen),
                1,
            )
            self.assertEqual(
                runtime_side_effect_count(
                    adapter
                ),
                0,
            )


if __name__ == "__main__":
    unittest.main()
