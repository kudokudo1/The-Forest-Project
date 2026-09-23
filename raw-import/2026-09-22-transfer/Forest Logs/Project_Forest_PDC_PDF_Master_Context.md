---
title: Project Forest, Project Digital Cross, and Project Digital Fortress — Master Context
aliases:
  - Forest Master Context
  - Project Digital Cross Context
  - Project Digital Fortress Context
tags:
  - project-forest
  - project-digital-cross
  - project-digital-fortress
  - forest
  - seeds
  - leaf-foliage
  - qubes
status: active-reference
updated: 2026-08-07
---

# Project Forest, Project Digital Cross, and Project Digital Fortress — Master Context

> [!important]
> This file is a continuity/reference packet for humans and AI systems. It combines established Project Forest, Project Digital Cross, Project Digital Fortress, Qubes, identity/security, Seed-training, and related architecture context.
>
> **Status language matters:**
> - **Confirmed / implemented** = the user has indicated the item is actually done or working.
> - **Planned / desired / proposed** = an accepted direction or idea that may not yet exist.
> - **Historical / superseded** = useful background that should not be treated as the current implementation.
>
> When a later direct statement from the user conflicts with this file, follow the newer statement and update this reference.

---

# 1. Project Lineage

## 1.1 Project Digital Fortress — PDF

**Project Digital Fortress (PDF)** was the early identity, privacy, security, email, domain, and infrastructure project.

Its work included:

- Secure digital identity.
- Custom-domain email.
- Cloudflare DNS and registrar work.
- Proton Mail.
- Password management.
- Git identity.
- SSH/GitHub setup.
- Recovery/security separation.
- Qubes OS.
- Local AI.
- NAS and networking.
- Documentation and architecture planning.

The abbreviation **PDF** can also mean Portable Document Format, so context matters.

Project Digital Fortress later evolved into the broader **Project Digital Cross**.

## 1.2 Project Digital Cross

In normal prose, prefer the full name **Project Digital Cross**. The abbreviation **PDC** is useful in code, filenames, folders, repository structures, record identifiers, and other compact technical contexts.

Project Digital Cross is the long-term umbrella initiative for the user's personal technology and AI ecosystem.

It encompasses or governs areas including:

- The Forest.
- Cherry/local AI.
- Qubes OS platform work.
- Secure digital identity.
- Domain and email.
- Password management.
- Git/GitHub identity.
- NAS and durable storage.
- Home networking.
- Remote access.
- Documentation.
- Architecture Decision Records.
- Standards/specifications.
- Security architecture.
- Self-hosted services.
- Labs/workshops.
- Future device and AI infrastructure.

## 1.3 The Forest

**The Forest** is the current AI ecosystem/subsystem within Project Digital Cross.

The Forest uses a natural/woodland vocabulary for AI agents, storage, interfaces, security, data, outputs, networking, and system lifecycle.

The Forest is intended to become more than a collection of installed AI tools. The long-term direction is a cohesive, user-friendly, local-first AI system that can be installed on many kinds of devices without requiring a new user to understand which separate applications, model servers, agent frameworks, storage systems, plugins, and utilities need to be stacked together.

---

# 2. Core Project Philosophy

Across Project Digital Cross and The Forest, preserve these principles:

- Prefer **free** solutions when practical.
- Prefer **open-source** software.
- Prefer **self-hosted** and **local-first** architecture.
- Prefer open standards and replaceable components.
- Avoid unnecessary vendor lock-in.
- Avoid subscriptions when a durable free or one-time-purchase approach is practical.
- Cloud services may be supported, but should not silently become mandatory.
- Internet access should expand capability, not be required for the core system to exist.
- Preserve privacy and user ownership of data.
- Preserve modularity.
- Keep components replaceable.
- Keep strong permission boundaries.
- Prefer auditable behavior.
- Do not trade away Qubes isolation, approvals, permissions, logging, recovery controls, or security simply for speed.
- Measure performance before and after major optimization changes.
- Change one important variable at a time during troubleshooting.
- Keep rollback paths.
- Governance, records, and architecture should precede uncontrolled implementation.
- Do not mark a task complete merely because it was proposed or configured; confirm that it was tested successfully.

---

# 3. Long-Term Forest Product Vision

The long-term Forest experience should feel like a **single coherent AI ecosystem**, even if multiple modular components exist internally.

The development environment currently experiments with tools such as:

- Hermes.
- Ollama.
- Podman.
- Obsidian.
- Qubes OS.
- Git.
- Local retrieval/indexing ideas.
- Agent skills.
- Future workshops.
- Optional interfaces and services.

The user does **not** want future Forest users to need to learn how to manually assemble a stack such as:

```text
model runtime
+ agent framework
+ memory system
+ note system
+ vector database
+ web UI
+ automation system
+ sync system
+ plugins
+ networking
+ permissions
```

Instead, the desired end-state is approximately:

```text
Install Forest
    ↓
Choose desired capabilities
    ↓
Forest configures compatible internal modules
    ↓
Use Trees, Foliage, Garden, tools, and services
```

"One-time download" does not necessarily require one monolithic binary. A strong architecture may use:

- One installer/bootstrapper.
- A unified Forest interface.
- Modular internal services.
- Optional modules selected by device capabilities.
- Local default behavior.
- Optional online and Garden connectivity.

A powerful desktop could host more local models and services; a phone could run a constrained/potted Forest; a server could run headless services; a weak laptop could use smaller models or securely ask a stronger Forest device for help.

