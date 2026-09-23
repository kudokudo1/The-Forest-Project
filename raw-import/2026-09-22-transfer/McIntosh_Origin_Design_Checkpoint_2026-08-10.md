---
title: "McIntosh — Origin Design Checkpoint"
project: "The Forest"
tree: "McIntosh"
role: "Software Engineer / Digital Technician"
status: "Early design checkpoint — origin concepts agreed, implementation not frozen"
date: "2026-08-10"
tags:
  - forest
  - mcintosh
  - coding
  - troubleshooting
  - software-engineering
  - digital-technician
  - observation
  - privacy
  - tree-design
---

# McIntosh — Origin Design Checkpoint

## Status

This document captures the **origin and starting design direction** for McIntosh.

The concepts here are architectural rather than implementation-frozen. Exact schemas, APIs, permission formats, capture providers, model choices, and UI details can change as The Forest develops.

---

# 1. Core Identity

> **McIntosh builds, diagnoses, repairs, and maintains the user's digital world.**

McIntosh is intended to be more than a Coding Tree.

Its broader role is:

> **Software Engineer & Digital Technician**

McIntosh should serve both ordinary users and serious developers/power users.

It should scale naturally from:

> "Why won't my game launch?"

to:

> "Trace this failure across these services, identify the responsible code path, patch the repository, run tests, and verify the regression is fixed."

---

# 2. Relationship to Other Trees

## Bristlecone Pine

**Bristlecone Pine is the Treewright.**

Bristlecone focuses on:

- designing Trees and AI systems
- Forest architecture
- model design and evaluation
- difficult cross-system reasoning
- training/customization strategy
- architecture review
- creating and maintaining Forest system components

Conceptually:

```text
Bristlecone:
"How should this be designed?"
"How should this Tree work?"
"What architecture should we use?"

McIntosh:
"Build it."
"Test it."
"Debug it."
"Maintain it."
```

## Maple

Maple remains the Forest's semantic steward/cartographer.

Maple focuses on:

- files and their meaning
- Leaf Foliage
- Leaf Litter
- Syrup
- Mycelium
- historical continuity
- semantic relationships
- old fixes and failed approaches
- user preferences and recurring patterns
- personal knowledge and media history

McIntosh may manipulate files during engineering work, but Maple remains responsible for understanding their broader meaning, history, provenance, and relationships.

Useful collaboration:

```text
McIntosh:
"Have we encountered this problem before?"

Maple / Forest history:
"Yes. Fix A failed. Fix B worked."

McIntosh:
avoids repeating Fix A
and begins from verified experience
```

## Cedar

Cedar remains the security specialist.

McIntosh may write security-conscious code and detect suspicious behavior, but Cedar retains the dedicated security role.

## Spirit

Spirit is the deterministic permission, state, and policy authority.

McIntosh may interpret user intent, request permissions, recommend policy changes, and perform semantic diagnosis.

Spirit should:

- store durable permissions
- enforce observation boundaries
- enforce control boundaries
- maintain deterministic state
- prevent McIntosh from reasoning around permissions

> **McIntosh interprets. Spirit enforces.**

---

# 3. McIntosh Responsibilities

## Software Engineering

McIntosh should be highly capable at:

- writing code
- reviewing code
- debugging
- refactoring
- testing
- repository understanding
- build systems
- package management
- APIs
- databases
- plugins/extensions
- automation
- scripting
- developer tooling
- performance profiling
- technical documentation
- configuration work
- application development
- web development
- software maintenance

## Everyday Technical Support

McIntosh should also be useful to people who do not consider themselves programmers.

Examples:

- "Why won't this game start?"
- "My computer is suddenly slow."
- "This app keeps crashing."
- "Why is my microphone not working?"
- "Help me install this."
- "Why did this update break my program?"
- "Make these two apps work together."
- "Watch what happens when I try this."
- "Can you fix it for me?"

---

# 4. The Apple Tree Concept

The name **McIntosh** creates a natural connection between:

- the Forest metaphor
- an apple tree / apple cultivar
- computers and technology

