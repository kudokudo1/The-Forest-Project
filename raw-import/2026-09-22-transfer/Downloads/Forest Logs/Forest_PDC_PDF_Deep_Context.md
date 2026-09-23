---
title: The Forest, Project Digital Cross, and Project Digital Fortress — Deep Continuity Context
aliases:
  - Forest Master Context
  - PDC/PDF Deep Handoff
  - Forest Project Continuity
tags:
  - forest
  - project-digital-cross
  - project-digital-fortress
  - cherry
  - bristlecone
  - governance
  - identity
  - security
  - qubes
status: active-reference
updated: 2026-08-07
---

# The Forest, Project Digital Cross, and Project Digital Fortress — Deep Continuity Context

> [!important]
> This file is a continuity and handoff record. It is intended for use in Obsidian, another AI session, or a future Forest knowledge system.
>
> Treat **confirmed decisions as authoritative context**, but distinguish them from proposals, drafts, and future plans. Do not silently overwrite earlier versions. Preserve version history and migration paths.

---

# 1. High-Level Project Map

## Project Digital Cross

**Project Digital Cross** is the broad engineering, governance, infrastructure, and long-term technology project.

It is the umbrella under which the user's secure computing environment, identity, AI ecosystem, storage, networking, documentation, and self-hosted services are designed.

Core goals:

- Long-term ownership and portability.
- Open standards.
- Replaceable components.
- Local-first operation.
- Self-hosting where practical.
- Privacy and security.
- Documentation as infrastructure.
- Explicit governance and change control.
- Vendor independence.
- Recovery and rollback.
- Systems that remain understandable years later.

Project Digital Cross should be written in full in normal prose. The abbreviation `PDC` is acceptable in technical filenames, paths, commands, repository names, or identifiers.

## Project Digital Fortress

**Project Digital Fortress** is the identity, account-security, domain, email, password, recovery, and trust-foundation project.

It includes:

- Domain ownership.
- DNS.
- Registrar control.
- Email identity.
- Password management.
- Account recovery.
- MFA.
- Git/GitHub identity.
- SSH.
- Security email separation.
- Future service identities.
- Reduced dependency on a single provider.

Project Digital Fortress is part of Project Digital Cross.

## The Forest

**The Forest** is the local AI, knowledge, reasoning, coordination, and future multi-agent ecosystem.

The Forest is not just one model, one qube, one machine, or Cherry alone.

It can include:

- Trees.
- Seeds.
- Roots.
- Leaves.
- Leaf Foliage.
- Soil.
- Earth.
- Streams.
- Mycelium.
- Forest Compass.
- Garden.
- Potted Plants.
- Workshops.
- Memory/knowledge/governance layers.
- Multiple devices.
- Multiple models.
- Local and optionally remote compute.
- Human-controlled automation.

The Forest should remain local-first and offline-capable. Online connectivity and synchronization should be optional rather than required.

---

# 2. Project History and Naming

Retained history:

- Early umbrella name: **Project Digital Fortress**.
- Broader engineering umbrella later became **Project Digital Cross**.
- The AI ecosystem became **The Forest**.
- The NAS/home infrastructure concept was earlier called **Cherry Orchard**.
- The user frequently uses tree, forest, root, branch, leaf, seed, growth, soil, fruit, and seasonal language to make technical architecture easier to understand and navigate.

This metaphor system is not intended to hide engineering meaning. Every canonical Forest term should map to real system behavior.

---

# 3. Project Digital Cross — Architecture and Governance

## Current governance direction

Retained architecture principles:

- Governance should be separate from implementation.
- Records should have durable identities.
- The repository should be the source of truth.
- Chat history is useful context, but not the authoritative store.
- Documents should cross-reference one another.
- Decisions should be preserved instead of silently rewritten.
- Important changes should be recorded with an ADR/RCR/other governed record where appropriate.
- Every adopted technology should have an exit strategy and future alternatives.
- Open standards should be preferred over vendor-specific lock-in.

## Draft 11 direction

Draft 11 was adopted as the working governance architecture.

Important retained concepts include:

