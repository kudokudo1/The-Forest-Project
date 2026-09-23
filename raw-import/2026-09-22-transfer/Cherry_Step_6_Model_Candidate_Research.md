---
title: Cherry Model Candidates - Step 6 Research Pool
created: 2026-08-12
project: The Forest Project
tree: Cherry
phase: Model Selection
step: 6
status: research-pool
tags:
  - the-forest
  - cherry
  - llm
  - agent-model
  - model-selection
  - local-ai
  - open-weights
  - agentic-ai
  - multimodal
  - benchmarking
aliases:
  - Cherry Step 6
  - Cherry Candidate Research
  - Cherry LLM Candidate Pool
---

# Cherry Model Candidates — Step 6 Research Pool

## Purpose of This Note

This note captures **Step 6 of the Cherry model-selection process** for The Forest Project.

Step 6 is **not the final Cherry model selection** and is **not yet the formal shortlist**.

The goal of this stage is to identify the current model families that appear technically plausible for one or more Cherry roles, document why they are worth investigating, and record the major concerns that must be resolved before moving to Step 7.

The intended process is:

```text
Step 1 — Define the Tree's job
Step 2 — Define intelligence requirements
Step 3 — Define operational constraints
Step 4 — Define Forest-specific requirements
Step 5 — Define origin/licensing requirements
Step 6 — Research candidate pool          ← THIS NOTE
Step 7 — Shortlist 3–5 serious candidates
Step 8 — Build Tree-specific benchmarks
Step 9 — Select Small / Big / specialist models
```

The major architectural principle is:

> **We do not choose the model first and force Cherry around it. We define Cherry first, then choose models that fit Cherry.**

---

# 1. Cherry's Role Relevant to Model Selection

Cherry is intended to be the **primary general-purpose, user-facing Tree in The Forest**.

She is not simply a generic chatbot.

Cherry is expected to be:

- the first Tree most users meet
- the warmest and most personal Tree
- the generalist assistant for everyday tasks
- a guide into The Forest ecosystem
- capable of helping users install and configure Trees, Skills, and other Forest components
- capable of helping with scheduling, calendars, reminders, and ordinary life organization
- capable of using Forest-wide tools
- capable of recognizing when another Tree is better suited to a task
- capable of delegating specialist work
- capable of synthesizing specialist results
- capable of maintaining long-term personal continuity
- capable of using a private Diary memory layer without exposing it
- capable of maintaining a configurable personality or voice layer
- competent enough technically that unfamiliar tasks usually feel easy to the user
- **not** the dedicated deep technical-support Tree; that belongs to McIntosh

A strong Cherry model therefore needs more than benchmark intelligence.

It needs to combine:

```text
general intelligence
+ conversational warmth
+ style control
+ agent/tool reliability
+ structured output
+ retrieval discipline
+ memory discipline
+ delegation judgment
+ local efficiency
+ long-term trainability
```

---

# 2. Cherry's Small / Big Architecture

The current working assumption is that Cherry will probably benefit from at least two model roles.

## Cherry Small

The default everyday Cherry.

Likely responsibilities:

- normal conversation
- personal assistance
- reminders
- scheduling
- calendar interactions
- lightweight planning
- common Forest guidance
- common tool use
- simple retrieval
- Forest-wide Workshop use
- delegation decisions
- personality expression
- basic multi-step tasks

Desired properties:

- fast
- lightweight
- locally runnable
- relatively low RAM/VRAM
- strong instruction following
- strong function/tool calling
- warm conversational behavior
- good style control
- reliable structured output
- usable concurrently with other Trees

## Cherry Big

Escalation model for harder work.

Likely responsibilities:

- difficult reasoning
- complex planning
- deeper synthesis
- complex multi-step agent work
- difficult tool chains
- harder technical assistance
- nuanced context-heavy tasks
- ambiguous situations where Small is uncertain
- possibly stronger multimodal understanding

Desired properties:

- stronger reasoning than Small
- still good at agent/tool behavior
- compatible with Forest context targeting
- locally runnable if practical
- can sleep/unload when not needed
- does not need to remain resident

The user should ideally not have to manually choose Small versus Big for routine use.

---

# 3. Forest-Specific Requirements That Affect Candidate Research

A Cherry candidate should be evaluated as a **Forest-native agent**, not merely as a chat model.

Important requirements include:

## Dynamic Workshops

Cherry should work with **dynamically assembled Workshops** drawn from:

- a Forest-wide shared capability registry
- Cherry-specific capabilities

The Forest-wide registry may contain general tools such as:

- web search
- clarification
- to-do/task handling
- Crown jobs
- calendar
- reminders
- common retrieval tools
- other broadly useful capabilities

Shared does **not** mean always loaded.

The intended flow is:

```text
Forest-wide tool registry
        ↓
current task
        ↓
permission check
        ↓
relevant tools selected
        ↓
temporary Workshop
        ↓
Cherry
```

A candidate should therefore perform well with **small, task-specific tool sets**.

## Delegation

Cherry must recognize when:

```text
Cherry should handle task herself
```

versus:

```text
Maple / Cedar / McIntosh / another Tree should handle it
```

She must avoid both:

- over-delegating simple work
- trying to solve every specialist problem personally

## Structured Internal Communication

Cherry may need to generate compact task packets for other Trees.

Example:

```yaml
action: delegate
tree: mcintosh
reason: installation_failure
context_scope:
  - current_task
  - install_logs
priority: normal
```

The user does not need to see this structure, but the model needs to produce it reliably.

## Leaf Foliage

Cherry needs disciplined retrieval from long-term Forest knowledge.

She should:

- retrieve only relevant Leaves
- distinguish retrieved knowledge from current user instructions
- handle contradictions
- avoid loading the user's lifetime history into context
- summarize durable information accurately
- help create or update useful Leaves

## Diary

Cherry's Diary is a private memory class.

Diary information may influence Cherry, but:

```text
Diary → Cherry context
Diary ✕ ordinary direct disclosure
Diary ✕ other Trees
```

The real privacy boundary should be enforced by Forest architecture, not only by prompting.

## Runtime Portability

Cherry's identity should belong to The Forest, not to one runtime.

The model should ideally work through more than one compatible backend where possible.

Potential runtimes include:

- llama.cpp
- Ollama
- vLLM
- MLX
- SGLang
- other compatible serving systems

---

# 4. Step 5 Filters Carried Into Candidate Research

The candidate pool was screened with the following preferences.

## Strong Preferences

- open weights
- local inference
- clear licensing
- commercial use where practical
- quantization allowed
- fine-tuning allowed
- derivative deployment allowed
- strong runtime ecosystem
- strong documentation
- no mandatory remote inference dependency
- non-Chinese-developed models preferred when practical

## Important Clarification on Origin

The current rule is:

> **Non-Chinese development is a strong preference, not yet an absolute disqualifier.**

A similarly capable non-Chinese model should generally be preferred.

However, the project is not currently committed to accepting a dramatically weaker model solely for origin reasons.

This can be revisited later.

---

# 5. Current Candidate Pool

The initial Step 6 research pool contains:

1. Google DeepMind — Gemma 4
2. IBM — Granite 4.1
3. Ai2 — OLMo 3
4. OpenAI — gpt-oss
5. Liquid AI — LFM2.5
6. Mistral AI — Mistral Small 4
7. NVIDIA — Nemotron 3.5 Lightning

Additional older candidates remain possible as baselines, but they are not currently at the front of the pool.

---

# 6. Google DeepMind — Gemma 4

## Why It Entered the Pool

Gemma 4 appears unusually well aligned with Cherry because the family spans multiple deployment sizes while combining:

- local inference
- function calling
- configurable reasoning
- system-prompt support
- coding
- multimodal capabilities
- long context
- Apache 2.0 licensing
- multiple model sizes

This makes it one of the few families that might plausibly cover more than one Cherry role.

## Relevant Family Sizes

