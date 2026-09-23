"""Phase 14.11I.3 fake Small second-turn session reuse."""

import importlib.util
from pathlib import Path


SOURCE = Path(__file__).with_name(
    "test_model_form_governor_task_session_integration.py"
)

spec = importlib.util.spec_from_file_location(
    "i3_source",
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
    # --------------------------------------------------
    # Turn 1
    # --------------------------------------------------

    first = manager.send_runtime_turn(
        "I.3 first fake Small turn",
        state=module.active_state(),
        instructions="I.3 reuse certification",
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-g5d",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source="i3-certification",
        resource_request_reasons=(
            "first_turn",
        ),
        resource_may_defer=True,
    )

    assert isinstance(first, dict)
    assert isinstance(first.get("state"), dict)

    first_state = first["state"]

    first_binding = (
        first_state[
            "task_session"
        ][
            "runtime_sessions"
        ][
            "ctx-g5d"
        ][
            "binding-0001"
        ]
    )

    first_session_id = first_binding[
        "session_id"
    ]

    assert first_session_id == "g5d-session-1"

    assert len(adapter.create_calls) == 1
    assert len(adapter.send_calls) == 1

    # --------------------------------------------------
    # Turn 2
    #
    # Reuse the returned Forest state from turn 1.
    # --------------------------------------------------

    second = manager.send_runtime_turn(
        "I.3 second fake Small turn",
        state=first_state,
        instructions="I.3 reuse certification",
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-g5d",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source="i3-certification",
        resource_request_reasons=(
            "second_turn",
        ),
        resource_may_defer=True,
    )

    assert isinstance(second, dict)
    assert isinstance(second.get("state"), dict)

    second_state = second["state"]

    second_binding = (
        second_state[
            "task_session"
        ][
            "runtime_sessions"
        ][
            "ctx-g5d"
        ][
            "binding-0001"
        ]
    )

    second_session_id = second_binding[
        "session_id"
    ]

    # --------------------------------------------------
    # Reuse invariants
    # --------------------------------------------------

    assert first_session_id == second_session_id

    # Session was created only on turn 1.
    assert len(adapter.create_calls) == 1

    # Both turns reached the fake runtime.
    assert len(adapter.send_calls) == 2

    assert (
        adapter.send_calls[0]["session_id"]
        == first_session_id
    )

    assert (
        adapter.send_calls[1]["session_id"]
        == first_session_id
    )

    # One Governor decision per logical turn.
    assert len(governor.requests) == 2

    for request in governor.requests:
        assert request.task_id == "task-g5d"
        assert (
            request.execution_context_id
            == "ctx-g5d"
        )
        assert request.model_form == "small"
        assert request.reasoning_mode == "normal"

    # Second turn must not create a neighboring slot.
    sessions = second_state[
        "task_session"
    ][
        "runtime_sessions"
    ]

    assert set(sessions) == {
        "ctx-g5d"
    }

    assert set(
        sessions["ctx-g5d"]
    ) == {
        "binding-0001"
    }


print("PASS 01: turn 1 created g5d-session-1")
print("PASS 02: turn 2 reused g5d-session-1")
print("PASS 03: only one session creation occurred")
print("PASS 04: both turns reached send_turn")
print("PASS 05: both sends used the same session")
print("PASS 06: Governor ran once per logical turn")
print("PASS 07: Task/context/Small identity stayed stable")
print("PASS 08: no neighboring runtime-session slot appeared")

print()
print("8 PASS / 0 FAIL")
print("14.11I.3 status: 0")
