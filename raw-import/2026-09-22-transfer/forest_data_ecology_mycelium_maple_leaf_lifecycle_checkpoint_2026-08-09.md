# Project Forest — Data Ecology, Continuity, and Personal Knowledge Architecture

**Date:** 2026-08-09  
**Status:** Design checkpoint / concepts largely agreed, exact implementation still pending  
**Relevant future phases:** Phase 14 Layered Hot Context, Phase 15 Leaf Foliage, Phase 16 Operational Learning, Phase 17 Spirit / Permissions, Phase 18 Multi-model / Future Runtime

---

# Core Design Philosophy

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

> **The Forest gets deeper as you wonder.**

The Forest metaphor is a human-facing abstraction over real AI, storage, retrieval, security, lifecycle, continuity, and resource-management mechanics.

Casual users should be able to use intuitive Forest tools without learning AI infrastructure. Power users should be able to inspect progressively deeper layers and control how their Trees grow, retain knowledge, share continuity, and handle data.

---

# Information Origin

## Water

> **Water is information entering the user's Forest from outside sources.**

Examples include internet searches, downloaded documents, public APIs, messages, another Forest, and other approved external sources.

Water is generally a **visible information transfer**: the user normally knows a Tree connected outward or received something, and usually sees or approves it in real time.

Water does not automatically become a Leaf.

## Sunlight

> **Sunlight is information originating from the user.**

Examples include conversation, notes, diaries, calendar data, user-created documents, instructions, images, and personal records.

Water and Sunlight describe **origin**, not sensitivity.

A downloaded medical document may be Water and highly sensitive. A user-created note may be Sunlight and completely ordinary.

---

# Leaves

## Leaf

> **A Leaf is an independently addressable, durable, human-readable unit of Forest knowledge.**

A Leaf exists independently of model context and may be connected through Roots to sources, other Leaves, files, Tasks, Trees, user history, ideas, projects, Fruit, and other Forest knowledge.

> **A Leaf can become context, but context does not automatically become a Leaf.**

A retrieval chunk, embedding, prompt fragment, or model KV cache is not a Leaf.

## Leaves

> **Leaves is simply the plural of Leaf.**

It should not become a separate technical object type.

---

# Leaf Retention Strength

Leaf retention describes how strongly a Tree should keep a Leaf during normal autonomous lifecycle behavior. It does not describe sensitivity or encryption.

## Loose

> **Temporary growth that may naturally shed relatively easily when its usefulness fades.**

Conceptually:

```text
Loose
→ temporary / easy natural shedding
```

## Normal

> **Ordinary durable knowledge retained while useful and eligible for normal seasonal lifecycle behavior.**

Conceptually:

```text
Normal
→ hold for a while / normal lifecycle
```

## Sturdy

> **Persistent growth protected from normal autonomous shedding.**

Conceptually:

```text
Sturdy
→ do not naturally drop
```

Sturdy must not mean undeletable. The user may still deliberately Prune or explicitly alter/remove it.

### Sturdy vs. Tar Sap

```text
Sturdy
→ retention rule
→ "Do not naturally drop this."

Tar Sap
→ handling rule
→ "Do not autonomously alter this."
```

A Leaf may be both.

---

# Shedding

> **Shedding is natural, Tree-driven removal from active growth as part of the Tree's lifecycle.**

Shedding is not deletion and is not Pruning.

Loose and Normal Leaves may naturally shed according to lifecycle policy. Sturdy Leaves should not naturally shed unless the user changes their retention status or explicitly authorizes an intervention.

---

# Leaf Litter

> **Leaf Litter is the lifecycle state entered by shed material before final decomposition or reuse.**

Leaf Litter is not merely a recycle bin. It is a **decay and salvage environment**.

```text
Active Leaf
    ↓
Shedding
    ↓
Leaf Litter
    ↓
Decay
    ↓
Salvage / Reuse / Decomposition
```

Spirit should handle cheap deterministic lifecycle mechanics such as age, retention period, protection state, dependency checks, storage pressure, user rules, and lifecycle timers.

Maple may selectively perform semantic salvage before material fully decomposes.

---

# Maple and Leaf Litter Salvage

Maple helps turn the user's digital history into usable continuity.

> **Maple draws the map, tends the archive, and salvages what should not be forgotten.**

Maple may inspect permitted Leaf Litter and older data for useful material such as:

- half-developed ideas
- abandoned projects
- failed fixes
- successful fixes
- old screenshots
- old pictures
- previous design directions
- rejected drafts
- accepted drafts
- user corrections
- coding habits
- visual preferences
- writing preferences
- recurring mistakes
- past experiments
- lessons learned
- old concepts that may become useful later

