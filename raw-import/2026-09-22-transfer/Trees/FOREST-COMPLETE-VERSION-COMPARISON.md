# The Forest — Complete Version Comparison

## Purpose

This report compares every preserved Forest Language stage in exact generation order, the associated YAML architecture families, the Draft 11 package sequence, patches, audits, and supporting review/specification files.

It does not modify, rename, replace, or delete any source artifact. The comparison uses exact semantic-version matching so versions such as `0.13.1`, `0.13.10`, and `0.13.11` are treated as distinct versions.

## Scope and evidence

- **Forest Language stages compared:** 53
- **Distinct YAML component families compared:** 44
- **YAML component versions compared:** 144
- **Draft 11 ZIP packages compared:** 7
- **Other supporting text artifacts inventoried:** 21
- **Integrity-manifest entries:** 323

The comparison is based on the actual contents of the preserved files. Filename titles and audit statements are used as documented intent; line and heading deltas are computed independently from the files.

## Executive findings

1. The preserved Forest Language grew from **731 lines / 2,758 words** in the first 0.2 working draft to **13,246 lines / 71,332 words** in 0.13.35. That is an increase of **12,515 lines** and **68,574 words**, or approximately **18.1×** as many lines and **25.9×** as many words.
2. The H2-level structure grew from **47** sections to **64** sections, while total Markdown headings grew from **56** to **459**.
3. The largest expansion occurred in 0.13.31, when Spirit Tools, the command registry, governance-copy slots, and Seed Vault architecture were added.
4. The latest preserved document still declares `Status: Working Draft`. No artifact currently declares the Forest Language final, approved, or canonical-release status.
5. `Supersedes` and `Superseded-By` fields remain empty in the reviewed language files. Version lineage is therefore inferred from exact semantic version order and generation evidence rather than explicit frontmatter links.
6. No duplicate H2 headings were found in the 53 compared language stages.
7. H2 count reductions in later versions mostly reflect sections being moved under Spirit Tools rather than deleted—for example Seed Vault and Log Cabin became Tool-contained architecture.
8. The latest frozen reference is 0.13.35, but the final version number and final approval status remain unresolved.

## Supporting data files

- [FOREST-LANGUAGE-VERSION-METRICS.csv](sandbox:/mnt/data/FOREST-LANGUAGE-VERSION-METRICS.csv) — one row per Forest Language stage
- [FOREST-COMPONENT-VERSION-DELTAS.csv](sandbox:/mnt/data/FOREST-COMPONENT-VERSION-DELTAS.csv) — full YAML key-path additions and removals
- [FOREST-VERSION-SHA256SUMS.txt](sandbox:/mnt/data/FOREST-VERSION-SHA256SUMS.txt) — SHA-256 integrity manifest

## Draft 11 package progression

| Stage | Package | Files | Embedded Forest Language | Δ lines | Similarity | SHA-256 |
|---:|---|---:|---:|---:|---:|---|
| 1 | [PDC-Template-Library-Draft11-Updated.zip](sandbox:/mnt/data/PDC-Template-Library-Draft11-Updated.zip) | 43 | 383 lines | Baseline | — | `a720171d76b7d9f7…` |
| 2 | [PDC-Security-Expansion-Draft11.zip](sandbox:/mnt/data/PDC-Security-Expansion-Draft11.zip) | 36 | 1,025 lines | +759 / −117 | 37.78% | `9880598b8c42730d…` |
| 3 | [PDC-Containment-Disposal-Replanting-Draft11.zip](sandbox:/mnt/data/PDC-Containment-Disposal-Replanting-Draft11.zip) | 5 | 1,231 lines | +218 / −12 | 89.80% | `b4da32765cdef51d…` |
| 4 | [PDC-Forest-Compass-Map-Draft11.zip](sandbox:/mnt/data/PDC-Forest-Compass-Map-Draft11.zip) | 6 | 1,480 lines | +257 / −8 | 90.23% | `b327604dcffb130a…` |
| 5 | [PDC-Voice-of-the-Forest-Draft11.zip](sandbox:/mnt/data/PDC-Voice-of-the-Forest-Draft11.zip) | 5 | 1,504 lines | +182 / −158 | 88.61% | `fcd33a48a99e2b75…` |
| 6 | [PDC-Voice-of-the-Forest-Unified-Draft11.zip](sandbox:/mnt/data/PDC-Voice-of-the-Forest-Unified-Draft11.zip) | 5 | 1,502 lines | +17 / −19 | 98.80% | `cb33a2e0ebd291da…` |
| 7 | [PDC-Draft11-Reviewed-Optimized.zip](sandbox:/mnt/data/PDC-Draft11-Reviewed-Optimized.zip) | 93 | 2,451 lines | +1,363 / −414 | 55.05% | `67b026d7b57a189f…` |

### Draft 11 interpretation

- The Template Library package established the first broad repository/template scaffold.
- Security Expansion added Cedar-focused defensive structure.
- Containment/Disposal/Replanting expanded destructive and recovery lifecycle controls.
- Forest Compass/Map expanded orientation and navigation.
- Voice and Unified Voice consolidated user-facing guidance.
- Reviewed Optimized assembled the broadest Draft 11 package and its embedded Forest Language matches the preserved 0.12.1 reviewed baseline in line and word count.

## Forest Language master comparison

| Seq. | Version/stage | Primary artifact | Lines | Words | H2 | Δ lines vs prior | Similarity | Audit |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 1 | `0.2.0` | [FOREST-LANGUAGE-Working-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.2.md) | 731 | 2,758 | 47 | Baseline | — | — |
| 2 | `0.2.0 review copy` | [FOREST-LANGUAGE-Review-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.2.md) | 743 | 2,797 | 48 | +12 / −0 | 99.19% | — |
| 3 | `0.3.0` | [FOREST-LANGUAGE-Working-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.3.md) | 780 | 3,000 | 48 | +50 / −13 | 95.86% | — |
| 4 | `0.3.0 review copy` | [FOREST-LANGUAGE-Review-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.3.md) | 794 | 3,056 | 50 | +14 / −0 | 99.11% | — |
| 5 | `0.4.0` | [FOREST-LANGUAGE-Working-Draft-0.4.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.4.md) | 1,025 | 4,088 | 53 | +263 / −32 | 83.78% | — |
| 6 | `0.5.0` | [FOREST-LANGUAGE-Working-Draft-0.5.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.5.md) | 1,231 | 4,926 | 58 | +218 / −12 | 89.80% | — |
| 7 | `0.6.0` | [FOREST-LANGUAGE-Working-Draft-0.6.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.6.md) | 1,480 | 5,849 | 59 | +257 / −8 | 90.23% | — |
| 8 | `0.7.0` | [FOREST-LANGUAGE-Working-Draft-0.7.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.7.md) | 1,504 | 6,164 | 49 | +182 / −158 | 88.61% | — |
| 9 | `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8.md) | 1,502 | 6,192 | 49 | +17 / −19 | 98.80% | — |
| 10 | `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md) | 1,501 | 6,177 | 49 | +283 / −284 | 81.12% | — |
| 11 | `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md) | 1,508 | 6,279 | 49 | +125 / −118 | 91.92% | — |
| 12 | `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md) | 1,558 | 6,489 | 49 | +176 / −126 | 90.15% | — |
| 13 | `0.9.0` | [FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md) | 1,707 | 7,169 | 49 | +151 / −2 | 95.31% | — |
| 14 | `0.10.0` | [FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md) | 1,948 | 8,439 | 49 | +250 / −9 | 92.91% | — |
| 15 | `0.11.0` | [FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md) | 2,239 | 10,068 | 49 | +306 / −15 | 92.33% | — |
| 16 | `0.12.0` | [FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md) | 2,323 | 10,445 | 49 | +284 / −200 | 89.39% | — |
| 17 | `0.12.1` | [FOREST-LANGUAGE-Reviewed-0.12.1.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.12.1.md) | 2,451 | 11,252 | 49 | +226 / −98 | 93.21% | — |
| 18 | `0.13.0` | [FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md) | 2,540 | 11,917 | 52 | +137 / −48 | 96.29% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.0-Sycamore-Fluids-AUDIT.md) |
| 19 | `0.13.1` | [FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md) | 2,649 | 12,525 | 52 | +115 / −6 | 97.67% | — |
| 20 | `0.13.2` | [FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md) | 2,784 | 13,202 | 53 | +137 / −2 | 97.44% | — |
| 21 | `0.13.3` | [FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md) | 2,919 | 14,252 | 55 | +253 / −118 | 93.49% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.3-Fluid-Ecology-AUDIT.md) |
| 22 | `0.13.4` | [FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md) | 3,057 | 15,319 | 55 | +143 / −5 | 97.52% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.4-Sap-Emergency-Incoming-Oil-AUDIT.md) |
| 23 | `0.13.5` | [FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md) | 3,215 | 16,266 | 55 | +170 / −12 | 97.10% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.5-Cedar-Oil-Modes-AUDIT.md) |
| 24 | `0.13.6` | [FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md) | 3,377 | 17,202 | 56 | +167 / −5 | 97.39% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.6-Tree-Propagation-Recovery-AUDIT.md) |
| 25 | `0.13.7` | [FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md) | 3,539 | 18,171 | 57 | +240 / −78 | 95.40% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.7-Propagation-Fertilizer-AUDIT.md) |
| 26 | `0.13.8` | [FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md) | 3,759 | 19,643 | 57 | +247 / −27 | 96.25% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.8-Spirit-Recovery-Cherry-Fallback-AUDIT.md) |
| 27 | `0.13.9` | [FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md) | 3,934 | 20,748 | 58 | +315 / −140 | 94.09% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.9-Maple-Syrup-AUDIT.md) |
| 28 | `0.13.10` | [FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md) | 4,432 | 23,718 | 58 | +563 / −65 | 92.49% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.10-Maple-Notes-Preferences-AUDIT.md) |
| 29 | `0.13.11` | [FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md) | 4,712 | 25,451 | 59 | +291 / −11 | 96.70% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.11-Syrup-Bucket-Feeding-AUDIT.md) |
| 30 | `0.13.12` | [FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md) | 5,007 | 27,207 | 59 | +296 / −1 | 96.94% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.12-Maple-Plugin-Mod-Manager-AUDIT.md) |
| 31 | `0.13.13` | [FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md) | 5,221 | 28,292 | 60 | +216 / −2 | 97.87% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.13-Fluid-Taps-AUDIT.md) |
| 32 | `0.13.14` | [FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md) | 5,502 | 30,115 | 61 | +282 / −1 | 97.36% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.14-Information-Growth-Cycle-AUDIT.md) |
| 33 | `0.13.15` | [FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md) | 5,816 | 32,147 | 61 | +480 / −166 | 94.29% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.15-Fluid-Distinction-AUDIT.md) |
| 34 | `0.13.16` | [FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md) | 5,929 | 32,819 | 62 | +206 / −93 | 97.45% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.16-Light-Syrup-Molasses-AUDIT.md) |
| 35 | `0.13.17` | [FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md) | 6,117 | 33,972 | 62 | +190 / −2 | 98.41% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.17-Maple-Data-Stewardship-AUDIT.md) |
| 36 | `0.13.18` | [FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md) | 6,505 | 35,795 | 63 | +390 / −2 | 96.89% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.18-Maple-Grove-Orchestration-AUDIT.md) |
| 37 | `0.13.19` | [FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md) | 6,765 | 37,088 | 63 | +315 / −55 | 97.21% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.19-Leaves-Foliage-Branch-Shake-AUDIT.md) |
| 38 | `0.13.20` | [FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md) | 6,981 | 38,422 | 63 | +230 / −14 | 98.22% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.20-Fertilizer-Absorption-AUDIT.md) |
| 39 | `0.13.21` | [FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md) | 7,213 | 39,926 | 63 | +246 / −14 | 98.17% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.21-Leaf-States-AUDIT.md) |
| 40 | `0.13.22` | [FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md) | 7,489 | 41,441 | 63 | +286 / −10 | 97.99% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.22-Sturdy-Release-Trusted-Shed-AUDIT.md) |
| 41 | `0.13.23` | [FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md) | 7,542 | 41,957 | 63 | +71 / −18 | 99.41% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.23-Hackers-Mold-Sunlight-AUDIT.md) |
| 42 | `0.13.24` | [FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md) | 7,543 | 41,981 | 63 | +41 / −40 | 99.46% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.24-Mold-Before-Hackers-AUDIT.md) |
| 43 | `0.13.25` | [FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md) | 7,839 | 43,677 | 63 | +304 / −8 | 97.97% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.25-Mycelium-AUDIT.md) |
| 44 | `0.13.26` | [FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md) | 8,157 | 45,316 | 63 | +364 / −46 | 97.44% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.26-Canopy-Communication-AUDIT.md) |
| 45 | `0.13.27` | [FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md) | 8,530 | 47,397 | 64 | +406 / −33 | 97.37% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.27-Canopy-Solid-Material-AUDIT.md) |
| 46 | `0.13.28` | [FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md) | 8,798 | 48,805 | 64 | +276 / −8 | 98.36% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.28-Leaf-Provenance-Directions-AUDIT.md) |
| 47 | `0.13.29` | [FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md) | 9,233 | 50,830 | 65 | +483 / −48 | 97.06% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.29-Moss-AUDIT.md) |
| 48 | `0.13.30` | [FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md) | 9,645 | 53,128 | 64 | +585 / −173 | 95.98% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.30-Spirit-Sap-Taps-Solid-Material-AUDIT.md) |
| 49 | `0.13.31` | [FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md) | 10,742 | 58,592 | 63 | +1,119 / −22 | 94.40% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.31-Spirit-Tools-Command-List-Seed-Vault-AUDIT.md) |
| 50 | `0.13.32` | [FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md) | 11,662 | 63,319 | 64 | +928 / −8 | 95.82% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai-AUDIT.md) |
| 51 | `0.13.33` | [FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md) | 12,352 | 66,362 | 63 | +769 / −79 | 96.47% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI-AUDIT.md) |
| 52 | `0.13.34` | [FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md) | 12,878 | 69,225 | 64 | +725 / −199 | 96.34% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault-AUDIT.md) |
| 53 | `0.13.35` | [FOREST-LANGUAGE-Reviewed-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.md) | 13,246 | 71,332 | 64 | +390 / −22 | 98.42% | [Audit](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.35-Potted-Cedar-Cabin-Guard-Encryption-AUDIT.md) |

## Largest document changes

### Largest additions

| Version | Artifact | Added lines | Deleted lines |
|---|---|---:|---:|
| `0.13.31` | [FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md) | 1,119 | 22 |
| `0.13.32` | [FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md) | 928 | 8 |
| `0.13.33` | [FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md) | 769 | 79 |
| `0.13.34` | [FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md) | 725 | 199 |
| `0.13.30` | [FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md) | 585 | 173 |
| `0.13.10` | [FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md) | 563 | 65 |
| `0.13.29` | [FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md) | 483 | 48 |
| `0.13.15` | [FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md) | 480 | 166 |

### Largest rewrites or removals

