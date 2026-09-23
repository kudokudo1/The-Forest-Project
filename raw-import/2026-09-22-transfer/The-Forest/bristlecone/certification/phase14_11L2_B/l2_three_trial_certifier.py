#!/usr/bin/env python3
"""
Terminal B Phase 14.11L.2 three-trial certifier.

READ-ONLY.

This script must only be run after Terminal A has completed
and frozen Trials 1, 2, and 3.

It performs no:
- Ollama command
- Hermes command
- TaskSession turn
- session creation/end operation
- service restart
- active.yaml modification
- production modification
"""

from pathlib import Path
import hashlib
import json
import math
import statistics
import sys

ROOT = Path("bristlecone")

EXPECTED = {
    ROOT / "runtime/task_session.py":
        "d666cb1471b568bf43db4255f5e84e98c1ea502af467e1e2670e4a93dc364991",

    ROOT / "runtime/session_store.py":
        "3c3449fa878920ea27f39b6216cf38a687d09a08da1d5b57af68c1a2f4beb48f",

    ROOT / "runtime/session_identity.py":
        "8a1d668e898dc2df7b60fd5099be0cf42dd2d4c864cbe163164f0a061a777353",

    ROOT / "runtime/adapters/hermes.py":
        "a09949eead5cb9772aca312c91630703c7ff8ce43df778730279445b25635084",

    ROOT / "resources/live_providers.py":
        "40b49375dbe014b27b6fc5696bccf74274864e42953c473b42ffe10a3c552299",

    ROOT / "model_form/bindings.yaml":
        "74110afd51de7ceddd02948d0430b0f9f1b5443a6eaaaa0b8a6e4164a52b0583",

    ROOT / "state/active.yaml":
        "6b8fb9b44757917c1889a7368d43f393165080d248cdb3d9c5982aad53b270e5",
}


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def check(condition, message):
    if not condition:
        raise AssertionError(message)

    print(f"PASS: {message}")


def nearest_rank(values, percentile):
    values = sorted(values)

    rank = math.ceil(
        percentile * len(values)
    )

    return values[
        max(rank, 1) - 1
    ]


def main(paths):
    check(
        len(paths) == 3,
        "exactly three trial artifacts supplied",
    )

    trials = []

    for path in paths:
        check(
            path.is_file(),
            f"artifact exists: {path}",
        )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        data["_path"] = str(path)
        data["_sha256"] = sha256(path)

        trials.append(data)

    check(
        sorted(
            t["trial"]
            for t in trials
        )
        == [1, 2, 3],
        "inputs are exactly Trials 1-3",
    )

    trials.sort(
        key=lambda t: t["trial"]
    )

    # Same benchmark contract across all three.
    for t in trials:
        n = t["trial"]

        check(
            t["phase"] == "14.11L.2",
            f"Trial {n} phase correct",
        )

        check(
            t["scenario"] == "cold-real-small",
            f"Trial {n} scenario correct",
        )

        check(
            t["status"] == "success",
            f"Trial {n} succeeded",
        )

        check(
            t["model_form"] == "small",
            f"Trial {n} requested Small",
        )

        check(
            t["binding_expected"] == "binding-0001",
            f"Trial {n} expected binding-0001",
        )

        check(
            t["reasoning_mode"] == "normal",
            f"Trial {n} requested Normal",
        )

        check(
            t["persist"] is False,
            f"Trial {n} persist=False",
        )

        check(
            t["active_yaml_sha_before"]
            == EXPECTED[
                ROOT / "state/active.yaml"
            ],
            f"Trial {n} active.yaml baseline correct",
        )

        check(
            t["active_yaml_sha_after"]
            == t["active_yaml_sha_before"],
            f"Trial {n} active.yaml unchanged",
        )

        check(
            t["before"]["resident_models"] == [],
            f"Trial {n} genuinely cold before",
        )

        check(
            len(
                t["after"]["resident_models"]
            )
            >= 1,
            f"Trial {n} resident after",
        )

        check(
            "bristlecone-qwen35:4b-64k"
            in json.dumps(
                t["after"],
                sort_keys=True,
            ),
            f"Trial {n} resident model is Small",
        )

        r = t["result"]

        check(
            r["binding_id"] == "binding-0001",
            f"Trial {n} actual binding correct",
        )

        check(
            r["model_form"] == "small",
            f"Trial {n} actual Model Form Small",
        )

        check(
            r["resolved_reasoning_mode"]
            == "normal",
            f"Trial {n} resolved Normal",
        )

        check(
            r["adapter"] == "hermes",
            f"Trial {n} adapter Hermes",
        )

        check(
            r["initial_session_created"] is True,
            f"Trial {n} fresh initial session",
        )

        check(
            r["session_created"] is True,
            f"Trial {n} reports session creation",
        )

        check(
            r["session_reused"] is False,
            f"Trial {n} no reuse",
        )

        check(
            r["session_recovered"] is False,
            f"Trial {n} no recovery",
        )

        check(
            r["session_rotated"] is False,
            f"Trial {n} no rotation",
        )

        check(
            r["binding_persisted"] is False,
            f"Trial {n} no persistence",
        )

        ns = int(t["duration_ns"])

        check(
            math.isclose(
                ns / 1_000_000_000,
                float(t["duration_s"]),
                rel_tol=1e-12,
                abs_tol=1e-9,
            ),
            f"Trial {n} timing internally consistent",
        )

    # Fresh identities across runs.
    check(
        len(
            {
                t["task_id"]
                for t in trials
            }
        )
        == 3,
        "three unique Forest Tasks",
    )

    check(
        len(
            {
                t["execution_context_id"]
                for t in trials
            }
        )
        == 3,
        "three unique execution contexts",
    )

    check(
        len(
            {
                t["result"]["session_id"]
                for t in trials
            }
        )
        == 3,
        "three unique runtime sessions",
    )

    # Frozen production/state.
    for path, expected in EXPECTED.items():
        check(
            sha256(path) == expected,
            f"frozen SHA: {path}",
        )

    durations = [
        t["duration_ns"]
        / 1_000_000_000
        for t in trials
    ]

    median = statistics.median(
        durations
    )

    output = {
        "n": 3,

        "trials": [
            {
                "trial":
                    t["trial"],

                "path":
                    t["_path"],

                "sha256":
                    t["_sha256"],

                "duration_s":
                    t["duration_ns"]
                    / 1_000_000_000,
            }
            for t in trials
        ],

        "min_s":
            min(durations),

        "max_s":
            max(durations),

        "mean_s":
            statistics.mean(durations),

        "median_s":
            median,

        "stdev_s":
            statistics.stdev(durations),

        "p90_s":
            nearest_rank(
                durations,
                0.90,
            ),
    }

    # Advisory only. Never exclude data.
    outliers = []

    for t, duration in zip(
        trials,
        durations,
    ):
        deviation = (
            abs(duration - median)
            / median
            if median
            else 0.0
        )

        outliers.append(
            {
                "trial":
                    t["trial"],

                "duration_s":
                    duration,

                "relative_deviation_from_median":
                    deviation,

                "advisory_outlier":
                    deviation > 0.25,

                "excluded":
                    False,
            }
        )

    output["outliers"] = outliers

    output["outlier_rule"] = (
        "advisory only: absolute deviation "
        "from median >25%; no observation excluded"
    )

    print(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
    )

    print()
    print(
        "PASS: all three raw timings preserved"
    )

    print(
        "PASS: no outlier silently discarded"
    )

    print("STATUS=0")


if __name__ == "__main__":
    main(
        [
            Path(value)
            for value in sys.argv[1:]
        ]
    )
