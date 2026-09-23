# Bristlecone Phase 14.3–14.4 — Repeated Work and Hot-Path Audit

**Date:** 2026-08-09  
**Phase:** 14 — Layered Hot Context / Performance

## 14.3 — Repeated-Work Source Map

The source audit found YAML parsing and capability resolution primarily in controller, resolver, state-management, and Spring-restoration paths rather than in the normal model-turn hot path.

### Decision

```text
Manifest/resolver caching:
DEFER — not currently justified as a latency fix.
```

Caching may still be useful later for cleanliness or scale, but there is no evidence that repeated manifest parsing or capability resolution explains the current 60–190 second turn latency.

---

## 14.4 — Hot-Turn Path Audit

The benchmark used for Phase 14.2 called the runtime adapter directly:

```text
create_session()
→ send_turn()
```

It did **not** send the benchmark through `TaskSessionManager.send_runtime_turn()`.

Therefore the measured 60–190 second latency does not include most Forest Task lifecycle bookkeeping, such as:

- guarded Task-session persistence
- Spring restoration logic
- stale-session recovery unless the adapter itself reports a stale session
- Task binding rotation
- Forest state locking
- capability resolution in Spring paths

### Hermes `send_turn()`

The normal Hermes adapter turn path is comparatively small:

```text
validate session/message
→ encode session ID
→ build session chat payload
→ POST /api/sessions/<id>/chat
→ wait for Hermes response
→ validate/return response metadata
```

The major blocking point is the Hermes API request itself.

### Hermes `_api_request()`

The request helper:

```text
resolve API key
→ JSON encode payload
→ build loopback HTTP request
→ opener.open(...)
→ response.read()
→ JSON decode response
```

The Python-side work surrounding the HTTP request is small relative to the observed multi-minute latency.

### Skill Overlay

`build_skill_overlay()` is a separate adapter method. It loads/builds a preloaded Skill prompt when explicitly invoked, but it is **not called by `HermesRuntimeAdapter.send_turn()` itself**.

No evidence from this audit shows Skill overlays being regenerated on every benchmark turn.

---

# Phase 14.4 Conclusion

> **The dominant latency exposed by Phase 14.2 is below the Forest control layer. The next investigation should measure Hermes/Ollama prompt evaluation, generation, session reuse, and prefix/KV behavior rather than adding Python-side manifest caches.**

Current leading investigation targets:

```text
Hermes request/session behavior
Ollama prompt evaluation
Ollama generation/evaluation
64K context configuration
prefix/KV reuse
reasoning behavior
CPU inference variability
```

---

# Phase Status

```text
✅ 14.1 — Prompt/schema baseline
✅ 14.2 — Cold/warm latency baseline
✅ 14.3 — Stable/dynamic repeated-work map
✅ 14.4 — Hot-turn path audit

→ 14.5 — Runtime timing + session/prefix reuse test
□ 14.6 — Layered Hot Context assembler
□ 14.7 — Source-context targeting
□ 14.8 — Quick / Normal / Deep routing
□ 14.9 — Small / Big model escalation boundary
□ 14.10 — Runtime/prefix-cache evaluation
□ 14.11 — Ollama vs. llama.cpp evaluation
□ 14.12 — Speculative decoding decision
□ 14.13 — Final performance benchmark
```
