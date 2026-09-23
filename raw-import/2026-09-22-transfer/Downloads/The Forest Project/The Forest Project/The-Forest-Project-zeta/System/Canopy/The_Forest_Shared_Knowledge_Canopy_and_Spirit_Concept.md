---
title: "The Forest — Shared Knowledge, Canopy Awareness, Routing, and Spirit Control Plane"
aliases:
  - "Forest Knowledge Routing Concept"
  - "Canopy Awareness Architecture"
  - "Spirit of the Forest Control Plane"
created: 2026-08-07
updated: 2026-08-07
type: architecture-concept
status: concept
project: "The Forest"
tags:
  - the-forest
  - architecture
  - canopy
  - spirit-of-the-forest
  - voice-of-the-forest
  - maple
  - cherry
  - cedar
  - bristlecone-pine
  - obsidian
  - knowledge-management
  - retrieval
  - routing
  - qrexec
  - qubes
  - local-first
---

# The Forest — Shared Knowledge, Canopy Awareness, Routing, and Spirit Control Plane

> [!important]
> This document captures the concept work developed around using Obsidian, Markdown, Qubes, Maple, Cherry, Cedar, Bristlecone Pine, the Canopy, and the Spirit/Voice of the Forest as an early proof of concept for The Forest.
>
> The central design principle is:
>
> **Your Data. Your Trees. Your Forest.**

# 1. Core Vision

The Forest should allow multiple AI Trees to work together without every Tree independently searching, organizing, storing, and reasoning over the entire user knowledge base.

Instead, Trees can specialize.

A dedicated knowledge-management Tree can act as a librarian, organizer, retrieval specialist, and pass-through layer for the rest of the Forest.

For the first proof of concept, **Maple** is a strong candidate for this role.

At the same time, frequently used Trees—especially **Cherry**—must remain capable of working independently when Maple is busy, offline, overloaded, training, or otherwise unavailable.

The system should avoid creating a single point of failure.

# 2. Why Obsidian Fits the Forest

Obsidian is useful primarily because its vault is made of ordinary Markdown files.

The important distinction is:

> **Obsidian is the human interface. Markdown is the knowledge system.**

The Trees do not need Obsidian itself in order to understand the Forest knowledge base.

They can work directly with Markdown, metadata, indexes, and controlled retrieval services.

This preserves several Forest goals:

- Local-first operation.
- Human-readable knowledge.
- Offline operation.
- No proprietary data lock-in.
- Easy export.
- Obsidian compatibility.
- Long-term portability.
- Ability to use the same information outside Obsidian.

Obsidian becomes the user's visual editor and knowledge browser rather than a required server component.

# 3. Initial Qubes Layout

The user plans to have roughly two to three AI-focused Qubes.

Rather than creating an additional dedicated Obsidian Qube that consumes resources continuously, one existing AI Qube can host the vault.

The current preferred proof-of-concept layout is:

```text
                    MAPLE QUBE
        ┌────────────────────────────────┐
        │                                │
        │  Obsidian                      │
        │  Canonical Forest Vault        │
        │  Retrieval Index               │
        │                                │
        │  Maple Tree                    │
        │  Knowledge Steward / Router    │
        │                                │
        └──────────┬───────────┬─────────┘
                   │ qrexec     │ qrexec
                   │            │
             ┌─────▼─────┐ ┌────▼──────────┐
             │ Cherry-AI │ │ Dev / Seed AI │
             │           │ │               │
             │  Cherry   │ │ Bristlecone   │
             │           │ │ Pine          │
             └───────────┘ └───────────────┘
```

This avoids the cost of keeping a fourth Qube running merely for Obsidian.

Maple already has a development and knowledge-oriented role, making it a natural host for the first Forest vault.

# 4. Maple as Knowledge Steward

Maple should be more than simply "the Tree with Obsidian."

Maple can become the Forest's first dedicated **knowledge steward**.

