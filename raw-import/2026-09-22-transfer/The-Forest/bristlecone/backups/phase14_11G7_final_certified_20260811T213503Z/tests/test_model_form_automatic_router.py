"""Regression tests for Phase 14.11G automatic Model Form routing."""

import unittest

from model_form.automatic_router import (
    AutomaticModelFormRecommendation,
    AutomaticModelFormRoutingError,
    AutomaticModelFormSignals,
    DeterministicAutomaticModelFormRouter,
)
from model_form.control import (
    default_model_form_control,
    set_pinned_baseline,
    set_task_override,
)
from model_form.registry import (
    ModelBinding,
    ModelBindingRegistry,
)
from model_form.resolution import (
    resolve_model_form_turn,
)


def synthetic_registry():
    return ModelBindingRegistry(
        form_bindings={
            "small": "binding-small",
            "big": "binding-big",
        },
        bindings={
            "binding-small": ModelBinding(
                binding_id="binding-small",
                runtime={
                    "adapter": "synthetic-small",
                },
            ),
            "binding-big": ModelBinding(
                binding_id="binding-big",
                runtime={
                    "adapter": "synthetic-big",
                },
            ),
        },
    )


def auto_is_eligible(
    control,
    *,
    task_id=None,
    exact_form=None,
):
    """Contract proven against resolver precedence in G.2C."""

    if exact_form is not None:
        return False

    override = control.task_override

    if (
        override is not None
        and override.task_id == task_id
    ):
        return False

    if control.baseline.policy == "pinned":
        return False

    return True


class AutomaticModelFormContractTests(
    unittest.TestCase
):
    def test_valid_signals(self):
        signals = AutomaticModelFormSignals(
            execution_context_id="ctx-a",
            task_id="task-1",
            message="Investigate this problem.",
            reasoning_mode="deep",
            current_form="small",
            workshop_id="debugging",
            general_capability_ids=("todo",),
            ready_capability_ids=(
                "debugging",
                "testing",
            ),
        )

        self.assertEqual(
            signals.execution_context_id,
            "ctx-a",
        )

    def test_valid_recommendation(self):
        result = AutomaticModelFormRecommendation(
            execution_context_id="ctx-a",
            form="big",
            reasons=("complex_debugging_demand",),
        )

        self.assertEqual(
            result.form,
            "big",
        )

    def test_empty_context_rejected(self):
        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            AutomaticModelFormSignals(
                execution_context_id="",
                message="hello",
                reasoning_mode="normal",
            )

    def test_auto_current_form_rejected(self):
        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            AutomaticModelFormSignals(
                execution_context_id="ctx-a",
                message="hello",
                reasoning_mode="normal",
                current_form="auto",
            )

    def test_duplicate_capabilities_rejected(self):
        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            AutomaticModelFormSignals(
                execution_context_id="ctx-a",
                message="hello",
                reasoning_mode="normal",
                ready_capability_ids=(
                    "debugging",
                    "debugging",
                ),
            )

    def test_auto_recommendation_rejected(self):
        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            AutomaticModelFormRecommendation(
                execution_context_id="ctx-a",
                form="auto",
                reasons=("invalid",),
            )

    def test_empty_recommendation_reasons_rejected(
        self,
    ):
        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            AutomaticModelFormRecommendation(
                execution_context_id="ctx-a",
                form="small",
                reasons=(),
            )


