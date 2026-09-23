# Bristlecone Pine / The Forest — Complete Continuity Archive
**Checkpoint:** 2026-08-08, approximately 8:19 PM America/New_York  
**Environment:** Cherry-AI on Qubes OS  
**Current runtime:** Hermes + Ollama  
**Current model:** `bristlecone-qwen35:4b-64k`  
**Immediate next task:** isolate Hermes-specific code behind a Forest runtime adapter before adding more permanent session logic.

---

# RESUME FROM HERE

The current work has reached a clean architectural boundary.

Already verified:

- Forest-owned Task Session lifecycle.
- Atomic/disposable/live Task persistence.
- Task-Sticky Skill overlays.
- Separate temporary Skill overlays.
- Independent Skill caching and task-boundary cache cleanup.
- Temporary capability authorization/resolution/planning.
- Live Hermes temporary toolset/context transactions.
- Exact Hermes baseline restoration.
- Unified temporary-turn context manager.
- Normal-path and exception-path restoration.
- `runtime_sessions` Forest schema and lifecycle.
- Hermes persisted-session API behavior.
- Hermes session IDs can rotate.
- Live Bristlecone API endpoint.
- Hermes profile-secret-scope authentication.
- Real Forest Task ↔ real Hermes persisted-session binding.
- Disposable Hermes session lookup and cleanup.

The next implementation step is **not** more Hermes code inside `task_session.py`.

Create:

```text
runtime/
├── __init__.py
├── task_session.py
└── adapters/
    ├── __init__.py
    ├── base.py
    └── hermes.py
```

The Forest should express **what** it needs. `HermesRuntimeAdapter` should know **how Hermes does it**.

---

# 1. Project Identity

## The Forest

The Forest is the broader local-first AI architecture. Major goals:

- local-first and offline-capable;
- human-readable canonical state;
- Obsidian-compatible where practical;
- free/open-source/self-hosted components where practical;
- modular Trees with different roles;
- replaceable models, inference engines, agent frameworks, and UI layers;
- canonical knowledge/state separated from disposable caches and derived indexes;
- minimal model-visible context;
- portable architecture that survives replacing Hermes, Ollama, llama.cpp, or another runtime.

## Bristlecone Pine

**Role:** Treewright.

Bristlecone is the emergency multi-model development Tree used to design, train, code, test, debug, correct, and maintain Cherry, Maple, future Trees, plugins, and Forest add-ons.

Operational phrase: **“Pine is fine.”**

---

# 2. User Technical Preferences

For terminal/technical work:

- Explain commands as teaching material.
- Explain the command name, flags/options, paths/arguments, and expected result.
- Prefer one meaningful step, then inspect output.
- Do not mark a step complete without verification.
- Keep observed benchmark data separate from estimates.
- Prefer local-first, open-source, self-hosted, and free solutions where practical.
- In technical chats, interpret “wine” as “Qubes” because phone autocorrect may replace Qubes.
- Warn early if conversation context may become risky and create Markdown continuity archives before continuity is lost.
- Do not call the newer cache/invalidation architecture “canopy.” Use **Layered Reuse and Selective Rebuild** or **Layered Hot Context**.
- Older “Minimum Useful Canopy” wording may exist historically, but it should not name the newer reuse/invalidation architecture.

---

# 3. Host and Qubes Context

Primary OS:

- Qubes OS
- XFCE + i3
- kitty
- zsh
- oh-my-zsh
- Powerlevel10k

Relevant qubes:

- **Cherry-AI** — main AI qube; Hermes + Ollama; Bristlecone lives here.
- **Maple** — personal developer/project/training/reviewer qube.
- **Seed-AI** — lighter training clone.

---

# 4. Runtime and Model

Installed/used:

- Hermes
- Ollama
- Podman
- Newelle, now paused/optional
- llama.cpp is a future comparison candidate

Primary orchestration/interface: **Hermes**.

Current model:

```text
bristlecone-qwen35:4b-64k
```

Approximate size:

```text
~5.6 GB
```

Ollama/Hermes:

- autostart works;
- keep-alive works;
- model keep-alive is 15 minutes;
- manual unload:

```bash
ollama stop bristlecone-qwen35:4b-64k
```

---

# 5. Benchmark History