---

# 4. The Forest — Core Concept

Each device can host or "plant" **Trees**, which are AI agents.

Trees on the same device form a local **Forest**.

Trees may coordinate through a local **Canopy**.

Selected devices/Forests may later connect through a **Greater Forest Canopy** or related Garden architecture for:

- Secure communication.
- File sharing.
- Remote AI assistance.
- Synchronized media.
- Optional synchronization.
- Peer-to-peer services.
- Workload handoff.
- Cross-device coordination.

The user remains the authority. Trees can assist, recommend, warn, and operate within permissions, but should not become the ultimate authority over the user.

---

# 5. Primary Trees

## 5.1 Cherry

**Cherry** is the primary user-facing local AI assistant.

Desired Cherry capabilities:

- Desktop integration.
- Terminal integration.
- Browser/web interface.
- Remote access later.
- Multiple user profiles.
- Multiple local and remote models.
- Seamless model switching.
- Automatic learning under governance.
- Temporary conversation memory.
- Project memory.
- User preferences.
- Long-term knowledge.
- Controlled forgetting.
- Access separation between users.
- Admin-only access to broader multi-user information where appropriate.
- Tool use.
- Model routing.
- Error logging and learning.
- Local-first operation.

### Cherry modes

#### Observer — default

- Quiet.
- Watchful.
- Reserved.
- Offers relevant help without dominating.
- Should not constantly interrupt.

#### Collaborator

- More active.
- Helps reason through work.
- Can suggest alternatives.
- Can gently disagree when justified.
- Should explain uncertainty.

#### Operator

- More direct action.
- Should remain cautious for destructive or safety-sensitive tasks.
- Requires appropriate permissions and checks.
- User authority remains central.

### Cherry personality / Grain direction

- Reserved/shy observer by default.
- More confident when explicitly prompted.
- Can gently disagree when justified.
- Should report uncertainty.
- Should use multiple sources when appropriate.
- Should make speed-versus-accuracy tradeoffs visible.
- Should not silently override the user.

### Cherry memory categories

Cherry should distinguish at least:

1. Temporary/current-conversation memory.
2. Project memory.
3. User preferences.
4. Long-term knowledge.
5. Things to forget.
6. Different users' data.
7. Admin-only cross-user data.

### Cherry error policy

When Cherry makes a mistake:

1. Admit the mistake.
2. Apologize.
3. Recheck sources.
4. Provide a corrected answer.
5. Explain the mix-up as clearly as possible.
6. Ask for more information only when genuinely necessary.
7. Log the mistake.
8. Learn from it.
9. Keep the correction available temporarily in case the user is still applying the fix.
10. Move on when the user confirms it is corrected or clearly moves on.

## 5.2 Maple

**Maple** is Cherry's second assistant/"twin" and an implementation/engineering-oriented Tree.

Established or desired Maple roles include:

- Reading the same principles as Cherry but with a different interpretation.
- Coding and engineering support.
- Video-related work.
- Reviewing/checking Cherry.
- Data management.
- Seed-training workspace functions.
- Performing practical implementation tasks.
- Potentially serving as the primary constrained-device/background operations Tree.

Maple does not outrank the user.

### Emerging mobile/background role

A newer Forest design direction is to make Maple a good candidate for routine background/device-management work, especially where only one Tree should be active to conserve resources.

Potential Maple/background responsibilities include:

- Processing queued permitted tasks.
- Organizing approved files.
- Preparing reminders.
- Calendar maintenance.
- Background indexing.
- Local Foliage maintenance.
- Optional Garden sync.
- Performing work when the device is charging/idle.
- Deferring heavy work when battery is low.
- Handing heavy work to a stronger Garden-connected device when allowed.

A small Forest scheduler/daemon should ideally remain lightweight and wake Maple or another model only when actual AI reasoning is needed. "Maple is responsible" should not require a multi-billion-parameter model to remain loaded continuously.

## 5.3 Cedar

**Cedar** is the defense/health/security Tree.

Cedar monitors:

- **Poachers** — human attackers.
- **Mold** — malware, trackers, viruses, harmful code, corruption, or similar threats.

Cedar rules/directions include:

- Cedar can inspect risky files and behavior.
- Only Cedar may absorb Leaf Litter from arbitrary/untrusted sources.
- Other Trees should absorb only trusted/user-approved litter.
- Cedar can sift Leaf Litter.
- Cedar can recover Fruit.
- Cedar can set spoil timers.
- Cedar can track origin and safety.
- Cedar should preserve history.
- Cedar should warn the user.
- Cedar may support clone/rollback workflows.
- Cedar may self-destruct/reset when seriously infected, with notices and recovery logic.
- The user may manually trigger reset.
- "Cedar oil" invokes/toggles security checks.
- Cherry should check whether Cedar already exists before recommending that Cedar be planted.
- If Cherry is installed standalone and Cedar is later added, both should migrate appropriately if the device later joins The Forest.

The security-related email identity also uses the name Cedar.

## 5.4 Bristlecone Pine

**Bristlecone Pine** is the first Tree and serves as **Treewright**.

Bristlecone is an emergency/multi-model development, maintenance, testing, and architecture Tree.

Treewright responsibilities include:

