# Bristlecone Pine Workshop Runtime
## Continuity Packet, Current Configuration, Verified Infrastructure, and Next Steps

**Project:** The Forest / Bristlecone Pine  
**Tree role:** Treewright  
**Current runtime stack:** Qubes OS → Cherry-AI qube → Hermes Agent → Ollama → Bristlecone model  
**Current live Hermes profile:** `bristlecone`  
**Current live gateway platform:** `api_server`  
**Date:** 2026-08-08  
**Status:** Core Workshop tool switching is live and verified end-to-end.

---

# 1. Purpose of This Work

This phase redesigned Bristlecone Pine's capability/tool architecture so that:

1. Bristlecone does **not** carry every tool, Skill, context provider, and capability in model context at all times.
2. Capabilities are activated only when needed.
3. Tool activation can happen dynamically without restarting Hermes.
4. General capabilities and task-specific capabilities can be active simultaneously without activating entire groups.
5. Bristlecone's canonical architecture remains **Forest-owned and portable**, instead of becoming dependent on Hermes naming or Hermes internals.
6. Switching inference runtimes later, such as Ollama → llama.cpp, should not require redesigning the Workshop architecture.
7. Switching agent/orchestration platforms later should require a **new adapter**, not a redesign of Bristlecone's identity, Workshops, Leaves, or capability registry.

This work directly supports the **Minimum Useful Canopy** principle:

> Keep Cold large, Warm small, and Hot tiny. Expose only the tools, Skills, knowledge, permissions, and context needed for the current task.

---

# 2. Why This Architecture Was Needed

Earlier Bristlecone performance testing showed large latency differences as tool schemas were added.

Previously observed examples:

- `file + terminal` ≈ 41 seconds in an earlier Hermes benchmark.
- `file + terminal + todo` = 1 minute 49.64 seconds.
- `file + terminal + skills` = 2 minutes 42.40 seconds.
- `file + terminal + skills + todo` = 2 minutes 49.16 seconds.

Later minimal Workshop cold tests showed a roughly 3-minute cold first-output floor, while warm runs could drop dramatically, including a warm first output around 30.58 seconds and later warm responses as low as a few seconds.

This led to two separate optimization targets:

- **Cold/runtime/model loading overhead**
- **Prompt/tool/Skill schema overhead**

The Workshop system addresses the second category by reducing what Bristlecone sees at any one time.

---

# 3. Final Architectural Model So Far

Bristlecone now uses three independent control axes.

## 3.1 Reasoning Mode

Controls reasoning effort only.

Current conceptual values:

- Light
- Normal
- Deep

Current state file uses:

```yaml
reasoning: light
```

Reasoning Mode is independent from Workshop and Model Form.

## 3.2 Workshop

Controls the capability/tool/Skill boundary for the task.

Current Workshops:

1. Research
2. Design
3. Code / Debug
4. Model

There is **no fifth System Workshop** and no separate Debug Workshop. Debugging belongs inside Code / Debug.

## 3.3 Model Form

Controls the underlying model/runtime form independently from the Workshop.

Current conceptual values:

- Small / Windowed
- Big / Fullscreen

Current state file uses:

```yaml
model_form: small
```

Examples of valid future combinations:

- Light + Code/Debug + Small
- Deep + Code/Debug + Small
- Normal + Code/Debug + Big
- Deep + Code/Debug + Big

The Tree identity remains above the model so the underlying model can be replaced.

---

# 4. Canonical Forest Portability Boundary

The architecture is intentionally split into Forest-owned and runtime-specific layers.

```text
TREE / FOREST-OWNED
────────────────────────────────
identity
Workshops
capability registry
Leaves
permissions
routing
operational learning
reasoning mode
model form
portable state

        │
        │ portability boundary
        ▼

RUNTIME ADAPTER
────────────────────────────────
Hermes adapter today
future runtime adapter later

        │
        ▼

EXECUTION / ORCHESTRATION
────────────────────────────────
Hermes today
future agent framework later

        │
        ▼

INFERENCE
────────────────────────────────
Ollama today
llama.cpp possible later
other inference runtime later
```

Important consequences:

- Ollama → llama.cpp should mostly affect runtime/model tuning.
- Hermes → another agent framework should require a new adapter and activation mechanism.
- The four Workshops should **not** need to be redesigned.
- Forest-native services such as Leaf Foliage should eventually live above Hermes.

---

# 5. Canonical Bristlecone Filesystem

Canonical Tree root:

```text
~/The-Forest/bristlecone
```

