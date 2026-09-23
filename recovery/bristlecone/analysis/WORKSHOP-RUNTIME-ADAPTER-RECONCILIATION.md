# Bristlecone Pine — Workshop / Runtime Adapter Foundation Reconciliation

Status: **RECONCILED**

## Recovery conclusion

The surviving late Workshop/capability-resolution implementation and runtime-adapter foundation are selected as the best recovered Bristlecone implementation.

The subsystem is reconstructed from a mixture of:

- current production source,
- exact certified anchors,
- earlier resolver lineage,
- the recovered Phase 14.11 master checkpoint,
- and the now-reconciled Phase 14.6/14.7 cache chronology.

## Selected architecture

```text
Workshop CLI
    ↓
ForestCapabilityResolver
    ↓
runtime adapter factory
    ↓
BaseRuntimeAdapter
    ↓
runtime-specific adapter
    ↓
exact runtime transaction
    ↓
verify runtime truth
    ↓
commit Forest state
```

The Forest owns canonical capability meaning.

The runtime adapter owns translation into runtime-specific toolsets/Skills/state.

## Selected files

Workshop/capability layer:

- capabilities/registry.yaml
- capabilities/resolver.py
- adapters/hermes.yaml
- workshops/code-debug.yaml
- workshops/design.yaml
- workshops/model.yaml
- workshops/research.yaml
- bin/bristlecone-workshop.py

Runtime adapter layer:

- runtime/adapters/base.py
- runtime/adapters/factory.py
- runtime/adapters/hermes.py

Support tools retained for provenance:

- bin/resolve-workshop
- bin/verify-live-workshop

## Certified anchors

### runtime/adapters/base.py

The surviving current file is byte-identical to the copy preserved in:

`backups/phase14_11E4E2_certified_20260811T155944Z/base.py`

### runtime/adapters/hermes.py

The surviving current file is byte-identical to certified source snapshots including:

- Phase 14.11 L.9 A recovery certification
- Phase 14.11 L.10 A sustained-session certification

This gives the runtime-specific adapter a very strong late certified anchor.

## Non-byte-certified late files

The following surviving current files do not have an exact certified backup copy:

- bin/bristlecone-workshop.py
- capabilities/resolver.py
- runtime/adapters/factory.py

They are nevertheless selected because the later engineering record explicitly documents the same architecture and because their evolution is explained by recovered phase chronology.

### Controller

The master checkpoint explicitly names `bin/bristlecone-workshop.py` and records the migration away from direct Hermes config mutation toward runtime-adapter transactions.

The surviving file implements that documented design, including:

- runtime-selected adapter construction,
- exact toolset application,
- runtime verification before Forest state commit,
- rollback if the post-runtime Forest update fails.

### Resolver

Earlier resolver snapshots survive from Phase 14.6D and 14.6E.

The current resolver is a later version with parsed-YAML and capability-resolution caching.

The recovered master checkpoint records Phase 14.6 capability caching as completed, including:

- shared cache reuse,
- strict/permissive callers sharing canonical resolution,
- caller mutation isolation,
- manifest-change invalidation,
- cache deletion/rebuild,
- Forest-shared resolution vs Clone-local activation.

Therefore the current resolver's additional cache logic is consistent with the later documented implementation rather than unexplained drift.

### Factory

The master checkpoint explicitly states that the runtime abstraction package and adapter factory were created before the Workshop controller migration.

The surviving `runtime/adapters/factory.py` is small and matches that documented contract: Forest state chooses the adapter, runtime-specific construction stays behind the adapter boundary.

## Recovered invariants

- Forest capability IDs are runtime-neutral.
- Whole capability groups are not activated blindly.
- Workshop Core is automatically included.
- General/Ready activation is individually validated.
- unresolved capabilities fail closed.
- runtime-specific names live behind adapter mappings.
- capability resolution is shared derived Forest state.
- activation remains Task/Clone/runtime-local.
- runtime mutation occurs before Forest claims the new state.
- runtime truth is verified before Forest state commit.
- rollback restores pre-activation runtime state if the Forest commit path fails.

## Recovery caveat

This is a historical reconstruction result, not a declaration that the Python/Hermes implementation should remain the modern Post-Apollo production implementation.

The modern Rust control plane should preserve these boundaries and transaction semantics while replacing runtime-specific mechanisms where appropriate.
