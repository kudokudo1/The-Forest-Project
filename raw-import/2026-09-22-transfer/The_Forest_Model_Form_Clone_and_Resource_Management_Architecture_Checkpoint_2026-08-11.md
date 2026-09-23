# The Forest — Model Form, Clone, and Resource Management Architecture Checkpoint
**Date:** 2026-08-11  
**Status:** Design checkpoint / implementation planning  
**Primary phase:** 14.11 — Small / Big Model Escalation

## Purpose

This checkpoint records the development of the Forest's Small/Big Model Form architecture and the ideas that grew out of it: cross-form handoffs, Clone-local Model Form and Reasoning state, shared model residency, dynamic whole-Forest resource allocation, and a future AI-assisted but Spirit-governed Resource Management subsystem.

This discussion began with a narrow continuity question—how Small and Big versions of the same Tree should hand work to each other—and expanded into a broader architecture for allowing many Tree and Clone workloads to coexist efficiently on finite local hardware.

Core principles reinforced during this discussion:

> **A Tree is not its model.**

> **Trees decide what would be useful. Spirit decides what is allowed.**

> **Resource cost scales with active work, not retained Clone count.**

New principle:

> **Compute follows active demand, not Tree ownership.**

---

# 1. Starting point: Phase 14.11

Phase 14.11 began as Small / Big Model Escalation for Bristlecone Pine.

The intended control axes are independent:

```text
BRISTLECONE
  ├── REASONING: Light / Normal / Deep
  ├── WORKSHOP: task-specific capability boundary
  └── MODEL FORM: Small / Big
```

Valid combinations:

```text
Small + Light
Small + Normal
Small + Deep

Big + Light
Big + Normal
Big + Deep
```

Important invariant:

> **Deep does not mean Big, and Big does not mean Deep.**

Reasoning controls how deeply the selected model reasons. Model Form controls which capability tier/model binding is selected.

The proposed Forest-level control values are:

```text
AUTO
SMALL
BIG
```

But `AUTO` is policy, not a runtime form. Every meaningful turn must eventually resolve to either:

```text
SMALL
or
BIG
```

The runtime should never receive `AUTO` as if it were a model.

---

# 2. Runtime-neutral Tree identity

Forest logic should not permanently encode vendor model names into Tree identity.

Conceptually:

```text
Bristlecone Small → bristlecone-small
Bristlecone Big   → bristlecone-big
```

A separate registry/runtime layer binds those Forest concepts to concrete models.

Current staging direction:

```text
Bristlecone Small → current Qwen Small runtime
Bristlecone Big   → Mistral Small 4 candidate
```

These bindings may change later without changing Bristlecone's identity.

This preserves:

> **A Tree is not its model.**

---

# 3. Current Big-model staging status

The candidate Big Bristlecone model has been downloaded and verified:

```text
Repository:
mistralai/Mistral-Small-4-119B-2603-NVFP4

Hugging Face download:
70.8 GB

Local disk footprint:
~66 GiB

Weight shards:
13 / 13 present

Verification:
23 repository files checked
all checksums matched

Cherry-AI free space after staging:
~53 GiB
```

Current status:

```text
✅ downloaded
✅ reconstructed
✅ 13/13 weight shards present
✅ checksums verified
✅ staged locally

❌ not loaded
❌ not connected to Hermes
❌ not activated as Bristlecone Big

✅ current Small Bristlecone remains untouched
```

The architecture is intentionally being built before the Big runtime is activated.

---

# 4. Development step: rejecting runtime-session transfer

The first continuity question was essentially:

> When Small switches to Big, how does Big know where Small left off?

One possible direction would have been to transfer runtime session internals.

That was rejected because different model/runtime combinations may have incompatible:

- KV caches,
- tokenization,
- architecture-specific state,
- session formats,
- inference engine assumptions,
- internal context representation.

Trying to transform:

```text
Qwen runtime state
      ↓
conversion
      ↓
Mistral runtime state
```

would be fragile and may not even be technically meaningful.

This produced a stronger rule:

> **Model Form continuity belongs to Forest state, not runtime session internals.**

---

# 5. Development step: Model Form Handoff

The user proposed a simpler and better continuity mechanism:

> Small and Big leave a small note for the other version explaining where the work stopped and why the switch happened.

This became the proposed **Model Form Handoff**.

Conceptually:

```text
Small Bristlecone
        ↓
writes compact handoff
        ↓
Big Bristlecone
        ↓
reads handoff
        ↓
retrieves deeper context only if needed
```

And in reverse:

```text
Big Bristlecone
        ↓
writes compact handoff
        ↓
Small Bristlecone
        ↓
continues the same Tree task
```

A handoff might contain:

```yaml
tree: bristlecone
task_id: forest-14.11

from_form: small
to_form: big

why_switched:
  "The task expanded into deeper architecture work."

where_we_left_off:
  "Defining Model Form continuity and resource behavior."

important_decisions:
  - Small and Big are the same Tree.
  - Reasoning and Model Form are independent.
  - Explicit Big must not silently downgrade.

unresolved:
  - finish Model Form integration
  - define resource behavior

relevant_sources:
  - task-state:forest-14.11
  - leaf:model-form-contract
  - conversation:current
```

The handoff is a **navigation note**, not a replacement for authoritative Task state.

The incoming form may still retrieve:

- Task state,
- Hot Context,
- Leaves,
- Roots,
- project files,
- conversation history,
- Operational Learning,
- other relevant Forest memory.

Key handoff rule:

> **The runtime changes. Forest leaves the next Model Form a note.**

---

# 6. Handoff versus runtime recovery

A Model Form transition is not the same as stale-session recovery.

```text
Small → Big
= Model Form transition
= handoff ✅
```

```text
Big → Small
= Model Form transition
= handoff ✅
```

But:

```text
Small runtime session A
→ stale
→ Small runtime session B
= same Model Form
= handoff ❌
```

Stale-session recovery is an execution repair, not a new semantic transition.

---

# 7. Development step: inspecting the certified 14.10 turn path

The existing 14.10 reasoning path was inspected before planning edits.

Current behavior:

```text
meaningful user turn
        ↓
resolve reasoning exactly once
        ↓
resolved_reasoning_mode
        ↓
prepare runtime/session
        ↓
send turn
        ↓
stale session?
        ↓
create replacement
        ↓
retry using SAME resolved_reasoning_mode
```

This became the template for Model Form.

Desired future behavior:

```text
meaningful user turn
        ↓
resolve reasoning exactly once
resolve Model Form exactly once
        ↓
freeze:
  resolved_reasoning_mode
  resolved_model_form
        ↓
prepare correct runtime/model session
        ↓
send
        ↓
stale recovery?
        ↓
reuse BOTH frozen values
```

No rerouting should happen during a retry.

If the turn began as:

```text
Big + Deep
```

then stale recovery must still be:

```text
Big + Deep
```

not Small + Deep, Big + Normal, or any other combination.

---

# 8. Why Model Form belongs above the runtime adapter

The current architecture delegates runtime selection from TaskSessionManager through a runtime adapter factory.

The generic runtime contract handles operations such as:

```text
create_session(...)
send_turn(...)
```

`send_turn()` already receives `reasoning_mode`.

That makes sense because Reasoning changes **how the selected model executes**.

Model Form is different: it helps determine **which model/runtime is selected before a session exists**.

Therefore the cleaner architecture is:

```text
resolved_model_form
        ↓
runtime/model binding selection
        ↓
ensure correct session
        ↓
send_turn(
  reasoning_mode=resolved_reasoning_mode
)
```

rather than forcing every runtime adapter to understand Forest values such as `AUTO`, `SMALL`, and `BIG`.

---

# 9. Development step: Clone independence

The design changed significantly when the user asked whether all Clones of a Tree should jump to Big/Deep when the Main Tree does.

Example:

```text
Maple Photo Clone
organizing a folder with many photos
Small + Light

Main Maple
later asked to generate a 1080p 35-second clip
Big + Deep
```

The Photo Clone should **not** jump to Big + Deep just because Main Maple does.

This produced a major invariant:

> **Model Form and Reasoning belong to an execution context, not to the Tree as a whole.**

A single Colony may therefore look like:

```text
MAPLE COLONY

Main Maple
└── video generation
    Big + Deep

Photo Clone
└── photo organization
    Small + Light

Document Clone
└── rename/sort files
    Small + Normal

Code Clone
└── complex code review
    Big + Normal
```

This should be normal behavior, not an edge case.

---

# 10. Tree defaults versus execution-context state

A useful hierarchy is:

