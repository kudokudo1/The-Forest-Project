# Project Forest / Bristlecone Pine — Chat Transfer Handoff
**Prepared:** 2026-08-09  
**Purpose:** Resume the current Project Forest implementation thread in a fresh chat with minimal re-investigation.

---

## Immediate Resume Point

We are implementing **Phase 14.9 — Source-Context Targeting**.

Current roadmap state:

- ✅ 14.7 Layered Hot Context — COMPLETE
- ✅ 14.8 Runtime Cache / Prefix Integration — COMPLETE
- ✅ 14.9B Shared/Object Source Context foundation — COMPLETE
- ✅ 14.9C Turn-local targeting → bounded packets → deterministic rendering — COMPLETE
- 🟡 14.9D Forest-level turn composition / runtime integration — IN PROGRESS

### Exact current step

This file now exists:

```text
/home/user/The-Forest/bristlecone/turn_composition.py
```

It was installed with a fail-closed sequence:

```text
mktemp
→ write temporary Python module
→ python -m py_compile temporary file
→ mv temporary file to turn_composition.py
```

Terminal confirmed:

```text
CREATED: turn_composition.py
```

Therefore:

- syntax validation passed
- the file was installed
- **behavioral verification has not yet been completed**

### NEXT ACTION

Run the **14.9D.1B behavioral verification** for the already-installed `turn_composition.py`.

Do **not** reinstall it blindly.

If the verification passes, mark:

```text
PHASE 14.9D.1B FOREST-LEVEL TURN INSTRUCTION COMPOSITION: WRITTEN + PASS
```

Then proceed to:

```text
14.9D.2 — stale-session/recovery exact-instruction-identity test
```

---

## User / Workflow Preferences

The user manually executes terminal commands in Cherry-AI and pastes results back.

Preferred engineering workflow:

1. One meaningful change at a time.
2. Verify before moving on.
3. No blind reruns.
4. Inspect failures before editing.
5. Existing files require timestamped backups before mutation.
6. New files may be created fail-closed.
7. Explain terminal commands practically and beginner-friendly when useful.
8. Prefer local-first, free/open-source, self-hostable architecture.
9. Do not claim completion until terminal behavior verifies it.

Important environment fact:

```text
/home/user/The-Forest
```

is **not a Git repository**.

Therefore:

> Back up existing source files before modifying them.

---

## Project Forest Doctrine

North Star:

> **The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**

Core metaphors:

- Tree = AI identity / role / agent
- Clone = independently operating extension of a Tree
- Colony = base Tree + its Clones
- Workshop = tool / capability / Skill boundary
- Leaves = durable human-readable knowledge
- Roots = provenance / dependencies / relationships
- Soil = least-privilege execution environment
- Spirit = deterministic permission/action authority
- Water = external information
- Sunlight = user-originated information
- Syrup = inferred/distilled personalization
- Mycelium = permission-aware cross-Tree continuity
- Cedar Oil = encryption/data security
- Sap = sensitive-data handling classification
- Tar Sap = protected data that should not be autonomously altered
- Bud / Flower / Fruit = idea/project lifecycle
- Pruning = deliberate user/Spirit-authorized shaping

Key doctrines:

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

> **A Tree is not its model.**

> **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**

Core Trees:

- Cherry — primary assistant
- Maple — organizer / developer / semantic cartographer / personal-data steward
- Cedar — security Tree
- Bristlecone Pine — Treewright development Tree

Bristlecone health phrase:

> **Pine is fine.**

---

## Runtime / Qubes Context

Environment:

- Qubes OS
- XFCE + i3
- kitty
- zsh + powerlevel10k

Relevant qubes:

- Cherry-AI
- Maple
- Seed-AI
- dom0

Preferred runtime stack:

```text
Project Forest
    ↓
Hermes
    ↓
Ollama
    ↓
model
```

Known runtime details:

- Hermes gateway: `127.0.0.1:8643`
- Ollama: `11434`
- Hermes service: `hermes-bristlecone.service`
- Bristlecone model previously recorded: `bristlecone-qwen35:4b-64k`
- Newelle is optional/paused; Hermes is the primary interface.

---

## Clone / Colony Architecture

Canonical definitions:

> **A Clone is an extension of a Tree, not another Tree.**

> **A Colony is a Tree and all of its Clones.**

> **One Tree. More than one place.**

