# The Forest — Core Design Doctrine: Seasons, Spirit, Progressive Depth, and Human-Centered AI

**Status:** HIGH PRIORITY / 100% IMPORTANT  
**Captured:** 2026-08-09  
**Purpose:** Preserve the core UX, architecture, lifecycle, permissions, observability, and philosophy decisions discussed for The Forest so later implementation does not lose the intent behind the system.

---

## 1. North Star

**The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**

The Forest should fit the user in two ways:

1. **Their lifestyle and needs**
2. **Their technical level**

A user should not need to know Linux, terminals, coding, token limits, context windows, model sizes, quantization, tool schemas, runtime services, prompt limits, or orchestration systems to get a powerful, competent, low-resource local AI system.

At the same time, the Forest must remain fully inspectable and controllable for expert users.

> **Complexity should be discoverable, not prerequisite.**

> **The Forest gets deeper as you wonder.**

Curiosity should be the navigation system.

---

## 2. Progressive Technical Legibility

The Forest should use the same language at every technical level. A casual user should not learn fake beginner terminology that must later be abandoned. Instead, the same Forest concepts should gain deeper technical meaning as the user investigates.

Example:

- Casual user: “This Tree is shedding Leaves.”
- Power user: “This Tree is unloading less-used context.”
- Developer: “The lifecycle manager is evicting low-priority context/capabilities from the hot runtime state.”

All three descriptions refer to the same real operation.

> **Every visible Forest metaphor should become more informative—not less accurate—the deeper a user investigates it.**

---

## 3. Forest Metaphors Must Map to Real Operations

Forest terminology must never be decorative-only.

If the Tree says it is:

- **Shedding** — something should really be leaving active state/context.
- **Dormant** — something should really be minimally retained / inactive.
- **Raking Leaves** — unnecessary or loose context should really be pruned/collected.
- **Pruning** — capabilities, memories, branches, or behavior should genuinely be constrained or cleaned.
- **Spring cleaning** — stored state should really be reviewed, cleaned, and selectively restored/rebuilt.
- **Growing** — the Tree should actually be gaining useful knowledge, procedures, capabilities, or quality from interaction/training.
- **Bearing fruit** — meaningful outputs, artifacts, procedures, knowledge, or reusable work should be produced.

A technical user inspecting the implementation should be able to recognize the real AI/software mechanism behind the Forest action.

---

## 4. Seasonal Lifecycle Language

The user-facing lifecycle should use seasons.

### 🌞 Summer — Growing

**Primary meaning:** Active, growing, readily available.

Summer represents work that is actively in use. Frequently needed capabilities, tools, context, Leaves, Workshops, and Skills can remain readily available.

Technical mapping may include active Tasks, hot context, frequently used capabilities, current Workshops, model-visible Leaves, and active runtime sessions.

### 🍂 Fall — Shedding

**Primary meaning:** Shedding.

Fall is the transition away from active use. The Forest begins dropping things that are no longer needed while keeping likely-to-return pieces nearby.

This is especially useful when a Task shift is uncertain. If a user moves from coding to homework or customer support, Forest does not need to instantly destroy the coding state. The coding Task can enter Fall, less-used coding tools/context can shed, and commonly reused pieces can remain cheap to restore.

### ❄️ Winter — Dormant

**Primary meaning:** Dormant.

Winter means the work is no longer active and should consume minimal runtime/context resources.

Winter does **not** initially mean permanent deletion. During the transition period while Forest still depends on Hermes, Winter can mean dormant, minimally retained, recoverable, with runtime sessions possibly preserved.

Later, after Forest-owned archival/reconstruction is mature, Winter can increasingly mean Forest owns the durable state and runtime state is disposable. The user-facing meaning does not need to change as the architecture matures.

### 🌱 Spring — Cleaning

**Primary meaning shown FIRST:** **Cleaning**

Whenever Spring is described in UI, documentation, tooltips, menus, hover text, or help, **Cleaning must be listed first**.

This is intentional so the reader naturally forms the connection:

> **Spring → Cleaning → Spring Cleaning**

Other Spring jobs may include reviewing, selectively restoring, rebuilding, reactivating, and deciding what survived Winter and still deserves to return.

The actual execution order does not need to be “clean first.” The user-facing description should still lead with **Cleaning**.

Recommended short labels:

- 🌞 **Summer — Growing**
- 🍂 **Fall — Shedding**
- ❄️ **Winter — Dormant**
- 🌱 **Spring — Cleaning**

The analogy should stay simple. People already understand how seasons affect real leaves and trees; their understanding of nature can fill in the gaps.

---

## 5. Lifecycle Applies Below the Task Level

Seasonal state should eventually apply not only to Tasks, but to components inside Tasks:

- Task
- Workshop
- capability/tool
- Skill
- Leaf/context bundle
- runtime session
- branch/project area

A Task itself can be in Fall while `file` and `terminal` remain in Summer, `debugging` is in Fall, and `testing` is in Winter. This allows selective restoration instead of reloading an entire old Task wholesale.

---

