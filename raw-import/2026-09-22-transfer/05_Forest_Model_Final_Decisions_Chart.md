---
title: "The Forest — Model Selection Master Chart"
project: "The Forest"
document_type: "model-selection-master-chart"
status: "current decisions and pending benchmarks"
updated: "2026-08-12"
tags: [forest, models, architecture, decision-log]
---

# The Forest — Model Selection Master Chart

> **Purpose:** master index of the current model decisions for Cherry, Maple, Cedar, and McIntosh.  
> **Important:** “Selected” means selected for the current architecture/benchmark direction, not necessarily already downloaded, installed, or permanently frozen.

---

# Current decisions

| Tree | Role | Current model | Decision status | Main reason |
|---|---|---|---|---|
| **Cherry** | Quick / Utility | **LFM2.5-2.6B** | Selected for 3-model bench | Tiny, agentic, native tools, 128K |
| **Cherry** | General / Multimodal | **Gemma 4 E4B** | Selected for 3-model bench | Conversation + reasoning + image/audio + tools |
| **Cherry** | Open / Trainable | **OLMo 3 7B-Instruct** | Selected for 3-model bench | Full model-flow openness and future Cherry training |
| **Maple** | Small / Utility | **LFM2.5-2.6B** | **Preferred core selection** | Efficient file/email/job/tool agent |
| **Maple** | Big / Multimodal Reasoner | **Gemma 4 E4B** | **Preferred core selection** | Adds visual/audio understanding + deeper judgment |
| **Cedar** | Small / Visual Triage | **Gemma 4 E2B vs E4B** | **Pending benchmark** | Background efficiency vs stronger judgment |
| **Cedar** | Big / Deep Investigator | **Muse Glimmer 30B K-Quant-17GB** | **Leading selected direction** | Deep agent reasoning + screenshots + failure recovery |
| **McIntosh** | Small / Technician | **Essential AI Rnj-1 Instruct** | **Top choice** | Code/STEM + software agents + tools |
| **McIntosh** | Updated Small checkpoint | **Rnj-1.5-Instruct** | Must benchmark against Rnj-1 | 160K follow-up with stronger long-context/agent claims |
| **McIntosh** | Big / Senior Investigator | **Muse Glimmer 30B K-Quant-17GB** | **Leading selected direction** | Deep troubleshooting + vision + long agents + recovery |

---

# Forest-wide roster

```text
THE FOREST

Cherry
├── LFM2.5-2.6B
├── Gemma 4 E4B
└── OLMo 3 7B-Instruct

Maple
├── LFM2.5-2.6B
└── Gemma 4 E4B

Cedar
├── Gemma 4 E2B OR E4B  ← benchmark decides
└── Muse Glimmer K-Quant-17GB

McIntosh / Apple Tree
├── Rnj-1 Instruct
│   └── Rnj-1.5 must be benchmarked as newer checkpoint
└── Muse Glimmer K-Quant-17GB
```

---

# Shared-weight opportunities

A Tree is not its model weights.

```text
model weights
≠ Tree identity
≠ runtime session
≠ conversation context
```

## Gemma sharing

```text
Gemma 4 E4B resident weights
          │
     ┌────┼────┐
     ▼    ▼    ▼
 Cherry Maple Cedar?
 session session session
```

Each Tree must retain separate:

- `execution_context_id`
- `binding_id`
- `session_id`
- KV/cache state
- system prompt
- permissions
- Workshop/tool set
- memory retrieval
- control state

## Muse sharing

```text
Muse Glimmer K-Quant-17GB resident weights
                  │
             ┌────┴────┐
             ▼         ▼
           Cedar    McIntosh
           session   session
```

This allows one expensive weight set to support two specialist Trees without merging identity, memory, authority, or runtime state.

---

# Unique model directions currently retained

| Model direction | Trees |
|---|---|
| **LFM2.5-2.6B** | Cherry, Maple |
| **Gemma 4 E4B** | Cherry, Maple, possible Cedar |
| **Gemma 4 E2B** | Cedar candidate |
| **OLMo 3 7B-Instruct** | Cherry |
| **Muse Glimmer K-Quant-17GB** | Cedar, McIntosh |
| **Rnj-1 / Rnj-1.5** | McIntosh |

This is far more efficient than assigning completely unique weights to every Tree.

---

# Main competitions by Tree

## Cherry

| Retained | Main competitors | Why retained |
|---|---|---|
| **LFM2.5-2.6B** | Liquid 1.2B, Granite 4.1 | Better agentic headroom while still tiny |
| **Gemma 4 E4B** | Granite 4.1, gpt-oss-20b | Multimodal complete assistant at low size |
| **OLMo 3 7B** | other general/open models | Unusually open/trainable model flow |

**Pending:** exact routing and whether all three deserve permanent production roles.

---

## Maple

| Selected | Main competitors | Why selected |
|---|---|---|
| **LFM2.5-2.6B** | Granite family | Tiny, agentic, ideal Utility role |
| **Gemma 4 E4B** | Granite 4.1 8B, LFM2.5-8B-A1B, OLMo 7B | Adds multimodality rather than duplicating agentic reasoning |

**Current architecture:** two core models.

---

## Cedar

