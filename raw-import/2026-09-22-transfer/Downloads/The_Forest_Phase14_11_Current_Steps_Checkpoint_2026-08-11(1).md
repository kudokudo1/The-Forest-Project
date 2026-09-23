# The Forest — Bristlecone Pine
## Phase 14.11 Current Engineering Checkpoint
### E4E3C2 Transaction Integration → E4E5 End-to-End Certification
**Date:** 2026-08-11  
**Scope:** Only the most current engineering work. This file intentionally does **not** repeat the full Forest history, Phase 0–14.10 history, broad doctrine, or older setup details except where necessary to safely resume the current transaction work.

---

# 1. Purpose

This is a focused continuation checkpoint for the latest Bristlecone Pine / Model Form work inside:

```text
Phase 14.11 — Small / Big Model Escalation
```

It covers the most recent implementation sequence from the certified handoff rollback substrate through the completed E4E3C2 transaction integration and the immediate next step, E4E5 end-to-end handoff certification.

Use this file when the large master checkpoint is more history than is needed.

Current direction:

```text
✅ 14.11E4E3C1   CAS-aware runtime binding rollback
✅ 14.11E4E3C2A   Initial handoff bootstrap / persistence
✅ 14.11E4E3C2B1  Continuity-aware stale recovery
✅ 14.11E4E3C2B2A Failure / success cleanup primitives
✅ 14.11E4E3C2B2B Frozen handoff transaction integration
→  14.11E4E5      End-to-end Model Form handoff certification
□  14.11F         Resource Request + Governor Contract
□  14.11G         Automatic Escalation Router
□  14.11H         Colony Runtime / Shared-Weight Semantics
□  14.11I         Fake-Adapter Certification
□  14.11J         Real Small Runtime Certification
□  14.11K         Real Big Runtime Boundary Test
□  14.11L         Model Form Benchmark
```

E4E3C2 is assembled and individually certified through B2B. E4E5 is the next active task.

---

# 2. Critical Resume Marker

Current live source:

```text
/home/user/The-Forest/bristlecone/runtime/task_session.py
```

Current fully certified SHA256:

```text
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

Current fully certified rollback copy:

```text
bristlecone/backups/
phase14_11E4E3C2B2B_certified_20260811T174522Z/
task_session.py
```

That backup is byte-identical to the current certified live source.

If the live SHA differs from the value above, stop before continuing. Determine exactly why it changed before editing or restoring anything.

---

# 3. Current Phase 14.11 Status

```text
✅ 14.11A     Canonical Model Form Contract
✅ 14.11B     Model Form Control State / execution-context isolation
✅ 14.11C     Runtime-Neutral Model Registry
✅ 14.11D-0   Runtime Binding / Session Identity prerequisite
✅ 14.11D1    Effective Model Form Resolution + Freeze
✅ 14.11D2    Public Resolution API
✅ 14.11D3    TaskSession Resolution Integration
✅ 14.11D4A   Self-contained Runtime Binding
✅ 14.11D4B   Ephemeral Frozen Runtime View
✅ 14.11D4C1  Identity-aware Session Ensure
✅ 14.11D4C2  Identity-aware Persistence / CAS
✅ 14.11D4D1  Frozen Normal Send Path
✅ 14.11D5    Frozen Stale Recovery / Retry Freeze

✅ 14.11E1     Immutable ModelFormHandoff Contract
✅ 14.11E2     Pure Handoff Detection
✅ 14.11E3A    Frozen Instruction Continuity substrate
✅ 14.11E3B    Portable ConversationContinuity
✅ 14.11E3C    Combined ModelFormContinuity
✅ 14.11E4A    Canonical context-local state shape
✅ 14.11E4B    Effective-form read/write helpers
✅ 14.11E4C    Conversation read/write helpers
✅ 14.11E4D    Successful-turn semantic commit integration
✅ 14.11E4E1   Pure handoff-continuity preparation
✅ 14.11E4E2   Runtime-neutral continuity-bootstrap contract
✅ 14.11E4E3A  Typed instruction-composition passthrough
✅ 14.11E4E3B  Handoff runtime bootstrap helper
✅ 14.11E4E3C1 CAS-aware binding rollback
✅ 14.11E4E3C2A Initial handoff transaction bootstrap
✅ 14.11E4E3C2B1 Continuity-aware stale recovery
✅ 14.11E4E3C2B2A Handoff cleanup / retirement primitives
✅ 14.11E4E3C2B2B Frozen handoff transaction integration

→ 14.11E4E5 End-to-end handoff certification

□ 14.11F Resource Request + Governor Contract
□ 14.11G Automatic Escalation Router
□ 14.11H Colony Runtime / Shared-Weight Semantics
□ 14.11I Fake-Adapter Certification
□ 14.11J Real Small Runtime Certification
□ 14.11K Real Big Runtime Boundary Test
□ 14.11L Model Form Benchmark
```

---

# 4. Current Model Form Transaction

The transaction now behaves conceptually as:

```text
resolve / freeze Reasoning
        ↓
resolve / freeze Model Form
        ↓
read previous successful effective form
        ↓
prepare handoff
        ↓
actual form change?
 ┌──────┴────────┐
 no              yes
 │                ↓
 │          build exact ModelFormContinuity
 │                ↓
 │          fresh target-form runtime session
 │                ↓
 │          persist runtime binding before send
 │                ↓
 └──────────────→ send current user message
                  ↓
                stale?
              ┌───┴────┐
              no       yes
              │         ↓
              │    fresh replacement
              │    from SAME continuity
              │         ↓
              │    persist replacement
              │    before retry
              │         ↓
              │       retry once
              └────┬────┘
                   ↓
          normalize final runtime binding
                   ↓
        freeze rollback guard at final
        durable runtime generation
                   ↓
             E4D semantic commit
          ┌────────┴─────────┐
        success             failure
          │                    ↓
          │              C1 Forest rollback
          │                    ↓
          │              safe runtime cleanup
          ↓
 retire old target and obsolete
 handoff-created runtime sessions
 AFTER semantic success
