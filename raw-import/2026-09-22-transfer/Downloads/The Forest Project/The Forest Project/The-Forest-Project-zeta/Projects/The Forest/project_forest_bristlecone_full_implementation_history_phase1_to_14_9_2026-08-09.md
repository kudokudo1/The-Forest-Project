---
title: "Project Forest / Bristlecone Pine — Full Implementation History, Hermes Findings, and Retained Code"
aliases:
  - Bristlecone Full Engineering Archive
  - Project Forest Phase 1 to 14.9 History
  - Bristlecone Hermes Implementation History
tags:
  - project-forest
  - bristlecone-pine
  - hermes
  - ollama
  - qubes
  - runtime
  - workshops
  - task-sessions
  - seasonal-lifecycle
  - cache
  - learning
  - user-context
  - source-context
  - continuity
  - implementation-history
status: current-authoritative-history
prepared: 2026-08-09
current_phase: "14.10 — Quick / Normal / Deep"
last_completed: "14.9 — Source-Context Targeting"
---

# Project Forest / Bristlecone Pine — Full Implementation History
## Phase 1 / 2 Origins Through Phase 14.9

> [!important]
> This file is intentionally **larger and more historical than a normal checkpoint**.
> It records what we built, what we measured, what failed, what was rejected,
> how the architecture changed, what Hermes actually exposed, what runtime behavior
> we verified, and the important code/interfaces that survived those changes.

> [!warning]
> **Authority rule:** later verified checkpoints override older status labels.
> An old section saying a phase was pending is preserved as history, not as current truth.
> Planned or representative code is labeled as such. Code labeled **retained interface**
> or **verified implementation shape** reflects behavior that was actually implemented
> and terminal-tested.

## Current highest-level status

```text
✅ Phase 0  — Existing Hermes / Bristlecone runtime
✅ Phase 1  — Workshop / capability architecture
✅ Phase 2  — Runtime adapter foundation
✅ Phase 3  — Workshop controller migration
✅ Phase 4  — Runtime sessions
✅ Phase 5  — Seasonal lifecycle foundation
✅ Phase 6  — Winter durability
✅ Phase 7  — Spring wake / Cleaning
✅ Phase 8  — Spring restoration planner
✅ Phase 9  — Durable Spring decision
✅ Phase 10 — Controlled Spring application
✅ Phase 11 — Spring → Summer completion
✅ Phase 12 — Temporary capability restoration
✅ Phase 13 — Runtime-Independence Audit

✅ 14.1 — Prompt/schema baseline
✅ 14.2 — Cold/warm latency baseline
✅ 14.3 — Repeated-work map
✅ 14.4 — Hot-turn path audit
✅ 14.5 — Forest Cache Architecture / Coordinator
✅ 14.6 — Parsed manifests, resolution caches, Learning/User Context foundation
✅ 14.7 — Layered Hot Context
✅ 14.8 — Runtime Cache / Prefix Integration
✅ 14.9 — Source-Context Targeting

→ 14.10 — Quick / Normal / Deep
□ 14.11 — Small / Big escalation
□ 14.12 — Ollama vs llama.cpp
□ 14.13 — Speculative decoding
□ 14.14 — Final benchmark

Then:
□ Phase 15 — Leaf Foliage
```


# 0. How to Read This Archive

This archive combines:

1. verified terminal results from the current implementation thread;
2. earlier Bristlecone continuity archives;
3. Hermes/Ollama benchmark records;
4. architecture checkpoints created as the design evolved;
5. current Phase 14.9 completion data.

### Status legend

- ✅ **Verified complete** — implemented and behavior-tested.
- 🔬 **Real-runtime verified** — exercised against actual Hermes/Forest state.
- 🧪 **Synthetic/fake-runtime verified** — tested without changing live runtime.
- 📐 **Architecture decision** — accepted design boundary.
- 🕰️ **Historical** — true at an earlier point but superseded by later implementation.
- ⏳ **Pending/current next work**.
- ❌ **Rejected**.
- 💤 **Paused**.
- ⚠️ **Safety/invariant**.

### Code legend

- **Exact retained interface** — function/class/signature verified in source or terminal.
- **Verified implementation shape** — logic and behavior were implemented and tested,
  but this archive may show a condensed excerpt rather than every source line.
- **Historical code/config** — real earlier configuration retained for context.
- **Representative schema** — structurally accurate, but not necessarily a byte-for-byte
  dump of the current file.

The purpose is continuity, not source-control replacement. The actual canonical source
still lives under:

```text
/home/user/The-Forest/bristlecone
```

This repository directory is **not a Git repository**, so the engineering workflow
continues to require timestamped backups before modifying existing source.



# 1. North Star, Product Doctrine, and Tree Identity

## North Star

> **The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**

The metaphor must map to real technical behavior rather than being decoration.

| Forest concept | Technical meaning |
|---|---|
| Tree | AI identity / role / agent |
| Clone | independently operating extension of a Tree |
| Colony | base Tree + its Clones |
| Workshop | capability/tool/Skill boundary |
| Leaves | durable human-readable knowledge |
| Roots | provenance, dependencies, relationships |
| Soil | least-privilege execution environment |
| Spirit | deterministic permissions/action authority |
| Water | external information entering the Forest |
| Sunlight | user-originated information |
| Leaf Litter | shed material / lifecycle state |
| Syrup | inferred/distilled personalization |
| Mycelium | permission-aware cross-Tree continuity |
| Cedar Oil | encryption / data security |
| Sap | sensitive handling classification |
| Tar Sap | protected material not autonomously changed |
| Bud / Flower / Fruit | idea/project/output growth states |
| Pruning | deliberate user/Spirit-authorized shaping |
| Summer | Growing |
| Fall | Shedding |
| Winter | Dormant |
| Spring | Cleaning |

## Core doctrine

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

> **The Forest gets deeper as you wonder.**

> **Complete by default. Modular underneath.**

> **External tools are choices, not dependencies.**

> **A Tree is not its model.**

> **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**

> **The Forest should feel simple because complexity is organized, not because complexity is hidden or discarded.**

## Core Trees

### Cherry
Primary assistant Tree.

### Maple
Developer, organizer, semantic cartographer, personal-data steward, project/training/reviewer role.

### Cedar
Security Tree.

### Bristlecone Pine
**Treewright**: designs, codes, tests, debugs, evaluates, maintains, and helps train
Cherry, Maple, future Trees, plugins, and Forest add-ons.

Health phrase:

> **Pine is fine.**



# 2. Qubes OS, Host, and Runtime Environment

## Qubes environment

- Qubes OS
- XFCE + i3
- kitty
- zsh + oh-my-zsh
- Powerlevel10k
- rofi
- nitrogen
- picom / GLX

Important qubes:

- **Cherry-AI** — primary AI qube; Hermes, Ollama, Bristlecone, active Forest runtime development.
- **Maple** — developer/project/training/reviewer qube.
- **Seed-AI** — lighter training/review participant.
- **dom0** — host control only; broad AI work must not be moved into dom0.

## Known performance modes

### Forest Normal Mode
Historical known allocation:

```text
Cherry-AI:
  memory: 8192 MB
  maxmem: 16000 MB
  vCPUs: 9

Maple:
  memory: 800 MB
  maxmem: 8000 MB
  vCPUs: 4
```

### Pine Cone Mode
- Hermes/Ollama available.
- Model can remain unloaded until first use.
- ~15-minute keepalive verified.

### Maple Seed Mode
Frees resources for Maple development/training.

### Forest Mixed Mode
Mixed review/training.

### Seed Mixed target
Historical target:

```text
Maple      12288 / 16000 MB, 4 vCPUs
Cherry-AI   6144 /  9000 MB, 3 vCPUs
Seed-AI     2048 /  6000 MB, 2 vCPUs
```

Cherry-AI should use a more-developed Cherry Seed reviewer in that mode, not Bristlecone.

### i3 bindings
Num Lock OFF:

```text
Numpad 1 → Forest Normal
Numpad 2 → Pine Cone
Numpad 3 → Maple Seed
Numpad 4 → Forest Mixed
Numpad 5 → Seed Mixed target / later verification
```

## Qubes security direction

Cross-qube collaboration should use narrow, explicit channels such as:

- qrexec services;
- Git exchange;
- approved file transfer;
- purpose-specific handoff packets.

Do not weaken Qubes isolation merely to make AI coordination easier.



# 3. Hermes, Ollama, Bristlecone Model, and Newelle Findings

## Current stack

```text
Project Forest
    ↓
Hermes
    ↓
Ollama
    ↓
bristlecone-qwen35:4b-64k
```

Known endpoints/services:

```text
Hermes gateway: 127.0.0.1:8643
Ollama:         127.0.0.1:11434
Hermes service: hermes-bristlecone.service
Hermes profile: ~/.hermes/profiles/bristlecone
```

Gateway command concept:

```bash
hermes -p bristlecone gateway run
```

Model unload:

```bash
ollama stop bristlecone-qwen35:4b-64k
```

Keepalive of roughly 15 minutes was verified and persisted across Cherry-AI restart.

### Model-size history

An older runtime observation described the model at approximately **5.6 GB**.
A later archive recorded approximately **3.4 GB**. These are historical observations
from different checkpoints; capacity planning should recheck the live local model rather
than treating either number as immutable truth.

## Why Hermes became primary

Hermes provided:

- configurable toolsets;
- explicit Skill behavior;
- persisted sessions;
- session continuation and session ID rotation;
- a local gateway API;
- a runtime profile;
- a useful place to isolate runtime-specific behavior behind an adapter.

Newelle was tested but paused.

### Newelle stripped tests

```text
Run 1: 5:25.65 before useful output
Run 2: ~15 minutes, no answer → FAIL
Run 3: 5:42.23 welcome/suggestion prompts, no Bristlecone answer → FAIL
```

Decision:

> **Hermes is the primary Bristlecone interface/orchestration layer. Newelle is paused/optional.**

Newelle duplicate functions were disabled during optimization, including overlapping
agent/file/RAG/search/command/image features; TTS was retained by user preference.



# 4. Hermes Performance Investigation — What We Actually Learned

Performance work changed the architecture significantly because it showed that
**what is visible to the model** matters much more than merely how many capabilities
exist on disk.

## Early minimal-tool benchmarks — reasoning `none`

| Hermes toolsets | Observed time |
|---|---:|
| `file,terminal` | ~41 s |
| `file,terminal,todo` | 1:49.64 |
| `file,terminal,skills` | 2:42.40 |
| `file,terminal,skills,todo` | 2:49.16 |

Major result:

> **Tool/schema count strongly affects latency.**

This became one of the roots of Workshop-based selective capability exposure.

## Minimal Workshop cold runs

| Workshop | Observed |
|---|---|
| Design | ~2:52 first output |
| Code/Debug | ~3:12 first output; ~5:42 completion |
| Research | ~2:44 first output |
| Model | ~3:04 first output; ~11:49 completion |

Cold first-output average was about 2:58.

Warm follow-ups included:

```text
30.58 s
43.72 s
2.23 s
total sequence ~1:16.54
```

Warm reuse clearly mattered, but runtime behavior had significant variance.

## Raw/Ollama baseline work

Important controlled measurements:

```text
Raw tiny cold total:        10.68 s
Raw tiny warm total:         1.40 s
Raw cold TTFT:               9.74 s
Raw warm TTFT:               0.99 s
Raw long generation:         2.44 tok/s
```

A large raw prefill test:

```text
Prompt tokens:        5,915
Prompt evaluation:   130.91 s
Prompt speed:          45.18 tok/s
TTFT:                 131.48 s
Model load:             0.48 s
Generation:             0.47 s
```

This was crucial:

> **A warm model can still have multi-minute TTFT when CPU prompt prefill is large.**

## Real Hermes Normal tests

Same nominal input size: **12,341 tokens**.

```text
Warm model / first large prefix:
  wall: 5m42.793s
  cache-read tokens: 0
  cache-write tokens: 0

Immediate repeated prefix:
  wall: 27.782s
  cache-read tokens: 0
  cache-write tokens: 0

Genuine cold model:
  wall: 4m52.349s
  cache-read tokens: 0
  cache-write tokens: 0
```

The large drop on immediate repeated prefix strongly suggested lower-level prompt/prefix/KV
reuse, but the exact cache layer was not proven at that stage.

Important caution:

The one genuine-cold run happened to finish faster than one warm-model/first-prefix run.
That did **not** establish that cold is intrinsically faster; it demonstrated large
run-to-run variance in the full Hermes stack.

## Prompt/schema reductions over time

Earlier API:

```text
system prompt: 17,727 B
tool schemas:  40,712 B
tools:         25
```

Trimmed API:

```text
system prompt: 16,864 B
tool schemas:  28,188 B
tools:         12
```

Trimmed CLI:

```text
system prompt: 20,994 B
tool schemas:  31,532 B
tools:         14
```

Later Phase 14.1 baseline:

```text
system prompt:  9,832 B
tool schemas:  11,159 B
combined:      20,991 B
tools:              6
```

Despite the much smaller static footprint, Phase 14.2 warm response times still varied:

```text
158.82 s
189.47 s
63.75 s
```

Conclusion:

> Static prompt reduction succeeded, but model residency and static prompt size alone
> did not explain remaining latency.

## Phase 14.3–14.4 hot-path audit

The source audit found YAML parsing and capability resolution mainly in:

- controller;
- resolver;
- state management;
- Spring restoration paths.

They were not responsible for the 60–190 second direct adapter benchmark.

The benchmark path was effectively:

```text
create_session()
→ HermesRuntimeAdapter.send_turn()
→ POST /api/sessions/<id>/chat
→ wait
```

`send_turn()` itself performed relatively small Python work:

