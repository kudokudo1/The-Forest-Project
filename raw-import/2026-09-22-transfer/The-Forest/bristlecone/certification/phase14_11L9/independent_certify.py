from __future__ import annotations

import hashlib
import json
import math
import statistics
from pathlib import Path


ROOT = Path("/home/user/The-Forest/bristlecone")

A_ARCHIVE = (
    ROOT
    / "backups"
    / "phase14_11L9_A_recovery_certified_20260813T023040Z"
)

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l9_independent_certification.json"
)

EXPECTED_A_MANIFEST_SHA = (
    "25bf82477b8384c16bed030aeff4418e23fac45988d493c7971af6fe7459a1fa"
)

EXPECTED_A_ANALYZER_SHA = (
    "146437f1e5d76d300ea24e8f26a03e1b8089d9431a5e050b21d41e30e748d308"
)

EXPECTED_A_SUMMARY_SHA = (
    "68b9ef58980c62c3686d90c087b45b020d54a2fa2c7cf119caad0a045abbce4f"
)


EXPECTED_FROZEN = {
    "certification/recovery_control_benchmark.py":
        "4eaa7b4ce6153973f55566fa7087b5aed0b758fc58216aed4c2d4e61869c9eab",

    "certification/hermes_session_cost.py":
        "2e7a911e39c1b4fae8b6f18deb28af0cf14b2994adb84c53702538be87cbf1ac",

    "certification/real_recovery_trial.py":
        "69a83958e9d4f8951b18fbb59825ae664eff93d8ae88b4fb0a380bdff46b5a5f",

    "certification/matched_recovery_benchmark.py":
        "c8d1bc70f629b14f3314fd1c5e89078db1625f9db8af97fd5699c35b8b78e99e",

    "certification/analyze_recovery.py":
        EXPECTED_A_ANALYZER_SHA,

    "benchmarks/l9_recovery_control_raw.json":
        "944c68ded31899f29b5ae1ef6d0f55cca1451b3f065f6e124ccea7bf018a3553",

    "benchmarks/l9_hermes_session_cost_raw.json":
        "cbe31786ff78742442eee72c39282cbcfb888db4b178338605ed4453f104f4f1",

    "benchmarks/l9_real_recovery_trial_raw.json":
        "14ec9478a04c1760677c18c8981449b959f153b7a232c60fd8dd3b48268b7fbf",

    "benchmarks/l9_matched_recovery_raw.json":
        "c66535846e9ec532eef8d1c7f750b0119a20e3b0d66ec81e6ac184e2cb8de944",

    "benchmarks/l9_recovery_summary.json":
        EXPECTED_A_SUMMARY_SHA,
}


REQUIRED_MANIFEST_PATHS = {
    "CERTIFICATION.md",

    "benchmarks/l9_hermes_session_cost_raw.json",
    "benchmarks/l9_matched_recovery_raw.json",
    "benchmarks/l9_real_recovery_trial_raw.json",
    "benchmarks/l9_recovery_control_raw.json",
    "benchmarks/l9_recovery_summary.json",

    "certification/analyze_recovery.py",
    "certification/hermes_session_cost.py",
    "certification/matched_recovery_benchmark.py",
    "certification/real_recovery_trial.py",
    "certification/recovery_control_benchmark.py",

    "source_snapshots/hermes.py",
    "source_snapshots/live_providers.py",
    "source_snapshots/task_session.py",
    "source_snapshots/test_model_form_retry_task_session_integration.py",
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


def median(values):
    require(
        isinstance(values, list)
        and values,
        "Expected non-empty timing list.",
    )

    return statistics.median(
        values
    )


def mean(values):
    require(
        isinstance(values, list)
        and values,
        "Expected non-empty timing list.",
    )

    return statistics.mean(
        values
    )


def stdev(values):
    require(
        isinstance(values, list)
        and values,
        "Expected non-empty timing list.",
    )

    if len(values) <= 1:
        return 0.0

    return statistics.stdev(
        values
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


print(
    "=== L.9 B INDEPENDENT CERTIFICATION ==="
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
    sha256(manifest_path)
    == EXPECTED_A_MANIFEST_SHA,
    (
        "A manifest SHA256 does not "
        "match frozen anchor."
    ),
)


manifest = parse_manifest(
    manifest_path
)


require(
    len(manifest) == 15,
    (
        "Expected 15 manifest entries, "
        f"found {len(manifest)}."
    ),
)

require(
    set(manifest)
    == REQUIRED_MANIFEST_PATHS,
    (
        "A manifest inventory differs "
        "from expected 15 files."
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
        f"Missing archived file: {rel}",
    )

    actual = sha256(
        path
    )

    require(
        actual
        == expected_digest,
        (
            "Manifest validation failed: "
            f"{rel}"
        ),
    )


print(
    "PASS A manifest SHA256"
)

print(
    "PASS A archive inventory 15/15"
)

print(
    "PASS A manifest contents 15/15"
)


# ============================================================
# FROZEN EVIDENCE ANCHORS
# ============================================================

print()
print(
    "Checking frozen evidence anchors..."
)


for rel, expected in (
    EXPECTED_FROZEN.items()
):
    actual = sha256(
        A_ARCHIVE
        / rel
    )

    require(
        actual == expected,
        (
            "Frozen evidence hash mismatch: "
            f"{rel}"
        ),
    )

    print(
        "PASS",
        rel,
        actual,
    )


# ============================================================
# LOAD ARCHIVED RAW EVIDENCE
# ============================================================

control = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l9_recovery_control_raw.json"
)

session = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l9_hermes_session_cost_raw.json"
)

real = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l9_real_recovery_trial_raw.json"
)

