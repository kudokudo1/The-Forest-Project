# Forest Spirit and Pruning Policy

## Core Principle

> **Trees maintain themselves naturally. Spirit enforces bounded maintenance policies. Users shape the Tree.**

The Forest should allow Trees and Spirit to handle routine maintenance automatically so casual users do not need to understand AI internals, commands, memory systems, retrieval systems, or storage architecture.

At the same time, Forest tools should give power users deliberate control over the exact shape, growth, and retained knowledge of their Trees.

The metaphor is not decorative. It is a human-facing abstraction over real AI operations.

> **Simple on the surface. Precise underneath. Inspectable when desired.**

---

## Natural Tree Maintenance

Trees should generally maintain themselves through their normal lifecycle.

Examples include:

- growing useful knowledge
- shedding material that no longer needs to remain active
- entering dormancy
- Spring Cleaning
- selective restoration
- routine context reduction
- ordinary cache maintenance
- knowledge organization
- retrieval maintenance
- duplicate detection
- health checks
- index maintenance
- seasonal transitions

These processes are part of normal Tree behavior and do **not** require the user to manually intervene.

Natural maintenance is distinct from Pruning.

---

## Pruning

> **Pruning is a controlled, deliberate intervention initiated or authorized by the user or Spirit to shape a Tree by cutting back unwanted, incorrect, obsolete, excessive, harmful, or otherwise undesired growth while preserving the knowledge, behaviors, and structure that should remain.**

Pruning is not ordinary autonomous Tree maintenance.

A Tree may identify or recommend possible pruning candidates, but normal autonomous reduction belongs to seasonal and Leaf Litter processes.

### Short distinction

> **Pruning shapes the Tree. Shedding is part of the Tree's natural lifecycle.**

---

## Pruning vs. Shedding vs. Leaf Litter

### Shedding

Tree-driven and part of the natural lifecycle.

Typical meaning:

> "This is not needed in the active canopy right now."

Shedding does not necessarily mean deletion.

### Leaf Litter

Leaf Litter is the lifecycle handling of material that has naturally left active use.

It can support:

- temporary retention
- later inspection
- restoration
- decomposition
- eventual deletion
- recycling or consolidation

### Pruning

Pruning is deliberate Tree shaping.

Typical meaning:

> "This growth should not remain part of the Tree in its current form."

Pruning may target:

- incorrect knowledge
- obsolete knowledge
- duplicate growth
- unwanted new growth
- excessive growth
- harmful growth
- behavior the user does not want reinforced
- material outside the intended shape or purpose of the Tree

---

# Authority Model

## Trees

Trees handle ordinary self-maintenance.

They may:

- grow
- shed
- sleep
- clean
- restore
- organize
- identify problems
- recommend pruning candidates

Trees should **not** have unrestricted access to their own pruning tools simply because they believe something is unnecessary.

---

## Spirit

Spirit may have **restricted, bounded, automated access** to pruning functions.

Spirit does not receive unrestricted authority to shape a Tree.

Instead, Spirit executes user-approved maintenance policies.

A useful principle is:

> **Spirit has broad visibility but narrow autonomous authority.**

Spirit can monitor:

- Tree growth
- Leaf counts
- storage use
- health
- user-defined limits
- permissions
- pruning policies
- protected knowledge

But automatic pruning must remain inside explicit policy boundaries.

---

## User

The user has the primary deliberate shaping authority.

The user may explicitly:

- prune selected growth
- preserve selected growth
- set Tree-specific growth budgets
- protect important Leaves
- remove incorrect knowledge
- cut back unwanted new or old growth
- restrict a Tree's growth direction
- set automatic pruning rules
- restore recently pruned material where possible
- inspect exactly what a pruning operation changed

---

# Manual and Automatic Pruning

Pruning can occur in two authorization modes.

## Manual Pruning

The user explicitly chooses what should be cut back or reshaped.

Examples:

- "Prune this topic."
- "Remove everything learned from this bad source."
- "Keep these Leaves and cut the rest."
- "Undo the last unwanted growth."
- "Cut this branch back to the approved state."

Manual pruning is direct user shaping.

---

## Automatic Pruning

Spirit executes a pruning policy previously defined or authorized by the user.

Automatic pruning is still ultimately **user-directed**.

Spirit is not deciding:

> "I do not like these Leaves."

Spirit is enforcing:

> "The user defined this growth limit and approved this pruning policy."

This avoids requiring another AI model to wake up simply to perform routine size or storage maintenance.

---

# Tree-Specific Growth Budgets

Each Tree may have its own growth and storage policy.

For example:

```text
Personal Tree
Leaf budget: large
Auto-prune: conservative or off

Code Tree
Leaf budget: smaller
Auto-prune: on
```

A user may want to dedicate more memory or storage to a Personal Tree while allowing a heavily used Code Tree to prune aggressively because it continually generates troubleshooting or project-specific Leaves the user does not want to retain forever.

Possible user-facing limits include:

- maximum Leaf count
- target Leaf count after pruning
- maximum Tree storage
- maximum indexed storage
- maximum number of inactive Leaves
- minimum free device storage
- age limits for low-priority generated Leaves
- maximum growth per time period

---

# Example: Leaf-Count Auto-Pruning

A budget device may use a deterministic policy such as:

```text
IF Code Tree Leaf count >= 2,000
THEN run approved pruning policy
UNTIL Leaf count <= 1,750
```

This can often be handled by Spirit without invoking an LLM.

Spirit may use metadata such as:

- Leaf age
- last access time
- access frequency
- importance
- confidence
- protected status
- user pinning
- duplicate status
- superseded status
- source availability
- Tree ownership
- current Task relevance

---

# Protected Classes

Automatic pruning should operate behind strong safety boundaries.

## Never Auto-Prune

Examples may include:

- user-pinned Leaves
- Tree identity
- Spirit policies
- explicitly permanent memories
- protected Roots
- critical project decisions
- current Task material
- other user-marked protected knowledge

## Auto-Prune Eligible

Examples may include:

- duplicates
- superseded Leaves
- expired temporary knowledge
- low-value generated observations
- old low-use debugging artifacts
- recoverable derived data
- other categories explicitly approved by the user

## Review Required

Examples may include:

- unique user-created knowledge
- high-value memories
- Leaves with important dependents
- Leaves whose importance is uncertain
- material with ambiguous provenance

---

# Pruning Does Not Always Mean Immediate Deletion

Pruning is the deliberate shaping action.

The technical treatment may vary depending on what is being pruned.

Possible outcomes include:

```text
Incorrect
→ replace or remove

Obsolete
→ archive or mark superseded

Duplicate
→ merge

Unwanted
→ remove

Potentially harmful
→ quarantine or restrict

Excessive growth
→ cut back to an approved state
```

A pruning operation should preserve useful structure wherever possible.

---

# Leaf Litter as a Safety Layer

Pruned material does not always need to be destroyed immediately.

A safer workflow may be:

```text
Tree
  ↓
Pruning
  ↓
Leaf Litter
  ├─ inspect
  ├─ restore
  └─ decompose after retention period
```

This allows accidental or overly aggressive pruning to be reversible for a defined period.

Some pruning actions, such as merging duplicates or marking a Leaf as superseded, may not require destructive deletion at all.

---

# Casual User Experience

A casual user should not need to understand:

- vector databases
- embeddings
- index invalidation
- graph edges
- retrieval chunks
- context caches
- memory consolidation
- capability policy
- provenance systems

They should be able to express conceptual intent:

- "Keep this."
- "This is wrong."
- "Cut this back."
- "Do not let this Tree grow this way."
- "Keep this Tree around 2,000 Leaves."
- "Protect these memories."

Forest translates that intent into the required AI and storage operations.

---

# Power User Experience

The same Forest tool should expose deeper technical visibility when desired.

A casual user might see:

> ✂️ Pruned.

A power user might inspect:

```text
3 Leaves superseded
1 Leaf removed
2 Leaves merged
14 retrieval chunks rebuilt
6 Roots updated
hot-context cache invalidated
```

An expert view may expose:

- canonical IDs
- storage paths
- graph relationships
- embedding/index changes
- policy decisions
- transaction logs
- runtime effects
- rollback information

The Forest should not require separate "simple" and "advanced" systems.

Instead:

> **The Forest gets deeper as you wonder.**

---

# Human Intent as the Interface

A central Forest design principle is:

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

And:

> **Forest tools express human intent at the level of the metaphor while performing the necessary AI operations underneath.**

A tiny pair of pruning shears may conceptually represent a complex transactional operation involving:

- selecting affected Leaves
- checking Roots and provenance
- preserving protected knowledge
- superseding obsolete Leaves
- removing incorrect durable memory
- merging duplicates
- rebuilding retrieval chunks
- regenerating embeddings
- updating graph relationships
- invalidating affected caches
- adjusting operational-learning records
- applying permission rules
- recording the pruning transaction
- verifying Tree consistency afterward

The user does not need to know any of that unless they choose to inspect it.

---

# Canonical Responsibility Split

```text
AUTONOMOUS TREE CARE
Tree + Spirit
│
├── seasonal lifecycle
├── Leaf Litter
├── ordinary maintenance
├── health management
└── routine cleanup


BOUNDED AUTOMATED SHAPING
Spirit
│
├── user-defined limits
├── storage budgets
├── Leaf-count policies
├── protected classes
└── deterministic auto-pruning


DELIBERATE TREE SHAPING
User / Spirit-authorized
│
├── pruning
├── targeted correction
├── structural intervention
└── explicit growth control
```

---

# Frozen Design Principles

> **Trees maintain themselves naturally. Spirit enforces bounded maintenance policies. Users shape the Tree.**

> **Pruning shapes the Tree. Shedding is part of the Tree's natural lifecycle.**

> **Spirit has broad visibility but narrow autonomous authority.**

> **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**

> **Forest tools express human intent at the level of the metaphor while performing the necessary AI operations underneath.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

> **The Forest gets deeper as you wonder.**
