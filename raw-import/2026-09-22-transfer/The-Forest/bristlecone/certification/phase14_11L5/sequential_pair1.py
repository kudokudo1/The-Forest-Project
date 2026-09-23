from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

from runtime.task_session import TaskSessionManager
from resources.live_providers import (
    build_live_small_resource_governor,
)


ROOT = Path("/home/user/The-Forest/bristlecone")
ACTIVE = ROOT / "state" / "active.yaml"

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l5_sequential_pair1_raw.json"
)

CTX_A = "ctx-l5-seq-a1"
CTX_B = "ctx-l5-seq-b1"

MESSAGE = "Reply only with: L2-COLD-01"

EXPECTED_ACTIVE = (
    "6b8fb9b44757917c1889a7368d43f393"
    "165080d248cdb3d9c5982aad53b270e5"
)


def sha256(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def ollama_ps():
    return subprocess.run(
        ["ollama", "ps"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def resident_lines(raw):
    lines = [
        line
        for line in raw.splitlines()
        if line.strip()
    ]

    if lines and lines[0].startswith("NAME"):
        return lines[1:]

    return lines


def write_json(path, payload):
    temp = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temp.open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            payload,
            handle,
            indent=2,
            sort_keys=True,
            default=str,
        )
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())

    os.replace(temp, path)


if OUTPUT.exists():
    raise RuntimeError(
        "L.5 sequential pair 1 artifact "
        "already exists."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "active.yaml is not frozen."
    )


# --------------------------------------------------
# WARM SHARED-RESIDENCY PRECONDITION
# --------------------------------------------------

resident_before = resident_lines(
    ollama_ps()
)

print("=== L.5A SEQUENTIAL MULTI-CONTEXT — PAIR 1 ===")
print()
print("Resident before:", resident_before)

if (
    len(resident_before) != 1
    or "bristlecone-qwen35:4b-64k"
    not in resident_before[0]
):
    raise RuntimeError(
        "Warm shared-residency precondition failed."
    )


# --------------------------------------------------
# ONE FOREST TASK
# --------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = manager.load_state()

adapter = manager._runtime_adapter_for_state(
    configured_state
)

if type(adapter).__name__ != "HermesRuntimeAdapter":
    raise RuntimeError(
        "Unexpected runtime adapter."
    )

governor = (
    build_live_small_resource_governor()
)

started = manager.start_task(
    state=copy.deepcopy(configured_state),
    persist=False,
)

state = started["state"]
task_id = started["task_session"]["id"]

print("Task:", task_id)
print("Context A:", CTX_A)
print("Context B:", CTX_B)
print()


def send(message, state, context):
    return manager.send_runtime_turn(
        message,
        state=state,
        reasoning_mode="normal",
        persist=False,
        execution_context_id=context,
        model_form="small",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "phase14_11L5-sequential"
        ),
        resource_request_reasons=(
            "sequential multi-context baseline",
        ),
        resource_may_defer=False,
    )


# --------------------------------------------------
# SEQUENTIAL PAIR
# --------------------------------------------------

print("Starting sequential Context A...", flush=True)

pair_start_ns = time.perf_counter_ns()

a_start_ns = time.perf_counter_ns()

output_a = send(
    MESSAGE,
    state,
    CTX_A,
)

a_end_ns = time.perf_counter_ns()

state_after_a = output_a.get("state")

if not isinstance(state_after_a, dict):
    raise RuntimeError(
        "Context A did not return Task-local state."
    )


print("Starting sequential Context B...", flush=True)

b_start_ns = time.perf_counter_ns()

output_b = send(
    MESSAGE,
    state_after_a,
    CTX_B,
)

b_end_ns = time.perf_counter_ns()

pair_end_ns = time.perf_counter_ns()


# --------------------------------------------------
# ASSERT ISOLATION + SHARED BINDING
# --------------------------------------------------

session_a = output_a.get("session_id")
session_b = output_b.get("session_id")

