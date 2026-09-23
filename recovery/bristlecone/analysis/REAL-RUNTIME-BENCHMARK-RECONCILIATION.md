# Bristlecone Pine — Real Runtime and Benchmark Evidence Reconciliation

Status: **RECONCILED**

## Real-runtime J-series

The J-series certifications prove that the late recovered Task Session and resource path were exercised through the real Hermes runtime rather than only fake adapters.

### J.1 — first real Small turn

Certified a successful Forest-mediated real Small turn through Hermes using binding-0001 and execution_context_id ctx-j1 with persist=False.

### J.2 — working-state session commitment

Certified that a newly created runtime session is written into canonical working Forest state before optional durable persistence. The run also exposed and repaired double-counting of already-resident model weights in the live Small resource provider.

### J.3 — same-session reuse

Certified two turns in the same Forest Task/context/binding reusing the same real Hermes session without an unnecessary replacement session.

### J.4 — multi-context isolation

Certified two execution contexts retaining separate Hermes runtime sessions while sharing one resident Small model process/weight residency.

Together these J-series records anchor the distinction between Tree/context identity, runtime-session identity, and shared model residency.

## L.8 — Resource Governor

L.8 A+B independently certifies the resource-governor semantic matrix and the frozen performance artifacts. The current resources package is byte-identical to source included in this certification.

## L.9 — Recovery Cost

L.9 A certified:

- Forest additional recovery-control median: 71.605 µs
- Hermes create_session median: 327.564180 ms
- Hermes end_session median: 207.023972 ms
- genuine real Hermes stale-session S -> replacement R recovery: PASS
- exactly-one-retry enforcement

The matched whole-turn experiment did not establish a recovery speedup or a clean whole-turn recovery-cost estimate because Small-model generation variance dominated.

Terminal B independently verified the archive, raw-sample recomputation, exactly-one-retry behavior, genuine S -> R recovery, matched pairs, production-source identity, and A-summary consistency.

## L.10 — sustained same-session behavior

L.10 A certification ran eight measured real Small turns after one unmeasured prime using one runtime session.

Certified invariants included stable session identity, Model Form, Reasoning, binding, execution context, residency, zero unexpected recovery, zero unexpected rotation, and no persistent production-state mutation.

The evidence did not support a causal latency-improvement, latency-degradation, or memory-leak claim.

## Benchmark chronology encoded by surviving L.11A source

The surviving L.11A evidence-inventory builder records:

- L.0 foundation-certified
- L.1 A+B
- L.2 A+B
- L.3 A-only; B deferred
- L.4 A+B
- L.5 A-only; B pending
- L.6 A+B
- L.7 A+B
- L.8 A+B
- L.9 A+B
- L.10 A+B

This chronology is treated as late source evidence. It does not convert the missing L.11 output into a recovered certification artifact.

## Recovery conclusion

The benchmark/certification corpus is sufficiently coherent to use as the historical regression specification for the Bristlecone implementation.

Historical latency numbers must not be treated as current Post-Apollo expectations because model, runtime, host OS, hardware exposure, and implementation language are changing.