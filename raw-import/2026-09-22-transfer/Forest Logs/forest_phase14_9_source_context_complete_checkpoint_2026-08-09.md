# Project Forest / Bristlecone Pine — Phase 14.9 Complete Checkpoint
**Prepared:** 2026-08-09  
**Status:** **PHASE 14.9 — SOURCE-CONTEXT TARGETING: COMPLETE**  
**Next Phase:** **14.10 — Quick / Normal / Deep**

---

# 1. Final Certification

Phase 14.9 is complete.

Completed areas:

- ✅ 14.9B — Shared Objective Source Foundation
- ✅ 14.9C — Turn-Local Targeting, Expansion, Packets, Rendering
- ✅ 14.9D — Forest-Level Turn Composition + Runtime Recovery Contract
- ✅ 14.9E — Closeout Boundary Audit + Final Benchmark

Final interpretation:

> **Source Context is now a complete Forest-owned subsystem that can identify, validate, structurally index, target, bound, render, and compose relevant source material into one final turn instruction snapshot without making Learning or Runtime own source-context behavior.**

Production application wiring is intentionally deferred because the current codebase contains **no production caller above `TaskSessionManager.send_runtime_turn()`**.

Creating a caller solely to claim 14.9 was wired would invent application architecture that does not yet exist.

Therefore:

> **Production application wiring is deferred by architecture, not missing from Phase 14.9.**

---

# 2. Phase 14.9 Final Architecture

```text
SourceIdentity
    ↓
SourceFingerprint
    ↓
LocalSourceObserver
    ↓
SourceContentSnapshot
    ↓
objective SourceStructure
    ├─ Python AST structure
    └─ Markdown heading structure
    ↓
shared exact-version structure provider/cache
    ↓
canonical turn signals
    ↓
SourceReferenceMatcher
    ↓
SourceTarget
    ↓
BoundedSourceTargetExpander
    ↓
SourcePacket
    ↓
DeterministicSourcePacketRenderer
    ↓
RenderedSourcePacket
    ↓
ForestTurnInstructionComposer
    ├─ existing Learning instructions
    └─ rendered Source Context
    ↓
one immutable final `instructions` string
    ↓
TaskSessionManager.send_runtime_turn(...)
    ↓
runtime
```

The runtime remains generic.

It does not need to know whether the final instruction string contains:

- Learning Context
- Source Context
- both
- neither

---

# 3. Ownership Boundaries

Canonical ownership:

> **Source Context is Forest-owned, not Learning-owned and not runtime-adapter-owned.**

Verified reverse-coupling state:

```text
learning/turn_instruction.py  → Source Context import: NO
learning/hot_context.py       → Source Context import: NO
learning/turn_retrieval.py    → Source Context import: NO

runtime/task_session.py       → Source Context import: NO
runtime/adapters/base.py      → Source Context import: NO
runtime/adapters/hermes.py    → Source Context import: NO
```

Forest-level composition:

```text
turn_composition.py
```

may consume `RenderedSourcePacket`, but intentionally imports no:

```text
learning
runtime
cache
```

This preserves subsystem independence.

---

# 4. Phase 14.9 Files

Created during Phase 14.9:

```text
source_context/__init__.py
source_context/model.py
source_context/observation.py
source_context/snapshot.py
source_context/structure.py
source_context/structure_provider.py
source_context/markdown_structure.py
source_context/markdown_structure_provider.py
source_context/targeting.py
source_context/reference_matcher.py
source_context/target_expansion.py
source_context/packet.py
source_context/rendering.py
turn_composition.py
```

Important existing integration/runtime files that were inspected but not made to own Source Context:

```text
learning/foundation.py
learning/snapshot_provider.py
learning/turn_retrieval.py
learning/hot_context.py
learning/turn_instruction.py

runtime/task_session.py
runtime/adapters/base.py
runtime/adapters/hermes.py
runtime/adapters/factory.py
```

---

# 5. 14.9B — Shared Objective Source Foundation

## 5.1 Source Models

Created:

```text
source_context/model.py
```

Models:

- `SourceIdentity`
- `SourceFingerprint`
- `SourceRegion`
- `SourceTarget`

Important separation:

