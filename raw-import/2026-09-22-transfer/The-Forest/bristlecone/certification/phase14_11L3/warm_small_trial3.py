from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from runtime.task_session import TaskSessionManager
from resources.live_providers import (
    build_live_small_resource_governor,
)


ROOT = Path("/home/user/The-Forest/bristlecone")
ACTIVE = ROOT / "state" / "active.yaml"

OUTPUT_DIR = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

SUCCESS_PATH = (
    OUTPUT_DIR
    / "l3_warm_small_trial3_raw.json"
)

IN_PROGRESS_PATH = (
    OUTPUT_DIR
    / "l3_warm_small_trial3_in_progress.json"
)

CTX = "ctx-l3-warm-03"

MESSAGE = (
    "Reply only with: L2-COLD-01"
)

EXPECTED_BINDING = "binding-0001"
EXPECTED_MODEL_FORM = "small"
EXPECTED_REASONING = "normal"

EXPECTED_ACTIVE_SHA = (
    "6b8fb9b44757917c1889a7368d43f393"
    "165080d248cdb3d9c5982aad53b270e5"
)

EXPECTED_PRODUCTION = {
    ROOT / "runtime/task_session.py":
        "d666cb1471b568bf43db4255f5e84e98"
        "c1ea502af467e1e2670e4a93dc364991",

    ROOT / "runtime/session_store.py":
        "3c3449fa878920ea27f39b6216cf38a6"
        "87d09a08da1d5b57af68c1a2f4beb48f",

    ROOT / "runtime/session_identity.py":
        "8a1d668e898dc2df7b60fd5099be0cf4"
        "2dd2d4c864cbe163164f0a061a777353",

    ROOT / "runtime/adapters/hermes.py":
        "a09949eead5cb9772aca312c91630703c"
        "7ff8ce43df778730279445b25635084",

    ROOT / "resources/live_providers.py":
        "40b49375dbe014b27b6fc5696bccf7427"
        "4864e42953c473b42ffe10a3c552299",

    ROOT / "model_form/bindings.yaml":
        "74110afd51de7ceddd02948d0430b0f9f"
        "1b5443a6eaaaa0b8a6e4164a52b0583",
}


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def sha256(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def run_readonly(command):
    result = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )

    return result.stdout


def ollama_ps():
    return run_readonly(
        ["ollama", "ps"]
    )


