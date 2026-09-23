---
type: architecture-concept
tree:
project: The Forest
status: active-reference
tags:
  - the-forest
  - Trees
  - architecture
  - AI
updated: 2026-08-08
---
# The Forest — Workshops + Quick / Normal / Deep Quick Draft

**Status:** Early architecture draft  
**Purpose:** Define how Workshops and Quick/Normal/Deep should work together before Phase 2 benchmarking.

## Core Idea

> **Workshop = What kind of work are we doing?**  
> **Mode = How much effort should the Tree spend doing it?**

They should remain separate and combine.

```text
Code Workshop + Quick
→ simple edit, minimal tools, low reasoning, narrow context

Code Workshop + Normal
→ everyday coding/debugging, standard tools, normal verification

Code Workshop + Deep
→ architecture/refactor/hard debugging, broader retrieval,
  more reasoning, more verification
```

Deep should not mean “turn every tool on.”

## What Each Control Decides

| Control | Primarily controls |
|---|---|
| **Workshop** | Tools, Skills, Soil capabilities, task-specific instructions, retrieval sources |
| **Quick / Normal / Deep** | Reasoning effort, context budget, retrieval depth, verification, number of passes |

Workshops largely decide **which Skills are relevant**. Modes decide **how deeply they are used**.

## Initial Bristlecone Workshops

### Everyday Workshop
General Bristlecone interaction that does not clearly belong elsewhere.

Possible capabilities:
- clarify
- memory/context
- light file access
- possibly session search

Use cases:
- planning
- Forest architecture discussion
- project questions
- organizing work
- continuity

Likely default Workshop.

### Code Workshop
For modifying, understanding, and reviewing code.

Likely tools:
- file
- terminal
- clarify
- code_execution

Possible Skills:
- systematic-debugging
- test-driven-development
- simplify-code
- requesting-code-review
- opencode

Future:
- source-context targeting / React Grab-like UI-to-source mapping

### System Workshop
For Linux, Qubes, services, runtimes, hardware, and Forest infrastructure.

Likely tools:
- terminal
- file
- clarify
- possibly memory/context

Use cases:
- systemctl
- Qubes configuration
- Ollama
- llama.cpp
- Forest Runtime Manager
- networking/service debugging

Should use stricter permissions for dom0, services, networking, permissions, and destructive actions.

### Debug Workshop
For structured troubleshooting.

```text
error
↓
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

Likely tools:
- file
- terminal
- code_execution
- clarify

Possible Skills:
- systematic-debugging
- python-debugpy
- node-inspect-debugger

### Research Workshop
For research, comparisons, and evidence gathering.

Likely capabilities:
- web
- session_search
- memory
- clarify
- possibly file

Future:
- RAG
- Leaf Foliage
- grounded citations

### Memory / Retrieval Workshop
For finding relevant knowledge rather than performing the main user task.

Possible capabilities:
- Leaf search
- metadata
- links/backlinks
- RAG
- session search
- memory

May eventually function more like a Forest service than a user-facing Workshop.

### Model Development Workshop
For Bristlecone's Treewright work on models and Seeds.

Use cases:
- Seeds
- quantization
- evaluation
- training
- Ollama / llama.cpp
- benchmarking
- LoRA / QLoRA later

Possible Skills:
- evaluating-llms-harness
- llama-cpp
- weights-and-biases if retained
- future Hugging Face/model tooling

This should not be loaded for ordinary Forest tasks.

## Quick / Normal / Deep Across Workshops

```text
                QUICK      NORMAL       DEEP

Everyday          ○           ○           ○
Code              ○           ○           ○
System            ○           ○           ○
Debug             ○           ○           ○
Research          ○           ○           ○
Model Dev         ○           ○           ○
```

Examples:

```text
"tar this folder"
→ System Workshop + Quick

"Why did this Python test fail?"
→ Debug Workshop + Normal

"Redesign the Forest runtime architecture"
→ System/Architecture Workshop + Deep

"Compare llama.cpp caching strategies"
→ Model Development Workshop + Deep

"Change this button text"
→ Code Workshop + Quick
```

## Future Router

```text
User request
    ↓
What kind of task?
    ↓
WORKSHOP
    ↓
How difficult / risky?
    ↓
MODE
    ↓
Expose only required:
tools
Skills
Leaves
Soil capabilities
    ↓
Tree executes
```

Possible explicit overrides later:

```text
/quick
/normal
/deep
/workshop code
/workshop system
```

Exact syntax is undecided.

## Skill Categories

### Core Skills
Fundamental/lightweight Skills Bristlecone should always know exist.

### Workshop Skills
Skills exposed primarily when a particular Workshop is active.

### On-Demand Skills
Not placed in the main working context until the router or Tree determines they are needed.

> **Workshop determines WHICH Skills are relevant.**  
> **Mode determines HOW DEEPLY they are used.**

## Phase 2 Benchmarking Rule

Do not blindly benchmark random tool combinations.

First define:
1. Workshop purpose
2. likely core tools
3. likely Skills
4. Soil capabilities
5. Quick / Normal / Deep behavior inside the Workshop

Then benchmark real candidate configurations:

```text
Code Workshop / Normal
→ X input tokens
→ Y seconds

System Workshop / Normal
→ X input tokens
→ Y seconds

Everyday Workshop / Normal
→ X input tokens
→ Y seconds
```

Then later:

```text
Code / Quick
Code / Normal
Code / Deep
```

## Current Working Principle

> **Workshop controls capability.**  
> **Mode controls effort.**  
> **Router chooses both.**
