from __future__ import annotations

import copy
import hashlib
import json
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from runtime.task_session import TaskSessionManager
from resources.live_providers import (
    build_live_small_resource_governor,
)


ROOT = Path("/home/user/The-Forest/bristlecone")

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l10_sustained_session_raw.json"
)

MODEL = "bristlecone-qwen35:4b-64k"
BINDING_ID = "binding-0001"

TURN_COUNT = 8

PRIME_MESSAGE = (
    "Reply only with: L10-PRIME"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def resident_models():
    result = subprocess.run(
        ["ollama", "ps"],
        check=True,
        capture_output=True,
        text=True,
    )

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if (
        lines
        and lines[0].startswith("NAME")
    ):
        lines = lines[1:]

    return lines


def mem_available_kib():
    path = Path(
        "/proc/meminfo"
    )

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():

        if line.startswith(
            "MemAvailable:"
        ):
            parts = line.split()

            require(
                len(parts) >= 2,
                (
                    "Malformed MemAvailable "
                    "line."
                ),
            )

            return int(
                parts[1]
            )

    raise RuntimeError(
        "MemAvailable not found."
    )


def stats(values):
    require(
        values,
        "Cannot summarize empty timing list.",
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


def write_json(
    path,
    payload,
):
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )


require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing "
        f"L.10 evidence: {OUTPUT}"
    ),
)


print(
    "=== L.10 SUSTAINED SAME-SESSION HEALTH ==="
)


# ============================================================
# WARM SMALL PRECONDITION
# ============================================================

resident_before_benchmark = (
    resident_models()
)

print(
    "Resident models:",
    resident_before_benchmark,
)

require(
    len(
        resident_before_benchmark
    )
    == 1
    and MODEL
    in resident_before_benchmark[0],
    (
        "L.10 requires exactly one "
        "warm resident Small model: "
        f"{MODEL}"
    ),
)

print(
    "PASS warm Small precondition"
)


# ============================================================
# FOREST / HERMES SETUP
#
# This follows the certified L.4 same-session pattern:
#
# fresh Task
# fixed execution context
# persist=False
# Small
# Normal
# live Governor
# ============================================================

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = (
    manager.load_state()
)

runtime_adapter = (
    manager._runtime_adapter_for_state(
        configured_state
    )
)

require(
    getattr(
        runtime_adapter,
        "adapter_name",
        None,
    )
    == "hermes",
    (
        "L.10 requires the "
        "Hermes runtime adapter."
    ),
)

governor = (
    build_live_small_resource_governor()
)

working = copy.deepcopy(
    configured_state
)

started = manager.start_task(
    state=working,
    persist=False,
)

state = started[
    "state"
]

task_session = started[
    "task_session"
]

task_id = str(
    task_session[
        "id"
    ]
)

context_id = (
    "l10-sustained-"
    f"{time.time_ns()}"
)


print(
    "Task:",
    task_id,
)

print(
    "Context:",
    context_id,
)

print(
    "Model Form: small"
)

print(
    "Binding:",
    BINDING_ID,
)

print(
    "Reasoning: normal"
)

print(
    "Measured turns:",
    TURN_COUNT,
)


def send(
    message,
    turn_state,
    *,
    reason,
):
    return manager.send_runtime_turn(
        message,

        state=turn_state,

        instructions=None,

        reasoning_mode="normal",

        persist=False,

        execution_context_id=context_id,

        model_form="small",

        resource_governor=governor,

        resource_priority="standard",

        resource_request_source=(
            "phase14_11L10-sustained-session"
        ),

        resource_request_reasons=(
            reason,
        ),

        resource_may_defer=False,
    )


# ============================================================
# UNMEASURED PRIME
#
# Establish exactly one fresh session S.
# ============================================================

print()
print(
    "Starting UNMEASURED prime turn...",
    flush=True,
)

prime = send(
    PRIME_MESSAGE,
    state,
    reason=(
        "L.10 unmeasured sustained-session prime"
    ),
)


require(
    isinstance(
        prime,
        dict,
    ),
    (
        "Prime returned "
        "non-mapping."
    ),
)


session_s = str(
    prime.get(
        "session_id"
    )
    or ""
).strip()


require(
    session_s,
    (
        "Prime returned "
        "no session ID."
    ),
)

require(
    prime.get(
        "session_created"
    )
    is True,
    (
        "Prime did not create "
        "a fresh session."
    ),
)