```text
validate session/message
→ encode session ID
→ build payload
→ HTTP POST
→ wait/read response
→ JSON decode
```

Thus the dominant delay was below most Forest bookkeeping.

This prevented us from wasting effort on Python caching as a fake latency cure.



# 5. Hermes Configurable Toolsets and Runtime Mapping

## Verified Hermes configurable toolsets

The following configurable toolsets were discovered/verified:

```text
web
browser
terminal
file
code_execution
vision
video
image_gen
video_gen
bfl
x_search
tts
stt
skills
todo
memory
context_engine
session_search
clarify
delegation
cronjob
homeassistant
spotify
discord
discord_admin
yuanbao
computer_use
```

Important implication:

Forest canonical `toolset` and `context` capabilities can both be transported through
Hermes configurable toolsets. Forest `skill` capabilities are delivered as Skill/instruction overlays.

## Hermes mapping file

Path:

```text
~/The-Forest/bristlecone/adapters/hermes.yaml
```

Verified mapping shape:

```yaml
schema_version: 1
tree: bristlecone
runtime: hermes

capabilities:
  todo:
    type: toolset
    target: todo

  clarify:
    type: toolset
    target: clarify

  session:
    type: toolset
    target: session_search

  memory:
    type: toolset
    target: memory

  web:
    type: toolset
    target: web

  file:
    type: toolset
    target: file

  terminal:
    type: toolset
    target: terminal

  code-execution:
    type: toolset
    target: code_execution

skills:
  debugging:
    target: systematic-debugging

  testing:
    target: test-driven-development

  model-evaluation:
    target: evaluation

  model-inference:
    target: inference

unresolved:
  leaf:
    reason: Forest-native Leaf Foliage access has not been implemented yet.

  special:
    reason: Placeholder for task-specific capabilities.

  model-benchmarking:
    reason: No exact Hermes mapping has been verified yet.

  quantization:
    reason: No exact Hermes mapping has been verified yet.

  training:
    reason: No exact Hermes mapping has been verified yet.

  runtime-inspection:
    reason: No exact Hermes mapping has been verified yet.
```

Quick map:

```text
file               → file
terminal           → terminal
todo               → todo
clarify            → clarify
session            → session_search
memory             → memory
web                → web
code-execution     → code_execution

debugging          → systematic-debugging
testing            → test-driven-development
model-evaluation   → evaluation
model-inference    → inference
```

## Critical resolver correction

A first resolver version incorrectly required non-Skill Hermes toolset transports
to have canonical Forest `kind: toolset`.

That broke `memory`:

```text
Forest:
  memory = context

Hermes:
  memory = configurable toolset transport
```

The resolver was corrected.

Canonical doctrine:

> **Canonical Forest kind describes what something IS. Runtime mapping describes HOW a runtime exposes it.**

Examples:

```text
Forest context    → Hermes toolset
Forest context    → future native context provider
Forest capability → future MCP/native tool
Forest skill      → Hermes Skill
```

Never distort canonical Forest meaning to satisfy one runtime.



# 6. Phase 1 — Workshop / Capability Architecture

**Current status: ✅ COMPLETE**

Phase 1 began as an effort to reduce capability bloat and understand Hermes Skill loading.
It ultimately established the Forest capability model.

## Four Workshops

### Research

Core:

```text
web
```

### Design

Core:

```text
memory
clarify
```

### Code / Debug

Retained Workshop example:

```yaml
schema_version: 2
tree: bristlecone
id: code-debug
name: Code / Debug

core:
  - file
  - terminal

ready:
  - code-execution
  - debugging
  - testing
  - special

policy:
  sticky_workshop: true
  minimum_useful_canopy: true
```

The old term `minimum_useful_canopy` exists historically in files. Later architecture
prefers **Layered Reuse and Selective Rebuild / Layered Hot Context** for the broader
cache/reuse system.

### Model

Core:

```text
file
terminal
```

Ready:

```text
model-evaluation
model-benchmarking
model-inference
quantization
training
runtime-inspection
```

## General Ready rack

```text
todo
clarify
session
memory
leaf
```

Ready means individually addressable and cheap to discover — **not model-visible by default**.

## Capability states

The model evolved from:

```text
Dormant
Active
Sticky
Core
```

to:

```text
Dormant
Active
Task-Sticky
Core
```

### Core
Automatically available for the current Workshop.

### Active
Temporary need for the immediate task/turn.

### Task-Sticky
Activated and retained across related turns inside one Forest Task.

### Dormant
Known to the Tree but not currently exposed.

## Canonical capability registry

Path:

```text
~/The-Forest/bristlecone/capabilities/registry.yaml
```

Known capabilities include:

```text
todo
clarify
session
memory
leaf
web
file
terminal
code-execution
debugging
testing
special
model-evaluation
model-benchmarking
model-inference
quantization
training
runtime-inspection
```

Example canonical kinds:

```text
todo           → toolset
file           → toolset
terminal       → toolset
code-execution → toolset

debugging      → skill
testing        → skill

memory         → context

special        → capability
```

## Shared resolver

Created:

```text
capabilities/resolver.py
```

Conceptual flow:

```text
Workshop
+ selected General
+ selected Ready
      ↓
validate Forest policy
      ↓
include Workshop Core
      ↓
canonical capability identity
      ↓
runtime adapter mapping
      ↓
separate:
  runtime toolsets
  runtime Skills
  unresolved capabilities
```

Example Code/Debug + todo + debugging:

```text
Canonical:
file
terminal
todo
debugging

Hermes toolsets:
file
terminal
todo

Hermes Skill:
systematic-debugging
```

Verified resolver behaviors included:

- Workshop Core automatic inclusion;
- canonical IDs;
- runtime toolsets;
- Skill bindings;
- `testing → test-driven-development`;
- `code-execution → code_execution`;
- invalid General fail closed;
- invalid Ready fail closed;
- unresolved `special` fail closed;
- curated unresolved reason surfaced;
- all four Workshop cores resolve.



# 7. Phase 1 Skill Experiment — What Failed and What Survived

Hermes Skill behavior was one of the earliest architecture-changing discoveries.

Known Skill overlay sizes:

```text
systematic-debugging:       14,510 characters
test-driven-development:    10,753 characters
```

## Rejected: Skill as the base system prompt

The attempt to make a Skill effectively become the persistent base prompt did not
behave as intended because Hermes restored its own base semantics.

Historical observed timings:

```text
failed Skill-as-base Turn 1:
  326.1 s
  input 5287
  output 491
  total 5778

failed Skill-as-base Turn 2:
  191.3 s
  input 5610
  output 462
  total 6072
```

## Retained approach: instruction overlay

Correct direction:

```text
Forest canonical Skill
        ↓
runtime adapter
        ↓
build runtime-specific Skill overlay
        ↓
pass as ephemeral instructions/system overlay
        ↓
reuse while Task remains relevant
```

Historical benchmark observations:

```text
valid overlay:
  279.13 s
  input 8827
  output 278
  total 9105

sticky reuse T1:
  197.99 s
  input 8823
  output 419
  total 9242

sticky reuse T2:
  307.33 s
  input 9140
  output 810
  total 9950

clean no-Skill:
  187.81 s
  input 5288
  output 238
  total 5526

deactivation active:
  183.71 s
  input 8826
  output 187

deactivation inactive:
  118.02 s
  input 5323
  output 204

state-driven:
  291.78 s
  input 8492
  output 334
  total 8826
```

Important interpretation:

Forest caching can prevent repeated discovery/read/parse/build of a Skill, but
the model still has to consume the Skill text when it is injected. Caching a Skill
in RAM is not the same as making it free in model context.

This led directly to:

> **Cached in RAM ≠ visible to the model.**

and eventually:

> **Forest owns semantic stickiness. Hermes owns execution. The adapter bridges the two.**



# 8. Task Sessions — Separation from User Conversation

The Task Session architecture was introduced after discovering that Hermes preloaded
Skills behaved similarly to Forest's concept of sticky capabilities.

Key distinction:

```text
USER CONVERSATION
        │
        ├── Forest Task A: Design
        ├── Forest Task B: Code / Debug + debugging
        └── Forest Task C: Research
```

One user conversation may span multiple internal Forest Tasks.

A Task can own:

```text
Reasoning Mode
Model Form
Workshop
Workshop Core capabilities
Task-Sticky Skills
temporary General overlays
temporary Ready overlays
Hot Leaves/context
task-specific state
runtime-session bindings
```

Early representative state:

```yaml
task_session:
  id: <forest-task-id>
  status: active
  started_at: ...
  updated_at: ...

  task_sticky_skills:
    - debugging

  temporary_capabilities: []

  runtime_sessions: {}
```

Forest Task IDs:

```text
forest-task-<UTC>-<8 hex>
```

The current `TaskSessionManager` lives in:

```text
runtime/task_session.py
```

and remains a central Forest lifecycle/control object, even though runtime-specific
behavior was progressively extracted into adapters.

## Important later API behavior

Exact constructor verified during Phase 14.9 testing:

```python
TaskSessionManager(
    forest_root=None,
    runtime_adapter=None,
)
```

Important `start_task()` behavior discovered:

```python
result = manager.start_task(
    state=working,
    persist=False,
)

runtime_state = result["state"]
task_session = result["task_session"]
```

`start_task()` returns a new state object; it does **not** mutate the passed-in state
object in place.

Runtime operations require an active Forest Task. The guard correctly rejects
`send_runtime_turn()` on inactive state.



# 9. Atomic Persistence, Locking, and No-Git Safety

## Atomic state writes

State persistence evolved into a durable pattern:

```text
validate state
→ acquire lock
→ write temp file in same directory
→ YAML serialize
→ flush
→ fsync
→ os.replace
```

Locking uses:

```python
fcntl.flock(..., LOCK_EX)
```

Active-state lock:

```text
.active.yaml.lock
```

Main active state:

```text
state/active.yaml
```

## Concurrency doctrine

For sensitive durable mutations:

```text
capture expected Task identity
→ acquire lock
→ reload latest state
→ revalidate Task ID / season / decision
→ rebuild against latest truth
→ atomic write
```

This avoids treating an earlier in-memory decision as current truth after another
process has modified Forest state.

## Engineering workflow because there is no Git repository

The root is not a Git repo.

Therefore:

1. timestamped backup before existing source mutation;
2. structural match guards;
3. abort on unexpected match counts;
4. syntax-check before install;
5. test in memory/disposable state first;
6. verify before persisting;
7. never blindly rerun a failed installer.



# 10. Temporary Capability Planning and Transactions

Temporary capabilities were separated from persistent/Task-Sticky state.

## Resolver categories

The temporary resolver distinguishes:

```text
all
toolsets
contexts
skills
capabilities
```

Verified examples:

```text
todo    → toolset → Hermes todo
memory  → context → Hermes memory transport
testing → Skill   → test-driven-development
leaf    → unresolved → fail closed
```

## Authorization

Rules:

```text
Workshop Core      → already active
General Ready      → authorized
current Workshop Ready → authorized
anything else      → denied
```

Code/Debug examples:

```text
todo             → AUTHORIZED via general_ready
testing          → AUTHORIZED via workshop_ready
file             → ALREADY ACTIVE via core
web              → DENIED
model-evaluation → DENIED
```

Authorization and runtime resolution are separate.

## Temporary activation planner

Retained interface:

```python
plan_temporary_activation(...)
```

Responsibilities:

- authorize request;
- exclude Core that is already active;
- resolve allowed additions;
- combine runtime toolsets + contexts into runtime toolsets;
- keep Skill bindings separate.

Example request:

```text
todo
memory
testing
file
```

produced:

```text
runtime toolsets:
  todo
  memory

Skill:
  testing → test-driven-development

file:
  excluded because already Core
```

## Temporary Hermes toolset transaction

Early implementation names inside TaskSessionManager included:

```text
_load_hermes_toolset_runtime
_hermes_configurable_toolsets
begin_temporary_runtime_toolsets
restore_temporary_runtime_toolsets
```

These behaviors were later moved behind the runtime adapter.

Live verified example:

```text
Before:
file
terminal

Inside:
file
memory
terminal
todo

After:
file
terminal
```

Transaction behavior:

```text
validate request
→ capture exact baseline
→ desired = baseline + requested
→ backup Hermes config
→ apply
→ reload
→ verify
→ use
→ restore exact baseline in finally
```

On failure, rollback uses the backup.

Forest durable state remains untouched by the temporary runtime transaction.

Known historical backup example:

```text
backups/hermes-temporary/config-20260808T235043-389581Z.yaml
```



# 11. Temporary Skill Layer and Unified Temporary Turn

Two separate caches were introduced:

```text
_skill_overlay_cache
_temporary_skill_overlay_cache
```

Counters used during verification:

```text
_overlay_build_count
_temporary_overlay_build_count
```

Retained methods:

```text
prepare_temporary_skill_overlay(...)
prepare_turn_skill_overlay(...)
```

Example:

Task-Sticky:

```text
debugging
→ systematic-debugging
```

Temporary for one turn:

```text
testing
→ test-driven-development
```

Combined turn:

```text
Canonical Skills:
debugging
testing

Runtime Skills:
systematic-debugging
test-driven-development
```

Next turn without temporary testing:

```text
Canonical:
debugging

Runtime:
systematic-debugging

Temporary prompt chars:
0
```

Task end clears both relevant Skill caches.

Important rule:

> **Cached temporary Skill text is not equivalent to an active/injected temporary Skill.**

## Unified temporary turn

Context manager retained historically:

```python
temporary_turn(...)
```

Flow:

```text
authorize + resolve
→ build Skill layers
→ begin temporary runtime toolsets
→ yield turn
→ finally restore exact runtime baseline
```

A deliberate `FOREST_TEST_EXCEPTION` inside the turn proved exception-path restoration.

