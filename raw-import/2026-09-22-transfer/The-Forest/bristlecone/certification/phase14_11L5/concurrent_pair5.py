from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
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
    / "l5_concurrent_pair5_raw.json"
)

CTX_A = "ctx-l5-con-a5"
CTX_B = "ctx-l5-con-b5"

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

    if (
        lines
        and lines[0].startswith("NAME")
    ):
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
        "L.5 concurrent Pair 5 artifact "
        "already exists; refusing duplicate inference."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "active.yaml is not frozen."
    )


# --------------------------------------------------
# SHARED WARM-RESIDENCY PRECONDITION
# --------------------------------------------------

resident_before = resident_lines(
    ollama_ps()
)

print(
    "=== L.5B CONCURRENT MULTI-CONTEXT — PAIR 5 ==="
)
print()
print(
    "Resident before:",
    resident_before,
)

if (
    len(resident_before) != 1
    or "bristlecone-qwen35:4b-64k"
    not in resident_before[0]
):
    raise RuntimeError(
        "Warm shared-residency precondition failed."
    )


# --------------------------------------------------
# CREATE ONE FOREST TASK
# --------------------------------------------------

base_manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = base_manager.load_state()

started = base_manager.start_task(
    state=copy.deepcopy(configured_state),
    persist=False,
)

base_state = started["state"]
task_id = started["task_session"]["id"]

print("Task:", task_id)
print("Context A:", CTX_A)
print("Context B:", CTX_B)
print()


# --------------------------------------------------
# INDEPENDENT EXECUTION LANES
# --------------------------------------------------

manager_a = TaskSessionManager(
    forest_root=ROOT,
)

manager_b = TaskSessionManager(
    forest_root=ROOT,
)

governor_a = (
    build_live_small_resource_governor()
)

governor_b = (
    build_live_small_resource_governor()
)

state_a = copy.deepcopy(base_state)
state_b = copy.deepcopy(base_state)

barrier = threading.Barrier(3)


def run_context(
    manager,
    governor,
    state,
    context,
):
    # Both workers stop here until A, B, and
    # the coordinating main thread are ready.
    barrier.wait()

    start_ns = time.perf_counter_ns()

    output = manager.send_runtime_turn(
        MESSAGE,
        state=state,
        reasoning_mode="normal",
        persist=False,
        execution_context_id=context,
        model_form="small",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "phase14_11L5-concurrent"
        ),
        resource_request_reasons=(
            "concurrent multi-context "
            "shared-residency benchmark",
        ),
        resource_may_defer=False,
    )

    end_ns = time.perf_counter_ns()

    return {
        "context": context,
        "start_ns": start_ns,
        "end_ns": end_ns,
        "output": output,
    }


print(
    "Launching two synchronized runtime turns...",
    flush=True,
)

with ThreadPoolExecutor(
    max_workers=2
) as executor:

    future_a = executor.submit(
        run_context,
        manager_a,
        governor_a,
        state_a,
        CTX_A,
    )

    future_b = executor.submit(
        run_context,
        manager_b,
        governor_b,
        state_b,
        CTX_B,
    )

    # Release both workers together.
    pair_start_ns = time.perf_counter_ns()

    barrier.wait()

    result_a = future_a.result()
    result_b = future_b.result()

    pair_end_ns = time.perf_counter_ns()


# --------------------------------------------------
# EXTRACT / VALIDATE
# --------------------------------------------------

output_a = result_a["output"]
output_b = result_b["output"]

session_a = output_a.get("session_id")
session_b = output_b.get("session_id")

state_out_a = output_a.get(
    "state",
    {},
)

state_out_b = output_b.get(
    "state",
    {},
)

task_out_a = (
    state_out_a
    .get("task_session", {})
    .get("id")
)

task_out_b = (
    state_out_b
    .get("task_session", {})
    .get("id")
)

runtime_keys_a = sorted(
    str(key)
    for key in (
        state_out_a
        .get("task_session", {})
        .get("runtime_sessions", {})
        .keys()
    )
)

runtime_keys_b = sorted(
    str(key)
    for key in (
        state_out_b
        .get("task_session", {})
        .get("runtime_sessions", {})
        .keys()
    )
)

