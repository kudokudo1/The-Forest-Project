# Bristlecone Pine Reconstruction Status

This file is a human-readable recovery dashboard.

It is **not evidence by itself**. Every status must be traceable to the migration ledger and recovered source/certification evidence.

## Status vocabulary

- `NOT STARTED` — subsystem has not been reconciled.
- `EVIDENCE FOUND` — relevant recovered material exists, but no authoritative selection has been made.
- `RECONCILING` — evidence/source versions are actively being compared.
- `RECONCILED` — best recovered logical artifact has been selected with provenance.
- `CERTIFIED` — recovered certification evidence establishes the claimed behavior/checkpoint.
- `PARTIAL` — some implementation/evidence survives, but the recovered state is incomplete.
- `SOURCE CONFLICT` — surviving evidence disagrees and requires resolution.

## Current dashboard

| Subsystem / checkpoint | Recovery state | Notes |
|---|---|---|
| Tree identity / Seed 0.0.2 | EVIDENCE FOUND | SOUL/AGENTS/Seed/bootstrap material survives in the raw corpus. |
| Workshop system | EVIDENCE FOUND | Architecture, controller snapshots, and runtime evidence survive. |
| Capability resolver | EVIDENCE FOUND | Python resolver snapshots and Hermes mapping survive. |
| Task Sessions | EVIDENCE FOUND | Numerous certified and pre-change snapshots survive through Phase 14.11. |
| Layered Hot Context | EVIDENCE FOUND | Architecture/checkpoints and implementation-era evidence survive. |
| Reasoning Controls | EVIDENCE FOUND | Phase 14.10 source/checkpoint material survives. |
| Model Forms | EVIDENCE FOUND | Phase 14.11 model-form source and certified snapshots survive. |
| Session Identity / Store | EVIDENCE FOUND | Certified Phase 14.11 runtime snapshots survive. |
| Handoff / Continuity | EVIDENCE FOUND | Handoff and continuity source snapshots survive. |
| Hermes runtime adapter | EVIDENCE FOUND | Adapter mappings and multiple source snapshots survive. |
| Benchmarks | EVIDENCE FOUND | Phase 14 benchmark material survives. |
| Phase 14.11 L.9 | CERTIFIED | Recovery authority records A+B certification. |
| Phase 14.11 L.10 | CERTIFIED | Recovery authority records independent A+B certification. |
| Phase 14.11 L.11 | PARTIAL | Work began; expected generated evidence inventory has not been found. |

## Next recovery target

Start with **Tree identity / Seed 0.0.2** because it defines Bristlecone independently of the runtime and provides the foundation for interpreting later implementation.

Then proceed subsystem-by-subsystem, recording every promoted artifact in `recovery/MIGRATION-LEDGER.tsv`.
