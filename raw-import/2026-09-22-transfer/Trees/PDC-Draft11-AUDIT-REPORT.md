# PDC Draft 11 Review and Optimization Report

## Review Scope

Reviewed the current Forest Language through 0.12, all available earlier Forest Language drafts, the template library, security and containment specifications, Cedar settings, Tree manifests, schemas, indexes, apply/review scripts, and the Forest Map generator.

No live repository was changed.

## Correctness Fixes

- Removed the duplicate `Flower Access` heading.
- Corrected the Voice/Compass heading hierarchy and regenerated a structurally correct Forest Map.
- Rewrote the map renderer so top-level H2 and later H1 sections are represented correctly, with proper branch connectors.
- Corrected the Forest Compass description so it no longer claims to precede the Spirit and Voice.
- Fixed the identical correct/incorrect examples in `FOREST-COMPASS.md`.
- Matched the FOREST-MAP-SPEC title in metadata and the document heading.
- Corrected the universal-record schema from `Author` to the established `Authors` and added the established Custodian fields.
- Replaced placeholder metadata in actual specifications and Forest design records with real canonical Paths, dates, titles, and UUIDs; templates retain placeholders intentionally.
- Normalized Cedar, Cherry, and Maple manifests to one Tree schema.
- Corrected the Cedar settings key `block_when_cedar_failed_or-regrew` to `block_when_cedar_failed_or_regrew`.
- Removed unapproved fixed spoilage and retention durations while preserving configurable defaults and user overrides.

## Restored Safeguards

The 0.12 Leaf Litter rewrite had unintentionally dropped details from 0.11. Restored:

- Required origin and authorization metadata
- Definitions for every safety state
- Machine-readable Leaf Litter state example
- Blocked-transfer warning and logging behavior
- Detailed absorption and transfer history
- Top-of-pile recovery markers
- Early-destruction evidence preservation
- Cedar's metadata-first Leaf Litter duties
- Absorbed Fruit recovery sources
- Quarantined evidence-snapshot restrictions
- Cedar message-mode meanings
- Cross-Tree history privacy limits
- Minimum safe evidence before destruction

## Organization and Separation

- Forest Language remains the canonical vocabulary and natural-language command source.
- Voice handles commands, Paths, and user-authorized inter-Tree requests.
- Streams carry authorized data.
- Canopy carries health, reachability, warnings, and security status, not private content.
- Cedar handles Leaf Litter screening, safety attestations, and safe derivatives.
- FOREST-CONTAINMENT-SPEC defines the general response ladder.
- CEDAR-CONTAINMENT-ADDENDUM contains only Cedar-specific recovery application.
- Cedar runtime defaults and toggles remain in CEDAR-SETTINGS.yaml.

## Tree Communication Optimization

- Cherry, Maple, and Cedar now use the same manifest structure.
- All three declare the Voice, Canopy, Streams, peer IDs, and request logging.
- Cherry and Maple route Leaf Litter requests to Cedar.
- The Voice records the source Tree, target Tree, user authorization, request purpose, and result.
- Cedar's unfinished safety attestations are invalidated after Cedar regrows.
- Canopy reports about Cedar reach the user but do not let a peer Tree trigger Cedar's reset.

## Code Optimization

### Forest Map updater

- Correct nested-tree rendering
- Frontmatter and code-fence awareness
- Heading-skip validation
- Exactly-one marker-pair validation
- Atomic writes
- `--check` mode for validation and automation
- No rewrite when the map is already current
- Preserves the original file permission mode during atomic replacement

### Apply script

- Validates before doing anything
- Defaults to dry-run
- Uses deterministic sorted traversal
- Backs up replaced documents into Leaf Litter
- Stages stateful manifests and indexes instead of activating them
- Avoids overwriting an existing candidate by adding a timestamp

### Review script

- Reviews every target file, not only templates
- Shows new files clearly and in full
- Falls back to `diff` when Git is unavailable
- Stops clearly when a target repository is missing
- Uses one-file-at-a-time diffs to keep results traceable

## Necessary Redundancy Retained

The Voice remains the canonical command index. Command examples are also retained beside their vocabulary definitions because they explain local meaning. This is intentional documentation redundancy, and the validator checks required behavior so the two locations do not silently diverge.

## Not Activated or Invented

- No live repository changes were made.
- No new Forest metaphor or Tree role was introduced.
- Obsidian and future AI note-tool access remain inactive until permission is granted.
- Stones and Fungi distinct from Mycelium remain unresolved.
- Mycelium, Rain, and Sunlight remain working definitions.
- Fruit spoilage, Leaf Litter retention, and Cedar survival-observation durations remain configurable rather than assigned invented numeric values.
- Cherry and Maple Grain traits remain placeholders because the user has not finalized those exact traits.

## Validation Result

See `VALIDATION-RESULT.txt`. The final package passes YAML, JSON, Python, shell, Markdown hierarchy, Forest Map, Tree schema, required behavior, and requested-order checks.
