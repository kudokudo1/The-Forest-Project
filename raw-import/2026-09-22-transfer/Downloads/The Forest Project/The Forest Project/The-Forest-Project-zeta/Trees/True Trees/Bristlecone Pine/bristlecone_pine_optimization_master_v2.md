---
type: Optimization Plan
tree: Bristlecone Pine
project: The Forest
status: active-reference
source: Chat GPT+ User
tags:
  - AI
  - bristlecone-pine
  - knowledge-management
  - Trees
  - the-forest
  - Optimization
  - architecture
  - bristlecone
created: 2026-08-07
updated:
---
# BRISTLECONE PINE OPTIMIZATION MASTER FILE — V2

**Updated:** 2026-08-07  
**Project:** The Forest  
**Tree:** Bristlecone Pine  
**Role:** Treewright  

## Purpose

This file is designed to be dropped into a new ChatGPT chat or another AI so work can continue without rebuilding the Bristlecone optimization project.

It contains:

- the original optimization plan,
- user-confirmed decisions,
- completed work,
- measured benchmarks,
- failed experiments,
- current Hermes/Newelle decisions,
- Qubes compatibility and access boundaries,
- Quick/Standard/Deep plans,
- automatic mode-routing ideas,
- tool-routing and Workshop plans,
- Ollama/Qubes/retrieval optimization plans,
- Maple/Seed training plans,
- PyTorch/Unsloth plans,
- and assistant-originated suggestions clearly separated from user-confirmed project decisions.

---

# A. STATUS LEGEND

- ✅ **Confirmed complete** — user explicitly confirmed it was done/fixed.
- 🧪 **Measured/tested** — actually benchmarked or tried.
- ❌ **Failed / poor result** — timed out, failed, or performed badly in the tested form.
- ⏸️ **Paused/deferred** — intentionally not in the active path right now.
- ⬜ **Pending** — planned but not implemented and confirmed.
- ❓ **Needs investigation** — not enough evidence yet.
- 💡 **Idea** — possible future direction.
- 🤖 **Assistant-originated suggestion** — assistant proposal only; not automatically a user decision.

**Rule:** Never mark a pending item complete unless the user confirms it was implemented and tested.

---

# B. CURRENT AUTHORITATIVE STATUS

## Confirmed complete

- ✅ Unnecessary Hermes skills were disabled.
- ✅ `humanizer` was disabled; Bristlecone's Tree voice belongs in his Grain/SOUL/personality.
- ✅ Hermes automatic auxiliary title generation was disabled.
- ✅ The title-generation timeout problem was confirmed fixed.
- ✅ The user has chosen Hermes as Bristlecone's primary operating/orchestration layer for now.
- ✅ Newelle is no longer preferred in Bristlecone's normal daily request path.

## Still pending

- ⬜ Permanent lean Hermes launch configuration.
- ⬜ Quick / Standard / Deep modes.
- ⬜ Automatic Mode Router.
- ⬜ Task-specific Hermes Workshops.
- ⬜ Qubes/Cherry-AI resource tuning.
- ⬜ Ollama tuning.
- ⬜ Structure-aware code retrieval.
- ⬜ Web/database/memory/document retrieval optimization.
- ⬜ Full benchmark suite.
- ⬜ Maple Seed Nursery implementation.
- ⬜ PyTorch/Unsloth Model Workshop.
- ⬜ LoRA/QLoRA training workflow.

---

# C. CURRENT PREFERRED ARCHITECTURE

```text
Qubes OS
├── dom0
│   └── administration only; no unrestricted AI access
│
├── Cherry-AI
│   ├── Hermes
│   ├── Bristlecone Pine profile
│   └── Ollama
│
├── Maple
│   ├── normal development/personal environment
│   ├── possible lightweight Maple-local AI
│   └── possible Seed Nursery
│
└── future isolated Workshops
    ├── Model Workshop
    ├── Retrieval Workshop
    ├── Research Workshop
    └── other narrowly scoped services
```

### Current interface decision

```text
Hermes = primary Bristlecone brain/orchestrator/interface
Newelle = paused/optional future Bark or specialist interface
Ollama = model server
```

The older continuity material below may still describe Newelle as part of the active Cherry-AI stack. **That is historical context and is superseded by this section.**

---

# D. MEASURED PERFORMANCE RESULTS

These are actual user-run measurements from the current investigation.

| Path / Toolset                            |              Reasoning |                                     Result |
| ----------------------------------------- | ---------------------: | -----------------------------------------: |
| Direct Ollama `/api/generate` test        | model thinking present |                           ~13.75 sec total |
| Direct Ollama OpenAI-compatible streaming |                   none |                             **23.477 sec** |
| Hermes `todo` only                        |                   none |                             **~22–24 sec** |
| Hermes tiny-tool test                     |                 medium |                                **1:07.70** |
| Hermes `file,terminal`                    |                   none |                                 **41 sec** |
| Hermes `file,terminal,todo`               |                   none |                                **1:49.64** |
| Hermes `file,terminal,skills`             |                   none |                                **2:42.40** |
| Hermes `file,terminal,skills,todo`        |                   none |                                **2:49.16** |
| Broad/full 27-tool Hermes setup           |                   none |                                 **~3 min** |
| Normal Newelle-backed Bristlecone         |                 varied | repeatedly **~10 min before visible text** |

### Direct Ollama timing breakdown from one raw test

Approximate values read from Ollama's returned metrics:

- Total duration: **~13.75 sec**
- Load duration: **~9.98 sec**
- Prompt evaluation: **~1.31 sec**
- Generation: **~2.46 sec**

### Prompt/tool measurements after skill pruning

Approximate current screenshot values:

```text
System prompt total: 20,584 B (~20.1 KB)
Skills index:         3,680 B (~3.6 KB)
Tool schemas:        44,800 B (~43.8 KB)
Tool count:          27
```

Earlier skill index was about **6.7 KB**, so skill pruning reduced that portion substantially.

### Benchmark conclusion

The major measured latency factors are:

1. **Hermes tool-schema size/complexity**
2. **Reasoning effort**
3. **Tool combinations**
4. **Newelle in the Hermes request path**
5. Possibly long history/context and frontend/API streaming behavior

The raw Ollama model itself does **not** explain the 5–15 minute Newelle delays.

---

# E. NEWELLE TESTS — FAILED / PAUSED PATH

Newelle's duplicate prompt/tool features were reduced for testing.

Potential duplicated Newelle layers included:

- Helpful Assistant prompt
- Environment Information
- Tools prompt
- Todo prompt/system
- Skills prompt/system
- memory/RAG/context features
- Newelle's own agent/tool layer on top of Hermes

## Stripped-down Newelle benchmarks

### Run 1
🧪 Output appeared after:

**5:25.65**

### Run 2
❌ Failed:

- approximately **15 minutes**
- no Bristlecone answer
- user considered the run failed

### Run 3
❌ Failed:

- approximately **5:42.23**
- Newelle showed/returned to its suggested-prompt/welcome state rather than a Bristlecone answer

### Prior normal Newelle behavior
❌ Multiple runs around **10 minutes before visible words appeared**.

## Current decision

⏸️ **Pause Newelle in Bristlecone's daily path.**

The user currently prefers Hermes because of:

- learning features,
- multi-model features,
- long-term Forest integration,
- and much better current measured performance.

Newelle may be revisited later as a visual Bark/interface or Maple-local assistant.

---

# F. CURRENT FASTEST PRACTICAL TREEWRIGHT PATH

Current best practical measured path:

```text
Hermes
→ reasoning none
→ file + terminal toolsets
→ Ollama
```

Measured simple-prompt latency:

**41 seconds**

This is slower than direct Ollama (~23 sec), but it retains core Treewright file and terminal abilities.

The following are currently poor defaults for routine work:

- ❌ `file,terminal,todo` — 1:49.64
- ❌ `file,terminal,skills` — 2:42.40
- ❌ `file,terminal,skills,todo` — 2:49.16
- ❌ full/broad Hermes tools — ~3 min

---

# G. TODO AND SKILLS TOOLSET FINDINGS

## Hermes `todo`

Purpose:

- internal task-list management,
- keeping track of multi-step work,
- marking work pending/in-progress/completed during a session.

It does not itself:

- speed inference,
- run commands,
- replace persistent Forest records,
- schedule reminders.

Current project direction:

- Keep `todo` out of the lean everyday Workshop.
- Use it only for long, complicated, multi-stage work if its reliability benefit justifies the latency.

## Hermes `skills` toolset

Current measured effect is large.

`file,terminal`:
- 41 sec

`file,terminal,skills`:
- 2:42.40

Current project direction:

- Keep the `skills` toolset out of Bristlecone's fastest everyday Workshop.
- Use it in a specialized Skill/Agent Development Workshop when Bristlecone actually needs to inspect, manage, create, or invoke skills.

---

# H. UPDATED MASTER CHECKLIST