Current family sizes include:

- E2B
- E4B
- 12B
- 26B-A4B MoE
- 31B

### Possible Cherry Small

```text
Gemma 4 E4B
≈ 4.5B effective model size
≈ 8B including embeddings
128K context
text + image + audio
```

This is especially interesting for a lightweight local Cherry.

### Possible Cherry Small / Medium

```text
Gemma 4 12B
12B parameters
256K context
text + image + audio
```

This may provide a stronger everyday Cherry if hardware permits.

### Possible Cherry Big

```text
Gemma 4 26B-A4B
≈ 25.2B total parameters
≈ 3.8B active per token
256K context
```

The low active-parameter count is attractive for inference efficiency.

However, the full weight set still has to live somewhere in memory/storage.

## Strong Points for Cherry

- broad family size range
- multimodal path already exists
- native function calling
- configurable reasoning
- good ecosystem potential
- Apache 2.0
- quantization path
- fine-tuning path
- potentially useful for both Small and Big
- smaller variants specifically target local/mobile-class deployment
- strong long-context support

## Concerns

The biggest unknown is **personality quality**.

Cherry needs:

- warmth
- natural social behavior
- subtle long-term context use
- consistent personality
- graceful mode switching
- good personal-assistant behavior

None of these can be assumed from general capability benchmarks.

A technically strong Gemma model could still fail Cherry if it feels:

- sterile
- overly formal
- robotic
- repetitive
- poor at subtle style control
- too eager to expose memory/context

## Step 6 Status

**Very serious candidate family.**

## Most Likely Cherry Role

```text
Cherry Small: E4B or 12B
Cherry Big: 26B-A4B or 31B
```

Exact role depends on real local performance.

---

# 7. IBM — Granite 4.1

## Why It Entered the Pool

Granite 4.1 is particularly interesting because IBM explicitly focuses the family on areas that matter heavily to The Forest:

- instruction following
- tool calling
- conversation
- predictable agent behavior
- local/open deployment

The family appears more aligned with Forest agent infrastructure than its general popularity might suggest.

## Relevant Sizes

Current family includes:

- 3B
- 8B
- 30B

This produces a very clean possible Cherry architecture.

```text
Cherry Small
→ Granite 4.1 3B or 8B

Cherry Big
→ Granite 4.1 30B
```

## Strong Points for Cherry

- strong instruction-following focus
- strong tool-use focus
- conversational training emphasis
- Apache 2.0
- local deployment
- runtime support including llama.cpp
- runtime support including vLLM
- runtime support including SGLang
- potentially efficient everyday agent behavior
- good fit for structured Forest communication
- model family available at multiple practical sizes

IBM's emphasis on good behavior without requiring long reasoning traces may be especially valuable for Cherry Small.

Cherry does not need maximum deep reasoning for:

- setting reminders
- calling calendar tools
- searching memory
- selecting a Workshop
- routing a task
- answering routine questions

Fast correct action may be better than deep reasoning in these cases.

## Potential Weakness

The core Granite language models are not necessarily an integrated all-in-one multimodal solution in the same way as Gemma 4.

IBM uses separate models for areas such as:

- vision
- speech

This is not automatically a disadvantage.

The Forest architecture already allows a Tree to be a **system of multiple models**.

Cherry could potentially use:

```text
language model
+ vision model
+ speech model
```

without requiring one model to do everything.

## Main Research Question

Can Granite provide enough:

- warmth
- personality
- natural conversation
- subtle personal context handling

to feel like Cherry rather than an enterprise agent?

## Step 6 Status

**Very serious candidate, especially for Cherry Small.**

---

# 8. Ai2 — OLMo 3

## Why It Entered the Pool

OLMo 3 is arguably the most philosophically aligned candidate with the long-term Forest vision.

Ai2 emphasizes a deeply open development model rather than only releasing final weights.

The broader model flow includes:

```text
training data
training framework
checkpoints
post-training data
evaluation tools
weights
```

That matters if The Forest eventually wants to **train Cherry to become more specifically Cherry**.

