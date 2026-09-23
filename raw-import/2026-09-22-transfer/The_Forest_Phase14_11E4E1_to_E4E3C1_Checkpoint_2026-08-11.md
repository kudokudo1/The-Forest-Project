# The Forest — Phase 14.11E4E1 → E4E3C1 Checkpoint
**Date:** 2026-08-11  
**Project:** The Forest / Bristlecone Pine  
**Scope:** Model Form handoff continuity, typed instruction continuity, runtime continuity bootstrap, fresh target-session bootstrap, and CAS-aware rollback.

## Current position

```text
✅ 14.11E4E1 Pure handoff-continuity preparation
✅ 14.11E4E2 Runtime-neutral continuity-bootstrap contract
✅ 14.11E4E3A Typed instruction-composition passthrough
✅ 14.11E4E3B Handoff runtime bootstrap helper
✅ 14.11E4E3C1 CAS-aware runtime-binding rollback
→ 14.11E4E3C2 Frozen handoff transaction integration
□ 14.11E5 End-to-end handoff certification
```

Phase 14 still continues through 14.14 Final Benchmark.

## Governing architecture

- A Tree is not its model. Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.
- Small and Big Model Form are capability forms of the same Tree, not different identities.
- Canonical live runtime-session identity is `(execution_context_id, binding_id) -> session`.
- Adapter name is runtime metadata, not session identity.
- Forest semantic truth remains authoritative over runtime session state.
- If runtime advances but Forest rejects the semantic state transition, the runtime advancement must not silently remain authoritative.

## 14.11E1 — ModelFormHandoff

`model_form/handoff.py` defines immutable `ModelFormHandoff` with:
- execution_context_id
- task_id
- from_form
- to_form
- source
- reasons
- schema version

It requires an actual form change and carries no runtime/session/vendor/continuity state.

Certified backup:
`bristlecone/backups/phase14_11E1_certified_20260811T135713Z`

## 14.11E2 — Pure handoff detection

`detect_model_form_handoff(previous_form, frozen_turn)`:
- previous form missing -> no handoff
- previous form same as frozen form -> no handoff
- previous form differs -> canonical handoff

No runtime I/O or state mutation.

Certified backup:
`bristlecone/backups/phase14_11E2_certified_20260811T140259Z`

## 14.11E3 — Portable continuity

### E3A
Existing `ForestTurnInstructionComposition` is the frozen instruction-continuity substrate. It preserves the exact final instruction string plus source packets and learning provenance.

### E3B
`ConversationContinuity` contains ordered completed exchanges only. It is Task-local and execution-context local, and contains no runtime session/KV/reasoning/tool/inflight state.

### E3C
`ModelFormContinuity` combines:
- exact `ForestTurnInstructionComposition`
- `ConversationContinuity`

It is portable and runtime-neutral.

Certified E3 snapshot:
`bristlecone/backups/phase14_11E3_certified_20260811T142122Z`

## 14.11E4A/B/C — Canonical semantic state

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

Helpers:
- `_effective_model_form_context_id`
- `_effective_model_form_for_context`
- `_write_effective_model_form_for_context`
- `_conversation_continuity_for_context`
- `_append_conversation_exchange_for_context`

These are detached/in-memory helpers unless wrapped by a persistent transaction.

## 14.11E4D — Unified successful-turn commit

`_commit_successful_model_form_turn(...)` is the single successful semantic-commit boundary.

Failure:
- previous effective form unchanged
- no conversation exchange appended
- temporary reasoning lease not consumed

Success:
- effective form becomes frozen form
- exact completed user/assistant exchange appended
- temporary reasoning lease consumed exactly once

Concurrency correction freezes previous effective form from pre-turn `control_state`. Persistent commit allows only:
- latest previous form == source previous form, or
- latest previous form == frozen form

A newer different-form generation causes stale semantic commit failure.

Certified backup:
`bristlecone/backups/phase14_11E4D_certified_20260811T150951Z/task_session.py`

## 14.11E4E1 — Pure handoff-continuity preparation

Added:
`_prepare_model_form_handoff_continuity(...)`

It:
- validates Task identity
- detects actual handoff
- requires exact typed `ForestTurnInstructionComposition` on actual handoff
- reads prior completed conversation
- constructs `ModelFormContinuity`

