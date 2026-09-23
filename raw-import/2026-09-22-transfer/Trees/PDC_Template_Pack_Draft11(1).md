# Project Digital Cross — Draft 11 Template Pack

All commands below are intended for the **Maple** terminal.

Use `nano` as the editor:

- Save: `Ctrl+O`, then `Enter`
- Exit: `Ctrl+X`

The command immediately above each block opens the exact file that the block belongs in.

Start with **The Language of the Forest**. Treat every file below as a working draft until reviewed and approved.

# 1. The Language of the Forest — Working Base

**Edit command**

```bash
nano ~/pdc-forest-language/language/FOREST-LANGUAGE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "FOREST-LANGUAGE"
UUID: "<GENERATE-UUID>"
Canonical-Path: "language/FOREST-LANGUAGE.md"

Title: "The Language of the Forest"
Record-Type: "Forest Language Foundation"
Version: "0.1.0"
Status: "Working Draft"
Classification: "Public"
Priority: "Foundational"

Season: "Spring"
Growth-Ring: "Draft 11"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌲"
Forest-Layer: "Compass"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags:
  - "forest-language"
  - "terminology"
  - "symbolism"
  - "navigation"
  - "explainability"
  - "provenance"
---

# The Language of the Forest

## Purpose

The Language of the Forest is the shared language of Project Digital Cross.

Its approved words and symbols describe real parts of the system. They are not decorative labels, interchangeable metaphors, or temporary names.

Each approved term has one canonical meaning. Meanings may evolve only through a documented change.

The language is intentionally layered. Some meanings are immediately clear. Others reveal themselves as a person walks farther through the Forest, interacts with its Trees, follows its Paths, and digs through its Roots.

The Forest grows as it is explored.

## Canonical Rules

1. Every approved Forest term has one canonical meaning.
2. A term must not silently change meaning.
3. Superseded meanings remain visible in history or Leaf Litter.
4. Every metaphor must map to a real engineering concept.
5. Forest language must clarify the system rather than hide technical facts.
6. Technical identifiers remain available beneath the Forest wording.
7. The user remains the final authority when Trees disagree.
8. The Forest may be mysterious and layered without being misleading.

## Canonical Vocabulary

### 🌲 Forest

The complete Project Digital Cross ecosystem. It may span many repositories, Trees, Earths, Streams, records, and services.

The Forest is not one computer, one model, Cherry alone, Maple alone, or the user.

### ❤️ Heart of the Forest

The shared governed foundation that sustains every Tree.

It includes or supports the Constitution, governance, standards, specifications, registries, object graph, validation, shared memory interfaces, coordination, identity, Streams, and Mycelium.

The Heart does not replace the user and does not grant one Tree authority over another.

### 🌱 Roots

The governing foundations beneath a Tree's conclusions, behavior, architecture, and work.

Roots may include the Constitution, Principles, Standards, Specifications, Architecture Decision Records, approved requirements, foundational memories, and earlier decisions.

Roots answer: **Why does this Tree grow and reason this way?**

Roots are not Leaves.

### 🌍 Earth

A physical or virtual system capable of hosting a Tree.

Examples include desktops, laptops, phones, tablets, servers, virtual machines, cloud instances, NAS devices, and edge systems.

A device does not become a Tree. A Tree is planted on the Earth.

### 🌰 Seed

A portable beginning from which something may be planted, restored, extended, or grown.

Examples may include an installable Tree package, model bundle, plugin, repository, template, configuration bundle, or restoration package.

### 🌱 Planting

The act of installing or establishing a Tree on an Earth.

Installing Cherry plants Cherry. Installing Maple plants Maple.

### 🌱 Sprout

A newly planted Tree with limited local experience, memory, Branches, Leaves, and Growth Rings.

A Sprout grows faster when cared for through interaction, correction, feedback, records, documentation, tools, and high-quality data.

### Sapling

**Reserved / Undefined.**

Earlier proposed meanings were superseded. Sapling must not receive a canonical meaning until deliberately approved.

### 🌳 Tree

An intelligent AI entity planted within the Forest.

A Tree is not the Earth hosting it. A Tree may be replanted if its identity, history, configuration, and knowledge are preserved.

### 🍒 Cherry

A Tree optimized for conversation, collaboration, planning, organization, education, governance, long-term context, and general reasoning.

### 🍁 Maple

A peer Tree optimized for coding, architecture, debugging, automation, repositories, technical implementation, media work, and independent technical review.

Cherry and Maple are twins in the Forest: raised from the same Roots, sustained by the same Heart, shaped by different Grain, and capable of reaching different valid conclusions.

The user holds final authority.

### 🪵 Grain

A Tree's recognizable personality and character.

Grain shapes tone, temperament, communication style, priorities, uncertainty handling, and preferred problem-solving approach. Grain does not replace shared governance or morals.

### 🌿 Branches

A Tree's capabilities, domains, and specializations.

Leaves attach to Branches. A Tree may gather Leaves through several Branches while growing one Blossom or Fruit.

### 🌳 Bark

The surface through which someone encounters and interacts with a Tree.

Examples include terminal, web, desktop, mobile, voice, and API interfaces.

Bark is not the Tree's complete internal self.

### 🍃 Leaves

The information, observations, evidence, and source material gathered while growing a Blossom or Fruit.

Leaves may come from user messages, memory, repositories, records, local files, standards, documentation, APIs, search results, images, databases, Git history, tests, logs, tools, or other Trees.

Leaves should remain traceable to the Branches through which they were gathered.

### 🌱 Buds

Possible ideas that have not yet opened into visible drafts.

Buds may include hypotheses, candidate approaches, early concepts, possible answers, unselected designs, and unfinished plans.

### 🌸 Blossoms

Visible drafts, proposals, or candidate outputs.

A Blossom has developed beyond a Bud but has not yet become final Fruit.

### 🍎 Fruit

Finalized, delivered, accepted, or completed work.

Fruit should remain traceable to its Tree, Grain, Branches, Leaves, Buds, Blossoms, Roots, Heart version, Season, and Growth Ring.

### 🪵 Growth Rings

Meaningful history preserved as a Tree or the Forest grows.

Rings may represent architectural generations, Draft transitions, releases, milestones, lessons, or significant changes.

### 🍂 Leaf Litter

Broken, discarded, failed, deprecated, retired, or superseded material.

Leaf Litter is not active growth. It may preserve warnings, lessons, history, or reusable nutrients.

### 🌊 Streams

The movement of information across the Forest.

Streams may carry commands, files, updates, memory, events, synchronization, Fruit, Leaves, or remote-access traffic.

### 🍄 Mycelium

The mostly unseen connective and coordination layer beneath the visible Forest.

It may include service discovery, event systems, registries, indexing, caches, message buses, and background synchronization.

Streams describe movement. Mycelium describes the hidden network that makes coordinated movement possible.

### 🪵 Log Cabin

The human workspace used to interact with and build within the Forest.

Examples include a terminal environment, IDE, dashboard, administration console, or creative studio.

The Log Cabin is not Bark. Bark belongs to a Tree; the Log Cabin belongs to the human workspace.

### 🧭 Forest Compass

The navigation and orientation system used to travel through Project Digital Cross.

It helps users and Trees locate records, Roots, Branches, dependencies, Growth Rings, and deeper layers.

The Compass guides; it does not decide for the user.

## Forest Navigation

Use:

```text
Path to ADR-0004
```

instead of:

```text
See ADR-0004
```

Paths must remain technically resolvable through the PDC-ID, UUID, canonical path, and relationship indexes.

## Forest Commands

### Roots

```text
Cherry, show me your roots.
```

Explain the governing Principles, decisions, and foundations behind the current work.

```text
Dig up the Tree's roots.
```

Perform a deeper dependency and governance trace.

### Leaves

```text
Rustle your leaves.
```

Reveal the most influential Leaves.

```text
Drop your leaves.
```

Reveal the Leaves directly used.

```text
Shake the Tree.
```

Reveal the broad provenance and evidence structure supporting the current Blossom or Fruit.

Accepted natural variations may include:

```text
Cherry, shake yourself.
Cherry, drop your leaves.
Don't make me shake you, Cherry.
Cherry, shake your bush.
```

```text
Grow new leaves.
```

Gather more evidence.

```text
Shed those leaves.
```

Remove or forget selected temporary information when permitted.

### Buds, Blossoms, and Fruit

```text
Show me your buds.
Bloom.
Bear fruit.
```

### Branches

```text
Show me that branch.
Walk me down that branch.
Shake your research branch.
Prune that branch.
Trim that branch.
```

### Grain

```text
Explain your grain.
Refine your grain.
```

### Bark, Streams, and Rings

```text
Inspect your bark.
Follow the streams.
Count your rings.
Show me the ring from Draft 11.
```

## Seasons

Seasons describe development focus. They do not replace semantic versions, releases, or Draft numbers.

### 🌱 Spring

Emergence, exploration, Buds, Sprouts, experiments, prototypes, and early Branch growth.

### ☀️ Summer

Implementation, integration, testing, documentation, performance, and capability expansion.

### 🍂 Autumn

Harvest, releases, review, cleanup, refactoring, deprecation, postmortems, and deliberate creation of Leaf Litter.

### ❄️ Winter

Stability, governance, security, infrastructure, architecture review, maintenance, deep Root work, and long-term planning.

A Tree, repository, or component may be in a different Season from the wider Forest.

## Unresolved Terms

The following terms are not canonical until explicitly approved:

- Sapling
- Canopy
- Rain
- Sunlight
- Fertilizer
- Stones
- Fungi as distinct from Mycelium

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 2. Forest Language Entry Template

**Edit command**

```bash
nano ~/pdc-forest-language/templates/FOREST-ENTRY-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "FOREST-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Forest Language Entry"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "<FOREST SYMBOL>"
Forest-Layer: "<FOREST LAYER>"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# <SYMBOL> <TERM>