checks = {
    "a_created":
        output_a.get("session_created") is True,

    "b_created":
        output_b.get("session_created") is True,

    "a_not_reused":
        output_a.get("session_reused") is False,

    "b_not_reused":
        output_b.get("session_reused") is False,

    "different_sessions":
        session_a != session_b,

    "a_context":
        output_a.get("execution_context_id")
        == CTX_A,

    "b_context":
        output_b.get("execution_context_id")
        == CTX_B,

    "a_binding":
        output_a.get("binding_id")
        == "binding-0001",

    "b_binding":
        output_b.get("binding_id")
        == "binding-0001",

    "a_small":
        output_a.get("model_form")
        == "small",

    "b_small":
        output_b.get("model_form")
        == "small",

    "a_normal":
        output_a.get("resolved_reasoning_mode")
        == "normal",

    "b_normal":
        output_b.get("resolved_reasoning_mode")
        == "normal",

    "a_no_recovery":
        output_a.get("session_recovered")
        is False,

    "b_no_recovery":
        output_b.get("session_recovered")
        is False,
}

failed = [
    name
    for name, passed in checks.items()
    if not passed
]

if failed:
    raise RuntimeError(
        "L.5 sequential assertions failed: "
        + ", ".join(failed)
    )


final_state = output_b.get("state", {})

runtime_sessions = (
    final_state
    .get("task_session", {})
    .get("runtime_sessions", {})
)

resident_after = resident_lines(
    ollama_ps()
)

if not any(
    "bristlecone-qwen35:4b-64k"
    in line
    for line in resident_after
):
    raise RuntimeError(
        "Shared Small residency disappeared."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "persist=False changed active.yaml."
    )


record = {
    "phase": "14.11L.5A",
    "scenario":
        "sequential-multicontext-shared-residency",
    "pair": 1,

    "task_id": task_id,

    "context_a": CTX_A,
    "context_b": CTX_B,

    "session_a": session_a,
    "session_b": session_b,

    "different_sessions":
        session_a != session_b,

    "binding_a":
        output_a.get("binding_id"),
    "binding_b":
        output_b.get("binding_id"),

    "model_form_a":
        output_a.get("model_form"),
    "model_form_b":
        output_b.get("model_form"),

    "reasoning_a":
        output_a.get("resolved_reasoning_mode"),
    "reasoning_b":
        output_b.get("resolved_reasoning_mode"),

    "session_created_a":
        output_a.get("session_created"),
    "session_created_b":
        output_b.get("session_created"),

    "session_reused_a":
        output_a.get("session_reused"),
    "session_reused_b":
        output_b.get("session_reused"),

    "latency_a_ns":
        a_end_ns - a_start_ns,
    "latency_b_ns":
        b_end_ns - b_start_ns,

    "latency_a_s":
        (a_end_ns - a_start_ns) / 1e9,
    "latency_b_s":
        (b_end_ns - b_start_ns) / 1e9,

    "pair_wall_ns":
        pair_end_ns - pair_start_ns,
    "pair_wall_s":
        (pair_end_ns - pair_start_ns) / 1e9,

    "latency_sum_s":
        (
            (a_end_ns - a_start_ns)
            + (b_end_ns - b_start_ns)
        ) / 1e9,

    "resident_before":
        resident_before,
    "resident_after":
        resident_after,

    "runtime_session_keys":
        sorted(
            str(key)
            for key in runtime_sessions.keys()
        ),

    "persist":
        False,

    "active_yaml_sha":
        EXPECTED_ACTIVE,

    "cleanup_performed":
        False,

    "status":
        "success",
}

write_json(
    OUTPUT,
    record,
)


print()
print("=== L.5A PAIR 1 RESULT ===")
print()

print("Session A:", session_a)
print("Session B:", session_b)
print(
    "Separate sessions:",
    session_a != session_b,
)

print()
print(
    "Latency A s:",
    record["latency_a_s"],
)
print(
    "Latency B s:",
    record["latency_b_s"],
)
print(
    "Latency sum s:",
    record["latency_sum_s"],
)
print(
    "Pair wall s:",
    record["pair_wall_s"],
)

print()
print(
    "Runtime context keys:",
    record["runtime_session_keys"],
)

print(
    "Resident after:",
    resident_after,
)

print()
print("Cleanup performed: False")
print("Evidence:", OUTPUT)
print()
print("L.5A Pair 1 status: 0")