It does not:
- create runtime sessions
- persist state
- replay conversation
- append current turn
- send current message
- perform runtime I/O

Certified backup:
`bristlecone/backups/phase14_11E4E1_certified_20260811T152409Z/task_session.py`

## 14.11E4E2 — Runtime-neutral continuity-bootstrap contract

`runtime/adapters/base.py` adds:
- `RuntimeContinuityUnsupportedError`
- optional, non-abstract `create_session_with_continuity(...)`

Unsupported runtimes fail closed. Hermes remains concrete and currently inherits the fail-closed default.

Certified backup:
`bristlecone/backups/phase14_11E4E2_certified_20260811T155944Z/base.py`

SHA256:
`e2b002a37b7048fa543876a26c8608154a9707acdb93c378d3a1bdea66b395fb`

## 14.11E4E3A — Typed instruction-composition passthrough

Public and frozen send APIs now accept:
`[REDACTED - OLD QUBES AI API KEY]`

Rules:
- omitted -> legacy callers remain valid
- supplied -> must be `ForestTurnInstructionComposition`
- if `instructions` omitted, use exact `instruction_composition.instructions` object
- if both supplied, they must be the same string object
- equal-but-distinct strings fail closed

Certification proved:
- exact typed object identity preserved
- exact instruction object identity preserved
- invalid types fail before runtime work
- validation occurs before meaningful input
- no handoff/bootstrap behavior was added
- D5 retains exactly initial send + one stale retry
- E4D still has exactly one unified semantic commit

Certified backup:
`bristlecone/backups/phase14_11E4E3A_certified_20260811T161005Z/task_session.py`

SHA256:
`c87c27e6c4b7962754faa6f2fd809f320411805bb91803d93298521ff19d4ab2`

## 14.11E4E3B — Detached handoff runtime bootstrap

Added:
`_bootstrap_runtime_session_for_model_form_handoff(...)`

Actual handoff creates a fresh target-form runtime session from `ModelFormContinuity`.

Important rule:
An older dormant target-form session is not reused. A fresh target session is bootstrapped from current Forest-owned continuity. The old target session is only reported as `replaced_session_id`.

E4E3B:
- validates frozen and continuity identity
- resolves frozen target adapter
- calls `create_session_with_continuity`
- requires a fresh session ID
- writes target context+binding only into detached state
- carries old target session as `previous_session_id`
- cleans a new unbound session if post-create validation or binding write fails

It does not:
- persist Forest state
- send the current user message
- consume reasoning
- semantic-commit conversation
- retire the old canonical target session

A pre-certification cleanup gap was caught: a mismatched adapter result after session creation could leak a fresh session. This was corrected so only the fresh unbound session is retired; an existing canonical target session is never destroyed.

Certified backup:
`bristlecone/backups/phase14_11E4E3B_certified_20260811T161700Z/task_session.py`

SHA256:
`bde405826e48e3332a9eff33dd7b3828b1733e3e1f760108a02fd0100348392e`

## 14.11E4E3C1 — CAS-aware binding rollback

Recon established that the existing identity persistence path is write/merge only.

Guard keys:
- task_id
- execution_context_id
- binding_id
- adapter
- session_id

Forward persistence uses:
- `get_runtime_session_binding`
- `set_runtime_session_binding`
- `_state_write_lock`
- `load_state`
- `_atomic_write_yaml`

There is no session-store remove/delete API and no deletion shape in existing forward CAS.

Added:
`_rollback_runtime_binding_guarded_for_identity(working, guard, restore_binding)`

### Case A: old target binding existed

```text
old target binding
  -> fresh handoff binding persisted
  -> transaction rejected
  -> CAS verifies durable slot still points to this handoff session
  -> restore exact old target binding
```

### Case B: no old target binding existed

```text
no target binding
  -> fresh handoff binding persisted
  -> transaction rejected
  -> CAS verifies durable slot still points to this handoff session
  -> remove only this binding
  -> prune execution-context bucket if empty
```

Rollback proceeds only while durable state still matches:
- same Task
- same execution_context_id
- same binding_id
- same adapter
- same session_id

A newer concurrent generation causes rollback to fail stale rather than overwrite newer Forest state.

C1 repairs Forest state only. It does not create/end runtime sessions, send turns, consume reasoning, or semantic-commit.