class DeterministicRouterTests(
    unittest.TestCase
):
    def setUp(self):
        self.router = (
            DeterministicAutomaticModelFormRouter()
        )

    def route(
        self,
        *,
        execution_context_id="ctx-a",
        message="Handle this routine request.",
        reasoning_mode="normal",
        **kwargs,
    ):
        return self.router.route(
            AutomaticModelFormSignals(
                execution_context_id=(
                    execution_context_id
                ),
                message=message,
                reasoning_mode=reasoning_mode,
                **kwargs,
            )
        )

    def test_routine_light_stays_small(self):
        result = self.route(
            reasoning_mode="light"
        )

        self.assertEqual(
            result.form,
            "small",
        )

    def test_routine_deep_may_stay_small(self):
        result = self.route(
            reasoning_mode="deep"
        )

        self.assertEqual(
            result.form,
            "small",
        )

    def test_architecture_escalates_big(self):
        result = self.route(
            message=(
                "Design the architecture "
                "for this subsystem."
            ),
            reasoning_mode="light",
        )

        self.assertEqual(
            result.form,
            "big",
        )

        self.assertEqual(
            result.reasons,
            (
                "architecture_or_cross_module_demand",
            ),
        )

    def test_complex_debugging_escalates_big(self):
        result = self.route(
            message=(
                "Find the root cause "
                "of this race condition."
            )
        )

        self.assertEqual(
            result.form,
            "big",
        )

        self.assertEqual(
            result.reasons,
            (
                "complex_debugging_demand",
            ),
        )

    def test_known_small_failure_escalates_big(
        self,
    ):
        result = self.route(
            known_small_failure=True
        )

        self.assertEqual(
            result.form,
            "big",
        )

    def test_broad_capability_demand_escalates_big(
        self,
    ):
        result = self.route(
            general_capability_ids=(
                "memory",
                "todo",
            ),
            ready_capability_ids=(
                "debugging",
                "testing",
            ),
        )

        self.assertEqual(
            result.form,
            "big",
        )

    def test_three_capabilities_remain_small(self):
        result = self.route(
            general_capability_ids=(
                "memory",
            ),
            ready_capability_ids=(
                "debugging",
                "testing",
            ),
        )

        self.assertEqual(
            result.form,
            "small",
        )

    def test_current_form_is_not_a_pin(self):
        small_to_big = self.route(
            current_form="small",
            message="Investigate this concurrency bug.",
        )

        big_to_small = self.route(
            current_form="big",
            message="Summarize this short note.",
        )

        self.assertEqual(
            small_to_big.form,
            "big",
        )

        self.assertEqual(
            big_to_small.form,
            "small",
        )

    def test_combined_reasons_have_stable_order(
        self,
    ):
        result = self.route(
            message=(
                "Review the architecture and root cause "
                "of this race condition."
            ),
            known_small_failure=True,
            general_capability_ids=(
                "memory",
                "todo",
            ),
            ready_capability_ids=(
                "debugging",
                "testing",
            ),
        )

        self.assertEqual(
            result.reasons,
            (
                "known_small_failure",
                "architecture_or_cross_module_demand",
                "complex_debugging_demand",
                "broad_capability_demand",
            ),
        )

    def test_identical_input_is_deterministic(self):
        signals = AutomaticModelFormSignals(
            execution_context_id="ctx-replay",
            message=(
                "Find the root cause "
                "of this deadlock."
            ),
            reasoning_mode="deep",
        )

        self.assertEqual(
            self.router.route(signals),
            self.router.route(signals),
        )


