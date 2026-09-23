from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path


ROOT = Path(
    "/home/user/The-Forest/bristlecone"
)

A_ARCHIVE = (
    ROOT
    / "backups"
    / "phase14_11L10_A_sustained_certified_20260813T033046Z"
)

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l10_independent_certification.json"
)


EXPECTED_A_MANIFEST_SHA = (
    "3dccc25349079a1dc2ce79f9be5f66506e0c1f9eed3b59ebe4a10152378736e0"
)

EXPECTED_A_ANALYZER_SHA = (
    "7a9a5800159f63791108bf77fa7c95467c1fa8190dab7164829fe889d035ad9d"
)

EXPECTED_A_SUMMARY_SHA = (
    "99884aff29cba88c8057f916b83b6dad537aa26a29e850737ca471942454fd46"
)

EXPECTED_HARNESS_SHA = (
    "f2397758642dd7c51c2240608df4846dfc8ee80258abf11619e392fa34a3bed4"
)

EXPECTED_RAW_SHA = (
    "e592c4ff7fa339b18a977cd1da0412a74035caee6c8f16a403f1b51a0697f6f7"
)


EXPECTED_SOURCE_SHA = {
    "task_session":
        "d666cb1471b568bf43db4255f5e84e98c1ea502af467e1e2670e4a93dc364991",

    "hermes":
        "a09949eead5cb9772aca312c91630703c7ff8ce43df778730279445b25635084",

    "live_providers":
        "40b49375dbe014b27b6fc5696bccf74274864e42953c473b42ffe10a3c552299",

    "l4_reuse_foundation":
        "ce343935d5c8078d3c9f802609d662a2650f9a4e269b1f209967f3aac7a5d9dd",
}


REQUIRED_MANIFEST_PATHS = {
    "CERTIFICATION.md",

    "benchmarks/l10_sustained_session_raw.json",
    "benchmarks/l10_sustained_session_summary.json",

    "certification/analyze_sustained_session.py",
    "certification/sustained_session_benchmark.py",

    "source_snapshots/hermes.py",
    "source_snapshots/l4_reuse_trial1.py",
    "source_snapshots/live_providers.py",
    "source_snapshots/task_session.py",
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


def parse_manifest(path):
    entries = {}

    for raw_line in path.read_text(
        encoding="utf-8"
    ).splitlines():

        line = raw_line.strip()

        if not line:
            continue

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip()

        if rel.startswith("*"):
            rel = rel[1:]

        if rel.startswith("./"):
            rel = rel[2:]

        require(
            rel not in entries,
            f"Duplicate manifest path: {rel}",
        )

        entries[rel] = digest

    return entries


def recompute(values):
    require(
        isinstance(values, list)
        and values,
        "Expected non-empty numeric list.",
    )

    ordered = sorted(
        values
    )

    return {
        "count":
            len(values),

        "median_ns":
            statistics.median(
                values
            ),

        "mean_ns":
            statistics.mean(
                values
            ),

        "stdev_ns":
            (
                statistics.stdev(
                    values
                )
                if len(values) > 1
                else 0.0
            ),

        "min_ns":
            ordered[0],

        "max_ns":
            ordered[-1],

        "median_seconds":
            statistics.median(
                values
            )
            / 1_000_000_000,

        "mean_seconds":
            statistics.mean(
                values
            )
            / 1_000_000_000,
    }


def compare_stats(
    label,
    calculated,
    stored,
):
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
            f"{label} missing {key}.",
        )

        require(
            close(
                calculated[key],
                stored[key],
            ),
            (
                f"{label} {key} mismatch: "
                f"{calculated[key]!r} "
                f"!= {stored[key]!r}"
            ),
        )


print(
    "=== L.10 B INDEPENDENT CERTIFICATION ==="
)


# ============================================================
# A ARCHIVE / MANIFEST
# ============================================================

require(
    A_ARCHIVE.is_dir(),
    f"Missing A archive: {A_ARCHIVE}",
)

require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing "
        f"B report: {OUTPUT}"
    ),
)


