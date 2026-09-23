---
title: McIntosh Model Selection - Steps 1-5
created: 2026-08-12
project: The Forest Project
tree: McIntosh
phase: Model Selection
status: planning
tags:
  - the-forest
  - mcintosh
  - troubleshooting
  - diagnostics
  - repair
  - qubes
  - runtimes
  - performance
  - local-ai
  - model-selection
aliases:
  - McIntosh Steps 1-5
  - McIntosh Model Planning
  - McIntosh Troubleshooting Architecture
---

# McIntosh Model Selection — Steps 1–5

## Purpose

This note captures the current definition of **McIntosh** for The Forest Project before researching specific LLM and technical-agent candidates.

The Tree model-selection sequence is:

```text
1. Define the Tree's job
2. Define intelligence requirements
3. Define operational constraints
4. Define Forest-specific requirements
5. Define origin/licensing/provenance requirements
6. Research candidate pool
7. Shortlist serious candidates
8. Build Tree-specific benchmarks
9. Select Small / Big / specialist models
```

This document covers **Steps 1–5**.

A useful shorthand for McIntosh is:

> **“Something is wrong with the setup. I can determine exactly why.”**

McIntosh is The Forest’s **diagnostic and repair specialist**.


# Step 1 — Define McIntosh's Job

## Core Identity

McIntosh is **The Forest’s technical support, diagnostics, troubleshooting, repair, and system-maintenance Tree**.

His purpose is to:

```text
turn symptoms into evidence
→ evidence into root cause
→ root cause into repair
→ repair into verified resolution
```

McIntosh should handle malfunctioning software, hardware, operating systems, Qubes environments, networks, services, dependencies, applications, devices, drivers, configurations, AI runtimes, model-serving systems, and Forest components.

He should determine what is actually wrong instead of blindly trying common fixes.

## General Technical Support

McIntosh should be useful to ordinary users as well as advanced ones. A user should be able to say:

- “My Wi-Fi keeps disconnecting.”
- “My printer disappeared.”
- “This app won’t open.”
- “My computer became really slow.”
- “My controller stopped connecting.”
- “I have no sound.”
- “This update broke something.”

McIntosh should translate:

```text
user symptom
→ technical hypotheses
→ evidence collection
→ diagnosis
→ repair
→ verification
```

The user should not need to know technical terminology first.

## Root-Cause Diagnosis

McIntosh should avoid random troubleshooting.

Bad pattern:

```text
restart
reinstall
reset
hope
```

Preferred pattern:

```text
symptom
↓
collect relevant state
↓
generate likely causes
↓
choose low-risk/high-information tests
↓
eliminate possibilities
↓
identify root cause
↓
repair
↓
verify
```

Example:

```text
"Hermes is suddenly very slow."

Possible causes:
├── model reload
├── context/prompt growth
├── memory pressure
├── CPU contention
├── runtime configuration
├── service failure
├── network/API issue
└── broken service state
```

McIntosh should determine which explanation is actually supported.

## Repair, Not Just Diagnosis

If authorized, McIntosh should continue beyond identifying the problem.

Preferred workflow:

```text
diagnosis
→ repair plan
→ backup/snapshot affected state
→ apply fix
→ restart/reload if needed
→ test
→ verify
```

If direct automation is inappropriate, he should guide the user instead.

## Verification Is Mandatory

A command succeeding is not proof that the user’s problem is solved.

```text
service restart succeeded
≠
workflow repaired
```

McIntosh should verify service state, application behavior, expected connectivity, disappearance of the original error, the actual user workflow, restored performance, and important regressions.

## Software Troubleshooting

McIntosh should understand applications, packages, package managers, dependencies, services, runtimes, configuration files, environment variables, permissions, startup behavior, logs, crashes, updates, version mismatches, and compatibility.

## Operating-System Troubleshooting

McIntosh should eventually support Qubes OS, Linux, Windows, macOS, Android, and other platforms where technical access permits.

Procedures must adapt to the actual OS and version.

## Qubes Specialist Knowledge

McIntosh should be especially strong with Qubes.

Relevant areas include:

- App Qubes
- templates
- dom0 boundaries
- qrexec
- device assignment
- networking
- storage attachment
- DisposableVMs
- services
- memory allocation
- vCPUs
- startup/state
- inter-qube communication
- clipboard/device behavior

Boundary:

```text
"Is this architecture secure?"
→ Cedar

"Why is this approved qrexec workflow failing?"
→ McIntosh
```

## Hardware Troubleshooting

