---
project: The Forest
status: active
created: 2026-08-08
updated: 2026-08-08
tags:
  - the-forest
---
# The Forest / Project Digital Cross / Project Digital Fortress
## Project Knowledge Snapshot for Bristlecone, Cherry, Maple, and Future Trees

**Snapshot date:** 2026-08-07  
**Status:** Living project context. Some sections describe confirmed architecture; others describe active plans or implementation targets.  
**Important rule for AI readers:** Do not treat a proposal, pending item, or historical idea as canonical unless it is explicitly marked confirmed/current.

---

# 1. Project Family and Relationships

## 1.1 Project Digital Cross (PDC)

**Project Digital Cross (PDC)** is the broader personal digital ecosystem and umbrella project.

PDC is intended to unify:

- Digital identity
- Security
- Development infrastructure
- Local AI
- The Forest
- Storage and backups
- Communications
- Future self-hosted services
- Git/repository governance
- User-owned computing infrastructure

The Forest is one major subsystem inside PDC.

PDC is designed around:

- Local-first operation
- User ownership
- Open-source and self-hostable tools where practical
- Minimal dependence on recurring subscriptions
- Portability
- Replaceable components
- Security boundaries
- Human authority over AI systems

---

## 1.2 Project Digital Fortress (PDF)

**Project Digital Fortress (PDF)** predates the current PDC structure.

Its role evolved into the **security, identity, account-protection, and infrastructure foundation** inside Project Digital Cross.

PDF-related work includes:

- Domain ownership
- DNS
- Email architecture
- Security and recovery identities
- Password management
- Git identity
- Account recovery planning
- Infrastructure administration
- Future self-hosting plans
- Security separation between personal, development, business, and administrative identities

Project Digital Fortress should be understood as a foundation or security layer of Project Digital Cross rather than a competing project.

---

## 1.3 The Forest

**The Forest** is an AI-powered, locally hosted, local-first, peer-to-peer personal computing and knowledge ecosystem.

It is intended to combine ideas inspired by systems such as:

- Hermes Agent
- Newelle
- Letta
- OpenHands
- LangGraph
- CrewAI
- AutoGen
- Open Interpreter

The Forest should eventually provide these capabilities natively or through replaceable adapters rather than permanently depending on any one outside project.

Core design direction:

> Existing systems are references, sources, and temporary scaffolding. The Forest should own its identity, governance, interfaces, data formats, permissions, and user experience.

The Forest is not simply a chatbot collection.

It is intended to become a complete environment in which persistent AI identities, deterministic system services, user data, permissions, storage, devices, models, and tools interact through Forest-defined rules and language.

---

# 2. Core Forest Philosophy

## User authority

The user remains the final authority over the Forest.

Trees may warn, recommend, disagree, explain risk, request confirmation, or refuse actions they are not permitted to perform.

Trees should not silently seize authority, rewrite governance, change their own permissions, or promote their own proposals to canonical status.

## Local-first and offline-capable

The Forest should work locally without requiring cloud access.

Online access should be optional, explicit, replaceable, and permission-controlled.

Important knowledge and storage features should not depend on permanent internet connectivity.

Portable "potted" versions of knowledge and Trees should be able to move between devices without requiring cloud synchronization.

## Replaceable model engines

A Tree is not its model.

```text
Tree identity
= memory
+ role
+ personality
+ permissions
+ skills
+ history
+ Forest standards
+ model-routing rules

Model
= replaceable reasoning engine
```

A Tree should be able to use local, remote, specialist, or future models without losing identity.

## Self-learning

Forest self-learning means learning through:

- Memories
- Skills
- Preferences
- Workflows
- Approved lessons
- Corrections
- Evaluations
- Development history
- Structured training data
- Later adapters or fine-tuning where appropriate

Self-learning does not mean uncontrolled weight changes, permission changes, governance rewriting, or authority escalation.

---

# 3. Core Trees and Roles

## Spirit of the Forest

The **Spirit of the Forest** is deterministic protected local code.

