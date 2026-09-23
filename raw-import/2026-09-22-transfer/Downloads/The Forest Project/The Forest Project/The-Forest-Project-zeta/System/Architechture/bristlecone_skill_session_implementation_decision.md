# Bristlecone Pine — Skill Session Implementation Decision

**Project:** The Forest / Bristlecone Pine  
**Area:** Workshops, Skills, Task Sessions, Hermes adapter  
**Date:** 2026-08-08  
**Decision:** Use **Design 2 — Modular Test Harness** for Phase 1 testing.  
**Long-term direction:** Build a Forest-native `TaskSessionManager` above a `HermesAdapter`.

---

# 1. Decision Summary

For the current Phase 1 Skill tests, use the modular implementation rather than the original linear diagnostic script.

The modular implementation separates:

```text
Skill resolution
HTTP client setup
Task Session creation
chat execution
```

into clear reusable functions.

This gives us a cleaner test harness without prematurely building the full Forest production architecture.

The production target remains:

```text
Forest
  ↓
TaskSessionManager
  ↓
HermesAdapter
  ↓
Hermes runtime
```

The Phase 1 test script is therefore a stepping stone, not the final Forest implementation.

---

# 2. Design 1 — Linear Diagnostic Script

The original test design performs every operation inline:

```text
load Skill
read API key
create Hermes session
send Turn 1
send Turn 2
read session metadata
print diagnostics
```

## Advantages

- Extremely explicit.
- Easy to inspect during initial troubleshooting.
- Easy to identify which individual HTTP operation failed.
- Useful as a disposable diagnostic.

## Disadvantages

- Repeats HTTP and error-handling logic.
- Mixes Skill resolution, transport, Task Session behavior, and output formatting.
- Harder to reuse.
- Poor foundation for eventual Forest code.
- Becomes cumbersome as more Skills, Workshops, or session states are added.

---

# 3. Design 2 — Modular Test Harness

The selected Phase 1 design separates functionality into small pieces:

```text
build_skill()
make_client()
create_task_session()
chat()
```

Execution then becomes:

```text
Skill
  ↓
Task Session
  ↓
Turn 1
  ↓
Turn 2
```

## Advantages

- Clear separation of responsibilities.
- Less duplicated code.
- Easier to test individual components.
- Easier to extend to additional Skills.
- Easier to convert into a Hermes adapter later.
- Uses a persistent `requests.Session()` for localhost HTTP connection reuse.
- Keeps credentials loaded once and never prints them.
- Uses `raise_for_status()` for simple HTTP failure handling.
- Keeps the Task-Sticky test logically clean.

## Performance

The modular version may save a small amount of HTTP setup overhead through connection reuse.

However, this is not expected to be the main Bristlecone speed improvement.

The dominant costs are likely to remain:

```text
model load
prompt processing
Skill prompt size
tool schemas
inference
KV / prefix cache behavior
```

The `systematic-debugging` Skill generated a prompt of approximately **14,510 characters** during the Phase 1 isolated loader test.

That makes Skill prompt processing a much more meaningful benchmark target than Python function-call overhead.

---

# 4. Design 3 — Production Forest Architecture

The eventual production architecture should not simply promote the Phase 1 test script into permanent infrastructure.

Recommended architecture:

```text
                 THE FOREST
                     │
              TaskSessionManager
                     │
          ┌──────────┴──────────┐
          │                     │
 Capability Registry        Forest State
          │                     │
          └──────────┬──────────┘
                     │
                HermesAdapter
                     │
          ┌──────────┴──────────┐
          │                     │
     Skill Backend         Session Backend
          │                     │
          ▼                     ▼
 Hermes Skill loader      Hermes API server
```

High-level Forest code should eventually resemble:

```python
session = forest.start_task(
    workshop="code-debug",
    sticky=["debugging"],
)

session.chat("Investigate this service failure.")
```

The Forest should not need to know that Hermes calls the canonical Forest capability `debugging`:

```text
systematic-debugging
```

The Hermes adapter performs that translation.

---

# 5. Forest / Hermes Responsibility Boundary

## Forest owns

```text
canonical capability IDs
Workshop definitions
Task Session lifecycle
Core capabilities
Task-Sticky Skills
temporary overlays
Reasoning Mode
Model Form
Hot Leaves
operational learning
portable state
```

## Hermes adapter owns

```text
Forest capability → Hermes capability mapping
Skill preload calls
Hermes session creation
Hermes API transport
runtime-specific validation
resolved Hermes Skill names
```

## Hermes runtime owns

```text
SKILL.md loading
Skill security / disabled filtering
system prompt construction
session database
agent execution
tool execution
runtime credentials
```

---

# 6. Do Not Store Hermes Skill Prompt Text as Forest State

Forest should preserve semantic state such as:

```yaml
task_session:
  workshop: code-debug

  task_sticky:
    - debugging

  runtime:
    adapter: hermes
    resolved_skills:
      - systematic-debugging
    session_id: forest_task_001
```