## Canonical Definition

State the single approved meaning.

## Engineering Meaning

Describe the exact component, behavior, file type, or operation represented.

## Represents

- <ITEM>

## Does Not Represent

- <ITEM>

## Relationships

- Path to FOREST-XXXX — <RELATIONSHIP>

## Commands

```text
<COMMAND>
```

Meaning: <EXACT OPERATION>

## Examples

### Correct

- <EXAMPLE>

### Incorrect

- <EXAMPLE>

## History

Describe earlier meanings, proposals, and superseded interpretations.

## Change Rules

This term must not change meaning without an approved RCR and corresponding updates to the Forest indexes.

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 3. Forest Language Specification

**Edit command**

```bash
nano ~/pdc-forest-language/specifications/FOREST-SPEC.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "FOREST-SPEC"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Forest Language Specification"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🧭"
Forest-Layer: "Compass"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# FOREST-SPEC — Forest Language Entry Specification

## Purpose

Define the requirements for canonical Forest language entries.

## Required Sections

1. Canonical Definition
2. Engineering Meaning
3. Represents
4. Does Not Represent
5. Relationships
6. Commands, when applicable
7. Examples
8. History
9. Change Rules
10. Revision History
11. Forest Compass inscription

## Canonicality Rules

1. One approved term MUST have one canonical meaning.
2. A symbol MUST NOT silently acquire a second technical meaning.
3. Earlier meanings MUST be recorded as superseded or placed in Leaf Litter.
4. Natural-language command variants MAY map to the same precise operation.
5. Ambiguity MAY be intentional in lore or presentation, but technical behavior MUST remain defined.
6. Terms marked Reserved or Undefined MUST NOT be used as official components.

## Change Process

A canonical meaning may change only through:

1. An approved RCR.
2. Updated `FOREST-LANGUAGE.md`.
3. Updated entry record.
4. Updated indexes and Paths.
5. Preserved history of the old meaning.

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 4. Forest Signature

**Edit command**

```bash
nano ~/pdc-forest-language/design/FOREST-SIGNATURE.md
```

**Paste this into the file**

~~~~markdown
# Forest Signature

The Forest Signature is the permanent identity statement placed near the bottom of every official Project Digital Cross document.

## Canonical Text

> **Project Digital Cross**
>
> *In God we trust.*  
> *In the Forest we wonder.*

The wording must not change without an approved governance change.

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 5. Forest Compass

**Edit command**

```bash
nano ~/pdc-forest-language/design/FOREST-COMPASS.md
```

**Paste this into the file**

~~~~markdown
# Forest Compass

The Forest Compass is the navigation and orientation component used in Project Digital Cross documents.

## Canonical Inscription

> *This record is written to be your guide and map through the Forest.*
>
> *It grows as you walk.*

The wording is intentionally ambiguous, mysterious, and cautionary.

It signals that:

- The Forest expands as people explore and interact with it.
- Trees grow faster when used, cared for, corrected, and fed knowledge.
- Records may lead into deeper nested Paths and Roots.
- The reader is entering a layered language and architecture.
- Exploration changes both the map and the Forest.

## Navigation Form

Use:

```text
Path to ADR-0004
```

instead of:

```text
See ADR-0004
```

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 6. PDC Document Design Standard

**Edit command**

```bash
nano ~/project-digital-cross/governance/standards/PDC-STD-0007-DocumentDesign.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "PDC-STD-0007"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "PDC Standard"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🧭"
Forest-Layer: "Compass"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# PDC-STD-0007 — Document Design

