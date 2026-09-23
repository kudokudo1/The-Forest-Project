"""14.11K.2/K.3 — explicit Big pre-runtime Governor boundary."""

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


def send_explicit_big_governed_turn(
    manager,
    *,
    governor,
    task_id="task-k23",
):
    """Send explicit Big semantic intent only to the Governor boundary."""

    return manager.send_runtime_turn(
        "K.2/K.3 explicit Big boundary turn",
        state=g5d.active_state(
            task_id
        ),
        instructions=(
            "K.2/K.3 deterministic Big boundary test"
        ),
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-k23",
        model_form="big",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "k23-big-boundary-test"
        ),
        resource_request_reasons=(
            "explicit_big_boundary_certification",
        ),
        resource_may_defer=True,
    )


class ExplicitBigGovernorBoundaryTests(
    unittest.TestCase
):
    """Big reaches Governor unchanged but never reaches runtime."""

    def assert_zero_runtime_effects(
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

    def assert_exact_big_request(
        self,
        governor,
    ):
        self.assertEqual(
            len(governor.requests),
            1,
        )

        request = governor.requests[0]

        # K.2 — explicit Big semantic intent survives
        # unchanged into ResourceRequest.
        self.assertEqual(
            request.model_form,
            "big",
        )

        self.assertEqual(
            request.execution_context_id,
            "ctx-k23",
        )

        self.assertEqual(
            request.task_id,
            "task-k23",
        )

        self.assertEqual(
            request.reasoning_mode,
            "normal",
        )

        self.assertEqual(
            request.priority,
            "standard",
        )

        self.assertTrue(
            request.may_defer,
        )

        # No Big -> Small semantic substitution.
        self.assertNotEqual(
            request.model_form,
            "small",
        )

        return request

    def test_k2_explicit_big_reaches_governor_unchanged(
        self,
    ):
        governor = g5d.RecordingGovernor(
            "defer"
        )

        with g5d.manager_fixture(
            include_big=True
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                g5d.TaskSessionError
            ):
                send_explicit_big_governed_turn(
                    manager,
                    governor=governor,
                )

            self.assert_exact_big_request(
                governor
            )

            self.assert_zero_runtime_effects(
                adapter
            )

    def test_k3_big_defer_stops_before_runtime(
        self,
    ):
        governor = g5d.RecordingGovernor(
            "defer"
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
                send_explicit_big_governed_turn(
                    manager,
                    governor=governor,
                )

            request = (
                self.assert_exact_big_request(
                    governor
                )
            )

            self.assert_zero_runtime_effects(
                adapter
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

            # Governor decision must belong to the
            # exact ResourceRequest object.
            self.assertIs(
                decision.request,
                request,
            )

    def test_k3_big_deny_stops_before_runtime(
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
                send_explicit_big_governed_turn(
                    manager,
                    governor=governor,
                )

            request = (
                self.assert_exact_big_request(
                    governor
                )
            )

            self.assert_zero_runtime_effects(
                adapter
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


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
