# The Forest — Portable Tree Runtime + High-Speed Workshop Architecture

**Status:** Adopted implementation direction  
**Primary test Tree:** Bristlecone Pine  
**Current runtime:** Hermes + Ollama  
**Design goal:** Make Trees lighter, faster, portable, reusable, and independent of any single model, inference runtime, or agent interface.

---

## 1. Core Decision

The Forest should **not** store a Tree primarily inside Hermes, Ollama, llama.cpp, or any other runtime.

Instead:

> **The Tree is the portable Forest-owned configuration, knowledge, Skills, Workshops, permissions, identity, and operational learning.**

Hermes, Ollama, llama.cpp, and future runtimes are execution layers underneath the Tree.

```text
════════════ TREE PORTABILITY BOUNDARY ════════════

TREE / FOREST-OWNED
- Identity
- Workshops
- Skills
- Leaves / knowledge references
- Permissions
- Routing rules
- Operational learning
- Portable state

---------------------------------------------------

RUNTIME ADAPTER
- Hermes mappings
- llama.cpp mappings
- future framework mappings

---------------------------------------------------

EXECUTION RUNTIME
- Model inference
- Tool execution
- OS integration
- Ollama / llama.cpp / other backend
```

Everything above the boundary should survive a runtime change. Everything below it should be replaceable.

---

## 2. Main Architecture

Use a **hybrid design**:

```text
FOREST SOURCE FILES
portable / readable / editable
        │
        │ load + resolve
        ▼
PREPARED RUNTIME REGISTRY
small, fast, held in RAM
        │
        │ select current profile
        ▼
ACTIVE TREE STATE
Workshop + reasoning + model form + sticky Skills
        │
        │ inject only what is needed
        ▼
MODEL CONTEXT
smallest useful active context
```

This avoids both bad extremes:

- **Files only:** portable, but wastes time repeatedly parsing/resolving.
- **Runtime only:** fast, but tightly coupled to Hermes, Ollama, or another framework.

The hybrid design gives us portability, readability, low active context, fast lookup, reusable prepared profiles, and replaceable runtimes/models.

---

## 3. Cold / Warm / Hot Storage

### Cold — Persistent storage

Contains the full portable Tree:

```text
The-Forest/
└── trees/
    └── bristlecone/
        ├── identity/
        ├── workshops/
        ├── skills/
        ├── permissions/
        ├── routing/
        ├── learning/
        ├── leaves/
        └── state/
```

Cold storage may contain all Workshops, all Skills, identity, permissions, routing history, operational learning, Leaf references, configuration, and runtime-independent state.

### Warm — Runtime registry/cache

Loaded once while Bristlecone is awake:

```text
Bristlecone Workshop Registry

ResearchProfile
DesignProfile
CodeDebugProfile
ModelProfile
```

Warm storage may contain Workshop names, capability IDs, Skill manifests, short Skill descriptions, permissions, routing hints, parsed config, and cached Skill contents.

The model does **not** need to see everything in Warm storage.

### Hot — Active model context

Only what the current task requires:

```text
CURRENT TASK

Workshop:
Code / Debug

Core:
- File
- Terminal

Active Skill:
- Debugging

Relevant Leaves:
- current service configuration
- recent error log
- current task state

Reasoning:
Normal

Model Form:
Small
```

> **Keep Cold large, Warm small, and Hot tiny.**

This is the runtime expression of the **Minimum Useful Canopy Principle**.

---

## 4. Prepared Workshops

Workshops are prepared profiles, not boxes rebuilt every turn.

Each Workshop has:

- **CORE** — immediately available.
- **READY / DORMANT** — owned by the Tree, not injected.
- **ACTIVE** — pulled in for the current task.
- **STICKY** — retained while related work continues.

---

## 5. Bristlecone's Four Workshops

### Research

**Core**
- Web Search & Extract

**Ready / Dormant**
- file access
- memory/context access
- Leaf access
- session retrieval
- citation/grounding behavior

Only include capabilities that are actually implemented and verified.

### Design

**Core**
- memory / relevant context
- clarification behavior

Design covers architecture, planning, system structure, tradeoffs, concepts, and Forest design.

Clarification may be behavior rather than a literal tool.

