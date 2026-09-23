# Bristlecone Pine — Layered Hot Context, Task Sessions, and Selective Cache Rebuild

**Project:** The Forest / Bristlecone Pine  
**Date:** 2026-08-08  
**Status:** Architecture update based on live Hermes Skill + Task Session testing

---

# 1. Purpose

This note records the newest live findings from Phase 1 and the resulting architecture improvement.

The Forest should adopt the useful **reuse-or-rebuild pattern** observed in Hermes, but at the Forest's own semantic layer rather than copying Hermes' internal implementation.

The Forest should maintain reusable layers of active Task Session state, invalidate only the layers affected by a change, and rebuild only what is necessary.

The important concept is:

> **Keep stable Task Session layers reusable. When something changes, invalidate only the affected layer or dependent layers, then rebuild the active Hot Context from the remaining reusable pieces.**

This note intentionally does **not** use the older “canopy” term for this architecture.

---

# 2. New Live Data

## 2.1 Individual Skill loading worked

The Hermes Skill loader successfully resolved only:

```text
systematic-debugging
```

The test produced:

```text
Loaded Skills: ['systematic-debugging']
Missing: none
Generated prompt: yes
Prompt characters: 14510
```

This confirmed that a single Skill can be loaded independently without loading the entire Hermes Skills surface.

---

## 2.2 Task Session creation worked

A disposable Hermes session was created:

```text
forest_skill_test_1786223745
```

with:

```text
Model:
bristlecone-qwen35:4b-64k

Skill requested:
systematic-debugging

Skill-generated prompt:
14510 characters
```

Immediately after the first turn, the API reported:

```text
Has system prompt: True
Message count: 2
Tool calls: 0
```

This demonstrated that Hermes had created and persisted the session and that Turn 1 completed server-side.

---

## 2.3 Turn 1 exceeded the client timeout but completed server-side

The first synchronous HTTP call used:

```text
read timeout = 300 seconds
```

The client timed out after five minutes.

However, the later session query returned:

```text
Message count: 2
```

which indicates the server-side turn completed and persisted the conversation even though the original HTTP client stopped waiting.

This separates two concepts:

```text
agent execution
vs
client transport timeout
```

A client timeout does not necessarily mean the Hermes Task Session failed.

---

## 2.4 Turn 2 succeeded without resending Skill data

Turn 2 was sent to the same session.

The request did **not** include:

```text
system_prompt
system_message
instructions
Skill name
Skill prompt
```

Result:

```text
Status: 200
Elapsed: 191.37 seconds

Input tokens: 5610
Output tokens: 462
Total tokens: 6072
```

The model was already loaded in Ollama:

```text
bristlecone-qwen35:4b-64k
5.6 GB
100% CPU allocation
64000 context
```

Therefore Turn 2 did not include a cold 5.6 GB model-load event.

The 191.37-second result is therefore especially important for later Phase 3 performance work.

---

# 3. Important Correction to the Original Task-Sticky Interpretation

The successful Turn 2 originally appeared to prove that the Skill prompt persisted automatically across the Task Session.

A direct SQLite inspection changed that conclusion.

The session database was:

```text
/home/user/.hermes/profiles/bristlecone/state.db
```

After Turn 2:

```text
Stored prompt characters: 0

systematic-debugging       ABSENT
test-driven-development    ABSENT
evaluation                 ABSENT
inference                  ABSENT
```

Therefore:

> Turn 2 succeeding does not by itself prove that `systematic-debugging` remained in the active system prompt.

The conversation continued, but the persisted Skill prompt was no longer present afterward.

This is an important Phase 1 correction.

---

# 4. Hermes System Prompt Restore Behavior

Inspection of:

```text
agent/conversation_loop.py
```

showed that Hermes explicitly supports persisted system-prompt reuse.

Simplified behavior:

```text
read stored system prompt
        ↓
stored prompt exists?
        ↓
check runtime compatibility
        ↓
compatible?
   ┌────┴────┐
  YES        NO
   │          │
reuse       rebuild
   │          │
   └────┬─────┘
        ↓
continue session
```

The relevant runtime identity checks include:

```text
Model
Provider
Current working directory
Platform
```

Importantly, Hermes only rejects a stored field when:

```text
stored value exists
AND
current value exists
AND
stored != current
```

Therefore a Skill-only prompt containing none of those runtime identity fields would generally pass the runtime identity test.

This ruled out the earlier theory that the debugging prompt disappeared simply because it lacked Hermes runtime metadata.

---

# 5. Hermes Compression Can Rebuild the System Prompt

The only direct `update_system_prompt()` writers found in the agent/gateway code were:

```text
agent/conversation_loop.py:603
agent/conversation_compression.py:3324
```

