from __future__ import annotations

import argparse
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

BENCH = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
)

MESSAGE = "Reply only with: L2-COLD-01"

EXPECTED_ACTIVE = (
    "6b8fb9b44757917c1889a7368d43f393"
    "165080d248cdb3d9c5982aad53b270e5"
)

EFFORT_MAP = {
    "light": "low",
    "normal": "medium",
    "deep": "high",
}


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


parser = argparse.ArgumentParser()

parser.add_argument(
    "--mode",
    required=True,
    choices=(
        "light",
        "normal",
        "deep",
    ),
)

parser.add_argument(
    "--trial",
    required=True,
    type=int,
    choices=range(1, 6),
)

args = parser.parse_args()

mode = args.mode
trial = args.trial

context = (
    f"ctx-l6-{mode}-{trial:02d}"
)

output = (
    BENCH
    / f"l6_reasoning_{mode}_trial{trial}_raw.json"
)


# --------------------------------------------------
# DUPLICATE / INTEGRITY GUARDS
# --------------------------------------------------

if output.exists():
    raise RuntimeError(
        f"L.6 {mode} Trial {trial} "
        "artifact already exists; "
        "refusing duplicate inference."
    )

active_sha = sha256(ACTIVE)

if active_sha != EXPECTED_ACTIVE:
    raise RuntimeError(
        "active.yaml is not frozen."
    )


# --------------------------------------------------
# WARM SMALL PRECONDITION
# --------------------------------------------------

resident_before = resident_lines(
    ollama_ps()
)

print(
    f"=== L.6 {mode.upper()} "
    f"REASONING — TRIAL {trial} ==="
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
        "Warm Small residency "
        "precondition failed."
    )


# --------------------------------------------------
# FRESH TASK / CONTEXT / SESSION
# --------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = manager.load_state()

started = manager.start_task(
    state=copy.deepcopy(
        configured_state
    ),
    persist=False,
)

state = started["state"]
task_id = started["task_session"]["id"]

governor = (
    build_live_small_resource_governor()
)

print("Task:", task_id)
print("Context:", context)
print("Forest reasoning:", mode)
print(
    "Expected Hermes effort:",
    EFFORT_MAP[mode],
)

print()
print(
    "Starting timed runtime turn...",
    flush=True,
)


start_ns = time.perf_counter_ns()

result = manager.send_runtime_turn(
    MESSAGE,
    state=state,
    reasoning_mode=mode,
    persist=False,
    execution_context_id=context,
    model_form="small",
    resource_governor=governor,
    resource_priority="standard",
    resource_request_source=(
        "phase14_11L6-reasoning"
    ),
    resource_request_reasons=(
        f"L.6 {mode} reasoning benchmark",
    ),
    resource_may_defer=False,
)

end_ns = time.perf_counter_ns()


# --------------------------------------------------
# ASSERT EXACT SEMANTICS
# --------------------------------------------------

session_id = result.get(
    "session_id"
)

checks = {
    "context":
        result.get(
            "execution_context_id"
        ) == context,

    "session_exists":
        isinstance(
            session_id,
            str,
        )
        and bool(
            session_id.strip()
        ),

    "session_created":
        result.get(
            "session_created"
        ) is True,

    "session_not_reused":
        result.get(
            "session_reused"
        ) is False,

    "session_not_recovered":
        result.get(
            "session_recovered"
        ) is False,

    "binding":
        result.get(
            "binding_id"
        ) == "binding-0001",

    "small":
        result.get(
            "model_form"
        ) == "small",

    "reasoning":
        result.get(
            "resolved_reasoning_mode"
        ) == mode,
}

failed = [
    name
    for name, passed in checks.items()
    if not passed
]

if failed:
    raise RuntimeError(
        "L.6 reasoning assertions failed: "
        + ", ".join(failed)
    )


duration_ns = end_ns - start_ns

resident_after = resident_lines(
    ollama_ps()
)

if not any(
    "bristlecone-qwen35:4b-64k"
    in line
    for line in resident_after
):
    raise RuntimeError(
        "Small residency disappeared."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "persist=False changed active.yaml."
    )


record = {
    "phase":
        "14.11L.6",

    "scenario":
        "warm-small-reasoning-level",

    "trial":
        trial,

    "task_id":
        task_id,

    "execution_context_id":
        context,

    "message":
        MESSAGE,

    "requested_reasoning_mode":
        mode,

    "resolved_reasoning_mode":
        result.get(
            "resolved_reasoning_mode"
        ),

    "expected_hermes_reasoning_effort":
        EFFORT_MAP[mode],

    "model_form":
        result.get(
            "model_form"
        ),

    "binding_id":
        result.get(
            "binding_id"
        ),

    "session_id":
        session_id,

    "session_created":
        result.get(
            "session_created"
        ),

    "session_reused":
        result.get(
            "session_reused"
        ),

    "session_recovered":
        result.get(
            "session_recovered"
        ),

    "duration_ns":
        duration_ns,

    "duration_s":
        duration_ns / 1e9,

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
    output,
    record,
)


print()
print(
    f"=== L.6 {mode.upper()} "
    f"TRIAL {trial} RESULT ==="
)

print()
print(
    "Duration s:",
    record["duration_s"],
)

print(
    "Session:",
    session_id,
)

print(
    "session_created:",
    record["session_created"],
)

print(
    "session_reused:",
    record["session_reused"],
)

print(
    "session_recovered:",
    record["session_recovered"],
)

print(
    "binding:",
    record["binding_id"],
)

print(
    "model_form:",
    record["model_form"],
)

print(
    "reasoning:",
    record["resolved_reasoning_mode"],
)

print(
    "expected Hermes effort:",
    record[
        "expected_hermes_reasoning_effort"
    ],
)

print()
print("Cleanup performed: False")
print("Evidence:", output)
print()

print(
    f"L.6 {mode} Trial {trial} status: 0"
)