Hermes-specific runtime/profile state:

```text
~/.hermes/profiles/bristlecone
```

Important Forest directories currently used or created:

```text
~/The-Forest/bristlecone/
├── adapters/
├── backups/
│   ├── hermes-config/
│   └── workshops-before-registry/
├── bin/
├── capabilities/
├── corpus/
├── learning/
├── logs/
├── routing/
├── skills/
├── state/
└── workshops/
```

Existing historical Bristlecone files also include:

```text
AGENTS.md
API-ARCHITECTURE.md
FIRST-CONVERSATION.txt
Modelfile.qwen35-4b-64k
NEWELLE-CONNECTION.txt
NEWELLE-PROFILE-INSTRUCTIONS.txt
seed-manifest.json
```

---

# 6. Central Capability Registry

A central capability registry was created at:

```text
~/The-Forest/bristlecone/capabilities/registry.yaml
```

The registry defines capabilities **once**.

Workshops no longer redefine capability kind/type metadata. They only reference canonical capability IDs.

Old-style duplication:

```yaml
- id: file
  kind: toolset
```

New Workshop reference:

```yaml
core:
  - file
  - terminal
```

This reduces duplication and makes future runtime/name migrations easier.

---

# 7. Current Registry Contents

The registry validated with:

```text
Registry capabilities: 18
General Ready: todo, clarify, session, memory, leaf
RESULT: General Tool Box is valid.
Individual activation: True
```

## 7.1 General Ready

These are available across Workshops but are **not always loaded**:

```text
todo
clarify
session
memory
leaf
```

Important rule:

> General Ready does not mean active.

If Bristlecone requests `leaf`, only Leaf should activate. It must **not** automatically activate todo, clarify, session, or memory.

## 7.2 Specialized Capabilities

Current specialized concepts include:

```text
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

Several remain intentionally unresolved at the Hermes adapter layer.

---

# 8. Capability States

Planned runtime states:

- **Dormant** — known to runtime, not exposed to the model.
- **Active** — activated for the current need.
- **Sticky** — retained across related turns/tasks.
- **Core** — automatically active when a Workshop is active.

Target structure:

```text
BASE TREE
+
WORKSHOP CORE
+
selected GENERAL OVERLAY
+
selected WORKSHOP READY OVERLAY
+
HOT LEAVES
```

Example:

```text
Workshop: Code / Debug
Core: file + terminal
General overlay: todo
Ready overlay: debugging

Effective Forest capabilities:
file
terminal
todo
debugging
```

Everything else remains dormant.

---

# 9. Current Workshop Definitions

The Workshop YAML files were refactored to schema version 2 and validated against the registry.

Path:

```text
~/The-Forest/bristlecone/workshops/
```

Files:

```text
research.yaml
design.yaml
code-debug.yaml
model.yaml
```

## 9.1 Research

```yaml
core:
  - web
ready: []
```

Hermes target:

```text
web → web
```

Live Hermes `web` toolset expands to:

```text
web_extract
web_search
```

## 9.2 Design

```yaml
core:
  - memory
  - clarify
ready: []
```

These General concepts are promoted into Design core when Design is active.

## 9.3 Code / Debug

```yaml
core:
  - file
  - terminal

ready:
  - code-execution
  - debugging
  - testing
  - special
```

## 9.4 Model

```yaml
core:
  - file
  - terminal

ready:
  - model-evaluation
  - model-benchmarking
  - model-inference
  - quantization
  - training
  - runtime-inspection
```

---

# 10. Workshop Validation Result

All current Workshop references exist in the central registry.

Verified output:

```text
Code / Debug
OK core  file
OK core  terminal
OK ready code-execution
OK ready debugging
OK ready testing
OK ready special

Design
OK core memory
OK core clarify

Model
OK core file
OK core terminal
OK ready model-evaluation
OK ready model-benchmarking
OK ready model-inference
OK ready quantization
OK ready training
OK ready runtime-inspection

Research
OK core web

