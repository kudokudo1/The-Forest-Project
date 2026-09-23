# Bristlecone Pine — Workshops, Reasoning Modes, Model Forms, and Optimization Plan

**Status:** Working architecture / continuity note  
**Created:** 2026-08-08  
**Purpose:** Preserve the current Bristlecone optimization plan, the three independent execution controls, the planned larger-model Bristlecone form, and concepts that were considered but rejected or reframed.

---

## 1. Current Goal

Bristlecone Pine is being optimized to be as fast and efficient as practical for his normal Treewright work without unnecessarily reducing his usefulness.

The current optimization strategy is to avoid exposing Bristlecone to every possible tool, Skill, retrieval source, and reasoning budget on every request.

Instead, execution is divided into independent controls:

1. **Reasoning Mode** — how much reasoning effort Bristlecone should use.
2. **Workshop** — which tools/capabilities are relevant to the current job.
3. **Model Form** — which underlying model is powering Bristlecone.

These controls should remain independent so they can be freely combined.

---

# 2. Settled Three-Axis Architecture

## Axis A — Reasoning Mode

Reasoning Mode controls **how much effort Bristlecone spends thinking**.

Current conceptual levels:

- **Light / Quick** — low reasoning effort for straightforward work.
- **Normal** — normal reasoning and verification for everyday work.
- **Deep** — increased reasoning, context use, verification, and/or multiple passes for difficult work.

The exact name of the lowest level should remain consistent with whichever naming is ultimately implemented. Earlier notes used **Quick / Normal / Deep**; recent discussion also used **Light / Normal / Deep**.

Reasoning Mode does **not** decide which tools are available and does **not** decide which model is running.

Examples:

```text
Light / Coding / Small
Deep / Coding / Small
Normal / Coding / Big
Deep / Coding / Big
```

---

## Axis B — Workshop

A Workshop determines:

> **What kind of work are we doing, and what capabilities should Bristlecone see?**

Workshops primarily control:

- tool exposure
- Skill exposure
- Soil capabilities
- task-specific instructions
- retrieval sources
- relevant context sources

Core principle:

> **Do not expose a tool merely because it might occasionally be useful.**

Capabilities that are only occasionally needed should preferably be unlocked on demand rather than permanently loaded into the Workshop context.

### Current Candidate Workshops

#### 1. Treewright / Design Workshop

For:

- Forest architecture
- project planning
- feature design
- implementation discussion
- organizing development work
- project continuity
- conceptual review

This may be Bristlecone's lightest and fastest Workshop.

Likely core capabilities:

- minimal context
- memory/relevant project context
- clarification when necessary

Possible on-demand capabilities:

- file access
- session retrieval
- Leaf Foliage retrieval

---

#### 2. Coding Workshop

For:

- writing code
- modifying code
- understanding code
- code review
- simple implementation tasks

Likely minimal core:

```text
file
terminal
```

Possible on-demand additions:

- code execution
- specialized Skills
- testing/review procedures

Important benchmark clue from the current Bristlecone setup:

```text
file + terminal
≈ 41 seconds
```

This was dramatically faster than previously tested configurations that exposed additional Skills/tools.

Therefore, `file + terminal` is an important candidate baseline for Coding Workshop benchmarking.

---

#### 3. System Workshop

For:

- Linux
- Qubes
- services
- Hermes
- Ollama
- llama.cpp
- Forest Runtime Manager
- resource configuration
- hardware/runtime troubleshooting
- networking/service work

Likely minimal core:

```text
terminal
file
```

Possible on-demand additions:

- relevant memory/context
- system-specific Skills

System Workshop should use stricter safety/verification rules for:

- dom0
- destructive commands
- permissions
- networking
- service modifications
- security-sensitive changes

---

#### 4. Research Workshop

For:

- external research
- comparisons
- evidence gathering
- current information
- technical research

Possible capabilities:

- web/search
- session retrieval
- memory
- Leaf retrieval
- file access when relevant
- grounded citations/RAG later

Research should remain isolated from ordinary work so web/retrieval capabilities do not burden tasks that do not need them.

---

#### 5. Model Lab / Model Development Workshop

For Bristlecone's specialized Treewright work involving AI models and Seeds.

Examples:

- model evaluation
- quantization
- benchmarking
- model runtime testing
- Ollama
- llama.cpp
- Seeds
- training
- future LoRA / QLoRA
- future Hugging Face tooling

