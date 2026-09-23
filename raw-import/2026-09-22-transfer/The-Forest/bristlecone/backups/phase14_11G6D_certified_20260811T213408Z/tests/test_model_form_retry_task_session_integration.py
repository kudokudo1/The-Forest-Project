"""Phase 14.11G.6D real TaskSession retry/isolation certification.

Production path exercised:

TaskSessionManager.send_runtime_turn()
    -> Reasoning resolution
    -> Auto eligibility
    -> production Auto router
    -> Model Form freeze
    -> optional ResourceRequest/Governor
    -> runtime session
    -> stale detection
    -> replacement session
    -> ONE retry

Only the external runtime adapter is fake.
Production source is not replaced.
"""

from contextlib import contextmanager
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import reasoning

import model_form.automatic_routing_policy as routing_policy

from model_form.automatic_routing import (
    AutomaticModelFormRecommendation,
)
from model_form.automatic_routing_evidence import (
    AutomaticModelFormEvidence,
)
from resources import GovernorDecision
from runtime.task_session import (
    TaskSessionError,
    TaskSessionManager,
)


ROOT = Path(__file__).resolve().parents[1]


class SyntheticStaleSessionError(RuntimeError):
    pass


class SyntheticRuntimeFailure(RuntimeError):
    pass


class RetryRuntimeAdapter:
    adapter_name = "hermes"

    def __init__(
        self,
        outcomes=(),
    ):
        self.outcomes = list(outcomes)
        self.create_calls = []
        self.send_calls = []
        self.end_calls = []
        self.classifier_calls = []

    def get_active_toolsets(
        self,
        state,
    ):
        return []

    def create_session(
        self,
        state,
        task_id=None,
    ):
        session_id = (
            f"g6d-session-"
            f"{len(self.create_calls) + 1}"
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

        outcome = (
            self.outcomes.pop(0)
            if self.outcomes
            else "ok"
        )

        if outcome == "stale":
            raise SyntheticStaleSessionError(
                "synthetic stale session"
            )

        if outcome == "fail":
            raise SyntheticRuntimeFailure(
                "synthetic runtime failure"
            )

        if outcome != "ok":
            raise AssertionError(
                f"Unknown outcome: {outcome!r}"
            )

        return {
            "adapter": self.adapter_name,
            "session_id": str(session_id),
            "output": "G.6D success",
        }

    def is_stale_session_error(
        self,
        exc,
    ):
        self.classifier_calls.append(
            exc
        )

        return isinstance(
            exc,
            SyntheticStaleSessionError,
        )

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
    def __init__(self):
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
            outcome="approve",
            source="g6d-governor",
            reasons=(
                "g6d_approve",
            ),
        )


def active_state(
    task_id="task-g6d",
):
    return {
        "task_session": {
            "id": task_id,
            "status": "active",
            "runtime_sessions": {},
            "task_sticky_skills": [],
            "temporary_capabilities": [],
        },
    }


def high_complexity():
    return (
        AutomaticModelFormEvidence(
            signal="task_complexity",
            value="high",
            producer="g6d-integration-test",
        ),
    )


@contextmanager
def manager_fixture(
    *,
    outcomes=(),
    include_big=False,
):
    adapter = RetryRuntimeAdapter(
        outcomes=outcomes
    )

    manager = TaskSessionManager(
        forest_root=ROOT,
        runtime_adapter=adapter,
    )

    if not include_big:
        yield manager, adapter
        return

    with tempfile.TemporaryDirectory(
        prefix="forest-g6d-bindings-"
    ) as temp_dir:
        binding_file = (
            Path(temp_dir)
            / "bindings.yaml"
        )

        binding_file.write_text(
            """schema_version: 1
forms:
  small: binding-0001
  big: binding-g6d-big
bindings:
  binding-0001:
    runtime:
      adapter: hermes
      profile: bristlecone
      platform: api_server
  binding-g6d-big:
    runtime:
      adapter: hermes
      profile: bristlecone-g6d-big
      platform: api_server
""",
            encoding="utf-8",
        )

        manager.model_binding_registry_file = (
            binding_file
        )

        yield manager, adapter