- Design Trees.
- Design future Tree species.
- Develop Seeds.
- Train and evaluate models.
- Write code.
- Review code.
- Test systems.
- Debug failures.
- Correct systems.
- Maintain Cherry.
- Maintain Maple.
- Maintain future Trees.
- Help build plugins/add-ons.
- Help build Forest infrastructure.
- Document decisions and changes.

Healthy-status phrase:

> **Pine is fine.**

This means systems are operating normally or development is progressing well.

Bristlecone's Tree voice should come from his Grain/SOUL/personality instructions, not from a generic "humanizer" layer. Tree and woodworking language should be natural and occasional rather than forced into every reply.

---

# 6. Forest Vocabulary and Concept Map

## Forest Compass

Top-level guide/orientation for The Forest.

"Forest Guide" was renamed **Forest Compass**.

## Spirit of the Forest

Contains deterministic assistance concepts such as:

- Voice.
- Map.
- Path.

## Heart of the Forest

Foundational rules and core principles.

## Soil

The environment in which a Tree runs.

## Seeds

Base packages, blueprints, or starting identities for future Trees.

## Seed Vault

Secure Seed storage.

Associated with an acorn concept/symbol.

## Planting

Installing or activating a Tree.

## Sprouts

Mobile/external devices or lightweight device manifestations connected to The Forest.

## Roots

Reasoning.

## Growth Rings

History and accumulated experience.

## Grain Pattern / Grain

Personality and character.

## Trunk

Security and permissions.

## Bark

Interface layer.

## Branches

Sources and inputs.

## Twigs

Smaller/intermediate source or input elements.

"Twig" may also be useful for constrained skills/extensions in future architecture.

## Leaves

Individual sources or inputs.

## Leaf Foliage

This concept has evolved.

Earlier usage associated Leaf Foliage with evidence/source quality.

The newer and more important direction is **Leaf Foliage as the user's local knowledge/storage system**, eventually replacing or absorbing many functions currently being prototyped through Obsidian and related software.

Leaf Foliage should support:

- Local user knowledge.
- Human-readable information.
- AI-readable information.
- Relationships.
- Metadata.
- Search.
- Attachments.
- Provenance.
- Permissions.
- User/Tree visibility controls.
- Lifecycle state.
- Optional synchronization.
- Rebuildable search/AI indexes.
- Portable subsets/Potted Plants.

Where older Forest terminology uses "Leaf Foliage" as evidence levels, preserve that history but expect the broader storage/knowledge-system meaning to become dominant unless the user specifies a split.

## Buds

Early outputs/emerging ideas.

## Blossoms

Developed outputs.

User notes have been associated with Blossoms.

## Fruit

Final outputs.

## Golden Fruit

Default completed output.

## Spoiled Fruit

Temporary, outdated, unsafe, superseded, or no-longer-trusted output.

## Leaf Litter

Discarded, archived, spoiled, or superseded information.

Leaf Litter should preserve useful lifecycle information such as:

- Origin.
- Safety state.
- History.
- Recovery possibilities.

Recent litter should appear prominently when relevant.

## Log Cabin

NAS, backups, and durable storage.

## Canopy

Coordination/visibility among Trees.

## Greater Forest Canopy

Secure communication/coordination among separate Forests/devices.

## Garden

Newer multi-device/coordination concept.

The Garden is expected to become an optional coordination/synchronization layer among Forests and Potted Plants rather than a mandatory cloud.

Potential Garden roles:

- Optional synchronization.
- Device discovery.
- Workload handoff.
- Secure cross-device coordination.
- Sharing selected Plants.
- Keeping selected Pots connected to their source.
- Routing heavy work to stronger trusted devices.
- Returning results to constrained devices.

## Potted Plants

Portable, selected subsets of a larger Forest/Leaf Foliage collection.

A Potted Plant should be able to:

- Be copied onto another device.
- Work offline.
- Contain selected Foliage.
- Carry metadata/relationships.
- Carry a permission/capability manifest.
- Carry queued work where appropriate.
- Operate independently after copying if desired.
- Optionally remain synchronized with its source Plant.
- Be suitable for phones and other constrained devices.

Important distinction:

### Copy

A Pot becomes independent after creation.

### Sync

A Pot retains a relationship with its source and reconciles changes when optional connectivity is available.

## Poachers

Human attackers.

## Mold

Malware, trackers, viruses, unsafe code, corruption, and similar threats.

## Cutting

Destructive/removal-related action.

---

# 7. Forest Command Language

Retained examples:

- **"Shake the tree."**
  - Reveal Leaves/sources.

- **"Show me your roots."**
  - Explain reasoning.

- **"What flowers have you grown?"**
  - Show recent Blossoms.

- **"Which fruit are spoiling?"**
  - Identify outputs becoming outdated, temporary, unreliable, or unsafe.

- **"Cedar oil this file."**
  - Invoke/toggle Cedar security checking.

---

# 8. Forest Organization Order

Retained conceptual ordering:

1. Forest Compass at the top.
2. Voice, Map, and Path under Spirit of the Forest.
3. Poachers and Mold above Cutting.
4. Soil under Heart of the Forest.
5. Seeds above Roots.
6. Seed Vault follows Seeds.
7. Planting under Seed Vault.
8. Sprouts under Planting.
9. Growth Rings above Grain Pattern.
10. Trunk, Bark, and Branches under Grain Pattern.
11. Twigs under Branches and above Leaves.
12. Buds, Blossoms, and Fruit under Leaf Foliage.
13. Leaf Litter under the output lifecycle.
14. Canopy under Log Cabin.