1. ✅ Disable unnecessary Hermes skills
2. ✅ Disable failing automatic Hermes title generation
3. ⬜ Establish permanent lean Hermes default/workshop
4. ⬜ Optimize Qubes OS, Cherry-AI, and background-qube resources
5. ⬜ Tune Hermes performance settings
6. ⬜ Tune Ollama runtime/model loading
7. ⬜ Configure task-based tool routing and Workshops
8. ⬜ Add Quick Mode
9. ⬜ Add Standard Mode
10. ⬜ Add Deep Mode
11. ⬜ Add Automatic Mode Router
12. ⬜ Add task continuity / anti-oscillation rules
13. ⬜ Implement structure-aware block-level code retrieval
14. ⬜ Optimize web/database/memory/document retrieval
15. ⬜ Run full benchmark suite and isolate remaining bottlenecks
16. ⬜ Build Maple Seed Nursery / Seed-development workflow
17. ⬜ Audit GPU feasibility and Qubes passthrough compatibility
18. ⬜ Build isolated PyTorch + Unsloth Model Workshop
19. ⬜ Begin LoRA/QLoRA only after evaluation infrastructure exists
20. ⬜ Review results and choose the next optimization stage

---

# I. QUBES COMPATIBILITY / ACCESS BOUNDARIES

## Cherry-AI boundary

Because Bristlecone runs in Cherry-AI, ordinary Bristlecone tools can access only Cherry-AI by default:

- Cherry-AI files
- Cherry-AI processes
- Cherry-AI applications/windows
- devices attached to Cherry-AI
- network resources permitted to Cherry-AI

Bristlecone cannot automatically access:

- Maple files/processes/windows
- other AppVMs
- dom0

## Cross-qube integration

Future controlled options:

- narrow qrexec services
- Git-based exchange
- approved Qubes file copy
- controlled local APIs

Preferred pattern:

```text
Bristlecone in Cherry-AI
        ↓
specific approved qrexec service
        ↓
small helper inside Maple
        ↓
specific result
```

Examples:

- return Git status
- run approved tests
- search an approved repository
- return logs
- apply a reviewed patch

Avoid unrestricted cross-qube shells or general GUI control.

## dom0

Bristlecone should not receive unrestricted dom0 access.

Any future dom0 automation should be narrowly scoped, permission-gated, logged, and reversible.

---

# J. QUICK / STANDARD / DEEP + AUTOMATIC ROUTING

## Quick Mode

For:

- routine questions
- status checks
- simple commands
- familiar reversible edits
- small file operations

Intended behavior:

- none/minimal/low reasoning — final value still needs benchmark selection
- small context
- smallest safe toolset
- low search/tool budget

## Standard Mode

For:

- normal coding
- moderate debugging
- documentation
- ordinary research
- limited-risk changes

Intended behavior:

- low/medium reasoning
- moderate context
- normal verification
- task-specific Workshop

## Deep Mode

For:

- architecture
- difficult debugging
- multi-file changes
- migrations
- security-sensitive work
- high-impact decisions
- unfamiliar systems
- conflicting evidence
- root-cause investigation

Intended behavior:

- high reasoning
- larger context only when needed
- more verification/tests
- greater tool/search budget
- rollback planning

**Important:** Deep Mode should not mean "load every tool."

## Automatic Mode Router

Desired behavior:

```text
User prompt
    ↓
deterministic classification first
    ↓
small classifier only if ambiguous
    ↓
Quick / Standard / Deep
    +
Workshop
    +
context budget
    +
tool-turn budget
    ↓
Bristlecone
```

Rules:

- classify before the main model call
- default to Standard when uncertain
- escalate automatically when complexity/risk rises
- do not downgrade an unresolved Deep task
- use task continuity/hysteresis to avoid mode bouncing
- explicit user commands override automatic routing
- never silently switch to an expensive cloud model
- avoid main-model switching if it causes costly Ollama reloads

---

# K. WORKSHOP PLAN

## Lean / Everyday Treewright
Current leading measured candidate:

```text
file
terminal
```

## Code Workshop
Planned:

- repository navigation
- symbol index
- LSP
- Tree-sitter
- Git
- tests
- formatter/linter
- build tools
- restricted terminal
- code-specific docs/memory

## Research Workshop
Planned:

- web search
- page extraction
- official docs
- PDF/document handling
- source verification
- research cache
- optional SearXNG

## System Workshop
Planned:

- Qubes diagnostics
- Linux administration
- service management
- resource monitoring
- package/config inspection
- high-risk approval controls

## Model Workshop
Planned:

- PyTorch
- Unsloth
- LoRA/QLoRA
- dataset preparation
- model evaluation
- quantization/conversion
- checkpoints
- local-model export

## Retrieval Workshop
Planned:

- keyword search
- vector search
- embeddings
- reranking
- indexing
- metadata filtering
- caching

## Memory Workshop
Planned:

- temporary context
- project memory
- user preferences
- long-term knowledge
- correction/forgetting/archive
- access-control enforcement

---

# L. MAPLE / SEED TRAINING DIRECTION

The user expects Seeds to need **both**:

## Behavioral cultivation

Does not change model weights.

Includes:

- role
- Grain/SOUL/personality
- permissions
- memory behavior
- tool/workshop rules
- Quick/Standard/Deep behavior
- examples
- tests
- correction behavior
- evaluation rubrics

## Model-weight training

Changes weights or adapter weights.

Potential targets:

- Forest terminology
- tool-selection behavior
- ADR/record formatting
- Qubes-safe procedures
- coding conventions
- mode behavior
- stable role adherence

Preferred first training approaches:

- LoRA
- QLoRA

Full fine-tuning is later-stage.

## Proposed Seed cycle

```text
1. Bristlecone designs Seed behavior.
2. Maple prepares examples/evaluations.
3. Test without weight training.
4. Categorize failures.
5. Fix prompt/tool/memory/routing problems first.
6. Turn persistent learnable failures into reviewed training data.
7. Train a LoRA/QLoRA candidate in the Model Workshop.
8. Compare candidate against baseline.
9. Bristlecone reviews improvements/regressions.
10. User approves promotion, revision, or rejection.
```

---

# M. PYTORCH / UNSLOTH

PyTorch is the underlying machine-learning computation framework.

Unsloth is an optimized training workflow that uses PyTorch/Hugging Face tooling.

Relationship:

```text
Seed training
    ↓
Unsloth
    ↓
PyTorch
    ↓
CPU/GPU hardware
```

Current conclusion:

- PyTorch + Unsloth can support future Seed weight training.
- Installing them does not magically make CPU-only LLM training fast.
- A suitable GPU would matter greatly for real fine-tuning.
- Training dependencies should eventually live in an isolated Model Workshop rather than stable Cherry-AI.

Before GPU passthrough:

- identify exact GPU(s)
- VRAM
- display attachment
- IOMMU groups
- Qubes compatibility
- rollback path

---

# N. ASSISTANT-ORIGINATED SUGGESTIONS — NOT USER-CONFIRMED

The user explicitly asked that assistant additions be clearly separated. Everything in this section is an assistant proposal unless the user later adopts it.

## 🤖 Suggestion 1: make `file,terminal` the initial default Workshop

Reason:
It currently offers the best measured balance of useful Treewright capability and latency.

This has **not** yet been marked as permanently configured.

## 🤖 Suggestion 2: keep `todo` out of Quick Mode

Use it only for long multi-stage work because combined-tool benchmarks show significant latency.

## 🤖 Suggestion 3: keep `skills` out of the default Workshop

Expose it only when managing/invoking skills because it caused the largest tested toolset slowdown.

## 🤖 Suggestion 4: keep reasoning mode separate from Workshop selection

Example:

```text
Reasoning = Quick / Standard / Deep
Workshop = Code / Research / System / Model / Retrieval / Memory
```

This avoids Deep Mode automatically receiving every tool.

## 🤖 Suggestion 5: deterministic routing before a model router

Use cheap rules for obvious task classes; call a small classifier only for ambiguous requests.

## 🤖 Suggestion 6: keep one main model warm before experimenting with frequent model switching

First vary:

- reasoning
- context
- toolset
- retrieval depth

before switching main models per prompt.

## 🤖 Suggestion 7: use Maple as a lightweight Seed Nursery first

Start with behavioral Seed work, datasets, and evaluations before creating a dedicated training qube.

## 🤖 Suggestion 8: use narrow qrexec services rather than broad cross-qube access

Expose only specific actions required for Forest collaboration.

## 🤖 Suggestion 9: revisit Newelle only after Hermes is stable

Possible later roles:

- Bark
- visual dashboard
- voice frontend
- Maple-local assistant

---

# O. IMMEDIATE NEXT STEPS

1. ⬜ Make the lean Hermes path easy/repeatable.
2. ⬜ Repeat `file,terminal` benchmark several times and record median.
3. ⬜ Audit exact CPU/RAM/storage/Qubes settings.
4. ⬜ Tune Qubes/Cherry-AI one variable at a time.
5. ⬜ Tune Ollama keep-alive/model concurrency/context.
6. ⬜ Implement Quick/Standard/Deep.
7. ⬜ Implement task-based Workshops.
8. ⬜ Add Automatic Mode Router.
9. ⬜ Improve code/document retrieval.
10. ⬜ Build Seed behavioral evaluation pipeline.
11. ⬜ Audit GPU feasibility.
12. ⬜ Build isolated PyTorch/Unsloth Model Workshop later.