This Workshop may be relatively heavy.

That is acceptable because it should **not be loaded during normal Forest tasks**.

Likely core:

```text
file
terminal
```

Specialized capabilities should be added only when relevant.

---

# 3. Procedures Are Not Necessarily Workshops

Some concepts initially appeared as separate Workshops but were reconsidered.

## Debugging

Debugging should probably be a **procedure layered onto the relevant Workshop**, rather than a separate permanent Workshop.

Example:

```text
Coding Workshop
+ Debug Procedure
+ Normal Reasoning
```

or:

```text
System Workshop
+ Debug Procedure
+ Deep Reasoning
```

Suggested debugging loop:

```text
inspect evidence
↓
form hypothesis
↓
test
↓
observe
↓
repeat
```

This avoids duplicating nearly identical tool sets between Coding, System, and Debug Workshops.

Other future procedures could include:

- review
- testing
- verification
- architecture review

---

# 4. Shared Services Are Not Necessarily Workshops

## Memory / Retrieval

Memory and retrieval were initially considered as their own Workshop.

The preferred direction is now to treat them more like **shared Forest services**.

Possible shared services:

- Leaf Foliage retrieval
- session retrieval
- memory retrieval
- metadata lookup
- backlinks/links
- RAG
- Skill discovery

Example:

```text
Coding Workshop
      │
      └── asks retrieval service for relevant project Leaves

System Workshop
      │
      └── asks retrieval service for current Qubes configuration
```

The Workshop should receive only the relevant retrieved information instead of loading the whole knowledge system.

---

# 5. Model Form — Small vs Big

A third axis is planned in addition to Reasoning Mode and Workshop.

This axis changes the **underlying model**, not the reasoning level or tools.

Current conceptual names:

- **Small**
- **Big**

Possible Forest/UI metaphor:

- **Windowed**
- **Fullscreen**

The important concept is the separation, not the final naming.

## Small / Windowed Bristlecone

Purpose:

- daily driver
- low latency
- lower memory footprint
- everyday Treewright work
- common Coding/System tasks
- normal operation

This is the **current Bristlecone** that should be optimized first.

---

## Big / Fullscreen Bristlecone

Purpose:

- stronger reviewer
- difficult debugging
- architecture review
- complex code review
- difficult model-development decisions
- escalation when Small Bristlecone is uncertain or repeatedly failing

Big Bristlecone should normally remain unloaded when not needed.

Big does **not** automatically mean Deep reasoning.

Valid states include:

```text
Light / Coding / Big
Normal / Coding / Big
Deep / Coding / Big
```

Likewise, Small Bristlecone can use Deep reasoning:

```text
Deep / Coding / Small
```

Therefore:

> **Model size/capability and reasoning effort must remain separate controls.**

---

# 6. Bristlecone Execution State

The complete execution state should eventually be representable as:

```text
Reasoning / Workshop / Model Form
```

Examples:

```text
Light  / Coding   / Small
Normal / Coding   / Small
Deep   / Coding   / Small

Light  / Coding   / Big
Normal / Coding   / Big
Deep   / Coding   / Big

Normal / System   / Small
Deep   / System   / Big

Normal / Research / Small
Deep   / Model Lab / Big
```

Each axis answers a different question:

| Axis | Question |
|---|---|
| Reasoning Mode | How hard should Bristlecone think? |
| Workshop | What tools/capabilities should Bristlecone have? |
| Model Form | Which underlying model should power Bristlecone? |

---

# 7. Immediate Implementation Plan

## Phase 1 — Finish Current/Small Bristlecone First

Do **not** implement Big Bristlecone yet.

First finish a clean optimized baseline for the current model.

### Step 1 — Finalize Workshop Definitions

For each Workshop determine:

1. actual jobs Bristlecone performs
2. absolutely required tools
3. merely convenient tools
4. Skills that should always be present
5. Skills that should be on-demand
6. retrieval sources required
7. Soil capabilities required
8. safety/permission requirements

Avoid random tool combinations.

---

### Step 2 — Define Minimal Candidate Tool Sets

Start from the smallest credible set.

Examples:

```text
Coding:
file + terminal

System:
terminal + file

Treewright/Design:
minimal or no active tools when possible
```

Additional capabilities should be justified by real tasks.

---

### Step 3 — Benchmark Workshops

Benchmark realistic Workshop configurations instead of arbitrary combinations.

