# Bristlecone Recovery Reconciliation

Source:

`raw-import/2026-09-22-transfer/The-Forest/bristlecone/`

This inventory is descriptive recovery evidence.

It does **not** declare any surviving source file canonical.

## Mechanical inventory

- Total recovered Bristlecone files: 1380
- Total recovered Bristlecone bytes: 37,140,155

## Current Python implementation

The `CURRENT_SOURCE` classification excludes benchmark tools, tests,
certification tooling, backup snapshots, and generated Python caches.

- Current production Python files: 80
- Current production Python bytes: 1,018,071
- Exact certified-match files: 32
- Files without an exact certified match: 48
- Exact-certified coverage: 40.0%

## Recovered file categories

- BENCHMARK_EVIDENCE: 80
- BENCHMARK_TOOL: 5
- CERTIFICATION: 47
- CERTIFIED_BACKUP: 604
- CORPUS: 2
- CURRENT_CONFIG: 8
- CURRENT_DOCUMENTATION: 5
- CURRENT_OTHER: 1
- CURRENT_SCRIPT: 10
- CURRENT_SOURCE: 80
- GENERATED_CACHE: 190
- HISTORICAL_BACKUP: 320
- RUNTIME_LOG: 2
- RUNTIME_STATE: 2
- TEST: 24

## What an exact certified match means

A current production file with the same SHA-256 as a file preserved in a
certified backup is strong evidence that the current file existed unchanged
at that certified engineering checkpoint.

This is stronger than relying on:

- filenames,
- modification-looking timestamps,
- words such as `final` or `master`,
- narrative checkpoint descriptions,
- or the current filesystem location alone.

## What a missing certified match means

A current file without an exact certified-backup match is **not**
automatically invalid, unfinished, or newer than the certified system.

It means only that exact-content certification has not yet been established
by this mechanical comparison.

Those files require additional reconciliation using:

- engineering chronology,
- checkpoint documents,
- tests,
- manifests and hashes,
- benchmark evidence,
- architecture records,
- dependencies and imports,
- and surrounding certified source.

## Current recovery interpretation

The surviving Bristlecone tree contains both directly certified production
source and source whose authority must be established through broader
evidence.

The reconciliation process therefore separates:

1. files with direct exact-content certification evidence;
2. files requiring contextual reconciliation;
3. certification and benchmark evidence;
4. historical backups;
5. generated/runtime material.

No material is promoted to the clean canonical `bristlecone/` tree solely
because it currently lives at the top level of the recovered Bristlecone
directory.

## Preservation rule

`raw-import/2026-09-22-transfer/` is the frozen archaeological source.

This inventory may read and hash that material, but must not rename, move,
deduplicate, rewrite, or delete it.