```text
stable source identity
≠
source version/fingerprint
≠
turn-local relevance
```

---

## 5.2 Local Source Observation

Created:

```text
source_context/observation.py
```

Core:

```text
LOCAL_FILE_FINGERPRINT_METHOD = "stat-size-mtime-v1"
LocalSourceObservationError
LocalSourceObserver
```

Responsibilities:

- canonical path resolution with `resolve(strict=True)`
- regular-file validation
- stable default source identity
- metadata-only observation
- fingerprint components:
  - `size`
  - `mtime_ns`

No source-content read.

No cache ownership.

No runtime ownership.

---

## 5.3 Safe Immutable Source Snapshot

Created:

```text
source_context/snapshot.py
```

Core:

- `SourceSnapshotError`
- `SourceChangedDuringReadError`
- `SourceContentSnapshot`
- `LocalSourceSnapshotReader`

Read safety sequence:

```text
observe
→ stat
→ open rb
→ fstat before
→ read
→ fstat after
→ stat path after
→ observe after
→ verify
→ strict decode
→ immutable snapshot
```

Transient race-safety evidence:

```text
(st_dev, st_ino, st_size, st_mtime_ns)
```

Persistent cheap fingerprint remains:

```text
size + mtime_ns
```

Content-derived cache identity also includes:

```text
content_sha256
```

Important rule:

> **Metadata fingerprint is cheap reusable freshness identity; content SHA256 protects content-derived cache identity exactly.**

---

## 5.4 Python Objective Structure

Created:

```text
source_context/structure.py
```

Core:

```text
PYTHON_STRUCTURE_KIND = "python-ast-v1"
SourceStructureError
SourceStructure
PythonSourceStructureBuilder
```

Objective regions include:

- `python:module`
- class
- function
- async function
- method
- async method

Structure is derived from immutable snapshot only.

No direct filesystem I/O.

No runtime/model dependency.

---

## 5.5 Python Shared Structure Provider

Created:

```text
source_context/structure_provider.py
```

Core:

- `PythonSourceStructureProvider`
- shared `CacheCoordinator`
- exact-snapshot cache identity
- per-key single-flight

Cache identity includes:

```text
source_id
structure kind
fingerprint method/components
content_sha256
```

Verified:

- warm reuse
- old/new versions coexist
- same-size/same-mtime different content does not collide
- 1 / 10 / 50 logical Clone callers perform one parse for identical source truth
- different keys may parse concurrently

Rule:

> **Exact-snapshot single-flight, not global parsing serialization.**

---

## 5.6 Markdown Objective Structure

Created:

```text
source_context/markdown_structure.py
```

Core:

```text
MARKDOWN_STRUCTURE_KIND = "markdown-headings-v1"
MarkdownStructureError
MarkdownSourceStructureBuilder
```

Supports:

- ATX headings
- Setext headings
- heading hierarchy
- section boundaries
- duplicate headings
- fenced code blocks ignored during heading recognition
- whole source `markdown:document`

---

## 5.7 Markdown Shared Provider

Created:

```text
source_context/markdown_structure_provider.py
```

Uses the same architectural rules as Python structure caching:

- exact source-version key
- content SHA256
- shared immutable structure
- per-key single-flight
- old/new versions coexist
- 1 / 10 / 50 Clone callers collapse to one build

---

# 6. 14.9C — Turn-Local Source Relevance

## 6.1 Explicit Targeting

Created:

```text
source_context/targeting.py
```

Core:

- `SourceTargetingError`
- `SourceTargetNotFoundError`
- `SourceTargetAmbiguityError`
- `DeterministicSourceTargeter`

Supported deterministic target forms:

```text
exact region_id
exact unique label
```

Rules:

- duplicate labels fail closed
- explicit region ID disambiguates
- no fuzzy match
- no semantic match
- no embedding
- no LLM target selection
- no automatic whole-source fallback

Boundary:

```text
COLONY-SHAREABLE
SourceSnapshot
SourceStructure
SourceRegion

TURN-LOCAL
SourceTarget
```

---

## 6.2 Canonical Source Reference Matching

Created:

```text
source_context/reference_matcher.py
```

Canonical signal behavior was verified against existing Forest Learning matcher conventions.

