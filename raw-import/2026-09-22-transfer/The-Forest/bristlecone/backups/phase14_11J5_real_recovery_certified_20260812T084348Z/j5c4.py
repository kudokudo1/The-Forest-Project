import copy
import hashlib
import subprocess
from pathlib import Path

from runtime.task_session import TaskSessionManager
from resources.live_providers import (
    build_live_small_resource_governor,
)


ROOT = Path("/home/user/The-Forest/bristlecone")
ACTIVE = ROOT / "state" / "active.yaml"

CTX = "ctx-j5"
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


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)
    return digest.hexdigest()


def hermes_pid():
    result = subprocess.run(
        [
            "systemctl",
            "--user",
            "show",
            "hermes-bristlecone.service",
            "-p",
            "MainPID",
            "--value",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def state_from_output(output):
    """
    Recover the Task-local state without assuming more
    about send_runtime_turn's wrapper shape than needed.
    """
    candidates = []

    if isinstance(output, dict):
        candidates.append(output)

        for key in (
            "state",
            "updated_state",
            "task_state",
        ):
            value = output.get(key)
            if isinstance(value, dict):
                candidates.append(value)

    elif isinstance(output, (tuple, list)):
        candidates.extend(
            item
            for item in output
            if isinstance(item, dict)
        )

    for candidate in candidates:
        if isinstance(
            candidate.get("task_session"),
            dict,
        ):
            return candidate

    raise AssertionError(
        "Could not locate Task-local state in "
        "send_runtime_turn output."
    )


def evidence_field(output, name):
    """
    Read certification metadata while preferring the
    public/top-level result fields used by the J tests.
    """
    candidates = []

    if isinstance(output, dict):
        candidates.append(output)

        for key in (
            "runtime_result",
            "result",
            "last_runtime_result",
        ):
            value = output.get(key)
            if isinstance(value, dict):
                candidates.append(value)

    elif isinstance(output, (tuple, list)):
        for item in output:
            if not isinstance(item, dict):
                continue

            candidates.append(item)

            for key in (
                "runtime_result",
                "result",
                "last_runtime_result",
            ):
                value = item.get(key)
                if isinstance(value, dict):
                    candidates.append(value)

    for candidate in candidates:
        if name in candidate:
            return candidate[name]

    return None


def show_field(output, name):
    value = evidence_field(output, name)
    print(f"{name}: {value!r}")
    return value


def runtime_contexts(state):
    task_session = state.get(
        "task_session",
        {},
    )
    sessions = task_session.get(
        "runtime_sessions",
        {},
    )

    if not isinstance(sessions, dict):
        return None

    return sorted(sessions.keys())


def assert_production_frozen():
    for path, expected in EXPECTED_PRODUCTION.items():
        actual = sha256(path)

        print(
            f"{path.relative_to(ROOT)}: "
            f"{actual}"
        )

        assert actual == expected, (
            f"Production SHA changed: {path}"
        )


print("=== 14.11J.5C4 — CLEAN REAL STALE RECOVERY ===")
print()

# ----------------------------------------------------------
# PRE-FLIGHT GUARDS
# ----------------------------------------------------------

print("=== PRE-FLIGHT PRODUCTION GUARD ===")

assert_production_frozen()

active_before = sha256(ACTIVE)
print("active.yaml:", active_before)

assert active_before == EXPECTED_ACTIVE_SHA, (
    "active.yaml is not at the certified baseline."
)

pid_before = hermes_pid()
print("Hermes MainPID:", pid_before)

assert pid_before not in (
    "",
    "0",
), "Hermes is not running."

print("PASS: pre-flight baseline certified")
print()


# ----------------------------------------------------------
# CONFIGURED REAL RUNTIME
# ----------------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = manager.load_state()

print(
    "configured runtime:",
    configured_state.get("runtime"),
)

adapter = manager._runtime_adapter_for_state(
    configured_state
)

print(
    "configured adapter:",
    type(adapter).__name__,
)

assert type(adapter).__name__ == (
    "HermesRuntimeAdapter"
)

governor = (
    build_live_small_resource_governor()
)

state = copy.deepcopy(
    configured_state
)

state = manager.start_task(
    state=state,
    persist=False,
)

print(
    "Task:",
    state.get("task_session", {}).get(
        "task_id"
    ),
)
print("Context:", CTX)
print()


session_a = None
session_b = None

a_deleted = False
b_cleaned = False


def send_real_turn(message, state):
    return manager.send_runtime_turn(
        message,
        state=state,
        reasoning_mode=EXPECTED_REASONING,
        persist=False,
        execution_context_id=CTX,
        model_form=EXPECTED_MODEL_FORM,
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source=(
            "phase14_11J5C4-real-small"
        ),
        resource_request_reasons=(
            "genuine stale-session "
            "recovery certification",
        ),
        resource_may_defer=False,
    )


try:
    # ------------------------------------------------------
    # TURN 1 — CREATE REAL DISPOSABLE SESSION A
    # ------------------------------------------------------

    print(
        "=== TURN 1 — CREATE DISPOSABLE "
        "SESSION A ===",
        flush=True,
    )

    first_output = send_real_turn(
        "Reply only with: J5C4-A",
        state,
    )

    first_state = state_from_output(
        first_output
    )

    print()
    print("--- TURN 1 RESULT ---")

    for name in (
        "execution_context_id",
        "binding_id",
        "model_form",
        "resolved_reasoning_mode",
        "session_id",
        "initial_requested_session_id",
        "requested_session_id",
        "session_created",
        "initial_session_created",
        "session_reused",
        "session_recovered",
        "binding_persisted",
        "binding_persisted_before_turn",
    ):
        show_field(
            first_output,
            name,
        )

    session_a = evidence_field(
        first_output,
        "session_id",
    )

    assert isinstance(
        session_a,
        str,
    )
    assert session_a

    assert (
        evidence_field(
            first_output,
            "execution_context_id",
        )
        == CTX
    )

    assert (
        evidence_field(
            first_output,
            "binding_id",
        )
        == EXPECTED_BINDING
    )

    assert (
        evidence_field(
            first_output,
            "model_form",
        )
        == EXPECTED_MODEL_FORM
    )

    assert (
        evidence_field(
            first_output,
            "resolved_reasoning_mode",
        )
        == EXPECTED_REASONING
    )

    assert (
        evidence_field(
            first_output,
            "session_created",
        )
        is True
    )

    assert (
        evidence_field(
            first_output,
            "initial_session_created",
        )
        is True
    )

    assert (
        evidence_field(
            first_output,
            "session_reused",
        )
        is False
    )

    assert (
        evidence_field(
            first_output,
            "session_recovered",
        )
        is False
    )

    assert (
        evidence_field(
            first_output,
            "binding_persisted",
        )
        is False
    )

    print()
    print(
        "session A:",
        session_a,
    )

    print(
        "runtime contexts:",
        runtime_contexts(first_state),
    )

    assert runtime_contexts(
        first_state
    ) == [CTX]

    print(
        "PASS: real disposable session A created"
    )


    # ------------------------------------------------------
    # TARGETED DELETE A
    #
    # Forest first_state intentionally still references A.
    # ------------------------------------------------------

    print()
    print(
        "=== TARGETED HERMES DELETE SESSION A ===",
        flush=True,
    )

    delete_a = adapter.end_session(
        session_a,
        configured_state,
    )

    print(
        "delete A result:",
        repr(delete_a),
    )

    assert isinstance(
        delete_a,
        dict,
    )

    assert delete_a.get(
        "session_id"
    ) == session_a

    assert delete_a.get(
        "ended"
    ) is True

    a_deleted = True

    print(
        "PASS: Hermes deleted disposable session A"
    )
    print(
        "PASS: Forest intentionally still holds stale A"
    )


    # ------------------------------------------------------
    # TURN 2 — GENUINE STALE RECOVERY
    #
    # Expected:
    #   initial stale A
    #   genuine Hermes 404/session_not_found
    #   one replacement B
    #   same frozen turn retried once
    # ------------------------------------------------------

    print()
    print(
        "=== TURN 2 — GENUINE STALE RECOVERY ===",
        flush=True,
    )

    second_output = send_real_turn(
        "Reply only with: J5C4-B",
        first_state,
    )

    second_state = state_from_output(
        second_output
    )

    print()
    print("--- RECOVERY RESULT ---")

    fields = (
        "execution_context_id",
        "binding_id",
        "model_form",
        "resolved_reasoning_mode",
        "initial_requested_session_id",
        "requested_session_id",
        "session_id",
        "previous_session_id",
        "session_created",
        "initial_session_created",
        "session_reused",
        "session_rotated",
        "session_recovered",
        "recovery_from_session_id",
        "recovery_session_id",
        "binding_persisted",
        "binding_persisted_before_turn",
        "recovery_binding_persisted",
        "adapter",
    )

    for name in fields:
        show_field(
            second_output,
            name,
        )

    session_b = evidence_field(
        second_output,
        "session_id",
    )

    assert isinstance(
        session_b,
        str,
    )
    assert session_b

    # Core identity remains frozen.
    assert (
        evidence_field(
            second_output,
            "execution_context_id",
        )
        == CTX
    )

    assert (
        evidence_field(
            second_output,
            "binding_id",
        )
        == EXPECTED_BINDING
    )

    assert (
        evidence_field(
            second_output,
            "model_form",
        )
        == EXPECTED_MODEL_FORM
    )

    assert (
        evidence_field(
            second_output,
            "resolved_reasoning_mode",
        )
        == EXPECTED_REASONING
    )

    # Initial request reused stale A.
    assert (
        evidence_field(
            second_output,
            "initial_requested_session_id",
        )
        == session_a
    )

    assert (
        evidence_field(
            second_output,
            "initial_session_created",
        )
        is False
    )

    assert (
        evidence_field(
            second_output,
            "session_reused",
        )
        is True
    )

    # Recovery created exactly the observed replacement B.
    assert (
        evidence_field(
            second_output,
            "session_recovered",
        )
        is True
    )

    assert (
        evidence_field(
            second_output,
            "session_created",
        )
        is True
    )

    assert (
        evidence_field(
            second_output,
            "recovery_from_session_id",
        )
        == session_a
    )

    assert (
        evidence_field(
            second_output,
            "recovery_session_id",
        )
        == session_b
    )

    # CORRECTED C4 SEMANTICS:
    # requested_session_id becomes replacement B
    # before the one permitted retry.
    assert (
        evidence_field(
            second_output,
            "requested_session_id",
        )
        == session_b
    )

    assert (
        evidence_field(
            second_output,
            "previous_session_id",
        )
        == session_a
    )

    assert session_a != session_b

    # persist=False must not claim durable recovery writes.
    assert (
        evidence_field(
            second_output,
            "recovery_binding_persisted",
        )
        is False
    )

    assert (
        evidence_field(
            second_output,
            "binding_persisted",
        )
        is False
    )

    contexts = runtime_contexts(
        second_state
    )

    print(
        "runtime contexts:",
        contexts,
    )

    assert contexts == [CTX]

    print()
    print(
        "PASS: genuine stale A recovered to "
        "replacement B"
    )

    print(
        "PASS: recovery remained ctx-j5 / "
        "binding-0001 / Small / Normal"
    )

    print(
        "PASS: persist=False prevented durable "
        "recovery persistence"
    )


    # ------------------------------------------------------
    # CLEAN UP DISPOSABLE REPLACEMENT B
    # ------------------------------------------------------

    print()
    print(
        "=== CLEANUP DISPOSABLE SESSION B ===",
        flush=True,
    )

    cleanup_b = adapter.end_session(
        session_b,
        configured_state,
    )

    print(
        "cleanup B result:",
        repr(cleanup_b),
    )

    assert isinstance(
        cleanup_b,
        dict,
    )

    assert cleanup_b.get(
        "session_id"
    ) == session_b

    assert cleanup_b.get(
        "ended"
    ) is True

    b_cleaned = True

    print(
        "PASS: disposable replacement B cleaned up"
    )


finally:
    # ------------------------------------------------------
    # FAIL-SAFE HARNESS CLEANUP
    #
    # If a harness assertion fails, do not knowingly leave
    # a disposable real session behind.
    # ------------------------------------------------------

    if (
        session_b
        and not b_cleaned
    ):
        try:
            print(
                "FAIL-SAFE: attempting cleanup of B:",
                session_b,
                flush=True,
            )

            result = adapter.end_session(
                session_b,
                configured_state,
            )

            print(
                "FAIL-SAFE B cleanup:",
                repr(result),
            )
        except Exception as exc:
            print(
                "FAIL-SAFE B cleanup error:",
                repr(exc),
            )

    if (
        session_a
        and not a_deleted
    ):
        try:
            print(
                "FAIL-SAFE: attempting cleanup of A:",
                session_a,
                flush=True,
            )

            result = adapter.end_session(
                session_a,
                configured_state,
            )

            print(
                "FAIL-SAFE A cleanup:",
                repr(result),
            )
        except Exception as exc:
            print(
                "FAIL-SAFE A cleanup error:",
                repr(exc),
            )


# ----------------------------------------------------------
# POST-FLIGHT INTEGRITY
# ----------------------------------------------------------

print()
print("=== POST-FLIGHT INTEGRITY ===")

active_after = sha256(ACTIVE)

print(
    "active.yaml before:",
    active_before,
)
print(
    "active.yaml after: ",
    active_after,
)

assert active_after == active_before

pid_after = hermes_pid()

print(
    "Hermes MainPID before:",
    pid_before,
)
print(
    "Hermes MainPID after: ",
    pid_after,
)

assert pid_after == pid_before

assert_production_frozen()

print()
print(
    "PASS: active.yaml unchanged"
)
print(
    "PASS: Hermes PID unchanged"
)
print(
    "PASS: six-file production baseline unchanged"
)

print()
print(
    "14.11J.5C4 evidence status: 0"
)