---

# P. HISTORICAL / FULL CONTINUITY MATERIAL

The remainder of this file preserves the earlier full continuity packet and original detailed optimization plan.

**Important:** Where the older material conflicts with sections A–O above, the newer sections above are authoritative.

---

# BRISTLECONE PINE CONTINUITY PACKET

**Version:** 1.1  
**Created:** 2026-08-06  
**Purpose:** Restore the full working context for Bristlecone Pine’s speed, reliability, Qubes architecture, Seed development, and future training work in a new ChatGPT conversation or another AI system.

## Instructions to the receiving AI

1. Treat this packet as the current continuity source for the project.
2. Preserve the user’s terminology: **The Forest**, **Trees**, **Seeds**, **Treewright**, **Grain**, **Branches**, **Workshops**, **Cherry-AI**, **Maple**, and **Bristlecone Pine**.
3. Do not mark a pending item complete until the user confirms that it was configured and tested.
4. Distinguish carefully between:
   - confirmed changes,
   - planned changes,
   - provisional recommendations,
   - measurements still needed.
5. Preserve Qubes OS isolation. Do not recommend broad cross-qube or dom0 access merely for convenience.
6. Prefer free, open-source, local-first, private, and self-hostable approaches.
7. Explain commands before the user runs them. Change one major variable at a time and preserve rollback paths.
8. Do not assume commands, settings, ports, models, or hardware details remain current. Inspect the installed versions and configuration first.
9. Keep the active checklist visible regularly while this optimization project is underway.
10. When information in this packet conflicts with a later direct statement from the user, follow the user’s newer statement and update the packet.

## Project identity

- **Bristlecone Pine** is the first Tree and serves as **Treewright**.
- The Treewright helps design, train, code, test, correct, document, and maintain Cherry, Maple, future Tree species, plugins, add-ons, Seeds, and Forest infrastructure.
- Bristlecone’s healthy-status phrase is **“Pine is fine.”**
- His Tree voice should come from his **Grain/SOUL/personality instructions**, not from a generic Humanizer skill.
- Tree and woodworking language should be natural and occasional, not forced into every response.

## Confirmed status at handoff

- **Confirmed complete:** The user disabled Bristlecone’s unnecessary Hermes skills.
- **Not yet confirmed complete:** Quick/Standard/Deep aliases, automatic mode routing, Qubes resource tuning, Newelle/Hermes tuning, Ollama tuning, workshops, retrieval optimization, benchmarking, or PyTorch/Unsloth installation.
- The exact final enabled-skill list was not captured after the user finished pruning it. Audit and record it later.
- Do not infer that a recommendation was applied merely because it appears in this packet.

## Current high-level architecture

```text
Qubes OS host
├── dom0
│   └── Administration only; no unrestricted AI access
├── Cherry-AI qube
│   ├── Newelle interface
│   ├── Hermes agent/orchestrator
│   ├── Bristlecone Pine profile
│   └── Ollama model serving
├── Maple qube
│   ├── User’s personal/development environment
│   └── Possible Seed Nursery or Maple-local AI
└── Future isolated workshops
    ├── Model Workshop / Seed Nursery
    ├── Retrieval Workshop
    ├── Research Workshop
    └── other narrowly scoped services
```

### Qubes access boundary

- Because Bristlecone runs in **Cherry-AI**, his ordinary file, terminal, process, and GUI tools can access **Cherry-AI only**.
- He cannot automatically read Maple’s files, control Maple’s applications, inspect other qubes, or administer dom0.
- Selected cross-qube actions can later be exposed through narrow, policy-controlled **qrexec** services.
- Prefer specific services such as “run tests in this repository” or “return Git status,” not unrestricted remote shells.
- Any dom0-related operation should remain highly constrained, reviewed, logged, and permission-gated.
- Direct GUI control of Maple would require a helper inside Maple and carries more risk than controlled command or file operations.

## Hermes skill decisions

### Important behavior

Hermes presents skills with only two user-selectable states:

- **Enabled**
- **Disabled**

There is no separate “On Demand” toggle. Enabled skills are already progressively loaded: their short index entries are available, while their full skill instructions are loaded only when invoked or selected.

### Confirmed decisions

- `humanizer`: disabled; Bristlecone’s Tree voice belongs in his Grain/SOUL.
- Unrelated creative, presentation, office, entertainment, and external-service skills were considered unnecessary for his normal Treewright role.
- The user then confirmed that all unnecessary skills had been turned off.

### Previously discussed skill meanings

- `ascii-art`: creates pictures, banners, and decorative text using terminal characters; cosmetic, not core.
- `dogfood`: exploratory user-perspective testing of a web application; useful when testing a Forest web interface, otherwise unnecessary.
- `inspecting-hermes-desktop-dom`: inspects the live DOM/CSS/console of Hermes Desktop specifically; useful only when developing Hermes Desktop itself.
- `node-inspect-debugger`: advanced Node.js/JavaScript/TypeScript debugging with breakpoints, call stacks, variables, and profiling.
- `weights-and-biases`: experiment tracking for machine-learning runs, metrics, configurations, checkpoints, and comparisons; useful later for formal training/evaluation, not required for basic local model use.
- `claude-code`, `codex`, and `opencode`: external coding-agent systems, not merely models. OpenCode was recommended provisionally because it is open-source and provider-flexible, but Bristlecone does not need all three enabled.

### Core Treewright capabilities previously recommended

- File and repository inspection
- Safe file editing and patching
- Restricted terminal execution
- Git inspection, diffs, rollback points, and review
- Tests, linters, type checking, and builds
- Logs, stack traces, and diagnostics
- Project-specific records and limited memory
- Documentation and change reports

Specialized capabilities should be exposed through task-specific workshops rather than loaded universally.

## Baseline prompt/tool observation from an earlier screenshot

The earlier Hermes report appeared to show approximately:

- System prompt: **22.7 KB**
- Tool schemas: **43.8 KB across 27 tools**
- Skill index: **6.7 KB across roughly 65 skills**

Treat these as screenshot-derived preliminary values. Re-run the report after skill pruning and record the exact current values.

The main implication was that **tool schemas were a larger always-loaded burden than the skill index**, so tool routing and small workshops may produce a larger improvement than skill pruning alone.

## Reasoning modes

The intended modes are:

### Quick Mode
- Low or minimal reasoning
- Smallest safe context
- Minimal toolset
- Low tool-turn budget
- Routine, familiar, reversible, low-risk work

### Standard Mode
- Medium reasoning
- Moderate context and tool budget
- Normal coding, planning, research, and debugging

### Deep Mode
- High reasoning
- Larger context only when justified
- Broader dependency retrieval
- More verification, testing, logs, and rollback planning
- Architecture, difficult debugging, multi-file changes, migrations, security-sensitive work, unfamiliar systems, or high-impact decisions

Potential aliases were discussed:

```text
/quick
/standard or /balanced
/deep
```

These aliases are **pending**. Do not claim they exist until the user adds and tests them.

## Automatic Mode Router — added design

The user wants Bristlecone to switch modes automatically instead of manually entering commands.

### Required behavior

1. Classify a new task **before** the main Bristlecone request runs.
2. Select Quick, Standard, or Deep.
3. Select the matching workshop, toolset, context budget, retrieval depth, tool-turn budget, and verification level.
4. Use deterministic rules for obvious tasks.
5. Use a small, fast local classifier only for ambiguous cases.
6. Default to Standard when confidence is low.
7. Default to Deep for destructive, security-sensitive, architectural, migration, cross-system, or high-impact work.
8. Permit automatic escalation when complexity, risk, uncertainty, or repeated failures increase.
9. Do not automatically downgrade an unresolved Deep task.
10. Use task continuity and hysteresis to prevent repeated Quick/Deep oscillation.
11. Let explicit user mode commands override automatic routing.
12. Display and log the selected mode and workshop.
13. Never silently switch to an expensive cloud model.
14. Do not change the main model for every prompt when doing so would force costly Ollama unload/reload cycles.

### Preferred routing flow

```text
User prompt
    ↓
Fast deterministic router
    ↓
Small classifier only if ambiguous
    ↓
Mode + workshop + limits
    ↓
Bristlecone main model
    ↓
Escalation if necessary
```

## Tool routing and workshops

Instructions alone do not reduce prompt size when every tool schema remains visible. The actual visible tool collection must be narrowed before the main model call.

Proposed workshops:

### Code Workshop
- Repository navigation
- Symbol index
- LSP
- Tree-sitter
- Git
- Tests
- Formatter and linter
- Build tools
- Restricted terminal
- Code-specific documentation and memory

### Research Workshop
- Web search
- Page extraction
- Official documentation lookup
- PDF/document tools
- Source verification
- Research cache
- Optional self-hosted search

### System Workshop
- Qubes diagnostics
- Linux administration
- Service management
- Resource monitoring
- Package and configuration inspection
- Strong approval controls

