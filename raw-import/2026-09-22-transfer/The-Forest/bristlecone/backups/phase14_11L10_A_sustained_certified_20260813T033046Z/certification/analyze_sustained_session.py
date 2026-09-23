from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path


ROOT = Path(
    "/home/user/The-Forest/bristlecone"
)

HARNESS = (
    ROOT
    / "certification"
    / "phase14_11L10"
    / "sustained_session_benchmark.py"
)

RAW = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l10_sustained_session_raw.json"
)

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l10_sustained_session_summary.json"
)


EXPECTED = {
    "harness":
        "f2397758642dd7c51c2240608df4846dfc8ee80258abf11619e392fa34a3bed4",

    "raw":
        "e592c4ff7fa339b18a977cd1da0412a74035caee6c8f16a403f1b51a0697f6f7",

    "task_session":
        "d666cb1471b568bf43db4255f5e84e98c1ea502af467e1e2670e4a93dc364991",

    "hermes":
        "a09949eead5cb9772aca312c91630703c7ff8ce43df778730279445b25635084",

    "live_providers":
        "40b49375dbe014b27b6fc5696bccf74274864e42953c473b42ffe10a3c552299",

    "l4_reuse_foundation":
        "ce343935d5c8078d3c9f802609d662a2650f9a4e269b1f209967f3aac7a5d9dd",
}


SOURCE = {
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

    "l4_reuse_foundation":
        ROOT
        / "certification"
        / "phase14_11L4"
        / "reuse_trial1.py",
}


MODEL = "bristlecone-qwen35:4b-64k"
BINDING = "binding-0001"
TURN_COUNT = 8


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


def close(a, b):
    if (
        isinstance(a, int)
        and isinstance(b, int)
    ):
        return a == b

    return math.isclose(
        float(a),
        float(b),
        rel_tol=1e-12,
        abs_tol=1e-6,
    )


def recompute(values):
    require(
        isinstance(values, list)
        and values,
        "Expected non-empty timing list.",
    )

    ordered = sorted(values)

    return {
        "count":
            len(values),

        "median_ns":
            statistics.median(values),

        "mean_ns":
            statistics.mean(values),

        "stdev_ns":
            (
                statistics.stdev(values)
                if len(values) > 1
                else 0.0
            ),

        "min_ns":
            ordered[0],

        "max_ns":
            ordered[-1],

        "median_seconds":
            statistics.median(values)
            / 1_000_000_000,

        "mean_seconds":
            statistics.mean(values)
            / 1_000_000_000,
    }


def validate_stats(
    label,
    values,
    stored,
):
    calculated = recompute(
        values
    )

    for key in (
        "count",
        "median_ns",
        "mean_ns",
        "stdev_ns",
        "min_ns",
        "max_ns",
        "median_seconds",
        "mean_seconds",
    ):
        require(
            key in stored,
            f"{label} missing stored {key}.",
        )

        require(
            close(
                calculated[key],
                stored[key],
            ),
            (
                f"{label} {key} mismatch: "
                f"stored={stored[key]!r}, "
                f"recomputed={calculated[key]!r}"
            ),
        )

    return calculated


print(
    "=== L.10 A ANALYSIS / CERTIFICATION ==="
)


# ============================================================
# FROZEN FILE INTEGRITY
# ============================================================

print()
print(
    "Checking frozen L.10 evidence..."
)


require(
    HARNESS.is_file(),
    f"Missing harness: {HARNESS}",
)

require(
    RAW.is_file(),
    f"Missing raw evidence: {RAW}",
)

require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing "
        f"L.10 summary: {OUTPUT}"
    ),
)


actual_harness_sha = sha256(
    HARNESS
)

actual_raw_sha = sha256(
    RAW
)


require(
    actual_harness_sha
    == EXPECTED[
        "harness"
    ],
    (
        "L.10 harness hash changed: "
        f"{actual_harness_sha}"
    ),
)

require(
    actual_raw_sha
    == EXPECTED[
        "raw"
    ],
    (
        "L.10 raw evidence hash changed: "
        f"{actual_raw_sha}"
    ),
)