The first is the normal system-prompt persistence path.

The second occurs in conversation compression.

Inspection of the compression code showed:

```text
cached_system_prompt = agent._cached_system_prompt

agent._invalidate_system_prompt()
```

Hermes then determines whether the exact cached prompt can be retained.

Simplified:

```text
cached system prompt
        ↓
invalidate current cached prompt
        ↓
can exact previous prompt be reused safely?
        │
   ┌────┴────┐
  YES        NO
   │          │
reuse       rebuild
   │          │
   └────┬─────┘
        ↓
new_system_prompt
        ↓
persist replacement
```

The exact-prompt reuse path requires conditions including:

```text
cached_system_prompt is not None
no external memory manager
cached prompt correctly reflects built-in memory
```

If those conditions fail:

```python
new_system_prompt = agent._build_system_prompt(system_message)
```

The replacement can then be persisted.

---

# 6. Why a Skill-Only System Prompt Is Fragile

The test created the Task Session with:

```text
system_prompt = generated debugging Skill prompt
```

That made the Skill prompt function as the **entire Hermes system prompt**.

This is not the correct long-term architecture.

Hermes expects its cached system prompt to represent its normal runtime-generated prompt structure.

A standalone Skill prompt may not contain the memory, runtime, environment, or other internal prompt components Hermes expects when deciding whether an exact prompt is still reusable.

That means a later Hermes maintenance event such as compression can legally rebuild the system prompt and remove the Skill content.

The architectural problem is therefore:

```text
Skill prompt
    ↓
REPLACED Hermes base prompt
```

when the desired model is:

```text
Hermes / Tree base prompt
        +
Task-Sticky Skill layer
```

---

# 7. New Forest Architecture: Layered Hot Context

The Forest should maintain the active Task Session as several independent logical layers.

Example:

```text
FOREST TASK SESSION
│
├── Base Tree / runtime layer
│     identity
│     runtime environment
│     permissions
│
├── Workshop layer
│     Code / Debug
│
├── Core capability layer
│     file
│     terminal
│
├── Task-Sticky layer
│     debugging
│
├── General / temporary capability layer
│     todo
│     clarify
│
├── Leaf / knowledge layer
│     task-relevant Forest knowledge
│
├── Conversation / task state
│
└── Current user turn
```

These layers together form the current **Hot Context**.

The Forest does not need to rebuild all of them every turn.

---

# 8. Selective Invalidation

The Forest should track dependencies for each active layer.

When something changes:

```text
change detected
      ↓
which layer depends on it?
      ↓
invalidate affected layer
      ↓
invalidate dependent layers if required
      ↓
reuse unaffected layers
      ↓
rebuild only invalid layers
      ↓
compose new Hot Context
```

Example:

## New user turn in the same debugging task

Reuse:

```text
Tree identity             KEEP
Workshop                  KEEP
file                      KEEP
terminal                  KEEP
debugging Skill           KEEP
Task Session state        KEEP
relevant Leaves           KEEP
```

Change:

```text
current user turn         REPLACE
```

---

## Activating Todo

Existing state:

```text
Code / Debug
file
terminal
debugging
```

New request requires Todo.

Only add:

```text
todo                     BUILD / ACTIVATE
```

Keep:

```text
Workshop                  KEEP
file                      KEEP
terminal                  KEEP
debugging                 KEEP
Tree identity             KEEP
```

---

## Switching Code / Debug → Research

Invalidate:

```text
Code / Debug Workshop
file Core role
terminal Core role
debugging Task-Sticky state if the debugging task ends
```

Activate:

```text
Research Workshop
web Core
```

Keep if still valid:

```text
Tree identity
user profile
model
general Task Session metadata
relevant shared Leaves
runtime credentials
```

---

## Changing model

Potentially invalidate:

```text
model-dependent runtime identity
KV / prefix cache
model-specific prompt metadata
runtime performance assumptions
```

Potentially keep:

```text
Workshop semantic identity
Forest capability IDs
Task goal
Task-Sticky Skill identity
Leaves
permissions
```

The runtime adapter then regenerates whatever runtime-specific form is necessary.

---

# 9. Reuse-or-Rebuild Rule

A formal Forest architecture rule should be:

> **Reuse any Task Session layer whose dependencies remain valid. Invalidate and rebuild only layers whose dependencies changed. Then compose the current Hot Context from the valid reusable layers plus newly rebuilt layers.**

This is inspired by Hermes' cached prompt behavior but operates at a higher architectural level.

Hermes owns:

```text
runtime prompt caching
runtime prefix caching
runtime session DB
runtime compression
runtime-specific prompt rebuild
```

The Forest owns:

```text
Task Session semantics
Workshop identity
capability identity
Task-Sticky state
Leaves
operational learning
semantic cache validity
layer dependencies
runtime-independent state
```

---

# 10. Forest and Hermes Should Maintain Separate Cache Responsibilities

The Forest should not attempt to replace Hermes' internal prompt cache.

Instead:

```text
THE FOREST
semantic Task Session cache
      ↓
HermesAdapter
      ↓
HERMES
runtime prompt / prefix / session cache
```

Both systems can reuse cached state independently.

Example:

```text
Forest says:
debugging is still Task-Sticky

Hermes says:
my base prompt was rebuilt during compression
```

The Forest can then reapply the semantic Task-Sticky debugging layer through the adapter.

The Skill does not disappear merely because Hermes rebuilt its own internal system prompt.

---

# 11. Task-Sticky Skill Improvement

The strongest current implementation direction is:

```text
Task Session starts
        ↓
resolve canonical Forest Skill
        ↓
HermesAdapter maps:
debugging
    →
systematic-debugging
        ↓
build Skill prompt ONCE
        ↓
cache resolved Task-Sticky Skill layer
        ↓
Turn 1
Turn 2
Turn 3
...
        ↓
reuse the cached Skill layer
```

The important optimization is:

```text
DO NOT:
rediscover Skill every turn
reread SKILL.md every turn
re-resolve mapping every turn
rebuild Skill prompt every turn
```

Instead:

```text
resolve once
build once
cache once
reuse while Task Session remains valid
```

---

# 12. Hermes Adapter Behavior for Task-Sticky Skills

Hermes currently supports:

```text
ephemeral_system_prompt
```

through API fields such as:

```text
system_message
instructions
```

These are per-turn runtime overlays.

Therefore a practical current Forest implementation can be:

```text
Forest Task Session
task_sticky:
  - debugging

        ↓

HermesAdapter cache
systematic-debugging prompt

        ↓ each related turn

Hermes base prompt
        +
cached debugging overlay
```

This makes the Skill **semantically Task-Sticky at the Forest layer**, even if Hermes itself treats the supplied overlay as per-turn.

Forest owns the persistence decision.

Hermes owns execution.

---

# 13. Why Reapplying an Overlay Is Different From Rebuilding a Skill

These should not be confused.

## Expensive / unnecessary version

Every turn:

```text
discover Skill
read SKILL.md
parse metadata
resolve mapping
build prompt
send prompt
```

## Improved version

At Task Session start:

```text
discover
resolve
build
cache
```

Then:

```text
Turn 1 → reuse cached overlay
Turn 2 → reuse cached overlay
Turn 3 → reuse cached overlay
```

This gives the Forest Task-Sticky behavior without depending on Hermes to store the Skill forever in its internal base system prompt.

---

# 14. Potential Future Optimization

A future runtime adapter or Forest-native agent harness could expose separate prompt layers directly:

```text
base_prompt
workshop_prompt
task_sticky_prompt
temporary_prompt
```

rather than concatenating everything into one string.

A runtime with strong prefix/KV caching could then preserve stable prefixes more effectively.

Potential stable ordering:

```text
Tree / runtime identity
        ↓
Workshop
        ↓
Task-Sticky Skills
        ↓
relevant Leaves
        ↓
conversation history
        ↓
current user turn
```

The most stable content stays earlier.

The most volatile content stays later.

This may improve future prefix-cache reuse.

---

# 15. Relationship to Cold / Warm / Hot

The existing Cold / Warm / Hot architecture remains useful.

## Cold

Full Tree state on disk:

```text
identity
all Workshops
all capability definitions
all Skills
all Leaves
permissions
routing
learning history
```

## Warm

Prepared reusable structures in RAM:

```text
parsed capability registry
Workshop manifests
Skill metadata
adapter mappings
resolved Skill identifiers
prebuilt Skill overlays
routing tables
derived indexes
```

## Hot

Only active Task Session state:

```text
base Tree/runtime layer
current Workshop
current Core capabilities
active General capabilities
Task-Sticky Skills
relevant Leaves
current task history
current turn
```

Selective invalidation determines which Warm or Hot pieces need rebuilding.

---

# 16. Phase 1 Status Update