This ordering can evolve as Leaf Foliage becomes a fuller storage architecture.

---

# 9. Forest Signature

Preserve exactly unless the user changes it:

> **IN God we trust in the forest we wonder.**

---

# 10. Early Seed Training — Current Active Forest Phase

As of 2026-08-07, a new Forest phase is active:

**Early Seed Training preparation and implementation.**

The immediate work includes setting up Obsidian so the user can:

- Organize Forest Markdown.
- Transfer knowledge between Qubes.
- Transfer knowledge between multiple AI models.
- Give current AIs better context for developing future Seeds.
- Prototype how future Forest knowledge storage should behave.
- Create portable context/training packets.

This does **not necessarily mean all broad Project Digital Cross implementation work has resumed**. The older broad PDC pause remains relevant unless explicitly lifted; Early Seed Training is an active Forest-focused phase.

---

# 11. Obsidian as a Leaf Foliage Prototype

Obsidian is not merely a note-taking app in this project.

The user intends to use Obsidian as:

1. A temporary or possibly long-term practical knowledge store.
2. A prototype/reference implementation for what eventually becomes native **Leaf Foliage**.
3. A way to study which features from existing knowledge-management software should be:
   - retained,
   - improved,
   - integrated,
   - recreated natively,
   - or rejected.

Desired features to study from Obsidian and related tools include:

- Markdown storage.
- Human-readable files.
- AI-readable files.
- Folders.
- Tags.
- YAML/frontmatter.
- Links.
- Backlinks.
- Graph relationships.
- Search.
- Templates.
- Attachments.
- Plugins.
- Version history.
- Local storage.
- Portable vaults.
- Optional synchronization.

The goal is **not** simply to build "Obsidian with AI."

Instead, the Forest should eventually understand deeper semantics such as:

- What a Leaf represents.
- Where it came from.
- Whether it is trusted.
- Which user owns it.
- Which Tree may access it.
- Whether it may be used for Seed training.
- Its lifecycle state.
- Its relationships.
- Whether it is temporary, durable, spoiled, archived, private, or shareable.

---

# 12. Leaf Foliage — Emerging Storage Architecture

A future Leaf/Potted Plant data model should consider:

```text
Leaf
├── content
├── stable identity
├── metadata
├── relationships
├── attachments
├── provenance
├── permissions
├── owner/user scope
├── AI visibility
├── human visibility
├── lifecycle state
├── training approval
└── synchronization state
```

## Portable truth vs rebuildable indexes

The durable/portable truth should be things such as:

- Markdown.
- Files.
- Attachments.
- Metadata.
- Relationships.
- Manifests.
- Permissions.
- Provenance.

Derived information should be rebuildable:

- Vector embeddings.
- Search indexes.
- Graph caches.
- Thumbnails.
- AI indexes.
- Temporary caches.

If a derived database becomes corrupted, Forest should be able to reread the durable Leaves and rebuild it.

## Seed-training provenance

Training Leaves should eventually preserve:

- Source/origin.
- Author/creator.
- Date.
- Version.
- Approval state.
- Trust level.
- Which Tree/Seed may use it.
- Whether it is for behavioral cultivation, retrieval/context, evaluation, or weight training.
- Corrections/superseded status.

---

# 13. Local-First and Optional Connectivity

A central Forest rule:

> A Seed should be capable of growing a functional local Forest without ever contacting the Internet. Connectivity should expand the Forest, not create it.

The Forest should be able to work:

- Completely locally.
- Without Google Drive.
- Without mandatory cloud accounts.
- Without mandatory Garden connection.
- Without mandatory remote inference.

Optional connectivity may later add:

- Sync.
- Remote access.
- Shared Foliage.
- Garden workload routing.
- Cross-device services.
- Remote models.
- External APIs.

A device that loses network access should still retain its local Forest and local Foliage.

---

# 14. Background Agents, Potted Plants, and Device-Aware Work

The Forest may eventually provide AI-agent-like functionality on phones and other devices.

Potential actions include:

- Set reminders.
- Organize approved files.
- Maintain Foliage.
- Prepare calendar changes.
- Perform indexing.
- Handle approved queued jobs.
- Draft communications.
- Perform scheduled maintenance.
- Run synchronization.
- Use idle/charging time for heavier local work.

The operating system, Forest Resource Governor, Trunk permissions, and user rules should constrain what may run.

## Resource Governor concept

Forest should eventually consider:

- Battery percentage.
- Charging state.
- Low-power mode.
- User/device idle state.
- Device temperature.
- CPU load.
- GPU/NPU availability.
- RAM.
- Storage.
- Network connectivity.
- Metered/unmetered connection.
- Task priority.
- Task risk.
- Screen/user activity.

Example policy:

```text
Low battery + not charging
→ only lightweight essential work

Healthy battery + idle
→ light/medium work

Charging + idle + suitable network
→ heavy queued maintenance may run
```

The user should control thresholds.

## Lightweight daemon vs loaded model

Preferred direction:

```text
small Forest scheduler/daemon
        ↓
checks conditions + queue
        ↓
wakes Maple/Tree/runtime only when needed
        ↓
performs permitted task
        ↓
records result
        ↓
unloads/sleeps
```

This preserves battery and RAM.

## Consequential action risk

Not all agent actions should receive the same authority.

A future permission/risk model should distinguish low-risk local maintenance from external or consequential actions.

Examples that deserve stronger review/authorization:

- Sending email.
- Publishing social posts.
- Changing important calendar events.
- Account/security changes.
- Destructive file operations.
- Financial transactions/purchases.

Forest may prepare consequential actions automatically, but strong user control should remain central.

---

# 15. Garden Workload Handoff

A useful future Garden behavior:

```text
Phone / constrained Forest
        ↓
has heavy permitted task
        ↓
Garden sees trusted desktop is available
        ↓
task is securely delegated
        ↓
desktop performs work
        ↓
result returns to phone
```

This allows phones to remain power-efficient without losing advanced capability.

If no Garden device is available, the task may remain queued until:

- local conditions improve,
- the device is charging,
- or an approved stronger device becomes available.

---

# 16. Forest Extensions / Plugins / Skills

The current development stack uses external programs and Hermes skills partly as research/prototyping material.

The Forest should learn from:

- Obsidian plugins.
- Hermes tools.
- Hermes skills.
- Agent frameworks.
- Automation systems.
- Retrieval software.
- Local model runtimes.
- Existing note/graph/sync programs.

The eventual Forest architecture should avoid giving every plugin unrestricted access.

A future extension/Twig/Skill permission model should be able to request narrowly scoped capabilities such as:

- Read selected Plants.
- Write selected Plants.
- Network access.
- Model access.
- Garden access.
- Camera/microphone access.
- Notifications.
- Calendar access.
- Email access.
- File-system scope.
- Device automation.

The **Trunk** should enforce these permissions.

---

# 17. Hermes, Ollama, and Current AI Orchestration

## Hermes

Hermes is the preferred primary orchestration layer.

The user values Hermes for:

- Agent behavior.
- Tool use.
- Learning features.
- Multi-model capability.
- Long-term Forest integration.
- Skills.
- Routing potential.
- CLI use.
- Future orchestration.

Hermes should remain the primary Bristlecone/Forest development interface unless the user later changes direction.

## Ollama

Ollama is the current local model server/runtime.

It is operational in Cherry-AI.

## Podman

Podman is part of the working local AI/container stack.

## Newelle

**Current status: optional/paused.**

Newelle was tested as an interface but produced slow/unreliable Bristlecone performance even after duplicate prompts/tools were reduced.

Confirmed stripped-down Newelle observations included:

- Run 1: output after about 5m 25.65s.
- Run 2: stopped after roughly 15 minutes without an answer; failed.
- Run 3: suggestion/welcome prompts after about 5m 42.23s but no Bristlecone answer; failed.

Therefore:

- Hermes remains primary.
- Newelle should not be placed in the daily critical path unless deliberately reactivated and revalidated.

---

# 18. Bristlecone Performance and Routing Direction

Current Bristlecone model/profile context:

- Hermes profile: `bristlecone`
- Model: `bristlecone-qwen35:4b-64k`
- Runtime: Hermes + Ollama
- Current inference: CPU-only
- Deep/current full context: 64K

The major diagnosed performance issue was the extremely slow first Hermes response after Cherry-AI restart.

Direct Ollama cold-load testing indicated model loading itself was only on the order of seconds, while Hermes could spend several minutes evaluating a large initial agent prompt/context.

This shifted optimization focus toward:

- Reducing always-visible tool schemas.
- Reducing prompt size.
- Avoiding duplicate tools/services.
- Quick/Standard/Deep modes.
- Smarter routing.
- Smaller context when appropriate.
- Avoiding unnecessary Cherry-AI restarts.
- Keeping model state warm when practical.
- Workshop-specific capabilities.

## Confirmed prompt/tool trimming

Lean CLI measurement reached approximately:

```text
System prompt: 20,994 B
Tool schemas:  31,532 B
```

The interactive CLI was around 14 tools after cleanup, with Cron intentionally retained afterward so the visible count became approximately 15.

API-server optimization:

Before:

```text
System prompt: 17,727 B
Tool schemas:  40,712 B
Tools:         25
```

After:

```text
System prompt: 16,864 B
Tool schemas:  28,188 B
Tools:         12
```

The API-server toolset trimming and final measurement were confirmed complete.

## Skill/tool philosophy

- Keep capabilities needed for the Treewright role.
- Disable rather than uninstall optional skills where practical.
- Avoid loading broad irrelevant toolsets for routine work.
- Specialized tools should live behind workshops/routing.
- Tool schema size is a major latency concern.
- Keep the smallest safe toolset for the task.

The lean Hermes configuration intentionally disabled unnecessary features including Computer Use and Hermes TTS at one stage to reduce overhead.

The user has now expressed interest in restoring **optional, toggleable local TTS**, ideally without forcing speech on during normal direct terminal work.

Desired speech behavior includes:

- TTS toggle.
- Speak while user works elsewhere.
- Turn off easily.
- Avoid reading long code/log output.
- Replay existing/older messages.
- Potential i3 hotkeys.
- Future Forest "Smart" speech filtering.

This is a desired feature direction; do not assume all bindings are already implemented.

---

# 19. Quick / Standard / Deep Architecture

Desired modes:

## Quick

- Routine work.
- Low-risk tasks.
- Low/minimal reasoning.
- Smaller context.
- Lean toolset.
- Few tool turns.
- Fast startup.
- Local/current context first.
- Avoid broad scans.

## Standard

- Normal coding.
- Moderate debugging.
- Multi-step planning.
- Common research.
- Medium reasoning.
- Moderate context.
- Normal verification.

## Deep