## 6. Layered Reuse and Selective Rebuild

The seasonal lifecycle should directly support **Layered Reuse and Selective Rebuild**.

A Task can cool without disappearing. When the user returns, Spring does not blindly reload everything that existed before. Instead it asks:

- What is still useful?
- What was frequently used?
- What should remain dormant?
- What should be rebuilt?
- What context/Leaves are still relevant?
- Which tools or Skills should return immediately?
- Which should stay put away?

This is a core performance strategy as well as a UX metaphor.

---

## 7. Part 5 as the Bridge to Part 4

The lifecycle policy originally described as “Part 5” should be implemented now as an intermediate architecture.

### Part 5 = mechanism

Part 5 provides lifecycle states, runtime-session retirement, recent-Task/resume tracking, seasonal residency behavior, usage frequency / last-used information, selective Workshop/capability reactivation, cleanup policy, disposal/recovery hooks, and runtime lineage such as `previous_session_id`.

### Part 4 = eventual ownership model

Part 4 is the mature state where:

> **Forest keeps the memory of the work. The runtime keeps only what it needs to perform the work efficiently.**

Forest eventually owns durable Task records, Leaves, decisions, outputs, operational learning, summaries, relevant context, artifacts, and reconstruction data.

Hermes becomes a working runtime copy, not a second permanent source of truth.

> **Part 5 is the mechanism. Part 4 is the eventual ownership policy.**

Part 5 should not be thrown away later. It becomes the skeleton that Part 4 grows into.

---

## 8. Avoid Two Permanent Copies of the Same Conversation

Long-term, Forest and Hermes should not both permanently store equivalent conversation state as equal sources of truth.

Preferred model:

```text
THE FOREST
  canonical / durable information
        ↓
select useful working context
        ↓
Hermes or another runtime
  temporary working conversation/cache
```

Hermes should eventually be disposable once Forest has safely retained what needs to survive. During the transition, Hermes sessions may remain recoverable because Forest does not yet have all required archival/reconstruction components.

---

## 9. Highly Configurable Without Requiring Configuration

> **The Forest should be highly configurable without requiring the user to configure it.**

A casual user should not need to manually set toolsets, reasoning level, prompt limits, context limits, tokens, runtime services, model selection, cache settings, Workshop combinations, Skill activation, or routing rules.

The system should make competent automatic choices. Power users should still be able to inspect and override those choices.

---

## 10. Automatic Reasoning, Tool Selection, and Escalation

Users should not normally need to tell a Tree to “think harder.” The Tree should infer the needed effort level and capabilities.

Expected escalation behavior:

```text
Try normally
    ↓
Use better-fitting Workshop/Skill
    ↓
Increase reasoning effort if needed
    ↓
Use another permitted tool
    ↓
Retrieve relevant Leaves
    ↓
Escalate model if appropriate
    ↓
Still blocked?
    ↓
Ask the user only for information, permission, judgment, or physical action actually required
```

The user should not become the orchestration engine. Manual controls should exist as overrides, not prerequisites for competent operation.

---

## 11. Spirit and Tools Menu Philosophy

Spirit and the Tools menu exist partly to bridge casual and advanced use.

The Tree should remain the intelligent actor. Spirit should be the deterministic control/authority layer.

> **Trees decide what would be useful. Spirit decides what is allowed.**

Trees can reason creatively. Spirit should enforce permissions, protected data rules, action boundaries, external publication restrictions, security controls, safety boundaries, and deterministic capability authorization.

The Tree/model should never be the final authority on whether it is allowed to expose banking information, secrets, IP addresses, API credentials, or other protected information.

---

## 12. Permissions Without Permission Fatigue

The Forest needs strong definitive permissions without forcing users through a “Bible-sized” permission interface or constant approval prompts.

A casual permission view might say:

```text
Maple can:
✓ Work with my projects
✓ Browse the web
✓ Help with personal files

Maple cannot:
✗ Access banking
✗ Publish publicly without permission
✗ Change Forest security
```

Advanced users can inspect the precise capability/path/network rules underneath. This is progressive technical legibility applied to security.

---

## 13. Tools Menu as the Bridge Behind the Curtain

The Tools menu / Spirit tools should let curious users progressively inspect the system.

A casual user may only interact with Trees. A curious user can discover status, Map, Compass, permissions, lifecycle/seasons, diagnostics, recovery, and emergency controls.

A power user can inspect active tools, Workshops, reasoning level, model, Leaves, and runtime state.

A developer can inspect runtime adapters, session IDs, context composition, token usage, caches, latency, routing decisions, permissions rules, and model configuration.

There should be no abrupt switch between “beginner mode” and “developer mode.” The same Forest becomes deeper as the user investigates.

---

## 14. “The Forest Gets Deeper as You Wonder”

This is a core UX and architecture principle.

A user should be able to start with a simple observation:

> “Bristlecone went into Winter.”

Then wonder “Why?” and progressively discover:

1. The Task stopped being used.
2. It entered Fall first.
3. Low-use context/tools were shed.
4. Remaining state became dormant.
5. Runtime/session/cache details can be inspected.
6. A developer can inspect exact timestamps, IDs, context residency, routing decisions, model state, and code.

