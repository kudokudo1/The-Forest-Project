# Project Forest — Tree, Clone, and Colony Architecture Checkpoint

**Date:** 2026-08-09  
**Status:** Active architecture checkpoint  
**Purpose:** Preserve the Forest-native design for self-cloning Trees, Colonies, capability sharing, persistence, learning, permissions, resource management, and Phase 14 compatibility.

---

# Core Definitions

## Tree

A **Tree** is the primary/base identity.

When users say “Maple,” “Cherry,” “Cedar,” or “Bristlecone,” they normally mean the base Tree identity.

## Clone

A **Clone** is an independently operating extension of a Tree.

> **A Clone is an extension of a Tree, not another Tree.**

A Clone may operate in another time, place, role, Workshop, Task, runtime session, or environment while remaining part of the same Tree.

## Colony

A **Colony** is the base Tree and all of its Clones.

```text
MAPLE COLONY
│
├── Maple                 ← base Tree
├── Maple Clone: Mail
├── Maple Clone: Design
├── Maple Clone: Syrup
└── Maple Clone: Project X
```

> **A Colony is a Tree and all of its Clones. A Clone is an independently operating extension of that Tree, sharing its identity and durable continuity while maintaining its own active work state.**

> **One Tree. More than one place.**

---

# Architectural Hierarchy

```text
Forest
  ↓
Tree
  ↓
Colony
  ↓
Clone
  ↓
Task
  ↓
Turn
```

A Workshop answers: **What kind of work is this Tree/Clone doing?**

A Clone answers: **Which active presence of the Tree is doing it?**

A model answers: **What intelligence resource is currently powering it?**

These are independent axes.

---

# Self-Cloning Trees

Trees should normally be allowed to create, reuse, wake, or retain Clones autonomously within Spirit-defined boundaries.

Ordinary use should not require explicit approval for every Clone.

```text
User gives Task
    ↓
Tree determines a Clone is useful
    ↓
Spirit checks policy/resource/security boundaries
    ↓
Tree creates, wakes, or reuses Clone
    ↓
work begins
```

> **User control should exist without requiring user management.**

Possible future user controls:

```text
Cloning
○ Automatic
○ Conservative
○ Ask first
○ Disabled
```

Exact UI is not frozen.

---

# Spirit Governs Cloning

```text
Tree wants Clone
      ↓
Spirit checks
├── Is self-cloning allowed?
├── Is an existing Clone reusable?
├── Is the Colony within resource budget?
├── Is the requested Workshop allowed?
├── Are required permissions allowed?
├── Is the Soil/environment appropriate?
└── Is the action safe?
      ↓
reuse / wake / create / refuse
```

> **Reuse before clone.**

---

# Clone Lifetimes

## Ephemeral Clone

Created for one Task or temporary parallel activity, then sleeps or is removed after useful durable state is committed.

## Persistent Clone

Represents a recurring role, such as Maple-Mail.

## Project Clone

Exists for a long-running project and can be archived/dormant after the project closes.

The Forest should learn when repeated temporary work becomes a recurring function and cultivate a persistent Clone.

Possible internal lifecycle:

```text
Ephemeral
    ↓
Repeatedly useful
    ↓
Established
    ↓
Persistent
```

---

# Persistent Clone Does Not Mean Persistent Compute

Keeping a Clone should normally retain lightweight durable state:

```text
Clone ID
purpose
Workshop affinity
learned lessons
configuration
history references
capability preferences
schedule/event bindings
```

It should not automatically mean:

```text
model permanently loaded
large RAM reservation
runtime session permanently active
tools permanently hot
KV cache permanently retained
```

Preferred lifecycle:

```text
Dormant Clone
    ↓
Task/event arrives
    ↓
wake
    ↓
load minimal relevant state
    ↓
do work
    ↓
record useful durable changes
    ↓
sleep
```

---

# Shared Durable State vs. Separate Active State

## Shared across the Colony

```text
Tree identity
purpose/personality
Leaves
Roots
Operational Learning
General lessons
Tree-wide lessons
user corrections
Syrup / user model access
Mycelium relationships
long-term history
stable preferences
approved durable Skills
Tree configuration
```