RESULT: All Workshop capabilities exist in the registry.
```

---

# 11. Hermes Adapter

Runtime adapter:

```text
~/The-Forest/bristlecone/adapters/hermes.yaml
```

The adapter translates canonical Forest capability concepts into Hermes-specific implementations.

## 11.1 Current Verified Tool Mappings

```text
Forest                 Hermes
────────────────────────────────────
todo              →    todo
clarify           →    clarify
session           →    session_search
memory            →    memory
web               →    web
file              →    file
terminal          →    terminal
code-execution    →    code_execution
```

## 11.2 Current Skill Mappings

```text
debugging          →    systematic-debugging
testing            →    test-driven-development
model-evaluation   →    evaluation
model-inference    →    inference
```

## 11.3 Currently Unresolved

```text
leaf
special
model-benchmarking
quantization
training
runtime-inspection
```

These are intentionally left unresolved instead of guessing.

---

# 12. Future Official Forest Capability Names

The current canonical IDs are still somewhat Hermes-like:

```text
file
terminal
todo
memory
clarify
session
```

A future **Forest Naming Pass** is planned.

The final Forest-facing vocabulary should use official Forest-native names, while adapters preserve runtime mappings underneath.

Example future pattern:

```text
OFFICIAL FOREST NAME   →   Hermes implementation
──────────────────────────────────────────────────
<Forest file name>     →   file
<Forest shell name>    →   terminal
<Forest task name>     →   todo
<Forest memory name>   →   memory
Leaf                   →   Forest-native Leaf service
```

This naming pass should happen before the architecture is broadly cloned to Cherry, Maple, Cedar, and other Trees.

---

# 13. Workshop Resolver

Resolver created at:

```text
~/The-Forest/bristlecone/bin/resolve-workshop
```

Purpose:

- Read Workshop definitions.
- Read the capability registry.
- Validate requested General and Ready overlays.
- Resolve Forest IDs through the Hermes adapter.
- Return exact Hermes toolsets and Skills.
- Fail safely on unresolved capabilities.

## 13.1 Resolver Verification

### Code / Debug only

Resolved:

```text
file
terminal
```

### Code / Debug + General Todo

Resolved:

```text
file
terminal
todo
```

This proved General capability activation is individually addressable.

It did **not** activate:

```text
clarify
session
memory
leaf
```

### Code / Debug + Todo + Debugging

Resolved:

```text
Hermes toolsets:
file
terminal
todo

Hermes Skill:
systematic-debugging
```

This proved General overlays and task-specific Ready overlays can coexist.

### Code / Debug + Leaf

Result:

```text
UNRESOLVED:
leaf: Forest-native Leaf Foliage access has not been implemented yet.

RESULT: Cannot activate requested profile yet.
```

This is intentional safe behavior.

---

# 14. Hermes Toolset Investigation

The installed Hermes profile originally showed:

```yaml
toolsets:
  - hermes-cli
  - web
```

Further inspection showed live `platform_toolsets` are more important than the older top-level concept.

Observed platform toolsets included:

```text
cli:
file
terminal

api_server:
code_execution
context_engine
file
memory
session_search
skills
cronjob
terminal
vision
web
```

This triggered investigation of the actual runtime surface used by Bristlecone.

---

# 15. Kanban Investigation

A diagnostic initially showed:

```text
EFFECTIVE CLI TOOLSETS:
file
kanban
terminal
```

Naive expansion made it appear Kanban added 12 extra tools.

Hermes source showed Kanban is runtime `check_fn` gated.

Direct verification under the Bristlecone profile showed:

```text
Profile explicitly enables Kanban:
False

Kanban worker/general tools allowed:
False

Kanban orchestrator tools allowed:
False
```

Conclusion:

> Kanban may appear in Hermes's internally recovered/effective registry but its schemas are not exposed to Bristlecone unless its runtime gates pass.

Therefore Kanban was **not disabled** and was **not added to General Ready**.

---

# 16. Live Hermes Service

The actual Bristlecone systemd service was inspected.

Service:

```text
hermes-bristlecone.service
```

Verified at time of inspection:

```text
ActiveState=active
SubState=running
MainPID=930
```

Actual ExecStart:

```text
/home/user/.hermes/hermes-agent/venv/bin/python
/home/user/.hermes/hermes-agent/hermes
-p bristlecone
gateway run
```

Therefore Bristlecone's live path is:

```text
Hermes profile: bristlecone
        ↓
gateway run
        ↓
Gateway platform
```

It is **not** a plain CLI chat runtime.

---

# 17. Live Platform: api_server

Hermes source inspection confirmed the API-server request path calls:

```text
_load_gateway_config()
_get_platform_tools(user_config, "api_server")
```

during request handling.

Therefore the live Workshop toolset is controlled by:

```yaml
platform_toolsets:
  api_server:
```

The Forest state was updated to:

```yaml
runtime:
  adapter: hermes
  platform: api_server
```

---

# 18. Dynamic Reload Behavior

The API server request path reloads gateway configuration immediately before resolving `api_server` toolsets.

This means:

```text
Workshop switch
     ↓