Curiosity reveals depth. The Forest should reward investigation rather than require prior expertise.

---

## 15. Forest Behavior Is Also Observability

The visible behavior of the ecosystem should carry real diagnostic information. A user can learn to “read the Forest” like a real-world forest expert reads environmental signs.

### Tree enters Winter at an unusual time

Possible deeper meanings: Task detection issue, aggressive cooling, runtime interruption, lifecycle bug, or context/routing mistake.

### Simple request produces an unusual number of Leaves

Possible deeper meanings: retrieval fan-out too broad, Workshop loading excessive context, routing/relevance bug, context pressure, or unexpected memory generation.

### Capability repeatedly goes Summer → Fall → Summer

Possible deeper meanings: uncertain router, tool-selection oscillation, or a capability being unloaded too aggressively.

### Branch constantly needs pruning

Possible deeper meanings: over-retention, poor relevance scoring, or stale context accumulation.

### Tree takes unusually long to bear fruit

Possible deeper meanings: deeper reasoning, model escalation, tool retries, cache miss, runtime issue, or larger context rebuild.

### Spring repeatedly restores Leaves that are immediately shed

Possible deeper meaning: reconstruction/relevance policy needs tuning.

The nature metaphor therefore becomes part of the observability system.

---

## 16. Casual Users and Forest Experts Share the Same Signs

Casual user:

> “This Tree keeps dropping a lot of Leaves when I ask about homework.”

Power user:

> “Retrieval is probably pulling too much context.”

Developer:

> “Retrieval fan-out or context composition is abnormal; inspect Leaf sources and lifecycle state.”

Same sign. Deeper interpretation.

The Forest should allow users to become “Forest experts” naturally over time by observing patterns.

---

## 17. Help the Tree as the Tree Helps You

The interaction should feel reciprocal.

Users water, rake, prune, plant, clean, care for Trees, and help them grow.

Trees assist, learn, organize, work, reason, create, and produce useful fruit.

The user should not feel like they are administering an AI stack. They should feel like they are tending an ecosystem that helps them in return.

---

## 18. Low-Resource AI Should Not Require Expert Knowledge

A major Forest goal is to make efficient local AI accessible without requiring users to understand why low-resource AI systems are difficult.

The user should not need to manually manage multiple stacking applications/services, runtime dependencies, model selection, model speed/quality tradeoffs, prompt/context limits, cache state, tool schemas, reasoning settings, service startup, or orchestration logic.

Those systems can exist underneath. The Forest should translate their behavior into understandable ecosystem signs and competent automatic behavior.

---

## 19. Core UX Tests for Future Features

Before adopting a new Forest metaphor or feature, ask:

### Casual understanding
Could someone who knows nothing about AI make a reasonable decision from the Forest language alone?

### Technical truth
If an expert opens the details, will they find the real technical mechanism rather than a fake simplified abstraction?

### Metaphor integrity
Does the nature metaphor correspond to a meaningful system operation?

### Deeper as you wonder
Does investigating this feature reveal progressively more useful and accurate information?

If the answer to all four is yes, the design probably belongs in The Forest.

---

## 20. Terminology Rules to Preserve

### Seasons

- **Summer — Growing**
- **Fall — Shedding**
- **Winter — Dormant**
- **Spring — Cleaning**

**Spring must always list Cleaning first in user-facing descriptions.**

### Data / context language

- Leaves should remain understandable as knowledge/context pieces.
- Raking Leaves should correspond to context cleanup/pruning.
- Pruning should correspond to meaningful restriction/cleanup.
- Roots should correspond to underlying sources/dependencies/relationships when used.
- Fruit should correspond to useful outputs/results/artifacts/learned value.

### System ownership

- Forest = durable identity, policy, lifecycle, knowledge, permissions, routing, learning
- Spirit = deterministic authority/control
- Tree = intelligent actor
- Runtime adapter = translation/execution boundary
- Hermes = current runtime, increasingly disposable over time

---

## 21. Architectural Direction

```text
                         USER
                          │
                     natural work
                          │
                          ▼
                         TREE
                  intelligent decisions
                          │
                          ▼
                        SPIRIT
              deterministic authority/policy
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Permissions     Routing      Safety
             │            │            │
             └────────────┼────────────┘
                          ▼
                    Forest Lifecycle
       Summer / Fall / Winter / Spring Cleaning
                          │
                          ▼
              Selective activation/rebuild
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     Workshops         Skills            Leaves
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                    Runtime Adapter
                          │
                    Hermes today
                          │
              other runtimes tomorrow
```

---

## 22. Final Principle

The Forest should feel simple without being simplistic.

A person should be able to use it as:

> “Fun little Trees I ask to help me.”

And another person should be able to inspect the same system as:

> “A local-first, permissioned, multi-model, lifecycle-aware AI orchestration system with selective context residency, durable knowledge, automatic tool/reasoning routing, and runtime-independent state.”

Both users should be correct.