## Separate per Clone

```text
current Task
current conversation/session
hot context
active Workshop
Ready rack
temporary Skills
temporary capabilities
temporary files
working assumptions
runtime session ID
current model/runtime
runtime KV/inference state
current Soil/execution environment
short-lived scratch state
```

> **Clones share durable Tree state, not unrestricted live context.**

---

# Colony Synchronization vs. Mycelium

```text
Colony
→ same Tree, multiple presences

Mycelium
→ different Trees, permitted continuity
```

Maple-Mail ↔ Maple-Main is Colony continuity.

Maple-Mail ↔ Cherry is cross-Tree continuity through Mycelium and permissions.

---

# Clone Learning

Clone experience may be classified as:

```text
Clone Experience
      ↓
classify scope
      │
      ├── Clone-local
      ├── Workshop
      ├── Tree-wide
      └── Forest/user-wide
```

Durable learning may be shared, but retrieval remains relevance-based.

A Clone may specialize without becoming a separate Tree identity.

```text
Identity/personality
      ↑
   Tree-owned

specialized experience
      ↑
  Clone-owned
```

> **A Clone may become better at its job without becoming a different Tree.**

---

# Capability Ownership

Clones should not physically clone the Tree’s tools.

Separate these questions:

```text
Does the Tree know a capability exists?
        ≠
Is the Tree/Clone allowed to use it?
        ≠
Is the capability currently hot?
```

> **Trees own capability. Clones carry only the capability they need.**

> **Shared capability, separate activation.**

> **Clone the Tree’s working state, not the infrastructure.**

The base Tree and multiple Clones may know about and access the same capability simultaneously without loading every tool schema into hot context.

---

# Shared Capability Infrastructure

```text
                    mail.read
                       │
          shared Forest capability
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Base Maple     Mail Clone     Project Clone
```

Each can have its own permissions, Task state, runtime binding/session, hot schema activation, and temporary authorization without duplicating the tool implementation.

---

# Clone Tool Layers

## Clone Core
Bare minimum capabilities kept hot for the Clone’s purpose.

## Clone Ready Rack
A small set of likely-next capabilities whose metadata/preparation may remain warm without full hot-context cost.

## On-Demand Forest Capabilities
Everything else the Tree is permitted to use, resolved only when needed.

## Exclusive Resource Leases
Scarce or non-shareable resources temporarily leased by Spirit.

> **Ready keeps likely tools close; it does not keep them hot.**

Example:

```text
MAPLE-MAIL

HOT CORE
├── mail read/search
├── mail draft
├── contacts
└── basic file access

READY
├── calendar
├── document reading
└── attachment inspection

ON DEMAND
├── web research
├── image generation
├── terminal
└── code execution
```

---

# Capability Cultivation

Persistent Clones can learn which capabilities are typically useful.

Example:

```text
mail.search        98%
mail.read          97%
mail.draft         81%
contacts           63%
calendar           38%
web                 7%
image generation    1%
terminal             0%
```

This can cultivate:

```text
CORE
mail.search
mail.read
mail.draft
contacts

READY
calendar

COLD / ON DEMAND
web
image generation
terminal
```

This is desirable self-improvement without unrestricted Skill creation.

---

# Clone Permissions

A Clone inherits Tree identity, not necessarily every active privilege.

```text
Clone requests capability
       ↓
Spirit checks:
├── Is the Tree allowed?
├── Is this Clone allowed?
├── Does user policy require approval?
└── Is the action consequential?
       ↓
allow / ask / deny
```

> **A Clone inherits identity, not automatically every active privilege.**

---

# Shared Capabilities vs. Exclusive Resources

Ordinary software capabilities can generally be used concurrently:

```text
files
mail
calendar
web
search
contacts
code tools
document tools
```

Scarce or inherently exclusive resources may require Spirit leases:

```text
GPU-heavy model slot
camera
microphone recording session
single-writer resource
exclusive device
certain protected credentials
```

> **Capabilities are normally shared. Scarce resources are leased.**