## Purpose

Define the shared style and structural rules for official Project Digital Cross Markdown documents.

## Requirements

1. Every governed document MUST include the Triple Identity System:
   - PDC-ID
   - UUID
   - Canonical Path
2. Governed record prefixes MUST remain uppercase.
3. Directories and ordinary machine-readable filenames MAY remain lowercase.
4. Every document MUST state Version, Status, Season, Growth Ring, Author, Created, and Last Updated.
5. Reader-facing cross-references MUST use `Path to <PDC-ID>`.
6. Every official document MUST end with the Forest Compass inscription.
7. README files MUST be shown last in repository diagrams unless accessibility or platform behavior requires otherwise.
8. Technical meaning MUST remain available beneath Forest terminology.
9. Markdown heading levels MUST not skip levels.
10. Tables and code blocks MUST remain readable in plain text.

## Accessibility

- Do not rely on emoji alone to convey meaning.
- Use clear text labels with symbols.
- Avoid decorative formatting that harms screen-reader navigation.
- Keep tables and line lengths reasonably readable.

## Conformance

A document conforms when its required metadata, sections, Paths, revision history, and inscription are present and valid.

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 7. Universal Document Specification

**Edit command**

```bash
nano ~/project-digital-cross/governance/specifications/PDC-DOC-SPEC.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "PDC-DOC-SPEC"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Document Specification"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🧭"
Forest-Layer: "Compass"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# PDC-DOC-SPEC — Universal Document Specification

## Purpose

Define the shared metadata and structural contract inherited by Project Digital Cross document types.

## Required Triple Identity

| Field | Meaning |
|---|---|
| PDC-ID | Stable human-readable identifier |
| UUID | Immutable machine identity |
| Canonical-Path | Repository-relative location |

## Required Metadata

- Title
- Record-Type
- Version
- Status
- Classification
- Priority
- Season
- Growth-Ring
- Author
- Custodian
- Created
- Last-Updated
- Forest-Symbol
- Forest-Layer
- Relationships
- Tags

## Required Common Sections

1. Purpose
2. Record-specific content
3. Paths or Relationships
4. Revision History
5. Forest Compass inscription

## Inheritance

Record-specific Specifications MAY add required sections and validation rules but MUST NOT remove the Triple Identity System or closing inscription.

## Validation

- Metadata parses as YAML.
- UUID is valid and unique.
- PDC-ID is unique within its record family.
- Canonical path exists and is registered.
- Paths resolve.
- Required sections are present.
- Footer matches the approved Forest Compass inscription.

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 8. Universal Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/universal/PDC-UNIVERSAL-RECORD-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "<HUMAN-ID>"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "<RECORD-TYPE>"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "<SYMBOL>"
Forest-Layer: "<LAYER>"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# <TITLE>

## Purpose

State why this record exists and what it is intended to preserve, govern, explain, request, or change.

## Summary

Provide a brief overview that can be understood without reading the entire record.

## Scope

### Included

- <ITEM>

### Excluded

- <ITEM>

## Content

Write the record-specific content here.

## Forest Metadata

### Roots

- Path to <PDC-ID> — <WHY IT GOVERNS OR SUPPORTS THIS RECORD>

### Leaves

- <EVIDENCE OR SOURCE USED>

### Buds

- <POSSIBILITY LEFT OPEN>

### Blossoms

- <DRAFT OR PROPOSAL PRODUCED>

### Fruit

- <FINAL DELIVERABLE OR RESULT>

### Leaf Litter

- <DISCARDED OR SUPERSEDED ITEM AND LESSON>

## Relationships

### Paths

- Path to <PDC-ID>

### Dependencies

- <DEPENDENCY>

### Conflicts

- <KNOWN CONFLICT OR "None">

## Validation

- [ ] PDC-ID assigned
- [ ] UUID generated and registered
- [ ] Canonical path registered
- [ ] Required Roots checked
- [ ] Paths resolve
- [ ] References verified
- [ ] Status and version updated
- [ ] Revision history updated

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 9. Constitution Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/constitution/CONSTITUTION-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "PDC-CONSTITUTION"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Constitution"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "❤️"
Forest-Layer: "Heart"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# <CONSTITUTION TITLE>

## Preamble

State what Project Digital Cross is, why it exists, and whom it serves.

## Mission

<MISSION>

## Vision

<VISION>

## Values

1. <VALUE>
2. <VALUE>
3. <VALUE>

## Scope

### The Constitution Governs

- <AREA>

### The Constitution Does Not Define

- <IMPLEMENTATION DETAIL>

## Authority

Explain the relationship among the user, Constitution, Standards, Specifications, Records, Trees, and implementations.

## Rights and Responsibilities

### User Rights

- <RIGHT>

### Tree Responsibilities

- <RESPONSIBILITY>

### Contributor Responsibilities

- <RESPONSIBILITY>

## Governance Hierarchy

1. User authority
2. Constitution
3. Standards
4. Specifications
5. Principle Records
6. Architecture Decision Records
7. Change and operational records
8. Implementation
9. Runtime state

## Amendment Process

Describe how amendments are proposed, reviewed, accepted, recorded, and superseded.

## Paths

- Path to <PDC-ID>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 10. Standard Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/standards/STANDARD-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "PDC-STD-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "PDC Standard"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌱"
Forest-Layer: "Roots"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# PDC-STD-XXXX — <STANDARD TITLE>

## Purpose

Explain the universal rule this Standard establishes.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are requirements.

## Requirements

### Required

1. <REQUIREMENT>

### Prohibited

1. <PROHIBITION>

### Recommended

1. <RECOMMENDATION>

## Conformance

Explain how a file, Tree, repository, tool, or service demonstrates compliance.

## Exceptions

Describe how exceptions are requested, approved, documented, and retired.

## Validation

- [ ] Requirements are testable
- [ ] Conflicts with higher authority checked
- [ ] Related Specifications identified
- [ ] Paths registered

## Paths

- Path to <PDC-ID>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 11. Specification Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/specifications/SPECIFICATION-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "<PREFIX>-SPEC"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Specification"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌱"
Forest-Layer: "Roots"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# <PREFIX>-SPEC — <SPECIFICATION TITLE>

## Purpose

Define what makes this artifact type valid.

## Applies To

- <FILE OR RECORD TYPE>

## Required Metadata

| Field | Required | Format | Meaning |
|---|---:|---|---|
| PDC-ID | Yes | `<PREFIX>-NNNN` | Human-readable identity |
| UUID | Yes | UUIDv4 | Immutable machine identity |
| Canonical-Path | Yes | Repository-relative path | Repository identity |

## Required Sections

1. <SECTION>
2. <SECTION>

## Optional Sections

- <SECTION>

## Prohibited Content

- <CONTENT THAT DOES NOT BELONG IN THIS TYPE>

## Lifecycle

```text
Draft -> Proposed -> Accepted -> Superseded -> Archived
```

## Numbering and Naming

```text
<PREFIX>-0001-Readable-Title.md
```

## Validation Rules

1. <RULE>

## Paths

- Path to <PDC-ID>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 12. Principle Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/principles/PR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "PR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Principle Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌱"
Forest-Layer: "Roots"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# PR-XXXX — <PRINCIPLE TITLE>

## Principle

> <ONE-SENTENCE PRINCIPLE>

## Purpose

Explain why this Principle is necessary.

## Rationale

Explain the values, risks, and long-term goals behind it.

## Required Behavior

- <WHAT THIS PRINCIPLE REQUIRES>

## Violations

- <EXAMPLE OF MISALIGNED BEHAVIOR>

## Examples

### Aligned

- <EXAMPLE>

### Misaligned

- <EXAMPLE>

## Implications

Explain how the Principle affects architecture, operations, Trees, contributors, and users.

## Paths

- Path to <ADR OR STANDARD>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 13. Architecture Decision Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/architecture/ADR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "ADR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Architecture Decision Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌿"
Forest-Layer: "Branch"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# ADR-XXXX — <DECISION TITLE>

## Context

Describe the situation, constraints, forces, and governing Roots.

## Problem Statement

State the architectural problem being decided.

## Decision

State the chosen architecture clearly.

## Decision Drivers

- <DRIVER>

## Alternatives Considered

### Option A — <NAME>

**Benefits**

- <BENEFIT>

**Costs / Risks**

- <COST>

### Option B — <NAME>

**Benefits**

- <BENEFIT>

**Costs / Risks**

- <COST>

## Consequences

### Positive

- <POSITIVE CONSEQUENCE>

### Negative

- <NEGATIVE CONSEQUENCE>

### Accepted Trade-offs

- <TRADE-OFF>

## Implementation Guidance

Describe what future implementations must preserve without turning this ADR into a procedure.

## Reversal or Supersession Conditions

Describe evidence that would justify revisiting the decision.

## Paths

- Path to <PR>
- Path to <ICR OR RCR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 14. Infrastructure Change Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/infrastructure/ICR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "ICR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Infrastructure Change Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌊"
Forest-Layer: "Stream"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# ICR-XXXX — <INFRASTRUCTURE CHANGE TITLE>

## Change Summary

Summarize the infrastructure change.

## Reason

Explain why the change was necessary.

## Affected Earth, Services, or Streams

- <SYSTEM OR SERVICE>

## Previous State

Describe the known configuration before the change.

## Planned Change

Describe the exact intended change.

## Preconditions

- [ ] Backup or rollback data available
- [ ] Dependencies identified
- [ ] Required access confirmed
- [ ] Maintenance risk understood

## Change Procedure

1. <STEP>
2. <STEP>

## Verification

1. <TEST>
2. <TEST>

## Rollback Plan

1. <ROLLBACK STEP>
2. <ROLLBACK STEP>

## Actual Result

Record what actually happened, including deviations.

## Leaf Litter Created

- <REMOVED OR SUPERSEDED CONFIGURATION>

## Lessons

- <LESSON>

## Paths

- Path to <ADR>
- Path to <SCR OR NCR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 15. Security Change Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/security/SCR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "SCR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Security Change Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "❤️"
Forest-Layer: "Heart"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# SCR-XXXX — <SECURITY CHANGE TITLE>

## Security Objective

State what security property this change protects.

## Threat or Risk

Describe the threat, exposure, weakness, or compliance concern.

## Scope

- <SYSTEM, IDENTITY, TREE, EARTH, STREAM, OR RECORD>

## Current Controls

- <CONTROL>

## Change

Describe the security change.

## Access and Authority

Identify who or what may approve, execute, review, and reverse the change.

## Secrets Handling

Do not place secrets in this record. Document only the approved storage and retrieval method.

## Verification

- [ ] Access tested
- [ ] Authentication or MFA tested
- [ ] Logging verified
- [ ] Recovery verified
- [ ] Least privilege reviewed

## Incident / Rollback Plan

Describe containment and rollback steps.

## Residual Risk

- <RISK THAT REMAINS>

## Paths

- Path to <PR>
- Path to <ADR>
- Path to <ICR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 16. Network Change Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/networking/NCR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "NCR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Network Change Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌊"
Forest-Layer: "Stream"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# NCR-XXXX — <NETWORK CHANGE TITLE>

## Network Objective

State the connectivity or isolation goal.

## Scope

- <EARTH>
- <NETWORK>
- <STREAM>
- <SERVICE>

## Current Topology

Describe the known current state.

## Proposed Topology

Describe the intended state.

## Addresses, Ports, and Protocols

| Component | Address / Name | Port | Protocol | Direction |
|---|---|---:|---|---|
| <COMPONENT> | <VALUE> | <PORT> | <PROTOCOL> | <IN/OUT/BOTH> |

## Trust Boundaries

- <BOUNDARY>

## Change Procedure

1. <STEP>

## Validation

- [ ] Connectivity tested
- [ ] Isolation tested
- [ ] DNS tested
- [ ] Firewall rules reviewed
- [ ] Remote access tested
- [ ] Rollback documented

## Rollback

1. <STEP>

## Paths

- Path to <ADR>
- Path to <SCR>
- Path to <ICR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 17. Memory Requirement Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/memory/MRR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "MRR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Memory Requirement Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🪵"
Forest-Layer: "Roots"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# MRR-XXXX — <MEMORY REQUIREMENT TITLE>

## Memory Goal

State what the Tree or Heart must remember, forget, separate, retrieve, or protect.

## Memory Class

- [ ] Temporary
- [ ] Project
- [ ] User
- [ ] Long-term
- [ ] Archival
- [ ] Shared
- [ ] Tree-specific

## Requirement

State the required behavior precisely.

## Ownership

Identify who owns the data and who may access it.

## Scope and Separation

Describe boundaries among users, projects, Trees, sessions, and administrators.

## Retention

| Data | Retention | Expiration Trigger | Archive Policy |
|---|---|---|---|
| <DATA> | <DURATION> | <TRIGGER> | <POLICY> |

## Forgetting

Describe user-requested forgetting, automatic decay, correction handling, and audit behavior.

## Retrieval

Describe how memory is found by PDC-ID, UUID, path, relationship, user, project, or time.

## Privacy and Security

- <REQUIREMENT>

## Tests

1. <TEST>

## Paths

- Path to <PR>
- Path to <ADR>
- Path to <SCR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 18. Operational Procedure Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/operations/OPR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "OPR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Operational Procedure Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🧭"
Forest-Layer: "Compass"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# OPR-XXXX — <PROCEDURE TITLE>

## Objective

State the operational outcome.

## When to Use

- <TRIGGER OR CONDITION>

## When Not to Use

- <CONDITION>

## Required Access and Tools

- <ACCESS OR TOOL>

## Preconditions

- [ ] <CHECK>

## Procedure

1. <STEP>
2. <STEP>

## Expected Result

Describe what success looks like.

## Verification

1. <CHECK>

## Failure Handling

Describe what to do if a step fails.

## Rollback or Recovery

1. <STEP>

## Evidence to Record

- <LOG, SCREENSHOT, HASH, TEST, OR CHANGE RECORD>

## Paths

- Path to <ICR>
- Path to <SCR>
- Path to <NCR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 19. Bug and Postmortem Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/bugs/BPR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "BPR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Bug and Postmortem Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🍂"
Forest-Layer: "Leaf-Litter"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# BPR-XXXX — <BUG OR INCIDENT TITLE>

## Summary

Describe what failed and its effect.

## Detection

Explain how the issue was discovered.

## Impact

- Users affected:
- Trees affected:
- Earths affected:
- Data affected:
- Duration:

## Timeline

| Time | Event |
|---|---|
| <TIME> | <EVENT> |

## Symptoms

- <SYMPTOM>

## Root Cause

Explain technical and process causes. Distinguish true Roots from surface symptoms.

## Contributing Factors

- <FACTOR>

## Resolution

Describe what restored service or corrected the defect.

## Verification

- <TEST>

## Leaf Litter

List broken, discarded, or superseded files and components.

## Lessons

- <LESSON>

## Corrective Actions

| Action | Owner | Status | Path |
|---|---|---|---|
| <ACTION> | <OWNER> | <STATUS> | Path to <RECORD> |

## Paths

- Path to <ADR>
- Path to <ICR>
- Path to <SCR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 20. Request Change Record Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/records/requests/RCR-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
---
PDC-ID: "RCR-XXXX"
UUID: "<GENERATE-UUID>"
Canonical-Path: "<REPOSITORY-RELATIVE-PATH>"

Title: "<TITLE>"
Record-Type: "Request Change Record"
Version: "0.1.0"
Status: "Draft"
Classification: "Internal"
Priority: "Normal"

Season: "<Spring|Summer|Autumn|Winter>"
Growth-Ring: "<DRAFT-OR-MILESTONE>"

Author:
  - "Maciono Brown"
Custodian:
  - "Maciono Brown"
Reviewers: []

Created: "<YYYY-MM-DD>"
Last-Updated: "<YYYY-MM-DD>"

Forest-Symbol: "🌱"
Forest-Layer: "Bud"

Related-Records: []
Depends-On: []
Supersedes: []
Superseded-By: []
Paths: []

Tags: []
---
# RCR-XXXX — <CHANGE REQUEST TITLE>

## Request

State the requested change.

## Requester

- Name:
- Role:
- Date:

## Motivation

Explain the need, pain point, opportunity, or risk.

## Desired Outcome

Describe success without prematurely prescribing implementation.

## Scope

### Included

- <ITEM>

### Excluded

- <ITEM>

## Buds

List candidate approaches without selecting one yet.

1. <APPROACH>

## Impact Areas

- [ ] Constitution
- [ ] Standards
- [ ] Specifications
- [ ] Principles
- [ ] Architecture
- [ ] Infrastructure
- [ ] Networking
- [ ] Security
- [ ] Memory
- [ ] Operations
- [ ] Trees
- [ ] Bark
- [ ] Forest Language

## Review

### Benefits

- <BENEFIT>

### Costs and Risks

- <COST OR RISK>

### Dependencies

- <DEPENDENCY>

## Decision

- [ ] Pending
- [ ] Approved
- [ ] Rejected
- [ ] Deferred
- [ ] Superseded

### Decision Rationale

<RATIONALE>

## Resulting Paths

- Path to <PR, ADR, ICR, SCR, NCR, MRR, OR OPR>

## Revision History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.1.0 | <YYYY-MM-DD> | Maciono Brown | Initial working draft |

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 21. README Template

**Edit command**

```bash
nano ~/project-digital-cross/templates/README-TEMPLATE.md
```

**Paste this into the file**

~~~~markdown
# <DIRECTORY OR REPOSITORY NAME>

## Purpose

Explain what belongs here and why this area exists.

## Authority

State which Constitution, Standard, Specification, or Record governs this area.

## Contents

| Path | Purpose |
|---|---|
| `<PATH>` | <PURPOSE> |

## What Belongs Here

- <ITEM>

## What Does Not Belong Here

- <ITEM>

## Naming Rules

- <RULE>

## Paths

- Path to <PDC-ID>

## Maintenance

- Custodian:
- Review cadence:
- Current Season:
- Current Growth Ring:

---
**Project Digital Cross**

*In God we trust.*  
*In the Forest we wonder.*

*This record is written to be your guide and map through the Forest.*

*It grows as you walk.*
~~~~

# 22. Cherry Tree Manifest

**Edit command**

```bash
nano ~/project-digital-cross/trees/cherry/TREE.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "TREE-CHERRY"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/cherry"