- UUID-backed records.
- Repository-level registry/index.
- Relationship tracking.
- Governance index.
- Canonical paths.
- PDC IDs.
- History/supersession tracking.
- Forest-language records.
- Standards/specifications/templates.

Broad Project Digital Cross implementation was paused for a period while smaller reviews and Forest-specific work continued. Do not assume all PDC work has resumed unless explicitly confirmed.

## Triple Identity System

Governed records should be able to identify themselves using:

1. PDC-ID.
2. UUID.
3. Canonical Path.

This supports durable links even when filenames or folders move.

## Knowledge layers

Retained conceptual separation:

- **Memory** — what happened.
- **Knowledge** — what is true.
- **Governance** — what the system should do.

Governance should be treated as first-class and loaded before critical reasoning/actions.

## Preferred development order

Retained order:

1. Governance.
2. Knowledge.
3. Memory.
4. Reasoning.
5. Skills.
6. Automation.
7. Autonomy.

---

# 4. Project Digital Cross Principles

Retained principle set:

1. Own Your Identity.
2. Security Before Convenience.
3. Own Your Data.
4. Open Standards First.
5. Automate Repetitive Work.
6. Every System Needs a Recovery Plan.
7. Document Every Significant Decision.
8. Build in Layers.
9. Least Privilege by Default.
10. Technology Should Be Replaceable.
11. Understand Before Implementing.

Additional retained philosophy:

> Build for today, and even better tomorrow.

And:

> Govern with principles. Build with purpose. Evolve with intention.

The ecosystem should depend on open standards rather than specific vendors whenever practical.

---

# 5. Approved Engineering Workflow

Preferred workflow for Project Digital Cross / The Forest / Project Digital Fortress work:

1. Review the current checklist and milestone.
2. Define the problem and intended outcome.
3. Compare alternatives and tradeoffs.
4. Use an RFC/RCR when a decision remains open.
5. Use an ADR when a significant architecture decision is accepted.
6. Build in small, testable steps.
7. Validate before marking complete.
8. Document the implementation.
9. Record lessons learned.
10. Commit meaningful changes to Git.
11. Update changelog/history.
12. Preserve rollback paths.

Before high-impact changes, explain:

- What will change.
- Why.
- Expected result.
- Risks.
- Recovery/rollback.

---

# 6. Repository / Git State

## GitHub identity

Public online/development identity:

```text
kudokudo1
```

Development email:

```text
maple@kudostarstudios.com
```

Cherry service/development identity:

```text
cherry@kudostarstudios.com
```

## GitHub repository

Repository name:

```text
The-Forest-Project
```

Owner:

```text
kudokudo1
```

Canonical SSH remote:

```text
git@github.com:kudokudo1/The-Forest-Project.git
```

## Existing local repository

Existing local repository location recorded in Cherry-AI:

```text
~/Cherry/PDC
```

The technical folder name `PDC` is retained for compatibility even though prose should say Project Digital Cross.

## First synchronized repository state

Initial files:

```text
CHANGELOG.md
MISSION.md
README.md
ROADMAP.md
VISION.md
```

Preserved empty folders with `.gitkeep`:

```text
adr/
architecture/
archive/
assets/
decision-register/
diagrams/
governance/
principles/
projects/
scripts/
standards/
templates/
```

The local branch was renamed to:

```text
main
```

The local and GitHub histories were safely merged, then pushed. The working tree was verified clean and synchronized with `origin/main`.

Do not restructure or overwrite historical Forest versions until the final Forest inventory/finalization process is complete.

---

# 7. The Forest — Core Architecture

## High-level runtime shape

Retained runtime architecture:

```text
Qubes OS
├── dom0
│   └── Host administration only
├── Cherry-AI
│   ├── Hermes
│   ├── Bristlecone Pine
│   ├── Ollama
│   └── Forest AI runtime
├── Maple
│   ├── Personal/development work
│   ├── Project Digital Cross development
│   └── Possible Seed Nursery / training controller
└── Future isolated workshops
    ├── Model Workshop
    ├── Retrieval Workshop
    ├── Research Workshop
    ├── Code Workshop
    ├── Memory Workshop
    └── System Workshop
```

## Forest philosophy

The Forest should:

- Remain understandable.
- Preserve human authority.
- Support multiple models.
- Allow model replacement.
- Preserve isolation.
- Avoid unnecessary centralization.
- Keep local/offline use possible.
- Allow optional synchronization.
- Support multiple users with separated data.
- Learn from corrections without hiding mistakes.
- Be explainable through roots, leaves, paths, and records.

---

# 8. Trees

A **Tree** is an AI agent/personality/runtime role that grows within The Forest.

A Tree should not simply be a raw model. It may include:

- Model.
- Grain/personality.
- Tools.
- Skills.
- Memory access.
- Governance.
- Permissions.
- Roots.
- Leaves.
- Workshop access.
- Role.
- User-specific boundaries.
- Versioning.

Different Trees can serve different roles and may use different models.

---

# 9. Bristlecone Pine

## Identity

**Bristlecone Pine** is the first Tree.

Role:

> **Treewright**

The Treewright helps design, train, code, test, correct, document, maintain, and improve:

- Cherry.
- Maple.
- Future Tree species.
- Seeds.
- Plugins.
- Add-ons.
- Forest infrastructure.
- Tooling.
- Workshops.
- Model and retrieval systems.

Healthy-status phrase:

> **Pine is fine.**

Bristlecone's personality should come from his Grain/SOUL/personality instructions rather than a generic Humanizer tool.

Tree and woodworking language should feel natural and occasional, not forced into every response.

## Bristlecone runtime

Recorded profile:

```text
bristlecone
```

Recorded model:

```text
bristlecone-qwen35:4b-64k
```

Recorded context:

```text
64000
```

Runtime:

```text
Hermes + Ollama
```

Current inference:

```text
CPU-only
```

Observed model size:

```text
~5.6 GB
```

## Hermes position

Hermes is the preferred orchestration layer for Bristlecone and future Forest integration.

Reasons retained:

- Learning behavior.
- Multi-model capability.
- Tools and skills.
- Future routing.
- Modularity.
- Better fit for long-term Forest design.

Newelle is optional and paused for now.

## Hermes optimization status

Confirmed:

- Unnecessary Hermes skills were disabled.
- Humanizer disabled.
- API-server toolset trimming completed.
- Hermes CLI profile trimming completed.

Recorded trimmed API-server measurement:

```text
System prompt: 16,864 B
Tool schemas: 28,188 B
Tools: 12
```

Earlier API-server result:

```text
System prompt: 17,727 B
Tool schemas: 40,712 B
Tools: 25
```

Earlier trimmed Hermes CLI measurement:

```text
System prompt: 20,994 B
Tool schemas: 31,532 B
```

Exact post-pruning enabled skill list should be audited and recorded later.

## Benchmark history

Retained benchmark results:

```text
file,terminal,todo + reasoning none:
1m 49.64s

file,terminal,skills + reasoning none:
2m 42.40s

file,terminal,skills,todo:
2m 49.16s
```

Newelle stripped-down runs:

```text
Run 1: output after 5m 25.65s
Run 2: stopped after ~15m, no answer
Run 3: welcome/suggestion prompts after 5m 42.23s, no Bristlecone answer
```

Conclusion:

- Newelle remains too slow/unreliable for the daily Bristlecone path.
- Hermes remains primary.

## Planned Bristlecone modes

Reasoning modes:

```text
Quick
Standard
Deep
```

Workshop dimension:

```text
Code
Research
System
Model
Retrieval
Memory
```

These are separate dimensions.

Example:

> Deep reasoning does not imply every tool. A Deep task should receive only the workshop required.

Automatic routing should eventually use:

- Deterministic routing first.
- Small classifier only when necessary.
- Task continuity.
- Hysteresis.
- Safe defaults.
- Explicit overrides.
- Escalation rules.
- Visible mode reporting.
- Routing logs.

---

# 10. Seeds

A **Seed** is an early, trainable, portable, or developmental AI unit that may later grow into a Tree or specialized capability.

Seed development may include:

- Behavioral cultivation.
- Context packages.
- Prompt/personality work.
- Evaluation.
- Later model-weight training.

Weight training should not begin before:

- Evaluation suite.
- Routing.
- Retrieval.
- Runtime stability.
- Security boundaries.
- Dataset review.

Preferred future training direction:

```text
LoRA / QLoRA
```

Possible training stack:

```text
PyTorch
Unsloth
```

These should live in an isolated Model Workshop rather than the stable daily AI environment.

---

# 11. Early Seed Training

Current/recent active Forest phase:

> **Early Seed Training preparation and implementation**

Immediate goals include:

- Organize Forest knowledge in Markdown.
- Transfer knowledge between Qubes.
- Transfer context among multiple AI models.
- Improve context available to current AIs.
- Prototype future Leaf Foliage behavior.
- Create portable context/training packets.
- Prepare data structures for future Seeds.

This Forest-focused activity can continue even if broad Project Digital Cross development remains partially paused.

---

# 12. Leaf Foliage

**Leaf Foliage** is evolving into the Forest's knowledge/storage architecture.

It should support:

- Structured Markdown.
- Relationships.
- Metadata.
- Human-readable files.
- AI-readable files.
- Version history.
- Portable subsets.
- Offline use.
- Optional synchronization.
- Provenance.
- Permissions/capabilities.
- Long-term portability.
- Search/indexing.

Obsidian is currently useful as a prototype and interface for Leaf Foliage.

---

# 13. Obsidian

Obsidian is not only a note-taking application in this project.

It is being used to prototype:

- Forest knowledge storage.
- Markdown organization.
- Links and relationships.
- Portable context.
- AI handoff packages.
- Seed training context.
- Human/AI co-navigation.
- Future Leaf Foliage structures.

Markdown is preferred because it is:

- Plain text.
- Portable.
- Open.
- Human readable.
- AI readable.
- Git friendly.
- Easy to index.
- Easy to copy between systems.
- Offline-capable.

---

# 14. Garden and Potted Plants

## Garden

The **Garden** is a future optional multi-device coordination layer.

Potential roles:

- Optional sync.
- Device discovery.
- Workload handoff.
- Secure cross-device coordination.
- Sharing selected Plants.
- Routing heavy work to stronger trusted devices.
- Returning results to constrained devices.

The Garden should not become mandatory cloud infrastructure.

## Potted Plants

A **Potted Plant** is a portable selected subset of knowledge/capabilities from a larger Forest or Plant.

A Potted Plant should be able to:

- Be copied to another device.
- Work offline.
- Contain selected Leaf Foliage.
- Carry relationships/metadata.
- Carry capability/permission manifests.
- Carry queued work where useful.
- Operate independently after copying.
- Optionally stay synchronized with its source.
- Work on phones or constrained devices.

Important distinction:

### Copy

The Pot becomes independent after creation.

### Sync

The Pot retains a relationship with the source and reconciles changes when connectivity is available.

---

# 15. Forest Language — Important Terms

Retained concepts include:

## Forest
Complete Project Digital Cross AI/knowledge ecosystem.

## Heart of the Forest
Shared governed foundation supporting all Trees.

May include:

- Constitution.
- Governance.
- Standards.
- Specifications.
- Registries.
- Identity.
- Shared memory interfaces.
- Mycelium.
- Streams.
- Validation.

## Roots
Foundations beneath a Tree's conclusions and behavior.

Examples:

- Principles.
- ADRs.
- Standards.
- Specifications.
- Foundational memory.
- Requirements.
- Earlier decisions.

Roots answer:

> Why does this Tree grow and reason this way?

## Leaves
Sources/evidence/context used by a Tree.

## Branches
Sub-problems, reasoning areas, workstreams, or capability branches.

## Buds
Candidate ideas/approaches that are not yet fully developed.

## Blossoms
Emerging work/results.

## Fruit
Finished or usable outputs.

## Leaf Litter
Broken, superseded, deprecated, discarded, failed, retired, or historical material.

Leaf Litter remains useful for lessons and recovery.

## Streams
Movement of information across the Forest.

May carry:

- Commands.
- Files.
- Memory.
- Updates.
- Events.
- Results.
- Leaves.
- Fruit.
- Synchronization.

## Mycelium
Hidden coordination/connective layer.

