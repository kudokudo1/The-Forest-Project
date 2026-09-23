# Project Forest — Phase 14.7 Colony / Hot Context Checkpoint
Date: 2026-08-09

## Current phase state
Phase 14.6 is complete. Current work is Phase 14.7 — Layered Hot Context.

14.7A prompt/instruction ownership is complete:
- `send_runtime_turn()` does not assemble instructions.
- It accepts `instructions` from its caller.
- The same `instructions` string is reused on normal runtime send and stale-session recovery.
- Hot Context should be assembled once before `send_runtime_turn()` and reused unchanged through recovery.

## Colony / Clone concurrency decision
Tree/Clone architecture materially affects Hot Context implementation.

> Clones share knowledge, not mutable live routing state.
> Clone count must not scale infrastructure count.
> Resource cost should scale primarily with active work, not retained Clone count.
> Retain cheaply. Activate selectively. Share aggressively.
> Share the knowledge object, not the contextual decision.
> Concurrent identical work should collapse into one shared operation when the underlying truth is shared.
> An in-flight turn must not be invalidated merely because another turn begins.
> Hot Context is assembled once per meaningful turn and reused for runtime recovery/retry.
> The Hot Context assembler is stateless and Clone-neutral.

### Forest / Tree / Colony shared
- CacheCoordinator
- Warm User Context Trigger Index
- Warm Operational Learning Index
- deterministic context matchers
- capability-resolution cache
- parsed-YAML cache
- future immutable authoritative record snapshot cache
- future single-flight Cold record loader
- stateless LayeredHotContextAssembler logic

### Task-local
- ContextRouteState
- Context Route Stamp
- Task-Sticky User Context
- Task-Sticky Operational Learning
- capability/Skill activation state
- Task-specific routing selections

### Turn-local
- immutable route snapshot for one meaningful request
- selected record IDs for that turn
- assembled Hot Context result
- final instructions passed to the runtime
- per-turn source targeting

### Runtime-owned / leased
- model residency
- KV/inference cache
- runtime sessions
- GPU/inference slots
- device/resource leases
- Hermes-native runtime/tool state while Hermes remains authoritative

## Novice-user protection
Forest should tolerate users creating too many Clones. A novice may manually create a Clone for every small task without understanding the performance consequences. The architecture should degrade gracefully:
- retained Clone identity/state is cheap
- dormant Clones consume little/no compute
- Warm/Cold Forest knowledge remains shared
- capability definitions remain shared
- only active work receives Task/Turn state
- expensive resources are leased and bounded
- Spirit can later recommend reuse/consolidation, but correctness/performance must not depend on user expertise

Persistent Clone does not mean permanent compute.

## Power-user / mass-test behavior
Logical concurrency and physical concurrency are separate concepts.

Example:
- 100 logical test Clones
- 1 shared User Context index
- 1 shared Operational Learning index
- 1 shared capability cache
- 1 model installation
- N bounded inference workers / GPU slots
- remaining logical work queued or dormant

## Shared immutable record snapshot cache
Planned for Phase 14.7C.

Many simultaneous Clones may select the same authoritative record and independently Cold-load it. Add a Forest-shared immutable record snapshot cache:
- key by authoritative identity/revision/freshness data
- cache authoritative `ForestLearningRecord` snapshots only
- Tasks/Clones may share the immutable record object
- Tasks/Clones do NOT share selection/relevance/permission decisions
- cache remains derived/disposable and never authoritative
- do not create per-Clone record caches

## Single-flight Cold loading
Planned for Phase 14.7C.

A normal shared cache can still permit a cache stampede. Instead:
- first caller performs the Cold load
- concurrent callers requesting the same record wait for/share that result
- different record IDs may load concurrently
- avoid global serialization
- follow the same general concurrency principle already proven in the dormant Tool Availability Provider

This protects mass tests, automations, large Colonies, and novice-created excessive Clone counts.

## Same-Task simultaneous-turn protection
Current `ContextRouteState` is correct for sequential turns in one Task and many simultaneous Tasks/Clones.

Potential race: two meaningful requests may be active simultaneously inside the exact same Task.

Planned improvement: use an immutable per-turn route snapshot containing:
- input_generation
- user_context_generation
- operational_learning_generation
- policy_generation
- selected User Context IDs
- selected Operational Learning IDs
- routing metadata needed for that turn

A later turn can advance Task routing state without mutating an earlier in-flight turn's snapshot. Runtime recovery/retry reuses the same snapshot and assembled instructions.

## Hot Context assembler contract
The assembler is stateless and concurrency-safe.

Input:
- already-selected authoritative User Context records
- already-selected authoritative Operational Learning records

Output:
- immutable HotContextAssembly
- one deterministic model-facing string fragment
- selected record IDs
- section metadata/counts
- character count

Responsibilities:
- validate record boundaries
- preserve semantic authority ordering
- format records deterministically
- produce compact prompt fragment
- expose metadata
- optionally enforce a fail-closed character budget

Non-responsibilities:
- raw prompt parsing
- relevance decisions
- Warm matching
- Cold loading
- ContextRouteState ownership
- cache ownership
- runtime/Hermes/Ollama calls
- permission decisions
- KV/model caching

## User Context ordering inside Hot Context
1. User Corrections
2. User Constraints
3. User Preferences
4. Current Context
5. Operational Learning

Current user instruction and active Forest/Spirit policy remain above remembered Hot Context. Explicit User Context outranks inferred personalization such as Syrup.

## Revised Phase 14.7 roadmap

### 14.7A — Prompt/instruction boundary
COMPLETE.

### 14.7B — Hot Context architecture
- 14.7B.0 Colony concurrency contract — COMPLETE
- 14.7B.1 Stateless LayeredHotContextAssembler
- 14.7B.2 Assembler behavior verification

### 14.7C — Context retrieval bridge
- per-turn immutable route snapshot
- Task-Sticky lookup
- Cold-load only missing selected records
- Forest-shared immutable record snapshot cache
- single-flight Cold miss loading
- independent generation correctness
- no cross-Task relevance leakage

### 14.7D — Instruction composition
- combine existing caller instructions with Forest Hot Context once
- preserve current instruction semantics
- pass one final string into `send_runtime_turn()`
- recovery reuses same assembled string

### 14.7E — Concurrency verification
Test many Tasks, many Clone-like callers, same-record stampede, different-record parallel loads, simultaneous turns, Task isolation, recovery reuse, and generation changes.

### 14.7F — Performance benchmark
Benchmark 1, 10, and 50 Clones plus a pathological/high novice Clone count; compare repeated shared-record requests and Warm hits vs Cold misses. Keep extra complexity only where benchmark evidence justifies it.

## Existing invariants retained
- Caches are derived, never source of truth.
- Forest-shared semantic caches should use shared infrastructure where appropriate.
- Injected shared infrastructure uses explicit `is not None`, not truthiness.
- User Context and Operational Learning have independent durable generations.
- Conversation changes invalidate routing; execution steps do not.
- New meaningful input invalidates routing but may retain Task-Sticky data provisionally.
- Relevant generation changes invalidate only the corresponding sticky pool.
- Policy changes may invalidate both pools.
- Tree/Clone/Colony identity stays outside ContextRouteState; its owner establishes scope.
- No blind reruns.
- Back up existing source before modification.
- Avoid duplicate caching of the same representation across Forest/adapter/runtime.
- Forest-native replacements must not duplicate Hermes-owned runtime behavior while Hermes remains authoritative.
