---
title: "The Forest — Bristlecone Model, Vision, and Speculation Checkpoint"
project: "The Forest"
tree: "Bristlecone Pine"
role: "Treewright"
status: "Design checkpoint / pre-download"
date: "2026-08-10"
tags:
  - forest
  - bristlecone
  - treewright
  - model-form
  - mistral-small-4
  - gpt-oss
  - vision
  - speculative-decoding
  - eagle
  - clones
  - workshops
  - performance
  - phase-14
---

# The Forest — Bristlecone Model, Vision, and Speculation Checkpoint

## Purpose

This document captures the current Bristlecone model-selection and performance-design discussion before downloading a Big-model candidate.

It records:

- why Bristlecone needs more than coding ability
- GPT-OSS-120B vs Mistral Small 4
- graphical/vector/UI requirements
- native vision vs a Vision Workshop
- hardware and model-size considerations
- possible Small/Big/Mobile model forms
- GPT-OSS-20B as a future reusable model
- EAGLE speculative decoding
- a possible Forest-native speculation layer
- how Tree Clones may participate in speculation
- how two or more speculation layers can coexist
- current Phase 14 sequencing
- the immediate download/preflight plan

This is a **design checkpoint**, not a frozen final model assignment.

## Current Bristlecone role

Bristlecone Pine is the Forest's **Treewright**. Its role is broader than coding. It may be responsible for Forest architecture, code design/review, debugging, runtime design, UI and vector/interface design, model selection, AI architecture, helping create and improve other Trees/AIs, training strategy, evaluation systems, Workshop design, integration, and technical consistency.

> **Big Bristlecone should be more capable at being Bristlecone, not become a different Tree.**

## Current Small model

```text
qwen35:4b-64k
~3.4 GB
```

Current decision:

> **Do not replace Qwen yet.**

Sequence:

```text
complete current architecture/setup
        ↓
benchmark existing Qwen Small
        ↓
select non-Chinese Small replacement
        ↓
replace Qwen
        ↓
run the exact same benchmark suite
        ↓
compare objectively
```

Qwen remains the control/baseline until the architecture and benchmark are ready.

## Model-origin preference

For future Forest model selection, prioritize **non-Chinese-developed models and core technology when practical**. Chinese model families can still be mentioned for comparison when uniquely relevant, but they should not be default core candidates.

## Big Bristlecone candidate direction

Current strongest candidates:

```text
GPT-OSS-120B
vs
Mistral Small 4 119B
```

Current direction:

> **Mistral Small 4 is the leading Big Bristlecone candidate.**

This is not yet benchmark-certified.

## GPT-OSS-120B snapshot

```text
Developer: OpenAI
License: Apache 2.0
Total parameters: ~117B
Active/token: ~5.1B
Context: 128K
Architecture: MoE
Reasoning controls: low / medium / high
Tools/agent use: yes
Fine-tuning: yes
Native vision: no
Official low-precision checkpoint: ~60.8 GiB
```

Strengths:
- reasoning
- coding
- tools/agents
- AI/model engineering
- permissive license
- customization
- clean mapping to Forest Light/Normal/Deep
- relatively low active parameter count

Main limitation:

> **GPT-OSS is text-only and cannot natively inspect rendered graphical work.**

## Mistral Small 4 snapshot

Exact current model:

```text
Mistral-Small-4-119B-2603
```

Characteristics:

```text
Developer: Mistral AI
Origin: France
License: Apache 2.0
Total parameters: 119B
Active/token: ~6.5B
Experts: 128
Active experts/token: 4
Context: 256K
Text input: yes
Image input: yes
Text output: yes
Reasoning: configurable
Coding: yes
Agentic coding: yes
Function/tool calling: yes
Fine-tuning/customization: yes
```

Mistral Small 4 combines instruction-following, reasoning, coding-agent, and multimodal capabilities in one model.

## Mistral Small 4 deployment assets

### Main checkpoint

```text
mistralai/Mistral-Small-4-119B-2603
```

### Official NVFP4 checkpoint

```text
mistralai/Mistral-Small-4-119B-2603-NVFP4
```

Current official Hugging Face repository size observed during pre-download research:

```text
~70.8 GB
```

Mistral documentation reports roughly a ~60 GB GPU-memory floor at FP4, depending on configuration. Repository/download size and runtime-memory footprint are different measurements.

### EAGLE component

```text
mistralai/Mistral-Small-4-119B-2603-eagle
```

This is an acceleration component for speculative decoding, not another Tree or another main model.

## Why Mistral is attractive for Treewright

Bristlecone may need a visual build-feedback loop:

```text
design UI/vector
↓
write implementation
↓
run/render
↓
look at result
↓
criticize alignment/hierarchy/style
↓
modify code
↓
render again
```

Native image input lets the main model inspect screenshots, rendered SVGs, UI layouts, charts, diagrams, and other visual technical evidence.

## Forest flavor requirement

Bristlecone should understand the difference between:

```text
"Build a settings page."
```

and:

```text
"Build a settings page that belongs in The Forest."
```

Desired result:
- coherent Tree/Forest terminology where appropriate
- consistent visual language
- deliberate iconography and interaction design
- subtle ecological metaphors
- ability to turn the theme down when professionalism/usability requires it

> **Taste and steerability, not constant gimmicks.**

## Graphics as code vs visual inspection

### Graphics as code
- SVG
- CSS
- HTML Canvas
- WebGL
- charts
- diagrams
- vector paths
- icons
- animations
- UI components

Both GPT-OSS and Mistral can create these as code.

### Visual inspection
- inspect rendered SVG
- notice alignment
- judge spacing
- compare UI versions
- inspect screenshots
- identify clipping
- critique visual hierarchy

Mistral Small 4 has native image input. GPT-OSS would need a separate visual capability.

## Vision Workshop alternative

Vision can remain a **Tree capability** instead of being permanently tied to the main brain:

```text
                         BRISTLECONE
                              │
                        MAIN BRAIN
                              │
                ┌─────────────┴─────────────┐
                │                           │
          normal reasoning             VISION WORKSHOP
                                            │
                                      vision model
                                            │
                                     screenshot/image
                                            │
                                  structured observations
                                            │
                                            ↓
                                      main model
```

Benefits:
- main model can change without removing Bristlecone's eyes
- visual model can upgrade independently
- load vision only when needed
- keeps capability separate from Tree identity

## GPT-OSS-20B

Possible future model-library candidate:

```text
~21B total
~3.6B active/token
128K context
Apache 2.0
low/medium/high reasoning
tools/agents
fine-tunable
text-only
~13 GB-class checkpoint
~16 GB-class memory target
```

It is **not** GPT-OSS-120B compressed to 20B; it is a smaller family member.

Possible later uses:
- McIntosh Big candidate
- fallback model
- fine-tuning/training experiments
- alternative Tree
- portable/edge use

Do not assign it permanently yet.

## Device-aware Tree Forms

Future possibility:

```text
                      BRISTLECONE
                           │
                  same Tree identity
                  same durable memory
                  same permissions
                  same voice
                  same Leaves / Roots
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          BIG FORM      SMALL FORM    MOBILE FORM
         workstation       PC         phone/tablet
```

The model may change by device. The Tree does not.

> **A Tree is not its model.**

## Hardware reality

Both GPT-OSS-120B and Mistral Small 4 are roughly in a **60+ GB low-precision model-memory class**.

Current Forest hardware context:

```text
Ryzen 7 3700X
~32 GB system RAM
RX 580-class GPU
```

Therefore:
- staging/downloading is possible if disk space permits
- current hardware cannot comfortably run Big locally
- downloading does not mean activating
- do not remove current Qwen
- runtime/quantization tests should inform later hardware decisions

## EAGLE

EAGLE is a speculative-decoding acceleration method.

Conceptually:

```text
EAGLE
│
├── predicts likely future token/features
│
└── Mistral Small 4 verifies
```

Purpose:

> **Reduce generation latency.**

EAGLE does not change Bristlecone identity or make the model inherently smarter.

## Phase 14 placement

```text
14.11 — Small / Big Model Escalation
14.12 — Ollama vs. llama.cpp Evaluation
14.13 — Speculative Decoding Evaluation
14.14 — Final Performance Benchmark
```

Mistral's official EAGLE head belongs naturally in 14.13.

## Forest-native speculation

Forest may also develop a higher-level speculative system. This is closer to speculative execution/drafting than token-level speculative decoding.

### Small → Big drafting

```text
hard task
      ↓
Small Bristlecone drafts
      ↓
Big Bristlecone receives
user request + candidate
      ↓
Big verifies/corrects
```

For coding:

```text
SMALL BRISTLECONE / CLONE
│
├── inspect likely files
├── identify edit locations
├── draft patch
├── predict tests
└── summarize likely solution
        ↓
BIG BRISTLECONE
│
├── verify assumptions
├── inspect critical code
├── correct patch
└── approve final result
```

## Clones and speculation

Clones may perform speculative work, but:

> **A Clone is not a speculative decoder.**

A Clone is an independently operating extension of a Tree sharing Tree identity/durable knowledge. Speculative drafting is only one possible Clone job.

Potential pattern:

```text
Clone A → candidate architecture
Clone B → candidate implementation
Clone C → predicted test failures
                   ↓
             Main Bristlecone
                   ↓
             compare / verify
```

## Resource rule for Clone speculation

Avoid loading multiple copies of a huge 60+ GB Big model simply to speculate.

Preferred idea:

```text
one loaded Big model
        │
        ├── main session
        ├── Clone A context
        └── Clone B context
```

Prefer:

```text
Small Clone drafts
       ↓
Big verifies
```

over:

```text
Big drafts
↓
Big verifies
```

when quality permits.

## Workshop-level speculation