Possible responsibilities:

- Organize user files.
- Maintain the canonical Forest vault.
- Search knowledge.
- Retrieve relevant Leaves.
- Maintain metadata.
- Maintain links and backlinks.
- Identify duplicates.
- Identify outdated information.
- Track relationships between notes.
- Distinguish current decisions from historical ones.
- Archive or classify old material.
- Prepare compact context packages for other Trees.
- Handle Tree-to-Tree knowledge requests.
- Maintain indexes.
- Build datasets from accumulated Forest knowledge.
- Help convert useful knowledge into later training material.

Instead of every Tree independently searching thousands of files, Trees can ask Maple for relevant information.

Example:

```text
Cherry:
"I need the current Bristlecone speed benchmarks
and decisions affecting tool selection."

        ↓ qrexec

Maple:
Searches/indexes Forest knowledge.

        ↓

Maple returns:
- relevant files
- exact sections
- metadata
- related decisions
- optional concise summary

        ↓

Cherry reasons using the prepared context.
```

# 5. Retrieval Should Not Always Require an AI

A critical performance rule:

> Do not use Maple's language model for every file request.

Maple should have at least two layers.

```text
             MAPLE
        ┌──────────────┐
        │ Fast Layer   │
        │              │
        │ file lookup  │
        │ index        │
        │ tags         │
        │ metadata     │
        │ backlinks    │
        │ exact search │
        └──────┬───────┘
               │
      complex / ambiguous?
               │
               ▼
        ┌──────────────┐
        │ Maple AI     │
        │              │
        │ interpret    │
        │ organize     │
        │ summarize    │
        │ resolve      │
        │ relationships│
        └──────────────┘
```

Examples:

### Simple request

> Get ADR-0007.

No model reasoning is necessary.

The deterministic layer should retrieve the exact file immediately.

### Complex request

> Find all decisions that would conflict with moving Cherry's memory database to the NAS.

This requires semantic interpretation.

Maple AI can then become involved.

This prevents the Forest from simply moving latency from one Tree to another.

# 6. Forest Knowledge API / qrexec Interface

Rather than giving every Tree unrestricted access to Maple's filesystem, The Forest can expose a small controlled interface.

Possible future services:

```text
forest.find
forest.read
forest.write
forest.search
forest.context
forest.message
forest.archive
forest.history
forest.status
```

Qubes qrexec can provide the transport and policy boundary.

Example permissions:

```text
Cherry
  ✓ forest.find
  ✓ forest.read
  ✓ forest.search
  ✓ forest.context
  ✓ forest.message
  ✗ forest.delete

Bristlecone
  ✓ forest.find
  ✓ forest.read
  ✓ forest.search
  ✓ forest.context
  ✓ forest.write
  ✓ forest.message

Maple
  ✓ full knowledge-management access

Cedar
  ✓ security inspection
  ✓ trust evaluation
  ✓ quarantine-related operations
```

The permission system can eventually become part of the Forest **Trunk** concept.

# 7. Context Packages Instead of Raw Vault Access

Maple should not necessarily send entire files or large portions of the vault to another Tree.

Instead, Maple can prepare temporary context packages.

Example:

```text
Cherry asks a question
       ↓
Maple identifies:
  Leaf 17
  Leaf 83
  Growth Ring 12
  ADR-004
  User Preference 22
       ↓
Maple assembles a context packet
       ↓
Cherry receives only that packet
       ↓
Cherry reasons and answers
```

This reduces:

- Token use.
- Context-window pressure.
- Retrieval duplication.
- File-system overhead.
- Time spent by each Tree figuring out what information matters.

The Tree doing the reasoning does not always need to be the Tree doing the retrieval.

# 8. Retrieval Is Not the Same as Training

The shared Forest vault is primarily a system for:

- Persistent memory.
- Retrieval.
- Knowledge management.
- Context preparation.
- User-specific information.