### Model Workshop
- PyTorch
- Unsloth
- Model evaluation
- LoRA/QLoRA training
- Quantization and conversion
- Dataset preparation
- Checkpoints and exports

### Retrieval Workshop
- Keyword search
- Vector search
- Embeddings
- Reranking
- Document indexing
- Metadata filtering
- Caching

### Memory Workshop
- Temporary context
- Project memory
- User preferences
- Long-term knowledge
- Forget/correct/archive workflows
- Access-control enforcement

Routing should start with the smallest safe toolset, avoid tool ping-pong, and escalate only when the current workshop cannot complete the task.

## Proposed Qubes and Cherry-AI performance settings

These were recommendations only and remain unconfirmed:

- Test Cherry-AI with **8 GB initial memory** and **16 GB maximum memory**.
- Keep **6 vCPUs** initially and benchmark against fewer vCPUs.
- Keep memory balancing enabled for the first test; test fixed memory only later.
- Shut down unused app qubes during heavy AI work.
- Keep the normal network path through `sys-firewall` and `sys-net`.
- Do not weaken qrexec, GUI, firewall, networking, update, device, or permission services for speed.
- Audit autostart, background services, storage pressure, and running qubes before changing values.
- Keep active models, indexes, repositories, and caches on fast SSD storage.
- Use the phone for YouTube during heavy local work when practical, because a media qube adds CPU, RAM, and GUI load.

## Proposed Ollama settings

These values were proposed for testing, not confirmed:

```ini
OLLAMA_KEEP_ALIVE=30m
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_PARALLEL=1
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
OLLAMA_NO_CLOUD=1
```

Key reasoning:

- Keep Bristlecone’s main model resident.
- Avoid loading several large models at once.
- Avoid parallel requests multiplying context memory.
- Use the smallest context suitable for each mode.
- Test Flash Attention and K/V cache changes individually and roll back regressions.

## Maple-local AI and Seed Nursery

The user asked whether another AI can run inside Maple. The answer is yes:

- A Maple-local AI naturally accesses Maple only.
- It may be fully independent, a lightweight local Tree, or a client that asks Bristlecone for help.
- Running a second large model simultaneously can create substantial RAM and CPU contention.
- A lightweight Maple Tree plus Bristlecone as the deep specialist is the preferred initial design.

### Seed development role split

```text
Maple / Seed Nursery
├── Behavioral Seed configurations
├── Dataset creation and cleaning
├── Test conversations
├── Small evaluation batches
├── Candidate versions
└── Reproducible logs

Cherry-AI / Bristlecone Pine
├── Designs improvements
├── Reviews datasets
├── Diagnoses failures
├── Produces corrections
├── Compares candidates
└── Recommends promotion or rollback

User
├── Approves training data
├── Approves high-impact actions
└── Decides when a candidate becomes stable
```

Do not let Maple’s trainer and Bristlecone write to the same live files simultaneously. Use Git branches, candidate directories, immutable run folders, and rollback points.

## Two forms of Seed training

The user expects Seeds to need both forms.

### 1. Behavioral cultivation
Does not change model weights. It includes:

- Role and Grain
- SOUL/personality
- Permissions and boundaries
- Tools and workshops
- Memory rules
- Routing and mode behavior
- Example conversations
- Error handling
- Tests and evaluation rubrics

This should happen first because many failures can be fixed without weight training.

### 2. Model-weight training
Changes learned parameters or adds adapter weights. Potential targets include:

- Forest terminology
- Tool-selection behavior
- ADR/record formatting
- Qubes-safe procedures
- Coding conventions
- Quick versus Deep behavior
- Stable role adherence

Start with **LoRA or QLoRA**, not full fine-tuning. Full fine-tuning and reinforcement-learning workflows are later-stage options.

## PyTorch and Unsloth

### PyTorch
PyTorch is the underlying machine-learning engine. It performs numerical computation, loss calculation, backpropagation, weight updates, device placement, and checkpoint saving.

### Unsloth
Unsloth is an optimization and training workflow built on top of PyTorch and the Hugging Face ecosystem. It can simplify and accelerate LoRA/QLoRA and related model-training workflows.

```text
Seed training project
        ↓
Unsloth workflow
        ↓
PyTorch computation
        ↓
CPU/GPU hardware
```

PyTorch and Unsloth are complementary, not alternatives.

### Hardware reality

- Installing PyTorch and Unsloth does not make CPU-only LLM training fast.
- Their largest training benefit normally comes with a supported GPU.
- CPU-only work remains useful for dataset preparation, behavioral testing, small evaluations, conversion experiments, and learning the workflow.
- Before any GPU passthrough work, audit the exact CPU, GPU(s), VRAM, monitor connection, IOMMU grouping, and Qubes compatibility.
- Do not attempt PCI/GPU passthrough without a rollback plan.
- Prefer a dedicated **Model Workshop qube** rather than installing experimental training dependencies into everyday Maple or stable Cherry-AI.

## Recommended Seed training cycle

```text
1. Bristlecone designs the Seed behavior.
2. Maple prepares examples and evaluation tests.
3. Run the Seed without weight training.
4. Categorize failures.
5. Improve prompts, tools, memory, permissions, and routing first.
6. Convert repeated learnable failures into a reviewed dataset.
7. Train a LoRA or QLoRA candidate in the Model Workshop.
8. Evaluate it against the untrained baseline.
9. Bristlecone reviews regressions and improvements.
10. The user approves promotion, revision, or rejection.
```

## Provisional daily-use performance expectations

These are rough planning estimates, not benchmarks. They assume the previously discussed approximate host profile of 32 GB RAM, eight CPU threads exposed to Xen, and CPU-based Ollama. Verify the actual hardware.

Treat optimized Bristlecone running alone as 100%:

- Light Seed configuration/testing in Maple + YouTube on phone: roughly **85–95%**
- Small evaluation batches + YouTube on phone: roughly **75–90%**
- Light work + YouTube in another qube: roughly **70–85%**
- Heavy indexing, embeddings, or repeated evaluations: roughly **50–75%**
- Genuine CPU-heavy fine-tuning: roughly **25–50%**, potentially worse at peaks
- Heavy training plus video in another qube: roughly **15–40%**

The completed optimization plan can reduce prompt, routing, retrieval, tool, and model-loading overhead. It cannot create additional physical CPU, RAM, disk bandwidth, or GPU capacity.

For practical daily use:

- Maple may edit Seeds, build datasets, consult ChatGPT, and run small tests while Bristlecone remains responsive.
- Pause heavy Maple training before requesting Deep Bristlecone work.
- Resume training after Pine finishes.
- During actual fine-tuning, alternating training and deep review will likely feel better than running both at full load.

## Immediate next-stage recommendation

Before installing PyTorch or Unsloth:

1. Record the hardware and Qubes baseline.
2. Re-run Hermes prompt/tool/skill measurements after pruning.
3. Audit Cherry-AI RAM, maxmem, vCPUs, services, and storage.
4. Benchmark Bristlecone alone.
5. Implement and test Quick/Standard/Deep behavior.
6. Implement narrow tool routing/workshops.
7. Tune Ollama one setting at a time.
8. Build Seed behavioral tests and a dataset pipeline.
9. Audit GPU feasibility.
10. Create an isolated Model Workshop only after the baseline and hardware audit.

---

# AUTHORITATIVE OPTIMIZATION PLAN

The original plan supplied by the user is preserved below. Its status markings remain authoritative unless the user confirms a newer state.

BRISTLECONE PINE SPEED AND PERFORMANCE OPTIMIZATION PLAN
Version: 1.0
Primary focus: Improve the speed, responsiveness, retrieval efficiency, and resource use of Bristlecone Pine, the first Tree and Treewright in The Forest.

PURPOSE OF THIS FILE
Use this file to restore context in any new chat. Treat Bristlecone Pine optimization as the main focus unless the user explicitly changes or pauses it.

PROJECT RULES
1. Do not mark any pending item complete until the user confirms it was configured and tested.
2. Preserve Qubes OS security boundaries while optimizing performance.
3. Prefer free, open-source, local-first, private, self-hostable solutions.
4. Do not trade away safety, permissions, approval controls, or isolation merely for speed.
5. Measure before and after major changes whenever possible.
6. Fix orchestration, retrieval, configuration, and resource bottlenecks before attempting model fine-tuning.
7. Keep Bristlecone's architecture modular. Hermes, Newelle, Ollama, retrieval services, and workshops should have clearly separated responsibilities.
8. Avoid duplicate services, models, indexes, memory systems, or tool collections.
9. Use the smallest model, context window, toolset, and retrieval scope that can complete the task correctly.
10. Keep a record of changes, benchmarks, regressions, and rollbacks.

STATUS KEY
[X] Completed and confirmed
[ ] Pending
[~] In progress
[?] Needs investigation or decision

CURRENT MASTER CHECKLIST