matched = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l9_matched_recovery_raw.json"
)

summary = load_json(
    A_ARCHIVE
    / "benchmarks"
    / "l9_recovery_summary.json"
)


for label, artifact in (
    ("control", control),
    ("session", session),
    ("real", real),
    ("matched", matched),
):
    require(
        artifact.get("phase")
        == "14.11L.9",
        f"{label} phase mismatch.",
    )

    require(
        artifact.get("status")
        == "success",
        f"{label} raw status mismatch.",
    )


# ============================================================
# L.9A/B — INDEPENDENT RAW RECOMPUTATION
# ============================================================

print()
print(
    "Independently recomputing L.9A/B..."
)


stale_ns = (
    control[
        "classifier"
    ][
        "stale"
    ][
        "timings_ns"
    ]
)

nonstale_ns = (
    control[
        "classifier"
    ][
        "nonstale"
    ][
        "timings_ns"
    ]
)

normal_ns = (
    control[
        "normal_control"
    ][
        "timings_ns"
    ]
)

recovery_ns = (
    control[
        "recovery_control"
    ][
        "timings_ns"
    ]
)

delta_ns = (
    control[
        "paired_recovery_overhead"
    ][
        "timings_ns"
    ]
)


require(
    len(stale_ns) == 10_000,
    (
        "Stale classifier sample "
        "count mismatch."
    ),
)

require(
    len(nonstale_ns) == 10_000,
    (
        "Non-stale classifier sample "
        "count mismatch."
    ),
)

require(
    len(normal_ns) == 500,
    "Normal control sample count mismatch.",
)

require(
    len(recovery_ns) == 500,
    (
        "Recovery control sample "
        "count mismatch."
    ),
)

require(
    len(delta_ns) == 500,
    (
        "Recovery delta sample "
        "count mismatch."
    ),
)


independent_delta_ns = [
    recovery - normal
    for normal, recovery
    in zip(
        normal_ns,
        recovery_ns,
    )
]


require(
    independent_delta_ns
    == delta_ns,
    (
        "L.9A/B raw paired deltas are "
        "not recovery-normal."
    ),
)


recovery_slower_control = sum(
    value > 0
    for value
    in independent_delta_ns
)


require(
    recovery_slower_control
    == control[
        "paired_recovery_overhead"
    ][
        "recovery_slower_pairs"
    ],
    (
        "L.9A/B recovery-slower "
        "count mismatch."
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
            f"{case_name}: second "
            "error did not escape."
        ),
    )

    require(
        case[
            "session_creations"
        ]
        == 2,
        (
            f"{case_name}: session "
            "creation count mismatch."
        ),
    )

    require(
        case[
            "send_calls"
        ]
        == 2,
        (
            f"{case_name}: send "
            "count mismatch."
        ),
    )

    require(
        case[
            "classifier_calls"
        ]
        == 1,
        (
            f"{case_name}: classifier "
            "count mismatch."
        ),
    )


