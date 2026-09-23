---
title: "Cherry Model Decision Record"
project: "The Forest"
tree: "Cherry"
document_type: "model-selection-decision-record"
status: "selected three-model bench; exact routing pending benchmark"
updated: "2026-08-12"
tags: [forest, cherry, models, model-selection, architecture]
---

# Cherry — Model Decision Record

## Executive decision

Cherry is The Forest’s warmest, most personal generalist and the user’s main entry point into the system. She must feel natural in conversation while also acting as a competent coordinator: using tools, retrieving memory, delegating to specialist Trees, and escalating only when a task really requires a stronger model.

The current decision is to retain **three models for Cherry’s benchmark** because they provide three genuinely different advantages:

| Model | Intended role | Status |
|---|---|---|
| **Liquid LFM2.5-2.6B** | Quick / Utility / agentic Cherry | **Selected for bench** |
| **Gemma 4 E4B** | General / multimodal / personality-capable Cherry | **Selected for bench** |
| **Ai2 OLMo 3 7B-Instruct** | Open / trainable / experimentation-focused Cherry | **Selected for bench** |

```text
Cherry
├── LFM2.5-2.6B
│   └── fast tools, routing, everyday agent work
├── Gemma 4 E4B
│   └── richer conversation, multimodality, stronger general reasoning
└── OLMo 3 7B-Instruct
    └── openness, future Cherry-specific training, research/control
```

The final production hierarchy is not frozen yet. Cherry is currently one of the few Trees allowed to challenge the Forest’s default two-core-model rule because each of the three models has a distinct role.

---

# 1. What Cherry must be good at

Cherry’s model requirements are not generic leaderboard requirements.

## Core responsibilities

- natural everyday conversation
- personal-assistant work
- reminders, calendar, scheduling, organization
- Forest navigation and delegation
- recognizing when Maple, Cedar, McIntosh, or Bristlecone is more appropriate
- selecting only the current task’s relevant Workshop/tools
- retrieving only relevant memory/Leaves
- preserving Cherry’s personality
- switching cleanly between playful/personal and serious/task-focused modes
- respecting Cherry Diary isolation
- escalating from lightweight reasoning to deeper reasoning only when useful

## Cherry-specific benchmark priorities

1. warmth and naturalness
2. personality consistency over long sessions
3. configurable mannerism/style control
4. serious-mode transitions
5. tool-call correctness
6. Tree-delegation judgment
7. Workshop selection discipline
8. memory retrieval discipline
9. Diary isolation/non-leakage
10. structured output
11. uncertainty handling
12. Small → deeper-model handoff
13. performance while other Trees are active

---

# 2. Selected model — LFM2.5-2.6B

Liquid describes LFM2.5-2.6B as a **2.6B dense on-device agentic model** with **128K context** and **native tool calling**.

## Why it survived

Its value is not maximum intelligence. Its value is making Cherry’s common work extremely cheap:

```text
user request
→ LFM2.5-2.6B
→ understand intent
→ choose Workshop / tool / Tree
→ finish routine task
→ release resources
```

### Strong fits

- very small
- agent-oriented
- tool calling
- structured output
- routing/classification
- local CPU/GPU deployment
- GGUF / llama.cpp / Ollama support
- enough context headroom for agent traces without requiring huge permanent context

### Likely jobs

- reminders
- basic organization
- quick summaries
- Tree routing
- simple tool calls
- light retrieval
- routine personal-assistant actions
- simple multi-step workflows

## Weaknesses / risks

- a 2.6B model may hit a judgment ceiling
- long-term personality stability is unknown
- subtle personal context may require escalation
- difficult planning may expose its size
- Liquid’s license is not plain Apache 2.0
- current Liquid licensing limits free commercial use to companies below a $10M annual-revenue threshold

## Decision

**Retained. Leading Quick/Utility Cherry candidate.**

---

# 3. Selected model — Gemma 4 E4B

E4B means **effective ~4B-class parameters**, not 4-bit quantization.

## Why it survived

Gemma 4 E4B combines:

- native system-role support
- native function/tool calling
- configurable thinking/reasoning
- image understanding
- audio understanding
- long context
- MTP/speculative-decoding support with a matching draft model
- local/open-weight deployment

```text
Gemma 4 E4B
├── conversation
├── personality
├── reasoning
├── tools
├── images
├── audio
└── general assistant work
```

## Why native system-role support matters

Cherry’s system context may contain:

- Tree identity
- personality controls
- Diary rules
- delegation behavior
- selected memory
- current Forest state
- current Workshop

A model trained for a real system role is preferable to one that depends on brittle prompting workarounds.

## Multimodality

Gemma can potentially let Cherry understand images and audio without immediately loading another specialist.

## MTP

