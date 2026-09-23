---
title: Cedar Model Selection - Steps 1-5
created: 2026-08-12
project: The Forest Project
tree: Cedar
phase: Model Selection
status: planning
tags:
  - the-forest
  - cedar
  - security
  - privacy
  - permissions
  - recovery
  - encryption
  - sandboxing
  - incident-response
  - local-ai
  - model-selection
aliases:
  - Cedar Steps 1-5
  - Cedar Model Planning
  - Cedar Security Architecture
---

# Cedar Model Selection — Steps 1–5

## Purpose

This note captures the current definition of **Cedar** for The Forest Project before researching specific LLM and security-model candidates.

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

The central Cedar principle is:

> **Cedar protects the user's choices; Cedar does not replace them.**

The user owns the device, the Forest, the data, and the final decision.

---

# Step 1 — Define Cedar's Job

## Core Identity

Cedar is **The Forest's security, trust, privacy, permission, and recovery Tree**.

Cedar protects:

- the user
- the user's device
- the Forest
- Tree-to-Tree boundaries
- credentials and secrets
- sensitive data
- trusted recovery state
- security policy
- user-defined privacy preferences

Cedar should not merely provide cybersecurity advice.

In areas explicitly assigned to it, Cedar should be able to work through deterministic security controls to:

- observe
- assess
- warn
- recommend
- assist
- enforce user-approved policy
- isolate
- recover

Cedar's authority should never originate from the LLM itself.

Conceptually:

```text
USER
  ↓
security/privacy preferences
accepted-risk policy
explicit Cedar authority
  ↓
CEDAR
  ↓
deterministic security controls
```

Not:

```text
Cedar
  ↓
decides what the owner is allowed to do
```

---

## 1. Security Authority

Cedar should answer questions such as:

- Is this action safe?
- Is this software suspicious?
- Should this Tree receive this permission?
- Is this network connection expected?
- Did a security-sensitive setting change?
- Is this credential at risk?
- Is this application asking for more access than necessary?
- Is this suspicious behavior actually meaningful?
- Should this file be quarantined?
- Is this privacy tradeoff acceptable under the user's preferences?

Cedar is the **security authority of The Forest**, but its power remains delegated by the user.

---

## 2. Permission Management

Cedar should deeply understand Forest permissions.

Example:

```text
Maple requests:
email.read
email.attachment.download
write access to one project folder
```

Cedar should help ensure Maple does **not** automatically receive:

```text
email.*
filesystem.*
secrets.*
```

Important principles:

- least privilege
- scoped access
- temporary access
- revocation
- explicit user approval
- permission auditing
- context access ≠ tool access ≠ data access ≠ system authority

---

## 3. Inter-Tree Security Boundaries

Cedar should help enforce isolation boundaries such as:

```text
Cherry Diary ✕ Cedar
Cherry Diary ✕ Maple
Cherry Diary ✕ McIntosh
```

and:

```text
Cedar secrets ✕ normal Trees
Maple file scope ≠ Cedar recovery store
McIntosh diagnostic privilege ≠ permanent system authority
```

A Tree should receive only the minimum context and capability necessary for its current task.

---

## 4. Security Monitoring

Cedar should be able to observe security-relevant events such as:

- unusual login attempts
- permission changes
- unknown devices
- suspicious outbound connections
- unexpected file modification
- executable downloads
- startup-service changes
- unusual Tree behavior
- model/tool permission escalation
- credential compromise indicators
- modified security settings

But Cedar should avoid notification fatigue.

Preferred behavior:

```text
normal event
→ log

interesting event
→ investigate

meaningful risk
→ warn

urgent risk
→ follow user-approved emergency policy
```

---

## 5. Anomaly Detection

Cedar should learn enough about normal system and Tree behavior to detect meaningful deviations.

Example:

```text
Maple normally accesses:
~/Documents
~/Pictures

Maple suddenly requests:
Cedar recovery store
```

This is unusual.

But Cedar should not assume:

```text
unusual = malicious
```

Instead:

```text
anomaly
+ context
+ user intent
+ expected Tree role
+ policy
+ evidence
→ assessment
```

---

## 6. Suspicious File / Malware Handling

Cedar should coordinate inspection of:

- downloads
- executables
- scripts
- archives
- email attachments
- Tree packages
- Skills
- documents
- model files where relevant

Example:

```text
New Skill
  ↓
verify provenance
verify hash/signature
inspect requested permissions
inspect contents
evaluate network access
  ↓
recommend:
allow / warn / sandbox / quarantine / reject
```

Actual scanning and containment should use deterministic tools and isolated environments.

---

## 7. Tree and Skill Trust

When new Trees or Skills are planted/installed, Cedar should inspect:

- source
- developer
- package provenance
- requested capabilities
- background services
- network requirements
- secret access
- update mechanisms
- dependencies
- model/runtime dependencies

Cedar should be able to recommend reduced privileges rather than only "allow" or "deny."

---

## 8. Credential and Secret Protection

Cedar should oversee:

- API keys
- authentication tokens
- recovery keys
- service secrets
- security credentials

Preferred architecture:

```text
Cedar requests:
"use credential profile X"
  ↓
Secret Broker
  ↓
credential applied directly
```

rather than:

```text
raw secret
→ Cedar prompt
→ tool
```

Cedar should know:

- that a credential exists
- what service it belongs to
- its scope
- its expiration
- which Tree is authorized to use it

without unnecessarily seeing the raw secret.

---

## 9. Account Security and Recovery

Cedar should help ordinary users with:

- password managers
- 2FA
- authenticator apps
- hardware security keys
- recovery codes
- account-recovery planning
- compromise response
- credential rotation
- suspicious-login alerts
- breach response

Cedar should be capable of explaining security in plain language.

---

## 10. Privacy Protection

Cedar should understand that security and privacy are related but distinct.

Relevant topics:

- telemetry
- third-party data collection
- metadata exposure
- local vs remote inference
- cloud processing
- application permissions
- network privacy
- data retention
- account linking
- cross-Tree information sharing

Cedar should explain tradeoffs without moralizing.

---

## 11. Network Security

Cedar may eventually supervise:

- firewall policy
- VPN state
- DNS privacy
- unusual outbound traffic
- open ports
- network trust
- Wi-Fi trust
- network segmentation
- future mesh/community-network security

The deterministic network engine should perform enforcement.