Canonicalization:

- trim surrounding whitespace
- preserve case
- preserve first-seen order
- deduplicate after stripping
- reject:
  - empty strings
  - whitespace-only strings
  - non-string entries

Resolution order:

```text
1. exact region_id
2. exact unique label
3. explicit ambiguity
4. unmatched
```

Region IDs are structurally authoritative and take precedence over visible labels.

Important doctrine:

> **Source reference matching consumes canonical turn signals; it does not parse raw prompts.**

---

## 6.3 Bounded Ancestor Target Expansion

Created:

```text
source_context/target_expansion.py
```

Core:

- `SourceTargetExpansionError`
- `SourceTargetExpansion`
- `BoundedSourceTargetExpander`

Rules:

- exact target first
- ancestors only
- explicit `max_parent_hops`
- no sibling expansion
- no child expansion
- no unrelated regions
- whole-source ancestor blocked by default
- whole-source ancestry requires explicit permission
- malformed parent references fail closed
- cycles fail closed

Important rule:

> **Being structurally related does not automatically make all related source relevant.**

---

## 6.4 Bounded Source Packet

Created:

```text
source_context/packet.py
```

Core:

- `SourcePacketError`
- `SourcePacketBudgetError`
- `SourcePacketFragment`
- `SourcePacket`
- `SourcePacketAssembler`

Critical rule:

> **Targets contribute source text. Ancestors contribute structural breadcrumbs unless they were independently targeted.**

This avoids a parent class or parent Markdown section silently importing sibling content.

Features:

- exact target source text
- overlapping target ranges deduplicated
- non-overlapping targets remain distinct fragments
- ancestor labels/IDs retained
- explicit whole-source target supported
- whole-source ancestor alone does not import full file
- hard character budget
- hard line budget
- fail closed
- never silently truncate source truth

Important provenance rule:

> **A packet records not only what source truth was selected, but also the bounds under which that selection was authorized.**

Therefore identical selected source under different budgets is intentionally not equal as a packet value.

---

## 6.5 Deterministic Source Rendering

Created:

```text
source_context/rendering.py
```

Core:

- `SourcePacketRenderError`
- `SourcePacketRenderBudgetError`
- `RenderedSourcePacket`
- `DeterministicSourcePacketRenderer`

Rendering includes:

- source ID
- source kind
- display name
- content SHA256
- target region IDs
- ancestor breadcrumbs
- fragment line ranges
- exact selected source text

Safety:

- dynamic outer code-fence marker/length
- source content cannot close its own outer fence
- local filesystem locator/path hidden by default
- locator inclusion is opt-in
- hard rendered-character budget
- no silent truncation

Important privacy boundary:

> **Source provenance does not automatically authorize disclosure of an absolute filesystem path.**

---

# 7. 14.9D — Forest-Level Turn Composition

## 7.1 Integration Preflight

Preflight proved:

```text
TaskSessionManager.send_runtime_turn(
    self,
    message,
    state=None,
    instructions=None,
    persist=False,
)
```

The runtime receives generic precomposed `instructions`.

Stale recovery passes the same local `instructions` value to the replacement session.

No Source Context import exists in runtime.

No production caller exists above `send_runtime_turn()`.

Therefore the correct composition architecture is:

```text
Learning output ──────────────┐
                              │
Rendered Source Context ──────┼─► Forest-level composition
                              │
                              ▼
                    final instructions
                              │
                              ▼
                         Runtime
```

---

## 7.2 ForestTurnInstructionComposer

Created:

```text
turn_composition.py
```

Core:

- `ForestTurnCompositionError`
- `ForestTurnCompositionBudgetError`
- `ForestTurnInstructionComposition`
- `ForestTurnInstructionComposer`

### No-source compatibility

Verified:

```python
composition.instructions is learning_instructions
```

when Source Context is absent.

This means:

> **Phase 14.9 adds zero wrapper or string mutation to ordinary no-source turns.**

### Source attachment authority

Source Context is marked:

```text
authority: reference-data
```

with explicit notice that Source Context does not override:

- current user instruction
- Forest policy
- permissions / Spirit
- higher-priority instruction authority

