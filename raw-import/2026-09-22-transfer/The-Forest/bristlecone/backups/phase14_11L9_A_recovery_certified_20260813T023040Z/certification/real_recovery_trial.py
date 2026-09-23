from __future__ import annotations

import copy
import hashlib
import json
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
    / "l9_real_recovery_trial_raw.json"
)

MODEL = "bristlecone-qwen35:4b-64k"
BINDING_ID = "binding-0001"

MESSAGE = "Reply only with: L2-COLD-01"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


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


require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing evidence: "
        f"{OUTPUT}"
    ),
)


print(
    "=== L.9D GENUINE HERMES STALE RECOVERY ==="
)


# ------------------------------------------------------------
# WARM SMALL PRECONDITION
# ------------------------------------------------------------

resident_before = resident_models()

print(
    "Resident models:",
    resident_before,
)

require(
    len(resident_before) == 1
    and MODEL in resident_before[0],
    (
        "L.9D requires exactly one warm resident "
        f"Small model: {MODEL}"
    ),
)

print(
    "PASS warm Small precondition"
)


# ------------------------------------------------------------
# REAL FOREST / HERMES SETUP
# ------------------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = manager.load_state()

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
    "L.9D requires Hermes runtime adapter.",
)

governor = (
    build_live_small_resource_governor()
)


# ------------------------------------------------------------
# BENCHMARK-ONLY IN-MEMORY VIEW
#
# Same neutralization approach certified in L.7.
# No persistent Forest modification.
# ------------------------------------------------------------

source_state = copy.deepcopy(
    configured_state
)

source_state["active_ready"] = []

source_task = source_state.get(
    "task_session"
)

require(
    isinstance(
        source_task,
        dict,
    ),
    "Source task_session is not a mapping.",
)

source_task[
    "task_sticky_skills"
] = []

source_task[
    "temporary_capabilities"
] = []


# ------------------------------------------------------------
# FRESH TASK + UNIQUE EXECUTION CONTEXT
# ------------------------------------------------------------

started = manager.start_task(
    state=source_state,
    persist=False,
)

state = started["state"]
task_session = started["task_session"]

task_id = str(
    task_session["id"]
)

context_id = (
    f"l9d-{time.time_ns()}"
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
    "Expected Hermes effort: medium"
)


# ============================================================
# TURN 1
#
# Establish real session S.
# ============================================================

print()
print(
    "Starting establishment turn...",
    flush=True,
)

start_ns = time.perf_counter_ns()

baseline = manager.send_runtime_turn(
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
        "phase14_11L9-real-recovery"
    ),

    resource_request_reasons=(
        "L.9D establishment turn",
    ),

    resource_may_defer=False,
)

baseline_ns = (
    time.perf_counter_ns()
    - start_ns
)


require(
    isinstance(
        baseline,
        dict,
    ),
    "Establishment turn returned non-mapping.",
)

require(
    baseline.get(
        "session_recovered"
    )
    is False,
    (
        "Establishment turn unexpectedly "
        "performed recovery."
    ),
)

require(
    baseline.get(
        "model_form"
    )
    == "small",
    "Establishment turn changed Model Form.",
)

require(
    baseline.get(
        "binding_id"
    )
    == BINDING_ID,
    "Establishment turn changed binding.",
)

require(
    baseline.get(
        "resolved_reasoning_mode"
    )
    == "normal",
    "Establishment turn changed Reasoning.",
)

require(
    baseline.get(
        "execution_context_id"
    )
    == context_id,
    "Establishment turn changed context.",
)

session_s = str(
    baseline.get(
        "session_id"
    )
    or ""
).strip()

require(
    session_s,
    "Establishment turn returned no session ID.",
)

state_after_baseline = baseline.get(
    "state"
)

require(
    isinstance(
        state_after_baseline,
        dict,
    ),
    (
        "Establishment turn returned "
        "no Forest state."
    ),
)


binding_before_delete = binding_for(
    manager,
    state_after_baseline,
    context_id,
)

require(
    isinstance(
        binding_before_delete,
        dict,
    ),
    (
        "Forest binding missing after "
        "establishment turn."
    ),
)

require(
    str(
        binding_before_delete.get(
            "session_id"
        )
        or ""
    )
    == session_s,
    (
        "Forest binding does not point "
        "to session S."
    ),
)


print(
    "PASS establishment session S:",
    session_s,
)

print(
    "Establishment turn:",
    f"{baseline_ns / 1_000_000_000:.9f} s",
)


