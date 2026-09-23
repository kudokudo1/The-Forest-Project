# Project Forest — Phase 14.10 Revised Reasoning Control Plan

**Date:** 2026-08-10  
**Project:** The Forest / Bristlecone Pine  
**Phase:** 14.10 — Reasoning Modes and Human Control  
**Status:** 14.10A–E complete; revised 14.10E.1 and 14.10E.2 pending; 14.10F pending.

---

## 1. Current Phase Status

- ✅ **14.10A — Hermes/runtime reasoning contract**
- ✅ **14.10B — Canonical Forest reasoning model**
- ✅ **14.10C — Deterministic automatic reasoning router**
- ✅ **14.10D — Hermes runtime translation**
- ✅ **14.10E — Frozen turn reasoning + stale recovery**
- → **14.10E.1 — Human Reasoning Control Backend**
- → **14.10E.2 — Bare-Bones Native Forest Reasoning Menu**
- □ **14.10F — Benchmark + Final Certification**

---

## 2. Revised Human-Facing Reasoning Model

Preferred Forest-facing reasoning levels:

- **Light** — less reasoning; favors speed.
- **Normal** — balanced reasoning.
- **Deep** — more reasoning; favors deliberation.

The old `Quick` name becomes a compatibility/migration alias for **Light**.

Runtime mapping:

```text
Forest Light  → Hermes low
Forest Normal → Hermes medium
Forest Deep   → Hermes high
```

Hermes-only values such as `none`, `minimal`, `xhigh`, `max`, and `ultra` remain runtime-specific and must not become canonical Forest reasoning modes.

---

## 3. Auto Is a Policy, Not a Reasoning Level

**Auto must remain distinct from Normal.**

Auto means Forest chooses Light / Normal / Deep for the current meaningful turn.

Normal means the user explicitly wants balanced reasoning rather than automatic escalation/de-escalation.

```text
Reasoning levels:
Light
Normal
Deep

Routing policy:
Auto
```

---

## 4. Durable Baseline + Temporary Lease

The reasoning control model has two independent layers.

### Baseline

```text
Auto
Pinned Light
Pinned Normal
Pinned Deep
```

A pinned baseline is durable user intent.

### Temporary Lease

```text
Temporary Light
Temporary Normal
Temporary Deep
```

Factory default:

```text
5 meaningful turns
```

The default should later be configurable through Spirit.

---

## 5. Temporary Lease Semantics

Example:

```text
Baseline: Pinned Normal
Temporary: Deep
Turns remaining: 5
```

Then:

```text
User turn 1 → Deep → 4 remaining
User turn 2 → Deep → 3 remaining
User turn 3 → Deep → 2 remaining
User turn 4 → Deep → 1 remaining
User turn 5 → Deep → 0 remaining
Next meaningful user turn → Pinned Normal resumes
```

These do **not** consume turns:

- tool calls
- internal execution/reasoning steps
- stale-session recovery
- runtime retries
- runtime-session recreation
- Workshop execution steps
- model unload/reload
- other non-meaningful-turn infrastructure operations

A temporary lease is consumed only once per new meaningful user turn.

---

## 6. Temporary Override Above a Pinned Baseline

Temporary reasoning must not destroy the pinned baseline.

```text
Pinned Normal
+
Temporary Deep · 5 turns
```

Behavior:

```text
Deep
Deep
Deep
Deep
Deep
↓
Pinned Normal resumes
```

Changing the pinned baseline while a temporary lease is active should **not cancel the temporary lease**.

Example:

```text
Before:
Temporary Deep · 3 remaining
Baseline: Pinned Normal

User changes baseline to Pinned Light

After:
Temporary Deep · 3 remaining
Baseline: Pinned Light
```

After those three temporary turns, Light resumes.

---

## 7. Authority / Precedence

```text
explicit mode for this exact turn
        >
active temporary lease
        >
pinned baseline
        >
Auto router
        >
Normal fail-safe
```

---

## 8. Persistence Doctrine

> **Restart is not reset.**

Ordinary restarts should preserve reasoning intent.

A pinned baseline should survive ordinary Task/runtime/application/machine restarts when Forest durable state persists.

An active temporary lease should also survive ordinary restarts, including its remaining-turn count.

Example:

```text
Baseline: Pinned Normal
Temporary: Deep · 3 remaining

[restart]

Baseline: Pinned Normal
Temporary: Deep · 3 remaining
```

Explicit reset actions may clear reasoning intent according to their defined policy.

---

## 9. Proposed Durable State Shape

Conceptual structure:

```yaml
reasoning_control:
  schema_version: 1

  baseline:
    policy: pinned
    mode: normal

  temporary:
    mode: deep
    turns_remaining: 3

  settings:
    temporary_turn_default: 5
```

Auto example:

```yaml
reasoning_control:
  schema_version: 1

  baseline:
    policy: auto
    mode: null

  temporary:
    mode: light
    turns_remaining: 5

  settings:
    temporary_turn_default: 5
```

Exact persistence and locking must reuse existing Forest state doctrine rather than creating an independent store.

---

## 10. Native Forest Reasoning Menu

The core menu should **not depend on rofi**.

> **The Forest owns the menu. The desktop environment only launches it.**

The first version should be a bare-bones Forest-owned UI that can later be visually restyled into Spirit without changing reasoning behavior.

The UI should contain almost no policy logic. It should query and mutate the Forest reasoning-control backend.

---

## 11. Numpad Interaction

```text
Num Lock OFF + Num 2
→ Temporary Reasoning menu

Super + Num Lock OFF + Num 2
→ Baseline / Pinned Reasoning menu
```

Temporary menu:

```text
Reasoning — Temporary

Current baseline: Normal · pinned
Current temporary: Deep · 3 remaining

0  Auto
1  Light
2  Normal
3  Deep
```

Pinned menu:

```text
Reasoning — Baseline

Current baseline: Normal · pinned
Current temporary: Deep · 3 remaining

0  Auto / Clear Pin
1  Pin Light
2  Pin Normal
3  Pin Deep
```

Both should support keyboard and mouse/click selection.

`Super` conceptually means:

> **Keep this setting.**

Auto does not need a separate pinned variant.

---

## 12. Numpad Scaling Principle

Preferred Forest pattern:

```text
one feature
=
one numpad key
+
an internal menu of related choices
```

Potential future layout:

```text
Num 1 → Forest/System modes
Num 2 → Reasoning
Num 3 → Model controls
Num 4 → Clone controls
Num 5 → Workshop controls
...
Num 9 → Obsidian
```

---

## 13. Revised Remaining Phase 14.10 Roadmap

### 14.10E.1 — Human Reasoning Control Backend

Implement and verify:

- Light / Normal / Deep preferred naming
- Quick → Light migration compatibility
- Auto as a routing policy
- durable pinned baseline
- durable temporary lease
- default temporary lease = 5 meaningful turns
- configurable duration model for later Spirit integration
- restart persistence
- temporary-over-pinned behavior
- pinned-baseline change while temporary remains active
- precise precedence model
- one decrement per meaningful turn
- zero decrement on stale recovery/retry/tool execution
- atomic persistent state mutation
- fail-closed validation
- no Hermes-specific values in durable Forest state

### 14.10E.2 — Bare-Bones Native Forest Reasoning Menu

Implement and verify:

- Forest-owned menu
- no rofi dependency
- native minimal GUI
- keyboard + clickable options
- Num Lock OFF + Num 2 launches temporary menu
- Super + Num Lock OFF + Num 2 launches baseline/pinned menu
- `0 Auto / 1 Light / 2 Normal / 3 Deep`
- current baseline display
- temporary mode + turns remaining display
- menu delegates all behavior to backend
- no duplicated reasoning-policy logic in UI
- designed for later Spirit restyling

### 14.10F — Benchmark + Final Certification

Verify:

- automatic Light / Normal / Deep routing
- pinned Light / Normal / Deep
- temporary Light / Normal / Deep leases
- 5-turn default
- custom duration backend behavior
- correct lease decrement
- temporary expiration restoration
- temporary-over-pinned restoration
- pinned baseline survives temporary override
- baseline change during temporary lease
- restart persistence
- stale recovery consumes zero extra turns
- explicit exact-turn override precedence
- deterministic routing
- routing/control overhead
- no persistent Hermes configuration drift
- no accidental Task-Sticky Deep
- no runtime-specific reasoning values persisted as canonical Forest state
- native menu invokes the same backend API
- regression checks against Phase 14.7–14.9 turn/recovery invariants

---

## 14. Current Implementation Doctrine

> **A Tree is not its model.**

> **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Restart is not reset.**

> **The Forest owns the menu. The desktop environment only launches it.**

> **Runtime recovery is execution, not new meaningful input.**

> **Reasoning is decided once per meaningful turn and reused for recovery/retry.**

> **Temporary reasoning must not silently become permanent Tree configuration.**

> **Pinned reasoning is durable user intent and may persist across ordinary restarts.**

---

## 15. Immediate Next Step

Proceed with **14.10E.1**.

Build and verify the backend/state semantics before creating the native GUI.