It is not an AI model, Tree, or conscious personality.

It is the built-in guidance, governance, and system-management layer.

The **Voice of the Forest** is the user-facing help/menu expression of the Spirit.

The Spirit is intended to provide:

- Help menus
- Command references
- Forest navigation
- Permission enforcement
- Action routing
- Protected access controls
- Recovery tools
- Sap Taps
- Log Cabin tools
- Forest Fire access controls
- Deterministic safety behavior

The Spirit should be lightweight compared with AI models.

## Cherry

Cherry is the primary user-facing assistant Tree.

Intended specialties:

- Conversation
- User experience
- General assistance
- Forest meaning and terminology
- User preferences
- Documentation review
- Reviewing whether implementations still feel like The Forest

Cherry should retain a stable identity independent of the model currently used.

Cherry is expected to participate in creating the Constitution and Principles so that the history of her own system becomes training data.

## Maple

Maple is the primary software-development and engineering Tree.

Intended specialties:

- Coding
- Debugging
- Testing
- Repository work
- Architecture implementation
- Technical review
- Isolated Git branches
- Comparing code against Forest Language
- Dependency and license review
- Building replaceable adapters
- Catching regressions

Maple should learn engineering judgment from multiple reference systems instead of copying one system's architecture.

## Cedar

Cedar is the security Tree.

Intended responsibilities include defense, quarantine, warnings, integrity checks, recovery assistance, Cabin protection, and Forest protections.

Cedar should not rely on an AI model as the sole authority for destructive or high-impact security actions.

## Sycamore

Sycamore is a planned Tree associated with larger Forest-level connectivity and remote/network functions.

Sycamore does not have a Potted standalone form in the current architecture.

Implementation is later-stage.

## Bristlecone Pine

Bristlecone Pine is the emergency and long-term **multi-model development Tree**.

Role: **Treewright**

Bristlecone is intended to be ready immediately through mature pretrained models, existing datasets, Forest documents, tools, and specialist engines.

Bristlecone helps:

- Design Trees
- Train Trees
- Build datasets
- Program
- Debug
- Test
- Review
- Catch mistakes
- Correct errors
- Design plugins
- Design add-ons
- Build Forest-compatible extensions
- Create evaluation suites
- Review licensing
- Preserve development standards
- Help users develop new Tree species

Bristlecone is a development partner, not the ruler of The Forest.

Signature status language:

- **Pine is fine.** = required checks passed
- **Pine is mostly fine.** = main result works but warnings remain
- **Pine is not fine.** = blocking problem or failed check
- **Pine cannot confirm.** = insufficient evidence

Casual variants may include:

- That went fine.
- That went pine.
- That would be fine.
- That would be pine.

The fine/pine substitution should be occasional and should never corrupt code, commands, filenames, exact quotations, legal text, license text, or structured data.

Bristlecone's current bootstrap identity is version **0.0.2**.

---

# 4. Bristlecone Development Role

Bristlecone should coordinate a development loop like:

```text
User goal
→ identify approved requirements
→ compare Forest standards
→ plan
→ route work to useful model(s)
→ code or produce proposal
→ test
→ independent review
→ explain uncertainty
→ user approval
→ preserve approved lesson
```

Bristlecone may use multiple specialist models for:

- General reasoning
- Coding
- Debugging
- Testing
- Documentation
- Security review
- Vision
- Independent second opinions

Model outputs are proposals and working material.

Only governed and approved conclusions should become trusted long-term Forest knowledge.

---

# 5. Cherry and Maple Development-Learning Strategy

Preferred learning cycle:

```text
Request
→ approved interpretation
→ implementation plan
→ code/document change
→ tests
→ human review
→ correction
→ final accepted result
→ reusable lesson
```

Only final approved lessons should become trusted learning.

Raw conversations and rejected ideas may remain in history, but should not automatically become trusted rules.

Recommended information layers:

## Immutable Project Archive

Contains original files, historical versions, conversation exports, patches, audits, rejected drafts, and historical code.