print(
    "PASS frozen harness",
    actual_harness_sha,
)

print(
    "PASS frozen raw evidence",
    actual_raw_sha,
)


# ============================================================
# PRODUCTION / FOUNDATION SOURCE INTEGRITY
# ============================================================

print()
print(
    "Checking source integrity..."
)


live_source_sha = {}


for name, path in SOURCE.items():
    digest = sha256(
        path
    )

    live_source_sha[
        name
    ] = digest

    require(
        digest
        == EXPECTED[name],
        (
            f"Source anchor changed for "
            f"{name}: {digest}"
        ),
    )

    print(
        "PASS",
        name,
        digest,
    )


# ============================================================
# LOAD RAW
# ============================================================

raw = load_json(
    RAW
)


require(
    raw.get(
        "phase"
    )
    == "14.11L.10",
    "L.10 phase mismatch.",
)

require(
    raw.get(
        "scenario"
    )
    == "sustained-same-session-health",
    "L.10 scenario mismatch.",
)

require(
    raw.get(
        "status"
    )
    == "success",
    "L.10 raw status is not success.",
)

require(
    raw.get(
        "model"
    )
    == MODEL,
    "L.10 model mismatch.",
)

require(
    raw.get(
        "model_form"
    )
    == "small",
    "L.10 Model Form mismatch.",
)

require(
    raw.get(
        "binding_id"
    )
    == BINDING,
    "L.10 binding mismatch.",
)

require(
    raw.get(
        "reasoning_mode"
    )
    == "normal",
    "L.10 Reasoning mismatch.",
)

require(
    raw.get(
        "measured_turn_count"
    )
    == TURN_COUNT,
    "L.10 measured turn count mismatch.",
)


# ============================================================
# SOURCE HASHES EMBEDDED IN RAW
# ============================================================

print()
print(
    "Checking raw source anchors..."
)


raw_source = raw[
    "source_sha256"
]


for name in (
    "task_session",
    "hermes",
    "live_providers",
    "l4_reuse_foundation",
):
    require(
        raw_source[
            name
        ]
        == live_source_sha[
            name
        ],
        (
            "Raw source anchor does not "
            f"match current source: {name}"
        ),
    )


print(
    "PASS raw/live source anchors"
)


# ============================================================
# PRIME SEMANTICS
# ============================================================

print()
print(
    "Checking unmeasured prime..."
)


prime = raw[
    "prime"
]

session_s = str(
    prime.get(
        "session_id"
    )
    or ""
).strip()


require(
    session_s,
    "Prime has no session S.",
)

require(
    prime.get(
        "message"
    )
    == "Reply only with: L10-PRIME",
    "Prime message mismatch.",
)

require(
    prime.get(
        "session_created"
    )
    is True,
    "Prime did not create S.",
)

require(
    prime.get(
        "session_reused"
    )
    is False,
    "Prime unexpectedly reused session.",
)

require(
    prime.get(
        "session_recovered"
    )
    is False,
    "Prime unexpectedly recovered.",
)

require(
    prime.get(
        "session_rotated"
    )
    is False,
    "Prime unexpectedly rotated.",
)


print(
    "PASS prime established S:",
    session_s,
)


# ============================================================
# TURN-BY-TURN SEMANTICS
# ============================================================

print()
print(
    "Checking all 8 measured turns..."
)


turns = raw[
    "turns"
]


require(
    isinstance(
        turns,
        list,
    )
    and len(
        turns
    )
    == TURN_COUNT,
    "Expected exactly 8 turn records.",
)


timings_from_turns = []
memory_deltas = []
memory_before = []
memory_after = []