Potential examples:

- Message buses.
- Registries.
- Indexes.
- Discovery.
- Caches.
- Background synchronization.

Streams describe movement; Mycelium describes connective infrastructure.

## Log Cabin
Human workspace used to build/interact with The Forest.

Examples:

- Terminal.
- IDE.
- Dashboard.
- Admin console.
- Creative workspace.
- Future NAS/home infrastructure depending on context.

## Forest Compass
Navigation/orientation system.

Canonical navigation form:

```text
Path to ADR-0004
```

instead of simply:

```text
See ADR-0004
```

---

# 16. Forest Commands

Retained examples:

```text
Shake the tree.
```

Reveal broad evidence/provenance.

```text
Show me your roots.
```

Explain governing reasons/foundations.

```text
Rustle your leaves.
```

Reveal influential sources.

```text
Drop your leaves.
```

Reveal direct sources used.

```text
Grow new leaves.
```

Gather more evidence.

```text
Shed those leaves.
```

Forget/remove selected temporary information when permitted.

```text
Show me your buds.
Bloom.
Bear fruit.
```

Candidate -> develop -> produce usable output.

```text
Walk me down that branch.
```

Trace a workstream/problem area.

```text
Prune that branch.
```

Remove/retire an unnecessary branch.

```text
Explain your grain.
```

Explain personality/behavioral structure.

```text
Inspect your bark.
```

Inspect interface/protection/runtime boundary depending on canonical context.

```text
Follow the streams.
```

Trace data/information movement.

```text
Count your rings.
```

Show historical versions/milestones.

---

# 17. Forest Signature

Preserve exactly unless explicitly changed by the user:

> **IN God we trust in the forest we wonder.**

Earlier Draft 11 template material also contains styled variants such as:

> *In God we trust.*  
> *In the Forest we wonder.*

Do not silently normalize or replace the user's canonical wording without approval.

---

# 18. Forest Organization Concepts

Retained conceptual ordering:

1. Forest Compass.
2. Voice, Map, Path under Spirit of the Forest.
3. Poachers and Mold above Cutting.
4. Soil under Heart of the Forest.
5. Seeds above Roots.
6. Seed Vault after Seeds.
7. Planting under Seed Vault.
8. Sprouts under Planting.
9. Growth Rings above Grain Pattern.
10. Trunk, Bark, Branches under Grain Pattern.
11. Twigs under Branches and above Leaves.
12. Buds, Blossoms, Fruit under Leaf Foliage.
13. Leaf Litter under output lifecycle.
14. Canopy under Log Cabin.

This remains evolvable during final Forest design.

---

# 19. Security Language

## Poachers
Human attackers.

## Mold
Malware, trackers, viruses, unsafe code, corruption, and related threats.

## Cutting
Destructive/removal action.

Security behavior should be explicit and auditable rather than purely metaphorical.

---

# 20. Project Digital Fortress — Identity Architecture

Domain:

```text
kudostarstudios.com
```

Role-based email identities:

```text
kudokudo1@kudostarstudios.com
```
Personal.

```text
kudokudo@kudostarstudios.com
```
Business.

```text
maple@kudostarstudios.com
```
Development, projects, Git.

```text
admin@kudostarstudios.com
```
NAS, infrastructure, administration.

```text
cherry@kudostarstudios.com
```
Cherry/service identity.

```text
cedar@kudostarstudios.com
```
Security, recovery notices, alerts, account-protection messages.

The user uses `kudokudo1` as their gamertag and public online identity.

---

# 21. Proton Mail

Confirmed setup in the current Project Digital Fortress workflow:

- Custom domain connected.
- MX configured.
- SPF configured.
- DKIM configured.
- DMARC configured.
- Incoming mail tested.
- Outgoing mail tested.
- Independent recovery configured.
- Proton two-factor authentication enabled.
- Catch-all intentionally disabled unless later changed.

Important security point:

`cedar@kudostarstudios.com` is inside the same Proton account, so it should not be the only recovery path for that Proton account.

Recovery should include an independent external method plus offline recovery material.

---

# 22. Bitwarden

Bitwarden was selected as the current password manager.

Current confirmed direction:

- Free plan is adequate for core use.
- Bitwarden account/app configured.
- MFA enabled.
- Recovery material stored offline.
- Maple SSH passphrase stored.
- Cherry-AI SSH passphrase stored.

Future:

- Possible Vaultwarden on the NAS.
- Do not give Cherry unrestricted access to the entire password vault.
- Use selected secrets/service identities under least privilege.

---

# 23. Cloudflare / Domain / Registrar

Cloudflare is used for DNS and security.

Completed/confirmed during the current workflow:

- Domain added.
- Nameservers moved.
- DNS activated.
- Mail records corrected.
- DNSSEC enabled.
- `www` CNAME created.
- Registrar transfer to Cloudflare submitted.

At the latest stage:

```text
Registrar transfer: Pending release/completion
```

Cloudflare showed:

- Domain unlocked.
- WHOIS privacy disabled for transfer.
- Authorization code accepted.
- Waiting for old registrar to release the domain.

Do not expose registrar transfer authorization/EPP codes in screenshots or chat.

Obsolete Microsoft records identified for later cleanup:

```text
lyncdiscover
_sip._tls
_sipfederationtls._tcp
NETORGFT...
```

These should only be removed if Microsoft 365/Teams/related domain services are not in use.

---

# 24. Git / SSH Security

Public Git identity:

```text
kudokudo1
```

Maple Git email:

```text
maple@kudostarstudios.com
```

Cherry Git email:

```text
cherry@kudostarstudios.com
```

Maple SSH key files:

```text
~/.ssh/id_ed25519_maple
~/.ssh/id_ed25519_maple.pub
```

Cherry-AI SSH key files:

```text
~/.ssh/id_ed25519_cherry
~/.ssh/id_ed25519_cherry.pub
```

Private key files must never be shared.

Public `.pub` files are safe to add to GitHub.

Separate keys per qube are preferred because Qubes isolation should extend to identity and compromise boundaries.

---

# 25. Qubes OS — SEPARATED PROJECT CONTEXT SECTION

> [!important]
> This Qubes section is intentionally separated from the general Forest/PDC/PDF material so it can be extracted or replaced independently.

## Qubes role in the project

Qubes OS is the primary workstation security architecture.

It is not merely the user's desktop OS. It provides the isolation model that shapes:

- Project Digital Fortress security.
- Forest AI isolation.
- Maple development.
- Cherry-AI runtime.
- Future workshops.
- Cross-qube permissions.
- Secret separation.
- Networking boundaries.
- Storage/device handling.

## Recorded Qubes version

```text
Qubes OS 4.3.1
```

## Desktop

```text
XFCE + i3
```

## Core qubes

### dom0
Host/control domain.

Rules:

- Administration only.
- Keep minimal.
- Avoid unnecessary software.
- Do not install AI runtimes.
- No routine password manager use.
- No unrestricted AI access.
- Commands often need to be typed manually, so keep dom0 commands short/medium.

### Maple
Fedora-based personal/development qube.

Roles:

- Personal workspace.
- Main development environment.
- Project Digital Cross development.
- Git identity.
- Possible Seed Nursery/training controller.
- Browser/user-facing work.

### Cherry-AI
Primary AI qube.

Roles:

- Hermes.
- Ollama.
- Bristlecone Pine.
- Forest runtime.
- AI experimentation within defined boundaries.

Recorded Fedora version:

```text
Fedora 42
```

Current inference:

```text
CPU-only
```

GPU passthrough:

```text
Not configured
```

Network path:

```text
Cherry-AI -> sys-firewall -> sys-net -> Internet
```

### Sugar
Gaming.

### Honey
Work.

### Cedar
Untrusted/security-related role depending on context.

### Pine
Whonix/disposable-personal role in earlier setup.

## Cross-qube rules

Bristlecone in Cherry-AI should not automatically:

- Read Maple files.
- Control Maple GUI.
- Read all other qubes.
- Administer dom0.
- Bypass qrexec.
- Receive broad host privileges.

Future cross-qube actions should use narrow qrexec services.

Examples:

```text
return Git status
run tests in approved repository
copy approved file
return limited diagnostic
request selected Foliage
```

