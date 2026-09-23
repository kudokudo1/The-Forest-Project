# Bristlecone Pine / Project Forest — Complete Continuity Archive

**Archive date:** 2026-08-09  
**Primary system:** Bristlecone Pine / Project Forest  
**Current implementation checkpoint:** Controlled Spring restoration is real-runtime verified; Spring → Summer completion remains the next implementation step.  
**Preferred continuity use:** Obsidian / Markdown / future ChatGPT or Bristlecone development sessions.

---

# 0. How to Use This Archive

This file is intended to be a high-fidelity continuity packet for future work on Project Forest, Bristlecone Pine, Hermes integration, Qubes OS runtime layout, Workshop/capability architecture, Task Sessions, seasonal lifecycle, Spring Cleaning/restoration, runtime portability, and performance optimization.

Do **not** assume a planned item is implemented merely because it appears in this file. The checklist separates verified work from planned work.

## Status legend

- ✅ **Verified complete** — implemented and tested.
- 🧪 **Synthetic/fake-runtime verified** — implementation proven without touching live runtime.
- 🔬 **Real-runtime verified** — exercised against actual Bristlecone Hermes/runtime state.
- ⏳ **Next / pending**
- 💤 **Paused**
- 💡 **Future concept**
- ⚠️ **Important invariant / safety rule**

---

# 1. Project Identity and Doctrine

## Project Forest

**The Forest** is a local-first AI ecosystem and a subsystem of the larger Project Digital Cross / Project Digital Fortress ecosystem.

> **The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**

The metaphor should map to real technical behavior.

| Forest term | Real technical meaning |
|---|---|
| Tree | AI identity / agent / role |
| Workshop | capability/tool/Skill boundary |
| Leaves | knowledge artifacts / memory / references |
| Roots | sources, dependencies, relationships |
| Summer | active growth |
| Fall | shedding |
| Winter | dormant retained state |
| Spring | Cleaning / selective restoration |
| Pruning | meaningful restriction |
| Shedding | removing context/capabilities from active state |
| Growing | increasing useful knowledge, procedure, capability, or quality |
| Fruit | useful outputs / artifacts / results |
| Soil | permissions / execution environment / least-privilege base |
| Spirit | deterministic permission and action authority |

## Core UX doctrine

The design should satisfy four tests:

1. **Casual understanding**
2. **Technical truth**
3. **Metaphor integrity**
4. **Deeper as you wonder**

> **The Forest gets deeper as you wonder.**

Complexity should be discoverable, not prerequisite.

## Core Trees

### Cherry
Primary assistant Tree.

### Maple
Secondary assistant / developer / project / training / reviewer workspace.

### Cedar
Security Tree.

### Bristlecone Pine
**Role:** Treewright.

Responsibilities:
- design Trees
- code
- debug
- test
- evaluate models
- maintain Forest architecture
- correct other Trees
- help train Cherry / Maple / future Trees
- build plugins and add-ons

Health phrase:

> **Pine is fine.**

---

# 2. Qubes / Host Architecture

Primary environment:

- **OS:** Qubes OS
- **Desktop:** XFCE + i3
- **Terminal:** kitty
- **Shell:** zsh + oh-my-zsh
- **Prompt:** powerlevel10k
- **Launcher:** rofi
- **Wallpaper:** nitrogen
- **Compositor:** picom / GLX

## Important Qubes

### Cherry-AI
Primary AI qube. Contains Hermes, Ollama, Bristlecone runtime, and current Project Forest runtime work.

### Maple
Developer / project / training / reviewer qube.

### Seed-AI
Lighter training clone / future multi-model participant.

### dom0
Host control layer. Copy/paste and screenshot behavior is constrained, so commands intended for dom0 should be short and explained carefully.

## Performance modes / hotkeys

### Forest Normal Mode
Known approximate baseline:
- Cherry-AI mem 8192 MB
- Cherry-AI maxmem 16000 MB
- Cherry-AI 9 vCPUs
- Maple mem 800 MB
- Maple maxmem 8000 MB
- Maple 4 vCPUs

### Pine Cone Mode
- Hermes/Ollama active
- model unloaded until first use
- ~15 minute keepalive

### Maple Seed Mode
- frees runtime resources for Maple development/training

### Forest Mixed Mode
- mixed review/training

### Seed Mixed Mode target
- Maple 12288/16000 MB, 4 vCPUs
- Cherry-AI 6144/9000 MB, 3 vCPUs
- Seed-AI 2048/6000 MB, 2 vCPUs
- Cherry-AI should use a Cherry Seed reviewer, not Bristlecone

### Known i3 bindings
Num Lock OFF:
- Numpad 1 → Forest Normal
- Numpad 2 → Pine Cone
- Numpad 3 → Maple Seed
- Numpad 4 → Forest Mixed
- Numpad 5 → Seed Mixed planned/pending verification

---

# 3. Bristlecone Model / Hermes / Ollama Runtime

## Current model

Known Ollama model:

`bristlecone-qwen35:4b-64k`

Latest known local size reference: approximately **3.4 GB**. An older continuity packet referenced ~5.6 GB, so exact local size should be rechecked before capacity planning.

## Runtime stack

```text
Project Forest
    ↓
Hermes
    ↓
Ollama
    ↓
bristlecone-qwen35:4b-64k
```

## Network/service data

Hermes gateway:
- `127.0.0.1:8643`
- API base: `http://127.0.0.1:8643`

Ollama:
- `127.0.0.1:11434`

Hermes user service:
- `hermes-bristlecone.service`

Hermes gateway command conceptually:
- `hermes -p bristlecone gateway run`

Hermes restart restarts the gateway, not Ollama itself.

Model unload:
```bash
ollama stop bristlecone-qwen35:4b-64k
```

Keepalive:
- verified around 15 minutes
- persisted across Cherry-AI restart

---

# 4. Hermes Performance / Benchmark Data

## Minimal Hermes Workshop tests — reasoning none

| Tool set | Time |
|---|---:|
| file, terminal | ~41 sec |
| file, terminal, todo | 1:49.64 |
| file, terminal, skills | 2:42.40 |
| file, terminal, skills, todo | 2:49.16 |

Major lesson:

> **Tool/schema count strongly affects latency.**

## Minimal Workshop cold runs

| Workshop | Result |
|---|---|
| Design | ~2:52 |
| Code/Debug | ~3:12 first output; ~5:42 completion |
| Research | ~2:44 |
| Model | ~3:04 first output; ~11:49 completion |

Approximate cold first-output average:
- ~2:58

## Warm runs
- 30.58 sec
- 43.72 sec
- 2.23 sec
- total 1:16.54

Warm-state reuse clearly matters.

## Newelle stripped tests
- Run 1: 5:25.65 to output
- Run 2: ~15 minutes, no answer → fail
- Run 3: 5:42.23 welcome prompts only; no Bristlecone answer → fail

Decision:

> **Hermes is primary. Newelle is paused/optional.**

## Prompt/schema measurements

Post-trim Hermes CLI:
- system prompt ~20,994 bytes
- tool schemas ~31,532 bytes
- 14 tools

API final:
- system prompt ~16,864 bytes
- tool schemas ~28,188 bytes
- 12 tools

Earlier API:
- system prompt ~17,727 bytes
- tool schemas ~40,712 bytes
- 25 tools

This supports selective Workshop / capability loading.

---

# 5. High-Level Runtime Architecture

Three principal axes:

## Reasoning Mode
- Light
- Normal
- Deep

## Workshop
Capability / tool / Skill boundary.

## Model Form
- Small / Windowed
- Big / Fullscreen

Current optimization priority:

> Optimize Small/Windowed using Hermes + Ollama first.

Big/full model is a later escalation/reviewer path.

## Preferred architecture terms

> **Layered Reuse and Selective Rebuild**

> **Layered Hot Context**

### Cold
Tree exists on disk.

### Warm
Parsed manifests, mappings, indexes, caches are available in RAM but not necessarily model-visible.

### Hot
Current model-visible / execution-ready set:

```text
BASE TREE
+ Workshop Core
+ active General capabilities
+ active Ready capabilities
+ Task-Sticky Skills
+ temporary capabilities when permitted
+ relevant Leaves
+ current task
```

---

# 6. Workshop Architecture

Current Workshops:

1. Research
2. Design
3. Code / Debug
4. Model

## Research
Known Core:
- web

## Design
Known Core:
- memory
- clarify

Important discovery:

```text
memory
Forest canonical kind: context
Hermes runtime transport: toolset
```

This established the doctrine:

> **Canonical capability kind describes what something IS in the Forest. Runtime adapter mapping describes HOW a runtime exposes it.**

## Code / Debug

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

## Model
Known Core:
- file
- terminal

Ready:
- model-evaluation
- model-benchmarking
- model-inference
- quantization
- training
- runtime-inspection

## General Ready rack
- todo
- clarify
- session
- memory
- leaf

General Ready items are individually activated and may coexist with Workshop Ready.

---

# 7. Canonical Capability Registry

Path:

`~/The-Forest/bristlecone/capabilities/registry.yaml`

Known root keys:
- `schema_version`
- `tree`
- `capabilities`
- `general_ready`
- `policy`

Known capabilities:
- todo
- clarify
- session
- memory
- leaf
- web
- file
- terminal
- code-execution
- debugging
- testing
- special
- model-evaluation
- model-benchmarking
- model-inference
- quantization
- training
- runtime-inspection

Relevant canonical kinds:

```text
todo             → toolset
file             → toolset
terminal         → toolset
code-execution   → toolset

debugging        → skill
testing          → skill

memory           → context

special          → capability
```

Canonical kind is deliberately independent from runtime transport.

---

# 8. Hermes Capability Adapter Mapping

Path:

`~/The-Forest/bristlecone/adapters/hermes.yaml`

Current verified mapping:

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

Quick mapping reference:

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

---

# 9. Shared Forest Capability Resolver

Created:

`~/The-Forest/bristlecone/capabilities/resolver.py`

Purpose:

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

## Known Spring resolution

Input:

```text
Workshop: code-debug
General: todo
Ready: debugging
```

Canonical active IDs:

```text
file
terminal
todo
debugging
```

Hermes toolsets:

```text
file
terminal
todo
```

Hermes Skills:

```text
systematic-debugging
```

Binding:

```yaml
canonical_id: debugging
runtime_id: systematic-debugging
adapter: hermes
```

## Resolver tests passed

- Workshop Core automatic inclusion
- Spring canonical IDs
- Spring Hermes toolsets
- debugging Skill mapping
- canonical binding identity
- fully-resolved state
- testing → `test-driven-development`
- code-execution → `code_execution`
- invalid General rejected
- invalid Ready rejected
- `special` fails closed
- curated unresolved reason surfaced
- diagnostic unresolved mode
- Research Core resolves
- Design Core resolves
- Code/Debug Core resolves
- Model Core resolves

---

# 10. Resolver Design Correction — Canonical Kind vs Runtime Transport

The first resolver version incorrectly required non-Skill runtime toolsets to have canonical `kind: toolset`.

Design failed because:

```text
memory
canonical kind: context
Hermes mapping: toolset
```

The resolver was corrected.

Current doctrine:

> **Canonical Forest kind and runtime transport are separate axes.**

Future-compatible examples:

```text
Forest context → Hermes toolset
Forest context → future native context provider
Forest capability → future MCP tool
Forest skill → Hermes Skill
```

The canonical registry should never be distorted merely to fit one runtime.

---

# 11. Workshop Controller Refactor

Controller:

`~/The-Forest/bristlecone/bin/bristlecone-workshop.py`

Launcher:

`~/The-Forest/bristlecone/bin/bristlecone-workshop`

## Previous controller responsibilities
It duplicated:
- capability resolution
- Hermes mapping
- Hermes config mutation
- verification
- backup/rollback

## Current architecture

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

## Exact dry-run parity passed for
- code-debug + todo + debugging
- code-debug + testing
- code-debug + special unresolved
- invalid General selection
- invalid Workshop Ready selection
- Research Core
- Design Core
- Code/Debug Core
- Model Core

Result:

> Existing CLI behavior remained identical after resolver integration.

## Direct Hermes config manipulation removed