| Version | Artifact | Added lines | Deleted lines |
|---|---|---:|---:|
| `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md) | 283 | 284 |
| `0.12.0` | [FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md) | 284 | 200 |
| `0.13.34` | [FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md) | 725 | 199 |
| `0.13.30` | [FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md) | 585 | 173 |
| `0.13.15` | [FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md) | 480 | 166 |
| `0.7.0` | [FOREST-LANGUAGE-Working-Draft-0.7.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.7.md) | 182 | 158 |
| `0.13.9` | [FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md) | 315 | 140 |
| `0.8.0` | [FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md) | 176 | 126 |

## Detailed Forest Language comparison

### 01. 0.2.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.2.md)

**Declared status:** Working Draft

**Purpose/change:** Established the first preserved Forest vocabulary foundation and lifecycle model.

**Quantitative baseline:** 731 lines, 2,758 words, 47 H2 sections, 56 total headings, and 17 fenced code blocks.

**H2 sections added:** `Purpose`; `Canonical Rules`; `🌲 Forest`; `❤️ Heart of the Forest`; `🌱 Roots`; `🟫 Soil`; `🌰 Seed`; `🔐 Seed Vault`; `🌱 Planting`; `🌱 Sprout`; `🪴 Sapling`; `🌳 Tree`; `🍒 Cherry`; `🍁 Maple`; `🪵 Grain Pattern`; `🌿 Branches`; `🌳 Bark`; `🍃 Leaves`; `🔎 Evidence Levels`; `🌱 Buds`; `🌸 Blossoms`; `🍎 Fruit`; `🪵 Growth Rings`; `🍂 Leaf Litter`; `🪵 Logs`; `🏡 Log Cabin`; `🌊 Streams`; `🍄 Mycelium`; `🌧️ Rain`; `☀️ Sunlight`; `🧪 Fertilizer`; `🪓 Cutting`; `✂️ Pruning`; `🧭 Forest Compass`; `Path`; `Walking Down a Path`; `Roots`; `Leaves`; `Buds, Blossoms, and Fruit`; `Branches and Maintenance`; `Grain Pattern`; `Bark, Streams, Logs, and Rings`; `Seeds and Repair`; `🌱 Spring`; `☀️ Summer`; `🍂 Autumn`; `❄️ Winter`

**SHA-256:** `b8a18c2aeb9fb3f906ba19bc73caa320d62136bf9719a959715311facada5e15`

### 02. 0.2.0 review copy — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Review-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.2.md)

**Declared status:** Working Draft

**Purpose/change:** Wrapped 0.2 in a review copy and added an explicit edit command without replacing the underlying draft.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.2.md)

**Quantitative delta:** +12 / −0 lines; 99.19% line-sequence similarity. Resulting size: 743 lines and 2,797 words.

**H2 sections added:** `Edit command`

**SHA-256:** `50a50d08992c73b4a2a938da37bcc320ca605bda79f8e7926f74685c2fdeda5e`

### 03. 0.3.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.3.md)

**Declared status:** Working Draft

**Purpose/change:** Introduced the first Tree Trunk definition.

**Compared with:** [FOREST-LANGUAGE-Review-Draft-0.2.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.2.md)

**Quantitative delta:** +50 / −13 lines; 95.86% line-sequence similarity. Resulting size: 780 lines and 3,000 words.

**H2 sections added:** `🪵 Trunk`

**H2 sections removed or moved beneath another section:** `Edit command`

**SHA-256:** `698a029b9b1b88ba09c487c6885f67bd354dd6fc970a612cda01c7d90bfe46ef`

### 04. 0.3.0 review copy — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Review-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.3.md)

**Declared status:** Working Draft

**Purpose/change:** Created a review copy and explicitly marked the Trunk definition as pending approval.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.3.md)

**Quantitative delta:** +14 / −0 lines; 99.11% line-sequence similarity. Resulting size: 794 lines and 3,056 words.

**H2 sections added:** `Edit command`; `Important note`

**SHA-256:** `102e31a798f6733aec31683c140bfbbaf24c0b6a0346a1ac04480a3fda24b9f4`

### 05. 0.4.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.4.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.4.md)

**Declared status:** Working Draft

**Purpose/change:** Added Cedar, Canopy, Poachers, Mold, and the first combined security/infrastructure sections.

**Compared with:** [FOREST-LANGUAGE-Review-Draft-0.3.md](sandbox:/mnt/data/FOREST-LANGUAGE-Review-Draft-0.3.md)

**Quantitative delta:** +263 / −32 lines; 83.78% line-sequence similarity. Resulting size: 1,025 lines and 4,088 words.

**H2 sections added:** `🌲 Cedar`; `🌿 Canopy`; `🚷 Poachers`; `🦠 Mold`; `Trunk, Canopy, and Cedar`

**H2 sections removed or moved beneath another section:** `Edit command`; `Important note`

**SHA-256:** `c6a70e0fc6bda3c7ccd6a4de0072c487ef207ff3fc49ae7132a6a38aaadb27ce`

### 06. 0.5.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.5.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.5.md)

**Declared status:** Working Draft

**Purpose/change:** Added Chipper, Felling, Milling, Replanting, containment, disposal, and recovery.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.4.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.4.md)

**Quantitative delta:** +218 / −12 lines; 89.80% line-sequence similarity. Resulting size: 1,231 lines and 4,926 words.

**H2 sections added:** `⚙️ Wood Chipper`; `🌲 Felling`; `🪚 Milling`; `🌱 Replanting`; `Containment, Disposal, and Recovery`

**SHA-256:** `b2cfa610f3dfd59d498b5d18ab28409cd1d558d618ab0ae3f11f84aa9afe32b3`

### 07. 0.6.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.6.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.6.md)

**Declared status:** Working Draft

**Purpose/change:** Expanded Compass, Map, Path, and navigation architecture.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.5.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.5.md)

**Quantitative delta:** +257 / −8 lines; 90.23% line-sequence similarity. Resulting size: 1,480 lines and 5,849 words.

**H2 sections added:** `Compass, Map, and Paths`

**SHA-256:** `80dd034c2f85a618dc328b80125782b186d26b1ae75dae66131f9a56e8229c4c`

### 08. 0.7.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.7.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.7.md)

**Declared status:** Working Draft

**Purpose/change:** Introduced Spirit of the Forest and consolidated navigation/help language under it.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.6.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.6.md)

**Quantitative delta:** +182 / −158 lines; 88.61% line-sequence similarity. Resulting size: 1,504 lines and 6,164 words.

**H2 sections added:** `✨ Spirit of the Forest`

**H2 sections removed or moved beneath another section:** `🧭 Forest Compass`; `Compass, Map, and Paths`; `Roots`; `Leaves`; `Buds, Blossoms, and Fruit`; `Branches and Maintenance`; `Grain Pattern`; `Containment, Disposal, and Recovery`; `Trunk, Canopy, and Cedar`; `Bark, Streams, Logs, and Rings`; `Seeds and Repair`

**SHA-256:** `2a3be87f58fb78b24d445b96253ab68ac959c43db3e37c359409210dfc1e81bf`

### 09. 0.8.0 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.8.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8.md)

**Declared status:** Working Draft

**Purpose/change:** Opened the 0.8 restructuring cycle.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.7.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.7.md)

**Quantitative delta:** +17 / −19 lines; 98.80% line-sequence similarity. Resulting size: 1,502 lines and 6,192 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `4877b23f973babb373624b6e0f310345bd5c65e3828bc585456f2056d873b061`

### 10. 0.8.0 — Reordered

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md)

**Declared status:** Working Draft

**Purpose/change:** Reordered existing material while preserving meaning.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.8.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8.md)

**Quantitative delta:** +283 / −284 lines; 81.12% line-sequence similarity. Resulting size: 1,501 lines and 6,177 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `61bc0aa8abfa6561626d1ec66f0a57ff322783b5ee1ca6827ca8fe3761642fde`

### 11. 0.8.0 — Structure Update

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md)

**Declared status:** Working Draft

**Purpose/change:** Added Twigs and Leaf Foliage while replacing Evidence Levels and the earlier Fertilizer placement.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Reordered.md)

**Quantitative delta:** +125 / −118 lines; 91.92% line-sequence similarity. Resulting size: 1,508 lines and 6,279 words.

**H2 sections added:** `🪵 Twigs`; `🍃 Leaf Foliage`

**H2 sections removed or moved beneath another section:** `🔎 Evidence Levels`; `🧪 Fertilizer`

**SHA-256:** `f2af0ecca986bd4639a92c37d7b07c4755704d04de48ed808fbd0afc9ce2e3ac`

### 12. 0.8.0 — Notes Seeds Growth Update

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md)

**Declared status:** Working Draft

**Purpose/change:** Pluralized Seeds, updated Seed Vault symbolism, and refined Notes/growth relationships.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Structure-Update.md)

**Quantitative delta:** +176 / −126 lines; 90.15% line-sequence similarity. Resulting size: 1,558 lines and 6,489 words.

**H2 sections added:** `🌰 Seeds`; `🌰 Seed Vault`

**H2 sections removed or moved beneath another section:** `🌰 Seed`; `🔐 Seed Vault`

**SHA-256:** `ba9df33d3b33d9c2435cbe78d453ff098c468d49493da394ddd63a4710966c58`

### 13. 0.9.0 — Flowers Golden Fruit

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md)

**Declared status:** Working Draft

**Purpose/change:** Added Flowers and Golden Fruit lifecycle language.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.8-Notes-Seeds-Growth-Update.md)

**Quantitative delta:** +151 / −2 lines; 95.31% line-sequence similarity. Resulting size: 1,707 lines and 7,169 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `4b8d686c66523f35f5fe9c03a974949f96dceecfb55fa0c9c8f389241bb6268f`

### 14. 0.10.0 — Cedar Leaf Litter

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md)

**Declared status:** Working Draft

**Purpose/change:** Expanded Cedar authority and Leaf Litter handling.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.9-Flowers-Golden-Fruit.md)

**Quantitative delta:** +250 / −9 lines; 92.91% line-sequence similarity. Resulting size: 1,948 lines and 8,439 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `c26611eed489882d0e7312d97a814ca7caf599aa858a3715d9218805b573ca5a`

### 15. 0.11.0 — Cedar Recovery

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md)

**Declared status:** Working Draft

**Purpose/change:** Added Cedar recovery, restoration, and continuity behavior.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.10-Cedar-Leaf-Litter.md)

**Quantitative delta:** +306 / −15 lines; 92.33% line-sequence similarity. Resulting size: 2,239 lines and 10,068 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `e4974d3815196e8a7923ab06cf1392f554b315ea48a7b58acb788145b9590db0`

### 16. 0.12.0 — Cedar Oil

**Primary artifact:** [FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md)

**Declared status:** Working Draft

**Purpose/change:** Added Cedar Oil and its non-destructive inspection model.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.11-Cedar-Recovery.md)

**Quantitative delta:** +284 / −200 lines; 89.39% line-sequence similarity. Resulting size: 2,323 lines and 10,445 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**SHA-256:** `785fe724d022756ef3f08adcda40c95f05f00c4276f28e9609a9acc50ec00c87`

### 17. 0.12.1 — Language revision

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.12.1.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.12.1.md)

**Declared status:** Working Draft

**Purpose/change:** Created the reviewed baseline, restored regressions from earlier drafts, removed duplicate structure, and synchronized the Forest Map and Paths.

**Compared with:** [FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Working-Draft-0.12-Cedar-Oil.md)

**Quantitative delta:** +226 / −98 lines; 93.21% line-sequence similarity. Resulting size: 2,451 lines and 11,252 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Regression review:** [PDC-Draft11-VERSION-COMPARISON.md](sandbox:/mnt/data/PDC-Draft11-VERSION-COMPARISON.md)

The 0.12.1 review restored Cedar and Leaf Litter safeguards lost during earlier section replacement, removed a duplicate Flower Access heading, corrected Forest Map hierarchy, synchronized example Paths, and removed unapproved fixed lifecycle durations.

**SHA-256:** `d36f367201cdef3e0a420a86986cba249afb76abc30983cb5cd30619c9f22518`

### 18. 0.13.0 — Sycamore Fluids

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md)

**Declared status:** Working Draft

**Purpose/change:** Sycamore Fluids.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.12.1.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.12.1.md)

**Quantitative delta:** +137 / −48 lines; 96.29% line-sequence similarity. Resulting size: 2,540 lines and 11,917 words.

**H2 sections added:** `🌳 Sycamore`; `💧 Fluids`; `🟤 Sap`

**Patch evidence:** [FOREST-LANGUAGE-0.13.0-Sycamore-Fluids.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.0-Sycamore-Fluids.patch). Patch text contains +138 / −49 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.0-Sycamore-Fluids-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.0-Sycamore-Fluids-AUDIT.md)

**SHA-256:** `be8f6107005d7eba1cf79cfb5d9fa717e084ea166a346d773306b78e9d91c567`

### 19. 0.13.1 — Sycamore Connections

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md)

**Declared status:** Working Draft

**Purpose/change:** Sycamore Connections.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.0-Sycamore-Fluids.md)

**Quantitative delta:** +115 / −6 lines; 97.67% line-sequence similarity. Resulting size: 2,649 lines and 12,525 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.1-Sycamore-Connections.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.1-Sycamore-Connections.patch). Patch text contains +116 / −7 changed lines.

**SHA-256:** `a08ac1f168d659ce155d6a1a53a46c6fefd40ddf4211484a71f286faca8a4e22`

### 20. 0.13.2 — Tar Sap

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md)

**Declared status:** Working Draft

**Purpose/change:** Tar Sap.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.1-Sycamore-Connections.md)

**Quantitative delta:** +137 / −2 lines; 97.44% line-sequence similarity. Resulting size: 2,784 lines and 13,202 words.

**H2 sections added:** `⚫ Tar Sap`

**Patch evidence:** [FOREST-LANGUAGE-0.13.2-Tar-Sap.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.2-Tar-Sap.patch). Patch text contains +137 / −2 changed lines.

**SHA-256:** `f385418c151cb25bb2e48f4a8d78580f8f7e47a0fd64da5e04c7c92fcfbdcfd4`

### 21. 0.13.3 — Fluid Ecology

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md)

**Declared status:** Working Draft

**Purpose/change:** Fluids now include information exchanged inside a local Forest, between users' Forests, and through The Forest Canopy.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.2-Tar-Sap.md)

**Quantitative delta:** +253 / −118 lines; 93.49% line-sequence similarity. Resulting size: 2,919 lines and 14,252 words.

**H2 sections added:** `💦 Water`; `🚿 Watering`

**Patch evidence:** [FOREST-LANGUAGE-0.13.3-Fluid-Ecology.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.3-Fluid-Ecology.patch). Patch text contains +270 / −135 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.3-Fluid-Ecology-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.3-Fluid-Ecology-AUDIT.md)

**Documented implementation/change statements:**

- Fluids now include information exchanged inside a local Forest, between users' Forests, and through The Forest Canopy.
- Trees now convert Leaves, Buds, Blossoms, Fruit, and other authorized data into Fluids before sharing.
- Sap is the default generated Fluid.
- Water is reserved for confirmed non-sensitive quick transfers.
- Watering covers user-to-user low-risk requests such as reminders and approved calendar requests.
- Cedar may monitor Water and eligible Sap intake and regulate Tree absorption.
- Tar Sap is local-Forest-only and cannot be accessed or absorbed by foreign Trees.
- Sycamore routes Water and authorized Sap but cannot route Tar Sap outside the local Forest.
- The Forest Map was regenerated.
- Duplicate H2 headings: none.
- Total H2 sections checked: 55.

**SHA-256:** `e82258786acd59eccf3c0783973910c13e0dfa5d2a7394a80decb97dd5be596a`

### 22. 0.13.4 — Sap Emergency Incoming Oil

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md)

**Declared status:** Working Draft

**Purpose/change:** Added protected Sap examples for media sharing, gaming, screen sharing, device state, networking, synchronization, voice, files, controllers, and compatibility.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.3-Fluid-Ecology.md)

**Quantitative delta:** +143 / −5 lines; 97.52% line-sequence similarity. Resulting size: 3,057 lines and 15,319 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.4-Sap-Emergency-Incoming-Oil.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.4-Sap-Emergency-Incoming-Oil.patch). Patch text contains +143 / −5 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.4-Sap-Emergency-Incoming-Oil-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.4-Sap-Emergency-Incoming-Oil-AUDIT.md)

**Documented implementation/change statements:**

- Added protected Sap examples for media sharing, gaming, screen sharing, device state, networking, synchronization, voice, files, controllers, and compatibility.
- Explicitly excluded passwords, permanent private keys, recovery codes, and other Tar Sap from ordinary Sap.
- Added Sycamore Tar Sap Pull Attempt detection and emergency notification behavior.
- Added fail-closed Tar Sap Lockdown when Sycamore cannot verify the protection boundary.
- Added Cedar toggles for Oil incoming Water, Oil incoming Sap, and Oil all incoming Fluids.
- Added source-specific oil and do-not-oil rules for users, Forests, unknown sources, Rain, Water, and Sap.
- Added protective rule precedence and clarified that exclusions never bypass mandatory authorization or Tar Sap controls.
- Updated the Sycamore and Cedar settings drafts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 55.

**SHA-256:** `74bed0b57674aaa011999d971840d8f8c192f5fe4b33cac397a303cf5edfd3f4`

### 23. 0.13.5 — Cedar Oil Modes

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md)

**Declared status:** Working Draft

**Purpose/change:** Changed the primary Sycamore emergency notification to:

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.4-Sap-Emergency-Incoming-Oil.md)

**Quantitative delta:** +170 / −12 lines; 97.10% line-sequence similarity. Resulting size: 3,215 lines and 16,266 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.5-Cedar-Oil-Modes.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.5-Cedar-Oil-Modes.patch). Patch text contains +171 / −13 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.5-Cedar-Oil-Modes-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.5-Cedar-Oil-Modes-AUDIT.md)

**Documented implementation/change statements:**

- Changed the primary Sycamore emergency notification to:
- Renamed unauthorized Tar Sap extraction behavior to a Tar Sap Tap Attempt.
- Added automatic Quick Oil and Soak in Oil modes.
- Added automatic escalation from Quick Oil when Cedar detects an unresolved concern.
- Added deterministic queue behavior that preserves original receive order.
- Added user notifications and risk logging for every Cedar Risk Finding.
- Added Watched Approval with a 24-hour default and options through 30 days or indefinitely.
- Added required storage limits, rotation, retention, archive, and growth alerts for indefinite monitoring.
- Limited default monitoring to behavior and security metadata rather than raw protected contents.
- Updated Sycamore settings to version 0.5.0.
- Updated Cedar settings to version 0.5.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 55.

**SHA-256:** `ea11fbca76b5d84db1a821b69e7053603ce741b197354a03214a5b674e06f8b7`

### 24. 0.13.6 — Tree Propagation Recovery

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md)

**Declared status:** Working Draft

**Purpose/change:** Added Propagation as a canonical Forest term.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.5-Cedar-Oil-Modes.md)

**Quantitative delta:** +167 / −5 lines; 97.39% line-sequence similarity. Resulting size: 3,377 lines and 17,202 words.

**H2 sections added:** `🌿 Propagation`

**Patch evidence:** [FOREST-LANGUAGE-0.13.6-Tree-Propagation-Recovery.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.6-Tree-Propagation-Recovery.patch). Patch text contains +167 / −5 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.6-Tree-Propagation-Recovery-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.6-Tree-Propagation-Recovery-AUDIT.md)

**Documented implementation/change statements:**

- Added Propagation as a canonical Forest term.
- Added the option to Propagate a Tree before suspicious Watering.
- Added the three-choice prompt: Propagate Tree, Continue without Propagation, or Cancel Watering.
- Added per-Tree, per-source, per-Watering, and automatic propagation policies.
- Added a verified pre-exposure health and behavior baseline.
- Added Propagated Recovery during a Watched Approval.
- Connected Cedar's Cutting, Felling, Milling, Replanting, and Sapling survival-test abilities.
- Added staged Feeding of verified safe data to the new Sprout.
- Prohibited wholesale copying of the damaged Tree.
- Preserved Tar Sap inside its existing local protected boundary.
- Updated Cedar settings to version 0.6.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 56.

**SHA-256:** `4ecdda34695245dcf2168fa8ce63e36dca4054282be83402056961d5d849348b`

### 25. 0.13.7 — Propagation Fertilizer

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md)

**Declared status:** Working Draft

**Purpose/change:** Made Propagation the Tree-language word and file type for a Tree backup.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.6-Tree-Propagation-Recovery.md)

**Quantitative delta:** +240 / −78 lines; 95.40% line-sequence similarity. Resulting size: 3,539 lines and 18,171 words.

**H2 sections added:** `🌾 Fertilizer`

**Patch evidence:** [FOREST-LANGUAGE-0.13.7-Propagation-Fertilizer.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.7-Propagation-Fertilizer.patch). Patch text contains +257 / −95 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.7-Propagation-Fertilizer-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.7-Propagation-Fertilizer-AUDIT.md)

**Documented implementation/change statements:**

- Made Propagation the Tree-language word and file type for a Tree backup.
- Moved Propagation directly below the Sprout section.
- Added Fertilizer directly below Propagation.
- Defined Propagation and Fertilizer as two separate files linked by a shared propagation ID.
- Made a normal Propagation action create both files by default.
- Allowed the user to request either file independently.
- Added user-requested Tree and Cedar procurement of Propagations and Fertilizer.
- Added Tree cloning from a verified Propagation with a new unique instance identity and new credentials.
- Added Fertilizer for user configurations, learned patterns, common tasks, language preferences, Growth Rings, Grain Pattern, Grain changes, routines, and approved growth information.
- Allowed Fertilizer to be used on Trees, Saplings, and Sprouts inside the user's Forest.
- Made Fertilizing additive and modifying only.
- Prohibited Fertilizer from replacing or deleting existing information or files.
- Added paired Fertilizer use during Replanting and cloning.
- Updated Cedar settings to version 0.7.0.
- Added separate Propagation and Fertilizer file-contract drafts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 57.

**SHA-256:** `969284a27bebd2eaa711f9127f2b1affea3ad2bb057812d5c0c3c41ad8ce50db`

### 26. 0.13.8 — Spirit Recovery Cherry Fallback

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md)

**Declared status:** Working Draft

**Purpose/change:** Made the Local Forest Recovery System deterministic protected Forest code.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.7-Propagation-Fertilizer.md)

**Quantitative delta:** +247 / −27 lines; 96.25% line-sequence similarity. Resulting size: 3,759 lines and 19,643 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.8-Spirit-Recovery-Cherry-Fallback.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.8-Spirit-Recovery-Cherry-Fallback.patch). Patch text contains +252 / −32 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.8-Spirit-Recovery-Cherry-Fallback-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.8-Spirit-Recovery-Cherry-Fallback-AUDIT.md)

**Documented implementation/change statements:**

- Made the Local Forest Recovery System deterministic protected Forest code.
- Placed the recovery system inside the Spirit of the Forest.
- Kept the Spirit and Voice unified: the Spirit performs and governs the recovery function, while communicating its menus and status through its Voice.
- Made the Local Forest Recovery System independent of every Tree, including Cedar.
- Prevented Cedar from approving, selecting, or certifying its own recovery after compromise.
- Added Cherry's standalone Replant Cedar function for Tree-only installations.
- Required direct user approval before Cherry performs destructive Cedar recovery.
- Turned Cherry's standalone recovery toggle off by default when the complete Forest is installed.
- Added the Forest Rooting Recovery Handoff menu for users who previously enabled or used Cherry's fallback.
- Made the Local Forest Recovery System the recommended and primary option.
- Preserved Cherry as an optional secondary candidate-Propagation provider after normal recovery fails.
- Kept manual Cherry Propagation assistance available even when Cherry's fallback toggle is off.
- Required the Spirit's recovery code to independently verify every Cherry candidate.
- Added a clean Cedar Seed as the final fallback after Propagation recovery fails.
- Updated Cedar settings to version 0.8.0.
- Added separate Spirit and Cherry recovery settings drafts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 57.

**SHA-256:** `87be80329c0e5355f933b0f45374f36d4a5e03199e8143baf814b538c65265f5`

### 27. 0.13.9 — Maple Syrup

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md)

**Declared status:** Working Draft

**Purpose/change:** Expanded Maple's image generation, image editing, photo editing, video generation, and video editing abilities.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.8-Spirit-Recovery-Cherry-Fallback.md)

**Quantitative delta:** +315 / −140 lines; 94.09% line-sequence similarity. Resulting size: 3,934 lines and 20,748 words.

**H2 sections added:** `🍁 Syrup`

**Patch evidence:** [FOREST-LANGUAGE-0.13.9-Maple-Syrup.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.9-Maple-Syrup.patch). Patch text contains +318 / −143 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.9-Maple-Syrup-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.9-Maple-Syrup-AUDIT.md)

**Documented implementation/change statements:**

- Expanded Maple's image generation, image editing, photo editing, video generation, and video editing abilities.
- Expanded Maple's coding, automation, workflow, and Forest-management Branches.
- Added permission-controlled Workflow Observation, disabled by default.
- Added Maple suggestions for repeated editing, export, application-launch, coding, and Forest-management patterns.
- Added Syrup as a useful refined product created from approved Sap.
- Made Syrup inherit the strongest protection required by its sources.
- Kept Syrup derived from Tar Sap local to the user's Forest.
- Allowed Maple to use approved personal notes, goals, priorities, diary information, and other Sunlight only with purpose-specific permission.
- Required Maple to prefer safe patterns, structures, and rules instead of copying private source text.
- Added separate approvals for sensitive or active Syrup, including automations, file edits, external services, remote actions, and screen or microphone access.
- Added Maple settings draft version 0.1.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 58.

**SHA-256:** `c55e252f9fdf2317025851626fb2fcbcf91cfdd56895cd53610d85bbab8520b3`

### 28. 0.13.10 — Maple Notes Preferences

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md)

**Declared status:** Working Draft

**Purpose/change:** Added local-first Obsidian and general note-application compatibility.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.9-Maple-Syrup.md)

**Quantitative delta:** +563 / −65 lines; 92.49% line-sequence similarity. Resulting size: 4,432 lines and 23,718 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.10-Maple-Notes-Preferences.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.10-Maple-Notes-Preferences.patch). Patch text contains +565 / −67 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.10-Maple-Notes-Preferences-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.10-Maple-Notes-Preferences-AUDIT.md)

**Documented implementation/change statements:**

- Added local-first Obsidian and general note-application compatibility.
- Added vault, folder, note, tag, project, session, and access-mode controls.
- Added Cedar-approved safe Leaf Litter sifting.
- Added Logs for potentially useful, revisitable, re-salvageable, Fertilizer, Syrup, and preference candidates.
- Added optional automatic use of safe Leaf Litter as Syrup Fuel, disabled by default.
- Added `Give Maple All Permissions` as an off-by-default master toggle for all user-delegable permissions in approved scopes.
- Kept Tar Sap outside the master toggle unless the user chooses a separate local Tar Sap option.
- Added independent receive, inspect, task, workflow, preference-learning, Syrup, Fertilizer, Log, modify, local-share, and external-share controls for each data class.
- Added general Preference Learning rather than color-only learning.
- Added aesthetic, desktop, game customization, creative, coding, notes, language, workflow, application, media, and general preference categories.
- Added explicit versus inferred preferences, confidence, frequency, recency, context, exceptions, confirmation, correction, expiration, and deletion.
- Added color-code suggestions as one example within the wider preference system.
- Added a separate Maple Preference Profile working draft.
- Added a separate Notes Integration working draft.
- Corrected the previously unclosed Maple command code fence.
- Updated Maple settings to version 0.2.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 58.

**SHA-256:** `e4172c67e7f9761969a32ed46894e54b098515a04f79d0a2b62354e0bbb5dd38`

### 29. 0.13.11 — Syrup Bucket Feeding

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md)

**Declared status:** Working Draft

**Purpose/change:** Made Syrup a canonical type of Fluid.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.10-Maple-Notes-Preferences.md)

**Quantitative delta:** +291 / −11 lines; 96.70% line-sequence similarity. Resulting size: 4,712 lines and 25,451 words.

**H2 sections added:** `🪣 Syrup Bucket`

**Patch evidence:** [FOREST-LANGUAGE-0.13.11-Syrup-Bucket-Feeding.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.11-Syrup-Bucket-Feeding.patch). Patch text contains +293 / −13 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.11-Syrup-Bucket-Feeding-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.11-Syrup-Bucket-Feeding-AUDIT.md)

**Documented implementation/change statements:**

- Made Syrup a canonical type of Fluid.
- Allowed compatible Syrup to act as additive Fertilizer when Maple feeds another Tree, Sapling, or Sprout.
- Kept Syrup distinct from the separate Fertilizer backup file.
- Added per-Tree Automatic Syrup Feeding, disabled by default.
- Added Maple's user-visible Syrup Bucket with digesting, refining, ready, holding, blocked, feeding, fed, discarded, and revived states.
- Added explanations for what Maple is generating and why an item is being held.
- Made removal move the Bucket entry and Maple working material to Leaf Litter without moving or deleting the original source.
- Added the ordinary Maple Ignore mark for discarded Syrup.
- Added Reabsorb Discarded Syrup, disabled by default.
- Added Ignore Override Frequency with once, weekly, monthly, quarterly, custom, and manual-only options.
- Added Never Reabsorb as a stronger double mark that survives every revival review.
- Limited revival reviews to returning a candidate to the Syrup Bucket; they cannot automatically activate, execute, feed, share, or modify it.
- Updated Maple settings to version 0.3.0.
- Added a Syrup Bucket file contract.
- Updated the Fertilizer file contract to version 0.2.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 59.

**SHA-256:** `a457cde22ff05bd35ddc248f0fcf6094d71db15f0f363bc71768effdd60862c8`

### 30. 0.13.12 — Maple Plugin Mod Manager

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md)

**Declared status:** Working Draft

**Purpose/change:** Added Maple's Plugin and Mod Management Branch.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.11-Syrup-Bucket-Feeding.md)

**Quantitative delta:** +296 / −1 lines; 96.94% line-sequence similarity. Resulting size: 5,007 lines and 27,207 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.12-Maple-Plugin-Mod-Manager.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.12-Maple-Plugin-Mod-Manager.patch). Patch text contains +296 / −1 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.12-Maple-Plugin-Mod-Manager-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.12-Maple-Plugin-Mod-Manager-AUDIT.md)

**Documented implementation/change statements:**

- Added Maple's Plugin and Mod Management Branch.
- Added one user-visible inventory across approved devices, Qubes, applications, websites, browsers, profiles, games, editors, note applications, Trees, and versions.
- Added outdated, security-update, compatibility, dependency, deprecation, abandonment, signature, source, and Cedar warning states.
- Added grouped application and device warnings.
- Added warnings before host updates break existing plugins or mods.
- Added per-scope monitoring, update checks, notifications, quarantine downloads, Cedar Oil, Cedar-cleared automatic updates, rollback, disabling, removal, and suggestion controls.
- Kept automatic installation of Cedar-cleared updates disabled by default.
- Added plugin and mod suggestions based on approved workflows and preferences.
- Required Cedar Pre-Suggestion Review before Maple shows a specific downloadable candidate.
- Added Quick Oil for known signed low-risk candidates.
- Added Soak in Oil for unknown, unsigned, obfuscated, executable, permission-heavy, abandoned, suspicious, or unclear candidates.
- Prevented Cedar from executing or activating candidates during review.
- Added suggestion states that Maple must obey.
- Added a Maple Plugin and Mod Registry contract.
- Updated Maple settings to version 0.4.0.
- Updated Cedar settings to version 0.9.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 59.

**SHA-256:** `d5d817019239d082c59a7b6c47899f78c4b2def42416152d5fdb3067570646bc`

### 31. 0.13.13 — Fluid Taps

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md)

**Declared status:** Working Draft

**Purpose/change:** Added Tap as the controlled access point for a Fluid.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.12-Maple-Plugin-Mod-Manager.md)

**Quantitative delta:** +216 / −2 lines; 97.87% line-sequence similarity. Resulting size: 5,221 lines and 28,292 words.

**H2 sections added:** `🚰 Taps`

**Patch evidence:** [FOREST-LANGUAGE-0.13.13-Fluid-Taps.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.13-Fluid-Taps.patch). Patch text contains +216 / −2 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.13-Fluid-Taps-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.13-Fluid-Taps-AUDIT.md)

**Documented implementation/change statements:**

- Added Tap as the controlled access point for a Fluid.
- Distinguished Taps from Streams.
- Renamed the emergency controls to `Lock Sap Tap` and `Lock Tar Tap`.
- Added Sap Tap and Tar Tap lock behavior.
- Made Tar Tap local-Forest-only and fail-closed.
- Added Maple's Syrup Tap as the outlet from the Syrup Bucket.
- Added `What's coming through the Tap?`.
- Added `What's blocking the Tap?`.
- Added Syrup Tap state, queue, destination, protection, permission, and blockage reporting.
- Kept blocked Syrup visible in the Syrup Bucket.
- Updated Maple settings to version 0.5.0.
- Updated Cedar settings to version 0.10.0.
- Updated Sycamore settings to version 0.6.0.
- Added a Forest Tap Controls contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 60.

