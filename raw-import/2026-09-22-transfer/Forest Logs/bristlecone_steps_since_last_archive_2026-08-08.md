# Bristlecone Pine — Steps Since the Last Markdown Archive
**Checkpoint:** 2026-08-08  
**Previous archive baseline:** `bristlecone_layered_hot_context_and_task_session_cache_update.md`  
**Purpose:** Fast continuity handoff containing only the implementation steps, tests, fixes, and decisions made after that archive.

---

# RESUME HERE

**Next task:** create the Forest runtime adapter boundary before adding more Hermes session behavior.

Target:

```text
runtime/
├── __init__.py
├── task_session.py
└── adapters/
    ├── __init__.py
    ├── base.py
    └── hermes.py
```

First extraction target:

```text
_load_hermes_toolset_runtime
_hermes_configurable_toolsets
begin_temporary_runtime_toolsets
restore_temporary_runtime_toolsets
```

Then rerun the already-passing temporary-turn tests.

---

# Steps Completed Since the Last Archive

## 1. Forest Task Session lifecycle completed

Implemented and verified:

```text
start_task()
end_task()
```

Added:

- Forest-owned Task IDs: `forest-task-<UTC>-<8 hex>`
- active/inactive lifecycle
- timestamps
- Task-Sticky Skill retention
- task-boundary cache cleanup
- optional persistence

---

## 2. Atomic Task state persistence added

Added atomic YAML persistence using:

```text
temporary file
→ write
→ flush
→ fsync
→ os.replace
```

Verified with disposable and live state tests.

---

## 3. Live Forest Task lifecycle verified

A real Task was persisted and ended successfully.

Known live backup:

```text
/home/user/The-Forest/bristlecone/backups/task-state/active-20260808-193231.yaml
```

After the test, real Forest state returned to inactive.

---

## 4. Temporary capability resolver implemented

Added runtime classification for temporary capabilities:

```text
toolsets
contexts
skills
capabilities
```

Verified examples:

```text
todo → toolset → todo
memory → context → memory
testing → Skill → test-driven-development
```

Unresolved `leaf` correctly failed.

---

## 5. Duplicate resolver bug found and removed

An earlier patch had accidentally inserted two copies of the temporary resolver.

A guarded authorization patch detected:

```text
matches=2
```

and aborted safely.

The duplicate was inspected and removed.

Backup:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194150.py
```

---

## 6. Temporary capability authorization implemented

Authorization rules:

```text
Workshop Core → already_active
General Ready → authorized
Current Workshop Ready → authorized
Anything else → denied
```

Code/Debug verification:

```text
todo → AUTHORIZED
testing → AUTHORIZED
file → ALREADY ACTIVE
web → DENIED
model-evaluation → DENIED
```

---

## 7. Temporary activation planner implemented

Added:

```text
plan_temporary_activation(...)
```

Verified request:

```text
todo
memory
testing
file
```

Result:

```text
runtime toolsets:
todo
memory

temporary Skill:
testing → test-driven-development

file:
already active; not redundantly activated
```

Backup:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-194745.py
```

---

## 8. Hermes configurable-toolset behavior verified

Confirmed Hermes supports configurable:

```text
file
terminal
todo
memory
clarify
session_search
code_execution
...
```

This allowed Forest `toolset` and `context` kinds to use the same Hermes temporary-toolset transaction.

---

## 9. Live temporary Hermes toolset/context transaction implemented

Added:

```text
_load_hermes_toolset_runtime
_hermes_configurable_toolsets
begin_temporary_runtime_toolsets
restore_temporary_runtime_toolsets
```

Live baseline:

```text
file
terminal
```

Temporary additions:

```text
todo
memory
```

Inside transaction:

```text
file
memory
terminal
todo
```

After restoration:

```text
file
terminal
```

All checks passed.

Known backup:

```text
/home/user/The-Forest/bristlecone/backups/hermes-temporary/config-20260808T235043-389581Z.yaml
```

---

## 10. Separate temporary Skill cache added

Added:

```text
_temporary_skill_overlay_cache
_temporary_overlay_build_count
```

Task-end cleanup was extended to clear both:

```text
Task-Sticky Skill cache
Temporary Skill cache
```