Certification passed:
- exact prior binding restoration
- detached caller state
- one atomic write while locked
- complete removal when no prior binding existed
- empty context pruning
- unrelated contexts preserved
- sibling binding preserved
- newer session generation blocks rollback
- changed adapter blocks rollback
- changed active Task blocks rollback
- invalid restore binding fails before persistence
- Forest-state-only boundary
- exactly one atomic durable write site

Certified backup:
`bristlecone/backups/phase14_11E4E3C1_certified_20260811T163126Z/task_session.py`

SHA256:
`c6022d9f41426137dbed7c69f3d9e92b2d16d61693fc7dc7e614607f30cbd75c`

## Safe failures caught during this segment

1. E4E1 raw text anchor matched multiple locations; installer stopped before mutation.
2. E4E2 decorator insertion risked accidentally making optional continuity bootstrap abstract; structural validation caught it.
3. E4E3B mismatched-adapter post-create cleanup gap was found and fixed before certification.
4. E4E3C1 recon parsed indented `inspect.getsource()` output without `textwrap.dedent()`, causing `IndentationError`; no mutation.
5. First E4E3C1 installer executed module source only to inspect imports; `__file__` was absent and caused `NameError`; failure occurred before backup/write. Corrected to AST-only import inspection.

## E4E3C2 — exact remaining transaction

Target:

```text
resolve Reasoning once
  -> resolve Model Form once
  -> freeze previous successful Model Form
  -> prepare handoff continuity
     ├─ no handoff -> existing D5 path unchanged
     └─ handoff
          -> fresh target session from E4E3B
          -> persist target binding with identity CAS
          -> send current user turn
          -> one-shot stale recovery if needed
          -> E4D semantic commit
             ├─ success
             │    -> retire replaced old target session
             └─ reject/fail
                  -> C1 rollback Forest binding when safe
                  -> retire failed/advanced handoff runtime session
```

## E4E3C2 invariants

1. Same-form path must stay on the existing certified D5 flow.
2. Actual handoff requires exact typed `ForestTurnInstructionComposition`.
3. Portable continuity contains only prior completed conversation; current user message is sent as the current turn, not replayed.
4. A previously used target form still gets a fresh continuity-bootstrapped session.
5. Persistent handoff must durably CAS the target binding before long runtime/model work.
6. Stale recovery during a handoff must reuse the same frozen Model Form, current message, exact instructions, and same `ModelFormContinuity`; it must not create an empty replacement that loses prior conversation.
7. At most one stale recovery remains allowed.
8. E4D remains the single semantic commit.
9. Successful semantic commit may then retire the replaced old target session.
10. Semantic rejection must not leave an advanced runtime session authoritative.
11. C1 repairs Forest state; C2 owns runtime retirement.
12. If C1 rollback fails stale, newer Forest state must not be overwritten.

## Existing D5 invariants that C2 must preserve

- Model Form resolved once
- Reasoning resolved once
- one meaningful input
- one initial runtime send
- at most one stale replacement
- one stale retry
- exact frozen instructions reused
- exact current message reused
- no second recovery
- canonical context+binding identity

## Existing E4D invariants that C2 must preserve

- exactly one unified successful semantic commit
- commit occurs after all possible runtime sends
- failed runtime paths append no conversation
- failed runtime paths do not change effective form
- temporary reasoning lease finalizes only on successful semantic commit
- previous form remains frozen from pre-turn control state
- stale different-form commit fails closed

## Real-runtime boundary

Real Small remains the currently bound Bristlecone form. Big remains unbound in the live registry during this work.

E4E3C2 should therefore be tested with synthetic/fake runtime adapters before any real Big activation or boundary test.

## Development workflow

The project root `/home/user/The-Forest` is not a Git repository.

Continue:
```text
inspect
-> one isolated change
-> timestamped backup
-> compile
-> focused behavior test
-> certify
-> certified backup
-> next change
```

Do not:
- blindly rerun failures
- modify before understanding a failure
- certify merely because code compiles
- mix multiple transaction responsibilities without isolated tests
- execute source files just to inspect imports
- use ambiguous text anchors when AST structure is available

## Exact next step

**14.11E4E3C2 — Frozen handoff transaction integration**

The key rule entering C2 is:

> A runtime handoff becomes authoritative only when Forest successfully commits the corresponding semantic turn.

Until that point, the fresh target runtime session is transactional.