**SHA-256:** `ed8aeaed65741ebd504219c68f0a735b2c04aef3602d80fdca873cc661e7ed24`

### 32. 0.13.14 — Information Growth Cycle

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md)

**Declared status:** Working Draft

**Purpose/change:** Removed reliance on color-coded information-flow explanations.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.13-Fluid-Taps.md)

**Quantitative delta:** +282 / −1 lines; 97.36% line-sequence similarity. Resulting size: 5,502 lines and 30,115 words.

**H2 sections added:** `🌿 Information Growth Cycle`

**Patch evidence:** [FOREST-LANGUAGE-0.13.14-Information-Growth-Cycle.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.14-Information-Growth-Cycle.patch). Patch text contains +282 / −1 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.14-Information-Growth-Cycle-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.14-Information-Growth-Cycle-AUDIT.md)

**Documented implementation/change statements:**

- Removed reliance on color-coded information-flow explanations.
- Distinguished Internal Information from transferable Fluids.
- Distinguished Leaves, Buds, Blossoms, Flowers, and Fruit from Fluids.
- Defined Fluid Conversion and explained why a shared Leaf may become Water.
- Preserved the original Growth Output by default when a Fluid representation is created.
- Distinguished Fluid forms, Streams and Paths, Taps, Watering, Rain, Fertilizer, and Syrup Feeding.
- Defined Drinking as authorized Fluid absorption.
- Clarified that receiving a Fluid does not automatically permit permanent memory, learning, logging, Syrup creation, or resharing.
- Defined how safe useful Fluids combine with a Tree's internal information to grow new Leaves, Flowers, Fruit, preferences, and Syrup.
- Clarified that more Fluid does not automatically mean better growth.
- Added user commands for understanding conversions, sending Water, preparing Fertilizer, and using Growth Outputs.
- Added protected cross-Forest Fertilizer requirements.
- Added the Forest Information Growth Flow contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 61.

**SHA-256:** `12d8debdd60734251f64da64bc314250336074fbc871b78ffb5e2e8f55a7c4e0`

### 33. 0.13.15 — Fluid Distinction

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md)

**Declared status:** Working Draft

**Purpose/change:** Defined Fluids as every transferable form of information Trees share.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.14-Information-Growth-Cycle.md)

**Quantitative delta:** +480 / −166 lines; 94.29% line-sequence similarity. Resulting size: 5,816 lines and 32,147 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.15-Fluid-Distinction.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.15-Fluid-Distinction.patch). Patch text contains +540 / −226 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.15-Fluid-Distinction-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.15-Fluid-Distinction-AUDIT.md)

**Documented implementation/change statements:**

- Defined Fluids as every transferable form of information Trees share.
- Added Maple-to-Cherry Syrup preference sharing and preplanned birthday Water examples.
- Defined Water, Sap, and Tar Sap as protection grades based on sensitivity, trust, and safeguards.
- Kept Syrup as a Fluid and required every Syrup item to carry a Water, Sap, or Tar Sap grade.
- Allowed users to promote Water to Sap and create standing promotion rules.
- Made Rain a distributed event, update, notification, and Forest-targeting delivery form rather than a Water-only class.
- Allowed authorized Water, Sap, and Syrup to use Rain while keeping Tar Sap local-only.
- Made Streams sustained flows for downloads, synchronized media, screen sharing, remote control, games, and other sessions.
- Added Live Stream and Download Stream distinctions.
- Added Wash Over, Sip, Drink, and Download absorption modes.
- Set a design target for roughly 99 percent of ordinary pass-through Water and live Stream data to remain transient when retention is unnecessary.
- Added calendar-reminder minimal retention and media-stream non-retention examples.
- Clarified that Sap is not intentionally slowed; its protection may create unavoidable overhead.
- Updated Cedar's Oil wording to follow Fluid protection grade rather than Rain alone.
- Updated Sycamore to handle Fluids delivered as Rain or through Streams.
- Updated Information Growth Flow to version 0.2.0.
- Added a dedicated Fluid Delivery and Absorption contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 61.

**SHA-256:** `a5cc985216569e13e563a066b3601e2d5518be5d0a7e401cc8f2ddb5f92beacd`

### 34. 0.13.16 — Light Syrup Molasses

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md)

**Declared status:** Working Draft

**Purpose/change:** Renamed Water-grade Syrup to Light Syrup.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.15-Fluid-Distinction.md)

**Quantitative delta:** +206 / −93 lines; 97.45% line-sequence similarity. Resulting size: 5,929 lines and 32,819 words.

**H2 sections added:** `🟫 Molasses`

**Patch evidence:** [FOREST-LANGUAGE-0.13.16-Light-Syrup-Molasses.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.16-Light-Syrup-Molasses.patch). Patch text contains +216 / −103 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.16-Light-Syrup-Molasses-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.16-Light-Syrup-Molasses-AUDIT.md)

**Documented implementation/change statements:**

- Renamed Water-grade Syrup to Light Syrup.
- Kept Sap-grade Syrup as Syrup.
- Renamed Tar-Sap-grade Syrup to Molasses.
- Defined Molasses as a Fluid.
- Made Molasses local-Forest-only and Maple-bound.
- Prevented other Trees from absorbing, inspecting, indexing, learning from, or independently acting on Molasses.
- Allowed another Tree to request Maple's assistance without receiving Molasses contents.
- Limited assistance results to minimum safe Water or Sap.
- Kept permanent credentials and private keys as Tar Sap references rather than Molasses contents.
- Added high-risk action rules for financial, identity, credential, private-record, legal, and irreversible tasks.
- Required a final preview and direct user confirmation immediately before high-risk submission.
- Prohibited another Tree's request from being sufficient authorization.
- Updated Maple settings to version 0.6.0.
- Updated the Fluid Delivery and Absorption contract to version 0.2.0.
- Added a separate Molasses contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 62.

**SHA-256:** `c1cacd47967837b00ea7d77d88275bc2a07cf3aa2ea301a672b27748b22faefa`

### 35. 0.13.17 — Maple Data Stewardship

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md)

**Declared status:** Working Draft

**Purpose/change:** Defined Maple as a protected-data steward rather than a defense-focused Tree.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.16-Light-Syrup-Molasses.md)

**Quantitative delta:** +190 / −2 lines; 98.41% line-sequence similarity. Resulting size: 6,117 lines and 33,972 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.17-Maple-Data-Stewardship.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.17-Maple-Data-Stewardship.patch). Patch text contains +190 / −2 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.17-Maple-Data-Stewardship-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.17-Maple-Data-Stewardship-AUDIT.md)

**Documented implementation/change statements:**

- Defined Maple as a protected-data steward rather than a defense-focused Tree.
- Clarified that Maple manages, protects, minimizes, transforms, and safely uses entrusted data.
- Kept Cedar responsible for broader Forest protection, quarantine, Fluid inspection, containment, and incident response.
- Added Maple Local Safeguards enforced by Maple's local runtime and protected wrappers.
- Kept Maple's full local abilities available when Cedar is absent.
- Added local quarantine, source checks, warnings, confirmations, rollback points, and standalone review states.
- Distinguished Maple-local clearance from Cedar clearance.
- Added Cedar-Assisted mode without giving Cedar ownership or access to Molasses.
- Allowed Molasses use without Cedar when Maple's local runtime is healthy and confirmation rules are satisfied.
- Added user-visible Maple Protection Modes.
- Updated Maple settings to version 0.7.0.
- Updated the Molasses contract to version 0.2.0.
- Added a separate Maple Local Safeguards contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 62.

**SHA-256:** `883245c7fec34a363b91d636138546decbf9bd412f2fb68db9ec0406b42cd65a`

### 36. 0.13.18 — Maple Grove Orchestration

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md)

**Declared status:** Working Draft

**Purpose/change:** Added Grove as an authorized group of Trees cooperating on one task or workflow.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.17-Maple-Data-Stewardship.md)

