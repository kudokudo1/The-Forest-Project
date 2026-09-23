---
title: "The Forest — Bristlecone Pine Complete Engineering, Hermes Compatibility, and Phase 14.11 Master Checkpoint"
aliases:
  - "Bristlecone Complete Engineering Master Checkpoint"
  - "Forest Hermes Phase 14.11 Continuity Checkpoint"
project: "The Forest"
tree: "Bristlecone Pine"
role: "Treewright"
date: "2026-08-11"
status: "authoritative working continuity checkpoint"
current_phase: "14.11E4E3C2 — Frozen handoff transaction integration"
last_certified: "14.11E4E3C1 — CAS-aware runtime-binding rollback"
next_action: "Run the compact E4E3C2A pre-send recon to recover the exact ensured/persist_guard branch, then implement E4E3C2A without guessing."
tags:
  - forest
  - bristlecone
  - treewright
  - hermes
  - ollama
  - qubes
  - runtime
  - model-form
  - reasoning
  - workshops
  - clones
  - colony
  - task-session
  - session-identity
  - continuity
  - handoff
  - rollback
  - cache
  - hot-context
  - source-context
  - memory
  - resource-management
  - phase-14
---

# The Forest — Bristlecone Pine Complete Engineering, Hermes Compatibility, and Phase 14.11 Master Checkpoint

> [!important]
> **Purpose:** This is the largest working continuity checkpoint for the Bristlecone Pine / Forest engineering thread as of 2026-08-11. It consolidates architecture, implementation history, Hermes compatibility findings, Qubes constraints, performance benchmarks, completed code, failed attempts, certified rollback points, the Phase 14.11 roadmap, the current exact implementation boundary, and the detailed next steps.
>
> **Authority rule:** Later terminal-verified checkpoints override older files that still describe now-completed work as pending. Historical states are preserved here as history, not current truth.

> [!warning]
> **This is not source control.** The canonical source remains under:
>
> ```text
> /home/user/The-Forest/bristlecone
> ```
>
> `/home/user/The-Forest` is **not a Git repository**. Existing source must continue to receive timestamped backups before mutation.

---

# 0. Executive Resume Marker

If this file is used to resume work in a new chat, the immediate state is:

```text
PHASE 14 — PERFORMANCE / RUNTIME ARCHITECTURE

✅ 14.7  Layered Hot Context
✅ 14.8  Runtime Cache / Prefix Integration
✅ 14.9  Source-Context Targeting
✅ 14.10 Human Reasoning Control

PHASE 14.11 — SMALL / BIG MODEL ESCALATION

✅ 14.11A   Canonical Model Form Contract
✅ 14.11B   Model Form Control State / execution-context isolation
✅ 14.11C   Runtime-Neutral Model Registry
✅ 14.11D-0 Runtime Binding / Session Identity prerequisite
✅ 14.11D1  Effective Model Form Resolution + Freeze
✅ 14.11D2  Public Resolution API
✅ 14.11D3  TaskSession Resolution Integration
✅ 14.11D4A Self-contained Runtime Binding
✅ 14.11D4B Ephemeral Frozen Runtime View
✅ 14.11D4C1 Identity-aware Session Ensure
✅ 14.11D4C2 Identity-aware Persistence / CAS
✅ 14.11D4D1 Frozen Normal Send Path
✅ 14.11D5  Frozen Stale Recovery / Retry Freeze

✅ 14.11E1   Immutable ModelFormHandoff Contract
✅ 14.11E2   Pure Handoff Detection
✅ 14.11E3A  Frozen Instruction Continuity substrate
✅ 14.11E3B  Portable ConversationContinuity
✅ 14.11E3C  Combined ModelFormContinuity
✅ 14.11E4A  Canonical context-local state shape
✅ 14.11E4B  Effective-form read/write helpers
✅ 14.11E4C  Conversation read/write helpers
✅ 14.11E4D  Successful-turn commit integration
✅ 14.11E4E1 Pure handoff-continuity preparation
✅ 14.11E4E2 Runtime-neutral continuity-bootstrap contract
✅ 14.11E4E3A Typed instruction-composition passthrough
✅ 14.11E4E3B Handoff runtime bootstrap helper
✅ 14.11E4E3C1 CAS-aware runtime-binding rollback

→ 14.11E4E3C2 Frozen handoff transaction integration
□ 14.11E5     End-to-end handoff certification
□ 14.11F      Resource Request + Governor Contract
□ 14.11G      Automatic Escalation Router
□ 14.11H      Colony Runtime / Shared-Weight Semantics
□ 14.11I      Fake-Adapter Certification
□ 14.11J      Real Small Runtime Certification
□ 14.11K      Real Big Runtime Boundary Test
□ 14.11L      Model Form Benchmark

□ 14.12 Ollama vs llama.cpp evaluation
□ 14.13 Speculation & Speculative Decoding
□ 14.14 Final Performance Benchmark

THEN:
□ Phase 15 — Leaf Foliage
```

## Exact current boundary

**No E4E3C2 source mutation has been performed yet.**

A post-C1 landmark recon of the current frozen send method passed. A larger pre-send source recon also passed, but its numbered body did not reach the assistant. The next planned compact AST recon has **not yet been run**.

Therefore:

> **Do not patch E4E3C2A from memory or from the landmark list alone. Run the compact pre-send recon first so the exact `ensured`, `persist_guard`, and pre-turn branching are visible.**

The immediate intended split is:

```text
→ E4E3C2A
  Handoff preparation
  + initial fresh target-session bootstrap
  + pre-turn durable binding persistence

□ E4E3C2B
  continuity-aware stale recovery
  + semantic-commit rollback
  + safe runtime retirement
```

---

# 1. Forest North Star and Product Doctrine

## 1.1 North Star

> **The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**

The metaphor must map to actual technical behavior. It should not be decorative vocabulary pasted on top of ordinary agent architecture.

## 1.2 Signature / motto

Preserve unless explicitly changed:

> **IN God we trust in the forest we wonder.**

## 1.3 Ownership statement

> **Your Data. Your Trees. Your Forest.**

## 1.4 Bristlecone health phrase

> **Pine is fine.**

## 1.5 Core doctrine

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

> **The Forest gets deeper as you wonder.**

> **A Tree is not its model.**

> **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**

> **Big Form means more capable at being the same Tree, not a different identity.**

> **Retain cheaply. Activate selectively. Share aggressively.**

> **Compute follows active demand, not Tree ownership.**

> **Speculation must never become permission speculation.**

---

# 2. Forest Vocabulary and Technical Meaning

| Forest term | Technical meaning |
|---|---|
| Tree | AI identity / role / enduring Forest identity |
| Clone | Independently operating extension of a Tree |
| Colony | Base Tree plus all Clones |
| Workshop | Capability / tool / Skill boundary |
| Leaves | Durable human-readable knowledge |
| Roots | Provenance, dependencies, relationships |
| Soil | Least-privilege execution environment |
| Spirit | Deterministic permissions / action authority |
| Water | External information entering the Forest |
| Sunlight | User-originated information |
| Syrup | Inferred / distilled personalization |
| Mycelium | Permission-aware cross-Tree continuity |
| Cedar Oil | Encryption / security layer |
| Sap | Sensitive-handling classification |
| Tar Sap | Protected data not autonomously altered |
| Leaf Litter | Shed / colder lifecycle material |
| Pruning | Deliberate authorized shaping |
| Summer | Growing / active |
| Fall | Shedding |
| Winter | Dormant retained state |
| Spring | Cleaning / selective restoration |

## 2.1 Trees currently central to the architecture

### Cherry
Primary assistant/coordinator.

### Maple
Developer, organizer, semantic cartographer, knowledge steward, project/training/reviewer role.

### Cedar
Security Tree.

### Bristlecone Pine
The **Treewright**: designs, codes, tests, debugs, evaluates, maintains, and helps train Cherry, Maple, future Trees, plugins, and Forest add-ons.

### McIntosh
Future Tree concept: Software Engineer / Digital Technician.

### Sycamore
Exists in the broader Forest naming/design context, but is not central to the current Phase 14.11 implementation.

---

# 3. Tree Identity, Lineage, Clones, and Colony Semantics

## 3.1 Tree identity is not runtime identity

A Tree is enduring Forest identity. Model, runtime, quantization, context window, and session are replaceable implementation resources.

Conceptually:

```text
BRISTLECONE
    |
    +-- Small Form --> runtime/model binding A
    |
    +-- Big Form   --> runtime/model binding B
```

The Tree remains Bristlecone.

## 3.2 Lineage terminology

- **Ortet** — original execution context.
- **Ramet** — cloned execution context.
- **Genet / Colony** — contextual near-synonyms for the shared organism/Tree lineage, but do not duplicate separate `genet_id` and `colony_id` fields merely for flavor.

Important:

> **Main is an operational role. Ortet is a lineage role. Never encode `ortet == main`.**

## 3.3 Neutral internal IDs

Core code should use neutral technical identity fields such as:

```text
tree_id
execution_context_id
lineage_role
operational_role
```

Execution-context IDs should be opaque:

```text
ctx-0001
ctx-0002
```

Do not encode UI labels, model names, vendor names, Tree flavor, or Main/Clone semantics into technical IDs.

## 3.4 Clone lifetime and activation

Possible Clone lifetimes:

```text
ephemeral
persistent
project
```

Persistent Clone means durable lightweight state, **not** permanent compute.

Possible runtime states:

```text
dormant
warm
hot
```

## 3.5 What a Colony may share

Durable Tree/Colony state may include:

- identity;
- personality / purpose;
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

## 3.6 What remains execution-context local

Mutable live state includes:

- active Task/session/conversation;
- Hot Context;
- current Workshop;
- active Ready rack;
- temporary Skills/capabilities/files;
- current assumptions;
- runtime session;
- native KV/cache state;
- current Model Form;
- current Reasoning;
- temporary Reasoning/Form leases;
- Soil/environment;
- scratch state.

Core invariant:

> **Clones share durable Tree state, not unrestricted live context.**

Other retained rules:

> **Trees own capability. Clones carry only capability they need.**

> **Shared capability, separate activation.**

> **A Clone inherits identity, not automatically every active privilege.**

> **Capabilities normally shared. Scarce resources leased.**

> **Clone count must not scale infrastructure count.**

> **Resource cost should scale primarily with active work, not retained Clone count.**

---

# 4. Reasoning, Workshop, and Model Form Are Independent Axes

The three main control axes are:

```text
REASONING
Light / Normal / Deep

WORKSHOP
Research / Design / Code-Debug / Model / task-specific future Workshops

MODEL FORM
Small / Big
```

Valid examples:

```text
Small + Light
Small + Normal
Small + Deep

Big + Light
Big + Normal
Big + Deep
```

Core invariant:

> **Deep does not mean Big, and Big does not mean Deep.**

Reasoning controls **how deeply the selected model reasons**.

Model Form controls **which capability tier/model binding is selected**.

Workshop controls **which tools/Skills/capabilities are exposed**.

Resource pressure should not silently rewrite these semantic choices.

> **Resource pressure should affect scheduling/reclamation before silently altering a Clone's requested intelligence state.**

---

# 5. Qubes OS and Host Environment

## 5.1 Host and desktop

Known host environment:

```text
Qubes OS 4.3.1
XFCE + i3
kitty
zsh + oh-my-zsh
Powerlevel10k
rofi
picom / GLX
```

dom0 remains host/admin only.

Known dom0 home:

```text
/home/Mapple
```