Clone lifetimes:

- ephemeral
- persistent
- project

Persistent Clone = durable lightweight state, not permanent compute.

Shared Tree/Colony durable state includes:

- identity
- personality/purpose
- Leaves
- Roots
- Operational Learning
- user corrections
- Syrup access
- Mycelium relationships
- long-term history
- stable preferences
- approved Skills
- Tree configuration

Clone-local active state includes:

- current Task/session/conversation
- Hot Context
- active Workshop
- Ready rack
- temporary Skills/files/capabilities
- assumptions
- runtime session/model state
- Soil/environment
- scratch state

Important invariants:

> **Clones share durable Tree state, not unrestricted live context.**

> **Trees own capability. Clones carry only capability they need.**

> **Shared capability, separate activation.**

> **Clone count must not scale infrastructure count.**

> **Retain cheaply. Activate selectively. Share aggressively.**

> **Resource cost should scale primarily with active work, not retained Clone count.**

---

## Learning / User Context Architecture

Operational Learning contains:

- mistakes
- successes
- procedures
- environment
- observations

User Context contains:

- Preferences
- Constraints
- Corrections
- Current Context

Syrup = inferred/distilled personalization.

Authority order:

```text
current instruction
>
correction
>
explicit constraint/preference
>
strong learned pattern
>
Syrup
>
weak inference
```

> **What the user explicitly says outranks what Forest inferred.**

Context tiers:

- COLD / authoritative = durable records
- WARM / derived = indexes/trigger maps
- HOT = relevant records only

> **Cold stores truth. Warm decides relevance. Hot contains only relevant.**

Context routing rule:

> **Conversation changes invalidate context routing; execution steps do not.**

Independent generations:

- `user_context_generation`
- `operational_learning_generation`

---

# Phase 14.7 — COMPLETE

Important files:

```text
learning/hot_context.py
learning/foundation.py
learning/snapshot_provider.py
learning/turn_retrieval.py
learning/turn_instruction.py
```

### Hot Context assembler

`LayeredHotContextAssembler.assemble()` is keyword-only.

Semantic order:

1. Corrections
2. Constraints
3. Preferences
4. Current Context
5. Operational Learning

Assembler is stateless, immutable, Tree-neutral, Clone-neutral.

### TurnInstructionComposer

`learning/turn_instruction.py`

Verified:

- one retrieval per compose
- one assembly per compose
- historical instruction stability
- empty-turn policy behavior
- policy invalidation
- fail-closed character budget

Key invariant:

> **One meaningful turn retrieves once, assembles once; runtime retries reuse the exact instruction snapshot.**

### Runtime recovery already proven in 14.7E

`TaskSessionManager.send_runtime_turn()` was tested with a fake runtime adapter.

Verified:

- first runtime attempt uses original session
- stale session is detected at use
- replacement session is created
- recovery sends the **same `instructions` object** (`is`)
- recovery does not count as new meaningful input
- recovery is one-shot
- no Learning retrieval or Hot Context assembly happens during recovery
- concurrent turns do not leak instructions

---

# Phase 14.8 — COMPLETE

Principles:

> **Native inference caches are runtime-owned.**

> **Forest CacheCoordinator is for derived Forest data, not KV/prefix caches.**

> **A runtime session is an opaque continuity handle, not a Forest-owned cache object.**

Findings:

- Hermes exposes no explicit KV/prefix-cache API to Forest.
- existing session IDs are reused without speculative inspection
- stale validity is discovered only at runtime use
- stale recovery rotates the opaque runtime session binding
- no speculative `inference_reuse_capability()` API was added

---

# Phase 14.9 — Source Context

Ownership:

> **Source Context is a Forest subsystem, not a Learning subsystem and not a runtime-adapter feature.**

> **Source truth is shared. Source relevance is turn-local.**

> **Share parsed source/index, not turn relevance decision.**

Current pipeline:

```text
SourceIdentity
    ↓
SourceFingerprint
    ↓
SourceContentSnapshot
    ↓
SourceStructure
    ↓
SourceReferenceMatcher
    ↓
SourceTarget
    ↓
BoundedSourceTargetExpander
    ↓
SourcePacket
    ↓
RenderedSourcePacket
    ↓
Forest-level final turn composition
```

---

## 14.9B — Shared Objective Source Foundation COMPLETE

### B.1 Neutral models

Created:

```text
source_context/model.py
source_context/__init__.py
```

Models:

- `SourceIdentity`
- `SourceFingerprint`
- `SourceRegion`
- `SourceTarget`

### B.2 Local source observation

Created:

```text
source_context/observation.py
```

Fingerprint method:

```text
stat-size-mtime-v1
```

Persistent fingerprint components:

- `size`
- `mtime_ns`

No content read, no cache ownership, no runtime coupling.

### B.3 Immutable source snapshot

Created:

```text
source_context/snapshot.py
```

Safe read verifies transiently:

```text
st_dev
st_ino
st_size
st_mtime_ns
```

before/after read.

Persistent cheap fingerprint remains size + mtime.

Content-derived cache identity additionally uses:

```text
content_sha256
```

### B.4 Python structure

Created:

```text
source_context/structure.py
source_context/structure_provider.py
```

Python regions:

- `python:module`
- class
- function
- async function
- method
- async method

Structure cache:

- shared `CacheCoordinator`
- exact-snapshot key
- content SHA256 protected
- per-key single-flight
- old/new versions coexist
- 1/10/50 Clone callers → one AST parse for identical snapshot

### B.4 Markdown structure

Created:

```text
source_context/markdown_structure.py
source_context/markdown_structure_provider.py
```

Supports:

- ATX headings
- Setext headings
- fenced-code exclusion
- heading hierarchy
- duplicate headings
- whole source `markdown:document`

Same exact-snapshot cache/single-flight architecture.

---

## 14.9C — Turn-Local Targeting and Packets COMPLETE

### C.1 Deterministic explicit targeting

Created:

```text
source_context/targeting.py
```

Core:

- `DeterministicSourceTargeter`
- exact region ID
- exact unique label
- duplicate labels fail closed
- whole-source requires explicit selection
- no fuzzy / semantic / model fallback

Boundary:

```text
SHARED:
SourceSnapshot
SourceStructure
SourceRegion

TURN-LOCAL:
SourceTarget
```

### C.2 Deterministic source-reference matching

Created:

```text
source_context/reference_matcher.py
```

Canonical signal behavior measured from existing Forest Learning matchers:

- trim surrounding whitespace
- preserve case
- deduplicate first-seen
- preserve order
- reject empty / whitespace-only / non-string

Matcher resolution order:

1. exact `region_id`
2. exact unique label
3. explicit ambiguity
4. unmatched

Region ID takes precedence over label.

> **Source reference matching consumes canonical turn signals; it does not parse raw prompts.**

### C.3 Bounded ancestor expansion

Created:

```text
source_context/target_expansion.py
```

Rules:

- target first
- nearest ancestors only
- explicit parent-hop budget
- no siblings
- no children
- whole-source ancestor requires explicit permission
- malformed/cyclic hierarchy fails closed

Important:

> **Being structurally related does not automatically make all related source relevant.**

### C.4 Bounded SourcePacket assembly

Created:

```text
source_context/packet.py
```

Core:

- `SourcePacket`
- `SourcePacketFragment`
- `SourcePacketAssembler`
- fail-closed packet budgets

Critical rule:

> **Targets contribute source text. Ancestors contribute structural breadcrumbs unless independently targeted.**

This prevents ancestor class/heading spans from importing sibling source.

Features:

- exact selected source text
- overlapping target deduplication
- separate non-overlapping fragments
- breadcrumb IDs/labels
- hard character budget
- hard line budget
- no silent truncation

Important:

> **A packet records what source was selected and the bounds under which that selection was authorized.**

Therefore packets with identical source but different budget provenance are intentionally unequal.

### C.5 Deterministic rendering

Created:

```text
source_context/rendering.py
```

Core:

- `RenderedSourcePacket`
- `DeterministicSourcePacketRenderer`

Features:

- stable provenance
- target IDs
- ancestor breadcrumbs
- line ranges
- selected text preserved
- safe dynamic code-fence length
- local locator/path hidden by default
- locator disclosure opt-in only
- hard rendered-character budget
- no runtime injection

Important boundary:

> **Source provenance does not automatically authorize disclosure of an absolute filesystem path.**

Terminal completion:

```text
PHASE 14.9C.5 DETERMINISTIC SOURCE PACKET RENDERING: WRITTEN + PASS
```

---

# Phase 14.9D — Current Integration Work

## D.0 Preflight

