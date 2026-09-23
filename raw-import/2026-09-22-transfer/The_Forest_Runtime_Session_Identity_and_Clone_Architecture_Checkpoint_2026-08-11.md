# The Forest — Runtime Session Identity & Clone Architecture Checkpoint
**Date:** 2026-08-11  
**Status:** Architecture direction recorded for Phase 14.11D / Clone & Colony runtime work

---

## Purpose

This checkpoint records the runtime-session identity design that emerged while preparing **Phase 14.11D — Turn Resolution + Freeze**.

The immediate problem is that The Forest currently identifies stored runtime sessions primarily by the runtime adapter name, such as `hermes`. That works while one Tree has only one relevant Hermes configuration, but it becomes ambiguous once the same Tree can use:

- Small and Big Model Forms,
- multiple runtime profiles,
- multiple execution contexts,
- Ortets and Ramets,
- multiple simultaneous Clone tasks.

The design below separates those identities so the system does not need to be redesigned later when Clone/Colony support becomes active.

---

# Core Identity Hierarchy

```text
TREE IDENTITY
    ↓
EXECUTION CONTEXT IDENTITY
    ↓
MODEL BINDING IDENTITY
    ↓
RUNTIME SESSION IDENTITY
```

Each layer answers a different question.

## 1. Tree Identity

Example:

```text
Bristlecone
```

This answers:

> Which enduring AI identity does this work belong to?

A Tree is not its model and is not its runtime session.

---

## 2. Execution Context Identity

Examples:

```text
ctx-0001
ctx-0002
ctx-0003
```

User-facing lineage terms may describe these contexts as:

- **Ortet** — original execution context in the lineage
- **Ramet** — cloned execution context

The internal ID should stay neutral and opaque.

This answers:

> Which independently operating context of this Tree is doing the work?

Execution-context identity is separate from whether that context is currently Main, background, foreground, dormant, Ortet, or Ramet.

---

## 3. Model Binding Identity

Examples:

```text
binding-0001
binding-0002
```

A Model Binding connects a resolved Model Form to a runtime configuration.

Example:

```text
Small
→ binding-0001
→ Hermes / Small profile
```

```text
Big
→ binding-0002
→ Hermes / Big profile
```

Or a future binding may point to an entirely different runtime:

```text
Big
→ binding-0002
→ llama.cpp / another backend
```

This answers:

> Which specific model/runtime configuration is this execution context using?

The `binding_id` must remain runtime-neutral and should not encode vendor names, model names, Tree flavor, Ortet/Ramet terminology, or UI labels.

---

## 4. Runtime Session Identity

Example:

```text
session-A
session-B
session-C
```

This is the actual live session created and owned by the runtime adapter.

It may contain runtime-specific conversational/session state and may be associated with mutable KV/cache state.

This answers:

> Which actual live runtime conversation/session is serving this execution context and binding?

---

# Key Invariant

The Forest must not identify a runtime session using only:

```text
adapter_name
```

and it must not identify a runtime session using only:

```text
binding_id
```

The effective Forest-side identity is:

```text
(execution_context_id, binding_id)
→ runtime session
```

This is the core invariant.

---

# Why Adapter Name Alone Is Not Enough

The current system can conceptually look like:

```text
runtime_sessions
└── hermes
    └── session-123
```

That becomes unsafe when both Small and Big use Hermes:

```text
Small
→ Hermes
→ profile A
→ session A

Big
→ Hermes
→ profile B
→ session B
```

Both would otherwise compete for:

```text
runtime_sessions["hermes"]
```

The adapter name answers:

> Which runtime implementation operates this?

It does **not** answer:

> Which Small/Big configuration or execution context does this session belong to?

---

# Why Binding ID Alone Is Also Not Enough

Two execution contexts may use the exact same Small Model Binding while doing different work.

Example:

```text
ctx-0001
→ binding-0001
→ Small
→ session-A

ctx-0002
→ binding-0001
→ Small
→ session-B
```

Both contexts may share:

- the same Tree identity,
- the same Model Form,
- the same binding,
- the same runtime adapter,
- the same resident model weights,

while still requiring separate live sessions.

Therefore:

```text
binding-0001
```

cannot uniquely identify the live runtime session.

---

# Clone / Colony Example

```text
Tree: Bristlecone
│
├── ctx-0001        ← Ortet
│   ├── Model Form: Small
│   ├── binding: binding-0001
│   └── runtime session: session-A
│
├── ctx-0002        ← Ramet
│   ├── Model Form: Small
│   ├── binding: binding-0001
│   └── runtime session: session-B
│
└── ctx-0003        ← Ramet
    ├── Model Form: Big
    ├── binding: binding-0002
    └── runtime session: session-C
```

This permits multiple members of a Colony to operate independently without confusing their runtime sessions.