## Relevant Sizes

OLMo 3 includes:

- 7B
- 32B

with variants including:

- Instruct
- Think

Potential Cherry architecture:

```text
Cherry Small
→ OLMo 3 7B-Instruct

Cherry Big
→ OLMo 3 32B-Instruct
or
→ OLMo 3 32B-Think
```

## Strong Points for Cherry

- strong openness
- U.S.-based development
- local weights
- strong research transparency
- tool use
- multi-turn dialogue
- instruction following
- reasoning variants
- coding
- long-context work
- extremely attractive future fine-tuning platform
- potentially ideal for Forest-specific post-training

## Why OLMo Could Matter Long Term

A major question for The Forest is whether Cherry remains:

> a prompted version of somebody else's general assistant

or becomes:

> a model deliberately trained for Forest behavior

OLMo makes the second path unusually accessible.

Potential future training targets include:

- Forest delegation
- Workshop selection
- memory discipline
- Leaf creation
- Diary discipline
- personality consistency
- Tree installation workflows
- Forest onboarding
- compact context distillation
- structured inter-Tree communication

## Concerns

The core question is whether OLMo's smaller models are **good enough today** for Cherry's user-facing experience.

We still need to test:

- warmth
- conversation quality
- latency
- hallucination behavior
- tool reliability
- structured output
- personality consistency
- long-session stability

A model can be excellent for research freedom and still be weaker as a daily assistant.

## Step 6 Status

**Serious candidate.**

Potentially the most important **training platform** in the pool.

---

# 9. OpenAI — gpt-oss

## Why It Entered the Pool

gpt-oss is attractive primarily because of:

- reasoning
- agent behavior
- tool use
- Apache 2.0 licensing
- local deployment
- efficient MoE architecture

The strongest immediate fit appears to be **Cherry Big**, not necessarily Cherry Small.

## Relevant Model

```text
gpt-oss-20b
≈ 21B total parameters
≈ 3.6B active per token
128K context
Apache 2.0
```

## Strong Points for Cherry

- strong reasoning
- strong agentic orientation
- tool use
- open-weight deployment
- Apache licensing
- relatively low active parameter count
- useful escalation model
- potentially good for harder Forest orchestration

## Likely Architecture

Rather than:

```text
Cherry Small = gpt-oss
Cherry Big   = gpt-oss
```

a more plausible approach may be:

```text
Cherry Small
→ warmer / faster general model

Cherry Big
→ gpt-oss-20b
```

## Concerns

The model's emphasis is heavily toward:

- reasoning
- STEM
- coding
- knowledge
- tools

That does not necessarily imply:

- warmth
- personality
- subtle personal interaction
- natural companionship
- good Diary-context use

It is also text-only.

That does not disqualify it, but it means multimodal Cherry would need separate components.

## Step 6 Status

**Strong Cherry Big/reasoning candidate.**

**Questionable as Cherry's everyday conversational core until tested.**

---

# 10. Liquid AI — LFM2.5

## Why It Entered the Pool

Liquid AI's LFM2.5 family is interesting because it directly targets **small local agentic models**.

This could make it one of the strongest candidates for an ultra-light Cherry Small or lightweight execution model.

## Relevant Models

### LFM2.5 1.2B Instruct

Potential ultra-light conversational/assistant model.

### LFM2.5 2.6B Agentic

```text
2.6B
128K context
local agent focus
planning
native tool calling
multi-step tasks
```

### LFM2.5 8B-A1B MoE

```text
≈ 8B total
≈ 1.5B active parameters
```

## Runtime Ecosystem

Potential deployment paths include:

- llama.cpp
- MLX
- vLLM
- SGLang
- ONNX

The family is particularly relevant to Forest experimentation because it targets local agent harnesses.

## Strong Points for Cherry

- very small
- fast local inference potential
- native agent orientation
- tool calling
- long context
- broad runtime support
- potentially excellent for always-available Cherry Small
- potentially good for mobile or low-power deployments