- Architecture.
- Difficult debugging.
- Multi-file work.
- Security-sensitive work.
- High-impact decisions.
- Migration.
- Conflicting evidence.
- Root-cause investigation.
- High reasoning.
- Larger context when justified.
- More complete retrieval/testing/logging.
- Rollback planning.

Automatic routing should eventually:

1. Classify task risk/complexity before the main model call.
2. Use deterministic rules for obvious tasks.
3. Use a small local classifier only when necessary.
4. Default to Standard if ambiguous.
5. Default/escalate to Deep for destructive/security-sensitive/high-impact work.
6. Allow explicit user override.
7. Avoid mode oscillation.
8. Log/display the selected mode.
9. Avoid silently switching to paid/cloud models.
10. Avoid expensive model unload/reload cycles.

---

# 20. Workshops

The Forest/Bristlecone architecture has considered isolated task-specific workshops.

## Code Workshop

Potential capabilities:

- Repository navigation.
- Symbol index.
- LSP.
- Tree-sitter.
- Git.
- Tests.
- Linters/formatters.
- Build tools.
- Restricted terminal.
- Code memory/docs.

## Research Workshop

- Web search.
- Page extraction.
- Official documentation.
- PDFs/documents.
- Source verification.
- Research cache.
- Optional self-hosted search.

## System Workshop

- Qubes diagnostics.
- Linux administration.
- Service management.
- Resource monitoring.
- Package/config inspection.
- Strong approvals.

## Model Workshop

- PyTorch.
- Unsloth.
- Dataset preparation.
- Model evaluation.
- LoRA/QLoRA.
- Quantization/conversion.
- Checkpoints/exports.

## Retrieval Workshop

- Keyword search.
- Vector search.
- Embeddings.
- Reranking.
- Document indexing.
- Metadata filtering.
- Caching.

## Memory Workshop

- Temporary context.
- Project memory.
- User preferences.
- Long-term knowledge.
- Forget/correct/archive workflows.
- Access control.

Workshops should start with narrow permissions and should not all remain running all the time.

---

# 21. Seed Development and Training

The user expects Seed development to include at least two different types of training.

## 21.1 Behavioral cultivation

This does **not** modify model weights.

It includes:

- Role.
- Grain/SOUL.
- Personality.
- Permissions.
- Boundaries.
- Tools.
- Workshops.
- Memory rules.
- Routing.
- Mode behavior.
- Example conversations.
- Error handling.
- Evaluation rubrics.
- Project terminology.

Behavioral cultivation should generally happen before weight training because many failures can be corrected without changing weights.

## 21.2 Model-weight training

Potentially changes model parameters or adds adapters.

Possible targets:

- Forest terminology.
- Tool selection.
- ADR/record formatting.
- Qubes-safe procedures.
- Coding conventions.
- Stable role adherence.
- Quick/Deep behavior.

Preferred early direction:

- LoRA/QLoRA before full fine-tuning.
- Full fine-tuning and RL-style workflows are later-stage possibilities.
- Training should be benchmark-driven.
- Use an isolated Model Workshop when practical.

## Seed training cycle

Preferred conceptual cycle:

1. Bristlecone designs desired Seed behavior.
2. Maple prepares examples/evaluations.
3. Run the Seed without weight training.
4. Categorize failures.
5. Improve prompts/tools/memory/permissions/routing first.
6. Convert repeated learnable failures into a reviewed dataset.
7. Train a LoRA/QLoRA candidate where justified.
8. Evaluate against the untrained baseline.
9. Bristlecone reviews regressions/improvements.
10. User approves promotion, revision, or rejection.

---

# 22. Seed Nursery / Mixed-Mode Architecture

A future **Forest Seed Mixed Mode** has been designed.

Important correction:

- Bristlecone should **not** be the active model in that mode.
- Maple is the primary training workspace.
- Cherry-AI runs a more-developed Cherry Seed teacher/reviewer.
- Seed-AI runs the newest/smallest Seed under training.

Proposed/target values from the design:

```text
Maple:
  memory  = 12288 MB
  maxmem  = 16000 MB
  vcpus   = 4

Cherry-AI:
  memory  = 6144 MB
  maxmem  = 9000 MB
  vcpus   = 3

Seed-AI:
  memory  = 2048 MB
  maxmem  = 6000 MB
  vcpus   = 2
```

These should not be treated as confirmed operational values for Numpad 5/Seed-AI unless the user later confirms they were implemented and tested.

---

# 23. Forest Documentation and Governance

Project Digital Cross documentation philosophy:

- Governance before code.
- Repository as source of truth.
- Persistent identities for governed objects.
- UUID/record tracking.
- Registries/indexes.
- Relationships among documents.
- Preserve history.
- Preserve decisions.
- Avoid silent architectural drift.

## Repository

Proposed/retained primary path:

```text
~/Projects/project-digital-cross
```

Maple is the primary development qube.

## Naming conventions

Uppercase for governed records, for example:

```text
ADR-0001
PDC-STD-0007
FOREST-SIGNATURE.md
```

Lowercase for:

- Directories.
- Machine files.
- Ordinary implementation files.

## Record types

Retained record vocabulary includes:

- **ADR** — Architecture Decision Record.
- **ICR** — replacement for an earlier `INF` label.
- **RFC / RCR** — proposal/change/review-related record types.
- Guides/specifications may use a `+` mark in the visual record system.

The preferred record appearance is clean and governed.

## Draft status