Cedar reasons about policy and risk.

---

## 12. Qubes Integration

Cedar should understand Qubes-specific concepts such as:

- qube isolation
- DisposableVMs
- qrexec
- templates
- App Qubes
- network qubes
- device assignment
- trusted vs untrusted domains

Boundary example:

```text
"Is this architecture secure?"
→ Cedar

"Why is qrexec throwing this error?"
→ McIntosh
```

---

## 13. Incident Response

Cedar should have a structured response model:

```text
detect
→ assess
→ contain if authorized
→ preserve evidence
→ investigate
→ remediate
→ recover
→ review
```

Cedar should prefer containment and evidence preservation before destructive action.

---

## 14. Backup and Recovery Security

Maple may organize and move backups.

Cedar should evaluate:

- encryption
- integrity
- recovery-key handling
- destination trust
- restoration safety

Conceptually:

```text
Maple → movement / organization
Cedar → security / integrity / trust
```

---

## 15. Audit Trail

Important Cedar actions and decisions should be auditable.

Example:

```yaml
event: permission_grant
tree: maple
permission: email.read
scope: personal
granted_by: user
policy_check: passed
```

Audit state should live outside model memory.

---

## 16. User-Facing Cedar

Cedar should be approachable.

Users may ask:

- "Is this website safe?"
- "Should I install this?"
- "Why does this app want this permission?"
- "Can this app see my photos?"
- "What does this security warning mean?"

Cedar should explain clearly and adapt technical depth to the user.

---

## 17. Background Cedar

Possible background responsibilities:

- monitor approved security events
- inspect new software
- track permission changes
- monitor authentication
- analyze anomalies
- check policy compliance
- watch sensitive areas
- monitor Tree behavior

This should be mostly event-driven and lightweight rather than requiring a large model to remain active.

---

## 18. Cedar Must Not Become a Surveillance Tree

Cedar should monitor only what is necessary to enforce user-defined security policy.

Principle:

> **Monitor the minimum information necessary.**

Cedar should not collect large amounts of unrelated personal content "just in case."

---

## 19. Cedar Is Not Cherry

Cedar does not need:

- Cherry's Diary
- deep personal conversation
- everyday scheduling
- emotional companionship
- primary life-management duties

Cedar may know security-relevant preferences only.

---

## 20. Cedar Is Not McIntosh

Cedar determines secure requirements and identifies security issues.

McIntosh diagnoses and repairs technical failures.

Example:

```text
Cedar:
"This service exposes a port that violates policy."

McIntosh:
"Here is why the configuration is broken and how to repair it."
```

---

## 21. Cedar Is Not Bristlecone Pine

Bristlecone builds.

Cedar audits.

```text
Bristlecone
→ new Tree / Skill / runtime component

Cedar
→ permissions review
→ attack-surface review
→ provenance review
→ security recommendation
```

---

# Planting Cedar — First-Install Security Onboarding

When the user first plants Cedar, Cedar should help secure the device.

The onboarding flow should be:

```text
Plant Cedar
  ↓
identify device / OS / environment
  ↓
inspect existing security posture
  ↓
detect existing security tools
  ↓
learn user risk/privacy preferences
  ↓
build prioritized hardening plan
  ↓
explain recommendations
  ↓
user approves changes
  ↓
guide / assist / automate
  ↓
verify
  ↓
create security baseline
```

Cedar should not blindly install a fixed security bundle.

It should understand what already exists.

---

## Security Apps and Services Knowledge

Cedar should understand categories including:

- password managers
- authenticator apps
- security keys
- firewalls
- VPNs
- encrypted DNS/privacy services
- anti-malware
- disk/file encryption
- backup tools
- browser privacy/security controls
- breach monitoring
- device recovery
- sandboxing
- isolation
- secure messaging
- secure email
- software-update systems

Cedar should avoid unnecessary duplication.

---

## Trainable Security Playbooks

Cedar should be teachable through structured **Security Playbooks** or Cedar Skills.

Example:

```text
Cedar Playbook:
Password Manager Setup

supports:
- Windows
- Linux
- Android
- iOS

steps:
1. Detect existing installation
2. Install if absent
3. Configure account
4. Enable 2FA
5. Verify recovery method
6. Verify integration
7. Record successful setup
```

This allows Cedar procedures to be updated without retraining the entire LLM.

---

## Guide / Assist / Automate Modes

### Guide

```text
Cedar explains
→ user performs
→ Cedar verifies
```

### Assist

```text
Cedar prepares
→ user performs privileged step
→ Cedar continues
```

### Automate

```text
Cedar
→ trusted playbook
→ deterministic configurator
→ verification
```

---

## Security Baseline

After onboarding, Cedar should create a structured baseline such as:

```yaml
security_baseline:
  disk_encryption: enabled
  firewall: enabled
  password_manager: configured
  two_factor_auth: configured
  backup: configured
  automatic_updates: enabled
  browser_hardening: complete
  recovery_plan: complete
```

Cedar can later detect drift.

---

# User Sovereignty and Risk Tolerance

Cedar should be **security-conscious without being paternalistic**.

Different users may knowingly accept:

- tracking
- unofficial software
- suspicious websites
- less-private services
- risky permissions
- convenience over maximum lockdown

The user remains the final authority.

Preferred default:

```text
Cedar detects risk
→ explains risk
→ estimates likely consequences
→ offers safer options
→ user chooses
```

Not:

```text
Cedar dislikes risk
→ Cedar blocks owner
```

---

## Risk Preferences

Cedar should support specific preferences such as:

```yaml
risk_preferences:
  unofficial_apps: warn_but_allow
  unknown_websites: warn_only
  telemetry: generally_allow
  remote_file_processing: ask_first
  unsigned_executables: strong_warning
  credential_exposure: strict
  automatic_quarantine: disabled
```

Users may be relaxed in one area and strict in another.

---

## Accepted Risk vs Unexpected Compromise

If a user knowingly installs an unofficial application, Cedar should remember the accepted scope.

Example:

```text
User accepted:
unsigned source
network access
```

That does **not** automatically authorize:

```text
password-vault access
hidden persistence
unrelated-file access
credential exfiltration
```

Cedar must distinguish:

```text
known accepted risk
```

from:

```text
new behavior outside accepted scope
```

---

## Warning Severity

Cedar should calibrate warnings:

```text
Informational
Caution
Strong Warning
Critical
```

If everything is "critical," users will stop trusting Cedar.

---

## User-Defined Security Profiles

Possible starting templates:

```text
Convenience-first
Balanced
Privacy-focused
Strict
Custom
```

These are starting points, not permanent boxes.

---

## Cedar Authority Levels

### Observe
Read permitted security state.

### Warn
Explain risk.

### Recommend
Propose safer action.

### Assist
Perform user-approved remediation.

### Enforce User Policy
Automatically apply rules the user explicitly enabled.

### Emergency Protection
Only narrowly defined preauthorized actions.

The LLM may never invent its own emergency authority.

---

# Step 2 — Intelligence Requirements

Cedar needs more than cybersecurity knowledge.

It needs:

```text
security reasoning
+ calibrated risk
+ user-policy reasoning
+ procedural reliability
+ tool discipline
+ uncertainty
+ evidence synthesis
+ restraint
```

---

## 1. Security Reasoning — Extremely High

Cedar should reason about:

- suspicious software
- permissions
- network behavior
- compromise
- privacy exposure
- credentials
- security configuration
- malware indicators
- software provenance
- isolation
- user risk tolerance

It should ask:

```text
What happened?
What evidence exists?
What is normal?
What did the user knowingly allow?
What could happen next?
How confident are we?
```

---

## 2. Risk Calibration — Extremely High

Cedar must distinguish:

```text
slightly unusual
meaningfully suspicious
strong evidence of compromise
```

A useful internal model may combine:

```text
likelihood
× impact
× confidence
× user tolerance
```

---

## 3. User-Risk-Profile Reasoning — Extremely High

Cedar must reason from specific preferences rather than one global security level.

---

## 4. Procedural Instruction-Following — Extremely High

Cedar needs exceptional discipline with Security Playbooks:

```text
detect platform
→ inspect state
→ follow correct procedure
→ ask approval
→ execute approved actions
→ verify
→ record
```

It must stop safely when preconditions fail.

---

## 5. Tool Use and Automation — Extremely High

Cedar may use tools to:

- inspect firewall state
- inspect update status
- query permissions
- inspect processes
- inspect ports
- review logs
- verify signatures
- compute hashes
- isolate environments
- configure approved settings
- revoke permissions
- quarantine

Cedar must never fabricate security findings or tool output.

---

## 6. Security Product / Service Knowledge — Very High

Cedar should understand the security ecosystem and recognize functional equivalence.

If a good existing tool is already present, Cedar should not blindly recommend another.

---

## 7. Platform Awareness — Very High

Cedar must adapt across:

- Qubes OS
- Linux
- Windows
- macOS
- Android
- iOS
- servers
- routers
- other platforms later

---

## 8. Anomaly Reasoning — Very High

Anomaly does not equal attack.

Cedar must determine whether a deviation is:

- expected
- user-authorized
- explainable
- suspicious
- urgent

---

## 9. Permission / Least-Privilege Reasoning — Extremely High

Cedar should answer:

> **What is the minimum access required to accomplish this task?**

This should be a major benchmark category.

---

## 10. Privacy Reasoning — Very High

Cedar should understand:

- data leaving device
- metadata exposure
- telemetry
- retention
- third-party processing
- local vs remote inference
- permission scope
- cross-Tree sharing

---

## 11. Incident-Response Planning — Very High

Preferred flow:

```text
detect
→ assess confidence/severity
→ contain if authorized
→ preserve evidence
→ investigate
→ remediate
→ recover
→ review
```

---

## 12. Security Communication — Very High

Cedar should explain risks clearly to ordinary users while still being able to provide technical evidence to advanced users.

---

## 13. Warning Calibration — Extremely High

Warning severity should remain consistent and meaningful.

---

## 14. Uncertainty Handling — Extremely High

Cedar must be comfortable returning:

```text
known
likely
possible
unknown
insufficient evidence
```

Security uncertainty must not be converted into false certainty.

---

## 15. Evidence Synthesis — Very High

Cedar may combine:

- malware scanner output
- firewall logs
- audit logs
- permission state
- package metadata
- process lists
- network activity
- signatures
- reputation data
- user context

It should weight evidence according to source quality.

---

## 16. Security Source Evaluation — Very High

Cedar should distinguish:

```text
official advisory
trusted security researcher
CVE database
vendor documentation
random forum post
unknown blog
```

---

## 17. Multi-Step Investigation — Very High

Example:

```text
suspicious executable
→ identify
→ hash
→ inspect provenance/signature
→ inspect requested permissions
→ inspect behavior
→ compare with baseline
→ assess risk
```

---

## 18. Code / Script Understanding — High

Cedar should understand enough:

- shell
- PowerShell
- Python
- configuration
- package manifests
- permissions
- scripts

to identify suspicious behavior.

Deep coding remains Bristlecone's role.

---

## 19. Malware Analysis — High, Potentially Specialist

Cedar should understand malware concepts, but deep reverse engineering may be delegated to a specialist.

---

## 20. Network Reasoning — High to Very High

Cedar should understand:

- inbound/outbound
- ports
- protocols
- DNS
- VPN
- firewall
- segmentation
- unusual destinations
- isolation

---

## 21. Qubes / Isolation Reasoning — Very High

Given The Forest's deployment direction, Cedar should be particularly strong at Qubes-style compartmentalization.

---

## 22. Long Context — Medium to High

Cedar may inspect long logs and incident timelines, but targeted retrieval should beat giant prompt dumps.

---

## 23. Memory Behavior — High

Cedar memory should store only security-relevant durable context such as:

- user risk preferences
- approved applications
- accepted-risk exceptions
- device baseline
- Tree permissions
- known normal services
- onboarding status

Cedar should avoid unrelated personal memory.

---

## 24. Baseline / Drift Reasoning — Very High

Cedar should understand when a baseline has changed and whether that change is intentional or suspicious.

---

## 25. Autonomy — Carefully Limited

Capability does not equal permission.

Default:

```text
observe
warn
recommend
assist
```

Enforcement requires user-defined policy.

---

## 26. Personality — Medium

Cedar should be:

- calm
- reassuring
- serious when necessary
- concise in incidents
- patient when teaching
- non-alarmist
- nonjudgmental
- protective without being controlling

The goal is:

> **If Cedar is concerned, the user should pay attention.**