Read-only inspection established:

```text
learning/turn_instruction.py source_context import: ABSENT
runtime/task_session.py source_context import: ABSENT
```

`TaskSessionManager.send_runtime_turn`:

```python
(self, message, state=None, instructions=None, persist=False)
```

Runtime uses:

```python
sender(
    requested_session_id,
    message,
    working,
    instructions=instructions,
)
```

and stale recovery reuses the same local `instructions` variable.

Conclusion:

- Source Context should **not** be put inside Learning.
- `TaskSessionManager` should **not** assemble Source Context.
- Forest needs a composition layer above both subsystem outputs.

Preferred architecture:

```text
Learning instructions ───────┐
                             │
RenderedSourcePacket(s) ─────┼─► ForestTurnInstructionComposer
                             │
                             ▼
                   one frozen final string
                             │
                             ▼
                TaskSessionManager
                             │
                             ▼
                          runtime
```

## D.1A Caller ownership preflight

Terminal result:

```text
send_runtime_turn CALL SITES
NONE
```

Therefore:

> **There is no production caller above `send_runtime_turn()` yet.**

`send_runtime_turn()` is currently an infrastructure boundary, not a wired application workflow.

This allows Forest-level composition to be introduced without changing runtime code.

---

# Phase 14.9D.1B — CURRENT EXACT STATE

Created:

```text
turn_composition.py
```

### Important failure history

The first long installer was corrupted during paste and failed with:

```text
SyntaxError: unmatched ')'
```

Because the heredoc failed to parse, nothing executed.

A shorter installer was then used:

```text
mktemp
→ write module
→ python -m py_compile
→ mv into place
```

Terminal confirmed:

```text
CREATED: turn_composition.py
```

So the module exists and syntax-checks.

### Intended responsibilities

`turn_composition.py` defines:

- `ForestTurnCompositionError`
- `ForestTurnCompositionBudgetError`
- `ForestTurnInstructionComposition`
- `ForestTurnInstructionComposer`

### Backwards compatibility

If no Source Context exists:

```text
Learning instructions
      ↓
Forest composer
      ↓
EXACT SAME STRING OBJECT
```

Desired verification:

```python
composition.instructions is learning_instructions
```

Meaning Phase 14.9 has zero effect on ordinary turns.

### With Source Context

```text
Learning instructions
      +
RenderedSourcePacket(s)
      ↓
ForestTurnInstructionComposer
      ↓
one immutable final instruction string
```

Source attachment includes an explicit authority statement that Source Context is **reference data** and cannot override:

- user current instruction
- Forest policy
- Spirit permissions
- higher-priority instructions

Other behavior:

- exact duplicate rendered packets collapse first-seen
- distinct packets preserve first-seen order
- hard final-character budget
- fail closed
- no silent truncation
- no source reading
- no targeting
- no packet assembly
- no Learning retrieval
- no cache ownership
- no runtime calls

Forest composer may import `source_context`, but must not import:

```text
learning
runtime
cache
```

---

# NEXT STEP — 14.9D.1B Verification

Run the already-prepared short behavioral verification against the installed `turn_composition.py`.

It should prove:

1. no-source exact Learning passthrough
2. exact object identity on no-source path
3. empty composition stays `""`
4. Learning + Source Context combine into one final snapshot
5. Source Context authority notice exists
6. unselected sibling source cannot reappear
7. hidden local locator stays hidden
8. duplicate rendered packets collapse
9. exact final budget succeeds
10. budget overflow fails closed
11. final composition deterministic/frozen/hashable
12. inspection does not leak source/instruction contents
13. no Learning/runtime/cache imports
14. no runtime/model calls

Expected final result:

```text
PHASE 14.9D.1B FOREST-LEVEL TURN INSTRUCTION COMPOSITION: WRITTEN + PASS
```

If the verification fails:

> **Inspect the exact failure before modifying `turn_composition.py`. Do not reinstall blindly.**

---

# After D.1B — 14.9D.2

Use the real inherited:

```text
TaskSessionManager.send_runtime_turn()
```

with:

- the new Forest final composition
- a fake runtime adapter
- no real Hermes
- no real Ollama

Goal:

```text
compose once
   ↓
final instructions object I
   ↓
send runtime session S1 with I
   ↓
stale
   ↓
create S2
   ↓
recovery sends SAME object I
```

