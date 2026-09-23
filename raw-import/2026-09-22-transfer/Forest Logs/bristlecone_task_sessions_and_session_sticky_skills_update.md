# Bristlecone Pine — Task Sessions and Session-Sticky Skills
## Architecture Update

**Project:** The Forest / Bristlecone Pine  
**Focus:** Workshop lifecycle, Skill persistence, session boundaries, and future prompt-cache compatibility  
**Date:** 2026-08-08  
**Status:** Architectural refinement accepted for future implementation; Phase 1 live Skill work remains the immediate priority.

---

# 1. Why This Update Exists

During Phase 1 investigation of Hermes Skill loading, we confirmed that Hermes supports explicit Skill preloading for the duration of a session.

Hermes's preload behavior closely resembles the Forest concept of a **sticky Skill**:

```text
Forest concept:
Sticky Skill
  ↓
remain active across related turns
  ↓
remove when the task changes

Hermes behavior:
Preloaded Skill
  ↓
remain active for session
  ↓
session ends or changes
```

This suggests that sticky Skills should not be modeled as arbitrary global flags.

Instead, the Forest should introduce a lightweight **Task Session** that owns the current Workshop and its session-sticky capabilities.

---

# 2. New Recommended Structure

The user's conversation and the Forest's internal execution session should be separate concepts.

```text
USER CONVERSATION
        │
        ├── Task Session A
        │      Design
        │
        ├── Task Session B
        │      Code / Debug + Debugging
        │
        └── Task Session C
               Research
```

A user may remain in one continuous conversation while Bristlecone changes internal Task Sessions when the work changes.

This prevents the Forest from depending on Hermes's user-facing session model.

---

# 3. Task Session

A Task Session is an internal Forest execution/lifecycle container.

It can own:

```text
Reasoning Mode
Model Form
Workshop
Workshop Core capabilities
Task-sticky Skills
temporary General overlays
temporary Ready overlays
Hot Leaves
task-specific state
```

Example:

```yaml
task_session:
  workshop: code-debug
  reasoning: light
  model_form: small

  core:
    - file
    - terminal

  sticky:
    - debugging

  temporary:
    - todo
```

---

# 4. Revised Capability State Model

The earlier model was:

```text
Dormant
Active
Sticky
Core
```

The refined V1 model should be:

```text
Dormant
Active
Task-Sticky
Core
```

## Core

Automatically active for the lifetime of the current Workshop.

Example:

```text
Code / Debug:
file
terminal
```

## Active

Temporarily activated for an immediate need.

Example:

```text
todo
```

It may disappear after the need is satisfied.

## Task-Sticky

Activated once and retained for the current Task Session.

Example:

```text
systematic-debugging
```

It remains available through related follow-up turns without repeated routing/loading decisions.

## Dormant

Known to the Tree but not currently exposed to the model.

---

# 5. Example: Debugging Task

User begins troubleshooting a service.

Forest creates:

```text
Task Session A

Workshop:
Code / Debug

Core:
file
terminal

Task-Sticky Skill:
debugging
```

Effective Hot capability set:

```text
file
terminal
systematic-debugging
```

Follow-up turns in the same task reuse the same Task Session.

The Forest does not need to repeatedly decide whether debugging is still required.

---

# 6. Example: Adding Testing During the Same Task

Later in the debugging task, tests become useful.

Instead of destroying the session:

```text
debugging
↓
new session
testing
```

the Forest may transition the same Task Session:

```text
Task Session A

Core:
file
terminal

Task-Sticky:
debugging
testing
```

If debugging later becomes unnecessary, the Forest may remove it at a task boundary or capability transition.

---

# 7. Example: Changing Tasks

The user changes from debugging to research.

Old Task Session:

```text
Code / Debug

Core:
file
terminal

Task-Sticky:
debugging
```

New Task Session:

```text
Research

Core:
web

Task-Sticky:
none
```

The debugging instructions naturally disappear because they belong to the old Task Session.

---

# 8. Why This May Improve Speed

The largest likely advantage is not faster file loading.

The advantage is reduced **routing and context churn**.

Without Task Sessions:

```text
Turn 1
classify task
activate debugging
inject Skill

Turn 2
classify again
decide debugging still needed
rebuild state

Turn 3
classify again
repeat
```

With Task Sessions:

```text
Turn 1
create Code / Debug Task Session
activate debugging once

Turn 2
reuse session

Turn 3
reuse session
```

This reduces repeated selection work and makes runtime state more stable.

---

# 9. Prompt / KV Cache Benefit

A Task Session can provide a stable model prefix.

Example stable prefix:

```text
Tree identity
Workshop instructions
file tool schema
terminal tool schema
systematic-debugging Skill
```

Dynamic suffix:

```text
conversation history
Hot Leaves
current task state
new user message
```

A stable prefix may improve prompt/KV cache reuse in runtimes that support it.

This is especially relevant to future llama.cpp evaluation.

Rapid capability toggling may reduce cache reuse:

```text
debugging on
debugging off
todo on
testing on
debugging on
```

Task Session stability reduces that churn.

---

# 10. Relationship to Hermes

Hermes already provides an important runtime primitive:

```text
session-wide preloaded Skills
```

Hermes can therefore serve as the current implementation backend.

The intended structure becomes:

```text
FOREST
Task Session
Workshop policy
Task-Sticky Skill policy
        │
        ▼
HERMES ADAPTER
selected Skill preload
        │
        ▼
HERMES SESSION
```

Hermes does not determine Forest task boundaries.

The Forest decides:

```text
when the task begins
when it ends
which Workshop is active
which Skills remain sticky
which capabilities are temporary
```

---

# 11. Future Forest-Native Harness

The same Forest Task Session model should survive removal of Hermes.

Current:

```text
Forest Task Session
        ↓
Hermes Skill adapter
        ↓
Hermes preload/session system
```

Future:

```text
Forest Task Session
        ↓
Forest-native Skill backend
        ↓
Forest-native context/session system
```

The Task Session, Workshop, and capability policy remain unchanged.

This preserves portability.

---

# 12. Task Session Is Not Necessarily a User-Visible Chat Session

A Task Session should normally be internal.

Do not require the user to open a new conversation every time a Workshop or sticky Skill changes.

Example:

```text
ONE BRISTLECONE CONVERSATION

Task Session 1:
Design

Task Session 2:
Code / Debug + debugging

Task Session 3:
Research
```

The conversation remains continuous.

The internal execution state changes underneath it.

---

# 13. Do Not Create a New Session for Every Capability

Not every activation should produce a new Task Session.

For example:

```text
todo
```

is usually too small and temporary to justify a new session.

A Task Session should represent a meaningful task/workflow boundary.

Small temporary overlays can remain inside the existing session.

---

# 14. Suggested Task Session State

A future state structure may resemble:

```yaml
schema_version: 2
tree: bristlecone

conversation_id: <runtime-or-forest-id>

task_session:
  id: <forest-task-session-id>

  workshop: code-debug
  reasoning: light
  model_form: small

  capabilities:
    core:
      - file
      - terminal

    task_sticky:
      - debugging

    temporary:
      - todo

  resolved_runtime:
    adapter: hermes
    toolsets:
      - file
      - terminal
      - todo
    skills:
      - systematic-debugging
```

This cleanly separates:

```text
Forest canonical capability:
debugging

Hermes runtime implementation:
systematic-debugging
```

---

# 15. Operational Learning Benefits

Task Sessions provide a better unit for operational learning.

Instead of only recording:

```text
debugging Skill used
```

the Forest can record:

```yaml
task_session:
  task_type: service-debugging

  initial_workshop: code-debug

  core:
    - file
    - terminal

  sticky:
    - debugging

  temporary:
    - todo

  transitions:
    - added: testing
    - removed: debugging

  outcome: success
```

This can later teach Bristlecone:

```text
Tasks like this usually need:
Code / Debug
+
debugging

Testing often becomes useful after diagnosis.
```

---

# 16. Relationship to Minimum Useful Canopy

Task Sessions strengthen the Minimum Useful Canopy principle.

Instead of constantly rebuilding the canopy:

```text
load
unload
load
unload
```