```text
TREE DEFAULT
    ↓ seeds
EXECUTION CONTEXT
    ↓ may contain
LOCAL OVERRIDES
```

Example:

```text
Maple Tree default:
Model Form = Auto
Reasoning = Normal
```

A Photo Clone may later be pinned:

```text
Photo Clone:
Small + Light
```

Main Maple may later become:

```text
Main Maple:
Big + Deep
```

The Photo Clone remains unchanged.

This gives the rule:

> **Tree default ≠ live broadcast.**

Tree defaults should primarily seed new contexts. Existing work should not be silently rewritten.

---

# 11. Exact-turn, temporary, sticky, and baseline scope

The same isolation rule applies to control state.

Suggested hierarchy:

```text
TREE DEFAULT
    ↓
CONTEXT BASELINE / PIN
    ↓
CONTEXT TEMPORARY OVERRIDE
    ↓
EXACT-TURN OVERRIDE
```

Mutable live state should belong to the execution context.

Example:

```text
Main Maple:
baseline = Auto + Normal
temporary = Big + Deep

Photo Clone:
baseline = Small + Light
temporary = None
```

Main Maple's temporary state does not affect the Photo Clone.

Likewise, temporary leases must be counted locally.

If Main Maple is set to:

```text
Deep for the next 5 meaningful turns
```

only meaningful turns handled by Main Maple decrement that lease.

Photo Clone turns do not count against it.

---

# 12. Broadcasts should be deliberate

Default:

```text
"Maple, go Big."
→ current Main Maple context only
```

```text
"Use Deep for this task."
→ current execution context only
```

```text
"Set this Clone to Small + Light."
→ that Clone only
```

Possible future deliberate broadcasts:

```text
"Set every Maple Clone to Small."

"Make Big the default for future Maple work."

"Set the whole Maple Colony to Normal reasoning."
```

Broadcasts should be explicit.

Temporary state especially should never spread implicitly across a Colony.

---

# 13. Clone-local Model Form Handoffs

Handoffs belong to the context that actually switches.

```text
Main Maple:
Small → Big
→ handoff ✅

Photo Clone:
Small → Small
→ no handoff
```

If the Photo Clone later changes:

```text
Photo Clone:
Small → Big
→ its own handoff ✅
```

This reinforces:

> **Clones may share durable Tree knowledge without sharing mutable live routing/control state.**

---

# 14. Shared model weights, separate execution state

If two contexts both use the same Big model, the runtime should ideally avoid loading duplicate immutable weights.

Conceptually:

```text
                 Big model weights
                       │
           ┌───────────┴───────────┐
           ↓                       ↓
      Main Maple                Clone C
      own context               own context
      own KV/session            own KV/session
      own controls              own controls
```

Shared weights do **not** imply:

- shared session,
- shared KV cache,
- shared reasoning state,
- shared temporary lease,
- shared Model Form state,
- shared handoff.

This matters because Big models may consume tens of gigabytes.

---

# 15. Development step: dynamic whole-Forest resource allocation

The next idea was inspired by systems such as Qubes OS and power-management/solar systems:

> When the user suddenly needs more power, can Forest automatically scale back unimportant/background work and reallocate that power, then restore it when demand falls?

Initial concept:

```text
USER DEMAND SPIKES
        ↓
Forest Resource Governor
        ↓
reduce / pause low-priority work
        ↓
unload dormant models
        ↓
pause background Clones
        ↓
defer indexing
        ↓
release expendable caches
        ↓
give foreground work more resources
```

Recovery:

```text
foreground demand ends
        ↓
release resources
        ↓
resume background work
        ↓
gradually restore normal operation
```

This became a broader Forest Resource Management direction.

---

# 16. Big availability becomes resource-aware

Earlier behavior:

```text
Auto wants Big
→ Big unavailable
→ Small fallback allowed

User explicitly requests Big
→ Big unavailable
→ report Big unavailable
```

Improved behavior:

```text
BIG REQUEST
     ↓
Is Big immediately available?
     │
   YES
     ↓
launch Big

     NO
     ↓
ask Resource Management:
"Can enough resources be safely reclaimed?"
     ↓
pause/deprioritize permitted work
unload expendable resources
     ↓
Enough now?
   │       │
  YES      NO
   ↓       ↓
 Big    fallback policy
```

Core rule:

> **Automatic escalation may degrade gracefully. Explicit escalation must not silently downgrade.**

