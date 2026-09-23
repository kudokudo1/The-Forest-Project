# Bristlecone Pine — Reasoning Control Reconciliation

Status: **RECONCILED**

## Recovery conclusion

The surviving late Bristlecone reasoning subsystem is selected as the best recovered implementation of Forest reasoning control.

Selected implementation:

- `reasoning/__init__.py`
- `reasoning/model.py`
- `reasoning/router.py`
- `reasoning/control.py`

The evidence is mixed-strength and is recorded separately rather than flattened into one claim.

## What is byte-certified

### `reasoning/control.py`

The surviving current file has SHA-256:

`097a6eee9386d1b4db4310308ff8e053f9fad11f787430d87896bf20975a5779`

That is byte-identical to:

`backups/phase14_11G7_final_certified_20260811T213503Z/reasoning/control.py`

This strongly anchors the human reasoning-control state machine used by the later Phase 14.11 work.

The recovered control model includes:

- Auto baseline
- pinned Light / Normal / Deep baseline
- temporary Light / Normal / Deep lease
- default temporary lease length of five meaningful turns
- exact-turn override precedence
- temporary-over-pinned behavior
- lease identity
- one-turn-at-a-time consumption
- YAML-safe runtime-neutral persistence shape
- no Hermes-specific reasoning values in canonical Forest state

## What is checkpoint-backed rather than byte-certified

### `reasoning/model.py`

The current model defines canonical:

```text
Light
Normal
Deep
```

with migration aliases:

```text
Quick    -> Light
Standard -> Normal
```

This matches the recovered Phase 14.10 revised reasoning plan and the later Phase 14.11 master checkpoint.

### `reasoning/router.py`

The current router is deterministic and operates on prompt-shape signals rather than retaining raw user text.

It preserves explicit override above automatic routing and maps low-complexity turns to Light, higher-complexity turns to Deep, and uncertain/moderate turns to Normal.

Earlier Phase 14.10 router snapshots survive, but the current source is a later distinct revision. No later conflicting source copy has been found.

Therefore the current router is selected as the best recovered late implementation, but is not described as byte-certified.

## Later engineering checkpoint

The recovered Phase 14.11 master checkpoint explicitly records:

`14.10 Human Reasoning Control — COMPLETE`

and treats the following axes as independent:

```text
REASONING
Light / Normal / Deep

WORKSHOP
Research / Design / Code-Debug / Model / ...

MODEL FORM
Small / Big
```

Canonical invariant:

> Deep does not mean Big, and Big does not mean Deep.

## Phase 14.11 L.6 certification

A later terminal-certified L.6 benchmark ran:

- 5 Light trials
- 5 Normal trials
- 5 Deep trials
- all on Small / binding-0001
- warm Small before each measured turn
- fresh Task/context/session per turn
- no session reuse
- no stale-session recovery
- `persist=False`

The certified result states that Reasoning and Model Form remained independent and that Deep never silently escalated to Big.

This benchmark is strong evidence for runtime translation and reasoning/model-form independence.

It is **not** evidence that the automatic router's heuristic thresholds are optimal, nor does it independently certify every human-control lease transition.

## Runtime mapping

Recovered runtime contract:

```text
Forest Light  -> Hermes low
Forest Normal -> Hermes medium
Forest Deep   -> Hermes high
```

Hermes-only values such as `none`, `minimal`, `xhigh`, `max`, or `ultra` remain runtime-specific and are not canonical Forest modes.

## Control precedence

Recovered precedence:

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

## Turn/recovery invariant

Reasoning is resolved once per meaningful turn.

Runtime retry, stale-session recovery, tool execution, and other infrastructure operations do not count as new meaningful turns and must not consume additional temporary-lease turns.

This matches the broader Phase 14.7–14.11 freeze/retry doctrine.

## Historical UI

The old Qubes/i3 reasoning UI and menu files survive and are valuable historical evidence.

They are **not** selected as the modern Post-Apollo presentation layer. The modern Bark/QML UI should call the recovered reasoning-control semantics rather than porting the old host-specific UI verbatim.

## Recovery caveat

This reconciliation preserves the historical behavioral contract.

A future Rust implementation should re-test:

- automatic routing behavior
- pinned/temporary lease transitions
- persistence/restart behavior
- exact-turn precedence
- stale-recovery non-consumption
- runtime translation
- reasoning/model-form independence

Historical L.6 timing data should not be treated as representative of the modern model/runtime stack.