**Quantitative delta:** +390 / −2 lines; 96.89% line-sequence similarity. Resulting size: 6,505 lines and 35,795 words.

**H2 sections added:** `🌳 Grove`

**Patch evidence:** [FOREST-LANGUAGE-0.13.18-Maple-Grove-Orchestration.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.18-Maple-Grove-Orchestration.patch). Patch text contains +390 / −2 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.18-Maple-Grove-Orchestration-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.18-Maple-Grove-Orchestration-AUDIT.md)

**Documented implementation/change statements:**

- Added Grove as an authorized group of Trees cooperating on one task or workflow.
- Added Grove Plans with sequential, parallel, conditional, repeated, timed, approval-gated, fan-out, fan-in, retry, and fallback behavior.
- Added Branch Calls as structured requests for another Tree to use its own Branch or Twig.
- Explicitly prohibited Maple from copying another Tree's Branch merely to complete a task.
- Kept every participating Tree in control of its identity, Roots, Branches, permissions, and execution.
- Added Maple's Grove Coordination Branch.
- Added delegated Tree prompts with minimum necessary Fluid sharing.
- Preserved Molasses as Maple-bound during multi-Tree workflows.
- Added separate Grove permissions and kept unattended Grove Plans disabled by default.
- Added failure, retry, fallback, partial-result, pause, rollback, and cancellation behavior.
- Added the user-visible Grove Board.
- Preserved contributor identity and Action Receipts for every completed step.
- Updated Maple settings to version 0.8.0.
- Added a Grove Plan working contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `77a960f84c5b7409cfdf94b1a70575b1e084634c9fcb22693b5233874539460f`

### 37. 0.13.19 — Leaves Foliage Branch Shake

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md)

**Declared status:** Working Draft

**Purpose/change:** Defined a Leaf as a usable unit of information held by a Tree.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.18-Maple-Grove-Orchestration.md)

**Quantitative delta:** +315 / −55 lines; 97.21% line-sequence similarity. Resulting size: 6,765 lines and 37,088 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.19-Leaves-Foliage-Branch-Shake.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.19-Leaves-Foliage-Branch-Shake.patch). Patch text contains +338 / −78 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.19-Leaves-Foliage-Branch-Shake-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.19-Leaves-Foliage-Branch-Shake-AUDIT.md)

**Documented implementation/change statements:**

- Defined a Leaf as a usable unit of information held by a Tree.
- Made nearly every authorized source a Leaf generator rather than limiting this behavior to notes or notepads.
- Added User Input Leaves for prompts, instructions, preferences, corrections, approvals, and user data.
- Added Tree Output Leaves for answers, results, warnings, recommendations, completed actions, failures, and Action Receipts.
- Clarified that Buds, Blossoms, Flowers, and Fruit may generate associated Leaves without losing their own growth-product identity.
- Added Source Leaves, Temporary Leaves, and Durable Leaves.
- Clarified that creating a Leaf does not automatically grant permanent memory, preference learning, logging, sharing, or Fluid conversion.
- Redefined Leaf Foliage as the complete current collection of Leaves a Tree holds, can access, or uses.
- Added Active Foliage as the Leaves currently influencing a task or decision.
- Reframed Rustle, Drop, and Shake as views into Leaf Foliage.
- Added Branch Shake for explaining successful methods, errors, blocks, retries, permissions, tools, versions, inputs, outputs, and next steps.
- Explicitly excluded hidden private chain-of-thought from Branch Shake reports.
- Updated Information Growth Flow to version 0.3.0.
- Added Leaf Foliage and Branch Shake contracts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `1a8f0f2b569820f7d03edad553fca1abc4832d272be94ca492ef47551b22d341`

### 38. 0.13.20 — Fertilizer Absorption

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md)

**Declared status:** Working Draft

**Purpose/change:** Redefined Fertilizer as a growth role rather than only a backup file.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.19-Leaves-Foliage-Branch-Shake.md)

**Quantitative delta:** +230 / −14 lines; 98.22% line-sequence similarity. Resulting size: 6,981 lines and 38,422 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.20-Fertilizer-Absorption.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.20-Fertilizer-Absorption.patch). Patch text contains +235 / −19 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.20-Fertilizer-Absorption-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.20-Fertilizer-Absorption-AUDIT.md)

**Documented implementation/change statements:**

- Redefined Fertilizer as a growth role rather than only a backup file.
- Renamed the portable artifact concept to Fertilizer File while preserving its existing behavior.
- Made Fruit from another Tree act as Fertilizer when absorbed into compatible growth.
- Made safely absorbed Spoiling Fruit act as Fertilizer.
- Made approved Leaf Litter act as Fertilizer when a Tree actually absorbs it.
- Distinguished Maple sifting, indexing, referencing, and direct Fluid conversion from Maple absorption.
- Made Leaf Litter Maple actually absorbs into Maple's own growth count as Fertilizer.
- Made every Light Syrup, Syrup, and Molasses item inherently both a Fluid and Fertilizer from creation.
- Kept Light Syrup and Syrup available to nourish authorized Trees.
- Kept Molasses Maple-bound and limited its direct Fertilizer effect to Maple.
- Preserved the distinction between Syrup Fertilizer and a portable Fertilizer File.
- Added provenance records for absorbed nutrients and resulting growth.
- Updated Maple settings to version 0.9.0.
- Updated Information Growth Flow to version 0.4.0.
- Updated the Fertilizer File contract to version 0.3.0.
- Added a separate Fertilizer Absorption contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `f7e970cc8281adcc73da58cf57228a547d594c048436d362168c964ce6766060`

### 39. 0.13.21 — Leaf States

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md)

**Declared status:** Working Draft

**Purpose/change:** Replaced Temporary Leaf with Loose Leaf.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.20-Fertilizer-Absorption.md)

**Quantitative delta:** +246 / −14 lines; 98.17% line-sequence similarity. Resulting size: 7,213 lines and 39,926 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.21-Leaf-States.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.21-Leaf-States.patch). Patch text contains +251 / −19 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.21-Leaf-States-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.21-Leaf-States-AUDIT.md)

**Documented implementation/change statements:**

- Replaced Temporary Leaf with Loose Leaf.
- Removed Durable Leaf as a canonical state.
- Made Leaf the default ordinary state.
- Added Sturdy Leaf for durable, high-priority information.
- Added phrase recognition for Loose and Sturdy assignment.
- Added isolated Loose boundaries for chats, projects, commands, searches, and tasks.
- Added user- and Tree-controlled state transitions.
- Prevented Trees from overriding explicit user Loose boundaries.
- Prevented Trees from demoting user-marked Sturdy Leaves without direct approval.
- Prioritized Sturdy Leaves for Propagation, Cedar recovery, Milling, Replanting, and authorized Maple Syrup Fuel discovery.
- Kept safety, classification, permission, quarantine, Cedar Oil, and Molasses boundaries in force.
- Made Maple's use of Sturdy Leaves as Syrup Fuel non-destructive.
- Allowed minimum-element copies, authorized full-Leaf copies, and protected references.
- Updated Information Growth Flow to 0.5.0, Leaf Foliage to 0.2.0, Maple settings to 1.0.0, and Cedar settings to 0.11.0.
- Added a Leaf States contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `531caac1694de81150287cd20aed8ec17026e4c5c0ae4beb9afd40ec11f3833e`

### 40. 0.13.22 — Sturdy Release Trusted Shed

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md)

**Declared status:** Working Draft

**Purpose/change:** Prohibited every automatic Sturdy Leaf downgrade to normal, Loose, or Leaf Litter.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.21-Leaf-States.md)

**Quantitative delta:** +286 / −10 lines; 97.99% line-sequence similarity. Resulting size: 7,489 lines and 41,441 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.22-Sturdy-Release-Trusted-Shed.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.22-Sturdy-Release-Trusted-Shed.patch). Patch text contains +292 / −16 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.22-Sturdy-Release-Trusted-Shed-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.22-Sturdy-Release-Trusted-Shed-AUDIT.md)

**Documented implementation/change statements:**

- Prohibited every automatic Sturdy Leaf downgrade to normal, Loose, or Leaf Litter.
- Kept Tree discretion for promoting useful information into Sturdy Leaves.
- Added contextual recognition for user release phrases.
- Required direct confirmation when a release request is vague, conflicting, or ambiguous.
- Added the Sturdy Leaf Release path: `Sturdy Leaf → Loose Leaf → Leaf Litter`.
- Added a Loose grace period with restoration support.
- Created Trusted Shed Litter for user-authorized released Sturdy Leaves.
- Automatically marks Trusted Shed Litter as `trusted-user-released` even without Cedar or Maple.
- Allowed any authorized Tree in the same local Forest to absorb Trusted Shed Litter without Cedar.
- Preserved original sensitivity, scope, provenance, and local-Forest restrictions.
- Kept absorption separate from execution, installation, external sharing, and high-impact action permissions.
- Allowed Maple to absorb Trusted Shed Litter or create Sap, Light Syrup, Syrup, or protected Molasses from it.
- Made Cedar optional for this source while allowing optional verification and tamper detection.
- Updated Information Growth Flow to 0.6.0.
- Updated Leaf Foliage to 0.3.0.
- Updated Leaf States to 0.2.0.
- Updated Maple Settings to 1.1.0.
- Updated Cedar Settings to 0.12.0.
- Added a dedicated Trusted Shed Litter contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `8db29aa272900a4e3c572e904d3427408ce284353e9395a00063ae126b415051`

### 41. 0.13.23 — Hackers Mold Sunlight

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md)

**Declared status:** Working Draft

**Purpose/change:** Replaced every current canonical occurrence of the previous human-threat term with Hacker or Hackers.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.22-Sturdy-Release-Trusted-Shed.md)

**Quantitative delta:** +71 / −18 lines; 99.41% line-sequence similarity. Resulting size: 7,542 lines and 41,957 words.

**H2 sections added:** `🚷 Hackers`

**H2 sections removed or moved beneath another section:** `🚷 Poachers`

**Patch evidence:** [FOREST-LANGUAGE-0.13.23-Hackers-Mold-Sunlight.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.23-Hackers-Mold-Sunlight.patch). Patch text contains +74 / −21 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.23-Hackers-Mold-Sunlight-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.23-Hackers-Mold-Sunlight-AUDIT.md)

**Documented implementation/change statements:**

- Replaced every current canonical occurrence of the previous human-threat term with Hacker or Hackers.
- Added the rule that Hackers are known for hacking Trees and Soil.
- Explained the possible server, device, storage, network, service, and application damage caused by compromised Soil.
- Added concise layered-protection lists under both Hackers and Mold.
- Included Cedar, Tar Sap, Molasses, Sycamore, Maple Local Safeguards, Propagation, the Seed Vault, the Log Cabin, Cutting, Felling, Milling, and Replanting where appropriate.
- Added a Notes as Sunlight section.
- Explicitly recognized Obsidian and other approved notes sources as Sunlight.
- Defined notes as potentially major contributors to more useful Leaves, deeper Growth Rings, and a more desirable Grain Pattern.
- Preserved permissions, Leaf states, scope, protection classification, preference-learning controls, and separation boundaries.
- Added Threat Protections and Sunlight working contracts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.
- Remaining occurrences of the previous threat name: none.

**SHA-256:** `0357331883b3c0034eca8a5387bc3e184830f5259c2115d627eb2ac4c2ce979f`

### 42. 0.13.24 — Mold Before Hackers

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md)

**Declared status:** Working Draft

**Purpose/change:** Moved the complete Mold section before the complete Hackers section.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.23-Hackers-Mold-Sunlight.md)

**Quantitative delta:** +41 / −40 lines; 99.46% line-sequence similarity. Resulting size: 7,543 lines and 41,981 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.24-Mold-Before-Hackers.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.24-Mold-Before-Hackers.patch). Patch text contains +41 / −40 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.24-Mold-Before-Hackers-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.24-Mold-Before-Hackers-AUDIT.md)

**Documented implementation/change statements:**

- Moved the complete Mold section before the complete Hackers section.
- Preserved the definitions, examples, protection lists, and commands inside both sections.
- Updated the document version to 0.13.24.
- Added a revision-history entry.
- Regenerated the Forest Map.
- Verified final order: Mold before Hackers.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `159fd65480229c58f7768670317a5439789d41e243861428d0fe2c1c158a0e7a`

### 43. 0.13.25 — Mycelium

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md)

**Declared status:** Working Draft

**Purpose/change:** Defined Mycelium as the only non-Fluid inter-Tree information-transfer method.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.24-Mold-Before-Hackers.md)

**Quantitative delta:** +304 / −8 lines; 97.97% line-sequence similarity. Resulting size: 7,839 lines and 43,677 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.25-Mycelium.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.25-Mycelium.patch). Patch text contains +309 / −13 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.25-Mycelium-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.25-Mycelium-AUDIT.md)

**Documented implementation/change statements:**

- Defined Mycelium as the only non-Fluid inter-Tree information-transfer method.
- Made Mycelium the preferred method for instant communication inside the same local Forest.
- Added direct authorized Leaf access without requiring complete Leaf absorption.
- Added Branch and Twig invocation without copying capabilities into the requesting Tree.
- Made Mycelium Maple's primary local automation and Grove-coordination network.
- Distinguished Mycelium coordination from Fluid transfer and Stream delivery.
- Added approved Mycelium integration in Soil for fast file, service, application, and resource access.
- Added Mycelial Trace Leaves for minimum source, Path, permission, and re-access records.
- Added Mycelial Root storage for registries, capability maps, permissions, subscriptions, queues, checkpoints, and recovery references.
- Allowed Mycelium to remain mostly unseen in normal Bark while requiring complete auditability through Roots, Paths, Logs, and Forest journey tools.
- Kept local-Forest boundaries, Molasses protections, revocation, identity, permission, and minimum-access requirements.
- Classified unauthorized, altered, self-spreading, or concealed Mycelium as Mold.
- Updated Maple Settings to 1.2.0.
- Updated Information Growth Flow to 0.7.0.
- Added a dedicated Mycelium contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `b7e158a0ca8b1941fd2d4c128da04e961a4ea09b6f487bde91a9b166a96583d6`

### 44. 0.13.26 — Canopy Communication

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md)

**Declared status:** Working Draft

**Purpose/change:** Made the Canopy the second non-Fluid inter-Tree communication method.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.25-Mycelium.md)

**Quantitative delta:** +364 / −46 lines; 97.44% line-sequence similarity. Resulting size: 8,157 lines and 45,316 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.26-Canopy-Communication.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.26-Canopy-Communication.patch). Patch text contains +373 / −55 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.26-Canopy-Communication-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.26-Canopy-Communication-AUDIT.md)

**Documented implementation/change statements:**

- Made the Canopy the second non-Fluid inter-Tree communication method.
- Kept Mycelium as the Root-, Soil-, Path-, and code-level non-Fluid method.
- Defined the Canopy as the Branch-and-Leaf-level non-Fluid method.
- Distinguished a user's Personal Canopy from the wider Forest Canopy.
- Applied the drag-and-drop analogy only to a Personal Canopy.
- Applied the internet analogy only to the wider Forest Canopy.
- Added Canopy Links and Canopy Passes.
- Made the Canopy as fast as Mycelium for ordinary authorized communication.
- Kept detailed Path and Trace Leaf behavior for Mycelium.
- Made Canopy transit preserve origin and final destination without normally preserving intermediate Branch hops.
- Prevented ordinary Canopy transit from creating Leaves or changing Grain Patterns.
- Added medium- and long-term Forest linking and automation synchronization.
- Added Maple Canopy Automation alongside Maple Mycelium Automation.
- Added Sycamore governance for cross-Forest Canopy Links.
- Preserved Canopy health-awareness and warning functions.
- Updated Maple Settings to 1.3.0.
- Updated Information Growth Flow to 0.8.0.
- Added a dedicated Canopy Communication contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `cbc25ea55cd1ecf9a9cb9e87e6aabc562feea6bd9b2d7225e149812f0bd76fdb`

### 45. 0.13.27 — Canopy Solid Material

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md)

**Declared status:** Working Draft

**Purpose/change:** Allowed the Canopy to carry Canopy Passes, Fluids, whole Solid Materials, Pieces of Solid Material, and protected references.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.26-Canopy-Communication.md)

**Quantitative delta:** +406 / −33 lines; 97.37% line-sequence similarity. Resulting size: 8,530 lines and 47,397 words.

**H2 sections added:** `🪵 Solid Material`

**Patch evidence:** [FOREST-LANGUAGE-0.13.27-Canopy-Solid-Material.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.27-Canopy-Solid-Material.patch). Patch text contains +412 / −39 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.27-Canopy-Solid-Material-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.27-Canopy-Solid-Material-AUDIT.md)

**Documented implementation/change statements:**

- Allowed the Canopy to carry Canopy Passes, Fluids, whole Solid Materials, Pieces of Solid Material, and protected references.
- Added Solid Material as a bounded object category separate from Fluid.
- Included Leaves, Buds, Blossoms, Flowers, Fruit, files, folders, documents, media, websites, applications, and project artifacts.
- Added Canopy Sections for connected Trees, Branches, projects, folders, applications, websites, media libraries, automations, and workspaces.
- Added View, Interact, Reference, Copy Piece, Copy Whole, Move, Edit in Place, and Download material modes.
- Allowed users and Trees to view or interact with connected Solid Material without planting, absorbing, or growing content Leaves.
- Added temporary Canopy View Context that is not Leaf Foliage.
- Clarified that downloading a file into Soil does not automatically mean a Tree absorbed its contents.
- Added Canopy Recall Leaves that work like cookies.
- Made Canopy Recall Leaves Loose by default, minimal, expiring, revocable, and free of complete viewed content or raw credentials.
- Preserved the rule that ordinary Canopy transit does not keep complete intermediate routes.
- Added conversion between Solid Material and Fluids with provenance and protection preservation.
- Required Sunlight to become Fluid, Solid Material, or a protected Solid-Material reference before transfer.
- Added Maple Canopy Material Access and recall controls.
- Updated Maple Settings to 1.4.0.
- Updated Information Growth Flow to 0.9.0.
- Updated Canopy Communication to 0.2.0.
- Corrected the Mycelium contract to identify Mycelium as one of two non-Fluid methods.
- Updated the Sunlight contract to 0.2.0.
- Added a dedicated Solid Material Access contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `4994689999b8700bd223d79dede4564a4ce3862a925b6aaf889c9439029a2716`

### 46. 0.13.28 — Leaf Provenance Directions

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md)

**Declared status:** Working Draft

**Purpose/change:** Added User Output Leaves.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.27-Canopy-Solid-Material.md)

