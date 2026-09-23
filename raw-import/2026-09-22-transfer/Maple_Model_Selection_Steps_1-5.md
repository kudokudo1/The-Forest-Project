---
title: Maple Model Selection - Steps 1-5
created: 2026-08-12
project: The Forest Project
tree: Maple
phase: Model Selection
status: planning
tags:
  - the-forest
  - maple
  - llm
  - agent-model
  - model-selection
  - files
  - media
  - email
  - local-ai
  - workspace
  - leaf-foliage
aliases:
  - Maple Steps 1-5
  - Maple Model Planning
  - Maple Requirements
---

# Maple Model Selection — Steps 1–5

## Purpose

This note captures the current definition of **Maple** for The Forest Project before researching specific LLM and agent-model candidates.

The model-selection process being used for each Tree is:

```text
1. Define the Tree's job
2. Define intelligence requirements
3. Define operational constraints
4. Define Forest-specific requirements
5. Define origin/licensing requirements
6. Research candidate pool
7. Shortlist serious candidates
8. Build Tree-specific benchmarks
9. Select Small / Big / specialist models
```

This document covers **Steps 1–5**.

# Step 1 — Define Maple's Job

## Core Identity

Maple is The Forest's **personal workspace, file, media, and information-management Tree**.

Maple's purpose is to turn messy, scattered, difficult-to-manage information into clean, searchable, portable structure with minimal user effort.

A useful distinction is:

```text
Cherry → "What does the user need?"
Maple  → "Where does this information belong, how should it be organized, and what should happen to the user's files/content?"
```

Maple is not primarily a conversational companion. He is responsible for helping the user's digital workspace remain organized, searchable, portable, consistent, recoverable, personalized, and usable by other Trees.

## Primary Responsibilities

### File and folder organization

Maple should be exceptionally good at moving, renaming, sorting, categorizing, archiving, deduplicating, and maintaining files and folders. He should preserve project structure, detect misplaced content, maintain naming conventions, and prepare files for other Trees.

### Leaf Foliage caretaker

Maple should have one of the deepest operational relationships with **Leaf Foliage**.

```text
raw information
→ determine subject
→ extract metadata
→ create/update Leaf
→ link related Leaves
→ update index
→ maintain graph structure
```

Responsibilities include frontmatter, stable IDs, links/backlinks, orphan detection, duplicate detection, source preservation, Obsidian compatibility, Roots/graph relationships, and retrieval preparation.

### Retrieval preparation

Maple should make retrieval better for every other Tree by maintaining structured metadata, indexes, links, and project organization rather than forcing models to inspect huge raw file sets.

### Lightweight pass-through work

Many Maple tasks should require very little reasoning.

```text
request
→ tiny Maple Workshop
→ file capability
→ move/rename/convert
→ verify
→ done
```

Maple should be capable of acting as a lightweight organizer/pass-through Tree when the job is routine.

### Project/workspace management

Maple should understand and maintain project structures such as:

```text
Project/
├── README
├── Research/
├── Decisions/
├── Assets/
├── Drafts/
├── Archive/
└── Tasks/
```

### Import/export

Maple should be a primary Tree for moving information into and out of The Forest, including Obsidian vaults, folders of documents, Markdown exports, and portable project archives. The user should retain ordinary readable files rather than being locked into a proprietary format.

### Backup and synchronization assistance

Maple can prepare backups, identify changed files, synchronize approved locations, resolve simple conflicts, and verify expected files. Cedar may own security policy, but organization and movement fit Maple.

## Media editing

Maple should also handle consumer-oriented photo, video, and audio work where practical. He should use approved knowledge of the user's preferences, project context, and related files to personalize edits.

Possible capabilities include:

- crop and resize
- background removal
- color correction
- brightness/contrast
- compositing
- adding/removing visual elements through specialist models/tools
- restoration/enhancement
- batch image processing
- thumbnails
- video trimming and joining
- re-encoding
- audio extraction
- subtitles/captions
- compression
- media-library organization

The preferred architecture is:

```text
Maple
  ↓
understands request + user preferences + project context
  ↓
selects media capability
  ↓
image/video/audio engine performs work
  ↓
Maple evaluates and stores result
```

## File conversion

Maple should support practical conversion such as:

```text
DOCX → PDF
PNG → JPG/WebP
HEIC → JPG/PNG
WAV → MP3/FLAC
MP4 → WebM
Markdown → HTML
CSV → XLSX
```

