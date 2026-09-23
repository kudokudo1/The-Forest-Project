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
| Tree identity / Seed 0.0.2 | RECONCILED | Seed 0.0.2 package reconstructed verbatim with SHA-256 provenance; later identity evolution remains a separate reconciliation task. |
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

Next reconcile the **Workshop system + capability resolver** as a coupled subsystem: canonical Forest capability definitions, Workshop profiles, Hermes adapter mapping, controller/resolver source, and the evidence showing exact-state activation/rollback.