Before exception:

```text
file
memory
terminal
todo
```

After:

```text
file
terminal
```

`active.yaml` remained unchanged.



# 12. Phase 2 — Runtime Adapter Foundation

**Current status: ✅ COMPLETE**

The Forest originally had too much Hermes-specific logic in `TaskSessionManager`
and the Workshop controller.

Decision:

> **The Forest owns meaning. The adapter owns translation. Hermes is replaceable.**

Runtime package:

```text
runtime/
├── __init__.py
├── task_session.py
└── adapters/
    ├── __init__.py
    ├── base.py
    ├── factory.py
    └── hermes.py
```

## Base adapter

Actual class:

```python
BaseRuntimeAdapter
```

not the earlier proposed name `RuntimeAdapter`.

Error:

```python
RuntimeAdapterError
```

Retained contract includes:

```python
verify_runtime(...)
get_active_toolsets(...)
begin_temporary_toolsets(...)
restore_temporary_toolsets(...)
apply_toolsets_exact(...)
restore_toolsets_exact(...)
build_skill_overlay(...)
create_session(...)
get_session(...)
send_turn(...)
end_session(...)
is_stale_session_error(...)
```

`RuntimeAdapterError` supports structured details such as:

```text
message
status_code
error_code
method
path
```

## Hermes adapter

Class:

```python
HermesRuntimeAdapter
```

Verified constructor:

```text
(
  profile_name='bristlecone',
  profile_home=None,
  repo=None,
  forest_root=None,
  api_base_url=None,
  api_timeout=30,
  turn_timeout=900
)
```

## Factory

File:

```text
runtime/adapters/factory.py
```

Exact public function:

```python
create_runtime_adapter(state, forest_root=None)
```

Behavior:

1. read `state.runtime`;
2. require `state.runtime.adapter`;
3. currently support `hermes`;
4. derive profile from state or `HERMES_HOME`;
5. return `HermesRuntimeAdapter`;
6. fail closed on unknown runtime.

This function is the portability seam for future llama.cpp or other runtimes.

## Temporary vs exact semantics

Temporary:

```python
begin_temporary_toolsets(...)
```

means:

```text
desired = baseline + requested
```

Exact:

```python
apply_toolsets_exact(...)
```

means:

```text
runtime configurable set = desired exactly
```

Rollback:

```python
restore_toolsets_exact(...)
```

restores the captured baseline.

Fake-runtime verification included:

- exact apply/restore;
- same-set zero-write;
- invalid toolset rejection;
- invalid zero-write;
- verification-failure rollback;
- original config bytes restored;
- temporary additive behavior preserved.



# 13. Phase 3 — Workshop Controller Migration

**Current status: ✅ COMPLETE**

Controller:

```text
bin/bristlecone-workshop.py
```

Launcher:

```text
bin/bristlecone-workshop
```

## Before refactor

The controller duplicated:

- capability resolution;
- Hermes mapping;
- Hermes config mutation;
- verification;
- backup/rollback.

It directly imported private/internal Hermes APIs:

```python
from hermes_cli.config import load_config, save_config
from hermes_cli.tools_config import _save_platform_tools, CONFIGURABLE_TOOLSETS
```

## After refactor

```text
Workshop CLI
    ↓
ForestCapabilityResolver
    ↓
runtime adapter factory
    ↓
BaseRuntimeAdapter
    ↓
exact runtime transaction
    ↓
runtime verification
    ↓
Forest state commit
```

Direct Hermes config mutation was removed from the controller.

Dry-run parity passed for:

- Code/Debug + todo + debugging;
- Code/Debug + testing;
- unresolved `special`;
- invalid General;
- invalid Ready;
- all four Workshop Core sets.

The `memory` canonical-context/Hermes-toolset mismatch was discovered here and
corrected at the resolver layer rather than changing Forest canonical meaning.

## Runtime-before-Forest transaction safety

Current pattern:

```text
resolve desired Forest set
→ resolve runtime adapter
→ apply runtime exactly
→ get active runtime toolsets
→ verify runtime truth
→ update Forest working state
→ atomic-write active.yaml
```

If runtime activation succeeds but Forest write fails:

```python
restore_toolsets_exact(...)
```

is invoked.

Fake live-path tests verified rollback and unchanged failed state.



# 14. Phase 4 — Runtime Sessions and Hermes Persisted Session API

**Current status: ✅ COMPLETE**

A major architecture rule emerged:

```text
Forest Task ID = stable canonical identity
Hermes session ID = mutable runtime pointer
```

Do not bind them as the same identity.

## Forest runtime-session state

Representative retained shape:

```yaml
runtime_sessions:
  hermes:
    session_id: CURRENT
    previous_session_id: OLD
    updated_at: ...
```

Task start initializes an empty runtime mapping.

Task end:

- captures runtime mappings for retirement/cleanup;
- clears active runtime mapping;
- allows runtime adapter cleanup afterward.

## Hermes persisted session endpoints discovered

```text
POST   /api/sessions
GET    /api/sessions/{session_id}
PATCH  /api/sessions/{session_id}
DELETE /api/sessions/{session_id}

GET    /api/sessions/{session_id}/messages
POST   /api/sessions/{session_id}/fork
POST   /api/sessions/{session_id}/chat
POST   /api/sessions/{session_id}/chat/stream
POST   /api/sessions/{session_id}/model
```

Create session accepts an ID/session_id or lets Hermes generate one.

Persisted chat:

- loads stored history;
- runs using session ID;
- returns effective session ID;
- returns JSON session ID;
- returns `X-Hermes-Session-Id`.

Hermes session IDs can rotate, including during compression.

## Real Forest ↔ Hermes session binding

A first authentication attempt failed safely because secret scope was missing.
No network request was made.

Corrected live test entered the Bristlecone profile runtime scope and resolved the
credential there.

Historical real test:

```text
Forest Task:
forest-task-20260809T000736Z-0013c37e

Hermes create:
HTTP 201
api_1786234056_203cb1ee

Lookup:
HTTP 200
```

The returned ID matched; disposable session cleanup succeeded.
`active.yaml` and Hermes config remained unchanged.

## B3 / B4 session milestones

Completed:

- B3 persistent binding;
- B3.1 cross-process resume;
- B3.2 crash-consistent pre-turn binding;
- B4.1 gateway restart + history survival;
- B4.2 stale-session recovery.

Crash-consistent rule:

> Persist a newly created runtime session binding before entering a long model call.

Stale flow:

```text
send persisted session fast path
        ↓
404 / session_not_found
        ↓
create replacement once
        ↓
current = new
previous = old
        ↓
CAS-like guarded persistence
        ↓
retry once
```

Properties:

- no GET preflight required;
- competing writer preserved;
- non-stale errors propagate normally;
- replacement stays durable even if retry later fails;
- recovery is one-shot.

Stale classifier recognizes only the verified stale signature:

```text
HTTP status 404
or
error code session_not_found
```



# 15. Hermes Authentication / Secret Scope

Hermes gateway authentication uses:

```text
API_SERVER_KEY
```

Important discovery:

The key is not simply a credential we should copy out of the gateway process environment.

Hermes has profile-scoped credential machinery including:

```text
build_profile_secret_scope
set_secret_scope
reset_secret_scope
current_secret_scope
get_secret
```

The gateway also uses internal:

```text
gateway.run._profile_runtime_scope
```

which installs profile-local runtime context and secret scope, then restores it.

Verified probe:

```text
Before:
Scope active: False

Inside Bristlecone profile scope:
Scope active: True
API_SERVER_KEY resolved: True
API key displayed: NO

After:
Scope active: False
```

Security invariant:

> **Never store, print, copy, log, or persist `API_SERVER_KEY` into Forest canonical state, Leaves, or debugging output.**

This secret-scope handling belongs inside the Hermes adapter, not generic Forest core.



# 16. Phase 5 — Seasonal Lifecycle Foundation

**Current status: ✅ COMPLETE**

Official lifecycle:

```text
🌞 Summer — Growing
🍂 Fall   — Shedding
❄️ Winter — Dormant
🌱 Spring — Cleaning
```

Important UX rule:

> **Cleaning must always be listed first in Spring UI/help/tooltips/docs.**

The seasons are control-plane states, not decorative labels.

Legacy normalization:

```text
legacy active   → Summer
legacy inactive → Winter
```

Task start:

```text
Summer
```

Task end:

```text
Winter
```

Generic active-season transitions allow Summer, Fall, Spring.

Winter goes through `end_task()` instead of a generic season switch.

Verified:

- normalization;
- transition validation;
- same-season zero-write;
- lifecycle tests.



# 17. Phase 6 — Winter Durability

**Current status: ✅ COMPLETE**

Durable Winter directory:

```text
state/tasks/winter/
```

One YAML record per dormant Task.

Representative schema:

```yaml
schema_version: 1
record_type: forest_winter_task
tree: bristlecone
task_id: ...
retired_at: ...
retired_order: ...
task_session: ...
activation_snapshot: ...
```

Winter preserves:

- Task ID;
- dormant/Winter lifecycle;
- previous season;
- Task-Sticky Skills;
- temporary capability records;
- runtime session bindings.

Activation snapshot preserves:

```text
Workshop
active General
active Ready
reasoning
model form
```

## Loss-averse ordering

```text
1. write Winter record
2. clear active.yaml
```

If the process crashes between those steps, the Task may exist twice temporarily,
but it is not lost.

Crash simulation passed.

## Winter discovery

`list_winter_tasks()` was implemented.

Behavior:

- lightweight summaries;
- malformed-record isolation;
- newest-first;
- deterministic ordering;
- nanosecond `retired_order`;
- legacy fallback if `retired_order` missing.



# 18. Phase 7 — Spring Wake / Cleaning

**Current status: ✅ COMPLETE**

Retained API:

```python
begin_spring_cleaning(
    task_id,
    state=None,
    persist=False,
)
```

Persistent safety order:

```text
write active Spring first
        ↓
delete Winter record second
```

If cleanup fails:

- durable Spring state remains;
- Winter copy may also remain;
- wake is not undone.

Spring wake preserves runtime lineage but does not blindly restore the previous active set.

It does **not** automatically resurrect:

- old Workshop;
- old Ready resources;
- Deep reasoning;
- Big model form.

Spring creates a durable Cleaning worksheet.

Representative structure:

```yaml
spring_cleaning:
  status: cleaning
  started_at: ...
  source_retired_at: ...

  activation_snapshot: ...

  restoration_decision: ...

  restoration_application: ...
```



# 19. Phase 8 — Spring Selective Restoration Planner

**Current status: ✅ COMPLETE**

Retained API:

```python
plan_spring_restoration(...)
```

The planner is read-only.

### Keep automatically

```text
Task identity
runtime_sessions
Task-Sticky Skills
```

### Already available

Previous resources that are already active in the current environment.

### Review

- previous Workshop if changed;
- previous General capabilities not active now;
- previous Ready capabilities not active now;
- temporary capabilities always require revalidation.

### Leave dormant

- previous reasoning if different;
- previous model form if different.

Critical rule:

> **Deep reasoning and Big model form never auto-resurrect from historical state.**

A duplicate planner definition was discovered during implementation and removed.
Exactly one planner remained after repair.

This is a useful example of the workflow rule:

> inspect source after surprising behavior; do not blindly layer another fix on top.



# 20. Phase 9 — Durable Spring Restoration Decision

**Current status: ✅ COMPLETE**

Retained API:

```python
record_spring_restoration_decision(...)
```

This records **approved intent**, not runtime activation.

The method explicitly reported:

```text
resources_activated: False
```

Representative decision:

```yaml
decided_at: ...

restore:
  workshop: code-debug
  general_capabilities:
    - todo
  ready_capabilities:
    - debugging
  temporary_capabilities: []

leave_dormant:
  workshop: ...
  general_capabilities: []
  ready_capabilities:
    - testing
  temporary_capabilities:
    - testing
  reasoning: deep
  model_form: big
```

Rules:

- active Spring Task required;
- Cleaning worksheet required;
- planner rebuilt against latest state;
- only reviewed subsets may be restored;
- unreviewed restoration rejected;
- omissions become dormant;
- Deep/Big remain dormant;
- preview is memory-only;
- persistence uses lock + Task revalidation;
- identical repeated decision is zero-write.

Canonical distinction:

```text
Decision ≠ Reality
```



# 21. Phase 10 — Controlled Spring Application

**Current status: ✅ COMPLETE, including real Hermes verification**

Retained API:

```python
apply_spring_restoration(
    state=None,
    persist=False,
)
```

Truth boundary:

```text
durable decision
      ↓
resolve desired working set
      ↓
apply runtime exactly
      ↓
verify runtime reality
      ↓
build Forest truth
      ↓
validate Skill mappings
      ↓
record restoration_application
      ↓
atomic Forest state write
```

If runtime or state fails:

- runtime rollback is invoked when a transaction exists;
- Forest must not falsely claim activation.

## Verified test target

Forest:

```text
Workshop: code-debug
General:  todo
Ready:    debugging
```

Hermes exact toolsets:

```text
file
terminal
todo
```

Canonical Task-Sticky Skill:

```text
debugging
```

Runtime Skill:

```text
systematic-debugging
```

Stayed dormant:

```text
testing Ready
testing temporary
Deep reasoning
Big model form
```

At this historical stage, temporary restoration intentionally failed closed until
its later Phase 12 lifecycle was implemented.

## Durable application record

Representative:

```yaml
spring_cleaning:
  restoration_application:
    status: verified
    applied_at: ...
    decision_decided_at: ...
    adapter: hermes
    workshop: code-debug
    general_capabilities:
      - todo
    ready_capabilities:
      - debugging
    temporary_capabilities: []
    canonical_active_ids:
      - file
      - terminal
      - todo
      - debugging
    runtime_toolsets:
      - file
      - terminal
      - todo
    runtime_skills:
      - systematic-debugging
    task_sticky_skills:
      - debugging
    skill_bindings: ...
```