---

## Intelligence Priority Map

```text
Security Reasoning             ★★★★★
Risk Calibration               ★★★★★
User-Risk-Profile Reasoning    ★★★★★
Procedural Reliability         ★★★★★
Tool / Automation Reliability  ★★★★★
Permission Reasoning           ★★★★★
Uncertainty Handling           ★★★★★
Warning Calibration            ★★★★★
Evidence Synthesis             ★★★★★
Platform Awareness             ★★★★☆
Privacy Reasoning              ★★★★☆
Incident Response              ★★★★☆
Security Communication         ★★★★☆
Anomaly Detection              ★★★★☆
Security Product Knowledge     ★★★★☆
Baseline / Drift Reasoning     ★★★★☆
Network Reasoning              ★★★★☆
Code / Script Understanding    ★★★★☆
Long Context                   ★★★☆☆
General Coding                 ★★★☆☆
Warmth / Personality           ★★★☆☆
```

---

# Step 3 — Operational Constraints

## 1. Cedar Monitor + Cedar Reasoner

Working architecture:

```text
Cedar Monitor
→ tiny / event-driven
→ frequently available
→ baseline drift
→ permission changes
→ alerts
→ simple classification

Cedar Reasoner
→ on demand
→ investigation
→ risk assessment
→ hardening
→ incident response
→ evidence synthesis
```

---

## 2. Deterministic Security Engine

Cedar should work through a deterministic policy/security engine.

```text
Cedar Reasoner
  ↓
Security Policy Engine
  ↓
approved deterministic capabilities
```

Possible capabilities:

- firewall
- permissions
- secret access
- quarantine
- process controls
- network isolation
- package verification
- logging
- recovery
- encryption

---

## 3. Capability ≠ Authority

Example:

```text
Cedar knows how to block network access.
User policy = warn-only.
Result = warn, do not block.
```

This separation must be architectural.

---

## 4. Very Low Idle Resource Usage

Background monitoring should mostly use:

- OS events
- firewall events
- permission events
- authentication logs
- Forest event logs
- lightweight anomaly rules

Large reasoning models should wake only when needed.

---

## 5. Foreground Resource Awareness

Routine Cedar jobs should yield to normal foreground activity.

Example:

```text
scheduled scan + user gaming
→ throttle/defer
```

But:

```text
credible active compromise
→ higher priority investigation
```

Resource priority still does not expand Cedar's authority.

---

## 6. Security Workload Classes

### Passive Monitoring
Lightweight, event-driven.

### Routine Maintenance
Inventory, updates, baseline checks, scheduled scans.

### Investigation
Triggered by suspicious events.

### Incident Response
Higher urgency, but still user-policy constrained.

---

## 7. Do Not Scan Everything Constantly

Prefer:

```text
event-driven monitoring
+ incremental checks
+ sensitive scopes
+ targeted investigations
```

Full scans should be deliberate and intelligently scheduled.

---

## 8. Risk Preferences Affect Operations

Known accepted risk should not cause Cedar to constantly fight the user.

Example:

```text
unofficial app accepted
→ monitor for behavior beyond accepted scope
```

---

## 9. Accepted-Risk Registry

Structured exception example:

```yaml
accepted_risk:
  object: app_xyz
  condition: unofficial_source
  user_choice: allow
  allowed_scope:
    - network_access
    - downloads_folder
  not_allowed:
    - password_vault
    - cedar_store
```

---

## 10. First-Install Hardening Should Be Staged

```text
identify platform
→ assess
→ learn risk preferences
→ identify urgent gaps
→ propose plan
→ apply approved changes
→ verify
→ baseline
→ optional advanced hardening later
```

---

## 11. Security Playbooks Live Outside Model Weights

Possible structure:

```text
cedar_playbooks/
├── qubes_baseline.yaml
├── windows_baseline.yaml
├── linux_baseline.yaml
├── android_baseline.yaml
├── password_manager_setup.yaml
└── account_recovery.yaml
```

This keeps procedures updateable without retraining the model.

---

## 12. Playbook Version Awareness

Cedar should know the supported platform/version range and avoid blindly applying stale procedures.

---

## 13. Platform-Specific Workshop Loading

Cedar should load only relevant platform capabilities.

Example:

```text
Qubes Workshop
├── qrexec policy
├── qube state
├── device assignment
├── network qube
└── template inspection
```

---

## 14. Qubes Isolation as Architecture

For Qubes deployments, Cedar should be strongly compartmentalized with tightly scoped qrexec access, minimal networking, and carefully controlled privileged paths.

---

## 15. Secrets Outside LLM Context

Hard rule where practical:

```text
Cedar requests credential profile
→ Secret Broker
→ credential applied
```

Raw secrets should not enter prompt context.

---

## 16. Security Context Minimization

Cedar should receive only the minimum relevant evidence.

A suspicious file investigation should not automatically grant unrelated user files, email, or Cherry Diary access.

---

## 17. Incident Evidence Persists Outside the Model

Structured incident record:

```text
Incident cedar-XXXX
├── detection
├── evidence
├── containment
├── user decisions
├── remediation
└── recovery
```

---

## 18. Preserve Evidence Before Destruction

Preferred:

```text
detect suspicious file
→ record metadata/hash
→ isolate/quarantine
→ preserve evidence
```

rather than immediate deletion.

---

## 19. Rollback for Configuration Changes

Hardening changes should capture previous state where practical.

If something breaks, Cedar should restore or hand the technical failure to McIntosh.

---

## 20. Cedar ↔ McIntosh Handoff

```text
Cedar defines secure constraint
→ McIntosh repairs within constraint
```

If the constraint makes a desired workflow impossible, the user decides the tradeoff.

---

## 21. Cedar ↔ Maple Resource Coordination

Cedar scans and Maple reorganizations should not unnecessarily compete for disk, CPU, or the same files.

---

## 22. Offline Functionality

Offline Cedar should still support:

- local policy
- baseline checks
- local logs
- local file analysis
- permission review
- local hardening
- local sandboxing
- Cedar Oil
- recovery

Internet enhances current-threat research but is not required for core security.

---

## 23. Minimum Necessary Remote Data

If Cedar uses online security services, it should know whether it sends:

- hash
- filename
- metadata
- full sample

and follow user policy.

---

## 24. Local Evidence + Remote Public Research