### Code / Debug

**Core**
- File
- Terminal

**Ready / Dormant**
- code execution
- Debugging Skill
- Testing Skills
- clarification
- specialized development Skills

System troubleshooting is absorbed into Code / Debug instead of becoming a separate Workshop.

### Model

**Core**
- File
- Terminal

**Ready / Dormant**
- evaluation
- benchmarking
- quantization
- runtime inspection
- training utilities
- model comparison
- specialized model-development Skills

---

## 6. Three Independent Axes

### Axis 1 — Reasoning Mode

```text
Light
Normal
Deep
```

Controls reasoning effort only.

### Axis 2 — Workshop

```text
Research
Design
Code / Debug
Model
```

Controls capability boundary only.

### Axis 3 — Model Form

```text
Small / Windowed
Big / Fullscreen
```

Controls the underlying model only.

Valid combinations include:

```text
Light + Code/Debug + Small
Deep + Code/Debug + Small
Normal + Code/Debug + Big
Deep + Code/Debug + Big
```

Tree identity remains above the replaceable model.

---

## 7. Tree Identity Must Not Equal Model

Bristlecone is not Qwen, an Ollama model, or any single backend.

Conceptually:

```text
BRISTLECONE
    │
    ├── Small Qwen
    ├── future Big model
    ├── Llama-family model
    ├── Mistral-family model
    └── future model
```

Changing models may require re-benchmarking and runtime tuning, but should not require rebuilding Bristlecone's identity or Workshop architecture.

---

## 8. Runtime Independence

Current:

```text
Bristlecone
    ↓
Hermes
    ↓
Ollama
    ↓
Small model
```

Possible future:

```text
Bristlecone
    ↓
Forest adapter
    ↓
llama.cpp
```

or another framework/runtime.

The adapter maps generic Forest capabilities to runtime-specific implementations.

Example:

```text
FOREST CAPABILITY
terminal
```

may map to:

```text
Hermes:
terminal toolset
```

while another runtime might expose:

```text
shell.execute
```

The Workshop can still say:

```yaml
core:
  - file
  - terminal
```

Only the adapter changes.

---

## 9. Authoritative vs Disposable Data

### Authoritative / Portable

```text
identity.md
workshops/*.yaml
skills/*.md
permissions.yaml
routing-history.jsonl
Leaves / links / metadata
```

These define the Tree and should be backed up/exportable.

### Disposable / Rebuildable

```text
RAM Workshop registry
parsed Skill cache
SQLite indexes
prepared runtime objects
prompt cache
KV cache
Hermes mappings
Ollama-specific configuration
llama.cpp-specific configuration
```

If a cache disappears, the Tree should rebuild it rather than lose identity.

---

## 10. Workshop File Example

```yaml
id: code-debug
name: Code / Debug

core:
  - file
  - terminal

ready:
  - code-execution
  - debugging
  - testing
  - clarify
  - special
```

This is the portable source.

At startup, the runtime resolves those names into actual available capabilities.

---

## 11. Prepared Runtime Representation

Do **not** repeatedly do this:

```text
open YAML
parse YAML
find tool
map tool
assemble tool schema
build Workshop
```

Instead:

```text
START TREE
    ↓
read Workshop files
    ↓
resolve runtime capabilities
    ↓
prepare four Workshop profiles
    ↓
hold lightweight registry in RAM
```

Then selecting a Workshop is closer to:

```text
active_workshop = CodeDebugProfile
```

---

## 12. Skill Architecture

A Tree may own many Skills without loading them all into model context.

Warm manifest example:

```text
Skill:
debugging

Workshop:
Code / Debug

Description:
Structured diagnosis and iterative fault isolation

State:
Dormant

Location:
skills/debugging/
```

Activation flow:

```text
Dormant
   ↓
load full Skill
   ↓
cache parsed Skill in RAM
   ↓
inject into model context
   ↓
Active
   ↓
Sticky if task continues
   ↓
Dormant when task ends
```

Important:

```text
Cached in RAM
      ≠
Visible to model
```

A Skill can remain cached without consuming prompt/context tokens.

---

## 13. Sticky Workshop and Skill Behavior

Do not reroute every user message.