Hermes config update
     ↓
next API request
     ↓
new toolset
```

No Gateway restart is required for the tested toolset changes.

This was later verified against the running Gateway.

---

# 19. Hermes Native Configuration Writer

Relevant Hermes functions identified:

```text
hermes_cli.config.load_config()
hermes_cli.config.save_config()
hermes_cli.tools_config._save_platform_tools()
```

## 19.1 `load_config()`

- Follows `HERMES_HOME`.
- Caches using config path + file metadata.
- Returns a defensive deep copy for mutation.

## 19.2 `_save_platform_tools()`

- Saves exact platform toolset selections.
- Filters toolsets not allowed on that platform.
- Removes platform default/super toolsets that could silently expose everything.
- Preserves non-configurable entries such as MCP server names.
- Updates the platform's desired toolset selection.

## 19.3 `save_config()`

- Uses Hermes configuration locking.
- Respects managed settings.
- Refuses to overwrite an unreadable config blindly.
- Uses Hermes's atomic YAML writer.
- Resolves config path through active `HERMES_HOME`.

Therefore the Forest switcher uses Hermes-native config functions instead of rewriting the entire Hermes YAML with generic PyYAML.

---

# 20. Exact-State Switching

Hermes also contains an incremental helper that adds/removes from existing sets.

The Forest Workshop controller intentionally does **not** use accumulation as its main switching logic.

Workshop switching must apply an **exact desired state**.

Example:

```text
Research
web
```

switching to:

```text
Code / Debug
file
terminal
```

must result in:

```text
file
terminal
```

NOT:

```text
web
file
terminal
```

This exact replacement behavior has been live-tested successfully.

---

# 21. Active State File

Forest runtime state:

```text
~/The-Forest/bristlecone/state/active.yaml
```

Current structure includes:

```yaml
schema_version: 1
tree: bristlecone

workshop: code-debug

active_general: []
active_ready: []

reasoning: light
model_form: small

runtime:
  adapter: hermes
  platform: api_server

policy:
  sticky_workshop: true
  sticky_capabilities: true
  minimum_useful_canopy: true
```

The live switcher also records a `last_applied` section with:

- exact Hermes toolsets applied
- timestamp

---

# 22. Live Workshop Controller

Python controller:

```text
~/The-Forest/bristlecone/bin/bristlecone-workshop.py
```

Launcher:

```text
~/The-Forest/bristlecone/bin/bristlecone-workshop
```

The launcher:

1. Sets:

```text
HERMES_HOME=~/.hermes/profiles/bristlecone
```

2. Uses Hermes's own Python environment:

```text
~/.hermes/hermes-agent/venv/bin/python
```

3. Runs the Forest controller.

This avoids:

- wrong-profile fallback
- missing Hermes Python dependencies such as `httpx` / `dotenv`

---

# 23. Live Switcher Safety Features

Current switcher behavior:

1. Validates Workshop name.
2. Validates General overlay IDs.
3. Validates Workshop Ready IDs.
4. Resolves capabilities through the registry and adapter.
5. Refuses unresolved mappings.
6. Refuses live Skill activation for now.
7. Verifies runtime platform is `api_server`.
8. Verifies `HERMES_HOME` points to the Bristlecone profile.
9. Backs up Hermes config before changing it.
10. Loads config using Hermes `load_config()`.
11. Applies the **exact** desired platform toolset using `_save_platform_tools()`.
12. Saves via Hermes `save_config()`.
13. Reloads and verifies the resulting configurable set.
14. Writes Forest state atomically only after Hermes verification succeeds.
15. Rolls Hermes config back from backup if verification fails.

Backups:

```text
~/The-Forest/bristlecone/backups/hermes-config/
```

Examples created during live testing:

```text
config-20260808-153124.yaml
config-20260808-155013.yaml
config-20260808-155023.yaml
config-20260808-155120.yaml
```

---

# 24. Dry-Run Verification

The switcher supports:

```text
--dry-run
```

Dry-run Code / Debug resolved:

```text
file
terminal
```

Dry-run Code / Debug + Todo resolved:

```text
file
terminal
todo
```

Dry-run Code / Debug + Debugging resolved the Skill mapping but correctly refused live activation because individual Skill activation has not yet been implemented.

This safety gate is intentional.

---

# 25. First Real Live Workshop Activation

The first real activation was:

```text
Code / Debug
```

Forest resolved:

```text
file
terminal
```

The switcher reported successful activation and Forest/Hermes synchronization.

Independent verification showed:

```text
FOREST
Workshop: code-debug
General: []
Ready: []
Applied: ['file', 'terminal']