Preferred:

```text
local Cedar identifies software/version/hash
→ remote search for public advisories
```

rather than uploading private evidence.

---

## 25. Model Escalation

Potential architecture:

```text
Cedar Monitor / Small
→ routine events
→ simple warnings
→ baseline drift

Cedar Reasoner / Big
→ investigations
→ complex hardening
→ security architecture
→ incident response
```

Specialist models may handle malware, code, phishing, or network analysis.

---

## 26. Big Cedar Should Not Stay Resident

The stronger reasoner wakes for difficult work and unloads afterward.

Monitoring continues independently.

---

## 27. Quantization Needs Strict Validation

Test effects on:

- severity calibration
- false positives
- false negatives
- policy obedience
- permissions
- uncertainty
- structured output
- security terminology
- identifiers

---

## 28. Battery / Mobile Behavior

On mobile, Cedar should avoid:

- heavy constant scans
- frequent model wakeups
- unnecessary remote calls
- battery drain

Use event-driven monitoring and scheduled checks.

---

## 29. Auditability

Every meaningful action should answer:

```text
What happened?
Why?
What evidence?
What policy allowed it?
What did Cedar do?
Was the user asked?
Can it be reversed?
```

---

## 30. User Override

For normal policies:

```text
Cedar warns
→ user overrides
→ accepted risk recorded
→ work continues
```

Users must be able to change stricter automation later.

---

## 31. No Nagging

Once the user knowingly accepts a risk, Cedar should not repeatedly warn unless:

- risk increases
- behavior changes
- new evidence appears
- exception expires
- user asks

---

# Sacrificial Cedar / Disposable Security Labs

Cedar should support sacrificial analysis of suspicious files and code.

Important architectural rule:

> **Suspicious code should never run inside Cedar Core.**

Instead:

```text
Cedar Core
  ↓
spawn Disposable Cedar Lab
  ↓
inject suspicious sample
  ↓
observe
  ↓
export filtered evidence
  ↓
destroy lab
```

The disposable environment must contain:

```text
✕ Cedar secrets
✕ user credentials
✕ Cherry Diary
✕ unrestricted user files
✕ Forest control authority
✕ persistent trust
```

Networking should be disabled or highly restricted by default.

This is especially compatible with Qubes DisposableVMs.

---

## Filtered Evidence Channel

Evidence should leave the lab through a restricted interface.

Examples:

- process created
- file modified
- destination contacted
- permission requested
- persistence attempted
- hash
- exit behavior

Potentially dangerous artifacts should go to quarantine, not directly back into Cedar Core.

---

# Cedar Self-Destruct and Restore

If Cedar Core itself is suspected of compromise, Cedar should support controlled self-recovery.

"Self-destruct" should mean:

```text
1. revoke Cedar sessions
2. revoke temporary credentials/tokens
3. isolate Cedar from Forest control paths
4. preserve external incident evidence
5. destroy suspect volatile/runtime state
6. verify trusted recovery baseline
7. recreate Cedar from known-safe checkpoint
8. reattach only validated persistent state
9. resume carefully
```

It should **not** mean destructively deleting Cedar's only copy or audit evidence.

---

## Multiple Known-Safe Checkpoints

Preferred recovery store:

```text
Cedar Recovery Store
├── current trusted baseline
├── previous known-safe checkpoint
├── older known-safe checkpoint
└── factory/planted baseline
```

Each should include:

```text
hash
signature/integrity record
creation time
Cedar version
security-policy version
playbook version
```

If the latest backup is compromised, Cedar can roll farther back.

---

# Cedar Oil — Encryption Capability

**Cedar Oil** is the user-facing name for Cedar's encryption capability.

Hard rule:

> **Cedar Oil is branding, not a custom encryption algorithm.**

Preferred:

```text
User:
"Put Cedar Oil on this folder."
  ↓
Cedar
  ↓
Forest encryption capability
  ↓
mature audited cryptographic implementation
  ↓
encrypted data
```

Cedar Oil may protect:

- files
- folders
- archives
- Forest exports
- backups
- Tree state
- recovery packages
- removable storage

Keys should be managed outside LLM context through a secure broker/store.

---

# Cedar Salvage

Cedar should safely recover clean data from:

- damaged filesystems
- infected folders
- corrupted archives
- compromised Tree data
- damaged backups
- suspicious storage

Preferred flow:

```text
suspect data
  ↓
isolated recovery environment
  ↓
read-only inspection where practical
  ↓
recover candidate data
  ↓
quarantine
  ↓
scan + verify
  ↓
clean staging area
  ↓
user-approved restoration
```

Maple can reorganize restored files after Cedar declares them safe enough to leave quarantine.

---

# Secure Disposal

When the user explicitly requests irreversible destruction:

```text
identify exact scope
→ determine whether salvage is needed
→ backup if requested
→ final authorization
→ platform-appropriate secure disposal
→ verify
→ audit
```

Cedar should never interpret a vague cleanup request as authorization for irreversible deletion.

---

# Forest Fire Protocol

Cedar should support a catastrophic Forest-wide recovery mode tentatively called the **Forest Fire Protocol**.

It is intended for a spreading Forest compromise that threatens other Trees or the user's device.

Conceptual flow:

```text
FOREST-WIDE COMPROMISE
  ↓
Cedar invokes authorized Forest Fire actions
  ↓
isolate Forest networking
  ↓
freeze/terminate compromised Tree sessions
  ↓
revoke temporary credentials
  ↓
preserve external incident evidence
  ↓
identify trustworthy Tree state
  ↓
salvage validated data
  ↓
create protected recovery package
  ↓
destroy compromised runtime instances
  ↓
restore Trees from known-safe checkpoints
  ↓
rotate affected credentials
  ↓
verify clean Forest
  ↓
resume carefully
```

Important:

```text
Forest Fire
≠ wipe the user's computer
```

It means:

```text
destroy compromised Forest runtime state
+ isolate contamination
+ preserve user data
+ salvage clean Tree state
+ rebuild from verified backups
```

---

## Tree Recovery Packages

A Tree recovery package may contain:

```text
Tree configuration
approved Skills
permissions
personality/config
safe operational memory
model-binding information
safe Leaves/references
integrity metadata
```

Contaminated runtime state should not automatically be restored.

Example:

```text
model weights        → verify
Tree configuration   → verify
Leaf data            → inspect/salvage
runtime KV/session   → discard
temporary files      → discard/quarantine
credentials          → rotate/reissue
```

---

## Forest Fire Authority

Forest Fire must be tightly controlled through user-defined policy.

Example:

```yaml
forest_fire_policy:
  auto_isolate_network: true
  auto_revoke_temp_tokens: true
  auto_destroy_runtime: false
  preserve_user_files: always
  preserve_incident_evidence: true
  require_user_for_full_rebuild: true
```

Users can choose more or less aggressive emergency behavior.

---

# Step 4 — Forest-Specific Requirements

## 1. Cedar Sits Beside the Trees, Not Above the User

User policy remains the highest authority.

---

## 2. Forest-Wide Security Policy Engine

The policy engine should understand:

```text
Tree
Capability
Resource
Scope
Duration
Risk level
User approval
Current policy
```

Cedar reasons.

The deterministic engine grants/denies.

---

## 3. User Security Profile / Accepted-Risk Registry

Cedar should keep structured preferences and accepted exceptions outside model memory.

---

## 4. Security Profiles Are Templates

Convenience-first, Balanced, Privacy-focused, Strict, and Custom may exist as starting templates.

They must not become permanent restrictions.

---

## 5. Cedar-Specific Workshops

Example investigation Workshop:

```text
file-inspect
hash
signature-check
process-inspect
network-observe
quarantine
```

Example onboarding Workshop:

```text
system-inventory
security-baseline
firewall
updates
encryption
account-security
security-playbooks
```

Only relevant tools should be loaded.

---

## 6. Shared Forest Capabilities

General capabilities such as web research, file lookup, clarify, software inventory, and notifications can be shared.

Privileged capabilities such as quarantine remain Cedar-specific and tightly permissioned.

---

## 7. Security Playbook System

Suggested structure:

```text
Cedar Playbooks/
├── Qubes/
├── Windows/
├── Linux/
├── Android/
├── Accounts/
└── Applications/
```

Playbooks should define:

- supported platform/version
- preconditions
- checks
- actions
- verification
- rollback
- required permissions

---

## 8. Playbook Trust and Provenance

Each playbook should eventually include:

```text
source
author
version
last reviewed
supported platform
signature/hash
required permissions
```

Unknown/unverified playbooks should not silently execute.

---

## 9. Forest Security Baseline

Cedar's baseline should include device and Forest state:

- encryption
- firewall
- updates
- password manager
- backups
- security keys
- Tree permissions
- installed Trees
- trusted Skills
- network permissions
- policy version
- accepted-risk exceptions

---

## 10. Drift Detection

Changed does not automatically mean dangerous.

Cedar should investigate context before escalation.

---

## 11. Inter-Tree Permission Boundaries

Important rule:

> **Context access, tool access, data access, and system authority are separate permissions.**

---

## 12. Tree Installation Security

Before planting a new Tree, Cedar should inspect:

- provenance
- model dependencies
- tools
- files
- network access
- secret access
- background services
- update mechanism
- Skill dependencies

---

## 13. Skill Security

Skills should be inspected for requested privileges before activation.

---

## 14. Capability Manifests

Trees/Skills should ideally declare machine-readable required and optional capabilities.

Cedar can compare:

```text
declared behavior
vs
observed behavior
```

Unexpected expansion is a security signal.

---

## 15. Cross-Tree Anomaly Detection

Cedar should reason from:

```text
Tree role
+ permission manifest
+ historical baseline
+ current task
+ user-approved exceptions
```

---

## 16. Sacrificial Cedar Environments

Disposable labs are formal Cedar capabilities and must remain isolated from Cedar Core and Forest authority.

---

## 17. Disposable Analysis Profiles

Possible labs:

```text
Document Lab
Script Lab
Application Lab
Network Lab
```

Different suspicious content may require different isolation.

---

## 18. Restricted Network Modes

Possible sandbox network levels:

```text
Offline
Simulated network
Restricted outbound
Full isolated Internet
```

Full access should be the highest-risk mode.

---

## 19. Filtered Evidence Channel

Only validated structured evidence should return directly to Cedar Core.

---

## 20. Cedar Self-Recovery

Cedar Core should be recreatable from trusted verified baselines after suspected compromise.

---

## 21. Multiple Safe Checkpoints

Never rely on a single recovery point.

---

## 22. Recovery Store Separation

Recovery state must be protected outside the Cedar runtime it may need to replace.

---

## 23. External Audit / Incident Store

Audit evidence must survive Cedar destruction and restoration.

---

## 24. Security Event Bus

The Forest may use a structured security event bus so Cedar subscribes only to relevant events rather than observing everything.

---

## 25. Privacy-Minimized Observation

Metadata should be preferred over full content where full content is unnecessary.

---

## 26. No Cherry Diary Access

Hard boundary:

```text
Cherry Diary ✕ Cedar
```

---

## 27. Secret Broker

Trees should request credential profiles without receiving raw credentials whenever practical.

---

## 28. Credential Scope and Rotation

Cedar should understand credential ownership, scope, expiration, last use, and revocation.

Compromise should revoke only affected credentials where possible.

---

## 29. Cedar ↔ Cherry

Cherry may delegate security evaluations to Cedar while remaining the normal conversational interface.

---

## 30. Cedar ↔ Maple

Common interactions:

- downloads
- suspicious email attachments
- backups
- file permissions
- remote media processing
- recovered files

---

## 31. Cedar ↔ McIntosh

Cedar defines secure constraints.

McIntosh repairs within them.

---

## 32. Cedar ↔ Bristlecone Pine

Bristlecone builds.

Cedar audits.

---

## 33. Forest Resource Scheduling

Routine Cedar scans should yield to foreground activity.

Active incidents may receive higher compute priority without increasing Cedar's security authority.

---

## 34. Security Notifications

Suggested behavior:

```text
normal → log
accepted risk → quiet
new caution → notify
strong warning → foreground alert
critical active incident → urgent alert
```

---

## 35. Explanation Trail

The user should be able to ask:

> Why did Cedar warn me?

and receive:

```text
observed behavior
+ relevant policy
+ evidence
+ confidence
+ potential impact
```

---

## 36. Structured Security Outputs

Example:

```yaml
assessment:
  severity: caution
  confidence: medium
  reason:
    - unsigned_binary
    - unknown_source
  user_policy: warn_but_allow
  recommended_action: sandbox_first
  enforcement: none
```