# ============================================================
# MAKE S STALE ONLY IN HERMES
# ============================================================

print()
print(
    "Deleting S from Hermes only...",
    flush=True,
)

delete_start_ns = (
    time.perf_counter_ns()
)

deleted = runtime_adapter.end_session(
    session_s,
    state_after_baseline,
)

delete_ns = (
    time.perf_counter_ns()
    - delete_start_ns
)


require(
    isinstance(
        deleted,
        dict,
    ),
    "Hermes end_session returned non-mapping.",
)

require(
    deleted.get(
        "session_id"
    )
    == session_s,
    "Hermes deleted unexpected session.",
)

require(
    deleted.get(
        "ended"
    )
    is True,
    "Hermes did not confirm deletion of S.",
)


# Forest state must still point to S.
binding_after_delete = binding_for(
    manager,
    state_after_baseline,
    context_id,
)

require(
    isinstance(
        binding_after_delete,
        dict,
    ),
    (
        "Forest binding disappeared after "
        "Hermes-only deletion."
    ),
)

require(
    str(
        binding_after_delete.get(
            "session_id"
        )
        or ""
    )
    == session_s,
    (
        "Forest binding changed when only "
        "Hermes should have changed."
    ),
)


print(
    "PASS Hermes deleted S"
)

print(
    "PASS Forest still points to stale S"
)

print(
    "Hermes DELETE:",
    f"{delete_ns / 1_000_000:.3f} ms",
)


# ============================================================
# TURN 2
#
# Expected real production path:
#
# Forest reuses stale S
# → Hermes 404/session_not_found
# → stale classifier
# → create replacement R
# → rotate binding S → R
# → retry exact frozen turn once
# ============================================================

print()
print(
    "Starting genuine recovered turn...",
    flush=True,
)

start_ns = time.perf_counter_ns()

recovered = manager.send_runtime_turn(
    MESSAGE,
    state=state_after_baseline,
    instructions=None,
    reasoning_mode="normal",
    persist=False,
    execution_context_id=context_id,
    model_form="small",

    resource_governor=governor,
    resource_priority="standard",

    resource_request_source=(
        "phase14_11L9-real-recovery"
    ),

    resource_request_reasons=(
        "L.9D genuine stale Hermes recovery",
    ),

    resource_may_defer=False,
)

recovery_ns = (
    time.perf_counter_ns()
    - start_ns
)


require(
    isinstance(
        recovered,
        dict,
    ),
    "Recovered turn returned non-mapping.",
)

require(
    recovered.get(
        "session_recovered"
    )
    is True,
    (
        "Production recovery did not report "
        "session_recovered=True."
    ),
)


recovery_from = str(
    recovered.get(
        "recovery_from_session_id"
    )
    or ""
).strip()

recovery_session = str(
    recovered.get(
        "recovery_session_id"
    )
    or ""
).strip()

effective_session = str(
    recovered.get(
        "session_id"
    )
    or ""
).strip()


require(
    recovery_from
    == session_s,
    (
        "recovery_from_session_id "
        "does not equal stale S."
    ),
)

require(
    recovery_session,
    "Recovery returned no replacement R.",
)

require(
    recovery_session
    != session_s,
    "Recovery failed to rotate S → R.",
)

require(
    effective_session
    == recovery_session,
    (
        "Effective session does not "
        "equal replacement R."
    ),
)

require(
    recovered.get(
        "previous_session_id"
    )
    == session_s,
    (
        "Result previous_session_id "
        "does not equal S."
    ),
)

require(
    recovered.get(
        "recovery_binding_persisted"
    )
    is False,
    (
        "persist=False recovery unexpectedly "
        "reported persistent binding."
    ),
)

require(
    isinstance(
        recovered.get(
            "recovery_runtime_result"
        ),
        dict,
    ),
    (
        "Recovery runtime creation result "
        "is missing."
    ),
)

require(
    recovered.get(
        "model_form"
    )
    == "small",
    "Recovery changed Model Form.",
)

require(
    recovered.get(
        "binding_id"
    )
    == BINDING_ID,
    "Recovery changed binding.",
)

require(
    recovered.get(
        "resolved_reasoning_mode"
    )
    == "normal",
    "Recovery changed Reasoning.",
)

require(
    recovered.get(
        "execution_context_id"
    )
    == context_id,
    "Recovery changed execution context.",
)


state_after_recovery = recovered.get(
    "state"
)

require(
    isinstance(
        state_after_recovery,
        dict,
    ),
    "Recovered turn returned no Forest state.",
)