Simple user-facing idea:

> **Instead of calling tech support, ask the Apple Tree growing inside your computer.**

---

# 5. Small / Big Model Form

McIntosh should follow the Forest rule:

> **Big means "more capable at being this Tree," not "become a different Tree."**

Possible future model structure:

```text
McIntosh Small
├── routine scripting
├── ordinary troubleshooting
├── lightweight software work
├── quick automation
└── common user support

McIntosh Big
├── repository-scale engineering
├── difficult debugging
├── complex refactoring
├── long-horizon coding agents
├── performance analysis
├── advanced technical diagnosis
└── difficult system repair
```

**Qwen3-Coder-Next** is a strong current candidate for McIntosh Big because its specialization closely matches long-running coding, repository work, tool use, debugging, and failure recovery.

This is a candidate, not a frozen choice.

---

# 6. Observation Philosophy

McIntosh should be capable of seeing what is happening on a computer **when the user permits it**.

> **McIntosh should not secretly watch the user.**

Observation should be:

- user-controlled
- permission-aware
- inspectable
- durable when the user wants it to be
- narrow by default
- enforceable below the model
- revocable at any time

Users should be able to configure observation conversationally:

- "Always watch Minecraft."
- "Don't watch Discord."
- "Watch every game I launch."
- "Never watch Bitwarden."
- "When I'm coding, use Developer observation."
- "Watch this app until we figure out why it crashes."
- "You can watch everything except my protected apps."

Persistent preferences should not require re-authorization every launch.

---

# 7. Two Separate Vision Systems

## 7.1 Watch Vision

Watch Vision is:

- persistent or semi-persistent
- narrow
- target-locked
- application/window/tab scoped
- suitable for long-running observation

Example:

> "McIntosh, keep an eye on Minecraft."

This should mean:

```text
Target:
Minecraft

Visual source:
Minecraft only

Technical source:
Minecraft process / logs / resource state

Duration:
persistent until changed

Everything else:
outside McIntosh's visual scope
```

## 7.2 Troubleshoot Vision

Troubleshoot Vision is:

- broader
- temporary
- session-bound
- intended for active diagnosis

Example:

> "McIntosh, help me fix my desktop."

McIntosh may need to follow a problem through:

```text
desktop
↓
settings
↓
file manager
↓
browser
↓
terminal
↓
application
↓
error dialog
```

A Troubleshoot Vision session should **not automatically become a permanent Watch rule**.

---

# 8. Target-Locked Observation

Preferred design:

> **Attach McIntosh's eyes to the authorized object, not to a region of the monitor.**

Avoid:

```text
capture whole screen
↓
crop the rectangle where Minecraft was
↓
send crop to McIntosh
```

Prefer:

```text
authorized object:
Minecraft window identity

capture provider:
Minecraft window/surface only

output:
Minecraft-only observation stream
```

> **A target lock grants access to an object, not to the coordinates where that object happens to appear.**

---

# 9. Minecraft Eye Lock Example

User:

> "McIntosh, always watch Minecraft."

Forest creates:

```text
TRIGGER
Minecraft is running

TARGET
verified Minecraft instance/window

VISUAL
Minecraft window/surface only

TECHNICAL
Minecraft process
Minecraft logs
Minecraft resource use

PERSISTENCE
remember until revoked
```

Then:

```text
Minecraft visible
→ McIntosh sees Minecraft

User Alt+Tabs to Discord
→ McIntosh still sees only Minecraft
→ Discord never enters the observation stream

User opens banking site
→ McIntosh still sees only Minecraft
```

> **McIntosh's eyes remain attached to Minecraft rather than following the user around the desktop.**

---

# 10. Browser Tab Eye Lock

Browser windows and browser tabs should be separate target types.

Example:

```text
Browser
├── Tab A — YouTube
├── Tab B — Bank
├── Tab C — Discord
└── Tab D — Web App
              ↑
       McIntosh Eye Lock
```

If Tab D is authorized, switching to Tab B should not expose Tab B.

