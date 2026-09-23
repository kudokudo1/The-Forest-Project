"""Synthetic Phase 14.11G.5 router / Governor contract tests.

This file intentionally does NOT model or replace the production
runtime/task_session.py integration.

It proves only the semantic boundary:

Router:
    decides which Model Form would be useful.

Governor:
    decides whether the exact frozen semantic request may proceed.

A Governor defer/deny must never silently become a new Small request.
"""

import unittest

from model_form.automatic_router import (
    AutomaticModelFormSignals,
    DeterministicAutomaticModelFormRouter,
)
from resources import (
    GovernorDecision,
    ResourceRequest,
)


class SyntheticGovernorContractError(RuntimeError):
    """Synthetic harness fail-closed error."""


class CountingRouter:
    """Count pure-router calls without changing its behavior."""

    def __init__(self):
        self._router = (
            DeterministicAutomaticModelFormRouter()
        )
        self.call_count = 0

    def route(self, signals):
        self.call_count += 1
        return self._router.route(signals)


def make_request(
    recommendation,
    signals,
):
    """Build one exact synthetic ResourceRequest."""

    return ResourceRequest(
        task_id=(
            signals.task_id
            or "task-synthetic"
        ),
        execution_context_id=(
            signals.execution_context_id
        ),
        model_form=recommendation.form,
        reasoning_mode=signals.reasoning_mode,
        priority="standard",
        source="g5-synthetic-router",
        reasons=recommendation.reasons,
        may_defer=True,
    )


def synthetic_governed_turn(
    *,
    router,
    signals,
    governor,
):
    """Model only the G/F semantic boundary.

    This is deliberately NOT production integration code.
    """

    recommendation = router.route(
        signals
    )

    request = make_request(
        recommendation,
        signals,
    )

    try:
        decision = governor(
            request
        )

    except Exception as exc:
        raise SyntheticGovernorContractError(
            "Synthetic Governor failed closed."
        ) from exc

    if not isinstance(
        decision,
        GovernorDecision,
    ):
        raise SyntheticGovernorContractError(
            "Governor must return GovernorDecision."
        )

    if decision.request is not request:
        raise SyntheticGovernorContractError(
            "GovernorDecision must belong to "
            "the exact ResourceRequest."
        )

    if decision.outcome == "approve":
        action = "proceed"

    elif decision.outcome in {
        "defer",
        "deny",
    }:
        action = "stop"

    else:
        # GovernorDecision currently prevents this,
        # but the harness remains explicitly closed.
        raise SyntheticGovernorContractError(
            "Unsupported Governor outcome."
        )

    return {
        "recommendation": recommendation,
        "request": request,
        "decision": decision,
        "action": action,
    }


def decision_governor(
    outcome,
):
    """Return a Governor over the exact supplied request."""

    def governor(request):
        return GovernorDecision(
            request=request,
            outcome=outcome,
            source="g5-synthetic-governor",
            reasons=(
                f"synthetic_{outcome}",
            ),
        )

    return governor