for index, turn in enumerate(
    turns,
    start=1,
):
    label = (
        f"T{index:02d}"
    )

    expected_message = (
        "Reply only with: "
        f"L10-T{index:02d}"
    )

    expected_response = (
        f"L10-T{index:02d}"
    )


    require(
        turn[
            "turn"
        ]
        == index,
        f"{label} turn number mismatch.",
    )

    require(
        turn[
            "message"
        ]
        == expected_message,
        f"{label} prompt mismatch.",
    )

    require(
        turn[
            "response_message"
        ]
        == expected_response,
        (
            f"{label} response mismatch: "
            f"{turn['response_message']!r}"
        ),
    )

    require(
        turn[
            "session_id"
        ]
        == session_s,
        f"{label} changed session S.",
    )

    require(
        turn[
            "initial_requested_session_id"
        ]
        == session_s,
        (
            f"{label} initial requested "
            "session != S."
        ),
    )

    require(
        turn[
            "requested_session_id"
        ]
        == session_s,
        (
            f"{label} requested "
            "session != S."
        ),
    )

    require(
        turn[
            "session_created"
        ]
        is False,
        (
            f"{label} unexpectedly "
            "created a session."
        ),
    )

    require(
        turn[
            "initial_session_created"
        ]
        is False,
        (
            f"{label} unexpectedly "
            "created initial session."
        ),
    )

    require(
        turn[
            "session_reused"
        ]
        is True,
        f"{label} did not reuse S.",
    )

    require(
        turn[
            "session_recovered"
        ]
        is False,
        (
            f"{label} unexpectedly "
            "performed recovery."
        ),
    )

    require(
        turn[
            "session_rotated"
        ]
        is False,
        (
            f"{label} unexpectedly "
            "rotated session."
        ),
    )

    require(
        turn[
            "model_form"
        ]
        == "small",
        f"{label} changed Model Form.",
    )

    require(
        turn[
            "reasoning_mode"
        ]
        == "normal",
        f"{label} changed Reasoning.",
    )

    require(
        turn[
            "binding_id"
        ]
        == BINDING,
        f"{label} changed binding.",
    )

    require(
        turn[
            "execution_context_id"
        ]
        == raw[
            "execution_context_id"
        ],
        (
            f"{label} changed "
            "execution context."
        ),
    )


    checks = turn[
        "checks"
    ]

    require(
        isinstance(
            checks,
            dict,
        )
        and checks,
        f"{label} has no check map.",
    )

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if passed is not True
    ]

    require(
        not failed_checks,
        (
            f"{label} stored failed checks: "
            + ", ".join(
                failed_checks
            )
        ),
    )


    resident_before = turn[
        "resident_before"
    ]

    resident_after = turn[
        "resident_after"
    ]


    require(
        len(
            resident_before
        )
        == 1
        and MODEL
        in resident_before[0],
        (
            f"{label} Small not resident "
            "before measured turn."
        ),
    )

    require(
        len(
            resident_after
        )
        == 1
        and MODEL
        in resident_after[0],
        (
            f"{label} Small not resident "
            "after measured turn."
        ),
    )


    before = turn[
        "mem_available_before_kib"
    ]

    after = turn[
        "mem_available_after_kib"
    ]

    delta = turn[
        "mem_available_delta_kib"
    ]


    require(
        after - before
        == delta,
        (
            f"{label} MemAvailable "
            "delta arithmetic mismatch."
        ),
    )


    duration_ns = turn[
        "duration_ns"
    ]


    require(
        duration_ns > 0,
        f"{label} duration is invalid.",
    )

    require(
        close(
            turn[
                "duration_seconds"
            ],
            duration_ns
            / 1_000_000_000,
        ),
        (
            f"{label} duration seconds "
            "do not match ns."
        ),
    )


    timings_from_turns.append(
        duration_ns
    )

    memory_before.append(
        before
    )

    memory_after.append(
        after
    )

    memory_deltas.append(
        delta
    )


print(
    "PASS 8/8 turn semantics"
)

print(
    "PASS 8/8 exact responses"
)

print(
    "PASS 8/8 residency checks"
)

print(
    "PASS 8/8 memory arithmetic checks"
)


# ============================================================
# CROSS-TURN INVARIANTS
# ============================================================

print()
print(
    "Checking cross-turn invariants..."
)