[X] 1. Disable unnecessary Hermes skills
[ ] 2. Optimize Qubes OS, Cherry-AI, and background-qube resource use
[ ] 3. Tune Hermes and Newelle performance settings
[ ] 4. Tune Ollama runtime and model-loading settings
[ ] 5. Configure tool routing and workshops
[ ] 6. Add Quick Mode, Standard Mode, and Deep Mode
[ ] 7. Implement structure-aware, block-level code retrieval
[ ] 8. Optimize web, database, memory, and document retrieval
[ ] 9. Benchmark Bristlecone and identify remaining bottlenecks
[ ] 10. Evaluate an isolated Unsloth Model Workshop
[ ] 11. Review results and determine the next optimization stage

======================================================================
1. DISABLE UNNECESSARY HERMES SKILLS
STATUS: COMPLETED AND CONFIRMED
======================================================================

Goal:
Reduce prompt overhead, tool-selection confusion, startup work, and irrelevant capabilities loaded into Bristlecone.

Completed direction:
- Disable Hermes skills that Bristlecone does not currently need.
- Keep only the skills needed for the active role or workshop.
- Prefer loading skills on demand instead of preloading everything.

Still to verify during later tuning:
- Confirm whether unnecessary tools, toolsets, MCP servers, and integrations remain enabled.
- Record the final minimum default skill set.
- Confirm that disabled skills can still be activated when a relevant workshop requires them.

======================================================================
2. OPTIMIZE QUBES OS, CHERRY-AI, AND BACKGROUND-QUBE RESOURCE USE
STATUS: PENDING
======================================================================

Goal:
Give Bristlecone enough CPU, RAM, disk performance, and stable networking without weakening Qubes isolation.

2.1 Audit the system
- Record total system RAM, CPU model, CPU core/thread count, storage type, and available GPU.
- Record the current Qubes OS version.
- List all running qubes.
- Record each running qube's memory use, configured memory, maxmem, vCPUs, autostart state, and NetVM.
- Identify qubes that remain running without an active purpose.
- Identify templates, disposables, Whonix qubes, VPN qubes, browsers, media qubes, or helper qubes left open unnecessarily.
- Check dom0 resource use without adding unnecessary software to dom0.

Suggested audit commands in dom0:
qvm-ls --fields NAME,STATE,MEMORY,VCPUS,NETVM
qvm-prefs <QUBE_NAME> memory
qvm-prefs <QUBE_NAME> maxmem
qvm-prefs <QUBE_NAME> vcpus
qvm-prefs <QUBE_NAME> autostart

2.2 Preserve the security chain
- Keep the normal network path:
  Cherry-AI -> sys-firewall -> sys-net -> Internet
- Do not connect Cherry-AI directly to sys-net merely for speed.
- Do not disable required Qubes networking, qrexec, GUI, firewall, update-proxy, or security services.
- Keep sys-net and sys-firewall functionally intact.

2.3 Reduce unnecessary active qubes
- Create a Bristlecone work state that keeps only required qubes running.
- Keep essential service qubes running.
- Keep Cherry-AI running.
- Keep the active project qube running when project files live elsewhere.
- Shut down unused app qubes during heavy model, indexing, or coding work.
- Shut down old DisposableVMs and unused templates.
- Avoid keeping Sugar, Honey, Maple, Whonix, research qubes, or media qubes open when they are not needed.

2.4 Review autostart
- Keep autostart enabled for essential service qubes.
- Disable autostart for optional app qubes and helper services that do not need to run after every boot.
- Review Cherry-AI autostart based on whether Bristlecone should be available immediately.
- Document every autostart decision.

2.5 Tune memory
- Measure normal and peak memory use before changing limits.
- Give Cherry-AI a deliberate minimum memory allocation.
- Give Cherry-AI enough maxmem for the primary model, context, Hermes, Newelle, retrieval services, and active tools.
- Lower oversized maxmem values on lightweight background qubes.
- Avoid values so low that sys-net loses Wi-Fi stability or sys-firewall becomes unreliable.
- Watch for swapping, memory pressure, model unloading, and qmemman redistribution.
- Test whether fixed memory or dynamic memory works better for the AI workload.
- Change one variable at a time.

2.6 Tune vCPUs
- Measure CPU use during idle, model loading, generation, indexing, and tool execution.
- Give Cherry-AI enough vCPUs for inference and tool work.
- Avoid assigning every logical CPU to Cherry-AI.
- Leave capacity for dom0, sys-net, sys-firewall, and the active project qube.
- Reduce unnecessarily high vCPU allocations on lightweight qubes.
- Check whether too many vCPUs create scheduling overhead.

2.7 Reduce unnecessary background services
Potential candidates in app qubes, only where unused:
- Printing/CUPS
- File indexing
- Mail and calendar integration
- Bluetooth components
- Desktop search services
- Automatic background sync
- Unneeded tray applications
- Unneeded extension processes
- Duplicate update checks

Do not disable:
- Qubes networking services required by NetVMs
- qrexec
- Qubes GUI services
- Firewall services
- Required device services
- Security and permission controls

2.8 Storage optimization
- Keep active models, indexes, code repositories, caches, and vector databases on fast SSD storage.
- Avoid running active retrieval indexes from slow NAS storage.
- Keep archives and backups on the NAS when appropriate.
- Check free disk space.
- Check whether model files are duplicated across qubes.
- Check whether logs, caches, or unused model layers are consuming excessive space.
- Keep enough free space for model loading, updates, temporary files, and indexing.

2.9 Service-qube optimization
- First tune current sys-net and sys-firewall allocations.
- Later evaluate minimal templates or minimal-state service qubes.
- Do not rebuild sys-net on a minimal template until required Wi-Fi firmware, NetworkManager packages, and networking components are known.
- Prepare a rollback path before changing a service qube template.

2.10 Bristlecone performance work state
Create a repeatable work state that:
- Starts required qubes.
- Stops optional qubes.
- Confirms network availability.
- Confirms enough free memory.
- Starts Ollama and Bristlecone services.
- Preloads the primary model when appropriate.
- Records a baseline status.
- Can be exited cleanly without damaging other workflows.

======================================================================
3. TUNE HERMES AND NEWELLE PERFORMANCE SETTINGS
STATUS: PENDING
======================================================================

Goal:
Prevent Hermes and Newelle from duplicating work, loading unnecessary capabilities, or sending oversized prompts.

Recommended responsibility split:
- Hermes: reasoning, planning, tool routing, skills, agent behavior, and execution policy.
- Newelle: user interface, chat controls, profiles, and desktop integration.
- Ollama: model serving.
- Retrieval service: indexing, search, embeddings, reranking, and cached content.
- Workshops: isolated task-specific tools and permissions.

3.1 Hermes skills, tools, and toolsets
- Audit enabled skills.
- Audit enabled tools.
- Audit enabled toolsets.
- Audit MCP servers and integrations.
- Disable anything not required by the default Bristlecone profile.
- Load specialized tools only through workshops or explicit routing.
- Keep a minimal emergency toolset available for diagnostics.

3.2 Hermes reasoning level
- Use low or minimal reasoning for routine, reversible, low-risk tasks.
- Use medium reasoning for normal work.
- Use high reasoning for architecture, multi-file changes, debugging, security-sensitive work, and high-impact decisions.
- Avoid maximum reasoning unless the task justifies the latency.

3.3 Hermes turn and iteration limits
- Create lower tool-turn limits for Quick Mode.
- Use moderate limits for Standard Mode.
- Keep larger limits for Deep Mode.
- Add stopping rules so Bristlecone does not continue searching after enough evidence is available.
- Prevent repetitive retries and circular tool calls.
- Require a reason before expanding the search budget.

Tentative ranges to benchmark:
- Quick Mode: 15-25 turns
- Standard Mode: 30-50 turns
- Deep Mode: 60-90 turns

3.4 Auxiliary models and tasks
Use a small, fast local model for tasks such as:
- Conversation titles
- Context compression
- Search-result classification
- Page relevance classification
- Tool selection support
- Approval classification, where safe
- Simple extraction
- Summaries used only for routing

Disable automatic auxiliary tasks that provide little value.
Do not use the main coding model for trivial background jobs.

3.5 Context compression
- Keep conversation compression available for long sessions.
- Assign compression to a smaller model when possible.
- Preserve important project decisions, constraints, file references, errors, and unresolved tasks.
- Avoid compressing active code or exact commands into vague summaries.
- Benchmark the threshold at which compression begins.

3.6 Newelle profiles
Create separate profiles such as:
- Bristlecone Quick
- Bristlecone Standard
- Bristlecone Deep
- Bristlecone Code Workshop
- Bristlecone Research Workshop
- Bristlecone System Workshop

Each profile should expose only relevant tools, prompts, memory sources, and permissions.

3.7 Disable unused Newelle features by profile
Potential features to keep off unless needed:
- Text-to-speech
- Speech-to-text
- Wake-word listening
- Call mode
- Image generation
- Vision
- Web search
- Document RAG
- Local-folder indexing
- Unneeded MCP servers
- Unneeded extensions
- Duplicate long-term memory
- Duplicate model backends

3.8 Avoid duplicate model servers
- Use Ollama as the main model server unless the architecture is intentionally changed.
- Do not let Newelle independently load the same model through llama.cpp while Ollama is already serving it.
- Check for leftover llama-server, Ollama, Python, or extension processes.
- Ensure one service owns the primary model.
- Document exceptions for dedicated helper or embedding services.

