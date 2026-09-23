"""Phase 14.11G.6 synthetic retry/isolation certification.

This suite uses the production automatic Model Form routing
contracts, but deliberately does NOT reproduce or replace
runtime/task_session.py.

It proves the semantic invariants required around retry:

- one meaningful turn routes at most once;
- stale-session recovery reuses the same frozen semantic turn;
- retry never changes Model Form, reasons, or Reasoning;
- retry failure does not reroute;
- Task/context-local recommendations cannot cross identities;
- Reasoning mode does not mechanically select Model Form.
"""

from dataclasses import dataclass
import unittest

from reasoning.control import (
    EffectiveReasoningDecision,
)

from model_form.automatic_routing import (
    AutomaticModelFormRecommendation,
)

from model_form.automatic_routing_evidence import (
    AutomaticModelFormEvidence,
    AutomaticModelFormRoutingInput,
)

from model_form.automatic_routing_policy import (
    recommend_automatic_model_form,
)


class SyntheticRoutingBoundaryError(RuntimeError):
    """Synthetic fail-closed routing boundary error."""


class SyntheticStaleSessionError(RuntimeError):
    """Synthetic runtime stale-session signal."""


class SyntheticRuntimeFailure(RuntimeError):
    """Synthetic non-recoverable runtime failure."""


@dataclass(
    frozen=True,
    slots=True,
)
class SyntheticFrozenTurn:
    """Minimal immutable semantic state reused across retry."""

    task_id: str
    execution_context_id: str
    form: str
    reasons: tuple[str, ...]
    reasoning_decision: EffectiveReasoningDecision


class CountingProductionRouter:
    """Count calls to the real production routing policy."""

    def __init__(self):
        self.call_count = 0

    def route(
        self,
        routing_input,
    ):
        self.call_count += 1

        return recommend_automatic_model_form(
            routing_input
        )


class SyntheticRuntime:
    """Runtime stub that records exact frozen-turn identity."""

    def __init__(
        self,
        outcomes,
    ):
        self.outcomes = list(outcomes)
        self.send_count = 0
        self.seen_turns = []
        self.replacement_count = 0

    def replace_stale_session(
        self,
    ):
        self.replacement_count += 1

    def send_turn(
        self,
        frozen_turn,
    ):
        self.send_count += 1
        self.seen_turns.append(
            frozen_turn
        )

        if not self.outcomes:
            return "ok"

        outcome = self.outcomes.pop(0)

        if outcome == "ok":
            return "ok"

        if outcome == "stale":
            raise SyntheticStaleSessionError(
                "synthetic stale session"
            )

        if outcome == "fail":
            raise SyntheticRuntimeFailure(
                "synthetic runtime failure"
            )

        raise AssertionError(
            f"Unknown synthetic outcome: {outcome!r}"
        )


def reasoning(
    mode="normal",
):
    return EffectiveReasoningDecision(
        mode=mode,
        source="automatic",
    )


def evidence(
    signal,
    value,
):
    return AutomaticModelFormEvidence(
        signal=signal,
        value=value,
        producer="g6-synthetic-test",
    )


def routing_input(
    *,
    task_id="task-A",
    execution_context_id="ctx-A",
    reasoning_mode="normal",
    evidence_items=(),
):
    return AutomaticModelFormRoutingInput(
        task_id=task_id,
        execution_context_id=
            execution_context_id,
        reasoning_decision=reasoning(
            reasoning_mode
        ),
        evidence=tuple(
            evidence_items
        ),
    )


def freeze_recommendation(
    routing_input_value,
    recommendation,
):
    """Freeze only if recommendation identity matches input."""

    if not isinstance(
        recommendation,
        AutomaticModelFormRecommendation,
    ):
        raise SyntheticRoutingBoundaryError(
            "Recommendation has wrong type."
        )

    if (
        recommendation.task_id
        != routing_input_value.task_id
    ):
        raise SyntheticRoutingBoundaryError(
            "Recommendation belongs to another Task."
        )

    if (
        recommendation.execution_context_id
        != routing_input_value.execution_context_id
    ):
        raise SyntheticRoutingBoundaryError(
            "Recommendation belongs to another "
            "execution context."
        )

    return SyntheticFrozenTurn(
        task_id=routing_input_value.task_id,
        execution_context_id=(
            routing_input_value.execution_context_id
        ),
        form=recommendation.form,
        reasons=recommendation.reasons,
        reasoning_decision=(
            routing_input_value.reasoning_decision
        ),
    )