This supports continuity such as:

> "You already tried this fix before and it failed because of X."

> "You had a related idea several years ago."

> "You repeatedly changed generated images in this same direction."

---

# Syrup

> **Syrup is reusable material distilled from recycled or historical user data, especially Leaf Litter, and potentially combined with permitted Water, Sunlight, and Leaves to help future Tree growth better reflect the user.**

Syrup is not another kind of Leaf. It is derived personalization / experience material.

```text
Leaf Litter
old files
old drafts
old images
failed attempts
abandoned ideas
past preferences
       │
       ↓
     Maple
   salvage /
   distill
       │
       ├── Water
       ├── Sunlight
       └── relevant Leaves
               ↓
             Syrup
```

Possible Syrup content includes writing tendencies, visual preferences, recurring corrections, coding habits, known failed approaches, successful patterns, unfinished ideas, historical references, and personalization signals.

Syrup should retain provenance through Roots so its conclusions can be inspected and revised as the user changes.

---

# Protection Must Survive Recycling

Leaf Litter must never become a loophole around privacy or security.

If protected source material contributes to Syrup or other derived data, its restrictions must follow the derived material as required to prevent information leakage.

```text
Protected source
        ↓
Maple salvage
        ↓
Derived material

Result:
must preserve required source restrictions
```

Spirit and Cedar enforce these rules. Maple performs semantic salvage only inside the permitted boundaries.

---

# Roots

> **Roots describe provenance, dependencies, and relationships.**

A Leaf is the knowledge object. Roots explain where it came from, what supports it, what it relates to, what replaced it, what depends on it, and what history led to it.

---

# Mycelium

> **Mycelium is the Forest's permission-aware, below-the-surface continuity network that connects knowledge, history, relationships, and useful experience across Trees without requiring those Trees to directly observe or remember one another's conversations.**

Simple user-facing version:

> **Mycelium lets Trees quietly share what the Forest has learned.**

Key distinction:

> **Water is visible transfer. Mycelium is hidden continuity.**

A user generally sees Water happen. Mycelium may operate quietly after permission has already been granted, with the user noticing its effects later when another Tree unexpectedly knows something useful.

```text
User talks to Tree A
        ↓
relevant records / Roots updated

User talks to Tree B
        ↓
relevant records / Roots updated

Maple connects related history
        ↓
Mycelium relationship exists

years pass
        ↓
User mentions related subject to Tree C
        ↓
permitted continuity is retrieved
        ↓
Tree C naturally recognizes the history
```

Trees do not need to constantly run models and directly talk to one another. Most Mycelium activity should use cheap IDs, references, backlinks, indexes, metadata, retrieval, and permission checks.

Actual Tree-to-Tree model communication should be reserved for cases where one Tree genuinely needs another Tree's intelligence.

---

# Inspectable Mycelium

Mycelium should feel invisible by default but remain auditable.

Most users may only see:

> "The Tree somehow knew."

A curious user may follow:

```text
Current Tree
   ↓
idea thread
   ↓
related Leaves
   ↓
Roots
   ↓
earlier Tree events
   ↓
source files / conversations
```

Deeper inspection may expose timestamps, stable IDs, access decisions, protection status, Tree permissions, who created a link, why retrieval occurred, and what information actually crossed a boundary.

> **The magic should be inspectable magic.**

---

# Maple's Role in Mycelium

Maple does not own Mycelium.

> **Maple is one of Mycelium's primary cultivators and semantic cartographers.**

Maple helps determine that apparently separate things are related and updates the shared map / relationship structures.

Maple does not need to be the Tree that announces these discoveries to the user. The Tree the user is currently interacting with should receive the relevant permitted continuity and experience that knowledge naturally.

> **Maple does not make every Tree remember everything. Maple makes it possible for every Tree to remember the right things.**

> **Maple draws the relationships. Spirit maintains the records. The Tree you're with experiences the continuity.**

> **Trees share continuity without sharing consciousness.**

Cross-Tree awareness comes from shared Forest records, not unrestricted access to every Tree's conversations.

---

# Spirit's Role

Spirit is the deterministic steward of Forest state.

> **Spirit preserves the state of the Forest.**

Spirit handles low-cost deterministic work such as:

- file locations
- stable IDs
- hashes
- modification state
- integrity metadata
- version history
- cache validity
- permissions
- lifecycle timers
- retention rules
- auto-pruning policies
- Mycelium access enforcement
- resource limits
- storage budgets
- deterministic triggers