control_recomputed = {
    "stale_classifier_median_ns":
        median(
            stale_ns
        ),

    "nonstale_classifier_median_ns":
        median(
            nonstale_ns
        ),

    "normal_median_ns":
        median(
            normal_ns
        ),

    "recovery_median_ns":
        median(
            recovery_ns
        ),

    "paired_delta_median_ns":
        median(
            delta_ns
        ),

    "paired_delta_mean_ns":
        mean(
            delta_ns
        ),

    "paired_delta_stdev_ns":
        stdev(
            delta_ns
        ),

    "recovery_slower_pairs":
        recovery_slower_control,
}


print(
    "PASS L.9A/B raw recomputation"
)

print(
    "PASS exactly-one-retry independent check"
)


# ============================================================
# L.9C — REAL HERMES SESSION COST
# ============================================================

print()
print(
    "Independently recomputing L.9C..."
)


samples = session[
    "samples"
]


require(
    len(samples) == 50,
    "L.9C sample count mismatch.",
)

require(
    session[
        "iterations"
    ]
    == 50,
    "L.9C iteration count mismatch.",
)

require(
    session[
        "chat_endpoint_called_by_harness"
    ]
    is False,
    (
        "L.9C claims chat endpoint "
        "was called."
    ),
)

require(
    session[
        "model_turn_executed_by_harness"
    ]
    is False,
    (
        "L.9C claims a model turn ran."
    ),
)

require(
    session[
        "persistent_production_state_modified"
    ]
    is False,
    (
        "L.9C claims persistent mutation."
    ),
)


create_ns = []
end_ns = []
round_trip_ns = []


for index, item in enumerate(
    samples,
    start=1,
):
    create_value = (
        item[
            "create_ns"
        ]
    )

    end_value = (
        item[
            "end_ns"
        ]
    )

    round_value = (
        item[
            "round_trip_ns"
        ]
    )

    require(
        round_value
        == create_value
        + end_value,
        (
            "L.9C round-trip mismatch "
            f"at sample {index}."
        ),
    )

    create_ns.append(
        create_value
    )

    end_ns.append(
        end_value
    )

    round_trip_ns.append(
        round_value
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
    (
        "L.9C round-trip arrays "
        "disagree."
    ),
)


session_recomputed = {
    "create_median_ns":
        median(
            create_ns
        ),

    "end_median_ns":
        median(
            end_ns
        ),

    "round_trip_median_ns":
        median(
            round_trip_ns
        ),
}


print(
    "PASS L.9C 50 raw samples independently recomputed"
)


# ============================================================
# L.9D — GENUINE PRODUCTION STALE RECOVERY
# ============================================================

print()
print(
    "Independently checking L.9D..."
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
    real[
        "real_hermes_used"
    ]
    is True,
    "L.9D did not use real Hermes.",
)

require(
    real[
        "real_small_inference_executed"
    ]
    is True,
    (
        "L.9D did not run real "
        "Small inference."
    ),
)

require(
    real[
        "production_recovery_logic_used"
    ]
    is True,
    (
        "L.9D did not use production "
        "recovery logic."
    ),
)

require(
    real[
        "persistent_production_state_modified"
    ]
    is False,
    (
        "L.9D claims persistent mutation."
    ),
)

require(
    establishment[
        "session_recovered"
    ]
    is False,
    (
        "L.9D establishment "
        "unexpectedly recovered."
    ),
)

require(
    stale[
        "deleted_session_id"
    ]
    == session_s,
    (
        "L.9D deleted ID does "
        "not equal S."
    ),
)