Potential safe read-only work can sometimes happen ahead of need:

```text
read file
search repo
inspect logs
run non-destructive tests
query service status
inspect process state
```

Do not speculate destructive or externally consequential actions.

Core rule:

> **Speculation must never become permission speculation.**

Spirit remains authoritative.

## Possible three-level speculation stack

```text
LEVEL 3 — TREE / SEMANTIC
Small Form or Clone drafts
plans, patches, answers

             ↓

LEVEL 2 — WORKSHOP / TOOL
safe likely inspections
prefetched/executed ahead

             ↓

LEVEL 1 — RUNTIME / TOKEN
EAGLE or another speculative decoder

             ↓

OUTPUT
```

Each attacks a different latency source.

```text
Runtime EAGLE
→ token-generation latency

Workshop speculation
→ tool round-trip latency

Tree/Clone speculation
→ planning/reasoning latency
```

They can coexist.

## Terminology distinction

```text
Speculative Decoding
= runtime/token level

Forest Speculative Execution / Drafting
= Tree/Clone/Workshop level
```

Forest-level drafts may influence Big reasoning, so they do not have exactly the same verification guarantees as token-level speculative decoding.

## Proposed expansion of 14.13

```text
14.13 — SPECULATION & SPECULATIVE DECODING

14.13A — Runtime speculation
          EAGLE / draft decoding

14.13B — Forest-native drafting
          Small → Big verification

14.13C — Clone speculation
          parallel candidate work

14.13D — Workshop speculation
          safe read-only prefetch/execution

14.13E — Combined two-level test
          Forest speculation
                +
          runtime EAGLE

14.13F — Resource benchmark
          latency / RAM / VRAM /
          CPU / GPU / quality /
          wasted work / stability
```

This is proposed, not frozen.

## Current Ollama caution

Do **not** assume:

```bash
ollama pull mistral-small
```

means Mistral Small 4.

The public Ollama `mistral-small` entry currently refers to earlier Mistral Small generations, and Mistral Small 4 has had a separate model-support request.

Use exact model provenance when staging Big Bristlecone.

## Exact staging candidate

Current leading download candidate:

```text
mistralai/Mistral-Small-4-119B-2603-NVFP4
```

Why:
- official Mistral repository
- Apache 2.0
- 119B / ~6.5B active
- multimodal
- 256K context
- official FP4 quantization
- more practical than full-precision checkpoint
- appropriate for eventual Big-form testing

Current official repository reports:

```text
~70.8 GB
```

## Download safety/provenance rules

Before downloading:

1. verify exact official repository
2. verify available disk space
3. choose staging location
4. record exact repository/model identity
5. keep current Qwen untouched
6. do not activate automatically
7. preserve current Forest/Hermes config
8. verify downloaded files
9. record provenance in future Forest model registry/Roots

> **Download/staging is not activation.**

## Immediate pre-download plan

First run a non-destructive storage preflight in Cherry-AI:

```bash
df -h ~
du -sh ~/.cache/huggingface 2>/dev/null || true
du -sh ~/.ollama 2>/dev/null || true
```

These commands only inspect storage.

Do not start the ~70.8 GB download until the available space and intended Qubes storage location are confirmed.

## Current decision snapshot

```text
BRISTLECONE

Current Small:
qwen35:4b-64k
KEEP until setup + baseline benchmark

Future Small:
non-Chinese replacement
TBD by benchmark

Leading Big candidate:
Mistral Small 4 119B
NVFP4 staging candidate

Big comparison/reference:
GPT-OSS-120B

Future model-library candidate:
GPT-OSS-20B

Vision:
native in Mistral Small 4
but Vision Workshop remains architecturally valuable

Speculation:
EAGLE at runtime layer
+
possible Forest-native Tree/Clone/Workshop speculation

14.11:
Small / Big architecture

14.12:
runtime evaluation

14.13:
speculation / speculative decoding

14.14:
final performance benchmark
```

## Reinforced Forest invariants

> **A Tree is not its model.**

> **Big Form means more capable at being the same Tree.**

> **Vision can be a Tree capability rather than permanently coupled to one model.**

> **Speculation must not become permission speculation.**

> **Runtime acceleration stays below Tree identity.**

> **Clones may speculate, but speculation does not define a Clone.**

> **Small/Big Model Form and speculation are independent architectural axes.**

> **Do not replace a working baseline until it has been measured.**

> **Model provenance should be explicit and inspectable.**

> **Download/staging is not activation.**

## Next action

```text
1. Run non-destructive storage preflight in Cherry-AI.
2. Confirm where ~70.8 GB of model data should live.
3. If necessary, expand/attach Qubes storage safely.
4. Use an exact download method for the official NVFP4 checkpoint.
5. Verify model files and provenance.
6. Leave current Qwen runtime unchanged.
7. Continue Phase 14.11 architecture work.
```

Do not mark the Mistral download or Big Bristlecone activation complete until terminal output verifies each step.
