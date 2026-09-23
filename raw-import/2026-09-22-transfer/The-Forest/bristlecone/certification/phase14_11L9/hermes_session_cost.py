from __future__ import annotations

import hashlib
import json
import statistics
import time
from pathlib import Path

from runtime.task_session import (
    TaskSessionManager,
)


ROOT = Path(
    "/home/user/The-Forest/bristlecone"
)

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l9_hermes_session_cost_raw.json"
)

WARMUPS = 5
ITERATIONS = 50


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def stats(values):
    require(
        values,
        "Cannot summarize empty timing samples.",
    )

    ordered = sorted(values)
    count = len(ordered)

    p95_index = min(
        count - 1,
        max(
            0,
            (95 * count + 99) // 100 - 1,
        ),
    )

    return {
        "count":
            count,
        "median_ns":
            statistics.median(ordered),
        "mean_ns":
            statistics.mean(ordered),
        "stdev_ns":
            (
                statistics.stdev(ordered)
                if count > 1
                else 0.0
            ),
        "min_ns":
            ordered[0],
        "max_ns":
            ordered[-1],
        "p95_ns":
            ordered[p95_index],
        "median_us":
            statistics.median(ordered)
            / 1_000,
        "mean_us":
            statistics.mean(ordered)
            / 1_000,
    }


require(
    not OUTPUT.exists(),
    f"Refusing to overwrite existing artifact: {OUTPUT}",
)


# ------------------------------------------------------------
# REAL FOREST / HERMES SETUP
# ------------------------------------------------------------

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
    "L.9C requires the real Hermes runtime adapter.",
)


print(
    "=== L.9C REAL HERMES SESSION COST ==="
)

print(
    "Adapter:",
    runtime_adapter.adapter_name,
)

print(
    "Warmups:",
    WARMUPS,
)

print(
    "Measured iterations:",
    ITERATIONS,
)


# ------------------------------------------------------------
# ONE CREATE + END OPERATION
# ------------------------------------------------------------

def create_and_end(
    task_id,
    *,
    measured,
):
    session_id = None

    try:
        create_start = (
            time.perf_counter_ns()
        )

        created = (
            runtime_adapter.create_session(
                configured_state,
                task_id=task_id,
            )
        )

        create_end = (
            time.perf_counter_ns()
        )

        require(
            isinstance(
                created,
                dict,
            ),
            "Hermes create_session returned non-mapping.",
        )

        require(
            created.get(
                "adapter"
            )
            == "hermes",
            "Hermes create_session adapter mismatch.",
        )

        session_id = str(
            created.get(
                "session_id"
            )
            or ""
        ).strip()

        require(
            session_id,
            "Hermes create_session returned no session ID.",
        )

        end_start = (
            time.perf_counter_ns()
        )

        ended = (
            runtime_adapter.end_session(
                session_id,
                configured_state,
            )
        )

        end_end = (
            time.perf_counter_ns()
        )

        require(
            isinstance(
                ended,
                dict,
            ),
            "Hermes end_session returned non-mapping.",
        )

        require(
            ended.get(
                "session_id"
            )
            == session_id,
            "Hermes ended wrong session.",
        )

        require(
            ended.get(
                "ended"
            )
            is True,
            "Hermes did not confirm session deletion.",
        )

        return {
            "session_id":
                session_id,
            "create_ns":
                create_end
                - create_start,
            "end_ns":
                end_end
                - end_start,
            "round_trip_ns":
                (
                    create_end
                    - create_start
                    + end_end
                    - end_start
                ),
            "measured":
                measured,
        }

    except Exception:
        # If creation succeeded but measurement failed before
        # normal deletion, make a best-effort cleanup.
        if session_id:
            try:
                runtime_adapter.end_session(
                    session_id,
                    configured_state,
                )
            except Exception:
                pass

        raise


# ------------------------------------------------------------
# UNMEASURED WARMUP
# ------------------------------------------------------------

print()
print(
    "Running unmeasured create/end warmups...",
    flush=True,
)

for index in range(
    WARMUPS
):
    create_and_end(
        f"l9c-warmup-{index}",
        measured=False,
    )


# ------------------------------------------------------------
# MEASURED REAL HERMES SESSION OPERATIONS
# ------------------------------------------------------------

print(
    "Running measured create/end operations...",
    flush=True,
)

samples = []

for index in range(
    ITERATIONS
):
    sample = create_and_end(
        f"l9c-measured-{index}",
        measured=True,
    )

    samples.append(
        sample
    )


create_ns = [
    sample["create_ns"]
    for sample in samples
]

end_ns = [
    sample["end_ns"]
    for sample in samples
]

round_trip_ns = [
    sample["round_trip_ns"]
    for sample in samples
]


create_stats = stats(
    create_ns
)

end_stats = stats(
    end_ns
)

round_trip_stats = stats(
    round_trip_ns
)


print()
print(
    "PASS Hermes create_session median:",
    f"{create_stats['median_us']:.3f} us",
)

print(
    "PASS Hermes end_session median:",
    f"{end_stats['median_us']:.3f} us",
)

print(
    "PASS create+end median:",
    f"{round_trip_stats['median_us']:.3f} us",
)


# ------------------------------------------------------------
# RAW EVIDENCE
# ------------------------------------------------------------

payload = {
    "phase":
        "14.11L.9",
    "scenario":
        "real-hermes-session-create-end-cost",

    "adapter":
        "hermes",

    "warmups":
        WARMUPS,

    "iterations":
        ITERATIONS,

    # Preserve every observation so Terminal B can
    # recompute all statistics independently.
    "samples": samples,

    "create_session": {
        "timings_ns":
            create_ns,
        "stats":
            create_stats,
    },

    "end_session": {
        "timings_ns":
            end_ns,
        "stats":
            end_stats,
    },

    "create_end_round_trip": {
        "timings_ns":
            round_trip_ns,
        "stats":
            round_trip_stats,
    },

    "chat_endpoint_called_by_harness":
        False,

    "model_turn_executed_by_harness":
        False,

    "forest_binding_persisted":
        False,

    "persistent_production_state_modified":
        False,

    "transient_hermes_sessions_created":
        ITERATIONS + WARMUPS,

    "transient_hermes_sessions_deleted":
        ITERATIONS + WARMUPS,

    "source_sha256": {
        "task_session":
            sha256(
                ROOT
                / "runtime"
                / "task_session.py"
            ),

        "hermes_adapter":
            sha256(
                ROOT
                / "runtime"
                / "adapters"
                / "hermes.py"
            ),
    },

    "status":
        "success",
}


OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print()
print(
    "=== L.9C RESULT ==="
)

print(
    "Hermes create median:",
    f"{create_stats['median_us']:.3f} us",
)

print(
    "Hermes end median:",
    f"{end_stats['median_us']:.3f} us",
)

print(
    "Create+end median:",
    f"{round_trip_stats['median_us']:.3f} us",
)

print(
    "Raw measured samples retained:",
    len(samples),
)

print(
    "Chat endpoint called: False"
)

print(
    "Persistent Forest state modified: False"
)

print()
print("Evidence:")
print(OUTPUT)

print()
print("Evidence SHA256:")
print(
    sha256(OUTPUT)
)

print()
print(
    "PHASE 14.11L.9C HERMES SESSION COST: PASS"
)
