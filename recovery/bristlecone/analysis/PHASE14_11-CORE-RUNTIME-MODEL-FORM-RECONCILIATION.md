# Bristlecone Pine — Phase 14.11 Core Runtime / Model Form Reconciliation

Status: **RECONCILED — CERTIFIED-HEAVY**

## Recovery conclusion

The surviving late Bristlecone Task Session, Session Identity/Store, Model Form, Handoff/Continuity, and model-residency source is selected as the best recovered historical implementation.

This is the strongest reconstruction area so far: the current files are largely byte-identical to source preserved inside certified Phase 14.11 checkpoints.

## Task Session

Selected:

- `runtime/task_session.py`

Current SHA-256:

`d666cb1471b568bf43db4255f5e84e98c1ea502af467e1e2670e4a93dc364991`

Exact certified matches survive across multiple later checkpoints, including:

- H.5G
- H.6D
- H.7 final
- I.9 final
- J.1 real Small
- J.2 real commit
- J.3 real reuse
- J.4 real multi-context
- L.9 A recovery
- L.10 A sustained-session

The L.10 certified source snapshot is byte-identical to the current recovered file.

This establishes that the surviving current Task Session is not merely a plausible later copy; it is the exact implementation used by late certified real-runtime work.

## Session Identity / Store

Selected:

- `runtime/session_identity.py`
- `runtime/session_store.py`

Current hashes:

- session_identity.py: `8a1d668e898dc2df7b60fd5099be0cf42dd2d4c864cbe163164f0a061a777353`
- session_store.py: `3c3449fa878920ea27f39b6216cf38a687d09a08da1d5b57af68c1a2f4beb48f`

Both have exact certified matches.

The H.B5 independent certification preserves the identifier doctrine:

- `tree_id` = durable Tree / Colony identity
- `execution_context_id` = individual Ortet/Ramet execution context
- `binding_id` = selected model/runtime binding
- `session_id` = one live runtime session
- `residency_id` = one shared immutable model-weight residency

Runtime-session lookup/write requires both:

`execution_context_id + binding_id`

## Model residency

Selected:

- `runtime/model_residency.py`

Current SHA-256:

`a09e7c2a6203eafd8f1d748b65798d87d0b281635f0b2515addbba4027b7df63`

Exact certified matches survive through H.7 final and related H checkpoints.

Recovered H.7 doctrine:

- session state is per execution-context + binding
- model weights may be shared by multiple execution contexts
- shared residency must not contain per-context Task/control/KV state

## Model Form package

Selected current package:

- `model_form/__init__.py`
- `model_form/model.py`
- `model_form/control.py`
- `model_form/registry.py`
- `model_form/resolution.py`
- `model_form/bindings.yaml`
- `model_form/handoff.py`
- `model_form/handoff_detection.py`
- `model_form/continuity.py`
- `model_form/automatic_router.py`
- `model_form/automatic_routing.py`
- `model_form/automatic_routing_evidence.py`
- `model_form/automatic_routing_policy.py`

Every selected current Python file above has at least one exact certified backup match. `bindings.yaml` also has exact certified matches.

### Important G.7 distinction

The G.7 final certification explicitly says that `automatic_router.py` is retained as the earlier isolated prototype/regression artifact.

The authoritative production routing path is:

```text
model_form/automatic_routing.py
model_form/automatic_routing_evidence.py
model_form/automatic_routing_policy.py
model_form/resolution.py
runtime/task_session.py
```

Therefore the recovery keeps `automatic_router.py` for historical/regression completeness but does not misidentify it as the authoritative production router.

## Automatic Model Form routing

Recovered G.7 production path:

```text
Frozen effective Reasoning
    ↓
AutomaticModelFormRoutingInput
    ↓
recommend_automatic_model_form()
    ↓
Task/context-bound recommendation
    ↓
canonical Model Form precedence/resolution
    ↓
FrozenModelFormTurn
    ↓
exact ResourceRequest
    ↓
Governor
    ↓
runtime/session execution
```

Certified boundaries include:

- router decides whether Small or Big would be useful
- router consumes normalized semantic evidence only
- router observes already-resolved Reasoning but cannot mutate it
- router does not inspect Governor/resource availability
- Governor cannot rewrite Reasoning or Model Form
- resource pressure does not trigger semantic rerouting
- stale recovery reuses the same frozen Model Form
- retry failure does not reroute
- Task/context mismatch fails closed
- Deep does not mechanically imply Big
- Light does not mechanically imply Small

## Handoff / Continuity

Selected:

- `model_form/handoff.py`
- `model_form/handoff_detection.py`
- `model_form/continuity.py`
- `runtime/conversation_continuity.py`

All have exact certified matches in the Phase 14.11 E-series recovery corpus.

The recovered architecture separates:

- immutable handoff contract
- pure handoff detection
- portable conversation continuity
- combined Model Form continuity
- runtime/session mechanics

## L.10 sustained-session certification

The promoted L.10 certification used:

- real Hermes runtime
- real Small inference
- Normal Reasoning
- binding-0001
- one unmeasured prime
- eight measured same-session turns
- `persist=False`

Certified findings:

- 8/8 measured turns
- one unique measured runtime session
- zero unexpected recovery
- zero unexpected rotation
- stable session identity
- stable Model Form
- stable Reasoning
- stable binding
- stable execution context
- warm residency maintained
- persistent production state unmodified

The certification deliberately did **not** claim latency improvement, degradation, or a memory leak from the small sample.

## Recovery strength

For this subsystem, "RECONCILED" is stronger than a prose/checkpoint inference.

The selection is grounded primarily in exact SHA-256 identity between the surviving current production tree and certified source snapshots.

## Modernization caveat

These files define the recovered historical behavior and regression contract.

The modern Post-Apollo Forest may replace the Python implementation with Rust and replace Hermes/model bindings, but should preserve the certified semantic boundaries unless deliberately redesigned and re-certified.