class RouterResolverSeamTests(
    unittest.TestCase
):
    def setUp(self):
        self.router = (
            DeterministicAutomaticModelFormRouter()
        )
        self.registry = synthetic_registry()

    def handoff(
        self,
        *,
        control,
        task_id,
        signals,
        exact_form=None,
    ):
        recommendation = self.router.route(
            signals
        )

        if (
            recommendation.execution_context_id
            != control.execution_context_id
        ):
            raise AutomaticModelFormRoutingError(
                "Automatic recommendation execution "
                "context does not match "
                "Model Form control."
            )

        frozen = resolve_model_form_turn(
            control,
            self.registry,
            task_id=task_id,
            exact_form=exact_form,
            automatic_form=recommendation.form,
        )

        return recommendation, frozen

    def test_routine_auto_freezes_small(self):
        control = default_model_form_control(
            execution_context_id="ctx-a"
        )

        recommendation, frozen = self.handoff(
            control=control,
            task_id="task-routine",
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-a",
                task_id="task-routine",
                message="Summarize this short note.",
                reasoning_mode="deep",
            ),
        )

        self.assertEqual(
            recommendation.form,
            "small",
        )
        self.assertEqual(
            frozen.form,
            "small",
        )
        self.assertEqual(
            frozen.binding_id,
            "binding-small",
        )
        self.assertEqual(
            frozen.decision.source,
            "auto_policy",
        )

        # Current resolver does not yet preserve
        # detailed automatic-router reasons.
        self.assertEqual(
            frozen.decision.reasons,
            ("automatic_form_supplied",),
        )

    def test_semantic_escalation_freezes_big(self):
        control = default_model_form_control(
            execution_context_id="ctx-b"
        )

        recommendation, frozen = self.handoff(
            control=control,
            task_id="task-architecture",
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-b",
                task_id="task-architecture",
                message=(
                    "Design the architecture for this "
                    "multi-module subsystem."
                ),
                reasoning_mode="light",
            ),
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
            frozen.binding_id,
            "binding-big",
        )

    def test_exact_small_beats_automatic_big(self):
        control = default_model_form_control(
            execution_context_id="ctx-b"
        )

        recommendation, frozen = self.handoff(
            control=control,
            task_id="task-explicit",
            exact_form="small",
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-b",
                task_id="task-explicit",
                message=(
                    "Design the architecture for this "
                    "multi-module subsystem."
                ),
                reasoning_mode="deep",
            ),
        )

        self.assertEqual(
            recommendation.form,
            "big",
        )
        self.assertEqual(
            frozen.form,
            "small",
        )
        self.assertEqual(
            frozen.decision.source,
            "exact_turn",
        )

    def test_context_mismatch_fails_before_resolver(
        self,
    ):
        control = default_model_form_control(
            execution_context_id="ctx-a"
        )

        with self.assertRaises(
            AutomaticModelFormRoutingError
        ):
            self.handoff(
                control=control,
                task_id="task-mismatch",
                signals=AutomaticModelFormSignals(
                    execution_context_id="ctx-WRONG",
                    task_id="task-mismatch",
                    message="Design the architecture.",
                    reasoning_mode="normal",
                ),
            )


class AutoEligibilityContractTests(
    unittest.TestCase
):
    def test_truth_table_matches_resolver_precedence(
        self,
    ):
        registry = synthetic_registry()

        auto_control = default_model_form_control(
            execution_context_id="ctx"
        )

        task_control = set_task_override(
            auto_control,
            "task-a",
            "small",
        )

        pinned_control = set_pinned_baseline(
            auto_control,
            "small",
        )

        cases = (
            (
                "plain Auto",
                auto_control,
                "task-a",
                None,
                True,
                "auto_policy",
            ),
            (
                "exact Small",
                auto_control,
                "task-a",
                "small",
                False,
                "exact_turn",
            ),
            (
                "matching Task override",
                task_control,
                "task-a",
                None,
                False,
                "task_override",
            ),
            (
                "mismatched Task override",
                task_control,
                "task-b",
                None,
                True,
                "auto_policy",
            ),
            (
                "pinned Small",
                pinned_control,
                "task-a",
                None,
                False,
                "pinned_baseline",
            ),
        )

        for (
            name,
            control,
            task_id,
            exact_form,
            expected_eligible,
            expected_source,
        ) in cases:
            with self.subTest(name=name):
                eligible = auto_is_eligible(
                    control,
                    task_id=task_id,
                    exact_form=exact_form,
                )

                frozen = resolve_model_form_turn(
                    control,
                    registry,
                    task_id=task_id,
                    exact_form=exact_form,
                    automatic_form="big",
                )

                self.assertEqual(
                    eligible,
                    expected_eligible,
                )

                self.assertEqual(
                    frozen.decision.source,
                    expected_source,
                )

                self.assertEqual(
                    (
                        frozen.decision.source
                        == "auto_policy"
                    ),
                    eligible,
                )


if __name__ == "__main__":
    unittest.main()
