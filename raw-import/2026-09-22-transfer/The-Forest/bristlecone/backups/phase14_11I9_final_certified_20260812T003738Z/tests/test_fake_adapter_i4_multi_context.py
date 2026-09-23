"""Phase 14.11I.4 multi-context fake Small execution."""

import importlib.util
from pathlib import Path


SOURCE = Path(__file__).with_name(
    "test_model_form_governor_task_session_integration.py"
)

spec = importlib.util.spec_from_file_location(
    "i4_source",
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
    state = module.active_state()

    # --------------------------------------------------
    # Context R1
    # --------------------------------------------------

    r1 = manager.send_runtime_turn(
        "I.4 turn for R1",
        state=state,
        instructions="I.4 multi-context certification",
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-R1",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source="i4-certification",
        resource_request_reasons=(
            "ctx-R1",
        ),
        resource_may_defer=True,
    )

    assert isinstance(r1, dict)
    state_after_r1 = r1["state"]

    # --------------------------------------------------
    # Context R2
    # --------------------------------------------------

    r2 = manager.send_runtime_turn(
        "I.4 turn for R2",
        state=state_after_r1,
        instructions="I.4 multi-context certification",
        reasoning_mode="normal",
        persist=False,
        execution_context_id="ctx-R2",
        resource_governor=governor,
        resource_priority="standard",
        resource_request_source="i4-certification",
        resource_request_reasons=(
            "ctx-R2",
        ),
        resource_may_defer=True,
    )

    assert isinstance(r2, dict)
    final_state = r2["state"]

    sessions = (
        final_state[
            "task_session"
        ][
            "runtime_sessions"
        ]
    )

    assert set(sessions) == {
        "ctx-R1",
        "ctx-R2",
    }

    r1_binding = sessions[
        "ctx-R1"
    ][
        "binding-0001"
    ]

    r2_binding = sessions[
        "ctx-R2"
    ][
        "binding-0001"
    ]

    r1_session = r1_binding[
        "session_id"
    ]

    r2_session = r2_binding[
        "session_id"
    ]

    assert r1_session != r2_session

    assert len(adapter.create_calls) == 2
    assert len(adapter.send_calls) == 2

    assert (
        adapter.send_calls[0]["session_id"]
        == r1_session
    )

    assert (
        adapter.send_calls[1]["session_id"]
        == r2_session
    )

    assert len(governor.requests) == 2

    assert (
        governor.requests[0].execution_context_id
        == "ctx-R1"
    )

    assert (
        governor.requests[1].execution_context_id
        == "ctx-R2"
    )

    assert (
        governor.requests[0].model_form
        == "small"
    )

    assert (
        governor.requests[1].model_form
        == "small"
    )

    # Same binding, distinct live sessions.
    assert (
        r1_binding["adapter"]
        == r2_binding["adapter"]
        == "hermes"
    )

print("PASS 01: ctx-R1 created its own fake Small session")
print("PASS 02: ctx-R2 created its own fake Small session")
print("PASS 03: both contexts use binding-0001")
print("PASS 04: R1 and R2 session IDs are different")
print("PASS 05: exactly two session creations occurred")
print("PASS 06: each send used its owning context session")
print("PASS 07: Governor preserved R1/R2 context identity")
print("PASS 08: both contexts remained model_form=small")

print()
print("8 PASS / 0 FAIL")
print("14.11I.4 status: 0")