require(
    raw[
        "unique_measured_session_ids"
    ]
    == [
        session_s
    ],
    (
        "Raw unique session list "
        "is not exactly [S]."
    ),
)

require(
    raw[
        "unexpected_recovery_count"
    ]
    == 0,
    (
        "Unexpected recovery count "
        "is not zero."
    ),
)

require(
    raw[
        "unexpected_rotation_count"
    ]
    == 0,
    (
        "Unexpected rotation count "
        "is not zero."
    ),
)

require(
    all(
        turn[
            "session_id"
        ]
        == session_s
        for turn in turns
    ),
    (
        "Cross-turn session identity "
        "was not stable."
    ),
)


print(
    "PASS one session S across 8/8 turns"
)

print(
    "PASS zero recovery"
)

print(
    "PASS zero rotation"
)


# ============================================================
# RAW TIMING RECOMPUTATION
# ============================================================

print()
print(
    "Recomputing timing statistics..."
)


raw_timings = raw[
    "timings_ns"
]


require(
    raw_timings
    == timings_from_turns,
    (
        "Top-level timings_ns differs "
        "from per-turn durations."
    ),
)


all_stats = validate_stats(
    "all-turn timing",
    raw_timings,
    raw[
        "timing_stats"
    ],
)

early_values = (
    raw_timings[:4]
)

late_values = (
    raw_timings[4:]
)


early_stats = validate_stats(
    "early turns 1-4",
    early_values,
    raw[
        "early_turns_1_to_4"
    ],
)

late_stats = validate_stats(
    "late turns 5-8",
    late_values,
    raw[
        "late_turns_5_to_8"
    ],
)


late_minus_early = (
    late_stats[
        "median_ns"
    ]
    - early_stats[
        "median_ns"
    ]
)


require(
    close(
        raw[
            "late_minus_early_median_ns"
        ],
        late_minus_early,
    ),
    (
        "Stored late-minus-early "
        "median mismatch."
    ),
)

require(
    close(
        raw[
            "late_minus_early_median_seconds"
        ],
        late_minus_early
        / 1_000_000_000,
    ),
    (
        "Stored late-minus-early "
        "seconds mismatch."
    ),
)


first_to_last = (
    raw_timings[-1]
    - raw_timings[0]
)


require(
    raw[
        "first_to_last_ns"
    ]
    == first_to_last,
    (
        "Stored first-to-last "
        "delta mismatch."
    ),
)

require(
    close(
        raw[
            "first_to_last_seconds"
        ],
        first_to_last
        / 1_000_000_000,
    ),
    (
        "Stored first-to-last "
        "seconds mismatch."
    ),
)


print(
    "PASS all timing samples independently recomputed"
)

print(
    "PASS early/late descriptors independently recomputed"
)


# ============================================================
# CLEANUP / SAFETY BOUNDARIES
# ============================================================

print()
print(
    "Checking cleanup and mutation boundaries..."
)


cleanup = raw[
    "cleanup"
]


require(
    cleanup[
        "attempted"
    ]
    is True,
    "Cleanup was not attempted.",
)

require(
    cleanup[
        "success"
    ]
    is True,
    "Cleanup was not successful.",
)

require(
    cleanup[
        "session_id"
    ]
    == session_s,
    (
        "Cleanup targeted a "
        "session other than S."
    ),
)

require(
    cleanup[
        "error"
    ]
    is None,
    "Cleanup recorded an error.",
)

require(
    raw[
        "real_hermes_used"
    ]
    is True,
    "L.10 did not record real Hermes.",
)

require(
    raw[
        "real_small_inference_executed"
    ]
    is True,
    (
        "L.10 did not record "
        "real Small inference."
    ),
)

require(
    raw[
        "persistent_production_state_modified"
    ]
    is False,
    (
        "L.10 claims persistent "
        "production modification."
    ),
)


print(
    "PASS cleanup"
)

print(
    "PASS persist=False production boundary"
)


# ============================================================
# MEMORY DESCRIPTORS
#
# /proc/meminfo is system-wide and noisy. These observations
# must not be interpreted as a process-specific memory leak.
# ============================================================