manifest_path = (
    A_ARCHIVE
    / "MANIFEST.sha256"
)


print()
print(
    "Checking A archive anchor..."
)


require(
    sha256(
        manifest_path
    )
    == EXPECTED_A_MANIFEST_SHA,
    "A manifest SHA256 mismatch.",
)


manifest = parse_manifest(
    manifest_path
)


require(
    len(manifest)
    == 9,
    (
        "Expected 9 manifest entries, "
        f"found {len(manifest)}."
    ),
)

require(
    set(manifest)
    == REQUIRED_MANIFEST_PATHS,
    (
        "A archive inventory differs "
        "from expected 9 files."
    ),
)


for rel, expected_digest in (
    manifest.items()
):
    path = (
        A_ARCHIVE
        / rel
    )

    require(
        path.is_file(),
        f"Missing archive file: {rel}",
    )

    require(
        sha256(path)
        == expected_digest,
        (
            "Manifest validation "
            f"failed for {rel}."
        ),
    )


print(
    "PASS A manifest SHA256"
)

print(
    "PASS A archive inventory 9/9"
)

print(
    "PASS A manifest contents 9/9"
)


# ============================================================
# FROZEN ARTIFACT ANCHORS
# ============================================================

print()
print(
    "Checking frozen artifact anchors..."
)


require(
    sha256(
        A_ARCHIVE
        / "certification"
        / "sustained_session_benchmark.py"
    )
    == EXPECTED_HARNESS_SHA,
    "Frozen harness SHA mismatch.",
)

require(
    sha256(
        A_ARCHIVE
        / "certification"
        / "analyze_sustained_session.py"
    )
    == EXPECTED_A_ANALYZER_SHA,
    "Frozen A analyzer SHA mismatch.",
)

require(
    sha256(
        A_ARCHIVE
        / "benchmarks"
        / "l10_sustained_session_raw.json"
    )
    == EXPECTED_RAW_SHA,
    "Frozen raw SHA mismatch.",
)

require(
    sha256(
        A_ARCHIVE
        / "benchmarks"
        / "l10_sustained_session_summary.json"
    )
    == EXPECTED_A_SUMMARY_SHA,
    "Frozen A summary SHA mismatch.",
)


print(
    "PASS frozen harness"
)

print(
    "PASS frozen A analyzer"
)

print(
    "PASS frozen raw evidence"
)

print(
    "PASS frozen A summary"
)


# ============================================================
# LOAD ARCHIVED RAW + SUMMARY
# ============================================================

raw = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l10_sustained_session_raw.json"
)

summary = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l10_sustained_session_summary.json"
)


require(
    raw.get("phase")
    == "14.11L.10",
    "Raw phase mismatch.",
)

require(
    raw.get("scenario")
    == "sustained-same-session-health",
    "Raw scenario mismatch.",
)

require(
    raw.get("status")
    == "success",
    "Raw status is not success.",
)

require(
    raw.get("model")
    == MODEL,
    "Raw model mismatch.",
)

require(
    raw.get("model_form")
    == "small",
    "Raw Model Form mismatch.",
)

require(
    raw.get("binding_id")
    == BINDING,
    "Raw binding mismatch.",
)

require(
    raw.get("reasoning_mode")
    == "normal",
    "Raw Reasoning mismatch.",
)

require(
    raw.get("measured_turn_count")
    == TURN_COUNT,
    "Raw turn count mismatch.",
)


# ============================================================
# PRIME
# ============================================================

print()
print(
    "Independently checking prime..."
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
    "Prime session S missing.",
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
    "Prime unexpectedly reused.",
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
    "PASS prime established fresh S"
)


# ============================================================
# 8 MEASURED TURNS
# ============================================================

print()
print(
    "Independently checking 8 measured turns..."
)


turns = raw[
    "turns"
]


require(
    isinstance(
        turns,
        list,
    )
    and len(turns)
    == TURN_COUNT,
    "Expected exactly 8 turn records.",
)


timings = []
memory_before = []
memory_after = []
memory_deltas = []


