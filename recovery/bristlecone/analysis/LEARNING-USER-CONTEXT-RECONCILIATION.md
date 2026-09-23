# Bristlecone Pine — Learning, User Context, and Layered Hot Context Reconciliation

Status: **RECONCILED FROM SURVIVING CURRENT SOURCE + PHASE 14.6/14.7 CHECKPOINT EVIDENCE**

## Recovery conclusion

The current recovered cache/learning tree is selected as the best late Bristlecone implementation for:

- Forest cache coordination
- Operational Learning
- User Context
- Warm indexes
- deterministic context/learning routing
- Context Route State
- Task-Sticky User Context / Operational Learning
- historical snapshot retrieval
- Layered Hot Context
- immutable turn instruction composition

This is **not byte-certification** of the current files against one terminal-certified backup.

It is a reconstruction conclusion based on chronology and consistency:

1. multiple earlier Phase 14.6/14.7 source snapshots survive;
2. the current files are later distinct revisions, not regressions to earlier copies;
3. the recovered 2026-08-11 master checkpoint records Phase 14.6 learning/User Context work and Phase 14.7 Layered Hot Context as complete;
4. the master checkpoint names the same main module family and APIs found in the current source;
5. the dedicated User Context checkpoint preserves the same routing/generation/Task-Sticky doctrine implemented by the surviving code;
6. no conflicting later source copy has been found.

## Selected current implementation

### Cache

- cache/__init__.py
- cache/coordinator.py
- cache/entry.py

### Learning / User Context

- learning/__init__.py
- learning/foundation.py
- learning/indexes.py
- learning/context_matcher.py
- learning/operational.py
- learning/operational_matcher.py
- learning/context_state.py
- learning/snapshot_provider.py
- learning/turn_retrieval.py
- learning/hot_context.py
- learning/turn_instruction.py

## Historical lineage retained

Earlier snapshots remain in raw-import, including:

- Phase 14.6F2 Operational Learning
- Phase 14.6F3A1/F3A2 learning indexes
- Phase 14.6F4A0/F4A1/F4A2 foundation/index/matcher work
- Phase 14.7C1 Context Route State
- Phase 14.7C3A foundation
- Phase 14.7C4A1 CacheCoordinator
- Phase 14.7C4B2 foundation
- Phase 14.7C4C1 snapshot provider
- Phase 14.7C5D turn retrieval
- Phase 14.7D2B turn instruction

These snapshots establish implementation progression but are not selected over the later current source.

## Recovered invariants

### Authority

Explicit user context outranks inferred personalization.

Recovered precedence:

1. current explicit instruction
2. correction
3. explicit constraint / preference
4. strong learned pattern
5. Syrup inference
6. weak inference

### Cold / Warm / Hot

- Cold stores durable truth.
- Warm decides relevance through indexes/triggers.
- Hot contains only the records selected for the current meaningful turn.

### Separate durable generations

User Context and Operational Learning have independent generations:

- user_context_generation
- operational_learning_generation

This allows one domain to invalidate without unnecessarily discarding the other.

### Context Route State

Conversation/input changes invalidate routing.

Execution steps do not.

A Context Route Stamp memoizes the deterministic routing result for one meaningful input.

### Task-Sticky state

Selected User Context and Operational Learning may remain Task-Sticky while:

- the Task remains active,
- the relevant durable generation remains valid,
- the records remain relevant,
- policy permits them.

Retained sticky records are not automatically reused after a new meaningful input until routing selects them again.

### Shared truth, local selection

Forest/Tree/Colony infrastructure may share immutable knowledge/index/cache objects.

Task/Clone routing state remains local.

Turn-local selections remain immutable for that turn.

### Historical retrieval

The current snapshot/retrieval path preserves historical visibility:

- old turns may resolve the record revision visible at their captured generation;
- future generations fail closed;
- same Cold misses can single-flight;
- historical misses must not mutate newer Task-Sticky state.

### Hot Context

The recovered current assembler is stateless and deterministic.

Semantic rendering order is:

1. User Corrections
2. User Constraints
3. User Preferences
4. Current Context
5. Operational Learning

### Turn freeze / runtime recovery

One meaningful turn performs context resolution/retrieval/assembly once.

Runtime retries or stale-session recovery reuse the same final instruction snapshot and must not reopen routing/retrieval/Hot Context assembly.

## Recovered performance evidence

The later master checkpoint records Phase 14.7 measurements including:

- Hot assembler p50: 7.77 µs
- Hot assembler p95: 11.28 µs
- full sticky compose p50: 24.54 µs
- full sticky compose p95: 36.28 µs
- provider warm p50: 50.69 µs
- provider warm p95: 77.62 µs
- provider cold p50: 2.373 ms
- provider cold p95: 2.525 ms
- 1 Clone shared-cold wall: 2.65 ms
- 10 Clone shared-cold wall: 9.34 ms
- 50 Clone shared-cold wall: 17.72 ms

The checkpoint's architectural conclusion is that Forest-side bookkeeping had become negligible compared with historical model/runtime latency.

## Recovery caveat

These current source files are selected as the best recovered late implementation, but they are not being declared modern Post-Apollo production code.

The modern Rust/QML Forest should preserve these behavioral contracts unless deliberately superseded, while re-certifying any implementation-specific correctness/performance claims.