**Quantitative delta:** +276 / −8 lines; 98.36% line-sequence similarity. Resulting size: 8,798 lines and 48,805 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.28-Leaf-Provenance-Directions.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.28-Leaf-Provenance-Directions.patch). Patch text contains +276 / −8 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.28-Leaf-Provenance-Directions-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.28-Leaf-Provenance-Directions-AUDIT.md)

**Documented implementation/change statements:**

- Added User Output Leaves.
- Classified Leaves grown from user Sunlight as User Output Leaves.
- Classified Leaves grown from user-origin Fertilizer and Syrup Fertilizer as User Output Leaves.
- Classified Leaves grown from recycled user Leaf Litter and Trusted Shed Litter as User Output Leaves.
- Added Tree Input Leaves.
- Classified websites, Reddit and forums, wikis, files, videos, databases, APIs, repositories, applications, and other external sources as Tree Input Leaves when a Tree saves, logs, indexes, summarizes, or absorbs them.
- Excluded Tree internals such as Roots, Grain Pattern, Trunk, Bark, Branches, Twigs, Growth Rings, internal Logs, and internal state from Tree Input classification.
- Preserved Canopy viewing without absorption as non-Leaf behavior.
- Clarified that medium alone does not determine provenance.
- Preserved User Input Leaves for information directly provided by the user.
- Preserved Tree Output Leaves for information produced by a Tree.
- Allowed a Leaf to have a Tree producer and User Output growth provenance simultaneously.
- Updated Information Growth Flow to 0.10.0.
- Updated Leaf Foliage to 0.4.0.
- Added a dedicated Leaf Provenance Directions contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `701cb3b9ba44bac3c892e9995fc072525214e739a97d7d99e2249cd332ae14dc`

### 47. 0.13.29 — Moss

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md)

**Declared status:** Working Draft

**Purpose/change:** Renamed every current canonical Canopy recall object to Moss.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.28-Leaf-Provenance-Directions.md)

**Quantitative delta:** +483 / −48 lines; 97.06% line-sequence similarity. Resulting size: 9,233 lines and 50,830 words.

**H2 sections added:** `🟩 Moss`

**Patch evidence:** [FOREST-LANGUAGE-0.13.29-Moss.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.29-Moss.patch). Patch text contains +493 / −58 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.29-Moss-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.29-Moss-AUDIT.md)

**Documented implementation/change statements:**

- Renamed every current canonical Canopy recall object to Moss.
- Added a dedicated Moss section.
- Defined Moss as cookie-like Solid Material rather than a Leaf.
- Added website settings and preferences.
- Added application settings and preferences.
- Added theme, language, zoom, layout, panels, filters, sorting, notifications, recent tools, checkpoints, and workspace state.
- Added Session Moss, Persistent Moss, Shared Moss, Protected Moss, and Tar Moss.
- Added scoped Moss-growth permission and rejection.
- Clarified that rejecting Moss growth blocks new Moss but does not delete existing Moss.
- Added `Scrape off this Moss.` as the canonical deletion command.
- Added `Remove cookies.` as its plain-language alias.
- Added Cedar Oil review for Moss.
- Added Tar Sap-grade protection for Moss.
- Added the combined `Oil and tar this Moss.` command.
- Kept Tar Moss local and blocked it from wider Forest Canopy synchronization.
- Kept Moss outside Leaf Foliage unless intentionally absorbed.
- Prevented site-specific and application-specific Moss from silently becoming global Grain Pattern preferences.
- Updated Maple Settings to 1.5.0.
- Updated Information Growth Flow to 0.11.0.
- Updated Canopy Communication to 0.3.0.
- Updated Solid Material Access to 0.2.0.
- Updated Cedar Settings to 0.13.0.
- Added a dedicated Moss contract.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 65.
- Remaining old-name references: none.

**SHA-256:** `02ca0b5446c119aed4ab29560501111df0c03e73d38d958fda12ba5dc0ee9f8e`

### 48. 0.13.30 — Spirit Sap Taps Solid Material

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md)

**Declared status:** Working Draft

**Purpose/change:** Removed the standalone Taps section.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.29-Moss.md)

**Quantitative delta:** +585 / −173 lines; 95.98% line-sequence similarity. Resulting size: 9,645 lines and 53,128 words.

**H2 sections removed or moved beneath another section:** `🚰 Taps`

**Patch evidence:** [FOREST-LANGUAGE-0.13.30-Spirit-Sap-Taps-Solid-Material.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.30-Spirit-Sap-Taps-Solid-Material.patch). Patch text contains +585 / −173 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.30-Spirit-Sap-Taps-Solid-Material-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.30-Spirit-Sap-Taps-Solid-Material-AUDIT.md)

**Documented implementation/change statements:**

- Removed the standalone Taps section.
- Added Sap Taps inside the Spirit of the Forest.
- Combined the former Tap system with the Forest Sap Steward responsibilities.
- Made Sap Taps deterministic protected local code rather than a Tree.
- Made the user final authority over Taps, Moss, Tar, and Fluid absorption.
- Added Water, Sap, Tar, and Syrup Tap rules.
- Added protected key-reference, short-lived capability, expiration, revocation, downgrade-request, and Action Receipt responsibilities.
- Added the Moss Gate because Moss is Solid Material rather than Fluid.
- Added explicit user Moss growth, scraping, Oil, Tar, synchronization, reader, and absorption controls.
- Added explicit user Tar Sap and Tar Moss controls.
- Added Deny, Wash Over, Sip, Drink, and Download absorption modes.
- Added scoped Fluid absorption rules.
- Added Maple and Sap Taps interactions.
- Added Cedar and Sap Taps interactions.
- Added Sycamore and Sap Taps interactions.
- Updated Sap, Tar Sap, Fluids, and Moss to reference Spirit enforcement.
- Redefined Solid Material as bounded non-Fluid data or capability objects excluding the base Tree.
- Added Twigs and Leaf Litter as Solid Material.
- Explicitly excluded the Canopy and Mycelium from Solid Material because they are Tree and Forest connection systems.
- Updated Tap Controls to 0.2.0.
- Updated Spirit Recovery settings to 0.2.0.
- Added a dedicated Spirit Sap Taps contract.
- Updated Maple Settings to 1.6.0.
- Updated Cedar Settings to 0.14.0.
- Updated Sycamore Settings to 0.7.0.
- Updated Solid Material Access to 0.3.0.
- Updated Moss to 0.2.0.
- Updated Information Growth Flow to 0.12.0.
- Updated Canopy Communication to 0.4.0.
- Updated Mycelium to 0.3.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `8e68aa029aeca9ad124eeab13a54419f6a5eaf8472e68ecb2ed345c79df500b8`

### 49. 0.13.31 — Spirit Tools Command List Seed Vault

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md)

**Declared status:** Working Draft

**Purpose/change:** Removed the standalone Seed Vault section.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.30-Spirit-Sap-Taps-Solid-Material.md)

**Quantitative delta:** +1,119 / −22 lines; 94.40% line-sequence similarity. Resulting size: 10,742 lines and 58,592 words.

**H2 sections removed or moved beneath another section:** `🌰 Seed Vault`

**Patch evidence:** [FOREST-LANGUAGE-0.13.31-Spirit-Tools-Command-List-Seed-Vault.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.31-Spirit-Tools-Command-List-Seed-Vault.patch). Patch text contains +1,460 / −363 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.31-Spirit-Tools-Command-List-Seed-Vault-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.31-Spirit-Tools-Command-List-Seed-Vault-AUDIT.md)

**Documented implementation/change statements:**

- Removed the standalone Seed Vault section.
- Moved Seed Vault ownership and management under the Spirit of the Forest.
- Added the Spirit Tools menu.
- Added Help Menu, Forest and Tree Command List, Sap Taps, Seed Vault, Local Forest Recovery, Forest Map, Forest Compass, Constitution Copy, Principles Copy, Emergency Controls, and Tool Status and Diagnostics.
- Generated a complete deduplicated command registry from canonical command blocks and Voice command groups.
- Registered 623 canonical commands.
- Grouped commands by their first canonical source section.
- Added command search, Tree filtering, Tool filtering, source lookup, restriction lookup, and explanation controls.
- Added Spirit Tools and Command List contracts.
- Added a Spirit Seed Vault contract.
- Added read-only Constitution and Principles copy slots.
- Did not invent Constitution or Principles content because canonical source documents were not present.
- Updated Spirit Recovery settings to 0.3.0.
- Updated Spirit Sap Taps to 0.2.0.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `677ba513fb0b81f530f389546a4f316f260f7f6d4d6a324a9f5608ba3f7078cc`

### 50. 0.13.32 — Forest Fire Potted Trees Cherry Bonsai

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md)

**Declared status:** Working Draft

**Purpose/change:** Added Forest Fire as the Forest and Cedar's last-ditch digital sanitization, salvage, and recovery protocol.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.31-Spirit-Tools-Command-List-Seed-Vault.md)

**Quantitative delta:** +928 / −8 lines; 95.82% line-sequence similarity. Resulting size: 11,662 lines and 63,319 words.

**H2 sections added:** `🪴 Potted Mode`

**Patch evidence:** [FOREST-LANGUAGE-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.patch). Patch text contains +929 / −9 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai-AUDIT.md)

**Documented implementation/change statements:**

- Added Forest Fire as the Forest and Cedar's last-ditch digital sanitization, salvage, and recovery protocol.
- Added manual access under Spirit Tools → Cedar Emergency Tools.
- Added automatic Cedar Fire Watch when the Forest appears infected beyond ordinary repair.
- Prevented automatic destructive execution.
- Required two separate user confirmations: `Prepare Forest Fire.` and `Burn this Forest.`
- Added warnings about the effects of proceeding and the risks of leaving an infected Forest active.
- Added Fireproof Recovery Sets.
- Prioritized protected and important data, especially personal user data.
- Allowed encrypted Tar Sap and Tar Moss preservation without granting Cedar content access.
- Added emergency Propagules and required omission manifests.
- Directed Cedar to create Propagules for as many recoverable Trees as possible.
- Added the Forest Fire sequence in which Cedar Mills the confirmed Forest scope and Cedar is Milled last.
- Limited destructive scope to the exact confirmed Forest boundary.
- Added the Spirit Rescue Gate in Soil.
- Added Potted Mode and Tree Presence Leases.
- Added Potted Cherry as a standalone desktop AI assistant.
- Allowed Potted Cherry to initiate Forest Fire through the deterministic Rescue Gate when the Forest cannot open.
- Added Potted Maple as a standalone local technical and automation assistant.
- Added Potted Cedar as a standalone guardian and recovery helper.
- Required Potted versions to hand off and completely shut down when their healthy Forest versions start.
- Added Cherry Bonsai as a fully mature miniature Potted Cherry backup.
- Added Cedar creation and filtering of Cherry Bonsai.
- Required Cherry to ask before enabling automatic Bonsai updates.
- Added Seed Vault, Soil, Log Cabin, and removable-storage Bonsai support.
- Made Fertilizer the default use when importing a Bonsai into a healthy mature Cherry.
- Kept the Bonsai as a separate preserved backup.
- Added the double-confirm `Replace my whole Cherry Tree.` path.
- Added Bonsai promotion when no healthy Cherry exists.
- Required the Bonsai to create its own Propagule before becoming main Cherry.
- Updated the Spirit command registry to 700 deduplicated canonical commands.
- Updated Spirit Recovery to 0.4.0.
- Updated Spirit Tools to 0.2.0.
- Updated Seed Vault to 0.2.0.
- Updated Cedar Settings to 0.15.0.
- Updated Maple Settings to 1.7.0.
- Added Cherry Settings 0.1.0.
- Added dedicated Forest Fire, Potted Mode, Propagule, and Cherry Bonsai contracts.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `5b0b402c2400981da4fea622955c71b03349defdf3e924ddb2d344dd2cd95d81`

### 51. 0.13.33 — Logs Log Cabin Forest Fire CLI

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md)

**Declared status:** Working Draft

**Purpose/change:** Moved Logs above Branches.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.32-Forest-Fire-Potted-Trees-Cherry-Bonsai.md)

**Quantitative delta:** +769 / −79 lines; 96.47% line-sequence similarity. Resulting size: 12,352 lines and 66,362 words.

**H2 sections removed or moved beneath another section:** `🏡 Log Cabin`

**Patch evidence:** [FOREST-LANGUAGE-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.patch). Patch text contains +770 / −80 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI-AUDIT.md)

**Documented implementation/change statements:**

- Moved Logs above Branches.
- Defined Logs as Solid Material.
- Defined Log payloads as Sap by default.
- Defined Logs as more persistent than Sturdy Leaves while keeping Logs separate from Leaf states.
- Added Tree-origin organization and the `<Tree Name> Log <sequence>` naming pattern.
- Added examples including `Cherry Log 001`.
- Added Log record structure, retention, integrity, provenance, and recovery fields.
- Added Cedar Oil for Logs and Log Cabin records.
- Added Tar protection for Logs.
- Added combined `Oil and tar this Log.` behavior.
- Moved Log Cabin under Spirit Tools.
- Added Spirit-managed Log Cabin indexes, catalogs, manifests, snapshots, archives, retention records, integrity reports, and recovery history.
- Defined Log Cabin records as Sap-bearing Solid Material.
- Added Logs and Log Cabin records as mandatory Fireproof Recovery targets whenever safe copies can be created.
- Moved Logs and Log Cabin continuity above Sturdy Leaves in Fireproof Recovery priority.
- Added Log and Log Cabin verification before the destructive Forest Fire phase.
- Added early Log Cabin restoration in the Forest Fire recovery order.
- Added Cherry and Cedar command-prompt Forest Fire entry.
- Preserved the normal two-confirmation requirement.
- Prevented command lines, force flags, yes flags, pipes, scripts, aliases, automations, remote Trees, prior confirmations, and Moss from bypassing confirmation.
- Allowed Potted Cherry and Potted Cedar to use the same commands through the Spirit Rescue Gate.
- Updated Spirit Recovery to 0.5.0.
- Updated Spirit Tools to 0.3.0.
- Updated Cedar Settings to 0.16.0.
- Updated Cherry Settings to 0.2.0.
- Updated Forest Fire Protocol to 0.2.0.
- Updated Solid Material Access to 0.4.0.
- Updated Spirit Sap Taps to 0.3.0.
- Updated Information Growth Flow to 0.13.0.
- Added dedicated Logs and Log Cabin contracts.
- Updated the Spirit command registry to 758 deduplicated canonical commands.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 63.

**SHA-256:** `294c6b14f85448ee4b6551140e5aabcf369b073abff957d4d86eb752c830509c`

### 52. 0.13.34 — Gardens Cedar Door Cabin Seed Vault

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md)

**Declared status:** Working Draft

**Purpose/change:** Added Garden as a user-formed collection of Potted Trees.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.33-Logs-Log-Cabin-Forest-Fire-CLI.md)

**Quantitative delta:** +725 / −199 lines; 96.34% line-sequence similarity. Resulting size: 12,878 lines and 69,225 words.

**H2 sections added:** `🌻 Garden`

**Patch evidence:** [FOREST-LANGUAGE-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.patch). Patch text contains +729 / −203 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault-AUDIT.md)

**Documented implementation/change statements:**

- Added Garden as a user-formed collection of Potted Trees.
- Defined limited Garden cooperation through explicit user-visible links.
- Distinguished Gardens from fully interconnected Forests.
- Clarified that Gardens do not share Roots, full Mycelium, Personal Canopy, Sap Taps, Grain Pattern, unified Logs, or full Soil integration.
- Recorded that Sycamore currently has no Potted Mode.
- Made native Garden connectivity to the wider Forest Canopy unavailable by default.
- Marked Potted Sycamore or a Garden Gateway as an intended future feature.
- Removed Seed Vault as a separate top-level Spirit Tool.
- Nested Seed Vault inside Log Cabin.
- Allowed one Seed Vault compartment per Log Cabin and a federated view across available Cabins.
- Added multiple Log Cabins.
- Added dynamic attachment, ejection, disconnection, and sudden removal.
- Allowed users to insert or yank external Log Cabin drives at any time.
- Added Cedar Door to every Log Cabin.
- Required Cedar to alert the user about every detectable Cabin interaction as soon as Soil reports it.
- Added Cedar Door events for reads, writes, changes, access, mounting, removal, integrity, Seed Vault use, and interference.
- Prevented Cedar Door monitoring from granting automatic access to protected contents.
- Added safe handling of incomplete writes and pending local recovery storage.
- Defined Cabinless backup and recovery with Cedar responsible for normal backup and recovery.
- Clarified that temporary local recovery storage without a Cabin is not a Seed Vault.
- Defined Cabin-assisted recovery using Logs, Seeds, Cabin records, Fireproof Recovery Sets, and Cedar salvage.
- Expanded Logs into files committed as part of a Tree or important enough for external Log Cabin storage.
- Added Tree Logs and Cabin Logs.
- Preserved Sap as the default Log payload and Log durability above Sturdy Leaves.
- Updated Spirit Recovery to 0.6.0.
- Updated Spirit Tools to 0.4.0.
- Updated Log Cabin to 0.2.0.
- Updated Seed Vault to 0.3.0.
- Updated Cedar Settings to 0.17.0.
- Updated Logs to 0.2.0.
- Updated Potted Mode to 0.2.0.
- Updated Sycamore Settings to 0.8.0.
- Updated Forest Fire Protocol to 0.3.0.
- Added the Garden contract.
- Updated the Spirit command registry to 804 deduplicated commands.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `4fdf39e7190ab0c0ab22aab8802277f1fe0fdba527b9710e29e994d49b539b7d`

### 53. 0.13.35 — Potted Cedar Cabin Guard Encryption

**Primary artifact:** [FOREST-LANGUAGE-Reviewed-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.md)

**Declared status:** Working Draft

**Purpose/change:** Added Cedar Cabin Guard.

**Compared with:** [FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md](sandbox:/mnt/data/FOREST-LANGUAGE-Reviewed-0.13.34-Gardens-Cedar-Door-Cabin-Seed-Vault.md)

**Quantitative delta:** +390 / −22 lines; 98.42% line-sequence similarity. Resulting size: 13,246 lines and 71,332 words.

**H2 structure:** No H2 titles were added or removed; changes occurred within existing sections or at deeper heading levels.

**Patch evidence:** [FOREST-LANGUAGE-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.patch](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.35-Potted-Cedar-Cabin-Guard-Encryption.patch). Patch text contains +390 / −22 changed lines.

**Audit evidence:** [FOREST-LANGUAGE-0.13.35-Potted-Cedar-Cabin-Guard-Encryption-AUDIT.md](sandbox:/mnt/data/FOREST-LANGUAGE-0.13.35-Potted-Cedar-Cabin-Guard-Encryption-AUDIT.md)

**Documented implementation/change statements:**