Maple should understand lossy vs lossless conversion, transparency, metadata, print vs web usage, compression, codec compatibility, and preservation requirements.

Preferred safety pattern:

```text
source
→ convert
→ verify output
→ preserve original unless replacement explicitly requested
```

## Email management

Maple should manage ordinary personal email workflows:

- reading
- searching
- organization
- labels/folders
- thread summaries
- important-mail identification
- reply drafting
- attachment retrieval
- saving attachments into projects
- linking email to Leaves/projects
- follow-up reminders
- routine inbox cleanup

A future dedicated **Business Tree** may reuse the same Forest-level email capabilities with business-specific workflows.

## Boundaries

Maple is not Cherry, Cedar, McIntosh, or Bristlecone Pine.

- Cherry owns the deepest personal relationship, Diary, and general personal-assistant role.
- Cedar owns final security authority.
- McIntosh owns deep technical troubleshooting and repair.
- Bristlecone Pine owns Treewright/development/model-engineering work.

## User-facing vs background

Maple can be heavily background-oriented.

User-facing requests may include:

- "Organize these files."
- "Find that PDF."
- "Clean up this project."
- "Convert these photos."
- "Find that email and save the attachment."
- "Make this image match the previous ones."

Background work may include indexing, metadata maintenance, directory watching, duplicate detection, retrieval-index preparation, graph maintenance, and queued conversions.

## Potential Utility + Reasoner split

Maple may fit this architecture better than a simple Small/Big split:

```text
Maple Utility
→ very small / fast
→ file movement
→ indexing
→ metadata
→ simple conversion
→ routine classification
→ routine email actions

Maple Reasoner
→ ambiguous organization
→ project restructuring
→ complex retrieval
→ media planning
→ multi-step file/email workflows
```

# Step 2 — Intelligence Requirements

## Agent and tool use — Extremely High

Maple's core pattern is:

```text
understand request
→ inspect context
→ select capability
→ execute
→ verify
→ report
```

He must reliably choose tools, use exact paths, chain operations, handle failure, avoid inventing files/tools/results, distinguish read/write actions, respect permissions, and operate with small dynamic Workshops.

## Organization and classification — Extremely High

Maple must distinguish project, subject, type, archive state, duplicates, source vs finished artifacts, private vs shared, and temporary vs durable material without over-organizing.

## Retrieval and search — Extremely High

Maple should search across files, folders, Leaves, email, attachments, media, metadata, and project history using semantic, temporal, and relational clues.

## Multimodal understanding — Very High

Maple should reason across images, screenshots, scanned documents, PDFs, video, audio, and document layouts. Specialist models/tools may perform the heavy processing.

## Context-conditioned personalization — Very High

Maple should learn functional preferences such as folder structures, naming conventions, image dimensions, preferred formats, export quality, media style, common project paths, and email organization.

This is operational personalization, not Cherry Diary access.

## Structured reasoning and planning — High

Large jobs should follow a plan:

```text
inspect
→ identify structure
→ detect duplicates
→ derive organization
→ preserve originals
→ reorganize
→ verify
→ update indexes
```

## Precision and conservatism — Extremely High

Maple should favor reversible operations, preserved originals, verified writes, dry-runs/previews for large changes, and asking only when ambiguity materially matters.

## Email reasoning — High

Maple must understand threads, senders, attachments, dates, importance, follow-up state, categories, and distinguish:

```text
read/search
organize
draft
send
delete
```

## Media-editing judgment — High

Maple should interpret requests such as "make this cleaner" or "match the previous one" using reference comparison, project memory, visual judgment, restraint, and output-format awareness.

## File-format knowledge — High

Maple needs broad practical conversion knowledge while deterministic tools perform the operation.

## Long context — Medium to High

Long context is useful, but indexes, search, summaries, metadata, and graph relationships are more important than giant prompt dumps.

## Memory behavior — High

Maple needs operational memory, not Cherry's Diary.

## Coding ability — Medium

Maple should understand practical scripting for batch renames, metadata extraction, indexing, CSV cleanup, simple transformations, and automation.

## General reasoning — High

Maple needs strong practical and structured reasoning.

## Autonomy — Medium to High

Low-risk reversible work can be more autonomous. High-risk actions such as deleting files, overwriting originals, sending mail, permanently removing messages, or destructive conversion require stronger confirmation/permission.