Controller no longer directly owns:
- `load_config`
- `save_config`
- `_save_platform_tools`
- `CONFIGURABLE_TOOLSETS`

Runtime mutation is delegated to runtime adapter.

---

# 12. Runtime Adapter Architecture

Directory:

`~/The-Forest/bristlecone/runtime/adapters/`

Known files:
```text
__init__.py
base.py
factory.py
hermes.py
```

## Actual base symbols
- `ABC`
- `BaseRuntimeAdapter`
- `RuntimeAdapterError`

Important correction:
- actual base class is **BaseRuntimeAdapter**
- not `RuntimeAdapter`

## Hermes class
- `HermesRuntimeAdapter`

Constructor:

```text
(profile_name='bristlecone',
 profile_home=None,
 repo=None,
 forest_root=None,
 api_base_url=None,
 api_timeout=30,
 turn_timeout=900)
```

## Runtime factory

File:
`runtime/adapters/factory.py`

Public function:

```python
create_runtime_adapter(state, forest_root=None)
```

Behavior:
1. reads `state.runtime`
2. requires `state.runtime.adapter`
3. currently supports `hermes`
4. gets Hermes profile from:
   - `state.runtime.profile`
   - `state.runtime.profile_name`
   - or `HERMES_HOME`
5. returns `HermesRuntimeAdapter`
6. fails closed for unknown runtime

This is the portability seam for future runtimes.

---

# 13. Base Runtime Adapter Contract

Known established methods:

- `verify_runtime`
- `get_active_toolsets`
- `begin_temporary_toolsets`
- `restore_temporary_toolsets`
- `apply_toolsets_exact`
- `restore_toolsets_exact`
- `build_skill_overlay`
- `create_session`
- `get_session`
- `send_turn`
- `end_session`
- `is_stale_session_error`

`RuntimeAdapterError` supports structured details such as:
- message
- optional status code
- optional error code
- optional method
- optional path

---

# 14. Temporary vs Exact Toolset Semantics

## Temporary activation

```python
begin_temporary_toolsets(...)
```

Semantics:

```text
desired = baseline + requested
```

Use:
- ephemeral/temporary overlay

It is additive.

## Exact activation

```python
apply_toolsets_exact(...)
```

Semantics:

```text
runtime configurable toolsets = desired exactly
```

Use:
- Workshop activation
- Spring restoration
- authoritative working-set changes

It is replacement, not additive.

## Exact rollback

```python
restore_toolsets_exact(...)
```

Restores the baseline captured by exact transaction.

---

# 15. Exact Toolset Contract Verification

Fake-runtime verification passed:

- Base exact apply abstract method
- Base exact restore abstract method
- Hermes adapter remained concrete
- exact transaction applied
- exact baseline captured
- exact desired set captured
- exact runtime membership
- non-additive semantics
- exact rollback
- restored marker
- same-set zero-write
- invalid toolset rejected
- invalid toolset zero-write
- verification failure rejected
- verification failure restored original bytes
- verification failure restored baseline runtime
- temporary activation still additive
- temporary rollback regression

No live Forest or Hermes state changed during that test.

---

# 16. Hermes Toolset Transaction Data

## Current real baseline from latest tests

```text
file
terminal
```

## Verified Spring target

```text
file
terminal
todo
```

## Real runtime sequence

```text
Before:
  file
  terminal

During Spring:
  file
  terminal
  todo

After restore:
  file
  terminal
```

## Exact live hashes from the real-runtime checkpoint

`active.yaml`:

```text
7904bc802fee0eadae5075c04f3df8359a0e44640da425fbdd62d28356dc9b60
```

Hermes `config.yaml`:

```text
436da2a229114b6848ddc76f959d54bcd63017f4f93eb015d7e323976274c30b
```

At the end of the controlled test:
- both hashes matched the original values
- `active.yaml` was byte-identical
- Hermes config was byte-identical

---

# 17. Hermes Temporary Transaction Behavior

## `get_active_toolsets`
Loads runtime config and reports current configurable toolsets.

## `begin_temporary_toolsets`
1. validate list
2. unique requested values
3. load Hermes runtime API
4. reject unknown/non-configurable toolsets
5. capture baseline
6. build `baseline + requested`
7. back up config
8. write
9. reload
10. verify desired set
11. return transaction
12. restore backup on failure

Known transaction fields:
```yaml
adapter:
platform:
baseline_toolsets:
requested_toolsets:
desired_toolsets:
backup_path:
applied:
restored:
```

## `restore_temporary_toolsets`
- validates transaction
- handles already-restored safely
- handles never-applied safely
- writes baseline
- verifies baseline
- uses backup fallback if needed

---

# 18. Exact Hermes Transaction Behavior

`apply_toolsets_exact` now:

1. validates list
2. unique desired set
3. checks configurable Hermes toolsets
4. captures baseline
5. returns zero-write transaction if baseline already equals desired
6. backs up config
7. writes exact desired set
8. reloads config
9. verifies exact saved set
10. marks applied
11. on failure:
   - restore backup
   - verify baseline
   - fail closed if rollback verification fails

`restore_toolsets_exact`:
- validates transaction type
- restores baseline
- verifies it
- has backup fallback
- marks transaction restored

---

# 19. Controller Transaction Safety Boundary

Current live controller order:

```text
resolve desired Forest working set
        ↓
resolve runtime adapter
        ↓
apply_toolsets_exact()
        ↓
get_active_toolsets()
        ↓
verify runtime truth
        ↓
update Forest working-state fields
        ↓
atomic-write active.yaml
```

If runtime activation succeeds but Forest state write fails:

```text
restore_toolsets_exact()
```

is invoked.

Fake live-path verification passed:
- success exact toolsets
- Workshop committed
- General committed
- Ready committed
- Task-Sticky Skill committed
- no rollback on success
- simulated Forest write failure triggered rollback
- runtime baseline restored
- failed state file unchanged

---

# 20. Task Session / State Architecture

Main file:

`~/The-Forest/bristlecone/runtime/task_session.py`

Active state:

`~/The-Forest/bristlecone/state/active.yaml`

Lock:

`.active.yaml.lock`

## State persistence

`persist_state(state)`:
1. requires mapping
2. validates Task Session
3. obtains exclusive write lock
4. atomic YAML write