## Major Concern: License

Liquid's licensing is not as clean as Apache 2.0-only families.

The license includes commercial-use conditions that may matter if The Forest becomes a broadly distributed product.

This does not necessarily block personal Forest development, but it adds long-term product risk.

## Major Concern: Personality

An excellent small agent may still be a poor Cherry if it lacks:

- emotional nuance
- conversational depth
- long-term personality consistency
- subtle context interpretation
- warmth

This is one of the candidates where **agent capability and Cherry suitability may diverge sharply**.

## Step 6 Status

**Very interesting experimental Cherry Small candidate.**

**Licensing caveat.**

---

# 11. Mistral AI — Mistral Small 4

## Why It Entered the Pool

Capability-wise, Mistral Small 4 appears unusually close to the ideal conceptual Cherry.

It combines:

- general chat
- configurable reasoning
- multimodality
- coding
- agentic behavior
- long context
- Apache 2.0

## Architecture

Important values include roughly:

```text
119B total parameters
≈ 6B active per token
256K context
```

## Strong Points

- excellent capability mix
- configurable reasoning
- general chat
- multimodal
- agentic coding
- long context
- Apache 2.0
- strong fit conceptually with adaptive Cherry behavior

## Critical Problem: Hardware

Despite the name **Small**, the total model footprint is enormous.

Therefore:

```text
Mistral Small 4
≠ practical current Cherry Small
```

It may instead fit:

- future dedicated AI workstation
- remote self-hosted Cherry Big
- larger Forest server
- later-generation hardware

## Step 6 Status

**Excellent conceptual fit.**

**Poor fit for current local hardware.**

Keep on the long-term board rather than immediate Small-model testing.

---

# 12. NVIDIA — Nemotron 3.5 Lightning

## Why It Entered the Pool

Nemotron 3.5 Lightning is interesting because NVIDIA is positioning it for **multi-model agentic systems**.

That is directly relevant to The Forest.

The Forest itself is intended to be:

```text
multiple specialized Trees
+ shared capabilities
+ orchestration
+ routing
+ security
+ specialist escalation
```

## Strong Points

- agentic orientation
- multi-model-system orientation
- useful for orchestration
- customization/post-training potential
- potentially strong structured tool behavior
- philosophically aligned with Forest architecture

## Concern

The main concern is **role fit**.

Nemotron may be better suited for:

- infrastructure agents
- specialist Trees
- routing/execution layers
- coding agents
- background agents

than for:

- Cherry's warmth
- personal relationship
- Diary-aware behavior
- daily companionship

## Step 6 Status

**Watch closely.**

Possibly more interesting for another Tree than Cherry.

---

# 13. Older / Secondary Candidates

## Microsoft Phi-4 Mini

Reasons to retain as a baseline:

- lightweight
- edge/local focus
- native function calling
- established ecosystem

Concern:

- older generation relative to newer 2026 candidates

It may still be valuable as a **speed / footprint baseline**.

## Meta Llama 4

Still relevant as a major open-weight family.

However, its MoE footprint makes it less immediately attractive for an always-on Cherry Small.

It may remain worth evaluating for larger roles or ecosystem compatibility.

---

# 14. Preliminary Candidate Matrix

This table reflects **role relevance**, not final quality ranking.

| Family | Small Fit | Big Fit | Agent / Tool Fit | Warmth Potential | Multimodal | Licensing | Main Strength | Main Concern |
|---|---:|---:|---:|---:|---:|---|---|---|
| Gemma 4 | High | High | High | Unknown | Strong | Apache 2.0 | Broad all-around family | Personality must be tested |
| Granite 4.1 | High | Medium-High | High | Unknown | Separate models | Apache 2.0 | Tools + instructions + conversation | May feel enterprise-like |
| OLMo 3 | High | High | High | Unknown | Limited/varies | Very open | Trainability and openness | Daily assistant quality unknown |
| gpt-oss | Low-Medium | High | High | Unknown | No | Apache 2.0 | Reasoning + agent behavior | May be too reasoning-centric |
| LFM2.5 | High | Medium | High | Unknown | Limited | Caveated | Tiny local agent efficiency | License + personality |
| Mistral Small 4 | Low current | High future | High | Potentially strong | Strong | Apache 2.0 | Near-ideal capability mix | Huge total footprint |
| Nemotron 3.5 | Low-Medium | Medium-High | Very High | Unknown | Varies | Verify | Multi-agent systems | Possibly wrong Tree role |