HERMES
api_server: ['file', 'terminal']
```

This proved Forest and Hermes config synchronization.

---

# 26. Live Gateway Verification Endpoint

Hermes exposes:

```text
GET /v1/toolsets
```

The endpoint is documented in the local source as the deterministic toolset surface the `api_server` actually exposes to its agent.

It:

1. Loads current config.
2. Resolves `api_server` toolsets.
3. Returns each toolset's enabled/configured state and concrete tools.

This became the end-to-end verification mechanism.

---

# 27. Qube-Local / Profile-Scoped API Credentials

The API server authenticates with:

```text
Authorization: Bearer <API_SERVER_KEY>
```

Hermes source showed that named profiles resolve the key through profile-scoped secret handling.

Named-profile API keys are stored under the profile-local environment file:

```text
~/.hermes/profiles/<profile>/.env
```

For Bristlecone:

```text
~/.hermes/profiles/bristlecone/.env
```

Important Forest security rule:

> Runtime credentials stay Qube-local and runtime-owned. Portable Forest state stores capability mappings, not runtime secrets.

The Forest Workshop files, capability registry, Leaves, and adapter must **not** contain API secrets.

---

# 28. Clone / Secret Rotation Rule

A normal Qubes clone should be assumed to copy the qube's persistent files, including profile-local secrets.

Therefore a cloned Cherry-AI qube would initially be expected to inherit the same Hermes profile `.env` unless a provisioning step rotates it.

Planned Forest rule:

> Cloning a Tree/Qube copies identity and portable state, but Qube-local runtime credentials should be regenerated during clone provisioning.

Portable/copyable:

```text
Tree identity
Workshops
capability registry
Leaves
Skills
routing
operational learning
Forest configuration
```

Regenerate per clone/Qube:

```text
Hermes API_SERVER_KEY
machine/Qube-local service credentials
runtime tokens
other local secrets
```

This provisioning/rotation system has **not yet been implemented**.

---

# 29. Reusable Live Workshop Verifier

Reusable diagnostic:

```text
~/The-Forest/bristlecone/bin/verify-live-workshop
```

It:

1. Uses the Bristlecone `HERMES_HOME`.
2. Uses Hermes's virtual environment.
3. Reads the profile-local API key without printing it.
4. Detects the running Bristlecone systemd PID.
5. Detects the Gateway listening port.
6. Calls `GET /v1/toolsets`.
7. Prints only enabled toolsets and concrete tool names.

At the time of testing:

```text
Gateway PID: 930
Port: 8643
Platform: api_server
```

PID/port are runtime details and may change after restart.

---

# 30. End-to-End Live Verification: Code / Debug

The running Gateway reported:

```text
terminal
  process
  terminal

file
  patch
  read_file
  search_files
  write_file

Enabled toolset count: 2
```

This proved the running Gateway exposed exactly the Code / Debug core.

No Gateway restart was performed.

---

# 31. End-to-End Live Verification: Research

Bristlecone was switched live from Code / Debug to Research.

Applied:

```text
web
```

The running Gateway then reported:

```text
web
  web_extract
  web_search

Enabled toolset count: 1
```

Critically:

```text
file      removed
terminal  removed
```

This proved Workshop switching performs **replacement**, not accumulation.

---

# 32. End-to-End Live Verification: Code / Debug + Todo

The next live switch used:

```text
Code / Debug
+
General overlay: todo
```

Applied:

```text
file
terminal
todo
```

The running Gateway reported:

```text
terminal
  process
  terminal

file
  patch
  read_file
  search_files
  write_file

todo
  todo