memory_summary = {
    "before_samples_kib":
        memory_before,

    "after_samples_kib":
        memory_after,

    "per_turn_delta_kib":
        memory_deltas,

    "median_per_turn_delta_kib":
        statistics.median(
            memory_deltas
        ),

    "mean_per_turn_delta_kib":
        statistics.mean(
            memory_deltas
        ),

    "first_before_kib":
        memory_before[0],

    "last_after_kib":
        memory_after[-1],

    "last_after_minus_first_before_kib":
        (
            memory_after[-1]
            - memory_before[0]
        ),

    "memory_leak_claim_supported":
        False,

    "reason":
        (
            "MemAvailable is a system-wide noisy "
            "snapshot rather than process-attributed "
            "memory. Eight observations can describe "
            "the run but cannot establish a leak."
        ),
}


# ============================================================
# INTERPRETATION
# ============================================================

interpretation = {
    "sustained_session_health_supported":
        True,

    "session_identity_stable":
        True,

    "semantic_drift_observed":
        False,

    "unexpected_recovery_observed":
        False,

    "unexpected_rotation_observed":
        False,

    "obvious_latency_degradation_observed":
        False,

    "latency_improvement_claim_supported":
        False,

    "latency_degradation_claim_supported":
        False,

    "memory_leak_claim_supported":
        False,

    "reason":
        (
            "All eight measured real Small turns reused "
            "the same session and preserved Model Form, "
            "Reasoning, binding, and execution context "
            "without recovery or rotation. Late-turn "
            "median latency was lower than early-turn "
            "median latency, but the run contains only "
            "eight samples and substantial natural "
            "generation variance, so neither improvement "
            "nor degradation should be claimed."
        ),
}


# ============================================================
# WRITE A SUMMARY
# ============================================================

summary = {
    "phase":
        "14.11L.10",

    "certification":
        "A",

    "status":
        "PASS",

    "scenario":
        "sustained-same-session-health",

    "frozen_sha256": {
        "harness":
            actual_harness_sha,

        "raw":
            actual_raw_sha,
    },

    "source_sha256":
        live_source_sha,

    "session": {
        "session_s":
            session_s,

        "measured_turn_count":
            TURN_COUNT,

        "unique_measured_session_ids":
            [
                session_s
            ],

        "unexpected_recovery_count":
            0,

        "unexpected_rotation_count":
            0,

        "all_exact_responses":
            True,

        "all_residency_checks":
            True,

        "cleanup_success":
            True,
    },

    "timing": {
        "all_turns":
            all_stats,

        "early_turns_1_to_4":
            early_stats,

        "late_turns_5_to_8":
            late_stats,

        "late_minus_early_median_ns":
            late_minus_early,

        "first_to_last_ns":
            first_to_last,

        "raw_timings_ns":
            raw_timings,
    },

    "memory":
        memory_summary,

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
    "=== L.10 A CERTIFICATION RESULT ==="
)

print(
    "Session S:",
    session_s,
)

print(
    "Measured turns:",
    TURN_COUNT,
)

print(
    "Unique measured sessions: 1"
)

print(
    "Unexpected recoveries: 0"
)

print(
    "Unexpected rotations: 0"
)

print(
    "All exact responses: PASS"
)

print(
    "All-turn median:",
    f"{all_stats['median_seconds']:.9f} s",
)

print(
    "Early 1-4 median:",
    f"{early_stats['median_seconds']:.9f} s",
)

print(
    "Late 5-8 median:",
    f"{late_stats['median_seconds']:.9f} s",
)

print(
    "Late - early median:",
    f"{late_minus_early / 1_000_000_000:.9f} s",
)

print(
    "Latency improvement claim supported: False"
)

print(
    "Latency degradation claim supported: False"
)

print(
    "Memory leak claim supported: False"
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
    sha256(
        OUTPUT
    ),
)

print()
print(
    "PHASE 14.11L.10 A ANALYSIS/CERTIFICATION: PASS"
)