```

---

# 5. Core Transaction Invariants

## 5.1 Same-form path

A same-form turn must remain on the existing D5 path.

Examples:

```text
Small → Small
Big → Big
```

Requirements:

- no Model Form handoff bootstrap;
- no portable continuity requirement;
- ordinary session ensure/reuse remains valid;
- same-form stale recovery may use ordinary `create_session()`;
- B2 transaction rollback/retirement logic must not alter successful same-form turns.

## 5.2 Actual handoff path

Examples:

```text
Small → Big
Big → Small
```

Requirements:

- previous successful form differs from frozen target form;
- handoff uses `ModelFormContinuity`;
- target-form runtime session is fresh;
- old dormant target-form session is not reused;
- old target remains alive as rollback anchor until semantic success.

## 5.3 Continuity

The handoff continuity package contains only prior completed Forest-owned state.

It must not contain:

- current in-flight user message as a completed exchange;
- runtime KV cache;
- runtime session identity;
- reasoning scratch state;
- tool execution state;
- in-flight operations.

The current user message is sent normally after continuity bootstrap.

## 5.4 Retry freeze

If the first target runtime session is verified stale:

- only the stale classifier may trigger recovery;
- create one fresh replacement;
- actual handoff recovery uses the **same exact frozen ModelFormContinuity**;
- same execution context;
- same binding;
- same frozen form;
- same frozen reasoning;
- same exact instruction object;
- same exact user message;
- no rerouting;
- no context recomputation;
- no source-context recomputation;
- no learning reassembly;
- at most one retry.

## 5.5 Persistence ordering

For `persist=True`:

```text
create/select runtime generation
    ↓
write detached binding
    ↓
CAS persist binding
    ↓
ONLY THEN send to runtime
```

The same ordering applies to stale replacement and final runtime rotation.

## 5.6 Semantic boundary

`_commit_successful_model_form_turn(...)` remains the one Forest-owned success boundary.

Success commits together:

- frozen effective Model Form;
- completed user/assistant exchange;
- successful Reasoning-control finalization / temporary lease consumption.

Failure must not partially commit those semantics.

## 5.7 Retirement

Before E4D succeeds:

```text
old target session = rollback anchor
```

After E4D succeeds:

```text
old target may retire
obsolete handoff-created sessions may retire
final canonical session must survive
```

## 5.8 Rollback race

If a newer writer advances the canonical binding before C1 rollback:

```text
do not overwrite newer Forest truth
do not blindly end the newer canonical runtime session
```

Cleanup is permitted only for transaction-owned sessions proven noncanonical.

If canonical truth cannot be safely inspected, cleanup fails closed.

---

# 6. E4E3C1 — CAS-Aware Rollback

Certified helper:

```python
_rollback_runtime_binding_guarded_for_identity(
    working,
    guard,
    restore_binding,
)
```

Its job is Forest-state repair only.

It does not:

- create runtime sessions;
- end runtime sessions;
- send turns;
- semantic-commit;
- consume reasoning.

Rollback guard identity:

```text
task_id
execution_context_id
binding_id
adapter
session_id
```

Rollback succeeds only if the durable canonical slot still matches the transaction generation.

A newer Task, adapter, session generation, or missing binding blocks rollback.

Successful rollback returns the latest repaired Forest state.

Representative fail-closed errors observed in recon:

```text
Runtime rollback guard must be a mapping.
Runtime rollback guard is incomplete.
Runtime rollback guard does not match the supplied active Task.
Runtime rollback restore binding must be a mapping or None.
Runtime rollback restore binding is incomplete.
Runtime rollback restore binding uses a different adapter.
Persistent runtime rollback refused: the active Forest Task changed.
Latest canonical runtime_sessions is not a mapping.
Stale runtime rollback: the target binding disappeared.
Stale runtime rollback adapter: persisted adapter changed before rollback.
Stale runtime rollback session: expected ..., found ...
Stale runtime rollback: execution-context session bucket disappeared.
Stale runtime rollback: binding disappeared before removal.
Could not read latest canonical runtime binding for rollback.
Could not restore canonical runtime binding.
```

Certified C1 backup:

```text
bristlecone/backups/
phase14_11E4E3C1_certified_20260811T163126Z/
task_session.py
```

SHA256:

```text
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c
```

---

# 7. E4E3C2A — Initial Handoff Bootstrap

C2A integrated the certified continuity bootstrap into the frozen send path.

For an actual Model Form change:

1. capture previous successful form;
2. prepare `ModelFormHandoff` and `ModelFormContinuity`;
3. capture old target binding;
4. create a fresh target-form session from continuity;
5. write fresh target binding into detached state;
6. if persistent, CAS-persist before first model send;
7. preserve old target as rollback anchor.

Same-form turns continue through ordinary D5 session acquisition.

Behavior certification proved:

```text
PASS: first successful-form baseline does not bootstrap a handoff
PASS: same-form warm turn retains ordinary D5 session acquisition
PASS: same-form warm turn remains pre-turn write-free
PASS: actual Small -> Big handoff bypasses ordinary session ensure
PASS: actual handoff captures old target before fresh bootstrap
PASS: actual handoff creates a fresh continuity-bootstrapped target session
PASS: fresh handoff binding is persisted before first runtime send
PASS: first handoff send uses the fresh target session
PASS: old target session is not retired before semantic commit
PASS: failed pre-turn handoff CAS prevents runtime/model send
PASS: failed pre-turn handoff CAS cleans only the fresh child
PASS: failed pre-turn handoff CAS preserves the old target session
PASS: every tested turn performs one handoff-preparation decision
PASS: every tested turn performs one meaningful-input transition
```

Certified C2A backup:

```text
bristlecone/backups/
phase14_11E4E3C2A_certified_20260811T171153Z/
task_session.py
```

SHA256:

```text
451633e52832447b4585c8c1953913e8bda0d48589e1cda4279bbf62675c737d
```

---

# 8. E4E3C2B1 — Continuity-Aware Stale Recovery

B1 changed stale recovery so handoffs do not lose Forest continuity.

Same-form stale recovery remains:

```python
create_session()
```

Actual handoff stale recovery becomes:

```text
fresh continuity bootstrap
using SAME ModelFormContinuity
```

Structural certification proved:

```text
PASS: B1 changed only the frozen Model Form send method
PASS: B1 adds exactly one new handoff bootstrap site
PASS: B1 contains no semantic rollback integration
PASS: stale Model Form handoff branch located
PASS: stale handoff replacement uses current detached working state
PASS: stale handoff replacement reuses the same frozen ModelFormContinuity
PASS: handoff stale branch bypasses ordinary create_session
PASS: same-form stale branch retains ordinary create_session
PASS: ordinary stale creator remains exactly once
PASS: D5 binding/persistence/cleanup call counts are unchanged
PASS: runtime sender count is unchanged
PASS: E4D remains exactly one semantic commit
PASS: semantic commit remains after all runtime send sites
PASS: existing D5 recovery state remains present
PASS: certified C2A handoff state remains present
```

Behavior certification proved:

```text
PASS: same-form stale recovery uses ordinary create_session
PASS: same-form stale recovery performs exactly one replacement
PASS: same-form stale recovery performs exactly one retry
PASS: same-form stale recovery classifies stale exactly once
PASS: same-form replacement is persisted before retry
PASS: same-form retry preserves message, instructions, and reasoning