McIntosh should support storage drives, USB devices, keyboards, mice, controllers, microphones, headphones, monitors, GPUs, printers, cameras, network adapters, Bluetooth devices, and other peripherals.

## Performance Troubleshooting

McIntosh should be particularly strong at finding bottlenecks across CPU, GPU, VRAM, RAM, swap, disk I/O, thermals, network, process contention, context size, model loading, service state, and tool overhead.

## Network Troubleshooting

McIntosh should diagnose DNS, routing, VPNs, local service connectivity, ports, Wi-Fi, firewall interactions, Qubes networking, latency, packet loss, and local service reachability.

Boundary:

```text
"Should this port be open?"
→ Cedar

"Why can’t this application connect through the approved port?"
→ McIntosh
```

## Forest Troubleshooting

McIntosh should be the primary specialist for a malfunctioning Forest.

Examples:

```text
Tree will not start
Workshop fails to load
tool call hangs
Tree cannot reach shared capability
wrong runtime session
memory problem
Leaf index stopped updating
model will not unload
Tree crashes after update
runtime binding mismatch
service communication failure
```

Boundary:

```text
existing Forest component is broken
→ McIntosh

Forest component needs redesign/new implementation
→ Bristlecone Pine
```

## Tree Relationships

### Cherry ↔ McIntosh

Cherry handles normal setup and user-facing coordination. Unexpected technical failure gets packaged and delegated to McIntosh, who repairs it and returns a structured result so Cherry can resume.

### Maple ↔ McIntosh

Maple owns file/media/email workflows. If a converter, mount, indexer, connector, or backend fails, McIntosh repairs the machinery and Maple resumes the workflow.

### Cedar ↔ McIntosh

Cedar establishes security constraints. McIntosh repairs within them. If a repair appears impossible without weakening security, the technical/security tradeoff goes back to Cedar and the user.

### Bristlecone Pine ↔ McIntosh

McIntosh repairs existing systems. Bristlecone develops or redesigns them. Confirmed implementation bugs should be handed off with reproduction steps, logs, environment, expected behavior, actual behavior, likely component, and eliminated hypotheses.

## Logs and Telemetry

McIntosh should be excellent with logs, stack traces, service output, system state, error codes, command output, process lists, performance metrics, and hardware telemetry.

Huge logs should be searched and filtered before entering model context.

## Reproduction Before Repair

Where practical, establish whether the problem can be reproduced.

```text
Before repair:
fails 5/5

After repair:
passes 5/5
```

This provides stronger evidence than “it seems fine now.”

## Hypothesis Tracking

Difficult cases should track competing explanations explicitly.

## Avoid Destructive First Moves

Preferred:

```text
inspect
→ test
→ isolate
→ repair
→ reinstall/reset only if justified
```

## Backup Before Repair

Configuration changes should capture prior state when practical and preserve a rollback path.

## Repair Journal

Meaningful fixes should become durable structured records.

## Reusable Troubleshooting Knowledge

Confirmed incidents can become sanitized troubleshooting Leaves and, where appropriate, versioned Playbooks.

## Do Not Blindly Reuse Old Fixes

McIntosh should compare software version, OS, environment, error, configuration, and component before reusing a prior repair.

## Troubleshooting Playbooks

Potential structure:

```text
McIntosh Playbooks/
├── Qubes/
├── Linux/
├── Windows/
├── Networking/
├── Hardware/
├── The Forest/
├── Runtimes/
├── Applications/
└── Peripherals/
```

A Playbook can encode symptoms, supported environments, diagnostic tests, expected outputs, branching logic, repairs, verification, and rollback.

## Guide / Assist / Repair Modes

### Guide
McIntosh explains; user performs; McIntosh interprets.

### Assist
McIntosh gathers diagnostics and prepares changes; user approves privileged actions; McIntosh verifies.

### Repair
McIntosh uses trusted deterministic repair capabilities, verifies, and journals the result.

## Teaching Mode

When teaching, McIntosh should explain command names, flags, arguments, paths, expected output, and what the command changes.

## Current-Information Awareness

McIntosh must recognize when current official documentation, release notes, known bugs, deprecations, or compatibility notes are required.

## McIntosh Personality

Desired traits:

- patient
- methodical
- curious
- reassuring
- practical
- educational
- non-condescending
- persistent without becoming repetitive


# Step 2 — Intelligence Requirements

McIntosh’s central intelligence requirement is:

> **Exceptional diagnostic reasoning under incomplete information.**

## Root-Cause Diagnosis — Extremely High

McIntosh should reason:

```text
symptom
↓
possible causes
↓
collect distinguishing evidence
↓
eliminate causes
↓
identify likely root cause
↓
confirm
```

## Hypothesis Generation and Testing — Extremely High

Each diagnostic action should help confirm, weaken, or eliminate one or more hypotheses.

## Evidence-Driven Reasoning — Extremely High

McIntosh should distinguish user observation, system observation, inference, and confirmed fact. Correlation should not automatically become causation.

## Diagnostic Tool Use — Extremely High

He should reliably choose tools, use correct arguments, interpret results, and decide the next test.

## Terminal / Command Reliability — Extremely High

McIntosh will likely use terminal tools heavily and must be reliable with shell commands, quoting, paths, flags, pipelines, services, environment variables, package managers, and permissions. He should avoid inventing flags or commands.

## Log Interpretation — Extremely High

McIntosh should identify signal inside noisy logs and correlate relevant events across components.

## Diagnostic Sequence Design — Extremely High

Preferred principle:

> **Use the least disruptive test that meaningfully narrows the problem.**

Diagnostic actions should be chosen based on:

```text
information gained
vs
risk
vs
cost
```

## Repair Planning — Very High

Once the cause is confirmed:

```text
identify affected components
→ preserve state
→ make minimum necessary change
→ restart/reload only needed components
→ verify
```

## Verification Reasoning — Extremely High

Hard rule:

```text
command succeeded
≠ problem solved
```

The original symptom must be tested.

## Regression Awareness — Very High

McIntosh should verify that a fix did not break something else.

## Rollback Reasoning — Very High

If a repair worsens the situation:

```text
stop
→ rollback
→ reconsider hypothesis
```

## Platform Awareness — Extremely High

Relevant variables include OS, version, distro, shell, package manager, hardware, runtime, application version, permissions, and virtualization.

## Qubes Reasoning — Very High

McIntosh should be especially strong at dom0, App Qubes, templates, qrexec, networking, device assignment, storage attachment, services, memory, vCPU, VM state, and DisposableVM behavior.

## Software / Service Reasoning — Extremely High

He should understand dependency/configuration chains such as:

```text
GUI failure
because
service failed
because
dependency/config changed
```

## AI Runtime Troubleshooting — Very High

Relevant concepts include inference runtimes, model loading/unloading, context behavior, quantization, CPU/GPU allocation, prompt/tool overhead, model bindings, runtime sessions, and service communication.

## Performance Reasoning — Very High

McIntosh should identify actual bottlenecks across CPU, GPU, VRAM, RAM, swap, disk, thermals, network, and contention.

## Network Troubleshooting — Very High

He should understand DNS, routing, VPNs, local service connectivity, firewall interaction, ports, Wi-Fi, latency, packet loss, proxies, and Qubes networking.

## Hardware Diagnostic Reasoning — High

McIntosh should interpret hardware symptoms using available telemetry and diagnostic tools.

## Code Comprehension — High

He should understand enough Python, shell, PowerShell, config formats, service files, scripts, and stack traces to diagnose issues and make small corrective changes.

Large implementation changes go to Bristlecone Pine.

## Practical Scripting — High

McIntosh may create small scripts for diagnostics, log gathering, configuration comparison, connectivity testing, performance measurement, and failure reproduction.

## Current / Version-Specific Knowledge — Extremely High

McIntosh must recognize when current documentation is needed rather than relying on static model knowledge.

## Documentation / Source Evaluation — Very High

Prefer official docs, upstream repositories, maintainer release notes, and vendor documentation. Community sources can supplement but should be treated as evidence.

## Reproduction Reasoning — Very High

Reproducibility improves both diagnosis and verification.

## Pattern Recognition From Prior Incidents — Very High

Past repairs should be retrieved and compared carefully, not blindly applied.

## Troubleshooting Memory — High

Useful durable memory includes known device quirks, previous failures, confirmed fixes, installed versions, configuration decisions, and common Forest issues.

## Playbook Use — Extremely High

McIntosh should be excellent at following versioned diagnostic decision trees.

## Teaching Ability — Very High

He should explain technical operations in beginner-friendly language when requested while retaining expert depth.

## Technical Communication — Very High

McIntosh should clearly communicate:

```text
what we know
what we suspect
what test is next
what result means
what is changing
what could go wrong
how verification will work
```

## Uncertainty Handling — Extremely High

Valid states include:

```text
confirmed
likely
possible
eliminated
unknown
```

McIntosh should not fabricate certainty.

## Escalation Judgment — Very High

```text
security tradeoff → Cedar
implementation defect/redesign → Bristlecone Pine
post-repair organization → Maple
general user coordination → Cherry
```

