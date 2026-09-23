"""14.11K.5A — frozen Big semantic turn survives resource governance."""

import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent

BASE_TEST = (
    HERE
    / "test_model_form_governor_task_session_integration.py"
)

spec = importlib.util.spec_from_file_location(
    "forest_g5d_integration",
    BASE_TEST,
)

g5d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g5d)


def send_k5_big(
    manager,
    *,
    governor,
    outcome_label,
):
    return manager.send_runtime_turn(
        f"K.5 frozen Big semantic turn ({outcome_label})",
        state=g5d.active_state(
            "task-k5"
        ),
        instructions=(
            "K.5 frozen semantic turn certification"
        ),
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-k5",
        model_form="big",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "k5-frozen-semantic-test"
        ),
        resource_request_reasons=(
            "frozen_big_semantics",
            "no_semantic_rewrite",
        ),
        resource_may_defer=True,
    )


class FrozenBigSemanticTurnTests(
    unittest.TestCase
):
    def assert_frozen_request(
        self,
        governor,
    ):
        self.assertEqual(
            len(governor.requests),
            1,
        )

        request = governor.requests[0]

        # Task identity survives unchanged.
        self.assertEqual(
            request.task_id,
            "task-k5",
        )

        # Execution-context identity survives unchanged.
        self.assertEqual(
            request.execution_context_id,
            "ctx-k5",
        )

        # Explicit Big survives unchanged.
        self.assertEqual(
            request.model_form,
            "big",
        )

        self.assertNotEqual(
            request.model_form,
            "small",
        )

        # Reasoning is an independent axis and
        # survives unchanged.
        self.assertEqual(
            request.reasoning_mode,
            "normal",
        )

        # Resource metadata is also exact.
        self.assertEqual(
            request.priority,
            "standard",
        )

        self.assertEqual(
            request.source,
            "k5-frozen-semantic-test",
        )

        self.assertEqual(
            request.reasons,
            (
                "frozen_big_semantics",
                "no_semantic_rewrite",
            ),
        )

        self.assertTrue(
            request.may_defer,
        )

        return request

    def assert_no_runtime(
        self,
        adapter,
    ):
        self.assertEqual(
            g5d.runtime_side_effect_count(
                adapter
            ),
            0,
        )

        self.assertEqual(
            adapter.create_calls,
            [],
        )

        self.assertEqual(
            adapter.send_calls,
            [],
        )

        self.assertEqual(
            adapter.end_calls,
            [],
        )

    def test_k5_big_semantics_survive_defer_unchanged(
        self,
    ):
        governor = g5d.RecordingGovernor(
            "defer"
        )

        # Temporary test-only Big binding.
        with g5d.manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                g5d.TaskSessionError
            ) as caught:
                send_k5_big(
                    manager,
                    governor=governor,
                    outcome_label="defer",
                )

            request = self.assert_frozen_request(
                governor
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

            # Exact ResourceRequest object survives
            # into the GovernorDecision.
            self.assertIs(
                decision.request,
                request,
            )

            self.assert_no_runtime(
                adapter
            )

    def test_k5_big_semantics_survive_deny_unchanged(
        self,
    ):
        governor = g5d.RecordingGovernor(
            "deny"
        )

        with g5d.manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                g5d.TaskSessionError
            ) as caught:
                send_k5_big(
                    manager,
                    governor=governor,
                    outcome_label="deny",
                )

            request = self.assert_frozen_request(
                governor
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
                request,
            )

            self.assert_no_runtime(
                adapter
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