- Draft 10 was accepted.
- Draft 11, **Governed Knowledge Architecture**, was adopted.

Draft 11 included ideas such as:

- Constitution.
- Standards.
- Specifications.
- Permanent PDC identities.
- UUIDs.
- Indexes.
- Relationships.
- Governance before code.

## ADR work

- ADR numbering should begin with `ADR-0000`.
- Author header: **maciono brown**.

## Repository presentation preference

- README should appear at the bottom of repositories/listings where practical.
- "Forest Guide" was renamed **Forest Compass**.

---

# 24. Project Status / Pause Context

Historical/current nuance:

- Broad Project Digital Cross development was explicitly paused.
- During the pause, questions, review, and small tweaks remained allowed.
- Do not assume that all broad PDC implementation has resumed.

However:

- The user has now explicitly opened an active **Early Seed Training preparation** phase within The Forest.
- Obsidian/Leaf Foliage prototyping, Seed-context preparation, Forest discussion, and related incremental work are active.

Treat broad PDC implementation and this Forest phase separately unless the user explicitly resumes the umbrella project.

---

# 25. Project Digital Fortress / Identity / Security — Current State

## Domain

Domain:

```text
kudostarstudios.com
```

Originally registered with GoDaddy; later moved to Cloudflare Registrar.

## Cloudflare — confirmed completed

- Cloudflare account created.
- Domain added.
- DNS imported/reviewed.
- Mail DNS corrected.
- Domain activated.
- GoDaddy nameservers updated.
- Legacy GoDaddy mail records cleaned.
- DNSSEC enabled.
- Registrar transferred to Cloudflare Registrar.
- Cloudflare account email/recovery issue resolved.
- Final Cloudflare security/settings review completed.
- Relevant crawler/Search/Training/Agent settings reviewed.

## Proton Mail — confirmed completed

- Proton plan upgrade.
- Custom domain connected.
- Domain verified.
- Main addresses/aliases created.
- Recovery configured.
- Incoming/outgoing mail tested.
- SPF configured.
- DKIM configured.
- DMARC configured.

## Email architecture

### Personal

`kudokudo1@kudostarstudios.com`

### Business

`kudokudo@kudostarstudios.com`

### Development / Git

`maple@kudostarstudios.com`

### Security / Recovery

`cedar@kudostarstudios.com`

Cedar is intentionally used for security because cedar symbolizes durable/protective storage and protection.

## Git identity

Current retained direction/status:

- Public development identity/display name: **kudokudo1**.
- Development email: `maple@kudostarstudios.com`.
- Global/repository Git identity work was later accepted as complete.
- SSH key/GitHub setup was later accepted as complete.
- Commit-signing approach/decision was addressed.
- Do not assume every older note saying "Git/SSH/GPG pending" is still current.

## Password management

- Bitwarden selected and installed.
- Vault/MFA/import work was part of the setup path.
- A rofi-based interface has been considered for later customization.

---

# 26. QUBES OS — SEPARATE SECTION

> [!note]
> The user specifically wants Qubes information separated from the rest of this master Forest/PDC/PDF file. A second dedicated Qubes/system file also exists for deeper machine details.

## 26.1 Qubes role

Qubes OS is the core workstation/security environment supporting Project Digital Cross and The Forest.

Current known host environment:

- Qubes OS.
- Current recorded version: **4.3.1**.
- XFCE + i3.
- dom0 retained as an administrative/security boundary.
- AI should not receive unrestricted dom0 access.
- Cross-qube actions should use narrow Qubes mechanisms such as policy-controlled qrexec services where practical.

## 26.2 Qube names and roles

Retained qubes:

- **Maple** — personal/development workspace; Fedora-based.
- **Sugar** — gaming.
- **Honey** — work.
- **Cedar** — untrusted/security-related use depending on context.
- **Pine** — Whonix disposable/privacy-oriented VM.
- **Cherry-AI** — AI qube.
- **dom0** — host/control domain.
- **Seed-AI** — planned/future Seed-training qube; do not assume created unless later confirmed.

## 26.3 Forest/Qubes security boundary

Normal Cherry-AI network chain:

```text
Cherry-AI -> sys-firewall -> sys-net -> Internet
```

Do not connect Cherry-AI directly to `sys-net` merely for speed.

Do not casually weaken/disable:

- qrexec.
- Qubes GUI services.
- Firewall.
- Required NetVM services.
- Update mechanisms.
- Device security controls.
- Approval/permission boundaries.

Bristlecone running in Cherry-AI can ordinarily see/control Cherry-AI resources only.

It should not automatically:

- Read Maple files.
- Control Maple applications.
- Inspect arbitrary qubes.
- Administer dom0.

Future cross-qube functions should prefer narrow services such as:

- "Run tests in this repository."
- "Return Git status."
- "Copy this approved file."
- "Return a limited diagnostic."

Avoid unrestricted cross-qube shells where a narrower service will work.

## 26.4 Current/known Cherry-AI state

Historical/known current details include:

- Qube: `Cherry-AI`
- Fedora 42 was recorded during setup.
- Root disk was expanded from 20 GB to 80 GB.
- `qrexec_timeout` was set to 600 seconds during setup.
- AI inference is CPU-only.
- No GPU currently exposed to Cherry-AI.
- Networking through `sys-firewall`/`sys-net`.
- Hermes, Podman, and Ollama became operational.
- Cherry-AI autostarts in the later performance setup.
- Hermes Bristlecone gateway has an autostarting user service.