PASS: handoff stale recovery bypasses ordinary create_session
PASS: handoff stale recovery creates a second fresh continuity session
PASS: initial and stale handoff bootstrap use the SAME continuity object
PASS: handoff stale replacement is persisted before retry
PASS: handoff stale recovery performs exactly one retry
PASS: handoff stale recovery classifies stale exactly once
PASS: handoff retry preserves message, instructions, and reasoning
PASS: old handoff target remains untouched by B1 cleanup

PASS: both stale paths perform one meaningful-input transition
PASS: both stale paths prepare handoff state exactly once
PASS: behavioral certification did not modify task_session.py
```

Certified B1 backup:

```text
bristlecone/backups/
phase14_11E4E3C2B1_certified_20260811T172216Z/
task_session.py
```

SHA256:

```text
b761c7d4eeab8b0635b664cba828406fa213bf631f0a0e7165e8c7d5d86cbbd0
```

---

# 9. E4E3C2B2A — Cleanup / Retirement Primitives

B2A added helper-only transaction cleanup infrastructure before touching the live send flow.

Helpers:

```python
_cleanup_failed_model_form_handoff_transaction(...)
```

and:

```python
_retire_successful_model_form_handoff_sessions(...)
```

## Failure helper behavior

For persistent failures:

1. C1 rollback first;
2. if rollback succeeds, restored target becomes canonical;
3. old target excluded from cleanup;
4. failed transaction sessions may retire;
5. if rollback loses a race, reload latest Forest state;
6. inspect latest canonical binding;
7. exclude current canonical session;
8. clean only proven noncanonical transaction sessions;
9. if latest canonical truth cannot be established, end nothing.

For `persist=False`:

- no C1 rollback;
- no durable Forest read;
- clean detached handoff children;
- preserve old target.

## Success helper behavior

Called only after E4D success.

It:

- receives final canonical session ID;
- receives old replaced target;
- receives transaction-created runtime session IDs;
- deduplicates candidates;
- excludes final canonical session;
- retires old target and obsolete children;
- performs no Forest rollback.

Behavior certification:

```text
PASS: successful C1 rollback occurs before runtime cleanup
PASS: restored old target is never retired after rollback
PASS: duplicate transaction sessions are cleaned only once
PASS: rollback race loss preserves newer Forest truth
PASS: newer canonical transaction session is excluded from cleanup
PASS: only proven noncanonical transaction sessions are retired
PASS: unknown durable canonical truth fails closed
PASS: no runtime session is retired when canonical ownership is unknown
PASS: persist=False performs no durable Forest rollback
PASS: persist=False still cleans failed handoff runtime children
PASS: persist=False preserves the old target session
PASS: post-E4D success retires the old replaced target
PASS: post-E4D success retires obsolete transaction sessions
PASS: final canonical session is never retired
PASS: behavioral certification did not modify source
```

Certified B2A backup:

```text
bristlecone/backups/
phase14_11E4E3C2B2A_certified_20260811T173230Z/
task_session.py
```

SHA256:

```text
7184ff36637eba106e03af6cccc10fc11d5cd18d67397662f561c657a3a97a40
```

Pre-B2A backup:

```text
bristlecone/backups/
phase14_11E4E3C2B2A_pre_cleanup_primitives_20260811T172959Z/
task_session.py
```

---

# 10. E4E3C2B2B — Frozen Transaction Integration

B2B wired the B2A helpers into the live frozen Model Form send transaction.

Pre-B2B backup:

```text
bristlecone/backups/
phase14_11E4E3C2B2B_pre_frozen_transaction_20260811T173920Z/
task_session.py
```

## 10.1 Transaction-local ownership

B2B introduced transaction-local tracking for actual handoffs:

```text
handoff_transaction_session_ids
handoff_rollback_guard
initial_handoff_session_id
recovery_handoff_session_id
```

These distinguish transaction sessions from:

- old rollback target;
- final canonical session;
- newer concurrent canonical session.

## 10.2 D5 cleanup isolation

Existing direct D5 cleanup remains for same-form behavior.

Actual handoff failures bypass those direct cleanup sites and centralize through:

```python
_cleanup_failed_model_form_handoff_transaction(...)
```

This ensures:

```text
rollback first
cleanup second
```

## 10.3 Rollback guard advancement

Recon showed the normal guard advances after:

- initial handoff persistence;
- stale replacement persistence.

Runtime success may then rotate again:

```text
effective_session_id = result["session_id"]
```

B2B therefore advances the rollback guard after a persisted final rotation so C1 names the **final durable generation** before E4D.

## 10.4 Failure wrapper

The runtime-to-E4D handoff transaction is failure guarded.

Conceptually:

```text
try:
    runtime work
    stale recovery if needed
    final binding normalization
    E4D commit
