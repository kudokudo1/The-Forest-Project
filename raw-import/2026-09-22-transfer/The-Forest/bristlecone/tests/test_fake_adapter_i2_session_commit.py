"""Phase 14.11I.2 fake Small session commit certification."""

import importlib.util
from pathlib import Path


SOURCE = Path(__file__).with_name(
    "test_model_form_governor_task_session_integration.py"
)

spec = importlib.util.spec_from_file_location(
    "i2_source",
    SOURCE,
)

assert spec is not None
assert spec.loader is not None

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

governor = module.RecordingGovernor(
    "approve"
)

with module.manager_fixture() as (
    manager,
    adapter,
):
    result = module.send_governed_turn(
        manager,
        governor=governor,
    )

    assert isinstance(result, dict)
    assert isinstance(result.get("state"), dict)

    returned_state = result["state"]

    task = returned_state.get(
        "task_session"
    )

    assert isinstance(task, dict)
    assert task["id"] == "task-g5d"
    assert task["status"] == "active"

    sessions = task.get(
        "runtime_sessions"
    )

    assert isinstance(sessions, dict)

    # Exact Colony member.
    assert set(sessions) == {
        "ctx-g5d"
    }

    context_sessions = sessions[
        "ctx-g5d"
    ]

    assert isinstance(
        context_sessions,
        dict,
    )

    # Exact Small binding.
    assert set(context_sessions) == {
        "binding-0001"
    }

    binding = context_sessions[
        "binding-0001"
    ]

    assert binding[
        "adapter"
    ] == "hermes"

    assert binding[
        "previous_session_id"
    ] is None

    # One create + one send.
    assert len(adapter.create_calls) == 1
    assert len(adapter.send_calls) == 1

    created_id = adapter.create_calls[
        0
    ][
        "session_id"
    ]

    sent_id = adapter.send_calls[
        0
    ][
        "session_id"
    ]

    stored_id = binding[
        "session_id"
    ]

    assert created_id == "g5d-session-1"

    assert (
        created_id
        == sent_id
        == stored_id
    )

    # The state passed to the runtime send must
    # already contain the exact same binding.
    send_state = adapter.send_calls[
        0
    ][
        "state"
    ]

    send_binding = (
        send_state[
            "task_session"
        ][
            "runtime_sessions"
        ][
            "ctx-g5d"
        ][
            "binding-0001"
        ]
    )

    assert (
        send_binding["session_id"]
        == created_id
    )

    # Governor identity also agrees.
    assert len(governor.requests) == 1

    request = governor.requests[0]

    assert request.task_id == "task-g5d"
    assert (
        request.execution_context_id
        == "ctx-g5d"
    )
    assert request.model_form == "small"

print("PASS 01: returned Task remains task-g5d")
print("PASS 02: runtime binding stored under ctx-g5d")
print("PASS 03: runtime binding stored under binding-0001")
print("PASS 04: stored adapter is hermes")
print("PASS 05: created session equals sent session")
print("PASS 06: sent session equals returned-state session")
print("PASS 07: binding exists before send_turn executes")
print("PASS 08: Governor context agrees with stored session context")

print()
print("8 PASS / 0 FAIL")
print("14.11I.2 status: 0")