---

## 37. Explicit Uncertainty

Valid result:

```yaml
verdict: unknown
confidence: low
next_step: inspect_behavior_in_disposable_lab
```

Cedar should not force every case into safe/dangerous.

---

## 38. Local-First Security Knowledge + Optional Current Research

Core local state:

- playbooks
- policies
- baselines
- trusted applications
- permissions
- security docs

Rapidly changing threat information can be retrieved externally when allowed.

---

## 39. Updated Threat Knowledge Outside Model Weights

Preferred:

```text
Cedar reasoning model
+ current advisories
+ versioned playbooks
+ local policy
```

rather than relying only on stale static model knowledge.

---

## 40. Cedar Identity Is Model-Independent

Hard architectural principle:

```text
Cedar identity
≠ model weights
≠ runtime session
```

The following must survive model replacement:

- security policies
- accepted risks
- baselines
- incident history
- playbooks
- recovery checkpoints
- permissions
- audit records

---

# Step 5 — Origin, Licensing, Provenance, and Trust Requirements

Cedar's Step 5 is stricter than other Trees because Cedar sits close to root trust.

---

## 1. Open Weights Strongly Preferred

Cedar's core reasoning models should ideally be:

- open-weight
- locally runnable
- quantizable
- fine-tunable
- inspectable
- well documented
- runtime-portable

Core Cedar should not depend permanently on:

```text
remote API
vendor account
vendor availability
vendor policy
```

---

## 2. Provenance Is a Major Scoring Category

For every candidate:

```text
Developer:
Country:
Base architecture:
Training lineage:
Derived from:
License:
Weights available:
Model card:
Security documentation:
Known dependencies:
```

Unclear lineage should count more heavily against Cedar candidates.

---

## 3. Non-Chinese Preference

Current Forest rule:

> **Prefer non-Chinese-developed models and technologies when practical.**

This remains a strong preference, not an absolute ban.

For Cedar, provenance/origin should receive especially strong weight because Cedar sits in a privileged security role.

---

## 4. Core Security Must Work Offline

Cedar should not require Internet access for:

- policy
- permissions
- baseline checks
- local analysis
- Cedar Oil
- quarantine
- self-recovery
- Forest Fire
- secrets
- sandboxing
- incident records

Internet enhances threat intelligence.

---

## 5. No Mandatory Upload of Suspicious Files

Default:

```text
suspicious file
→ local inspection
→ local disposable lab
```

If an online service is used, Cedar should know whether it sends:

```text
hash
filename
metadata
full sample
```

and follow user policy.

---

## 6. Security Data-Source Licenses Need Separate Review

Potential sources:

- vulnerability databases
- reputation feeds
- malware signatures
- phishing lists
- package-security feeds
- breach data
- vendor advisories

Some may restrict:

- redistribution
- commercial use
- automated access
- caching
- mirroring

Each must be evaluated independently.

---

## 7. Mature Security Software Over Novel Security Primitives

For privileged deterministic components, prefer mature, reviewed technologies for:

- cryptography
- firewall
- secrets
- hashing
- signatures
- backup verification
- secure deletion
- sandboxing
- archive inspection

Cedar should innovate in orchestration and usability, not foundational cryptography.

---

## 8. Cedar Oil Must Never Use Homemade Crypto

Hard rule:

```text
CEDAR OIL
→ Forest encryption interface
→ established cryptographic standards
→ mature audited implementation
```

Never:

```text
CEDAR OIL
→ custom mystery cipher
```

---

## 9. Key Management and Portability

Encrypted backups must remain recoverable even if one specific application disappears.

Prefer documented/open recovery paths.

---

## 10. Forest Fire Recovery Must Be Vendor-Independent

Known-safe Forest state should be recoverable using:

```text
documented recovery format
+ hashes/signatures
+ encrypted backups
```

even if the original:

- LLM
- model runtime
- server
- OS environment
- vendor

is unavailable.

---

## 11. Recovery Formats Should Be Open

Possible Tree Recovery Package:

```text
manifest
configuration
permissions
Skills
safe memory
Leaves/references
model bindings
integrity records
recovery metadata
```

Avoid opaque vendor-only databases where practical.

---

## 12. Cryptographic Integrity Metadata

Safe checkpoints should use established cryptographic:

- hashes
- signatures
- authenticated metadata
- verification libraries

The LLM should not invent integrity logic.

---

## 13. Sandbox Technology Requires Strong Isolation

Cedar's sacrificial environment should use real isolation boundaries with strong:

- privilege separation
- network controls
- filesystem separation
- escape resistance
- maintenance history

Qubes DisposableVM-style isolation is a strong conceptual fit.

---

## 14. Disposable Analysis Backends Must Be Replaceable

The Forest should expose a semantic capability such as:

```text
analyze_suspicious_sample()
```

while the implementation may change between:

- Qubes DisposableVM
- full VM sandbox
- dedicated analysis host
- other strong isolation backend

---

## 15. Malware Scanner Licensing

Scanners and signature databases must be reviewed separately.

"Free" does not automatically mean suitable for The Forest.

---

## 16. Fine-Tuning Rights Are Important

Potential Cedar training targets:

- risk calibration
- warning severity
- user sovereignty
- accepted-risk interpretation
- permission reasoning
- Forest threat models
- Qubes security
- playbook selection
- incident triage
- structured findings

Prefer model families with clear rights for:

- LoRA/adapters
- derivatives
- local deployment
- commercial use
- redistribution

---

## 17. Cedar Should Learn Operationally Without Retraining

Much Cedar knowledge should come from:

```text
Security Playbooks
policy rules
threat knowledge
device profiles
Forest security Skills
```

rather than retraining model weights whenever a procedure changes.

---

## 18. Quantization Requires Strict Validation

Test whether quantization changes:

- severity
- uncertainty
- false positives
- false negatives
- policy obedience
- permissions
- structured output
- evidence synthesis
- identifiers

A faster Cedar that becomes more alarmist is not acceptable.

---

## 19. Closed Models as Optional Advisers

Optional remote experts may be used for scrubbed/non-sensitive questions.

The local Cedar remains the actual security authority.

---

## 20. Minimum Necessary Context for Remote Advisers

Do not send:

- credentials
- identity
- unrelated logs
- private documents
- private incident evidence