Only verified runtime reality may receive:

```yaml
status: verified
```

Core distinction:

```text
Past      = what existed before Winter
Decision  = what Spring approved
Reality   = what exists after verified application
```

## Fake-runtime suite

Verified, among other things:

- preview no runtime call;
- correct target Workshop/General/Ready;
- exact toolsets;
- debugging Skill;
- no rollback on success;
- runtime mismatch rollback;
- state-write-failure rollback;
- repeated application zero-write;
- temporary restoration rejected before Phase 12;
- Deep/Big dormant;
- Task remains Spring;
- Cleaning remains Cleaning after application.

## Real Hermes tests

Real initial Hermes:

```text
file
terminal
```

Applied Spring target:

```text
file
terminal
todo
```

Real Skill:

```text
debugging → systematic-debugging
```

Then exact restoration:

```text
file
terminal
```

A stronger live `active.yaml` rehearsal also passed.

Known emergency backup directory:

```text
backups/live-spring-rehearsal/
```

Known files:

```text
active-before-live-spring-20260809T115355Z.yaml
config-before-live-spring-20260809T115355Z.yaml
```

Historical exact hashes from that checkpoint:

```text
active.yaml:
7904bc802fee0eadae5075c04f3df8359a0e44640da425fbdd62d28356dc9b60

Hermes config:
436da2a229114b6848ddc76f959d54bcd63017f4f93eb015d7e323976274c30b
```

At the end of the rehearsal, both files returned byte-identical/hash-identical.

This established:

> **Runtime truth before Forest truth.**

and:

> **If Forest commit fails after runtime mutation, roll runtime back.**



# 22. Phases 11–13 — Later Completion and Historical Status Reconciliation

**Current authoritative status: ✅ Phase 11, 12, and 13 COMPLETE**

An earlier August 9 continuity archive was created immediately after Phase 10 and therefore
correctly listed Phases 11–13 as pending **at that time**.

A later Phase 14 handoff explicitly records:

```text
✅ Phase 0–13
→ Phase 14
```

and later architecture checkpoints repeat:

```text
✅ Phase 11 — Spring → Summer completion
✅ Phase 12 — Temporary capability restoration
✅ Phase 13 — Runtime-Independence Audit
```

Therefore the old pending status is superseded.

## Phase 11 — Spring → Summer completion

Earlier planned API:

```python
complete_spring_cleaning(...)
```

The design contract that led into implementation required:

```text
verified restoration_application
+
Forest state still matches application
+
runtime toolsets still match application
+
Skill mapping still matches
        ↓
mark Cleaning completed
        ↓
Spring → Summer
```

Required design properties were:

- no runtime mutation during completion;
- reverify runtime before Summer;
- one locked atomic state write;
- `spring_cleaning.status: completed`;
- `completed_at`;
- season → summer;
- previous season → spring;
- idempotent repeat;
- runtime drift blocks completion;
- direct Spring→Summer bypass blocked during unfinished Cleaning.

**Current status is complete**, although this archive does not have the complete
line-by-line terminal transcript for the later implementation available in the retrieved
historical packets. Treat the above as the verified design contract plus current completion
status, not a claim that every source line is reproduced here.

## Phase 12 — Temporary capability restoration

Current status: complete.

The later invariants preserved from this work include:

- temporary approval ≠ persistent activation;
- temporary Skills remain non-Sticky unless separately approved;
- unresolved temporary capability fails before runtime mutation;
- temporary toolsets exist only for the turn and restore afterward;
- temporary resources require permission/Spirit revalidation;
- temporary lifecycle and expiration/removal are distinct from Task-Sticky state.

Earlier Phase 10 intentionally failed closed for temporary Spring restoration until this
work existed. That earlier refusal was therefore a safety feature, not missing architecture.

## Phase 13 — Runtime-Independence Audit

Current status: complete.

The audit consolidated these boundaries:

> **Runtime-specific names belong in adapters.**

> **Portable persistent fields should remain runtime-neutral.**

> `state.runtime.adapter` is a legitimate namespaced runtime identity.

> Controllers must use the configured adapter explicitly; do not silently default to Hermes.

> Canonical capability kind is separate from runtime transport.

> Forest Task identity, Workshops, permissions, learning, Leaves, and lifecycle must survive
> a future replacement of Hermes/Ollama.

This is why Phase 14 could later reason about native inference caches without polluting
Forest canonical state with Hermes/Ollama implementation details.



# 23. Clone / Colony Architecture Added Before and During Phase 14

Canonical definitions:

> **A Clone is an extension of a Tree, not another Tree.**

> **A Colony is a Tree and all of its Clones.**

> **One Tree. More than one place.**

Clone lifetimes:

```text
ephemeral
persistent
project
```

A persistent Clone is durable lightweight state, not permanent compute.

Possible runtime states:

```text
dormant
warm
hot
```

## Shared durable Tree/Colony state

- identity;
- personality/purpose;
- Leaves;
- Roots;
- Operational Learning;
- user corrections;
- Syrup access;
- Mycelium relationships;
- long-term history;
- stable preferences;
- approved Skills;
- Tree configuration.

## Clone-local active state

- current Task/session/conversation;
- Hot Context;
- active Workshop;
- Ready rack;
- temporary Skills/capabilities/files;
- assumptions;
- runtime session/model/KV state;
- Soil/environment;
- scratch state.

Key invariant:

> **Clones share durable Tree state, not unrestricted live context.**

Capability doctrine:

> **Trees own capability. Clones carry only capability they need.**

> **Shared capability, separate activation.**

> **A Clone inherits identity, not automatically every active privilege.**

> **Capabilities normally shared. Scarce resources leased.**

> **Clone count must not scale infrastructure count.**

Concurrency/scaling:

> **Retain cheaply. Activate selectively. Share aggressively.**

> **Resource cost should scale primarily with active work, not retained Clone count.**

> **Share the knowledge object, not the contextual decision.**

> **Concurrent identical work should collapse into one shared operation when the underlying truth is shared.**



# 24. Phase 14.1 — Fresh Prompt / Schema Baseline

**Status: ✅ COMPLETE**

After Phases 0–13, static prompt/tool footprint was remeasured.

Phase 14.1 snapshot:

```text
System prompt:  9,832 B
Tool schemas:  11,159 B
Combined:      20,991 B
Tools:          6
```

This was dramatically smaller than older Bristlecone configurations.

However, later latency tests proved that reduced static footprint alone did not guarantee
fast warm turns.



# 25. Phase 14.2 — Cold / Warm Latency Baseline

**Status: ✅ COMPLETE**

Warm repeated tests after the static prompt reduction:

```text
158.82 s
189.47 s
63.75 s
```

The best warm result proved the current stack could be materially faster than its slow runs.

Interpretation:

- model residency alone did not explain variance;
- static prompt size alone did not explain variance;
- investigation needed to separate prompt prefill, session reuse, runtime behavior,
  CPU inference, and lower-level prefix/KV effects.

Safety verification:

```text
Forest state unchanged: PASS
Hermes config unchanged: PASS
model returned to unloaded state: PASS
persistent source modified: NONE
```



# 26. Phase 14.3–14.4 — Repeated-Work Map and Hot-Path Audit

**Status: ✅ COMPLETE**

## 14.3 repeated-work source map

YAML parsing and capability resolution existed mainly in management paths rather than the
direct model-turn benchmark.

Initial decision:

```text
Manifest/resolver caching:
DEFER as a latency fix
```

because there was no evidence it caused multi-minute turn latency.

## 14.4 hot-turn path

The benchmark bypassed most TaskSessionManager lifecycle work and called the adapter directly:

```text
create_session()
→ send_turn()
```

Therefore measured 60–190 second latency did not include most Forest lifecycle operations.

Hermes blocking point was the API/model work after:

```text
POST /api/sessions/<id>/chat
```

This avoided optimizing the wrong layer.

Leading targets became:

```text
Hermes request/session behavior
Ollama prompt evaluation
Ollama generation
64K context behavior
prefix/KV reuse
reasoning behavior
CPU inference variability
```



# 27. Phase 14.5 — Forest Cache Architecture / Coordinator

**Status: ✅ COMPLETE**

Phase 14 introduced a generalized Forest-side cache doctrine.

Core principle:

> **Caches are derived. They are never authoritative Forest truth.**

Important rules:

- deleting a cache causes rebuild, not knowledge loss;
- cache entries carry schema/version identity;
- technical cache identity is separate from display labels;
- invalidation is dependency-aware;
- avoid duplicate caches of the same representation;
- runtime/model changes do not automatically invalidate Forest-neutral derived data;
- shared cache infrastructure should be reused across Trees/Clones when dependencies match.

Conceptual hierarchy:

```text
Forest Cache
    ↓
Tree Cache
    ↓
Clone Cache
    ↓
Task Cache
    ↓
Turn
    ↓
Runtime / inference cache
```

Native inference caches remain a different category and are not owned by Forest CacheCoordinator.

Concurrency:

The shared CacheCoordinator was made thread-safe for dictionary lifecycle, while expensive
producer/Cold work remains outside the coordinator lock.

Important distinction:

> **Cache identity should follow the truth object being cached, not whichever Clone happened to request it.**



# 28. Phase 14.6A–E — Manifest and Capability Resolution Caches

**Status: ✅ COMPLETE**

14.6 mapped YAML/manifest reads, resolver lifecycle, and integration points before adding caches.

### 14.6D Parsed-YAML cache

Rules:

- derived;
- dependency-fingerprinted;
- Forest-neutral;
- mutable parsed YAML must be deep-copied before caller mutation;
- deleting cache forces safe rebuild.

### 14.6E Capability-resolution cache

Installed in:

```text
capabilities/resolver.py
```

Backup:

```text
backups/phase14_6E_20260809T192122Z/capabilities/resolver.py
```

Behavior verification included:

```text
first resolution performs real canonical resolution
second resolver sharing Forest cache reuses it
resolution stored once
identity contains no Tree/Clone/Task/session scope
strict/permissive callers share canonical resolution
caller selection order preserved conservatively
caller mutation cannot poison cached result
changed source manifest invalidates result
deleting cache causes rebuild
```

Core architecture:

> **Capability resolution is Forest-shared. Capability activation is Clone-specific.**

Cache identity deliberately excludes:

```text
tree_id
clone_id
colony_id
task_id
session_id
```

and excludes:

```text
require_resolved
```

because strictness is caller behavior, not canonical resolution identity.



# 29. Phase 14.6F — Forest Learning + User Context Foundation

A preflight discovered that the `learning/` namespace was initially effectively empty:
no live implementation existed to preserve.

An early Operational-Learning-only JSONL draft was proposed but **not installed unchanged**
because the architecture evolved before execution.

Final foundation separates:

## Operational Learning

Examples:

- mistakes;
- successes;
- procedures;
- environment observations;
- recurring execution lessons.

## User Context

Explicit categories:

- Preferences;
- Constraints;
- Corrections;
- Current Context.

## Syrup

Inferred/distilled personalization.

Authority:

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

Core rule:

> **What the user explicitly says outranks what Forest inferred.**

## Cold / Warm / Hot

```text
COLD
durable authoritative records
        ↓
WARM
trigger/index structures
        ↓
routing decision
        ↓
HOT
only matched records
```

Doctrine:

> **Cold stores truth. Warm decides relevance. Hot contains only relevant.**

Context Trigger Index stays Forest-side rather than being model-visible on every turn.

Routing should use broad categories and deterministic signals before model classification.

Examples:

```text
shopping/recommendation → purchasing preferences
food                    → dietary context
software/services       → software preferences
communication           → communication/action policy
design                  → design preferences
technical work          → technical/workflow preferences
```

Trigger strengths:

```text
CHECK
MUST CHECK
```

MUST CHECK means Forest must not silently behave as if no constraint exists when required
context retrieval fails.

Independent generations:

```text
user_context_generation
operational_learning_generation
```

New meaningful input invalidates route state; execution steps do not.



# 30. Task-Sticky Context Routing Rules

Current Task-Sticky semantics:

- new meaningful input invalidates the current Route Stamp;
- already-loaded records may remain provisionally retained;
- route runs once for the new input;
- same record IDs + same generations may reuse loaded records;
- User generation change clears only User sticky context;
- Operational generation change clears only Operational sticky context;
- policy change clears both;
- Task end clears both.

Critical rule:

> **Conversation changes invalidate context routing; execution steps do not.**

This rule later becomes essential for runtime retry/recovery: a stale runtime session is
an execution event, not a new user input.



# 31. Phase 14.7 — Layered Hot Context

**Status: ✅ COMPLETE**

Main files:

```text
learning/hot_context.py
learning/foundation.py
learning/snapshot_provider.py
learning/turn_retrieval.py
learning/turn_instruction.py
```

## 14.7B — Stateless assembler

Type:

```python
HotContextAssembly
```

Fields:

```text
schema_version
prompt
user_context_record_ids
operational_learning_record_ids
section_names
character_count
```

Exact retained API:

```python
assemble(
    *,
    user_context_records,
    operational_learning_records,
)
```

Both arguments are keyword-only.

Semantic prompt order:

```text
1. User Corrections
2. User Constraints
3. User Preferences
4. Current Context
5. Operational Learning
```

Important distinction:

- provenance IDs preserve captured Route Stamp order;
- prompt rendering uses semantic authority order.

Result is immutable, stateless, Tree/Clone/Task-neutral, and fails closed on character budget.

## Historical retrieval

Added/used APIs:

```python
get_revision(record_id, revision)
_record_at_generation(...)
get_user_context_at_generation(...)
get_operational_learning_at_generation(...)
```

