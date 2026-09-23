# Project Forest — User Context, Preference, Correction, Trigger Routing, and Learning Checkpoint

**Date:** 2026-08-09  
**Status:** Active architecture checkpoint  
**Purpose:** Preserve the current Forest architecture for explicit user context, preferences, constraints, corrections, Syrup, context-trigger routing, Cold/Warm/Hot placement, per-input route memoization, Task-Sticky context, and how these systems interact with Trees, Clones, Colonies, Spirit, Operational Learning, and Phase 14 Layered Hot Context.

---

# 1. Core Product Goal

The Forest should not make users repeatedly restate durable facts, preferences, or constraints that materially affect recommendations and actions.

Examples:

- A user asking for recipes should not need to repeatedly restate a serious food constraint.
- A user who consistently prefers free/open-source/local-first/self-hosted software should not routinely receive expensive subscriptions or proprietary products as the first recommendation merely because they are popular or technically correct.
- A user should not have to repeatedly remind a Tree of communication, workflow, purchasing, design, privacy, or execution preferences that the Forest already knows.

At the same time, the Forest should **not load the user's entire context before every Task**.

The architecture must provide strong continuity without turning personalization into permanent prompt bloat or a retrieval pass on every turn.

---

# 2. User Preference and User Correction Are Different Concepts

## User Preference

A **User Preference** describes how the user generally likes or wants something done.

Examples:

```text
Prefer free/open-source software.
Prefer local-first or self-hostable solutions.
Avoid subscriptions when practical.
Prefer a particular communication style.
Prefer a particular design style.
Prefer a certain price range.
```

A preference may be explicit or, eventually, proposed from strong repeated patterns.

## User Correction

A **User Correction** records that the Forest's previous belief, behavior, interpretation, or action was wrong or insufficient and should change.

Examples:

```text
"Don't mark a technical phase complete until it is verified."
"That is the wrong slogan."
"Draft the email, but do not send it automatically."
"I already told you to prioritize open-source options."
```

A correction represents a transition:

```text
previous belief / behavior
        ↓
user says it is wrong
        ↓
replacement belief / behavior
```

Corrections should retain provenance and revision history rather than silently erasing what was previously believed.

---

# 3. User Constraints Are Also Distinct

Some user context should not be represented merely as a preference.

A **User Constraint** restricts behavior or recommendations.

Examples:

```text
Food safety / allergy restriction
Privacy requirement
"Never send without approval"
"Do not use cloud services for this project"
Hard budget boundary
Accessibility requirement
```

Conceptually:

```text
Preference
→ favor / disfavor

Constraint
→ permit / exclude
```

Constraints may be normal or hard.

A hard constraint should be able to create a **MUST CHECK** context trigger.

---

# 4. User Context Is the Broader Category

The Forest should treat **User Context** as a first-class system.

Proposed structure:

```text
USER CONTEXT
│
├── Preferences
│   ├── likes / dislikes
│   ├── purchasing preferences
│   ├── software philosophy
│   ├── communication preferences
│   ├── workflow preferences
│   └── design preferences
│
├── Constraints
│   ├── safety restrictions
│   ├── privacy/security requirements
│   ├── hard purchasing limits
│   ├── accessibility requirements
│   └── explicit must / never rules
│
├── Corrections
│   └── explicit changes to Forest belief/behavior
│
└── Current Context
    ├── active project
    ├── current environment
    ├── device / OS
    ├── available resources
    └── relevant temporary circumstances
```

User Context is broader than Operational Learning.

---

# 5. Forest Learning and User Context Should Share Infrastructure, Not Meaning

The current conceptual architecture:

```text
FOREST LEARNING & CONTEXT
│
├── Operational Learning
│   ├── mistake
│   ├── success
│   ├── procedure
│   ├── environment
│   ├── constraint discovered through work
│   └── observation
│
├── User Context
│   ├── preference
│   ├── user constraint
│   ├── correction
│   └── current context
│
└── Syrup
    └── inferred / distilled personalization
```

Operational Learning and User Context may use common persistence, revision, provenance, indexing, and cache infrastructure while remaining semantically distinct.