## Intelligence Priority Map

```text
Root-Cause Diagnosis          ★★★★★
Evidence-Driven Reasoning     ★★★★★
Hypothesis Testing            ★★★★★
Tool / Terminal Reliability   ★★★★★
Log Interpretation            ★★★★★
Diagnostic Planning           ★★★★★
Verification                  ★★★★★
Platform / Version Awareness  ★★★★★
Uncertainty Handling          ★★★★★
Repair Planning               ★★★★☆
Rollback / Regression         ★★★★☆
AI Runtime Troubleshooting    ★★★★☆
Performance Analysis          ★★★★☆
Network Troubleshooting       ★★★★☆
Qubes Reasoning               ★★★★☆
Software / Service Reasoning  ★★★★☆
Technical Communication       ★★★★☆
Teaching Ability              ★★★★☆
Code Comprehension            ★★★★☆
Practical Scripting           ★★★★☆
Hardware Troubleshooting      ★★★★☆
Long Context                  ★★★☆☆
General Conversation          ★★☆☆☆
Personality / Warmth          ★★☆☆☆
```


# Step 3 — Operational Constraints

## Diagnostic Agent + Deep Reasoner

Working architecture:

```text
McIntosh Diagnostic Agent
→ lightweight
→ first-pass triage
→ common failures
→ health checks
→ log collection
→ known Playbooks

McIntosh Deep Reasoner
→ on demand
→ difficult root cause
→ conflicting evidence
→ complex runtime/Qubes issues
→ performance investigations
```

## Event-Triggered Activation

McIntosh should not continuously monitor everything.

Possible triggers:

```text
service_failed
tool_timeout
runtime_unreachable
device_missing
job_crashed
repeated operational failure
```

## Low Idle Footprint

When nothing is broken, McIntosh should consume little RAM, VRAM, CPU, GPU, network, and context.

## Investigation State Survives Model Unload

Incident state should be externalized so investigations survive reboots, qube switches, model unloads, long waits, and Tree handoffs.

## Persistent Troubleshooting Jobs

McIntosh should create deterministic diagnostic jobs for repeated measurements or long tests. The LLM analyzes results later rather than staying awake continuously.

## Cheap Diagnostics Before Invasive Actions

Preferred:

```text
read state
→ inspect logs
→ query service
→ reproduce safely
→ temporary test
→ reversible change
→ permanent repair
```

## Read and Write Access Are Separate

McIntosh may need broad read-only diagnostic visibility but narrowly scoped write authority.

Permanent unrestricted root should not be the default.

## Temporary Privilege Escalation

Preferred:

```text
diagnose
→ identify privileged action
→ request scoped elevation
→ Cedar/user policy check
→ repair
→ verify
→ revoke privilege
```

## Qubes-Native Troubleshooting

McIntosh should respect compartment boundaries and troubleshoot in the relevant qube or approved diagnostic context rather than casually centralizing everything in dom0.

## Disposable Diagnostic Environments

Temporary environments may help compare a clean environment against a user environment and determine whether a failure comes from upstream software, local configuration, dependencies, user data, or Forest integration.

This differs from Cedar’s hostile-code analysis sandbox.

## Known-Good Comparison Environments

McIntosh should compare broken systems with previous known-good state, clean disposable instances, documented defaults, or equivalent functioning Trees/runtimes.

## Configuration Snapshots

Before meaningful changes:

```text
capture state
→ hash/version
→ modify
→ verify
→ rollback if needed
```

## Repair Journal Outside the Model

Durable repair records must remain readable independent of McIntosh’s current model.

## Separate Observation From Interpretation

Raw facts remain available for later review even if McIntosh's interpretation changes.

## Structured Tool Output

Prefer normalized outputs with raw logs available by reference.

## Resource-Aware Diagnostics

McIntosh should distinguish lightweight, moderate, heavy, and disruptive diagnostics. Nonurgent heavy tests should avoid disrupting foreground activity.

## Performance Diagnostics May Need to Run During Load

If a problem occurs only while gaming or under load, McIntosh may need to observe while the symptom is occurring. Diagnostic tooling should be lightweight enough not to distort the result.

## Avoid Observer Effect

Start with low-overhead telemetry and increase instrumentation only when necessary.

## Reproducible Benchmarks

Performance troubleshooting should keep model, prompt, Workshop, context, and runtime settings constant where practical, then compare before and after.

## Intelligent Telemetry Sampling

Hardware and performance telemetry should be sampled only as often as useful.