| Current direction | Main competitors | Why |
|---|---|---|
| **Gemma E2B/E4B Small** | Ministral 3 3B Reasoning, Phi-4 Multimodal, PLaMo 2.1-2B-VL | Best combined edge size + vision/audio + tools + reasoning found so far |
| **Muse K-Quant-17GB Big** | Gemma 12B, Nemotron Omni 30B-A3B, Ministral 14B Reasoning | Adds long-horizon agent behavior + failure recovery + screenshots |

**Pending:** E2B vs E4B is one of the most important Forest performance tests.

---

## McIntosh

| Current direction | Main competitors | Why |
|---|---|---|
| **Rnj-1 Small** | Nemotron 3 Nano 4B, OLMo 3 7B | Strongest direct code/STEM/software-agent fit |
| **Muse K-Quant-17GB Big** | Ministral 14B Reasoning, gpt-oss-20b, Phi-4 Reasoning Vision | Adds deep reasoning, GUI/screenshots, long agents, failure recovery |

**Mandatory update test:** Rnj-1 vs Rnj-1.5.

---

# Two-model rule

Forest design rule:

> **Prefer two core models per Tree: one lightweight/fast model and one stronger/deeper model. A third core model must earn its place by providing an important non-overlapping capability.**

| Tree | Preferred core count | Current state |
|---|---:|---|
| Cherry | 2 preferred; 3 allowed if justified | **3 retained for benchmark** |
| Maple | 2 | **2** |
| Cedar | 2 | **2** |
| McIntosh | 2 | **2** |

Specialists such as OCR, image editing/generation, audio, embeddings, malware analysis, or deterministic media processors do not automatically count against the core-model target because they wake only for a narrow capability.

---

# Origin/provenance policy

Current preference:

1. **U.S.-developed models** — preferred
2. **Google DeepMind / U.K.–U.S.** — accepted
3. **Japanese-developed models** — accepted and actively considered
4. **Other close-allied Western models** — allowed when technically compelling
5. **Chinese-developed core models** — strongly deprioritized when practical

Important: provenance includes training/base-model lineage, not only company headquarters.

---

# Runtime invariants

## Weights are not identity

Multiple Trees may share model bindings/resident weights while preserving:

- separate sessions
- separate KV
- separate tools
- separate prompts
- separate permissions
- separate memory
- separate control state

## Small must be tested under concurrency

A Small model is not successful merely because it is fast in isolation. Test while:

- other Trees are loaded
- background jobs run
- normal desktop applications run
- the user is doing foreground work

## Big wakes on demand

```text
Small
→ normal task
→ complexity/uncertainty threshold
→ Big
→ persist result/incident state
→ unload Big
```

---

# Remaining decisions

## Cherry
- Does LFM2.5-2.6B maintain personality?
- Does OLMo earn production residency or become training-only?
- Can Gemma E4B collapse roles?

## Maple
- Validate LFM tool reliability.
- Validate Gemma visual/media judgment.
- Only revisit Granite/LFM8B if weaknesses appear.

## Cedar
- **E2B vs E4B under real concurrent load**
- screen-event trigger policy
- Muse K-Quant-17GB actual hardware feasibility
- lighter Big fallback if necessary

## McIntosh
- Rnj-1 vs Rnj-1.5
- terminal/tool correctness
- Muse visual troubleshooting
- Big escalation thresholds

---

# Recommended benchmark order

```text
1. Cherry
   LFM2.5-2.6B vs Gemma E4B vs OLMo 7B

2. Maple
   LFM2.5-2.6B + Gemma E4B role validation

3. Cedar Small
   Gemma E2B vs Gemma E4B
   under concurrent Forest load

4. Cedar Big
   Muse K-Quant-17GB feasibility

5. McIntosh Small
   Rnj-1 vs Rnj-1.5

6. McIntosh Big
   Muse K-Quant-17GB technical-agent benchmark
```

---

# Compact chart

```text
┌────────────┬──────────────────────────────┬──────────────────────────────┐
│ TREE       │ SMALL / EVERYDAY             │ BIG / SPECIAL ROLE           │
├────────────┼──────────────────────────────┼──────────────────────────────┤
│ Cherry     │ LFM2.5-2.6B                  │ Gemma 4 E4B                  │
│            │ + OLMo 7B retained as        │ exact 3-model routing TBD    │
│            │ open/trainable third model   │                              │
├────────────┼──────────────────────────────┼──────────────────────────────┤
│ Maple      │ LFM2.5-2.6B                  │ Gemma 4 E4B                  │
├────────────┼──────────────────────────────┼──────────────────────────────┤
│ Cedar      │ Gemma 4 E2B vs E4B           │ Muse Glimmer K-Quant-17GB    │
│            │ benchmark pending            │                              │
├────────────┼──────────────────────────────┼──────────────────────────────┤
│ McIntosh   │ Rnj-1 Instruct               │ Muse Glimmer K-Quant-17GB    │
│            │ test Rnj-1.5 update          │                              │
└────────────┴──────────────────────────────┴──────────────────────────────┘
```

---

# Related files

- `01_Cherry_Model_Decision.md`
- `02_Maple_Model_Decision.md`
- `03_Cedar_Model_Decision.md`
- `04_McIntosh_Model_Decision.md`