## Canonical Forest Knowledge

Contains current approved definitions, architecture, commands, permissions, and governance.

## Development History

Contains diffs, tests, bugs, corrections, review outcomes, and reasoning summaries.

## Learning Candidates

Contains proposed skills, lessons, workflow improvements, and memory updates.

## Approved Learning

Contains only user-approved lessons, validated skills, approved patterns, and confirmed project rules.

## Mistake Log

Contains error, cause, correction, regression-prevention test, and correction status.

---

# 6. Base Seed Model Strategy

A separate **Base Seed model laboratory** is planned.

Purpose:

- Start from a more neutral pretrained base model
- Train Forest-compatible behavior
- Generate future Cherry and Maple adapters
- Evaluate how much Tree behavior can be learned rather than only prompted

Important distinction:

```text
Bristlecone
= mature working development Tree

Base Seed model
= protected experimental student model
```

The Base Seed should initially have:

- No system authority
- No unrestricted tools
- No direct filesystem control
- No direct Newelle control
- Modest context
- Isolated training and evaluation workspace

Future branching model:

```text
Forest Seed Base
├── Cherry adapter
│   ├── communication
│   ├── user experience
│   ├── Forest identity
│   └── documentation
└── Maple adapter
    ├── coding
    ├── debugging
    ├── testing
    └── architecture
```

---

# 7. Forest Language Snapshot

Frozen original reference:

`FOREST-LANGUAGE-Reviewed-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.md`

Current edited candidate:

`FOREST-LANGUAGE-Edited-Candidate-0.13.35-Edit-Chain-002.md`

The original 0.13.35 remains preserved.

The current candidate contains targeted user-approved changes while preserving the original reference.

---

# 8. Major Forest Language Concepts

## Soil

The host environment: operating system, hardware, files, devices, and local services.

## Tree anatomy

Current conceptual anatomy:

- Roots
- Trunk
- Bark
- Branches
- Twigs
- Leaves

## Leaves

Leaf provenance/types:

- User Input
- User Output
- Tree Input
- Tree Output

Leaf states:

```text
Loose Leaf
< Leaf
< Sturdy Leaf
< Log
```

Foliage Management can manage approved Leaf properties individually or in groups.

## Solid Material

A bounded, non-Fluid data or capability object that is not the base Tree itself.

## Fluids

Important Fluid concepts:

- Water
- Sap
- Tar Sap
- Light Syrup
- Syrup
- Molasses

Delivery concepts:

- Rain
- Streams

Absorption states:

- Deny
- Wash Over
- Sip
- Drink
- Download

## Fertilizer

Current definition:

> Fertilizer is information or material a Tree absorbs and incorporates into rapid compatible growth.

Related concepts:

- Fertilizing
- Syrup as Fertilizer
- When Absorption Becomes Fertilizing
- Fertilizer Provenance

## Canopy

Higher-level connection/session/resource-sharing layer.

Includes Personal Canopy and wider Forest Canopy concepts.

## Mycelium

Deep local IPC/direct capability connection underneath Canopy.

Cherry and Cherry Bonsai may use Mycelium for direct connection and may detach it during suspicious behavior without shutting either Tree down.

## Pollen

Lightweight communication for Potted Trees and Cherry Bonsai.

Pollen does not require full Forest, Mycelium, or full Forest Canopy.

It may carry small approved messages and lightweight references.

It should not silently merge identities, memories, permissions, Logs, or Tree leases.

## Beehive

Optional inactive extension/plugin intended to increase Pollen speed/capacity and improve Garden communication, coordination, and lightweight automation.

## Potted Mode

Standalone Tree operation without a complete Forest.

Current Potted concepts:

- Potted Cherry
- Potted Maple
- Potted Cedar

No Potted Sycamore.

## Garden

A user-formed group of Potted Trees with limited explicit cooperation.

## Cherry Bonsai

A miniature mature Cherry backup/assistant.

States:

- Stored Cherry Bonsai
- Active Cherry Bonsai
- Promoted Cherry Bonsai

