from __future__ import annotations

import copy
import hashlib
import json
import statistics
import subprocess
import time
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
    / "l9_matched_recovery_raw.json"
)

MODEL = "bristlecone-qwen35:4b-64k"
BINDING_ID = "binding-0001"
MESSAGE = "Reply only with: L2-COLD-01"

PAIRS = 3


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
        "Cannot summarize empty timing list.",
    )

    ordered = sorted(values)

    return {
        "count":
            len(ordered),

        "median_ns":
            statistics.median(ordered),

        "mean_ns":
            statistics.mean(ordered),

        "stdev_ns":
            (
                statistics.stdev(ordered)
                if len(ordered) > 1
                else 0.0
            ),

        "min_ns":
            ordered[0],

        "max_ns":
            ordered[-1],

        "median_seconds":
            statistics.median(ordered)
            / 1_000_000_000,

        "mean_seconds":
            statistics.mean(ordered)
            / 1_000_000_000,
    }


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

    if lines and lines[0].startswith("NAME"):
        lines = lines[1:]

    return lines


def neutral_source(configured_state):
    state = copy.deepcopy(
        configured_state
    )

    state["active_ready"] = []

    task = state.get(
        "task_session"
    )

    require(
        isinstance(task, dict),
        "Source task_session is not a mapping.",
    )

    task[
        "task_sticky_skills"
    ] = []

    task[
        "temporary_capabilities"
    ] = []

    return state


def binding_for(
    manager,
    state,
    context_id,
):
    return (
        manager
        ._runtime_session_binding_for_identity(
            state,
            context_id,
            BINDING_ID,
        )
    )


def create_bound_session(
    manager,
    runtime_adapter,
    configured_state,
    *,
    label,
):
    """
    Create a fresh Forest Task/context and a real Hermes
    session outside the measured turn.

    The binding write is benchmark setup only and remains
    in memory because persist=False.
    """

    started = manager.start_task(
        state=neutral_source(
            configured_state
        ),
        persist=False,
    )

    state = started["state"]

    task_session = started[
        "task_session"
    ]

    task_id = str(
        task_session["id"]
    )

    context_id = (
        f"l9e-{label}-"
        f"{time.time_ns()}"
    )

    create_start_ns = (
        time.perf_counter_ns()
    )

    created = (
        runtime_adapter.create_session(
            state,
            task_id=task_id,
        )
    )

    create_ns = (
        time.perf_counter_ns()
        - create_start_ns
    )

    require(
        isinstance(created, dict),
        (
            "Hermes create_session returned "
            "non-mapping."
        ),
    )

    require(
        created.get("adapter")
        == "hermes",
        "Created session adapter mismatch.",
    )

    session_id = str(
        created.get(
            "session_id"
        )
        or ""
    ).strip()

    require(
        session_id,
        "Hermes returned no session ID.",
    )

    manager._write_runtime_session_binding_for_identity(
        state,
        context_id,
        BINDING_ID,
        "hermes",
        session_id,
        previous_session_id=None,
    )

    binding = binding_for(
        manager,
        state,
        context_id,
    )

    require(
        isinstance(binding, dict),
        (
            "Benchmark setup failed to "
            "create Forest binding."
        ),
    )

    require(
        str(
            binding.get(
                "session_id"
            )
            or ""
        )
        == session_id,
        (
            "Benchmark Forest binding does "
            "not point to created session."
        ),
    )

    return {
        "state":
            state,

        "task_id":
            task_id,

        "context_id":
            context_id,

        "session_id":
            session_id,

        "create_ns":
            create_ns,
    }


def send_measured_turn(
    manager,
    governor,
    *,
    state,
    context_id,
    label,
):
    start_ns = time.perf_counter_ns()

    result = manager.send_runtime_turn(
        MESSAGE,

        state=state,

        instructions=None,

        reasoning_mode="normal",

        persist=False,

        execution_context_id=context_id,

        model_form="small",

        resource_governor=governor,

        resource_priority="standard",

        resource_request_source=(
            "phase14_11L9-matched-recovery"
        ),

        resource_request_reasons=(
            f"L.9E {label}",
        ),

        resource_may_defer=False,
    )

    elapsed_ns = (
        time.perf_counter_ns()
        - start_ns
    )

    require(
        isinstance(result, dict),
        "Measured turn returned non-mapping.",
    )

    require(
        result.get(
            "model_form"
        )
        == "small",
        "Measured turn changed Model Form.",
    )

    require(
        result.get(
            "binding_id"
        )
        == BINDING_ID,
        "Measured turn changed binding.",
    )

    require(
        result.get(
            "resolved_reasoning_mode"
        )
        == "normal",
        "Measured turn changed Reasoning.",
    )

    require(
        result.get(
            "execution_context_id"
        )
        == context_id,
        (
            "Measured turn changed "
            "execution context."
        ),
    )

    return elapsed_ns, result