require(
    prime.get(
        "session_reused"
    )
    is False,
    (
        "Prime unexpectedly "
        "reused a session."
    ),
)

require(
    prime.get(
        "session_recovered"
    )
    is False,
    (
        "Prime unexpectedly "
        "performed recovery."
    ),
)

require(
    prime.get(
        "session_rotated"
    )
    is False,
    (
        "Prime unexpectedly "
        "rotated session."
    ),
)

require(
    prime.get(
        "model_form"
    )
    == "small",
    (
        "Prime changed "
        "Model Form."
    ),
)

require(
    prime.get(
        "resolved_reasoning_mode"
    )
    == "normal",
    (
        "Prime changed "
        "Reasoning."
    ),
)

require(
    prime.get(
        "binding_id"
    )
    == BINDING_ID,
    (
        "Prime changed binding."
    ),
)

require(
    prime.get(
        "execution_context_id"
    )
    == context_id,
    (
        "Prime changed "
        "execution context."
    ),
)


current_state = prime.get(
    "state"
)

require(
    isinstance(
        current_state,
        dict,
    ),
    (
        "Prime did not return "
        "Task-local state."
    ),
)


print(
    "PASS prime created session S:",
    session_s,
)


# ============================================================
# MEASURED REPEATED TURNS
# ============================================================

turns = []
timings_ns = []

benchmark_started_utc = (
    utc_now()
)


for turn_number in range(
    1,
    TURN_COUNT + 1,
):
    print()
    print(
        "=" * 68
    )

    print(
        f"MEASURED TURN "
        f"{turn_number}/{TURN_COUNT}"
    )

    print(
        "=" * 68
    )


    message = (
        "Reply only with: "
        f"L10-T{turn_number:02d}"
    )


    resident_before = (
        resident_models()
    )

    mem_before = (
        mem_available_kib()
    )


    require(
        len(
            resident_before
        )
        == 1
        and MODEL
        in resident_before[0],
        (
            "Small lost warm residency "
            f"before turn {turn_number}."
        ),
    )


    print(
        "Starting timed turn...",
        flush=True,
    )


    start_ns = (
        time.perf_counter_ns()
    )


    try:
        result = send(
            message,
            current_state,
            reason=(
                "L.10 sustained "
                f"measured turn {turn_number}"
            ),
        )

    except Exception as exc:
        end_ns = (
            time.perf_counter_ns()
        )

        failed = {
            "phase":
                "14.11L.10",

            "scenario":
                "sustained-same-session-health",

            "status":
                "failed",

            "failed_turn":
                turn_number,

            "session_s":
                session_s,

            "completed_turns":
                turns,

            "failure_duration_ns":
                end_ns - start_ns,

            "exception_type":
                type(exc).__name__,

            "exception":
                str(exc),

            "persistent_production_state_modified":
                False,

            "completed_utc":
                utc_now(),
        }


        failed_path = OUTPUT.with_name(
            "l10_sustained_session_failed_"
            + datetime.now(
                timezone.utc
            ).strftime(
                "%Y%m%dT%H%M%SZ"
            )
            + ".json"
        )


        write_json(
            failed_path,
            failed,
        )


        print(
            "Failure evidence:",
            failed_path,
        )

        raise


    end_ns = (
        time.perf_counter_ns()
    )

    duration_ns = (
        end_ns - start_ns
    )


    resident_after = (
        resident_models()
    )

    mem_after = (
        mem_available_kib()
    )


    require(
        isinstance(
            result,
            dict,
        ),
        (
            f"Turn {turn_number} "
            "returned non-mapping."
        ),
    )


    measured_session = str(
        result.get(
            "session_id"
        )
        or ""
    ).strip()


    checks = {
        "same_session":
            measured_session
            == session_s,

        "created_false":
            result.get(
                "session_created"
            )
            is False,

        "reused_true":
            result.get(
                "session_reused"
            )
            is True,

        "initial_created_false":
            result.get(
                "initial_session_created"
            )
            is False,

        "not_recovered":
            result.get(
                "session_recovered"
            )
            is False,

        "not_rotated":
            result.get(
                "session_rotated"
            )
            is False,

        "same_context":
            result.get(
                "execution_context_id"
            )
            == context_id,

        "same_binding":
            result.get(
                "binding_id"
            )
            == BINDING_ID,

        "same_model_form":
            result.get(
                "model_form"
            )
            == "small",

        "same_reasoning":
            result.get(
                "resolved_reasoning_mode"
            )
            == "normal",

        "initial_request_is_s":
            result.get(
                "initial_requested_session_id"
            )
            == session_s,

        "requested_session_is_s":
            result.get(
                "requested_session_id"
            )
            == session_s,

        "resident_after":
            (
                len(
                    resident_after
                )
                == 1
                and MODEL
                in resident_after[0]
            ),
    }


    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not passed
    ]


    require(
        not failed_checks,
        (
            f"Turn {turn_number} "
            "failed sustained-session checks: "
            + ", ".join(
                failed_checks
            )
        ),
    )


    returned_state = (
        result.get(
            "state"
        )
    )

    require(
        isinstance(
            returned_state,
            dict,
        ),
        (
            f"Turn {turn_number} "
            "returned no Task-local state."
        ),
    )


    turn_record = {
        "turn":
            turn_number,

        "message":
            message,

        "duration_ns":
            duration_ns,

        "duration_seconds":
            duration_ns
            / 1_000_000_000,

        "session_id":
            measured_session,

        "initial_requested_session_id":
            result.get(
                "initial_requested_session_id"
            ),

        "requested_session_id":
            result.get(
                "requested_session_id"
            ),

        "previous_session_id":
            result.get(
                "previous_session_id"
            ),

        "session_created":
            result.get(
                "session_created"
            ),

        "initial_session_created":
            result.get(
                "initial_session_created"
            ),

        "session_reused":
            result.get(
                "session_reused"
            ),

        "session_recovered":
            result.get(
                "session_recovered"
            ),

        "session_rotated":
            result.get(
                "session_rotated"
            ),

        "model_form":
            result.get(
                "model_form"
            ),

        "reasoning_mode":
            result.get(
                "resolved_reasoning_mode"
            ),

        "binding_id":
            result.get(
                "binding_id"
            ),

        "execution_context_id":
            result.get(
                "execution_context_id"
            ),

        "response_message":
            result.get(
                "message",
                "",
            ),

        "resident_before":
            resident_before,

        "resident_after":
            resident_after,

        "mem_available_before_kib":
            mem_before,

        "mem_available_after_kib":
            mem_after,

        "mem_available_delta_kib":
            mem_after
            - mem_before,

        "checks":
            checks,
    }


    turns.append(
        turn_record
    )

    timings_ns.append(
        duration_ns
    )

    current_state = (
        returned_state
    )


    print(
        "Session:",
        measured_session,
    )

    print(
        "Reuse:",
        result.get(
            "session_reused"
        ),
    )

    print(
        "Recovered:",
        result.get(
            "session_recovered"
        ),
    )

    print(
        "Rotated:",
        result.get(
            "session_rotated"
        ),
    )

    print(
        "Duration:",
        f"{duration_ns / 1_000_000_000:.9f} s",
    )

    print(
        "PASS sustained invariants"
    )