A favorite design style should not have to be called an “operational lesson.”

---

# 6. Explicit User Context vs. Syrup

Preferred distinction:

```text
Explicit User Context
→ things the user directly told the Forest

Syrup
→ personalization inferred or distilled from history
```

Example:

```text
"I prefer open-source software."
→ explicit User Preference
```

Whereas:

```text
The Forest observes over time that the user almost always chooses:
- offline-capable tools
- lightweight interfaces
- keyboard-friendly workflows
```

may initially become Syrup.

Strong inferred patterns might later become candidate preferences, but explicit user statements remain stronger.

---

# 7. Priority / Authority Principle

Important doctrine:

> **What the user explicitly says outranks what the Forest inferred about them.**

Conceptual priority:

```text
Explicit current user instruction
        ↓
Explicit user correction
        ↓
Explicit user constraint / preference
        ↓
well-supported learned pattern
        ↓
Syrup inference
        ↓
weak inference
```

This is semantic authority, not necessarily a fixed numerical scoring formula.

---

# 8. Why Full User Context Should NOT Be Front-Loaded

Loading all User Context before every Task would create:

- unnecessary retrieval work
- prompt bloat
- irrelevant context
- repeated loading/unloading
- slower Trees and Clones
- larger hot context
- increased model evaluation cost

Example:

```text
User:
"Fix this Python indentation error."
```

The Forest should not need to retrieve food preferences, travel preferences, shopping budgets, or design tastes.

Therefore:

> **Relevant user context should shape reasoning when needed, but the full User Context should not be loaded before every Task.**

---

# 9. Context Trigger Index

Instead of front-loading all User Context, the Forest should maintain a **Context Trigger Index**.

The index contains small routing rules indicating when a category of User Context should be checked.

Examples:

```text
food / recipes / restaurants
→ dietary context

shopping / product recommendation
→ purchasing preferences

software / service recommendation
→ software preferences

email / communication
→ communication preferences and action policy

travel
→ travel preferences and constraints

design
→ design preferences
```

The trigger does **not** need to contain the actual preference or constraint.

Example:

```text
software recommendation
→ relevant User Context exists
```

not:

```text
software recommendation
→ user prefers X, Y, Z, A, B, C...
```

---

# 10. Keep Trigger Categories Broad

Do not create a separate top-level routing rule for every individual preference.

Bad:

```text
shoes → check context
jackets → check context
hats → check context
phones → check context
keyboards → check context
...
```

Preferred:

```text
shopping/recommendation
→ purchasing preferences

food
→ dietary context

software/services
→ software preferences

communication
→ communication preferences

design
→ design preferences

technical work
→ technical/workflow preferences
```

Hundreds of durable User Context records may still require only a small number of broad routing categories.

---

# 11. CHECK vs. MUST CHECK

Context triggers may have different strengths.

## CHECK

Useful personalization.

Example:

```text
software recommendation
→ CHECK software preferences
```

If retrieval fails, the Forest may be able to proceed cautiously depending on policy.

## MUST CHECK

Required before a relevant recommendation or action.

Examples:

```text
food recommendation
→ MUST CHECK dietary constraints

email.send
→ MUST CHECK communication/action policy
```

If required context cannot be retrieved, the Forest should not silently act as though no restriction exists.

A repeated user correction may strengthen a routing rule if the Forest has repeatedly failed to apply an important preference or constraint.

---

# 12. Cold / Warm / Hot Placement

The Context Trigger Index should **not normally be Hot model context**.

Preferred architecture:

```text
COLD
Durable User Context
preferences / constraints / corrections / current context
        ↓
WARM
Context Trigger Index
parsed / compiled / RAM-resident Forest-side routing
        ↓
Task arrives
        ↓
cheap relevance match
        ↓
HOT
only matched User Context
```

Doctrine:

> **Cold stores the truth. Warm decides whether it is relevant. Hot contains only what is relevant.**

---

# 13. Warm Routing Should Be Forest-Side

The model should not need to consciously skim trigger rules on every turn.

Preferred flow:

```text
Task
 ↓
Forest-side lightweight routing
 ↓
Warm Context Trigger Index
 ↓
relevant category?
   │
   ├── no
   │    ↓
   │  normal prompt
   │
   └── yes
        ↓
   retrieve matched User Context
        ↓
   prompt assembly
        ↓
   Tree / Clone reasoning
```

The Tree experiences continuity, but the actual routing is handled by Forest infrastructure.

This saves prompt tokens and avoids depending on the model to remember to ask for context.

---

# 14. Deterministic Routing Before AI Routing

The Context Trigger Index should use cheap deterministic or structural routing wherever practical.

Example Task signals:

```text
domain: software
intent: recommendation
action: choose
```

can route to:

```text
software-preferences
```

without an LLM call.

Doctrine:

> **Do the cheapest deterministic routing that works before involving AI.**

Smarter semantic routing can remain a fallback for ambiguous cases.

---

# 15. Partial Warmth / Layered Trigger Index

If the Context Trigger Index grows large, it can itself be layered.

Example:

```text
WARM CORE INDEX
├── food
├── shopping
├── software
├── communication
├── travel
├── technical
└── design
       ↓
secondary category index
       ↓
specific context records
```

This keeps the first routing layer extremely small even if the Forest eventually contains thousands of User Context records.

---

# 16. Context Route Stamp

The Forest should not repeatedly evaluate the same User Context routing decision for every internal reasoning step, tool call, terminal command, file read, retry, or test.

Introduce a small **Context Route Stamp**.

This is not another heavyweight global cache.

It is tiny Clone/session/Task-local ephemeral state recording that context routing has already been evaluated for the current meaningful input.

Example:

```text
context_route_stamp:
    input_generation: 43
    user_context_generation: 18
    matched:
      - preferences/software
      - preferences/purchasing
```

---

# 17. Route Stamp Behavior

Example:

```text
User:
"Fix this Python function."
        ↓
new meaningful input #42
        ↓
check Warm Context Trigger Index ONCE
        ↓
no relevant User Context
        ↓
record:
context_route_checked_for = 42
```

Then the Tree may:

```text
reason
inspect file
use terminal
run test
read tool result
edit file
run test again
```

without rechecking whether food, shopping, travel, or design context is relevant.

---

# 18. Route Stamp Invalidation

Core invariant:

> **Conversation changes invalidate context routing; execution steps do not.**

Should invalidate / re-evaluate when:

```text
new user message
new external event becomes meaningful Task input
Task meaning materially changes
User Context changes
relevant policy changes
```

Should NOT invalidate for:

```text
model reasoning step
tool call
tool result
terminal command
file read
retry
test run
Clone continuing the same work
```

---

# 19. User Context Generation

Introduce a monotonically increasing **User Context Generation** or equivalent source version.

Example:

```text
context_route_stamp:
    input_generation: 43
    user_context_generation: 17
```

If a new User Context item is added:

```text
current User Context generation = 18
```

the previous route decision becomes stale.

Conceptually:

```text
Can previous routing decision be reused?

same meaningful input?
        AND
same User Context generation?
        ↓
       YES
        ↓
reuse route decision

otherwise
        ↓
check Warm index again
```

This keeps invalidation cheap and deterministic.

---

# 20. Task-Sticky User Context

Some relevant User Context should remain available across related turns within a long-running Task.

Example:

```text
Task:
Bristlecone development

Relevant context:
- technical teaching preference
- Qubes environment
- free/open-source preference
- Forest engineering workflow rules
```

Rather than unloading and refetching this after every message, selected context may be **Task-Sticky** while:

- the Task remains the same
- the underlying User Context generation remains valid
- the context remains relevant
- policy allows it

Possible context lifetimes:

```text
TURN-STICKY
→ re-evaluate each meaningful input

TASK-STICKY
→ retain while Task remains active

CLONE-STICKY
→ retain while useful to this Clone

TREE CORE
→ tiny stable Tree identity/rules
```

This parallels the existing capability layering.

---

# 21. Route Stamp + Task-Sticky Interaction

Preferred flow:

```text
DURABLE USER CONTEXT
        ↓
User Context generation
        ↓
WARM CONTEXT TRIGGER INDEX
        ↓
new meaningful input
        ↓
CONTEXT ROUTE STAMP
"Have I already routed this input?"
        ↓
      yes ─────────────→ continue
        │
       no
        ↓
warm trigger lookup
        ↓
matched categories
        ↓
already Task-Sticky and still valid?
        │
     yes│             no
        ↓              ↓
    continue        retrieve
                       ↓
                      HOT
```

On many internal steps, context-routing cost should collapse to a trivial version/stamp comparison.

---

# 22. Hot Context Principle

Important Phase 14 doctrine:

> **Hot is for information the model needs now. Warm is for information the Forest needs to decide what the model needs now.**

This applies beyond User Context.

Likely Warm infrastructure includes:

- Context Trigger Index
- capability catalog and resolution structures
- Operational Learning index
- Leaf index
- Roots maps
- Clone records
- other derived routing metadata

Only selected relevant payloads become Hot.

---

# 23. User Context and Clones / Colonies

All Clones should not duplicate User Context.

Preferred:

```text
                 USER CONTEXT
                      │
               Trigger Index
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   Base Maple     Mail Clone     Code Clone
```

Each Clone routes and retrieves only the context needed for its Task.

Example:

```text
Maple-Mail
→ communication preferences
→ send/draft policies
→ privacy constraints
```

while:

```text
Maple-Code
→ technical preferences
→ software philosophy
→ environment context
```

The same authoritative User Context is shared without duplicating the records into each Clone.

---

# 24. User Context Is Shared; Activation Is Local

This mirrors the capability architecture.

```text
User Context records
→ shared durable Forest/user state

Context Trigger Index
→ shared derived Warm routing

Route Stamp
→ Clone/session/Task-local ephemeral state

Matched User Context
→ Clone/Task-specific Hot context
```

This is analogous to:

```text
shared capability
→ separate Clone activation
```

---

# 25. Preference Updates Should Update Routing

When a new relevant preference/constraint/correction is stored, the Forest should ensure the Context Trigger Index can discover it.

Example:

```text
New User Preference:
"When recommending clothing, usually stay under $100."
```

The durable record belongs under purchasing/clothing context.

If the current routing system lacks a suitable trigger/category, the derived trigger/index should be rebuilt or updated so future clothing/shopping recommendations route to the correct context.

The durable preference is authoritative.

The trigger is derived and disposable.

---

# 26. Context Trigger Index Is Derived State

Critical invariant:

> **The Context Trigger Index is not the User Context.**

If the index/cache disappears:

```text
User Context survives.
The Forest may temporarily rebuild routing metadata.
No preference, constraint, or correction is forgotten.
```

This follows the Phase 14 cache doctrine:

> **Caches are derived state, never authoritative state.**

---

# 27. Context Routing Should Not Become Another Tool Explosion

The system should avoid:

```text
hundreds of Clones
×
duplicated User Context
×
duplicated trigger lists
×
duplicated retrieval infrastructure
```

Instead:

```text
shared authoritative User Context
shared Warm indexes where valid
lightweight per-Clone Route Stamp
selected per-Task Hot context
```

This follows the Colony rule:

> **Clone count must not scale infrastructure count.**

---

# 28. Relationship to Operational Learning

Operational Learning can influence User Context routing.

Example:

```text
User repeatedly corrects:
"Please stop recommending subscription software first."
        ↓
User Correction
        ↓
Operational Learning notes repeated failure
        ↓
software recommendation trigger may become stronger
        ↓
software preferences reliably checked before ranking
```

Operational Learning and User Context remain separate, but they may inform one another.

---

# 29. Relationship to Spirit

Spirit should eventually govern deterministic policy around:

- MUST CHECK routing
- permissions to read protected User Context
- hard constraints
- protected preference data
- User Context generation/version updates
- concurrent durable changes from Clones
- Route Stamp invalidation when policy/source generations change

Core doctrine remains:

> **Trees decide what would be useful. Spirit decides what is allowed.**

---

# 30. Relationship to Cedar