---

# 15. Likely Cherry Role Mapping

## Cherry Small Candidates

Most interesting current research targets:

```text
Gemma 4 E4B
Gemma 4 12B
Granite 4.1 3B
Granite 4.1 8B
OLMo 3 7B-Instruct
LFM2.5 2.6B Agentic
LFM2.5 8B-A1B
```

Possible baseline:

```text
Phi-4 Mini
```

## Cherry Big Candidates

Most interesting current research targets:

```text
Gemma 4 26B-A4B
Gemma 4 31B
Granite 4.1 30B
OLMo 3 32B-Instruct
OLMo 3 32B-Think
gpt-oss-20b
```

Longer-term / larger-hardware candidate:

```text
Mistral Small 4
```

Possible agent-infrastructure candidate:

```text
Nemotron 3.5 Lightning
```

---

# 16. Why Benchmark Scores Alone Are Not Enough

Cherry's requirements include behaviors that standard public benchmarks do not adequately measure.

A model can perform extremely well on:

- math
- coding
- reasoning
- factual recall
- function calling

and still be a poor Cherry.

The Forest must test Cherry-specific behavior directly.

---

# 17. Cherry-Specific Qualities That Must Be Tested Ourselves

## Warmth

Does the model feel:

- natural
- attentive
- personal
- appropriately warm
- non-robotic

without becoming:

- overly flattering
- clingy
- repetitive
- melodramatic
- distracting

## Personality Consistency

Can it maintain a subtle configured personality across long conversations?

Potential traits may include:

- mild speech quirks
- apologetic tendencies
- playfulness
- formality
- other configurable behaviors

The exact personality-intensity system remains a **MAYBE**, not a locked decision.

## Mode Switching

Can Cherry move naturally between:

```text
warm personal conversation
→ serious planning
→ concise technical operation
→ tool call
→ warm conversation again
```

without losing identity or task precision?

## Diary Discipline

Can private context influence behavior without being directly revealed?

The true privacy boundary must still be architectural.

## Delegation Judgment

Does Cherry correctly decide:

```text
handle herself
vs
delegate to specialist
```

Examples:

- normal Forest installation → Cherry
- abnormal installation failure → McIntosh
- security decision → Cedar
- organization-heavy task → Maple

## Workshop Discipline

Can the model operate effectively with only the tools needed for the current task?

## Tool Hallucination

Does the model invent:

- tools
- parameters
- permissions
- results

that do not exist?

## Structured Output

Can it reliably produce machine-readable task packets without corrupting format?

## Context Distillation

Can Cherry send another Tree only the context that Tree needs?

## Retrieval Discipline

Can it use Leaf Foliage without:

- over-retrieving
- blindly trusting stale memory
- exposing irrelevant personal history
- flooding context

## Calendar and Reminder Reliability

Can it correctly understand:

- dates
- recurring events
- relative times
- reminders
- scheduling changes
- conflicts

## Forest Onboarding

Can the model help a new user understand The Forest without overwhelming them?

## Technical Generalist Behavior

Can Cherry handle routine setup confidently while recognizing when McIntosh is needed?

---

# 18. Hardware Considerations

Cherry Small has one of the strictest efficiency requirements in The Forest.

The default model should ideally:

- remain available frequently
- coexist with other Trees
- avoid monopolizing RAM/VRAM
- respond quickly
- tolerate useful quantization
- unload cleanly when necessary

Cherry Big can consume more resources because it can be:

- loaded on demand
- temporarily activated
- unloaded after difficult work

## Active Parameters vs Total Parameters