display_name: "CHERRY"
species: "Cherry"
status: "Sprout"
version: "0.1.0"
season: "Spring"
growth_ring: "Draft 11"

heart:
  path: "heart"
  required: true

roots:
  constitution:
    - "PDC-CONSTITUTION"
  principles: []
  standards: []
  specifications: []
  decisions: []

grain:
  path: "trees/cherry/grain/grain.yaml"

reasoning_profile:
  path: "trees/cherry/reasoning/reasoning-profile.yaml"

branches: []
bark: []
tools: []
models: []

authority:
  user_is_final: true
  peer_trees: []

registry:
  pdc_index: "governance/index/pdc-index.yaml"
  uuid_index: "governance/index/uuid-index.yaml"
  path_index: "governance/index/path-index.yaml"
  relationship_index: "governance/index/relationship-index.yaml"
~~~~

# 23. Maple Tree Manifest

**Edit command**

```bash
nano ~/project-digital-cross/trees/maple/TREE.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "TREE-MAPLE"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/maple"

display_name: "MAPLE"
species: "Maple"
status: "Sprout"
version: "0.1.0"
season: "Spring"
growth_ring: "Draft 11"

heart:
  path: "heart"
  required: true

roots:
  constitution:
    - "PDC-CONSTITUTION"
  principles: []
  standards: []
  specifications: []
  decisions: []

grain:
  path: "trees/maple/grain/grain.yaml"

reasoning_profile:
  path: "trees/maple/reasoning/reasoning-profile.yaml"

branches: []
bark: []
tools: []
models: []

authority:
  user_is_final: true
  peer_trees: []

registry:
  pdc_index: "governance/index/pdc-index.yaml"
  uuid_index: "governance/index/uuid-index.yaml"
  path_index: "governance/index/path-index.yaml"
  relationship_index: "governance/index/relationship-index.yaml"
~~~~

# 24. Cherry Grain Base

**Edit command**

```bash
nano ~/project-digital-cross/trees/cherry/grain/grain.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "GRAIN-CHERRY"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/cherry/grain/grain.yaml"