# ============================================================
# CROSS-TURN ASSERTIONS
# ============================================================

require(
    len(turns)
    == TURN_COUNT,
    (
        "Did not complete all "
        "measured turns."
    ),
)


unique_sessions = sorted({
    turn[
        "session_id"
    ]
    for turn in turns
})


require(
    unique_sessions
    == [
        session_s
    ],
    (
        "Measured turns used more "
        "than one runtime session."
    ),
)


require(
    all(
        turn[
            "session_recovered"
        ]
        is False
        for turn in turns
    ),
    (
        "Unexpected recovery occurred "
        "during sustained run."
    ),
)


require(
    all(
        turn[
            "session_rotated"
        ]
        is False
        for turn in turns
    ),
    (
        "Unexpected session rotation "
        "occurred during sustained run."
    ),
)


# ============================================================
# LATENCY / DRIFT DESCRIPTORS
#
# These are descriptive only.
# Eight samples are not enough to claim a causal trend.
# ============================================================

all_stats = stats(
    timings_ns
)

early_ns = (
    timings_ns[:4]
)

late_ns = (
    timings_ns[4:]
)

early_stats = stats(
    early_ns
)

late_stats = stats(
    late_ns
)

late_minus_early_median_ns = (
    late_stats[
        "median_ns"
    ]
    - early_stats[
        "median_ns"
    ]
)

first_to_last_ns = (
    timings_ns[-1]
    - timings_ns[0]
)


# ============================================================
# CLEANUP SESSION S
# ============================================================

print()
print(
    "Cleaning up sustained session S...",
    flush=True,
)


cleanup = {
    "attempted":
        True,

    "session_id":
        session_s,

    "success":
        False,

    "error":
        None,
}