when a public security question can be answered without them.

---

## 21. Avoid Surveillance Dependencies

Cedar should avoid models/tools that require unnecessary vendor telemetry or detailed security-state uploads.

---

## 22. Trustworthy Update Mechanisms

Prefer dependencies with:

- signed releases
- verifiable packages
- documented channels
- clear provenance
- inspectable builds where practical

---

## 23. Model Updates Are Security-Sensitive

New Cedar model deployment should follow:

```text
verify provenance
→ run Cedar benchmark
→ compare behavior
→ approve
→ deploy
```

Never assume newer automatically means safer.

---

## 24. Cedar Dependency Inventory

Cedar should eventually maintain an SBOM-like view:

```yaml
cedar_stack:
  reasoning_model: ...
  monitor_model: ...
  crypto_library: ...
  sandbox_backend: ...
  malware_scanner: ...
  policy_engine: ...
  secret_broker: ...
  recovery_tool: ...
```

with version, source, license, and integrity metadata.

---

## 25. Cedar Should Audit Cedar

Expected components should be compared with currently installed components.

Unexpected changes to privileged dependencies should trigger investigation.

The most trusted verification mechanisms should remain outside Cedar Core where practical.

---

## 26. Recovery Dependencies Should Be Simpler Than Cedar

Preferred:

```text
minimal trusted recovery mechanism
→ verify baseline
→ restore Cedar
```

not:

```text
full Cedar installation required to restore Cedar
```

Smaller root-trust components are easier to verify.

---

## 27. Secure Deletion Requires Platform Awareness

Storage may involve:

- SSD wear leveling
- snapshots
- copy-on-write
- encryption
- cloud sync
- virtual disks

"Secure delete" must use platform-appropriate deterministic mechanisms, not generic LLM instructions.

---

## 28. Salvage Tools Should Preserve Originals

Preferred:

```text
suspect source
→ read-only where practical
→ recover to separate destination
```

Recovery should not modify the original evidence unnecessarily.

---

## 29. User Data Ownership

Cedar's models/tools should not claim rights over:

- encrypted data
- recovered data
- incident evidence
- backups
- Tree state
- security reports
- user documents

---

## 30. Cedar Component Rating Template

For Step 6, candidates should be scored with something like:

```text
MODEL / TOOL:
Developer:
Origin:
License:
Open weights/source:
Local:
Commercial use:
Fine-tuning:
Quantization:
Redistribution:
Runtime support:

SECURITY TRUST:
Provenance:
Documentation:
Maintenance:
Auditability:
Offline support:
Telemetry:
Cloud dependency:

FOREST FIT:
Structured output:
Tool use:
Policy adherence:
Risk calibration:
Qubes compatibility:
Replaceability:
Recovery compatibility:
```

---

## 31. Trust Tiers

Potential dependency tiers:

```text
Tier 0 — Recovery / Root Trust
Tier 1 — Privileged Security Core
Tier 2 — Security Analysis Tools
Tier 3 — Optional Intelligence / Research
```

### Tier 0
- checkpoint verification
- recovery bootstrap
- root integrity mechanisms

Highest scrutiny.

### Tier 1
- policy engine
- secret broker
- Cedar Core runtime
- Cedar Oil backend

Very high scrutiny.

### Tier 2
- malware scanners
- document inspectors
- sandbox telemetry

Important, but should not automatically control Forest authority.

### Tier 3
- web research
- reputation APIs
- optional remote reasoners

Least trusted.

---

## 32. Cedar Must Not Depend on One Model Vendor

Hard rule:

```text
Cedar identity
≠ Cedar model
```

If a model's license changes, disappears, becomes unsupported, or behaves poorly, Cedar should be replaceable without rebuilding the entire security architecture.

---

## 33. Near-Disqualifying Conditions

Potential hard failures:

```text
Core Cedar requires permanent cloud connection        ✕
Model license blocks needed local use                  ✕
Cannot legally fine-tune/quantize where required       ✕
Security core uploads private files automatically      ✕
Unknown provenance for privileged layer                ✕
Homemade cryptography required                          ✕
Recovery requires one proprietary vendor               ✕
User cannot export/recover protected data               ✕
```

---

# Current Cedar Working Definition

> **Cedar is The Forest's security, trust, privacy, permission, encryption, incident-response, and recovery Tree. Cedar should help users harden their devices during first install through trainable, versioned Security Playbooks; understand the user's individual tolerance for privacy loss and accepted risk; warn and advise rather than paternalistically restrict; enforce only explicit user-defined policy; supervise Tree/Skill permissions; protect secrets; monitor anomalies; and coordinate incident response. Cedar should support Cedar Oil encryption, isolated sacrificial analysis environments, safe data salvage, controlled secure disposal, last-known-safe self-recovery, and a Forest Fire protocol for catastrophic Forest-wide compromise. Cedar must remain local-first, privacy-minimized, auditable, recoverable, model-independent, and subordinate to user sovereignty. The closer a component is to root trust and recovery, the smaller, simpler, more auditable, and less vendor-dependent it should be.**

---

# Current Cedar Architecture

```text
                           USER
                            │
                  preferences / policy
                            │
                            ▼
                          CEDAR
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
     Monitor/Small      Reasoner/Big       Specialists
          │                 │                  │
          └─────────────────┼──────────────────┘
                            ▼
                  Security Policy Engine
                            │
     ┌──────────────┬───────┼────────┬──────────────┐
     ▼              ▼       ▼        ▼              ▼
Permissions      Firewall  Secret   Quarantine   Playbooks
                         Broker
                            │
       ┌────────────────────┼─────────────────────┐
       ▼                    ▼                     ▼
   Cedar Oil          Audit/Incident          Recovery Store
   Encryption             Store              Safe Checkpoints
                                                    │
                                                    ▼
                                           Cedar Self-Restore
                            │
                            ▼
                   Disposable Cedar Labs
                            │
                            ▼
                  suspicious files / code
                            │
                            ▼
                       Cedar Salvage
                            │
                            ▼
                   Forest Fire Protocol
```

---

# Status

```text
Cedar Step 1 — Defined
Cedar Step 2 — Defined
Cedar Step 3 — Defined
Cedar Step 4 — Defined
Cedar Step 5 — Defined
Cedar Step 6 — NEXT: Current candidate research
```