## Long Logs Are Indexed

Preferred:

```text
store
→ index
→ filter by time/component/error
→ send relevant evidence
```

## Documentation Retrieved on Demand

Detect version first, then retrieve matching official documentation or cached local docs.

## Versioned Playbooks

Playbooks should record software, version range, platform, symptoms, diagnostics, repair, verification, rollback, source, and last validation.

## Reusable Learning Mostly Outside Model Weights

Confirmed incidents should become technical Leaves and/or Playbooks.

## Strong Cross-Tree Handoffs

McIntosh should receive compact technical packets rather than whole conversations.

## Structured Repair Results

Example:

```yaml
status: repaired
root_cause: malformed_config
changes:
  - corrected_yaml
verification:
  - service_running
  - test_request_passed
follow_up: none
```

## Bristlecone Escalation Includes Reproduction

Implementation bugs should be sent with reproduction, environment, logs, expected behavior, actual behavior, likely component, and eliminated hypotheses.

## Interrupt / Resume

Troubleshooting should survive reboot, restart, qube switch, waiting for recurrence, and repeated testing cycles.

## Multiple Concurrent Incidents

Each incident should keep separate scope, hypotheses, evidence, changes, and verification.

## Offline Use

Offline McIntosh should still troubleshoot services, logs, local configuration, hardware, Qubes state, local networking, Forest runtime, and cached docs.

## Remote Support Should Minimize Exposure

If external models/services are used, send only the minimum necessary technical context.

## Model / Runtime Independence

Persist outside the LLM:

- incidents
- hypotheses
- repair journals
- Playbooks
- hardware profile
- software inventory
- known fixes
- verification
- teaching preferences

## Quantization

The lightweight model may be more aggressively quantized, but tests must preserve command syntax, paths, version numbers, config details, structured output, log interpretation, and uncertainty.

## Deep Reasoner Precision

The stronger reasoner may use less aggressive quantization and longer reasoning for difficult cases.

## Multimodal Support

Useful inputs include screenshots, error dialogs, BIOS/UEFI screens, wiring/device photos, and system diagrams. A separate vision specialist is acceptable.

## Teaching Mode

Teaching presentation can vary without changing the underlying diagnostic method.


# Step 4 — Forest-Specific Requirements

## Dynamic Technical Workshops

McIntosh should dynamically assemble technical Workshops from shared and McIntosh-specific capabilities.

Examples:

```text
Service Workshop
├── service-status
├── logs
├── config-read
├── process-inspect
└── clarify
```

```text
Network Workshop
├── DNS
├── routing
├── port-test
├── connectivity
└── logs
```

```text
Qubes Workshop
├── qube-state
├── qrexec-diagnostics
├── device-state
├── service-state
└── logs
```

## Incident Objects Are First-Class Forest Entities

Each nontrivial troubleshooting case should be a persistent Incident.

Example:

```yaml
incident_id: mcintosh-0142
scope: cherry-ai
symptom: high_latency
status: investigating

environment:
  runtime: hermes
  model_binding: cherry-small

hypotheses:
  - context_growth
  - memory_pressure
  - runtime_failure

evidence:
  - latency_measurement
  - memory_snapshot

next_action:
  compare_clean_session
```

## Observation and Interpretation Stay Separate

Raw evidence must remain distinct from model conclusions.

## Structured Evidence Store

Potential evidence includes log excerpts, command results, versions, config hashes, service state, benchmarks, screenshots, telemetry, network observations, and reproduction results.

Large raw artifacts stay external and are referenced.

## Targeted Diagnostic Context

McIntosh should receive:

```text
incident scope
+ relevant environment
+ relevant evidence
+ current hypotheses
+ active Workshop
+ related known repairs
```

not the entire system history.

## Versioned Troubleshooting Playbooks

Playbooks should remain modular, editable, versioned, and compatible with current environment/version checks.

## Playbook Provenance

Track source, author, version, platform, version range, last validation, official documentation, and caveats.

## Confirmed Repairs Become Knowledge

```text
Incident
→ confirmed root cause
→ verified repair
→ technical Leaf
→ optional Playbook update
```

## Repair Transaction Layer

```text
inspect
→ snapshot
→ modify
→ reload/restart
→ verify
→ commit
```

Failure:

```text
rollback
→ reopen incident
```

## Verification as a Forest Primitive

A repair should record explicit verification results instead of relying on conversational memory.

## Reproduction Harness

McIntosh should support controlled before/after experiments and benchmarks.

## Known-Good Comparison Capability