## Lock implementation

Uses:
```python
fcntl.flock(..., LOCK_EX)
```

## Concurrency doctrine

For sensitive durable changes:
1. capture expected Task identity
2. acquire lock
3. reload latest state
4. revalidate Task ID / season / decision
5. rebuild using latest state
6. atomic write

---

# 21. Runtime Sessions — B3 / B4

Completed:

## B3
Persistent runtime binding.

## B3.1
Cross-process resume.

## B3.2
Crash-consistent pre-turn binding.

New runtime session binding is persisted before a long model call.

## B4.1
Gateway restart + history survival.

## B4.2 stale recovery

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
- no GET preflight required
- competing writer preserved
- non-stale errors unchanged
- durable replacement retained if retry later fails

Hermes session API:
- POST `/api/sessions`
- GET session
- POST chat
- DELETE session
- session rotation detection

Stale classifier only recognizes:
- status 404
- code `session_not_found`

---

# 22. Task-Sticky Skills

Task Session stores canonical IDs:

```yaml
task_sticky_skills:
  - debugging
```

`resolve_task_sticky_skills(state, task_session)`:

1. reads selected runtime adapter
2. loads registry
3. validates canonical capability
4. requires `kind: skill`
5. loads runtime Skill map
6. returns canonical/runtime binding

Example:

```text
debugging
    ↓
systematic-debugging
```

Skill overlay is constructed through runtime adapter:

```python
build_skill_overlay(...)
```

Spring does **not** convert Skills into configurable toolsets.

---

# 23. Seasonal Lifecycle Doctrine

Official language:

- 🌞 **Summer — Growing**
- 🍂 **Fall — Shedding**
- ❄️ **Winter — Dormant**
- 🌱 **Spring — Cleaning**

Important UI rule:

> **Cleaning must always be listed first in Spring UI/help/tooltips/docs.**

The seasonal model is a real control plane, not decoration.

Legacy normalization:
- active → Summer
- inactive → Winter

Task start:
- Summer

Task end:
- Winter

Generic active transitions:
- Summer
- Fall
- Spring

Winter uses `end_task()` rather than generic transition.

---

# 24. Durable Winter Storage

Directory:

`~/The-Forest/bristlecone/state/tasks/winter/`

One YAML record per dormant Task.

Known fields:
```yaml
schema_version: 1
record_type: forest_winter_task
tree:
task_id:
retired_at:
retired_order:
task_session:
activation_snapshot:
```

Winter Task preserves:
- Task ID
- dormant status
- Winter lifecycle
- previous season
- Task-Sticky Skills
- temporary capabilities
- runtime session bindings

Activation snapshot:
- Workshop
- active General
- active Ready
- reasoning
- model form

Loss-averse write order:

```text
1. write Winter record
2. clear active.yaml
```

Crash between steps may duplicate the Task, but does not lose it.

Crash simulation passed.

---

# 25. Winter Discovery

`list_winter_tasks()` is implemented.

Behavior:
- lightweight summaries only
- malformed-record isolation
- newest-first
- deterministic ordering using nanosecond `retired_order`
- human-readable `retired_at`
- legacy records without `retired_order` supported

---

# 26. Spring Wake / Cleaning Worksheet

Implemented:

```python
begin_spring_cleaning(task_id, state=None, persist=False)
```

Persistent safety order:

```text
write active Spring first
        ↓
delete Winter record second
```

If cleanup fails:
- durable Spring remains
- Winter copy may also remain
- wake is not undone

Spring wake:
- preserves runtime binding
- does not auto-restore old Workshop/Ready/reasoning/model
- creates durable Cleaning worksheet

Current Spring Cleaning structure:

```yaml
spring_cleaning:
  status: cleaning
  started_at:
  source_retired_at:
  activation_snapshot:
  restoration_decision:
  restoration_application:
```

`restoration_application` was added during the controlled-application phase.

At this archive checkpoint, `status: completed` and `completed_at` have **not yet been implemented** because the archive was requested before running the Spring→Summer completion patch.

---

# 27. Spring Selective Restoration Planner

Implemented:

```python
plan_spring_restoration(...)
```

Read-only.

## Keep
- Task identity
- runtime_sessions
- Task-Sticky Skills

## Already available
Previous resources that are already active now.

## Review
- previous Workshop when changed
- previous General not currently active
- previous Ready not currently active
- temporary capabilities always require revalidation

## Leave dormant
- historical reasoning if different
- historical model form if different

Important:

> Deep reasoning and Big model form must not auto-resurrect.

Planner outputs previous/current working sets, policy, and `applied: false`.

A duplicate planner definition was discovered later and removed. Exactly one planner remains.

---

# 28. Durable Spring Restoration Decision

Implemented:

```python
record_spring_restoration_decision(...)
```

This records **intent only**.

It explicitly returns:

```text
resources_activated: False
```

Decision shape:

```yaml
decided_at:

restore:
  workshop:
  general_capabilities:
  ready_capabilities:
  temporary_capabilities:

leave_dormant:
  workshop:
  general_capabilities:
  ready_capabilities:
  temporary_capabilities:
  reasoning:
  model_form:
```

Rules:
- active Spring Task required
- Cleaning worksheet required
- planner rebuilt against current/latest state
- only reviewed subsets may be restored
- unreviewed restoration rejected
- omitted candidates become dormant
- historical Deep/Big stay dormant
- preview is memory-only
- persistence uses lock and Task revalidation
- exact repeated decision is zero-write
- decision ≠ activation

---

# 29. Known Spring Decision Used for Testing

Historical environment before Winter:
- Workshop: code-debug
- General: todo
- Ready: debugging, testing
- reasoning: deep
- model form: big
- Task-Sticky debugging
- temporary testing

Spring choice:

## Restore
```yaml
workshop: code-debug
general_capabilities:
  - todo
ready_capabilities:
  - debugging
temporary_capabilities: []
```

## Leave dormant
```yaml
ready_capabilities:
  - testing
temporary_capabilities:
  - testing
reasoning: deep
model_form: big
```

Present wake/test environment:
- Workshop: research
- General: []
- Ready: []
- Reasoning: normal
- Model form: small

---

# 30. Controlled Spring Restoration

