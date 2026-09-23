---
type: architecture-concept
tree: All
project: The Forest
source: Chat GPT+ User
status: active-reference
tags:
  - the-forest
  - architecture
  - Trees
  - software
  - Optimization
  - routing
  - Tool-management
  - skills-management
created: 2026-08-08
updated:
---
## The Forest — Workshop Fallback, Skill Finder, and Operational Learning Architecture

**Status:** Working architecture direction  
**Created:** 2026-08-08  
**Purpose:** Define how Trees remain lightweight through Prepared Workshops while retaining reliable access to their full Tree-owned capabilities when routing is uncertain, a Workshop is insufficient, or a needed Skill is hidden.

---

# 1. Core Goal

The Forest should optimize Trees aggressively without making them fragile.

Prepared Workshops should keep normal tasks fast by exposing only the smallest useful set of tools, Skills, context, and instructions.

However, a Tree must not become unable to complete a task simply because the correct capability is currently dormant or because the task was initially routed to the wrong Workshop.

Therefore, the Workshop system needs a fallback layer that allows the Tree to:

1. Extend its current Workshop when the Workshop is correct but incomplete.
2. Search its own dormant Skills and tools when it does not know what capability is needed.
3. Compare multiple Workshop profiles when task classification is ambiguous.
4. Temporarily expose its broader Tree-owned capability set as a last resort.
5. Log successful recovery paths so future routing improves.

---

# 2. Prepared Workshop Architecture

For Bristlecone Pine, the current planned Workshops are:

```text
RESEARCH
DESIGN
CODE / DEBUG
MODEL
```

Each Workshop exists as a **Prepared Workshop Profile** rather than being rebuilt from scratch every time.

Example:

```text
CODE / DEBUG

CORE
├── file
└── terminal

READY / DORMANT
├── exec
├── debug
├── test
├── clarify
└── specialized Skills/tools
```

Core capabilities are active immediately when the Workshop is selected.

Ready/Dormant capabilities belong to Bristlecone and are associated with that Workshop, but are not necessarily injected into the active model context until needed.

---

# 3. The Problem With Aggressive Optimization

A very small Workshop improves speed, but it introduces a possible failure mode:

```text
User gives debugging request
        ↓
Code/Debug loads only:
file + terminal
        ↓
Tree does not recognize that
debugging Skill is available
        ↓
Tree incorrectly concludes
it cannot complete the task
```

The Forest must prevent this.

Optimization should reduce unnecessary capability exposure without hiding capability so effectively that the Tree becomes less useful.

---

# 4. The Tool Shed / Skill Finder

The preferred solution is a lightweight **meta-layer** beneath the normal Workshops.

Possible Forest names:

- Tool Shed
- Skill Finder
- Capability Finder

This should **not** be treated as a fifth normal Workshop.

It is a fallback and discovery layer shared by a Tree's Workshops.

Concept:

```text
                    BRISTLECONE
                         │
               choose normal Workshop
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Research          Design         Code/Debug
        │                                 │
        └──────────── Model ──────────────┘
                         │
              capability insufficient?
                         ↓
                  TOOL SHED
                         │
            inspect/search Bristlecone's
             Tree-owned capabilities
```

The Tool Shed should remain lightweight.

It should preferably expose only:

- capability name
- short description
- owning/typical Workshop
- activation information
- optional usage/success statistics

It should **not** inject the full instructions for every Skill into the active prompt.

---

# 5. Capability Manifests

A Tree can know what Skills it owns without carrying every full Skill in context.

Example:

```text
AVAILABLE BRISTLECONE SKILLS

systematic-debugging
Structured troubleshooting and hypothesis testing.

test-driven-development
Create and use targeted tests.

code-review
Review implementation for correctness and maintainability.

model-evaluation
Evaluate model behavior and performance.
```

This lightweight manifest allows the Tree or runtime to recognize available capabilities cheaply.

The full Skill instructions are injected only when activated.

Core principle:

> **Owned by the Tree does not mean actively loaded into the model context.**

---

# 6. Extension vs Replacement

The runtime should distinguish two different situations.

## Extension

The current Workshop is correct, but it needs additional capability.

Example:

```text
Code/Debug
file + terminal
        ↓
Tree needs structured debugging
        ↓
activate debug Skill
```