---

# Avoiding Clone / Tool Explosion

The Forest must avoid dozens of Maple and Cherry Clones each carrying duplicated email, todo, model, and backend infrastructure.

> **Clone count must not scale infrastructure count.**

Ideally:

```text
10× more retained Clones
≠
10× more tool implementations
≠
10× more models
≠
10× more backend services
```

Most retained Clone cost should be lightweight state, references, and metadata.

Only simultaneously hot Clones should materially increase compute/RAM.

---

# Active vs. Retained Clone Limits

Spirit should distinguish:

## Retained Clone limit
Can be relatively generous because dormant records are cheap.

## Active Clone limit
Must be stricter because hot Clones consume compute, context, RAM, sessions, and active capability state.

Example:

```text
25 retained Clones

2 hot
3 warm
20 dormant
```

---

# Colony Resource Policy

```text
New work arrives
      ↓
Can an existing Clone handle it?
   YES → reuse/wake
    │
    NO
    ↓
Can the base Tree handle it cheaply?
   YES → base Tree handles it
    │
    NO
    ↓
Would parallel/specialized Clone help?
   NO → continue without Clone
    │
   YES
    ↓
Resource/security policy allows?
    ↓
create Clone
```

> **Reuse before clone.**

---

# Concurrency and Durable Updates

Multiple Clones may propose simultaneous durable changes.

Preferred pattern:

```text
Clone proposes durable update
        ↓
Spirit
        ↓
permission validation
        ↓
version/generation check
        ↓
commit / merge / conflict
        ↓
shared Tree state updated
```

The existing TaskSession generation/CAS/locking philosophy should influence Colony design.

---

# Cache Hierarchy Extended by Colonies

```text
FOREST CACHE
     ↓
TREE CACHE
     ↓
CLONE CACHE
     ↓
TASK CACHE
     ↓
TURN
     ↓
RUNTIME / INFERENCE CACHE
```

## Forest-level examples
- parsed manifests
- capability-resolution structures
- shared Operational Learning indexes
- shared Leaf indexes

## Tree-level examples
- prepared Tree Core
- general Tree lessons
- stable Tree context

## Clone-level examples
- Clone Workshop preparation
- Clone-specific lessons
- recurring source indexes
- capability affinity / Ready preparation

## Task-level examples
- current working set
- temporary capabilities
- Task-Sticky state
- relevant Leaves

## Runtime-level examples
- KV cache
- native prefix cache
- runtime session
- model execution state

---

# Phase 14 Requirement

Phase 14 must not assume that one Tree has only one active presence.

> **Cache and capability architecture must scale with active state, not total Colony size.**

Full Clone execution can come later, but current cache/session identities must remain Clone-compatible.

Immediate engineering consequences:

1. Keep Forest-neutral caches shared.
2. Avoid cache keys that assume Tree == one session.
3. Leave room for Tree ID and Clone ID scopes.
4. Keep tool definitions shared.
5. Keep tool activation Clone-specific.
6. Separate retained Clone records from hot runtime sessions.
7. Let shared capability resolution feed many Clone-specific activation plans.
8. Preserve Spirit arbitration for exclusive resources and concurrent durable writes.

---

# Updated Forest Doctrines

> **A Colony is a Tree and all of its Clones.**

> **A Clone is an extension of a Tree, not another Tree.**

> **One Tree. More than one place.**

> **Trees may extend themselves through Clones within Spirit-defined boundaries.**

> **The user controls the Colony without having to manage it.**

> **Reuse before clone.**

> **Clones share durable Tree state, not unrestricted live context.**

> **Trees own capability. Clones carry only the capability they need.**

> **Shared capability, separate activation.**

> **Clone the Tree’s working state, not the infrastructure.**

> **Ready keeps likely tools close; it does not keep them hot.**

> **A Clone inherits identity, not automatically every active privilege.**

> **Capabilities are normally shared. Scarce resources are leased.**

> **Clone count must not scale infrastructure count.**

> **Cache and capability architecture must scale with active state, not total Colony size.**

> **A Clone may become better at its job without becoming a different Tree.**