Forest should **not** make the generated 14,510-character Hermes Skill prompt its canonical state.

Hermes may persist the generated system prompt inside its own runtime/session database.

This protects portability.

If Hermes is later replaced:

```text
Forest:
debugging
   ↓
new runtime adapter
   ↓
new runtime-specific Skill implementation
```

No Hermes-formatted prompt migration is required.

---

# 7. Why We Are Not Modifying Hermes Yet

A theoretically cleaner Hermes API might accept:

```json
{
  "skills": ["systematic-debugging"]
}
```

and internally perform:

```text
Skill list
  ↓
build_preloaded_skills_prompt()
  ↓
session system prompt
```

That would let Forest use one Hermes interface instead of:

```text
Python Skill loader
+
HTTP session API
```

However, modifying Hermes now would create unnecessary coupling:

```text
Hermes update
  ↓
Forest-specific Hermes patch may break
```

Current preference:

```text
Stock Hermes
     ↑
HermesAdapter
     ↑
Forest
```

rather than:

```text
Modified Hermes fork
     ↑
Forest
```

Only reconsider modifying Hermes if measurement later proves the adapter boundary causes a meaningful performance or reliability problem.

---

# 8. Implementation Ranking

## 1. Forest `TaskSessionManager` + `HermesAdapter`

**Best production architecture**

```text
★★★★★
```

Advantages:

- portable
- clean ownership boundaries
- easy runtime replacement
- appropriate place for Task-Sticky policy
- appropriate place for operational learning

---

## 2. Modular Phase 1 Test Harness

**Selected current design**

```text
★★★★☆
```

Advantages:

- clean
- reusable
- testable
- low implementation overhead
- structurally similar to the eventual adapter

Use this now.

---

## 3. Original Linear Diagnostic Script

**Useful troubleshooting tool**

```text
★★★☆☆
```

Keep the pattern available for deep debugging, but do not use it as permanent architecture.

---

## 4. Modify Hermes Source Immediately

```text
★★☆☆☆
```

Potentially elegant interface, but creates unnecessary maintenance and coupling at the current stage.

Do not pursue during Phase 1.

---

# 9. Selected Phase 1 Test Architecture

The selected test flow is:

```text
Forest Phase 1 test
      │
      ▼
build_skill("systematic-debugging")
      │
      ▼
Hermes build_preloaded_skills_prompt()
      │
      ▼
create disposable Hermes Task Session
      │
      ▼
persist Skill-generated system prompt once
      │
      ├── Turn 1
      │
      └── Turn 2
           no Skill prompt resent
```

The key experiment is whether Turn 2 restores the Task Session's persisted system prompt automatically.

If successful, this validates Hermes's persisted session prompt as a runtime primitive for Forest **Task-Sticky Skills**.

---

# 10. Current Phase 1 Status

```text
✓ Skill discovery understood
✓ metadata / full-content split understood
✓ lazy Skill loading confirmed
✓ exact single-Skill preload confirmed
✓ disabled Skill filtering confirmed
✓ build_preloaded_skills_prompt() confirmed
✓ systematic-debugging loads independently
✓ generated prompt confirmed
✓ API server live
✓ native session API live
✓ persisted system_prompt support identified
✓ ephemeral prompt mechanism identified
✓ cached + ephemeral prompt composition identified

→ live Task-Sticky Skill session test
□ verify Skill persists into Turn 2
□ verify unrelated Skills are absent
□ integrate Skill selection with bristlecone-workshop
□ verify activation/deactivation
```

---

# 11. Phase 2 Implication

Phase 2 remains:

**Unified Live State + Task Sessions**

Likely responsibilities:

```text
Task Session schema
Workshop state
Core capabilities
Task-Sticky capabilities
temporary overlays
resolved runtime toolsets
resolved runtime Skills
Hermes session ID
atomic transitions
rollback
verification
```

---

# 12. Phase 3 Benchmark Implication

Benchmark at minimum:

```text
file + terminal
file + terminal + todo
file + terminal + debugging
file + terminal + todo + debugging
web
```

Compare:

```text
new Task Session
vs
reused Task Session

cold Skill activation
vs
Task-Sticky Skill reuse
```

Measure:

```text
first-output latency
completion time
input tokens
Skill prompt overhead
Workshop switching overhead
Task Session reuse benefit
cache behavior
```

---

# 13. Final Decision

> **Use Design 2, the modular test harness, for current Phase 1 testing.**

It provides the best balance of:

```text
clarity
reusability
low complexity
diagnostic value
future adapter compatibility
```

Do not treat it as the final Forest production implementation.

After Phase 1 validates the runtime behavior, implement the production feature behind:

```text
TaskSessionManager
      ↓
HermesAdapter
```

while keeping Forest canonical state independent of Hermes implementation details.
