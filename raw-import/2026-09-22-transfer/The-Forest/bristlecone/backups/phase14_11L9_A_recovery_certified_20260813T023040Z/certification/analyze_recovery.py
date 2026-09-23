from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path


ROOT = Path(
    "/home/user/The-Forest/bristlecone"
)

CERT = (
    ROOT
    / "certification"
    / "phase14_11L9"
)

BENCH = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
)

OUTPUT = (
    BENCH
    / "l9_recovery_summary.json"
)


FILES = {
    "control_harness":
        CERT
        / "recovery_control_benchmark.py",

    "session_harness":
        CERT
        / "hermes_session_cost.py",

    "real_recovery_harness":
        CERT
        / "real_recovery_trial.py",

    "matched_harness":
        CERT
        / "matched_recovery_benchmark.py",

    "control_raw":
        BENCH
        / "l9_recovery_control_raw.json",

    "session_raw":
        BENCH
        / "l9_hermes_session_cost_raw.json",

    "real_recovery_raw":
        BENCH
        / "l9_real_recovery_trial_raw.json",

    "matched_raw":
        BENCH
        / "l9_matched_recovery_raw.json",
}


EXPECTED_SHA256 = {
    "control_harness":
        "4eaa7b4ce6153973f55566fa7087b5aed"
        "0b758fc58216aed4c2d4e61869c9eab",

    "session_harness":
        "2e7a911e39c1b4fae8b6f18deb28af0c"
        "f14b2994adb84c53702538be87cbf1ac",

    "real_recovery_harness":
        "69a83958e9d4f8951b18fbb59825ae664"
        "eff93d8ae88b4fb0a380bdff46b5a5f",

    "matched_harness":
        "c8d1bc70f629b14f3314fd1c5e89078d"
        "b1625f9db8af97fd5699c35b8b78e99e",

    "control_raw":
        "944c68ded31899f29b5ae1ef6d0f55cca"
        "1451b3f065f6e124ccea7bf018a3553",

    "session_raw":
        "cbe31786ff78742442eee72c39282cbcfb"
        "888db4b178338605ed4453f104f4f1",

    "real_recovery_raw":
        "14ec9478a04c1760677c18c8981449b959"
        "f153b7a232c60fd8dd3b48268b7fbf",

    "matched_raw":
        "c66535846e9ec532eef8d1c7f750b0119a"
        "20e3b0d66ec81e6ac184e2cb8de944",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def load_json(path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def p95(values):
    ordered = sorted(values)

    index = min(
        len(ordered) - 1,
        max(
            0,
            (
                95 * len(ordered)
                + 99
            )
            // 100
            - 1,
        ),
    )

    return ordered[index]


def recompute(values):
    require(
        isinstance(values, list)
        and values,
        "Timing samples must be a non-empty list.",
    )

    ordered = sorted(values)

    result = {
        "count":
            len(ordered),

        "median_ns":
            statistics.median(
                ordered
            ),

        "mean_ns":
            statistics.mean(
                ordered
            ),

        "stdev_ns":
            (
                statistics.stdev(
                    ordered
                )
                if len(ordered) > 1
                else 0.0
            ),

        "min_ns":
            ordered[0],

        "max_ns":
            ordered[-1],

        "p95_ns":
            p95(
                ordered
            ),

        "median_us":
            statistics.median(
                ordered
            )
            / 1_000,

        "mean_us":
            statistics.mean(
                ordered
            )
            / 1_000,

        "median_seconds":
            statistics.median(
                ordered
            )
            / 1_000_000_000,

        "mean_seconds":
            statistics.mean(
                ordered
            )
            / 1_000_000_000,
    }

    return result


def same_number(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a == b

    return math.isclose(
        float(a),
        float(b),
        rel_tol=1e-12,
        abs_tol=1e-6,
    )


def validate_stored_stats(
    label,
    values,
    stored,
):
    calculated = recompute(
        values
    )

    keys = (
        "count",
        "median_ns",
        "mean_ns",
        "stdev_ns",
        "min_ns",
        "max_ns",
        "p95_ns",
        "median_us",
        "mean_us",
        "median_seconds",
        "mean_seconds",
    )

    checked = []

    for key in keys:
        if key not in stored:
            continue

        require(
            same_number(
                calculated[key],
                stored[key],
            ),
            (
                f"{label} stored {key} "
                f"does not match raw samples: "
                f"{stored[key]!r} vs "
                f"{calculated[key]!r}"
            ),
        )

        checked.append(
            key
        )

    require(
        checked,
        (
            f"{label} contained no "
            "recomputable statistics."
        ),
    )

    return calculated


# ============================================================
# FILE PRESENCE + FROZEN HASHES
# ============================================================

print(
    "=== L.9 A ANALYSIS / CERTIFICATION ==="
)

print()
print(
    "Checking frozen harness/raw hashes..."
)

actual_hashes = {}

for name, path in FILES.items():
    require(
        path.exists(),
        f"Missing L.9 file: {path}",
    )

    digest = sha256(
        path
    )

    actual_hashes[name] = (
        digest
    )

    require(
        digest
        == EXPECTED_SHA256[name],
        (
            f"Frozen hash mismatch for "
            f"{name}: {digest}"
        ),
    )

    print(
        "PASS",
        name,
        digest,
    )


require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing "
        f"L.9 summary: {OUTPUT}"
    ),
)


# ============================================================
# LOAD FROZEN RAW EVIDENCE
# ============================================================

control = load_json(
    FILES["control_raw"]
)

session = load_json(
    FILES["session_raw"]
)

real = load_json(
    FILES["real_recovery_raw"]
)

matched = load_json(
    FILES["matched_raw"]
)


for name, artifact in (
    ("control", control),
    ("session", session),
    ("real", real),
    ("matched", matched),
):
    require(
        artifact.get("phase")
        == "14.11L.9",
        f"{name} phase mismatch.",
    )

    require(
        artifact.get("status")
        == "success",
        f"{name} status is not success.",
    )


# ============================================================
# A/B CONTROL PATH — RECOMPUTE FROM RAW SAMPLES
# ============================================================

print()
print(
    "Checking L.9A/B raw timing samples..."
)

require(
    control.get(
        "model_inference_executed"
    )
    is False,
    (
        "Control benchmark unexpectedly "
        "claims inference."
    ),
)

require(
    control.get(
        "persistent_production_state_modified"
    )
    is False,
    (
        "Control benchmark claims "
        "persistent modification."
    ),
)

classifier_stale = (
    control[
        "classifier"
    ][
        "stale"
    ][
        "timings_ns"
    ]
)

classifier_nonstale = (
    control[
        "classifier"
    ][
        "nonstale"
    ][
        "timings_ns"
    ]
)

normal_control = (
    control[
        "normal_control"
    ][
        "timings_ns"
    ]
)

recovery_control = (
    control[
        "recovery_control"
    ][
        "timings_ns"
    ]
)

control_delta = (
    control[
        "paired_recovery_overhead"
    ][
        "timings_ns"
    ]
)


require(
    len(classifier_stale)
    == 10_000,
    (
        "Unexpected stale classifier "
        "sample count."
    ),
)

require(
    len(classifier_nonstale)
    == 10_000,
    (
        "Unexpected non-stale classifier "
        "sample count."
    ),
)

require(
    len(normal_control)
    == 500,
    "Unexpected normal sample count.",
)

require(
    len(recovery_control)
    == 500,
    "Unexpected recovery sample count.",
)

require(
    len(control_delta)
    == 500,
    "Unexpected paired-delta count.",
)


expected_control_delta = [
    recovery - normal
    for normal, recovery
    in zip(
        normal_control,
        recovery_control,
    )
]

require(
    control_delta
    == expected_control_delta,
    (
        "Control paired deltas do not "
        "match recovery-normal samples."
    ),
)


control_stats = {
    "classifier_stale":
        validate_stored_stats(
            "stale classifier",
            classifier_stale,
            control[
                "classifier"
            ][
                "stale"
            ][
                "stats"
            ],
        ),

    "classifier_nonstale":
        validate_stored_stats(
            "non-stale classifier",
            classifier_nonstale,
            control[
                "classifier"
            ][
                "nonstale"
            ][
                "stats"
            ],
        ),

    "normal":
        validate_stored_stats(
            "normal control",
            normal_control,
            control[
                "normal_control"
            ][
                "stats"
            ],
        ),

    "recovery":
        validate_stored_stats(
            "recovery control",
            recovery_control,
            control[
                "recovery_control"
            ][
                "stats"
            ],
        ),

    "paired_delta":
        validate_stored_stats(
            "control paired delta",
            control_delta,
            control[
                "paired_recovery_overhead"
            ][
                "stats"
            ],
        ),
}


control_slower = sum(
    value > 0
    for value in control_delta
)

require(
    control_slower
    == control[
        "paired_recovery_overhead"
    ][
        "recovery_slower_pairs"
    ],
    (
        "Control recovery-slower count "
        "does not match raw deltas."
    ),
)


for case_name in (
    "stale_then_stale",
    "stale_then_runtime_failure",
):
    case = (
        control[
            "one_retry_enforcement"
        ][
            case_name
        ]
    )

    require(
        case[
            "second_error_escaped"
        ]
        is True,
        (
            f"{case_name} did not "
            "escape second error."
        ),
    )

    require(
        case[
            "session_creations"
        ]
        == 2,
        (
            f"{case_name} creation "
            "count mismatch."
        ),
    )

    require(
        case[
            "send_calls"
        ]
        == 2,
        (
            f"{case_name} send "
            "count mismatch."
        ),
    )

    require(
        case[
            "classifier_calls"
        ]
        == 1,
        (
            f"{case_name} classifier "
            "count mismatch."
        ),
    )


print(
    "PASS L.9A/B sample/stat recomputation"
)

print(
    "PASS exactly-one-retry semantics"
)


# ============================================================
# C — REAL HERMES CREATE/END
# ============================================================

print()
print(
    "Checking L.9C Hermes session samples..."
)

require(
    session.get(
        "adapter"
    )
    == "hermes",
    "L.9C adapter mismatch.",
)

require(
    session.get(
        "iterations"
    )
    == 50,
    "L.9C iteration count mismatch.",
)

require(
    session.get(
        "chat_endpoint_called_by_harness"
    )
    is False,
    "L.9C unexpectedly called chat.",
)

require(
    session.get(
        "model_turn_executed_by_harness"
    )
    is False,
    "L.9C unexpectedly ran inference.",
)

require(
    session.get(
        "persistent_production_state_modified"
    )
    is False,
    "L.9C claims persistent modification.",
)


samples = session[
    "samples"
]

require(
    len(samples) == 50,
    "L.9C sample count mismatch.",
)

create_ns = [
    item[
        "create_ns"
    ]
    for item in samples
]

end_ns = [
    item[
        "end_ns"
    ]
    for item in samples
]

round_trip_ns = [
    item[
        "round_trip_ns"
    ]
    for item in samples
]


for index, item in enumerate(
    samples
):
    require(
        item[
            "round_trip_ns"
        ]
        == (
            item[
                "create_ns"
            ]
            + item[
                "end_ns"
            ]
        ),
        (
            "L.9C round-trip mismatch "
            f"at sample {index}."
        ),
    )


require(
    create_ns
    == session[
        "create_session"
    ][
        "timings_ns"
    ],
    "L.9C create arrays disagree.",
)

require(
    end_ns
    == session[
        "end_session"
    ][
        "timings_ns"
    ],
    "L.9C end arrays disagree.",
)

require(
    round_trip_ns
    == session[
        "create_end_round_trip"
    ][
        "timings_ns"
    ],
    "L.9C round-trip arrays disagree.",
)


session_stats = {
    "create":
        validate_stored_stats(
            "Hermes create",
            create_ns,
            session[
                "create_session"
            ][
                "stats"
            ],
        ),

    "end":
        validate_stored_stats(
            "Hermes end",
            end_ns,
            session[
                "end_session"
            ][
                "stats"
            ],
        ),

    "round_trip":
        validate_stored_stats(
            "Hermes round trip",
            round_trip_ns,
            session[
                "create_end_round_trip"
            ][
                "stats"
            ],
        ),
}


print(
    "PASS L.9C 50/50 raw samples recomputed"
)


# ============================================================
# D — GENUINE PRODUCTION RECOVERY SEMANTICS
# ============================================================

print()
print(
    "Checking L.9D genuine stale recovery..."
)

require(
    real.get(
        "scenario"
    )
    == "genuine-hermes-stale-small-recovery",
    "L.9D scenario mismatch.",
)

require(
    real.get(
        "real_hermes_used"
    )
    is True,
    "L.9D did not record real Hermes.",
)

require(
    real.get(
        "real_small_inference_executed"
    )
    is True,
    "L.9D did not record real inference.",
)

require(
    real.get(
        "production_recovery_logic_used"
    )
    is True,
    "L.9D did not record production recovery.",
)

require(
    real.get(
        "persistent_production_state_modified"
    )
    is False,
    "L.9D claims persistent modification.",
)


establishment = real[
    "establishment"
]

stale = real[
    "stale_trigger"
]

recovery = real[
    "recovery"
]

cleanup = real[
    "cleanup"
]


session_s = establishment[
    "session_id"
]

session_r = recovery[
    "recovery_session_id"
]


require(
    establishment[
        "session_recovered"
    ]
    is False,
    "L.9D establishment recovered unexpectedly.",
)

require(
    stale[
        "deleted_session_id"
    ]
    == session_s,
    "L.9D deleted session != S.",
)

require(
    stale[
        "forest_binding_after_delete"
    ]
    == session_s,
    (
        "L.9D Forest did not retain "
        "stale S after DELETE."
    ),
)

require(
    recovery[
        "session_recovered"
    ]
    is True,
    "L.9D recovery flag false.",
)

require(
    recovery[
        "recovery_from_session_id"
    ]
    == session_s,
    "L.9D recovery source != S.",
)

require(
    session_r
    and session_r
    != session_s,
    "L.9D replacement R invalid.",
)

require(
    recovery[
        "effective_session_id"
    ]
    == session_r,
    "L.9D effective session != R.",
)

require(
    recovery[
        "previous_session_id"
    ]
    == session_s,
    "L.9D previous session != S.",
)

require(
    recovery[
        "recovery_binding_persisted"
    ]
    is False,
    "L.9D persist=False boundary violated.",
)

require(
    recovery[
        "model_form"
    ]
    == "small",
    "L.9D Model Form changed.",
)

require(
    recovery[
        "reasoning_mode"
    ]
    == "normal",
    "L.9D Reasoning changed.",
)

require(
    recovery[
        "binding_id"
    ]
    == "binding-0001",
    "L.9D binding changed.",
)

require(
    cleanup[
        "attempted"
    ]
    is True
    and cleanup[
        "success"
    ]
    is True
    and cleanup[
        "session_id"
    ]
    == session_r,
    "L.9D replacement cleanup failed.",
)

require(
    establishment[
        "timing_ns"
    ]
    > 0
    and recovery[
        "timing_ns"
    ]
    > 0,
    "L.9D invalid turn timing.",
)


print(
    "PASS genuine S -> R recovery semantics"
)


# ============================================================
# E — MATCHED REAL NORMAL/RECOVERY
# ============================================================

print()
print(
    "Checking L.9E matched real pairs..."
)

require(
    matched.get(
        "scenario"
    )
    == "matched-normal-vs-genuine-recovery",
    "L.9E scenario mismatch.",
)

require(
    matched[
        "pair_count"
    ]
    == 3,
    "L.9E pair count mismatch.",
)

require(
    matched[
        "persistent_production_state_modified"
    ]
    is False,
    "L.9E claims persistent modification.",
)


pairs = matched[
    "pairs"
]

require(
    len(pairs) == 3,
    "L.9E raw pair count mismatch.",
)


expected_orders = [
    "normal-recovery",
    "recovery-normal",
    "normal-recovery",
]

normal_e = []
recovery_e = []
delta_e = []


for index, pair in enumerate(
    pairs
):
    require(
        pair[
            "order"
        ]
        == expected_orders[index],
        (
            "L.9E pair order mismatch "
            f"at pair {index + 1}."
        ),
    )

    normal = pair[
        "normal"
    ]

    recovered = pair[
        "recovery"
    ]

    require(
        normal[
            "session_recovered"
        ]
        is False,
        (
            f"L.9E normal pair "
            f"{index + 1} recovered."
        ),
    )

    require(
        recovered[
            "session_recovered"
        ]
        is True,
        (
            f"L.9E recovery pair "
            f"{index + 1} did not recover."
        ),
    )

    require(
        normal[
            "session_id"
        ]
        == normal[
            "setup_session_id"
        ],
        (
            f"L.9E normal pair "
            f"{index + 1} changed session."
        ),
    )

    require(
        recovered[
            "recovery_from_session_id"
        ]
        == recovered[
            "setup_session_id"
        ],
        (
            f"L.9E recovery pair "
            f"{index + 1} source != stale S."
        ),
    )

    require(
        recovered[
            "recovery_session_id"
        ]
        != recovered[
            "setup_session_id"
        ],
        (
            f"L.9E recovery pair "
            f"{index + 1} failed S→R."
        ),
    )

    require(
        recovered[
            "effective_session_id"
        ]
        == recovered[
            "recovery_session_id"
        ],
        (
            f"L.9E recovery pair "
            f"{index + 1} effective != R."
        ),
    )

    n = normal[
        "timing_ns"
    ]

    r = recovered[
        "timing_ns"
    ]

    d = r - n

    require(
        pair[
            "delta_ns"
        ]
        == d,
        (
            f"L.9E pair "
            f"{index + 1} delta mismatch."
        ),
    )

    require(
        pair[
            "recovery_slower"
        ]
        is (d > 0),
        (
            f"L.9E pair "
            f"{index + 1} slower flag mismatch."
        ),
    )

    normal_e.append(n)
    recovery_e.append(r)
    delta_e.append(d)


require(
    normal_e
    == matched[
        "normal"
    ][
        "timings_ns"
    ],
    "L.9E normal arrays disagree.",
)

require(
    recovery_e
    == matched[
        "recovery"
    ][
        "timings_ns"
    ],
    "L.9E recovery arrays disagree.",
)

require(
    delta_e
    == matched[
        "paired_delta"
    ][
        "timings_ns"
    ],
    "L.9E delta arrays disagree.",
)


matched_stats = {
    "normal":
        validate_stored_stats(
            "L.9E normal",
            normal_e,
            matched[
                "normal"
            ][
                "stats"
            ],
        ),

    "recovery":
        validate_stored_stats(
            "L.9E recovery",
            recovery_e,
            matched[
                "recovery"
            ][
                "stats"
            ],
        ),

    "paired_delta":
        validate_stored_stats(
            "L.9E paired delta",
            delta_e,
            matched[
                "paired_delta"
            ][
                "stats"
            ],
        ),
}


recovery_slower_e = sum(
    value > 0
    for value in delta_e
)

require(
    recovery_slower_e
    == matched[
        "paired_delta"
    ][
        "recovery_slower_pairs"
    ],
    (
        "L.9E recovery-slower count "
        "does not match raw pairs."
    ),
)


boundary = matched[
    "measurement_boundary"
]

require(
    boundary[
        "session_creation_inside_timed_turn"
    ]
    is False,
    (
        "L.9E session creation boundary "
        "changed."
    ),
)

require(
    boundary[
        "stale_trigger_delete_inside_timed_turn"
    ]
    is False,
    (
        "L.9E stale DELETE boundary "
        "changed."
    ),
)

require(
    boundary[
        "normal_generation_count_per_timed_turn"
    ]
    == 1,
    (
        "L.9E normal generation count "
        "is not one."
    ),
)

require(
    boundary[
        "recovery_generation_count_per_timed_turn"
    ]
    == 1,
    (
        "L.9E recovery generation count "
        "is not one."
    ),
)


print(
    "PASS L.9E 3/3 pair semantics"
)

print(
    "PASS L.9E sample/stat recomputation"
)


# ============================================================
# PRODUCTION SOURCE INTEGRITY
# ============================================================

print()
print(
    "Checking production source integrity..."
)


LIVE_SOURCE = {
    "task_session":
        ROOT
        / "runtime"
        / "task_session.py",

    "hermes":
        ROOT
        / "runtime"
        / "adapters"
        / "hermes.py",

    "live_providers":
        ROOT
        / "resources"
        / "live_providers.py",

    "retry_test_scaffold":
        ROOT
        / "tests"
        / "test_model_form_retry_task_session_integration.py",
}


live_source_hashes = {
    name:
        sha256(path)
    for name, path
    in LIVE_SOURCE.items()
}


require(
    control[
        "source_sha256"
    ][
        "task_session"
    ]
    == live_source_hashes[
        "task_session"
    ],
    (
        "Control task_session source "
        "changed since measurement."
    ),
)

require(
    control[
        "source_sha256"
    ][
        "retry_test_scaffold"
    ]
    == live_source_hashes[
        "retry_test_scaffold"
    ],
    (
        "Retry test scaffold changed "
        "since measurement."
    ),
)


for label, artifact in (
    ("L.9C", session),
    ("L.9D", real),
    ("L.9E", matched),
):
    source = artifact[
        "source_sha256"
    ]

    require(
        source[
            "task_session"
        ]
        == live_source_hashes[
            "task_session"
        ],
        (
            f"{label} task_session "
            "source changed."
        ),
    )

    # L.9C calls this key hermes_adapter;
    # L.9D/E call it hermes.
    hermes_key = (
        "hermes_adapter"
        if "hermes_adapter"
        in source
        else "hermes"
    )

    require(
        source[
            hermes_key
        ]
        == live_source_hashes[
            "hermes"
        ],
        (
            f"{label} Hermes "
            "source changed."
        ),
    )


for artifact, label in (
    (real, "L.9D"),
    (matched, "L.9E"),
):
    require(
        artifact[
            "source_sha256"
        ][
            "live_providers"
        ]
        == live_source_hashes[
            "live_providers"
        ],
        (
            f"{label} live provider "
            "source changed."
        ),
    )


print(
    "PASS production source integrity"
)


# ============================================================
# CERTIFICATION INTERPRETATION
# ============================================================

# Important: L.9E's negative observed delta must NOT be
# interpreted as recovery improving performance. The paired
# whole-turn measurements are dominated by previously observed
# Small-generation variance. Recovery objectively performs
# additional operations, and its isolated components are
# measured separately by L.9A/C.

interpretation = {
    "recovery_speedup_claim_supported":
        False,

    "whole_turn_recovery_cost_cleanly_resolved":
        False,

    "reason":
        (
            "L.9E whole-turn variation is much larger "
            "than the isolated recovery machinery. "
            "Recovered turns were faster in 2/3 pairs, "
            "despite recovery objectively adding stale "
            "classification, replacement creation, "
            "binding rotation, and retry control. "
            "Therefore current Small-generation variance "
            "dominates the whole-turn comparison."
        ),

    "supported_findings": [
        (
            "The stale classifier cost is "
            "effectively negligible."
        ),
        (
            "Forest-side additional recovery "
            "control cost is tens of microseconds."
        ),
        (
            "Real Hermes replacement-session creation "
            "cost is hundreds of milliseconds."
        ),
        (
            "Production stale recovery successfully "
            "rotates S to R while preserving frozen "
            "Small/Normal/binding/context semantics."
        ),
        (
            "Recovery is exactly one-shot; a second "
            "failure escapes rather than looping."
        ),
        (
            "Whole-turn Small inference variance "
            "prevents a clean recovery-latency estimate "
            "from L.9E alone."
        ),
    ],
}


# ============================================================
# SUMMARY
# ============================================================

summary = {
    "phase":
        "14.11L.9",

    "certification":
        "A",

    "status":
        "PASS",

    "frozen_hashes":
        actual_hashes,

    "live_source_sha256":
        live_source_hashes,

    "control": {
        "classifier_stale":
            control_stats[
                "classifier_stale"
            ],

        "classifier_nonstale":
            control_stats[
                "classifier_nonstale"
            ],

        "normal":
            control_stats[
                "normal"
            ],

        "recovery":
            control_stats[
                "recovery"
            ],

        "paired_delta":
            control_stats[
                "paired_delta"
            ],

        "recovery_slower_pairs":
            control_slower,

        "pair_count":
            len(
                control_delta
            ),
    },

    "hermes_session_cost": {
        "create":
            session_stats[
                "create"
            ],

        "end":
            session_stats[
                "end"
            ],

        "round_trip":
            session_stats[
                "round_trip"
            ],

        "sample_count":
            len(samples),
    },

    "real_recovery": {
        "establishment_timing_ns":
            establishment[
                "timing_ns"
            ],

        "recovery_timing_ns":
            recovery[
                "timing_ns"
            ],

        "stale_session_id":
            session_s,

        "replacement_session_id":
            session_r,

        "session_recovered":
            True,

        "binding_rotated":
            True,

        "semantic_identity_preserved":
            True,

        "cleanup_success":
            cleanup[
                "success"
            ],
    },

    "matched_real": {
        "normal":
            matched_stats[
                "normal"
            ],

        "recovery":
            matched_stats[
                "recovery"
            ],

        "paired_delta":
            matched_stats[
                "paired_delta"
            ],

        "recovery_slower_pairs":
            recovery_slower_e,

        "pair_count":
            len(pairs),
    },

    "interpretation":
        interpretation,

    "inference_run_by_analyzer":
        False,

    "runtime_mutation_by_analyzer":
        False,

    "persistent_production_state_modified":
        False,
}


OUTPUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


print()
print(
    "=== L.9 A CERTIFICATION RESULT ==="
)

print(
    "Control recovery overhead median:",
    (
        f"{control_stats['paired_delta']['median_us']:.3f} us"
    ),
)

print(
    "Hermes create median:",
    (
        f"{session_stats['create']['median_us']:.3f} us"
    ),
)

print(
    "Hermes end median:",
    (
        f"{session_stats['end']['median_us']:.3f} us"
    ),
)

print(
    "L.9D genuine S -> R recovery: PASS"
)

print(
    "L.9E normal median:",
    (
        f"{matched_stats['normal']['median_seconds']:.9f} s"
    ),
)

print(
    "L.9E recovery median:",
    (
        f"{matched_stats['recovery']['median_seconds']:.9f} s"
    ),
)

print(
    "L.9E paired delta median:",
    (
        f"{matched_stats['paired_delta']['median_seconds']:.9f} s"
    ),
)

print(
    "Recovery speedup claim supported: False"
)

print(
    "Inference executed by analyzer: False"
)

print(
    "Runtime mutation by analyzer: False"
)

print()
print(
    "Summary:",
    OUTPUT,
)

print()
print(
    "Summary SHA256:",
    sha256(OUTPUT),
)

print()
print(
    "PHASE 14.11L.9 A ANALYSIS/CERTIFICATION: PASS"
)