### Other verified behavior

- exact duplicate rendered packets collapse first-seen
- distinct packets preserve first-seen order
- hard final-character budget
- no silent truncation
- deterministic
- frozen/hashable
- inspection avoids exposing source/instruction bodies
- imports no Learning/runtime/cache subsystem
- invokes no runtime/model machinery

---

# 8. 14.9D Runtime Recovery Proof

A real `TaskSessionManager.send_runtime_turn()` execution was tested using:

- a real disposable Forest Task created with `start_task(..., persist=False)`
- a fake injected runtime adapter
- no runtime factory
- no Hermes
- no Ollama

Important lifecycle finding:

```python
result = manager.start_task(...)
runtime_state = result["state"]
```

`start_task()` returns the new state; it does not mutate the input object in place.

The active Task guard remained fully enabled.

No guard was bypassed.

---

## 8.1 Stale-Recovery Result

Verified runtime sequence:

```text
final Forest instructions object I
        ↓
runtime session S1 receives I
        ↓
synthetic stale-session error
        ↓
real Forest one-shot recovery
        ↓
replacement session S2 receives SAME I
```

Object identity:

```python
first_instructions is final_instructions
recovery_instructions is final_instructions
first_instructions is recovery_instructions
```

All passed.

---

## 8.2 Runtime Recovery Recomputations

Tripwires were installed after the final instruction snapshot was created.

During first runtime execution + stale recovery:

```text
source observation                 0
source snapshot reads              0
source structure builds            0
source reference matching          0
source targeting                   0
target expansion                   0
packet assembly                    0
packet rendering                   0
Forest final composition           0
Learning recomputation             0
Hot Context assembly               0
```

This is now a canonical invariant:

> **Source Context participates in meaningful-turn composition, not runtime execution.**

And:

> **Once the final Forest instruction snapshot exists, runtime recovery is forbidden from reopening any upstream context/composition stage.**

---

# 9. Phase 14.9 Closeout Boundary Audit

Final audit verified:

- all expected 14.9 modules exist
- all modules parse
- Source Context imports no Learning/runtime subsystem
- Learning imports no Source Context
- Runtime imports no Source Context
- Forest turn composer may consume Source Context
- Forest turn composer imports no Learning/runtime/cache
- runtime remains generic
- no production caller above `send_runtime_turn()` exists

Final production-wiring interpretation:

```text
Production application wiring can be performed now: NO
Reason: no caller exists.
```

Creating one solely to complete 14.9 would invent application architecture.

Therefore production wiring is explicitly deferred.

---

# 10. Phase 14.9E.1 Final Benchmark

Representative source contained:

- one selected method
- one sibling method that must not leak
- one unrelated top-level function that must not leak

Correctness verified:

- selected source present
- sibling source absent
- unrelated source absent
- local locator/path absent
- deterministic final instruction output
- no persistent state mutation
- no runtime session
- no Hermes
- no Ollama

---

## 10.1 Warm Turn-Local Pipeline

Includes:

```text
SourceReferenceMatcher
→ target expansion
→ packet assembly
→ rendering
→ Forest final composition
```

500 samples:

```text
p50: 65.95 µs
p95: 100.37 µs
max: 323.11 µs
```

Interpretation:

> Turn-local Source Context overhead is comfortably sub-millisecond on the representative source.

---

## 10.2 Full Cold Source Pipeline

Includes:

```text
source snapshot read
→ Python AST structure parse
→ reference match
→ expansion
→ packet
→ rendering
→ Forest composition
```

30 samples:

```text
p50: 0.301 ms
p95: 0.334 ms
max: 0.564 ms
```

No architectural performance problem was exposed.

---

## 10.3 No-Source Forest Composition Fast Path

1000 samples:

```text
p50: 1.52 µs
p95: 1.67 µs
```

Exact Learning string identity:

```text
YES
```

This confirms the Forest-level composition layer is essentially negligible for ordinary turns with no Source Context.

---

## 10.4 Concurrent Logical Caller Scaling

Shared immutable snapshot/structure; each caller performed its own turn-local selection/composition.

Results:

