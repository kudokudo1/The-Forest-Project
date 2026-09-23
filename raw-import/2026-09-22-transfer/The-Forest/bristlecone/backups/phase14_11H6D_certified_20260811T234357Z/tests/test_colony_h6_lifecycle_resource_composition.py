"""Phase 14.11H.6C lifecycle/resource/residency certification."""

import copy
import importlib.util
import inspect
from pathlib import Path
import unittest

from resources.model import ResourceRequest
from runtime.model_residency import (
    SharedModelResidency,
    residency_supports_session_identity,
)
from runtime.session_store import RuntimeSessionIdentity


CTX_A = "ctx-A"
CTX_B = "ctx-B"


# ==================================================
# Load the already-certified H.4 lifecycle module.
# ==================================================

h4_path = (
    Path(__file__).with_name(
        "test_colony_runtime_lifecycle.py"
    )
)

spec = importlib.util.spec_from_file_location(
    "certified_h4_lifecycle",
    h4_path,
)

assert spec is not None
assert spec.loader is not None

h4 = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    h4
)

assert hasattr(h4, "BINDING")
BINDING = h4.BINDING


# ==================================================
# Helper for the real residency compatibility API.
# ==================================================

def residency_supports(residency, identity):
    signature = inspect.signature(
        residency_supports_session_identity
    )

    kwargs = {}

    for name in signature.parameters:
        lowered = name.lower()

        if "resid" in lowered:
            kwargs[name] = residency
        elif (
            "session" in lowered
            or "identity" in lowered
        ):
            kwargs[name] = identity
        else:
            raise AssertionError(
                "Unexpected residency helper parameter: "
                + name
            )

    return residency_supports_session_identity(
        **kwargs
    )


# ==================================================
# 1. H.4 lifecycle prerequisite remains green.
# ==================================================

suite = unittest.defaultTestLoader.loadTestsFromTestCase(
    h4.ColonyRuntimeLifecycleTests
)

result = unittest.TextTestRunner(
    verbosity=0
).run(
    suite
)

assert result.testsRun == 6
assert result.wasSuccessful()

print("PASS 01: all six certified H.4 lifecycle cases still pass")


# ==================================================
# 2. H.4 helpers still use canonical session store.
# ==================================================

bind_source = inspect.getsource(
    h4.bind
)

lookup_source = inspect.getsource(
    h4.lookup
)

assert "set_runtime_session_binding" in bind_source
assert "get_runtime_session_binding" in lookup_source

print("PASS 02: composition uses canonical session-store primitives")


# ==================================================
# 3. Resource target selects exact Colony member.
# ==================================================

request_a = ResourceRequest(
    task_id="task-h6c",
    execution_context_id=CTX_A,
    model_form="small",
    reasoning_mode="deep",
    priority="standard",
    source="h6c",
    reasons=(
        "lifecycle-composition",
    ),
    may_defer=True,
)

assert request_a.execution_context_id == CTX_A

print("PASS 03: ResourceRequest explicitly targets ctx-A")


# ==================================================
# 4. Create same-binding sessions for A and B.
# ==================================================

sessions = {}

sessions = h4.bind(
    sessions,
    CTX_A,
    "session-A1",
)

sessions = h4.bind(
    sessions,
    CTX_B,
    "session-B1",
)

before_a = copy.deepcopy(
    h4.lookup(
        sessions,
        CTX_A,
    )
)

before_b = copy.deepcopy(
    h4.lookup(
        sessions,
        CTX_B,
    )
)

assert before_a is not None
assert before_b is not None
assert before_a != before_b

print("PASS 04: A and B have separate same-binding sessions")


# ==================================================
# 5. Resource-targeted rotation/replacement touches A.
# ==================================================

sessions = h4.bind(
    sessions,
    request_a.execution_context_id,
    "session-A2",
    previous_session_id="session-A1",
)

after_a = copy.deepcopy(
    h4.lookup(
        sessions,
        CTX_A,
    )
)

after_b = copy.deepcopy(
    h4.lookup(
        sessions,
        CTX_B,
    )
)

assert after_a != before_a
assert after_b == before_b

print("PASS 05: ctx-A lifecycle change modifies A")
print("PASS 06: ctx-A lifecycle change leaves B untouched")


# ==================================================
# 6. Session identity agrees with ResourceRequest.
# ==================================================

identity_a = RuntimeSessionIdentity(
    execution_context_id=(
        request_a.execution_context_id
    ),
    binding_id=BINDING,
)

identity_b = RuntimeSessionIdentity(
    execution_context_id=CTX_B,
    binding_id=BINDING,
)

assert (
    identity_a.execution_context_id
    == request_a.execution_context_id
)

assert identity_a.binding_id == identity_b.binding_id
assert identity_a != identity_b

print("PASS 07: Resource target joins the same A session identity")
print("PASS 08: A and B remain distinct despite shared binding")


# ==================================================
# 7. Shared weights survive one-context lifecycle change.
# ==================================================

residency = SharedModelResidency(
    residency_id="residency-h6c-small",
    binding_id=BINDING,
    adapter="hermes",
)

assert residency_supports(
    residency,
    identity_a,
)

assert residency_supports(
    residency,
    identity_b,
)

print("PASS 09: shared residency still supports changed A")
print("PASS 10: shared residency still supports untouched B")


# ==================================================
# 8. Wrong binding remains rejected.
# ==================================================

wrong_binding = RuntimeSessionIdentity(
    execution_context_id=CTX_A,
    binding_id="binding-other",
)

assert not residency_supports(
    residency,
    wrong_binding,
)

print("PASS 11: lifecycle composition does not weaken binding ownership")


# ==================================================
# 9. Resource layer cannot retarget silently.
# ==================================================

request_b = ResourceRequest(
    task_id=request_a.task_id,
    execution_context_id=CTX_B,
    model_form=request_a.model_form,
    reasoning_mode=request_a.reasoning_mode,
    priority=request_a.priority,
    source=request_a.source,
    reasons=request_a.reasons,
    may_defer=request_a.may_defer,
)

assert request_a.execution_context_id == CTX_A
assert request_b.execution_context_id == CTX_B
assert request_a != request_b

print("PASS 12: changing resource target creates a distinct request")


print()
print("12 PASS / 0 FAIL")
print("14.11H.6C status: 0")