def cleanup_session(
    runtime_adapter,
    state,
    session_id,
):
    cleanup = {
        "attempted": False,
        "success": False,
        "session_id": session_id,
        "error": None,
    }

    if not session_id:
        return cleanup

    cleanup["attempted"] = True

    try:
        ended = (
            runtime_adapter.end_session(
                session_id,
                state,
            )
        )

        cleanup["success"] = (
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
        cleanup["error"] = (
            f"{type(exc).__name__}: {exc}"
        )

    return cleanup


require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing evidence: "
        f"{OUTPUT}"
    ),
)


print(
    "=== L.9E MATCHED NORMAL VS RECOVERED ==="
)


# ============================================================
# PRECONDITION
# ============================================================

resident_before = resident_models()

print(
    "Resident models:",
    resident_before,
)

require(
    len(resident_before) == 1
    and MODEL in resident_before[0],
    (
        "L.9E requires exactly one warm resident "
        f"Small model: {MODEL}"
    ),
)

print(
    "PASS warm Small precondition"
)


# ============================================================
# REAL FOREST / HERMES
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
    "L.9E requires Hermes runtime adapter.",
)

governor = (
    build_live_small_resource_governor()
)


# ============================================================
# THREE MATCHED PAIRS
#
# Pair order alternates:
#
# 1 normal → recovery
# 2 recovery → normal
# 3 normal → recovery
#
# Session creation / stale-trigger DELETE are outside the
# measured turn.
# ============================================================

pairs = []

normal_ns = []
recovery_ns = []
delta_ns = []


def run_normal(pair_index):
    setup = create_bound_session(
        manager,
        runtime_adapter,
        configured_state,
        label=(
            f"pair{pair_index}-normal"
        ),
    )

    result = None
    cleanup = None

    try:
        elapsed_ns, result = (
            send_measured_turn(
                manager,
                governor,
                state=setup["state"],
                context_id=setup[
                    "context_id"
                ],
                label=(
                    f"pair {pair_index} normal"
                ),
            )
        )

        require(
            result.get(
                "session_recovered"
            )
            is False,
            (
                "Normal condition unexpectedly "
                "performed recovery."
            ),
        )

        require(
            result.get(
                "initial_session_created"
            )
            is False,
            (
                "Normal measured turn unexpectedly "
                "created its initial session."
            ),
        )

        require(
            result.get(
                "session_reused"
            )
            is True,
            (
                "Normal measured turn did not "
                "reuse precreated session."
            ),
        )

        require(
            result.get(
                "session_id"
            )
            == setup["session_id"],
            (
                "Normal turn changed "
                "session identity."
            ),
        )

        return {
            "timing_ns":
                elapsed_ns,

            "timing_seconds":
                elapsed_ns
                / 1_000_000_000,

            "task_id":
                setup["task_id"],

            "execution_context_id":
                setup["context_id"],

            "setup_session_id":
                setup["session_id"],

            "setup_create_ns":
                setup["create_ns"],

            "session_id":
                result.get(
                    "session_id"
                ),

            "session_recovered":
                False,
        }

    finally:
        if result is not None:
            cleanup_state = result.get(
                "state",
                setup["state"],
            )

            cleanup_id = result.get(
                "session_id",
                setup["session_id"],
            )

        else:
            cleanup_state = setup[
                "state"
            ]

            cleanup_id = setup[
                "session_id"
            ]

        cleanup = cleanup_session(
            runtime_adapter,
            cleanup_state,
            cleanup_id,
        )

        print(
            "Normal cleanup:",
            cleanup,
        )


