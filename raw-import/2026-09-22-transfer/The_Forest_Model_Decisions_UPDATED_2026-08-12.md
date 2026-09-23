# The Forest — Updated Model Decisions

**Updated:** August 12, 2026  
**Status:** Current confirmed architecture  
**Purpose:** Preserve the current model roster, the reasoning behind each choice, rejected alternatives, licensing/provenance rules, runtime caveats, and future upgrade triggers.

---

# 1. Global Model-Selection Rules

The Forest does **not** choose models by generic benchmark score alone. Each Tree gets a model chosen for that Tree's exact job, failure modes, resource profile, runtime needs, and escalation path.

## Core rules

- Prefer local-first, self-hostable deployment.
- Prefer clean permissive licenses such as Apache 2.0, MIT, or BSD.
- Avoid foundational/core models with:
  - revenue thresholds,
  - field-of-use restrictions,
  - separate mandatory usage policies,
  - unclear redistribution or derivative-model rights.
- Prefer two core models per Tree:
  - a lightweight/fast model;
  - a stronger/deeper model.
- A third core model is justified only if it provides a genuinely distinct critical capability.
- Narrow specialists such as document parsers, OCR models, or vision helpers do **not** count as a third core model when they are loaded only when needed.
- Model weights are not Tree identity.
- Trees must keep separate:
  - `execution_context_id`,
  - `binding_id`,
  - `session_id`,
  - KV/cache state,
  - system prompt,
  - permissions,
  - Workshops/tools,
  - memory,
  - control state.
- Prefer model-family diversity where practical so one family does not create a Forest-wide shared failure mode.
- Use targeted context, durable incident/project state, Leaves, and retrieval instead of stuffing giant histories/logs into model context.
- Keep runtimes modular so models can move between llama.cpp, Ollama, Hermes, vLLM, or future runtimes.

## Provenance preference chain

Use provenance as a preference/tiebreaker, not as a substitute for technical merit, openness, licensing, or role fit.

**UK/Ireland + USA > Japan > UK > Sweden > Poland > Switzerland > Italy > France > Germany > other Europe**

France and Germany are allowed but not preferred when otherwise similar alternatives exist. Italy is welcome if a strong candidate appears. Switzerland and Sweden are explicitly acceptable.

---

# 2. Final Confirmed Roster

| Tree | Slot | Model / Capability | Status |
|---|---|---|---|
| 🍒 Cherry | Small / Quick Multimodal | **Phi-4 Multimodal Instruct 5.6B** | ✅ Confirmed |
| 🍒 Cherry | General / Strong Multimodal | **Gemma 4 E4B** | ✅ Confirmed |
| 🍒 Cherry | Open / Trainable | **OLMo 3 7B-Instruct** | ✅ Confirmed |
| 🍁 Maple | Small / Utility | **IBM Granite 4.1 3B** | ✅ Confirmed |
| 🍁 Maple | Big / Multimodal | **Gemma 4 E4B** | ✅ Confirmed |
| 🍁 Maple | Document Workshop | **Docling + Granite Docling 258M** | ✅ Confirmed |
| 🌲 Cedar | Small / Security Triage | **Gemma 4 E4B** | ✅ Confirmed |
| 🌲 Cedar | Big / Deep Visual Investigator | **Phi-4 Reasoning Vision 15B** | ✅ Confirmed |
| 🍎 McIntosh | Small / Technician | **Essential AI Rnj-1 Instruct** | ✅ Confirmed for now |
| 🍎 McIntosh | Big / Senior Engineer | **Magistral Small 1.2 24B** | ✅ Confirmed |

---

# 3. 🍒 Cherry

## Role

Cherry is the primary conversational and personal-assistant Tree.

Cherry should handle:

- everyday conversation,
- intent recognition,
- Tree routing/delegation,
- lightweight memory retrieval,
- Forest navigation/help,
- simple tools,
- screenshots/images,
- OCR,
- audio/speech,
- escalation to stronger models when necessary.

Cherry should feel **fast, available, broad, and natural** rather than behaving like a deep specialist.

## Small / Quick Multimodal
### ✅ Phi-4 Multimodal Instruct 5.6B

### Why it won

Phi-4 Multimodal gives Cherry a compact model that is still genuinely useful as the Forest's front door.

It can cover:

- text conversation,
- lightweight reasoning,
- routing,
- memory retrieval,
- function/tool calling,
- screenshots/images,
- OCR,
- audio,
- speech understanding.

