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

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l4_same_session_trial5_raw.json"
)

IN_PROGRESS = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l4_same_session_trial5_in_progress.json"
)

CTX = "ctx-l4-reuse-05"

PRIME_MESSAGE = (
    "Reply only with: L4-PRIME"
)

# Keep measured prompt identical to L.2/L.3.
MEASURED_MESSAGE = (
    "Reply only with: L2-COLD-01"
)

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


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def ollama_ps():
    return subprocess.run(
        ["ollama", "ps"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def resident_lines(text):
    lines = [
        line
        for line in text.splitlines()
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
        "Successful L.4 Trial 5 artifact "
        "already exists."
    )

if IN_PROGRESS.exists():
    raise RuntimeError(
        "L.4 Trial 5 in-progress artifact "
        "already exists."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "active.yaml is not frozen."
    )


# --------------------------------------------------
# WARM PRECONDITION
# --------------------------------------------------

before_ps = ollama_ps()
before_resident = resident_lines(
    before_ps
)

print("=== 14.11L.4 SAME-SESSION REUSE — TRIAL 5 ===")
print()
print("Resident before:")
print(before_ps)

if (
    len(before_resident) != 1
    or "bristlecone-qwen35:4b-64k"
    not in before_resident[0]
):
    raise RuntimeError(
        "L.4 warm precondition failed."
    )


# --------------------------------------------------
# FRESH FOREST TASK
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

working = copy.deepcopy(
    configured_state
)

started = manager.start_task(
    state=working,
    persist=False,
)

state = started["state"]
task_id = started["task_session"]["id"]

print("Task:", task_id)
print("Context:", CTX)
print()


def send(message, state):
    return manager.send_runtime_turn(
        message,
        state=state,
        reasoning_mode="normal",
        persist=False,
        execution_context_id=CTX,
        model_form="small",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "phase14_11L4-same-session-reuse"
        ),
        resource_request_reasons=(
            "same-session performance certification",
        ),
        resource_may_defer=False,
    )


# --------------------------------------------------
# TURN 1 — UNMEASURED PRIME
# --------------------------------------------------

print(
    "Starting UNMEASURED prime turn...",
    flush=True,
)

prime = send(
    PRIME_MESSAGE,
    state,
)

prime_session = prime.get(
    "session_id"
)

if not prime_session:
    raise RuntimeError(
        "Prime returned no session ID."
    )

if prime.get("session_created") is not True:
    raise RuntimeError(
        "Prime did not create a fresh session."
    )

if prime.get("session_reused") is not False:
    raise RuntimeError(
        "Prime unexpectedly reused a session."
    )

prime_state = prime.get(
    "state"
)

if not isinstance(
    prime_state,
    dict,
):
    raise RuntimeError(
        "Prime output did not expose "
        "Task-local state for reuse."
    )

print("Prime session:", prime_session)
print("Prime created: True")
print()


attempt = {
    "phase": "14.11L.4",
    "trial": 5,
    "scenario":
        "warm-small-same-session-reuse",
    "task_id": task_id,
    "execution_context_id": CTX,
    "prime_session_id":
        prime_session,
    "prime_message":
        PRIME_MESSAGE,
    "measured_message":
        MEASURED_MESSAGE,
    "model_form": "small",
    "reasoning_mode": "normal",
    "binding_expected":
        "binding-0001",
    "persist": False,
    "resident_before":
        before_resident,
    "started_utc":
        utc_now(),
    "status": "in_progress",
}

write_json(
    IN_PROGRESS,
    attempt,
)


# --------------------------------------------------
# TURN 2 — MEASURED SAME-SESSION REUSE
# --------------------------------------------------

print(
    "Starting timed SAME-SESSION turn...",
    flush=True,
)

start_ns = time.perf_counter_ns()

try:
    measured = send(
        MEASURED_MESSAGE,
        prime_state,
    )

except Exception as exc:
    end_ns = time.perf_counter_ns()

    attempt.update({
        "status": "failed",
        "duration_ns":
            end_ns - start_ns,
        "exception_type":
            type(exc).__name__,
        "exception":
            str(exc),
        "completed_utc":
            utc_now(),
    })

    failed = OUTPUT.with_name(
        "l4_same_session_trial5_failed_"
        + datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%SZ"
        )
        + ".json"
    )

    write_json(
        failed,
        attempt,
    )

    IN_PROGRESS.unlink(
        missing_ok=True
    )

    raise