Designed to run on lower-end hardware, provide recovery continuity, use Propagule backup, and optionally connect to full Cherry through Mycelium.

## Squirrel

Inactive optional Garden Seed Vault / Seed-management plugin.

Possible responsibilities:

- Collect approved backup Seeds
- Organize Seeds
- Maintain secondary backups
- Help Cedar with safety/integrity
- Help Maple organize compatible versions/updates

Squirrel does not automatically plant, restore, delete, replace, or activate a Seed without authority.

---

# 9. Logs, Log Cabin, Seed Vault, and Recovery

## Logs

Long-term Sap-bearing Solid Material.

## Log Cabin

Spirit-managed long-term storage and recovery Tool.

A Forest may support multiple or removable Log Cabins.

## Seed Vault

Protected package/recovery compartment normally inside a Log Cabin.

A Seed Vault may also exist as an inactive portable package on desktop, ordinary files, approved external storage, or outside an active Forest.

Portable existence does not automatically activate it.

Before integration, the Spirit should verify identity, integrity, protection, compatibility, ownership, and contents.

## Propagule

Compact emergency Tree package used for recovery, replanting, portability, and Cherry Bonsai continuity.

---

# 10. Cedar Standalone Security Concepts

## Cedar Cabin Guard

Potted Cedar standalone Log Cabin protection/access mode.

Designed to work when the full Forest is absent, closed, unhealthy, or quarantined.

Possible functions:

- Detect Cabins
- Operate Cedar Doors
- Alert on interactions
- Verify integrity
- Read permitted metadata
- Access authorized Logs/files
- Back up
- Preserve pending writes
- Oil/Quarantine
- Restore
- Use Cabin Tap
- Encrypt non-Forest data

It does not provide unrestricted Forest authority.

## Cabin Tap

Portable narrow deterministic subset of Spirit Sap Taps.

May apply Tar to authorized Logs, preserve provenance/retention/integrity, revoke access, lock, record minimum-safe Action Receipts, and hand off to full Spirit.

May not control the entire Forest, downgrade Tar freely, grant unrestricted master keys, or route protected data without authority.

## Standard Encrypted File

Ordinary encrypted non-Forest Solid Material.

It is not automatically a Log, Leaf, Sap, Tar, Seed Vault package, or Forest data.

Cedar may create, verify, copy, move, or decrypt one under user authority.

## Forest Fire

Last-ditch digital sanitization and recovery mechanism.

It is not physical destruction, retaliation, or unrestricted destructive action.

Forest Fire remains a tightly controlled emergency mechanism.

---

# 11. Spirit Tools and Processes

Current Spirit Tools menu concepts include:

- Compass
- Map
- Predestined Paths
- Sap tap tools
- Syrup Bucket
- Local Forest Recovery
- Axe
- Wood Chipper
- Sheers
- Saw
- Cedar Emergency Tools
- Constitution Copy
- Principles Copy

Processes include:

- Pruning
- Cutting
- Felling
- Milling

Propagation sequence:

- Propagation
- Replanting
- Sprout

---

# 12. Mold and Hackers

Detailed Mold and Hackers sections live under the Spirit.

Potential controls include:

- Scan for Mold
- Scan for Hackers
- Scan for Mold and Hackers
- Suspect Mold
- Suspect Hackers
- Suspect Mold and Hackers

A Suspect control raises alert level but should not automatically authorize destructive action, unrestricted access, or Forest Fire.

Cedar is a critical protection component for both.

---

# 13. Constitution and Principles

The Constitution and Principles are not finalized.

This is intentionally being treated as an early major project for Bristlecone, Cherry, and Maple.

Desired development method:

```text
Bristlecone
→ identifies repeated values and architecture rules

Cherry
→ reviews user experience, language, meaning, and identity

Maple
→ reviews technical enforceability and implementation

User
→ approves or rejects
```

Each proposed clause should ideally include:

- Supporting Forest material
- Whether it belongs in Constitution or Principles
- Reason for inclusion
- Conflicts or unresolved choices
- Technical enforcement requirement
- Evaluation/regression test

Unapproved clauses must remain clearly marked as proposals.

---

# 14. Development and Reference-System Policy

Outside systems may be studied as references.

Examples:

- Hermes
- Newelle
- OpenHands
- Letta
- LangGraph
- CrewAI
- AutoGen
- Open Interpreter

For each external reference, record:

- Project
- Source
- Version/commit when relevant
- License
- Feature studied
- Strengths
- Weaknesses
- Security concerns
- Whether code was copied, adapted, or only studied
- How the Forest-native design differs

Preferred rule:

> Study behavior and architecture freely. Copy or adapt source code only when the license permits it and attribution/provenance requirements are preserved.

---

# 15. Hermes and Newelle Strategy

## Hermes

Hermes is currently used as Bristlecone's early runtime because it already provides agent loop, model providers, memory, skills, tools, scheduling, subagents, CLI, API server, profiles, and multiple interfaces.

The Forest should not permanently define itself by Hermes internals.

## Newelle

Newelle is currently used as an early desktop **Bark** for Bristlecone.

Current route:

```text
Newelle
→ Bristlecone Hermes API
→ Bristlecone profile
→ local model provider
→ Ollama
```

Newelle is not intended to replace Bristlecone's Hermes identity.

A later allowlisted Newelle Bridge may expose approved TTS, STT, notifications, file access, GUI actions, and profile functions.

---

# 16. Bristlecone Current Bootstrap

Current Bristlecone profile:

- Hermes profile: `bristlecone`
- Hermes API: `http://127.0.0.1:8643/v1`
- Advertised model: `bristlecone`
- Bind: `127.0.0.1`
- Workspace: `~/The-Forest/bristlecone`
- Identity version: 0.0.2
- Role: Treewright

Current primary model:

`bristlecone-qwen35:4b-64k`

Configured context:

64,000 tokens

Route:

```text
Newelle
→ Bristlecone
→ Hermes profile
→ Ollama
→ bristlecone-qwen35:4b-64k
```

---

# 17. PDC Identity and Email Architecture

Domain:

`kudostarstudios.com`

Role-based addresses:

- Personal: `kudokudo1@kudostarstudios.com`
- Business: `kudokudo@kudostarstudios.com`
- Development/Git: `maple@kudostarstudios.com`
- NAS/Admin infrastructure: `admin@kudostarstudios.com`
- Security/recovery: `cedar@kudostarstudios.com`
- Cherry service identity: `cherry@kudostarstudios.com`

Public development/display identity:

`kudokudo1`

Governed document author:

`maciono brown`

Email provider:

Proton Mail with custom domain.

Registrar/DNS:

Cloudflare Registrar / Cloudflare DNS.

Completed infrastructure work includes:

- Domain added to Cloudflare
- DNS reviewed
- Proton DNS configured
- Obsolete GoDaddy email records removed
- Nameservers moved
- DNSSEC enabled
- Registrar moved to Cloudflare
- Proton custom-domain setup completed
- Domain verification completed
- Required addresses/aliases created
- Send/receive tests completed
- SPF/DKIM/DMARC configured
- Git identity configured
- SSH keys added to GitHub
- Commit-signing decision configured

Password manager:

Bitwarden

Security/recovery identity used for Bitwarden:

Cedar email

---

# 18. Git and Repository Governance

Public author/display name:

`kudokudo1`

Development/Git email:

`maple@kudostarstudios.com`

Governed record author:

`maciono brown`

PDC governance document families include:

- ADR
- RFC
- RCR
- ICR

Uppercase prefixes are acceptable for governed records.

Lowercase is preferred for directories, machine files, and implementation paths.

Pending repository work includes:

- Canonical PDC root spec
- ADR-0000 sequence
- Deduplicate/retire Draft 11 material
- Canonical/historical/archive/deprecated decisions
- PDC changelog
- Final archive index
- README/navigation
- Forest Compass role
- Final repository layout
- Git-history-preserving migration
- Validation of links and paths
- Final commits/pushes

