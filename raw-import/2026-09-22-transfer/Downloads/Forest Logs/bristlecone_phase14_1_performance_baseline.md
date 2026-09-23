# Bristlecone Phase 14.1 — Post-Phase-13 Performance Baseline

**Date:** 2026-08-09  
**Phase:** 14 — Layered Hot Context / Performance  
**Checkpoint:** 14.1 Fresh Baseline

---

## Current Runtime State

```text
Runtime adapter: hermes
Workshop: code-debug
General: []
Ready: ['debugging']
Task status: inactive
Task-Sticky Skills: ['debugging']
```

Ollama residency at capture time:

```text
No model currently loaded.
```

---

## Current Hermes Prompt-Size Baseline

Model:

```text
bristlecone-qwen35:4b-64k
```

### System Prompt

```text
System prompt total: 9,832 B
Characters:          9,574
```

Major blocks:

```text
skills index:    0 B
memory:          0 B
user profile:  582 B
```

Prompt tiers:

```text
stable:    7,189 B
context:   1,956 B
volatile:    683 B
```

Approximately **73% of the current system prompt is stable**.

### Tool Schemas

```text
Tool schemas total: 11,159 B
Total tools:         6
```

Toolsets:

```text
file:
  tools:  4
  schema: 6,328 B

terminal:
  tools:  2
  schema: 4,819 B
```

### Combined Current Static Footprint

```text
System prompt:   9,832 B
Tool schemas:   11,159 B
────────────────────────
Combined:       20,991 B
```

---

# Historical Comparison

| Test | System Prompt | Tool Schemas | Tools | Combined |
|---|---:|---:|---:|---:|
| Earlier API | 17,727 B | 40,712 B | 25 | 58,439 B |
| API final after trimming | 16,864 B | 28,188 B | 12 | 45,052 B |
| CLI post-trim | 20,994 B | 31,532 B | 14 | 52,526 B |
| **Phase 14.1 current baseline** | **9,832 B** | **11,159 B** | **6** | **20,991 B** |

---

## Improvement vs. Previous API Final

Previous API final:

```text
System prompt: 16,864 B
Tool schemas:  28,188 B
Combined:      45,052 B
Tools:         12
```

Current Phase 14.1 baseline:

```text
System prompt:  9,832 B
Tool schemas:  11,159 B
Combined:      20,991 B
Tools:          6
```

Approximate reductions:

```text
System prompt: ~42% smaller
Tool schemas:  ~60% smaller
Combined:      ~53% smaller
Tool count:     50% fewer
```

---

## Improvement vs. Earlier API Test

Earlier API:

```text
System prompt: 17,727 B
Tool schemas:  40,712 B
Combined:      58,439 B
Tools:         25
```

Current:

```text
System prompt:  9,832 B
Tool schemas:  11,159 B
Combined:      20,991 B
Tools:          6
```

Approximate reductions:

```text
Combined static footprint: ~64% smaller
Tool-schema footprint:     ~73% smaller
Tool count:                25 → 6
```

---

# Interpretation

Selective Workshop loading is working as intended.

Code / Debug currently exposes only its minimum useful runtime canopy:

```text
file
terminal
```

Those two toolsets account for all six currently exposed runtime tools.

Current Skill and memory blocks are not contributing additional prompt cost:

```text
Skills index: 0 B
Memory:       0 B
```

The current prompt shape is also favorable for Layered Hot Context work because most system-prompt material is already classified as stable:

```text
Stable:   7,189 B
Dynamic:  2,639 B
```

This creates a strong target for prefix/KV reuse and for avoiding unnecessary prompt reconstruction.

---

# Phase 14 Status

```text
✅ 14.1 — Fresh post-Phase-13 baseline

→ 14.2 — Cold / warm latency measurement
□ 14.3 — Stable vs. dynamic context map
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

# Phase 14 Principle

> **Stop Bristlecone from repeatedly loading, rebuilding, resolving, or transmitting information that has not changed.**

The next measurement should establish whether the dramatically smaller post-Phase-13 prompt footprint has translated into lower **cold and warm response latency**.
