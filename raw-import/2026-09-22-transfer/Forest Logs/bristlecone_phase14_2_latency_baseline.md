# Bristlecone Phase 14.2 — Cold / Warm Latency Baseline

**Date:** 2026-08-09  
**Phase:** 14 — Layered Hot Context / Performance  
**Checkpoint:** 14.2 Cold / Warm End-to-End Latency

---

## Test Conditions

Runtime:

```text
Adapter: hermes
Model: bristlecone-qwen35:4b-64k
```

The model was confirmed **not resident** before the cold run.

After the cold turn, Ollama reported:

```text
bristlecone-qwen35:4b-64k
SIZE:      5.6 GB
PROCESSOR: 100% CPU
CONTEXT:   64000
KEEPALIVE: ~14 minutes
```

Each benchmark turn used a fresh Hermes session so conversation-history growth would not contaminate the comparison.

The model remained resident for the three warm runs.

---

# Results

| Run | Latency |
|---|---:|
| Cold | 162.29 s |
| Warm 1 | 158.82 s |
| Warm 2 | 189.47 s |
| Warm 3 | 63.75 s |
| **Warm average** | **137.34 s** |
| **Warm median** | **158.82 s** |
| **Warm best** | **63.75 s** |

Calculated:

```text
Cold → warm speedup: 1.18x
Average latency reduction: 15.4%
```

---

# Interpretation

The current system has a dramatically smaller static prompt footprint than earlier Bristlecone configurations, but that reduction has **not translated into consistently fast warm turns**.

Phase 14.1 current static footprint:

```text
System prompt:  9,832 B
Tool schemas:  11,159 B
Combined:      20,991 B
Tools:          6
```

Despite this, warm response times were highly variable:

```text
158.82 s
189.47 s
63.75 s
```

This means model residency alone is not sufficient to explain current latency.

The result does **not** yet prove what the bottleneck is.

Possible categories to inspect next include:

- prompt/context reconstruction
- runtime/session setup
- repeated configuration or manifest parsing
- repeated capability resolution
- Hermes request assembly
- prompt-prefix reuse or lack of reuse
- CPU inference variability
- context-window/runtime behavior
- model evaluation/generation cost
- Skill or instruction material being rebuilt even when not visibly large

These are investigation targets, not yet confirmed causes.

---

# Important Observation

The warm-best result of:

```text
63.75 seconds
```

shows that the current stack **can** complete the same benchmark materially faster than the other runs.

Therefore the immediate Phase 14 goal should be to determine why warm behavior is inconsistent rather than assuming the remaining cost is unavoidable model inference.

---

# Safety Verification

```text
Forest state unchanged: PASS
Hermes config unchanged: PASS
Model returned to unloaded state: PASS
Persistent source files modified: NONE
```

The benchmark did not alter persistent Forest or Hermes configuration.

---

# Phase 14 Status

```text
✅ 14.1 — Fresh post-Phase-13 prompt/schema baseline
✅ 14.2 — Cold / warm latency baseline

→ 14.3 — Stable vs. dynamic context/rebuild map
□ 14.4 — Manifest + capability-resolution cache
□ 14.5 — Warm Skill caching
□ 14.6 — Layered Hot Context assembler
□ 14.7 — Source-context targeting
□ 14.8 — Quick / Normal / Deep routing
□ 14.9 — Small / Big model escalation boundary
□ 14.10 — Runtime/prefix-cache evaluation
□ 14.11 — Ollama vs. llama.cpp evaluation
□ 14.12 — Speculative decoding decision
□ 14.13 — Final performance benchmark
```

---

# Phase 14.2 Conclusion

> **Prompt-size reduction succeeded, but warm-turn latency remains inconsistent. Phase 14 should now identify repeated work and unstable runtime cost before adding new optimization layers.**
