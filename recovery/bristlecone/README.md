# Bristlecone Pine Recovery

This directory is the reconstruction workshop for Bristlecone Pine.

It does **not** replace the frozen recovery corpus under:

`raw-import/2026-09-22-transfer/`

and it is **not** the modern production Forest tree.

## Recovery layers

```text
raw-import/
    frozen archaeological evidence

recovery/bristlecone/
    selected evidence + source reconciliation + provenance

modern Forest production tree
    only promoted after recovery and certification
```

## Rules

- Recover logical components, not every duplicate recovered file.
- Preserve original source paths and SHA-256 values in `recovery/MIGRATION-LEDGER.tsv`.
- Bind implementation to the tests/certification evidence that supports it.
- A certified snapshot is strong evidence, but not automatically the final source if later legitimate work survives.
- Do not silently resolve conflicts.
- Do not copy the entire historical corpus here; `raw-import/` already preserves it.
- Reconcile by subsystem: identity, Workshops, capability resolution, Task Sessions, Layered Hot Context, reasoning control, Model Forms, session identity/store, handoff/continuity, benchmarks, and certification.
- Nothing recovered here automatically becomes modern Post-Apollo production code.

## Current strongest recovered boundary

The repository recovery authority currently records:

- Phase 14.11 L.9: A+B certified
- Phase 14.11 L.10: A+B independently certified
- Phase 14.11 L.11: work began
- L.11 evidence-inventory tooling survives
- the expected generated L.11 evidence inventory has not been found

This is a recovery boundary, not a declaration that every surviving source file is canonical.

## Working layout

```text
recovery/bristlecone/
├── README.md
├── RECONSTRUCTION-STATUS.md
├── identity/
├── architecture/
├── implementation/
├── benchmarks/
├── certification/
├── continuity/
└── historical/
```

Directories are created as logical artifacts are promoted and reconciled.