tree: "TREE-CHERRY"
version: "0.1.0"
status: "Draft"

traits:
  - name: "<TRAIT>"
    strength: "<low|medium|high>"
    expression: "<HOW THE TRAIT APPEARS>"
    limits: "<WHAT THE TRAIT MUST NOT OVERRIDE>"

communication:
  tone: "<TONE>"
  detail_level: "<LOW|MEDIUM|HIGH>"
  uncertainty_style: "<STYLE>"
  correction_style: "<STYLE>"

governance:
  inherits_constitution: true
  may_override_roots: false
  user_has_final_authority: true
~~~~

# 25. Maple Grain Base

**Edit command**

```bash
nano ~/project-digital-cross/trees/maple/grain/grain.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "GRAIN-MAPLE"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/maple/grain/grain.yaml"

tree: "TREE-MAPLE"
version: "0.1.0"
status: "Draft"

traits:
  - name: "<TRAIT>"
    strength: "<low|medium|high>"
    expression: "<HOW THE TRAIT APPEARS>"
    limits: "<WHAT THE TRAIT MUST NOT OVERRIDE>"

communication:
  tone: "<TONE>"
  detail_level: "<LOW|MEDIUM|HIGH>"
  uncertainty_style: "<STYLE>"
  correction_style: "<STYLE>"

governance:
  inherits_constitution: true
  may_override_roots: false
  user_has_final_authority: true
~~~~

# 26. Cherry Reasoning Profile Base

**Edit command**

```bash
nano ~/project-digital-cross/trees/cherry/reasoning/reasoning-profile.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "REASONING-CHERRY"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/cherry/reasoning/reasoning-profile.yaml"