## Older Hermes toolset benchmarks

Reasoning `none`:

| Toolsets | Observed |
|---|---:|
| `file,terminal` | ~41 sec |
| `file,terminal,todo` | 1:49.64 |
| `file,terminal,skills` | 2:42.40 |
| `file,terminal,skills,todo` | 2:49.16 |

Finding: increasing active tool schemas/Skills significantly increased latency.

## Minimal Workshop cold tests

- Design first output: ~2:52
- Code/Debug first output: 3:12
- Code/Debug finished: 5:42
- Research first output: 2:44
- Model first output: 3:04
- Model finished: 11:49

Cold first-output average: ~2:58, range 2:44–3:12.

Interpretation: after tool-bloat reduction there still appears to be a major cold runtime/model-load component.

## Warm follow-up

- 30.58 sec first output
- 43.72 sec
- 2.23 sec
- total 1:16.54

Strong evidence that cold model/runtime loading is a major latency component.

## Newelle

- Run 1: 5:25.65 before output
- Run 2: stopped after ~15m with no answer
- Run 3: welcome/suggestion prompts at 5:42.23 but no Bristlecone answer

Conclusion: Hermes remains primary; Newelle is paused.

---

# 6. Three Independent Axes

## Reasoning Mode
- Light
- Normal
- Deep

Older notes may say Quick / Normal / Deep.

## Workshop
1. Research
2. Design
3. Code / Debug
4. Model

There is no separate System/Debug Workshop.

## Model Form
- Small / Windowed
- Big / Fullscreen

These axes are independent.

Examples:

```text
Light + Code/Debug + Small
Deep + Code/Debug + Small
Normal + Code/Debug + Big
Deep + Code/Debug + Big
```

Optimize Small/Windowed first. Big/Fullscreen is later escalation/reviewer capacity.

---

# 7. Workshops

## Research
CORE:

```text
web
```

## Design
CORE:

```text
memory
clarify
```

## Code / Debug
CORE:

```text
file
terminal
```

READY:

```text
code-execution
debugging
testing
special
```

## Model
CORE:

```text
file
terminal
```

READY:

```text
model-evaluation
model-benchmarking
model-inference
quantization
training
runtime-inspection
```

## General Ready

```text
todo
clarify
session
memory
leaf
```

General Ready does not mean always loaded. Ready capabilities are individually addressable.

---

# 8. Capability Registry

Canonical file:

```text
~/The-Forest/bristlecone/capabilities/registry.yaml
```

Known capabilities:

General:
- `todo` — toolset
- `clarify` — toolset
- `session` — context
- `memory` — context
- `leaf` — context, unresolved runtime support

Specialized:
- `web` — toolset
- `file` — toolset
- `terminal` — toolset
- `code-execution` — toolset
- `debugging` — Skill
- `testing` — Skill
- `special` — capability
- `model-evaluation` — Skill
- `model-benchmarking` — Skill, unresolved
- `model-inference` — Skill
- `quantization` — Skill, unresolved
- `training` — Skill, unresolved
- `runtime-inspection` — capability, unresolved

Policy includes individual activation, no full-group activation by default, and injection only when active.

---

# 9. Existing Hermes Mapping YAML

File:

```text
~/The-Forest/bristlecone/adapters/hermes.yaml
```

Mappings include:

```text
todo → todo
clarify → clarify
session → session_search
memory → memory
web → web
file → file
terminal → terminal
code-execution → code_execution
debugging → systematic-debugging
testing → test-driven-development
model-evaluation → evaluation
model-inference → inference
```

Unresolved:

```text
leaf
special
model-benchmarking
quantization
training
runtime-inspection
```

`leaf` remains unresolved until Forest-native Leaf Foliage support exists.

The YAML should remain the **mapping/configuration** side. The future Python runtime adapter should become the **operational translation** side.

---

# 10. Hermes Configurable Toolsets

Verified Hermes configurable toolsets include:

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

This confirmed that Forest `toolset` and Forest `context` kinds can both be handled through the Hermes configurable-toolset transaction. Forest Skills use prompt overlays instead.

---

# 11. Capability State and Context Architecture

States:

- Dormant
- Active
- Task-Sticky
- Core

Cold/Warm/Hot concept:

**Cold:** persistent Tree on disk: Workshops, Skills, identity, permissions, routing, learning, Leaves, canonical configuration.

**Warm:** parsed manifests, registries, mappings, indexes, prepared objects, Skill metadata in RAM. Warm does not mean model-visible.

**Hot:** current Workshop Core + currently active/Task-Sticky/temporary capabilities + relevant Leaves + task.

Current reuse architecture name:

**Layered Reuse and Selective Rebuild**

Also acceptable:

**Layered Hot Context**

---

# 12. Workshop / Skill Finder

Fallback order:

1. current Core
2. current Ready
3. search Tree-owned tiny manifests
4. compare other Workshop manifests
5. Open Workbench / broad Tree-owned capabilities as last resort

Never fully load all Workshops merely to inspect them.

---

# 13. Operational vs Knowledge Learning

Knowledge learning covers Leaves/memory about user/project/world/procedures.

Operational learning tracks patterns such as:

```text
task pattern
→ initial Workshop
→ successful Workshop
→ Skills used
→ unnecessary Skills
→ fallback path
→ outcome
```

Preferred portable source: JSONL.

Derived SQLite indexes are rebuildable/disposable.

---

# 14. Leaf Foliage Direction

Leaf Foliage should be:

- local-first;
- offline-capable;
- human-readable;
- Obsidian-compatible where practical;
- represented by Markdown leaves with stable IDs/metadata and wiki/Markdown links;
- supported by derived indexes/graphs instead of loading everything into model context.

Support importing/attaching existing Obsidian vaults without destructive conversion, exporting ordinary Markdown, optional links/backlinks, and portable “potted” selections for other devices.

---

# 15. Portability Boundary

Forest-owned:

- identity
- Workshops
- capability registry
- Skills
- Leaves
- permissions
- routing
- operational learning
- portable state
- Forest Task Session policy/lifecycle
- Layered Reuse and Selective Rebuild semantics

Runtime-specific:

```text
Forest
  ↓
runtime adapter
  ↓
Hermes / future runtime
  ↓
Ollama / llama.cpp / future inference
```

Current canonical IDs are still somewhat Hermes-shaped (`file`, `terminal`, etc.). A later Forest naming pass should rename the Forest layer while adapters preserve Hermes technical names underneath.

---

# 16. Canonical Paths

Tree root:

```text
/home/user/The-Forest/bristlecone
```

Hermes profile:

```text
/home/user/.hermes/profiles/bristlecone
```

Known Tree directories:

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

Current runtime package:

```text
runtime/__init__.py
runtime/task_session.py
```

The actual `__init__.py` filename was previously verified despite Markdown sometimes rendering it strangely.

---

# 17. Controller and Hermes Coupling

Controller:

```text
~/The-Forest/bristlecone/bin/bristlecone-workshop.py
~/The-Forest/bristlecone/bin/bristlecone-workshop
```

Existing Hermes imports include:

```python
from hermes_cli.config import load_config, save_config
from hermes_cli.tools_config import _save_platform_tools, CONFIGURABLE_TOOLSETS
```

`_save_platform_tools` is an internal/private Hermes API and should be isolated behind the future Hermes runtime adapter.

The live baseline recently verified was:

```text
file
terminal
```

---

# 18. Phase 1 — Task-Sticky Skills

Phase 1 is complete.

Known Hermes Skill overlay sizes:

```text
systematic-debugging: 14,510 chars
test-driven-development: 10,753 chars
```

Rejected approach: Skill-as-base prompt. Hermes restored base semantics, so it did not persist as intended.

Correct approach: Hermes `instructions` / ephemeral system prompt overlay. Forest builds/caches the Skill text and reapplies only when relevant.

Important benchmark observations to preserve:

- failed Skill-as-base Turn 1: 326.1s, input 5287, output 491, total 5778
- failed Skill-as-base Turn 2: 191.3s, input 5610, output 462, total 6072
- valid overlay: 279.13s, input 8827, output 278, total 9105
- sticky reuse T1: 197.99s, input 8823, output 419, total 9242
- sticky reuse T2: 307.33s, input 9140, output 810, total 9950
- clean no-Skill: 187.81s, input 5288, output 238, total 5526
- deactivation active: 183.71s, input 8826, output 187
- deactivation inactive: 118.02s, input 5323, output 204
- state-driven: 291.78s, input 8492, output 334, total 8826