def execute_synthetic_turn(
    *,
    router,
    routing_input_value,
    runtime,
):
    """Route once, freeze once, then permit one stale retry."""

    recommendation = router.route(
        routing_input_value
    )

    frozen_turn = freeze_recommendation(
        routing_input_value,
        recommendation,
    )

    try:
        result = runtime.send_turn(
            frozen_turn
        )

    except SyntheticStaleSessionError:
        runtime.replace_stale_session()

        # Deliberately reuse the exact same frozen object.
        # A second stale failure or any other failure escapes.
        result = runtime.send_turn(
            frozen_turn
        )

    return (
        recommendation,
        frozen_turn,
        result,
    )


class ProductionRoutingPolicyTests(
    unittest.TestCase
):
    def test_no_evidence_deep_still_small(
        self,
    ):
        router = CountingProductionRouter()

        recommendation = router.route(
            routing_input(
                reasoning_mode="deep"
            )
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            recommendation.form,
            "small",
        )
        self.assertEqual(
            recommendation.reasons,
            (
                "no_big_escalation_evidence",
            ),
        )

    def test_high_complexity_light_is_big(
        self,
    ):
        recommendation = (
            recommend_automatic_model_form(
                routing_input(
                    reasoning_mode="light",
                    evidence_items=(
                        evidence(
                            "task_complexity",
                            "high",
                        ),
                    ),
                )
            )
        )

        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertIn(
            "high_task_complexity",
            recommendation.reasons,
        )

    def test_known_small_failure_is_big(
        self,
    ):
        recommendation = (
            recommend_automatic_model_form(
                routing_input(
                    evidence_items=(
                        evidence(
                            "known_small_failure",
                            "present",
                        ),
                    ),
                )
            )
        )

        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertIn(
            "known_small_failure",
            recommendation.reasons,
        )

    def test_small_capability_insufficient_is_big(
        self,
    ):
        recommendation = (
            recommend_automatic_model_form(
                routing_input(
                    evidence_items=(
                        evidence(
                            "small_capability_suitability",
                            "insufficient",
                        ),
                    ),
                )
            )
        )

        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertIn(
            "small_capability_insufficient",
            recommendation.reasons,
        )

    def test_multiple_reasons_have_stable_order(
        self,
    ):
        recommendation = (
            recommend_automatic_model_form(
                routing_input(
                    evidence_items=(
                        evidence(
                            "small_capability_suitability",
                            "insufficient",
                        ),
                        evidence(
                            "known_small_failure",
                            "present",
                        ),
                        evidence(
                            "task_complexity",
                            "high",
                        ),
                    ),
                )
            )
        )

        self.assertEqual(
            recommendation.reasons,
            (
                "high_task_complexity",
                "known_small_failure",
                "small_capability_insufficient",
            ),
        )