def send_turn(
    manager,
    *,
    task_id="task-g6d",
    context_id="ctx-g6d",
    reasoning_mode="normal",
    evidence=(),
    governor=None,
):
    kwargs = {}

    if governor is not None:
        kwargs.update(
            resource_governor=governor,
            resource_priority="standard",
            resource_request_source=(
                "g6d-integration-test"
            ),
            resource_request_reasons=(
                "retry_certification",
            ),
            resource_may_defer=True,
        )

    return manager.send_runtime_turn(
        "G.6D production retry turn",
        state=active_state(
            task_id
        ),
        instructions="G.6D integration test",
        reasoning_mode=reasoning_mode,
        persist=False,
        execution_context_id=context_id,
        automatic_model_form_evidence=(
            tuple(evidence)
        ),
        **kwargs,
    )


@contextmanager
def semantic_spies(
    manager,
):
    frozen_turns = []
    execution_frozen_turns = []

    original_reasoning = (
        reasoning.resolve_effective_reasoning
    )

    original_router = (
        routing_policy
        .recommend_automatic_model_form
    )

    original_prepare = (
        manager.prepare_model_form_turn
    )

    original_execution_state = (
        manager
        ._execution_state_for_model_form_turn
    )

    def capture_prepare(
        *args,
        **kwargs,
    ):
        frozen = original_prepare(
            *args,
            **kwargs,
        )

        frozen_turns.append(
            frozen
        )

        return frozen

    def capture_execution_state(
        state,
        frozen_turn,
    ):
        execution_frozen_turns.append(
            frozen_turn
        )

        return original_execution_state(
            state,
            frozen_turn,
        )

    with patch.object(
        reasoning,
        "resolve_effective_reasoning",
        wraps=original_reasoning,
    ) as reasoning_spy, patch.object(
        routing_policy,
        "recommend_automatic_model_form",
        wraps=original_router,
    ) as router_spy, patch.object(
        manager,
        "prepare_model_form_turn",
        side_effect=capture_prepare,
    ) as freeze_spy, patch.object(
        manager,
        "_execution_state_for_model_form_turn",
        side_effect=capture_execution_state,
    ):
        yield {
            "reasoning": reasoning_spy,
            "router": router_spy,
            "freeze": freeze_spy,
            "frozen_turns": frozen_turns,
            "execution_frozen_turns":
                execution_frozen_turns,
        }