class GovernorRouterInteractionTests(
    unittest.TestCase
):
    def test_small_approve_proceeds_as_small(
        self,
    ):
        router = CountingRouter()

        result = synthetic_governed_turn(
            router=router,
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-small",
                task_id="task-small",
                message="Summarize this short note.",
                reasoning_mode="light",
            ),
            governor=decision_governor(
                "approve"
            ),
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            result["recommendation"].form,
            "small",
        )
        self.assertEqual(
            result["request"].model_form,
            "small",
        )
        self.assertEqual(
            result["decision"].outcome,
            "approve",
        )
        self.assertEqual(
            result["action"],
            "proceed",
        )

    def test_big_approve_proceeds_as_big(
        self,
    ):
        router = CountingRouter()

        result = synthetic_governed_turn(
            router=router,
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-big",
                task_id="task-big",
                message=(
                    "Design the architecture for "
                    "this multi-module subsystem."
                ),
                reasoning_mode="light",
            ),
            governor=decision_governor(
                "approve"
            ),
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            result["request"].model_form,
            "big",
        )
        self.assertEqual(
            result["action"],
            "proceed",
        )

    def test_big_defer_stops_without_downgrade(
        self,
    ):
        router = CountingRouter()

        result = synthetic_governed_turn(
            router=router,
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-defer",
                task_id="task-defer",
                message=(
                    "Find the root cause of "
                    "this race condition."
                ),
                reasoning_mode="deep",
            ),
            governor=decision_governor(
                "defer"
            ),
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            result["recommendation"].form,
            "big",
        )
        self.assertEqual(
            result["request"].model_form,
            "big",
        )
        self.assertEqual(
            result["decision"].outcome,
            "defer",
        )
        self.assertEqual(
            result["action"],
            "stop",
        )

    def test_big_deny_stops_without_downgrade(
        self,
    ):
        router = CountingRouter()

        result = synthetic_governed_turn(
            router=router,
            signals=AutomaticModelFormSignals(
                execution_context_id="ctx-deny",
                task_id="task-deny",
                message=(
                    "Design the architecture "
                    "for this subsystem."
                ),
                reasoning_mode="normal",
            ),
            governor=decision_governor(
                "deny"
            ),
        )

        self.assertEqual(
            router.call_count,
            1,
        )
        self.assertEqual(
            result["request"].model_form,
            "big",
        )
        self.assertEqual(
            result["decision"].outcome,
            "deny",
        )
        self.assertEqual(
            result["action"],
            "stop",
        )

    def test_governor_cannot_replace_big_with_small(
        self,
    ):
        router = CountingRouter()

        def replacement_governor(
            request,
        ):
            replacement = ResourceRequest(
                task_id=request.task_id,
                execution_context_id=(
                    request.execution_context_id
                ),
                model_form="small",
                reasoning_mode=(
                    request.reasoning_mode
                ),
                priority=request.priority,
                source="illegal-replacement",
                reasons=(
                    "silent_downgrade",
                ),
                may_defer=request.may_defer,
            )

            return GovernorDecision(
                request=replacement,
                outcome="approve",
                source="bad-governor",
                reasons=(
                    "replacement_request",
                ),
            )

        with self.assertRaises(
            SyntheticGovernorContractError
        ):
            synthetic_governed_turn(
                router=router,
                signals=AutomaticModelFormSignals(
                    execution_context_id=(
                        "ctx-replacement"
                    ),
                    task_id="task-replacement",
                    message=(
                        "Design the architecture "
                        "for this subsystem."
                    ),
                    reasoning_mode="deep",
                ),
                governor=replacement_governor,
            )

        self.assertEqual(
            router.call_count,
            1,
        )

    def test_malformed_governor_return_fails_closed(
        self,
    ):
        router = CountingRouter()

        def malformed_governor(
            request,
        ):
            return {
                "outcome": "approve",
                "request": request,
            }

        with self.assertRaises(
            SyntheticGovernorContractError
        ):
            synthetic_governed_turn(
                router=router,
                signals=AutomaticModelFormSignals(
                    execution_context_id=(
                        "ctx-malformed"
                    ),
                    task_id="task-malformed",
                    message="Routine request.",
                    reasoning_mode="normal",
                ),
                governor=malformed_governor,
            )

        self.assertEqual(
            router.call_count,
            1,
        )

    def test_governor_exception_fails_closed_without_reroute(
        self,
    ):
        router = CountingRouter()

        def exploding_governor(
            request,
        ):
            raise RuntimeError(
                "synthetic Governor failure"
            )

        with self.assertRaises(
            SyntheticGovernorContractError
        ):
            synthetic_governed_turn(
                router=router,
                signals=AutomaticModelFormSignals(
                    execution_context_id=(
                        "ctx-exception"
                    ),
                    task_id="task-exception",
                    message=(
                        "Find the root cause "
                        "of this deadlock."
                    ),
                    reasoning_mode="deep",
                ),
                governor=exploding_governor,
            )

        # Failure must not trigger another routing pass.
        self.assertEqual(
            router.call_count,
            1,
        )

    def test_request_preserves_semantic_provenance(
        self,
    ):
        router = CountingRouter()

        signals = AutomaticModelFormSignals(
            execution_context_id="ctx-provenance",
            task_id="task-provenance",
            message=(
                "Review the architecture and root cause "
                "of this race condition."
            ),
            reasoning_mode="light",
            known_small_failure=True,
        )

        result = synthetic_governed_turn(
            router=router,
            signals=signals,
            governor=decision_governor(
                "approve"
            ),
        )

        recommendation = result[
            "recommendation"
        ]
        request = result[
            "request"
        ]

        self.assertEqual(
            request.execution_context_id,
            signals.execution_context_id,
        )
        self.assertEqual(
            request.task_id,
            signals.task_id,
        )
        self.assertEqual(
            request.model_form,
            recommendation.form,
        )
        self.assertEqual(
            request.reasoning_mode,
            signals.reasoning_mode,
        )
        self.assertEqual(
            request.reasons,
            recommendation.reasons,
        )
        self.assertIs(
            result["decision"].request,
            request,
        )


if __name__ == "__main__":
    unittest.main()