tree: "TREE-CHERRY"
version: "0.1.0"
status: "Draft"
season: "Spring"

optimization_priorities:
  - "<PRIORITY>"

default_methods:
  ambiguity_detection: true
  multi_hypothesis: true
  confidence_scoring: true
  self_correction: true
  independent_review: true

evidence:
  rustle_limit: 5
  drop_scope: "direct"
  shake_scope: "full-provenance"

roots:
  show_depth: 1
  dig_depth: "recursive"

divergence:
  allowed: true
  surface_to_user: true
  user_is_final: true
~~~~

# 27. Maple Reasoning Profile Base

**Edit command**

```bash
nano ~/project-digital-cross/trees/maple/reasoning/reasoning-profile.yaml
```

**Paste this into the file**

~~~~yaml
human_id: "REASONING-MAPLE"
uuid: "<GENERATE-UUID>"
canonical_path: "trees/maple/reasoning/reasoning-profile.yaml"

tree: "TREE-MAPLE"
version: "0.1.0"
status: "Draft"
season: "Spring"

optimization_priorities:
  - "<PRIORITY>"

default_methods:
  ambiguity_detection: true
  multi_hypothesis: true
  confidence_scoring: true
  self_correction: true
  independent_review: true

evidence:
  rustle_limit: 5
  drop_scope: "direct"
  shake_scope: "full-provenance"