Rules:

- historical retrieval never silently returns a newer revision;
- global generation is a visibility boundary;
- committed learning records are deeply immutable;
- durable serialization explicitly thaws JSON-compatible containers;
- same `(domain,id,generation)` Cold load single-flights;
- different keys can load concurrently;
- exact `(record_id,revision)` publication single-flights;
- stable historical absence may be negatively cached;
- future generations fail closed.

## Snapshot provider / retained turn retrieval

Old in-flight turns can retrieve their captured historical truth without contaminating
newer Task sticky state.

Important rule:

> **An old snapshot-generation miss must never mutate newer sticky state.**

Policy changes invalidate retained snapshots.

## TurnInstructionComposer

One turn:

```text
resolve once
→ retrieve once
→ assemble once
→ immutable instruction snapshot
→ runtime attempts reuse it
```

A bug was found because the assembler API was keyword-only while one call site was positional.

Backup:

```text
backups/phase14_7D2B_20260809T235800Z/learning/turn_instruction.py
```

The call was corrected rather than weakening the assembler API.

Historical turn truth remains stable even if retrieval provenance later changes
from sticky to shared provider.

Rule:

> **Instruction determinism does not require retrieval-path provenance to remain identical after Task state changes.**

## Runtime recovery proof

`TaskSessionManager.send_runtime_turn()` was tested with stale recovery.

Both first send and retry received the **same exact Python `instructions` object**.

Two overlapping turns test:

```text
Captured turns:                2
Instruction snapshots:         2
Concurrent runtime attempts:   4
Meaningful-input transitions:  2
Runtime-triggered retrievals:  0
Runtime-triggered assemblies:  0
Cross-turn leakage:            0
```

## 14.7 performance

Representative six-record assembly:

```text
Assembler only:
  p50 7.77 µs
  p95 11.28 µs

Full compose, sticky:
  p50 24.54 µs
  p95 36.28 µs

Provider warm:
  p50 50.69 µs
  p95 77.62 µs

Provider cold:
  p50 2.373 ms
  p95 2.525 ms
```

Colony shared-cold wall:

```text
1 Clone:  p50  2.65 ms
10 Clone: p50  9.34 ms
50 Clone: p50 17.72 ms
```

Cold loads stayed fixed at **6** regardless logical Clone count.

Decision:

> No Phase 14.7 optimization patch was justified.



# 32. Phase 14.8 — Runtime Cache / Prefix Integration

**Status: ✅ COMPLETE**

This phase intentionally did **not** invent a Forest-owned KV cache.

Canonical principles:

> **Native inference caches are runtime-owned; Forest treats them through opaque interfaces/handles rather than reimplementing them.**

> **Forest may coordinate inference-cache lifetime and identity; runtime owns inference-cache contents.**

> **Forest CacheCoordinator stores derived Forest data; it is not an inference/KV cache.**

> **When a runtime exposes no explicit cache API, Forest treats the runtime session as the opaque continuity handle and makes no claims about cache contents behind it.**

> **A runtime session is an opaque continuity handle, not a Forest-owned cache object.**

Preflight found no explicit Hermes adapter controls for:

```text
cache
prefix
KV
keepalive
num_ctx
context_length
prompt_cache
cached_tokens
```

`ensure_runtime_session(state=None, persist=False)` does not GET/preflight an existing
session. If a binding exists, it reuses it.

Behavior:

```text
Forest binding S1
→ ensure reuses S1
→ runtime send(S1)
→ runtime reports stale at actual use
→ create S2 once
→ rotate binding
→ retry with S2
```

No speculative `inference_reuse_capability()` was added because Hermes did not expose a
real contract to support it.

This kept the Forest honest about what it could and could not prove.



# 33. Phase 14.9 — Source Context: Ownership Doctrine

**Status: ✅ COMPLETE**

Main doctrine:

> **Source Context is a Forest subsystem, not a Learning subsystem and not a runtime-adapter feature.**

> **Source truth is shared. Source relevance is turn-local.**

> **Share parsed source/index, not turn relevance decision.**

Final pipeline:

```text
SourceIdentity
    ↓
SourceFingerprint
    ↓
LocalSourceObserver
    ↓
SourceContentSnapshot
    ↓
SourceStructure
    ├─ Python AST
    └─ Markdown headings
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
    ├─ Learning instructions
    └─ Source Context
    ↓
one final immutable `instructions` string
    ↓
TaskSessionManager.send_runtime_turn(...)
```

Created files:

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



# 34. 14.9B — Neutral Source Models

Created:

```text
source_context/model.py
```

Core retained model names:

```python
SourceIdentity
SourceFingerprint
SourceRegion
SourceTarget
```

Conceptual separation:

```text
SourceIdentity
  stable source identity

SourceFingerprint
  observed source version

SourceRegion
  objective structural range

SourceTarget
  turn-local relevance decision
```

A SourceTarget must not mutate shared structure.

Important properties verified:

- frozen/hashable;
- fingerprint/source consistency;
- invalid ranges fail closed;
- duplicate fingerprint component names fail;
- stable technical identity separate from display name.



# 35. 14.9B — Local Observation and Fingerprinting

Created:

```text
source_context/observation.py
```

Exact constant:

```python
LOCAL_FILE_FINGERPRINT_METHOD = "stat-size-mtime-v1"
```

Core types:

```python
LocalSourceObservationError
LocalSourceObserver
```

Behavior:

1. canonicalize locator with `Path.resolve(strict=True)`;
2. require regular file;
3. default stable source ID:

```text
local-file:<sha256(canonical-locator)>
```

4. source kind:

```text
file
```

5. fingerprint components exactly:

```text
size
mtime_ns
```

The observer reads metadata only, not source contents.

It owns no cache and knows nothing about runtime.

### Safety-validation lesson

An installer initially failed because a naive textual guard saw the word
`CacheCoordinator` inside documentation.

Correction:

> **Static safety validation should inspect executable structure when practical; comments and docstrings are not runtime coupling.**



# 36. 14.9B — Race-Safe Immutable Source Snapshot

Created:

```text
source_context/snapshot.py
```

Core types:

```python
SourceSnapshotError
SourceChangedDuringReadError
SourceContentSnapshot
LocalSourceSnapshotReader
```

Snapshot fields include:

```text
source
fingerprint
text
encoding
content_sha256
byte_count
character_count
line_count
schema_version
```

Read sequence:

```text
observe metadata
→ stat path
→ open rb
→ fstat before
→ read bytes
→ fstat after
→ stat path after
→ observe after
→ verify all evidence
→ strict decode
→ immutable snapshot
```

Transient race-safety signature:

```text
(st_dev, st_ino, st_size, st_mtime_ns)
```

Persistent SourceFingerprint remains cheaper:

```text
size + mtime_ns
```

Why two layers?

> `size + mtime` is cheap reusable freshness identity.
> Device/inode/size/mtime around a read is stronger transient evidence that the bytes
> came from one stable file object.
> `content_sha256` provides exact identity for content-derived caches.

Tests caught:

- in-place mutation during read;
- same-size/same-mtime atomic replacement via inode/path validation;
- invalid UTF-8;
- changed revisions.



# 37. 14.9B — Python Objective Structure and Shared Provider

Created:

```text
source_context/structure.py
source_context/structure_provider.py
```

Exact constant:

```python
PYTHON_STRUCTURE_KIND = "python-ast-v1"
```

Core:

```python
SourceStructureError
SourceStructure
PythonSourceStructureBuilder
PythonSourceStructureProvider
```

Regions:

```text
whole source: python:module
python-class
python-function
python-async-function
python-method
python-async-method
```

Builder uses the immutable snapshot only, not filesystem I/O.

Qualified lexical parent relationships are retained.
Decorator line is included in the region start where applicable.
Duplicate definitions receive deterministic distinct region IDs.

Provider cache identity includes:

```text
source_id
structure kind
fingerprint method/components
content_sha256
```

This prevents same-size/same-mtime different-content collisions.

Single-flight behavior:

```text
same exact snapshot key:
  one parser producer

different keys:
  may parse concurrently
```

1 / 10 / 50 logical Clone callers for identical source truth produced one parse.

Rule:

> **Exact-snapshot single-flight, not global parser serialization.**



# 38. 14.9B — Markdown Objective Structure and Shared Provider

Created:

```text
source_context/markdown_structure.py
source_context/markdown_structure_provider.py
```

Exact constant:

```python
MARKDOWN_STRUCTURE_KIND = "markdown-headings-v1"
```

Core:

```python
MarkdownStructureError
MarkdownSourceStructureBuilder
MarkdownSourceStructureProvider
```

Supports:

- ATX headings `#` through `######`;
- Setext `=` level 1;
- Setext `-` level 2;
- heading hierarchy;
- section boundaries;
- duplicate heading labels;
- fenced code block exclusion using backticks or tildes;
- whole source `markdown:document`.

Heading-like text inside code fences is not interpreted as document structure.

Shared provider uses the same exact-version + content-hash + per-key single-flight rules
as Python structure.



# 39. 14.9C.1 — Deterministic Explicit Targeting

Created:

```text
source_context/targeting.py
```

Core types:

```python
SourceTargetingError
SourceTargetNotFoundError
SourceTargetAmbiguityError
DeterministicSourceTargeter
```

Exact retained method shapes:

```python
target_region_id(
    structure,
    region_id,
    *,
    reason="explicit structural region ID",
    required=True,
)

target_exact_label(
    structure,
    label,
    *,
    region_kind=None,
    reason="explicit unique structural label",
    required=True,
)
```

Rules:

- exact region ID;
- exact unique label;
- duplicate label → fail closed ambiguity;
- explicit region ID can disambiguate;
- whole-source selected only explicitly;
- missing target fails closed;
- no file I/O;
- no cache mutation;
- no fuzzy matching;
- no embedding/model targeting.

Boundary:

```text
COLONY-SHAREABLE TRUTH:
SourceSnapshot
SourceStructure
SourceRegion

TURN-LOCAL DECISION:
SourceTarget
```



# 40. 14.9C.2 — Canonical Source Reference Matching

Created:

```text
source_context/reference_matcher.py
```

Canonical signal behavior was measured directly against existing Forest Learning matcher
conventions before implementation.

Rules:

```text
strip surrounding whitespace
preserve case
deduplicate after stripping
preserve first-seen order
reject empty
reject whitespace-only
reject non-string
```

Examples:

```python
(" Alpha.work ", "Alpha.work")
→ ("Alpha.work",)

("Details", "DETAILS", "details")
→ all three preserved
```

Resolution precedence:

```text
1. exact region_id
2. exact unique structural label
3. ambiguous exact label
4. unmatched
```

Region ID is authoritative.

Result tracks:

```text
requested_signals
matched_signals
unmatched_signals
ambiguous_signals
targets
mode
schema_version
```

Important doctrine:

> **Source reference matching consumes canonical turn signals; it does not parse raw prompts.**

A second static-test false positive occurred because the words `fuzzy` and `similarity`
appeared in a docstring explaining that the matcher did **not** use them.
The implementation was correct; the validation was fixed to inspect executable AST.



# 41. 14.9C.3 — Bounded Ancestor Target Expansion

Created:

```text
source_context/target_expansion.py
```

Core:

```python
SourceTargetExpansionError
SourceTargetExpansion
BoundedSourceTargetExpander
```

Conceptual behavior:

```text
exact target
   ↓
nearest structural parent
   ↓
next parent only while hop budget allows
   ↓
STOP before whole source by default
```

Properties:

- ancestor-only;
- no siblings;
- no children;
- no unrelated regions;
- explicit `max_parent_hops`;
- whole-source parent requires opt-in;
- missing parent fails closed;
- cycles fail closed;
- frozen/hashable.

Examples:

```text
Python:
Alpha.method.nested
→ Alpha.method
→ Alpha
→ STOP before python:module

Markdown:
Details
→ Setup
→ Forest
→ STOP before markdown:document
```

Critical insight:

> **Being structurally related does not automatically make all related source relevant.**



# 42. 14.9C.4 — Bounded SourcePacket

Created:

```text
source_context/packet.py
```

Core:

```python
SourcePacketError
SourcePacketBudgetError
SourcePacketFragment
SourcePacket
SourcePacketAssembler
```

Main rule:

> **Targets contribute source text. Ancestors contribute structural breadcrumbs unless they were independently targeted.**

This solved a subtle problem: a class region may span all methods, so blindly dumping
an ancestor region would reintroduce sibling code that was never selected.

Packet behavior:

- explicit target text only;
- overlapping explicit ranges unioned/deduplicated;
- non-overlapping targets remain separate fragments;
- ancestor IDs/labels retained as metadata;
- whole-source body only if whole-source is itself an explicit target;
- hard character budget;
- hard line budget;
- no silent truncation.

Representative fragment model:

```python
@dataclass(frozen=True, slots=True)
class SourcePacketFragment:
    source: SourceIdentity
    fingerprint: SourceFingerprint
    region_ids: tuple[str, ...]
    start_line: int
    end_line: int
    text: str
```

Representative packet fields:

```python
@dataclass(frozen=True, slots=True)
class SourcePacket:
    source: SourceIdentity
    fingerprint: SourceFingerprint
    content_sha256: str
    fragments: tuple[SourcePacketFragment, ...]
    target_region_ids: tuple[str, ...]
    ancestor_region_ids: tuple[str, ...]
    ancestor_labels: tuple[str, ...]
    source_character_count: int
    source_line_count: int
    max_characters: int
    max_lines: int
```

### Important test correction

A verification originally asserted that two packets with identical selected source but
different budgets should be dataclass-equal.

That was wrong.

Correct rule:

> **Packet content may be identical while packet authorization/budget provenance differs.**

