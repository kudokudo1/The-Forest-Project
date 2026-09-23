"""Phase 14.11L.0 benchmark foundation tests."""

from __future__ import annotations

import tempfile
import unittest

from dataclasses import FrozenInstanceError
from pathlib import Path

from benchmarks.records import (
    BenchmarkTrial,
    append_jsonl,
    read_jsonl,
)
from benchmarks.timing import (
    BenchmarkTimingError,
    MonotonicTimeline,
)


class FakeClock:
    def __init__(
        self,
        values,
    ):
        self.values = iter(values)

    def __call__(
        self,
    ):
        return next(
            self.values
        )


class BenchmarkFoundationTests(
    unittest.TestCase
):

    def test_monotonic_timeline_duration(
        self,
    ):
        timeline = MonotonicTimeline(
            clock=FakeClock(
                (
                    100,
                    150,
                    275,
                )
            )
        )

        timeline.mark("T0")
        timeline.mark("T1")
        timeline.mark("T4")

        self.assertEqual(
            timeline.duration_ns(
                "T0",
                "T1",
            ),
            50,
        )

        self.assertEqual(
            timeline.duration_ns(
                "T0",
                "T4",
            ),
            175,
        )

        frozen = timeline.freeze()

        self.assertEqual(
            tuple(
                item.label
                for item in frozen
            ),
            (
                "T0",
                "T1",
                "T4",
            ),
        )

    def test_duplicate_mark_rejected(
        self,
    ):
        timeline = MonotonicTimeline(
            clock=FakeClock(
                (
                    10,
                    20,
                )
            )
        )

        timeline.mark("T0")

        with self.assertRaises(
            BenchmarkTimingError
        ):
            timeline.mark("T0")

    def test_backwards_clock_rejected(
        self,
    ):
        timeline = MonotonicTimeline(
            clock=FakeClock(
                (
                    20,
                    10,
                )
            )
        )

        timeline.mark("T0")

        with self.assertRaises(
            BenchmarkTimingError
        ):
            timeline.mark("T1")

    def make_trial(
        self,
    ):
        return BenchmarkTrial(
            schema_version=1,
            run_id="L0-test-001",
            phase="14.11L.0",
            scenario="foundation",
            trial=1,
            recorded_at_utc=(
                "2026-08-12T00:00:00Z"
            ),
            prompt_id="none",
            execution_context_id=(
                "ctx-benchmark-test"
            ),
            binding_id="binding-0001",
            model_form="small",
            reasoning_mode="normal",
            workshop=None,
            session_mode="none",
            residency_mode="none",
            persistence=False,
            status="test",
            total_turn_ns=175,
            notes=(
                "deterministic",
                "no-runtime",
            ),
        )

    def test_trial_is_frozen(
        self,
    ):
        trial = self.make_trial()

        with self.assertRaises(
            FrozenInstanceError
        ):
            trial.status = "changed"

    def test_jsonl_round_trip(
        self,
    ):
        trial = self.make_trial()

        with tempfile.TemporaryDirectory() as td:
            path = (
                Path(td)
                / "records.jsonl"
            )

            append_jsonl(
                path,
                trial,
            )

            records = read_jsonl(
                path
            )

        self.assertEqual(
            len(records),
            1,
        )

        self.assertEqual(
            records[0]["run_id"],
            "L0-test-001",
        )

        self.assertEqual(
            records[0]["total_turn_ns"],
            175,
        )

        self.assertEqual(
            records[0]["notes"],
            [
                "deterministic",
                "no-runtime",
            ],
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