---

# What Clones May Share

Separate runtime sessions do **not** require separate copies of the model weights.

For example:

```text
ctx-0001 ─┐
ctx-0002 ─┼──→ one resident Small model
ctx-0004 ─┘
```

Those contexts may share the same loaded model weights while keeping separate:

- runtime sessions,
- conversation/session state,
- mutable context/KV state,
- Model Form controls,
- Reasoning controls,
- task state,
- handoff state,
- execution-context-local decisions.

This supports the Forest resource principle:

> Resource cost should scale primarily with active work, not merely with retained Clone count.

---

# Separation of Responsibilities

```text
tree_id
= Which enduring Tree identity owns this lineage?

execution_context_id
= Which Ortet/Ramet/Clone context is operating?

binding_id
= Which Small/Big runtime configuration is selected?

adapter_name
= Which runtime implementation operates the binding?

session_id
= Which actual live runtime session exists?
```

These identities must not be collapsed into one another.

---

# Model Weight Sharing vs. Session Sharing

The Forest should distinguish:

```text
SHARED
- immutable model weights
- potentially shared runtime residency
- durable Tree knowledge where policy permits
```

from:

```text
ISOLATED PER EXECUTION CONTEXT / SESSION
- runtime session
- mutable conversational state
- mutable KV/session context
- Model Form control
- Reasoning control
- local task state
- local handoffs
```

Shared model weights do **not** imply shared live session state.

---

# Relationship to Model Form

The canonical Model Form system remains:

```text
CONTROL VALUES
Auto / Small / Big
```

```text
RESOLVED VALUES
Small / Big
```

Then:

```text
resolved Model Form
    ↓
binding_id
    ↓
runtime configuration
    ↓
runtime session for the current execution context
```

`Auto` is policy only and never becomes an executable runtime binding.

---

# Relationship to Phase 14.11C

Phase 14.11C established the runtime-neutral Model Binding Registry:

```text
Small / Big
    ↓
opaque binding ID
    ↓
runtime-state fragment
```

The new session-identity rule extends that architecture:

```text
execution_context_id
    +
binding_id
    ↓
runtime session
```

The registry chooses the runtime configuration.

The execution context determines which independently operating Tree context owns the live session.

---

# Relationship to Phase 14.11D

Before wiring Small/Big Model Form resolution into the live turn path, Forest runtime-session handling must not accidentally reuse a session merely because two bindings use the same adapter.

Recommended immediate roadmap:

```text
✅ 14.11A — Canonical Model Form Contract
✅ 14.11B — Execution-context-local Model Form Control
✅ 14.11C — Runtime-Neutral Model Registry

→ 14.11D-0 — Runtime Binding / Session Identity Prerequisite
□ 14.11D — Turn Resolution + Freeze
□ 14.11E — Model Form Handoff + Continuity
□ 14.11F — Resource Request + Governor Contract
□ 14.11G — Automatic Escalation Router
□ 14.11H — Colony Runtime / Shared-Weight Semantics
```

The exact storage migration still requires inspection of the existing persistence guard and compatibility assumptions before code is changed.

---

# Frozen-Turn Direction

A future meaningful turn should resolve and freeze something conceptually like:

```text
Frozen Turn Execution
├── execution_context_id
├── reasoning_mode
├── resolved_model_form
├── binding_id
└── runtime_state
```

The runtime session is then selected or created for:

```text
(execution_context_id, binding_id)
```

A stale-session recovery or retry must reuse the same frozen decision rather than resolving Model Form again.

---

# Spring Cleaning Clarification

**Spring Cleaning is not part of the Small/Big runtime-session identity problem.**

It appeared during reconnaissance only because older Forest lifecycle code already reads a simple `model_form` value as part of its working-set history.

That older scalar should not be confused with the new canonical Model Form control system.

Keep these concepts separate:

```text
Spring Cleaning
= lifecycle / restoration policy

Model Form Control
= Auto / pinned / task-scoped decision system

Resolved Model Form
= Small or Big for one meaningful turn

Model Binding
= runtime configuration selected for Small or Big

Runtime Session
= live runtime-specific session owned by an execution context + binding
```

The Spring Cleaning behavior can be reconciled with the new Model Form architecture later without blocking the runtime-session identity work.

---

# Architecture Invariant

> **A runtime adapter identifies how a runtime is operated; a Model Binding identifies which runtime configuration is selected; an execution context identifies which Ortet/Ramet is working; and a runtime session identifies the actual live session.**

Therefore:

> **Forest runtime-session identity must account for both execution-context identity and Model Binding identity.**

Conceptually:

```text
(execution_context_id, binding_id)
→ runtime session
```

This invariant should guide Phase 14.11D, future Clone lifecycle work, Colony concurrency, resource management, and shared-model residency.