class RealRetryFreezeTests(
    unittest.TestCase
):
    def test_stale_big_retry_routes_and_freezes_once(
        self,
    ):
        governor = RecordingGovernor()

        with manager_fixture(
            outcomes=(
                "stale",
                "ok",
            ),
            include_big=True,
        ) as (
            manager,
            adapter,
        ):
            with semantic_spies(
                manager
            ) as spies:
                result = send_turn(
                    manager,
                    reasoning_mode="deep",
                    evidence=high_complexity(),
                    governor=governor,
                )

            self.assertEqual(
                spies["reasoning"].call_count,
                1,
            )
            self.assertEqual(
                spies["router"].call_count,
                1,
            )
            self.assertEqual(
                spies["freeze"].call_count,
                1,
            )

            self.assertEqual(
                len(spies["frozen_turns"]),
                1,
            )

            frozen = spies[
                "frozen_turns"
            ][0]

            self.assertEqual(
                frozen.form,
                "big",
            )
            self.assertEqual(
                frozen.source,
                "auto_policy",
            )
            self.assertIn(
                "high_task_complexity",
                frozen.reasons,
            )

            self.assertGreaterEqual(
                len(
                    spies[
                        "execution_frozen_turns"
                    ]
                ),
                2,
            )

            for seen in spies[
                "execution_frozen_turns"
            ]:
                self.assertIs(
                    seen,
                    frozen,
                )

            self.assertEqual(
                len(governor.requests),
                1,
            )
            self.assertEqual(
                governor.requests[0].model_form,
                "big",
            )

            self.assertEqual(
                len(adapter.create_calls),
                2,
            )
            self.assertEqual(
                len(adapter.send_calls),
                2,
            )
            self.assertEqual(
                len(adapter.classifier_calls),
                1,
            )

            self.assertEqual(
                [
                    call["reasoning_mode"]
                    for call
                    in adapter.send_calls
                ],
                [
                    "deep",
                    "deep",
                ],
            )

            self.assertNotEqual(
                adapter.send_calls[0][
                    "session_id"
                ],
                adapter.send_calls[1][
                    "session_id"
                ],
            )

            self.assertIsInstance(
                result,
                dict,
            )

    def test_second_stale_escapes_without_reroute(
        self,
    ):
        with manager_fixture(
            outcomes=(
                "stale",
                "stale",
            ),
            include_big=True,
        ) as (
            manager,
            adapter,
        ):
            with semantic_spies(
                manager
            ) as spies:
                with self.assertRaises(
                    SyntheticStaleSessionError
                ):
                    send_turn(
                        manager,
                        evidence=high_complexity(),
                    )

            self.assertEqual(
                spies["reasoning"].call_count,
                1,
            )
            self.assertEqual(
                spies["router"].call_count,
                1,
            )
            self.assertEqual(
                spies["freeze"].call_count,
                1,
            )

            self.assertEqual(
                len(adapter.create_calls),
                2,
            )
            self.assertEqual(
                len(adapter.send_calls),
                2,
            )

            # The second stale error is not classified
            # into another recovery cycle.
            self.assertEqual(
                len(adapter.classifier_calls),
                1,
            )

    def test_retry_runtime_failure_does_not_reroute(
        self,
    ):
        with manager_fixture(
            outcomes=(
                "stale",
                "fail",
            ),
            include_big=True,
        ) as (
            manager,
            adapter,
        ):
            with semantic_spies(
                manager
            ) as spies:
                with self.assertRaises(
                    SyntheticRuntimeFailure
                ):
                    send_turn(
                        manager,
                        evidence=high_complexity(),
                    )

            self.assertEqual(
                spies["reasoning"].call_count,
                1,
            )
            self.assertEqual(
                spies["router"].call_count,
                1,
            )
            self.assertEqual(
                spies["freeze"].call_count,
                1,
            )
            self.assertEqual(
                len(adapter.create_calls),
                2,
            )
            self.assertEqual(
                len(adapter.send_calls),
                2,
            )