The Workshop remains Code/Debug.

Its current state becomes:

```text
Code/Debug
├── file
├── terminal
└── debug [active/sticky]
```

## Replacement

The task itself has changed and the current Workshop is no longer appropriate.

Example:

```text
Code/Debug

"Research whether this is a known llama.cpp issue."
        ↓
Research Workshop
```

The old box is released and the new Prepared Workshop becomes active.

The Tree should ask conceptually:

> **Do I need more capability from this Workshop, or am I doing a different kind of job?**

---

# 7. Skill Activation States

Tree-owned Skills should support a lifecycle.

## Dormant

The Tree owns the Skill, but it is not injected into active context.

```text
debug → dormant
```

## Active

The Skill has been activated for the current task.

```text
debug → active
```

## Sticky

The Skill remains active across related turns because it is still likely to be useful.

```text
debug → sticky
```

When the task clearly changes, it can return to dormant.

---

# 8. Sticky Skills and Capability Hysteresis

Skills should not repeatedly load and unload during a continuous task.

Bad behavior:

```text
load debug
drop debug
load debug
drop debug
```

Preferred behavior:

```text
DORMANT
   ↓ relevant
ACTIVE
   ↓ used
STICKY
   ↓
remain active while the same
task or Workshop continues
```

The threshold to **activate** a Skill can be lower than the threshold required to **drop** it.

This reduces capability thrashing.

Possible drop signals:

- Workshop changes
- clear task boundary
- several unrelated turns
- long inactivity
- context pressure
- explicit user request to stop/end task

Exact thresholds should be benchmarked later.

---

# 9. Proactive and Reactive Activation

There should be two activation paths.

## Proactive Activation — Fast Path

When the need is obvious before the main inference, the runtime can activate the relevant Skill immediately.

Example:

```text
"Run the tests and explain why they fail."
        ↓
Code/Debug selected
        ↓
testing capability recognized
        ↓
first inference receives:
file + terminal + test
```

This avoids an extra Tree round trip.

Preferred rule:

> **Predict when obvious.**

## Reactive Activation

Sometimes the need becomes clear only after the Tree starts working.

Example:

```text
file + terminal
        ↓
inspect project
        ↓
Tree discovers a specialized
capability is required
        ↓
activate capability
        ↓
continue task
```

This may require an extra step, but only when the requirement could not reasonably be predicted beforehand.

Preferred rule:

> **Reach into the box when necessary.**

---

# 10. Ambiguous Task Routing

Sometimes the Tree may not know which Workshop a request belongs to.

Instead of forcing an early choice, the runtime can compare the lightweight manifests of several Workshops.

Example:

```text
Incoming request
        ↓
Ambiguous

Possible:
Research
Design
Code/Debug
Model
```

The Tree/router should compare **small Workshop summaries**, not load all full Workshop tools and Skill instructions.

Example manifest:

```text
RESEARCH
External information, evidence, documentation, comparison.

DESIGN
Architecture, planning, conceptual design, system structure.

CODE/DEBUG
Implementation, files, terminal work, diagnosis, testing.

MODEL
Training, evaluation, quantization, inference, model runtime.
```

The likely Workshop can then be selected without paying the cost of fully activating all four.

---

# 11. Multi-Workshop Inspection

A Tree should be allowed to inspect several Workshop manifests at the same time when routing is uncertain.

Important distinction:

> **Inspect multiple boxes simultaneously; do not automatically fully open all boxes simultaneously.**

This preserves speed.

The Tree can compare the contents/labels of several boxes and open only the likely Workshop.

---

# 12. Full Fallback — Open Workbench

Optimization must have an escape hatch.

If normal routing and Skill discovery fail, the Tree may enter a temporary broad state:

## Open Workbench

The Open Workbench exposes a much larger portion of **that Tree's own capabilities**.

For Bristlecone:

```text
BRISTLECONE OPEN WORKBENCH

├── architecture Skills
├── coding Skills
├── debugging Skills
├── testing Skills
├── model-development Skills
├── permitted tools
├── retrieval capabilities
└── other Bristlecone-owned capabilities
```

This should **not** mean all capabilities in the entire Forest.