```text
FOUNDATION
✓ Central Capability Registry
✓ Workshop schema
✓ Hermes adapter
✓ Workshop resolver
✓ live tool switching

PHASE 1 — Individual Skills / Task Sessions

✓ Hermes Skill discovery understood
✓ lazy Skill loading understood
✓ exact individual Skill loading confirmed
✓ systematic-debugging loaded alone
✓ generated Skill prompt measured: 14510 chars
✓ Hermes API Task Session creation confirmed
✓ Turn 1 completed server-side
✓ client timeout behavior identified
✓ Turn 2 completed on same Task Session
✓ warm Turn 2 completion measured: 191.37 s
✓ persisted system-prompt restore logic inspected
✓ runtime identity validation inspected
✓ compression system-prompt rebuild path identified
✓ Skill-as-entire-system-prompt identified as unsafe design

→ confirm whether compression caused the exact test-session prompt loss
→ test cached Task-Sticky overlay approach

□ prove exact Skill presence during inference
□ prove unrelated Skills absent
□ deactivation test
□ integrate Task-Sticky Skills into bristlecone-workshop
□ final Phase 1 end-to-end verification
```

---

# 17. New Phase 3 Benchmark Data to Preserve

Current live measurements:

## Isolated Skill generation

```text
Skill:
systematic-debugging

Generated prompt:
14510 characters
```

## Turn 1

```text
Task Session:
forest_skill_test_1786223745

Client read timeout:
300 seconds

Result:
client timed out

Server-side:
turn completed
message_count became 2
```

Therefore:

```text
Turn 1 full synchronous response > 300 seconds
```

Exact server completion time was not captured.

---

## Turn 2

```text
same Task Session
no Skill data resent in request

Elapsed:
191.37 seconds

Input tokens:
5610

Output tokens:
462

Total:
6072
```

Model was already loaded.

Therefore this is a warm-session result, not a cold-load benchmark.

Do not compare directly with earlier first-output timings because this measurement is full synchronous completion time.

---

# 18. Performance Questions Created by This Test

The Phase 3 benchmark should investigate:

```text
How much time is Skill prompt processing?
How much is model inference?
How much is Hermes agent overhead?
How much is 64K context configuration overhead?
How much is Task Session history?
How much does reusing a cached Skill overlay help?
How much does stable prefix / KV reuse help?
How much does a smaller active context improve latency?
```

The model currently reports:

```text
5.6 GB
CPU execution
64000 context
```

The large context setting may be a performance factor even when the actual turn contains far fewer tokens.

This must be measured rather than assumed.

---

# 19. Portability Benefit

The layered Forest design remains runtime-independent.

Example Forest state:

```yaml
task_session:
  workshop: code-debug

  task_sticky:
    - debugging

  active_general:
    - todo

  runtime:
    adapter: hermes
    session_id: forest_task_001
    resolved_skills:
      - systematic-debugging
```

Forest stores:

```text
debugging
```

not:

```text
14510-character Hermes-generated Skill prompt
```

The generated runtime overlay remains adapter/runtime state.

If Hermes is replaced:

```text
Forest debugging
      ↓
new adapter
      ↓
new runtime-specific implementation
```

The Task Session semantics remain intact.

---

# 20. Architectural Principle

The new principle should be treated as a companion to Cold / Warm / Hot:

> **Layered Reuse and Selective Rebuild**
>
> Keep stable Task Session components reusable. Track what each layer depends on. When state changes, invalidate only the affected layer and anything that depends on it. Rebuild only what is invalid, then compose the current Hot Context from the reusable and rebuilt layers.

This should apply to:

```text
Workshops
capabilities
Skills
Leaves
Task Sessions
reasoning state
model state
runtime adapters
future Tree components
```

---

# 21. Current Recommended Direction

For the immediate Phase 1 implementation:

```text
Forest TaskSessionManager
        ↓
tracks Task-Sticky Skill IDs
        ↓
HermesAdapter
        ↓
resolves Skill once
        ↓
builds Skill overlay once
        ↓
caches overlay for Task Session
        ↓
reapplies cached overlay on each relevant Hermes turn
```

Do not currently:

```text
replace Hermes base system prompt with a Skill prompt
```

Do not currently:

```text
modify or fork Hermes
```

Do not currently:

```text
rebuild Skill prompts every turn
```

Instead:

```text
Forest owns semantic stickiness.
Hermes owns runtime execution.
The adapter bridges the two.
```

---

# 22. Summary

The newest testing revealed two major things.

First, Hermes' session and caching architecture is useful and confirms that **reuse-or-rebuild** is a strong pattern.

Second, a Forest Skill should not be treated as Hermes' entire persisted system prompt.

The better design is a layered Task Session:

```text
stable base
+
Workshop
+
active capabilities
+
Task-Sticky Skills
+
relevant Leaves
+
conversation/task state
+
current turn
```

The Forest should cache and reuse those semantic layers independently, invalidate only what changes, and let each runtime adapter translate the resulting Hot Context into the runtime's native execution model.

This preserves:

```text
speed
portability
modularity
Task-Sticky behavior
runtime independence
future model/runtime replacement
```