class RealIdentityIsolationTests(
    unittest.TestCase
):
    def test_wrong_task_recommendation_fails_before_freeze(
        self,
    ):
        forged = AutomaticModelFormRecommendation(
            task_id="task-WRONG",
            execution_context_id="ctx-g6d",
            form="big",
            reasons=(
                "forged_wrong_task",
            ),
        )

        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with patch.object(
                routing_policy,
                "recommend_automatic_model_form",
                return_value=forged,
            ) as router_spy, patch.object(
                manager,
                "prepare_model_form_turn",
                wraps=manager.prepare_model_form_turn,
            ) as freeze_spy:
                with self.assertRaises(
                    TaskSessionError
                ):
                    send_turn(
                        manager,
                        evidence=high_complexity(),
                    )

            self.assertEqual(
                router_spy.call_count,
                1,
            )
            self.assertEqual(
                freeze_spy.call_count,
                0,
            )
            self.assertEqual(
                len(adapter.create_calls),
                0,
            )
            self.assertEqual(
                len(adapter.send_calls),
                0,
            )

    def test_wrong_context_recommendation_fails_before_freeze(
        self,
    ):
        forged = AutomaticModelFormRecommendation(
            task_id="task-g6d",
            execution_context_id="ctx-WRONG",
            form="big",
            reasons=(
                "forged_wrong_context",
            ),
        )

        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with patch.object(
                routing_policy,
                "recommend_automatic_model_form",
                return_value=forged,
            ) as router_spy, patch.object(
                manager,
                "prepare_model_form_turn",
                wraps=manager.prepare_model_form_turn,
            ) as freeze_spy:
                with self.assertRaises(
                    TaskSessionError
                ):
                    send_turn(
                        manager,
                        evidence=high_complexity(),
                    )

            self.assertEqual(
                router_spy.call_count,
                1,
            )
            self.assertEqual(
                freeze_spy.call_count,
                0,
            )
            self.assertEqual(
                len(adapter.create_calls),
                0,
            )
            self.assertEqual(
                len(adapter.send_calls),
                0,
            )

    def test_separate_tasks_and_contexts_route_independently(
        self,
    ):
        original_router = (
            routing_policy
            .recommend_automatic_model_form
        )

        with manager_fixture(
            outcomes=(
                "ok",
                "ok",
            ),
            include_big=True,
        ) as (
            manager,
            adapter,
        ):
            with patch.object(
                routing_policy,
                "recommend_automatic_model_form",
                wraps=original_router,
            ) as router_spy:
                send_turn(
                    manager,
                    task_id="task-A",
                    context_id="ctx-A",
                    evidence=high_complexity(),
                )

                send_turn(
                    manager,
                    task_id="task-B",
                    context_id="ctx-B",
                    evidence=(),
                )

            self.assertEqual(
                router_spy.call_count,
                2,
            )

            input_a = (
                router_spy
                .call_args_list[0]
                .args[0]
            )

            input_b = (
                router_spy
                .call_args_list[1]
                .args[0]
            )

            self.assertEqual(
                (
                    input_a.task_id,
                    input_a.execution_context_id,
                ),
                (
                    "task-A",
                    "ctx-A",
                ),
            )

            self.assertEqual(
                (
                    input_b.task_id,
                    input_b.execution_context_id,
                ),
                (
                    "task-B",
                    "ctx-B",
                ),
            )

            self.assertIsNot(
                input_a,
                input_b,
            )

            self.assertEqual(
                len(adapter.send_calls),
                2,
            )


class RealReasoningFormIndependenceTests(
    unittest.TestCase
):
    def test_deep_without_escalation_evidence_freezes_small(
        self,
    ):
        with manager_fixture() as (
            manager,
            adapter,
        ):
            with semantic_spies(
                manager
            ) as spies:
                send_turn(
                    manager,
                    reasoning_mode="deep",
                    evidence=(),
                )

            frozen = spies[
                "frozen_turns"
            ][0]

            self.assertEqual(
                spies["reasoning"].call_count,
                1,
            )
            self.assertEqual(
                spies["router"].call_count,
                1,
            )
            self.assertEqual(
                frozen.form,
                "small",
            )

            self.assertEqual(
                adapter.send_calls[0][
                    "reasoning_mode"
                ],
                "deep",
            )

    def test_light_with_high_complexity_freezes_big(
        self,
    ):
        with manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with semantic_spies(
                manager
            ) as spies:
                send_turn(
                    manager,
                    reasoning_mode="light",
                    evidence=high_complexity(),
                )

            frozen = spies[
                "frozen_turns"
            ][0]

            self.assertEqual(
                spies["reasoning"].call_count,
                1,
            )
            self.assertEqual(
                spies["router"].call_count,
                1,
            )
            self.assertEqual(
                frozen.form,
                "big",
            )
            self.assertIn(
                "high_task_complexity",
                frozen.reasons,
            )

            self.assertEqual(
                adapter.send_calls[0][
                    "reasoning_mode"
                ],
                "light",
            )


if __name__ == "__main__":
    unittest.main()