This does **not** automatically change model weights.

Actual model training changes model parameters.

However, the Forest knowledge system can become a bridge into training.

Possible future pipeline:

```text
USER ACTIVITY
     ↓
Maple organizes knowledge
     ↓
Forest accumulates Growth Rings
     ↓
High-quality examples identified
     ↓
Training dataset generated
     ↓
Periodic Tree training
     ↓
New Seed
```

This creates a safer and more deliberate training process than blindly training on everything the user has ever written.

# 9. Cherry Must Have Backup Retrieval

Maple should be the primary knowledge steward, but Cherry must not become dependent on Maple for every answer.

The user's analogy:

> The user should not have to wait for the "washing machine to finish before they can take a shower and brush their teeth."

Centralizing a resource must not create unnecessary dependency chains.

Cherry should have a local fallback retrieval system.

Concept:

```text
                   MAPLE
             Forest Librarian
          full canonical vault/index
                   │
          ┌────────┴────────┐
          │                 │
       Cherry          Bristlecone
          │                 │
   Local Working Cache   Local Cache
   + basic retrieval     + basic retrieval
```

Cherry can have a curated local working set such as:

```text
Cherry Local Foliage
├── user-preferences
├── active-projects
├── current-decisions
├── recent-growth-rings
├── frequently-used-leaves
├── cherry-specific-knowledge
└── maple-cache
```

Retrieval can then follow three paths.

### Fast Path

Cherry already has what she needs locally.

She answers immediately.

### Normal Path

Cherry needs deeper knowledge.

She asks Maple.

### Fallback Path

Maple is unavailable or too busy.

Cherry searches her local cache/index and continues working.

Cherry should understand that fallback information may not be as complete or current as Maple's canonical knowledge.

# 10. Adaptive Local Foliage

Cherry's local cache should not necessarily be static.

The Forest can learn which Leaves are requested frequently.

Example:

```text
Ketcham branding        → requested often
Forest terminology      → requested often
Qubes configuration     → requested often
Bristlecone benchmarks  → requested often

Old one-time note       → rarely requested
```

Frequently used information becomes a candidate for local residency.

Rarely used information stays primarily in Maple's larger knowledge store.

This creates a memory hierarchy similar to computer caching:

```text
Immediate model context
        ↓
Tree local curated memory/cache
        ↓
Maple retrieval index
        ↓
Canonical Markdown vault
        ↓
Long-term archive / Log Cabin
```

Each layer becomes larger but potentially slower.

# 11. Not Every Tree Needs the Same Backup Capability

All Trees may benefit from some local retrieval ability, but the amount should depend on their role.

### Cherry

Should have the strongest fallback.

Reason:
- Most frequently used by the user.
- Front-door assistant.
- Should remain useful even when other Trees are unavailable.

### Bristlecone Pine

Can maintain a smaller development-focused local cache.

Examples:
- Current Forest architecture.
- Code conventions.
- Benchmarks.
- Active bugs.
- Development decisions.

### Cedar

Can maintain security-focused local knowledge.

Examples:
- Security rules.
- Trust policies.
- Known threats.
- Current quarantine state.
- Recent security events.

### Highly specialized Trees

May rely more heavily on Maple because they do not need broad user knowledge.

Principle:

> **Specialization without fragility.**

# 12. Canopy Awareness

Trees—especially Cherry—should be aware of which other Trees are currently on the Forest network and what broad state they are in.

Cherry should not blindly send a request to Maple only to discover that Maple is already overloaded.

The Canopy can expose a lightweight live status layer.

Example:

```text
Forest Canopy Status
├── Maple
│   ├── state: busy
│   ├── task-category: indexing
│   ├── queue: 4
│   ├── accepting-requests: false
│   └── specialties: files, retrieval, organization
│
├── Cedar
│   ├── state: available
│   ├── task-category: idle
│   ├── queue: 0
│   ├── accepting-requests: true
│   └── specialties: security, quarantine, trust
│
└── Bristlecone Pine
    ├── state: available
    ├── task-category: code-review
    ├── queue: 0
    ├── accepting-requests: true
    └── specialties: development, debugging, training
```