require(
    stale[
        "forest_binding_after_delete"
    ]
    == session_s,
    (
        "L.9D Forest did not "
        "retain stale S."
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
    (
        "L.9D recovery source != S."
    ),
)

require(
    session_r
    and session_r
    != session_s,
    (
        "L.9D replacement R is invalid."
    ),
)

require(
    recovery[
        "effective_session_id"
    ]
    == session_r,
    (
        "L.9D effective session != R."
    ),
)

require(
    recovery[
        "previous_session_id"
    ]
    == session_s,
    (
        "L.9D previous session != S."
    ),
)

require(
    recovery[
        "recovery_binding_persisted"
    ]
    is False,
    (
        "L.9D persist=False "
        "boundary violated."
    ),
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
    is True,
    (
        "L.9D replacement cleanup failed."
    ),
)

require(
    cleanup[
        "session_id"
    ]
    == session_r,
    (
        "L.9D cleanup targeted "
        "wrong session."
    ),
)


print(
    "PASS L.9D independent S -> R semantic check"
)


# ============================================================
# L.9E — MATCHED REAL PAIRS
# ============================================================

print()
print(
    "Independently recomputing L.9E..."
)


pairs = matched[
    "pairs"
]


require(
    matched[
        "pair_count"
    ]
    == 3
    and len(pairs)
    == 3,
    "L.9E pair count mismatch.",
)

require(
    matched[
        "persistent_production_state_modified"
    ]
    is False,
    (
        "L.9E claims persistent mutation."
    ),
)


expected_orders = [
    "normal-recovery",
    "recovery-normal",
    "normal-recovery",
]


matched_normal_ns = []
matched_recovery_ns = []
matched_delta_ns = []


for index, pair in enumerate(
    pairs
):
    pair_number = (
        index + 1
    )

    require(
        pair[
            "order"
        ]
        == expected_orders[index],
        (
            f"L.9E pair {pair_number} "
            "order mismatch."
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
            f"{pair_number} recovered."
        ),
    )

    require(
        recovered[
            "session_recovered"
        ]
        is True,
        (
            f"L.9E recovery pair "
            f"{pair_number} did not recover."
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
            f"{pair_number} changed session."
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
            f"{pair_number} source != stale S."
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
            f"{pair_number} failed S -> R."
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
            f"{pair_number} effective != R."
        ),
    )

    normal_value = normal[
        "timing_ns"
    ]

    recovery_value = recovered[
        "timing_ns"
    ]

    delta_value = (
        recovery_value
        - normal_value
    )

    require(
        pair[
            "delta_ns"
        ]
        == delta_value,
        (
            f"L.9E pair "
            f"{pair_number} delta mismatch."
        ),
    )

    require(
        pair[
            "recovery_slower"
        ]
        is (
            delta_value > 0
        ),
        (
            f"L.9E pair "
            f"{pair_number} slower flag mismatch."
        ),
    )

    matched_normal_ns.append(
        normal_value
    )

    matched_recovery_ns.append(
        recovery_value
    )

    matched_delta_ns.append(
        delta_value
    )


require(
    matched_normal_ns
    == matched[
        "normal"
    ][
        "timings_ns"
    ],
    (
        "L.9E normal sample arrays disagree."
    ),
)

require(
    matched_recovery_ns
    == matched[
        "recovery"
    ][
        "timings_ns"
    ],
    (
        "L.9E recovery sample arrays disagree."
    ),
)

require(
    matched_delta_ns
    == matched[
        "paired_delta"
    ][
        "timings_ns"
    ],
    (
        "L.9E delta arrays disagree."
    ),
)


matched_recovery_slower = sum(
    value > 0
    for value
    in matched_delta_ns
)


require(
    matched_recovery_slower
    == matched[
        "paired_delta"
    ][
        "recovery_slower_pairs"
    ],
    (
        "L.9E recovery-slower "
        "count mismatch."
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
        "L.9E session-create "
        "boundary mismatch."
    ),
)

require(
    boundary[
        "stale_trigger_delete_inside_timed_turn"
    ]
    is False,
    (
        "L.9E stale-delete "
        "boundary mismatch."
    ),
)

require(
    boundary[
        "normal_generation_count_per_timed_turn"
    ]
    == 1,
    (
        "L.9E normal generation "
        "count mismatch."
    ),
)

require(
    boundary[
        "recovery_generation_count_per_timed_turn"
    ]
    == 1,
    (
        "L.9E recovery generation "
        "count mismatch."
    ),
)


matched_recomputed = {
    "normal_median_ns":
        median(
            matched_normal_ns
        ),

    "recovery_median_ns":
        median(
            matched_recovery_ns
        ),

    "paired_delta_median_ns":
        median(
            matched_delta_ns
        ),

    "recovery_slower_pairs":
        matched_recovery_slower,
}


print(
    "PASS L.9E 3/3 pairs independently recomputed"
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
    == "14.11L.9",
    "A summary phase mismatch.",
)

require(
    summary[
        "certification"
    ]
    == "A",
    (
        "A summary certification "
        "label mismatch."
    ),
)

require(
    summary[
        "status"
    ]
    == "PASS",
    (
        "A summary status is not PASS."
    ),
)


require(
    close(
        summary[
            "control"
        ][
            "classifier_stale"
        ][
            "median_ns"
        ],
        control_recomputed[
            "stale_classifier_median_ns"
        ],
    ),
    (
        "A summary stale classifier "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "control"
        ][
            "classifier_nonstale"
        ][
            "median_ns"
        ],
        control_recomputed[
            "nonstale_classifier_median_ns"
        ],
    ),
    (
        "A summary non-stale classifier "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "control"
        ][
            "paired_delta"
        ][
            "median_ns"
        ],
        control_recomputed[
            "paired_delta_median_ns"
        ],
    ),
    (
        "A summary control recovery "
        "median does not match raw."
    ),
)