class RetryFreezeTests(
    unittest.TestCase
):
    def test_normal_send_routes_once(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            ("ok",)
        )

        recommendation, frozen, result = (
            execute_synthetic_turn(
                router=router,
                routing_input_value=routing_input(
                    evidence_items=(
                        evidence(
                            "task_complexity",
                            "high",
                        ),
                    ),
                ),
                runtime=runtime,
            )
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            runtime.send_count,
            1,
        )
        self.assertEqual(
            runtime.replacement_count,
            0,
        )
        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertEqual(
            frozen.form,
            "big",
        )
        self.assertEqual(
            result,
            "ok",
        )

    def test_stale_retry_routes_once(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            (
                "stale",
                "ok",
            )
        )

        recommendation, frozen, result = (
            execute_synthetic_turn(
                router=router,
                routing_input_value=routing_input(
                    reasoning_mode="deep",
                    evidence_items=(
                        evidence(
                            "known_small_failure",
                            "present",
                        ),
                    ),
                ),
                runtime=runtime,
            )
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            runtime.send_count,
            2,
        )
        self.assertEqual(
            runtime.replacement_count,
            1,
        )

        self.assertIs(
            runtime.seen_turns[0],
            frozen,
        )
        self.assertIs(
            runtime.seen_turns[1],
            frozen,
        )
        self.assertIs(
            runtime.seen_turns[0],
            runtime.seen_turns[1],
        )

        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertEqual(
            frozen.form,
            "big",
        )
        self.assertEqual(
            result,
            "ok",
        )

    def test_stale_retry_preserves_reasoning_identity(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            (
                "stale",
                "ok",
            )
        )

        input_value = routing_input(
            reasoning_mode="deep",
            evidence_items=(
                evidence(
                    "task_complexity",
                    "high",
                ),
            ),
        )

        _, frozen, _ = (
            execute_synthetic_turn(
                router=router,
                routing_input_value=input_value,
                runtime=runtime,
            )
        )

        self.assertIs(
            frozen.reasoning_decision,
            input_value.reasoning_decision,
        )

        self.assertIs(
            runtime.seen_turns[0].reasoning_decision,
            input_value.reasoning_decision,
        )

        self.assertIs(
            runtime.seen_turns[1].reasoning_decision,
            input_value.reasoning_decision,
        )

        self.assertEqual(
            router.call_count,
            1,
        )

    def test_stale_retry_preserves_form_and_reasons(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            (
                "stale",
                "ok",
            )
        )

        recommendation, frozen, _ = (
            execute_synthetic_turn(
                router=router,
                routing_input_value=routing_input(
                    evidence_items=(
                        evidence(
                            "task_complexity",
                            "high",
                        ),
                        evidence(
                            "known_small_failure",
                            "present",
                        ),
                    ),
                ),
                runtime=runtime,
            )
        )

        self.assertEqual(
            frozen.form,
            recommendation.form,
        )
        self.assertEqual(
            frozen.reasons,
            recommendation.reasons,
        )

        for seen in runtime.seen_turns:
            self.assertEqual(
                seen.form,
                recommendation.form,
            )
            self.assertEqual(
                seen.reasons,
                recommendation.reasons,
            )

        self.assertEqual(
            router.call_count,
            1,
        )

    def test_retry_runtime_failure_does_not_reroute(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            (
                "stale",
                "fail",
            )
        )

        with self.assertRaises(
            SyntheticRuntimeFailure
        ):
            execute_synthetic_turn(
                router=router,
                routing_input_value=routing_input(
                    evidence_items=(
                        evidence(
                            "task_complexity",
                            "high",
                        ),
                    ),
                ),
                runtime=runtime,
            )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            runtime.send_count,
            2,
        )
        self.assertEqual(
            runtime.replacement_count,
            1,
        )

    def test_second_stale_failure_does_not_reroute(
        self,
    ):
        router = CountingProductionRouter()
        runtime = SyntheticRuntime(
            (
                "stale",
                "stale",
            )
        )

        with self.assertRaises(
            SyntheticStaleSessionError
        ):
            execute_synthetic_turn(
                router=router,
                routing_input_value=routing_input(
                    evidence_items=(
                        evidence(
                            "known_small_failure",
                            "present",
                        ),
                    ),
                ),
                runtime=runtime,
            )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            runtime.send_count,
            2,
        )
        self.assertEqual(
            runtime.replacement_count,
            1,
        )


class TaskContextIsolationTests(
    unittest.TestCase
):
    def test_router_copies_task_identity(
        self,
    ):
        input_value = routing_input(
            task_id="task-A",
            execution_context_id="ctx-A",
        )

        recommendation = (
            recommend_automatic_model_form(
                input_value
            )
        )

        self.assertEqual(
            recommendation.task_id,
            "task-A",
        )
        self.assertEqual(
            recommendation.execution_context_id,
            "ctx-A",
        )

    def test_task_mismatch_fails_closed(
        self,
    ):
        input_value = routing_input(
            task_id="task-B",
            execution_context_id="ctx-A",
        )

        forged = AutomaticModelFormRecommendation(
            task_id="task-A",
            execution_context_id="ctx-A",
            form="big",
            reasons=(
                "synthetic_wrong_task",
            ),
        )

        with self.assertRaises(
            SyntheticRoutingBoundaryError
        ):
            freeze_recommendation(
                input_value,
                forged,
            )

    def test_context_mismatch_fails_closed(
        self,
    ):
        input_value = routing_input(
            task_id="task-A",
            execution_context_id="ctx-B",
        )

        forged = AutomaticModelFormRecommendation(
            task_id="task-A",
            execution_context_id="ctx-A",
            form="big",
            reasons=(
                "synthetic_wrong_context",
            ),
        )

        with self.assertRaises(
            SyntheticRoutingBoundaryError
        ):
            freeze_recommendation(
                input_value,
                forged,
            )

    def test_contexts_route_independently(
        self,
    ):
        router = CountingProductionRouter()

        rec_a = router.route(
            routing_input(
                task_id="task-A",
                execution_context_id="ctx-A",
                evidence_items=(
                    evidence(
                        "task_complexity",
                        "high",
                    ),
                ),
            )
        )

        rec_b = router.route(
            routing_input(
                task_id="task-B",
                execution_context_id="ctx-B",
            )
        )

        self.assertEqual(
            router.call_count,
            2,
        )

        self.assertEqual(
            rec_a.task_id,
            "task-A",
        )
        self.assertEqual(
            rec_a.execution_context_id,
            "ctx-A",
        )
        self.assertEqual(
            rec_a.form,
            "big",
        )

        self.assertEqual(
            rec_b.task_id,
            "task-B",
        )
        self.assertEqual(
            rec_b.execution_context_id,
            "ctx-B",
        )
        self.assertEqual(
            rec_b.form,
            "small",
        )


if __name__ == "__main__":
    unittest.main()