Backup:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-195210.py
```

---

## 11. Temporary Skill layer added

Added:

```text
prepare_temporary_skill_overlay(...)
prepare_turn_skill_overlay(...)
```

Turn composition became:

```text
Task-Sticky Skill layer
+
current temporary Skill layer
```

---

## 12. Temporary Skill behavior fully verified

Test:

```text
Task-Sticky:
debugging

Temporary:
testing
```

Turn 1:

```text
systematic-debugging
test-driven-development
```

Repeated Turn 1:

```text
sticky cache hit: True
temporary cache hit: True
```

Turn 2 without temporary testing:

```text
systematic-debugging
```

Temporary prompt length:

```text
0
```

Task end:

```text
cache entries discarded: 2
```

All checks passed.

---

## 13. Unified temporary-turn helper added

Added context manager:

```text
temporary_turn(...)
```

Flow:

```text
authorize/resolve
→ build Skill layers
→ activate temporary Hermes toolsets
→ yield
→ finally restore exact baseline
```

Requires an active Forest Task ID.

Backup:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-195349.py
```

---

## 14. Unified normal-path test passed

Temporary request:

```text
todo
memory
testing
```

Task-Sticky:

```text
debugging
```

Inside:

```text
Hermes:
file
memory
terminal
todo

Skills:
systematic-debugging
test-driven-development
```

After:

```text
Hermes:
file
terminal
```

All checks passed.

---

## 15. Exception-path restoration test passed

A deliberate:

```text
FOREST_TEST_EXCEPTION
```

was raised while temporary capabilities were active.

Hermes still restored from:

```text
file
memory
terminal
todo
```

to:

```text
file
terminal
```

All restoration checks passed.

---

## 16. Hermes session lifecycle investigated

Source inspection confirmed:

- Hermes owns its own session IDs.
- Hermes can resume sessions.
- Hermes persists history through SessionDB.
- Hermes can rotate session IDs.
- Compression can produce a continuation/new durable session ID.

Decision:

```text
Forest Task ID = stable
Hermes session ID = mutable runtime state
```

---

## 17. Hermes persisted-session API identified

Relevant API routes:

```text
POST   /api/sessions
GET    /api/sessions/{session_id}
DELETE /api/sessions/{session_id}
POST   /api/sessions/{session_id}/chat
POST   /api/sessions/{session_id}/chat/stream
```

Persisted chat returns the effective Hermes session ID, enabling Forest to detect rotation.

Preferred integration:

```text
/api/sessions/{session_id}/chat
```

---

## 18. `runtime_sessions` added to Forest Task schema

Added:

```yaml
runtime_sessions: {}
```

Active shape:

```yaml
runtime_sessions:
  hermes:
    session_id: ...
    previous_session_id: ...
    updated_at: ...
```

Missing field defaults to `{}` for backward compatibility.

Backup:

```text
/home/user/The-Forest/bristlecone/backups/runtime/task-session-20260808-200134.py
```

---

## 19. runtime-session lifecycle added

Task start:

```text
runtime_sessions: {}
```

Task end:

```text
active runtime_sessions cleared
```

and returns:

```text
retired_runtime_sessions
```

for later runtime cleanup.

---

## 20. runtime-session lifecycle test passed

Simulated:

```text
current:
api_test_current

previous:
api_test_previous
```

Normalization preserved both.

Task end cleared active mapping while returning the retired mapping.

`active.yaml` remained unchanged.

---

## 21. Live Bristlecone API endpoint identified

Running:

```text
hermes -p bristlecone gateway run
```

Listening:

```text
127.0.0.1:8643
```

Current API base:

```text
http://127.0.0.1:8643
```

---

## 22. API authentication investigated

Hermes requires:

```text
API_SERVER_KEY
```

Gateway PID inspection showed the key is **not** stored as a normal process environment variable.

Therefore standalone environment lookup was not the correct authentication mechanism.

---

## 23. Hermes profile secret-scope mechanism identified

Relevant module:

```text
agent.secret_scope
```

Relevant functions:

```text
build_profile_secret_scope
set_secret_scope
reset_secret_scope
current_secret_scope
get_secret
```

Hermes gateway wrapper:

```text
gateway.run._profile_runtime_scope
```

This installs profile-specific runtime/credential context and restores it afterward.

---

## 24. First session-binding attempt failed safely