> **Spirit has broad visibility but narrow autonomous authority.**

---

# Maple's File and Personal-Data Role

Maple should not store the user's entire file map in the model's brain.

> **Maple draws the map and knows how it works; the map itself belongs to the Forest.**

The Forest may maintain a live data catalog containing stable file IDs, paths, types, hashes, timestamps, versions, relationships, permissions, integrity state, and derived-index state.

Spirit maintains deterministic truth. Maple adds semantic understanding.

Maple may understand which files belong to a project, which document supersedes another, which images are related, what old project decisions mean, what failed before, and what may matter to another Tree.

Full knowledge should mean **full addressability**, not "everything loaded into model context."

---

# Cache Management: Maple vs. Spirit

## Spirit / Cache Coordinator

Owns deterministic cache mechanics:

- dependency versions
- hashes
- invalidation
- storage limits
- cache lifecycle
- runtime change detection
- tokenizer/model change detection
- integrity

## Maple

May contribute semantic judgments:

- a summary is conceptually obsolete
- old material contains useful experience
- two records describe the same idea
- a pattern deserves durable retention
- an artifact may improve future work

> **Cache mechanics belong to Spirit. Cache meaning may involve Maple.**

---

# Cedar

Cedar is the Forest's security Tree.

> **Cedar protects data. Spirit enforces protection policy.**

Cedar responsibilities include file security, encryption, protected storage, secure transfer policy, key-related security mechanics, and security classification assistance.

Maple must respect Cedar's protection boundaries during file mapping, Leaf Litter salvage, Syrup generation, and Mycelium continuity.

---

# Cedar Oil

> **Cedar Oil represents actual data security / encryption protection.**

It answers:

> **How is this material physically or cryptographically protected?**

Possible mechanisms include encryption at rest, encrypted transfer, key custody, protected backups, secure storage, and controlled decryption.

---

# Sap

> **Sap marks sensitive data that requires careful handling.**

Sap is not necessarily encrypted.

Sap may restrict sharing, learning, summarization, recycling, Mycelium propagation, storage, retention, and which Trees may use derived material.

---

# Tar Sap

> **Tar Sap marks material protected from autonomous transformation or manipulation.**

Core user concept:

> **Do not touch this unless explicitly allowed.**

Tar Sap may block autonomous actions such as pruning, Leaf Litter decomposition, Syrup recycling, summarization, consolidation, training-data extraction, semantic merging, moving, renaming, rewriting, format conversion, and propagation.

Tar Sap is a handling lock, not simply a secrecy rating.

---

# Tree Access Permissions

Protection and Tree access should remain independent axes.

Critical distinction:

```text
Knows it exists
≠
May read it
≠
May modify it
≠
May share it
≠
May learn from it
```

A Tree may be allowed to know that relevant protected history exists without being permitted to read it.

Foreign Trees should not automatically inherit the user's history merely because they were planted.

---

# Who May Request Protection?

Any Tree may recognize that information appears sensitive or recommend protection.

Preferred architecture:

```text
Tree identifies / requests protection
        ↓
Cedar security specialization
        ↓
Spirit validates/enforces policy
```

Arbitrary Trees should not have unrestricted authority to redefine security policy.

---

# Pruning

> **Pruning is a controlled, deliberate intervention initiated or authorized by the user or Spirit to shape a Tree by cutting back unwanted, incorrect, obsolete, excessive, harmful, or otherwise undesired growth while preserving the knowledge, behaviors, and structure that should remain.**

> **Pruning shapes the Tree. Shedding is part of the Tree's natural lifecycle.**

Trees may recommend pruning candidates but should not have unrestricted access to their own pruning tools.

---

# Automatic Pruning

Spirit may execute narrow user-approved pruning policies without waking an LLM.

Example:

```text
IF Code Tree Leaf count >= 2,000
THEN run approved pruning policy
UNTIL Leaf count <= 1,750
```

Possible Tree-specific budgets include Leaf count, storage, inactive Leaves, free-device-storage thresholds, age limits, and growth-rate limits.

Automatic Pruning remains ultimately user-directed.

---

# Buds

Buds should not appear for every cluster of Leaves.

> **A Bud represents an emerging medium- or long-term idea, intention, project, or line of thought that recurs or develops enough for the Forest to recognize ongoing growth.**

A Bud may emerge from repeated discussion, meaningful recurrence, development across multiple Trees, related Leaves, planning, Tasks, user emphasis, or return after long inactivity.