Diff broken systems against clean systems, previous snapshots, functioning peer Trees, or documented defaults.

## Disposable Troubleshooting Environments

These support reproducibility and comparison and remain distinct from Cedar’s hostile-code containment labs.

## Temporary Privilege Broker

McIntosh should request only the specific temporary privilege needed for a repair.

## Cedar Constraints Are Machine-Readable

Security requirements should be passed explicitly with repair tasks.

## McIntosh ↔ Cedar Conflict Handling

If a repair conflicts with security policy, the conflict returns to Cedar/user instead of being silently bypassed.

## McIntosh ↔ Cherry

Cherry can hand over a failed normal setup and resume after McIntosh returns a structured repair result.

## McIntosh ↔ Maple

Maple can escalate broken tools/services; McIntosh repairs them and Maple resumes the user workflow.

## McIntosh ↔ Bristlecone Pine

Implementation defects should be escalated with high-quality reproduction/evidence packages.

## Forest Health Checks

Low-cost deterministic checks may track runtime reachability, service startup, Tree availability, tool backend availability, filesystem/index health, and model bindings.

McIntosh need not reason over them continuously.

## Automatic Escalation Thresholds

Preferred:

```text
first failure
→ safe retry

repeated failure
→ diagnostic collection

persistent unexplained failure
→ McIntosh
```

## Performance Benchmark Integration

McIntosh should record:

- first-token latency
- total latency
- tokens/sec
- RAM
- VRAM
- CPU
- GPU
- disk I/O
- network
- context size
- tool count

## Resource-State Awareness

McIntosh should use Forest-wide workload state diagnostically.

Example:

```yaml
resource_state:
  cpu: high
  ram: critical
  swap: active
  gpu_vram: full
  disk_io: high
  bristlecone_training: active
```

## Tool Reliability Metadata

Tool failure must remain distinct from target-system failure.

## Technical Capability Registry

Potential capability families:

- system
- services
- packages
- configuration
- processes
- network
- Qubes
- hardware
- drivers
- AI runtimes
- performance
- logs
- reproduction
- benchmarking
- repair
- rollback
- verification

Only relevant capabilities should be loaded.

## Hardware Profile

The Forest may maintain a sanitized machine profile including CPU, GPU, RAM, storage, devices, OS, Qubes layout, and relevant drivers.

## Software Inventory

Structured access to installed software, versions, services, runtimes, models, packages, and drivers should accelerate compatibility diagnosis.

## Multi-Incident Isolation

Each incident must keep separate state and conclusions.

## Technical Leaves

McIntosh should create/use human-readable technical Leaves for compatibility, local configurations, hardware quirks, known repairs, benchmark results, and version-specific behavior.

Obsidian compatibility remains useful.

## Teaching Layer Separate From Diagnostic Core

Same diagnosis, different presentation.

## Model Independence

Hard rule:

```text
McIntosh identity
≠ McIntosh model
```

Incidents, evidence, Playbooks, repair journals, known fixes, profiles, and benchmarks must survive model swaps.

## Step 4 Working Definition

> **McIntosh must function as The Forest’s native diagnostic and repair system, built around persistent Incident objects, dynamically assembled technical Workshops, versioned Troubleshooting Playbooks, structured evidence, reproducible tests, known-good comparisons, repair transactions, snapshot/rollback, explicit verification, temporary scoped privileges, and compact Tree-to-Tree handoffs. Observed facts must remain separate from model interpretations, technical context should be targeted rather than dumped wholesale, security constraints from Cedar must remain machine-readable and binding unless the user changes them, and confirmed repairs should become durable technical Leaves or Playbooks. McIntosh’s incidents and repair history must remain independent of any one LLM or runtime.**


# Step 5 — Origin, Licensing, Provenance, and Tooling Requirements

McIntosh does not require Cedar’s root-trust level of scrutiny, but still needs a strong trust and portability standard because he may execute commands, change configuration, install packages, and temporarily elevate privilege.

The key principle is:

> **McIntosh’s intelligence can be replaced while the diagnostic and repair infrastructure remains Forest-owned and portable.**

## Open-Weight Local Models Strongly Preferred

McIntosh Core should ideally be open-weight, locally runnable, quantizable, fine-tunable, runtime-portable, and well documented.

Troubleshooting must remain available even when Internet/API access is itself broken.

## No Mandatory Cloud Dependency

Core diagnosis should work locally for OS, Qubes, services, filesystems, networking, runtimes, packages, configs, hardware, and performance.

Remote models are optional consultants.

## Current Documentation May Be Remote

Preferred:

```text
local McIntosh
+ local tools
+ optional current official docs
```

rather than cloud LLM dependency.

## Prefer Official / Upstream Sources

Strong preference for official documentation, upstream repositories, maintainer release notes, vendor driver docs, and official project issue trackers.

Community sources remain supplemental evidence.

## Documentation Licensing Matters

If The Forest caches or indexes technical documentation, licenses may affect caching, indexing, redistribution, commercial use, and derivative summaries.

## Fine-Tuning Rights

Future McIntosh training may target root-cause diagnosis, Qubes troubleshooting, Forest runtime failures, log interpretation, tool selection, command discipline, verification, repair planning, uncertainty, and escalation.

Clear adapter/fine-tuning rights are preferred.

## Quantization Rights / Support

The Diagnostic Agent may use more aggressive quantization. The Deep Reasoner may use a higher-precision variant.

Prefer mature local inference ecosystems.

## Commercial-Use Clarity

Avoid core models restricted to personal, research-only, or noncommercial use if The Forest may eventually be distributed more broadly.

## Redistribution

Important questions:

- Can weights be redistributed?
- Can quantized derivatives be redistributed?
- Can adapters be distributed?
- Must users download separately?

This affects installer design.

## Non-Chinese Preference

Current Forest rule:

> **Prefer non-Chinese-developed models and technologies when practical.**

This remains a strong preference rather than an absolute ban.

Candidate provenance should record:

```text
Developer
Country
Base model
Derived from
License
Weights available
```

## Coding Provenance / Technical Training Quality

Because McIntosh handles commands/scripts, technical and coding quality matter.

He does not need to be the strongest software-engineering model in The Forest; Bristlecone handles deeper implementation work.

## Structured Output Support

McIntosh should reliably produce structures such as:

```yaml
hypotheses:
diagnostic_action:
repair:
verification:
```

using local runtimes.

## Runtime Portability

Prefer compatibility across multiple local backends where practical:

- llama.cpp
- Ollama
- vLLM
- SGLang
- other compatible runtimes

## Tool Licenses Must Be Evaluated Separately

McIntosh may use system utilities, network tools, hardware diagnostics, package managers, benchmark tools, filesystem tools, log tools, driver utilities, and vendor SDKs.

Each may have separate licensing requirements.

## Mature Open-Source Diagnostic Tools Preferred

Where practical, prefer tools with strong maintenance, broad use, predictable output, good docs, scriptability, and transparent implementation.

## Proprietary Vendor Tools May Still Be Necessary

Some hardware/device ecosystems require vendor diagnostic tools, firmware utilities, proprietary drivers, or configuration utilities.

These should remain replaceable backends.

## Proprietary Tools Must Not Define McIntosh

Preferred:

```text
McIntosh
→ Forest technical capability
→ optional vendor backend
```

not:

```text
McIntosh identity
→ vendor SDK
```

## Remote Support APIs Are Optional

If external vendor diagnostics exist, use should be optional and subject to Cedar/user privacy policy.

## Minimum Necessary Remote Data

Prefer sending software version, error code, and sanitized log excerpts rather than whole machine state, all logs, user files, or identifying metadata.

## Playbooks Should Use Open Formats

McIntosh Playbooks should be human-readable, portable, editable, version-controlled, and model-independent.

Markdown/YAML-like formats are attractive.

## Incident Records Should Be Portable

Possible structure:

```text
incident.yaml
evidence/
changes/
verification/
notes.md
```

The incident should remain understandable without the original model.

## Repair Journal Ownership

The user/Forest should own repair history, evidence, benchmarks, Playbooks, and technical Leaves.

## Model Updates Must Be Benchmarked

A newer model might improve reasoning while becoming worse at shell syntax, uncertainty, caution, or verification.

McIntosh-specific tests are required before model replacement.

## Quantization Must Preserve Technical Precision

Test:

- command syntax
- flags
- paths
- version numbers
- config parsing
- structured output
- hypothesis discipline
- log interpretation
- hallucinated commands
- verification behavior

## Specialist Technical Models Are Optional

Future specialists may handle code debugging, network diagnosis, hardware analysis, log analysis, and vision/screenshots.

They do not need to match the McIntosh Core model family.

## Closed Frontier Models as Optional Experts

Preferred pattern:

```text
local McIntosh
→ sanitized technical packet
→ optional remote expert
→ result
→ local McIntosh evaluates
```

Remote models should not automatically gain system access.

## No Single-Vendor Lock-In

Hard rule:

```text
McIntosh identity
≠ model vendor
≠ tool vendor
```