checks = {
    "same_task_a":
        task_out_a == task_id,

    "same_task_b":
        task_out_b == task_id,

    "a_context":
        output_a.get("execution_context_id")
        == CTX_A,

    "b_context":
        output_b.get("execution_context_id")
        == CTX_B,

    "different_sessions":
        session_a != session_b,

    "a_created":
        output_a.get("session_created")
        is True,

    "b_created":
        output_b.get("session_created")
        is True,

    "a_not_reused":
        output_a.get("session_reused")
        is False,

    "b_not_reused":
        output_b.get("session_reused")
        is False,

    "a_not_recovered":
        output_a.get("session_recovered")
        is False,

    "b_not_recovered":
        output_b.get("session_recovered")
        is False,

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

    # Each independent lane should contain only
    # its own new runtime-context slot.
    "a_isolated":
        runtime_keys_a == [CTX_A],

    "b_isolated":
        runtime_keys_b == [CTX_B],
}

failed = [
    name
    for name, passed in checks.items()
    if not passed
]

if failed:
    raise RuntimeError(
        "L.5 concurrent assertions failed: "
        + ", ".join(failed)
    )


# --------------------------------------------------
# CONCURRENCY MEASUREMENTS
# --------------------------------------------------

a_start = result_a["start_ns"]
a_end = result_a["end_ns"]

b_start = result_b["start_ns"]
b_end = result_b["end_ns"]

latency_a_ns = a_end - a_start
latency_b_ns = b_end - b_start

pair_wall_ns = (
    pair_end_ns - pair_start_ns
)

start_skew_ns = abs(
    a_start - b_start
)

overlap_start = max(
    a_start,
    b_start,
)

overlap_end = min(
    a_end,
    b_end,
)

overlap_ns = max(
    0,
    overlap_end - overlap_start,
)

latency_sum_ns = (
    latency_a_ns
    + latency_b_ns
)

max_latency_ns = max(
    latency_a_ns,
    latency_b_ns,
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
    "phase": "14.11L.5B",
    "scenario":
        "concurrent-multicontext-shared-residency",
    "pair": 5,

    "task_id":
        task_id,

    "context_a":
        CTX_A,
    "context_b":
        CTX_B,

    "session_a":
        session_a,
    "session_b":
        session_b,

    "different_sessions":
        session_a != session_b,

    "runtime_keys_a":
        runtime_keys_a,
    "runtime_keys_b":
        runtime_keys_b,

    "binding_a":
        output_a.get("binding_id"),
    "binding_b":
        output_b.get("binding_id"),

    "model_form_a":
        output_a.get("model_form"),
    "model_form_b":
        output_b.get("model_form"),

    "reasoning_a":
        output_a.get(
            "resolved_reasoning_mode"
        ),
    "reasoning_b":
        output_b.get(
            "resolved_reasoning_mode"
        ),

    "session_created_a":
        output_a.get("session_created"),
    "session_created_b":
        output_b.get("session_created"),

    "session_reused_a":
        output_a.get("session_reused"),
    "session_reused_b":
        output_b.get("session_reused"),

    "latency_a_ns":
        latency_a_ns,
    "latency_b_ns":
        latency_b_ns,

    "latency_a_s":
        latency_a_ns / 1e9,
    "latency_b_s":
        latency_b_ns / 1e9,

    "latency_sum_s":
        latency_sum_ns / 1e9,

    "max_individual_latency_s":
        max_latency_ns / 1e9,

    "pair_wall_ns":
        pair_wall_ns,
    "pair_wall_s":
        pair_wall_ns / 1e9,

    "start_skew_ns":
        start_skew_ns,
    "start_skew_ms":
        start_skew_ns / 1e6,

    "client_overlap_ns":
        overlap_ns,
    "client_overlap_s":
        overlap_ns / 1e9,

    "wall_vs_latency_sum_ratio":
        pair_wall_ns
        / latency_sum_ns,

    "wall_vs_max_latency_ratio":
        pair_wall_ns
        / max_latency_ns,

    "resident_before":
        resident_before,
    "resident_after":
        resident_after,

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
print("=== L.5B CONCURRENT PAIR 5 RESULT ===")
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
    "Max individual s:",
    record["max_individual_latency_s"],
)

print(
    "Concurrent pair wall s:",
    record["pair_wall_s"],
)

print(
    "Start skew ms:",
    record["start_skew_ms"],
)

print(
    "Client-call overlap s:",
    record["client_overlap_s"],
)

print(
    "Wall / latency sum:",
    record["wall_vs_latency_sum_ratio"],
)

print(
    "Wall / max latency:",
    record["wall_vs_max_latency_ratio"],
)

print()
print(
    "Runtime keys A:",
    runtime_keys_a,
)

print(
    "Runtime keys B:",
    runtime_keys_b,
)

print(
    "Resident after:",
    resident_after,
)

print()
print("Cleanup performed: False")
print("Evidence:", OUTPUT)
print()
print("L.5B Pair 5 status: 0")