There should not be a simplistic rule such as "five mentions always equals Bud."

Maple may determine semantic sameness across references. Spirit may cheaply track dates, occurrence counts, Trees involved, and activity.

The **current Tree** should normally be the one that naturally mentions the recurring idea to the user.

---

# Flowers

> **A Flower represents a Bud that has developed into a coherent, actively cultivated medium- or long-term effort.**

Not every Bud flowers. Not every set of Leaves produces a Flower.

Flowers should be meaningful and may be supported by active planning, requirements, project files, multiple related Leaves, Tasks, design decisions, prototypes, and sustained development.

A Flower is primarily a **growth-state representation**, not another large knowledge store.

---

# Fruit

> **Fruit is a useful realized result produced by a Tree's growth.**

Possible Fruit includes completed programs, finished images, videos, approved emails, working automations, completed documents, milestones, released versions, trained artifacts, and successful designs.

One Flower/project may produce multiple Fruits over time.

---

# Creation Lifecycle

The growth-state lifecycle applies only where appropriate:

```text
Recurring / developing idea
        ↓
       Bud
        ↓
sustained cultivation
        ↓
      Flower
        ↓
useful realized result
        ↓
       Fruit
```

Most information instead follows:

```text
Water / Sunlight
      ↓
     Tree
      ↓
    Leaves
```

and stops there.

---

# Cross-Tree Continuity

Trees should not personally remember everything that happened with every other Tree.

They receive relevant permitted continuity through Forest infrastructure.

A Tree may naturally know:

> "You've returned to this idea several times over the years."

without having participated in every earlier discussion.

Underneath, continuity may come from Maple's semantic map, Mycelium relationships, Roots, Leaves, activity records, Operational Learning, permissions, and retrieval.

On the surface, it feels like the Trees have been growing together.

---

# Future User Model

The Forest may gradually build a structured personal knowledge model about the user.

This is not necessarily another neural model.

Possible components include:

- preferences
- projects
- relationships
- history
- prior decisions
- successful approaches
- failed approaches
- creative tendencies
- workflows
- recurring ideas
- meaningful artifacts

Maple helps build and interpret this model. It belongs to the Forest, not Maple's model weights.

---

# Operational Experience

Not all useful salvage becomes an ordinary Leaf.

```text
Leaf Litter salvage
        ↓
┌──────────────┬──────────────┬───────────────┐
│              │              │               │
Knowledge    Preference     Experience      Nothing useful
│              │              │               │
Leaf          Syrup /       Operational     Decompose
candidate     user model     Learning
```

Operational Learning can preserve failed fixes, successful methods, incompatible configurations, repeated errors, useful Skills, and other experience that helps future Trees avoid repeating mistakes.

---

# Future Training Value

With user permission, accumulated structured history may eventually support retrieval, personalization, evaluations, LoRA, fine-tuning, preference optimization, and specialized Tree training.

Useful records may look like:

```text
user request
→ Tree response
→ user correction
→ final accepted result
```

or:

```text
approach A
→ failed

approach B
→ partially worked

approach C
→ verified
```

The initial architecture should prioritize high-quality structured experience rather than continuously retraining models.

---

# Current Responsibility Split

```text
                         SPIRIT
                            │
               deterministic stewardship
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
 filesystem state       integrity           permissions
 versions/hashes        continuity          resource limits
 cache validity         lifecycle           retention
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ↓
                     FOREST DATA MAP
                            │
                            ↓
                         MAPLE
                            │
                   semantic stewardship
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
 understand             salvage             connect
 history                useful litter       patterns
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ↓
            LEAF FOLIAGE / USER MODEL /
         MYCELIUM / OPERATIONAL LEARNING
                            │
                            ↓
                       OTHER TREES
```

Cedar overlays the system as the security specialist:

```text
CEDAR
→ security
→ encryption
→ Cedar Oil
→ protection policy

SPIRIT
→ deterministic enforcement

MAPLE
→ semantic use only when permitted
```

---

# Core Vocabulary Snapshot

| Forest Term | Current Meaning |
|---|---|
| Water | Outside information entering the Forest |
| Sunlight | User-originated information |
| Leaf | Durable Forest knowledge object |
| Leaves | Plural of Leaf |
| Loose | Temporary/easily shed Leaf |
| Normal | Ordinary-retention Leaf |
| Sturdy | Leaf protected from natural shedding |
| Roots | Provenance and relationships |
| Shedding | Natural Tree-driven removal from active growth |
| Leaf Litter | Shed material in decay/salvage lifecycle |
| Syrup | Reusable distilled user/history material |
| Mycelium | Permission-aware below-surface cross-Tree continuity |
| Sap | Sensitive-handling designation |
| Tar Sap | Protected from autonomous alteration |
| Cedar Oil | Security/encryption protection |
| Bud | Emerging recurring medium/long-term idea |
| Flower | Actively cultivated medium/long-term effort |
| Fruit | Useful realized result |
| Pruning | Deliberate user/Spirit-authorized shaping |