A Browser Eye could eventually expose separately permissioned sources such as:

- rendered tab pixels
- title
- URL/domain
- DOM/accessibility tree
- console errors
- failed network requests
- browser diagnostics

---

# 11. Target Death Must Fail Closed

If an authorized target disappears, McIntosh must not automatically inherit a replacement.

```text
Minecraft closes
↓
target disappears
↓
Eye Lock closes
↓
McIntosh sees nothing
```

If Minecraft launches again, Spirit may apply the user's persistent rule to the **new verified Minecraft instance**.

Likewise:

```text
authorized browser tab closes
→ observation ends

new tab opens in same position
→ NOT automatically authorized
```

Identity must matter more than screen position.

---

# 12. Durable Observation Policies

A preference such as:

> "Always watch Minecraft."

should survive:

- app restarts
- McIntosh restarts
- model changes
- quantization changes
- runtime changes
- Qubes restarts
- replacing McIntosh's model

Therefore:

```text
User
↓
McIntosh interprets request
↓
Spirit stores durable policy
↓
McIntosh follows it whenever criteria match
```

---

# 13. Observation Depth

Possible levels:

```text
OFF
→ no active McIntosh observation

ASSIST
→ observe when help is requested

WATCH
→ app state + relevant events

DIAGNOSTIC
→ deeper logs / processes / errors / resources

DEVELOPER
→ traces / builds / tests / code / runtime diagnostics
```

Names are not frozen.

---

# 14. Scope and Duration

Possible scopes:

```text
This time
→ one interaction

Until app closes
→ current launch only

Always for this app
→ persistent rule

Always for this category
→ e.g. games, IDEs

Default for all apps
→ broad default

Never for this app
→ durable exclusion
```

Observation depth and duration should remain separate axes.

---

# 15. Policy Precedence

Possible precedence:

```text
explicit temporary instruction
↓
specific application rule
↓
application/category rule
↓
global default
```

Explicit **Never** exclusions should fail closed.

Example:

```text
Global:
Watch

Games:
Diagnostic

Minecraft:
Developer

Bitwarden:
Never
```

---

# 16. Protected Applications

Some applications should support hard observation exclusions:

- password managers
- banking apps
- private journals
- medical portals
- other user-selected protected apps

During broad Troubleshoot Vision, McIntosh might receive:

```text
[PROTECTED WINDOW]
```

instead of protected contents.

McIntosh may know that a protected window exists without seeing its contents.

---

# 17. Vision and Control Are Separate

```text
VISION
→ may observe

CONTROL
→ may interact
```

User:

> "Watch what I do, but don't touch anything."

Result:

```text
Desktop Eye: ON
Control: OFF
```

Possible control levels:

```text
LOOK
→ inspect only

GUIDE
→ explain what user should do

ASSIST
→ prepare actions and request approval

CONTROL
→ perform approved actions

TASK AUTONOMY
→ complete a bounded authorized objective
```

High-impact actions may still require stronger confirmation.

---

# 18. Sensor Architecture

Possible sensor set:

```text
Target Eye
→ exact app / window / tab

Desktop Eye
→ monitor / workspace / desktop

UI Eye
→ accessibility tree / controls / dialogs

Process Eye
→ processes / services / resources

Log Eye
→ logs / errors / events

Code Eye
→ repository / build / tests / debugger

Browser Eye
→ authorized tab / DOM / console / network
```

Spirit should assemble the minimum sensor bundle required for the task.

Minecraft Watch:

```text
Target Eye     ✅
Process Eye    ✅
Log Eye        ✅
Desktop Eye    ❌
Browser Eye    ❌
```

Desktop Troubleshooting:

```text
Desktop Eye    ✅
UI Eye         ✅
Process Eye    ✅
Log Eye        ✅
Target Eye     maybe
Code Eye       maybe
```

Web App Debugging:

```text
Browser Eye    ✅
Code Eye       ✅
Log Eye        ✅
Process Eye    ✅
Desktop Eye    usually unnecessary
```

---

# 19. Criteria-Based Activation

McIntosh should not need to remain fully active all day.