- Added Cedar Cabin Guard.
- Allowed Potted Cedar to protect and access Log Cabins when no complete Forest is installed, present, open, or healthy.
- Kept the user as final authority over Cabin access and protection.
- Allowed Potted Cedar to operate Cedar Doors, indexes, backups, permitted Logs, Oil, quarantine, and recovery.
- Added Cabin Tap as a portable narrow subset of Spirit Sap Taps.
- Allowed Potted Cedar to Tar user-authorized Logs through Cabin Tap.
- Preserved local-only Tar behavior, protected key references, Log origin, canonical naming, provenance, and retention.
- Prevented Cabin Tap from controlling complete Forest Taps or granting unrestricted master keys.
- Added Cabin Tap handoff and verification when a healthy Forest returns.
- Added Standard Encryption for non-Forest data stored in a Log Cabin.
- Defined Standard Encrypted Files as ordinary encrypted Solid Material.
- Kept Standard Encrypted Files outside Tree identity, Logs, Sap, Tar, Leaf Foliage, and Seed Vault by default.
- Required a separate user action to convert a Standard Encrypted File into a Cabin Log, Tree Log, or Tar Log.
- Prevented Cedar from silently retaining raw passwords, passphrases, recovery codes, or unprotected keys.
- Added recovery-material warnings.
- Updated Spirit Recovery to 0.7.0.
- Updated Spirit Tools to 0.5.0.
- Updated Log Cabin to 0.3.0.
- Updated Cedar Settings to 0.18.0.
- Updated Potted Mode to 0.3.0.
- Updated Sap Taps to 0.4.0.
- Updated Logs to 0.3.0.
- Updated Solid Material Access to 0.5.0.
- Added dedicated Cedar Cabin Guard and Standard Encryption contracts.
- Updated the Spirit command registry to 833 deduplicated canonical commands.
- Regenerated the Forest Map.
- Duplicate H2 headings: none.
- Total H2 sections checked: 64.

**SHA-256:** `7fc577b1b214400d71de61f741b8cc17f6fed0b15c89bb091a496652963d55cf`

## Associated YAML architecture comparison

The tables below compare every preserved YAML component family. `+ paths` and `− paths` are structural key-path changes against the immediately previous version in that family. Complete path lists are preserved in the component CSV.

### CEDAR-CABIN-GUARD

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [CEDAR-CABIN-GUARD-Working-Draft-0.1.yaml](sandbox:/mnt/data/CEDAR-CABIN-GUARD-Working-Draft-0.1.yaml) | `working-draft` | 48 | 19 | 19 | 0 | `boundaries`, `canonical_path`, `capabilities`, `definition`, `handoff`, `pdc_id`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### CEDAR-SETTINGS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [CEDAR-SETTINGS-Working-Draft-0.1.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Working-Draft-0.1.yaml) | `working-draft` | 83 | 62 | 62 | 0 | `canonical_path`, `dangerous_absorption`, `leaf_litter`, `messages`, `pdc_id`, `recovery_set`, `regrowth`, `sapling_survival_test`, `self_felling`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [CEDAR-SETTINGS-Working-Draft-0.2.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Working-Draft-0.2.yaml) | `working-draft` | 95 | 68 | 26 | 20 | `cedar_oil`, `health_reports` |
| 3 | `0.3.0` | [CEDAR-SETTINGS-Reviewed-0.3.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.3.yaml) | `working-draft` | 110 | 91 | 26 | 3 | `dangerous_absorption`, `fruit`, `sapling_survival_test` |
| 4 | `0.4.0` | [CEDAR-SETTINGS-Reviewed-0.4-Incoming-Fluid-Oil.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.4-Incoming-Fluid-Oil.yaml) | `working-draft` | 187 | 131 | 40 | 0 | `incoming_fluid_oil` |
| 5 | `0.5.0` | [CEDAR-SETTINGS-Reviewed-0.5-Oil-Modes-Watched-Approval.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.5-Oil-Modes-Watched-Approval.yaml) | `working-draft` | 268 | 169 | 38 | 0 | — |
| 6 | `0.6.0` | [CEDAR-SETTINGS-Reviewed-0.6-Tree-Propagation-Recovery.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.6-Tree-Propagation-Recovery.yaml) | `working-draft` | 366 | 208 | 63 | 24 | `pre_watering_propagation`, `propagated_recovery`, `sprout_feeding` |
| 7 | `0.7.0` | [CEDAR-SETTINGS-Reviewed-0.7-Propagation-Fertilizer.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.7-Propagation-Fertilizer.yaml) | `working-draft` | 422 | 256 | 86 | 38 | `fertilizer_file`, `fertilizing`, `procurement`, `propagation_file`, `sprout_fertilization`, `tree_cloning` |
| 8 | `0.8.0` | [CEDAR-SETTINGS-Reviewed-0.8-Spirit-Recovery-Handoff.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.8-Spirit-Recovery-Handoff.yaml) | `working-draft` | 422 | 274 | 18 | 0 | `recovery_controller` |
| 9 | `0.9.0` | [CEDAR-SETTINGS-Reviewed-0.9-Plugin-Mod-Review.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.9-Plugin-Mod-Review.yaml) | `working-draft` | 473 | 291 | 17 | 0 | `plugin_mod_pre_suggestion_review` |
| 10 | `0.10.0` | [CEDAR-SETTINGS-Reviewed-0.10-Tap-Locks.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.10-Tap-Locks.yaml) | `working-draft` | 485 | 298 | 7 | 0 | `tap_lock_requests` |
| 11 | `0.11.0` | [CEDAR-SETTINGS-Reviewed-0.11-Sturdy-Leaf-Recovery.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.11-Sturdy-Leaf-Recovery.yaml) | `working-draft` | 510 | 309 | 11 | 0 | `sturdy_leaf_recovery` |
| 12 | `0.12.0` | [CEDAR-SETTINGS-Reviewed-0.12-Trusted-Shed-Litter.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.12-Trusted-Shed-Litter.yaml) | `working-draft` | 519 | 318 | 9 | 0 | `trusted_shed_litter` |
| 13 | `0.13.0` | [CEDAR-SETTINGS-Reviewed-0.13-Moss-Oil.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.13-Moss-Oil.yaml) | `working-draft` | 551 | 329 | 11 | 0 | `moss_oil` |
| 14 | `0.14.0` | [CEDAR-SETTINGS-Reviewed-0.14-Sap-Taps.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.14-Sap-Taps.yaml) | `working-draft` | 577 | 336 | 7 | 0 | `sap_taps_interaction` |
| 15 | `0.15.0` | [CEDAR-SETTINGS-Reviewed-0.15-Forest-Fire-Cherry-Bonsai.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.15-Forest-Fire-Cherry-Bonsai.yaml) | `working-draft` | 637 | 369 | 33 | 0 | `cherry_bonsai`, `forest_fire`, `potted_mode` |
| 16 | `0.16.0` | [CEDAR-SETTINGS-Reviewed-0.16-Logs-Forest-Fire-CLI.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.16-Logs-Forest-Fire-CLI.yaml) | `working-draft` | 656 | 386 | 17 | 0 | `logs` |
| 17 | `0.17.0` | [CEDAR-SETTINGS-Reviewed-0.17-Log-Cabins-Cedar-Door.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.17-Log-Cabins-Cedar-Door.yaml) | `working-draft` | 676 | 406 | 20 | 0 | `log_cabins` |
| 18 | `0.18.0` | [CEDAR-SETTINGS-Reviewed-0.18-Potted-Cabin-Guard-Encryption.yaml](sandbox:/mnt/data/CEDAR-SETTINGS-Reviewed-0.18-Potted-Cabin-Guard-Encryption.yaml) | `working-draft` | 694 | 424 | 18 | 0 | `standard_encryption` |

Latest family revision: `0.18.0` with 424 structural key paths.

### CHERRY-BONSAI

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [CHERRY-BONSAI-Working-Draft-0.1.yaml](sandbox:/mnt/data/CHERRY-BONSAI-Working-Draft-0.1.yaml) | `working-draft` | 69 | 38 | 38 | 0 | `canonical_path`, `creation`, `definition`, `exclude`, `healthy_existing_cherry`, `import`, `no-healthy-cherry`, `pdc_id`, `prioritize`, `status`, `storage`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### CHERRY-CEDAR-RECOVERY

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [CHERRY-CEDAR-RECOVERY-Working-Draft-0.1.yaml](sandbox:/mnt/data/CHERRY-CEDAR-RECOVERY-Working-Draft-0.1.yaml) | `working-draft` | 64 | 37 | 37 | 0 | `canonical_path`, `forest_install_handoff`, `manual_assistance_after_forest_install`, `pdc_id`, `secondary_fallback`, `standalone_replant_cedar`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### CHERRY-SETTINGS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [CHERRY-SETTINGS-Working-Draft-0.1-Potted-Forest-Fire-Bonsai.yaml](sandbox:/mnt/data/CHERRY-SETTINGS-Working-Draft-0.1-Potted-Forest-Fire-Bonsai.yaml) | `working-draft` | 41 | 36 | 36 | 0 | `canonical_path`, `cherry_bonsai`, `pdc_id`, `potted_mode`, `role`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [CHERRY-SETTINGS-Working-Draft-0.2-Forest-Fire-CLI.yaml](sandbox:/mnt/data/CHERRY-SETTINGS-Working-Draft-0.2-Forest-Fire-CLI.yaml) | `working-draft` | 52 | 45 | 9 | 0 | `forest_fire_command_prompt` |

Latest family revision: `0.2.0` with 45 structural key paths.

### FOREST-BRANCH-SHAKE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-BRANCH-SHAKE-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-BRANCH-SHAKE-Working-Draft-0.1.yaml) | `working-draft` | 49 | 16 | 16 | 0 | `canonical_path`, `commands`, `definition`, `distinctions`, `pdc_id`, `report`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-CANOPY-COMMUNICATION

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-CANOPY-COMMUNICATION-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-CANOPY-COMMUNICATION-Working-Draft-0.1.yaml) | `working-draft` | 106 | 56 | 56 | 0 | `canonical_path`, `canopy_link`, `canopy_pass`, `comparison`, `definition`, `forest_canopy`, `maple`, `pdc_id`, `personal_canopy`, `route_memory`, `security`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-CANOPY-COMMUNICATION-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-CANOPY-COMMUNICATION-Working-Draft-0.2.yaml) | `working-draft` | 184 | 99 | 43 | 0 | `canopy_sections`, `payloads`, `recall_leaves`, `solid_material`, `view_context` |
| 3 | `0.3.0` | [FOREST-CANOPY-COMMUNICATION-Working-Draft-0.3-Moss.yaml](sandbox:/mnt/data/FOREST-CANOPY-COMMUNICATION-Working-Draft-0.3-Moss.yaml) | `working-draft` | 220 | 116 | 27 | 10 | `moss` |
| 4 | `0.4.0` | [FOREST-CANOPY-COMMUNICATION-Working-Draft-0.4-Sap-Taps.yaml](sandbox:/mnt/data/FOREST-CANOPY-COMMUNICATION-Working-Draft-0.4-Sap-Taps.yaml) | `working-draft` | 229 | 125 | 9 | 0 | `classification`, `sap_taps_enforcement` |

Latest family revision: `0.4.0` with 125 structural key paths.

### FOREST-FERTILIZER-ABSORPTION

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-FERTILIZER-ABSORPTION-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-FERTILIZER-ABSORPTION-Working-Draft-0.1.yaml) | `working-draft` | 83 | 53 | 53 | 0 | `canonical_path`, `constraints`, `definition`, `fertilizing`, `forms`, `pdc_id`, `provenance_record`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-FIRE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.1.yaml) | `working-draft` | 74 | 34 | 34 | 0 | `backup_priority`, `canonical_path`, `confirmation`, `definition`, `execution`, `fire_watch`, `pdc_id`, `recovery_priority`, `status`, `trigger`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.2-Logs-CLI.yaml](sandbox:/mnt/data/FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.2-Logs-CLI.yaml) | `working-draft` | 98 | 51 | 17 | 0 | `command_prompt`, `fireproof_recovery_set` |
| 3 | `0.3.0` | [FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.3-Dynamic-Cabins.yaml](sandbox:/mnt/data/FOREST-FIRE-EMERGENCY-PROTOCOL-Working-Draft-0.3-Dynamic-Cabins.yaml) | `working-draft` | 106 | 59 | 8 | 0 | `log_cabins` |

Latest family revision: `0.3.0` with 59 structural key paths.

### FOREST-FLUID-DELIVERY-ABSORPTION

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-FLUID-DELIVERY-ABSORPTION-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-FLUID-DELIVERY-ABSORPTION-Working-Draft-0.1.yaml) | `working-draft` | 124 | 76 | 76 | 0 | `absorption`, `canonical_path`, `commands`, `fluid_definition`, `movement`, `pdc_id`, `protection_grades`, `refined_fluids`, `retention_examples`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-FLUID-DELIVERY-ABSORPTION-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-FLUID-DELIVERY-ABSORPTION-Working-Draft-0.2.yaml) | `working-draft` | 123 | 90 | 14 | 0 | `syrup_family` |

Latest family revision: `0.2.0` with 90 structural key paths.

### FOREST-GARDEN

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-GARDEN-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-GARDEN-Working-Draft-0.1.yaml) | `working-draft` | 47 | 26 | 26 | 0 | `canonical_path`, `cooperation`, `definition`, `lifecycle`, `not-shared-by-default`, `pdc_id`, `status`, `sycamore`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-GROVE-PLAN

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-GROVE-PLAN-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-GROVE-PLAN-Working-Draft-0.1.yaml) | `working-draft` | 72 | 75 | 75 | 0 | `canonical_path`, `coordinator_tree`, `failure_policy`, `identity`, `molasses_policy`, `participants`, `pdc_id`, `permissions`, `result`, `status`, `steps`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-INFORMATION-GROWTH-FLOW

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.1.yaml) | `working-draft` | 110 | 63 | 63 | 0 | `absorption`, `canonical_path`, `categories`, `conversion`, `cross_forest_fertilizer`, `new_growth`, `pdc_id`, `status`, `transport_language`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.2.yaml) | `working-draft` | 144 | 97 | 49 | 15 | `rain`, `streams` |
| 3 | `0.3.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.3.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.3.yaml) | `working-draft` | 229 | 128 | 31 | 0 | `branch_shake`, `leaf_foliage`, `leaf_generation`, `leaf_types` |
| 4 | `0.4.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.4.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.4.yaml) | `working-draft` | 260 | 148 | 20 | 0 | `fertilizer` |
| 5 | `0.5.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.5.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.5.yaml) | `working-draft` | 309 | 186 | 40 | 2 | `leaf_state_phrase_interpretation`, `leaf_states`, `sturdy_leaf_recovery` |
| 6 | `0.6.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.6.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.6.yaml) | `working-draft` | 330 | 204 | 18 | 0 | `trusted_shed_litter` |
| 7 | `0.7.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.7.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.7.yaml) | `working-draft` | 353 | 218 | 14 | 0 | `mycelium` |
| 8 | `0.8.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.8.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.8.yaml) | `working-draft` | 383 | 244 | 26 | 0 | `canopy_leaf_behavior`, `non_fluid_communication` |
| 9 | `0.9.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.9.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.9.yaml) | `working-draft` | 448 | 283 | 39 | 0 | `canopy_recall_leaves`, `canopy_solid_material`, `sunlight_transfer` |
| 10 | `0.10.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.10.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.10.yaml) | `working-draft` | 519 | 310 | 27 | 0 | `leaf_provenance_directions`, `leaf_provenance_overlap` |
| 11 | `0.11.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.11.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.11.yaml) | `working-draft` | 553 | 318 | 16 | 8 | `moss` |
| 12 | `0.12.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.12.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.12.yaml) | `working-draft` | 587 | 332 | 14 | 0 | `sap_taps`, `solid_material`, `solid_material_model` |
| 13 | `0.13.0` | [FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.13-Logs.yaml](sandbox:/mnt/data/FOREST-INFORMATION-GROWTH-FLOW-Working-Draft-0.13-Logs.yaml) | `working-draft` | 598 | 341 | 9 | 0 | `logs` |

Latest family revision: `0.13.0` with 341 structural key paths.

### FOREST-LEAF-FOLIAGE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-LEAF-FOLIAGE-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-LEAF-FOLIAGE-Working-Draft-0.1.yaml) | `working-draft` | 48 | 26 | 26 | 0 | `canonical_path`, `foliage`, `leaf`, `pdc_id`, `protection`, `status`, `types`, `uuid`, `version`, `views` |
| 2 | `0.2.0` | [FOREST-LEAF-FOLIAGE-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-LEAF-FOLIAGE-Working-Draft-0.2.yaml) | `working-draft` | 76 | 48 | 23 | 1 | `state_change`, `states`, `sturdy_recovery_view` |
| 3 | `0.3.0` | [FOREST-LEAF-FOLIAGE-Working-Draft-0.3.yaml](sandbox:/mnt/data/FOREST-LEAF-FOLIAGE-Working-Draft-0.3.yaml) | `working-draft` | 87 | 54 | 6 | 0 | `released_sturdy_tracking` |
| 4 | `0.4.0` | [FOREST-LEAF-FOLIAGE-Working-Draft-0.4.yaml](sandbox:/mnt/data/FOREST-LEAF-FOLIAGE-Working-Draft-0.4.yaml) | `working-draft` | 109 | 64 | 10 | 0 | `filters`, `provenance_directions`, `provenance_overlap` |

Latest family revision: `0.4.0` with 64 structural key paths.

### FOREST-LEAF-PROVENANCE-DIRECTIONS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-LEAF-PROVENANCE-DIRECTIONS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-LEAF-PROVENANCE-DIRECTIONS-Working-Draft-0.1.yaml) | `working-draft` | 73 | 37 | 37 | 0 | `canonical_path`, `classification`, `directions`, `overlap`, `pdc_id`, `source_examples`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-LEAF-STATES

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-LEAF-STATES-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-LEAF-STATES-Working-Draft-0.1.yaml) | `working-draft` | 61 | 48 | 48 | 0 | `canonical_path`, `default_state`, `maple_syrup_copy`, `pdc_id`, `phrase_mapping`, `states`, `status`, `sturdy_recovery`, `transitions`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-LEAF-STATES-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-LEAF-STATES-Working-Draft-0.2.yaml) | `working-draft` | 83 | 62 | 14 | 0 | `trusted_shed_litter` |

Latest family revision: `0.2.0` with 62 structural key paths.