except:
    if actual handoff:
        B2A failed-handoff cleanup
    re-raise original transaction error
```

The cleanup helper is itself protected so cleanup errors do not replace the original failure.

## 10.5 Success retirement

Only after E4D succeeds:

```python
_retire_successful_model_form_handoff_sessions(...)
```

receives:

```text
final_session_id = binding["session_id"]
replaced_session_id = old target
transaction_session_ids = handoff-created/advanced sessions
```

The final canonical session is preserved.

---

# 11. B2B Installation / Structural Results

Installation reported:

```text
PASS: live source matches certified E4E3C2B2A
PASS: certified B2A/B1 transaction shape located
PASS: all B2B mutation landmarks located
PASS: pre-E4E3C2B2B source backed up
PASS: handoff transaction generation tracking generated successfully
PASS: same-form D5 cleanup retained; handoff cleanup centralized
PASS: runtime-to-E4D handoff transaction is now failure-guarded
PASS: B2B changes only frozen Model Form send behavior
PASS: same-form D5 sender, persistence, and cleanup topology is preserved
PASS: actual handoff bypasses old direct D5 cleanup sites
PASS: actual handoff failures centralize through certified B2A cleanup
PASS: preturn and stale-recovery durable generations freeze rollback guards
PASS: final runtime rotation advances rollback guard before E4D
PASS: E4D remains exactly one semantic success boundary
PASS: old target retirement occurs only after E4D returns successfully
PASS: final canonical session is passed to certified success retirement
PASS: frozen send performs no direct C1 rollback
PASS: 14.11E4E3C2B2B source update complete
```

New live SHA:

```text
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

Compile result:

```text
patch status: 0
compile status: 0
```

---

# 12. B2B Live Transaction Behavioral Certification

The B2B behavior harness exercised the integrated frozen send transaction with synthetic runtime/persistence boundaries.

Source guard:

```text
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

The test did not modify source.

## 12.1 Same-form regression

```text
PASS: same-form successful turn remains on ordinary D5 path
PASS: B2B adds no rollback or retirement to same-form success
```

## 12.2 Pre-turn CAS failure

```text
PASS: failed pre-turn handoff CAS prevents model send
PASS: failed pre-turn handoff CAS does not attempt C1 rollback
PASS: failed pre-turn handoff CAS cleans its fresh transaction child
PASS: old target remains untouched when pre-turn persistence never commits
```

## 12.3 Initial send failure

```text
PASS: persisted handoff send failure rolls Forest binding back first
PASS: initial handoff failure cleanup occurs only after C1 rollback
PASS: initial handoff failure preserves the old target rollback anchor
```

Correct order:

```text
persist
→ send
→ rollback
→ cleanup
```

## 12.4 Stale replacement then retry failure

```text
PASS: failed stale retry rolls back from the replacement generation
PASS: stale retry failure cleans both handoff-created generations
PASS: stale retry remains exactly once
PASS: stale retry keeps the same message, instructions, reasoning, and ModelFormContinuity
```

## 12.5 Final runtime rotation + E4D failure

```text
PASS: final runtime rotation advances the rollback guard to the final generation
PASS: E4D failure after runtime rotation rolls back final durable runtime truth
PASS: E4D failure retires only failed handoff generations after rollback
```

This specifically proves rollback names the final runtime generation.

## 12.6 Rollback race loss

```text
PASS: rollback race loss preserves newer durable Forest truth
PASS: rollback race loss re-reads latest canonical runtime identity
PASS: current canonical transaction session is never retired after race loss
PASS: only proven noncanonical transaction sessions are cleaned
```

## 12.7 Detached failure

```text
PASS: persist=False handoff failure performs no durable C1 rollback
PASS: persist=False handoff failure still retires its runtime child
PASS: persist=False preserves the old target session
```

## 12.8 Successful stale + rotation handoff

```text
PASS: successful handoff commits semantic Forest truth exactly once
PASS: old target remains alive until E4D succeeds
PASS: post-E4D retirement removes the old target and obsolete children
PASS: final canonical runtime session survives successful retirement
PASS: successful stale+rotation handoff returns the final canonical session
```

## 12.9 Shared invariants

```text
PASS: every tested turn performs one meaningful-input transition
PASS: every tested turn prepares handoff state exactly once
PASS: B2B behavioral certification did not modify task_session.py
```

Final:

```text
PASS: 14.11E4E3C2B2B live transaction behavior certification
Live SHA256: a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71

14.11E4E3C2B2B behavior status: 0
```

---

# 13. Current Certified Backup Ledger

## E4E3C1

```text
bristlecone/backups/
phase14_11E4E3C1_certified_20260811T163126Z/
task_session.py

SHA256:
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c
```

## E4E3C2A

```text
bristlecone/backups/
phase14_11E4E3C2A_certified_20260811T171153Z/
task_session.py

