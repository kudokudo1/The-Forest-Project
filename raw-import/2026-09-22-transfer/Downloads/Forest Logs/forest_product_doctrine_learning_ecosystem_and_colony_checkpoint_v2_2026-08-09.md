# Project Forest — Product Doctrine, Learning Architecture, and Ecosystem Checkpoint

**Date:** 2026-08-09  
**Status:** Active design checkpoint  
**Context:** Captures the product-level principles and learning-system decisions refined during Phase 14 performance/cache work.

---

# 1. Forest Product North Star

The Forest is not trying to be the absolute best AI application at every individual task.

Its target is:

- **Capability / raw power:** generally **7/10–9/10**
- **Experience:** **10/10**
- **Ownership:** **10/10**
- **Privacy / security:** **10/10**
- **Continuity:** **10/10**
- **Extensibility:** **10/10**

The goal is to provide nearly everything a user reasonably needs from AI in one coherent ecosystem, without requiring them to assemble and mentally manage several disconnected AI applications.

A specialized external application may occasionally outperform the Forest at one narrow task. That is acceptable.

The Forest wins by making the overall environment coherent, connected, owned by the user, secure, understandable, and extensible.

> **Complete by default. Modular underneath.**

> **External tools are choices, not dependencies.**

> **Users should gain capabilities by growing their Forest, not by assembling a collection of unrelated AI applications.**

---

# 2. What “Complete Ecosystem” Means

A Forest installation should provide strong built-in access to the kinds of capabilities users commonly seek across separate AI applications and services, including:

- general assistance
- coding and debugging
- research
- creative work
- files and documents
- knowledge management
- memory
- learning and personalization
- automation
- voice
- model access
- image/media tooling where appropriate
- security
- multi-agent / multi-Tree collaboration
- training and development support
- extensibility and add-ons

This does **not** mean every subsystem should always be active.

The architectural target is:

```text
Complete ecosystem on disk
        ↓
Warm services only when useful
        ↓
Small selected hot context
        ↓
Current Tree / current Task
```

The Forest should be broad at the ecosystem level while remaining selective at runtime.

---

# 3. User Choice and Ownership

The Forest should not prevent users from using other tools.

A user may:

- plug in a stronger local model
- use a cloud model
- connect Hermes
- use a specialized coding/research/image application
- add another runtime
- replace a model behind a Tree
- add new Workshops, plugins, or services

But those should be **optional choices**, not requirements caused by missing core Forest capability.

The desired experience is:

> “I use this external tool because I prefer it.”

not:

> “I have to use this external tool because the Forest cannot do the job.”

Core principle:

> **It’s your Soil and your Forest. You use it how you want.**

---

# 4. Forest vs. External Applications

The Forest should not blindly copy other AI applications.

Instead, when a product has a highly praised feature, ask:

> **What user need does this feature satisfy, and what would the Forest-native version look like when connected to the rest of the ecosystem?**

Possible adoption patterns:

## Native

Core enough that the Forest itself should own the capability.

Examples:
- Tree identity
- durable knowledge
- learning/personalization
- permissions
- security policy
- continuity
- Operational Learning

## Forest-Adapted

Take a proven concept and redesign it around:

- Trees
- Workshops
- Spirit
- Cedar
- Maple
- Mycelium
- Leaves
- Roots
- Syrup
- Forest permissions

Example: Hermes-style self-improvement and adjustment, adapted so learning does not automatically become unrestricted Skill creation.

## Integrated

Use a strong external engine or service behind a Forest-native interface.

Examples may include:
- models
- speech engines
- image models
- search systems
- specialized runtimes
- external services

The user interacts with the Forest abstraction; the Forest manages infrastructure.

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

---

# 5. Why Integration Is a Core Advantage

The Forest does not need every individual component to be the absolute best if the ecosystem makes them work together unusually well.

Example continuity:

```text
Bristlecone encounters a debugging failure
            ↓
Operational Learning records the lesson
            ↓
Roots preserve provenance
            ↓
Mycelium makes the lesson discoverable
            ↓
Maple later encounters related architecture
            ↓
the relevant lesson is retrieved
            ↓
Spirit checks permissions
            ↓
Cedar protections remain enforced
            ↓
Cherry can later explain the historical decision
```

A set of disconnected high-performing applications usually does not naturally provide this shared continuity.

Therefore:

> **Integration itself is one of the Forest's strongest capabilities.**

---

# 6. Tree Identity Must Survive Model Replacement

The Forest learning architecture strengthens the existing principle:

> **A Tree is not its model.**

Technical form:

> **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**

If a model changes, the following should survive:

- Tree identity
- Leaves
- Roots
- Operational Learning
- user model
- Syrup
- Mycelium relationships
- Workshop history
- permissions
- security boundaries
- task/history references

A new model should be able to inherit the benefit of what the Tree learned without retraining that model to literally become the Tree.

---

# 7. Learning vs. Skill Creation

Hermes is useful as evidence that self-improvement, user adjustment, procedural learning, and reusable experience can be valuable.

The Forest should study those ideas without copying Hermes wholesale.

Important distinction:

> **The Forest should learn from experience more freely than it creates new capabilities.**

A Tree should be able to learn:

- a mistake
- a failed approach
- a successful fix
- a user correction
- an environmental constraint
- a preferred workflow
- a repeated pattern
- a useful technique
- a limitation
- a prior outcome

without automatically generating or modifying executable capabilities.

Preferred flow:

```text
Experience
   ↓
Learning classification
   ↓
Operational Learning / user model / Syrup
   ↓
possibly a Procedure Candidate
   ↓
only sometimes:
Skill proposal
   ↓
Spirit / supporting-Tree governance
```

A lesson is not the same thing as a Skill.

Example lesson:

> “This configuration failed because the Bristlecone Hermes profile must remain explicitly scoped.”

Example Skill:

> A reusable procedure that executes commands and manipulates the affected subsystem.

The latter has higher consequences and should receive tighter governance.

---

# 8. Forest Learning System

Operational Learning should become a central Forest subsystem rather than a small task-outcome log.

Possible experience inputs:

```text
Experience
│
├── mistake
├── failed approach
├── successful technique
├── user correction
├── recurring preference
├── environment discovery
├── repeated workflow
└── useful historical outcome
        ↓
  learning classifier
```

Potential destinations:

```text
                  EXPERIENCE
                       │
                       ▼
              Learning Classifier
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
Operational        User Model       Procedure
Learning             / Syrup         Candidate
       │               │                │
       ▼               ▼                ▼
Lessons          Personalization    Workshop/Skill
                                       proposal
```

---

# 9. Operational Learning Scopes

Operational Learning should support multiple scopes.

## General Lessons

Applicable across Trees or Workshops when permissions allow.

Examples:
- do not blindly rerun a failed command
- inspect exact source before patching after a structural mismatch
- backup existing source before modification when no Git safety net exists
- temporary approval does not imply permanent activation

## Workshop Lessons

Specific to a kind of work.

### Code / Debug
- known failed fixes
- successful debugging methods
- incompatible configurations
- recurring error patterns
- useful testing strategies

### Research
- source reliability lessons
- failed search strategies
- useful evidence patterns

### Design
- rejected design patterns
- successful conventions
- user corrections

### Model
- runtime/model incompatibilities
- benchmark observations
- training failures
- optimization wins

## Tree-Specific Lessons

Useful for one Tree's role or operating pattern.

## Environment Lessons

Facts learned about the user's actual system/environment that materially affect execution.

## User Corrections

Explicit instructions or corrections from the user that should alter future behavior.

---

# 10. Operational Learning vs. Syrup

The systems overlap but should remain conceptually distinct.

```text
Operational Learning
→ actionable lessons from experience

Syrup
→ distilled personalization and tendencies
```

Example Syrup:
> User prefers concise openings in email drafts.