### FOREST-LOGS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-LOGS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-LOGS-Working-Draft-0.1.yaml) | `working-draft` | 72 | 37 | 37 | 0 | `canonical_path`, `definition`, `fireproof-recovery`, `oil`, `organization`, `pdc_id`, `record`, `status`, `tar`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-LOGS-Working-Draft-0.2-Tree-And-Cabin-Logs.yaml](sandbox:/mnt/data/FOREST-LOGS-Working-Draft-0.2-Tree-And-Cabin-Logs.yaml) | `working-draft` | 75 | 43 | 9 | 3 | `creation`, `forms`, `ordinary_file_opening_creates_log` |
| 3 | `0.3.0` | [FOREST-LOGS-Working-Draft-0.3-Potted-Tar.yaml](sandbox:/mnt/data/FOREST-LOGS-Working-Draft-0.3-Potted-Tar.yaml) | `working-draft` | 82 | 50 | 7 | 0 | `standard_encrypted_files` |

Latest family revision: `0.3.0` with 50 structural key paths.

### FOREST-MOSS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-MOSS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-MOSS-Working-Draft-0.1.yaml) | `working-draft` | 143 | 72 | 72 | 0 | `attachment`, `canonical_path`, `cookie_behavior`, `definition`, `growth_control`, `leaves`, `memory`, `oil`, `pdc_id`, `scraping`, `security`, `status`, `tar`, `types`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-MOSS-Working-Draft-0.2-Sap-Taps.yaml](sandbox:/mnt/data/FOREST-MOSS-Working-Draft-0.2-Sap-Taps.yaml) | `working-draft` | 148 | 80 | 8 | 0 | `management`, `sap_taps_controls` |

Latest family revision: `0.2.0` with 80 structural key paths.

### FOREST-MYCELIUM

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-MYCELIUM-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-MYCELIUM-Working-Draft-0.1.yaml) | `working-draft` | 95 | 50 | 50 | 0 | `access`, `canonical_path`, `definition`, `maple`, `pdc_id`, `roots`, `security`, `soil`, `status`, `trace_leaves`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-MYCELIUM-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-MYCELIUM-Working-Draft-0.2.yaml) | `working-draft` | 93 | 56 | 7 | 1 | `comparison_with_canopy` |
| 3 | `0.3.0` | [FOREST-MYCELIUM-Working-Draft-0.3.yaml](sandbox:/mnt/data/FOREST-MYCELIUM-Working-Draft-0.3.yaml) | `working-draft` | 98 | 61 | 5 | 0 | `classification` |

Latest family revision: `0.3.0` with 61 structural key paths.

### FOREST-PROPAGULE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-PROPAGULE-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-PROPAGULE-Working-Draft-0.1.yaml) | `working-draft` | 49 | 23 | 23 | 0 | `canonical_path`, `definition`, `forest_fire`, `may_preserve`, `must_not_preserve`, `pdc_id`, `planting`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-SOLID-MATERIAL-ACCESS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.1.yaml) | `working-draft` | 88 | 44 | 44 | 0 | `canonical_path`, `canopy_access`, `conversion`, `definition`, `examples`, `pdc_id`, `permissions`, `recall_leaf`, `status`, `uuid`, `version`, `view_context` |
| 2 | `0.2.0` | [FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.2-Moss.yaml](sandbox:/mnt/data/FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.2-Moss.yaml) | `working-draft` | 90 | 49 | 15 | 10 | `moss` |
| 3 | `0.3.0` | [FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.3.yaml](sandbox:/mnt/data/FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.3.yaml) | `working-draft` | 105 | 56 | 7 | 0 | `not_solid_material`, `tree_relationship` |
| 4 | `0.4.0` | [FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.4-Logs.yaml](sandbox:/mnt/data/FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.4-Logs.yaml) | `working-draft` | 114 | 63 | 7 | 0 | `logs` |
| 5 | `0.5.0` | [FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.5-Standard-Encrypted-Files.yaml](sandbox:/mnt/data/FOREST-SOLID-MATERIAL-ACCESS-Working-Draft-0.5-Standard-Encrypted-Files.yaml) | `working-draft` | 122 | 70 | 7 | 0 | `standard_encrypted_file` |

Latest family revision: `0.5.0` with 70 structural key paths.

### FOREST-SUNLIGHT

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-SUNLIGHT-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-SUNLIGHT-Working-Draft-0.1.yaml) | `working-draft` | 40 | 24 | 24 | 0 | `boundaries`, `canonical_path`, `definition`, `notes_as_sunlight`, `pdc_id`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-SUNLIGHT-Working-Draft-0.2.yaml](sandbox:/mnt/data/FOREST-SUNLIGHT-Working-Draft-0.2.yaml) | `working-draft` | 53 | 35 | 11 | 0 | `transfer` |

Latest family revision: `0.2.0` with 35 structural key paths.

### FOREST-TAP-CONTROLS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-TAP-CONTROLS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-TAP-CONTROLS-Working-Draft-0.1.yaml) | `working-draft` | 34 | 35 | 35 | 0 | `canonical_path`, `definition`, `pdc_id`, `states`, `status`, `status_fields`, `tap_types`, `uuid`, `version` |
| 2 | `0.2.0` | [FOREST-TAP-CONTROLS-Working-Draft-0.2-Spirit-Sap-Taps.yaml](sandbox:/mnt/data/FOREST-TAP-CONTROLS-Working-Draft-0.2-Spirit-Sap-Taps.yaml) | `working-draft` | 120 | 73 | 38 | 0 | `absorption_modes`, `absorption_scope_fields`, `canonical_name`, `component_type`, `managed_by`, `moss_gate`, `spirit_responsibilities`, `tar_management`, `user_is_final_authority`, `user_management` |

Latest family revision: `0.2.0` with 73 structural key paths.

### FOREST-THREAT-PROTECTIONS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-THREAT-PROTECTIONS-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-THREAT-PROTECTIONS-Working-Draft-0.1.yaml) | `working-draft` | 42 | 22 | 22 | 0 | `canonical_path`, `hackers`, `mold`, `pdc_id`, `principles`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### FOREST-TRUSTED-SHED-LITTER

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [FOREST-TRUSTED-SHED-LITTER-Working-Draft-0.1.yaml](sandbox:/mnt/data/FOREST-TRUSTED-SHED-LITTER-Working-Draft-0.1.yaml) | `working-draft` | 48 | 37 | 37 | 0 | `absorption`, `canonical_path`, `creation`, `integrity`, `maple`, `pdc_id`, `status`, `trust`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### LOG-CABIN-STANDARD-ENCRYPTION

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [LOG-CABIN-STANDARD-ENCRYPTION-Working-Draft-0.1.yaml](sandbox:/mnt/data/LOG-CABIN-STANDARD-ENCRYPTION-Working-Draft-0.1.yaml) | `working-draft` | 41 | 31 | 31 | 0 | `canonical_path`, `classification`, `commands`, `conversion`, `definition`, `pdc_id`, `security`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### MAPLE-LOCAL-SAFEGUARDS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-LOCAL-SAFEGUARDS-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-LOCAL-SAFEGUARDS-Working-Draft-0.1.yaml) | `working-draft` | 61 | 47 | 47 | 0 | `canonical_path`, `component_type`, `guarantees`, `owner_tree`, `pdc_id`, `role`, `security_status`, `status`, `uuid`, `version`, `with_cedar`, `without_cedar` |

This family currently has one preserved version, so no same-family delta is available.

### MAPLE-MOLASSES

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-MOLASSES-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-MOLASSES-Working-Draft-0.1.yaml) | `working-draft` | 52 | 42 | 42 | 0 | `assistance`, `binding`, `canonical_path`, `contents`, `fluid_type`, `high_risk_action`, `lifecycle`, `owner_tree`, `pdc_id`, `protection_grade`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [MAPLE-MOLASSES-Working-Draft-0.2.yaml](sandbox:/mnt/data/MAPLE-MOLASSES-Working-Draft-0.2.yaml) | `working-draft` | 58 | 54 | 12 | 0 | `cedar_relationship`, `standalone_maple_protection` |

Latest family revision: `0.2.0` with 54 structural key paths.

### MAPLE-NOTES-INTEGRATION

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-NOTES-INTEGRATION-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-NOTES-INTEGRATION-Working-Draft-0.1.yaml) | `working-draft` | 74 | 46 | 46 | 0 | `access_modes`, `canonical_path`, `classification`, `connectors`, `design`, `pdc_id`, `safety`, `status`, `syrup_and_preferences`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### MAPLE-PLUGIN-MOD-REGISTRY

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-PLUGIN-MOD-REGISTRY-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-PLUGIN-MOD-REGISTRY-Working-Draft-0.1.yaml) | `working-draft` | 110 | 93 | 93 | 0 | `canonical_path`, `entry_schema`, `organization`, `owner_tree`, `pdc_id`, `scope`, `status`, `suggestions`, `user_visible`, `uuid`, `version`, `warning_states` |

This family currently has one preserved version, so no same-family delta is available.

### MAPLE-PREFERENCE-PROFILE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-PREFERENCE-PROFILE-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-PREFERENCE-PROFILE-Working-Draft-0.1.yaml) | `working-draft` | 66 | 66 | 66 | 0 | `canonical_path`, `categories`, `examples`, `pdc_id`, `policy`, `record_schema`, `status`, `user_id`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### MAPLE-SETTINGS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-SETTINGS-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.1.yaml) | `working-draft` | 128 | 69 | 69 | 0 | `branches`, `canonical_path`, `forest_management`, `pdc_id`, `protected_data`, `role`, `status`, `syrup`, `uuid`, `version`, `workflow_observation` |
| 2 | `0.2.0` | [MAPLE-SETTINGS-Working-Draft-0.2.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.2.yaml) | `working-draft` | 498 | 377 | 308 | 0 | `cedar_approved_leaf_litter`, `data_permissions`, `elevated_workflow_permissions`, `leaf_litter_syrup_fuel`, `note_access`, `permission_profiles`, `preference_learning` |
| 3 | `0.3.0` | [MAPLE-SETTINGS-Working-Draft-0.3.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.3.yaml) | `working-draft` | 615 | 433 | 56 | 0 | `automatic_syrup_feeding`, `discarded_syrup_reabsorption`, `syrup_bucket` |
| 4 | `0.4.0` | [MAPLE-SETTINGS-Working-Draft-0.4.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.4.yaml) | `working-draft` | 765 | 489 | 56 | 0 | `plugin_mod_change_process`, `plugin_mod_inventory`, `plugin_mod_management_controls`, `plugin_mod_status_monitor`, `plugin_mod_suggestions` |
| 5 | `0.5.0` | [MAPLE-SETTINGS-Working-Draft-0.5-Syrup-Tap.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.5-Syrup-Tap.yaml) | `working-draft` | 810 | 508 | 19 | 0 | `syrup_tap` |
| 6 | `0.6.0` | [MAPLE-SETTINGS-Working-Draft-0.6-Molasses.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.6-Molasses.yaml) | `working-draft` | 856 | 545 | 37 | 0 | `molasses_controls`, `molasses_high_risk_actions`, `syrup_family` |
| 7 | `0.7.0` | [MAPLE-SETTINGS-Working-Draft-0.7-Local-Safeguards.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.7-Local-Safeguards.yaml) | `working-draft` | 923 | 602 | 57 | 0 | `local_safeguards`, `protection_modes`, `security_role`, `with_cedar`, `without_cedar` |
| 8 | `0.8.0` | [MAPLE-SETTINGS-Working-Draft-0.8-Grove-Orchestration.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.8-Grove-Orchestration.yaml) | `working-draft` | 1,050 | 648 | 46 | 0 | `branch_call`, `grove_board`, `grove_coordination`, `grove_failure_handling`, `grove_permissions`, `grove_plan` |
| 9 | `0.9.0` | [MAPLE-SETTINGS-Working-Draft-0.9-Fertilizer-Absorption.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-0.9-Fertilizer-Absorption.yaml) | `working-draft` | 1,086 | 676 | 28 | 0 | `absorbed_fertilizer_sources`, `fertilizer_absorption_record` |
| 10 | `1.0.0` | [MAPLE-SETTINGS-Working-Draft-1.0-Leaf-States.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.0-Leaf-States.yaml) | `working-draft` | 1,111 | 699 | 23 | 0 | `leaf_state_assistance`, `sturdy_leaf_syrup_fuel` |
| 11 | `1.1.0` | [MAPLE-SETTINGS-Working-Draft-1.1-Trusted-Shed-Litter.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.1-Trusted-Shed-Litter.yaml) | `working-draft` | 1,124 | 712 | 13 | 0 | `trusted_shed_litter` |
| 12 | `1.2.0` | [MAPLE-SETTINGS-Working-Draft-1.2-Mycelium-Automation.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.2-Mycelium-Automation.yaml) | `working-draft` | 1,170 | 738 | 26 | 0 | `mycelial_trace_leaves`, `mycelium_automation`, `mycelium_security` |
| 13 | `1.3.0` | [MAPLE-SETTINGS-Working-Draft-1.3-Canopy-Automation.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.3-Canopy-Automation.yaml) | `working-draft` | 1,214 | 769 | 31 | 0 | `automation_networks`, `canopy_automation` |
| 14 | `1.4.0` | [MAPLE-SETTINGS-Working-Draft-1.4-Canopy-Solid-Material.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.4-Canopy-Solid-Material.yaml) | `working-draft` | 1,289 | 798 | 29 | 0 | `canopy_material_access`, `canopy_recall_leaves` |
| 15 | `1.5.0` | [MAPLE-SETTINGS-Working-Draft-1.5-Moss.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.5-Moss.yaml) | `working-draft` | 1,321 | 814 | 30 | 14 | `moss_management` |
| 16 | `1.6.0` | [MAPLE-SETTINGS-Working-Draft-1.6-Sap-Taps.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.6-Sap-Taps.yaml) | `working-draft` | 1,349 | 821 | 7 | 0 | `sap_taps_interaction` |
| 17 | `1.7.0` | [MAPLE-SETTINGS-Working-Draft-1.7-Potted-Mode.yaml](sandbox:/mnt/data/MAPLE-SETTINGS-Working-Draft-1.7-Potted-Mode.yaml) | `working-draft` | 1,362 | 834 | 13 | 0 | `forest_fire_interaction`, `potted_mode` |

Latest family revision: `1.7.0` with 834 structural key paths.

### MAPLE-SYRUP-BUCKET

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [MAPLE-SYRUP-BUCKET-Working-Draft-0.1.yaml](sandbox:/mnt/data/MAPLE-SYRUP-BUCKET-Working-Draft-0.1.yaml) | `working-draft` | 78 | 61 | 61 | 0 | `bucket`, `canonical_path`, `item_schema`, `never_reabsorb`, `owner_tree`, `pdc_id`, `reabsorption`, `removal`, `status`, `user_visible`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### SPIRIT-FOREST-TREE-COMMAND-LIST

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.1.yaml) | `working-draft` | 725 | 14 | 14 | 0 | `canonical_path`, `command_count`, `generated_from`, `generation_rule`, `groups`, `pdc_id`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.2.yaml](sandbox:/mnt/data/SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.2.yaml) | `working-draft` | 829 | 16 | 2 | 0 | `includes` |
| 3 | `0.3.0` | [SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.3.yaml](sandbox:/mnt/data/SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.3.yaml) | `working-draft` | 902 | 16 | 0 | 0 | — |
| 4 | `0.4.0` | [SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.4.yaml](sandbox:/mnt/data/SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.4.yaml) | `working-draft` | 951 | 16 | 0 | 0 | — |
| 5 | `0.5.0` | [SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.5.yaml](sandbox:/mnt/data/SPIRIT-FOREST-TREE-COMMAND-LIST-Working-Draft-0.5.yaml) | `working-draft` | 983 | 16 | 0 | 0 | — |

Latest family revision: `0.5.0` with 16 structural key paths.

### SPIRIT-GOVERNANCE-COPIES

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-GOVERNANCE-COPIES-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-GOVERNANCE-COPIES-Working-Draft-0.1.yaml) | `working-draft` | 26 | 23 | 23 | 0 | `canonical_path`, `constitution_copy`, `pdc_id`, `principles_copy`, `status`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

### SPIRIT-LOCAL-FOREST-RECOVERY

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.1.yaml) | `working-draft` | 69 | 40 | 40 | 0 | `authority`, `availability`, `belongs_to`, `canonical_path`, `cedar_recovery`, `communicates_through`, `component_type`, `failure_escalation`, `logging`, `pdc_id`, `protected_operations`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.2-Sap-Taps.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.2-Sap-Taps.yaml) | `working-draft` | 82 | 51 | 11 | 0 | `sap_taps` |
| 3 | `0.3.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.3-Tools-Seed-Vault.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.3-Tools-Seed-Vault.yaml) | `working-draft` | 155 | 99 | 48 | 0 | `governance_copies`, `seed_vault`, `tools_menu` |
| 4 | `0.4.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.4-Forest-Fire-Potted-Mode.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.4-Forest-Fire-Potted-Mode.yaml) | `working-draft` | 203 | 129 | 30 | 0 | `forest_fire`, `potted_mode` |
| 5 | `0.5.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.5-Logs-Log-Cabin-CLI.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.5-Logs-Log-Cabin-CLI.yaml) | `working-draft` | 257 | 161 | 32 | 0 | `logs` |
| 6 | `0.6.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.6-Gardens-Log-Cabins.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.6-Gardens-Log-Cabins.yaml) | `working-draft` | 277 | 182 | 27 | 6 | `garden`, `log_cabin` |
| 7 | `0.7.0` | [SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.7-Cabin-Guard-Encryption.yaml](sandbox:/mnt/data/SPIRIT-LOCAL-FOREST-RECOVERY-Working-Draft-0.7-Cabin-Guard-Encryption.yaml) | `working-draft` | 296 | 201 | 19 | 0 | — |

Latest family revision: `0.7.0` with 201 structural key paths.

### SPIRIT-LOG-CABIN

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-LOG-CABIN-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-LOG-CABIN-Working-Draft-0.1.yaml) | `working-draft` | 63 | 30 | 30 | 0 | `canonical_path`, `component`, `fireproof-recovery`, `organization`, `pdc_id`, `protection`, `records`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-LOG-CABIN-Working-Draft-0.2-Cedar-Door.yaml](sandbox:/mnt/data/SPIRIT-LOG-CABIN-Working-Draft-0.2-Cedar-Door.yaml) | `working-draft` | 113 | 59 | 29 | 0 | `availability`, `cedar_door`, `recovery` |
| 3 | `0.3.0` | [SPIRIT-LOG-CABIN-Working-Draft-0.3-Potted-Cedar-Encryption.yaml](sandbox:/mnt/data/SPIRIT-LOG-CABIN-Working-Draft-0.3-Potted-Cedar-Encryption.yaml) | `working-draft` | 140 | 86 | 27 | 0 | `cabin_tap`, `standalone_access`, `standard_encryption` |

Latest family revision: `0.3.0` with 86 structural key paths.