SHA256:
451633e52832447b4585c8c1953913e8bda0d48589e1cda4279bbf62675c737d
```

## E4E3C2B1

```text
bristlecone/backups/
phase14_11E4E3C2B1_certified_20260811T172216Z/
task_session.py

SHA256:
b761c7d4eeab8b0635b664cba828406fa213bf631f0a0e7165e8c7d5d86cbbd0
```

## E4E3C2B2A

```text
bristlecone/backups/
phase14_11E4E3C2B2A_certified_20260811T173230Z/
task_session.py

SHA256:
7184ff36637eba106e03af6cccc10fc11d5cd18d67397662f561c657a3a97a40
```

## E4E3C2B2B — CURRENT

```text
bristlecone/backups/
phase14_11E4E3C2B2B_certified_20260811T174522Z/
task_session.py

SHA256:
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

---

# 14. Recent Pre-Edit Backups

## Pre-B1

```text
bristlecone/backups/
phase14_11E4E3C2B1_pre_stale_continuity_20260811T171559Z/
task_session.py
```

Baseline SHA:

```text
451633e52832447b4585c8c1953913e8bda0d48589e1cda4279bbf62675c737d
```

## Pre-B2A

```text
bristlecone/backups/
phase14_11E4E3C2B2A_pre_cleanup_primitives_20260811T172959Z/
task_session.py
```

Baseline SHA:

```text
b761c7d4eeab8b0635b664cba828406fa213bf631f0a0e7165e8c7d5d86cbbd0
```

## Pre-B2B

```text
bristlecone/backups/
phase14_11E4E3C2B2B_pre_frozen_transaction_20260811T173920Z/
task_session.py
```

Baseline SHA:

```text
7184ff36637eba106e03af6cccc10fc11d5cd18d67397662f561c657a3a97a40
```

---

# 15. Source Generation Ledger

```text
E4E3C1
c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c

        ↓ C2A

451633e52832447b4585c8c1953913e8bda0d48589e1cda4279bbf62675c737d

        ↓ B1

b761c7d4eeab8b0635b664cba828406fa213bf631f0a0e7165e8c7d5d86cbbd0

        ↓ B2A

7184ff36637eba106e03af6cccc10fc11d5cd18d67397662f561c657a3a97a40

        ↓ B2B

a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

The final hash is the authoritative generation for E4E5 work.

---

# 16. Important Current Frozen-Send Variables

Recent recon showed these transaction generations.

Initial guard:

```text
persist_guard = None
```

then:

```text
persist_guard =
    _capture_runtime_persist_guard_for_identity(...)
```

Initial selected runtime session:

```text
requested_session_id = str(ensured["session_id"])
```

After initial durable advancement:

```text
persist_guard = {
    task_id: ...,
    execution_context_id: ...,
    binding_id: ...,
    adapter: ...,
    session_id: requested_session_id,
}
```

Stale recovery:

```text
recovery_session_id = None
```

after replacement:

```text
recovery_session_id = replacement_session_id
requested_session_id = replacement_session_id
```

and guard advances to:

```text
persist_guard = {
    ...
    session_id: replacement_session_id,
}
```

Final runtime success:

```text
effective_session_id = result.get("session_id")
effective_session_id = str(effective_session_id)
```

Detached canonical write:

```python
binding = self._write_runtime_session_binding_for_identity(
    working,
    frozen_turn.execution_context_id,
    frozen_turn.binding_id,
    adapter_name,
    effective_session_id,
    previous_session_id=previous_session_id,
)
```

After final persistent rotation B2B advances the rollback guard to `effective_session_id`.

Then canonical binding is reread:

```python
binding = self._runtime_session_binding_for_identity(
    working,
    frozen_turn.execution_context_id,
    frozen_turn.binding_id,
)
```

Then E4D:

```python
successful_turn_commit = (
    self._commit_successful_model_form_turn(...)
)
```

The normal result reports:

```text
session_id = binding["session_id"]
```

---

# 17. E4D Remains the Only Semantic Success Boundary

Current call:

```python
_commit_successful_model_form_turn(
    working=working,
    frozen_turn=frozen_turn,
    user_message=message,
    assistant_message=result.get("message", ""),
    expected_previous_form=turn_previous_effective_form,
    turn_control=turn_reasoning_control,
    decision=reasoning_decision,
    persist=persist,
)
```

E4D owns:

```text
effective_model_forms
conversation_continuity
reasoning success finalization
```

Successful state conceptually becomes:

```yaml
task_session:
  effective_model_forms:
    <execution_context_id>: <frozen target form>

  conversation_continuity:
    <execution_context_id>:
      schema_version: 1
      execution_context_id: <context>
      task_id: <task>
      exchanges:
        - user_message: <exact user message>
          assistant_message: <exact assistant result>
```

Failed runtime attempts must not append the current exchange.

A stale retry must not duplicate the exchange.

---

# 18. Current Runtime Continuity Limitation

The runtime-neutral adapter contract has:

```python
create_session_with_continuity(...)
```

The base adapter fails closed when unsupported.

At this checkpoint Hermes has **not** been certified as implementing this real continuity-bootstrap contract.

Therefore:

```text
synthetic/fake handoff certification:
    correct current activity

real Small→Big or Big→Small Hermes handoff:
    not ready
```

Do not interpret synthetic E4E5 success as real Hermes handoff certification.

---

# 19. E4E5 — Next Active Step

E4E5 should now test the complete Forest Model Form handoff chain instead of only isolated transaction pieces.

Target integrated chain:

```text
real typed ForestTurnInstructionComposition
        ↓
real E4E1 handoff detection/preparation
        ↓
real ConversationContinuity
        ↓
real ModelFormContinuity
        ↓
fake external runtime bootstrap
        ↓
actual frozen send path
        ↓
stale recovery / final rotation as configured
        ↓
real E4D semantic commit
        ↓
effective form + conversation + reasoning semantics
        ↓
