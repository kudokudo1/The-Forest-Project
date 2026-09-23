# Phase 14.11H.5 — Terminal 2 Certification Matrix

Status: PREPARATION ONLY

Production H.5 is still moving.
This document does not certify runtime/task_session.py or Reasoning behavior.

## Colony Fixture

Tree:
- tree_id: bristlecone

Ortet:
- execution_context_id: ctx-O
- lineage_role: ortet

Ramet A:
- execution_context_id: ctx-R1
- lineage_role: ramet

Ramet B:
- execution_context_id: ctx-R2
- lineage_role: ramet

Operational role is independent of lineage role.

---

## H5-01 — Same Tree

ctx-O, ctx-R1, and ctx-R2 may share:

tree_id = bristlecone

PASS:
All three remain members of the same Tree/Colony.

---

## H5-02 — Unique Execution Contexts

PASS:
ctx-O != ctx-R1
ctx-O != ctx-R2
ctx-R1 != ctx-R2

No Ramet state may be keyed only by tree_id.

---

## H5-03 — Lineage / Operational Role Independence

PASS:
Ortet does not mechanically imply Main.
Ramet does not mechanically imply worker.
A Ramet may hold Main or another operational role.

---

## H5-04 — Model Form Isolation

Action:
Change Model Form control for ctx-R1.

PASS:
ctx-R1 changes.
ctx-O unchanged.
ctx-R2 unchanged.

No Tree-global Model Form mutation.

---

## H5-05 — Durable Reasoning Isolation

Action:
Change durable Reasoning control for ctx-R1.

PASS:
ctx-R1 changes.
ctx-O unchanged.
ctx-R2 unchanged.

No Tree-global Reasoning mutation.

---

## H5-06 — Temporary Reasoning Lease Isolation

Fixture:
Temporary Reasoning leases exist for multiple contexts.

Action:
Resolve/finalize one turn for ctx-R1.

PASS:
Only ctx-R1 lease is consumed/decremented/finalized.
ctx-O lease unchanged.
ctx-R2 lease unchanged.

---

## H5-07 — Live-Turn Reasoning Resolution

PASS:
A live turn resolves effective Reasoning using its
execution_context_id.

No sibling execution context contributes durable or
temporary Reasoning state.

---

## H5-08 — Workshop Isolation

Action:
Activate/change Workshop state for ctx-R1.

PASS:
ctx-R1 changes.
ctx-R2 unchanged.
ctx-O unchanged where applicable.

---

## H5-09 — Temporary Capability Isolation

Action:
Grant/consume temporary Task capability in ctx-R1.

PASS:
No capability appears in ctx-O or ctx-R2.

---

## H5-10 — Task-Sticky Skill Isolation

Action:
Attach Task-sticky Skill state to ctx-R1.

PASS:
No Skill state leaks into ctx-O or ctx-R2.

---

## H5-11 — Runtime Session Isolation

Same binding is permitted.

PASS:

(ctx-O, binding-1)  -> session-O
(ctx-R1, binding-1) -> session-R1
(ctx-R2, binding-1) -> session-R2

session-O != session-R1 != session-R2

---

## H5-12 — Shared Residency

Same immutable weights are permitted.

PASS:
Multiple Colony contexts may reference one compatible
SharedModelResidency.

Shared residency contains no:
- execution_context_id
- session_id
- Task state
- Reasoning state
- permissions
- KV/conversation state

---

## H5-13 — Legacy ctx-default Compatibility

Legacy Reasoning state may remain readable through the
designated ctx-default compatibility path.

PASS:
Existing single-context/legacy state behaves deterministically.

Compatibility must not convert legacy state into an implicit
Tree-global value for every future execution context.

---

## H5-14 — New Ramet Does Not Inherit Legacy Global Reasoning

Fixture:
Legacy reasoning_control exists.

Create/use a new non-default Ramet execution context.

PASS:
The new Ramet does not silently inherit legacy global
Reasoning merely because it shares tree_id.

Any fallback behavior must follow the explicit compatibility
contract.

---

# Cross-Layer Doctrine

tree_id
= Tree / Colony

execution_context_id
= Ortet/Ramet execution context

binding_id
= model/runtime binding

session_id
= live runtime session

residency_id
= shared immutable model weights

These identities must remain distinct.

Resource-management targeting of one Ramet must use the
execution-context boundary and must not accidentally become:

- Tree-wide
- binding-wide
- session-wide
- residency-wide

---

# Certification Gate

Terminal 2 MUST NOT execute final H.5 certification until
Terminal A provides:

1. H.5 candidate checkpoint
2. exact production SHAs
3. exact test SHAs
4. confirmation that H.5 production is frozen

First Terminal-2 action after handoff:

VERIFY SHAs.

If any SHA differs:

STOP — candidate drift.

Only after SHA verification may H.5 certification run.