require(
    summary[
        "control"
    ][
        "recovery_slower_pairs"
    ]
    == control_recomputed[
        "recovery_slower_pairs"
    ],
    (
        "A summary control slower-pair "
        "count does not match raw."
    ),
)


require(
    close(
        summary[
            "hermes_session_cost"
        ][
            "create"
        ][
            "median_ns"
        ],
        session_recomputed[
            "create_median_ns"
        ],
    ),
    (
        "A summary Hermes create "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "hermes_session_cost"
        ][
            "end"
        ][
            "median_ns"
        ],
        session_recomputed[
            "end_median_ns"
        ],
    ),
    (
        "A summary Hermes end "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "hermes_session_cost"
        ][
            "round_trip"
        ][
            "median_ns"
        ],
        session_recomputed[
            "round_trip_median_ns"
        ],
    ),
    (
        "A summary Hermes round-trip "
        "median does not match raw."
    ),
)


require(
    summary[
        "real_recovery"
    ][
        "stale_session_id"
    ]
    == session_s,
    (
        "A summary L.9D stale ID mismatch."
    ),
)

require(
    summary[
        "real_recovery"
    ][
        "replacement_session_id"
    ]
    == session_r,
    (
        "A summary L.9D "
        "replacement ID mismatch."
    ),
)

require(
    summary[
        "real_recovery"
    ][
        "session_recovered"
    ]
    is True,
    (
        "A summary L.9D "
        "recovery flag mismatch."
    ),
)

require(
    summary[
        "real_recovery"
    ][
        "binding_rotated"
    ]
    is True,
    (
        "A summary L.9D "
        "binding flag mismatch."
    ),
)

require(
    summary[
        "real_recovery"
    ][
        "semantic_identity_preserved"
    ]
    is True,
    (
        "A summary L.9D "
        "semantic flag mismatch."
    ),
)

require(
    summary[
        "real_recovery"
    ][
        "cleanup_success"
    ]
    is True,
    (
        "A summary L.9D "
        "cleanup flag mismatch."
    ),
)


require(
    close(
        summary[
            "matched_real"
        ][
            "normal"
        ][
            "median_ns"
        ],
        matched_recomputed[
            "normal_median_ns"
        ],
    ),
    (
        "A summary L.9E normal "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "matched_real"
        ][
            "recovery"
        ][
            "median_ns"
        ],
        matched_recomputed[
            "recovery_median_ns"
        ],
    ),
    (
        "A summary L.9E recovery "
        "median does not match raw."
    ),
)

require(
    close(
        summary[
            "matched_real"
        ][
            "paired_delta"
        ][
            "median_ns"
        ],
        matched_recomputed[
            "paired_delta_median_ns"
        ],
    ),
    (
        "A summary L.9E paired "
        "delta median does not match raw."
    ),
)

require(
    summary[
        "matched_real"
    ][
        "recovery_slower_pairs"
    ]
    == matched_recomputed[
        "recovery_slower_pairs"
    ],
    (
        "A summary L.9E slower-pair "
        "count does not match raw."
    ),
)


require(
    summary[
        "interpretation"
    ][
        "recovery_speedup_claim_supported"
    ]
    is False,
    (
        "A summary incorrectly "
        "supports speedup."
    ),
)