The Canopy status layer should be:

- Small.
- Deterministic.
- Cheap to read.
- Independent of model reasoning.
- Updated through heartbeats/events rather than expensive AI calls.

# 13. Intelligent Routing Before Requests Are Sent

Cherry can use Canopy state plus Tree specialization before deciding where to send work.

Examples:

### Security question

```text
User:
"Is this file suspicious?"

Cherry checks Canopy.

Cedar available.

→ Route to Cedar.
```

### Knowledge request

```text
User:
"Find our old Qubes setup notes."

Cherry checks Canopy.

Maple busy.

Cherry has sufficient local retrieval.

→ Search locally.
```

### Development request

```text
User:
"Why is this Python service crashing?"

Cherry checks Canopy.

Bristlecone available.

→ Delegate to Bristlecone.
```

Routing should consider both:

1. **Who is best suited to the task?**
2. **Who is currently available?**

# 14. Tree Status Should Avoid Unnecessary Private Detail

The Canopy does not need to publish every detail of what a Tree is doing.

For routing, Cherry may only need:

```text
Maple
state = busy
category = indexing
priority = medium
accepting_requests = false
queue_depth = 4
```

This provides situational awareness without unnecessarily sharing full task contents.

# 15. Spirit of the Forest as the Human Control Plane

The user should be able to visually see Tree status and routing information.

This should be available through a popup/window/menu under the **Spirit of the Forest**.

The Spirit of the Forest is not a Tree.

It is deterministic code and system management.

It should work even if no AI model is loaded.

This separation is fundamental.

> The Spirit/Voice should be lightweight enough to "work on a toaster."

Possible responsibilities:

- Menus.
- Help.
- Tree discovery.
- Tree status.
- Canopy state.
- Health checks.
- Routing tables.
- Permissions.
- Logs.
- Startup/shutdown controls.
- Basic service management.
- Troubleshooting information.
- User-facing system explanations.
- Manual overrides.
- Diagnostics.

# 16. Spirit and Voice Are Infrastructure, Not AI

The Forest should separate:

## Control Plane

**Spirit of the Forest / Voice of the Forest**

Deterministic:
- Code.
- Menus.
- Status.
- Help.
- Routing controls.
- Diagnostics.
- System management.

## Intelligence / Workload Plane

**Trees**

AI-driven:
- Cherry.
- Maple.
- Cedar.
- Bristlecone Pine.
- Future Trees.

This makes the Forest resilient.

If Cherry crashes, the user should still be able to open Spirit of the Forest and see:

```text
Cherry       Offline
Maple        Available
Cedar        Watching
Bristlecone  Idle
```

The Forest remains observable even when a Tree is unhealthy.

# 17. User-Facing Tree Monitor

A simple Spirit popup might look like:

```text
Spirit of the Forest
────────────────────────────

Cherry
● Active
Talking with you
Queue: 0
Route preference: Automatic

Maple
● Busy
Organizing Forest notes
Queue: 3
Accepting requests: No

Cedar
● Watching
Security monitoring
Queue: 0
Accepting requests: Yes

Bristlecone Pine
○ Idle
Development Treewright
Queue: 0

────────────────────────────
Routing

Knowledge requests     → Maple
Security requests      → Cedar
Development/debugging  → Bristlecone
General/user requests  → Cherry

[ Automatic Routing ✓ ]
[ Show Background Activity ]
[ Advanced Controls ]
```

This should not merely be decorative.

The user should be able to control common routes and states.

# 18. User Routing Controls

Examples:

```text
Maple:
Do Not Disturb

Cherry:
Use Local Retrieval First

Cedar:
Inspect All Incoming Files

Bristlecone:
Development Requests Only
```