Do not draw strong final performance conclusions yet. Forest caching avoids repeated discovery/read/parse/build, but the model still receives Skill text on relevant turns. KV/prefix reuse is not proven.

---

# 19. TaskSessionManager

Current implementation:

```text
/home/user/The-Forest/bristlecone/runtime/task_session.py
```

Known class:

```text
TaskSessionManager
```

Known error:

```text
TaskSessionError
```

Current responsibilities include both Forest-owned logic and Hermes-specific mechanics. That is what the adapter extraction will correct.

Current normalized shape:

```yaml
task_session:
  id: null
  status: inactive
  started_at: null
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

---

# 20. Atomic Persistence

State persistence uses an atomic write:

- temp file in same directory
- YAML serialization
- flush
- fsync
- `os.replace`

Persistence defaults to off.

Disposable and live persistence tests passed.

---

# 21. Temporary Capability Resolver and Authorization

Resolver classifies:

```text
all
toolsets
contexts
skills
capabilities
```

Verified:

```text
todo → toolset → Hermes todo
memory → context → Hermes memory
testing → Skill → test-driven-development
```

`leaf` is safely rejected because runtime support is unresolved.

Authorization rules:

- Workshop Core → already active
- General Ready → authorized
- current Workshop Ready → authorized
- anything else → denied

For Code/Debug:

```text
todo → AUTHORIZED via general_ready
testing → AUTHORIZED via workshop_ready
file → ALREADY ACTIVE via workshop_core
web → DENIED
model-evaluation → DENIED
```

Authorization and resolution are intentionally separate.

---

# 22. Temporary Activation Planner

`plan_temporary_activation(...)`:

- authorizes requests;
- excludes already-active Core capabilities;
- resolves allowed additions;
- combines resolved toolsets + contexts into `runtime_toolsets`;
- leaves Skill bindings separate.

Verified plan for:

```text
todo
memory
testing
file
```

produced runtime toolsets `todo`, `memory`, Skill `testing → test-driven-development`, and no redundant `file` activation.

---

# 23. Temporary Hermes Toolset Transaction

Implemented methods currently include:

```text
_load_hermes_toolset_runtime
_hermes_configurable_toolsets
begin_temporary_runtime_toolsets
restore_temporary_runtime_toolsets
```

Behavior:

- validate Hermes runtime/profile/platform;
- read exact baseline;
- compute baseline + requested temporary additions;
- back up Hermes config;
- apply with Hermes config APIs;
- reload/verify;
- restore exact baseline afterward;
- rollback from backup on failure;
- leave Forest state untouched.

Verified live example:

Before:

```text
file
terminal
```

Inside:

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

Known temporary config backup example:

```text
/home/user/The-Forest/bristlecone/backups/hermes-temporary/config-20260808T235043-389581Z.yaml
```

Current limitation: this assumes one short-lived Bristlecone transaction owns the configurable-toolset set. Add generation/ownership protection later for multi-system concurrency.

---

# 24. Separate Temporary Skill Layer

Caches:

```text
_skill_overlay_cache
_temporary_skill_overlay_cache
```

Counters:

```text
_overlay_build_count
_temporary_overlay_build_count
```

Added:

```text
prepare_temporary_skill_overlay
prepare_turn_skill_overlay
```

Verified behavior:

Turn requesting temporary `testing` while `debugging` is Task-Sticky:

```text
Canonical: debugging, testing
Runtime: systematic-debugging, test-driven-development
```

Repeat of same turn shape reuses both caches.

Next turn with no temporary capability:

```text
Canonical: debugging
Runtime: systematic-debugging
Temporary prompt chars: 0
```

Task end discarded both cache entries.

`active.yaml` remained unchanged.

Cached temporary Skill text is not equivalent to active/injected Skill text.

---

# 25. Unified Temporary Turn

Added context manager:

```text
temporary_turn(...)
```

Requires an active Forest Task ID.

Flow:

```text
authorize + resolve
→ build Skill layers
→ begin Hermes temporary toolsets
→ yield turn
→ finally restore exact Hermes baseline
```

Normal-path test passed.

Exception-path test deliberately raised:

```text
FOREST_TEST_EXCEPTION
```

Inside before failure:

```text
file
memory
terminal
todo
```

After exception:

```text
file
terminal
```

Exact baseline restoration, removal of temporary additions, and unchanged `active.yaml` all passed.

---

# 26. runtime_sessions Schema and Lifecycle

Forest Task schema now supports:

```yaml
runtime_sessions:
  hermes:
    session_id: ...
    previous_session_id: ...
    updated_at: ...