Implemented:

```python
apply_spring_restoration(state=None, persist=False)
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
- runtime rolls back when transaction exists
- Forest does not falsely claim activation

For the test decision:

## Forest target
- Workshop `code-debug`
- General `todo`
- Ready `debugging`

## Hermes exact toolsets
- file
- terminal
- todo

## Task-Sticky canonical Skill
- debugging

## Runtime Skill
- systematic-debugging

## Remains dormant
- testing Ready
- testing temporary
- Deep reasoning
- Big model form

## Temporary restore policy
Current controlled Spring application fails closed if a decision tries to restore temporary capabilities because that lifecycle/permission path has not yet been wired.

---

# 31. Spring Restoration Application Record

Durable field:

```yaml
spring_cleaning:
  restoration_application:
```

Normalized fields:

```yaml
status: verified
applied_at:
decision_decided_at:
adapter:
workshop:
general_capabilities:
ready_capabilities:
temporary_capabilities:
canonical_active_ids:
runtime_toolsets:
runtime_skills:
task_sticky_skills:
skill_bindings:
```

Only verified runtime reality should receive:

```yaml
status: verified
```

Core distinction:

```text
Past      = what existed before Winter
Decision  = what Spring approved
Reality   = what actually exists after verified application
```

---

# 32. Controlled Spring Application — Verification History

## Fake-runtime suite passed

- application method callable
- normalizer callable
- synthetic Spring Task valid
- application initially absent
- preview makes no runtime call
- preview does not activate
- correct target Workshop
- correct General
- correct Ready
- exact toolsets
- debugging Skill
- success reports activation
- exact runtime request
- exact runtime state
- no rollback on success
- Workshop committed
- General committed
- Ready committed
- debugging became Task-Sticky
- temporary testing remained dormant
- application verified
- toolsets recorded
- Skill recorded
- decision preserved
- Deep dormant
- Big dormant
- Task stayed Spring
- Cleaning stayed Cleaning
- restart persistence
- repeated application zero-write
- repeated changed false
- runtime mismatch rejected
- mismatch rollback invoked
- baseline restored
- mismatch state unchanged
- state-write failure rejected
- state-write rollback invoked
- failed write unchanged
- temporary restoration rejected
- temporary rejection made no runtime call

---

# 33. First Real Spring Runtime Test

This test used:
- real Hermes runtime
- temporary Forest active state

Real initial Hermes:

```text
file
terminal
```

Spring target:

```text
file
terminal
todo
```

Observed real runtime:

```text
file
terminal
todo
```

Real Skill overlay:

```text
Canonical Skills:
debugging

Runtime Skills:
systematic-debugging
```

Finally restored:

```text
file
terminal
```

Exactness:
- real `active.yaml` unchanged
- active state byte-identical
- active hash-identical
- Hermes config byte-identical
- Hermes config hash-identical

Result:

> **Spring integration: REAL-RUNTIME VERIFIED**

---

# 34. Live `active.yaml` Spring Rehearsal

This stronger test used:
- real Hermes runtime
- real `active.yaml`
- synthetic Spring Task temporarily installed
- emergency backups
- exact restoration afterward

Initial live state:
```text
Task status: inactive
Task ID: None
Season: winter
Hermes baseline: file + terminal
```

Emergency backup directory:

`/home/user/The-Forest/bristlecone/backups/live-spring-rehearsal/`

Specific known backups:
```text
active-before-live-spring-20260809T115355Z.yaml
config-before-live-spring-20260809T115355Z.yaml
```

During live Spring:
```text
Hermes: file + terminal + todo
Forest Workshop: code-debug
General: todo
Ready: debugging
Task-Sticky: debugging
Application: verified
```

Verified:
- temporary testing dormant
- Deep dormant
- Big dormant
- Spring remained Cleaning
- real canonical Skill overlay
- real runtime Skill overlay

Then:
- Hermes baseline restored
- original active.yaml restored
- active.yaml byte-identical
- active.yaml hash-identical
- Hermes config byte-identical
- Hermes config hash-identical
- final runtime baseline exact

Final result:

> **Live Spring controlled application: VERIFIED**

This is the current highest-confidence Spring application checkpoint.

---

# 35. Current Spring Completion Status

Next planned method:

```python
complete_spring_cleaning(...)
```

Purpose:

```text
verified restoration_application
        +
Forest state still matches application
        +
runtime toolsets still match application
        +
Skill resolution still matches
        ↓
mark Spring Cleaning completed
        ↓