Enabled toolset count: 3
```

Critically:

```text
web removed
todo added alone
memory not added
session not added
clarify not added
leaf not added
```

This proves the General Tool Box/rack works as an **individual overlay**, not a bundled activation group.

---

# 33. Infrastructure Now Proven Complete

The following infrastructure is implemented and verified:

```text
✓ Canonical Forest Tree root
✓ Central capability registry
✓ General Ready capability rack
✓ Individual General activation
✓ Four Workshop definitions
✓ Workshop → registry validation
✓ Hermes adapter
✓ Safe unresolved mappings
✓ Workshop resolver
✓ General overlay resolver
✓ Ready/Skill resolution
✓ Active-state file
✓ Correct live Hermes service identified
✓ Gateway runtime identified
✓ api_server platform identified
✓ Dynamic per-request config loading identified
✓ Hermes-native config writer identified
✓ Exact-state Workshop switching
✓ Hermes config backup
✓ Verification and rollback logic
✓ Correct profile isolation via HERMES_HOME
✓ Hermes virtualenv usage
✓ Live Code/Debug switch
✓ Live Research switch
✓ Live Code/Debug + Todo overlay
✓ Running Gateway verification
✓ No Gateway restart required for tested tool switches
✓ Qube-local/profile-local API-secret boundary established
```

---

# 34. What Is NOT Yet Complete

## 34.1 Individual Skill Activation

Current mappings include:

```text
debugging → systematic-debugging
testing → test-driven-development
model-evaluation → evaluation
model-inference → inference
```

However the live switcher intentionally blocks them.

Reason:

We have not yet verified how Hermes injects **one specific Skill** without exposing/loading the entire Skills surface or bringing unnecessary Skill metadata into Hot context.

This is the next major technical target.

## 34.2 Leaf Foliage Runtime Access

`leaf` exists in General Ready but remains unresolved.

Future implementation should be Forest-native.

Hermes should eventually receive a narrow interface such as:

```text
forest_leaf_search
forest_leaf_read
```

rather than owning the Leaf system.

## 34.3 Model Workshop Specialized Capabilities

Still unresolved or not yet live-wired:

```text
model-benchmarking
quantization
training
runtime-inspection
```

Do not guess these mappings.

## 34.4 `special` Capability

`special` remains a placeholder for unusual task-specific capability activation and needs a clearer definition before implementation.

## 34.5 Sticky Capability Hysteresis

The state model supports sticky concepts but automatic sticky activation/deactivation logic has not yet been implemented.

Future behavior should avoid thrashing when related turns continue.

## 34.6 Automatic Workshop Routing

The current switcher is command-driven.

Bristlecone does not yet automatically classify a task and select Research, Design, Code / Debug, or Model.

Build the automatic router only after switching and benchmarking are stable.

## 34.7 Operational Learning

Planned operational learning should record:

```text
task pattern
initial Workshop
successful Workshop
capabilities used
capabilities unnecessary
fallback used
outcome
```

Portable source may be JSONL. A derived SQLite index may be used for speed and rebuilt when necessary.

Knowledge learning and operational learning must remain separate concepts.

## 34.8 Skill Finder / Open Workbench Fallback

Planned escalation:

```text
Level 0: current Workshop Core
Level 1: current Workshop Ready
Level 2: search Tree-owned capability/Skill manifests
Level 3: compare other Workshop manifests
Level 4: Open Workbench
```

This is a meta-layer, not a fifth normal Workshop.

## 34.9 Official Forest Naming Pass

Current canonical names are provisional.

Before broad Forest deployment, rename capabilities to official Forest-native terminology while keeping runtime mappings in adapters.

## 34.10 Clone Provisioning / Secret Rotation

Need first-boot-after-clone detection and secret rotation.

Proposed behavior:

```text
clone Qube
   ↓
detect new Qube identity
   ↓
preserve portable Tree state
   ↓
rotate runtime-local credentials
   ↓
update only cloned Qube runtime
```

---

# 35. Completed Infrastructure Plan

The completed base infrastructure is now:

```text
                    THE FOREST
                        │
                        ▼
             BRISTLECONE PINE TREE
                        │
       ┌────────────────┴────────────────┐
       │                                 │
       ▼                                 ▼
CAPABILITY REGISTRY                ACTIVE STATE
canonical IDs                      current Workshop
kinds/scopes                       overlays
general-ready rack                 reasoning
runtime status                     model form
       │                                 │
       └────────────────┬────────────────┘
                        ▼
                  WORKSHOP POLICY
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
        CORE      GENERAL OVERLAY   READY OVERLAY
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  FOREST RESOLVER
                        │
                        ▼
                   HERMES ADAPTER
                        │
                        ▼
            EXACT DESIRED TOOLSET SET
                        │
                        ▼
        Hermes _save_platform_tools()
                        │
                        ▼
               Hermes save_config()
                        │
                        ▼
          platform_toolsets.api_server
                        │
                        ▼
              RUNNING HERMES GATEWAY
                        │
                        ▼
                  BRISTLECONE AGENT
                        │
                        ▼
               MINIMUM HOT CANOPY
