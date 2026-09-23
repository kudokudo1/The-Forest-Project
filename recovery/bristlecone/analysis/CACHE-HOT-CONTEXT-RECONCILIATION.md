# Bristlecone Pine — Cache / Layered Hot Context Reconciliation

Status: **RECONCILING**

## Current finding

The recovered current cache/learning files do **not** have byte-identical matches elsewhere in the rescued corpus.

However, they sit on top of a clear Phase 14.7 lineage with multiple earlier backups and explicit architecture/checkpoint documents.

Important current files include:

- cache/__init__.py
- cache/coordinator.py
- cache/entry.py
- learning/context_state.py
- learning/foundation.py
- learning/snapshot_provider.py
- learning/turn_retrieval.py
- learning/hot_context.py
- learning/turn_instruction.py

Later learning files also survive:

- learning/indexes.py
- learning/context_matcher.py
- learning/operational.py
- learning/operational_matcher.py

## Earlier source lineage

Recovered pre/current snapshots include:

- Phase 14.7C1 — learning/context_state.py
- Phase 14.7C3A — learning/foundation.py
- Phase 14.7C4A1 — cache/coordinator.py
- Phase 14.7C4B2 — learning/foundation.py
- Phase 14.7C4C1 — learning/snapshot_provider.py
- Phase 14.7C5D — learning/turn_retrieval.py
- Phase 14.7D2B — learning/turn_instruction.py

The current versions are later distinct revisions, so rollback to those backups would risk deleting legitimate later work.

## Recovered doctrine

The Phase 14.7 checkpoint establishes:

- Clones share knowledge, not mutable live routing state.
- Clone count must not scale infrastructure count.
- Resource cost should scale primarily with active work, not retained Clone count.
- Retain cheaply. Activate selectively. Share aggressively.
- Shared semantic caches belong at Forest/Tree/Colony scope where the underlying truth is shared.
- ContextRouteState and Task-Sticky decisions remain Task-local.
- final Hot Context is turn-local and immutable for that meaningful turn.
- recovery/retry reuses the same assembled Hot Context/instructions.
- caches are derived state, never source of truth.
- User Context and Operational Learning have independent durable generations.

The earlier architecture update also records the reuse-or-rebuild principle:

> Keep stable Task Session layers reusable. When something changes, invalidate only the affected layer or dependent layers, then rebuild the active Hot Context from the remaining reusable pieces.

## Why this subsystem is not yet marked reconciled

Unlike Phase 14.9 Source Context, the current cache/learning files are later than the available Phase 14.7 snapshots and the current corpus contains several subsequent architectural additions.

The recovery must determine whether the current files reflect:

1. the completed Phase 14.7 implementation,
2. later Phase 14.8/14.9 integration work,
3. later User Context / Operational Learning additions,
4. or a mixture of all three.

Until that chronology is mapped, the current files remain strong production candidates rather than selected canonical recovery artifacts.

## Next evidence needed

- later checkpoints that name the current cache/learning APIs
- test/certification references for the later revisions
- chronology linking Phase 14.7 → 14.8 → 14.9
- evidence for the later User Context/Operational Learning additions

Do not replace current source with the older Phase 14.7 backups merely because those backups are named by phase.