Spring → Summer
```

Required properties:
- no runtime mutation during completion
- reverify runtime before Summer
- one locked atomic state write
- `spring_cleaning.status: completed`
- add `completed_at`
- lifecycle season → summer
- previous season → spring
- idempotent repeat
- runtime drift blocks Summer
- direct `transition_task_season("summer")` while Cleaning is blocked

## Current state
⏳ **NOT YET IMPLEMENTED / RUN**

A patch/test design was prepared, but this archive was requested before execution.

Do not mark complete without terminal verification.

---

# 36. Known Backups

## Seasonal foundation
`task-session-before-seasonal-lifecycle-20260809T091245Z.py`

## Winter storage
`task-session-before-winter-storage-20260809T091936Z.py`

## Winter discovery
`task-session-before-winter-discovery-v2-20260809T092241Z.py`

## Spring wake
`task-session-before-spring-cleaning-20260809T092653Z.py`

## Durable Spring Cleaning
`task-session-before-durable-spring-cleaning-v3-20260809T094104Z.py`

## Spring planner
`task-session-before-spring-restoration-plan-20260809T094250Z.py`

## Planner dedup
`task-session-before-planner-dedup-20260809T094725Z.py`

## Spring decisions
`task-session-before-spring-decisions-v2-20260809T094910Z.py`

## Resolver transport correction
`resolver-before-runtime-transport-fix-20260809T113258Z.py`

## Controller shared resolver
`bristlecone-workshop-before-shared-resolver-20260809T113018Z.py`  
`bristlecone-workshop-before-shared-resolver-v2-20260809T113448Z.py`

## Exact runtime contract
`base-before-exact-toolsets-20260809T113720Z.py`  
`hermes-before-exact-toolsets-20260809T113720Z.py`

## Controller runtime factory
`bristlecone-workshop-before-runtime-factory-20260809T114220Z.py`

## Controlled Spring application
`task-session-before-spring-application-20260809T114957Z.py`

## Live Spring rehearsal
`active-before-live-spring-20260809T115355Z.yaml`  
`config-before-live-spring-20260809T115355Z.yaml`

---

# 37. Layered Workshop / Skill Finder

Desired fallback:

```text
0. current Workshop Core
1. current Ready
2. Tree-owned tiny manifests
3. other Workshop manifests
4. Open Workbench — last resort
```

Important:

> Never load every Workshop merely to inspect them.

Goal:
- lower schema/prompt overhead
- preserve latency
- still allow capability discovery

---

# 38. Operational Learning

Operational learning should capture:

```text
task pattern
→ Workshop selected
→ Skills used
→ Skills unnecessary
→ fallback
→ outcome
```

Preferred storage:
- portable JSONL
- derived SQLite index

Operational learning is distinct from knowledge Leaves.

---

# 39. Leaf Foliage

High-priority architecture direction.

Principles:
- local-first
- offline-capable
- human-readable
- Obsidian-compatible where practical

Preferred Leaves:
- Markdown
- stable IDs
- metadata
- wiki/Markdown links

Derived:
- graph
- index
- backlinks
- retrieval structures

Do not load all Leaves into model context.

Desired Obsidian behavior:
- non-destructive attach/import
- ordinary Markdown export
- optional links/backlinks
- continued vault usability

Portability:
- “potted” selected knowledge
- copy to mobile/other devices
- no network required
- online sync completely optional

---

# 40. Runtime Portability Boundary

Forest owns:
- Tree identity
- Workshops
- canonical capabilities
- Skills
- Leaves
- permissions
- routing
- operational learning
- portable state
- Task Sessions
- seasonal lifecycle
- Layered Reuse and Selective Rebuild

Runtime adapter owns:
- runtime translation
- toolset mutation
- Skill overlay construction
- session API
- runtime verification
- rollback

Current:
- Hermes + Ollama

Potential future:
- llama.cpp
- other local runtimes
- MCP/native provider arrangements

---

# 41. Future Ollama → llama.cpp Evaluation

Reasons to evaluate:
- lower-level runtime control
- stable-prefix/KV-cache opportunities
- speculative decoding
- advanced performance tuning

Migration should **not** redesign the Forest.

It would require:
- new runtime adapter work
- benchmark reruns
- retuning
- possibly conversion/quantization

But Tree identity, Workshops, capability registry, Leaves, Task Sessions, Spirit, and operational learning should survive.

---

# 42. Reasoning / Model Form Future Work

## Reasoning
- Light
- Normal
- Deep

Desired:
- automatic temporary escalation based on complexity
- return to lower-cost mode afterward

Spring policy:
- historical Deep does not auto-return

## Model form
- Small / Windowed
- Big / Fullscreen

Spring policy:
- historical Big does not auto-return

Current priority:
- Small/Windowed optimization

---

# 43. Spirit

Core rule:

> **Trees decide what would be useful. Spirit decides what is allowed.**

Spirit should govern:
- permissions
- protected data
- action boundaries
- publication restrictions
- security restrictions
- least privilege
- consent boundaries

Trees may recommend capability escalation.
Spirit decides whether it is permitted.

---

# 44. Automatic Escalation Ladder

Desired:

```text
normal path
    ↓
better Workshop / Skill
    ↓
deeper reasoning
    ↓
tool
    ↓
relevant Leaves
    ↓
model escalation
    ↓
ask user only when necessary
```

Ask user mainly for:
- information
- permission
- judgment
- physical action

Do not interrupt for every internal routing decision.

---

# 45. Ownership Doctrine

Future ownership policy:

> **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**

Forest should eventually own durable:
- Tasks
- Leaves
- decisions
- outputs
- learning
- summaries
- artifacts
- reconstruction data

Runtime is a temporary working/execution layer.

---

# 46. Canonical Paths

Main root:

`/home/user/The-Forest/bristlecone`

Hermes profile:

`/home/user/.hermes/profiles/bristlecone`

Key directories:
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
backups/
```

Runtime files:
```text
runtime/__init__.py
runtime/task_session.py
runtime/adapters/__init__.py
runtime/adapters/base.py
runtime/adapters/hermes.py
runtime/adapters/factory.py
```

Capability files:
```text
capabilities/registry.yaml
capabilities/resolver.py
```

Hermes mapping:
```text
adapters/hermes.yaml
```

Workshop controller:
```text
bin/bristlecone-workshop.py
```

---

# 47. UPDATED COMPLETE IMPLEMENTATION CHECKLIST

## Phase 0 — Existing Hermes / Bristlecone runtime
- ✅ Hermes installed/configured
- ✅ Bristlecone Hermes profile
- ✅ Ollama runtime
- ✅ Bristlecone model available
- ✅ Hermes gateway autostart
- ✅ Ollama unload behavior
- ✅ ~15 minute keepalive
- ✅ Hermes primary interface
- 💤 Newelle paused / optional

## Phase 1 — Workshop / capability architecture
- ✅ four Workshops
- ✅ Research Core
- ✅ Design Core
- ✅ Code/Debug Core
- ✅ Model Core
- ✅ General Ready rack
- ✅ Workshop Ready racks
- ✅ canonical capability registry
- ✅ Hermes adapter mapping
- ✅ Task-Sticky Skill concept
- ✅ selective loading doctrine
- ✅ unresolved capabilities fail closed
- ✅ shared Forest capability resolver
- ✅ canonical-kind/runtime-transport separation
- ✅ Workshop Core automatic inclusion
- ✅ Skill/toolset separation

## Phase 2 — Runtime adapter foundation
- ✅ BaseRuntimeAdapter
- ✅ HermesRuntimeAdapter
- ✅ runtime adapter factory
- ✅ runtime verification
- ✅ toolset inspection
- ✅ temporary additive activation
- ✅ temporary rollback
- ✅ exact-set activation
- ✅ exact-set rollback
- ✅ same-set zero-write
- ✅ invalid toolset fail closed
- ✅ exact verification
- ✅ rollback verification
- ✅ fake-runtime exact-set tests
- ✅ temporary overlay regression