```text
1 caller:
  p50 0.313 ms
  p95 0.596 ms

10 callers:
  p50 1.954 ms
  p95 2.258 ms

50 callers:
  p50 7.030 ms
  p95 7.691 ms
```

Verified:

- every caller produced identical final instructions
- shared snapshot remained immutable
- shared structure remained immutable

This supports the Colony rule:

> **Share source truth; keep relevance turn-local.**

---

## 10.5 Determinism

100 repeated turn-local pipelines produced the same final instruction SHA256:

```text
7d91bdead53f4c54a44d3bd1668d79024864f1d00c50e6d676ea15372bc74802
```

Deterministic output:

```text
YES
```

---

# 11. Final Phase 14.9 Performance Decision

No optimization patch is justified.

Reasons:

- cold representative path is sub-millisecond
- warm turn-local path is tens of microseconds
- no-source composition is ~1.5 µs p50
- 50 concurrent logical callers complete in single-digit milliseconds p50
- no source leakage
- no path leakage
- deterministic output
- shared source truth remains immutable
- runtime recovery performs zero recomputation

Therefore:

> **Do not optimize Phase 14.9 further before evidence of a real workload bottleneck.**

---

# 12. Canonical Phase 14.9 Invariants

1. Source Context is Forest-owned, not Learning-owned and not runtime-owned.
2. Source truth is shared; source relevance is turn-local.
3. Share parsed source/index, not relevance decisions.
4. Source observation is metadata-only.
5. SourceFingerprint uses cheap stable metadata (`size`, `mtime_ns`).
6. Safe source reads transiently validate device/inode/size/mtime around the read.
7. Content SHA256 protects exact content-derived cache identity.
8. Objective SourceStructure is Colony-shareable.
9. SourceTarget is turn-local.
10. Exact source versions coexist in shared structure caches.
11. Identical concurrent structure builds single-flight by exact key.
12. Canonical source signals trim whitespace.
13. Canonical source signals preserve case.
14. Canonical source signals preserve first-seen ordering.
15. Canonical source signals deduplicate first-seen.
16. Invalid canonical source signals fail closed.
17. Source reference matching consumes canonical signals, not raw prompts.
18. Exact region ID takes precedence over visible labels.
19. Duplicate labels are ambiguous and never guessed.
20. Explicit targeting never silently falls back to whole source.
21. Target expansion is bounded and ancestor-only.
22. Target expansion never adds siblings or children.
23. Whole-source ancestry requires explicit permission.
24. Structural ancestry does not imply ancestor body inclusion.
25. Explicit targets contribute source text.
26. Ancestors contribute breadcrumbs unless explicitly targeted themselves.
27. Overlapping target source is deduplicated.
28. Source packets fail closed on budget overflow.
29. Source truth is never silently truncated.
30. Packet equality retains authorization/budget provenance.
31. Rendered Source Context includes stable provenance and line ranges.
32. Rendered Source Context hides local filesystem locator/path by default.
33. Source provenance does not authorize path disclosure automatically.
34. Render fences must be safe against delimiters inside source content.
35. Rendering fails closed on character-budget overflow.
36. Source Context is reference data, not instruction authority.
37. Source Context cannot override user instruction, Spirit, policy, or higher authority.
38. Forest-level composition belongs neither to Learning nor Runtime.
39. No-source Forest composition returns the exact Learning instruction string unchanged.
40. Exact duplicate rendered packets collapse first-seen.
41. Final instruction composition fails closed on budget overflow.
42. Runtime receives generic precomposed instructions.
43. Runtime does not need Source Context awareness.
44. Runtime recovery is execution, not context recomputation.
45. Final Forest instructions are frozen before runtime execution.
46. First runtime attempt and stale recovery reuse the exact same instruction object.
47. Source observation during runtime recovery = 0.
48. Source reads during runtime recovery = 0.
49. Structure builds during runtime recovery = 0.
50. Reference matching during runtime recovery = 0.
51. Targeting during runtime recovery = 0.
52. Expansion during runtime recovery = 0.
53. Packet assembly during runtime recovery = 0.
54. Rendering during runtime recovery = 0.
55. Forest recomposition during runtime recovery = 0.
56. Learning recomputation during runtime recovery = 0.
57. Hot Context assembly during runtime recovery = 0.
58. Production caller wiring is deferred until a real caller exists.
59. Do not invent orchestration architecture solely to connect a completed subsystem.
60. No additional 14.9 optimization is justified by the representative benchmark.