---

# Important Orthogonal Axes

These concepts should not collapse into one status field.

A Leaf may independently have:

```text
ORIGIN
Water / Sunlight

RETENTION
Loose / Normal / Sturdy

HANDLING
normal / Sap / Tar Sap

SECURITY
Cedar Oil on/off

ACCESS
per-Tree permissions

RELATIONSHIPS
Roots / Mycelium

LIFECYCLE
active / shed / Leaf Litter / decay

GROWTH RELATION
possibly linked to Bud / Flower / Fruit
```

Example conceptual schema:

```yaml
leaf:
  id: leaf-example

  origin:
    sunlight: true

  retention:
    sturdy

  handling:
    sap

  security:
    cedar_oil: true

  permissions:
    read:
      - cherry
      - maple
    write:
      - user
    foreign_trees: deny

  recycling:
    syrup_allowed: false
```

Exact schema is not yet frozen.

---

# Design Principles to Preserve

> **Trees maintain themselves naturally. Spirit enforces bounded maintenance policies. Users shape the Tree.**

> **Pruning shapes the Tree. Shedding is part of the Tree's natural lifecycle.**

> **Spirit preserves the state of the Forest. Maple preserves the meaning of its history.**

> **Spirit maintains the map. Maple understands the territory.**

> **Maple draws the relationships. Spirit maintains the records. The Tree you're with experiences the continuity.**

> **Maple does not make every Tree remember everything. Maple makes it possible for every Tree to remember the right things.**

> **Cross-Tree awareness comes from shared Forest records, not unrestricted access to other Trees' conversations.**

> **Trees share continuity without sharing consciousness.**

> **Water is visible transfer. Mycelium is hidden continuity.**

> **The magic should be inspectable magic.**

> **The user does not always need to know exactly how or when knowledge traveled. If they dig into the Soil and follow the Roots, they can find out. Most of the time, what matters is that the Tree knows — and the Tree grows.**

---

# Relationship to Current Roadmap

```text
✅ Phase 0  — Hermes / Bristlecone runtime
✅ Phase 1  — Workshop / capability architecture
✅ Phase 2  — Runtime adapter foundation
✅ Phase 3  — Workshop controller migration
✅ Phase 4  — Runtime sessions
✅ Phase 5  — Seasonal lifecycle foundation
✅ Phase 6  — Winter durability
✅ Phase 7  — Spring wake / Cleaning
✅ Phase 8  — Spring planner
✅ Phase 9  — Spring decision
✅ Phase 10 — Controlled Spring application
✅ Phase 11 — Spring → Summer completion
✅ Phase 12 — Temporary capability restoration
✅ Phase 13 — Runtime-Independence Audit

→ Phase 14 — Layered Hot Context / Performance
□ Phase 15 — Leaf Foliage
□ Phase 16 — Operational Learning
□ Phase 17 — Spirit / Permissions
□ Phase 18 — Multi-model / Future Runtime
```

Phase 14 has also adopted:

> **Forest owns reusable meaning. Adapters translate reusable meaning into runtime-specific reuse. Native runtimes own inference state.**

The concepts in this document should inform Phase 15–17 without being prematurely forced into Phase 14 unless extension points are needed.

---

# Still Requiring Formal Freeze Before Implementation

- exact Leaf schema
- Loose / Normal / Sturdy lifecycle thresholds
- exact Leaf decay stages
- Leaf Litter retention rules
- Syrup storage format
- Syrup revalidation/update policy
- Maple salvage scheduling
- user-model representation
- Mycelium graph/storage model
- cross-Tree propagation rules
- how Trees receive Mycelium context
- per-Tree Mycelium access levels
- Sap policy details
- Tar Sap exact allowed/blocked operations
- Cedar Oil key/encryption architecture
- permission inheritance
- protection inheritance for derived data
- Bud candidate detection
- Bud / Flower / Fruit state machine
- exact relationship between Roots and Mycelium
- exact relationship between Leaf Foliage, Maple's map, and Operational Learning

These should be resolved deliberately instead of being defined accidentally during coding.