post-E4D retirement
```

Where practical, only external boundaries should remain synthetic:

```text
runtime adapter I/O
durable disk writes
runtime adapter factory resolution if needed
```

---

# 20. E4E5 Certification Matrix

## Baseline / same-form

Test:

```text
first Small success
Small → Small
Big → Big
```

Expected:

- no handoff bootstrap;
- no continuity requirement;
- ordinary D5 session semantics;
- one current user send;
- E4D exactly once on success;
- current exchange appended once;
- effective form correct;
- no handoff retirement.

## Small → Big

Expected:

- handoff detected;
- exact typed instruction composition required;
- continuity includes only prior completed conversation;
- fresh Big target session;
- old Big target retained until E4D;
- current user message sent exactly once;
- E4D commits Big;
- current exchange appended once;
- old replaced Big target retired afterward;
- final canonical Big session survives.

## Big → Small

Same semantics in reverse.

## Context isolation

Example:

```text
ctx-A → binding-small → session-A
ctx-B → binding-small → session-B
```

Handoff in `ctx-A` must not alter:

- `ctx-B` runtime binding;
- `ctx-B` effective form;
- `ctx-B` conversation continuity.

## Task isolation

Continuity from Task A must never bootstrap Task B.

Task identity and execution-context identity both matter.

## Unsupported runtime

Base fail-closed continuity behavior must reject an actual handoff instead of pretending continuity exists.

Expected:

- no semantic commit;
- old target remains authoritative;
- no false continuity success.

## Pre-turn CAS failure

Expected:

- fresh target created;
- CAS fails before send;
- no user send;
- no E4D;
- no conversation append;
- no reasoning lease consumption;
- child cleaned;
- old target preserved.

## Initial send failure

Expected:

- durable fresh binding may exist;
- no E4D;
- C1 rollback;
- old target restored;
- child cleaned after rollback.

## Stale handoff

Expected:

- first target verified stale;
- one second fresh session;
- same `ModelFormContinuity`;
- replacement persisted before retry;
- same exact current user message;
- same instructions object;
- same reasoning;
- same context/binding/form;
- one retry only.

## Retry failure

Expected:

- no E4D;
- rollback from replacement generation;
- failed handoff children cleaned when noncanonical;
- old target preserved.

## Final rotation + semantic failure

Expected:

- final runtime generation persisted;
- E4D fails;
- C1 guard names final generation;
- durable runtime truth rolled back if still ours.

## Rollback race

Expected:

- C1 refuses to overwrite newer writer;
- latest canonical binding reread;
- canonical session excluded from cleanup;
- only proven noncanonical transaction sessions retired.

## Reasoning lease

Temporary reasoning:

- not consumed on initial failure;
- not consumed on stale first attempt;
- not consumed on retry failure;
- consumed exactly once after final successful semantic commit.

## Conversation continuity

Prove:

- bootstrap continuity contains prior completed exchanges only;
- current user message is not pre-inserted as a completed exchange;
- stale recovery reuses same continuity package;
- current message is sent normally;
- success appends completed exchange once;
- no duplicate exchange after retry.

---

# 21. Immediate Pending Recon Before E4E5 Harness

The latest planned next command is a read-only contract recon.

It should print:

```text
===== CORE METHOD SIGNATURES =====
===== LIVE TYPE CONTRACTS =====
===== E4E1 HANDOFF PREPARATION =====
===== E4D SEMANTIC COMMIT =====
===== SEMANTIC STATE HELPERS =====
===== PUBLIC SEND PASSTHROUGH =====
```

Purpose:

- exact constructors for live handoff/continuity dataclasses;
- exact live method signatures;
- real E4E1 return shape;
- real E4D return shape;
- conversation/effective-form helper contracts;
- public typed `instruction_composition` passthrough.

Do not guess constructors when building E4E5.

---

# 22. Live Types E4E5 Should Resolve

Expected relevant symbols:

```text
ForestTurnInstructionComposition
ConversationContinuity
ConversationExchange
ModelFormContinuity
ModelFormHandoff
FrozenModelFormTurn
ModelFormDecision
```

Use real live types whenever possible rather than `SimpleNamespace` stand-ins.

E4E5 is meant to certify semantic integration, not only runtime mechanics.

---

# 23. Exact Instruction Object Rule

Already-certified typed composition rules:

```text
if instruction_composition omitted:
    legacy callers remain valid

if supplied:
    it must be ForestTurnInstructionComposition

if instructions omitted:
    use instruction_composition.instructions

if both supplied:
    they must be the exact same string object
```

Equality alone is insufficient.

Conceptually:

```python
instructions is instruction_composition.instructions
```

must be true when both are provided.

E4E5 should retain this guarantee through a successful handoff.

---

# 24. Conversation Continuity Rule

`ConversationContinuity` is:

- ordered;
- completed exchanges only;
- Task-local;
- execution-context local;
- runtime-neutral.

It must not contain:

- runtime session ID;
- adapter ID;
- KV state;
- reasoning state;
- tool state;
- in-flight turn state.

`ModelFormContinuity` combines:

```text
ForestTurnInstructionComposition
+
ConversationContinuity
```

The runtime receives a portable package and creates its own fresh runtime representation.

---

# 25. Why Old Target Retirement Must Wait

Suppose:

```text
Small is current successful form
Big has an old dormant target session
Small → Big begins
```

The new Big session may be created, persisted, used, replaced, or rotated.

Until E4D commits the successful turn:

```text
old Big target = rollback anchor
```

If semantic commit fails:

```text
Forest must be able to restore old Big binding
```

Therefore B2B enforces:

```text
E4D first
retirement second
```

---

# 26. Why Final Rotation Guard Advancement Matters

Example:

```text
old target = big-old
initial handoff child = big-continuity-1
runtime final session = big-final
```

Durable sequence:

```text
big-old
   ↓