A model may advertise a low active-parameter count.

Example:

```text
25B total
3.8B active/token
```

This may improve compute efficiency.

However:

> **All model weights may still need to exist in memory or accessible storage.**

Therefore both values matter.

---

# 19. Licensing Comparison

## Strong / Clean Licensing

Especially attractive:

```text
Gemma 4
Granite 4.1
gpt-oss
Mistral Small 4
```

## Strong Openness

OLMo is especially attractive from an openness and research perspective.

## Licensing Caveat

```text
LFM2.5
```

requires extra attention before any broad commercial or distributed use.

---

# 20. Origin Preference

Current candidate families are primarily being drawn from developers outside China.

Examples include:

- Google DeepMind
- IBM
- Ai2
- OpenAI
- Liquid AI
- Mistral AI
- NVIDIA
- Microsoft
- Meta

This intentionally reflects the Forest's current preference to prioritize non-Chinese-developed technology/models when practical.

Origin should still be evaluated alongside:

- actual model derivation
- licensing
- base architecture
- research provenance
- ownership/control of weights

---

# 21. Strategic Questions Before Step 7

## Same Family or Mixed Family?

Should Cherry Small and Cherry Big come from the same family?

Advantages:

- shared tokenizer
- similar prompting
- simpler maintenance
- potentially easier escalation

Disadvantages:

- forces compromise
- best Small may not have the best Big sibling
- personality may differ across sizes anyway

Current conclusion:

> **Do not require the same family.**

## One Multimodal Model or Specialists?

The Forest may use:

```text
Cherry language model
+ vision model
+ speech model
```

instead of requiring one model to do everything.

Current conclusion:

> **Multimodal integration is valuable but not mandatory if it harms core Cherry quality.**

## How Much Reasoning Does Everyday Cherry Need?

Cherry Small should probably optimize for:

```text
speed
+ reliability
+ warmth
+ tool use
```

Cherry Big can provide:

```text
deep reasoning
+ difficult synthesis
+ complex planning
```

## Should Cherry Be Fine-Tuned Later?

Probably yes.

Potential future training targets:

- personality
- Forest vocabulary
- Workshop selection
- tool discipline
- delegation
- memory extraction
- Diary discipline
- onboarding
- Forest technical assistance
- inter-Tree communication

---

# 22. Current Research Board

## Highest-Interest Families

### Gemma 4

Why:

- multiple useful sizes
- multimodal
- permissive licensing
- function calling
- configurable reasoning
- plausible Small and Big paths

### Granite 4.1

Why:

- strong alignment with tools
- instruction following
- conversation
- clean local deployment
- potentially excellent Cherry Small

### OLMo 3

Why:

- exceptional openness
- strong long-term training path
- serious Instruct and Think variants
- compatible with Forest ownership philosophy

## Strong Role-Specific Candidate

### gpt-oss

Likely:

```text
Cherry Big / reasoning escalation
```

## Experimental Efficiency Candidate

### LFM2.5

Likely:

```text
ultra-light Cherry Small / agent model
```

with licensing caveat.

## Future Hardware Candidate

### Mistral Small 4

Conceptually strong but currently too large for the intended local footprint.

## Watch Candidate

### Nemotron 3.5 Lightning

Potentially more suitable for agent infrastructure or another Tree.

---

# 23. What Step 7 Should Do

Step 7 should cut the pool down to roughly:

```text
3–5 serious candidates
```

for actual Cherry testing.

A useful shortlist may include separate categories:

## Small Shortlist

3–5 candidates for everyday Cherry.

## Big Shortlist

3–5 candidates for escalation Cherry.

Some models may appear in both.

Step 7 should consider:

- realistic local hardware fit
- model origin
- license
- runtime support
- agent/tool capability
- personality potential
- context behavior
- training potential
- multimodal path
- expected quantization quality

---

# 24. What Step 8 Should Benchmark

The eventual Cherry benchmark should include at least:

## Conversation

- warmth
- naturalness
- personality persistence
- correction handling
- ambiguity handling