3.9 Parallel tool execution
- Keep parallel model generations limited at first.
- Allow lightweight independent tools to run in parallel when they do not compete for the same bottleneck.
- Avoid parallel disk-heavy indexing, model inference, and large page extraction on limited hardware.
- Add workshop-specific concurrency limits.
- Benchmark sequential versus parallel execution.

3.10 Preserve safeguards
Do not disable for speed:
- Dangerous-command approvals
- Destructive-action confirmations
- File permission boundaries
- Workshop isolation
- User authorization
- Qubes separation
- Audit logging
- Recovery and rollback controls

======================================================================
4. TUNE OLLAMA RUNTIME AND MODEL-LOADING SETTINGS
STATUS: PENDING
======================================================================

Goal:
Reduce model reloads, memory pressure, context overhead, and inefficient request scheduling.

4.1 Record the current model state
Record:
- Primary model name
- Model parameter size
- Quantization
- Model file size
- Context length
- Ollama version
- CPU/GPU split
- RAM assigned to Cherry-AI
- Available RAM before and after model load
- Tokens per second
- Time to first token
- Model load time

Useful command:
ollama ps

4.2 Keep the main model warm
- Test OLLAMA_KEEP_ALIVE=30m.
- Consider a longer period after measuring memory pressure.
- Consider OLLAMA_KEEP_ALIVE=-1 only when the model can remain resident safely.
- Preload the primary model as part of Bristlecone startup when appropriate.
- Confirm the model is not repeatedly unloading between normal requests.

4.3 Limit loaded models
Initial test:
OLLAMA_MAX_LOADED_MODELS=1

Then evaluate whether memory permits:
- One main model plus one small helper model.
- One main model plus one embedding model.
- A separate retrieval server for embeddings.

Avoid model swapping that repeatedly unloads and reloads Bristlecone's main model.

4.4 Limit parallel model requests
Initial test:
OLLAMA_NUM_PARALLEL=1

Increase only when:
- Multiple users or independent workloads justify it.
- Memory use remains safe.
- Throughput improves without hurting latency.
- Context-memory multiplication is understood.

4.5 Context by mode
Do not force one enormous context globally.

Tentative values to benchmark:
- Quick Mode: 8K-16K
- Standard Mode: 16K-32K
- Deep/Code Mode: 32K-64K or only as required

Principle:
Use the smallest context that can correctly complete the task.

4.6 Flash Attention
Test:
OLLAMA_FLASH_ATTENTION=1

- Confirm backend and model compatibility.
- Compare memory use and tokens per second.
- Return to automatic behavior if it causes instability.

4.7 K/V cache
Test:
OLLAMA_KV_CACHE_TYPE=q8_0

- Compare quality, memory use, and speed against f16.
- Avoid q4_0 initially for architecture and code review unless memory constraints require testing it.
- Record any quality regression at long contexts.

4.8 Local-only mode
Test:
OLLAMA_NO_CLOUD=1

- Keep cloud use explicit and routed through an approved research path.
- Do not allow hidden fallback to cloud models.
- Preserve local-first operation.

4.9 Model selection and quantization
- Benchmark the current model against smaller and more efficient coding models.
- Compare quality per second, not just raw tokens per second.
- Prefer a model that fits fully in available memory.
- Avoid CPU/GPU split when a smaller model can fit fully on the faster device and produce acceptable quality.
- Test quantization levels deliberately.
- Keep a high-quality Deep Mode model and a smaller Quick Mode model if hardware supports the architecture without costly switching.
- Consider separate servers only if they prevent model eviction and fit available resources.

4.10 GPU and offloading
- Verify whether Cherry-AI has GPU access.
- Verify whether the model is fully on GPU, fully on CPU, or split.
- In Qubes, preserve safe PCI assignment practices.
- Do not attempt risky passthrough changes without a rollback plan.
- If no GPU is available, optimize CPU inference, model size, quantization, thread use, and memory.

Initial Ollama configuration shortlist for testing:
OLLAMA_KEEP_ALIVE=30m
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_NUM_PARALLEL=1
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
OLLAMA_NO_CLOUD=1

These are test values, not confirmed final settings.

======================================================================
5. CONFIGURE TOOL ROUTING AND WORKSHOPS
STATUS: PENDING
======================================================================

Goal:
Load only the tools needed for the current task and prevent Bristlecone from inspecting every available tool on every prompt.

5.1 Tool Router
The router should classify:
- Task type
- Risk
- Required capabilities
- Required data sources
- Expected depth
- Whether internet access is needed
- Whether code execution is needed
- Whether human approval is required

5.2 Default routing behavior
- Start with the smallest safe toolset.
- Add a workshop only when the task requires it.
- Do not expose every tool description to the model.
- Prefer deterministic routing for obvious tasks.
- Allow Bristlecone to request escalation when the initial workshop is insufficient.
- Log routing decisions for later tuning.

5.3 Proposed workshops

Code Workshop:
- Repository navigation
- Symbol index
- LSP
- Tree-sitter
- Git
- Tests
- Formatter and linter
- Build tools
- Restricted terminal
- Code-specific memory and documentation

Research Workshop:
- Web search
- Page extraction
- Documentation lookup
- PDF/document tools
- Source verification
- Research cache
- Optional SearXNG

System Workshop:
- Qubes diagnostics
- Linux administration
- Service management
- Resource monitoring
- Package and configuration inspection
- High-risk approval controls

Model Workshop:
- Model evaluation
- Quantization
- Conversion
- Unsloth
- Dataset preparation
- Fine-tuning
- Export to Ollama-compatible formats

Retrieval Workshop:
- Keyword search
- Vector search
- Embeddings
- Reranking
- Document indexing
- Metadata filtering
- Search caching

Memory Workshop:
- Project memory
- User preferences
- Long-term knowledge
- Temporary context
- Things to forget
- Access-control enforcement
- Memory correction and archival

5.4 Workshop isolation
- Give each workshop only required tools and permissions.
- Use separate qubes or services where isolation materially improves security or performance.
- Avoid creating too many always-running qubes.
- Start workshops on demand.
- Stop them after inactivity when safe.
- Keep lightweight services resident only when the performance gain justifies it.

5.5 Routing cache
- Cache stable routing decisions for repeated task patterns.
- Invalidate the cache when tools, profiles, permissions, or project context change.
- Do not cache unsafe approvals.

5.6 Workshop fallback
- If a workshop cannot complete a task, return a structured reason.
- Route to another workshop only when justified.
- Avoid tool ping-pong.
- Limit escalation depth.
- Ask the user only when a decision or permission cannot be safely inferred.

======================================================================
6. ADD QUICK MODE, STANDARD MODE, AND DEEP MODE
STATUS: PENDING
======================================================================

Goal:
Match reasoning, context, tools, retrieval, and execution effort to the task.

6.1 Quick Mode
Use for:
- Routine questions
- Low-risk edits
- Simple commands
- Small file changes
- Status checks
- Formatting
- Reversible actions
- Familiar workflows

Quick Mode behavior:
- Low or minimal reasoning
- Small context window
- Minimal toolset
- Current conversation first
- One local collection when needed
- Keyword search before semantic search
- Web only when required
- Few search results
- One or two extracted pages
- Lower tool-turn limit
- No broad repository scan
- No deep dependency expansion unless necessary
- Stop after sufficient evidence
- Prefer a smaller fast model if switching cost is acceptable

6.2 Standard Mode
Use for:
- Normal coding work
- Moderate debugging
- Multi-step planning
- Project documentation
- Common research
- Changes with limited risk

Standard Mode behavior:
- Medium reasoning
- Moderate context
- Workshop routing
- Hybrid retrieval where useful
- Normal verification
- Moderate tool-turn limit
- Escalate to Deep Mode when complexity grows

6.3 Deep Mode
Use for:
- Architecture
- Multi-file changes
- Difficult debugging
- Security-sensitive work
- High-impact decisions
- Conflicting evidence
- Unfamiliar systems
- Migration planning
- Large refactors
- Root-cause investigation

Deep Mode behavior:
- High reasoning
- Larger context only as needed
- Broader dependency retrieval
- Multiple authoritative sources
- Reranking
- Verification and testing
- Higher tool-turn budget
- Explicit assumptions and uncertainty
- More complete logs
- Rollback planning
- Do not automatically use maximum context or every tool

6.4 Mode selection
- Let the user explicitly choose a mode.
- Allow deterministic automatic mode selection based on task risk and complexity.
- Permit Bristlecone to recommend escalation.
- Require user approval before high-risk operations regardless of mode.
- Display the active mode clearly.
- Do not silently switch to an expensive cloud model.

6.5 Mode aliases
Potential aliases:
- Quick
- Standard
- Deep

Do not mark aliases configured until the user confirms they were added and tested.

======================================================================
7. IMPLEMENT STRUCTURE-AWARE, BLOCK-LEVEL CODE RETRIEVAL
STATUS: PENDING
======================================================================