big-continuity-1
   ↓
big-final
```

If E4D fails after `big-final` is persisted, rollback must compare against:

```text
big-final
```

not:

```text
big-continuity-1
```

Otherwise C1 correctly refuses the rollback as stale.

B2B explicitly fixed this and the behavior harness certified it.

---

# 27. Rollback Failure Is Not Automatically Cleanup Failure

A rollback may fail because another valid writer advanced the canonical slot.

Example:

```text
our failed transaction:
  big-continuity-1
  big-final

newer Forest truth:
  canonical = big-final
```

Even if `big-final` originally came from this transaction, it may now be canonical under newer Forest truth.

Therefore B2A:

```text
rollback fails
    ↓
reload latest Forest state
    ↓
read current canonical session
    ↓
exclude canonical session from cleanup
```

Historical creation alone does not decide deletion safety.

Current canonical truth does.

---

# 28. Fail-Closed Cleanup

If:

```text
rollback fails
AND
latest canonical binding cannot be inspected
```

then:

```text
cleanup_session_ids = ()
```

No runtime sessions are ended.

This may temporarily leak resources, but avoids destroying an unknown canonical session.

Priority:

```text
1. preserve canonical correctness
2. prevent session destruction
3. clean resources when safe
```

---

# 29. Same-Form Fast Path Boundary

Future E4E5 and Resource changes must not make every turn a handoff transaction.

Current same-form success is certified as:

```text
ordinary D5 path
no handoff bootstrap
no B2 rollback
no B2 success retirement
normal warm session reuse
```

Preserve this path.

---

# 30. Real Runtime Safety Rule

Do not run a real Small→Big or Big→Small handoff merely because B2B passed.

Current fully safe activities:

```text
read-only recon
synthetic fake-adapter certification
source structural certification
transaction harnesses
```

Real Hermes continuity remains unproven.

Do not call a live Hermes handoff certified until the adapter actually implements and passes continuity bootstrap semantics.

---

# 31. Immediate Resume Procedure

In Cherry-AI:

```bash
cd /home/user/The-Forest
```

Verify:

```bash
sha256sum bristlecone/runtime/task_session.py
```

Expected:

```text
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

If different:

```text
STOP
```

Inspect before changing anything.

Certified rollback source:

```text
bristlecone/backups/
phase14_11E4E3C2B2B_certified_20260811T174522Z/
task_session.py
```

Then continue with:

```text
14.11E4E5 contract recon
```

not with new architecture.

---

# 32. What Not to Do Next

Do not:

- start 14.11F before E4E5 closes;
- replace the Small baseline model yet;
- activate the staged Big model;
- run a real Big handoff on current hardware;
- add Hermes-specific fields to the runtime-neutral Model Form contract;
- put runtime session IDs into `ModelFormHandoff`;
- include current in-flight input inside completed continuity;
- add a second stale retry;
- recompute retrieval/context on retry;
- retire old target before E4D;
- let cleanup overwrite the original transaction exception;
- let rollback clobber a newer writer;
- end a session only because this transaction originally created it;
- modify current source without a timestamped backup.

---

# 33. Current Development Safety Procedure

Continue:

```text
1. exact source hash guard
2. read-only recon
3. uniquely identify mutation landmarks
4. timestamped pre-edit backup
5. generate change in memory
6. AST parse before write
7. structural assertions before write
8. write source
9. py_compile
10. synthetic behavioral certification
11. certified backup
12. record final SHA
```

If a step fails:

```text
do not blindly rerun
inspect exact failure first
```

---

# 34. Shell Safety Reminder

For interactive Cherry/Maple terminal work, do not paste bare:

```bash
set -euo pipefail
```

Do not use unnecessary:

```bash
exit
```

or:

```bash
cd ... || exit 1
```

when failure could close the interactive terminal.

For fail-fast work use a subshell:

```bash
(
  set -euo pipefail
  ...
)
```

or a standalone script.

Capture exit status immediately:

```bash
some_command
status=$?
echo "$status"
```

A previous workflow accidentally displayed `0` after another command overwrote `$?`.

---

# 35. Current Architecture Separation

## Forest owns

```text
Tree identity
Model Form meaning
execution-context identity
Task identity
continuity semantics
effective successful form
conversation continuity
rollback policy
resource policy
semantic commit
```

## Runtime adapter owns

```text
runtime-specific session creation
runtime-specific continuity translation
model send
runtime stale classification
runtime session ending
runtime session rotation reporting
```

## ModelFormHandoff remains runtime-neutral

Do not add:

```text
session_id
adapter
provider
vendor
model path
runtime cache
continuity payload
```

## Transaction locals may hold runtime mechanics

Examples:

```text
rollback guard
transaction session IDs
old replaced session
current effective session
```

Those remain implementation details, not semantic handoff fields.

---

# 36. Current Runtime Session Identity

Identity is scoped by:

```text
(execution_context_id, binding_id)
```

This permits:

```text
ctx-A + binding-small → session-A
ctx-B + binding-small → session-B
```

even with shared model weights.

E4E5 must preserve context isolation.

---

# 37. Canonical Runtime Session State Shape

Conceptually:

```yaml
task_session:
  runtime_sessions:
    ctx-A:
      binding-0001:
        adapter: hermes
        session_id: session-A
        previous_session_id: null
        updated_at: ...
```

Execution-context identity, binding identity, and runtime session identity remain distinct.

---

# 38. Current Model Registry Reality

Current real registry is partial.

Conceptually:

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

Small is bound.

Big remains intentionally unbound in the normal active registry.

Synthetic adapters can still certify handoff semantics without pretending a real Big runtime is ready.

---

# 39. Real Model Situation Relevant Now