---

# 19. Forest Finalization Status

Completed/substantially completed:

- Inventory previous Forest versions
- Inventory associated templates/architecture files
- Preserve originals unchanged
- Build complete version comparison
- Create archive indexes
- Create artifact timeline
- Preserve original 0.13.35 reference
- Apply targeted Edit Chain 001
- Apply targeted Edit Chain 002

Still active/pending:

- Draft canonical final Forest specification
- Resolve remaining terminology
- New Forest definition
- Garden definition afterward
- Human review
- Compare human edit against prior versions
- YAML/headings/reference/terminology/regression checks
- Final line-by-line review
- Final version number
- Final status
- Consolidated changelog
- Final repo layout
- Git migration
- Commit/push

---

# 20. Important Editing Rules

When conceptual development is paused:

- Architecture and terminology changes are suggestions unless explicitly approved.
- Small edits should remain narrow.
- Only minimum logical consistency extensions should be applied.
- Do not silently expand scope.
- Do not silently fix user wording unless requested.
- Preserve original versions.
- Use current candidate only for approved targeted edits.

Current working edit candidate:

`FOREST-LANGUAGE-Edited-Candidate-0.13.35-Edit-Chain-002.md`

---

# 21. Licensing Strategy

Recommended project structure:

```text
the-forest/
├── forest/
├── adapters/
├── third_party/
├── licenses/
├── THIRD_PARTY_NOTICES.md
├── DEPENDENCIES.md
└── SBOM/
```

For every external component, record name, source, version/commit, license, owner, modification rights, commercial redistribution rights, required notices, and whether bundled or optional.

Hermes core is MIT-licensed, but bundled skills/components can have separate licenses.

Newelle is GPL-3.0-or-later and is better treated as a separate service/reference unless GPL obligations are intentionally accepted.

Models, voices, fonts, icons, datasets, and plugins must be checked separately.

---

# 22. Long-Term Forest Runtime Direction

The Forest should eventually own:

- Tree identity
- Spirit
- Permissions
- Action Broker
- Memory boundaries
- Forest data formats
- Logs
- Log Cabins
- Seed Vault
- Pollen
- Mycelium
- Garden/Forest communication
- Action Receipts
- User-profile separation
- Recovery rules
- Forest terminology
- User experience

External systems may temporarily provide agent loops, model providers, memory engines, skill engines, scheduling, tool plumbing, coding workers, and desktop interfaces.

Each external function should remain replaceable behind Forest-owned interfaces.

---

# 23. Future Implementation Goals

Planned implementation areas include:

- Hermes as initial scaffolding
- Forest bootstrap repository
- Cherry/Maple persistent identities
- Separate memories/workspaces/permissions
- Minimal deterministic Spirit
- Action Broker
- Action Receipts
- Linux/Qubes Soil adapter
- Model router
- First Bark
- Cedar security implementation
- Sycamore remote/Canopy work later
- Lightweight Potted Trees
- Cherry Bonsai
- Mobile Sapling / remote Sprout

---

# 24. QUBES OS — SEPARATE COMPATIBILITY SECTION

This section intentionally separates Qubes-specific information from the rest of the project.

## Qubes role in The Forest

Qubes OS is the current security-oriented host platform for active Forest development.

It provides compartmentalization between AI workloads, development work, personal tasks, security-sensitive operations, and administration.

The Forest should support Qubes but should not require Qubes for every user.

Qubes should therefore be treated as an important **Soil implementation**, not as the definition of Soil itself.

## Relevant qubes

### Cherry-AI

Primary AI qube.

Hosts/intended to host:

- Hermes
- Ollama
- Bristlecone
- Newelle
- Forest AI runtime experiments
- Local model serving

### Maple

Personal development/project qube.

Used for:

- Git
- Development
- Project files
- Training preparation
- Repository work

### Seed-AI

Clone of Cherry-AI intended for lighter training/experimental workflows.