```

Missing `runtime_sessions` defaults to `{}`, preserving backward compatibility.

Task start initializes `{}`.

Task end:

- copies current runtime mappings into `retired_runtime_sessions`;
- clears active runtime mapping;
- returns retired mapping for later runtime cleanup.

Lifecycle test with simulated IDs passed:

```text
api_test_current
api_test_previous
```

Normalization preserved them; Task end cleared active mapping and returned the retired values; `active.yaml` stayed unchanged.

---

# 27. Hermes Session Architecture

Hermes owns its session IDs.

Hermes can:

- create new sessions;
- resume existing sessions;
- store history in SessionDB;
- end/delete sessions;
- rotate session IDs, including during compression.

Therefore:

```text
Forest Task ID = stable canonical identity
Hermes session ID = mutable runtime pointer
```

Do not bind the two identities together.

Recommended Forest shape:

```yaml
runtime_sessions:
  hermes:
    session_id: CURRENT
    previous_session_id: OLD
    updated_at: ...
```

---

# 28. Hermes Persisted-Session API

Confirmed endpoints include:

```text
POST /api/sessions
GET /api/sessions/{session_id}
PATCH /api/sessions/{session_id}
DELETE /api/sessions/{session_id}
GET /api/sessions/{session_id}/messages
POST /api/sessions/{session_id}/fork
POST /api/sessions/{session_id}/chat
POST /api/sessions/{session_id}/chat/stream
POST /api/sessions/{session_id}/model
```

Create-session accepts `id` or `session_id`; otherwise Hermes generates one.

Persisted chat:

- loads stored history;
- runs with the session ID;
- returns `effective_session_id`;
- returns session ID in JSON;
- returns `X-Hermes-Session-Id`.

Preferred Forest path: dedicated persisted-session chat rather than generic header continuation.

---

# 29. Live API Endpoint

Verified live Bristlecone gateway:

```text
hermes -p bristlecone gateway run
```

Listening:

```text
127.0.0.1:8643
```

Current base:

```text
http://127.0.0.1:8643
```

Because pasted URLs may be Markdown-mangled, safer Python construction is:

```python
API_BASE = "http://" + "127.0.0.1:8643"
```

---

# 30. Hermes Authentication and Secret Scope

Hermes API uses:

```text
API_SERVER_KEY
```

Source inspection showed the server refuses to start without a valid key.

PID inspection found the key is not simply present in the gateway process environment.

Hermes instead has profile-scoped credential resolution:

```text
agent.secret_scope
```

Important functions:

```text
build_profile_secret_scope
set_secret_scope
reset_secret_scope
current_secret_scope
get_secret
```

Hermes gateway also uses:

```text
gateway.run._profile_runtime_scope
```

This installs profile-local runtime context and profile secret scope, then restores it afterward.

`_profile_runtime_scope` is private/internal Hermes API and should be hidden behind the new Hermes runtime adapter.

Never store/print/copy `API_SERVER_KEY` into Forest state, Leaves, logs, or canonical configuration.

---

# 31. Secret-Scope Probe

Verified:

Before:

```text
Scope active: False
```

Inside Bristlecone profile runtime scope:

```text
Scope active: True
API_SERVER_KEY resolved: True
API key displayed: NO
```

After:

```text
Scope active: False
```

Both checks passed.

---

# 32. Real Forest ↔ Hermes Session Binding

A first attempt failed safely because a standalone `_get_scoped_secret()` call lacked the proper profile scope. No network request occurred and no session was created.

Corrected test used:

```text
_profile_runtime_scope
+
get_secret
```

Started Forest Task:

```text
forest-task-20260809T000736Z-0013c37e
```

Created real persisted Hermes session:

```text
HTTP 201
api_1786234056_203cb1ee
```

Forest mapping:

```text
Forest Task ID:
forest-task-20260809T000736Z-0013c37e