Budget provenance is intentionally part of the immutable value.



# 43. 14.9C.5 — Deterministic Source Rendering

Created:

```text
source_context/rendering.py
```

Core:

```python
SourcePacketRenderError
SourcePacketRenderBudgetError
RenderedSourcePacket
DeterministicSourcePacketRenderer
```

Rendered block includes stable metadata such as:

```text
source ID
source kind
display name
content SHA256
selected character/line counts
packet budgets
target IDs
ancestor breadcrumbs
fragment line ranges
exact selected source text
```

## Safe dynamic fence

The renderer measures the longest run of:

```text
`
~
```

inside selected source and chooses an outer Markdown fence longer than any run that source
contains.

Stable tie-break behavior was tested.

This means source containing its own triple-backtick block cannot accidentally close
the outer source-context fence.

## Path privacy

Local filesystem locator/path is hidden by default.

Opt-in exists for explicit locator rendering.

Rule:

> **Source provenance does not automatically authorize disclosure of an absolute path.**

## Render budget

Rendered output has its own hard character budget.

Failure behavior:

```text
overflow → fail closed
```

not silent truncation.



# 44. 14.9D — Forest-Level Final Turn Composition

Preflight found no production caller above:

```python
TaskSessionManager.send_runtime_turn(
    self,
    message,
    state=None,
    instructions=None,
    persist=False,
)
```

Learning and runtime did not import Source Context.

Therefore we created a Forest-level boundary:

```text
Learning instructions ───────┐
                             │
RenderedSourcePacket(s) ─────┼─► ForestTurnInstructionComposer
                             │
                             ▼
                   final instructions
                             │
                             ▼
                TaskSessionManager
                             ↓
                         runtime
```

Created:

```text
turn_composition.py
```

Core:

```python
ForestTurnCompositionError
ForestTurnCompositionBudgetError
ForestTurnInstructionComposition
ForestTurnInstructionComposer
```

## Important retained constants/authority policy

Source attachment is explicitly marked as:

```text
authority: reference-data
```

The notice states Source Context does not override:

- current user instruction;
- Forest policy;
- permissions;
- higher-priority instructions.

## No-source compatibility

Strongest verified backward-compatibility behavior:

```python
composition.instructions is learning_instructions
```

when no Source Context exists.

There is no wrapper, copy, or altered content for the no-source path.

## Condensed retained implementation shape

```python
class ForestTurnInstructionComposer:
    def compose(
        self,
        *,
        learning_instructions="",
        source_packets=(),
        max_characters,
    ):
        source_packets = self._canonical_packets(source_packets)

        if not source_packets:
            instructions = learning_instructions
        else:
            attachment = self._attachment(source_packets)

            if learning_instructions:
                # stable newline separation
                instructions = (
                    learning_instructions
                    + separator
                    + attachment
                )
            else:
                instructions = attachment

        if len(instructions) > max_characters:
            raise ForestTurnCompositionBudgetError(...)

        return ForestTurnInstructionComposition(
            learning_instructions=learning_instructions,
            source_packets=source_packets,
            instructions=instructions,
            max_characters=max_characters,
        )
```

Behavior verified:

- duplicate rendered packets collapse first-seen;
- distinct packets preserve first-seen order;
- hard final character budget;
- no silent truncation;
- deterministic;
- immutable/hashable result;
- inspection does not leak prompt/source contents;
- module imports no Learning/runtime/cache subsystem;
- module performs no source I/O or runtime work.

## Why production wiring was deferred

Read-only audit found:

```text
send_runtime_turn CALL SITES:
NONE
```

There is no production caller above that infrastructure boundary yet.

Decision:

> **Do not invent application/orchestration architecture solely to say Phase 14.9 is wired.**

Future real application caller can compose Learning + Source Context and then hand the
final immutable string to runtime.



# 45. 14.9D.2 — End-to-End Stale Recovery Proof

This was one of the strongest Phase 14.9 tests.

We used:

- real `TaskSessionManager`;
- real Forest Task lifecycle;
- `start_task(..., persist=False)`;
- injected fake runtime adapter;
- no runtime factory;
- no real Hermes;
- no Ollama;
- real `send_runtime_turn()` unchanged.

Important Task setup behavior:

```python
task_result = manager.start_task(
    state=working,
    persist=False,
)

runtime_state = task_result["state"]
```

Attempting runtime operations on the original inactive state correctly raised:

```text
TaskSessionError:
Runtime session operations require an active Forest Task Session.
```

We did **not** bypass the guard.

## Final instruction flow

```text
Source Context pipeline once
        ↓
Forest final composition once
        ↓
final Python string object I
        ↓
send_runtime_turn(... instructions=I)
        ↓
fake runtime S1 receives I
        ↓
synthetic stale session
        ↓
real Forest one-shot recovery
        ↓
fake runtime S2 receives SAME I
```

Verified:

```python
first_instructions is final_instructions
recovery_instructions is final_instructions
first_instructions is recovery_instructions
```

All passed.

## Recomputation tripwires

After final instructions were created, relevant upstream methods were temporarily
patched in-process to raise if called.

During runtime execution + stale recovery:

```text
source observation:          0
source reads:                0
structure builds:            0
reference matching:          0
source targeting:            0
target expansion:            0
packet assembly:             0
packet rendering:            0
Forest recomposition:        0
Learning recomputation:      0
Hot Context assembly:        0
```

Persistent Forest state remained unchanged because `persist=False`.

Canonical invariant:

> **Source Context participates in meaningful-turn composition, not runtime execution.**

> **Once the final Forest instruction snapshot exists, stale recovery is forbidden from reopening any upstream context/composition stage.**



# 46. 14.9 Final Benchmark

Representative source contained:

- one selected method;
- one sibling method that must not leak;
- one unrelated function that must not leak.

Correctness:

```text
selected source present: YES
sibling leakage:         NO
unrelated leakage:       NO
local locator leakage:   NO
persistent state change: NO
Hermes contacted:        NO
Ollama contacted:        NO
```

## Warm turn-local pipeline

Includes:

```text
reference match
→ expansion
→ packet
→ rendering
→ Forest final composition
```

500 samples:

```text
p50: 65.95 µs
p95: 100.37 µs
max: 323.11 µs
```

## Full cold source pipeline

Includes:

```text
snapshot read
→ AST structure parse
→ reference match
→ expansion
→ packet
→ render
→ final composition
```

30 samples:

```text
p50: 0.301 ms
p95: 0.334 ms
max: 0.564 ms
```

## No-source Forest composition

1000 samples:

```text
p50: 1.52 µs
p95: 1.67 µs
exact Learning string identity: YES
```

## Shared source / concurrent logical callers

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

All callers produced identical final instructions.

## Determinism

100 repeated pipelines produced identical final instruction SHA-256:

```text
7d91bdead53f4c54a44d3bd1668d79024864f1d00c50e6d676ea15372bc74802
```

Final decision:

> **No additional Phase 14.9 optimization is justified before evidence of a real workload bottleneck.**



# 47. Retained Runtime and Forest APIs — Quick Code Reference

This section is intentionally code-heavy for future implementation continuity.

## Runtime adapter factory

**Exact retained interface:**

```python
create_runtime_adapter(
    state,
    forest_root=None,
)
```

## Hermes adapter constructor

```python
HermesRuntimeAdapter(
    profile_name="bristlecone",
    profile_home=None,
    repo=None,
    forest_root=None,
    api_base_url=None,
    api_timeout=30,
    turn_timeout=900,
)
```

## Base adapter contract

```python
class BaseRuntimeAdapter(ABC):
    def verify_runtime(...): ...
    def get_active_toolsets(...): ...
    def begin_temporary_toolsets(...): ...
    def restore_temporary_toolsets(...): ...
    def apply_toolsets_exact(...): ...
    def restore_toolsets_exact(...): ...
    def build_skill_overlay(...): ...
    def create_session(...): ...
    def get_session(...): ...
    def send_turn(...): ...
    def end_session(...): ...
    def is_stale_session_error(...): ...
```

## TaskSessionManager constructor

**Exact verified:**

```python
TaskSessionManager(
    forest_root=None,
    runtime_adapter=None,
)
```

Constructor behavior includes:

```python
self.forest = Path(forest_root)
self.runtime_adapter = runtime_adapter
self._cache_coordinator = CacheCoordinator()
self._context_route_states_lock = RLock()
self._context_route_states = {}
self._overlay_build_count = 0
self._temporary_overlay_build_count = 0

self.state_file = self.forest / "state" / "active.yaml"
self.winter_tasks_dir = (
    self.forest / "state" / "tasks" / "winter"
)
self.registry_file = (
    self.forest / "capabilities" / "registry.yaml"
)
```

## Runtime adapter injection

Exact implementation observed:

```python
def _runtime_adapter_for_state(self, state):
    if self.runtime_adapter is not None:
        return self.runtime_adapter

    from .adapters.factory import create_runtime_adapter

    return create_runtime_adapter(
        state,
        forest_root=self.forest,
    )
```

The real implementation wraps errors into `TaskSessionError`, but the key behavior is:
an injected adapter bypasses the factory entirely.

## Adapter identity

```python
@staticmethod
def _runtime_adapter_name(runtime_adapter):
    adapter_name = getattr(
        runtime_adapter,
        "adapter_name",
        None,
    )

    if not adapter_name:
        raise TaskSessionError(...)

    return str(adapter_name)
```

## Runtime turn API

Exact signature:

```python
send_runtime_turn(
    self,
    message,
    state=None,
    instructions=None,
    persist=False,
)
```

The same `instructions` variable is passed to both normal send and stale recovery.

## Runtime session ensure

Exact signature:

```python
ensure_runtime_session(
    self,
    state=None,
    persist=False,
)
```

Existing binding reuse does not GET/preflight the remote runtime session.

## Task lifecycle

```python
start_task(
    self,
    state=None,
    persist=False,
)

end_task(
    self,
    state=None,
    persist=False,
)

transition_task_season(
    self,
    season,
    state=None,
    persist=False,
)

begin_spring_cleaning(
    self,
    task_id,
    state=None,
    persist=False,
)
```

Additional implemented lifecycle methods exist for Spring restoration/completion and Winter records.

## Hot Context assembler

```python
LayeredHotContextAssembler().assemble(
    *,
    user_context_records=...,
    operational_learning_records=...,
)
```

## Source observation

```python
LocalSourceObserver().observe(...)
```

Fingerprint method:

```python
"stat-size-mtime-v1"
```

## Source snapshot

```python
LocalSourceSnapshotReader().read(path)
```

## Python structure

```python
PythonSourceStructureBuilder().build(snapshot)
PythonSourceStructureProvider(...)
```

## Markdown structure

```python
MarkdownSourceStructureBuilder().build(snapshot)
MarkdownSourceStructureProvider(...)
```

## Explicit source targeting

```python
DeterministicSourceTargeter().target_region_id(...)
DeterministicSourceTargeter().target_exact_label(...)
```

## Source-reference matching

```python
SourceReferenceMatcher().match(
    structure,
    signals,
)
```

## Bounded expansion

```python
BoundedSourceTargetExpander().expand(
    structure,
    target,
    max_parent_hops=...,
    include_whole_source_parent=False,
)
```

## Packet assembly

```python
SourcePacketAssembler().assemble(
    snapshot,
    expansions,
    max_characters=...,
    max_lines=...,
)
```

## Packet rendering

```python
DeterministicSourcePacketRenderer().render(
    packet,
    max_rendered_characters=...,
    include_locator=False,
)
```

## Forest final composition

```python
ForestTurnInstructionComposer().compose(
    learning_instructions=...,
    source_packets=(...),
    max_characters=...,
)
```



# 48. Hermes Session Chat Payload and Runtime Cache Conclusions

Phase 14.8 preflight found the Hermes session-chat payload path dealt with normal fields such as:

```text
content
input
message
messages
role
user_message
```

No explicit adapter-level interface was found for:

```text
KV cache
prompt cache
cached tokens
prefix cache
context reuse object
num_ctx
context_length
```

Therefore the Forest deliberately did **not** claim visibility into those internals.

This is a recurring engineering principle:

> **Do not create an abstraction merely because a runtime might have an internal feature. Create it when the runtime exposes a real contract Forest can safely use.**



# 49. Rejected, Paused, and Reframed Designs

## ❌ Load all Workshops to inspect capability

Rejected because discovery should not require exposing all capability schemas.

Preferred fallback:

```text
0. current Workshop Core
1. current Ready
2. tiny Tree-owned manifests
3. other Workshop manifests
4. Open Workbench / broad fallback last
```

## ❌ Deep mode turns on all tools

Reason:

```text
Reasoning effort
≠
capability exposure
```

Deep reasoning and Workshop are independent axes.

## ❌ Workshop controls model strength

Reason:

```text
Workshop
≠
Model Form
```

Small/Big is a separate axis.

## ❌ Big replaces Small Bristlecone

Small/Windowed remains useful for routine work.
Big/Fullscreen is later escalation/reviewer capacity.

## ❌ All capabilities stay loaded

Violates selective exposure and increases prompt/schema cost.

## ❌ Workshop profiles rebuilt from disk every prompt

Preferred:

```text
disk source
→ parse/validate
→ prepared Warm representation
→ cheap reuse
```

## ❌ Hermes configuration is the authoritative Tree

Would couple Tree identity to one agent runtime.

## ❌ Ollama configuration is the authoritative Tree

Would couple identity to one inference backend.

## ❌ Skill-as-base system prompt

Hermes restored base semantics; retained model is runtime Skill/instruction overlay.

## ❌ Duplicate resolver logic inside Spring

Spring should reuse the shared Forest capability resolver.

## ❌ TaskSessionManager directly manipulates Hermes config

Runtime-specific behavior moved behind `HermesRuntimeAdapter`.

## ❌ Additive temporary semantics for authoritative Spring restoration

Spring authoritative restoration uses exact-set runtime application.

## ❌ Change `memory` canonical kind merely to fit Hermes

Canonical kind and transport remain separate.

## ❌ Auto-restore Deep / Big after Winter

Historical resource intensity does not imply current permission/need.

## 💤 Newelle primary path

Paused due latency and unreliable response completion.

## Reframed: Debug Workshop

Old separate debugging/system concepts became:

```text
Code / Debug Workshop
+
Debugging Skill
```

## Reframed: Retrieval Workshop

Retrieval is increasingly treated as shared Forest retrieval/Leaf/source infrastructure,
not necessarily a user-facing Workshop.

## Reframed terminology

Older notes used “Minimum Useful Canopy” as a broad optimization label.

Current architecture uses:

> **Layered Reuse and Selective Rebuild**

or:

> **Layered Hot Context**

for the cache/context reuse system.



# 50. Bugs, Test-Harness Mistakes, and Repair Lessons

This history is important because many apparent failures were **not product failures**.

## Hermes YAML indentation / configuration correction

An `api_server:` alignment/indentation problem was corrected under the Hermes profile
configuration. After correction, prompt-size inspection reported the intended model/runtime
configuration correctly.

## Resolver `memory` parity bug

Problem:

```text
memory canonical kind = context
Hermes transport = toolset
```

The resolver incorrectly tied canonical kind to transport.
Fixed by separating those axes.

## Duplicate Spring planner definition

A duplicate implementation existed.
It was discovered, backed up, removed, and exactly one planner remained.

## Keyword-only HotContext API mismatch

`LayeredHotContextAssembler.assemble()` was intentionally keyword-only.
A caller used positional arguments.
The caller was fixed; the safe API was retained.

## Source matcher static false positive

Validation searched raw file text for forbidden words.
A docstring contained `similarity` only to say similarity was not used.
Validation changed to executable AST inspection.

## SourcePacket equality test mistake

Same source selection under different budgets was incorrectly expected to compare equal.
Corrected because budget authorization is part of packet provenance.

## C.4A malformed pasted verifier

A duplicated summary line caused an `IndentationError`.
Python parsed nothing, so no Forest behavior had run.

## D.1B large installer paste corruption

A long heredoc was mangled and produced:

```text
SyntaxError: unmatched ')'
```

before execution.

Corrected installer pattern:

```text
mktemp
→ write candidate module
→ python -m py_compile candidate
→ mv into place only after syntax succeeds
```

## D.2 inactive Task harness

The first stale-recovery test correctly failed with:

```text
Runtime session operations require an active Forest Task Session.
```

This was a harness setup error.

It revealed a useful lifecycle truth:
`start_task()` returns the new active state rather than mutating the passed state.

Correct setup:

```python
result = manager.start_task(
    state=working,
    persist=False,
)

