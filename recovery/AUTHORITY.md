# Forest Recovery Authority Model

This document defines how conflicting recovered Forest material is evaluated.

The raw recovery corpus is preserved under:

`raw-import/2026-09-22-transfer/`

Nothing in `raw-import/` becomes canonical merely because it exists,
has a newer-looking filename, or appears in multiple locations.

## Engineering authority

For claims about what software existed, executed, passed, or was certified,
use this order of authority:

1. Terminal-certified artifacts with hashes/manifests and surviving source.
2. Surviving production source and its tests.
3. Benchmark evidence and certification tooling.
4. Later engineering checkpoints.
5. Architecture and design checkpoints.
6. Forest Language and product doctrine.
7. Continuity packets, transfers, and historical working notes.
8. Duplicate vault copies, Downloads copies, leaf litter, and miscellaneous
   recovered material.

A lower-authority document cannot override stronger later evidence.

Example:

A checkpoint saying "L.10 not started" does not override a later
Terminal A + Terminal B certification proving L.10 completed.

## Conceptual authority

Engineering authority and conceptual importance are different.

Forest Language, doctrine, terminology, and design documents may define
what a concept means even when that concept has not yet been implemented.

A design specification is therefore valid evidence of intended behavior,
but not evidence that the behavior existed in running code.

## Recovery rules

- `raw-import/` is frozen archaeological source material.
- Do not reorganize, rename, deduplicate, or delete files in place.
- Canonical material is promoted into clean repository locations.
- Every promotion should preserve its original source path and SHA-256.
- Exact duplicates should normally produce one canonical copy plus provenance,
  not multiple promoted copies.
- Conflicts must be recorded rather than silently resolved.
- Historical files remain available even after canonical material is selected.
- Certification evidence must remain associated with the source it certifies.
- A newer timestamp alone does not establish authority.
- A filename containing words such as "final", "master", or "complete"
  does not establish authority by itself.

## Current strongest Bristlecone recovery boundary

Recovered evidence currently establishes:

- Phase 14.11 L.9: A+B certified.
- Phase 14.11 L.10: A+B independently certified.
- Phase 14.11 L.11: work began.
- `certification/phase14_11L11/build_evidence_inventory.py` survives.
- The expected generated `l11_evidence_inventory.json` has not been found.

Therefore the current recovery hypothesis is:

**L.10 is fully certified; L.11A was begun but was not completed or its
generated result did not survive.**

This is a recovery conclusion, not yet a declaration that every surviving
current source file is canonical. Source/certification reconciliation must
still be completed.