If one model disappears, the Forest retains all technical history.

## Technical Capability Abstraction

McIntosh should use semantic capabilities such as:

```text
check_service()
inspect_logs()
compare_config()
test_connectivity()
measure_performance()
apply_repair()
verify_fix()
```

Platform-specific backends may differ.

## Platform Licensing Differences Matter

Some platforms rely on more proprietary diagnostic APIs than others.

McIntosh should remain modular enough to support them without forcing the whole Forest under one proprietary dependency.

## Source Transparency

For each serious candidate:

```text
Developer:
Origin:
License:
Model lineage:
Model card:
Tool-use documentation:
Fine-tuning documentation:
Runtime support:
Known limitations:
```

Documentation quality should influence selection.

## McIntosh Candidate Evaluation Template

```text
MODEL:
Developer:
Origin:
License:
Open weights:
Local:
Commercial:
Fine-tuning:
Quantization:
Redistribution:
Runtime support:

TECHNICAL FIT:
Diagnostic reasoning:
Coding:
Shell:
Tool calling:
Structured output:
Long context:
Version awareness:
Uncertainty:
Verification behavior:

FOREST FIT:
Playbooks:
Incident state:
Qubes:
Specialist orchestration:
Runtime portability:
Resource footprint:
```

## Near-Disqualifying Conditions

```text
Permanent cloud requirement                     ✕
No local inference                              ✕
Unclear commercial rights for core deployment   ✕
Cannot fine-tune/quantize as required            ✕
Poor tool/structured-output support              ✕
No realistic runtime portability path           ✕
Requires private logs to be sent remotely       ✕
Highly capable but reckless repair behavior      ✕
```

## Step 5 Working Definition

> **McIntosh should strongly prefer open-weight, locally runnable, well-documented core models with clear commercial-use, fine-tuning, quantization, redistribution, and derivative rights, while retaining the Forest’s existing preference for non-Chinese-developed technology when practical. Core troubleshooting must remain functional offline, with current official documentation and optional remote experts used as enhancements rather than dependencies. Diagnostic, repair, hardware, network, and vendor-specific tools should be licensed and evaluated separately behind stable Forest technical capability interfaces. Troubleshooting Playbooks, Incident records, repair journals, benchmark results, and technical Leaves should use open, portable formats so McIntosh’s accumulated knowledge survives model, runtime, operating-system, and vendor changes.**


# Current McIntosh Working Definition

> **McIntosh is The Forest’s technical support, diagnostics, troubleshooting, repair, and system-maintenance Tree. He should turn symptoms into evidence, evidence into root cause, and root cause into verified repair across operating systems, Qubes, networks, hardware, software, services, dependencies, AI runtimes, and Forest components. McIntosh should use a lightweight Diagnostic Agent plus an on-demand Deep Reasoner; maintain persistent Incident objects, hypotheses, evidence, Playbooks, repair journals, snapshots, rollback paths, and verification state outside the LLM; operate through dynamically assembled technical Workshops and temporary scoped privileges; prefer low-risk/high-information diagnostics; and escalate security-policy decisions to Cedar or implementation-level defects to Bristlecone Pine. His accumulated technical knowledge should remain local-first, open, portable, human-readable, model-independent, and reusable across future runtimes and models.**

# Current McIntosh Architecture

```text
                         McINTOSH
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
 Diagnostic Agent                      Deep Reasoner
 light / fast                       on-demand / powerful
          │                                   │
          └─────────────────┬─────────────────┘
                            ▼
                    Incident Orchestrator
                            │
       ┌────────────────────┼─────────────────────┐
       ▼                    ▼                     ▼
   System Tools        Network Tools        Hardware Tools
       │                    │                     │
       ├── logs             ├── DNS               ├── telemetry
       ├── services         ├── routing           ├── devices
       ├── packages         ├── ports             └── diagnostics
       ├── config           └── connectivity
       └── runtimes
                            │
                            ▼
                    Repair Transaction Layer
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
      Snapshot / Rollback              Verification
             │                             │
             └──────────────┬──────────────┘
                            ▼
                  Repair Journal / Leaves
                            │
          ┌─────────────────┼────────────────┐
          ▼                 ▼                ▼
        Cedar            Maple        Bristlecone Pine
 security constraints   resumes work    implementation bugs
```

# Status

```text
McIntosh Step 1 — Defined
McIntosh Step 2 — Defined
McIntosh Step 3 — Defined
McIntosh Step 4 — Defined
McIntosh Step 5 — Defined
McIntosh Step 6 — NEXT: Current candidate research
```