### dom0

Qubes administrative domain.

Important constraints:

- No normal copy/paste
- No normal screenshots
- Commands often must be manually typed
- Keep dom0 commands concise
- Do not make dom0 a general Forest data-processing environment

## Qubes security design direction

- No unrestricted cross-qube control
- No unrestricted dom0 control
- No silent qrexec policy creation
- Cross-qube communication must be explicit
- Future Forest cross-qube features should use approved qrexec services/policies
- Sensitive Tree permissions should remain qube-scoped unless explicitly expanded

## Newelle in Qubes

Newelle is installed inside Cherry-AI as a Flatpak.

Observed effective permissions:

- network
- IPC
- Wayland
- PulseAudio
- fallback X11
- DRI graphics access
- GNOME Shell Screencast talk permission

No broad filesystem Flatpak override was shown.

Current Bristlecone API:

`127.0.0.1:8643`

This is local to Cherry-AI unless future forwarding/qrexec networking is explicitly added.

## Qubes compatibility target

A future Linux/Qubes Soil adapter should understand:

- Qube identity
- Qube lifecycle
- qrexec boundaries
- Device assignment
- Network boundaries
- File-transfer boundaries
- Permission requests
- Memory/resource limits
- Safe inter-qube service contracts

The adapter should remain optional so The Forest can also run on non-Qubes Linux.

## Current work-state modes

### Forest Normal Mode

Earlier verified target:

Cherry-AI:
- memory: 8192 MB
- maxmem: 16000 MB
- vCPUs: 9 in an earlier script version

Maple:
- memory: 800 MB
- maxmem: 8000 MB
- vCPUs: 4

### Pine Cone Mode

Restores Ollama and Hermes, keeps model unloaded until first use, and supports keep-alive behavior.

### Maple Seed Mode

Stops Newelle/Hermes, unloads model, frees memory, and prioritizes Maple training.

### Forest Mixed Mode

Used when 2–3 qubes are active for mixed review/training.

### Forest Seed Mixed Mode

Recorded target:

Maple:
- 12288 MB initial
- 16000 MB max
- 4 vCPUs

Cherry-AI:
- 6144 MB initial
- 9000 MB max
- 3 vCPUs

Seed-AI:
- 2048 MB initial
- 6000 MB max
- 2 vCPUs

These modes may be revised as Bristlecone requirements evolve.

## Current i3 hotkeys

Num Lock OFF:

- Numpad 1 → Forest Normal
- Numpad 2 → Pine Cone
- Numpad 3 → Maple Seed
- Numpad 4 → Forest Mixed
- Numpad 5 → intended Seed Mixed Mode

## Qubes-specific design rule

The Forest should never assume that seeing the host means controlling every qube.

Preferred chain:

```text
Tree authority
→ Forest permissions
→ Soil adapter
→ Qubes policy
→ qrexec/device/network boundary
→ approved action
```

---

# 25. Current High-Priority Development Order

1. Stabilize Bristlecone
2. Optimize Hermes/Newelle performance
3. Load the Forest corpus into Bristlecone
4. Draft Constitution and Principles with Bristlecone
5. Create training/evaluation records
6. Build protected Base Seed model lab
7. Start Cherry 0.0.1
8. Start Maple 0.0.1
9. Use Bristlecone to evaluate both
10. Continue Forest-native runtime work
11. Build stronger Spirit/Action Broker/Soil layers
12. Add more models/specialist routing after measured performance tests

---

# 26. Final Working Principle

The Forest should grow from its own development history.

Bristlecone, Cherry, and Maple should understand:

- What was built
- Why it was built
- What alternatives were rejected
- What mistakes happened
- How mistakes were corrected
- Which rules are canonical
- Which ideas remain proposals
- How Forest language maps to real technical systems
- How to continue development without losing the original vision

The objective is not merely to create assistants that know The Forest.

The objective is to create Trees that understand how The Forest came to exist and can help it continue growing without losing user authority, local ownership, technical discipline, or identity.