That means Cherry does not need to wake Gemma E4B every time an image, screenshot, or audio clip appears.

### Why not Phi-4 Mini Instruct 3.8B?

Phi-4 Mini Instruct was a serious finalist and is cheaper.

It was attractive because it is:

- small,
- fast,
- instruction-focused,
- tool-capable,
- MIT-licensed,
- U.S.-developed.

But Cherry is the main user-facing assistant. The extra multimodal capability of the 5.6B model was judged worth the larger footprint.

The distinction became:

```text
Phi-4 Mini Instruct
→ text + tools + quick reasoning

Phi-4 Multimodal Instruct
→ text + tools + quick reasoning
  + vision
  + OCR
  + audio/speech
```

For Cherry, the second profile is more useful.

### Why not Phi-4 Mini Reasoning?

Phi-4 Mini Reasoning is more specialized toward mathematical/reasoning workloads.

That is not Cherry Small's main job.

Cherry should escalate difficult reasoning rather than spend extra compute acting like a proof engine.

There was also a provenance yellow flag because the reasoning training involved synthetic data generated from DeepSeek-R1. The final model is Microsoft-developed and MIT-licensed, but this was still less attractive than the cleaner general/multimodal path.

### Why not Ministral 3 3B Instruct?

Ministral 3 3B was one of the strongest technical alternatives because it offered:

- compact size,
- vision,
- native tools,
- structured output,
- long context,
- Apache 2.0.

It lost mainly because Phi gave Cherry:

- preferred U.S. provenance,
- MIT licensing,
- broad multimodality,
- audio/speech,
- a very strong match for the "resident quick assistant" role.

Ministral remains a good fallback benchmark if Phi's local runtime proves inconvenient.

### Why not Granite 4.1 3B?

Granite is excellent, but its strongest role is Maple.

Using Granite for Cherry too would reduce specialization.

Granite is better at structured enterprise-style information handling. Phi is better suited to the conversational, multimodal front-door role.

### Why not Gemma E2B?

Gemma E2B would create too much same-family redundancy:

```text
Cherry Small = Gemma
Cherry General = Gemma
```

Using Phi for Small and Gemma for General gives Cherry two different model families and reduces shared failure modes.

---

## General / Strong Multimodal
### ✅ Gemma 4 E4B

Gemma 4 E4B remains Cherry's stronger general-purpose escalation model.

It handles:

- harder reasoning,
- ambiguity,
- more difficult multimodal work,
- more difficult tool/agent tasks,
- stronger general judgment.

The intended escalation path is:

```text
Phi-4 Multimodal 5.6B
→ quick / resident / everyday multimodal

        ↓ escalate

Gemma 4 E4B
→ harder reasoning / ambiguity / heavier work
```

---

## Open / Trainable
### ✅ OLMo 3 7B-Instruct

OLMo stays because it serves a different strategic purpose.

It is valuable for:

- experimentation,
- fine-tuning,
- reproducibility,
- training research,
- understanding how behavior changes during training.

Its openness is the reason it survives the normal two-core-model rule.

It is not merely a third inference tier.

---

## Cherry deployment checks

Before final rollout, benchmark:

- quantized RAM footprint,
- latency,
- image/audio latency,
- tool-call reliability,
- hallucinated tool names,
- behavior with tiny dynamic Workshops,
- escalation reliability.

The Forest runtime should deterministically reject malformed or nonexistent tool calls.

---

# 4. 🍁 Maple

## Role

Maple is the Forest's workspace, file, document, email, organization, and information-management Tree.

Maple handles:

- files/folders,
- metadata,
- structured extraction,
- organization,
- RAG,
- Leaf Foliage maintenance,
- imports/exports,
- email,
- moving/copying/renaming,
- backup/sync workflows,
- document ingestion.

Maple should be **structured, predictable, precise, and efficient**.

## Small / Utility
### ✅ IBM Granite 4.1 3B

### Why Granite won

Granite matches Maple's job unusually well.

Its strengths align with:

- structured information handling,
- extraction,
- classification,
- RAG,
- instruction following,
- tool calling,
- coding/automation,
- predictable workflow execution.

Maple's common flow is:

```text
understand request
→ locate information
→ extract / classify
→ call narrow tool
→ verify result
→ update metadata / Leaf
```

That is almost exactly the kind of work Granite is suited for.

### Why not Ministral 3 3B?

Ministral is more broadly capable and includes vision.

But Maple does not need to pay for vision in Small because:

- Gemma E4B already handles harder multimodal work;
- Docling handles document-specific vision;
- Maple Small benefits more from structured information discipline.

### Why not Phi-4 Mini?

Phi-4 Mini is a stronger conversational generalist.

That is more valuable for Cherry.

Maple benefits more from Granite's structured enterprise/document/RAG orientation.

### Why not SmolLM3?

SmolLM3 is attractive for openness and tool use.

Granite won because its specialization maps more directly to Maple's everyday job.

### Why LFM2.5 was removed

LFM2.5 had previously been considered/selected.

It was removed after the licensing standard tightened because its custom license includes commercial/revenue-threshold concerns.

Granite's Apache 2.0 licensing is a much cleaner foundational fit.

---

## Big / Multimodal
### ✅ Gemma 4 E4B

Maple Big handles:

- difficult visual organization,
- ambiguous semantic classification,
- screenshots/images,
- audio,
- deeper content comparison,
- cases where routine structured utility work becomes genuinely ambiguous.

Granite handles the procedural work.

Gemma handles the harder judgment.

---

## Document Workshop
### ✅ Docling + Granite Docling 258M

Docling is now formally included in Maple.

### Why it was added

Docling gives Maple a specialized local document-ingestion pipeline without adding a third always-running core model.

The distinction matters:

```text
Docling
= document-processing framework/toolchain

Granite Docling 258M
= tiny specialized vision-language model used when helpful
```

### What it can help Maple process

- PDFs,
- scans,
- OCR,
- tables,
- forms,
- headings,
- page layout,
- reading order,
- equations,
- code blocks,
- structured document hierarchy.

### Why this is better than asking Granite 4.1 3B to do everything

Instead of asking a 3B general model to visually parse an entire document:

```text
document
→ Docling / Granite Docling
→ structured document representation
→ Granite 4.1 3B
→ organize / classify / link
→ Leaf Foliage
```

Docling can preserve structure before the general model reasons about content.

### Why it is especially useful for Leaf Foliage

Docling can produce structured forms such as:

- DoclingDocument,
- DocTags,
- Markdown,
- JSON,
- RAG-friendly chunks.

That fits the Forest's Markdown/Obsidian-compatible knowledge architecture extremely well.

### Why Docling does not violate the two-core-model rule

Docling is an **on-demand specialist capability**, not a third resident brain.

It should live inside a Maple Document Workshop and load only when needed.

---

## Maple transaction rule

For risky file operations:

```text
prepare
→ validate
→ snapshot/journal
→ execute
→ verify
→ commit
→ rollback if needed
```

The model should never replace deterministic file-system safeguards.

---

# 5. 🌲 Cedar

## Role

Cedar is the Forest's security, privacy, permissions, trust, incident-response, and recovery Tree.

Cedar follows a user-sovereignty-first approach:

```text
detect
→ explain
→ warn
→ propose mitigation
→ user decides
```

unless the user explicitly pre-authorizes a deterministic enforcement action.

The LLM is not the security boundary.

## Small / Background Security Triage
### ✅ Gemma 4 E4B

### Why E4B won

Cedar Small needs enough intelligence to perform actual triage, not just classify alerts.

It should handle:

- screenshots,
- routine visual checks,
- OCR,
- permission/risk reasoning,
- normal security reasoning,
- routine tools,
- deciding when escalation is needed.

### Why not Gemma E2B?

E2B was attractive for efficiency.

But the capability difference from E2B to E4B was judged significant enough that Cedar should spend the extra resources.

Cedar Small should be able to:

```text
observe
→ interpret
→ run a diagnostic
→ apply policy context
→ decide whether escalation is necessary
```

rather than escalating nearly everything.

### Why not Phi-4 Multimodal 5.6B?

Phi-4 Multimodal is broader in audio/multi-image capability, but Cedar Small benefits more from Gemma's established local stack, configurable reasoning, and balanced security-triage capability.

Phi Multimodal found a better role as Cherry Small.

---

## Big / Deep Visual Investigator
### ✅ Phi-4 Reasoning Vision 15B

### Why Phi won

Cedar Big is intentionally specialized toward difficult **visual security investigation**.

Its role includes:

- high-resolution screenshot analysis,
- GUI grounding,
- locating interface elements,
- documents/OCR,
- charts/technical images,
- visual evidence,
- deep reasoning,
- computer-use perception,
- difficult multimodal security reasoning.