Goal:
Retrieve complete relevant code units instead of scanning entire repositories or returning isolated text matches.

7.1 Required retrieval units
Retrieve complete:
- Functions
- Methods
- Classes
- Modules
- Interfaces
- Type definitions
- Configuration blocks
- Tests
- Related documentation sections

7.2 Structure-aware tools
Evaluate:
- Tree-sitter for syntax trees and symbol boundaries
- Language Server Protocol for definitions, references, symbols, types, and diagnostics
- ripgrep or equivalent for exact fallback search
- Git metadata for change history
- Dependency graphs for callers, imports, and relationships

7.3 Retrieval process
Preferred process:
1. Identify the target symbol, error, behavior, or feature.
2. Search the symbol index.
3. Retrieve the complete relevant function, method, class, or module.
4. Include necessary imports and type definitions.
5. Expand to callers, callees, tests, or configuration only when needed.
6. Rerank the candidate code units.
7. Give the model the smallest complete set needed for the task.

7.4 Avoid poor retrieval patterns
Avoid:
- Reading every repository file.
- Repeatedly scanning the same files.
- Returning tiny text fragments without structure.
- Loading an entire repository into context.
- Pulling every reference when only one implementation matters.
- Re-indexing the full repository after one small edit.

7.5 Incremental code indexing
- Index each repository once.
- Update only changed files and affected symbols.
- Watch file changes.
- Store language, path, symbol type, symbol name, relationships, and commit information.
- Detect renamed and deleted symbols.
- Rebuild the full index only when required.

7.6 Code retrieval profiles
Quick code retrieval:
- Exact symbol
- Current file
- Direct definition
- One level of dependencies
- Relevant test only when needed

Deep code retrieval:
- Symbol
- Definitions and references
- Call graph
- Imports and types
- Related tests
- Recent changes
- Architecture documents
- Multiple dependency levels as justified

7.7 Validation
- Test retrieval on known repository questions.
- Measure search time.
- Measure number of files opened.
- Measure tokens sent to the model.
- Compare answer quality against full-repository scanning.
- Record missed dependencies and false matches.

======================================================================
8. OPTIMIZE WEB, DATABASE, MEMORY, AND DOCUMENT RETRIEVAL
STATUS: PENDING
======================================================================

Goal:
Reduce the time between deciding information is needed and presenting the correct evidence to Bristlecone.

8.1 Retrieval Router
Use this general ladder:
1. Current conversation
2. Active project memory
3. Relevant local structured index
4. Broader local databases
5. Web search
6. Deep research only when necessary

The router should consider:
- Freshness
- Authority
- Privacy
- Project scope
- User permissions
- Required precision
- Cost and latency
- Whether the answer may have changed

8.2 Separate search from extraction
Preferred web flow:
1. Search.
2. Inspect titles, domains, dates, and snippets.
3. Select the best one to three sources.
4. Extract only selected pages.
5. Expand only if evidence is insufficient or conflicting.

Avoid opening and reading every search result.

8.3 Fast and deep web profiles
Quick web retrieval:
- Targeted query
- Three to five results
- One or two extracted pages
- One follow-up search maximum
- Cache use when valid
- Prefer official sources

Standard web retrieval:
- Five to eight results
- Two to four extracted pages
- Verification when needed
- Moderate follow-up

Deep web retrieval:
- Multiple targeted searches
- Several authoritative sources
- Date and version verification
- Conflict comparison
- Source diversity
- More complete extraction
- Explicit uncertainty

8.4 Query targeting
Automatically use appropriate filters:
- Official documentation domains
- GitHub repository or organization
- Exact error messages
- File types
- Version numbers
- Date filters
- Academic domains
- Project-specific terms

8.5 Web cache
Cache:
- Search query
- Result titles
- URLs
- Snippets
- Cleaned page text
- Retrieval date
- Page hash or version
- Source type
- Trust rating

Possible cache policy:
- Current news and volatile data: very short or no cache
- Software documentation: hours to one day
- Stable reference material: several days
- Project pages: until changed
- User-controlled refresh at any time

8.6 Local database indexing
When a document is added:
1. Parse it once.
2. Split it into meaningful sections.
3. Preserve headings and metadata.
4. Create keyword and semantic indexes.
5. Save source, project, date, document type, trust, permissions, and version.
6. Retrieve only relevant sections for questions.

8.7 Hybrid search
Combine:
- Exact keyword search
- Semantic/vector search
- Metadata filtering
- Symbol search for code
- Recency and trust scoring
- Relationship or graph search where useful

Use exact search first for:
- Error codes
- Filenames
- Function names
- Commands
- Record IDs
- Exact phrases

Use semantic search for:
- Concepts
- Behavior descriptions
- Architectural questions
- Related ideas with different wording

8.8 Reranking
Suggested process:
- Retrieve approximately 10-20 lightweight candidates.
- Rerank candidates using a fast local method or small model.
- Give the main model only the best 3-5 complete sections.
- Expand when the first set is insufficient.

8.9 Collection separation
Use separate indexes or collections for:
- Forest architecture
- ADRs and governed records
- Bristlecone source code
- Qubes documentation
- Ollama/Hermes/Newelle documentation
- User preferences
- Project memory
- Archived material
- Web research cache
- Security records
- Model and benchmark records

Route to likely collections before searching everything.

8.10 Incremental indexing
- Re-index only changed documents or sections.
- Preserve stable embeddings for unchanged content.
- Update metadata without rebuilding everything.
- Re-index linked dependencies only when necessary.
- Schedule heavy maintenance outside active Bristlecone sessions.

8.11 Embedding model architecture
Avoid using an embedding model in a way that evicts the primary coding model.

Evaluate:
- Allowing two loaded models only if both fit.
- A separate Ollama instance for embeddings.
- A dedicated lightweight retrieval service.
- A Retrieval Workshop qube.
- Keyword-first routing that invokes embeddings only when needed.

Current preference:
Use a small dedicated retrieval service so the main Bristlecone model can remain resident.

8.12 Self-hosted search
Evaluate a SearXNG Research Workshop because it can support:
- Local control
- Privacy
- Multiple search backends
- Self-hosting
- Explicit routing

Do not enable excessive engines.
Benchmark it against simpler search providers.
Keep only useful technical, general, GitHub, and academic sources.

8.13 Active index placement
- Keep active indexes on SSD.
- Keep databases close to the service using them.
- Avoid unnecessary network hops between qubes.
- Use qrexec or controlled APIs when cross-qube access is required.
- Keep slow archives on NAS.
- Cache frequently used records locally when allowed.

8.14 Memory retrieval
- Search temporary context first.
- Search project memory next.
- Search user preferences only when relevant.
- Search long-term knowledge by project and permissions.
- Respect different-user access controls.
- Never mix private memories across users.
- Allow correction, forgetting, expiry, and provenance tracking.
- Avoid injecting unrelated memories into prompts.

======================================================================
9. BENCHMARK BRISTLECONE AND IDENTIFY REMAINING BOTTLENECKS
STATUS: PENDING
======================================================================

Goal:
Measure real improvements and locate the next limiting component.

9.1 Create a baseline before major changes
Record:
- Cold startup time
- Warm startup time
- Model load time
- Time to first token
- Tokens per second
- Total task completion time
- Tool-selection time
- Tool startup time
- Number of tool calls
- Search time
- Page extraction time
- Local retrieval time
- Index update time
- Peak RAM
- Peak CPU
- GPU use
- Disk read/write
- Number of running qubes
- Model reload count
- Errors and retries

9.2 Benchmark tasks
Use repeatable examples:
- Simple conversational response
- Small code explanation
- Locate a function in a repository
- Diagnose a known bug
- Modify one file
- Modify several related files
- Search local documentation
- Search the web for current official documentation
- Retrieve a project ADR
- Run tests
- Perform a Qubes diagnostic
- Compare Quick and Deep Mode

9.3 Test method
- Run each task multiple times.
- Separate cold and warm runs.
- Change one major variable at a time.
- Record model, quantization, context, mode, tools, and running qubes.
- Compare median performance rather than one lucky run.
- Record quality and correctness, not just speed.
- Note regressions.

9.4 Bottleneck categories
Classify delays as:
- Qube startup
- Model loading
- Prompt construction
- Context processing
- Token generation
- Tool routing
- Tool execution
- Web latency
- Page extraction
- Local database search
- Embedding generation
- Reranking
- Disk access
- Network hop
- Memory pressure
- CPU contention
- GPU limitation
- Repeated retries
- Bad workflow design

9.5 Optimization log
For every change, record:
- Date
- Setting changed
- Old value
- New value
- Reason
- Benchmark before
- Benchmark after
- Quality impact
- Security impact
- Stability impact
- Decision: keep, revise, or roll back

9.6 Success criteria
Bristlecone should:
- Start reliably.
- Keep the main model resident when appropriate.
- Respond faster to routine work.
- Use deeper processing only when needed.
- Retrieve fewer but more relevant sources.
- Avoid scanning whole repositories.
- Avoid loading unnecessary tools.
- Preserve security and correctness.
- Use stable, repeatable configurations.
- Show measurable improvement over baseline.