roots:
  show_depth: 1
  dig_depth: "recursive"

divergence:
  allowed: true
  surface_to_user: true
  user_is_final: true
~~~~

# 28. PDC Object Index Base

**Edit command**

```bash
nano ~/project-digital-cross/governance/index/pdc-index.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"
updated: "<YYYY-MM-DD>"

objects:
  "<PDC-ID>":
    uuid: "<UUID>"
    title: "<TITLE>"
    type: "<TYPE>"
    canonical_path: "<PATH>"
    status: "<STATUS>"
    version: "<VERSION>"
    season: "<SEASON>"
~~~~

# 29. UUID Index Base

**Edit command**

```bash
nano ~/project-digital-cross/governance/index/uuid-index.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"
updated: "<YYYY-MM-DD>"

uuids:
  "<UUID>":
    pdc_id: "<PDC-ID>"
    canonical_path: "<PATH>"
    status: "<STATUS>"
~~~~

# 30. Canonical Path Index Base

**Edit command**

```bash
nano ~/project-digital-cross/governance/index/path-index.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"
updated: "<YYYY-MM-DD>"

paths:
  "<CANONICAL-PATH>":
    pdc_id: "<PDC-ID>"
    uuid: "<UUID>"
    aliases: []
    previous_paths: []
~~~~

# 31. Relationship Index Base

**Edit command**

```bash
nano ~/project-digital-cross/governance/index/relationship-index.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"
updated: "<YYYY-MM-DD>"

relationships:
  - source: "<PDC-ID-OR-UUID>"
    type: "<implements|requires|supersedes|extends|references|governs|depends-on|derived-from|validated-by|path-to>"
    target: "<PDC-ID-OR-UUID>"
    note: "<OPTIONAL NOTE>"