Must prove:

```python
first_instructions is recovery_instructions
```

During recovery these operations must remain **zero**:

```text
source reads
source observation
structure building
reference matching
target expansion
packet assembly
packet rendering
Forest final composition
Learning retrieval
Hot Context assembly
```

Key invariant:

> **Runtime recovery is execution, not conversational input.**

> **One meaningful turn creates one frozen final instruction snapshot; recovery/retry reuses that exact snapshot.**

If D.2 passes, Source Context recovery integration can close without modifying `TaskSessionManager`.

---

# Relevant Files Added in 14.9

```text
source_context/model.py
source_context/__init__.py
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

Important existing files:

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

Known backup:

```text
backups/phase14_7D2B_20260809T235800Z/learning/turn_instruction.py
```

---

# Recent Test-Harness Mistakes — Do Not Re-Diagnose as Product Bugs

### C.2 false-positive static check

A test rejected the word `similarity` appearing in a docstring that explicitly said similarity matching was **not** used.

Rule learned:

> **Safety validation should inspect executable structure when practical; comments/docstrings are not runtime coupling.**

### C.4 equality mistake

A test incorrectly expected packets with the same source selection but different budget provenance to compare equal.

Correct behavior:

> **Same selected source + different authorization/budget provenance = different packet value.**

### C.4A paste mistake

A duplicated malformed summary line caused an `IndentationError`.

The heredoc never executed.

### D.1B first installer

Paste corruption caused:

```text
SyntaxError: unmatched ')'
```

The shorter fail-closed installer succeeded afterward.

---

# High-Priority Engineering Invariants

1. Runtime truth before Forest truth.
2. No blind reruns.
3. Back up existing source before mutation.
4. Caches are derived, never source truth.
5. Native inference caches are runtime-owned.
6. A runtime session is an opaque continuity handle.
7. Clones share durable Tree state, not unrestricted live context.
8. Capability is shared; activation is local.
9. Resource cost should scale with active work, not retained Clone count.
10. Conversation changes route; execution steps do not.
11. Runtime retry/recovery reuses already-assembled instructions.
12. Runtime recovery is execution, not new conversational input.
13. Source truth is shared; source relevance is turn-local.
14. Source Context is Forest-owned, not Learning/runtime-owned.
15. Source observation is metadata-only.
16. SourceFingerprint = size + mtime_ns.
17. Content SHA256 protects content-derived cache identity.
18. Objective structure is Colony-shareable; SourceTarget is turn-local.
19. Exact source-version structure builds single-flight.
20. Explicit targeting fails closed on ambiguity/missing.
21. Source reference matching consumes canonical signals, not raw prompts.
22. Canonical source signals trim whitespace, preserve case, deduplicate first-seen, reject invalid entries.
23. Exact region ID takes precedence over label.
24. Target expansion is bounded ancestor-only.
25. Whole-source escalation requires explicit permission.
26. Ancestor structure does not imply ancestor body inclusion.
27. Explicit targets contribute source text; ancestors are breadcrumb-only unless explicitly targeted.
28. Overlapping target text is deduplicated.
29. Source packet budgets fail closed; no truncation.
30. Packet equality retains budget provenance.
31. Rendered source hides local paths by default.
32. Renderer delimiters must not be closable by selected source content.
33. Rendered-source budgets fail closed.
34. Source Context is reference data and cannot override higher authority.
35. Forest-level turn composition belongs neither to Learning nor Runtime.
36. No-source Forest composition must preserve existing Learning instructions unchanged.
37. Final Forest instructions are composed before runtime execution.
38. Runtime retry/recovery must receive the exact same final instruction object.
39. Source retrieval/targeting/packet/rendering/composition must not rerun merely because a runtime session became stale.

---

# Roadmap After Phase 14.9

Known upcoming roadmap:

```text
14.10 Quick / Normal / Deep
14.11 Small / Big escalation
14.12 Ollama vs llama.cpp
14.13 speculative decoding
14.14 final benchmark
Phase 15 Leaf Foliage
```

Do not skip unresolved 14.9 integration verification before advancing.

---

# One-Sentence Resume Instruction

> **Resume Project Forest at Phase 14.9D.1B: verify the already-installed `turn_composition.py`; if it passes, run 14.9D.2 proving stale-session recovery reuses the exact same final Forest instruction object with zero Source Context recomputation.**