Record at minimum:

- time to first useful output
- total completion time
- prompt/input tokens
- tool schema size
- system prompt size
- correctness
- tool-call accuracy
- unnecessary tool calls
- failures
- RAM usage
- CPU usage
- perceived usefulness

Candidate tests:

```text
Coding / Normal
System / Normal
Treewright / Normal
Research / Normal
Model Lab / Normal
```

Then compare reasoning modes:

```text
Coding / Light
Coding / Normal
Coding / Deep
```

and repeat for other important Workshops.

---

### Step 4 — Implement Workshop Routing

The router should make a **small classification decision**.

It should not need to load every tool schema in order to choose a Workshop.

Concept:

```text
User request
    ↓
tiny task/router description
    ↓
choose Workshop
    ↓
load only that Workshop's capabilities
    ↓
Bristlecone executes
```

The router should know short Workshop descriptions, not entire tool catalogs.

---

### Step 5 — Make Workshops Sticky

Do not reroute every message when the user is clearly continuing the same task.

Example:

```text
System Workshop active
↓
check service
↓
inspect logs
↓
try fix
↓
verify
```

Remain in System Workshop until a meaningful task boundary occurs.

This may reduce routing overhead and improve continuity.

---

### Step 6 — Add Progressive Capability Exposure

Within a Workshop, begin with the smallest core tool set.

Example:

```text
Coding Workshop

Start:
file + terminal

Need more?
↓
unlock code execution

Need specialized help?
↓
unlock relevant Skill
```

The goal is to avoid paying the context/tool-selection cost for capabilities that are not needed.

---

### Step 7 — Tune Light / Normal / Deep

After Workshop tool sets are stable, benchmark and tune the reasoning axis.

Reasoning should alter things such as:

- reasoning effort
- context budget
- retrieval depth
- verification
- number of passes

It should **not automatically expose unrelated tools**.

Important rule:

> **Deep does not mean “turn everything on.”**

---

### Step 8 — Establish the Small Bristlecone Baseline

Before adding Big Bristlecone, preserve:

- final Workshop configuration
- reasoning behavior
- benchmark suite
- benchmark results
- prompt sizes
- tool schema sizes
- RAM/CPU measurements
- known weaknesses
- known strong tasks

This becomes the control/baseline for future comparisons.

---

# 8. Phase 2 — Implement Big / Fullscreen Bristlecone

Only after Small Bristlecone is stable.

## Step 1 — Select Candidate Larger Model

Evaluate models specifically for Bristlecone's Treewright role.

Priorities include:

- coding ability
- Linux/system reasoning
- tool calling
- architecture/reasoning
- structured instruction following
- long-context behavior
- latency
- memory requirements
- compatibility with local hardware/runtime
- quantization options

Do not choose only by generic benchmark rankings.

---

## Step 2 — Install Alongside Small Bristlecone

Do not replace Small Bristlecone.

Concept:

```text
Bristlecone Pine
├── Small model
└── Big model
```

Both should be available so they can be benchmarked and used independently.

---

## Step 3 — Preserve the Tree Identity

Bristlecone's identity should belong to the Tree, not the model.

Shared Tree-level components may include:

- Treewright role
- Forest terminology
- Workshops
- reasoning modes
- Skills
- Leaves
- permissions
- procedures
- project context
- behavioral instructions

The underlying model becomes a replaceable reasoning engine.

---

## Step 4 — Model-Specific Adaptation

Different model families may require adjustments to:

- prompt format
- system instructions
- tool calling configuration
- context limits
- reasoning controls
- quantization
- Ollama/llama.cpp settings

These are adapter/tuning changes, not a redesign of Bristlecone.

---

## Step 5 — Benchmark Small vs Big Using the Same Suite

Run the same real tasks through both models.

Compare:

- speed
- correctness
- reliability
- tool use
- reasoning
- RAM
- CPU
- context behavior
- failures

This makes the larger model an evidence-based addition.

---

## Step 6 — Add Manual Escalation First

Initial behavior should allow explicit switching:

```text
Deep / Coding / Small
        ↓
Deep / Coding / Big
```

Workshop and reasoning state remain unchanged.

Only the underlying model changes.

---

## Step 7 — Consider Automatic Escalation Later

Possible escalation signals:

- repeated failed hypotheses
- low confidence
- difficult multi-file debugging
- unresolved contradiction
- high-risk architectural decision
- Small model asks for review