Example Operational Learning:
> User explicitly requires runtime verification before a technical phase is marked complete.

Strong user corrections may therefore become Operational Learning records rather than only personalization.

---

# 11. Operational Learning vs. Leaves

Operational Learning should not merely be ordinary Leaves under a different name.

A Leaf is durable Forest knowledge.

Operational Learning is structured experience about **how to act, what happened, what failed, what worked, or what should change next time**.

Operational Learning may reference Leaves through Roots.

Possible relationship:

```text
Task / event / test
      ↓
evidence
      ↓
Operational Learning record
      ↓
Roots
      ├── source conversation
      ├── file
      ├── Task
      ├── Leaf
      ├── benchmark
      └── result
```

---

# 12. Mycelium and Learned Experience

Operational Learning should participate in Mycelium.

A Tree does not need direct access to another Tree's full conversations.

Instead:

```text
Bristlecone learns a relevant debugging lesson
            ↓
Operational Learning
            ↓
Mycelium
            ↓
Maple later works on related code
            ↓
relevant permitted lesson retrieved
```

The current Tree receives the useful continuity.

> **Trees share continuity without sharing consciousness.**

> **The magic should be inspectable magic.**

Roots should allow deep provenance inspection when the user wants it.

---

# 13. Maple, Spirit, and Cedar in Learning

## Maple

Maple can help:

- identify semantic similarity
- connect lessons across Tasks/Trees/time
- consolidate duplicates
- identify contradictions
- salvage useful experience from history
- map relationships
- distinguish recurring lessons from one-off noise

Maple does not own the learning database.

## Spirit

Spirit should handle deterministic rules:

- permissions
- retention
- cache invalidation
- lesson eligibility rules
- allowed propagation
- automatic policy
- lifecycle boundaries
- Skill-creation authorization

> **Trees decide what would be useful. Spirit decides what is allowed.**

## Cedar

Cedar ensures learned experience does not bypass data protection.

Protected source material must keep appropriate restrictions when converted into:
- lessons
- Syrup
- indexes
- summaries
- Mycelium references
- Skill proposals

---

# 14. Cache and Retrieval Architecture for Learning

Learned lessons must **not live only in cache**.

Caches are disposable derived state.

If every cache is deleted:
- lessons remain
- provenance remains
- the Forest still knows what it learned
- only retrieval becomes slower until caches rebuild

Preferred layering:

```text
Durable Operational Learning
            ↓
Lesson / Experience Index
            ↓
Prepared lesson caches
            ↓
Relevant hot subset
            ↓
Current Workshop / Task / Tree
```

Potential cache/index categories:

```text
forest / operational-learning-index
    Fast lookup over durable lessons.

forest / workshop-lessons
    Prepared relevant lessons for a Workshop.

forest / task-lessons
    Small hot lesson subset for the current Task.
```

Not every lesson belongs in model context.

> **A lesson can become context, but every lesson does not belong in context.**

---

# 15. Phase 14 and Phase 16 Relationship

Do not derail Phase 14 by building the entire learning system immediately.

## Phase 14

Build the infrastructure needed for fast future learning retrieval:

- CacheCoordinator
- parsed manifests
- capability-resolution cache
- learning retrieval/index cache foundations
- General Lesson cache path
- Workshop Lesson cache path
- future Task Lesson hot subset
- Layered Hot Context integration point

## Phase 16

Build the complete Forest Learning System:

- durable Operational Learning store
- mistake → lesson extraction
- successful outcome → lesson extraction
- explicit user correction handling
- General / Workshop / Tree scopes
- environment lessons
- confidence
- evidence and provenance
- Roots
- contradiction handling
- lesson aging/revision
- deduplication
- Mycelium sharing
- Maple consolidation
- Syrup interaction
- procedure candidates
- Skill proposal pathway
- Spirit approval rules
- protection inheritance
- evaluation of whether learning improved future work

Concise principle:

> **Phase 14 builds the roads. Phase 16 teaches the Forest how to drive on them.**

---

# 16. Revised Product / Architecture Doctrines

Preserve these as explicit Forest principles:

> **Complete by default. Modular underneath.**

> **External tools are choices, not dependencies.**

> **The Forest should learn from experience more freely than it creates new capabilities.**

> **Tree identity belongs to the Forest; intelligence providers are replaceable resources.**

> **Users grow and use their Forest. The Forest handles the infrastructure.**

> **A Forest installation should provide a complete AI ecosystem while remaining modular underneath: users should gain capabilities by growing their Forest, not by assembling a collection of unrelated AI applications.**

> **The Forest aims for 7–9/10 capability and 10/10 experience, ownership, privacy, security, continuity, and extensibility.**

> **It’s your Soil and your Forest. You use it how you want.**

---

# 17. Current Technical Status When This Checkpoint Was Written

Phase 14.5 — Cache Architecture / Coordinator:
- complete

Phase 14.6:
- 14.6A YAML / manifest load map — complete
- 14.6B Resolver lifecycle — complete
- 14.6C cache integration points — complete
- 14.6D parsed-YAML manifest cache — complete and behavior verified
- 14.6E capability-resolution cache — in preflight
  - 14.6E1 resolution contract captured
  - 14.6E2 selection normalization inspection is next

Important 14.6E1 finding:

`require_resolved` is applied after the resolver constructs `result`.

Therefore:
- it should **not** be part of the cached resolution identity
- the same resolution may support strict and non-strict callers
- strictness should be re-applied after retrieving a cached result

Current intended cache layering:

```text
authoritative manifests
        ↓
parsed-YAML cache
        ↓
capability-resolution cache
        ↓
Layered Hot Context
        ↓
Tree / Task
```

Future learning layering:

```text
authoritative Operational Learning
        ↓
learning indexes/caches
        ↓
relevant General / Workshop / Task lessons
        ↓
Layered Hot Context
        ↓
Tree
```

---

# 18. Long-Term Success Test

A user should be able to install the Forest and reasonably feel:

- I have the tools I normally need.
- My Trees know how to work together.
- My history does not vanish when I change models.
- My data belongs to me.
- I can inspect what the system knows and why.
- I can protect sensitive information.
- I can extend the system without replacing it.
- I can plug in stronger models or favorite apps when I choose.
- I do not need several separate AI applications just to obtain basic continuity.
- The Forest becomes more useful as it learns from experience.

The Forest does not need to be the fastest or strongest system at every isolated benchmark.

It should aspire to be the **best place for the user's AI ecosystem to live**.

---

# Addendum — Tree / Clone / Colony Architecture

The Forest architecture now explicitly includes a Colony layer.

Key decisions:

- **Tree** = primary/base identity.
- **Clone** = independently operating extension of that Tree.
- **Colony** = base Tree + all Clones.
- Trees may self-clone within Spirit-defined resource, permission, and security boundaries.
- Prefer **reuse/wake before clone**.
- Persistent Clones are lightweight durable state, not permanently active compute.
- Clones share durable Tree continuity but keep separate live Tasks, sessions, Workshops, hot context, and runtime state.
- Colony synchronization is same-Tree continuity; Mycelium remains cross-Tree continuity.
- Clone learning may be Clone-local, Workshop-level, Tree-wide, or Forest/user-wide.
- Capability infrastructure is shared; activation is Clone-specific.
- Base Tree and Clones may access the same ordinary capability simultaneously without each loading all tools.
- Scarce/exclusive resources should be leased through Spirit.
- Clone count must not scale tool/model/backend infrastructure count.
- Retained Clone limits and active Clone limits should be separate.
- Cache architecture should support Forest → Tree → Clone → Task → runtime scopes.
- Phase 14 must remain Clone-compatible before full Clone execution is implemented.

See the focused checkpoint:

`forest_tree_clone_colony_architecture_checkpoint_2026-08-09.md`