```

This toolset path is now live.

---

# 36. Cold / Warm / Hot Architecture

## Cold

Large, authoritative portable Tree state on disk:

```text
identity
Workshop definitions
Skills
Leaves
permissions
routing
learning
adapter definitions
portable state
```

## Warm

Small prepared runtime structures in RAM:

```text
parsed capability registry
parsed Workshop profiles
tiny Skill manifests
adapter mappings
derived indexes
prepared selectors
```

Cached in RAM does **not** mean visible to the model.

## Hot

Only current task requirements:

```text
tiny Tree identity
active Workshop core
selected General overlays
selected Ready overlays
relevant Hot Leaves
current task
```

Rule:

> Keep Cold large, Warm small, Hot tiny.

---

# 37. Stable Prefix / Future Prompt Caching

A future stable Workshop prefix may improve prompt/KV caching, especially if/when moving to llama.cpp.

Potential stable prefix:

```text
Tree identity
Forest rules
Workshop rules
core tool schemas
small capability manifest
```

Dynamic suffix:

```text
active Skills
Hot Leaves
task
current user message
```

Evaluate after basic runtime behavior is stable.

---

# 38. Next Steps — Recommended Order

## Phase 1 — Individual Skill Activation

Highest priority.

Investigate exactly how Hermes:

- discovers installed Skills
- decides which Skills are visible/loaded
- injects Skill descriptions/instructions
- enables/disables individual Skills
- exposes the `/v1/skills` API

Goal:

```text
Code / Debug
Core:
file
terminal

Ready overlay:
debugging

Hot result:
file
terminal
systematic-debugging
```

without loading unrelated Skills.

Also test:

```text
testing
model-evaluation
model-inference
```

## Phase 2 — Live Skill State Integration

Extend `state/active.yaml` so it records:

```yaml
active_general:
active_ready:
live_toolsets:
live_skills:
```

The switcher should synchronize tool and Skill state atomically.

## Phase 3 — Benchmark the New Workshop Runtime

Benchmark exact states.

### Tool-only baseline

```text
file + terminal
```

### General overlay

```text
file + terminal + todo
```

### Skill overlay

```text
file + terminal + debugging
```

### Combined overlay

```text
file + terminal + todo + debugging
```

### Research

```text
web
```

Measure separately:

- cold first-output latency
- warm first-output latency
- completion time
- token/context overhead where measurable
- behavior quality
- Workshop switching overhead
- live config application overhead

Do not mix cold model load time with tool/Skill schema overhead.

## Phase 4 — Compare Against Historical Benchmarks

Historical relevant numbers:

```text
file + terminal ≈ 41 sec
file + terminal + todo = 1:49.64
file + terminal + skills = 2:42.40
file + terminal + skills + todo = 2:49.16
```

Also compare against later cold/warm Workshop observations.

Goal: determine whether the new architecture reduces real latency or only improves organization.

## Phase 5 — Sticky Workshop and Capability Logic

Implement:

- sticky Workshop across related turns
- sticky General overlays
- sticky Ready overlays
- explicit task boundary detection
- hysteresis to prevent rapid activate/deactivate thrashing

## Phase 6 — Automatic Router

Only after manual switching is reliable.

Router chooses:

```text
Research
Design
Code / Debug
Model
```

using a very small routing prompt/heuristic.

The router itself must not become a large latency source.

## Phase 7 — Skill Finder / Open Workbench

Implement fallback escalation using tiny manifests first.

Do not load all Skills or Workshops merely to inspect them.

## Phase 8 — Operational Learning

Record successful routing/capability patterns and use them to improve first-choice Workshop selection.

Keep this separate from user/project/world knowledge Leaves.

## Phase 9 — Leaf Foliage Integration

Implement Forest-native Leaf access.

Desired behavior:

```text
General Ready:
leaf

activate leaf
   ↓
only Leaf access becomes available
```

No automatic activation of memory/session/todo/clarify.

## Phase 10 — Official Forest Naming Pass

Replace provisional Hermes-like canonical IDs with official Forest vocabulary.

Update:

```text
capability registry
Workshop references
Forest documentation
adapter keys
migration aliases if needed
```

Keep Hermes targets unchanged in the Hermes adapter.

## Phase 11 — Clone Provisioning

Implement Qube/Tree clone initialization:

- identify cloned runtime
- preserve portable state
- rotate local API keys/secrets
- update Qube-local runtime config
- verify connectivity
- never store secrets in portable Tree files

## Phase 12 — Ollama vs llama.cpp A/B

After the Workshop baseline is stable, compare Ollama and llama.cpp using:

- same Bristlecone model if possible
- same quantization
- same Workshop
- same toolset
- same reasoning mode
- same prompts
- same Qube resources
- same warm/cold conditions

Do not re-architect Workshops merely to change inference runtime.

---

# 39. Current Live State at End of This Packet

Most recently verified live state:

```text
Workshop: Code / Debug
General overlay: todo
Ready overlays: none live