======================================================================
10. EVALUATE AN ISOLATED UNSLOTH MODEL WORKSHOP
STATUS: PENDING
======================================================================

Goal:
Determine whether model fine-tuning, quantization, conversion, or specialized embedding training is justified after simpler bottlenecks are fixed.

10.1 Role of Unsloth
Potential uses:
- Fine-tune a coding model.
- Teach Bristlecone project conventions.
- Fine-tune a retrieval embedding model.
- Create or convert efficient quantized models.
- Export models for Ollama-compatible use.
- Experiment with LoRA or QLoRA.
- Build a specialized Bristlecone model.

10.2 Why this comes later
Unsloth does not directly fix:
- Too many loaded tools
- Bad routing
- Full repository scans
- Oversized contexts
- Duplicate services
- Weak Qubes allocations
- Repeated model swaps
- Inefficient web research

Fix orchestration, retrieval, system, and runtime issues first.

10.3 Isolated Model Workshop
- Use a separate qube or isolated environment.
- Keep training dependencies out of the main Bristlecone runtime.
- Store datasets, checkpoints, and exports separately.
- Require dataset review.
- Keep provenance for every example.
- Test for regressions.
- Export only models that pass evaluation.
- Do not replace the stable model without a rollback path.

10.4 Potential training targets
- ADR and record formatting
- Forest terminology
- Tool-selection examples
- Quick versus Deep Mode behavior
- Qubes-safe procedures
- Coding conventions
- Error correction behavior
- Structured retrieval decisions
- Workshop routing examples

10.5 Evaluation requirement
Do not adopt a fine-tuned model merely because it feels more customized.

Compare:
- Accuracy
- Coding quality
- Instruction following
- Tool routing
- Hallucination rate
- Security behavior
- Tokens per second
- RAM/VRAM use
- Time to first token
- Context performance
- Regression on general tasks

======================================================================
11. REVIEW RESULTS AND DETERMINE THE NEXT OPTIMIZATION STAGE
STATUS: PENDING
======================================================================

Goal:
Use measurements to decide what Bristlecone needs next rather than adding complexity without evidence.

Possible future areas:
- Better model selection
- Speculative decoding
- Dedicated inference hardware
- GPU passthrough or a separate AI host
- Distributed inference
- Retrieval graph
- Better reranker
- Prompt and system-message compression
- Tool schema compression
- Persistent workshop services
- Faster storage
- Network architecture improvements
- Dedicated model server qube
- Remote inference node
- Automated performance profiles
- Self-monitoring and regression alerts
- Additional TBD items discovered during testing

Do not add a future stage merely because it is popular. Add it only when it addresses a measured bottleneck and fits The Forest's principles.

======================================================================
RECOMMENDED IMPLEMENTATION ORDER
======================================================================

Phase 1: Establish baseline
1. Record hardware, Qubes, model, and current benchmark data.
2. Confirm exactly which skills, tools, services, and models are running.

Phase 2: Recover wasted system resources
3. Optimize running qubes, autostart, memory, vCPUs, and background services.
4. Confirm storage placement and free space.

Phase 3: Tune the current software stack
5. Tune Ollama loading, context, concurrency, Flash Attention, and K/V cache.
6. Tune Hermes reasoning, turns, tools, skills, and auxiliary tasks.
7. Tune Newelle profiles and disable duplicate features.

Phase 4: Improve task execution
8. Add Quick, Standard, and Deep modes.
9. Configure the Tool Router and workshops.
10. Prevent duplicate model servers and duplicate memory/index services.

Phase 5: Improve information retrieval
11. Add structure-aware code retrieval.
12. Add the Retrieval Router.
13. Build hybrid local search, caching, reranking, and incremental indexing.
14. Optimize web search and page extraction.

Phase 6: Measure and refine
15. Re-run the benchmark suite.
16. Keep successful changes.
17. Roll back regressions.
18. Identify the remaining bottleneck.

Phase 7: Advanced model work
19. Evaluate Unsloth in an isolated Model Workshop.
20. Fine-tune or quantize only when benchmark evidence supports it.

======================================================================
CURRENT SHORT STATUS
======================================================================

[X] Unnecessary Hermes skills disabled.

[ ] Qubes and background resource optimization not yet configured and tested.
[ ] Hermes and Newelle tuning not yet configured and tested.
[ ] Ollama tuning not yet configured and tested.
[ ] Tool routing and workshops not yet configured and tested.
[ ] Quick, Standard, and Deep modes not yet configured and tested.
[ ] Structure-aware code retrieval not yet configured and tested.
[ ] Web, database, memory, and document retrieval optimization not yet configured and tested.
[ ] Benchmarking not yet completed.
[ ] Unsloth Model Workshop not yet evaluated.
[ ] Next optimization stage remains TBD.

CONTINUITY INSTRUCTION FOR FUTURE CHATS
Treat this checklist as the authoritative Bristlecone Pine speed-optimization plan. Keep it updated. Do not mark pending steps complete without the user's confirmation that they were implemented and tested. When working through the plan, focus on one section at a time, explain commands before they are run, preserve Qubes security boundaries, and compare performance before and after changes.


# CONVERSATION CONTINUITY ADDENDUM

## Decisions that extend the original plan

### Added to Step 6: Automatic Mode Router
Add an automatic mode-routing subsection that selects Quick, Standard, or Deep before the main model call. It must use deterministic routing first, a small classifier only when necessary, task continuity, hysteresis, safe defaults, explicit overrides, escalation rules, visible mode reporting, and routing logs.

### Linked Step 5 and Step 6
Reasoning mode and tool workshop are separate dimensions:

```text
Reasoning:
Quick / Standard / Deep

Workshop:
Code / Research / System / Model / Retrieval / Memory
```

A Deep task must not automatically receive every tool. It should receive only the narrow workshop needed for that task.

### Added architecture direction
Bristlecone remains centralized in Cherry-AI, while Maple may host a local Tree or Seed Nursery. Cross-qube collaboration must use narrow qrexec services, Git exchanges, approved file transfer, or similarly controlled interfaces.

### Added training direction
Seeds will likely receive both behavioral cultivation and later model-weight training. PyTorch and Unsloth belong in an isolated Model Workshop. LoRA/QLoRA is the preferred initial weight-training method. Training should occur only after routing, retrieval, system, runtime, and evaluation foundations are working.

## Current unresolved questions

- Exact CPU model and physical core/thread count
- Exact GPU model(s), VRAM, monitor attachment, and IOMMU groups
- Exact Qubes OS version
- Exact Cherry-AI memory, maxmem, vCPU, and storage configuration
- Exact Bristlecone model, size, quantization, context, and measured speed
- Exact Newelle-to-Hermes/Ollama connection path
- Exact current enabled tools and post-pruning skill list
- Whether Hermes supports the desired automatic mode/workshop change directly in the installed version or needs a custom router
- Whether Maple should remain the Seed Nursery or whether a dedicated qube should be created immediately
- Whether a second small local model can remain resident without evicting Bristlecone’s main model
- Whether GPU passthrough is safe and practical on the current hardware

## Safety and correctness reminders

- Do not grant Bristlecone unrestricted access to Maple, other qubes, or dom0.
- Do not install experimental ML dependencies into stable environments merely for convenience.
- Do not start weight training before an evaluation suite exists.
- Do not train on unreviewed, private, copyrighted, low-quality, contradictory, or unsafe data.
- Do not promote a candidate merely because it sounds more customized.
- Compare candidate and baseline quality, tool routing, security behavior, memory use, speed, and regressions.
- Preserve stable versions and rollback paths.
- Measure cold and warm runs separately.
- Change one major variable at a time.

## Handoff prompt for another AI

Use the following as the first instruction after attaching this file:

> Read the complete Bristlecone Pine Continuity Packet. Restore the project’s terminology, architecture, confirmed status, pending checklist, and safety boundaries. Do not mark anything complete unless I confirm it was implemented and tested. Start by summarizing the current confirmed state, the next safest measurable step, and any information you need from me before giving commands.



---

# Q. FINAL HANDOFF SUMMARY

```text
Bristlecone Pine = Treewright
Current preferred stack = Hermes + Ollama in Cherry-AI
Newelle = paused/optional
Unnecessary Hermes skills = disabled
Automatic Hermes title generation = disabled/fixed

Measured:
Direct Ollama reasoning-none ≈ 23.48 sec
Hermes todo-only ≈ 22–24 sec
Hermes file+terminal = 41 sec
file+terminal+todo = 1:49.64
file+terminal+skills = 2:42.40
file+terminal+skills+todo = 2:49.16
broad Hermes ≈ 3 min
Newelle = 5–15+ min and unreliable in current integration

Current optimization direction:
narrow Hermes tool Workshops
→ Quick/Standard/Deep
→ Automatic Mode Router
→ Qubes/Ollama tuning
→ retrieval optimization
→ Maple Seed Nursery
→ isolated PyTorch/Unsloth Model Workshop
```

When continuing this project, do not mark a planned step complete unless the user confirms it was implemented and tested.