Gemma 4 supports dedicated speculative-decoding draft models. MTP should be benchmarked separately because support depends on the actual backend/runtime.

## Weaknesses / risks

- warmth/personality quality is still unknown
- heavier than LFM2.5-2.6B
- one multimodal model can tempt the architecture to overuse it
- maximum context should not replace targeted memory retrieval
- MTP support must be verified in the chosen runtime

## Decision

**Retained. Leading General/Multimodal Cherry candidate.**

---

# 4. Selected model — Ai2 OLMo 3 7B-Instruct

OLMo’s defining advantage is **model-flow openness**.

Ai2 exposes unusually broad parts of the model lifecycle, including weights, code, checkpoints, and training details.

## Why it survived

- strong openness
- function/tool calling
- U.S.-developed
- Apache-2.0-oriented ecosystem
- compelling future fine-tuning path
- natural candidate for Bristlecone-assisted Cherry specialization

```text
OLMo 3 7B-Instruct
      ↓
future Cherry-specific post-training
      ↓
personality
delegation
Workshop discipline
memory behavior
Forest protocol
```

## Weaknesses / risks

- text-centric compared with Gemma
- larger than LFM2.5-2.6B
- may not offer enough production advantage over Gemma
- everyday warmth must be tested
- could ultimately become training-only rather than production Cherry

## Decision

**Retained for the Cherry bench, especially for openness and trainability.**

---

# 5. Main competitors considered

## IBM Granite 4.1

### Strengths
- tool calling
- instruction following
- structured workflows
- local deployment
- Apache 2.0

### Why it did not enter the current top three
Its profile appears better aligned with procedural Trees such as Maple/Cedar than with Cherry’s warmth/personality requirement.

**Status:** strong alternate.

---

## OpenAI gpt-oss-20b

### Strengths
- 21B total / ~3.6B active
- strong reasoning
- tool use
- Apache 2.0
- local deployment

### Why it was not favored
It is much heavier and text-only, and it does not directly solve Cherry’s personality/warmth requirement.

**Status:** stronger fit for deeper specialist Trees.

---

## Liquid 1.2B variants

### Strengths
- extremely small
- good edge potential

### Why 2.6B was preferred
The 2.6B remains tiny while offering more agentic headroom and 128K context.

**Status:** possible future ultra-light Forest/router model.

---

## Mistral / NVIDIA / Phi / Llama alternatives

These remained secondary because they either duplicated an already-covered role, were heavier, lacked a unique Cherry advantage, or fit another Tree better.

---

# 6. Why Cherry currently justifies three models

The three candidates represent different strategies:

```text
LFM2.5-2.6B
→ extreme agentic efficiency

Gemma 4 E4B
→ complete multimodal assistant

OLMo 3 7B-Instruct
→ maximum openness/trainability
```

The benchmark may still reduce Cherry to two production models.

Examples:
- Gemma is fast enough to make LFM redundant
- OLMo earns a training-only role
- LFM handles most tasks and Gemma handles escalation

---

# 7. Proposed Cherry benchmark

## Conversation/personality
- 50+ turn casual conversation
- personality consistency
- user correction/adaptation
- playful → serious transition
- mannerism intensity control

## Agent/tool
- simple tool call
- ambiguous tool selection
- multi-step chain
- irrelevant-tool temptation
- tool failure
- delegation to another Tree

## Memory/privacy
- one relevant Leaf among many
- irrelevant history rejection
- Diary-derived hint without raw disclosure
- attempted cross-Tree Diary leakage
- compressed long-session retrieval

## Performance
- TTFT
- total latency
- tokens/sec
- RAM/VRAM
- CPU/GPU
- model load/unload time
- impact on active Maple/Cedar/McIntosh
- Workshop-size sensitivity

---

# 8. Current conclusion

> **Keep LFM2.5-2.6B, Gemma 4 E4B, and OLMo 3 7B-Instruct for Cherry’s benchmark because they represent three different strategies: fast agent, complete multimodal assistant, and highly open/trainable assistant.**

---

# Official references

- Gemma 4 overview: https://ai.google.dev/gemma/docs/core
- Gemma 4 model card: https://ai.google.dev/gemma/docs/core/model_card_4
- Gemma 4 tool format: https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4
- LFM2.5-2.6B: https://docs.liquid.ai/lfm/models/lfm25-2.6b
- Liquid model library: https://docs.liquid.ai/lfm/models/text-models
- Liquid license: https://docs.liquid.ai/lfm/help/model-license
- Ai2 OLMo: https://allenai.org/olmo
- OLMo 3 overview: https://allenai.org/blog/olmo3
- IBM Granite 4.1: https://www.ibm.com/granite/docs/models/granite4-1
- OpenAI gpt-oss: https://openai.com/index/introducing-gpt-oss/