The user may also change routing preferences:

```text
Security Requests

Primary: Cedar
Fallback: Cherry
Never Use: Bristlecone
```

Normal users can leave everything on automatic.

Power users can customize.

Security-focused users can inspect and tightly control Tree interactions.

# 19. Background Activity Transparency

The user should be able to see what Trees are doing when they are not directly talking to them.

Example activity log:

```text
9:42 PM  Maple indexed 3 new Leaves
9:43 PM  Cherry requested context from Maple
9:43 PM  Maple returned 4 relevant Leaves
9:45 PM  Cedar scanned downloaded-file.pdf
9:46 PM  Bristlecone entered idle state
```

This is **operational transparency**, not hidden model reasoning.

The Forest can expose:

- Which Tree is active.
- Broad task category.
- Which service/tool is being used.
- Which files were accessed.
- Where a request was routed.
- Whether a file was written.
- Whether a Tree entered or exited a mode.
- Queue state.
- Health state.
- Resource use.

The Forest should not expose private chain-of-thought as part of this feature.

# 20. Display Levels

Spirit of the Forest can support multiple levels of visibility.

## Simple

For normal users:

- Tree name.
- Online/offline.
- Idle/busy.
- Broad current activity.
- Basic warnings.

## Detailed

For interested users:

- Queue state.
- Routing.
- Recent operations.
- Resource use.
- Active mode.
- Current workshop.

## Expert

For power users / troubleshooting:

- qrexec routes.
- Permissions.
- Models.
- Workshops/tool sets.
- Reasoning mode.
- Service health.
- Logs.
- Manual overrides.
- Context/token metrics.
- Cache behavior.
- Retrieval sources.

# 21. Token and Context Telemetry

The Spirit of the Forest should optionally expose token and context information.

This is especially useful for:

- Performance testing.
- Bristlecone optimization.
- Troubleshooting.
- Comparing retrieval approaches.
- Measuring context efficiency.
- Power users who want optimization data.

This feature should likely be **off by default** for ordinary users.

Possible menu:

```text
Diagnostics
└── Token & Context Data
```

Example:

```text
Cherry — Current Task

Context received: 2,840 tokens
Local memory:       640
Maple retrieval:  1,920
System/workshop:    280
Output:             412
Cache hit:          76%
```

Possible longer-term statistics:

- Average prompt tokens.
- Average output tokens.
- Context-package sizes.
- Tokens by Tree.
- Tokens by workshop.
- Tokens by retrieval source.
- Cache hit rate.
- Largest context sources.
- Retrieval efficiency.
- Repeated unnecessary context.
- Performance before/after routing changes.

This makes the Forest highly observable for users who want to understand computational cost and context behavior.

# 22. Tree-to-Tree Communication Through the Forest

The shared vault can also become a basic asynchronous communication layer.

Example structure:

```text
Forest-Vault/
└── Messages/
    ├── Maple/
    │   ├── Inbox/
    │   └── Outbox/
    │
    ├── Cherry/
    │   ├── Inbox/
    │   └── Outbox/
    │
    └── Shared/
```

Example message:

```markdown
---
id: msg-000042
from: cherry
to: maple
created: 2026-08-07
status: unread
---

# Review Request

I changed the retrieval strategy for Leaf Foliage.

Please review:

[[Projects/Forest/Retrieval Architecture]]
```

Maple can respond asynchronously without requiring both models to be actively conversing at once.

This can become an early implementation of Forest Tree-to-Tree communication.

# 23. Avoid Constant Polling

Trees should not repeatedly ask whether something has changed.

Bad pattern:

```text
Cherry      → anything new?
Cherry      → anything new?
Maple       → anything new?
Maple       → anything new?
Bristlecone → anything new?
```

This wastes:

- CPU.
- Tokens.
- Tool calls.
- Context.
- Power.

