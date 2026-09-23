# Bristlecone Pine — Control-Path Reconciliation

Status: active recovery analysis

This note records the first reconciliation pass over current-production Python files that do not have a byte-identical certified-backup match.

It does **not** declare these files canonical.

## Strong certified anchors adjacent to this work

The recovered current tree contains byte-identical matches to certified snapshots for major core components including:

- `runtime/task_session.py`
- `runtime/adapters/base.py`
- `runtime/adapters/hermes.py`
- `runtime/session_identity.py`
- `runtime/session_store.py`
- `runtime/model_residency.py`
- `runtime/conversation_continuity.py`
- `reasoning/control.py`
- core Model Form files including `control.py`, `model.py`, `registry.py`, `resolution.py`, `handoff.py`, `handoff_detection.py`, and `continuity.py`

This means the unmatched control-path files sit around a strongly anchored core rather than replacing an entirely uncertified runtime.

## Current unmatched control-path files

### `bin/bristlecone-workshop.py`

Evidence state: **strong implementation/documentation support; no exact certified backup match located**

The recovered Phase 14.11 master checkpoint explicitly documents the controller migration and names:

`bin/bristlecone-workshop.py`

The checkpoint describes the same architecture visible in the surviving current file:

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

The current source implements runtime-before-Forest verification and rollback through the adapter contract.

Recovery interpretation: strong candidate for the late live controller. It still requires chronology/test reconciliation because no exact certified copy has been identified.

### `runtime/adapters/factory.py`

Evidence state: **strong architectural support; no exact certified backup match located**

The Phase 14.11 master checkpoint states that the runtime abstraction package and adapter factory were created as part of the runtime-adapter foundation.

The surviving factory is small and consistent with that contract: runtime identity comes from Forest state and Hermes-specific construction remains behind the adapter boundary.

Recovery interpretation: strong candidate, but still requires direct chronology/test linkage.

### `capabilities/resolver.py`

Evidence state: **clear historical lineage; current version later than surviving Phase 14.6 backups**

Recovered backups show at least these earlier resolver states:

- Phase 14.6D
- Phase 14.6E

The current resolver is larger and includes Forest cache integration not present in the early resolver snapshots.

The Phase 14.11 master checkpoint explicitly identifies `capabilities/resolver.py` as the shared resolver and records verified resolver behavior including Core inclusion, canonical IDs, tool/Skill separation, fail-closed unresolved capabilities, and all four Workshop cores.

Recovery interpretation: current source is a strong late candidate. Its cache additions must be reconciled against the later cache/Layered Hot Context evidence before final selection.

### `turn_composition.py`

Evidence state: **very strong Phase 14.9 completion evidence; no exact certified backup copy located**

The Phase 14.9 Source Context complete checkpoint explicitly lists `turn_composition.py` among the files created during Phase 14.9 and defines its ownership boundary.

The current file matches the documented architecture:

- Forest-level composition boundary
- Learning and Source Context remain independently owned
- runtime receives one already-frozen final instruction string
- no Source Context means exact Learning passthrough
- bounded final instruction budget
- Source Context marked as reference data rather than instruction authority

The Phase 14.11 master checkpoint repeats the same composition flow.

Recovery interpretation: this file has stronger evidence than its lack of an exact certified backup match initially suggests. It is a high-confidence recovery candidate pending source/hash chronology reconciliation.

### `runtime/helpers/hermes_profile_bridge.py`

Evidence state: **surviving current support implementation; direct checkpoint linkage not yet found**

The file implements a bounded Forest-to-Hermes profile bridge with only two allowed operations:

- default model
- API key

It validates profile identity and isolates Hermes-native imports inside the Hermes virtual environment.

Recovery interpretation: plausible later runtime support code, but currently lower confidence than the files above because this first pass has not found an explicit named checkpoint/certified copy.

### `runtime/tool_availability.py`

Evidence state: **surviving current support implementation; direct checkpoint linkage not yet found**

The file explicitly declares itself dormant by default and defines a Forest-native fallback availability cache for runtimes that do not provide equivalent caching.

Its architecture separates:

```text
capability exists
    ↓
shared infrastructure availability
    ↓
Tree / Clone permission evaluation
    ↓
Spirit resource arbitration when required
```

Recovery interpretation: coherent with Forest doctrine, but direct chronology/certification evidence still needs to be located.

### `cache/coordinator.py`

Evidence state: **clear historical progression; current version later than surviving backup copies**

Recovered snapshots exist from earlier Phase 14.5/14.7 work, while the current file is a later distinct version.

Recovery interpretation: reconcile as part of the Cache / Layered Hot Context subsystem rather than as a standalone file.

## First-pass conclusion

The unmatched files are not evidence that Bristlecone's core runtime was lost.

The strongest runtime core is heavily anchored by certified exact matches. The unmatched set is concentrated in later wrappers, composition, cache, learning/context, and presentation/support layers.

Priority order for continued reconciliation:

1. Workshop controller + runtime factory + resolver
2. Turn composition + Source Context
3. Cache coordinator / Layered Hot Context
4. Learning/User Context subsystem
5. Hermes profile bridge and tool-availability support
6. Qubes/i3 presentation layer as historical compatibility code