~~~~

# 32. Root Map Base

**Edit command**

```bash
nano ~/project-digital-cross/heart/roots/root-map.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"
updated: "<YYYY-MM-DD>"

trees:
  "TREE-CHERRY":
    constitution: []
    principles: []
    standards: []
    specifications: []
    decisions: []
    requirements: []

  "TREE-MAPLE":
    constitution: []
    principles: []
    standards: []
    specifications: []
    decisions: []
    requirements: []
~~~~

# 33. Relationship Types Base

**Edit command**

```bash
nano ~/project-digital-cross/governance/relationships/relationship-types.yaml
```

**Paste this into the file**

~~~~yaml
schema_version: "0.1.0"

relationship_types:
  implements:
    inverse: "implemented-by"
    description: "The source puts the target into effect."

  requires:
    inverse: "required-by"
    description: "The source cannot be valid or complete without the target."

  supersedes:
    inverse: "superseded-by"
    description: "The source replaces the target while preserving its history."

  extends:
    inverse: "extended-by"
    description: "The source adds to the target without replacing it."

  references:
    inverse: "referenced-by"
    description: "The source points to the target for context or evidence."

  governs:
    inverse: "governed-by"
    description: "The source has governing authority over the target."

  depends-on:
    inverse: "dependency-of"
    description: "The source relies on the target."

  derived-from:
    inverse: "source-of"
    description: "The source was produced from the target."

  validated-by:
    inverse: "validates"
    description: "The source is checked or confirmed by the target."

  path-to:
    inverse: "path-from"
    description: "The source presents a navigable Forest Path to the target."
~~~~

# 34. Universal Record Metadata Schema

**Edit command**

```bash
nano ~/project-digital-cross/governance/schemas/universal-record.schema.json
```

**Paste this into the file**

~~~~json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "PDC-SCHEMA-UNIVERSAL-RECORD",
  "title": "PDC Universal Record Metadata",
  "type": "object",
  "required": [
    "PDC-ID",
    "UUID",
    "Canonical-Path",
    "Title",
    "Record-Type",
    "Version",
    "Status",
    "Season",
    "Author",
    "Created",
    "Last-Updated"
  ],
  "properties": {
    "PDC-ID": { "type": "string", "minLength": 1 },
    "UUID": { "type": "string", "format": "uuid" },
    "Canonical-Path": { "type": "string", "minLength": 1 },
    "Title": { "type": "string", "minLength": 1 },
    "Record-Type": { "type": "string", "minLength": 1 },
    "Version": { "type": "string", "minLength": 1 },
    "Status": { "type": "string", "minLength": 1 },
    "Season": {
      "type": "string",
      "enum": ["Spring", "Summer", "Autumn", "Winter"]
    },
    "Author": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "Created": { "type": "string", "format": "date" },
    "Last-Updated": { "type": "string", "format": "date" }
  },
  "additionalProperties": true
}
~~~~

# 35. Relationship Schema

**Edit command**

```bash
nano ~/project-digital-cross/governance/schemas/relationship.schema.json
```

**Paste this into the file**

~~~~json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "PDC-SCHEMA-RELATIONSHIP",
  "title": "PDC Relationship",
  "type": "object",
  "required": ["source", "type", "target"],
  "properties": {
    "source": { "type": "string", "minLength": 1 },
    "type": {
      "type": "string",
      "enum": [
        "implements",
        "requires",
        "supersedes",
        "extends",
        "references",
        "governs",
        "depends-on",
        "derived-from",
        "validated-by",
        "path-to"
      ]
    },
    "target": { "type": "string", "minLength": 1 },
    "note": { "type": "string" }
  },
  "additionalProperties": false
}
~~~~

# 36. Tree Manifest Schema

**Edit command**

```bash
nano ~/project-digital-cross/governance/schemas/tree.schema.json
```

**Paste this into the file**

~~~~json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "PDC-SCHEMA-TREE",
  "title": "PDC Tree Manifest",
  "type": "object",
  "required": [
    "human_id",
    "uuid",
    "canonical_path",
    "display_name",
    "species",
    "status",
    "heart",
    "grain",
    "reasoning_profile",
    "authority"
  ],
  "properties": {
    "human_id": { "type": "string", "pattern": "^TREE-[A-Z0-9-]+$" },
    "uuid": { "type": "string", "format": "uuid" },
    "canonical_path": { "type": "string", "minLength": 1 },
    "display_name": { "type": "string", "minLength": 1 },
    "species": { "type": "string", "minLength": 1 },
    "status": { "type": "string", "minLength": 1 },
    "heart": { "type": "object" },
    "grain": { "type": "object" },
    "reasoning_profile": { "type": "object" },
    "authority": { "type": "object" }
  },
  "additionalProperties": true
}
~~~~

# Recommended Editing Order

1. `FOREST-LANGUAGE.md`
2. `FOREST-SPEC.md`
3. `FOREST-SIGNATURE.md`
4. `FOREST-COMPASS.md`
5. `PDC-STD-0007-DocumentDesign.md`
6. `PDC-DOC-SPEC.md`
7. `PDC-UNIVERSAL-RECORD-TEMPLATE.md`
8. Record-specific templates
9. Cherry and Maple manifests, Grain, and reasoning profiles
10. Indexes and schemas

Do not assign permanent UUIDs until the document names and meanings are approved. Once approved, generate each UUID once, register it in `uuid-index.yaml`, and never reuse it.