Automatic escalation should come **after** manual switching is proven reliable.

---

# 9. Small-to-Big Handoff

Big Bristlecone should not automatically need the entire raw conversation.

Small Bristlecone could create a compact review packet:

```text
TASK
What are we trying to solve?

EVIDENCE
Relevant logs, files, outputs, and facts.

ACTIONS ALREADY TAKEN
What was tried?

CURRENT HYPOTHESIS
What does Small Bristlecone think is happening?

PROPOSED FIX
What does it recommend?

REVIEW QUESTION
What specifically should Big Bristlecone verify?
```

This reduces context cost for the larger model and creates a reusable Tree-to-Tree/model-to-model handoff pattern.

---

# 10. Connection to Potted Plants

The Small/Big architecture can also help test the Forest concept of **potted Plants**.

A Pot should not necessarily mean cloning an entire VM or copying everything associated with a Tree.

A Pot may instead be a bounded portable expression of a Tree.

Example:

```text
FULL BRISTLECONE
├── identity
├── all Workshops
├── all relevant Leaves
├── Skills
├── procedures
├── permissions
└── model/runtime configuration

        ↓ pot

BRISTLECONE DEBUG POT
├── Bristlecone identity
├── Coding Workshop
├── System Workshop
├── Debug procedure
├── selected Skills
├── selected Leaves
├── restricted permissions
└── chosen model
```

Possible future Pot types:

### Working Pot
Enough of a Tree to independently perform a bounded job.

### Knowledge Pot
Selected Leaves/context without necessarily carrying a dedicated model.

### Seedling Pot
A very small Tree expression with basic identity, limited knowledge, and lightweight capabilities.

### Reviewer Pot
A stronger bounded Bristlecone intended primarily to check difficult work.

The Big Bristlecone experiment may therefore serve as an early practical test of separating:

```text
Tree identity
from
underlying model
from
portable bounded Tree state
```

---

# 11. Rejected or Reframed Concepts

This section records ideas that should **not** be treated as the current plan unless deliberately reconsidered later.

## Rejected: Deep Mode Turns On Every Tool

Why rejected:

- reasoning effort and tool availability solve different problems
- loading unrelated tools increases context/tool-selection overhead
- Deep reasoning should mean more effort with the **appropriate** capabilities

Current rule:

> Workshop controls capability. Reasoning Mode controls effort.

---

## Rejected: Workshop Also Controls Reasoning

Why rejected:

A Coding task can be simple or extremely difficult.

Examples:

```text
Light / Coding
Deep / Coding
```

Therefore Coding cannot imply one fixed reasoning level.

Workshop and Reasoning Mode remain separate axes.

---

## Rejected: Model Size Is Another Reasoning Mode

Why rejected:

A larger model and deeper reasoning are not the same thing.

Valid combinations include:

```text
Deep / Coding / Small
Light / Coding / Big
```

Therefore model selection is a third independent axis.

---

## Rejected: Replace Small Bristlecone When a Better Model Is Found

Why rejected/reframed:

A stronger model can coexist with the optimized smaller Bristlecone.

Preferred direction:

```text
Bristlecone Pine
├── Small / Windowed form
└── Big / Fullscreen form
```

This preserves the fast daily driver while creating a stronger reviewer/escalation path.

---

## Rejected: Treat Small and Big as Completely Separate Trees

Why rejected:

The desired experiment is to determine whether Bristlecone's identity can remain stable while the underlying model changes.

Preferred model:

```text
one Bristlecone Tree identity
        ↓
multiple model forms
```

The model should eventually behave like a replaceable reasoning engine beneath the Tree.

---

## Reframed: Debug Workshop

Initial idea:

```text
Debug Workshop
```

Preferred direction:

```text
Coding Workshop + Debug procedure
System Workshop + Debug procedure
```

Reason:

Debugging uses many of the same tools as Coding or System work. Making Debug a procedure avoids duplicating tool bundles.

This remains open to benchmarking if a dedicated Debug Workshop later proves faster or more reliable.

---

## Reframed: Memory / Retrieval Workshop

Initial idea:

```text
Memory / Retrieval Workshop
```

Preferred direction:

Memory, Leaf Foliage, session search, and RAG should likely become shared retrieval services available to Workshops when needed.

Reason:

Retrieval is often supporting work rather than the user's primary task.