Explicit Big:

```text
reclaim safe resources
→ attempt Big
→ if still impossible:
  report Big unavailable
```

Auto Big:

```text
reclaim only within Auto's allowed budget
→ if still unavailable:
  continue Small
  record that escalation was resource-constrained
```

---

# 17. Intelligence control is not resource control

The Maple example made another distinction necessary.

```text
INTELLIGENCE CONTROL
- Model Form
- Reasoning
- Workshops
- context

            ≠

RESOURCE CONTROL
- CPU
- RAM
- GPU
- scheduling priority
- runtime residency
- cache allocation
- bandwidth
```

If Main Maple is Big + Deep and the Photo Clone is Small + Light, resource pressure should not rewrite the Photo Clone into another intelligence state.

Instead, Forest may:

- slow it,
- reduce CPU share,
- defer it,
- checkpoint it,
- pause it,
- resume it later.

The Photo Clone remains Small + Light.

New invariant:

> **Resource pressure should affect scheduling/reclamation before silently altering a Clone's requested intelligence state.**

---

# 18. Development step: one larger Resource Management System

The next design question was whether the intelligent resource logic should be:

1. a separate AI/Tree-like subsystem, or
2. another tool inside a larger, Spirit-heavy resource system.

The preferred architecture is **one umbrella Forest Resource Management system with several layers**:

```text
                 FOREST RESOURCE MANAGEMENT
                           │
          ┌────────────────┴────────────────┐
          │                                 │
 RESOURCE STEWARD                    RESOURCE GOVERNOR
 intelligent planner                deterministic authority
 "What should we do?"               "What are we allowed to do?"
          │                                 │
          └───────────────┬─────────────────┘
                          ↓
                   RESOURCE SCHEDULER
                          ↓
             constrained execution adapters
                          ↓
      ┌───────────┬───────────┬──────────────┐
      ↓           ↓           ↓              ↓
   Models       Clones     Workshops       Qubes
```

This is one system with separate responsibilities.

---

# 19. Resource Steward

The **Resource Steward** is the intelligent planning layer.

It understands what Forest workloads mean.

Example:

```text
Main Maple
1080p 35-second video task
Big + Deep
foreground
user waiting

Photo Clone
sorting thousands of old photos
Small + Light
background

Bristlecone Clone
optional repository analysis
Small + Normal
background

Maple indexing
maintenance
non-interactive
```

The Steward may infer:

```text
Video:
high demand
high priority
latency-sensitive

Photo organization:
background
low urgency
safe to slow

Repository analysis:
optional
safe to pause

Indexing:
deferrable
```

It then proposes a plan such as:

```text
- prioritize Main Maple
- pause deep indexing
- reduce Photo Clone scheduling
- suspend optional Bristlecone Clone
- unload unused model
- prepare GPU/RAM
```

This is where AI is useful: process metrics alone do not always reveal which task matters most.

---

# 20. Resource Governor

The **Resource Governor** is the deterministic authority layer.

It asks:

> Is this action permitted, safe, and within policy?

Example:

```text
Steward:
"Pause Photo Clone."

Governor checks:
- is it pausable?
- is it user-pinned?
- is it protected?
- can it checkpoint?
- would data be lost?
- is this action permitted?
```

Then:

```text
APPROVED
```

or:

```text
DENIED
```

Example:

```text
Steward:
"Stop Cedar's active protected operation."

Governor:
DENIED
```

The Governor is where Spirit remains authoritative.

---

# 21. Resource Scheduler

The **Resource Scheduler** translates approved policy into allocation mechanics.

Example:

```text
Governor:
"Approved: reclaim 12 GB from low-priority work."
```

Scheduler may choose:

```text
1. release expendable cache
2. unload dormant model
3. pause indexing
4. checkpoint background Clone
5. reduce background allocation
```

Clean separation:

```text
Steward
= WHAT SHOULD happen

Governor
= MAY IT happen

Scheduler
= HOW should it happen

Adapters
= DO it
```

This is safer and easier to test than giving one AI broad control.

---

# 22. Resource Adapters

Future constrained adapters may include:

```text
Model runtime adapter
- load/unload model
- query residency
- query memory demand

Clone adapter
- pause
- resume
- checkpoint
- query interruptibility

Linux/process adapter
- resource usage
- scheduling priority
- process state

Cache adapter
- release expendable caches

GPU adapter
- availability / workload admission

Qubes adapter
- approved memory changes
- approved vCPU changes
- approved qube start/stop
```