for index, turn in enumerate(
    turns,
    start=1,
):
    label = (
        f"T{index:02d}"
    )

    expected_prompt = (
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
        f"{label} number mismatch.",
    )

    require(
        turn[
            "message"
        ]
        == expected_prompt,
        f"{label} prompt mismatch.",
    )

    require(
        turn[
            "response_message"
        ]
        == expected_response,
        f"{label} response mismatch.",
    )

    require(
        turn[
            "session_id"
        ]
        == session_s,
        f"{label} session != S.",
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
        f"{label} created session.",
    )

    require(
        turn[
            "initial_session_created"
        ]
        is False,
        (
            f"{label} initial session "
            "was created."
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
        f"{label} recovered unexpectedly.",
    )

    require(
        turn[
            "session_rotated"
        ]
        is False,
        f"{label} rotated unexpectedly.",
    )

    require(
        turn[
            "model_form"
        ]
        == "small",
        f"{label} Model Form drift.",
    )

    require(
        turn[
            "reasoning_mode"
        ]
        == "normal",
        f"{label} Reasoning drift.",
    )

    require(
        turn[
            "binding_id"
        ]
        == BINDING,
        f"{label} binding drift.",
    )

    require(
        turn[
            "execution_context_id"
        ]
        == raw[
            "execution_context_id"
        ],
        f"{label} context drift.",
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
        f"{label} check map missing.",
    )

    require(
        all(
            value is True
            for value
            in checks.values()
        ),
        f"{label} stored failed check.",
    )


    resident_before = turn[
        "resident_before"
    ]

    resident_after = turn[
        "resident_after"
    ]


    require(
        len(resident_before)
        == 1
        and MODEL
        in resident_before[0],
        (
            f"{label} Small was not "
            "resident before turn."
        ),
    )

    require(
        len(resident_after)
        == 1
        and MODEL
        in resident_after[0],
        (
            f"{label} Small was not "
            "resident after turn."
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
            f"{label} memory delta "
            "arithmetic mismatch."
        ),
    )


    duration_ns = turn[
        "duration_ns"
    ]


    require(
        duration_ns > 0,
        f"{label} invalid duration.",
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
            "mismatch."
        ),
    )


    timings.append(
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
    "PASS 8/8 residency observations"
)

print(
    "PASS 8/8 memory arithmetic checks"
)


# ============================================================
# CROSS-TURN STABILITY
# ============================================================

print()
print(
    "Checking sustained session stability..."
)


require(
    raw[
        "unique_measured_session_ids"
    ]
    == [
        session_s
    ],
    (
        "Unique-session list "
        "is not exactly [S]."
    ),
)

require(
    raw[
        "unexpected_recovery_count"
    ]
    == 0,
    "Recovery count is not zero.",
)

require(
    raw[
        "unexpected_rotation_count"
    ]
    == 0,
    "Rotation count is not zero.",
)

require(
    all(
        turn[
            "session_id"
        ]
        == session_s
        for turn in turns
    ),
    "Session identity was not stable.",
)


print(
    "PASS one S across all measured turns"
)

print(
    "PASS zero recovery"
)

print(
    "PASS zero rotation"
)


# ============================================================
# INDEPENDENT TIMING RECOMPUTATION
# ============================================================

print()
print(
    "Independently recomputing timing statistics..."
)


require(
    timings
    == raw[
        "timings_ns"
    ],
    (
        "Per-turn timings disagree "
        "with top-level timing array."
    ),
)


all_stats = recompute(
    timings
)

early_stats = recompute(
    timings[:4]
)

late_stats = recompute(
    timings[4:]
)


compare_stats(
    "raw all-turn stats",
    all_stats,
    raw[
        "timing_stats"
    ],
)

compare_stats(
    "raw early stats",
    early_stats,
    raw[
        "early_turns_1_to_4"
    ],
)