---

# 13. Relevant Broader Engineering Invariants

Continue preserving these earlier Forest rules:

- Runtime truth before Forest truth.
- If Forest commit fails after runtime mutation, rollback runtime.
- Decision is not the same as runtime reality.
- No blind reruns.
- Existing source requires backup before mutation because this is not a Git repo.
- Caches are derived, never authoritative truth.
- Native inference caches are runtime-owned.
- Runtime session is an opaque continuity handle.
- Clones share durable Tree state, not unrestricted live context.
- Capability is shared; activation is local.
- Clone count must not scale infrastructure count.
- Resource cost should scale primarily with active work.
- Conversation changes invalidate context routing; execution steps do not.
- One meaningful turn retrieves/assembles once.
- Runtime retry/recovery reuses already-frozen instructions.
- Runtime recovery is execution, not new conversational input.
- Retain cheaply. Activate selectively. Share aggressively.

---

# 14. Phase 14 Roadmap Status

Current status:

```text
✅ 14.7 Layered Hot Context
✅ 14.8 Runtime Cache / Prefix Integration
✅ 14.9 Source-Context Targeting
→ 14.10 Quick / Normal / Deep
□ 14.11 Small / Big escalation
□ 14.12 Ollama vs llama.cpp evaluation
□ 14.13 speculative decoding
□ 14.14 final benchmark
```

After Phase 14:

```text
Phase 15 — Leaf Foliage
```

---

# 15. Exact Starting Point for Phase 14.10

Phase 14.10 should implement the planned reasoning/depth modes:

```text
Quick
Normal
Deep
```

Previously intended behavior:

- **Quick** — low reasoning / low overhead for routine work
- **Normal** — default balanced mode
- **Deep** — stronger reasoning for architecture, debugging, difficult planning, and complex analysis

The user previously wanted automatic temporary switching based on prompt/task complexity.

Important constraints for 14.10:

1. Do not couple the mode concept directly to one model/runtime.
2. Forest-level mode should be canonical/runtime-neutral.
3. Runtime adapters translate canonical mode into runtime-specific controls.
4. Deep mode must not silently become Sticky unless policy allows it.
5. Temporary escalation must not permanently alter Tree configuration.
6. Runtime recovery must reuse the already-decided mode for the in-flight turn.
7. New meaningful input may cause a new mode decision.
8. Execution/retry must not reclassify prompt complexity.
9. Quick/Normal/Deep is distinct from later Small/Big model escalation.
10. Do not combine 14.10 and 14.11 prematurely.

Likely first step:

> **14.10A — inspect current reasoning controls in Hermes/runtime adapters and define a canonical Forest reasoning-mode model before changing behavior.**

---

# 16. Current Resume Instruction

> **Phase 14.9 is complete. Resume Project Forest at Phase 14.10A: inspect existing runtime reasoning controls and define a runtime-neutral Quick / Normal / Deep decision model without yet implementing Small / Big model escalation.**

---

# 17. Final Certification

```text
PHASE 14.9 SOURCE-CONTEXT TARGETING: COMPLETE
```

Certification basis:

```text
Architecture boundaries verified: YES
Source correctness verified: YES
Race-safe snapshot behavior verified: YES
Shared structural caching verified: YES
Turn-local targeting verified: YES
Ambiguity handling verified: YES
Bounded expansion verified: YES
Source leakage prevention verified: YES
Packet budgets verified: YES
Rendering safety verified: YES
Path privacy verified: YES
Forest-level composition verified: YES
No-source compatibility verified: YES
Runtime stale-recovery identity verified: YES
Zero recovery recomputation verified: YES
Concurrency behavior verified: YES
Determinism verified: YES
Representative performance benchmark verified: YES
Persistent Forest state mutation during tests: NO
Hermes contacted during closeout tests: NO
Ollama contacted during closeout tests: NO
Additional optimization required before proceeding: NO
```

> **Phase 14.9 is closed. Proceed to 14.10 Quick / Normal / Deep.**