No Tree should receive unrestricted dom0 or host shell access simply because it requested more power.

---

# 23. Why the Resource Steward should not initially be a normal Tree

Resource Management must arbitrate between Trees.

If Maple owned it, Maple could favor Maple.
If Bristlecone owned it, Bristlecone could favor Bristlecone.

Therefore it belongs to Forest infrastructure:

```text
THE FOREST
│
├── Trees / Colonies
│   ├── Cherry
│   ├── Maple
│   ├── Bristlecone
│   ├── Cedar
│   └── ...
│
├── Spirit
│
├── Resource Management
│   ├── Resource Steward
│   ├── Resource Governor
│   ├── Resource Scheduler
│   └── Resource Adapters
│
├── Mycelium
├── Leaf Foliage
└── Soil / security boundaries
```

Trees can request resources.
No Tree owns the allocator.

---

# 24. Spirit and Cedar

Spirit remains the permission/policy authority.

Trees may request:

```text
"I need Big."
"I could use more RAM."
"This task is foreground."
"This Clone is safe to pause."
```

The Steward may recommend.
The Governor/Spirit authorizes.

Cedar can eventually impose constraints such as:

```text
Never suspend this protected workload.
Never move this task outside its qube.
Never expose this protected memory.
Never reduce this protected minimum.
```

The intelligent Steward cannot reason around those rules.

---

# 25. Qubes-aware resource control

Forest resource control can operate at two layers:

```text
FOREST / RUNTIME LAYER
│
├── unload model
├── release cache
├── pause Clone
├── defer indexing
├── reduce preloads
└── stop optional background work

        ↓

QUBES / HOST LAYER
│
├── memory allocation
├── vCPU allocation
├── qube start/stop
└── host scheduling policy
```

Preferred path:

```text
Tree
"I need more resources."
        ↓
Resource Steward
proposes
        ↓
Spirit / Governor
authorizes
        ↓
Resource Scheduler
chooses actions
        ↓
narrow Qubes adapter
        ↓
dom0 performs only pre-authorized operations
```

This preserves Qubes isolation.

---

# 26. Priority classes and resource budgets

Possible future priority classes:

```text
PROTECTED / FOREGROUND
- active user task
- security-critical Cedar operation
- explicitly pinned workload

HIGH
- active Big Model Form
- high-demand Workshop
- interactive vision

NORMAL
- other active Trees
- retrieval/indexing needed by active work

LOW
- background Clones
- embeddings
- Leaf maintenance
- training-data organization

IDLE / DEFERRABLE
- deep indexing
- archive maintenance
- optional analysis
- model preloading
```

Possible reclamation budgets:

```text
USER EXPLICIT
"Go Big."
Budget: HIGH

AUTO ESCALATION
Forest decides Big would help.
Budget: MODERATE

BACKGROUND WORK
Budget: LOW
```

This lets explicit user intent reclaim more resources than an automatic optimization.

---

# 27. Resource shedding stages

A gradual pressure model is preferable to binary on/off behavior:

```text
NORMAL
Everything runs normally.

PRESSURE 1
Delay optional background work.

PRESSURE 2
Pause background Clones / low-priority indexing.

PRESSURE 3
Unload dormant models / expendable caches.

PRESSURE 4
Concentrate resources on foreground work.

RECOVERY
Gradually restore suspended work.
```

The system should use:

- hysteresis,
- cooldowns,
- minimum residency windows,
- delayed recovery,
- pressure thresholds,

to prevent resource thrashing.

Bad pattern to avoid:

```text
Big loads
background stops
Big pauses
background restarts
Big loads again
background stops again
```

---

# 28. Retained Clones should be cheap

Desired idle Clone behavior:

```text
Clone exists
but idle
        ↓
durable identity/state retained
no active model
minimal memory
almost no compute
```

When work arrives:

```text
Resource Management allocates runtime
        ↓
Clone wakes
```

This makes it practical for a Forest to retain many Clones without paying full runtime cost for each one.

---

# 29. Compute follows active demand, not Tree ownership

New principle:

> **Compute follows active demand, not Tree ownership.**

Examples:

```text
A Maple Clone has the most important foreground task
→ the Clone gets the power.
```