runtime_state = result["state"]
```

We preserved the Task guard instead of bypassing it.

## General lesson

> **A failing verification is evidence to inspect, not permission to blindly patch production code.**



# 51. Known Backups and Safety Artifacts

This list is historical and not necessarily exhaustive.

Early runtime backups:

```text
backups/runtime/task-session-20260808-194150.py
backups/runtime/task-session-20260808-194223.py
backups/runtime/task-session-20260808-194745.py
backups/runtime/task-session-20260808-194928.py
backups/runtime/task-session-20260808-195210.py
backups/runtime/task-session-20260808-195349.py
backups/runtime/task-session-20260808-200134.py
```

State/config:

```text
backups/task-state/active-20260808-193231.yaml
backups/hermes-temporary/config-20260808T235043-389581Z.yaml
```

Seasonal/Spring:

```text
task-session-before-seasonal-lifecycle-20260809T091245Z.py
task-session-before-winter-storage-20260809T091936Z.py
task-session-before-winter-discovery-v2-20260809T092241Z.py
task-session-before-spring-cleaning-20260809T092653Z.py
task-session-before-durable-spring-cleaning-v3-20260809T094104Z.py
task-session-before-spring-restoration-plan-20260809T094250Z.py
task-session-before-planner-dedup-20260809T094725Z.py
task-session-before-spring-decisions-v2-20260809T094910Z.py
resolver-before-runtime-transport-fix-20260809T113258Z.py
bristlecone-workshop-before-shared-resolver-20260809T113018Z.py
bristlecone-workshop-before-shared-resolver-v2-20260809T113448Z.py
base-before-exact-toolsets-20260809T113720Z.py
hermes-before-exact-toolsets-20260809T113720Z.py
bristlecone-workshop-before-runtime-factory-20260809T114220Z.py
task-session-before-spring-application-20260809T114957Z.py
```

Live Spring:

```text
backups/live-spring-rehearsal/
active-before-live-spring-20260809T115355Z.yaml
config-before-live-spring-20260809T115355Z.yaml
```

Phase 14:

```text
backups/phase14_6E_20260809T192122Z/capabilities/resolver.py
backups/phase14_7D2B_20260809T235800Z/learning/turn_instruction.py
```

Additional Phase 14.7 source backups also exist from earlier steps.



# 52. Current Canonical File Map

Tree root:

```text
/home/user/The-Forest/bristlecone
```

Hermes profile:

```text
/home/user/.hermes/profiles/bristlecone
```

Important project paths:

```text
bin/
corpus/
logs/
workshops/
adapters/
routing/
learning/
state/
skills/
capabilities/
runtime/
source_context/
backups/
```

Runtime:

```text
runtime/__init__.py
runtime/task_session.py
runtime/adapters/__init__.py
runtime/adapters/base.py
runtime/adapters/factory.py
runtime/adapters/hermes.py
```

Capabilities:

```text
capabilities/registry.yaml
capabilities/resolver.py
```

Hermes mapping:

```text
adapters/hermes.yaml
```

Controller:

```text
bin/bristlecone-workshop.py
bin/bristlecone-workshop
```

Learning/Hot Context:

```text
learning/foundation.py
learning/snapshot_provider.py
learning/turn_retrieval.py
learning/hot_context.py
learning/turn_instruction.py
```

Source Context:

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
```

Forest final turn composition:

```text
turn_composition.py
```

State:

```text
state/active.yaml
state/tasks/winter/
```



# 53. Current Cache and Context Architecture

## Cold / Warm / Hot

### Cold
Authoritative durable truth:

```text
Tree identity
Workshop YAML
capability registry
Skill source
Forest Learning
User Context
Leaves
permissions/policy
Task history
```

### Warm
Derived/prepared Forest-side data:

```text
parsed manifests
capability mappings
trigger indexes
historical snapshot cache
structure indexes
prepared Skill metadata
shared source structure
```

Warm does not mean model-visible.

### Hot
Only what is needed now:

```text
Workshop Core
active General
active Ready
Task-Sticky Skills
temporary permitted capability
relevant User Context
relevant Operational Learning
targeted Source Context
current task/turn
```

## Reuse doctrine

> **Layered Reuse and Selective Rebuild**

Keep stable layers reusable.
Track dependencies.
Invalidate only affected layers.
Rebuild only invalid layers.
Compose Hot Context from retained + rebuilt layers.

## Inference state boundary

Forest may own semantic/context reuse, but:

```text
prompt cache
KV cache
native prefix cache
runtime model state
```

belong to the runtime unless an explicit supported interface exists.



# 54. Operational Learning, Syrup, Mycelium, and Leaf Direction

These concepts are broader than Phase 14.9 but shaped the Learning/Context architecture.

## Operational Learning

Structured experience about:

```text
what happened
what worked
what failed
what should change next time
how to execute better
```

Examples:

- do not blindly rerun a failed command;
- inspect exact source after structural mismatch;
- back up before mutation without Git;
- temporary approval does not imply persistent activation.

Potential scopes:

- general;
- Workshop;
- Tree-specific;
- environment;
- user corrections.

Operational Learning is not just another ordinary Leaf.

## Syrup

Distilled personalization/tendency inference.

Example distinction:

```text
Syrup:
User tends to prefer concise openings.

Operational Learning:
User explicitly requires runtime verification before phase completion.
```

## Mycelium

Permission-aware cross-Tree continuity.

> **Trees share continuity without sharing consciousness.**

> **Water is visible transfer. Mycelium is hidden continuity.**

Cross-Tree context should come from shared permitted Forest records, not unrestricted access
to another Tree's conversations.

## Leaf Foliage direction

Phase 15 remains next major knowledge-storage phase after Phase 14.

Preferred Leaf properties:

- local-first;
- offline-capable;
- human-readable Markdown;
- stable IDs;
- metadata;
- wiki/Markdown links;
- derived graph/index/backlinks;
- selective retrieval;
- Obsidian-compatible where practical;
- non-destructive vault attach/import;
- ordinary Markdown export;
- portable “potted” selections;
- optional sync only.

Do not load all Leaves into model context.



# 55. Engineering Invariants — Consolidated

These are the rules that should survive future refactors.

## Runtime / state truth

1. **Runtime truth before Forest truth.**
2. If runtime mutates and Forest commit fails, roll runtime back.
3. Decision is not reality.
4. A durable record claiming activation must represent verified reality.
5. Runtime recovery is execution, not conversational input.
6. Runtime retry/recovery reuses already-frozen turn instructions.
7. Runtime-specific names belong in adapters.
8. Canonical capability kind is separate from runtime transport.
9. A runtime session is an opaque continuity handle.
10. Native inference caches are runtime-owned unless a real explicit API says otherwise.

## Tasks / seasons / concurrency

11. Forest Task ID is stable canonical identity; runtime session ID is mutable pointer.
12. Sensitive durable writes revalidate latest Task identity under lock.
13. Winter write happens before active-state clearing.
14. Spring wake writes active Spring before deleting Winter.
15. Deep does not auto-resurrect.
16. Big does not auto-resurrect.
17. Temporary approvals do not imply persistent activation.
18. Temporary Skills are not Task-Sticky unless separately approved.
19. Unresolved temporary capability fails before runtime mutation.
20. Spring completion is certification of verified state, not another activation event.

## Cache / reuse

21. Caches are derived, never source truth.
22. Deleting cache must cause rebuild, not knowledge loss.
23. Cache invalidation is dependency-aware.
24. Avoid duplicate caching of the same representation.
25. Forest-neutral cache survives runtime/model changes when dependencies remain valid.
26. Capability resolution is Forest-shared; capability activation is Clone-specific.
27. Cache identity should not include Clone/Task/session scope when the cached truth does not.
28. Concurrent identical Cold work should single-flight.
29. Different keys should remain concurrently buildable.
30. Resource cost should scale primarily with active work, not retained Clone count.

## Learning / context

31. User Preference, Constraint, Correction, and Current Context are distinct.
32. Explicit User Context outranks Syrup.
33. Trigger indexes are Warm; actual durable records are Cold.
34. Deterministic routing before AI routing when practical.
35. New meaningful conversation input invalidates routing; execution does not.
36. User and Operational generations are independent monotonic clocks.
37. Generation is assigned at durable commit.
38. Old in-flight turns cannot downgrade newer sticky state.
39. Historical retrieval never silently returns newer truth.
40. Route Stamp defines selected record/provenance order; assembler owns semantic formatting.
41. Hot assembler is stateless and Tree/Clone/Task-neutral.
42. One turn retrieves/assembles once; retry uses exact result.

## Source Context

43. Source Context is Forest-owned, not Learning/runtime-owned.
44. Source truth is shared; relevance is turn-local.
45. Source observation is metadata-only.
46. SourceFingerprint uses size + mtime_ns for cheap freshness.
47. Safe source read uses stronger dev/inode/size/mtime evidence.
48. Content SHA256 protects exact content-derived cache identity.
49. Objective SourceStructure is Colony-shareable.
50. SourceTarget is turn-local.
51. Exact structure caches retain old/new versions independently.
52. Canonical source signals trim whitespace, preserve case/order, dedupe first-seen, reject invalid values.
53. Exact region ID takes precedence over label.
54. Ambiguous labels are explicit and never guessed.
55. No silent whole-source targeting fallback.
56. Expansion is bounded ancestor-only.
57. Whole-source ancestry requires explicit permission.
58. Structural ancestry does not imply ancestor body inclusion.
59. Explicit targets contribute source text.
60. Ancestors are breadcrumbs unless independently targeted.
61. Overlapping selected text is deduplicated.
62. Packet budgets fail closed; no silent source truncation.
63. Packet equality retains budget-policy provenance.
64. Renderer hides local filesystem path by default.
65. Renderer delimiter must not be closable by selected source.
66. Render budget fails closed.
67. Source Context is reference data, not instruction authority.
68. Final Forest composition belongs neither to Learning nor Runtime.
69. No-source composition preserves exact existing Learning string object.
70. Stale runtime recovery cannot reopen Source Context or upstream composition.

## Engineering workflow

71. No blind reruns.
72. Back up existing source before mutation.
73. Use structural guards and exact match counts.
74. Syntax-check before install.
75. Test in memory/disposable state first when practical.
76. Verify behavior before marking complete.
77. Keep credentials out of state/logs/Leaves/output.
78. Preserve passing regression tests.
79. Do not invent architecture solely to satisfy a checklist.
80. Optimize measured bottlenecks, not fashionable features.



# 56. Benchmark Master Table

This table intentionally mixes historical checkpoints. Dates/configurations differ, so use it
as engineering history rather than pretending every row is directly comparable.