Sensitive User Context may require Sap, Tar Sap, Cedar Oil, or Tree-specific permissions.

A derived Context Trigger Index must never bypass protections on the authoritative data.

A Tree/Clone may know:

```text
"relevant protected context exists"
```

without necessarily being permitted to read the protected content.

Protection inheritance must survive into:

- derived indexes
- context routing
- selected Hot context
- Syrup
- Operational Learning

---

# 31. Phase 14 Integration

The current Phase 14 Layered Hot Context roadmap should now explicitly include:

```text
Durable User Context foundation
        ↓
derived Context Trigger Index
        ↓
Warm routing
        ↓
Context Route Stamp
        ↓
Task-Sticky selected User Context
        ↓
Hot Context assembler
```

This work should integrate with:

- Forest Cache Coordinator
- Tree / Clone / Colony cache scopes
- Operational Learning indexes
- Layered Hot Context
- later Spirit permissions
- later Leaf Foliage
- later Syrup / Mycelium

---

# 32. Updated Phase 14 Cache / Context Hierarchy

```text
COLD / AUTHORITATIVE
│
├── User Context
├── Operational Learning
├── Leaves
└── Tree / Clone durable state
        ↓
WARM / DERIVED
│
├── Context Trigger Index
├── Operational Learning Index
├── capability-resolution cache
├── parsed-manifest cache
├── Leaf indexes
└── other routing/preparation metadata
        ↓
CLONE / TASK EPHEMERAL
│
├── Context Route Stamp
├── selected capability bindings
├── Task-Sticky context
└── current working state
        ↓
HOT
│
├── Base Tree Core
├── matched User Context only
├── relevant Operational Learning only
├── Workshop Core
├── Clone context
├── Task-Sticky Skills
├── relevant Leaves
└── current Task
        ↓
RUNTIME / INFERENCE
│
├── session
├── KV
├── native prefix cache
└── model execution state
```

---

# 33. Key Doctrines to Preserve

> **User Preference and User Correction are different concepts.**

> **User Constraints are distinct from Preferences.**

> **What the user explicitly says outranks what the Forest inferred about them.**

> **Explicit User Context is not Syrup.**

> **Relevant user context should shape reasoning when needed, but the full User Context should not be loaded before every Task.**

> **Trees carry access to context; the Forest routes context.**

> **Cold stores the truth. Warm decides whether it is relevant. Hot contains only what is relevant.**

> **Do the cheapest deterministic routing that works before involving AI.**

> **The Context Trigger Index is derived state, not authoritative User Context.**

> **Conversation changes invalidate context routing; execution steps do not.**

> **Hot is for information the model needs now. Warm is for information the Forest needs to decide what the model needs now.**

> **User Context should be available before it is needed, not loaded before every Task.**

> **Clone count must not scale User Context infrastructure count.**

---

# 34. Engineering Consequence Before 14.6F2

Do **not** install the previously drafted Operational Learning-only 14.6F2 unchanged.

The design has broadened.

The next implementation should account for a common durable Forest Learning / User Context foundation with distinct semantic categories, then build derived routing/index layers above authoritative records.

Before coding, preserve:

1. User Preference as first-class.
2. User Constraint as first-class.
3. User Correction as first-class.
4. Operational Learning as distinct.
5. Syrup as inferred/distilled personalization.
6. Context Trigger Index as derived Warm state.
7. Context Route Stamp as tiny Clone/session/Task-local state.
8. User Context Generation for invalidation.
9. Task-Sticky selected User Context.
10. Cold/Warm/Hot separation.
11. Clone/Colony compatibility.
12. Spirit/Cedar protection compatibility.

---

# 35. Current Design Summary

The Forest should feel as though its Trees know the user continuously without requiring every Tree or Clone to carry the user's entire history or preferences in every prompt.

The mechanism is:

```text
Remember durable context
        ↓
index it cheaply
        ↓
route only when relevant
        ↓
remember that routing was already checked
        ↓
keep relevant context sticky when useful
        ↓
place only what the model needs into Hot Context
```

This provides continuity, personalization, performance, and inspectability at the same time.