An initial test tried standalone scoped-secret resolution without entering the Bristlecone runtime scope.

Result:

```text
Could not resolve Bristlecone API_SERVER_KEY.
```

The failure happened before the network call.

Therefore:

```text
API request: NO
Hermes session created: NO
Forest state write: NO
cleanup needed: NO
```

---

## 25. Bristlecone secret-scope probe passed

Inside:

```text
_profile_runtime_scope(profile_home)
```

verified:

```text
scope active: True
API_SERVER_KEY resolved: True
```

After exit:

```text
scope active: False
```

The key was never displayed.

---

## 26. Real Forest ↔ Hermes binding test passed

Forest Task:

```text
forest-task-20260809T000736Z-0013c37e
```

Real Hermes persisted session:

```text
api_1786234056_203cb1ee
```

Create:

```text
HTTP 201
```

Lookup:

```text
HTTP 200
```

Forest in-memory mapping correctly connected the two.

All verification checks passed.

Cleanup:

```text
Disposable Hermes session deleted: True
```

`active.yaml` and Hermes configuration remained unchanged.

---

## 27. Self-reliance architecture reviewed

Confirmed Forest-owned concepts include:

```text
Task identity
Task lifecycle
Workshops
capability registry
Task-Sticky policy
temporary capability policy
runtime-session mapping
cache lifecycle
canonical state
```

But `task_session.py` still contains Hermes-specific implementation details.

Examples:

```text
_save_platform_tools
CONFIGURABLE_TOOLSETS
Hermes config loading
Hermes Skill prompt building
```

Continuing to add Hermes authentication/session code there would increase coupling.

---

## 28. Decision: isolate Hermes behind a runtime adapter

Architecture chosen:

```text
The Forest
    ↓
Forest runtime interface
    ↓
Hermes runtime adapter
    ↓
Hermes
```

Meaning:

> Forest says **what** it needs.  
> The adapter knows **how Hermes does it**.

Existing:

```text
adapters/hermes.yaml
```

continues to describe mappings.

New:

```text
runtime/adapters/hermes.py
```

will perform Hermes-specific operations.

---

## 29. Latest Hermes coupling inventory

Read-only scan of `runtime/task_session.py` found:

```text
571  _load_hermes_toolset_runtime
686  _hermes_configurable_toolsets
711  begin_temporary_runtime_toolsets
850  restore_temporary_runtime_toolsets
933  _build_hermes_skill_overlay
1175 prepare_temporary_skill_overlay
1297 prepare_turn_skill_overlay
```

Runtime package currently:

```text
runtime/
├── __init__.py
└── task_session.py
```

No Python runtime adapter package exists yet.

---

# NEXT STEPS ONLY

1. Create:

```text
runtime/adapters/__init__.py
runtime/adapters/base.py
runtime/adapters/hermes.py
```

2. Define a minimal Forest-facing runtime contract.

3. Extract Hermes toolset/runtime-loading code first.

4. Keep temporary compatibility wrappers if needed.

5. Re-run:
   - unified temporary-turn normal-path test;
   - exception-restoration test;
   - exact baseline verification.

6. Extract `_build_hermes_skill_overlay` into the Hermes adapter.

7. Re-run:
   - Task-Sticky Skill cache test;
   - temporary Skill cache test;
   - combined debugging+testing test;
   - next-turn temporary drop test;
   - Task-end cache cleanup.

8. Move Hermes profile secret scope and API authentication behind the adapter.

9. Add adapter session operations:
   - create
   - get
   - send turn
   - end

10. Make `TaskSessionManager` runtime-agnostic.

11. Persist Forest↔Hermes runtime mapping.

12. Reuse the mapped Hermes session across turns.

13. Compare every returned effective Hermes session ID with current mapping.

14. If Hermes rotates:
   - previous = old;
   - current = returned effective ID;
   - update timestamp.

15. Use `retired_runtime_sessions` for Task-end runtime cleanup.

16. Add generation/ownership protection for concurrent runtime transactions.

17. Run one unified Phase 2 end-to-end verifier.

---

# Exact Resume Rule

**Do not add more Hermes-specific behavior directly to `task_session.py`.**

Resume by creating the runtime adapter package and extracting the already-proven Hermes toolset transaction first.
