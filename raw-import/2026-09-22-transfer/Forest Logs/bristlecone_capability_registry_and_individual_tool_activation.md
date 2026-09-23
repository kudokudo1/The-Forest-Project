# The Forest — Bristlecone Capability Registry and Individual Tool Activation

**Status:** Adopted refinement  
**Tree:** Bristlecone Pine  
**Purpose:** Reduce duplication, keep active context minimal, and allow Bristlecone to activate individual general or task-specific capabilities without loading entire boxes.

## Core decision

Capabilities should be defined **once** in a central, Tree-owned capability registry.

Workshops and the General Tool Box should act as **activation policies**, not separate duplicate inventories.

> **Capabilities exist once. Boxes only describe when they are easy or automatic to activate.**

## General Ready capabilities

Initial General Ready set:

- `todo`
- `clarify`
- `session`
- `memory`
- `leaf`

`leaf` belongs here because Forest / Leaf Foliage context can be useful in Research, Design, Code / Debug, or Model work.

## Individual activation rule

Activating one General capability must **not** activate the rest of the General Tool Box.

```text
GENERAL TOOL BOX

todo        DORMANT
clarify     DORMANT
session     DORMANT
memory      DORMANT
leaf        DORMANT
```

If Bristlecone needs Leaf:

```text
todo        DORMANT
clarify     DORMANT
session     DORMANT
memory      DORMANT
leaf        ACTIVE
```

The same rule applies to task-specific Workshop Ready capabilities.

```text
CODE / DEBUG READY

debugging       DORMANT
testing         DORMANT
code-execution  DORMANT
special         DORMANT
```

If testing is needed:

```text
testing → ACTIVE
```

Nothing else is activated automatically.

## Boxes are indexes, not containers

Think of each box as a rack of individually addressable capabilities.

```text
GENERAL RACK
├── [todo]
├── [clarify]
├── [session]
├── [memory]
└── [leaf]
```

```text
CODE / DEBUG READY RACK
├── [debugging]
├── [testing]
├── [code-execution]
└── [special]
```

Bristlecone reaches for one capability rather than dumping the whole rack into model context.

## Capability states

Each capability can be:

- **Dormant** — known to the runtime, not injected into model context.
- **Active** — loaded because the current task needs it.
- **Sticky** — retained across related turns.
- **Core** — automatically active whenever a particular Workshop is selected.

## General capability promotion

A capability can be General Ready globally while also being Core in a specific Workshop.

Example:

```text
memory
│
├── General Ready
├── Design → CORE
├── Research → DORMANT
├── Code / Debug → DORMANT
└── Model → DORMANT
```

This does not duplicate `memory`; Design merely changes its activation policy.

The same pattern applies to `clarify`.

## Workshop Core sets

### Research

```text
CORE
web
```

General Ready capabilities remain individually available.

### Design

```text
CORE
memory
clarify
```

These are promoted from General Ready while Design is active.

### Code / Debug

```text
CORE
file
terminal
```

### Model

```text
CORE
file
terminal
```

## Workshop Ready sets

### Code / Debug Ready

```text
debugging
testing
code-execution
special
```

### Model Ready

```text
model-evaluation
model-benchmarking
model-inference
quantization
training
runtime-inspection
```

Research- and Design-specific Ready capabilities should only be added after testing shows they are useful.

## General and Workshop tools can be active together

Bristlecone does not leave a Workshop to use a General capability.

Example:

```text
CURRENT WORKSHOP
Code / Debug

CORE
file
terminal

GENERAL ACTIVE
todo

WORKSHOP READY ACTIVE
debugging
```

Effective capability set:

```text
file
terminal
todo
debugging
```

When Todo is no longer needed:

```text
todo → DORMANT
```

Code / Debug remains active.

## Central capability registry

Target architecture:

```text
BRISTLECONE CAPABILITY REGISTRY
│
├── todo
├── clarify
├── session
├── memory
├── leaf
├── file
├── terminal
├── web
├── code-execution
├── debugging
├── testing
├── model-evaluation
└── ...
        │
        ▼
ACTIVATION POLICIES
│
├── General Ready
├── Workshop Core
└── Workshop Ready
```

Capabilities are defined once. Activation policies reference them.

## Active capability stack

The runtime should construct Bristlecone's model-visible capability set from layers:

```text
BASE TREE
tiny always-present identity

+

WORKSHOP CORE
file
terminal

+

GENERAL OVERLAY
leaf

+

WORKSHOP READY OVERLAY
debugging

+

HOT LEAVES
only task-relevant knowledge
```

Effective active set:

```text
file
terminal
leaf
debugging
```

Everything else remains dormant.

## Performance principle

General Ready does **not** mean always loaded.

Earlier Bristlecone testing showed that permanently adding `todo` to `file + terminal` substantially increased latency. Therefore:

> **General availability should be cheap. General activation may have a cost.**

The runtime should only pay that cost when the task benefits from the capability.

## Minimum Useful Canopy rules

> **Activating one capability never activates the rest of its box.**

> **A capability becomes Core only when most tasks in that Workshop are expected to need it.**

This avoids both excessive context and unnecessary activation churn.

## Planned filesystem layout

```text
~/The-Forest/bristlecone/
├── capabilities/
│   └── registry.yaml
├── workshops/
│   ├── research.yaml
│   ├── design.yaml
│   ├── code-debug.yaml
│   └── model.yaml
├── adapters/
│   └── hermes.yaml
├── routing/
├── learning/
├── state/
└── skills/
```

The central registry is authoritative for capability definitions.

Workshop files become activation-policy documents.

## Verified Hermes mappings

```text
Forest ID          Hermes target

web                web
file               file
terminal           terminal
memory             memory
session            session_search
clarify            clarify
todo               todo
code-execution     code_execution
context-engine     context_engine
skills             skills
```

`leaf` remains Forest-native and unresolved until its real retrieval path is implemented.

## Immediate implementation plan

1. Create `capabilities/registry.yaml`.
2. Define verified capabilities once.
3. Mark `todo`, `clarify`, `session`, `memory`, and `leaf` as General Ready.
4. Refactor Workshop YAML files so they reference capability IDs.
5. Promote `memory` and `clarify` to Design Core.
6. Keep `file + terminal` as Code / Debug Core.
7. Keep `file + terminal` as Model Core.
8. Keep `web` as Research Core.
9. Keep specialized capabilities individually activatable.
10. Validate every Workshop reference against the registry.
11. Validate runnable capabilities against the Hermes adapter.
12. Build the Workshop selector/runtime registry only after validation succeeds.

## Working principle

> **One capability definition. Many activation policies. Individual activation. No unnecessary box-wide loading.**

This becomes part of the Forest's Minimum Useful Canopy architecture.

**Pine is fine.**