---

## Rejected: Load All Skills for Every Workshop

Why rejected:

Existing Bristlecone benchmarks showed substantial slowdown when Skill/tool schemas were added.

Preferred direction:

- lightweight core Skills where truly necessary
- Workshop-specific Skills
- on-demand Skill loading
- Skill discovery/retrieval rather than universal exposure

---

## Rejected: Random Tool-Combination Benchmarking as the Main Strategy

Why rejected:

Random combinations do not directly tell us whether a useful real-world Workshop is efficient.

Preferred sequence:

1. define Workshop purpose
2. define minimal required tools
3. define optional capabilities
4. define Skills
5. define reasoning behavior
6. benchmark realistic configurations

---

## Rejected: Router Must See Every Tool Definition

Why rejected:

If the routing step itself receives all tool schemas, the system pays much of the context cost before optimization even begins.

Preferred direction:

The router sees only compact Workshop/task descriptions and selects the capability profile before full tool schemas are exposed.

---

## Rejected: Reroute Every Message

Why rejected:

Long debugging/coding/system sessions often stay within the same task class.

Preferred direction:

Workshops should be **sticky** until a meaningful task boundary occurs.

---

## Rejected: A Potted Plant Is Merely a Full Clone

Why rejected/reframed:

A Pot should support carrying only bounded parts of a Tree relevant to a purpose.

Possible Pot contents can include selected:

- identity information
- Workshops
- Skills
- Leaves
- procedures
- permissions
- model/runtime configuration

A full clone can still exist, but it should not define the entire Pot concept.

---

# 12. Current Development Order

The agreed development order is:

```text
1. Configure and optimize current Small Bristlecone
        ↓
2. Finalize Workshops
        ↓
3. Benchmark minimal tool sets
        ↓
4. Implement routing / sticky Workshops / on-demand capabilities
        ↓
5. Tune Light/Normal/Deep reasoning behavior
        ↓
6. Freeze Small Bristlecone baseline
        ↓
7. Select and install Big Bristlecone model
        ↓
8. Adapt shared Tree identity to the larger model
        ↓
9. Benchmark Small vs Big
        ↓
10. Implement manual Small ↔ Big switching
        ↓
11. Test reviewer/handoff workflow
        ↓
12. Use the architecture to begin practical Potted Plant experiments
        ↓
13. Consider automatic escalation only after manual behavior is reliable
```

---

# 13. Core Design Principles to Preserve

1. **Workshop controls capability.**
2. **Reasoning Mode controls effort.**
3. **Model Form controls which model is running.**
4. These three controls remain independent.
5. Start with the smallest useful capability set.
6. Unlock optional capabilities only when justified.
7. Deep reasoning must not mean loading every tool.
8. Bristlecone's Tree identity should not be permanently tied to one model.
9. Small Bristlecone remains valuable even after Big Bristlecone exists.
10. Big Bristlecone is initially an escalation/reviewer path, not a replacement.
11. Benchmark real jobs, not arbitrary configurations.
12. Preserve a stable Small baseline before adding model complexity.
13. Treat retrieval and Skills as selectively supplied resources where practical.
14. Design the architecture so future model swaps do not require rebuilding the Tree.
15. Use the Small/Big experiment to test future bounded/Potted Plant concepts.

---

# 14. Immediate Next Step

Return to configuring the **current Small Bristlecone**.

The next design discussion should focus on the Workshops one at a time:

```text
What jobs does Bristlecone actually perform here?
↓
What tools are absolutely required?
↓
What tools are merely convenient?
↓
What should unlock only on demand?
↓
What Skills/context/retrieval are required?
↓
Benchmark the smallest credible configuration.
```

Recommended starting point:

**Treewright / Design Workshop** or **Coding Workshop**, followed by System Workshop.

Do not begin Big/Fullscreen implementation until the current Small Bristlecone has a stable, measured baseline.

---

## Short Architecture Summary

```text
                         BRISTLECONE PINE
                                │
                         TREE IDENTITY
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
       REASONING             WORKSHOP           MODEL FORM
     How hard think?       What tools?          Which model?
            │                   │                   │
     Light/Normal/Deep     Coding/System/...     Small / Big
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
                         TREE EXECUTION
                                │
                 shared/on-demand services
                                │
               Leaves / Memory / Skills / RAG
```

This is the current preferred Bristlecone architecture unless deliberately revised later.
