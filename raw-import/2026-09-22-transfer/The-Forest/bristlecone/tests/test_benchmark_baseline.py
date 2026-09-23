"""Phase 14.11L.0 baseline schema tests."""

import json
import tempfile
import unittest

from dataclasses import FrozenInstanceError
from pathlib import Path

from benchmarks.baseline import (
    BenchmarkBaseline,
    write_baseline_jsonl,
)


def fake_baseline():
    return BenchmarkBaseline(
        schema_version=1,
        record_type="benchmark_baseline",
        phase="14.11L.0",
        recorded_at_utc="2026-08-12T00:00:00Z",
        methodology_sha256="a" * 64,
        active_yaml_sha256="b" * 64,
        production_sha256={
            "example.py": "c" * 64,
        },
        environment={
            "cpu_count": 9,
        },
        model_form_under_test="small",
        binding_under_test="binding-0001",
        big_execution_allowed=False,
        notes=(
            "deterministic",
            "no-runtime",
        ),
    )


class BenchmarkBaselineTests(
    unittest.TestCase
):

    def test_baseline_is_frozen(
        self,
    ):
        baseline = fake_baseline()

        with self.assertRaises(
            FrozenInstanceError
        ):
            baseline.phase = "changed"

    def test_big_cannot_be_authorized(
        self,
    ):
        with self.assertRaises(
            ValueError
        ):
            BenchmarkBaseline(
                schema_version=1,
                record_type="benchmark_baseline",
                phase="14.11L.0",
                recorded_at_utc="x",
                methodology_sha256="a",
                active_yaml_sha256="b",
                production_sha256={},
                environment={},
                model_form_under_test="small",
                binding_under_test="binding-0001",
                big_execution_allowed=True,
                notes=(),
            )

    def test_jsonl_write(
        self,
    ):
        baseline = fake_baseline()

        with tempfile.TemporaryDirectory() as td:
            path = (
                Path(td)
                / "baseline.jsonl"
            )

            write_baseline_jsonl(
                path,
                baseline,
            )

            lines = (
                path.read_text(
                    encoding="utf-8"
                )
                .splitlines()
            )

        self.assertEqual(
            len(lines),
            1,
        )

        value = json.loads(
            lines[0]
        )

        self.assertEqual(
            value["record_type"],
            "benchmark_baseline",
        )

        self.assertFalse(
            value["big_execution_allowed"]
        )

        self.assertEqual(
            value["binding_under_test"],
            "binding-0001",
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