Possible rules:

- watch Minecraft when it is running
- watch games launched through Steam
- enter Developer observation when an IDE opens
- start diagnostics when an app crashes repeatedly
- watch an app until a specific bug is solved
- wake McIntosh when resource usage crosses a user-defined threshold

Conceptually:

```text
Spirit
↓
criteria satisfied?
↓ yes
open approved sensors
↓
activate McIntosh observer
↓
criteria no longer satisfied
↓
close sensors / return McIntosh to idle
```

---

# 20. Technical Observation Without Full Vision

Visual access should not be required for all troubleshooting.

```text
Minecraft process still observable
Minecraft logs still observable
Minecraft CPU/RAM still observable
Minecraft crash events still observable

Discord foreground
→ not visually observable
```

---

# 21. Lightweight Technical Event History

Even when McIntosh is not actively watching, the Forest may optionally preserve small deterministic technical events such as:

- application started/stopped
- crash occurred
- exit code
- service failure
- package update
- resource exhaustion
- OS error
- hardware disconnect

This should be separate from screen recording.

```text
McIntosh OFF
→ no semantic visual observation
→ no active AI monitoring
→ only user-permitted deterministic diagnostics remain
```

Users should be able to disable even this.

---

# 22. Three Different Kinds of Memory

## Watch Policy

```text
"What is McIntosh allowed to observe?"
```

Stored as durable Spirit policy.

## Technical Event History

```text
"What actually happened?"
```

Bounded logs, events, traces, and provenance.

## Operational Learning

```text
"What did we learn from fixing it?"
```

Examples:

- successful repairs
- failed fixes
- known incompatibilities
- recurring problems
- useful troubleshooting Skills
- environment-specific lessons

Raw observation does not need permanent retention when a useful lesson can be retained instead.

---

# 23. Causal Troubleshooting

McIntosh should distinguish:

```text
WHAT FAILED
from
WHY IT FAILED
from
WHAT CAUSED THAT CONDITION
```

Example:

```text
User:
"My program won't start."

Weak support:
"Try reinstalling it."

McIntosh:
"The application itself appears intact.

Package X was upgraded yesterday.
That replaced library Y with version 6.
This application expects version 5.

The first launch after that update produced
the same linker failure.

The safer fix is restoring compatibility,
not reinstalling the entire application."
```

The long-term goal is **technical causality**, not merely error explanation.

---

# 24. Direct Observation vs Reconstructed History

McIntosh should distinguish facts from inference.

If watching:

```text
Observed:
plugin C failed immediately before the crash.
```

If not watching:

```text
Recorded:
service X stopped at 8:14:03.

Recorded:
package Y updated at 8:12:51.

Cherry context:
the user changed a related setting.

Inference:
the update is likely related,
but McIntosh did not directly observe the interaction.
```

---

# 25. Cross-Tree Troubleshooting

If McIntosh was not observing when an issue occurred, it may request permitted continuity from:

- application/system logs
- crash reports
- deterministic event history
- Maple
- Mycelium
- Operational Learning
- Cherry conversation context
- other permitted Trees
- user's own description

---

# 26. Qubes-Oriented Security Direction

For Qubes-based Forest installations, observation should ideally be enforced below the model.

Preferred pattern:

```text
Application Qube
│
├── Minecraft
│
└── small Forest observation provider
      │
      │ authorized Minecraft-only data
      ↓
   qrexec boundary
      ↓
McIntosh
```

> **McIntosh does not have eyes where permission was never granted.**

---

# 27. User Profiles

## Casual User

```text
Default:
Off

"McIntosh, why isn't Chrome working?"
→ temporary troubleshooting session
```

## Gamer

```text
Default:
Off

Minecraft:
Always Watch

Skyrim:
Always Diagnostic

Steam:
Watch
```

## Developer

```text
IDEs:
Developer

Terminals:
Diagnostic

Games:
Watch

Personal apps:
Off
```

## High-Trust Local User

```text
Default:
Watch

Exceptions:
Password manager → Never
Banking → Never
Private journal → Never
```