## Priority map

```text
Agent / Tool Use            ★★★★★
Precision / Reliability     ★★★★★
Organization                ★★★★★
Retrieval / Search          ★★★★★
Multimodal Understanding    ★★★★★
Personalization             ★★★★☆
Planning                    ★★★★☆
Email Reasoning             ★★★★☆
Media Judgment              ★★★★☆
File-Format Knowledge       ★★★★☆
General Reasoning           ★★★★☆
Memory                      ★★★★☆
Long Context                ★★★☆☆
Coding                      ★★★☆☆
Warmth / Personality        ★★☆☆☆
```

Maple should feel **competent, calm, organized, precise, and familiar with the user** more than deeply emotional or companion-like.

# Step 3 — Operational Constraints

## Utility + Reasoner architecture

Maple Utility should be lightweight and frequently available. Maple Reasoner should wake for harder organizational work and unload afterward.

## Very low idle resource usage

Background functions should use lightweight deterministic watchers. The LLM wakes only when judgment is needed.

## RAM / VRAM

Maple Utility should coexist with Cherry and other Trees without creating serious pressure. Maple Reasoner and media specialists may use more resources on demand.

## CPU-friendly work

Moving, renaming, hashing, conversion, indexing, compression, parsing, and similar operations should use normal deterministic utilities. The LLM provides intent, judgment, and orchestration.

## Concurrent Tree operation

Maple should support background jobs while Cherry, Cedar, Bristlecone, or other Trees are active.

## Background jobs survive model unload

```text
Maple plans job
→ worker receives manifest
→ Maple unloads
→ worker continues
→ Maple wakes for completion/error
```

This should apply to file moves, indexing, conversion, media encoding, email organization, backups, and downloads.

## Storage awareness

Maple should understand free space, destination capacity, temporary storage, archive expansion, conversion size, and duplicate-storage cost.

## Transactional operations

Preferred pattern:

```text
prepare
→ execute
→ verify
→ commit
```

## Undo / rollback

Meaningful operations should be journaled externally so "undo that" can be deterministic.

## Modular media processing

The core Maple LLM should not need to be the image generator, video engine, transcoder, audio model, or OCR system.

## Connector-based email

```text
Maple
→ Forest Email Capability
→ provider connector
```

## Local-first

Maple should remain useful offline for local files, Leaves, media, conversion, organization, search, and draft preparation.

## Context strategy

A filesystem index and targeted retrieval should replace dumping huge directories into model context.

## Batch-job specifications

Maple should convert large requests into deterministic manifests with inputs, filters, actions, outputs, preservation policy, verification, and resource priority.

## Pause / resume / cancel

Long jobs should track pending, running, completed, failed, and skipped items.

## Hardware adaptation

Maple should adapt strategy across powerful desktops, phones, and home servers.

## Specialist offloading

Repeated tool/environment failure should escalate to McIntosh. Deep security concerns should escalate to Cedar. Forest development should escalate to Bristlecone Pine.

## Quantization

Aggressive quantization is acceptable only if it preserves path accuracy, schemas, tool arguments, classification, and instruction adherence.

## Runtime portability

Maple's jobs, indexes, preferences, permissions, and operation history must live outside the model runtime.

# Core Addition — Resource-Aware Work Scheduling

Maple should not merely be lightweight. He should be **resource-aware and workload-aware**.

## Principle

```text
Foreground user activity
vs
Background Maple work
```

Maple should preserve the user's interactive performance.

If the user is gaming, video editing, compiling, running heavy AI workloads, copying large files, or doing other resource-intensive work, Maple should defer, throttle, or pause heavy maintenance.

Example:

```text
PC idle
→ Maple starts video conversion
→ user launches game
→ Maple pauses/throttles
→ game closes
→ Maple resumes
```

## Resource types

```text
Large file move
→ disk I/O

Cloud sync
→ network + disk

Video conversion
→ CPU/GPU + disk

AI image edit
→ GPU/VRAM

Indexing
→ CPU + disk

Compression
→ CPU + RAM + disk
```

Maple should consider the actual resource profile of the task.

## Priority classes

### Foreground
User is waiting. Run immediately unless unsafe/impossible.

### Background Important
User requested it but does not need it immediately. Run when resources permit.

### Maintenance
Indexing, cleanup, organizational maintenance. Prefer idle periods.