Small baseline remains the current Bristlecone Qwen runtime.

Big candidate staged separately:

```text
mistralai/Mistral-Small-4-119B-2603-NVFP4
```

It is staged only.

It has not been:

- loaded;
- connected to Model Form;
- activated;
- used for real handoff certification.

The current machine is not expected to comfortably run a ~60+ GB Big runtime locally.

E4E5 should remain synthetic/runtime-neutral.

---

# 40. Hermes Compatibility Boundary

Hermes remains the preferred Bristlecone orchestration layer.

Relevant runtime facts:

```text
Hermes gateway:
127.0.0.1:8643

Ollama:
127.0.0.1:11434

Hermes service:
hermes-bristlecone.service

Hermes profile:
~/.hermes/profiles/bristlecone
```

But the current E4 limitation remains:

```text
BaseRuntimeAdapter.create_session_with_continuity(...)
    exists

Hermes:
    not yet certified for real continuity handoff
```

Do not bypass the fail-closed contract merely to make a live test run.

---

# 41. What E4E5 Completion Means

If E4E5 passes, the correct claim is:

```text
The Forest Model Form handoff transaction
is end-to-end certified against the synthetic
runtime boundary.
```

That should cover:

- semantic handoff detection;
- typed instruction continuity;
- conversation continuity;
- fresh target bootstrap;
- persistence ordering;
- stale retry;
- final rotation;
- rollback;
- concurrency race safety;
- semantic commit;
- retirement;
- context isolation;
- Task isolation;
- exact conversation append behavior.

It does **not** mean:

```text
real Hermes handoff certified
real Big runtime certified
resource governor complete
automatic escalation complete
```

---

# 42. After E4E5

Once E4E5 is certified and backed up:

```text
14.11E handoff transaction work is complete
```

Then move to:

```text
14.11F — Resource Request + Governor Contract
```

Intended separation:

```text
Tree/router:
    WHAT SHOULD be useful?

Governor:
    MAY IT run?

Scheduler:
    HOW should resources be arranged?

Runtime adapter:
    DO the runtime operation.
```

Stable future concepts:

```text
ResourceRequest
ResourcePriority
ResourceBudget
ResourceAvailability
Governor
Scheduler
```

Do not build a full OS scheduler inside 14.11F.

---

# 43. High-Confidence Properties at Current Certified B2B

```text
same-form path remains D5-compatible

actual handoff starts with a fresh continuity-backed target

stale handoff recovery uses the same continuity

stale recovery is one-shot

replacement binding persists before retry

old target is not retired before semantic success

failure after durable runtime advancement rolls back before cleanup

rollback guard advances with runtime generation

final runtime rotation is represented in rollback guard

rollback race does not overwrite newer Forest truth

cleanup excludes latest canonical runtime session

unknown canonical truth fails closed

persist=False performs no durable rollback

persist=False still cleans detached handoff children

E4D is exactly one semantic success boundary

post-success retirement preserves final canonical session
```

---

# 44. Still-To-Prove in E4E5

Integrated proof is still needed for:

```text
real ForestTurnInstructionComposition through full handoff

real E4E1 ModelFormHandoff creation inside full send path

real ConversationContinuity contents at bootstrap

real ModelFormContinuity through stale retry

real E4D effective-form write in integrated handoff

real E4D conversation append exactly once

real Reasoning temporary lease consumption exactly once

Small → Big semantic direction

Big → Small semantic direction

execution-context isolation across complete transaction

Task isolation across complete transaction

unsupported continuity runtime fail-closed in full path

no duplicate current exchange after stale recovery

public send passthrough with typed instruction composition
```

---

# 45. One-Page Resume Summary

Current live source:

```text
/home/user/The-Forest/bristlecone/runtime/task_session.py
```

Expected SHA:

```text
a8d089a7de0e4f469678831c6220f61ed3930e79f8f0f2afe70f4f3a03b1ec71
```

Current certified backup:

```text
bristlecone/backups/
phase14_11E4E3C2B2B_certified_20260811T174522Z/
task_session.py
```

Completed recent work:

```text
✅ C1   rollback primitive
✅ C2A  initial fresh handoff bootstrap / persistence
✅ B1   continuity-aware stale replacement
✅ B2A  safe rollback-race cleanup + success retirement helpers
✅ B2B  live frozen transaction integration
```

Current next steps:

```text
→ E4E5 contract recon
→ E4E5 end-to-end synthetic certification harness
→ E4E5 certified backup
→ 14.11F Resource Request + Governor
```

Do not run a real Hermes Model Form handoff yet.

Do not activate the staged Big model.

Do not alter current source before verifying the certified SHA and creating a new pre-edit backup.

---

# 46. Final Current Status

```text
PHASE 14.11 MODEL FORM

A-D
✅ contracts / state / registry / runtime identity / frozen send / D5

E1-E3
✅ handoff semantics + portable continuity

E4A-E4D
✅ semantic state + unified successful commit

E4E1-E4E3
✅ handoff preparation
✅ runtime-neutral continuity contract
✅ typed composition
✅ fresh continuity bootstrap
✅ CAS rollback
✅ initial persistence
✅ continuity-aware stale recovery
✅ failure cleanup
✅ concurrency-safe cleanup
✅ post-success retirement
✅ frozen transaction integration

E4E5
→ CURRENT NEXT STEP

F-L
□ resource governor
□ automatic escalation
□ Colony semantics
□ fake adapter full certification
□ real Small runtime
□ real Big runtime boundary
□ benchmark
```

**Authoritative current statement:**

> The Model Form handoff transaction implementation is assembled through E4E3C2B2B and has passed its focused structural and synthetic behavioral certifications. The next task is E4E5, which must certify the entire semantic handoff chain end-to-end using the real Forest continuity and commit types while keeping the external runtime behavior synthetic.