the Forest keeps the smallest useful canopy stable for the duration of the task.

```text
Cold:
all Tree capabilities

Warm:
registry + manifests + indexes

Hot Task Session:
Workshop Core
+
Task-Sticky Skills
+
temporary overlays
+
Hot Leaves
```

Rule remains:

> Keep Cold large, Warm small, Hot tiny.

---

# 17. Phase 2 Design Update

The Task Session architecture should be implemented primarily during Phase 2.

Previous Phase 2:

```text
Unified Live State
```

Refined Phase 2:

```text
Unified Live State + Task Sessions
```

Planned work:

```text
□ Define Task Session state schema
□ Store current Workshop inside Task Session
□ Store Task-Sticky Skills
□ Store temporary overlays separately
□ Track resolved Hermes toolsets
□ Track resolved Hermes Skills
□ Define task-boundary transition behavior
□ Keep state updates atomic
□ Add rollback
□ Upgrade live verifier
□ Verify Forest ↔ Hermes ↔ Gateway/session state
```

---

# 18. Phase 1 Does Not Change

This architectural refinement should **not derail Phase 1**.

Immediate Phase 1 remains:

```text
1. Trace Hermes Skill prompt injection
2. Find Gateway/session integration point
3. Load systematic-debugging alone
4. Verify unrelated Skills are absent
5. Integrate selected Skill loading with bristlecone-workshop
6. Verify activation/deactivation behavior
```

Hermes session preload will be used as the current runtime primitive.

Task Session management comes after the primitive is proven.

---

# 19. Phase 3 Benchmark Impact

Phase 3 should benchmark both capability composition and session reuse.

Required capability tests:

```text
file + terminal
file + terminal + todo
file + terminal + debugging
file + terminal + todo + debugging
web
```

Also compare:

```text
new Task Session / cold Skill activation
vs
reused Task Session / sticky Skill
```

Measure:

```text
cold first-output latency
warm first-output latency
completion time
Skill preload overhead
Workshop switch overhead
Task Session reuse benefit
```

This will tell us whether Task-Sticky Skills improve actual performance.

---

# 20. Current Decision

Adopt the following architecture direction:

> **Workshops define the task capability environment. Task Sessions define the lifetime of that environment. Skills may be Task-Sticky inside a Task Session. Hermes session-preloaded Skills are the current runtime primitive used to implement this behavior.**

Do not yet build the full Task Session manager.

First complete individual Skill activation in Phase 1.

---

# 21. Updated Phases 1–3

## Phase 1 — Individual Skill Activation

```text
✓ Skill discovery understood
✓ Metadata/full-content split understood
✓ Lazy full loading confirmed
✓ Exact preload mechanism discovered
✓ build_preloaded_skills_prompt() identified
✓ Disabled filtering confirmed
✓ Session-scoped preload semantics confirmed

→ Find Gateway/session injection point
□ Test systematic-debugging alone
□ Verify unrelated Skills absent
□ Integrate Skill activation into Workshop controller
□ Verify activation/deactivation
```

## Phase 2 — Unified State + Task Sessions

```text
□ Task Session schema
□ Core / Temporary / Task-Sticky state
□ Runtime toolset state
□ Runtime Skill state
□ atomic switching
□ rollback
□ task boundaries
□ verifier upgrade
```

## Phase 3 — Performance Benchmarking

```text
□ file + terminal
□ file + terminal + todo
□ file + terminal + debugging
□ file + terminal + todo + debugging
□ web
□ cold tests
□ warm tests
□ Task Session reuse tests
□ historical comparison
□ bottleneck analysis
```

---

# 22. Summary

The Forest should treat Hermes's session Skill preload mechanism as an implementation primitive, not as the Forest's architectural definition of a session.

The Forest owns:

```text
Conversation
Task Session
Workshop
Reasoning Mode
Model Form
Core capabilities
Task-Sticky Skills
Temporary overlays
Hot Leaves
```

Hermes currently provides:

```text
tool execution
Skill loading
session-level Skill preload
agent orchestration
```

This creates a clean portability boundary while making sticky Skill behavior simpler, more predictable, and potentially faster.