This makes Phi unusually well matched to Cedar.

### Why not Ministral 3 14B Reasoning?

Ministral was the strongest challenger.

In some ways, Ministral is a better **complete agent** because it offers:

- much longer context,
- explicit tool calling,
- structured JSON,
- mature GGUF support,
- llama.cpp/Ollama/Hermes friendliness,
- reasoning + vision.

Phi won because Cedar Big was intentionally optimized for:

> difficult visual interpretation and reasoning about what Cedar sees.

Cedar's deterministic policy and tool systems can compensate for Phi's weaker native structured-tool story.

If the priority shifted to:

> one long-context model that independently runs multi-step tool investigations,

Ministral would likely win.

### Why not Mistral Small 3.2 24B?

Mistral Small 3.2 is a strong multimodal agent, but it is:

- heavier,
- more general-purpose,
- less specifically aligned with deep visual-security reasoning.

### Why not Granite 4.1 30B?

Granite is strong at structured tool use but is text-oriented and would need a separate vision specialist.

### Why not Apertus?

Apertus was technically interesting and Swiss-developed, but its additional Acceptable Use Policy conflicts with the Forest's current clean-license preference.

---

## Known Cedar Big limitations

### 16K context

Phi's context is much smaller than Ministral's.

The Forest deliberately works around this with:

- external Incident state,
- evidence objects,
- targeted retrieval,
- compact summaries,
- no giant raw-log dumps.

This is compatible with Cedar's intended architecture anyway.

### Tool calling

Phi is not as cleanly positioned as Ministral for native structured function calling.

Cedar therefore relies on:

- deterministic tool routers,
- strict Workshop schemas,
- policy engine,
- external incident state,
- validation before execution.

### Local multimodal deployment

Phi's fully faithful multimodal local path may be less mature than Mistral's GGUF ecosystem.

This is a deployment qualification item.

**Primary fallback if Phi cannot be deployed faithfully: Ministral 3 14B Reasoning.**

---

## Deterministic Cedar systems

Cedar should also include deterministic components for:

- policy,
- permissions,
- secret handling,
- network controls,
- quarantine,
- integrity checks,
- snapshots/checkpoints,
- recovery,
- audit logs,
- Forest Fire emergency procedures.

The model reasons and explains.

Deterministic systems enforce.

---

# 6. 🍎 McIntosh

## Role

McIntosh is the Forest's technical-support, diagnostics, troubleshooting, repair, and maintenance Tree.

Its workflow should be:

```text
symptom
→ evidence
→ hypotheses
→ low-risk/high-information test
→ update hypothesis
→ repair
→ verify
→ record known-good state
```

McIntosh must avoid random reboot/reinstall troubleshooting.

## Small / Technician
### ✅ Essential AI Rnj-1 Instruct

### Why Rnj-1 won

Rnj-1 maps unusually well to technical troubleshooting.

Relevant strengths include:

- coding,
- STEM,
- software-agent work,
- terminal/bash workflows,
- tool calling,
- debugging,
- iterative software repair,
- technical instruction following.

It behaves more like a compact technician than a generic chat model.

### Why use an 8B-class model instead of something smaller?

McIntosh Small does not need to be the smallest possible model.

It needs enough capability to handle:

- terminal commands,
- configs,
- logs,
- code,
- services,
- debugging loops,
- software-agent behavior.

The extra footprint is justified by specialization.

---

## Rnj-1 vs Rnj-1.5

Rnj-1.5 is technically the stronger successor on paper.

It brings:

- longer intended context,
- local/global attention improvements,
- more software-engineering agent training,
- stronger agent benchmark results.

But the production choice remains:

### ✅ Rnj-1 Instruct for now

The reason is deployment maturity.

Rnj-1 currently has the cleaner official local GGUF/llama.cpp path.

The Forest prioritizes:

```text
faithful local behavior
+
reproducibility
+
runtime maturity
```

over adopting a newer checkpoint before its deployment path is mature.

So:

```text
Rnj-1
→ production now

Rnj-1.5
→ future upgrade candidate
```

This is not a rejection of Rnj-1.5.

It is a deployment-timing decision.

---

## Big / Senior Engineer
### ✅ Magistral Small 1.2 24B

### Why Magistral won

McIntosh Big is the senior-engineer model.

It should handle:

- deep root-cause analysis,
- long reasoning chains,
- difficult debugging,
- conflicting evidence,
- complex code problems,
- multi-system failures,
- architectural troubleshooting.