## Phase 3 — Workshop controller migration
- ✅ old behavior captured
- ✅ shared resolver integration
- ✅ exact dry-run parity
- ✅ Design `memory: context` parity bug found
- ✅ resolver corrected
- ✅ all four Workshop Core parity
- ✅ runtime factory integration
- ✅ direct Hermes config mutation removed
- ✅ exact-set adapter path
- ✅ runtime verification before Forest commit
- ✅ Forest-write-failure rollback
- ✅ fake live-path controller verification

## Phase 4 — Runtime sessions
- ✅ generic session contract
- ✅ Hermes persisted session API
- ✅ model routing bug fix
- ✅ real model execution
- ✅ Forest binding
- ✅ multi-turn continuity
- ✅ rotation mechanics
- ✅ B3 persistent binding
- ✅ generation/CAS safety
- ✅ B3.1 cross-process resume
- ✅ B3.2 crash-consistent pre-turn binding
- ✅ B4.1 gateway restart/history survival
- ✅ B4.2a stale signature capture
- ✅ B4.2b structured error + one-shot recovery
- ✅ B4.2c real stale-session recovery

## Phase 5 — Seasonal lifecycle foundation
- ✅ Summer/Fall/Winter/Spring normalization
- ✅ legacy active → Summer
- ✅ legacy inactive → Winter
- ✅ active transition validation
- ✅ Winter through end_task
- ✅ same-season zero-write
- ✅ lifecycle tests

## Phase 6 — Winter durability
- ✅ Winter Task storage
- ✅ one YAML per dormant Task
- ✅ activation snapshot
- ✅ runtime binding preserved
- ✅ loss-averse ordering
- ✅ crash simulation
- ✅ Winter discovery
- ✅ malformed-record isolation
- ✅ deterministic newest-first ordering
- ✅ retired_order nanoseconds
- ✅ legacy fallback

## Phase 7 — Spring wake / Cleaning
- ✅ Spring wake
- ✅ active-slot validation
- ✅ Spring-first / Winter-delete-second
- ✅ cleanup-failure duplicate-safe behavior
- ✅ runtime lineage preserved
- ✅ durable Cleaning worksheet
- ✅ activation snapshot survives restart

## Phase 8 — Spring planner
- ✅ selective restoration planner
- ✅ keep policy
- ✅ already-available policy
- ✅ review policy
- ✅ leave-dormant policy
- ✅ temporary review
- ✅ Deep auto-resurrection blocked
- ✅ Big auto-resurrection blocked
- ✅ planner read-only
- ✅ duplicate planner bug discovered
- ✅ duplicate removed
- ✅ single planner verified

## Phase 9 — Spring decision
- ✅ durable decision
- ✅ reviewed-subset enforcement
- ✅ unreviewed restore rejected
- ✅ omissions become dormant
- ✅ intent/reality separation
- ✅ preview no write
- ✅ persistent lock/revalidation
- ✅ repeated decision zero-write
- ✅ restart persistence
- ✅ `resources_activated: False`

## Phase 10 — Controlled Spring application
- ✅ durable `restoration_application`
- ✅ application normalizer
- ✅ decision → shared resolver
- ✅ exact runtime application
- ✅ runtime reality verification
- ✅ Forest commit after runtime verification
- ✅ Task-Sticky Skill restoration
- ✅ Skill validation
- ✅ temporary restore fails closed
- ✅ Deep stays dormant
- ✅ Big stays dormant
- ✅ Spring stays Cleaning after apply
- ✅ restart persistence
- ✅ idempotent application
- ✅ runtime mismatch rollback
- ✅ state-write failure rollback
- ✅ fake-runtime full suite
- 🔬 real Hermes runtime test
- 🔬 real Skill overlay
- 🔬 real active.yaml live rehearsal
- 🔬 exact Hermes restoration
- 🔬 exact Forest restoration
- 🔬 config byte-identical
- 🔬 active.yaml byte-identical
- ✅ **CONTROLLED SPRING APPLICATION COMPLETE**

## Phase 11 — Spring → Summer completion
- ⏳ add `spring_cleaning.status: completed`
- ⏳ add `completed_at`
- ⏳ implement `complete_spring_cleaning()`
- ⏳ require verified restoration application
- ⏳ require Forest state matches application
- ⏳ reverify runtime toolsets
- ⏳ reverify Skill mapping
- ⏳ block direct Spring → Summer bypass
- ⏳ atomic Cleaning-complete + Summer transition
- ⏳ idempotent repeat
- ⏳ runtime drift blocks completion
- ⏳ fake-runtime test
- ⏳ real Spring → Summer rehearsal
- ⏳ final live verification
- ⏳ mark seasonal Spring path complete

**Immediate next phase.**

## Phase 12 — Temporary capability restoration
- ⏳ define temporary restore semantics
- ⏳ Spirit/permission revalidation
- ⏳ runtime transaction behavior
- ⏳ expiration/removal semantics
- ⏳ application result recording
- ⏳ rollback

Current behavior: fail closed.

## Phase 13 — Runtime-independence audit
- ⏳ audit registry for runtime leakage
- ⏳ audit state fields such as `hermes_toolsets`
- ⏳ migrate `last_applied` toward runtime-neutral shape when appropriate
- ⏳ audit controller
- ⏳ audit Task Session runtime assumptions
- ⏳ audit Skill overlay
- ⏳ audit Hermes-only state names
- ⏳ confirm future llama.cpp adapter fit

## Phase 14 — Performance / Layered Hot Context
- ⏳ stable hot-prefix design
- ⏳ cache Workshop manifests
- ⏳ cache capability mappings
- ⏳ warm Skill manifests
- ⏳ source-context targeting
- ⏳ prompt/schema savings measurements
- ⏳ Quick/Deep automatic routing
- ⏳ model-form escalation
- ⏳ speculative decoding evaluation
- ⏳ Ollama vs llama.cpp benchmarks
- ⏳ KV/prefix-cache experiments