require(
    summary[
        "interpretation"
    ][
        "whole_turn_recovery_cost_cleanly_resolved"
    ]
    is False,
    (
        "A summary incorrectly claims "
        "clean whole-turn resolution."
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
    (
        "A analyzer claims "
        "runtime mutation."
    ),
)

require(
    summary[
        "persistent_production_state_modified"
    ]
    is False,
    (
        "A summary claims "
        "persistent mutation."
    ),
)


print(
    "PASS A summary faithfully represents frozen raw evidence"
)


# ============================================================
# SOURCE SNAPSHOT VS CURRENT PRODUCTION
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

    "retry_test_scaffold": (
        A_ARCHIVE
        / "source_snapshots"
        / "test_model_form_retry_task_session_integration.py",

        ROOT
        / "tests"
        / "test_model_form_retry_task_session_integration.py",
    ),
}


source_hashes = {}


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
        == live_sha,
        (
            "Live production source changed "
            "since A snapshot: "
            f"{name}"
        ),
    )

    source_hashes[name] = (
        live_sha
    )


require(
    control[
        "source_sha256"
    ][
        "task_session"
    ]
    == source_hashes[
        "task_session"
    ],
    (
        "Control task_session "
        "source anchor mismatch."
    ),
)

require(
    control[
        "source_sha256"
    ][
        "retry_test_scaffold"
    ]
    == source_hashes[
        "retry_test_scaffold"
    ],
    (
        "Control retry scaffold "
        "source anchor mismatch."
    ),
)


session_source = session[
    "source_sha256"
]


require(
    session_source[
        "task_session"
    ]
    == source_hashes[
        "task_session"
    ],
    (
        "L.9C task_session "
        "source anchor mismatch."
    ),
)

require(
    session_source[
        "hermes_adapter"
    ]
    == source_hashes[
        "hermes"
    ],
    (
        "L.9C Hermes "
        "source anchor mismatch."
    ),
)


for label, artifact in (
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
        == source_hashes[
            "task_session"
        ],
        (
            f"{label} task_session "
            "source anchor mismatch."
        ),
    )

    require(
        source[
            "hermes"
        ]
        == source_hashes[
            "hermes"
        ],
        (
            f"{label} Hermes "
            "source anchor mismatch."
        ),
    )

    require(
        source[
            "live_providers"
        ]
        == source_hashes[
            "live_providers"
        ],
        (
            f"{label} live-provider "
            "source anchor mismatch."
        ),
    )


require(
    summary[
        "live_source_sha256"
    ]
    == source_hashes,
    (
        "A summary live-source hashes "
        "differ from independently "
        "checked live source."
    ),
)


print(
    "PASS archived/live production source integrity"
)


# ============================================================
# B REPORT
# ============================================================

report = {
    "phase":
        "14.11L.9",

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
        len(
            manifest
        ),

    "a_analyzer_sha256":
        EXPECTED_A_ANALYZER_SHA,

    "a_summary_sha256":
        EXPECTED_A_SUMMARY_SHA,

    "control_recomputed":
        control_recomputed,

    "hermes_session_recomputed":
        session_recomputed,

    "real_recovery": {
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
            True,
    },

    "matched_recomputed":
        matched_recomputed,

    "summary_fidelity":
        True,

    "production_source_integrity":
        True,

    "recovery_speedup_claim_supported":
        False,

    "whole_turn_recovery_cost_cleanly_resolved":
        False,

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
    "=== L.9 B CERTIFICATION RESULT ==="
)

print(
    "Control recovery overhead median:",
    (
        f"{control_recomputed['paired_delta_median_ns'] / 1_000:.3f} us"
    ),
)

print(
    "Hermes create median:",
    (
        f"{session_recomputed['create_median_ns'] / 1_000_000:.6f} ms"
    ),
)

print(
    "Hermes end median:",
    (
        f"{session_recomputed['end_median_ns'] / 1_000_000:.6f} ms"
    ),
)

print(
    "L.9E normal median:",
    (
        f"{matched_recomputed['normal_median_ns'] / 1_000_000_000:.9f} s"
    ),
)

print(
    "L.9E recovery median:",
    (
        f"{matched_recomputed['recovery_median_ns'] / 1_000_000_000:.9f} s"
    ),
)

print(
    "L.9E paired delta median:",
    (
        f"{matched_recomputed['paired_delta_median_ns'] / 1_000_000_000:.9f} s"
    ),
)

print(
    "Recovery speedup claim supported: False"
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
    "PHASE 14.11L.9 B INDEPENDENT CERTIFICATION: PASS"
)