```text
Main Bristlecone is idle but a Bristlecone Clone needs Big
→ the Clone may receive Big.
```

```text
Main Maple needs Big + Deep
Photo Clone is background Small + Light
→ Main Maple gets priority
→ Photo Clone stays Small + Light but may slow/pause.
```

```text
Cedar has a protected operation
→ protected resource minimum remains protected.
```

The resource-allocation unit is the active execution context/workload, not the Tree name.

---

# 30. Predictive Resource Steward

Later, the Steward can learn workload patterns:

```text
"When the user asks Maple for this kind of video task,
it usually needs high RAM/GPU and several minutes."

"Photo organization can safely run in the background."

"Bristlecone indexing is safe to defer."

"Cherry normally uses little compute unless Big or Deep is selected."
```

Then it can prepare resources before contention:

```text
User:
"Maple, make the clip."

        ↓
Steward predicts high demand

        ↓
before Big loads:
- delay indexing
- checkpoint background Clone
- preserve Cedar minimum
- release expendable cache
- prepare GPU/RAM

        ↓
Maple Big starts cleanly
```

This gives the Forest semantic resource awareness, not just process monitoring.

---

# 31. What can be implemented now

The answer to "can this all be implemented today?" is:

> **The foundation can and should be built now. The entire autonomous Resource Management system should not be completed inside 14.11.**

Build now:

```text
Model Form contract
execution-context IDs/scope
Clone-local control rules
ResourceRequest
ResourcePriority
ResourceBudget
ResourceAvailability
Governor interface
Scheduler interface
Model Form handoff contract
fake/deterministic certification
```

An initial Resource Management response may be only:

```text
AVAILABLE
UNAVAILABLE
```

Later it can grow to:

```text
AVAILABLE
RECLAIMABLE
RECLAIMING
DEFERRED
DENIED
```

without changing Tree-facing semantics.

---

# 32. What can come soon after

Once Model Form and Clone execution contexts are stable:

```text
- unload unused models
- defer indexing
- stop preloading
- release expendable caches
- pause checkpointable background Clones
- resume background Clones
- reduce background scheduling priority
- query model residency
```

These are useful Forest-local improvements that do not require broad dom0 control.

---

# 33. What should wait

## Qubes-level Resource Adapter

Wait until:

- Spirit permissions are mature,
- narrow qrexec interfaces are designed,
- resource actions are auditable,
- rollback behavior exists,
- no broad dom0 shell is needed.

## Highly autonomous Resource Steward

Wait until:

- Governor policy is trustworthy,
- Scheduler behavior is tested,
- resource metadata is available,
- Clones can reliably pause/resume,
- model residency can be observed,
- telemetry is reliable.

The Steward can become highly autonomous later while still remaining advisory rather than authoritative.

---

# 34. Revised Phase 14.11 roadmap

```text
PHASE 14.11 — SMALL / BIG MODEL ESCALATION

14.11A — Canonical Model Form Contract
          + execution-context scope

14.11B — Model Form Control State
          + Tree defaults
          + context-local pins
          + context-local temporary state
          + exact-turn overrides
          + Clone isolation

14.11C — Runtime-Neutral Model Registry

14.11D — Turn Resolution + Freeze
          + resolve per execution context
          + freeze Reasoning and Model Form once
          + context-local lease decrement

14.11E — Model Form Handoff + Continuity
          + Small ↔ Big handoff
          + retrieval pointers
          + same Tree identity
          + no runtime-state conversion
          + Clone-local handoffs

14.11F — Resource Request + Governor Contract
          + availability
          + resource budget
          + explicit/Auto fallback
          + future Resource Management hook

14.11G — Automatic Escalation Router

14.11H — Colony Runtime / Shared-Weight Semantics
          + heterogeneous Clone Model Forms
          + heterogeneous Reasoning
          + shared immutable weights
          + independent sessions/KV/control state

14.11I — Fake-Adapter Certification

14.11J — Real Small Runtime Certification

14.11K — Real Big Runtime Boundary Test

14.11L — Model Form Benchmark
```

The complete Resource Management system should later receive its own larger phase rather than making 14.11 an operating-system scheduler project.

---

# 35. Why the Resource hook belongs in 14.11 now

14.11 should not hard-code today's machine assumptions.

Instead, Big escalation should ask a stable interface, conceptually:

```python
request_resources(
    tree_id="bristlecone",
    context_id="main",
    model_form="big",
    priority="foreground",
)
```

Today:

```text
AVAILABLE
UNAVAILABLE
```

Later:

```text
AVAILABLE
RECLAIMABLE
RECLAIMING
DEFERRED
DENIED
```

This lets the future Resource Steward/Governor/Scheduler plug in without rewriting Small/Big semantics.

---

# 36. Certification case: Maple Main versus Photo Clone

This user example should become a formal test.

Setup:

```text
Photo Clone:
Model Form = Small
Reasoning = Light
Task = organize photo folder
Priority = Background

Main Maple:
Model Form = Auto
Reasoning = Normal
Task = interactive
```

Then Main Maple receives a demanding video task.

Expected:

```text
Main Maple:
Big + Deep

Photo Clone:
Small + Light
```

PASS requires:

```text
✓ Main becomes Big + Deep
✓ Photo Clone remains Small + Light
✓ Main temporary turns do not decrement Clone lease
✓ Clone turns do not decrement Main lease
✓ no sticky-state leakage
✓ no exact-turn leakage
✓ Main transition gets its own handoff
✓ Photo Clone gets no handoff
✓ resource system may slow/pause Photo Clone
✓ resource system does not silently alter Photo Clone intelligence
✓ shared Maple identity remains intact
```

---

# 37. Certification case: stale recovery

Setup:

```text
Main Maple:
Big + Deep

runtime session becomes stale
```

Expected:

```text
replacement Big runtime session
same Deep reasoning
same resolved Big Model Form
no Model Form Handoff
```

PASS requires:

```text
resolved_reasoning_mode unchanged
resolved_model_form unchanged
same execution context
same task identity
one-shot recovery semantics preserved
```

---

# 38. Certification case: explicit Big unavailable

```text
User:
"Go Big."
```

Expected:

```text
check immediate availability

if unavailable:
attempt allowed safe reclamation

if still unavailable:
report Big unavailable
```

PASS requires:

```text
no silent downgrade
no unauthorized host action
no arbitrary Clone intelligence change
no violation of protected Cedar workloads
```

---

# 39. Certification case: Auto Big unavailable

```text
Auto determines Big would help.
```

Expected:

```text
request moderate reclamation budget
attempt Big if permitted

if still unavailable:
continue Small
record constrained escalation
```

PASS requires:

```text
graceful fallback
no deception
no excessive disruption of active work
```

---

# 40. Certification case: shared Big weights

Setup:

```text
Main Maple = Big
Maple Clone C = Big
```

Desired where the runtime supports it:

```text
one immutable Big weight residency
two independent execution contexts
two independent sessions/KV
two independent Reasoning states
two independent temporary/sticky states
```

Shared weights must not merge identity or live state.

---

# 41. Development history summary

The idea developed in this order:

## Step 1 — Small/Big continuity
Question:
```text
How does Big know where Small left off?
```
Rejected:
```text
transfer opaque runtime state
```
Chosen:
```text
Model Form Handoff
```

## Step 2 — Big unavailable behavior
Initial:
```text
fallback/error
```
Expanded:
```text
first ask if Forest can safely reclaim resources
```

## Step 3 — whole-Forest dynamic allocation
Question:
```text
Can Forest scale back background work when demand spikes?
```
Result:
```text
Resource Governor concept
```

## Step 4 — Clone independence
Question:
```text
Does Main Maple Big + Deep force every Maple Clone Big + Deep?
```
Answer:
```text
No.
```
Result:
```text
Model Form and Reasoning become execution-context local.
```

## Step 5 — layered Resource Management
Question:
```text
Should AI resource planning be separate or part of the same system?
```
Result:
```text
one umbrella:
Resource Steward
Resource Governor
Resource Scheduler
Resource Adapters
```

## Step 6 — implementation timing
Question:
```text
Can this all be built today?
```
Result:
```text
Build contracts/foundation now.
Grow real control progressively.
Do not explode 14.11 scope.
```

---

# 42. Candidate architecture invariants

> **A Tree may have many simultaneous Model Forms.**

> **A Tree may have many simultaneous Reasoning levels.**

> **Model Form and Reasoning belong to execution contexts, not the Tree globally.**

> **Main Tree control changes do not implicitly propagate to Clones.**

> **Exact-turn overrides are execution-context local.**