---

# 28. Early Workshop Concepts

```text
Troubleshoot
→ logs
→ processes
→ diagnostics
→ system state
→ screen/UI if permitted

Code
→ repository
→ terminal
→ tests
→ debugger

Build
→ apps
→ websites
→ APIs
→ automation

Repair
→ configuration
→ packages
→ services

Performance
→ CPU
→ RAM
→ disk
→ profiling

Desktop
→ screen inspection
→ UI guidance
→ bounded control

Software
→ install
→ update
→ configure
→ remove

Test
→ reproduce
→ isolate
→ verify
→ regression
```

---

# 29. Relationship to Tree Clones

McIntosh may later support Clones for parallel engineering work.

```text
McIntosh
├── Clone — frontend/UI
├── Clone — backend
├── Clone — tests
└── Clone — code review
```

These are Forest-level work units and should not be confused with internal Mixture-of-Experts model experts.

---

# 30. Core Design Principles

> **McIntosh builds, diagnoses, repairs, and maintains the user's digital world.**

> **McIntosh should not secretly watch the user.**

> **Watch is persistent and narrow; Troubleshoot Vision is temporary and broader.**

> **A target lock grants access to an object, not to the coordinates where that object happens to appear.**

> **The model should not enforce its own permissions. Spirit and the environment enforce them.**

> **McIntosh does not need eyes everywhere. He needs the right eyes for the current task.**

> **Vision and control are separate permissions.**

> **Big McIntosh should be more McIntosh, not a different Tree.**

> **Direct observation and reconstructed inference must remain distinguishable.**

> **Retain useful technical lessons without requiring permanent retention of raw surveillance data.**

> **Simple on the surface. Precise underneath. Inspectable when desired.**

---

# 31. Role Summary

```text
McINTOSH
Software Engineer / Digital Technician

BUILD
→ code
→ apps
→ websites
→ scripts
→ automation
→ integrations
→ developer tooling

DIAGNOSE
→ logs
→ processes
→ system events
→ crashes
→ technical causality
→ performance

OBSERVE
→ target-locked Watch Vision
→ temporary Troubleshoot Vision
→ browser/tab observation
→ application-specific sensors

REPAIR
→ configuration
→ software
→ services
→ packages
→ approved system changes

VERIFY
→ reproduce
→ test
→ regression-check
→ confirm the fix actually worked
```

---

# 32. Open Questions / Future Design Work

The following should be decided deliberately before implementation is frozen:

- exact McIntosh role title
- Watch / Troubleshoot user-facing terminology
- observation-depth names
- observation-policy schema
- target identity model
- application relaunch matching
- browser-tab identity and relaunch behavior
- protected-application policy
- capture providers per OS
- Qubes observation-provider architecture
- qrexec observation contract
- UI/accessibility capture
- event-history retention
- telemetry cleanup
- Operational Learning extraction
- sensor-specific permissions
- control permission levels
- high-risk action confirmation
- category rules such as "all games"
- criteria-based wake behavior
- resource budgets for passive Watch
- multi-monitor behavior
- audio observation
- input/action observation
- Small McIntosh model
- Big McIntosh model
- Qwen3-Coder-Next evaluation
- McIntosh Clone behavior
- McIntosh/Bristlecone review workflow
- McIntosh/Cedar security relationship
- McIntosh/Maple/Mycelium/Operational Learning relationship

---

# 33. Current Starting Point

```text
McIntosh
│
├── Software Engineer
├── Digital Technician
├── Everyday Tech Support
├── Advanced Coding / Repository Engineering
├── Technical Troubleshooter
├── Application Observer
├── Controlled Repair Agent
└── Power-User Engineering Tree
```

McIntosh should be approachable enough that an ordinary user can ask:

> "Why isn't my computer working?"

while deep enough that a power user can ask:

> "Observe this failing application, correlate the system events with its logs and code path, reproduce the failure, patch it, run the test suite, verify the regression, and hand the architectural findings to Bristlecone."

That is the intended origin of McIntosh.