### Why Magistral over Ministral 3 14B Reasoning?

Ministral is a better balanced reasoning/tool/vision agent.

Magistral won because McIntosh Big's defining need is **deep technical reasoning**, not visual perception.

In shorthand:

```text
Ministral
→ balanced reasoning agent

Magistral
→ deeper senior-engineer reasoning
```

### Vision caveat

The local GGUF path discussed does not preserve the same full vision capability.

That is acceptable because McIntosh's main Big role is technical diagnosis.

Visual evidence can be routed through another specialist or Tree when needed.

---

## McIntosh operating rules

McIntosh should:

- separate observation from interpretation,
- preserve evidence,
- prefer low-risk/high-information tests,
- snapshot before risky changes,
- verify repairs,
- keep repair journals,
- use targeted context instead of entire workspaces,
- escalate implementation-level defects to Bristlecone Pine when appropriate.

---

# 7. Major Rejected / Superseded Models

## LFM2.5-2.6B
Removed from foundational use because its custom license includes commercial/revenue-threshold concerns inconsistent with the Forest's stricter licensing rule.

## Muse Glimmer
Removed because separate usage-policy restrictions made it unsuitable under the clean-license standard.

## Apertus
Technically interesting and unusually open in several respects, but the additional Acceptable Use Policy conflicts with the current foundational-model license rule.

## Gemma 4 26B-A4B
Technically strong but deprioritized to avoid turning every Big slot into another Gemma model.

## Ministral 3 14B Reasoning
**Not rejected.**

It remains one of the strongest fallback/reference models in the project.

It narrowly lost Cedar Big to Phi because Cedar was intentionally specialized toward high-resolution GUI/screenshot reasoning.

It may still become Cedar Big if Phi's local multimodal deployment proves impractical.

---

# 8. Model-Family Diversity

The current Forest intentionally avoids one-family monoculture.

```text
🍒 Cherry
├── Microsoft Phi
├── Google Gemma
└── Ai2 OLMo

🍁 Maple
├── IBM Granite
├── Google Gemma
└── IBM Docling specialist

🌲 Cedar
├── Google Gemma
└── Microsoft Phi

🍎 McIntosh
├── Essential AI Rnj
└── Mistral Magistral
```

This spreads the Forest across:

- Microsoft,
- Google DeepMind,
- IBM,
- Ai2,
- Essential AI,
- Mistral.

That diversity is intentional because shared model-family weaknesses should not automatically propagate across every Tree.

---

# 9. Final Architecture at a Glance

```text
🌳 THE FOREST

🍒 CHERRY
├── Small   ✅ Phi-4 Multimodal Instruct 5.6B
├── General ✅ Gemma 4 E4B
└── Open    ✅ OLMo 3 7B-Instruct

🍁 MAPLE
├── Small   ✅ Granite 4.1 3B
├── Big     ✅ Gemma 4 E4B
└── Docs    ✅ Docling
             └── Granite Docling 258M on demand

🌲 CEDAR
├── Small   ✅ Gemma 4 E4B
└── Big     ✅ Phi-4 Reasoning Vision 15B

🍎 McINTOSH
├── Small   ✅ Rnj-1 Instruct
└── Big     ✅ Magistral Small 1.2 24B
```

---

# 10. Remaining Deployment Qualification

The selection phase is largely closed. What remains is deployment validation.

## Cherry
- Phi quantization
- image/audio latency
- resident RAM use
- tool reliability
- escalation behavior

## Maple
- Granite latency/RAM
- Docling document-ingestion benchmark
- Leaf Foliage export quality
- Workshop load/unload behavior

## Cedar
- Phi multimodal runtime qualification
- GUI/screenshot benchmark
- targeted 16K evidence packaging
- tool/policy integration
- keep Ministral 14B as deployment fallback

## McIntosh
- Rnj-1 local benchmark
- Magistral runtime/quantization benchmark
- revisit Rnj-1.5 once local support matures

---

# 11. Replacement Philosophy

These selections are **not permanent vendor commitments**.

The Forest should preserve stable Tree capabilities and benchmark suites so models can be swapped without redesigning the Tree.

A selected model remains selected only while it continues to satisfy:

1. role fit,
2. clean licensing,
3. provenance preference,
4. local deployment,
5. resource limits,
6. reliability,
7. benchmark performance,
8. Forest Workshop compatibility,
9. external-state compatibility,
10. acceptable failure behavior.

The architecture should outlive any individual model.