> **Temporary overrides are execution-context local.**

> **Temporary leases count only meaningful turns handled by that execution context.**

> **Sticky/context pins are local unless deliberately broadcast.**

> **Tree defaults seed contexts; they are not live broadcasts into running work.**

> **Model Form Handoffs belong to the execution context that actually switches.**

> **Shared Tree knowledge does not imply shared mutable control state.**

> **Shared model weights do not imply shared session, context, Reasoning, or Model Form control.**

> **Model Form continuity belongs to Forest state, not runtime session internals.**

> **A handoff is a navigation aid, not authoritative Task state.**

> **Explicit Big must not silently downgrade to Small.**

> **Auto escalation may degrade gracefully under resource constraints.**

> **Resource pressure should affect scheduling/reclamation before silently altering intelligence state.**

> **Trees may request resources; Trees do not directly control unrestricted host policy.**

> **The Resource Steward recommends; the Resource Governor authorizes.**

> **The Resource Scheduler implements only approved policy.**

> **Qubes host control remains behind narrow pre-authorized adapters.**

> **Retained Clones should remain cheap when idle.**

> **Resource cost scales with active work, not retained Clone count.**

> **Compute follows active demand, not Tree ownership.**

> **The Forest should concentrate power where the user currently needs it, then gradually restore the background Forest when demand passes.**

---

# 43. Immediate next technical work

At this checkpoint, no new 14.11 source change has yet been certified.

Recommended sequence:

```text
1. Finish inspecting current runtime factory/registry behavior.
2. Freeze 14.11A contract.
3. Create timestamped backup before source mutation.
4. Add the smallest isolated Model Form contract/module.
5. Test it independently.
6. Add execution-context scoping.
7. Add Model Form control state.
8. Add runtime-neutral model registry.
9. Integrate per-turn resolution/freeze.
10. Add Model Form Handoff.
11. Add Resource Request/Governor interface.
12. Add fake certification.
13. Certify current Small runtime.
14. Only later run the Big runtime boundary test.
```

The certified 14.10 reasoning path should remain stable while these layers are added incrementally.

---

# 44. Final architecture snapshot

```text
THE FOREST
│
├── Spirit
│   └── deterministic authority
│
├── Trees / Colonies
│   ├── Cherry
│   ├── Maple
│   │   ├── Main Maple      Big + Deep
│   │   ├── Photo Clone     Small + Light
│   │   └── Code Clone      Big + Normal
│   ├── Bristlecone
│   ├── Cedar
│   └── ...
│
├── Model Form Control
│   ├── Tree defaults
│   ├── context baselines
│   ├── temporary overrides
│   ├── exact-turn overrides
│   └── Model Form Handoffs
│
├── Reasoning Control
│   ├── Light
│   ├── Normal
│   └── Deep
│
├── Runtime-Neutral Model Registry
│   ├── Small bindings
│   └── Big bindings
│
├── Forest Resource Management
│   ├── Resource Steward
│   │   └── intelligent planning/prediction
│   ├── Resource Governor
│   │   └── Spirit-governed policy authority
│   ├── Resource Scheduler
│   │   └── deterministic allocation mechanics
│   └── Resource Adapters
│       ├── model runtimes
│       ├── Clones
│       ├── Linux/processes
│       ├── caches
│       ├── GPU
│       └── Qubes
│
├── Mycelium
├── Leaf Foliage
├── Roots / provenance
└── Soil / Qubes security boundaries
```

---

# 45. Short version

The design began with:

```text
"How does Small hand off to Big?"
```

and developed into:

```text
Tree continuity
      +
Clone-local intelligence state
      +
Small/Big escalation
      +
Reasoning isolation
      +
shared model weights
      +
resource-aware scheduling
      +
AI-assisted planning
      +
Spirit-controlled authority
      +
Qubes-safe execution
```

These systems are related but intentionally not collapsed into each other:

```text
Model Form
= capability tier/model choice

Reasoning
= how deeply that selected model reasons

Execution context
= where mutable control state belongs

Resource Management
= how much machine power the workload receives

Spirit/Governor
= what resource actions are allowed

Resource Steward
= intelligent planning/recommendation

Scheduler/Adapters
= safe implementation
```

This gives The Forest a path toward highly automated, AI-aware resource management while preserving deterministic authority, Clone independence, Qubes isolation, and user intent.

---

# End of checkpoint