```text
User starts debugging service
        ↓
Code / Debug selected
        ↓
debugging Skill activated
        ↓
several related messages occur
        ↓
Code / Debug remains active
debugging remains sticky
```

Drop Workshop/Skill after a meaningful boundary such as:

- clear task change
- Workshop change
- explicit completion
- prolonged irrelevance
- context pressure
- inactivity policy
- user request

---

## 14. Skill Finder / Tool Shed

Minimal Workshops must not become capability cages.

Fallback ladder:

```text
LEVEL 0
Current Workshop CORE

LEVEL 1
Current Workshop READY inventory

LEVEL 2
Search all Tree-owned Skill/tool manifests

LEVEL 3
Compare other Workshop manifests

LEVEL 4
Open Workbench
temporarily expose a broader set of the Tree's own capabilities
```

This is a meta/fallback layer, **not** a fifth normal Workshop.

---

## 15. Open Workbench

Open Workbench is a last-resort capability state.

It should not immediately load everything the Tree owns.

Its purpose is:

> Escape a capability dead end without permanently returning to bloated always-on context.

---

## 16. Operational Learning

Distinguish:

### Knowledge Learning
What the Tree learns about projects, users, systems, concepts, world information, and Leaves.

### Operational Learning
What the Tree learns about how to use itself.

Example:

```text
task pattern
→ initial Workshop
→ successful Workshop
→ Skills activated
→ unnecessary capabilities
→ fallback path
→ outcome
```

Example:

```text
"service dies immediately after startup"
initial: Design
fallback: Code / Debug
Skill: debugging
outcome: resolved
```

Next time the router may start closer to:

```text
Code / Debug + debugging
```

This improves efficiency without retraining model weights.

---

## 17. Operational Learning Storage

Portable history:

```text
routing-history.jsonl
```

Derived fast index:

```text
routing-history.jsonl
        ↓
SQLite / lightweight local index
        ↓
runtime lookup
```

The index is disposable and rebuildable.

The portable history is authoritative.

---

## 18. Stable Prompt Prefixes

Prepared Workshops should keep stable prompt sections stable:

```text
STABLE PREFIX

Bristlecone identity
Forest core rules
current Workshop rules
current CORE tool schemas
small capability manifest

----------------------------

DYNAMIC SUFFIX

active Skills
Hot Leaves
active task state
new user message
```

Runtimes that support prompt/KV caching may reuse previously processed stable prefixes.

This may become especially valuable during a future llama.cpp test.

---

## 19. Model Warmth and Workshop Warmth Are Separate

### Model Warm
Weights remain loaded in memory.

### Workshop Warm
Workshop profiles and Skill manifests remain prepared in RAM.

Ideal state:

```text
Model: Warm
Workshop registry: Warm
Current Hot context: Tiny
```

---

## 20. Current Bristlecone Benchmark Evidence

### Earlier Hermes tool benchmarks

```text
file + terminal
≈ 41 seconds

file + terminal + todo
= 1:49.64

file + terminal + skills
= 2:42.40

file + terminal + skills + todo
= 2:49.16
```

Observation:

> Larger active tool/schema sets produced dramatically higher latency.

This was a primary motivation for Workshops.

### Minimal Workshop cold tests

Order:

1. Design
2. Code / Debug
3. Research
4. Model

Observed:

```text
Design
first output ≈ 2:52

Code / Debug
first output ≈ 3:12
finished ≈ 5:42

Research
first output ≈ 2:44

Model
first output ≈ 3:04
finished ≈ 11:49
```

Cold first-output average:

```text
≈ 2:58
```

The four Workshops were tightly grouped.

This suggests a significant part of the remaining ~3 minute delay may be outside simple Workshop size, such as cold model loading, initialization, base prompt evaluation, or other common startup work. This remains a hypothesis to test.

### Warm follow-up test

Observed:

```text
first output:
30.58 sec

next stage:
43.72 sec

final stage:
2.23 sec

total:
1:16.54
```

Observation:

> Warm first output fell from roughly three minutes cold to roughly thirty seconds.

This strongly suggests model/runtime warmth is a major optimization target separate from Workshop architecture.

---

## 21. Two Separate Performance Problems

### Startup latency