compare_stats(
    "raw late stats",
    late_stats,
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

first_to_last = (
    timings[-1]
    - timings[0]
)


require(
    close(
        raw[
            "late_minus_early_median_ns"
        ],
        late_minus_early,
    ),
    (
        "Raw late-minus-early "
        "median mismatch."
    ),
)

require(
    raw[
        "first_to_last_ns"
    ]
    == first_to_last,
    "Raw first-to-last mismatch.",
)


print(
    "PASS raw timing statistics independently recomputed"
)


# ============================================================
# CLEANUP / SAFETY
# ============================================================

print()
print(
    "Checking cleanup and safety boundaries..."
)


cleanup = raw[
    "cleanup"
]


require(
    cleanup[
        "attempted"
    ]
    is True,
    "Cleanup not attempted.",
)

require(
    cleanup[
        "success"
    ]
    is True,
    "Cleanup unsuccessful.",
)

require(
    cleanup[
        "session_id"
    ]
    == session_s,
    "Cleanup targeted wrong session.",
)

require(
    cleanup[
        "error"
    ]
    is None,
    "Cleanup recorded error.",
)

require(
    raw[
        "real_hermes_used"
    ]
    is True,
    "Raw did not record real Hermes.",
)

require(
    raw[
        "real_small_inference_executed"
    ]
    is True,
    "Raw did not record real Small inference.",
)

require(
    raw[
        "persistent_production_state_modified"
    ]
    is False,
    "Raw claims persistent mutation.",
)


print(
    "PASS cleanup and persist=False boundary"
)


# ============================================================
# A SUMMARY FIDELITY
# ============================================================

print()
print(
    "Checking A summary fidelity..."
)


require(
    summary[
        "phase"
    ]
    == "14.11L.10",
    "A summary phase mismatch.",
)

require(
    summary[
        "certification"
    ]
    == "A",
    "A certification label mismatch.",
)

require(
    summary[
        "status"
    ]
    == "PASS",
    "A summary status is not PASS.",
)


require(
    summary[
        "frozen_sha256"
    ][
        "harness"
    ]
    == EXPECTED_HARNESS_SHA,
    "A summary harness hash mismatch.",
)

require(
    summary[
        "frozen_sha256"
    ][
        "raw"
    ]
    == EXPECTED_RAW_SHA,
    "A summary raw hash mismatch.",
)


session_summary = summary[
    "session"
]


require(
    session_summary[
        "session_s"
    ]
    == session_s,
    "A summary session S mismatch.",
)

require(
    session_summary[
        "measured_turn_count"
    ]
    == TURN_COUNT,
    "A summary turn count mismatch.",
)

require(
    session_summary[
        "unique_measured_session_ids"
    ]
    == [
        session_s
    ],
    "A summary unique sessions mismatch.",
)

require(
    session_summary[
        "unexpected_recovery_count"
    ]
    == 0,
    "A summary recovery count mismatch.",
)

require(
    session_summary[
        "unexpected_rotation_count"
    ]
    == 0,
    "A summary rotation count mismatch.",
)

require(
    session_summary[
        "all_exact_responses"
    ]
    is True,
    "A summary exact-response flag false.",
)

require(
    session_summary[
        "all_residency_checks"
    ]
    is True,
    "A summary residency flag false.",
)

require(
    session_summary[
        "cleanup_success"
    ]
    is True,
    "A summary cleanup flag false.",
)


timing_summary = summary[
    "timing"
]


compare_stats(
    "A all-turn stats",
    all_stats,
    timing_summary[
        "all_turns"
    ],
)

compare_stats(
    "A early stats",
    early_stats,
    timing_summary[
        "early_turns_1_to_4"
    ],
)

compare_stats(
    "A late stats",
    late_stats,
    timing_summary[
        "late_turns_5_to_8"
    ],
)


require(
    timing_summary[
        "raw_timings_ns"
    ]
    == timings,
    "A summary timing samples mismatch.",
)

require(
    close(
        timing_summary[
            "late_minus_early_median_ns"
        ],
        late_minus_early,
    ),
    (
        "A summary late-minus-early "
        "mismatch."
    ),
)

require(
    timing_summary[
        "first_to_last_ns"
    ]
    == first_to_last,
    (
        "A summary first-to-last "
        "mismatch."
    ),
)


memory_summary = summary[
    "memory"
]


require(
    memory_summary[
        "before_samples_kib"
    ]
    == memory_before,
    "A memory-before samples mismatch.",
)

require(
    memory_summary[
        "after_samples_kib"
    ]
    == memory_after,
    "A memory-after samples mismatch.",
)

require(
    memory_summary[
        "per_turn_delta_kib"
    ]
    == memory_deltas,
    "A memory-delta samples mismatch.",
)

require(
    close(
        memory_summary[
            "median_per_turn_delta_kib"
        ],
        statistics.median(
            memory_deltas
        ),
    ),
    (
        "A memory median delta "
        "mismatch."
    ),
)

require(
    close(
        memory_summary[
            "mean_per_turn_delta_kib"
        ],
        statistics.mean(
            memory_deltas
        ),
    ),
    (
        "A memory mean delta "
        "mismatch."
    ),
)

require(
    memory_summary[
        "first_before_kib"
    ]
    == memory_before[0],
    "A first memory sample mismatch.",
)

require(
    memory_summary[
        "last_after_kib"
    ]
    == memory_after[-1],
    "A last memory sample mismatch.",
)

require(
    memory_summary[
        "last_after_minus_first_before_kib"
    ]
    == (
        memory_after[-1]
        - memory_before[0]
    ),
    "A memory endpoint delta mismatch.",
)

require(
    memory_summary[
        "memory_leak_claim_supported"
    ]
    is False,
    (
        "A summary incorrectly "
        "supports memory leak claim."
    ),
)


interpretation = summary[
    "interpretation"
]


require(
    interpretation[
        "sustained_session_health_supported"
    ]
    is True,
    "A does not support sustained health.",
)

require(
    interpretation[
        "session_identity_stable"
    ]
    is True,
    "A session-stability flag false.",
)

require(
    interpretation[
        "semantic_drift_observed"
    ]
    is False,
    "A claims semantic drift.",
)

require(
    interpretation[
        "unexpected_recovery_observed"
    ]
    is False,
    "A claims unexpected recovery.",
)

require(
    interpretation[
        "unexpected_rotation_observed"
    ]
    is False,
    "A claims unexpected rotation.",
)

require(
    interpretation[
        "latency_improvement_claim_supported"
    ]
    is False,
    (
        "A incorrectly supports "
        "latency improvement."
    ),
)

require(
    interpretation[
        "latency_degradation_claim_supported"
    ]
    is False,
    (
        "A incorrectly supports "
        "latency degradation."
    ),
)

require(
    interpretation[
        "memory_leak_claim_supported"
    ]
    is False,
    (
        "A incorrectly supports "
        "memory leak."
    ),
)

require(
    summary[
        "inference_run_by_analyzer"
    ]
    is False,
    "A analyzer claims inference.",
)

require(
    summary[
        "runtime_mutation_by_analyzer"
    ]
    is False,
    "A analyzer claims runtime mutation.",
)

require(
    summary[
        "persistent_production_state_modified"
    ]
    is False,
    "A summary claims persistent mutation.",
)


print(
    "PASS A summary faithfully represents raw evidence"
)


# ============================================================
# ARCHIVED SOURCE SNAPSHOTS VS CURRENT PRODUCTION
# ============================================================

print()
print(
    "Checking archived source snapshots against live production..."
)


SOURCE_MAP = {
    "task_session": (
        A_ARCHIVE
        / "source_snapshots"
        / "task_session.py",

        ROOT
        / "runtime"
        / "task_session.py",
    ),

    "hermes": (
        A_ARCHIVE
        / "source_snapshots"
        / "hermes.py",

        ROOT
        / "runtime"
        / "adapters"
        / "hermes.py",
    ),

    "live_providers": (
        A_ARCHIVE
        / "source_snapshots"
        / "live_providers.py",

        ROOT
        / "resources"
        / "live_providers.py",
    ),

    "l4_reuse_foundation": (
        A_ARCHIVE
        / "source_snapshots"
        / "l4_reuse_trial1.py",

        ROOT
        / "certification"
        / "phase14_11L4"
        / "reuse_trial1.py",
    ),
}


live_source_sha = {}


for name, (
    snapshot,
    live,
) in SOURCE_MAP.items():

    snapshot_sha = sha256(
        snapshot
    )

    live_sha = sha256(
        live
    )

    require(
        snapshot_sha
        == EXPECTED_SOURCE_SHA[
            name
        ],
        (
            "Archived source hash "
            f"mismatch: {name}"
        ),
    )

    require(
        live_sha
        == EXPECTED_SOURCE_SHA[
            name
        ],
        (
            "Live source hash "
            f"mismatch: {name}"
        ),
    )

    require(
        snapshot_sha
        == live_sha,
        (
            "Archived/live source "
            f"differ: {name}"
        ),
    )

    live_source_sha[
        name
    ] = live_sha


require(
    raw[
        "source_sha256"
    ]
    == live_source_sha,
    (
        "Raw embedded source hashes "
        "differ from independently "
        "verified live source."
    ),
)

require(
    summary[
        "source_sha256"
    ]
    == live_source_sha,
    (
        "A summary source hashes "
        "differ from independently "
        "verified live source."
    ),
)


print(
    "PASS archived/live source integrity"
)


# ============================================================
# INDEPENDENT INTERPRETATION
# ============================================================

independent_interpretation = {
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

    "latency_improvement_claim_supported":
        False,

    "latency_degradation_claim_supported":
        False,

    "memory_leak_claim_supported":
        False,

    "reason":
        (
            "Eight consecutive measured real Small turns "
            "reused one runtime session and preserved "
            "Model Form, Reasoning, binding, execution "
            "context, exact expected responses, and warm "
            "residency with no recovery or rotation. "
            "The timing sample is too small and variable "
            "to support improvement or degradation claims. "
            "System-wide MemAvailable observations are not "
            "process-attributed and therefore do not "
            "establish a memory leak."
        ),
}


# ============================================================
# WRITE B REPORT
# ============================================================

report = {
    "phase":
        "14.11L.10",

    "certification":
        "B",

    "status":
        "PASS",

    "a_archive":
        str(
            A_ARCHIVE
        ),

    "a_manifest_sha256":
        EXPECTED_A_MANIFEST_SHA,

    "a_manifest_entries":
        9,

    "a_analyzer_sha256":
        EXPECTED_A_ANALYZER_SHA,

    "a_summary_sha256":
        EXPECTED_A_SUMMARY_SHA,

    "frozen_harness_sha256":
        EXPECTED_HARNESS_SHA,

    "frozen_raw_sha256":
        EXPECTED_RAW_SHA,

    "session": {
        "session_s":
            session_s,

        "measured_turn_count":
            TURN_COUNT,

        "unique_session_count":
            1,

        "unexpected_recovery_count":
            0,

        "unexpected_rotation_count":
            0,

        "exact_response_count":
            TURN_COUNT,

        "cleanup_success":
            True,
    },

    "timing_recomputed": {
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
            timings,
    },

    "memory_recomputed": {
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
    },

    "summary_fidelity":
        True,

    "production_source_integrity":
        True,

    "interpretation":
        independent_interpretation,

    "inference_executed_by_certifier":
        False,

    "runtime_mutation_by_certifier":
        False,

    "persistent_production_state_modified":
        False,
}


OUTPUT.write_text(
    json.dumps(
        report,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


print()
print(
    "=== L.10 B CERTIFICATION RESULT ==="
)

print(
    "Session S:",
    session_s,
)

print(
    "Measured turns: 8"
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
    "Exact responses: 8 / 8"
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
    (
        f"{late_minus_early / 1_000_000_000:.9f} s"
    ),
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
    "Inference executed by certifier: False"
)

print(
    "Runtime mutation by certifier: False"
)

print()
print(
    "Report:",
    OUTPUT,
)

print()
print(
    "Report SHA256:",
    sha256(
        OUTPUT
    ),
)

print()
print(
    "PHASE 14.11L.10 B INDEPENDENT CERTIFICATION: PASS"
)