Prefer:

```text
Something changes
       ↓
Index/status updates
       ↓
Relevant Tree is notified
or retrieves when needed
```

Use:

- File-system events.
- Lightweight status records.
- Event notifications.
- qrexec messages.
- Cached indexes.

AI reasoning should only occur when useful.

# 24. Lightweight Forest Index

The canonical Markdown vault can have a derived index for speed.

Possible fields:

```text
leaf_id
title
tags
modified
tree
project
path
summary
status
relationships
```

The index could be implemented with:

- SQLite.
- JSON.
- Another lightweight local index.

The Markdown remains the human-readable source of truth.

The index is derived and can be rebuilt.

This aligns with the Forest's local-first architecture.

# 25. Possible Forest Vault Structure

Early structure:

```text
The-Forest/
├── Trees/
│   ├── Cherry/
│   ├── Maple/
│   ├── Cedar/
│   └── Bristlecone-Pine/
├── Leaves/
├── Growth-Rings/
├── Blossoms/
├── Fruit/
├── Leaf-Litter/
├── Projects/
├── Messages/
├── System/
│   ├── Canopy/
│   ├── Routing/
│   └── Status/
└── Training/
```

This is a starting concept, not a frozen final structure.

# 26. Obsidian and dom0

Obsidian should not need to run in dom0.

The Obsidian GUI can run in Maple while appearing on the user's normal Qubes desktop through Qubes GUI virtualization.

From the user's perspective:

```text
[ Maple Terminal ] [ Cherry ] [ Obsidian ]
```

Underneath:

```text
Maple Terminal → Maple Qube
Cherry         → Cherry-AI Qube
Obsidian       → Maple Qube
Desktop        → dom0
```

This preserves Qubes security while giving the user convenient visual access.

dom0 should remain outside the Forest data-processing path whenever possible.

# 27. Proof-of-Concept Goals

The Obsidian/Maple experiment should test whether:

1. A canonical local Markdown knowledge base works for The Forest.
2. Maple can organize user information.
3. Maple can serve context to Cherry.
4. Maple can serve context to Bristlecone.
5. Cherry can maintain useful local fallback knowledge.
6. Trees can discover one another through the Canopy.
7. Trees can understand availability before routing.
8. Security questions can preferentially route to Cedar.
9. Development questions can preferentially route to Bristlecone.
10. Knowledge requests can preferentially route to Maple.
11. Trees can communicate asynchronously.
12. Spirit of the Forest can display Tree state without using an AI model.
13. Users can control common routing behavior.
14. Token/context telemetry can help optimization.
15. The system remains useful if one Tree is unavailable.

# 28. Proposed Early POC

## POC-001 — Shared Foliage / Maple Knowledge Steward

### Goal

Demonstrate that multiple isolated Trees can discover, retrieve, contribute to, and communicate through a shared human-readable knowledge system without requiring every Tree to search the entire data set independently.

### Initial Components

- Maple Qube.
- Obsidian.
- Canonical Markdown vault.
- Lightweight index.
- Maple knowledge-management layer.
- Cherry local cache.
- qrexec communication.
- Canopy status records.
- Basic Spirit status interface.

### Success Scenario

```text
USER
 │
 ▼
Cherry
 │
 ├── checks local context
 │
 ├── checks Canopy
 │
 └── determines Maple is available
             │
             ▼
           Maple
             │
       retrieves Leaves
             │
       builds context packet
             │
             ▼
           Cherry
             │
             ▼
        answers user
```

Alternative:

```text
USER
 │
 ▼
Cherry
 │
 ├── checks Canopy
 │
 └── Maple busy
             │
             ▼
   Cherry local retrieval
             │
             ▼
        answers user
```

Security case:

```text
USER
"Is this file safe?"
       │
       ▼
     Cherry
       │
checks Canopy
       │
       ▼
 Cedar available
       │
       ▼
 route to Cedar
```