def run_recovery(pair_index):
    setup = create_bound_session(
        manager,
        runtime_adapter,
        configured_state,
        label=(
            f"pair{pair_index}-recovery"
        ),
    )

    stale_s = setup[
        "session_id"
    ]

    delete_start_ns = (
        time.perf_counter_ns()
    )

    deleted = (
        runtime_adapter.end_session(
            stale_s,
            setup["state"],
        )
    )

    delete_ns = (
        time.perf_counter_ns()
        - delete_start_ns
    )

    require(
        isinstance(
            deleted,
            dict,
        )
        and deleted.get(
            "ended"
        )
        is True,
        (
            "Could not delete recovery "
            "setup session S."
        ),
    )

    binding = binding_for(
        manager,
        setup["state"],
        setup["context_id"],
    )

    require(
        isinstance(binding, dict),
        (
            "Forest binding disappeared "
            "after Hermes DELETE."
        ),
    )

    require(
        str(
            binding.get(
                "session_id"
            )
            or ""
        )
        == stale_s,
        (
            "Forest no longer points "
            "to stale S."
        ),
    )

    result = None

    try:
        elapsed_ns, result = (
            send_measured_turn(
                manager,
                governor,
                state=setup["state"],
                context_id=setup[
                    "context_id"
                ],
                label=(
                    f"pair {pair_index} recovery"
                ),
            )
        )

        require(
            result.get(
                "session_recovered"
            )
            is True,
            (
                "Recovery condition did not "
                "perform genuine recovery."
            ),
        )

        require(
            result.get(
                "initial_session_created"
            )
            is False,
            (
                "Recovery measured turn "
                "created an initial session "
                "instead of reusing stale S."
            ),
        )

        require(
            result.get(
                "session_reused"
            )
            is True,
            (
                "Recovery measured turn did "
                "not initially reuse stale S."
            ),
        )

        recovery_from = str(
            result.get(
                "recovery_from_session_id"
            )
            or ""
        )

        replacement_r = str(
            result.get(
                "recovery_session_id"
            )
            or ""
        )

        require(
            recovery_from
            == stale_s,
            (
                "Recovery source does not "
                "equal stale S."
            ),
        )

        require(
            replacement_r
            and replacement_r
            != stale_s,
            (
                "Recovery did not create "
                "distinct replacement R."
            ),
        )

        require(
            result.get(
                "session_id"
            )
            == replacement_r,
            (
                "Effective session does not "
                "equal replacement R."
            ),
        )

        require(
            result.get(
                "previous_session_id"
            )
            == stale_s,
            (
                "previous_session_id "
                "does not equal S."
            ),
        )

        require(
            result.get(
                "recovery_binding_persisted"
            )
            is False,
            (
                "persist=False recovery "
                "unexpectedly persisted binding."
            ),
        )

        return {
            "timing_ns":
                elapsed_ns,

            "timing_seconds":
                elapsed_ns
                / 1_000_000_000,

            "task_id":
                setup["task_id"],

            "execution_context_id":
                setup["context_id"],

            "setup_session_id":
                stale_s,

            "setup_create_ns":
                setup["create_ns"],

            "stale_delete_ns":
                delete_ns,

            "recovery_from_session_id":
                recovery_from,

            "recovery_session_id":
                replacement_r,

            "effective_session_id":
                result.get(
                    "session_id"
                ),

            "session_recovered":
                True,
        }

    finally:
        if result is not None:
            replacement = result.get(
                "session_id"
            )

            cleanup_state = result.get(
                "state",
                setup["state"],
            )

            cleanup = cleanup_session(
                runtime_adapter,
                cleanup_state,
                replacement,
            )

            print(
                "Recovery cleanup:",
                cleanup,
            )