| Area | Measurement | Result |
|---|---|---:|
| Hermes minimal | file+terminal | ~41 s |
| Hermes minimal | +todo | 1:49.64 |
| Hermes minimal | +skills | 2:42.40 |
| Hermes minimal | +skills+todo | 2:49.16 |
| Workshop cold | Research TTFT | ~2:44 |
| Workshop cold | Design TTFT | ~2:52 |
| Workshop cold | Code/Debug TTFT | ~3:12 |
| Workshop cold | Model TTFT | ~3:04 |
| Newelle | stripped run 1 | 5:25.65 |
| Newelle | stripped run 2 | ~15m fail |
| Raw Ollama | tiny cold total | 10.68 s |
| Raw Ollama | tiny warm total | 1.40 s |
| Raw Ollama | cold TTFT | 9.74 s |
| Raw Ollama | warm TTFT | 0.99 s |
| Raw large prefill | 5,915 tokens | 130.91 s |
| Raw large prefill | speed | 45.18 tok/s |
| Hermes Normal | 12,341 tokens first prefix | 5m42.793 |
| Hermes Normal | immediate repeat | 27.782 s |
| Hermes Normal | genuine cold | 4m52.349 |
| Phase 14.2 warm | run | 158.82 s |
| Phase 14.2 warm | run | 189.47 s |
| Phase 14.2 warm | best | 63.75 s |
| 14.7 Hot assembler | p50 | 7.77 µs |
| 14.7 full sticky compose | p50 | 24.54 µs |
| 14.7 provider warm | p50 | 50.69 µs |
| 14.7 provider cold | p50 | 2.373 ms |
| 14.9 warm source turn | p50 | 65.95 µs |
| 14.9 warm source turn | p95 | 100.37 µs |
| 14.9 cold source path | p50 | 0.301 ms |
| 14.9 no-source composition | p50 | 1.52 µs |
| 14.9 10 callers | p50 | 1.954 ms |
| 14.9 50 callers | p50 | 7.030 ms |

Main performance conclusion so far:

> **Forest-side deterministic routing, caching, and Source Context are now very cheap relative
> to the historical multi-second/minute Hermes/model path.**



# 57. Current Phase 14 Roadmap and Exact Resume Point

Current:

```text
✅ 14.7 Layered Hot Context
✅ 14.8 Runtime Cache / Prefix Integration
✅ 14.9 Source-Context Targeting

→ 14.10 Quick / Normal / Deep
□ 14.11 Small / Big escalation
□ 14.12 Ollama vs llama.cpp
□ 14.13 speculative decoding
□ 14.14 final benchmark
```

## 14.10 design constraints already established

Quick/Normal/Deep controls reasoning effort and must remain distinct from:

```text
Workshop
Model Form
```

The three independent axes remain:

```text
Reasoning:
Quick / Normal / Deep
(or older Light / Normal / Deep terminology)

Workshop:
Research / Design / Code-Debug / Model

Model Form:
Small / Big
```

Constraints:

1. Forest reasoning mode is canonical/runtime-neutral.
2. Runtime adapter translates it to runtime-specific controls.
3. Deep must not silently become sticky.
4. Temporary escalation must not permanently alter Tree configuration.
5. Runtime recovery reuses the already-decided mode for the in-flight turn.
6. New meaningful input may produce a new mode decision.
7. Execution/retry does not reclassify complexity.
8. Quick/Normal/Deep is separate from 14.11 Small/Big.
9. Deep must not imply “turn on every tool.”
10. Explicit user override should remain possible.

Likely first step:

> **14.10A — inspect current reasoning controls in Hermes/runtime adapters and define a canonical Forest reasoning-mode model before changing behavior.**



# 58. Older and Current Continuity Artifacts

Known project/continuity artifacts from this work include:

```text
bristlecone_workshops_reasoning_model_forms_plan_and_rejected_concepts.md
forest_minimum_useful_canopy_and_tree_workshops.md
forest_workshop_skill_finder_and_operational_learning_architecture.md
forest_portable_tree_runtime_and_high_speed_workshop_architecture.md
bristlecone_capability_registry_and_individual_tool_activation.md
bristlecone_task_sessions_and_session_sticky_skills_update.md
bristlecone_skill_session_implementation_decision.md
bristlecone_layered_hot_context_and_task_session_cache_update.md

bristlecone_forest_complete_continuity_archive_2026-08-08.md
bristlecone_forest_complete_continuity_archive_2026-08-09.md

forest_data_ecology_mycelium_maple_leaf_lifecycle_checkpoint_2026-08-09.md
forest_tree_clone_colony_architecture_checkpoint_2026-08-09.md
forest_product_doctrine_learning_ecosystem_and_colony_checkpoint_v2_2026-08-09.md
forest_user_context_routing_and_learning_checkpoint_2026-08-09.md
forest_phase14_current_state_handoff_2026-08-09.md
forest_phase14_7_colony_hot_context_checkpoint_2026-08-09.md
forest_phase14_7_layered_hot_context_complete_checkpoint_2026-08-09.md
project_forest_bristlecone_chat_transfer_2026-08-09.md
forest_phase14_9_source_context_complete_checkpoint_2026-08-09.md
```

A prior attempted comprehensive archive named approximately:

```text
bristlecone_workshop_runtime_continuity_and_infrastructure_plan_2026-08-08.md
```

failed during creation and should not be assumed to exist.



# 59. Confidence Notes and Historical Reconciliation

### High-confidence / current

The following have direct recent completion evidence:

- Phase 0–13 overall complete before Phase 14;
- Phase 14.1–14.9 through the current thread;
- all 14.9 files, behavior, recovery test, concurrency, and benchmark;
- Hermes primary / Newelle paused;
- runtime-adapter ownership boundary;
- Source Context ownership boundary;
- no production caller above `send_runtime_turn()` at Phase 14.9 closeout.

### Historical but useful

Older archives preserve the exact journey through:

- Task-Sticky Skills;
- direct Hermes coupling before adapter extraction;
- Spring application before completion;
- earlier prompt/schema sizes;
- old “Minimum Useful Canopy” terminology;
- earlier planned phase numbering.

These are retained because they explain **why** the present design exists.

### Phase 11–13 detail limitation

Current authoritative checkpoints establish that Phases 11–13 were completed.
The source material retrieved for this archive contains much more detail about their
pre-implementation contract than their entire later terminal transcript.

Accordingly, this archive:

- marks them complete;
- preserves the known contract/invariants;
- does **not** invent unobserved exact source lines.

If a future task requires an exact implementation detail from Phases 11–13, inspect the
live source or a dedicated later checkpoint before modifying behavior.



# 60. Resume Instruction

> **Phase 14.9 is complete. Resume Project Forest at Phase 14.10A. First inspect the existing reasoning controls exposed by Hermes and the runtime adapter; then define a canonical, runtime-neutral Quick / Normal / Deep model. Do not combine reasoning mode with Workshop selection or Small / Big model escalation. Preserve the rule that a meaningful turn decides once and runtime recovery reuses that already-decided mode.**



# 61. Final Development Doctrine

> **The Forest owns meaning. The adapter owns translation.**

> **Hermes is replaceable. Bristlecone remains Bristlecone even if the runtime underneath changes.**

```text
THE FOREST
    ↓
Forest runtime contract
    ↓
runtime adapter
    ↓
Hermes / llama.cpp / future runtime
    ↓
Ollama / native inference / future backend
```

> **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Cold stores truth. Warm decides relevance. Hot contains only relevant.**

> **Retain cheaply. Activate selectively. Share aggressively.**

> **The Forest gets deeper as you wonder.**

And for Bristlecone:

> **Pine is fine.**



# Appendix A — Source Context Retained Interface Skeleton

The following is intentionally a **condensed retained interface map**, not a replacement
for the real source files.

```python
# source_context/model.py
@dataclass(frozen=True, slots=True)
class SourceIdentity:
    source_id: str
    source_kind: str
    display_name: str
    locator: str | None = None

@dataclass(frozen=True, slots=True)
class SourceFingerprint:
    source: SourceIdentity
    method: str
    components: tuple[tuple[str, object], ...]

@dataclass(frozen=True, slots=True)
class SourceRegion:
    source: SourceIdentity
    fingerprint: SourceFingerprint
    region_id: str
    region_kind: str
    start_line: int | None
    end_line: int | None
    label: str | None = None
    parent_region_id: str | None = None

@dataclass(frozen=True, slots=True)
class SourceTarget:
    region: SourceRegion
    reason: str
```

```python
# observation.py
LOCAL_FILE_FINGERPRINT_METHOD = "stat-size-mtime-v1"

class LocalSourceObserver:
    def observe(self, ...):
        # resolve strict path
        # regular files only
        # stable source identity
        # fingerprint size + mtime_ns
        ...
```

```python
# snapshot.py
@dataclass(frozen=True, slots=True)
class SourceContentSnapshot:
    source: SourceIdentity
    fingerprint: SourceFingerprint
    text: str
    encoding: str
    content_sha256: str
    byte_count: int
    character_count: int
    line_count: int

class LocalSourceSnapshotReader:
    def read(self, path):
        # observe -> stat/open/fstat -> read -> verify -> strict decode
        ...
```

```python
# structure.py
PYTHON_STRUCTURE_KIND = "python-ast-v1"

@dataclass(frozen=True, slots=True)
class SourceStructure:
    fingerprint: SourceFingerprint
    structure_kind: str
    regions: tuple[SourceRegion, ...]

    def region_by_id(self, region_id):
        ...

class PythonSourceStructureBuilder:
    def build(self, snapshot):
        # ast.parse(snapshot.text)
        # objective lexical regions
        ...
```

```python
# targeting.py
class DeterministicSourceTargeter:
    def target_region_id(
        self,
        structure,
        region_id,
        *,
        reason="explicit structural region ID",
        required=True,
    ):
        ...

    def target_exact_label(
        self,
        structure,
        label,
        *,
        region_kind=None,
        reason="explicit unique structural label",
        required=True,
    ):
        ...
```

```python
# reference_matcher.py
class SourceReferenceMatcher:
    def match(self, structure, signals, *, required=True):
        # canonicalize
        # exact ID first
        # exact unique label second
        # explicit ambiguous/unmatched result
        ...
```

```python
# target_expansion.py
class BoundedSourceTargetExpander:
    def expand(
        self,
        structure,
        target,
        *,
        max_parent_hops=1,
        include_whole_source_parent=False,
    ):
        # ancestors only
        # no siblings/children
        ...
```

```python
# packet.py
class SourcePacketAssembler:
    def assemble(
        self,
        snapshot,
        expansions,
        *,
        max_characters,
        max_lines,
    ):
        # target bodies
        # ancestor breadcrumbs
        # overlap dedupe
        # hard fail-closed budgets
        ...
```

```python
# rendering.py
class DeterministicSourcePacketRenderer:
    def render(
        self,
        packet,
        *,
        max_rendered_characters,
        include_locator=False,
    ):
        # provenance
        # safe dynamic fence
        # path hidden by default
        # hard budget
        ...
```

```python
# turn_composition.py
class ForestTurnInstructionComposer:
    def compose(
        self,
        *,
        learning_instructions="",
        source_packets=(),
        max_characters,
    ):
        # exact no-source passthrough
        # Source Context attached as reference-data
        # dedupe packets
        # final hard budget
        ...
```



# Appendix B — Seasonal State and Spring Data Shapes

These examples combine retained/verified shapes from the seasonal implementation history.

```yaml
task_session:
  id: forest-task-...
  status: active

  lifecycle:
    season: spring
    previous_season: winter
    entered_at: ...

  task_sticky_skills:
    - debugging

  temporary_capabilities: []

  runtime_sessions:
    hermes:
      session_id: ...
      previous_session_id: ...
      updated_at: ...

  spring_cleaning:
    status: cleaning
    started_at: ...
    source_retired_at: ...

    activation_snapshot:
      workshop: code-debug
      general_capabilities:
        - todo
      ready_capabilities:
        - debugging
        - testing
      reasoning: deep
      model_form: big

    restoration_decision:
      decided_at: ...

      restore:
        workshop: code-debug
        general_capabilities:
          - todo
        ready_capabilities:
          - debugging
        temporary_capabilities: []

      leave_dormant:
        ready_capabilities:
          - testing
        temporary_capabilities:
          - testing
        reasoning: deep
        model_form: big

    restoration_application:
      status: verified
      applied_at: ...
      adapter: hermes
      workshop: code-debug
      general_capabilities:
        - todo
      ready_capabilities:
        - debugging
      temporary_capabilities: []
      canonical_active_ids:
        - file
        - terminal
        - todo
        - debugging
      runtime_toolsets:
        - file
        - terminal
        - todo
      runtime_skills:
        - systematic-debugging
      task_sticky_skills:
        - debugging
      skill_bindings:
        - canonical_id: debugging
          runtime_id: systematic-debugging
          adapter: hermes
```

Final completed Phase 11 later converts a verified Cleaning state into Summer only after
the completion contract is satisfied.



# Appendix C — Forest / Hermes Separation Cheat Sheet

```text
FOREST OWNS
-----------
Tree identity
Workshop meaning
canonical capabilities
canonical Skill IDs
Task identity
Task lifecycle
seasonal state
User Context
Operational Learning
Leaves / future Leaf Foliage
permissions / Spirit policy
source identity and source structure
turn-local source relevance
final semantic composition policy
durable state

RUNTIME ADAPTER OWNS
--------------------
runtime-specific capability translation
Hermes configurable toolset names
Hermes Skill implementation names
Hermes config transaction mechanics
Hermes profile secret scope
Hermes API request format
session create/get/send/end behavior
runtime verification
runtime rollback mechanics

NATIVE RUNTIME / INFERENCE OWNS
-------------------------------
model process
native KV cache
native prefix/prompt cache
inference execution state
session internals not explicitly exposed
Ollama/llama.cpp engine-specific implementation
```

The boundary exists so that:

```text
replace Hermes
or
replace Ollama
or
replace model
```

does **not** mean rebuilding Bristlecone's identity.