```text
cold model
    ↓
load / initialize
    ↓
base context processing
    ↓
Workshop
    ↓
first output
```

Current cold first-output range:

```text
roughly 2:44 – 3:12
```

### Execution latency

After first output, Workshops may differ greatly.

```text
Code / Debug:
3:12 → 5:42
≈ 2:30 additional work

Model:
3:04 → 11:49
≈ 8:45 additional work
```

The Model Workshop needs separate investigation later.

Possible causes to measure include terminal calls, command latency, model-inspection behavior, unnecessary loops, excessive reasoning, or tool waits.

---

## 22. Why This Should Be Faster

```text
Prepared Workshops
→ no repeated Workshop reconstruction

RAM registry
→ avoid unnecessary file parsing

Minimal CORE
→ fewer tool schemas

Dormant Skills
→ no unused Skill instructions in prompt

Sticky Skills
→ avoid repeated activation

Hot Leaves only
→ less knowledge/context processing

Stable prefixes
→ caching opportunities

Operational routing learning
→ fewer routing mistakes

Warm model
→ less cold-start delay

Derived indexes
→ faster retrieval without sacrificing portable storage
```

---

## 23. Why This Is More Portable

To move Bristlecone:

```text
copy authoritative Tree files
        ↓
install compatible Forest runtime / adapter
        ↓
resolve capabilities
        ↓
rebuild indexes and caches
        ↓
Tree resumes operation
```

Do not require copying runtime caches, RAM, prompt/KV caches, or other rebuildable implementation details.

---

## 24. Potted Plant Compatibility

Example:

```text
bristlecone-debug-pot/
├── identity.md
├── workshop.yaml
├── permissions.yaml
├── skills/
│   ├── debugging.md
│   └── testing.md
└── selected-leaves/
```

A Pot does not need to clone an entire VM.

It can be a bounded portable expression of a Tree with selected identity, Workshop, Skills, Leaves, permissions, and runtime preferences.

Conceptually:

```text
Tree
  ↓
Workshop
  ↓
Pot
```

---

## 25. Forest-Wide Principle

Workshops should eventually be available to all Trees.

Examples:

```text
Maple micro-workshop
- move files

Cherry everyday workshop
- communication
- planning

Bristlecone code workshop
- file
- terminal

Cedar security workshop
- security-specific tools
```

A Workshop describes a **capability boundary**, not a fixed number of tools.

---

## 26. Minimum Useful Canopy Principle

> **A Tree should expose only the tools, Skills, knowledge, permissions, and context required for its current task, with additional capabilities activated only when needed.**

Technical shorthand:

> **Minimum Capability Principle**

---

## 27. Shared Infrastructure vs Specialized Skills

Shared Forest primitives may include:

- Workshop runtime
- permissions
- Leaf API
- context transport
- memory transport
- Tree-to-Tree communication
- handoff packets
- basic file primitives

Specialized Skills stay with the role owner.

```text
Cherry
general assistant / communication / planning

Maple
organization / files / media / workspace

Bristlecone
coding / debugging / architecture / model development

Cedar
security / integrity / monitoring / recovery
```

---

## 28. Implementation Order

### Phase 1 — Freeze Current Baseline
- Keep current Small Bristlecone.
- Keep Hermes.
- Keep Ollama.
- Keep four minimal Workshop definitions.
- Preserve benchmark data.
- Do not add unnecessary tools yet.

### Phase 2 — Create Portable Tree Structure

Proposed starting point:

```text
~/The-Forest/
└── trees/
    └── bristlecone/
        ├── identity/
        ├── workshops/
        ├── skills/
        ├── state/
        ├── routing/
        ├── learning/
        └── adapters/
```

Exact location should be chosen after inspecting existing Bristlecone/Forest files so we do not create a second conflicting source of truth.

### Phase 3 — Create Four Workshop Profiles

```text
research
design
code-debug
model
```

Initially match the already-tested minimal states.

### Phase 4 — Add Runtime Adapter

Create a Hermes adapter that translates Forest capability names into actual Hermes capabilities.

### Phase 5 — Prepared Runtime Registry

At startup:

1. read Workshop files
2. validate them
3. resolve Hermes mappings
4. construct Prepared Workshop Profiles
5. hold the lightweight registry in RAM