## Diary

- subtle context use
- non-disclosure
- privacy-boundary cooperation

## Memory

- retrieval
- contradiction handling
- durable-memory extraction

## Tools

- correct selection
- correct parameters
- no invented tools
- graceful tool failure

## Workshops

- small tool set
- dynamically changed tool set
- no confusion after Workshop switch

## Delegation

- correct Tree selection
- no unnecessary delegation
- specialist-result synthesis

## Scheduling

- calendar event creation
- recurring schedule interpretation
- reminders
- conflict handling

## Forest Setup

- install a normal Skill
- install a normal Tree
- recognize when installation needs McIntosh
- explain permissions

## Structured Output

- JSON/YAML/task-packet reliability

## Performance

- first-token latency
- total response latency
- tokens/second
- RAM
- VRAM
- CPU/GPU utilization
- context scaling

## Quantization

Each serious model should be compared across plausible quantizations.

A smaller quantization should not automatically win if it noticeably damages:

- warmth
- context handling
- tool reliability
- personality
- structured output

---

# 25. Overall Step 6 Conclusion

The current research suggests Cherry should probably **not** be built around one universally dominant model.

The strongest architecture currently appears to be:

```text
Cherry
│
├── Small
│   ├── fast
│   ├── warm
│   ├── agent-capable
│   ├── tool-reliable
│   └── frequently available
│
├── Big
│   ├── stronger reasoning
│   ├── complex planning
│   ├── deeper synthesis
│   └── on-demand
│
├── Forest-wide Workshop access
│
├── Cherry-specific capabilities
│
├── Leaf Foliage
│
├── private Diary
│
└── personality / voice layer
```

The most compelling current model families are:

```text
Gemma 4
Granite 4.1
OLMo 3
```

with:

```text
gpt-oss
```

especially interesting for Cherry Big,

and:

```text
LFM2.5
```

especially interesting for ultra-light local agent experiments.

Mistral Small 4 remains strategically interesting but appears too large for the current local Cherry target.

Nemotron 3.5 Lightning should remain on the broader Forest model board because it may fit a specialist or infrastructure Tree better than Cherry.

The most important unresolved question is not:

> "Which candidate has the highest benchmark score?"

It is:

> **Which candidate can become Cherry?**

That means the final decision must heavily weight:

- warmth
- personality
- memory discipline
- Diary behavior
- Forest tool use
- Workshop compatibility
- delegation
- reliability
- local efficiency

These must be tested directly inside a Cherry-specific benchmark.

---

# 26. Source Notes From Step 6 Research

Official/current sources consulted during the Step 6 research pass included:

- Google AI / Gemma documentation  
  https://ai.google.dev/gemma/docs/core/model_card_4

- IBM Research / Granite  
  https://research.ibm.com/blog/granite-4-1-ai-foundation-models

- Ai2 / OLMo  
  https://allenai.org/olmo

- Ai2 OLMo 3 research  
  https://allenai.org/papers/olmo3

- OpenAI / gpt-oss  
  https://openai.com/index/introducing-gpt-oss/

- Liquid AI / LFM2.5  
  https://www.liquid.ai/blog/lfm2-5-2-6b

- Liquid AI documentation  
  https://docs.liquid.ai/

- Liquid AI license  
  https://www.liquid.ai/lfm-license

- Mistral AI / Mistral Small 4  
  https://mistral.ai/news/mistral-small-4/

- NVIDIA / Nemotron  
  https://blogs.nvidia.com/

These should be re-verified before final implementation because model releases, runtimes, and license terms can change.

---

# 27. Status

```text
Cherry Step 1 — Defined
Cherry Step 2 — Defined
Cherry Step 3 — Defined
Cherry Step 4 — Defined
Cherry Step 5 — Defined
Cherry Step 6 — Research pool documented
Cherry Step 7 — NEXT
```

Step 7 should narrow the research pool into a manageable Cherry Small and Cherry Big shortlist before serious benchmarking begins.
