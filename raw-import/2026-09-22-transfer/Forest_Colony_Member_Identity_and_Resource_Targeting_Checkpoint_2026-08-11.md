# The Forest — Colony Member Identity & Resource Targeting Checkpoint

**Date:** 2026-08-11  
**Phase:** 14.11H — Colony Runtime / Shared-Weight Semantics  
**Status:** Architecture clarification captured before H.5 certification

## Source checkpoint

This clarification is grounded in the existing Model Form / Clone / Resource Management architecture checkpoint:

[Open the original architecture checkpoint](./The_Forest_Model_Form_Clone_and_Resource_Management_Architecture_Checkpoint_2026-08-11_v3.md)

Original filename:

`The_Forest_Model_Form_Clone_and_Resource_Management_Architecture_Checkpoint_2026-08-11_v3.md`

## Clarified identity model

The Forest should treat each member of a Tree's Colony as individually addressable without creating a second competing Tree identity.

```text
Tree / Colony
tree_id = maple
│
├── Ortet
│   execution_context_id = maple-ortet-001
│
├── Ramet
│   execution_context_id = maple-photo-7f3a
│
└── Ramet
    execution_context_id = maple-code-a821
```

### Canonical fields

```text
tree_id
= Which Tree / Colony does this member belong to?

execution_context_id
= Which individual Ortet or Ramet is being addressed?

lineage_role
= Is this member the original Ortet or a cloned Ramet?

operational_role
= What job or role is this member currently performing?
```

## Important clarification

Earlier Colony planning explicitly left room for both **Tree ID** and **Clone ID** scopes.

The later architecture refined that idea so that a separate `clone_id` or `ramet_id` is normally unnecessary.

Instead:

> **`execution_context_id` is the canonical stable technical identifier for an individual Ortet or Ramet.**

This means Forest UI may say **Ramet**, **Clone**, **Ortet**, **Main**, or a user-friendly name such as **Photo Ramet**, while core logic targets the same stable `execution_context_id`.

## Resource-management targeting

The Resource Management system should be able to target an individual active Colony member rather than treating a Tree as one indivisible workload.

Conceptually:

```text
Resource target
= tree_id + execution_context_id
```

Examples:

```text
(tree_id=maple, execution_context_id=maple-code-a821)
→ prioritize this Ramet

(tree_id=maple, execution_context_id=maple-photo-7f3a)
→ pause/checkpoint this Ramet

(tree_id=cedar, execution_context_id=cedar-ortet-001)
→ preserve protected minimum resources
```

This keeps resource decisions precise when one Tree has several simultaneous Ramets.

## Identity must remain separate from runtime machinery

Do not confuse Colony-member identity with model/runtime identity.

```text
tree_id
+ execution_context_id
    = Tree/Colony member identity

binding_id
    = selected runtime/model binding

session_id
    = one live runtime session

residency_id
    = shared model-weight residency
```

Therefore:

```text
Same Tree
+ different execution_context_id
= different Ortet/Ramet members

Same binding_id
+ different execution_context_id
= separate sessions/KV/control state
  that may share model weights
```

## Current H identity layers

```text
ColonyExecutionContext
├── tree_id
├── execution_context_id
├── lineage_role
└── operational_role

RuntimeSessionIdentity
├── execution_context_id
└── binding_id

SharedModelResidency
├── residency_id
├── binding_id
└── adapter
```

These layers should remain distinct.

## H.5 doctrine update

H.5 should certify Ramets as actual Clones of the same Tree, not merely unrelated contexts.

The test model should therefore use one shared `tree_id` and several different `execution_context_id` values:

```text
Bristlecone Colony

Ortet
├── tree_id = bristlecone
└── execution_context_id = ctx-O

Ramet A
├── tree_id = bristlecone
└── execution_context_id = ctx-R1

Ramet B
├── tree_id = bristlecone
└── execution_context_id = ctx-R2
```

### Shared Tree-level state

Examples:

- Tree identity
- durable personality and purpose
- durable approved configuration
- durable Tree knowledge
- Leaves / Roots
- Operational Learning
- long-term shared state where policy permits

### Clone-local active state

Examples:

- `execution_context_id`
- active Task
- Model Form control
- Reasoning control
- temporary overrides and leases
- Workshop activation
- temporary capabilities
- Task-sticky Skills
- runtime session
- KV / conversation state
- temporary permissions and resource leases
- scratch state

## Resource invariant

> **The resource-allocation unit is the active execution context/workload, not merely the Tree name.**

Therefore Resource Steward / Governor / Scheduler logic should be able to reason about and act on one specific Ortet or Ramet while preserving the identity and state of the rest of the Colony.

## No duplicate identity fields without new semantics

Do not add fields such as:

```text
clone_id
ramet_id
colony_id
genet_id
```

merely as aliases for concepts already represented by:

```text
tree_id
execution_context_id
lineage_role
operational_role
```

A new identifier should only be introduced later if it represents genuinely different semantics rather than another name for the same object.

## Phase 14.11H invariant

> **`execution_context_id` is both the mutable-execution boundary and the canonical addressable identity of one Ortet or Ramet inside a Tree's Colony.**

> **`tree_id` says whose Colony it belongs to; `execution_context_id` says which Colony member.**

> **Resource Management targets active work at the execution-context level while Spirit/Governor remains the authority over what resource actions are allowed.**

---

**Forest doctrine:** One Tree. More than one place.
