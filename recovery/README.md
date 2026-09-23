# Forest Recovery

This directory records the recovery and canonicalization of the rescued
Forest project material.

The original recovered corpus remains frozen under:

`raw-import/2026-09-22-transfer/`

## Contents

- `AUTHORITY.md` — rules for resolving conflicting recovered evidence.
- `MIGRATION-LEDGER.tsv` — provenance record for promoted material.
- `inventory/MANIFEST.tsv` — every recovered file with size, type, path,
  and SHA-256.
- `inventory/EXACT-DUPLICATES.tsv` — groups of byte-identical recovered files.
- `inventory/SUMMARY.md` — mechanical inventory summary.

Recovery is additive: material is promoted out of `raw-import/`; the raw
corpus is not reorganized in place.