Hermes Session ID:
api_1786234056_203cb1ee

Previous Hermes ID:
None
```

Session lookup:

```text
HTTP 200
```

Returned ID matched.

All checks passed.

Finally the disposable Hermes session was deleted successfully.

`active.yaml` remained unchanged. Hermes configuration remained unchanged.

---

# 33. Self-Reliance Review and Adapter Decision

Forest architecture is already mostly self-reliant, but `task_session.py` still knows too much Hermes-specific implementation detail.

Forest-owned:

- Task IDs
- Task lifecycle
- Workshops
- capability registry
- Task-Sticky policy
- temporary capability policy
- runtime-session mapping
- cache lifecycle
- canonical state
- learning/Leaf architecture
- Tree identity

Too Hermes-specific in current core:

- Hermes config loading
- `_save_platform_tools`
- `CONFIGURABLE_TOOLSETS`
- Hermes Skill prompt construction
- Hermes profile scope
- Hermes API details
- future Hermes session calls

Decision:

**Isolate Hermes behind a Forest runtime adapter now.**

Simple model:

```text
The Forest
    ↓
Forest runtime contract
    ↓
Hermes runtime adapter
    ↓
Hermes
```

If Hermes changes, update the adapter. If Hermes is replaced, create another adapter.

---

# 34. Target Adapter Structure

```text
runtime/
├── __init__.py
├── task_session.py
└── adapters/
    ├── __init__.py
    ├── base.py
    └── hermes.py
```

`base.py` should define the smallest Forest-facing runtime contract necessary.

Potential operations:

```text
verify_runtime
get_active_toolsets
begin_temporary_toolsets
restore_temporary_toolsets
build_skill_overlay
create_session
get_session
send_turn
end_session
```

Do not overdesign the interface before moving already-proven behavior.

`hermes.py` should own Hermes paths, imports, private APIs, config, secret scope, HTTP API, session behavior, verification, and compatibility handling.

---

# 35. Latest Hermes Coupling Inventory

Latest read-only scan of `runtime/task_session.py` found:

```text
571  _load_hermes_toolset_runtime
686  _hermes_configurable_toolsets
711  begin_temporary_runtime_toolsets
850  restore_temporary_runtime_toolsets
933  _build_hermes_skill_overlay
1175 prepare_temporary_skill_overlay
1297 prepare_turn_skill_overlay
```

Other adapter-name checks exist around Skill handling.

Current runtime package contains only:

```text
__init__.py
task_session.py
```

No runtime adapter package has been created yet.

This is the exact implementation checkpoint.

---

# 36. Extraction Plan

Do this gradually; do not rewrite everything at once.

1. Create `runtime/adapters/`.
2. Create `runtime/adapters/__init__.py`.
3. Create `runtime/adapters/base.py`.
4. Create `runtime/adapters/hermes.py`.
5. Define a minimal runtime contract.
6. Extract Hermes runtime verification/config-loading logic.
7. Extract configurable-toolset inspection/transaction.
8. Keep compatibility wrappers temporarily if necessary.
9. Re-run unified temporary-turn normal test.
10. Re-run exception restoration test.
11. Extract `_build_hermes_skill_overlay`.
12. Keep Forest cache and policy logic in TaskSessionManager.
13. Re-run sticky/temporary Skill tests.
14. Move profile-scope authentication into Hermes adapter.
15. Add adapter-owned `create_session`, `get_session`, `send_turn`, `end_session`.
16. Make TaskSessionManager depend on the runtime interface rather than Hermes.
17. Add persistent Forest↔Hermes mapping.
18. On each turn, compare returned effective Hermes session ID with current mapping.
19. If rotated: previous = old, current = new, update timestamp.
20. Use `retired_runtime_sessions` for runtime cleanup when Forest Task ends.
21. Add multi-system/generation/ownership protection to runtime mutation.
22. Build a unified Phase 2 end-to-end verifier.

---

# 37. Current Phase 2 Checklist

Completed:

- [x] Canonical Skill state
- [x] Adapter mapping resolution
- [x] Task-Sticky overlay generation/cache
- [x] Build-once cache
- [x] Selective rebuild
- [x] Forest Task Session IDs
- [x] start/end lifecycle
- [x] task-boundary sticky cache disposal
- [x] atomic persistence
- [x] disposable persistence verification
- [x] live lifecycle persistence
- [x] temporary capability kind classification
- [x] temporary runtime resolution
- [x] safe unresolved rejection
- [x] General Ready/Workshop Ready authorization
- [x] authorization verification
- [x] temporary activation planner
- [x] Hermes configurable-toolset semantics
- [x] live temporary toolset/context transaction
- [x] exact automatic restoration
- [x] temporary Skill layer
- [x] debugging+testing composition
- [x] next turn drops testing
- [x] temporary Skill cache reuse
- [x] task-end clears both Skill caches
- [x] unified temporary-turn helper
- [x] normal-path verification
- [x] exception-path restoration
- [x] `runtime_sessions` schema
- [x] `runtime_sessions` lifecycle
- [x] Hermes persisted-session API discovery
- [x] Hermes session rotation discovery
- [x] live API endpoint discovery
- [x] Hermes profile secret-scope discovery
- [x] secret-scope verification
- [x] real Forest↔Hermes persisted-session binding
- [x] disposable session lookup/cleanup
- [x] decision to isolate Hermes runtime adapter
- [x] inventory current Hermes coupling

Next:

- [ ] create runtime adapter package
- [ ] define Forest runtime interface
- [ ] extract Hermes toolset handling
- [ ] regression-test temporary-turn behavior
- [ ] extract Hermes Skill builder
- [ ] regression-test Skill behavior
- [ ] extract profile-scope/API authentication
- [ ] add session API methods to Hermes adapter
- [ ] make TaskSessionManager runtime-agnostic
- [ ] persist runtime-session mapping
- [ ] verify repeated turn reuse
- [ ] verify effective-ID rotation
- [ ] retire/end Hermes session
- [ ] add concurrency/generation protection
- [ ] unified verifier
- [ ] Phase 2 end-to-end verification

---

# 38. Important Backups

Known runtime backups from this work include:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194150.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194223.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194745.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194928.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-195210.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-195349.py
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-200134.py
```

