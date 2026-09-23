"""Phase 14.11H.6B integrated Colony identity-join certification."""

import inspect

from colony.identity import ColonyExecutionContext
from resources.model import ResourceRequest
from runtime.session_store import RuntimeSessionIdentity
from runtime.model_residency import (
    SharedModelResidency,
    residency_supports_session_identity,
)


TREE = "bristlecone"
BINDING = "binding-0001"

CTX_O = "ctx-O"
CTX_R1 = "ctx-R1"
CTX_R2 = "ctx-R2"


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def support_check(residency, identity):
    """Call the real residency helper by its declared API."""

    signature = inspect.signature(
        residency_supports_session_identity
    )

    parameters = list(
        signature.parameters
    )

    assert len(parameters) == 2

    values = {}

    for name in parameters:
        lowered = name.lower()

        if "resid" in lowered:
            values[name] = residency
        elif (
            "session" in lowered
            or "identity" in lowered
        ):
            values[name] = identity
        else:
            raise AssertionError(
                "Unexpected residency-helper parameter: "
                + name
            )

    return residency_supports_session_identity(
        **values
    )


def resource_request(context_id, reasoning):
    """Build one synthetic frozen-resource request."""

    return ResourceRequest(
        task_id="task-h6b",
        execution_context_id=context_id,
        model_form="small",
        reasoning_mode=reasoning,
        priority="standard",
        source="h6b",
        reasons=("integrated-colony-cert",),
        may_defer=True,
    )


# ==================================================
# 1. SAME TREE, THREE EXECUTION CONTEXTS
# ==================================================

ortet = ColonyExecutionContext(
    tree_id=TREE,
    execution_context_id=CTX_O,
    lineage_role="ortet",
    operational_role="worker",
)

r1 = ColonyExecutionContext(
    tree_id=TREE,
    execution_context_id=CTX_R1,
    lineage_role="ramet",
    operational_role="main",
)

r2 = ColonyExecutionContext(
    tree_id=TREE,
    execution_context_id=CTX_R2,
    lineage_role="ramet",
    operational_role="specialist",
)

members = (
    ortet,
    r1,
    r2,
)

assert {
    member.tree_id
    for member in members
} == {TREE}

assert {
    member.execution_context_id
    for member in members
} == {
    CTX_O,
    CTX_R1,
    CTX_R2,
}

print("PASS 01: one Tree contains Ortet + two Ramets")


# ==================================================
# 2. RESOURCE TARGETING FOLLOWS CONTEXT
# ==================================================

requests = {
    CTX_O: resource_request(
        CTX_O,
        "normal",
    ),
    CTX_R1: resource_request(
        CTX_R1,
        "deep",
    ),
    CTX_R2: resource_request(
        CTX_R2,
        "light",
    ),
}

for member in members:
    request = requests[
        member.execution_context_id
    ]

    assert (
        request.execution_context_id
        == member.execution_context_id
    )

    assert request.task_id == "task-h6b"
    assert request.model_form == "small"

print("PASS 02: ResourceRequest targets exact execution context")
print("PASS 03: shared Task/model form does not erase member identity")


# ==================================================
# 3. SESSION IDENTITY JOINS CONTEXT + BINDING
# ==================================================

sessions = {
    context_id: RuntimeSessionIdentity(
        execution_context_id=context_id,
        binding_id=BINDING,
    )
    for context_id in (
        CTX_O,
        CTX_R1,
        CTX_R2,
    )
}

for context_id, session in sessions.items():
    assert (
        session.execution_context_id
        == requests[
            context_id
        ].execution_context_id
    )

    assert session.binding_id == BINDING

assert len(set(sessions.values())) == 3

print("PASS 04: Resource target joins same context to session identity")
print("PASS 05: same binding still yields three session identities")


# ==================================================
# 4. ONE RESIDENCY MAY SERVE ALL THREE
# ==================================================

residency = SharedModelResidency(
    residency_id="residency-small-001",
    binding_id=BINDING,
    adapter="fake",
)

for context_id in (
    CTX_O,
    CTX_R1,
    CTX_R2,
):
    assert support_check(
        residency,
        sessions[context_id],
    )

print("PASS 06: one shared residency supports Ortet")
print("PASS 07: same residency supports Ramet R1")
print("PASS 08: same residency supports Ramet R2")


# ==================================================
# 5. RESIDENCY MUST FOLLOW BINDING, NOT CONTEXT
# ==================================================

other_binding_session = RuntimeSessionIdentity(
    execution_context_id=CTX_R1,
    binding_id="binding-other",
)

assert not support_check(
    residency,
    other_binding_session,
)

# Changing execution context while retaining binding
# must remain compatible with the shared weights.
another_context_same_binding = (
    RuntimeSessionIdentity(
        execution_context_id="ctx-R3",
        binding_id=BINDING,
    )
)

assert support_check(
    residency,
    another_context_same_binding,
)

print("PASS 09: residency rejects wrong binding")
print("PASS 10: residency does not belong to one execution context")


# ==================================================
# 6. OWNERSHIP BOUNDARIES REMAIN DISTINCT
# ==================================================

residency_fields = set(
    getattr(
        SharedModelResidency,
        "__annotations__",
        {},
    )
)

session_fields = set(
    getattr(
        RuntimeSessionIdentity,
        "__annotations__",
        {},
    )
)

request_fields = set(
    getattr(
        ResourceRequest,
        "__annotations__",
        {},
    )
)

assert "execution_context_id" not in residency_fields
assert "tree_id" not in residency_fields
assert "task_id" not in residency_fields
assert "session_id" not in residency_fields

assert {
    "execution_context_id",
    "binding_id",
}.issubset(
    session_fields
)

assert {
    "task_id",
    "execution_context_id",
    "model_form",
    "reasoning_mode",
}.issubset(
    request_fields
)

print("PASS 11: residency contains no Colony-member ownership")
print("PASS 12: session identity owns context + binding only")
print("PASS 13: resource request retains exact context target")


print()
print("13 PASS / 0 FAIL")
print("14.11H.6B status: 0")