Hermes api_server toolsets:
terminal
file
todo
```

Concrete live tools:

```text
terminal
  process
  terminal

file
  patch
  read_file
  search_files
  write_file

todo
  todo
```

Live enabled toolset count:

```text
3
```

Earlier verified Research live state:

```text
web
  web_extract
  web_search
```

Live enabled toolset count:

```text
1
```

No Gateway restart was required between these switches.

---

# 40. Current Bristlecone Runtime Notes

Current Bristlecone model from the broader project:

```text
bristlecone-qwen35:4b-64k
```

Hermes is the primary orchestration/interface layer.

Ollama is the current inference runtime.

Newelle remains optional/paused because prior benchmarks were very slow.

Long-term model:

```text
Forest-owned Tree
    ↓
replaceable runtime adapter
    ↓
replaceable agent framework
    ↓
replaceable inference engine/model
```

---

# 41. Design Rules to Preserve

1. **Minimum Useful Canopy** — expose only capabilities required for the current task.
2. **General Ready is not Always Active** — General capabilities are individually addressable overlays.
3. **Workshop Ready is not Automatically Active** — specialized Skills/tools remain dormant until selected.
4. **Exact-State Switching** — switching Workshops replaces old task toolsets instead of accumulating them.
5. **Forest Owns Canonical Concepts** — Hermes is an implementation adapter, not the source of Bristlecone's identity.
6. **Do Not Guess Runtime Mappings** — unknown capability implementations stay unresolved.
7. **Secrets Stay Runtime/Qube Local** — never place API keys in portable Tree state.
8. **Cache Does Not Equal Context** — Warm RAM manifests may exist without being visible to the model.
9. **Separate Knowledge Learning from Operational Learning** — Leaves are not the same as routing/capability performance history.
10. **Measure Cold and Warm Separately** — do not confuse model/runtime load time with tool/Skill overhead.
11. **Portable Source, Rebuildable Indexes** — human-readable source is authoritative where practical; caches/indexes are rebuildable.
12. **Do Not Let Runtime Defaults Defeat Forest Policy** — verify the actual model-visible surface, not merely saved config names.

---

# 42. Immediate Next Technical Task

The next task should be:

> **Discover and implement individual Hermes Skill activation while preserving Minimum Useful Canopy.**

Specifically determine how to activate:

```text
systematic-debugging
test-driven-development
evaluation
inference
```

one at a time.

The live Workshop controller should continue to reject Skill overlays until this mechanism is proven.

After individual Skill activation works, immediately benchmark:

```text
file + terminal
file + terminal + todo
file + terminal + debugging
file + terminal + todo + debugging
```

under both cold and warm conditions.

---

# 43. Short Recovery Checklist for a Future Chat

If continuity is lost:

1. Confirm canonical root:

```text
~/The-Forest/bristlecone
```

2. Confirm Hermes profile:

```text
~/.hermes/profiles/bristlecone
```

3. Check Forest state:

```text
~/The-Forest/bristlecone/state/active.yaml
```

4. Verify live Workshop:

```bash
"$HOME/The-Forest/bristlecone/bin/verify-live-workshop"
```

5. Switch to Code / Debug:

```bash
"$HOME/The-Forest/bristlecone/bin/bristlecone-workshop" code-debug
```

6. Switch to Research:

```bash
"$HOME/The-Forest/bristlecone/bin/bristlecone-workshop" research
```

7. Add General Todo:

```bash
"$HOME/The-Forest/bristlecone/bin/bristlecone-workshop" \
code-debug \
--general todo
```

8. Do **not** activate Ready Skills live yet.
9. Continue with individual Skill activation research.

---

# 44. Bottom Line

The Workshop architecture has moved from concept to a functioning live runtime layer.

Bristlecone can now:

- switch between different task capability sets,
- remove old Workshop tools,
- add one General capability without adding the rest,
- synchronize Forest state with Hermes,
- change the running Gateway's effective toolset without restarting it,
- verify the actual live surface through Hermes's API,
- preserve runtime credentials outside portable Forest state,
- and keep the architecture portable enough to support a future runtime or orchestration change.

The remaining major technical gap is **individual Skill activation**.

Once that is solved and benchmarked, the Workshop system will be ready for sticky state, automatic routing, operational learning, Leaf integration, official Forest naming, clone provisioning, and broader deployment across The Forest.