try:
    ended = (
        runtime_adapter.end_session(
            session_s,
            current_state,
        )
    )

    cleanup[
        "success"
    ] = (
        isinstance(
            ended,
            dict,
        )
        and ended.get(
            "ended"
        )
        is True
    )

except Exception as exc:
    cleanup[
        "error"
    ] = (
        f"{type(exc).__name__}: {exc}"
    )


require(
    cleanup[
        "success"
    ]
    is True,
    (
        "Sustained session cleanup "
        "did not succeed."
    ),
)


print(
    "PASS cleanup session S"
)


# ============================================================
# FREEZE RAW EVIDENCE
# ============================================================

payload = {
    "phase":
        "14.11L.10",

    "scenario":
        "sustained-same-session-health",

    "status":
        "success",

    "model":
        MODEL,

    "model_form":
        "small",

    "binding_id":
        BINDING_ID,

    "reasoning_mode":
        "normal",

    "task_id":
        task_id,

    "execution_context_id":
        context_id,

    "prime": {
        "message":
            PRIME_MESSAGE,

        "session_id":
            session_s,

        "session_created":
            True,

        "session_reused":
            False,

        "session_recovered":
            False,

        "session_rotated":
            False,
    },

    "measured_turn_count":
        TURN_COUNT,

    "turns":
        turns,

    "timings_ns":
        timings_ns,

    "timing_stats":
        all_stats,

    "early_turns_1_to_4":
        early_stats,

    "late_turns_5_to_8":
        late_stats,

    "late_minus_early_median_ns":
        late_minus_early_median_ns,

    "late_minus_early_median_seconds":
        late_minus_early_median_ns
        / 1_000_000_000,

    "first_to_last_ns":
        first_to_last_ns,

    "first_to_last_seconds":
        first_to_last_ns
        / 1_000_000_000,

    "unique_measured_session_ids":
        unique_sessions,

    "unexpected_recovery_count":
        sum(
            turn[
                "session_recovered"
            ]
            is True
            for turn in turns
        ),

    "unexpected_rotation_count":
        sum(
            turn[
                "session_rotated"
            ]
            is True
            for turn in turns
        ),

    "resident_models_before_benchmark":
        resident_before_benchmark,

    "cleanup":
        cleanup,

    "measurement_notes": [
        (
            "Prime turn is real but "
            "unmeasured."
        ),
        (
            "All eight measured turns "
            "reuse the prime session."
        ),
        (
            "ollama ps and MemAvailable "
            "sampling occur outside each "
            "timed send boundary."
        ),
        (
            "Early/late latency differences "
            "are descriptive only and do "
            "not establish causal drift."
        ),
    ],

    "real_hermes_used":
        True,

    "real_small_inference_executed":
        True,

    "persistent_production_state_modified":
        False,

    "benchmark_started_utc":
        benchmark_started_utc,

    "benchmark_completed_utc":
        utc_now(),

    "source_sha256": {
        "task_session":
            sha256(
                ROOT
                / "runtime"
                / "task_session.py"
            ),

        "hermes":
            sha256(
                ROOT
                / "runtime"
                / "adapters"
                / "hermes.py"
            ),

        "live_providers":
            sha256(
                ROOT
                / "resources"
                / "live_providers.py"
            ),

        "l4_reuse_foundation":
            sha256(
                ROOT
                / "certification"
                / "phase14_11L4"
                / "reuse_trial1.py"
            ),
    },
}


write_json(
    OUTPUT,
    payload,
)


print()
print(
    "=== L.10 RESULT ==="
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
    "Unique measured sessions:",
    unique_sessions,
)

print(
    "Unexpected recoveries:",
    payload[
        "unexpected_recovery_count"
    ],
)

print(
    "Unexpected rotations:",
    payload[
        "unexpected_rotation_count"
    ],
)

print()
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
        f"{late_minus_early_median_ns / 1_000_000_000:.9f} s"
    ),
)

print(
    "First -> last delta:",
    (
        f"{first_to_last_ns / 1_000_000_000:.9f} s"
    ),
)

print()
print(
    "Cleanup:",
    cleanup,
)

print(
    "Persistent Forest modified: False"
)

print()
print(
    "Evidence:",
    OUTPUT,
)

print()
print(
    "Evidence SHA256:",
    sha256(
        OUTPUT
    ),
)

print()
print(
    "PHASE 14.11L.10 SUSTAINED SESSION: PASS"
)