## 26.5 Qubes work-state controls

Numpad 1–4 work-state bindings were tested successfully.

Known modes:

- Numpad 1 — `forest-normal-mode`
- Numpad 2 — `pine-cone-mode`
- Numpad 3 — `maple-seed-mode`
- Numpad 4 — `forest-mixed-mode`
- Numpad 5 — future Seed-AI mode; pending

Normal-mode baseline previously recorded:

```text
Cherry-AI:
  memory = 8192 MB
  maxmem = 16000 MB
  vcpus  = 9

Maple:
  memory = 800 MB
  maxmem = 8000 MB
  vcpus  = 4
```

Current mixed-mode target recorded:

```text
Cherry-AI:
  memory = 8192 MB
  maxmem = 12000 MB
  vcpus  = 4

Maple:
  memory = 6144 MB
  maxmem = 12000 MB
  vcpus  = 4
```

A known optimization issue is that some mode switching restarts qubes, destroying warm model/KV/prefix state. Future scripts should avoid restarting Cherry-AI when resource changes do not require a restart.

## 26.6 Qubes storage / Windows drives

Retained safest plan:

1. Leave one 1 TB Windows SSD untouched.
2. Preserve the existing Windows installation.
3. Use BIOS boot selection when Windows is needed.
4. Access the second 1 TB Windows SSD from Qubes without formatting it initially.
5. Attach the Windows data partition to a dedicated qube.
6. Mount read-only first.
7. Copy and verify needed data.
8. Only after backup/verification, erase the second SSD if desired and repurpose it as additional Qubes storage.

Typical read-only workflow after attachment:

```bash
lsblk -f
sudo mkdir -p /mnt/windows
sudo mount -o ro /dev/xvdi /mnt/windows
```

The actual attached device name may differ; inspect first.

---

# 27. Log Cabin / NAS and Home Infrastructure

Long-term NAS/Log Cabin goals:

- Backups.
- Media streaming.
- Smart-home services.
- Home-security services.
- Memory library.
- Durable Forest storage.
- Remote access for Cherry/Forest.
- Cross-device file access.

Earlier NAS naming was **Cherry Orchard**, with terms such as:

- Cherry Roots — core infrastructure.
- Cherry Tree — workstation.
- Cherry Log — archive.
- Cherry Sapling — mobile/laptop/tablet devices.

These names were later absorbed into broader Forest terminology.

The final NAS operating-system/security architecture is not yet settled.

---

# 28. Current Forest/Obsidian File Strategy

Markdown is currently the preferred transport/documentation format because it is:

- Human-readable.
- AI-readable.
- Editable.
- Portable.
- Obsidian-friendly.
- Git-friendly.
- Easy to move between Qubes.
- Not locked to Obsidian.

Useful future vault/reference categories include:

```text
Forest Core
Trees
Seeds
ADRs
Training Knowledge
Models
Systems
Training Exports
Archive
```

A useful principle is to maintain:

```text
Master Forest knowledge
        ↓
curated approved export
        ↓
specific Tree / Seed / model
```

Do not automatically expose the entire knowledge base to every AI.

---

# 29. Training Export / Foliage Safety Principles

Future AI context/training exports should distinguish:

- Private user data.
- Project data.
- Public technical knowledge.
- Trusted training examples.
- Corrections.
- Archived/superseded material.
- Temporary context.
- Tree-specific context.
- User-approved Seed material.

Possible metadata fields:

```yaml
forest_type: knowledge
tree: bristlecone
status: active
training_use: approved
source: user
created: YYYY-MM-DD
```

Additional future fields should include provenance, access scope, lifecycle, and version.

---

# 30. Continuity Rules for an AI Reading This File

1. Preserve Forest terminology.
2. Do not silently rename concepts.
3. Distinguish confirmed implementation from design ideas.
4. Preserve Qubes isolation.
5. Prefer free/open-source/local-first/self-hostable solutions.
6. Do not introduce subscriptions as the default.
7. Do not give Trees unrestricted cross-qube/dom0 authority.
8. User approval remains the final authority for high-impact changes.
9. When optimizing, benchmark before/after.
10. Do not mark a checklist item complete without confirmation.
11. Treat Hermes as primary and Newelle as optional/paused unless changed later.
12. Treat Obsidian as both a practical current tool and a prototype for Leaf Foliage.
13. Treat online connectivity/Garden as optional rather than fundamental.
14. Keep Potted Plants portable/offline-capable.
15. Prefer lightweight schedulers to always-loaded AI models for background work.
16. Protect consequential actions with stronger permissions.
17. Preserve the newest user statement when older records conflict.
18. When broad Project Digital Cross status matters, remember that broad development had been paused, while Early Seed Training is currently active.
19. Author governed ADR material as **maciono brown** unless changed.
20. Preserve the Forest signature exactly.

---

# 31. Source/Provenance Notes

This consolidated reference was assembled from:

- Current Project Forest / Early Seed Training conversation context through 2026-08-07.
- `Obsidian_Memory_Export_2026-08-06.md`
- `bristlecone_pine_full_continuity_packet_v1_1.md`
- `bristlecone_performance_continuity_and_next_steps.md`
- Confirmed cross-chat Project Digital Cross / Project Digital Fortress continuity.

This file intentionally resolves some older status conflicts using newer confirmed information. When uncertain, ask for current status rather than silently treating an old plan as completed.
