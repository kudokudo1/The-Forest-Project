"""14.11K.4 — explicit unbound Big fails closed without Small fallback."""

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


def send_explicit_big(
    manager,
    *,
    governor,
):
    return manager.send_runtime_turn(
        "K.4 explicit Big no-downgrade test",
        state=g5d.active_state(
            "task-k4"
        ),
        instructions=(
            "K.4 deterministic unavailable Big test"
        ),
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-k4",
        model_form="big",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "k4-no-downgrade-test"
        ),
        resource_request_reasons=(
            "explicit_big_no_downgrade",
        ),
        resource_may_defer=True,
    )


class BigNoDowngradeTests(
    unittest.TestCase
):
    def test_unbound_explicit_big_fails_before_governor_and_runtime(
        self,
    ):
        # Even though this Governor would approve,
        # an unavailable/unbound Big must never reach it.
        governor = g5d.RecordingGovernor(
            "approve"
        )

        # Production registry:
        #
        # small -> binding-0001
        # big   -> no binding
        with g5d.manager_fixture(
            include_big=False
        ) as (
            manager,
            adapter,
        ):
            with self.assertRaises(
                g5d.TaskSessionError
            ) as caught:
                send_explicit_big(
                    manager,
                    governor=governor,
                )

            message = str(
                caught.exception
            )

            # Exact semantic intent remains Big.
            self.assertIn(
                "Resolved Model Form 'big'",
                message,
            )

            # Failure reason must be the absence
            # of a runtime binding.
            self.assertIn(
                "has no available runtime binding",
                message,
            )

            # The request must fail before
            # resource governance.
            self.assertEqual(
                governor.requests,
                [],
            )

            # Absolutely no runtime/session activity.
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

            # If Big had silently become Small,
            # binding-0001 would be available and this
            # specific Big-unbound error could not occur.
            self.assertNotIn(
                "Resolved Model Form 'small'",
                message,
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