def resident_model_lines(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return []

    # ollama ps prints a header even when empty.
    if lines[0].startswith("NAME"):
        return lines[1:]

    return lines


def hermes_state():
    raw = run_readonly([
        "systemctl",
        "--user",
        "show",
        "hermes-bristlecone.service",
        "-p",
        "ActiveState",
        "-p",
        "SubState",
        "-p",
        "MainPID",
    ])

    parsed = {}

    for line in raw.splitlines():
        if "=" not in line:
            continue

        key, value = line.split(
            "=",
            1,
        )

        parsed[key] = value

    return parsed


def llama_server_lines():
    raw = run_readonly([
        "ps",
        "-eo",
        "pid=,args=",
    ])

    return [
        line.strip()
        for line in raw.splitlines()
        if "llama-server" in line
    ]


def runtime_socket_lines():
    raw = run_readonly([
        "ss",
        "-tnp",
    ])

    return [
        line.strip()
        for line in raw.splitlines()
        if (
            ":8643" in line
            or ":11434" in line
        )
    ]


def mem_available_kib():
    for line in Path(
        "/proc/meminfo"
    ).read_text(
        encoding="utf-8"
    ).splitlines():

        if line.startswith(
            "MemAvailable:"
        ):
            return int(
                line.split()[1]
            )

    return None


def load_average():
    one, five, fifteen = os.getloadavg()

    return {
        "1m": one,
        "5m": five,
        "15m": fifteen,
    }


def snapshot():
    ps_text = ollama_ps()

    return {
        "utc": utc_now(),
        "cpu_count": os.cpu_count(),
        "mem_available_kib":
            mem_available_kib(),
        "load_average":
            load_average(),
        "hermes":
            hermes_state(),
        "ollama_ps_raw":
            ps_text,
        "resident_models":
            resident_model_lines(
                ps_text
            ),
        "llama_server":
            llama_server_lines(),
        "runtime_sockets":
            runtime_socket_lines(),
    }


def write_json(path, payload):
    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temporary.open(
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
        os.fsync(
            handle.fileno()
        )

    os.replace(
        temporary,
        path,
    )


def assert_frozen():
    active_sha = sha256(
        ACTIVE
    )

    if active_sha != EXPECTED_ACTIVE_SHA:
        raise RuntimeError(
            "active.yaml is not at "
            "the certified baseline."
        )

    for path, expected in (
        EXPECTED_PRODUCTION.items()
    ):
        actual = sha256(
            path
        )

        if actual != expected:
            raise RuntimeError(
                "Frozen production file "
                f"changed: {path}"
            )

    return active_sha


def selected_result(output):
    if not isinstance(
        output,
        dict,
    ):
        return {
            "type":
                type(output).__name__,
            "repr":
                repr(output)[:2000],
        }

    keys = (
        "adapter",
        "binding_id",
        "binding_persisted",
        "binding_persisted_before_turn",
        "execution_context_id",
        "initial_requested_session_id",
        "initial_session_created",
        "model_form",
        "model_form_source",
        "requested_session_id",
        "resolved_reasoning_mode",
        "session_created",
        "session_id",
        "session_recovered",
        "session_reused",
        "session_rotated",
    )

    selected = {
        key: output.get(key)
        for key in keys
    }

    selected[
        "runtime_result_type"
    ] = type(
        output.get(
            "runtime_result"
        )
    ).__name__

    selected[
        "runtime_result_repr"
    ] = repr(
        output.get(
            "runtime_result"
        )
    )[:3000]

    return selected


# --------------------------------------------------
# REFUSE AMBIGUOUS RERUNS
# --------------------------------------------------

if SUCCESS_PATH.exists():
    raise RuntimeError(
        "Successful L.2 Trial 1 "
        "artifact already exists. "
        "Refusing duplicate real inference."
    )

if IN_PROGRESS_PATH.exists():
    raise RuntimeError(
        "An L.2 Trial 3 in-progress "
        "artifact already exists. "
        "Inspect it before rerunning."
    )


# --------------------------------------------------
# FROZEN BASELINE
# --------------------------------------------------

print(
    "=== 14.11L.3 WARM SMALL — TRIAL 3 ==="
)
print()

active_before = assert_frozen()

before = snapshot()

print(
    "Hermes before:",
    before["hermes"],
)

print(
    "Resident before:",
    before["resident_models"],
)

print(
    "llama-server before:",
    before["llama_server"],
)

print(
    "runtime sockets before:",
    before["runtime_sockets"],
)

resident_before = (
    before["resident_models"]
)

if (
    len(resident_before) != 1
    or "bristlecone-qwen35:4b-64k"
    not in resident_before[0]
):
    raise RuntimeError(
        "Warm precondition failed: "
        "expected exactly one resident "
        "bristlecone-qwen35:4b-64k model."
    )

if not before["llama_server"]:
    raise RuntimeError(
        "Warm precondition failed: "
        "llama-server is not active."
    )

if before["runtime_sockets"]:
    raise RuntimeError(
        "Warm precondition failed: "
        "a prior runtime socket is active."
    )

hermes = before["hermes"]

if (
    hermes.get("ActiveState")
    != "active"
    or hermes.get("SubState")
    != "running"
    or hermes.get("MainPID")
    in (None, "", "0")
):
    raise RuntimeError(
        "Hermes is not healthy."
    )


# --------------------------------------------------
# PREPARE FOREST TURN OUTSIDE TIMER
# --------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = (
    manager.load_state()
)

adapter = (
    manager._runtime_adapter_for_state(
        configured_state
    )
)

if (
    type(adapter).__name__
    != "HermesRuntimeAdapter"
):
    raise RuntimeError(
        "Configured adapter is not "
        "HermesRuntimeAdapter."
    )

governor = (
    build_live_small_resource_governor()
)

state = copy.deepcopy(
    configured_state
)

started = manager.start_task(
    state=state,
    persist=False,
)

state = started["state"]

task_id = (
    started["task_session"]["id"]
)

if not task_id:
    raise RuntimeError(
        "Fresh benchmark Task "
        "was not created."
    )

attempt = {
    "phase": "14.11L.3",
    "trial": 3,
    "scenario":
        "warm-resident-fresh-session",
    "started_utc":
        utc_now(),
    "task_id":
        task_id,
    "execution_context_id":
        CTX,
    "message":
        MESSAGE,
    "model_form":
        EXPECTED_MODEL_FORM,
    "reasoning_mode":
        EXPECTED_REASONING,
    "binding_expected":
        EXPECTED_BINDING,
    "persist":
        False,
    "before":
        before,
    "active_yaml_sha_before":
        active_before,
    "status":
        "in_progress",
}

write_json(
    IN_PROGRESS_PATH,
    attempt,
)

print()
print("Task:", task_id)
print("Context:", CTX)
print(
    "Adapter:",
    type(adapter).__name__,
)
print(
    "Governor:",
    type(governor).__name__,
)
print()
print(
    "Starting timed REAL Small turn...",
    flush=True,
)


# --------------------------------------------------
# ONLY THIS INTERVAL IS THE BENCHMARK
# --------------------------------------------------

start_ns = time.perf_counter_ns()

try:
    output = (
        manager.send_runtime_turn(
            MESSAGE,
            state=state,
            reasoning_mode=(
                EXPECTED_REASONING
            ),
            persist=False,
            execution_context_id=CTX,
            model_form=(
                EXPECTED_MODEL_FORM
            ),
            resource_governor=governor,
            resource_priority="standard",
            resource_request_source=(
                "phase14_11L3-warm-small"
            ),
            resource_request_reasons=(
                "warm resident Small runtime "
                "performance certification",
            ),
            resource_may_defer=False,
        )
    )

except Exception as exc:
    end_ns = time.perf_counter_ns()

    attempt.update({
        "completed_utc":
            utc_now(),
        "duration_ns":
            end_ns - start_ns,
        "duration_ms":
            (end_ns - start_ns)
            / 1_000_000,
        "status":
            "failed",
        "exception_type":
            type(exc).__name__,
        "exception":
            str(exc),
    })

    failed_path = (
        OUTPUT_DIR
        / (
            "l3_warm_small_trial3_failed_"
            + datetime.now(
                timezone.utc
            ).strftime(
                "%Y%m%dT%H%M%SZ"
            )
            + ".json"
        )
    )

    write_json(
        failed_path,
        attempt,
    )

    IN_PROGRESS_PATH.unlink(
        missing_ok=True
    )

    print(
        "Trial failed; evidence preserved:",
        failed_path,
    )

    raise

end_ns = time.perf_counter_ns()

duration_ns = (
    end_ns - start_ns
)


# --------------------------------------------------
# POST-TURN VALIDATION — OUTSIDE TIMER
# --------------------------------------------------

selected = selected_result(
    output
)

if selected.get(
    "binding_id"
) != EXPECTED_BINDING:
    raise RuntimeError(
        "Real turn did not retain "
        "binding-0001."
    )

if selected.get(
    "model_form"
) != EXPECTED_MODEL_FORM:
    raise RuntimeError(
        "Real turn did not retain Small."
    )

if selected.get(
    "resolved_reasoning_mode"
) != EXPECTED_REASONING:
    raise RuntimeError(
        "Real turn did not retain "
        "Normal reasoning."
    )

if selected.get(
    "execution_context_id"
) != CTX:
    raise RuntimeError(
        "Execution context changed."
    )

if selected.get(
    "session_created"
) is not True:
    raise RuntimeError(
        "Warm Trial 3 did not create "
        "a fresh runtime session."
    )

if selected.get(
    "session_reused"
) is not False:
    raise RuntimeError(
        "Warm Trial 3 unexpectedly "
        "reused a runtime session."
    )

after = snapshot()

if not any(
    "bristlecone-qwen35:4b-64k"
    in str(line)
    for line in after["resident_models"]
):
    raise RuntimeError(
        "Small residency disappeared "
        "during warm Trial 1."
    )

if not after["llama_server"]:
    raise RuntimeError(
        "llama-server disappeared "
        "during warm Trial 1."
    )

active_after = sha256(
    ACTIVE
)

if active_after != active_before:
    raise RuntimeError(
        "persist=False changed "
        "active.yaml."
    )

attempt.update({
    "completed_utc":
        utc_now(),
    "duration_ns":
        duration_ns,
    "duration_ms":
        duration_ns / 1_000_000,
    "duration_s":
        duration_ns / 1_000_000_000,
    "result":
        selected,
    "after":
        after,
    "active_yaml_sha_after":
        active_after,
    "status":
        "success",
    "cleanup_performed":
        False,
})

write_json(
    SUCCESS_PATH,
    attempt,
)

IN_PROGRESS_PATH.unlink(
    missing_ok=True
)

print()
print(
    "=== L.3 WARM TRIAL 3 RESULT ==="
)
print()

print(
    "Duration ns:",
    duration_ns,
)

print(
    "Duration ms:",
    round(
        duration_ns / 1_000_000,
        3,
    ),
)

print(
    "Duration s:",
    round(
        duration_ns
        / 1_000_000_000,
        6,
    ),
)

print()

for key, value in selected.items():
    if key == "runtime_result_repr":
        continue

    print(
        f"{key}: {value}"
    )

print()
print(
    "Resident after:",
    after["resident_models"],
)

print(
    "llama-server after:",
    after["llama_server"],
)

print(
    "runtime sockets after:",
    after["runtime_sockets"],
)

print()
print(
    "Cleanup performed: False"
)

print(
    "Evidence:",
    SUCCESS_PATH,
)

print()
print(
    "L.3 Warm Trial 3 status: 0"
)