Bristlecone should not automatically receive Cedar's security-specialist Skills or Maple's unique organization Skills.

Tree specialization remains intact.

Open Workbench is a last resort, not the normal state.

---

# 13. Fallback Ladder

A useful recovery hierarchy is:

```text
LEVEL 0
Current Workshop Core
        ↓ insufficient

LEVEL 1
Current Workshop Ready/Dormant inventory
        ↓ insufficient

LEVEL 2
Search all Tree-owned Skill/tool manifests
        ↓ uncertain

LEVEL 3
Compare multiple Workshop manifests
        ↓ unresolved

LEVEL 4
Open Workbench
temporarily expose broad Tree-owned capability set
```

This allows the Tree to remain lightweight during normal work without becoming trapped by its optimization.

---

# 14. Operational Learning

The fallback system should log what happened.

This allows the Tree/Forest runtime to improve how it configures itself over time without retraining the underlying model.

Example:

```text
TASK PATTERN
service dies after startup

INITIAL WORKSHOP
Design

RECOVERY
Skill Finder

SUCCESSFUL WORKSHOP
Code/Debug

SUCCESSFUL SKILLS
debug

OUTCOME
resolved
```

When a similar request appears later, the runtime can use that history as evidence:

```text
service
startup
crash
logs
failure
        ↓
likely route:
Code/Debug + debug
```

The Tree becomes faster because it learns which Workshop and capabilities usually work for recurring task patterns.

---

# 15. Two Types of Tree Learning

The Forest should distinguish:

## Knowledge Learning

What the Tree learns **about the world, project, user, or system**.

Examples:

- Leaves
- project facts
- memories
- architecture decisions
- user context

## Operational Learning

What the Tree learns **about how to use itself**.

Examples:

- successful Workshop choices
- successful Skill combinations
- common fallback paths
- failed routes
- useful handoffs
- unnecessary capabilities
- task-to-Skill associations

This operational layer may improve speed and reliability without changing the Tree's underlying model weights.

---

# 16. Routing Memory

Operational learning can be stored in a lightweight routing history.

Concept:

```text
routing history

task pattern
→ initial Workshop
→ final successful Workshop
→ useful Skills
→ unnecessary Skills
→ outcome
```

This does not need to be a large semantic memory system initially.

It may begin as simple structured records and later become more sophisticated.

---

# 17. Skill Use Statistics

The Forest may later measure Skill usefulness.

Example:

```text
TASK TYPE: debugging

file        used 98%
terminal    used 92%
debug       used 81%
test        used 44%
exec        used 21%
research     used 7%
```

These statistics can help improve Prepared Workshop profiles.

Important:

A capability that is frequently useful for a specific recognizable task does not necessarily need to become permanent Workshop Core.

Instead:

```text
generic Code task
→ file + terminal

recognized debugging task
→ file + terminal + debug
```

This retains efficiency.

---

# 18. Workshop Self-Optimization

Usage history can support gradual Workshop tuning.

Possible decisions:

```text
READY capability used almost every task
        ↓
consider promoting to CORE
```

or:

```text
CORE capability rarely used
        ↓
consider moving to READY
```

These changes should be evidence-driven and benchmarked.

The system should avoid blindly expanding Workshop cores.

---

# 19. Tree-Owned Skills Remain Important

The Tool Shed should primarily search **the current Tree's own Skill library**.

The Forest should not collapse into a universal Skill pool where every Tree can trivially become every other Tree.

Example specialization:

```text
CHERRY
everyday assistant Skills
communication
planning
general help

MAPLE
organization
file/media transformation
handoffs
workspace tasks

BRISTLECONE
coding
debugging
architecture
model development

CEDAR
security
integrity
monitoring
recovery
```

Shared Forest infrastructure may still provide basic utilities such as:

- context
- memory transport
- basic file primitives
- handoff
- permissions
- Tree-to-Tree communication

Specialized Skills remain Tree-specific.

---

# 20. Why This Preserves the Multiple-Tree Vision

A global all-purpose agent architecture would allow every Tree to load nearly every specialized Skill.

That would reduce meaningful specialization.

The preferred Forest architecture is:

```text
Tree receives task
        ↓
Can this Tree handle it with
its own role/capabilities?
        │
       yes
        ↓
select Workshop
        ↓
extend if needed
```