Avoid broad remote shells.

## Security principle

Do not weaken Qubes isolation merely for AI convenience or speed.

---

# 26. Qubes and Forest Workshops

Future workshops should ideally use Qubes isolation.

Possible workshops:

```text
Code Workshop
Research Workshop
System Workshop
Model Workshop
Retrieval Workshop
Memory Workshop
```

Benefits:

- Separate dependencies.
- Separate permissions.
- Lower blast radius.
- Clearer resource control.
- Easier rollback.
- Easier testing.
- Easier security review.

---

# 27. NAS / Log Cabin Direction

The future NAS/home infrastructure should support:

- Backups.
- Media.
- Smart-home services.
- Forest archives.
- Git/Forgejo.
- Model and dataset archives.
- Portable Plant storage.
- Optional Forest/Garden coordination.

The NAS should not become an unrestricted trust root.

Cherry should receive least-privilege access.

Future Vaultwarden and Forgejo are possible self-hosted services.

---

# 28. Open Standards and Portability

Preferred standards include:

- Markdown.
- Git.
- SSH.
- GPG/age where appropriate.
- DNS.
- SMTP/IMAP/JMAP concepts where provider compatibility allows.
- YAML.
- TOML.
- JSON.
- POSIX conventions.
- Python.
- Bash.
- REST.
- OpenAPI.
- OAuth2/OIDC.
- OpenAI-compatible model APIs.

Architecture should use adapters/interfaces instead of hardcoding one vendor.

Possible adapters:

```text
email adapter
password adapter
LLM adapter
storage adapter
retrieval adapter
identity adapter
```

---

# 29. Technology Records

Technology Records should capture:

- Purpose.
- Why selected.
- Standards used.
- Dependencies.
- Compatible services.
- Future alternatives.
- Migration targets.
- Exportability.
- Compatibility score.
- Principle alignment.
- Replacement criteria.

Candidate records:

- Qubes OS.
- Proton.
- Bitwarden.
- Cloudflare.
- Ollama.
- Hermes.
- GitHub.
- Future Forgejo.
- Future Vaultwarden.

Use **future alternatives**, not only "replacement", because a service may remain functional while no longer matching the architecture.

---

# 30. Forest Finalization / Migration Strategy

Before moving all Forest content into the final repository structure:

1. Inventory every Forest version.
2. Preserve original versions unchanged.
3. Inventory associated files/templates.
4. Compare versions.
5. Draft final canonical Forest specification.
6. Review unresolved terms.
7. Approve version number/status.
8. Create archive index.
9. Create changelog.
10. Design final repository layout.
11. Use Git moves where practical.
12. Commit migration.
13. Push and verify.

Do not overwrite older versions just because a newer draft exists.

---

# 31. Current High-Level Status

## Completed foundation

- GitHub identity established.
- Maple and Cherry-AI Git identities configured.
- Separate SSH keys created.
- Forest GitHub repository created and synchronized.
- Bitwarden configured.
- MFA and recovery configured.
- Proton custom-domain mail configured.
- Cloudflare DNS configured.
- DNSSEC enabled.
- Registrar transfer submitted.

## External wait

- Registrar transfer completion/release.

## Forest work

Pending:

- Complete version inventory.
- Final Forest draft.
- Canonical language review.
- Final repository layout.
- Migration.
- Governance records.
- Forest archive index.
- Final documentation commit.

---

# 32. Continuity Rules for Future AIs

When this file is loaded:

1. Do not assume plans were implemented unless explicitly marked confirmed.
2. Preserve Qubes isolation.
3. Do not grant AI broad dom0 access.
4. Keep Project Digital Cross as the governance/engineering umbrella.
5. Keep Project Digital Fortress as the identity/security foundation.
6. Treat The Forest as the AI/knowledge ecosystem.
7. Preserve earlier Forest drafts.
8. Prefer open, local-first, self-hosted, portable solutions.
9. Keep repository files as source of truth.
10. Use checklists and update status only after user confirmation.
11. Explain risky commands before running them.
12. Keep rollback paths.
13. Avoid vendor lock-in.
14. Keep human authority final.

# End