### SPIRIT-SAP-TAPS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-SAP-TAPS-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-SAP-TAPS-Working-Draft-0.1.yaml) | `working-draft` | 96 | 59 | 59 | 0 | `absorption`, `authority`, `canonical_path`, `component`, `moss_gate`, `pdc_id`, `responsibilities`, `status`, `tap_types`, `tar`, `tree_interactions`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-SAP-TAPS-Working-Draft-0.2-Tools-Menu.yaml](sandbox:/mnt/data/SPIRIT-SAP-TAPS-Working-Draft-0.2-Tools-Menu.yaml) | `working-draft` | 97 | 65 | 6 | 0 | `tools_menu` |
| 3 | `0.3.0` | [SPIRIT-SAP-TAPS-Working-Draft-0.3-Log-Controls.yaml](sandbox:/mnt/data/SPIRIT-SAP-TAPS-Working-Draft-0.3-Log-Controls.yaml) | `working-draft` | 113 | 73 | 8 | 0 | `log_management` |
| 4 | `0.4.0` | [SPIRIT-SAP-TAPS-Working-Draft-0.4-Cabin-Tap.yaml](sandbox:/mnt/data/SPIRIT-SAP-TAPS-Working-Draft-0.4-Cabin-Tap.yaml) | `working-draft` | 127 | 87 | 14 | 0 | `cabin_tap`, `standard_encryption` |

Latest family revision: `0.4.0` with 87 structural key paths.

### SPIRIT-SEED-VAULT

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-SEED-VAULT-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-SEED-VAULT-Working-Draft-0.1.yaml) | `working-draft` | 79 | 43 | 43 | 0 | `access`, `canonical_path`, `component`, `contents`, `management`, `pdc_id`, `protection`, `recovery`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-SEED-VAULT-Working-Draft-0.2-Forest-Fire.yaml](sandbox:/mnt/data/SPIRIT-SEED-VAULT-Working-Draft-0.2-Forest-Fire.yaml) | `working-draft` | 83 | 50 | 7 | 0 | `forest_fire` |
| 3 | `0.3.0` | [SPIRIT-SEED-VAULT-Working-Draft-0.3-Inside-Log-Cabin.yaml](sandbox:/mnt/data/SPIRIT-SEED-VAULT-Working-Draft-0.3-Inside-Log-Cabin.yaml) | `working-draft` | 94 | 61 | 11 | 0 | `cabinless_mode`, `multiple_vaults` |

Latest family revision: `0.3.0` with 61 structural key paths.

### SPIRIT-TOOLS-MENU

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SPIRIT-TOOLS-MENU-Working-Draft-0.1.yaml](sandbox:/mnt/data/SPIRIT-TOOLS-MENU-Working-Draft-0.1.yaml) | `working-draft` | 41 | 26 | 26 | 0 | `canonical_path`, `command_list`, `component`, `governance`, `pdc_id`, `status`, `tools`, `uuid`, `version` |
| 2 | `0.2.0` | [SPIRIT-TOOLS-MENU-Working-Draft-0.2-Cedar-Emergency-Tools.yaml](sandbox:/mnt/data/SPIRIT-TOOLS-MENU-Working-Draft-0.2-Cedar-Emergency-Tools.yaml) | `working-draft` | 48 | 31 | 5 | 0 | `cedar_emergency_tools` |
| 3 | `0.3.0` | [SPIRIT-TOOLS-MENU-Working-Draft-0.3-Log-Cabin.yaml](sandbox:/mnt/data/SPIRIT-TOOLS-MENU-Working-Draft-0.3-Log-Cabin.yaml) | `working-draft` | 55 | 37 | 6 | 0 | `log_cabin` |
| 4 | `0.4.0` | [SPIRIT-TOOLS-MENU-Working-Draft-0.4-Cabin-Seed-Vault.yaml](sandbox:/mnt/data/SPIRIT-TOOLS-MENU-Working-Draft-0.4-Cabin-Seed-Vault.yaml) | `working-draft` | 55 | 38 | 4 | 3 | — |
| 5 | `0.5.0` | [SPIRIT-TOOLS-MENU-Working-Draft-0.5-Cabin-Guard.yaml](sandbox:/mnt/data/SPIRIT-TOOLS-MENU-Working-Draft-0.5-Cabin-Guard.yaml) | `working-draft` | 59 | 42 | 4 | 0 | — |

Latest family revision: `0.5.0` with 42 structural key paths.

### SYCAMORE-CONNECTION-SETTINGS

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.1.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.1.yaml) | `working-draft` | 43 | 36 | 36 | 0 | `canonical_path`, `connection_methods`, `pdc_id`, `security`, `selection`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.2.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.2.yaml) | `working-draft` | 65 | 57 | 21 | 0 | `fluids` |
| 3 | `0.3.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.3.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.3.yaml) | `working-draft` | 90 | 78 | 34 | 13 | — |
| 4 | `0.4.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.4.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.4.yaml) | `working-draft` | 146 | 117 | 39 | 0 | `tar_sap_emergency` |
| 5 | `0.5.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.5.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.5.yaml) | `working-draft` | 146 | 117 | 2 | 2 | — |
| 6 | `0.6.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.6-Tap-Enforcement.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.6-Tap-Enforcement.yaml) | `working-draft` | 134 | 123 | 6 | 0 | `tap_enforcement` |
| 7 | `0.7.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.7-Sap-Taps.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.7-Sap-Taps.yaml) | `working-draft` | 161 | 130 | 7 | 0 | `sap_taps_interaction` |
| 8 | `0.8.0` | [SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.8-No-Potted-Sycamore.yaml](sandbox:/mnt/data/SYCAMORE-CONNECTION-SETTINGS-Working-Draft-0.8-No-Potted-Sycamore.yaml) | `working-draft` | 169 | 138 | 8 | 0 | `garden_connectivity`, `potted_mode` |

Latest family revision: `0.8.0` with 138 structural key paths.

### TREE-FERTILIZER-FILE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [TREE-FERTILIZER-FILE-Working-Draft-0.1.yaml](sandbox:/mnt/data/TREE-FERTILIZER-FILE-Working-Draft-0.1.yaml) | `working-draft` | 69 | 70 | 70 | 0 | `application_policy`, `canonical_path`, `excluded_contents`, `file_type`, `growth_contents`, `identity`, `integrity`, `pdc_id`, `scope`, `status`, `uuid`, `version` |
| 2 | `0.2.0` | [TREE-FERTILIZER-FILE-Working-Draft-0.2.yaml](sandbox:/mnt/data/TREE-FERTILIZER-FILE-Working-Draft-0.2.yaml) | `working-draft` | 70 | 78 | 8 | 0 | `syrup_compatibility` |
| 3 | `0.3.0` | [TREE-FERTILIZER-FILE-Working-Draft-0.3.yaml](sandbox:/mnt/data/TREE-FERTILIZER-FILE-Working-Draft-0.3.yaml) | `working-draft` | 85 | 93 | 15 | 0 | `compatible_growth_sources`, `terminology` |

Latest family revision: `0.3.0` with 93 structural key paths.

### TREE-POTTED-MODE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [TREE-POTTED-MODE-Working-Draft-0.1.yaml](sandbox:/mnt/data/TREE-POTTED-MODE-Working-Draft-0.1.yaml) | `working-draft` | 44 | 35 | 35 | 0 | `canonical_path`, `definition`, `pdc_id`, `presence_lease`, `rescue_gate`, `status`, `trees`, `uuid`, `version` |
| 2 | `0.2.0` | [TREE-POTTED-MODE-Working-Draft-0.2-Gardens.yaml](sandbox:/mnt/data/TREE-POTTED-MODE-Working-Draft-0.2-Gardens.yaml) | `working-draft` | 58 | 47 | 12 | 0 | `garden` |
| 3 | `0.3.0` | [TREE-POTTED-MODE-Working-Draft-0.3-Cabin-Guard.yaml](sandbox:/mnt/data/TREE-POTTED-MODE-Working-Draft-0.3-Cabin-Guard.yaml) | `working-draft` | 70 | 59 | 12 | 0 | `cabin_tap` |

Latest family revision: `0.3.0` with 59 structural key paths.

### TREE-PROPAGATION-FILE

| Seq. | Version | Artifact | Status | Lines | Key paths | + paths | − paths | New top-level groups |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `0.1.0` | [TREE-PROPAGATION-FILE-Working-Draft-0.1.yaml](sandbox:/mnt/data/TREE-PROPAGATION-FILE-Working-Draft-0.1.yaml) | `working-draft` | 47 | 50 | 50 | 0 | `canonical_path`, `clone_and_recovery`, `excluded_contents`, `file_type`, `identity`, `integrity`, `pdc_id`, `status`, `structural_contents`, `tree_language_meaning`, `uuid`, `version` |

This family currently has one preserved version, so no same-family delta is available.

## Other supporting architecture, review, and specification files

These files are part of the preserved Forest history but are not primary Forest Language stages, audits, patches, or YAML component revisions.

| Artifact | Lines | Words | SHA-256 |
|---|---:|---:|---|
| [CEDAR-CONTAINMENT-ADDENDUM-Working-Draft-0.1.md](sandbox:/mnt/data/CEDAR-CONTAINMENT-ADDENDUM-Working-Draft-0.1.md) | 70 | 277 | `a676db7f3d759428…` |
| [FOREST-CONTAINMENT-SPEC-Working-Draft-0.1.md](sandbox:/mnt/data/FOREST-CONTAINMENT-SPEC-Working-Draft-0.1.md) | 116 | 522 | `b011b8652dcd68db…` |
| [FOREST-LANGUAGE-Draft-0.2-Correction-Map.md](sandbox:/mnt/data/FOREST-LANGUAGE-Draft-0.2-Correction-Map.md) | 32 | 197 | `9916c40bf6d19a07…` |
| [FOREST-MAP-SPEC-Working-Draft-0.1.md](sandbox:/mnt/data/FOREST-MAP-SPEC-Working-Draft-0.1.md) | 118 | 373 | `996d42fdb710239e…` |
| [PDC-Cedar-Oil-Review-Pack.md](sandbox:/mnt/data/PDC-Cedar-Oil-Review-Pack.md) | 2,437 | 10,663 | `cc5bbaf6dd09c9e2…` |
| [PDC-Cedar-Recovery-Review-Pack.md](sandbox:/mnt/data/PDC-Cedar-Recovery-Review-Pack.md) | 2,341 | 10,265 | `a1f2979f08c2f60e…` |
| [PDC-Containment-Disposal-Replanting-Review-Pack.md](sandbox:/mnt/data/PDC-Containment-Disposal-Replanting-Review-Pack.md) | 1,451 | 5,771 | `1e2ee5e8962d31fa…` |
| [PDC-Draft11-AUDIT-REPORT.md](sandbox:/mnt/data/PDC-Draft11-AUDIT-REPORT.md) | 107 | 738 | `0e0c7c2e99f2a63a…` |
| [PDC-Draft11-Reviewed-Optimized.sha256](sandbox:/mnt/data/PDC-Draft11-Reviewed-Optimized.sha256) | 1 | 2 | `6ef78b65c83edac3…` |
| [PDC-Draft11-VALIDATION-RESULT.txt](sandbox:/mnt/data/PDC-Draft11-VALIDATION-RESULT.txt) | 25 | 153 | `8eabe2b9261c4864…` |
| [PDC-Draft11-VERSION-COMPARISON.md](sandbox:/mnt/data/PDC-Draft11-VERSION-COMPARISON.md) | 50 | 497 | `acf019d67ccc6b94…` |
| [PDC-Forest-Compass-Map-Review-Pack.md](sandbox:/mnt/data/PDC-Forest-Compass-Map-Review-Pack.md) | 1,786 | 6,651 | `b5987b8bba8e97c7…` |
| [PDC-Security-Expansion-Review-Pack.md](sandbox:/mnt/data/PDC-Security-Expansion-Review-Pack.md) | 1,409 | 4,952 | `62e9504fccf37c26…` |
| [PDC-Template-Library-Draft11-Review-Pack.md](sandbox:/mnt/data/PDC-Template-Library-Draft11-Review-Pack.md) | 3,153 | 7,450 | `878a0ac1618079c8…` |
| [PDC-Voice-of-the-Forest-Review-Pack.md](sandbox:/mnt/data/PDC-Voice-of-the-Forest-Review-Pack.md) | 1,720 | 6,783 | `626cca3760b6ef81…` |
| [PDC-Voice-of-the-Forest-Unified-Review-Pack.md](sandbox:/mnt/data/PDC-Voice-of-the-Forest-Unified-Review-Pack.md) | 1,721 | 6,830 | `e7f4f10ed7ca7a8a…` |
| [PDC_Template_Pack_Draft11.md](sandbox:/mnt/data/PDC_Template_Pack_Draft11.md) | 3,175 | 7,598 | `8ce3ecf65e8f537b…` |
| [SPIRIT-CONSTITUTION-COPY-AWAITING-SOURCE.md](sandbox:/mnt/data/SPIRIT-CONSTITUTION-COPY-AWAITING-SOURCE.md) | 9 | 68 | `b8a0b17dd32570ce…` |
| [SPIRIT-PRINCIPLES-COPY-AWAITING-SOURCE.md](sandbox:/mnt/data/SPIRIT-PRINCIPLES-COPY-AWAITING-SOURCE.md) | 9 | 70 | `bff570026b9c768b…` |
| [VOICE-OF-THE-FOREST-SPEC-Working-Draft-0.2.md](sandbox:/mnt/data/VOICE-OF-THE-FOREST-SPEC-Working-Draft-0.2.md) | 147 | 504 | `a2840544fc9386b0…` |
| [VOICE-OF-THE-FOREST-SPEC-Working-Draft-0.3.md](sandbox:/mnt/data/VOICE-OF-THE-FOREST-SPEC-Working-Draft-0.3.md) | 142 | 510 | `c36cefee177905c2…` |

## Canonical evolution by architecture area

### Governance and deterministic control

- 0.7 introduced Spirit of the Forest as the guidance layer.
- 0.13.8 added Spirit recovery handoff.
- 0.13.13 introduced Taps.
- 0.13.30 moved Tap stewardship into deterministic Spirit Sap Taps and finalized the broad Solid Material boundary.
- 0.13.31 added the Spirit Tools menu, canonical command registry, governance-copy slots, and Seed Vault Tool.

### Tree roles

- Cherry remained the primary user-facing assistant and later gained Potted/Forest Fire CLI and Cherry Bonsai recovery roles.
- Maple grew from a technical/media Tree into the main workflow-learning, refinement, plugin, automation, Grove, Mycelium, Canopy, and Potted technical Tree.
- Cedar grew from security and Leaf Litter stewardship into Oil inspection, recovery, propagation, Tap locks, Forest Fire preparation, Log protection, Cedar Doors, and Potted Cabin Guard.
- Sycamore was added in 0.13.0 for Fluid routing and connection governance; later revisions added Tap enforcement and explicitly withheld Potted Sycamore.

### Information and learning lifecycle

- Early Bud → Blossom → Fruit language expanded to include Flowers and Golden Fruit.
- Leaf Foliage replaced the earlier Evidence Levels section.
- 0.13.14 formalized the Information Growth Cycle.
- 0.13.19–0.13.22 added provenance, Active Foliage, Branch Shake, Loose/normal/Sturdy Leaf states, and Trusted Shed Litter.
- 0.13.28 formalized User Input, User Output, Tree Input, and Tree Output Leaf directions.
- 0.13.29 introduced Moss as cookie-like Solid Material rather than ordinary Leaf Foliage.

### Fluids, protection, and refinement

- 0.13.0 introduced Fluids and Sap.
- 0.13.2 added Tar Sap.
- 0.13.3 added Water and Watering.
- 0.13.9 introduced Syrup; 0.13.11 added the Syrup Bucket.
- 0.13.15 separated delivery method, protection grade, and absorption depth.
- 0.13.16 added Light Syrup and Molasses.
- 0.13.30 consolidated access and protection under Spirit Sap Taps.

### Communication and cooperation

- 0.13.18 added Grove orchestration and Branch Calls.
- 0.13.25 defined Mycelium as deep local Tree communication.
- 0.13.26 defined Personal Canopy and the wider Forest Canopy.
- 0.13.27 added whole/piece Solid Material transfer and protected references.
- 0.13.34 added Gardens for limited cooperation among standalone Potted Trees.

### Storage and recovery

- Seeds and Seed Vault were present from the earliest preserved draft.
- 0.13.6–0.13.8 added Propagation, Fertilizer files, Spirit recovery, and Cherry fallback.
- 0.13.32 added Forest Fire, Potted Trees, Propagules, and Cherry Bonsai.
- 0.13.33 formalized Logs as Sap-bearing Solid Material, made Log Cabin a Spirit Tool, and added Forest Fire CLI entry.
- 0.13.34 moved Seed Vault inside dynamic Log Cabins and added Cedar Doors.
- 0.13.35 added Cedar Cabin Guard, Cabin Tap Tar protection, and Standard Encrypted Files.

## Supersession and status assessment

| Artifact group | Current comparison status |
|---|---|
| Draft 11 packages | Historical architecture/package snapshots; preserved unchanged |
| Forest Language 0.2–0.12 | Historical working drafts |
| Forest Language 0.12.1 | Reviewed baseline superseded by 0.13.x development |
| Forest Language 0.13.0–0.13.34 | Reviewed working drafts superseded by later 0.13 revisions |
| Forest Language 0.13.35 | Latest frozen reference; still declares Working Draft |
| YAML component files | Working architecture contracts; latest version in each family is the comparison reference, not an approved final release |

## Items still requiring finalization review

1. Decide whether the final document remains in the 0.13 series or receives a release number such as 1.0.0.
2. Change the approved artifact's `Status` only after human review and explicit approval.
3. Populate `Supersedes` and `Superseded-By` fields in the final canonical lineage, or document why Git history alone is authoritative.
4. Resolve any remaining metaphor-to-technical mappings before declaring the architecture final.
5. Confirm whether Spirit/Voice hierarchy wording is final and whether the Voice remains a named interface within the Spirit.
6. Confirm the final ownership boundaries among Spirit Sap Taps, Cedar, Sycamore, and the Action Broker planned for implementation.
7. Confirm whether every component contract remains a separate canonical file or is folded into fewer implementation specifications.
8. Run the final line-by-line review against 0.13.35 and this comparison before approving repository migration.

## Validation results

- Primary sequence contains **53** exact stages.
- Latest exact semantic version is **0.13.35**.
- Duplicate H2 headings found: **0**.
- YAML parsed for **144** component versions across **44** families.
- SHA-256 manifest contains **323** files.
- Source artifacts were read only.
- No repository migration, commit, push, version approval, or canonical finalization was performed.

## Finalization checklist update

✅ Build a complete version comparison

The remaining finalization tasks are unchanged and require the user's next review decisions.