(two p's).

## 5.2 Hardware

Known host hardware:

```text
CPU: Ryzen 7 3700X
Xen-visible CPUs / physical class: 8 cores visible in current environment
RAM: ~32 GB
GPU: RX 580-class
```

Do not assume a physical host device is available inside a qube merely because the host contains it.

## 5.3 Important qubes

### Cherry-AI
Primary AI/runtime development qube.

Recorded details:

```text
Fedora 42
root disk expanded: 20 GB -> 80 GB
qrexec_timeout: 600
CPU-only inference
no GPU currently exposed
Hermes operational
Ollama operational
Podman operational
```

Normal network path:

```text
Cherry-AI
  -> sys-firewall
  -> sys-net
  -> Internet
```

Do **not** connect Cherry-AI directly to `sys-net` merely for speed.

### Maple
Developer/project/training/reviewer qube.

### Seed-AI
Appears in future/training/mixed-mode design. Do not infer present existence solely from older plans unless terminal-verified in the current environment.

### Other retained qubes

```text
Sugar  -> gaming
Honey  -> work
Cedar  -> security/untrusted use depending on context
Pine   -> Whonix disposable/privacy role
dom0   -> host/control boundary
```

## 5.4 Security boundary

Do not casually weaken:

- qrexec;
- Qubes GUI services;
- firewall;
- required NetVM services;
- update mechanisms;
- device security;
- permission/approval boundaries.

Bristlecone inside Cherry-AI should not automatically:

- read Maple files;
- control Maple applications;
- inspect arbitrary qubes;
- administer dom0.

Future cross-qube operations should use narrow explicit channels such as:

```text
"Run tests in this repository."
"Return Git status."
"Copy this approved file."
"Return a limited diagnostic."
```

Prefer purpose-specific qrexec services over unrestricted cross-qube shells.

## 5.5 Work-state modes

### Forest Normal Mode

Historical verified allocation:

```text
Cherry-AI:
  memory = 8192 MB
  maxmem = 16000 MB
  vcpus  = 9

Maple:
  memory = 800 MB
  maxmem = 8000 MB
  vcpus  = 4
```

### Pine Cone Mode

- Hermes/Ollama active/available.
- Model can stay unloaded until first use.
- ~15-minute keepalive verified.

### Maple Seed Mode

Frees resources for Maple development/training.

### Forest Mixed Mode

Mixed review/training use.

### Seed Mixed target

Historical target:

```text
Maple:
  12288 / 16000 MB
  4 vCPU

Cherry-AI:
  6144 / 9000 MB
  3 vCPU

Seed-AI:
  2048 / 6000 MB
  2 vCPU
```

Cherry-AI should use a more-developed Cherry Seed reviewer in that mode, not Bristlecone.

### i3 bindings

With Num Lock OFF:

```text
Numpad 1 -> Forest Normal
Numpad 2 -> Pine Cone
Numpad 3 -> Maple Seed
Numpad 4 -> Forest Mixed
Numpad 5 -> Seed Mixed target / pending verification
```

---

# 6. Current Bristlecone Runtime Stack

Current Small stack:

```text
The Forest
    ↓
Hermes
    ↓
Ollama
    ↓
bristlecone-qwen35:4b-64k
```

Known service/runtime locations:

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

`OLLAMA_KEEP_ALIVE` / effective keepalive of about 15 minutes was verified and persisted across a Cherry-AI restart.

## 6.1 Current Small model

```text
bristlecone-qwen35:4b-64k
Qwen3.5-4B
64K context
CPU-only
Hermes + Ollama
```

Historical observations differ on storage/runtime footprint:

```text
~5.6 GB runtime observation at one checkpoint
~3.4 GB model-file observation in another archive
```

Recheck live values for capacity planning rather than treating either as immutable.

## 6.2 Model-origin preference

Future core model selection should prefer **non-Chinese-developed models and core technology when practical**.

Current decision:

```text
DO NOT replace Qwen yet.
```

Sequence:

```text
finish architecture/setup
      ↓
benchmark current Qwen Small
      ↓
select non-Chinese Small candidate
      ↓
replace cleanly
      ↓
run same benchmark suite
      ↓
compare objectively
```

The current Qwen remains the baseline/control until measured.

---

# 7. Hermes — Why It Became the Primary Orchestration Layer

Hermes is the preferred primary Bristlecone/Forest orchestration layer because it provides or supports:

- agent behavior;
- tool use;
- learning-oriented features;
- multi-model potential;
- Skills;
- persisted sessions;
- routing potential;
- CLI;
- gateway API;
- runtime profile isolation;
- a clear adapter boundary;
- long-term Forest integration.

Current decision:

> **Hermes remains primary. Newelle is optional/paused.**

---

# 8. Newelle Findings and Why It Was Paused

Newelle was tested as a Bristlecone interface and remained slow/unreliable even after duplicate prompts/tools were reduced.

Confirmed stripped runs:

```text
Run 1: 5:25.65 before useful output
Run 2: ~15 minutes with no answer -> FAIL
Run 3: ~5:42.23 welcome/suggestion prompts but no Bristlecone answer -> FAIL
```

Duplicate Newelle functions were disabled during optimization, including overlapping:

- agent behavior;
- file operations;
- RAG;
- website reading;
- search;
- command execution;
- image generation.

TTS was retained in some earlier user-facing setup context, though broader later Forest design treats speech as optional/toggleable.

Decision:

> **Newelle should not be placed back into the daily critical path unless deliberately reactivated and revalidated.**

---

# 9. Hermes Compatibility Findings — Detailed

This section is critical for future runtime work.

## 9.1 Hermes runtime operations require `api_server`

Forest/Hermes runtime operations were verified to require:

```yaml
runtime:
  adapter: hermes
  platform: api_server
```

The adapter/controller should fail closed if:

```text
runtime platform != "api_server"
```

This was important during 14.11D4A, when Model Form runtime binding had to become self-contained.

## 9.2 `HERMES_HOME` profile correctness

Hermes runtime work requires `HERMES_HOME` to be set and resolve exactly to the intended profile:

```text
~/.hermes/profiles/bristlecone
```

Wrong or missing profile must fail closed.

## 9.3 Hermes configuration helpers

The adapter has historically used Hermes-side helpers including:

```python
from hermes_cli.config import (
    load_config,
    save_config,
)

from hermes_cli.tools_config import (
    _save_platform_tools,
    CONFIGURABLE_TOOLSETS,
)
```

These are runtime-specific and belong behind the Hermes adapter rather than in generic Forest core.

## 9.4 Configurable Hermes toolsets discovered

Verified/discovered configurable toolsets include:

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

## 9.5 Canonical Forest meaning vs Hermes transport

One of the most important compatibility corrections:

```text
Forest canonical kind
        !=
Hermes transport mechanism
```

Example:

```text
Forest:
  memory = context

Hermes:
  memory = configurable toolset transport
```

Canonical doctrine:

> **Canonical capability kind describes what something IS in the Forest. Runtime mapping describes HOW a runtime exposes it.**

Never distort Forest semantics merely to satisfy Hermes.

## 9.6 Verified Hermes adapter mapping

Path:

```text
~/The-Forest/bristlecone/adapters/hermes.yaml
```

Representative verified mapping:

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
file             -> file
terminal         -> terminal
todo             -> todo
clarify          -> clarify
session          -> session_search
memory           -> memory
web              -> web
code-execution   -> code_execution

debugging        -> systematic-debugging
testing          -> test-driven-development
model-evaluation -> evaluation
model-inference  -> inference
```

## 9.7 Skill-as-base prompt experiment — rejected

Known Skill overlay sizes:

```text
systematic-debugging:    14,510 characters
test-driven-development: 10,753 characters
```

An attempt to make a Skill function as the persistent/base system prompt did not behave as intended because Hermes restored its own base semantics.

Historical timings from that failed direction:

```text
Turn 1:
  326.1 s
  input 5287
  output 491
  total 5778

Turn 2:
  191.3 s
  input 5610
  output 462
  total 6072
```

Retained direction:

```text
Forest canonical Skill
        ↓
runtime adapter
        ↓
build runtime-specific Skill overlay
        ↓
ephemeral instruction/system overlay
        ↓
reuse while Task remains relevant
```

Key lesson:

> **Cached in RAM ≠ visible to the model.**

and:

> **Forest owns semantic stickiness. Hermes owns execution. The adapter bridges the two.**

## 9.8 Hermes temporary toolset transaction

Retained transaction shape:

```text
validate request
    ↓
capture exact baseline
    ↓
desired = baseline + requested
    ↓
backup Hermes config
    ↓
apply
    ↓
reload
    ↓
verify
    ↓
use
    ↓
finally restore exact baseline
```

On failure, restore from backup.

Forest durable state stays untouched by this temporary runtime transaction.

Historical real example:

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

## 9.9 Runtime adapter portability seam

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

Core class:

```python
BaseRuntimeAdapter
```

Error:

```python
RuntimeAdapterError
```

Historical retained contract included:

```text
verify_runtime
get_active_toolsets
begin_temporary_toolsets
restore_temporary_toolsets
apply_toolsets_exact
restore_toolsets_exact
build_skill_overlay
create_session
get_session
send_turn
end_session
is_stale_session_error
```

Factory:

```python
create_runtime_adapter(state, forest_root=None)
```

This factory is the portability seam for a future llama.cpp or other backend.

## 9.10 Hermes persisted session API findings

Discovered endpoints:

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

Hermes can rotate session IDs, including during compression.

Forest therefore must not equate:

```text
Forest Task ID
```

with:

```text
Hermes session ID
```

## 9.11 Hermes API secret scope

Gateway authentication uses:

```text
API_SERVER_KEY
```

Important discovery: the key should be resolved in Hermes profile-scoped secret context, not copied out of the gateway process environment.

Known profile-secret machinery included:

```text
build_profile_secret_scope
set_secret_scope
reset_secret_scope
current_secret_scope
get_secret
gateway.run._profile_runtime_scope
```

Security invariant:

> **Never store, print, copy, log, or persist `API_SERVER_KEY` into Forest canonical state, Leaves, or debugging output.**

## 9.12 Critical current Hermes compatibility gap for Model Form handoff

During E4E2, the base runtime contract gained an optional, non-abstract method:

```python
create_session_with_continuity(
    self,
    state,
    continuity,
    task_id=None,
)
```

Default behavior:

```python
raise RuntimeContinuityUnsupportedError(...)
```

Hermes remains a concrete adapter because the method is **not abstract**.

However:

> **Hermes currently inherits the fail-closed default. Hermes continuity bootstrap is not yet implemented.**

This is deliberate and important.

It means:

- Forest handoff architecture can be certified with fake adapters now;
- same-form Hermes runtime remains compatible;
- real Small↔Big continuity handoff cannot be declared Hermes-capable until the Hermes adapter implements or otherwise supports continuity bootstrap;
- this must be addressed before real 14.11K Big boundary work.

This is a compatibility gap, **not** a reason to couple Forest continuity to Hermes internals.

---

# 10. Performance Investigation — Master Benchmark History

These measurements span different dates/configurations. They are engineering history, not a claim that every row is directly comparable.

| Area | Measurement | Result |
|---|---|---:|
| Hermes minimal | `file,terminal` | ~41 s |
| Hermes minimal | `file,terminal,todo` | 1:49.64 |
| Hermes minimal | `file,terminal,skills` | 2:42.40 |
| Hermes minimal | `file,terminal,skills,todo` | 2:49.16 |
| Workshop cold | Research TTFT | ~2:44 |
| Workshop cold | Design TTFT | ~2:52 |
| Workshop cold | Code/Debug TTFT | ~3:12 |
| Workshop cold | Code/Debug completion | ~5:42 |
| Workshop cold | Model TTFT | ~3:04 |
| Workshop cold | Model completion | ~11:49 |
| Newelle | stripped run 1 | 5:25.65 |
| Newelle | stripped run 2 | ~15m fail |
| Newelle | stripped run 3 | ~5:42.23 no Bristlecone answer |
| Raw Ollama | tiny cold total | 10.68 s |
| Raw Ollama | tiny warm total | 1.40 s |
| Raw Ollama | cold TTFT | 9.74 s |
| Raw Ollama | warm TTFT | 0.99 s |
| Raw Ollama | long generation | 2.44 tok/s |
| Raw large prefill | 5,915 prompt tokens | 130.91 s prompt evaluation |
| Raw large prefill | prompt speed | 45.18 tok/s |
| Raw large prefill | TTFT | 131.48 s |
| Raw large prefill | model load | 0.48 s |
| Raw large prefill | generation | 0.47 s |
| Hermes Normal | 12,341-token first prefix | 5m42.793 |
| Hermes Normal | immediate repeated prefix | 27.782 s |
| Hermes Normal | genuine cold | 4m52.349 |
| Phase 14.2 | warm run | 158.82 s |
| Phase 14.2 | warm run | 189.47 s |
| Phase 14.2 | best warm | 63.75 s |
| Phase 14.7 | Hot assembler p50 | 7.77 µs |
| Phase 14.7 | Hot assembler p95 | 11.28 µs |
| Phase 14.7 | full sticky compose p50 | 24.54 µs |
| Phase 14.7 | full sticky compose p95 | 36.28 µs |
| Phase 14.7 | provider warm p50 | 50.69 µs |
| Phase 14.7 | provider warm p95 | 77.62 µs |
| Phase 14.7 | provider cold p50 | 2.373 ms |
| Phase 14.7 | provider cold p95 | 2.525 ms |
| Phase 14.7 | 1 Clone shared-cold wall | 2.65 ms |
| Phase 14.7 | 10 Clone shared-cold wall | 9.34 ms |
| Phase 14.7 | 50 Clone shared-cold wall | 17.72 ms |
| Phase 14.9 | warm source turn p50 | 65.95 µs |
| Phase 14.9 | warm source turn p95 | 100.37 µs |
| Phase 14.9 | cold source path p50 | 0.301 ms |
| Phase 14.9 | no-source composition p50 | 1.52 µs |
| Phase 14.9 | 10 callers p50 | 1.954 ms |
| Phase 14.9 | 50 callers p50 | 7.030 ms |
| Phase 14.10 | real Light turn | ~147.11 s |

## 10.1 Main performance conclusions

### Tool/schema count matters

Early minimal Hermes tests showed large latency increases as `todo` and especially `skills` were exposed.

This became a major reason for Workshop-based selective capability exposure.

### Large CPU prompt prefill matters

The raw prefill test showed:

```text
model load: ~0.48 s
prompt evaluation: ~130.91 s
```

Therefore:

> **A warm model can still have multi-minute TTFT when CPU prompt prefill is large.**

### Static prompt trimming helped but did not solve everything

Prompt/schema history:

#### Earlier API

```text
system prompt: 17,727 B
tool schemas:  40,712 B
tools:         25
```

#### Trimmed API

```text
system prompt: 16,864 B
tool schemas:  28,188 B
tools:         12
```

#### Trimmed CLI

```text
system prompt: 20,994 B
tool schemas:  31,532 B
tools:         14
```

Cron was intentionally retained later, making visible count approximately 15 in one configuration.

#### Phase 14.1 baseline

```text
system prompt:  9,832 B
tool schemas:  11,159 B
combined:      20,991 B
tools:              6
```

Even after large static reduction, warm turns still varied from ~64 to ~189 seconds.

### Forest bookkeeping is now cheap relative to model/runtime latency

By Phase 14.7 and 14.9, deterministic Forest routing/cache/Source Context work was measured in microseconds to low milliseconds.

Core conclusion:

> **Forest-side deterministic routing, caching, and Source Context are now very cheap relative to the historical multi-second/minute Hermes/model path.**

Do not optimize microsecond Forest machinery as a substitute for fixing measured runtime/model bottlenecks.

---

# 11. Workshop and Capability Architecture

## 11.1 Four foundational Workshops

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

Representative retained definition:

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

`minimum_useful_canopy` is historical terminology. Broader current architecture prefers:

```text
Layered Reuse and Selective Rebuild
Layered Hot Context
```

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

## 11.2 General Ready rack

```text
todo
clarify
session
memory
leaf
```

Ready means addressable and cheap to discover, **not model-visible by default**.

## 11.3 Capability states

Current conceptual states:

```text
Dormant
Active
Task-Sticky
Core
```

### Core
Automatically available for current Workshop.

### Active
Temporary need for immediate turn/task.

### Task-Sticky
Retained across related turns inside one Forest Task.

### Dormant
Known but not currently exposed.

## 11.4 Canonical registry

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
todo           -> toolset
file           -> toolset
terminal       -> toolset
code-execution -> toolset

debugging      -> skill
testing        -> skill

memory         -> context

special        -> capability
```

## 11.5 Shared resolver

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

Verified examples included:

- Workshop Core auto-inclusion;
- canonical IDs;
- runtime toolsets;
- Skill bindings;
- `testing -> test-driven-development`;
- `code-execution -> code_execution`;
- invalid General fail closed;
- invalid Ready fail closed;
- unresolved `special` fail closed;
- curated unresolved reason surfaced;
- all four Workshop cores resolve.

---

# 12. Forest Task Sessions

A user conversation and a Forest Task are not the same thing.

Conceptually:

```text
USER CONVERSATION
        |
        +-- Forest Task A: Design
        +-- Forest Task B: Code / Debug
        +-- Forest Task C: Research
```

A Task can own:

```text
Reasoning Mode
Model Form
Workshop
Workshop Core
Task-Sticky Skills
temporary General overlays
temporary Ready overlays
Hot Context
task-specific state
runtime-session bindings
```

Representative state:

```yaml
task_session:
  id: forest-task-...
  status: active
  started_at: ...
  updated_at: ...

  task_sticky_skills:
    - debugging

  temporary_capabilities: []

  runtime_sessions: {}
```

Forest Task IDs historically used:

```text
forest-task-<UTC>-<8 hex>
```

Central manager:

```text
runtime/task_session.py
```

Known constructor:

```python
TaskSessionManager(
    forest_root=None,
    runtime_adapter=None,
)
```

Important behavior:

```python
result = manager.start_task(
    state=working,
    persist=False,
)

runtime_state = result["state"]
task_session = result["task_session"]
```

`start_task()` returns a new state object rather than mutating the passed state in place.

---

# 13. Atomic Persistence and Concurrency Doctrine

Forest persistence evolved toward:

```text
validate
  ↓
acquire lock
  ↓
reload latest durable state
  ↓
revalidate Task / generation / state
  ↓
write temp file
  ↓
serialize
  ↓
flush + fsync
  ↓
os.replace
```

Locking uses:

```python
fcntl.flock(..., LOCK_EX)
```

Active state:

```text
state/active.yaml
```

Lock:

```text
.active.yaml.lock
```

Concurrency doctrine:

> **Capture expected generation, then re-check latest durable truth under the lock before mutating.**

For sensitive writes:

```text
capture expected Task/session/form generation
      ↓
runtime or other work
      ↓
acquire lock
      ↓
reload latest
      ↓
compare expected vs latest
      ↓
commit only if safe
```

This doctrine now underlies runtime-session CAS, Model Form semantic commit CAS, and rollback CAS.

---

# 14. Phases 0–13 — Implementation History

## Phase 0 — Existing Hermes / Bristlecone runtime

Baseline local Hermes + Ollama environment existed before Forest abstraction work.

## Phase 1 — Workshop / capability architecture

Established:

- Workshops;
- canonical capability IDs;
- capability registry;
- General Ready / Workshop Ready;
- Task-Sticky concept;
- Hermes mapping;
- Skill overlay behavior;
- fail-closed unresolved capabilities.

Rejected:

```text
Skill as permanent/base system prompt
```

Retained:

```text
Skill as runtime-specific ephemeral instruction overlay
```

## Phase 2 — Runtime adapter foundation

Decision:

> **The Forest owns meaning. The adapter owns translation. Hermes is replaceable.**

Created runtime abstraction package and adapter factory.

## Phase 3 — Workshop controller migration

Controller:

```text
bin/bristlecone-workshop.py
```

Launcher:

```text
bin/bristlecone-workshop
```

Before refactor, controller duplicated Hermes-specific mapping/config mutation.

After refactor:

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
verify runtime
    ↓
Forest state commit
```

Direct private Hermes config mutation was removed from controller.

Runtime-before-Forest transaction principle:

```text
apply runtime
  ↓
verify runtime truth
  ↓
commit Forest state
```

If Forest state write fails after runtime mutation:

```text
restore runtime
```

## Phase 4 — Runtime sessions

Major rule:

```text
Forest Task ID = stable canonical identity
Hermes session ID = mutable runtime pointer
```

B3/B4 milestones completed:

- persistent binding;
- cross-process resume;
- crash-consistent pre-turn binding;
- gateway restart/history survival;
- stale-session recovery.

Crash-consistent rule:

> **Persist a newly created runtime session binding before entering a long model call.**

Verified stale recovery:

```text
send existing session
    ↓
404 / session_not_found
    ↓
create one replacement
    ↓
current = new
previous = old
    ↓
guarded persistence
    ↓
retry once
```

No GET preflight was required.

## Phase 5 — Seasonal lifecycle foundation

Canonical seasons:

```text
Summer — Growing
Fall   — Shedding
Winter — Dormant
Spring — Cleaning
```

These are control-plane states, not decorative names.

## Phase 6 — Winter durability

Directory:

```text
state/tasks/winter/
```

Loss-averse retirement:

```text
1. write Winter record
2. clear active.yaml
```

If interrupted, duplication is preferable to loss.

## Phase 7 — Spring wake / Cleaning

API:

```python
begin_spring_cleaning(...)
```

Persistent order:

```text
write active Spring first
delete Winter second
```

Spring does not blindly resurrect old active resources.

## Phase 8 — Spring restoration planner

API:

```python
plan_spring_restoration(...)
```

Automatically preserve:

```text
Task identity
runtime_sessions
Task-Sticky Skills
```

Review old Workshop/General/Ready/temporary resources.

Critical rule:

> **Deep reasoning and Big Model Form never auto-resurrect from historical state.**

## Phase 9 — Durable Spring restoration decision

API:

```python
record_spring_restoration_decision(...)
```

This stores approved intent, not runtime reality.

Canonical distinction:

> **Decision ≠ Reality.**

## Phase 10 — Controlled Spring application

API:

```python
apply_spring_restoration(...)
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
record application
      ↓
atomic Forest write
```

Real Hermes verification passed.

This established:

> **Runtime truth before Forest truth.**

and:

> **If Forest commit fails after runtime mutation, roll runtime back.**

## Phase 11 — Spring → Summer completion

Completion requires verified application and continued runtime/state agreement before marking Cleaning complete and transitioning to Summer.

## Phase 12 — Temporary capability restoration

Rules include:

- temporary approval != persistent activation;
- temporary Skills remain non-Sticky unless separately approved;
- unresolved temporary capability fails before runtime mutation;
- temporary runtime additions restore afterward;
- temporary resources require permission revalidation.

## Phase 13 — Runtime-independence audit

Consolidated boundaries:

> **Runtime-specific names belong in adapters.**

> **Portable persistent fields remain runtime-neutral.**

> **Controllers use configured adapters explicitly. No silent Hermes default.**

> **Forest Task identity, Workshops, permissions, learning, Leaves, and lifecycle must survive replacement of Hermes/Ollama.**

---

# 15. Phase 14.1–14.4 — Baselines and Hot-Path Audit

## 14.1 — Prompt/schema baseline

Verified:

```text
System prompt:  9,832 B
Tool schemas:  11,159 B
Combined:      20,991 B
Tools:              6
```

## 14.2 — Cold/warm latency baseline

Warm tests:

```text
158.82 s
189.47 s
63.75 s
```

Static prompt size/model residency alone did not explain variance.

## 14.3 — Repeated-work map

YAML parsing and capability resolution were mainly management-path work.

Decision:

```text
Do not optimize manifest/resolver caching as a fake fix
for multi-minute runtime latency without evidence.
```

## 14.4 — Hot-turn path audit

Benchmark path was effectively:

```text
create_session()
    ↓
send_turn()
    ↓
POST /api/sessions/<id>/chat
    ↓
wait for runtime/model
```

Dominant delay was below most Forest Python bookkeeping.

---

# 16. Phase 14.5 — Forest Cache Architecture

Core principle:

> **Caches are derived. They are never authoritative Forest truth.**

Rules:

- deleting cache causes rebuild, not knowledge loss;
- entries carry schema/version identity;
- cache identity is technical, not display-label based;
- invalidation follows dependencies;
- avoid duplicate caches of same representation;
- runtime/model changes do not automatically invalidate Forest-neutral data;
- shared derived data should be reused across Trees/Clones when dependencies match.

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
Runtime-native inference cache
```

Native inference cache remains runtime-owned.

Important:

> **Cache identity should follow the truth object being cached, not whichever Clone happened to request it.**

---

# 17. Phase 14.6 — Parsed Data, Capability Cache, Learning, and User Context

## 17.1 Parsed YAML cache

Rules:

- derived;
- dependency-fingerprinted;
- Forest-neutral;
- deep-copy before caller mutation;
- deletion triggers rebuild.

## 17.2 Capability-resolution cache

Installed in:

```text
capabilities/resolver.py
```

Verified:

```text
first resolution does real work
second resolver sharing cache reuses it
identity excludes Tree/Clone/Task/session
strict/permissive callers share canonical result
caller mutation cannot poison cache
manifest change invalidates
cache deletion rebuilds
```

Key architecture:

> **Capability resolution is Forest-shared. Capability activation is Clone-specific.**

## 17.3 Learning + User Context foundation

Separated:

### Operational Learning

- mistakes;
- successes;
- procedures;
- environment observations;
- recurring execution lessons.

### User Context

- Preferences;
- Constraints;
- Corrections;
- Current Context.

### Syrup

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

Cold/Warm/Hot:

```text
COLD
durable truth
    ↓
WARM
indexes/triggers
    ↓
routing
    ↓
HOT
only relevant records
```

> **Cold stores truth. Warm decides relevance. Hot contains only relevant.**

Independent generations:

```text
user_context_generation
operational_learning_generation
```

Conversation changes invalidate routing; execution steps do not.

---

# 18. Phase 14.7 — Layered Hot Context

Status:

```text
✅ COMPLETE
```

Main files:

```text
learning/hot_context.py
learning/foundation.py
learning/snapshot_provider.py
learning/turn_retrieval.py
learning/turn_instruction.py
```

## 18.1 `HotContextAssembly`

Retained fields:

```text
schema_version
prompt
user_context_record_ids
operational_learning_record_ids
section_names
character_count
```

API:

```python
assemble(
    *,
    user_context_records,
    operational_learning_records,
)
```

Keyword-only.

Semantic prompt order:

```text
1. User Corrections
2. User Constraints
3. User Preferences
4. Current Context
5. Operational Learning
```

Provenance order and semantic rendering order are intentionally separate concerns.

## 18.2 Historical snapshot retrieval

Rules:

- old turns may retrieve their captured historical truth;
- historical retrieval never silently returns a newer revision;
- committed records deeply immutable;
- generations act as visibility boundaries;
- same Cold key single-flights;
- future generations fail closed;
- old snapshot misses must not mutate newer sticky state.

## 18.3 Turn instruction freeze

One meaningful turn:

```text
resolve once
    ↓
retrieve once
    ↓
assemble once
    ↓
immutable instruction snapshot
    ↓
all runtime attempts reuse it
```

A bug was found when a keyword-only assembler was called positionally. The caller was fixed rather than weakening the API.

## 18.4 Stale recovery proof

`TaskSessionManager.send_runtime_turn()` stale recovery was tested so first send and retry received the **same exact Python `instructions` object**.

Concurrent overlapping-turn test:

```text
Captured turns:                2
Instruction snapshots:         2
Concurrent runtime attempts:   4
Meaningful-input transitions:  2
Runtime-triggered retrievals:  0
Runtime-triggered assemblies:  0
Cross-turn leakage:            0
```

This became foundational for Model Form freeze/retry semantics.

---

# 19. Phase 14.8 — Runtime Cache / Prefix Integration

Status:

```text
✅ COMPLETE
```

This phase intentionally did **not** invent a Forest-owned KV cache.

Core rules:

> **Native inference caches are runtime-owned; Forest treats them through opaque interfaces/handles rather than reimplementing them.**

> **Forest may coordinate cache lifetime/identity, but runtime owns cache contents.**

> **Forest CacheCoordinator is not an inference/KV cache.**

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

Therefore no fake `inference_reuse_capability()` contract was invented.

Normal stale behavior:

```text
Forest binding S1
    ↓
ensure reuses S1
    ↓
runtime send(S1)
    ↓
runtime reports stale only when used
    ↓
create S2 once
    ↓
rotate binding
    ↓
retry
```

---

# 20. Phase 14.9 — Source Context Targeting

Status:

```text
✅ COMPLETE
```

Core doctrine:

> **Source Context is a Forest subsystem, not a Learning subsystem and not a runtime-adapter feature.**

> **Source truth is shared. Source relevance is turn-local.**

> **Share parsed source/index, not turn relevance decision.**

## 20.1 Pipeline

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

## 20.2 Created files

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

## 20.3 Important exact constants

```python
LOCAL_FILE_FINGERPRINT_METHOD = "stat-size-mtime-v1"
PYTHON_STRUCTURE_KIND = "python-ast-v1"
MARKDOWN_STRUCTURE_KIND = "markdown-headings-v1"
```

## 20.4 Neutral models

```python
SourceIdentity
SourceFingerprint
SourceRegion
SourceTarget
```

`SourceTarget` is turn-local and must not mutate shared objective structure.

## 20.5 Race-safe local snapshot

Transient race evidence:

```text
st_dev
st_ino
st_size
st_mtime_ns
```

Persistent cheap fingerprint:

```text
size
mtime_ns
```

Exact content-derived identity:

```text
content_sha256
```

## 20.6 Deterministic targeting rules

- exact region ID first;
- exact unique label second;
- ambiguous duplicate label -> fail closed;
- explicit region ID may disambiguate;
- no fuzzy guessing;
- no embedding/model targeting required for exact structural selection;
- no whole-source fallback unless explicit;
- bounded ancestor-only expansion;
- no siblings/children automatically;
- ancestor may contribute breadcrumbs instead of body unless explicitly targeted;
- overlap deduplicated;
- hard packet/render budgets;
- no silent source truncation;
- local filesystem path hidden by default;
- Source Context is reference data, not instruction authority.

## 20.7 Runtime recovery invariant

Stale runtime recovery performs **zero** new:

```text
source observation
source reads
structure builds
reference matching
targeting
target expansion
packet assembly
rendering
Forest recomposition
Learning recomputation
Hot Context assembly
```

The exact frozen final instruction object is reused.

Decision:

> **Do not optimize 14.9 further without evidence of a real workload bottleneck.**

---

# 21. Long-Term Memory and Progressive Retrieval Architecture

The model has finite context.

The Tree does not need a finite lifetime.

## 21.1 Do not destroy originals through summary-of-summary replacement

Rejected pattern:

```text
original
  ↓
summary
  ↓
summary of summary
  ↓
summary of summary of summary
  ↓
original effectively disappears
```

Preferred:

```text
ORIGINAL
├── detailed summary
├── episode summary
├── long-term abstract
├── structured Leaves
├── vector embedding
└── metadata / Roots
```

Every derived representation should preserve provenance back to original material.

## 21.2 Multi-resolution memory

Example:

```text
Original conversation: 40,000 tokens
Detailed summary:       4,000 tokens
Episode summary:          800 tokens
Memory abstract:          150 tokens
Embedding/index:        compact derived representation
```

Tree loads only the shallowest level needed.

## 21.3 Progressive retrieval

Core rule:

> **Retrieve at the shallowest depth that answers the question, then dig deeper only when necessary.**

Possible levels:

```text
LEVEL 1
tiny abstract
~50–150 tokens

LEVEL 2
Leaf / episode
~300–1,000 tokens

LEVEL 3
detailed historical chunks
~2,000–10,000 tokens

LEVEL 4
original conversation/artifact
full fidelity
```

This directly fits:

> **The Forest gets deeper as you wonder.**

## 21.4 Hybrid retrieval

Long-term memory should be hybrid:

- semantic/vector search;
- exact metadata;
- full-text/lexical search;
- stable IDs;
- graph relationships;
- date/version indexes;
- structured records.

A vector match is useful for similarity, but:

> **A vector index is not the memory itself.**

and:

> **A vector match does not grant permission to read the source.**

## 21.5 Permission before context assembly

Preferred:

```text
query
  ↓
candidate matches
  ↓
permission check
  ↓
allowed sources
  ↓
retrieve
  ↓
Hot Context
  ↓
model
```

Not:

```text
retrieve everything
  ↓
give everything to model
  ↓
ask model what it should have seen
```

## 21.6 Memory roles

- **Maple** helps organize and map knowledge.
- **Leaves** preserve durable knowledge.
- **Roots** preserve provenance/relationships.
- **Leaf Litter** provides colder lifecycle.
- **Operational Learning** preserves execution experience.
- **Mycelium** connects permission-aware continuity across Trees.
- **Hot Context** selectively rehydrates what matters.
- Originals remain available for deep inspection.

## 21.7 Storage scale vs active context

A Forest may eventually contain terabytes of:

- conversations;
- screenshots;
- code;
- documents;
- images;
- videos;
- logs;
- models;
- summaries;
- embeddings.

That does not imply terabytes of active RAM.

Separate:

```text
disk-scale lifetime history
from
RAM-scale selective working context
```

---

# 22. Phase 14.10 — Human Reasoning Control

Current authoritative terminology:

```text
Light
Normal
Deep
```

Older archives sometimes say:

```text
Quick
Normal
Deep
```

Treat Light/Normal/Deep as the current canonical user-facing terminology unless explicitly changed.

Status:

```text
✅ COMPLETE / CERTIFIED
```

## 22.1 Precedence

Current effective precedence:

```text
exact-turn override
    >
temporary override
    >
pinned
    >
Auto
    >
Normal safe default
```

## 22.2 Temporary lease

A temporary Reasoning lease was tested across **5 successful meaningful turns**.

Only successful meaningful turns consume the lease.

Execution/retry does not consume it again.

## 22.3 Important invariants

- Deep does not automatically activate more Skills.
- Deep does not imply Big.
- Runtime stale retry uses the already-frozen Reasoning decision.
- New meaningful user input may resolve a new mode.
- Execution recovery does not reclassify complexity.

## 22.4 Real runtime test

Historical real Light turn:

```text
~147.11 s
```

## 22.5 Certified adapter hash

Recorded post-certification Hermes adapter SHA256:

```text
e443eae3998ae48043e0be6b4ca576aefb0a5346995efb2
```

Do not retest 14.10 unless touched or a later integration demonstrates regression.

---

# 23. Phase 14.11 — Model Form Architecture

## 23.1 Model Form values

Forest-facing control:

```text
Auto
Small
Big
```

But:

> **Auto is policy, not a runtime form.**

Every meaningful turn resolves to:

```text
Small
or
Big
```

before runtime/session creation.

## 23.2 Execution-context scope

Model Form belongs to an execution context, not the Tree globally.

Example:

```text
Main Maple
Big + Deep

Photo Clone
Small + Light

Document Clone
Small + Normal

Code Clone
Big + Normal
```

This is normal, not an exception.

Tree default seeds contexts; it is not a live broadcast.

## 23.3 Explicit vs Auto

Core rule:

> **Automatic escalation may degrade gracefully. Explicit escalation must not silently downgrade.**

If explicit Big is unavailable:

```text
report unavailable
```

Do not silently use Small.

Auto may fall back if policy permits and should record why escalation was constrained.

---

# 24. 14.11A — Canonical Model Form Contract

Files:

```text
model_form/model.py
model_form/__init__.py
```

Core values:

```text
Auto
Small
Big
```

Resolved values:

```text
Small
Big
```

`ModelFormDecision` is immutable and contains semantic decision data such as:

```text
form
source
execution_context_id
reasons
```

It deliberately excludes:

- adapter;
- runtime session;
- model vendor;
- model filename;
- runtime-specific implementation.

Meaningful turn resolves once. Retry uses the frozen result.

---

# 25. 14.11B — Model Form Control State

Hierarchy:

```text
Tree
  ↓
execution context
  ↓
Task
  ↓
runtime session
```

Task is **not** the execution context.

Control direction includes:

```text
Tree default
  ↓
context baseline/pin
  ↓
temporary/task-local control
  ↓
exact-turn override
```

Current effective precedence captured during implementation:

```text
exact
  >
matching task override
  >
pinned
  >
Auto
  >
Small
```

`ctx-default` exists only for compatibility and must not encode Main/Ortet meaning.

Explicit Big unavailable fails closed.

---

# 26. 14.11C — Runtime-Neutral Model Registry

File:

```text
model_form/registry.py
```

Rules:

- Auto never maps directly to a runtime binding;
- form -> opaque binding ID;
- binding -> runtime configuration;
- partial registry is valid;
- an unbound requested form fails closed.

Current live registry shape:

```yaml
schema_version: 1

forms:
  small: binding-0001

bindings:
  binding-0001:
    runtime:
      adapter: hermes
      profile: bristlecone
      platform: api_server
```

Current reality:

```text
Small -> binding-0001
Big   -> unbound
```

This is intentional. Big architecture is being built before activation.

---

# 27. Big Bristlecone Model Candidate and Staging

Leading Big candidate:

```text
mistralai/Mistral-Small-4-119B-2603-NVFP4
```

Known characteristics:

```text
Developer: Mistral AI
Origin: France
License: Apache 2.0
Total params: ~119B
Active/token: ~6.5B
Experts: 128
Active experts/token: 4
Context: 256K
Text input: yes
Image input: yes
Text output: yes
Reasoning: configurable
Coding: yes
Agentic coding: yes
Tool/function calling: yes
Fine-tuning/customization: yes
```

## 27.1 Staging status

Verified staging checkpoint:

```text
Repository:
mistralai/Mistral-Small-4-119B-2603-NVFP4

Download:
~70.8 GB

Local footprint:
~66 GiB

Weight shards:
13 / 13

Repository files checked:
23

Checksums:
all matched

Approx Cherry-AI free space after staging:
~53 GiB at that checkpoint
```

Current status:

```text
✅ downloaded
✅ reconstructed
✅ all 13 shards present
✅ checksums verified
✅ staged locally

❌ not loaded
❌ not connected to Hermes
❌ not activated as Bristlecone Big
✅ current Small Qwen remains untouched
```

> **Download/staging is not activation.**

## 27.2 Do not blindly use `ollama pull mistral-small`

The public `mistral-small` Ollama tag historically referred to earlier Mistral Small generations.

Do not assume:

```bash
ollama pull mistral-small
```

means the exact staged Mistral Small 4.

Use exact provenance.

## 27.3 GPT-OSS comparison

### GPT-OSS-120B

Reference snapshot:

```text
Developer: OpenAI
License: Apache 2.0
Total params: ~117B
Active/token: ~5.1B
Context: 128K
MoE: yes
Reasoning: low / medium / high
Tools/agents: yes
Fine-tuning: yes
Native vision: no
Low-precision checkpoint: ~60.8 GiB
```

Strengths:

- reasoning;
- coding;
- agents/tools;
- AI/model engineering;
- permissive license;
- clean Light/Normal/Deep mapping.

Main limitation for Treewright:

```text
text-only
```

### GPT-OSS-20B

Possible future model-library candidate:

```text
~21B total
~3.6B active/token
128K context
Apache 2.0
reasoning controls
tools/agents
fine-tunable
text-only
~13 GB-class checkpoint
~16 GB-class memory target
```

Possible later uses:

- McIntosh Big;
- fallback;
- training experiments;
- alternative Tree;
- edge/portable use.

No permanent assignment yet.

## 27.4 Vision

Mistral Small 4 native vision is attractive for Bristlecone because Treewright work may include:

```text
build UI/vector
    ↓
render
    ↓
inspect screenshot
    ↓
critique spacing/alignment/hierarchy
    ↓
modify code
    ↓
render again
```

However, Vision Workshop remains valuable architecturally:

```text
BRISTLECONE
    |
    +-- normal reasoning
    |
    +-- Vision Workshop
          ↓
        vision model
          ↓
        structured observations
          ↓
        main model
```

This keeps vision as a Tree capability rather than permanently coupling identity to one model.

## 27.5 Hardware reality

Both GPT-OSS-120B and Mistral Small 4 are roughly in a **60+ GB low-precision model-memory class**.

Current ~32 GB RAM / RX580 hardware cannot comfortably run Big locally.

Therefore:

- staging is possible;
- activation is not yet practical;
- runtime/quantization testing should inform future hardware decisions;
- do not remove Qwen baseline.

---

# 28. 14.11D-0 — Runtime Session Identity Prerequisite

One of the most important architectural corrections:

> **Adapter name alone is not session identity. Binding ID alone is not session identity.**

Canonical live identity:

```text
(execution_context_id, binding_id)
    ->
runtime session
```

Why adapter alone fails:

```text
Small -> Hermes -> profile A -> session A
Big   -> Hermes -> profile B -> session B
```

Both would otherwise compete for one:

```text
runtime_sessions["hermes"]
```

Why binding alone fails:

```text
ctx-0001 -> binding-0001 -> session-A
ctx-0002 -> binding-0001 -> session-B
```

Both contexts may share model weights/binding while requiring independent mutable sessions.

## 28.1 Created files

```text
runtime/session_identity.py
runtime/session_store.py
```

`RuntimeSessionIdentity`:

```python
RuntimeSessionIdentity(
    execution_context_id,
    binding_id,
)
```

Canonical state:

```yaml
runtime_sessions:
  ctx-0001:
    binding-0001:
      adapter: hermes
      session_id: session-A
      previous_session_id: null
      updated_at: ...
```

## 28.2 Helpers

```text
_runtime_session_binding_for_identity
_write_runtime_session_binding_for_identity
_capture_runtime_persist_guard_for_identity
_persist_runtime_binding_guarded_for_identity
```

Legacy no-context runtime APIs were retained as compatibility paths.

## 28.3 Certified snapshot

```text
bristlecone/backups/phase14_11D0_certified_20260811T123502Z
```

8 files.

---

# 29. 14.11D1–D3 — Frozen Form Resolution and TaskSession Integration

## D1 — `model_form/resolution.py`

Added:

```text
ModelFormResolutionError
FrozenModelFormTurn
resolve_model_form_turn(...)
```

`FrozenModelFormTurn` contains a frozen `ModelFormDecision`, resolved binding, optional Task ID, and exposes properties such as:

```text
execution_context_id
form
source
reasons
binding_id
adapter
runtime_state
```

## D2 — public resolution API

Exports were made public through the Model Form package.

## D3 — TaskSession integration

`TaskSessionManager.prepare_model_form_turn(...)`:

- requires explicit execution context;
- requires active Task;
- uses canonical `model_form_control`;
- ignores legacy `state["model_form"]`;
- loads registry;
- resolves once;
- performs no runtime I/O;
- performs no persistence.

---

# 30. 14.11D4A/B/C — Frozen Runtime View and Identity-Aware Session State

## D4A — self-contained runtime binding

Discovered that Hermes runtime operations require:

```yaml
platform: api_server
```

The frozen runtime binding must therefore carry enough runtime config to execute independently.

## D4B — ephemeral runtime view

Helper:

```text
_execution_state_for_model_form_turn
```

Behavior:

```text
deepcopy authoritative Forest state
    ↓
replace only execution copy's `runtime`
    ↓
leave authoritative state untouched
```

## D4C1 — identity-aware session ensure

Uses:

```text
execution_context_id + binding_id
```

not adapter-only state.

## D4C2 — identity-aware persistent CAS

Forward persistence uses expected Task/context/binding/adapter/session generation and re-checks latest durable state before mutation.

---

# 31. 14.11D4D1 — Frozen Normal Send Path

Explicit-context send path resolves:

```text
Reasoning once
Model Form once
```

before meaningful input and runtime execution.

It then uses frozen runtime identity for the turn.

Explicit Big unbound fails before model I/O.

---

# 32. 14.11D5 — Frozen Stale Recovery

Status:

```text
✅ CERTIFIED
```

One-shot stale recovery preserves:

```text
same frozen Model Form
same frozen Reasoning
same exact user message
same exact instructions object
same execution context
same binding identity
```

Flow:

```text
initial send
  ↓
verified stale?
  ↓ yes
create exactly one replacement
  ↓
persist replacement if needed
  ↓
retry exactly once
  ↓
no second recovery
```

Runtime recovery is execution repair, not new meaningful input.

Certified snapshot:

```text
bristlecone/backups/phase14_11D5_certified_20260811T135122Z
```

8 files.

---

# 33. 14.11E1 — Immutable ModelFormHandoff

File:

```text
model_form/handoff.py
```

Immutable fields:

```text
execution_context_id
task_id
from_form
to_form
source
reasons
schema_version
```

Requirements:

- actual form change required;
- no runtime adapter;
- no binding ID;
- no session ID;
- no vendor/model name;
- no continuity payload.

This object represents semantic handoff meaning, not execution implementation.

Certified backup:

```text
bristlecone/backups/phase14_11E1_certified_20260811T135713Z
```

---

# 34. 14.11E2 — Pure Handoff Detection

File:

```text
model_form/handoff_detection.py
```

Function:

```python
detect_model_form_handoff(
    previous_form,
    frozen_turn,
)
```

Behavior:

```text
previous is None -> no handoff
same form        -> no handoff
changed form     -> ModelFormHandoff
```

No runtime I/O or state mutation.

Certified backup:

```text
bristlecone/backups/phase14_11E2_certified_20260811T140259Z
```

---

# 35. 14.11E3 — Portable Continuity

## E3A — frozen instruction continuity

Reuses the existing:

```python
ForestTurnInstructionComposition
```

This preserves:

- exact final instruction string;
- source packets;
- learning provenance;
- frozen composition state.

No duplicate instruction-continuity class was created.

## E3B — `ConversationContinuity`

File:

```text
runtime/conversation_continuity.py
```

Core:

```python
ConversationExchange(
    user_message,
    assistant_message,
)
```

and:

```python
ConversationContinuity(
    execution_context_id,
    task_id,
    exchanges,
    schema_version=1,
)
```

Contains only completed conversation.

Does **not** contain:

- runtime session ID;
- KV/cache;
- reasoning state;
- tool/inflight execution state.

Assistant message text is preserved exactly, including an empty string.

## E3C — `ModelFormContinuity`

File:

```text
model_form/continuity.py
```

Combines:

```text
ForestTurnInstructionComposition
+
ConversationContinuity
```

into a portable runtime-neutral artifact.

Certified snapshot:

```text
bristlecone/backups/phase14_11E3_certified_20260811T142122Z
```

4 files.

---

# 36. 14.11E4A/B/C — Context-Local Semantic State

Canonical sibling state:

```yaml
task_session:
  runtime_sessions: ...

  effective_model_forms:
    ctx-A: small

  conversation_continuity:
    ctx-A:
      schema_version: 1
      execution_context_id: ctx-A
      task_id: task-...
      exchanges:
        - user_message: ...
          assistant_message: ...
```

## E4B helpers

```text
_effective_model_form_context_id
_effective_model_form_for_context
_write_effective_model_form_for_context
```

## E4C helpers

```text
_conversation_continuity_for_context
_append_conversation_exchange_for_context
```

Detached/in-memory by default.

Backups:

```text
E4A:
bristlecone/backups/phase14_11E4A_certified_20260811T143316Z/task_session.py

E4B:
bristlecone/backups/phase14_11E4B_certified_20260811T144133Z/task_session.py

E4C:
bristlecone/backups/phase14_11E4C_certified_20260811T144507Z/task_session.py
```

---

# 37. 14.11E4D — Unified Successful-Turn Semantic Commit

Core helper:

```python
_commit_successful_model_form_turn(
    self,
    *,
    working,
    frozen_turn,
    user_message,
    assistant_message,
    turn_control,
    decision,
    expected_previous_form,
    persist,
)
```

## 37.1 Failure semantics

Failed turn:

```text
previous effective form unchanged
no conversation exchange appended
temporary Reasoning lease unchanged
```

## 37.2 Success semantics

Successful turn:

```text
effective form = frozen form
append exact completed user/assistant exchange
finalize temporary Reasoning lease exactly once
```

## 37.3 Critical concurrency correction

A subtle race was found before certification.

Problem:

The source previous form could have been read from `working` refreshed after runtime work. An older in-flight turn might overwrite a newer successful different-form turn.

Fix:

Immediately after form resolution, freeze previous successful form from **pre-turn `control_state`**:

```python
turn_previous_effective_form = (
    self._effective_model_form_for_context(
        control_state,
        frozen_turn.execution_context_id,
    )
)
```

Persistent semantic commit then checks:

```text
latest_previous_form == source_previous_form
OR
latest_previous_form == frozen_turn.form
```

Otherwise fail:

```text
Stale effective Model Form:
a newer successful turn changed this execution context
to a different form before commit.
```

This allows concurrent same-form completion but rejects an older conflicting form generation.

## 37.4 Structural harness lesson

The frozen send uses:

```python
sender = getattr(
    runtime_adapter,
    "send_turn",
    None,
)
```

and later:

```python
result = sender(...)
```

An initial structural harness incorrectly expected a direct `.send_turn(...)` call and failed despite correct behavior. The harness was corrected to recognize the indirect sender binding.

Certified backup:

```text
bristlecone/backups/phase14_11E4D_certified_20260811T150951Z/task_session.py
```

---

# 38. 14.11E4E1 — Pure Handoff Continuity Preparation

Added:

```python
_prepare_model_form_handoff_continuity(
    *,
    state,
    frozen_turn,
    previous_form,
    instruction_composition,
)
```

Responsibilities:

- validate state;
- validate `FrozenModelFormTurn`;
- validate execution context;
- validate active Task identity;
- detect actual Model Form handoff;
- for first/same form, return no bootstrap;
- actual handoff requires exact typed `ForestTurnInstructionComposition`;
- read context-local completed conversation;
- validate conversation Task/context identity;
- create `ModelFormContinuity`.

It does **not**:

- perform runtime I/O;
- create runtime session;
- persist;
- replay conversation;
- append current user turn;
- send model turn.

## 38.1 Safe failed installer

Initial raw-text installer looked for an anchor that appeared **five times**.

It stopped safely before mutation.

Lesson:

> **Use AST/structural boundaries when raw anchors are ambiguous.**

Historical pre backup:

```text
phase14_11E4E1_pre_handoff_preparation_20260811T151448Z
```

Correct AST installer pre-backup:

```text
phase14_11E4E1_pre_handoff_preparation_20260811T151957Z
```

Certified:

```text
bristlecone/backups/phase14_11E4E1_certified_20260811T152409Z/task_session.py
```

---

# 39. 14.11E4E2 — Runtime-Neutral Continuity Bootstrap Contract

File:

```text
runtime/adapters/base.py
```

Added:

```python
class RuntimeContinuityUnsupportedError(
    RuntimeAdapterError
):
    ...
```

Optional non-abstract method:

```python
def create_session_with_continuity(
    self,
    state,
    continuity,
    task_id=None,
):
    raise RuntimeContinuityUnsupportedError(
        "This runtime adapter does not support "
        "portable Forest continuity bootstrap."
    )
```

Important:

- optional;
- non-abstract;
- existing adapters remain concrete;
- runtimes opt in independently;
- unsupported runtime fails closed.

## 39.1 Safe decorator insertion failure

First installer inserted relative to `get_session` without respecting its decorator boundary and risked accidentally making the new optional method abstract.

Structural validation caught:

```text
optional continuity capability was accidentally made abstract
```

No certification occurred on that bad shape.

Backups:

```text
phase14_11E4E2_pre_continuity_contract_20260811T155602Z/base.py
phase14_11E4E2_pre_continuity_contract_20260811T155737Z/base.py
```

Certified backup:

```text
bristlecone/backups/phase14_11E4E2_certified_20260811T155944Z/base.py
```

SHA256:

```text
e2b002a37b7048fa543876a26c8608154a9707acdb93c378d3a1bdea66b395fb
```

---

# 40. 14.11E4E3A — Typed Instruction Composition Passthrough

Public and frozen send APIs now accept:

```python
instruction_composition=None
```

alongside:

```python
instructions=None
```

Rules:

```text
instruction_composition absent
    -> legacy callers remain valid

instruction_composition supplied
    -> must be ForestTurnInstructionComposition

instructions absent
    -> use exact instruction_composition.instructions object

both supplied
    -> instructions must be the SAME object

equal-but-distinct string
    -> fail closed
```

Identity is checked using object identity, not equality.

Validation occurs before meaningful-input transition.

E4E3A deliberately added **no** handoff/bootstrap transaction behavior.

Certification also confirmed:

- D5 still has initial send + one stale retry;
- E4D still has one unified semantic commit;
- E4E2 runtime contract unchanged.

Pre backup:

```text
bristlecone/backups/phase14_11E4E3A_pre_typed_passthrough_20260811T160700Z/task_session.py
```

Certified:

```text
bristlecone/backups/phase14_11E4E3A_certified_20260811T161005Z/task_session.py
```

SHA256:

```text
c87c27e6c4b7962754faa6f2fd809f320411805bb91803d93298521ff19d4ab2
```

---

# 41. 14.11E4E3B — Detached Handoff Runtime Bootstrap

Added:

```python
_bootstrap_runtime_session_for_model_form_handoff(
    *,
    state,
    frozen_turn,
    continuity,
)
```

Purpose:

```text
Frozen target Model Form
+
ModelFormContinuity
    ↓
target runtime adapter
    ↓
create_session_with_continuity
    ↓
fresh target session
    ↓
detached Forest context+binding state
```

## 41.1 Fresh-session invariant

Actual handoff must create a **fresh target-form session**, even if an older dormant session for that target form exists.

Why:

```text
Small -> Big -> Small
```

The old Small session does not necessarily contain the conversation performed while Big was active.

Correct:

```text
current Forest-owned conversation continuity
    ↓
fresh Small session
```

The old target session is reported as:

```text
replaced_session_id
```

but is not retired by E4E3B.

## 41.2 Responsibilities

E4E3B:

- validates frozen turn;
- validates continuity type;
- validates Task/context identity;
- deep-copies state;
- verifies active Task;
- constructs frozen execution state;
- resolves target runtime adapter;
- validates adapter matches frozen binding;
- observes existing target context+binding;
- calls `create_session_with_continuity`;
- validates returned adapter/session;
- requires fresh session ID;
- writes fresh target binding only into detached state;
- records old target as `previous_session_id` / `replaced_session_id`.

It does **not**:

- persist;
- send current user turn;
- consume reasoning;
- semantic-commit conversation;
- retire old target session.

## 41.3 Cleanup gap found before certification

Initial source cleaned a new session if binding write failed.

Review found another gap:

```text
runtime creates fresh session
    ↓
returns mismatched adapter
    ↓
helper raises before binding
    ↓
fresh unbound session could leak
```

Correction:

- if mismatched adapter returns a new session ID, best-effort retire that **new** session;
- never retire `replaced_session_id`;
- if runtime returns the old canonical target session ID, fail fresh-session invariant **without ending the old canonical session**;
- binding-write cleanup remains.

Pre backup:

```text
bristlecone/backups/phase14_11E4E3B_pre_bootstrap_helper_20260811T161227Z/task_session.py
```

Cleanup correction pre-backup:

```text
bristlecone/backups/phase14_11E4E3B_pre_cleanup_fix_20260811T161420Z/task_session.py
```

Certified backup:

```text
bristlecone/backups/phase14_11E4E3B_certified_20260811T161700Z/task_session.py
```

SHA256:

```text
bde405826e48e3332a9eff33dd7b3828b1733e3e1f760108a02fd0100348392e
```

Certification proved:

```text
fresh target session bootstrapped from exact continuity
caller state remains detached
old target reported without premature retirement
execution-context isolation
unsupported runtime fails closed
malformed adapter result cleans fresh new session
fresh-session violation preserves old canonical session
binding-write failure cleans fresh unbound session
continuity identity fails before runtime creation
no persistence
no send
no reasoning
no semantic commit
```

---

# 42. 14.11E4E3C1 — CAS-Aware Runtime Binding Rollback

This was required because forward persistence was write/merge only.

Recon found guard keys:

```text
task_id
execution_context_id
binding_id
adapter
session_id
```

Forward persistence uses:

```text
get_runtime_session_binding
set_runtime_session_binding
_state_write_lock
load_state
normalize_task_session
_atomic_write_yaml
```

No canonical session-store delete/remove API existed.

No deletion shape existed in forward persist helper.

Therefore rollback needed a dedicated helper.

## 42.1 Added helper

```python
_rollback_runtime_binding_guarded_for_identity(
    self,
    working,
    guard,
    restore_binding,
)
```

### Case A — old target existed

```text
old target binding
    ↓
fresh handoff binding persisted
    ↓
transaction rejected
    ↓
rollback CAS verifies durable slot still points at our handoff session
    ↓
restore exact old target binding
```

### Case B — no old target existed

```text
no target binding
    ↓
fresh handoff binding persisted
    ↓
transaction rejected
    ↓
rollback CAS verifies durable slot still points at our handoff session
    ↓
remove only our binding
    ↓
prune context bucket if empty
```

Rollback proceeds only while durable state still matches:

```text
same active Task
same execution_context_id
same binding_id
same adapter
same session_id
```

If a newer writer changed the slot:

```text
rollback fails stale
newer state remains untouched
```

## 42.2 C1 repairs Forest state only

It does **not**:

- create runtime sessions;
- end runtime sessions;
- send turns;
- consume reasoning;
- semantic-commit.

Runtime cleanup belongs to C2.

## 42.3 Safe recon failure: missing dedent

A micro-recon attempted:

```python
ast.parse(
    inspect.getsource(method)
)
```

without `textwrap.dedent`.

Result:

```text
IndentationError: unexpected indent
```

No source mutation occurred.

Lesson:

> **Dedent class-method source before AST parsing.**

## 42.4 Safe installer failure: `__file__`

First installer tried to execute `task_session.py` merely to prove imports existed.

Because the temporary `exec()` namespace lacked `__file__`, module initialization failed:

```text
NameError: name '__file__' is not defined
```

Failure happened before backup/write.

Correction:

> **Use AST-only import inspection. Do not execute source just to prove imports.**

## 42.5 Pre backup

```text
bristlecone/backups/phase14_11E4E3C1_pre_binding_rollback_20260811T162900Z/task_session.py
```

## 42.6 Certification

Passed:

```text
restore exact prior canonical target binding
leave caller working state detached
one atomic write while locked
remove target that did not exist before handoff
prune empty execution-context bucket
preserve unrelated execution context
preserve sibling binding in same context
newer concurrent session generation blocks rollback
changed adapter blocks rollback
changed active Task blocks rollback
invalid restore binding fails before persistence
Forest-state-only boundary
exactly one atomic durable write site
```

Certified backup:

```text
bristlecone/backups/phase14_11E4E3C1_certified_20260811T163126Z/task_session.py
```

SHA256:

```text
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c
```

---

# 43. Current Live Target — 14.11E4E3C2 Frozen Handoff Transaction Integration

Status:

```text
→ CURRENT
```

No source mutation has occurred yet.

## 43.1 Current frozen send signature

Latest recon:

```python
(
    self,
    message,
    *,
    execution_context_id,
    state=None,
    instructions=None,
    instruction_composition=None,
    reasoning_mode=None,
    persist=False,
    model_form=None,
    automatic_model_form=None,
)
```

## 43.2 Post-C1 landmark recon

Current local-method landmarks:

```text
132 CALL   self.prepare_model_form_turn
150 ASSIGN turn_previous_effective_form
183 CALL   context_route_state.begin_meaningful_input
237 ASSIGN persist_guard
240 ASSIGN persist_guard
241 CALL   self._capture_runtime_persist_guard_for_identity
250 ASSIGN ensured
291 ASSIGN requested_session_id
313 CALL   self._persist_runtime_binding_guarded_for_identity
321 CALL   self._best_effort_end_runtime_sessions
331 ASSIGN persist_guard
395 ASSIGN session_recovered
402 CALL   sender
582 CALL   self._best_effort_end_runtime_sessions
595 CALL   self._persist_runtime_binding_guarded_for_identity
602 CALL   self._best_effort_end_runtime_sessions
613 ASSIGN persist_guard
681 ASSIGN requested_session_id
685 ASSIGN session_recovered
693 CALL   sender
704 CALL   self._best_effort_end_runtime_sessions
783 ASSIGN binding
808 CALL   self._persist_runtime_binding_guarded_for_identity
822 CALL   self._best_effort_end_runtime_sessions
832 ASSIGN binding
854 CALL   self._commit_successful_model_form_turn
```

Recon status:

```text
0
```

## 43.3 Missing source detail

A numbered pre-send source recon covering the region around:

```text
persist_guard
ensured
requested_session_id
pre-turn persistence
```

ran successfully, but the actual numbered source body did not reach the assistant in the conversation.

A compact AST recon was then proposed to print only:

```text
persist_guard[...]
ensured[...]
requested_session_id[...]
IF@...
```

The user requested this master checkpoint instead of running that recon.

Therefore:

> **The compact E4E3C2A pre-send recon remains the immediate next terminal action before any patch.**

Do not infer the exact current `ensured` expression.

Do not guess the current no-handoff session-acquisition branch.

---

# 44. E4E3C2 — Intended Full Transaction

Target behavior:

```text
resolve Reasoning exactly once
        ↓
resolve Model Form exactly once
        ↓
freeze previous successful Model Form
        ↓
prepare handoff continuity
        │
        ├── no actual handoff
        │      ↓
        │   certified D5 path remains
        │
        └── actual handoff
               ↓
          exact E4E1 ModelFormContinuity
               ↓
          E4E3B fresh target session
               ↓
          CAS-persist target binding
          BEFORE long model I/O
               ↓
          send current user message
               ↓
          stale?
               │
               ├── no
               │
               └── yes
                      ↓
                one fresh replacement
                using SAME continuity
                      ↓
                persist replacement
                      ↓
                retry exact same turn once
               ↓
          normalize final runtime binding
               ↓
          E4D semantic commit exactly once
               │
         ┌─────┴────────┐
         │              │
      SUCCESS        REJECT/FAIL
         │              │
         ↓              ↓
 retire old        C1 rollback Forest
 replaced target  binding if still ours
 session           +
                   retire failed/advanced
                   handoff runtime sessions
                   that are provably ours
```

---

# 45. E4E3C2A — Detailed Next Implementation Plan

The planned first half is intentionally narrow.

## Goal

Wire:

```text
handoff preparation
+
fresh target-session bootstrap
+
pre-turn persistence
```

without simultaneously rewriting stale retry and semantic rollback.

## Step A1 — prepare handoff before meaningful input

After:

```text
frozen Model Form resolved
previous successful form frozen
```

but before:

```text
begin_meaningful_input()
runtime send
```

call E4E1 preparation.

Inputs must come from pre-turn state:

```text
control_state
frozen_turn
turn_previous_effective_form
instruction_composition
```

## Step A2 — distinguish no handoff from actual handoff

### No handoff

Examples:

```text
first successful Small baseline
Small -> Small
Big -> Big
```

Preserve existing certified D5 session-acquisition path as closely as possible.

### Actual handoff

Examples:

```text
Small -> Big
Big -> Small
```

Requires exact typed:

```python
ForestTurnInstructionComposition
```

Plain reconstructed instruction text is insufficient.

## Step A3 — capture pre-handoff target binding/generation

Before creating a fresh target session, record enough information to support:

- forward persistence CAS;
- later C1 rollback;
- later success retirement.

Need to know whether:

```text
old target binding exists
```

or:

```text
target binding did not exist
```

## Step A4 — fresh continuity bootstrap

Use:

```python
_bootstrap_runtime_session_for_model_form_handoff(...)
```

not ordinary:

```python
create_session(...)
```

The result should expose:

```text
fresh session
old/replaced session if any
detached working state
continuity
target context
target binding
adapter
```

## Step A5 — persistent handoff must commit binding before model I/O

For `persist=True`:

```text
fresh runtime session created
      ↓
CAS-persist target context+binding
      ↓
only then call model
```

This preserves the Phase 4 crash-consistency doctrine.

## Step A6 — pre-turn persistence failure cleanup

If the CAS fails before current user send:

```text
clean up fresh uncommitted session
do not retire old target
do not alter semantic state
do not append conversation
do not consume reasoning lease
```

If another writer already changed the slot, fail stale and leave newer truth untouched.

## Step A7 — reporting metadata

C2A may need transaction-local metadata such as:

```text
handoff
continuity
replaced_session_id
pre_handoff_binding
handoff_bootstrap_session_id
handoff_binding_persisted
rollback guard
```

Do not add runtime identity fields to `ModelFormHandoff` itself.

## Step A8 — test C2A synthetically

Before C2B:

- same-form branch unchanged;
- first baseline no bootstrap;
- actual handoff requires typed composition;
- fresh continuity session created;
- old target not retired;
- context/task isolation;
- persistent bootstrap binding written before any send;
- CAS failure cleans fresh child;
- no current message send in a helper-only test;
- no E4D semantic commit yet;
- no Reasoning finalization.

---

# 46. E4E3C2B — Detailed Next Implementation Plan

C2B handles the dangerous half: stale recovery, semantic failure, and retirement.

## B1 — initial send remains exactly once

Current user message must be sent once on the normal path.

Portable continuity must contain only **prior completed conversation**.

Do not include current user message inside continuity and then also send it normally.

## B2 — only verified stale triggers replacement

Use existing stale classifier semantics.

Do not turn arbitrary runtime errors into handoff recovery.

## B3 — stale replacement during handoff must use same continuity

This is critical.

Wrong:

```text
handoff session stale
    ↓
ordinary create_session()
    ↓
new session has no prior Forest conversation
```

Correct:

```text
handoff session stale
    ↓
create_session_with_continuity(
    same ModelFormContinuity
)
    ↓
fresh replacement knows same prior completed Forest conversation
```

## B4 — retry freezes everything

Retry must preserve:

```text
same execution_context_id
same frozen Model Form
same binding
same frozen Reasoning
same exact instruction object
same exact current user message
same exact ModelFormContinuity
```

No rerouting.

No source re-retrieval.

No learning reassembly.

No context recomputation.

At most one stale retry.

## B5 — persist replacement before retry if persistent

If replacement session becomes the active target binding:

```text
CAS-persist replacement
    ↓
then retry
```

This preserves crash consistency.

## B6 — final runtime binding normalization

After runtime success, normalize any effective session-ID rotation using existing D5 logic.

Do not accidentally collapse:

```text
context identity
binding identity
runtime session identity
```

## B7 — call E4D exactly once

All possible runtime sends must finish before:

```python
_commit_successful_model_form_turn(...)
```

E4D remains the only semantic success boundary.

## B8 — success retirement

Only **after E4D semantic commit succeeds** may the old pre-handoff target session be safely retired.

Reason:

Until Forest semantic truth commits the handoff turn, the old target binding is the rollback anchor.

## B9 — semantic failure after runtime advanced

If runtime succeeded but E4D semantic CAS rejects:

```text
runtime advanced
Forest semantic truth rejected
```

Then:

1. try C1 rollback of durable target binding;
2. rollback only if durable slot still points to this transaction's session generation;
3. if rollback succeeds, restore old binding or remove new-only binding;
4. retire failed/advanced new handoff session(s) that are provably ours;
5. do not retire restored old target;
6. do not overwrite newer concurrent Forest state.

## B10 — rollback itself may fail stale

If C1 reports newer writer:

```text
do not overwrite
do not blindly kill current canonical session
```

Cleanup only sessions provably owned by the failed transaction and no longer canonical.

This branch needs careful certification.

## B11 — `persist=False`

No durable binding rollback is necessary because there was no durable write.

However, a newly created handoff runtime session should still be cleaned if semantic commit fails, otherwise it leaks.

---

# 47. E4E5 — End-to-End Handoff Certification Plan

After C2A and C2B are individually stable, E4E5 should cover full behavior.

Suggested synthetic certification matrix:

## Baseline / same form

```text
first Small success
Small -> Small
Big -> Big
```

Expect:

- no handoff bootstrap;
- existing D5 path;
- no continuity requirement for same form;
- normal session reuse/recovery.

## Small -> Big

Expect:

- handoff detected;
- typed composition required;
- continuity contains only prior completed turns;
- fresh Big target session;
- current user message exactly once;
- old Big session, if any, retained until commit;
- successful semantic commit switches effective form to Big;
- old replaced Big session retired after commit.

## Big -> Small

Same semantics in reverse.

## Context isolation

Two contexts sharing same binding:

```text
ctx-A -> binding-small -> session-A
ctx-B -> binding-small -> session-B
```

Handoff in A must not affect B.

## Task isolation

Continuity from Task A must never bootstrap Task B.

## Unsupported runtime

Adapter inheriting E4E2 default must fail before pretending continuity is preserved.

## Pre-turn CAS failure

Fresh session must be cleaned.

Old target remains canonical.

No current-turn send.

## Initial send failure

No semantic commit.

If target binding had been persisted, rollback safely.

## Stale handoff send

One replacement from same continuity.

One retry.

No second recovery.

## Retry failure

No semantic commit.

Rollback/cleanup safely.

## Semantic commit stale failure

Simulate newer different-form successful writer.

Expect:

- E4D rejects old turn;
- C1 attempts rollback only if slot still ours;
- newer writer never overwritten;
- cleanup never kills newer canonical session.

## Reasoning lease

Temporary Reasoning consumed exactly once after final semantic success, not on failed attempts or stale retries.

## Conversation continuity

Current successful exchange appended exactly once.

No duplicate current user exchange due to continuity bootstrap/retry.

---

# 48. 14.11F — Resource Request + Governor Contract

This should establish a stable resource hook without building an entire OS scheduler inside 14.11.

## 48.1 Build now

Stable concepts:

```text
ResourceRequest
ResourcePriority
ResourceBudget
ResourceAvailability
Governor interface
Scheduler interface
```

Initial availability may be only:

```text
AVAILABLE
UNAVAILABLE
```

Later:

```text
AVAILABLE
RECLAIMABLE
RECLAIMING
DEFERRED
DENIED
```

without changing Tree-facing semantics.

## 48.2 Explicit vs Auto

### Explicit Big

```text
user explicitly asks Big
    ↓
ask resource system
    ↓
reclaim only permitted resources
    ↓
Big still impossible?
    ↓
report unavailable
```

Never silently downgrade.

### Auto Big

```text
Auto policy wants Big
    ↓
resource request
    ↓
reclaim within Auto budget
    ↓
still unavailable?
    ↓
continue Small if policy permits
    ↓
record resource-constrained reason
```

## 48.3 Resource-management layers

Preferred umbrella architecture:

```text
                  FOREST RESOURCE MANAGEMENT
                           |
          +----------------+----------------+
          |                                 |
   RESOURCE STEWARD                 RESOURCE GOVERNOR
   intelligent planner             deterministic authority
   WHAT SHOULD happen              MAY IT happen
          |                                 |
          +---------------+-----------------+
                          ↓
                  RESOURCE SCHEDULER
                  HOW should it happen
                          ↓
                  constrained adapters
                  DO it
```

### Resource Steward

AI-assisted planner.

Understands workload meaning and urgency.

### Resource Governor

Deterministic Spirit-aligned authority.

Checks:

- permitted?
- safe?
- protected?
- user-pinned?
- checkpointable?
- data-loss risk?

### Resource Scheduler

Translates approved policy into allocation mechanics.

### Adapters

Possible future adapters:

```text
Model runtime
  load/unload/query residency/query memory

Clone
  pause/resume/checkpoint/query interruptibility

Linux/process
  usage/priority/process state

Cache
  release expendable caches

GPU
  availability/workload admission

Qubes
  approved memory/vCPU/start/stop
```

No Tree gets broad dom0 control merely because it requests more power.

## 48.4 What should wait

Qubes-level resource adapter should wait until:

- Spirit permissions mature;
- narrow qrexec interfaces exist;
- actions are auditable;
- rollback is reliable;
- broad dom0 shell is unnecessary.

Highly autonomous Resource Steward should wait until:

- Governor policy is trustworthy;
- Scheduler tested;
- resource metadata reliable;
- Clones pause/resume reliably;
- model residency observable;
- telemetry reliable.

---

# 49. 14.11G — Automatic Escalation Router

Future Auto router responsibilities:

- evaluate task complexity/capability requirements;
- remain separate from Reasoning;
- respect explicit user Form overrides;
- resolve once per meaningful turn;
- consult ResourceAvailability;
- record reasons;
- allow Auto fallback;
- never silently downgrade explicit Big.

Possible signals:

```text
task complexity
required capability
latency tolerance
tool requirements
context demand
known Small failure
user waiting / foreground
resource availability
```

Do not make one stale retry re-run the router.

---

# 50. 14.11H — Colony Runtime / Shared-Weight Semantics

Desired normal behavior:

```text
MAPLE COLONY

Main
  Big + Deep

Photo Clone
  Small + Light

Document Clone
  Small + Normal

Code Clone
  Big + Normal
```

Shared immutable model weights are desirable:

```text
one resident Big model
      |
      +-- context/session A
      +-- context/session B
      +-- context/session C
```

But contexts keep independent:

- session;
- KV/cache;
- Model Form;
- Reasoning;
- temporary controls;
- handoff state.

Retained Clones should be cheap. Active work should drive resource cost.

---

# 51. 14.11I — Fake-Adapter Certification

This phase should provide exhaustive deterministic testing without relying on real Big hardware.

Coverage should include:

- Model Form resolution;
- explicit vs Auto;
- partial registry;
- unavailable form;
- execution-context isolation;
- Task isolation;
- same-form session reuse;
- handoff continuity;
- stale recovery;
- CAS persistence;
- concurrency races;
- rollback;
- ResourceAvailability;
- shared-weight semantics at the Forest identity layer.

No external model is needed for this phase.

---

# 52. 14.11J — Real Small Runtime Certification

Use current Qwen/Hermes Small as the real regression target.

Validate:

- Small registry resolution;
- `platform: api_server`;
- execution-context session identity;
- same-form frozen send;
- Reasoning + Model Form independence;
- stale session recovery;
- no regression in current Hermes path.

Do not require real Big.

Do not replace Qwen before baseline suite is recorded.

---

# 53. 14.11K — Real Big Runtime Boundary Test

Only after:

- runtime can actually support staged Mistral;
- resource/hardware path is safe;
- Big binding is explicitly configured;
- Hermes or alternate adapter supports required continuity behavior.

Minimal boundary test should verify:

```text
Big binding resolves
    ↓
correct runtime starts/loads
    ↓
session created
    ↓
minimal turn executes
    ↓
Forest identity remains Bristlecone
```

Explicit Big unavailable must fail clearly.

Do not remove Small/Qwen as part of a boundary test.

---

# 54. 14.11L — Model Form Benchmark

Benchmark same task suite across Small and Big.

Measure:

- cold TTFT;
- warm TTFT;
- prompt prefill;
- generation speed;
- memory footprint;
- model load;
- session creation;
- handoff overhead;
- continuity bootstrap overhead;
- stale recovery;
- quality;
- coding;
- architecture reasoning;
- visual inspection if applicable;
- tool use;
- resource pressure;
- stability.

Use identical tasks where practical.

Record exact model/runtime/quantization/hardware.

---

# 55. 14.12 — Ollama vs llama.cpp Evaluation

Architecture should make this possible without changing Tree identity.

Evaluate:

```text
model support
Mistral Small 4 support
quantization support
CPU performance
GPU support
context length
session semantics
prefix/KV behavior
cache observability
tooling
API stability
adapter complexity
startup
memory
model residency control
speculative decoding support
```

Core rule:

> **Changing runtime should not require rebuilding Bristlecone's identity, memory, Workshops, or Forest semantics.**

---

# 56. 14.13 — Speculation & Speculative Decoding

Proposed expanded structure:

```text
14.13A — Runtime speculation
          EAGLE / draft decoding

14.13B — Forest-native drafting
          Small -> Big verification

14.13C — Clone speculation
          parallel candidate work

14.13D — Workshop speculation
          safe read-only prefetch/execution

14.13E — Combined test
          Forest speculation
          +
          runtime EAGLE

14.13F — Resource benchmark
          latency / RAM / VRAM /
          CPU / GPU / quality /
          wasted work / stability
```

## 56.1 EAGLE

EAGLE is runtime/token-level speculative decoding.

Conceptually:

```text
EAGLE predicts likely future tokens/features
        ↓
main model verifies
```

Purpose:

```text
reduce generation latency
```

It does not change Tree identity or make the model inherently smarter.

## 56.2 Forest-native drafting

Possible:

```text
Small Bristlecone drafts
        ↓
Big Bristlecone verifies/corrects
```

For coding:

```text
Small:
  inspect likely files
  identify edit locations
  draft patch
  predict tests

Big:
  verify assumptions
  inspect critical code
  correct patch
  approve final
```

## 56.3 Clone speculation

A Clone may perform speculative work, but:

> **A Clone is not a speculative decoder.**

Clone identity is broader than speculation.

## 56.4 Workshop speculation

Potential safe read-only speculative work:

- read file;
- search repository;
- inspect logs;
- run non-destructive tests;
- query service status;
- inspect process state.

Do not speculate destructive or externally consequential actions.

> **Speculation must never become permission speculation.**

---

# 57. Phase 14.14 — Final Benchmark

Final Phase 14 benchmark should integrate:

- reasoning modes;
- Small/Big;
- runtime choice;
- source targeting;
- Hot Context;
- session/prefix reuse;
- speculation if retained;
- resource behavior;
- quality;
- latency;
- RAM/VRAM;
- reliability.

This is the point for a final evidence-based comparison, not before.

---

# 58. Future UI Bones — Do Not Build the Full UI Yet

Current conceptual UI direction:

Chat-bar button opens compact vertical mixer.

First controls:

```text
Reasoning
  Light
  Normal
  Deep

Model Form
  Small
  Big

Auto
  separate policy option
```

Same semantic action registry should support multiple input methods.

Do not make core code depend on:

- UI labels;
- theme names;
- keyboard binding names;
- Forest flavor text.

## 58.1 Delivery selector

Future semantic actions:

```text
Inject
Queue
Interrupt
```

Meaning:

### Queue
Wait for current work.

### Inject
Deliver at a safe checkpoint.

### Interrupt
Safe cancellation/stop behavior.

Prompt transient/persistent behavior should be explicit.

Full UI is not the current implementation target.

---

# 59. Engineering Workflow Rules

Because the project is not Git-backed:

```text
inspect
  ↓
one isolated change
  ↓
timestamped backup
  ↓
compile
  ↓
focused behavior test
  ↓
certify
  ↓
certified backup
  ↓
next change
```

Never:

- blindly rerun a failed installer;
- edit before understanding failure;
- mark code certified because it compiles;
- change multiple transaction responsibilities at once without need;
- invent architecture solely to satisfy a checklist;
- execute source just to inspect imports if AST/static analysis is enough;
- use ambiguous raw anchors if AST structure is available;
- mutate real learning data in architecture tests;
- expose credentials in state/logs/Leaves.

## 59.1 AST/source lessons

### `inspect.getsource`

For class methods:

```python
source = textwrap.dedent(
    inspect.getsource(method)
)
```

before:

```python
ast.parse(source)
```

### Decorators

When inserting relative to a decorated method, preserve the entire decorator boundary.

### Static validation

Prefer executable AST structure over naive text searching when comments/docstrings can contain forbidden words.

## 59.2 Shell safety for Cherry/Maple

Do not paste bare interactive:

```bash
set -euo pipefail
```

or:

```bash
cd ... || exit 1
```

or:

```bash
exit
```

into long interactive terminal blocks.

A prior failure closed the terminal.

If fail-fast is needed, use a subshell/script:

```bash
(
  set -euo pipefail
  ...
)
```

Capture status immediately:

```bash
some_command
status=$?
echo "$status"
```

Do not run another `echo` first and then read `$?`.

## 59.3 Safe dom0 transfer

For long dom0 scripts:

1. create in Cherry/Maple;
2. pull as data into dom0;
3. inspect/hash;
4. only then execute.

Example concept:

```bash
qvm-run --pass-io Cherry-AI \
  'cat /home/user/<script>' \
  > ~/<script>
```

Never pipe less-trusted qube output directly into dom0 shell execution.

---

# 60. Safe Failures and What They Taught Us

## 60.1 Skill-as-base prompt

Failed as architecture because Hermes restored base semantics.

Lesson:

```text
Skills are overlays, not Forest base identity.
```

## 60.2 Wrong optimization target

Prompt/schema/YAML bookkeeping was initially suspected.

Hot-path audit showed the major delay was largely runtime/model-side.

Lesson:

> **Measure before optimizing.**

## 60.3 E4E1 ambiguous raw anchor

Installer found five matching anchors and aborted safely.

Lesson:

```text
AST / structural insertion > ambiguous text replacement
```

## 60.4 E4E2 decorator boundary

First insertion risked attaching `@abstractmethod` to the new optional continuity function.

Structural check caught it.

Lesson:

```text
decorators are part of insertion boundary
```

## 60.5 E4E3B post-create leak

Fresh session could have leaked if adapter mismatch occurred after creation but before binding.

Review found it before certification.

Lesson:

> **Every post-create/pre-bind failure must either preserve old canonical session or clean the fresh unbound child.**

## 60.6 E4E3C1 AST indentation

Recon forgot to dedent method source.

Result:

```text
IndentationError: unexpected indent
```

No mutation.

## 60.7 E4E3C1 `__file__`

Installer executed module source just to inspect imports.

Temporary namespace had no `__file__`.

Result:

```text
NameError: name '__file__' is not defined
```

Failure before write.

Correction:

```text
AST-only import inspection
```

## 60.8 Structural test assumption about sender

A test expected direct:

```python
runtime_adapter.send_turn(...)
```

but code intentionally used:

```python
sender = getattr(runtime_adapter, "send_turn", None)
result = sender(...)
```

Test harness was corrected instead of changing valid production structure.

Lesson:

> **Test behavior/real structure, not an assumed syntax shape.**

---

# 61. Certified Backup and Hash Ledger

## D0

```text
bristlecone/backups/phase14_11D0_certified_20260811T123502Z
```

8 files.

## D5

```text
bristlecone/backups/phase14_11D5_certified_20260811T135122Z
```

8 files.

## E1

```text
bristlecone/backups/phase14_11E1_certified_20260811T135713Z
```

## E2

```text
bristlecone/backups/phase14_11E2_certified_20260811T140259Z
```

## E3

```text
bristlecone/backups/phase14_11E3_certified_20260811T142122Z
```

4 files.

## E4A

```text
bristlecone/backups/phase14_11E4A_certified_20260811T143316Z/task_session.py
```

## E4B

```text
bristlecone/backups/phase14_11E4B_certified_20260811T144133Z/task_session.py
```

## E4C

```text
bristlecone/backups/phase14_11E4C_certified_20260811T144507Z/task_session.py
```

## E4D

```text
bristlecone/backups/phase14_11E4D_certified_20260811T150951Z/task_session.py
```

## E4E1 failed/pre/certified

```text
phase14_11E4E1_pre_handoff_preparation_20260811T151448Z/task_session.py
phase14_11E4E1_pre_handoff_preparation_20260811T151957Z/task_session.py

bristlecone/backups/phase14_11E4E1_certified_20260811T152409Z/task_session.py
```

## E4E2 failed/pre/certified

```text
phase14_11E4E2_pre_continuity_contract_20260811T155602Z/base.py
phase14_11E4E2_pre_continuity_contract_20260811T155737Z/base.py

bristlecone/backups/phase14_11E4E2_certified_20260811T155944Z/base.py
```

SHA256:

```text
e2b002a37b7048fa543876a26c8608154a9707acdb93c378d3a1bdea66b395fb
```

## E4E3A

Pre:

```text
bristlecone/backups/phase14_11E4E3A_pre_typed_passthrough_20260811T160700Z/task_session.py
```

Certified:

```text
bristlecone/backups/phase14_11E4E3A_certified_20260811T161005Z/task_session.py
```

SHA256:

```text
c87c27e6c4b7962754faa6f2fd809f320411805bb91803d93298521ff19d4ab2
```

## E4E3B

Pre:

```text
bristlecone/backups/phase14_11E4E3B_pre_bootstrap_helper_20260811T161227Z/task_session.py
```

Cleanup-fix pre:

```text
bristlecone/backups/phase14_11E4E3B_pre_cleanup_fix_20260811T161420Z/task_session.py
```

Certified:

```text
bristlecone/backups/phase14_11E4E3B_certified_20260811T161700Z/task_session.py
```

SHA256:

```text
bde405826e48e3332a9eff33dd7b3828b1733e3e1f760108a02fd0100348392e
```

## E4E3C1

Pre:

```text
bristlecone/backups/phase14_11E4E3C1_pre_binding_rollback_20260811T162900Z/task_session.py
```

Certified:

```text
bristlecone/backups/phase14_11E4E3C1_certified_20260811T163126Z/task_session.py
```

SHA256:

```text
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c
```

---

# 62. Existing Continuity / Checkpoint Artifact Inventory

Important related artifacts:

```text
The_Forest_Long_Term_Context_Memory_and_Progressive_Retrieval_Checkpoint_2026-08-10.md

McIntosh_Origin_Design_Checkpoint_2026-08-10.md

The_Forest_Model_Form_Clone_and_Resource_Management_Architecture_Checkpoint_2026-08-11_v3.md

The_Forest_Bristlecone_Model_and_Speculation_Checkpoint_2026-08-10_v4.md

The_Forest_Runtime_Session_Identity_and_Clone_Architecture_Checkpoint_2026-08-11.md

The_Forest_Phase14_11E4E1_to_E4E3C1_Checkpoint_2026-08-11.md
```

Known generated sizes from the conversation:

```text
Runtime Session Identity & Clone Architecture:
~10,244 B
~497 lines

E4E1 -> E4E3C1 checkpoint:
13,860 B
```

Historical authoritative engineering archive:

```text
project_forest_bristlecone_full_implementation_history_phase1_to_14_9_2026-08-09.md
```

Other broad context artifacts include:

```text
Project_Forest_PDC_PDF_Master_Context.md
QUBES-PC-SYSTEM-AND-AI-RUNTIME-SNAPSHOT.md
PDC_PDF_FOREST_ALL_RELATED_PROJECTS_MASTER_CONTEXT_2026-08-07.md
bristlecone_forest_complete_continuity_archive_2026-08-09.md
forest_phase14_9_source_context_complete_checkpoint_2026-08-09.md
```

---

# 63. Forest / Hermes / Native Runtime Ownership Cheat Sheet

```text
FOREST OWNS
-----------
Tree identity
Clone / Colony identity
execution-context identity
Workshop meaning
canonical capabilities
canonical Skill IDs
Task identity
Task lifecycle
seasonal state
User Context
Operational Learning
Leaves / Leaf Foliage
permissions / Spirit policy
source identity / structure
turn-local source relevance
final semantic instruction composition
Model Form policy
Reasoning policy
portable continuity
durable state


RUNTIME ADAPTER OWNS
--------------------
runtime-specific capability translation
Hermes configurable toolset names
Hermes Skill implementation names
Hermes config transaction mechanics
Hermes profile secret scope
Hermes API request format
runtime session create/get/send/end
runtime verification
runtime-specific continuity bootstrap implementation
runtime-specific rollback/cleanup mechanics


NATIVE INFERENCE OWNS
---------------------
model process
native KV cache
native prefix/prompt cache
inference execution state
runtime/model session internals not explicitly exposed
Ollama/llama.cpp engine-specific implementation
speculative decoding internals
```

This boundary allows:

```text
replace Hermes
or
replace Ollama
or
replace model
```

without rebuilding Bristlecone identity.

---

# 64. Non-Negotiable Invariants to Protect During E4E3C2 and Later

1. **A Tree is not its model.**
2. Model Form is execution-context local.
3. Reasoning is execution-context local.
4. Deep does not mean Big.
5. Big does not mean Deep.
6. Tree defaults do not broadcast into existing contexts.
7. Explicit Big never silently downgrades.
8. Auto may fallback only under policy.
9. `(execution_context_id, binding_id)` is Forest-side live runtime session identity.
10. Adapter name alone is not session identity.
11. Binding ID alone is not session identity.
12. Shared weights do not mean shared mutable session/KV state.
13. Actual Model Form change creates a semantic handoff.
14. Same-form stale recovery is **not** a Model Form handoff.
15. Runtime session internals are not converted across model architectures.
16. Portable continuity belongs to Forest state.
17. Current user message is not inserted into prior completed continuity.
18. One meaningful turn retrieves/assembles once.
19. Runtime retry reuses frozen instructions.
20. Runtime retry reuses frozen Reasoning.
21. Runtime retry reuses frozen Model Form.
22. Handoff stale replacement must reuse the same ModelFormContinuity.
23. At most one stale recovery.
24. E4D remains the single semantic commit.
25. Failed runtime work does not append conversation.
26. Failed runtime work does not update effective Model Form.
27. Reasoning temporary lease finalizes only after successful semantic commit.
28. Fresh handoff target session remains transactional until semantic commit.
29. Old target session is not retired before semantic success.
30. If Forest semantic commit rejects runtime advancement, Forest truth wins.
31. Rollback must never overwrite a newer concurrent writer.
32. C1 repairs Forest state only.
33. C2 owns runtime-session retirement.
34. Runtime sessions may rotate.
35. Native inference cache remains runtime-owned.
36. Forest cache is derived, not authoritative.
37. Vector/derived memory never grants permission.
38. Source Context is reference data, not instruction authority.
39. Qubes isolation is not traded away for speed.
40. No broad dom0 control for Trees.
41. No credentials in Forest state/logs/Leaves.
42. No blind reruns.
43. Back up source before mutation.
44. Verify behavior before marking complete.
45. Optimize measured bottlenecks, not fashionable features.

---

# 65. Exact Resume Procedure for a New Chat

Use this sequence:

## Step 1 — state current checkpoint

```text
Last certified:
14.11E4E3C1

Current:
14.11E4E3C2

No C2 mutation yet.
```

## Step 2 — confirm certified C1 rollback point

```text
bristlecone/backups/phase14_11E4E3C1_certified_20260811T163126Z/task_session.py
```

SHA:

```text
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c
```

## Step 3 — run compact E4E3C2A recon

Do not reconstruct the pre-send branch from this archive alone.

Recover exact current:

```text
persist_guard assignments
ensured assignment
requested_session_id assignment
top-level IF blocks around pre-turn session acquisition/persistence
```

## Step 4 — only then implement C2A

Goals:

```text
prepare handoff
branch same-form vs handoff
fresh continuity bootstrap
persist target binding before send
clean fresh child if CAS fails
```

Do not yet rewrite stale retry/semantic rollback if C2A is kept isolated.

## Step 5 — compile + synthetic behavior certification

Only if source installs safely.

## Step 6 — certified C2A backup

Then proceed C2B.

---

# 66. Suggested Compact E4E3C2A Recon Shape

The previously proposed compact recon should print approximately:

```text
persist_guard[1]@...
persist_guard[2]@...
ensured[1]@...
requested_session_id[1]@...
IF@...
```

The purpose is not to inspect the whole send method again.

It is specifically to recover the exact current pre-send branch that was missing from the chat transcript.

> **Do not guess this branch.**

---

# 67. Why This Architecture Remains Portable

The work deliberately avoids making the Forest dependent on:

```text
Qwen
Mistral
Hermes
Ollama
llama.cpp
one GPU vendor
one context format
one session format
one UI
```

Forest owns:

```text
identity
meaning
policy
continuity
memory
permissions
state
```

Runtime owns:

```text
execution
session internals
model-specific cache
transport
```

This is why a future switch from Hermes/Ollama remains possible without destroying the Forest.

---

# 68. Broader Resource and Portability Direction

Once Model Form and Clone execution contexts are stable, useful Forest-local resource actions may include:

```text
unload unused models
defer indexing
stop preloading
release expendable caches
pause checkpointable background Clones
resume background Clones
reduce background scheduling priority
query model residency
```

These do not require broad dom0 access.

Qubes-level resource manipulation should remain behind narrow approved adapters.

---

# 69. What Not to Do Next

Do **not**:

- activate staged Big merely because it is downloaded;
- remove Qwen;
- assume Hermes supports continuity bootstrap already;
- patch C2 before recovering the missing pre-send branch;
- merge C2A and C2B into one giant untested edit unless the current source structure proves that separation is impossible;
- let stale retry create an empty handoff replacement session;
- retire old target before semantic commit;
- let rollback overwrite a newer writer;
- re-run 14.10 tests unless its code path is touched;
- optimize 14.7/14.9 microsecond paths without new evidence;
- build the full UI inside 14.11;
- give Resource Steward broad host authority;
- put runtime/vendor names into Tree identity.

---

# 70. Final Current Snapshot

```text
TREE:
Bristlecone Pine

ROLE:
Treewright

CURRENT SMALL:
bristlecone-qwen35:4b-64k
Hermes + Ollama
CPU-only
64K

BIG CANDIDATE:
mistralai/Mistral-Small-4-119B-2603-NVFP4
staged + checksum verified
not loaded
not connected
not activated

HERMES:
primary orchestration layer
api_server required
profile-scoped
session API verified
same-form runtime path working
continuity-bootstrap capability not yet implemented in Hermes adapter

NEWELLE:
paused/optional

LAST CERTIFIED IMPLEMENTATION:
14.11E4E3C1
CAS-aware binding rollback

CURRENT IMPLEMENTATION:
14.11E4E3C2
Frozen handoff transaction integration

CURRENT SOURCE MUTATION STATUS:
none for C2

IMMEDIATE NEXT ACTION:
run compact E4E3C2A pre-send AST recon
to recover exact ensured/persist_guard branching

THEN:
implement E4E3C2A
certify
backup
implement E4E3C2B
certify
backup
run E4E5 end-to-end handoff certification
```

The key rule entering the next edit remains:

> **A runtime handoff becomes authoritative only when Forest successfully commits the corresponding semantic turn.**

Until that point:

> **The fresh target runtime session is transactional.**

---

# 71. Source Inventory Used to Build This Master Checkpoint

This checkpoint consolidates information from the current conversation and prior Forest continuity artifacts, especially:

```text
project_forest_bristlecone_full_implementation_history_phase1_to_14_9_2026-08-09.md

Project_Forest_PDC_PDF_Master_Context.md

QUBES-PC-SYSTEM-AND-AI-RUNTIME-SNAPSHOT.md

The_Forest_Long_Term_Context_Memory_and_Progressive_Retrieval_Checkpoint_2026-08-10.md

The_Forest_Bristlecone_Model_and_Speculation_Checkpoint_2026-08-10_v2 / later v4 context

The_Forest_Model_Form_Clone_and_Resource_Management_Architecture_Checkpoint_2026-08-11_v3.md

The_Forest_Runtime_Session_Identity_and_Clone_Architecture_Checkpoint_2026-08-11.md

The_Forest_Phase14_11E4E1_to_E4E3C1_Checkpoint_2026-08-11.md

current terminal recon / certification output for E4E3A, E4E3B, E4E3C1, and E4E3C2 landmarks
```

Authority remains:

```text
later verified terminal result
    >
later certified checkpoint
    >
older architecture checkpoint
    >
historical plan
```

Planned/representative structures in older files should not override currently certified code.

---

# 72. One-Line Handoff for Another AI

If only one paragraph can be carried forward:

> **Continue The Forest / Bristlecone Pine at Phase 14.11E4E3C2. E4E3C1 CAS-aware binding rollback is certified at `bristlecone/backups/phase14_11E4E3C1_certified_20260811T163126Z/task_session.py`, SHA256 `c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c`. No C2 source mutation has happened. Before editing, run the compact C2A pre-send AST recon because the exact `ensured` / `persist_guard` branch was not captured in chat. Then wire actual Model Form handoff to exact typed `ModelFormContinuity`, fresh target-session bootstrap, CAS persistence before send, continuity-aware one-shot stale recovery, E4D single semantic commit, and C1 rollback + safe runtime retirement on semantic failure. Preserve same-form D5 byte-for-byte where possible. Hermes is primary, requires `platform: api_server`, and currently inherits the fail-closed `create_session_with_continuity` default, so fake-adapter handoff certification comes before real Hermes/Big. Do not activate staged Mistral or remove Qwen yet.**