end_ns = time.perf_counter_ns()

duration_ns = (
    end_ns - start_ns
)


# --------------------------------------------------
# REUSE ASSERTIONS
# --------------------------------------------------

measured_session = measured.get(
    "session_id"
)

checks = {
    "same_session":
        measured_session
        == prime_session,

    "created_false":
        measured.get(
            "session_created"
        ) is False,

    "reused_true":
        measured.get(
            "session_reused"
        ) is True,

    "initial_created_false":
        measured.get(
            "initial_session_created"
        ) is False,

    "not_recovered":
        measured.get(
            "session_recovered"
        ) is False,

    "not_rotated":
        measured.get(
            "session_rotated"
        ) is False,

    "same_context":
        measured.get(
            "execution_context_id"
        ) == CTX,

    "same_binding":
        measured.get(
            "binding_id"
        ) == "binding-0001",

    "small":
        measured.get(
            "model_form"
        ) == "small",

    "normal":
        measured.get(
            "resolved_reasoning_mode"
        ) == "normal",
}

failed_checks = [
    name
    for name, passed in checks.items()
    if not passed
]

if failed_checks:
    raise RuntimeError(
        "L.4 reuse assertions failed: "
        + ", ".join(failed_checks)
    )


after_ps = ollama_ps()
after_resident = resident_lines(
    after_ps
)

if not any(
    "bristlecone-qwen35:4b-64k"
    in line
    for line in after_resident
):
    raise RuntimeError(
        "Small did not remain resident."
    )

if sha256(ACTIVE) != EXPECTED_ACTIVE:
    raise RuntimeError(
        "persist=False changed active.yaml."
    )


attempt.update({
    "status": "success",
    "completed_utc":
        utc_now(),
    "duration_ns":
        duration_ns,
    "duration_ms":
        duration_ns / 1_000_000,
    "duration_s":
        duration_ns / 1_000_000_000,
    "measured_session_id":
        measured_session,
    "session_created":
        measured.get(
            "session_created"
        ),
    "session_reused":
        measured.get(
            "session_reused"
        ),
    "initial_session_created":
        measured.get(
            "initial_session_created"
        ),
    "session_recovered":
        measured.get(
            "session_recovered"
        ),
    "session_rotated":
        measured.get(
            "session_rotated"
        ),
    "binding_id":
        measured.get(
            "binding_id"
        ),
    "resolved_reasoning_mode":
        measured.get(
            "resolved_reasoning_mode"
        ),
    "resident_after":
        after_resident,
    "active_yaml_sha":
        EXPECTED_ACTIVE,
    "cleanup_performed":
        False,
})

write_json(
    OUTPUT,
    attempt,
)

IN_PROGRESS.unlink(
    missing_ok=True
)


print()
print("=== L.4 TRIAL 5 RESULT ===")
print()
print(
    "Duration s:",
    duration_ns / 1_000_000_000,
)
print(
    "Prime session:",
    prime_session,
)
print(
    "Measured session:",
    measured_session,
)
print(
    "Same session:",
    measured_session
    == prime_session,
)
print(
    "session_created:",
    measured.get(
        "session_created"
    ),
)
print(
    "session_reused:",
    measured.get(
        "session_reused"
    ),
)
print(
    "initial_session_created:",
    measured.get(
        "initial_session_created"
    ),
)
print(
    "session_recovered:",
    measured.get(
        "session_recovered"
    ),
)
print(
    "binding:",
    measured.get(
        "binding_id"
    ),
)
print(
    "reasoning:",
    measured.get(
        "resolved_reasoning_mode"
    ),
)
print()
print(
    "Cleanup performed: False"
)
print(
    "Evidence:",
    OUTPUT
)
print()
print(
    "L.4 Trial 5 status: 0"
)