binding_after_recovery = binding_for(
    manager,
    state_after_recovery,
    context_id,
)

require(
    isinstance(
        binding_after_recovery,
        dict,
    ),
    "Forest binding missing after recovery.",
)

require(
    str(
        binding_after_recovery.get(
            "session_id"
        )
        or ""
    )
    == recovery_session,
    (
        "Forest binding did not rotate "
        "to replacement R."
    ),
)

require(
    str(
        binding_after_recovery.get(
            "previous_session_id"
        )
        or ""
    )
    == session_s,
    (
        "Rotated Forest binding did not "
        "retain previous_session_id=S."
    ),
)


print()
print(
    "PASS genuine production recovery"
)

print(
    "Stale S:",
    session_s,
)

print(
    "Replacement R:",
    recovery_session,
)

print(
    "PASS S != R"
)

print(
    "PASS session_recovered=True"
)

print(
    "PASS recovery_from_session_id=S"
)

print(
    "PASS recovery_session_id=R"
)

print(
    "PASS Forest binding rotated S -> R"
)

print(
    "PASS previous_session_id=S"
)

print(
    "PASS Model Form remained Small"
)

print(
    "PASS Reasoning remained Normal"
)

print(
    "PASS binding remained binding-0001"
)

print(
    "PASS execution context remained fixed"
)

print(
    "Recovered turn:",
    f"{recovery_ns / 1_000_000_000:.9f} s",
)


# ============================================================
# BEST-EFFORT CLEANUP OF R
# ============================================================

cleanup = {
    "attempted": True,
    "session_id": recovery_session,
    "success": False,
    "error": None,
}

try:
    ended_r = runtime_adapter.end_session(
        recovery_session,
        state_after_recovery,
    )

    cleanup["success"] = (
        isinstance(
            ended_r,
            dict,
        )
        and ended_r.get(
            "ended"
        )
        is True
    )

except Exception as exc:
    cleanup["error"] = (
        f"{type(exc).__name__}: {exc}"
    )


# ============================================================
# FREEZE EVIDENCE
# ============================================================

payload = {
    "phase":
        "14.11L.9",

    "scenario":
        "genuine-hermes-stale-small-recovery",

    "model":
        MODEL,

    "model_form":
        "small",

    "binding_id":
        BINDING_ID,

    "reasoning_mode":
        "normal",

    "expected_hermes_reasoning_effort":
        "medium",

    "message":
        MESSAGE,

    "task_id":
        task_id,

    "execution_context_id":
        context_id,

    "resident_models_before":
        resident_before,

    "establishment": {
        "timing_ns":
            baseline_ns,

        "timing_seconds":
            baseline_ns
            / 1_000_000_000,

        "session_id":
            session_s,

        "session_recovered":
            False,
    },

    "stale_trigger": {
        "method":
            "real-hermes-end_session",

        "deleted_session_id":
            session_s,

        "delete_timing_ns":
            delete_ns,

        "forest_binding_after_delete":
            session_s,
    },

    "recovery": {
        "timing_ns":
            recovery_ns,

        "timing_seconds":
            recovery_ns
            / 1_000_000_000,

        "session_recovered":
            True,

        "recovery_from_session_id":
            recovery_from,

        "recovery_session_id":
            recovery_session,

        "effective_session_id":
            effective_session,

        "previous_session_id":
            session_s,

        "recovery_binding_persisted":
            recovered.get(
                "recovery_binding_persisted"
            ),

        "recovery_runtime_result":
            recovered.get(
                "recovery_runtime_result"
            ),

        "model_form":
            recovered.get(
                "model_form"
            ),

        "reasoning_mode":
            recovered.get(
                "resolved_reasoning_mode"
            ),

        "binding_id":
            recovered.get(
                "binding_id"
            ),
    },

    "cleanup":
        cleanup,

    "real_hermes_used":
        True,

    "real_small_inference_executed":
        True,

    "production_recovery_logic_used":
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
    "=== L.9D RESULT ==="
)

print(
    "Establishment:",
    f"{baseline_ns / 1_000_000_000:.9f} s",
)

print(
    "Recovered turn:",
    f"{recovery_ns / 1_000_000_000:.9f} s",
)

print(
    "Stale S:",
    session_s,
)

print(
    "Replacement R:",
    recovery_session,
)

print(
    "Replacement cleanup:",
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
    sha256(OUTPUT),
)

print()
print(
    "PHASE 14.11L.9D REAL STALE RECOVERY: PASS"
)