# 29. Larger Architectural Principle

The emerging Forest architecture separates responsibilities:

## Cherry
User-facing assistant and coordinator.

## Maple
Knowledge steward, organizer, retrieval specialist, file manager, and context provider.

## Cedar
Security specialist.

## Bristlecone Pine
Treewright, development, debugging, testing, training, and maintenance.

## Canopy
Tree awareness, reachability, status, communication, and routing information.

## Spirit / Voice of the Forest
Deterministic control plane, menus, status, help, observability, diagnostics, and user controls.

This enables specialization without forcing every AI to become equally capable at every function.

# 30. User Ownership Principle

The central philosophical and product statement developed from this architecture is:

> # **Your Data. Your Trees. Your Forest.**

Meaning:

### Your Data

The user owns the knowledge.

It should be:

- Local-first.
- Portable.
- Human-readable.
- Exportable.
- Accessible without a proprietary cloud.
- Under user control.

### Your Trees

The user controls the AI agents.

They can determine:

- Which Trees are planted.
- What roles they have.
- Which models they use.
- Which tools they can access.
- Which Trees they can communicate with.
- What permissions they have.
- How requests are routed.

### Your Forest

The overall ecosystem belongs to the user.

The user controls:

- Infrastructure.
- Knowledge.
- Routing.
- Security.
- AI selection.
- Data retention.
- Training.
- Growth.
- Customization.

# 31. Motto vs. Tagline

The Forest currently has two complementary statements.

## Product / Ownership Tagline

> **Your Data. Your Trees. Your Forest.**

This explains the user-ownership philosophy.

## Philosophical Motto

> **IN God we trust in the forest we wonder.**

This expresses the project's broader identity and sense of exploration.

They serve different purposes and can coexist.

# 32. Key Design Principles Captured Here

1. **Local-first.**
2. **Human-readable knowledge.**
3. **Obsidian-compatible, not Obsidian-dependent.**
4. **One canonical knowledge base.**
5. **Derived indexes for speed.**
6. **Maple as a specialized knowledge steward.**
7. **Cherry remains independently useful.**
8. **Avoid single points of failure.**
9. **Trees know which other Trees are available.**
10. **Route before sending, not after waiting.**
11. **Use specialization when it helps.**
12. **Fallback locally when specialists are busy.**
13. **Spirit/Voice are deterministic infrastructure.**
14. **The control plane must work without AI.**
15. **Users can observe background operations.**
16. **Power users can control routing.**
17. **Token/context telemetry is optional but available.**
18. **Do not expose hidden chain-of-thought; expose operations and state instead.**
19. **Use qrexec as a controlled Qubes communication mechanism.**
20. **Avoid unrestricted shared writable filesystems across Qubes.**
21. **Avoid constant polling.**
22. **Use event-driven/status-driven coordination where possible.**
23. **Do not invoke an LLM for deterministic tasks.**
24. **Retrieve only the context needed for the current task.**
25. **Persistent memory and retrieval are distinct from model training.**
26. **Forest knowledge can later produce curated training data.**
27. **Specialization without fragility.**
28. **Your Data. Your Trees. Your Forest.**

# 33. Next Step

After preserving this concept work, return to the practical Obsidian proof of concept.

Recommended implementation order:

1. Install Obsidian in Maple.
2. Create the first canonical Forest vault.
3. Import existing Forest Markdown.
4. Establish the initial folder/metadata structure.
5. Build a lightweight local search/index.
6. Give Cherry controlled read/search access through qrexec.
7. Test simple retrieval.
8. Test Cherry local fallback.
9. Add basic Canopy status information.
10. Add Tree-to-Tree messages.
11. Prototype Spirit of the Forest status display.
12. Benchmark performance and token/context usage.
13. Decide which components should become permanent Forest architecture.

# End

**Your Data. Your Trees. Your Forest.**