### Heavy Maintenance
Large reorganizations, mass conversions, backups, deduplication. Prefer idle/user-approved windows.

## Dynamic yielding

Maple should continuously adapt, not just check load once at startup.

Possible actions:

- lower worker count
- pause
- lower priority
- stop GPU work
- reduce disk pressure
- reduce network bandwidth
- resume later

## Resource budgets

The future Forest may expose budgets for CPU, GPU, RAM, disk I/O, network, power, and thermal load. Exact values are not yet decided.

## Awareness of other Trees

Maple should consider Forest-wide activity such as:

```text
Cherry Big loading
Bristlecone training
Cedar scan active
```

and avoid launching competing heavy jobs.

The scheduler should consider:

```text
user workload
+ OS workload
+ Forest workload
+ power/battery
+ thermal state
+ storage state
+ network state
```

# Step 4 — Forest-Specific Requirements

## Forest-wide Workshop compatibility

Maple should pull common capabilities from a shared Forest-wide registry rather than duplicating general tools.

Examples:

```text
Maple Workshop
├── file-search
├── file-move
├── email
├── conversion
└── clarify
```

or:

```text
Maple Workshop
├── file-search
├── image-understanding
├── image-edit
└── export
```

Shared does not mean always loaded.

## Maple-specific capabilities

Likely specialist capability families:

- files
- media
- conversion
- workspace/project organization
- Leaf maintenance
- email organization
- batch jobs
- indexing
- operation history

## Deep Leaf Foliage integration

Maple may be the primary maintenance Tree for Leaf Foliage and should understand stable IDs, frontmatter, Markdown/wiki links, backlinks, tags, projects, sources, archives, duplicates, and human-readable Obsidian-compatible storage.

## Derived indexes

Maple should maintain indexes, metadata, search structures, graph relationships, and embeddings where useful so other Trees can retrieve targeted context.

## File-state awareness

Before acting, Maple should know whether source/destination paths exist, are writable, have enough space, would overwrite data, or are currently in use.

## Operation journal + undo

Meaningful actions should be represented outside the model in structured operation history.

## Background job integration

Heavy requests should become persistent jobs that workers can continue after the model unloads.

## Resource-aware Forest scheduling

Maple may receive semantic resource state such as:

```text
user_activity: gaming
cpu_load: high
gpu_load: very_high
disk_io: moderate
network_load: low
bristlecone_training: active
power: AC
```

The Forest runtime should still enforce hard resource budgets.

## Cross-Tree workload awareness

Examples:

```text
Bristlecone training
→ avoid heavy GPU media work

Cherry Big active
→ reduce AI background load

Cedar filesystem scan
→ avoid reorganizing same files
```

## Tree-to-Tree delegation

```text
routine organization → Maple
conversion tool repeatedly crashes → McIntosh
suspicious executable → Cedar
Forest source refactor → Bristlecone Pine
```

## Cherry ↔ Maple relationship

Cherry may understand the user's high-level intent and delegate the workspace portion to Maple. Maple should receive compact distilled context, not Cherry's entire history.

## No Cherry Diary access

Hard boundary:

```text
Cherry Diary ✕ Maple
```

Maple may receive approved functional preferences or minimal derived instructions, but not the underlying Diary.

## Maple preference memory

Maple should maintain his own operational preference store for things such as preservation, naming conventions, image crops, export settings, and project locations.

## Media specialist orchestration

Possible stack:

```text
Maple
├── vision model
├── image editing model
├── video engine
├── audio model
├── OCR/document parser
└── deterministic media tools
```

The core LLM should excel at orchestration and judgment.

## File conversion registry

Maple should use stable semantic capabilities rather than one-off hard-coded tools.

Example:

```text
convert_file(
  input,
  target_format,
  quality_policy,
  preserve_metadata,
  preserve_original
)
```

## Email integration

Maple should use a Forest-level email abstraction with search, read, draft, organize, attachment, and send capabilities. Provider connectors sit underneath.

## Email permission tiers

The Forest should distinguish read/search, organize, draft, send, and delete permissions independently of Maple's reasoning.

## Context targeting

Maple should receive the current project, matched files, relevant metadata, applicable preferences, and active Workshop—not the entire filesystem, email archive, or Leaf store.

## Permission-aware file scopes

Tool access must not imply access to all data.

Example:

```text
Allowed:
~/Documents/School/
~/Pictures/Project/

Not allowed:
~/Secrets/
Cedar-owned storage
Cherry Diary
```

## Local-first operation

Core file, media, conversion, organization, and local-search functions should continue offline.

## Runtime/session independence

Maple state should live outside the model:

```text
job queue
operation journal
file index
Leaf index
media jobs
email state
preferences
resource policies
permissions
```

## Model specialization

Maple may ultimately be a cooperating model team rather than one universal LLM.

# Step 5 — Origin and Licensing Requirements

Maple's Step 5 applies to the **entire stack**, not just the core LLM.

Relevant components include:

```text
Maple Core Model
+ Vision Model
+ Image/Video Models
+ OCR/Document Models
+ Conversion Tools
+ Email Connectors
```

## Open weights strongly preferred

Maple Utility and Reasoner should ideally be open-weight, locally runnable, quantizable, fine-tunable, portable, and not cloud-dependent.

## Local processing strongly preferred

Core user-file, media, and email workflows should not require uploading user content to third parties.

Optional remote specialists may exist later with explicit user approval.

## Commercial-use rights

Licenses should clearly address commercial use, output ownership, fine-tuning, redistribution, quantization, and derivative models.

## Media licensing needs extra scrutiny

Image/video/audio model licenses may restrict commercial outputs, redistribution, derivatives, hosted services, or generated-content use. Maple should avoid unclear output-rights situations.

## User files remain user-owned

Using Maple should not change ownership of photos, documents, video, audio, email, derived edits, or converted files.

## Conversion tools

Prefer mature, open-source, replaceable tools behind stable Forest capabilities.

## Specialist models must be replaceable

Preferred architecture:

```text
Maple Core
→ Forest capability interface
→ replaceable specialist implementation
```

## Email connectors do not define Maple

Provider-specific connectors should remain underneath a stable Forest email capability.

## Avoid mandatory cloud dependencies

Core local Maple should not require remote OCR, remote document parsing, cloud image classification, vendor authentication for inference, mandatory cloud safety endpoints, or licensing callbacks.

## Fine-tuning rights

Future Maple-specific training may target file organization, classification, metadata extraction, batch planning, tool selection, email triage, media orchestration, resource awareness, reversible operations, and Forest delegation.

## Quantization rights

Maple Utility may be aggressively quantized only if path accuracy, filenames, JSON/schema adherence, classification, and tool reliability remain strong.

## Non-Chinese preference

Current Forest rule:

> **Prefer non-Chinese-developed models and technologies when practical.**

This remains a strong preference, not yet an absolute disqualifier.

Each component should eventually record:

```text
Developer:
Country:
Base model:
Derived from:
License:
Weights available:
```

## Openness beyond final weights

Good documentation matters because Maple is operationally complex. Tool formats, tokenization, context limitations, image preprocessing, supported resolutions, fine-tuning methods, and structured-output behavior all matter.

## Multimodal licenses may differ

Language, vision, image, video, audio, and OCR components must each be reviewed individually.

## Runtime portability

Maple Core should ideally work across multiple compatible local runtimes. Maple's identity, jobs, permissions, preferences, and history remain Forest-owned.

## Closed models as optional specialists

Closed APIs may be optional user-approved enhancements, but must never be mandatory for Maple's core local operation.

## Privacy as a candidate-selection criterion

Because Maple handles private files, family photos, email, school materials, personal videos, and possibly financial documents, **local privacy compatibility should be explicitly scored during model selection**.

# Current Working Definition

> **Maple is The Forest's personal workspace, file, media, email, and information-management Tree. He should combine extremely strong tool use, organization, retrieval, multimodal understanding, and operational precision with a lightweight Utility model and an on-demand Reasoner. Deterministic workers should execute file/media/email operations, while Maple plans, coordinates, verifies, and personalizes them. Maple must be deeply integrated with Leaf Foliage, persistent background jobs, undo/rollback, resource-aware scheduling, targeted context, shared Forest-wide Workshops, and strict permissions. He should preserve foreground user performance by deferring or throttling resource-intensive work and should remain local-first, portable, modular, and replaceable across models and tools.**

# Status

```text
Maple Step 1 — Defined
Maple Step 2 — Defined
Maple Step 3 — Defined
Maple Step 4 — Defined
Maple Step 5 — Defined
Maple Step 6 — NEXT: Current candidate research
```