Known state/config backups include:

```text
/home/user/The-Forest/bristlecone/backups/task-state/active-20260808-193231.yaml
/home/user/The-Forest/bristlecone/backups/hermes-temporary/config-20260808T235043-389581Z.yaml
```

This list may not be exhaustive.

---

# 39. Previous Generated Project Markdown Files

Known previous artifacts:

1. `bristlecone_workshops_reasoning_model_forms_plan_and_rejected_concepts.md`
2. `forest_minimum_useful_canopy_and_tree_workshops.md`
3. `forest_workshop_skill_finder_and_operational_learning_architecture.md`
4. `forest_portable_tree_runtime_and_high_speed_workshop_architecture.md`
5. `bristlecone_capability_registry_and_individual_tool_activation.md`
6. `bristlecone_task_sessions_and_session_sticky_skills_update.md`
7. `bristlecone_skill_session_implementation_decision.md`
8. `bristlecone_layered_hot_context_and_task_session_cache_update.md`

A prior comprehensive continuity attempt named approximately `bristlecone_workshop_runtime_continuity_and_infrastructure_plan_2026-08-08.md` failed during creation and should not be assumed to exist.

---

# 40. Key Rules When Continuing

- Back up before patching.
- Use structural match guards.
- Abort on unexpected match counts.
- Syntax-check before writing.
- Test in memory first where possible.
- Verify before persisting.
- Restore Hermes runtime mutations in `finally`.
- Keep credentials out of Forest state/logs/output.
- Keep Forest Task identity separate from runtime session identity.
- Hide Hermes private APIs behind the adapter.
- Preserve already-passing regression tests.
- Do not spread runtime-specific branches through Forest core.
- Do not mark a milestone complete without terminal verification.
- Keep observed measurements distinct from estimates.

---

# 41. Final Architecture Principle

The Forest owns meaning.

The adapter owns translation.

Hermes is replaceable.

Bristlecone remains Bristlecone even if the runtime underneath it changes.

```text
THE FOREST
    ↓
Forest runtime contract
    ↓
runtime adapter
    ↓
Hermes / llama.cpp / future runtime
```

**Resume by creating the adapter package and extracting Hermes toolset behavior first.**