## Phase 15 — Leaf Foliage
- ⏳ stable Markdown Leaf schema
- ⏳ IDs/metadata
- ⏳ wiki links/backlinks
- ⏳ derived graph/index
- ⏳ selective retrieval
- ⏳ Obsidian attach/import
- ⏳ safe export
- ⏳ potted knowledge
- ⏳ optional sync
- ⏳ Forest-native `leaf` mapping

## Phase 16 — Operational learning
- ⏳ task-pattern capture
- ⏳ Workshop selection learning
- ⏳ Skill use/non-use
- ⏳ fallback logging
- ⏳ outcome logging
- ⏳ JSONL
- ⏳ derived SQLite
- ⏳ routing improvements

## Phase 17 — Spirit / permissions
- ⏳ deterministic permissions layer
- ⏳ protected data rules
- ⏳ action boundaries
- ⏳ security restrictions
- ⏳ publication restrictions
- ⏳ capability activation permissions
- ⏳ temporary-resource revalidation

## Phase 18 — Multi-model / future runtime
- ⏳ Cherry reviewer integration
- ⏳ Seed-AI role
- ⏳ Maple trainer/organizer
- ⏳ model escalation routing
- ⏳ Big-model reviewer
- ⏳ llama.cpp evaluation
- ⏳ quantization strategy
- ⏳ training architecture
- ⏳ self-improving harness

---

# 48. Immediate Next Steps

## Step 1 — Implement Spring completion
Implement:

```python
complete_spring_cleaning()
```

Required:

```text
verified application
+ Forest truth matches
+ runtime truth matches
+ Skill mapping matches
        ↓
completed Cleaning
        ↓
Summer
```

No runtime mutation.

## Step 2 — Fake-runtime completion suite
Test:
- no application → reject
- direct bypass → reject
- preview no runtime read/mutation
- normal completion
- `completed_at`
- Summer lifecycle
- Deep/Big dormant
- repeat zero-write
- runtime drift blocks Summer

## Step 3 — Real Spring → Summer rehearsal
Use:
- real Hermes
- real active.yaml
- durable backups
- exact byte restoration

## Step 4 — Mark seasonal Spring path complete
Only after terminal verification.

---

# 49. Safety Invariants

## Runtime truth before Forest truth
Never claim a resource active in Forest until runtime reality is verified.

```text
apply runtime
verify runtime
commit Forest
```

## Roll back runtime if Forest commit fails

## Decision is not reality
- `restoration_decision` = approved intent
- `restoration_application` = verified reality

## Deep/Big do not auto-resurrect

## Temporary capabilities fail closed until explicitly implemented

## Runtime-specific names remain adapter-owned

## Canonical kind ≠ runtime transport

Especially:
```text
memory = canonical context
Hermes = toolset transport
```

## No blind reruns after failure
Inspect exact source/state first.

## Back up before code mutation

---

# 50. Rejected / Paused Directions

- 💤 Newelle as primary Bristlecone path — paused due latency/instability
- ❌ load all Workshops to find capability
- ❌ Skill-as-base architecture
- ❌ duplicate resolver inside Spring
- ❌ TaskSessionManager directly manipulating Hermes config
- ❌ additive temporary toolsets for final Spring restoration
- ❌ changing `memory` canonical kind merely for Hermes
- ❌ auto-restoring Deep/Big after Winter

---

# 51. Future Concepts Worth Preserving

- Layered Reuse and Selective Rebuild
- Layered Hot Context
- stable-prefix / KV cache work
- source-context targeting
- deterministic capability routing
- Workshop/Skill Finder
- operational learning
- multi-model escalation
- runtime adapter portability
- Leaf Foliage graph
- potted knowledge
- Spirit permissions
- Tree identity above replaceable model
- optional Garden/device integration
- optional online sync
- speculative decoding
- local-first self-improving harness

---

# 52. Hermes Quick Reference

## Runtime
```text
Adapter: hermes
Gateway: 127.0.0.1:8643
Ollama: 127.0.0.1:11434
Profile: bristlecone
HERMES_HOME: ~/.hermes/profiles/bristlecone
Service: hermes-bristlecone.service
```

## Adapter class
`HermesRuntimeAdapter`

## Factory
```python
create_runtime_adapter(state, forest_root=None)
```

## Constructor
```text
(profile_name='bristlecone',
 profile_home=None,
 repo=None,
 forest_root=None,
 api_base_url=None,
 api_timeout=30,
 turn_timeout=900)
```

## Real configurable baseline
```text
file
terminal
```

## Verified Spring target
```text
file
terminal
todo
```

## Verified Spring Skill
```text
debugging → systematic-debugging
```

## Existing runtime methods
```python
get_active_toolsets(...)
apply_toolsets_exact(...)
restore_toolsets_exact(...)
begin_temporary_toolsets(...)
restore_temporary_toolsets(...)
build_skill_overlay(...)
```

## Real test exactness
```text
Before:
file + terminal

During Spring:
file + terminal + todo

After:
file + terminal
```

Both real Hermes config and real active.yaml returned byte-identical after rehearsal.

---

# 53. Current Highest-Confidence Statement

At this archive checkpoint:

> **Bristlecone’s controlled Spring restoration path is implemented and verified through the real Hermes runtime, the real Forest active-state file, the real Task-Sticky Skill resolution path, and exact rollback/restoration.**

The next uncompleted part is:

> **Spring Cleaning completion and Spring → Summer transition.**

Do not skip that distinction.

---

# 54. Resume Prompt for a Future Session

> We are continuing Bristlecone Pine / Project Forest runtime development. Read the latest continuity archive. Controlled Spring restoration is complete and real-runtime verified. The current real Hermes baseline is file+terminal. The verified Spring target used code-debug + todo + debugging, resolving to Hermes toolsets file+terminal+todo and Skill systematic-debugging. Spring remains Cleaning after application. The next implementation task is complete_spring_cleaning(): require a verified restoration_application, reverify Forest/runtime/Skill truth, atomically mark Cleaning completed and move Spring→Summer, block direct bypass, be idempotent, and make no runtime mutation. Preserve rollback, lock, canonical/runtime separation, and runtime-before-Forest truth invariants.

---

# 55. Final Development Doctrine

> **The Forest should feel simple because complexity is organized, not because complexity is hidden or discarded.**

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**

> **The Forest gets deeper as you wonder.**