for pair_index in range(
    1,
    PAIRS + 1,
):
    print()
    print(
        "=" * 68
    )

    print(
        f"PAIR {pair_index}/{PAIRS}"
    )

    print(
        "=" * 68
    )

    if pair_index % 2 == 1:
        print(
            "Order: normal → recovery"
        )

        print(
            "Starting normal turn...",
            flush=True,
        )

        normal = run_normal(
            pair_index
        )

        print(
            "Normal:",
            f"{normal['timing_seconds']:.9f} s",
        )

        print(
            "Starting recovered turn...",
            flush=True,
        )

        recovery = run_recovery(
            pair_index
        )

        print(
            "Recovery:",
            f"{recovery['timing_seconds']:.9f} s",
        )

    else:
        print(
            "Order: recovery → normal"
        )

        print(
            "Starting recovered turn...",
            flush=True,
        )

        recovery = run_recovery(
            pair_index
        )

        print(
            "Recovery:",
            f"{recovery['timing_seconds']:.9f} s",
        )

        print(
            "Starting normal turn...",
            flush=True,
        )

        normal = run_normal(
            pair_index
        )

        print(
            "Normal:",
            f"{normal['timing_seconds']:.9f} s",
        )


    pair_delta = (
        recovery["timing_ns"]
        - normal["timing_ns"]
    )

    pair = {
        "pair":
            pair_index,

        "order":
            (
                "normal-recovery"
                if pair_index % 2 == 1
                else "recovery-normal"
            ),

        "normal":
            normal,

        "recovery":
            recovery,

        "delta_ns":
            pair_delta,

        "delta_seconds":
            pair_delta
            / 1_000_000_000,

        "recovery_slower":
            pair_delta > 0,
    }

    pairs.append(pair)

    normal_ns.append(
        normal["timing_ns"]
    )

    recovery_ns.append(
        recovery["timing_ns"]
    )

    delta_ns.append(
        pair_delta
    )

    print(
        "Pair delta recovery-normal:",
        f"{pair_delta / 1_000_000_000:.9f} s",
    )


# ============================================================
# SUMMARIZE
# ============================================================

normal_stats = stats(
    normal_ns
)

recovery_stats = stats(
    recovery_ns
)

delta_stats = stats(
    delta_ns
)


print()
print(
    "=== L.9E SUMMARY ==="
)

print(
    "Normal median:",
    f"{normal_stats['median_seconds']:.9f} s",
)

print(
    "Recovery median:",
    f"{recovery_stats['median_seconds']:.9f} s",
)

print(
    "Paired delta median:",
    f"{delta_stats['median_seconds']:.9f} s",
)

print(
    "Recovery slower pairs:",
    sum(
        value > 0
        for value in delta_ns
    ),
    "/",
    PAIRS,
)


# ============================================================
# FREEZE RAW EVIDENCE
# ============================================================

payload = {
    "phase":
        "14.11L.9",

    "scenario":
        "matched-normal-vs-genuine-recovery",

    "pairs":
        pairs,

    "pair_count":
        PAIRS,

    "model":
        MODEL,

    "binding_id":
        BINDING_ID,

    "model_form":
        "small",

    "reasoning_mode":
        "normal",

    "expected_hermes_reasoning_effort":
        "medium",

    "message":
        MESSAGE,

    "resident_models_before":
        resident_before,

    "normal": {
        "timings_ns":
            normal_ns,

        "stats":
            normal_stats,
    },

    "recovery": {
        "timings_ns":
            recovery_ns,

        "stats":
            recovery_stats,
    },

    "paired_delta": {
        "timings_ns":
            delta_ns,

        "stats":
            delta_stats,

        "recovery_slower_pairs":
            sum(
                value > 0
                for value in delta_ns
            ),
    },

    "measurement_boundary": {
        "session_creation_inside_timed_turn":
            False,

        "stale_trigger_delete_inside_timed_turn":
            False,

        "normal_generation_count_per_timed_turn":
            1,

        "recovery_generation_count_per_timed_turn":
            1,

        "recovery_timed_turn_includes":
            [
                "stale-send",
                "stale-classification",
                "replacement-session-creation",
                "Forest-binding-rotation",
                "one-retry",
                "one-Small-generation",
            ],
    },

    "real_hermes_used":
        True,

    "real_small_inference_executed":
        True,

    "persistent_production_state_modified":
        False,

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
    },

    "status":
        "success",
}


OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        default=str,
    )
    + "\n"
)


print()
print(
    "Raw normal samples:",
    normal_ns,
)

print(
    "Raw recovery samples:",
    recovery_ns,
)

print(
    "Raw paired deltas:",
    delta_ns,
)

print()
print(
    "Evidence:",
    OUTPUT,
)

print()
print(
    "Evidence SHA256:",
    sha256(OUTPUT),
)

print()
print(
    "PHASE 14.11L.9E MATCHED RECOVERY: PASS"
)