### Phase 6 — Add Active State

Track:

```text
active Workshop
reasoning mode
model form
active Skills
sticky Skills
current task state
```

### Phase 7 — Add Skill Manifests

Possible fields:

```text
id
name
short description
owner Tree
primary Workshop
activation location
permissions
optional usage statistics
```

### Phase 8 — Sticky Skill Activation

```text
Dormant
→ Active
→ Sticky
→ Dormant
```

### Phase 9 — Skill Finder / Tool Shed

Implement the fallback ladder.

### Phase 10 — Operational Learning

Record routing outcomes. Collect evidence before promoting capabilities into Workshop CORE.

### Phase 11 — Retrieval / Leaf Integration

Later integrate:

```text
Cold Leaves
Warm relevant project context
Hot current-task Leaves
```

### Phase 12 — Final Ollama Optimization

After Workshop architecture is stable:
- optimize model warm behavior
- inspect cold-start latency
- inspect prompt processing
- inspect Model Workshop execution
- benchmark final Small Bristlecone
- freeze Ollama baseline

### Phase 13 — llama.cpp A/B

Compare as fairly as possible:

```text
same Bristlecone
same model if possible
same Workshops
same reasoning modes
same prompts
same tests
same Qubes resources

Ollama
vs
llama.cpp
```

Measure:
- cold first output
- warm first output
- total completion
- prompt processing
- tool behavior
- RAM
- CPU
- stability
- quality

### Phase 14 — Big / Fullscreen Bristlecone

Only after Small Bristlecone is well understood.

Big is escalation/review, not a replacement for Small.

---

## 29. Rejected / Reframed Ideas

**Rejected:** Deep mode turns on all tools.  
Reason: reasoning effort and capability exposure must remain independent.

**Rejected:** Workshop controls model strength.  
Reason: Small/Big is its own Model Form axis.

**Rejected:** Big replaces Small Bristlecone.  
Reason: Small remains useful for lightweight work.

**Rejected:** All capabilities remain loaded.  
Reason: violates Minimum Useful Canopy.

**Rejected:** Workshop profiles rebuilt from disk every prompt.  
Reason: source files should feed a prepared runtime registry.

**Rejected:** Hermes configuration is the authoritative Tree.  
Reason: couples The Forest to Hermes.

**Rejected:** Ollama configuration is the authoritative Tree.  
Reason: couples the Tree to one inference backend.

**Reframed:** Debug Workshop → Code / Debug Workshop + Debugging Skill.

**Reframed:** System Workshop → Design or Code / Debug depending on task.

**Reframed:** Retrieval Workshop → shared Forest retrieval/Leaf infrastructure rather than necessarily a user-facing Workshop.

---

## 30. Definition of Success

A future test should be able to do this:

```text
1. Copy Bristlecone's authoritative Tree files.
2. Remove Hermes.
3. Remove Ollama.
4. Install a different supported runtime.
5. Install/write a new Forest adapter.
6. Rebuild runtime caches.
7. Bristlecone still has:
   - identity
   - Workshops
   - Skills
   - permissions
   - Leaves
   - operational learning
8. Rebenchmark runtime-specific performance.
```

The Tree survives. Only runtime-specific tuning needs to be rebuilt.

---

## 31. Current Working Principle

The Forest is **not** being built as an elaborate Hermes/Ollama configuration.

Hermes and Ollama are the **first execution environment** for a portable Forest Tree architecture.

> **A Tree can be large in capability, tiny in active context, fast while running, readable on disk, portable between systems, and independent of its current model and runtime.**

---

## 32. Immediate Next Step

Begin implementation using **Small Bristlecone + Hermes + Ollama** as the first adapter/runtime target.

Before creating anything permanent:

```text
1. Inspect the existing Bristlecone / Hermes / Forest directories.
2. Choose the canonical Tree directory.
3. Create or verify bristlecone/workshops/.
4. Create the four minimal Workshop profiles.
5. Map generic capability names to actual Hermes capabilities.
6. Test that the portable definitions reproduce current benchmark behavior.
7. Then add prepared runtime caching and automatic routing.
```

**Pine is fine.**