If the work genuinely belongs to another Tree:

```text
delegate
```

Example:

```text
Cherry receives difficult debugging request
        ↓
understands the request
        ↓
delegates specialized work
        ↓
Bristlecone
Code/Debug Workshop
```

This keeps delegation meaningful.

---

# 21. Workshop + Skill Finder Architecture

The combined system becomes:

```text
                         TREE
                          │
                  Prepared Workshops
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
     Core              Ready             Sticky
   always on          dormant          currently held
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    task continues
                          │
             capability insufficient?
                          ↓
                    SKILL FINDER
                          │
               search Tree-owned manifests
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     extend current   switch Workshop   uncertain
          │               │               │
          └───────────────┼───────────────┘
                          ↓
                   OPEN WORKBENCH
                    last resort
                          │
                          ↓
                     log outcome
                          │
                          ↓
                 improve future routing
```

---

# 22. Bristlecone Example

User request:

```text
"Why does Hermes keep dying after startup?"
```

Possible first encounter:

```text
Router:
uncertain / Design

Design Core:
mem + clarify

Task cannot be solved efficiently
        ↓
Skill Finder
        ↓
Code/Debug identified
        ↓
Code/Debug Core:
file + terminal
        ↓
debug Skill activated
        ↓
task solved
        ↓
routing outcome logged
```

Future similar request:

```text
"Service crashes immediately after startup."
        ↓
routing memory recognizes pattern
        ↓
Code/Debug
        +
debug preactivated
```

The second experience is faster than the first.

---

# 23. Anti-Bloat Rule

The fallback system must not recreate the original performance problem.

Therefore:

> **Failure to find the right capability should expand visibility progressively, not immediately load every capability.**

Preferred order:

```text
smallest useful view
        ↓
slightly broader view
        ↓
Tree-wide manifest
        ↓
multi-Workshop manifest comparison
        ↓
full Tree-owned Workbench
```

Open Workbench is deliberately expensive and rare.

---

# 24. Relationship to Prepared Workshops

Prepared Workshops remain the normal execution mechanism.

The Tool Shed does not replace them.

Instead:

```text
Prepared Workshops
= fast normal path

Sticky Skills
= efficient task continuation

Skill Finder
= recovery/discovery path

Open Workbench
= reliability safety net

Operational Learning
= future routing improvement
```

---

# 25. Current Preferred Architecture Statement

> **A Tree should normally operate from a small Prepared Workshop, extend that Workshop using its own dormant Skills when needed, keep useful extensions sticky while the task continues, switch Workshops only when the nature of the job changes, and retain a lightweight Skill Finder plus full Tree-owned Workbench as recovery paths. Successful recovery paths should be logged so future routing can activate the correct Workshop and Skills earlier.**

This architecture is intended to maximize:

- speed
- capability
- specialization
- reliability
- graceful recovery
- long-term operational learning

without requiring every Tree to carry every capability in active context.

---

# 26. Implementation Direction

For Bristlecone Workshop v1:

```text
1. Build four Prepared Workshop profiles:
   - Research
   - Design
   - Code/Debug
   - Model

2. Define:
   - Core
   - Ready/Dormant
   - Active/Sticky

3. Build lightweight manifests for dormant capabilities.

4. Preserve current Workshop across related turns.

5. Add extension logic:
   current Workshop → dormant capability activation

6. Add Workshop replacement logic:
   task changes → select new prepared profile

7. Add Skill Finder fallback.

8. Add multi-Workshop manifest inspection for ambiguous tasks.

9. Add Open Workbench as last resort.

10. Log:
    - initial route
    - activated Skills
    - switches/fallbacks
    - final successful state
    - outcome

11. Use logs later to improve proactive routing and Skill activation.

12. Benchmark every layer so fallback reliability does not erase the speed benefits of lightweight Workshops.
```

---

# 27. Final Design Principle

The Forest should optimize for:

> **Fast when the task is familiar.  
> Flexible when the task is unusual.  
> Capable when routing fails.  
> Smarter about its own operation after each successful recovery.**

Prepared Workshops provide the fast path.

The Skill Finder and Open Workbench ensure optimization never becomes a cage.
