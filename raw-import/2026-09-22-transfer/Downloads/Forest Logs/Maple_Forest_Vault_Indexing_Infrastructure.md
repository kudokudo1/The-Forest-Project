---
title: "Maple Forest Vault Indexing Infrastructure"
aliases:
  - "Forest Index Watcher"
  - "Maple Knowledge Steward POC"
created: 2026-08-08
updated: 2026-08-08
type: implementation-notes
status: active-reference
project: The Forest
tree: Maple
tags:
  - the-forest
  - maple
  - obsidian
  - indexing
  - inotify
  - systemd
  - metadata
  - retrieval
---

# Maple Forest Vault Indexing Infrastructure

> [!important]
> This note preserves the code, context, troubleshooting history, current paths, and future upgrade plans for the first deterministic knowledge-management infrastructure built for Maple and The Forest.

## 1. Why This Exists

The goal was to prepare Maple for a future **knowledge steward / retrieval specialist** role before Maple AI itself exists.

Core idea:

> **Build the library before hiring the librarian.**

The current system:
- keeps the Obsidian vault human-readable and local,
- maintains note metadata,
- builds a derived JSON index,
- automatically refreshes that index whenever Markdown files change,
- uses deterministic code instead of an AI model for simple work,
- gives future Maple AI a fast knowledge layer to query,
- prevents every Tree from repeatedly scanning the entire vault.

This is an early implementation of:

> **Your Data. Your Trees. Your Forest.**

---

## 2. Current Architecture

```text
Obsidian note changes
        ↓
Linux inotify detects filesystem event
        ↓
forest_index_watch.sh reacts
        ↓
forest_index.py scans Markdown notes
        ↓
System/forest-index.json is regenerated
        ↓
future Maple AI / Cherry / Forest tools query the index
```

No AI model is required for this process.

The watcher is event-driven rather than polling, so it stays very lightweight while idle.

---

## 3. Current Maple / Obsidian Setup

### Qube
```text
Maple
```

Maple is an AppVM and currently serves as a heavily used personal/development workspace.

### Obsidian AppImage

```text
/home/user/Applications/Obsidian-1.13.4.AppImage
```

### User launcher

```text
/home/user/.local/bin/obsidian
```

Typical launcher:

```bash
#!/bin/bash
exec "$HOME/Applications/Obsidian-1.13.4.AppImage" --password-store=basic "$@"
```

`--password-store=basic` was used to avoid the GNOME Keyring unlock popup inside Maple.

### AppImage dependencies

Installed in Maple's Fedora TemplateVM:

```bash
sudo dnf install fuse-libs
sudo dnf install fuse
```

`fuse-libs` fixed:

```text
dlopen(): error loading libfuse.so.2
```

`fuse` fixed:

```text
fuse: failed to exec fusermount
```

### Numpad shortcut

Obsidian is launched from i3 using Num Lock OFF + Numpad 9.

Conceptual binding:

```text
bindsym --release KP_Prior exec --no-startup-id qvm-run Maple '/home/user/.local/bin/obsidian'
```

User-facing idea:

```text
Numpad 9: Look at Leaf Foliage
```

---

## 4. Current Vault Location

Actual Obsidian vault root:

```text
/home/user/Downloads/The Forest Project/The Forest Project
```

A major nested project directory currently exists under it:

```text
The-Forest-Project-zeta
```

> [!warning]
> The vault currently lives under `~/Downloads/`. This works, but it should probably be moved later to a more intentional permanent location such as:
>
> ```text
> /home/user/The-Forest
> ```
>
> If it is moved, all hardcoded paths in the scripts below must be updated.

---

## 5. Metadata Work Already Completed

Existing Markdown notes were scanned and basic YAML/frontmatter was added where missing.

Typical generated metadata:

```yaml
---
project: The Forest
status: active
created: 2026-08-08
updated: 2026-08-08
tags:
  - the-forest
---
```

Tree-specific notes also received:

```yaml
tree: Maple
```

or:

```yaml
tree: Cherry
```

etc.

### Important classification rule

Tree ownership is inferred from **folder location**, not from mentions in the note body.

Recognized mappings:

```text
bristlecone pine → Bristlecone Pine
cherry           → Cherry
maple            → Maple
cedar            → Cedar
sycamore         → Sycamore
```

This rule was adopted after a dry run showed that content-based inference incorrectly assigned general Forest notes to Bristlecone simply because they mentioned him.

General Forest-wide notes are allowed to have no `tree` property.

---

## 6. Current Index Script

File:

```text
/home/user/forest_index.py
```

Code:

```python
from pathlib import Path
import json

VAULT = Path("/home/user/Downloads/The Forest Project/The Forest Project")
OUTPUT = VAULT / "System" / "forest-index.json"

def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    raw = parts[1]
    data = {}
    current_list = None

    for line in raw.splitlines():
        if not line.strip():
            continue

        if line.startswith("  - ") and current_list:
            data.setdefault(current_list, []).append(line[4:].strip())
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if value:
                data[key] = value
                current_list = None
            else:
                data[key] = []
                current_list = key

    return data

records = []

for path in VAULT.rglob("*.md"):
    if "Templates" in path.parts:
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")
    meta = parse_frontmatter(text)

    records.append({
        "title": path.stem,
        "path": str(path.relative_to(VAULT)),
        "project": meta.get("project"),
        "tree": meta.get("tree"),
        "status": meta.get("status"),
        "tags": meta.get("tags", []),
        "created": meta.get("created"),
        "updated": meta.get("updated"),
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(records, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"Indexed {len(records)} notes")
print(f"Index written to: {OUTPUT}")
```

---

## 7. Current Index Output

File:

```text
/home/user/Downloads/The Forest Project/The Forest Project/System/forest-index.json
```

First confirmed successful run:

```text
Indexed 22 notes
```

The index currently stores:

```text
title
path
project
tree
status
tags
created
updated
```

Existing richer metadata is preserved rather than overwritten.

`null` values are acceptable and mean that a note does not currently contain that property.

---

## 8. Current Watcher Script

File:

```text
/home/user/forest_index_watch.sh
```

Code:

```bash
#!/bin/bash

VAULT="/home/user/Downloads/The Forest Project/The Forest Project"

python3 "$HOME/forest_index.py"

inotifywait \
  -m \
  -r \
  -e close_write,create,delete,move \
  --exclude 'forest-index\.json$' \
  "$VAULT" |
while read -r directory events filename
do
    case "$filename" in
        *.md)
            python3 "$HOME/forest_index.py"
            ;;
    esac
done
```

Make executable:

```bash
chmod +x ~/forest_index_watch.sh
```

Required Fedora package:

```bash
sudo dnf install inotify-tools
```

Because Maple is an AppVM, this belongs in Maple's Fedora TemplateVM.

---

## 9. Why `inotify` Was Chosen

Rejected design:

```text
every few seconds:
"did anything change?"
```

Preferred design:

```text
filesystem change
      ↓
kernel event
      ↓
watcher reacts
```

Benefits:
- negligible CPU use while idle,
- no unnecessary AI work,
- no repeated polling,
- immediate updates,
- good fit for an always-running Maple Qube.

Forest rule reinforced:

> **Do deterministic work with deterministic code whenever possible.**

---

## 10. systemd User Service

Service file:

```text
/home/user/.config/systemd/user/forest-index.service
```

Configuration:

```ini
[Unit]
Description=Forest Vault Index Watcher
After=default.target

[Service]
ExecStart=/home/user/forest_index_watch.sh
Restart=on-failure
RestartSec=2

[Install]
WantedBy=default.target
```

Commands used:

```bash
systemctl --user daemon-reload
systemctl --user enable --now forest-index.service
```

Status check:

```bash
systemctl --user status forest-index.service
```

Confirmed:

```text
Active: active (running)
Watches established.
```

Observed resource use was roughly:

```text
Memory: ~1 MB current
Peak: ~6.6 MB
CPU: negligible while idle
```

This is the first confirmed always-on Forest infrastructure component in Maple.

---

## 11. Useful Maintenance Commands

Check service:

```bash
systemctl --user status forest-index.service
```

Check whether it is active:

```bash
systemctl --user is-active forest-index.service
```

Restart:

```bash
systemctl --user restart forest-index.service
```

Stop:

```bash
systemctl --user stop forest-index.service
```

Start:

```bash
systemctl --user start forest-index.service
```

Disable automatic startup:

```bash
systemctl --user disable --now forest-index.service
```

Re-enable:

```bash
systemctl --user enable --now forest-index.service
```

Recent logs:

```bash
journalctl --user -u forest-index.service -n 100
```

Manual index rebuild:

```bash
python3 ~/forest_index.py
```

Inspect index:

```bash
head -40 "/home/user/Downloads/The Forest Project/The Forest Project/System/forest-index.json"
```

---

## 12. Known Weaknesses

### Hardcoded vault path

Both scripts currently hardcode:

```text
/home/user/Downloads/The Forest Project/The Forest Project
```

Future improvement:
- config file,
- environment variable,
- or automatic `.obsidian` vault discovery.

Possible config location:

```text
~/.config/the-forest/config.toml
```

Example:

```toml
vault = "/home/user/The-Forest"
```

### Full rebuild on every Markdown change

Current behavior:

```text
one .md file changes
        ↓
scan all .md files
        ↓
rewrite entire JSON index
```

This is fine for 22 notes but will eventually become inefficient.

Future:
- incremental updates,
- update only changed file,
- remove deleted entry,
- rename moved entry,
- migrate to SQLite.

### Simple YAML parser

Current parser only supports basic:
- `key: value`,
- simple YAML lists.

It does not fully support nested or advanced YAML.

Future upgrade:
- PyYAML or another real YAML parser.

### JSON does not scale as well as SQLite

JSON was chosen because it is:
- transparent,
- human-inspectable,
- easy to debug,
- sufficient for the POC.

A later Forest index should likely use SQLite, potentially with FTS5.

Markdown should remain the canonical source of truth.

SQLite should remain rebuildable derived data.

### No note-body search yet

Current index is metadata-only.

Possible progression:

1. filename + metadata search,
2. SQLite FTS5 full-text search,
3. semantic/vector retrieval,
4. Maple AI semantic interpretation.

Do not jump to embeddings unless simpler search proves insufficient.

### `updated:` does not auto-change yet

The watcher updates the index but does not rewrite note frontmatter.

A future metadata worker could update `updated:` automatically.

Care must be taken to avoid an event loop where updating the metadata triggers another update endlessly.

### Multiple filesystem events

Some editors may generate multiple events for a single save.

Future improvement:
- debounce events,
- collapse duplicate events,
- update only the affected record.

---

## 13. Future Maple AI Role

Maple AI has **not yet been built**.

This system is intended to become Maple's knowledge-management substrate.

Future Maple responsibilities may include:
- querying the index,
- organizing incoming notes,
- locating relevant Leaves,
- maintaining links/backlinks,
- classifying notes,
- finding duplicates,
- distinguishing current vs superseded information,
- assembling compact context packets,
- serving Cherry and other Trees,
- maintaining metadata,
- identifying training candidates,
- tracking frequently requested knowledge,
- helping maintain Cherry's local fallback cache.

Important:

> **Maple AI should not be invoked for deterministic lookups.**

Example:

```text
"Open ADR-0007"
→ deterministic lookup
```

But:

```text
"Find every decision that conflicts with moving Cherry memory to the NAS."
→ Maple AI semantic reasoning
```

---

## 14. Planned Maple Two-Layer Architecture

```text
             MAPLE
        ┌──────────────┐
        │ Fast Layer   │
        │              │
        │ exact lookup │
        │ metadata     │
        │ tags         │
        │ index search │
        │ backlinks    │
        └──────┬───────┘
               │
       complex request?
               │
               ▼
        ┌──────────────┐
        │ Maple AI     │
        │              │
        │ interpretation
        │ organization
        │ summarization
        │ relationship
        │ context build
        └──────────────┘
```

Core rule:

> **Do not wake the model when ordinary code can answer the request.**

---

## 15. Planned `forest-search`

Next deterministic utility:

```bash
forest-search bristlecone
```

Possible future queries:

```bash
forest-search --tree Maple
forest-search --tag qubes
forest-search --status active-reference
forest-search --project "The Forest"
forest-search "Bristlecone benchmark"
```

Future Maple AI should call the same search layer rather than inventing a separate retrieval mechanism.

---

## 16. Planned qrexec Integration

Other Trees should eventually request Forest knowledge through controlled qrexec services.

Possible services:

```text
forest.find
forest.read
forest.search
forest.context
forest.message
forest.status
```

Target flow:

```text
Cherry
   ↓
qrexec
   ↓
Maple fast retrieval
   ↓
Forest index
   ↓
matching notes
   ↓
optional Maple AI context package
   ↓
Cherry
```

Cherry should retain local fallback retrieval so Maple does not become a single point of failure.

---

## 17. Planned Canopy Integration

Future Trees, especially Cherry, should know Maple's broad live state before sending requests.

Potential states:

```text
online
idle
busy
overloaded
accepting requests
not accepting requests
indexing
training
offline
```

Example:

```text
Maple busy
Cherry has enough local knowledge
→ Cherry retrieves locally instead
```

This avoids needless queue waits.

---

## 18. Planned Spirit of the Forest Integration

Spirit should eventually expose this deterministic service without requiring Maple AI.

Possible display:

```text
Forest Knowledge Index
● Healthy

Vault: The Forest Project
Notes indexed: 22
Watcher: Active
Index type: JSON
Maple AI: Not Installed
```

Expert diagnostics could later show:
- PID,
- CPU,
- memory,
- last event,
- last indexed file,
- rebuild time,
- errors,
- queue state.

This fits the Spirit/Voice principle:

> **The control plane should work even on a toaster.**

---

## 19. Future Retrieval Hierarchy

Target:

```text
Immediate model context
        ↓
Tree local curated cache
        ↓
Maple fast index
        ↓
Canonical Markdown vault
        ↓
Long-term Log Cabin / archive
```

Smaller layers are faster.

Larger layers contain more information.

Maple eventually helps decide what belongs at each level.

---

## 20. Recommended Upgrade Order

1. Build `forest-search`.
2. Move the vault out of `Downloads`.
3. Replace hardcoded paths with a config file.
4. Add safe automatic `updated:` maintenance.
5. Add incremental indexing.
6. Consider SQLite.
7. Add full-text search.
8. Add access counters / frequently used Leaves.
9. Build Maple AI.
10. Connect Maple AI to deterministic search.
11. Add qrexec retrieval.
12. Add Cherry local cache.
13. Add Canopy status integration.
14. Add Spirit diagnostics.
15. Add semantic retrieval only if needed.

---

## 21. Current State Summary

As of 2026-08-08:

```text
Obsidian: installed and working in Maple
Vault: working
Templates: configured
Metadata: added to existing notes
Index script: working
Indexed notes: 22
inotify watcher: working
systemd user service: active
Automatic index updates: confirmed
Maple AI: not built yet
Cherry qrexec access: not built yet
forest-search: next planned step
```

---

## 22. Important Files

```text
/home/user/forest_index.py
/home/user/forest_index_watch.sh
/home/user/.config/systemd/user/forest-index.service
/home/user/Downloads/The Forest Project/The Forest Project/System/forest-index.json
/home/user/Applications/Obsidian-1.13.4.AppImage
/home/user/.local/bin/obsidian
```

---

## 23. If the Vault Moves

Update:

```python
VAULT = Path(...)
```

inside:

```text
~/forest_index.py
```

Update:

```bash
VAULT="..."
```

inside:

```text
~/forest_index_watch.sh
```

Then:

```bash
systemctl --user restart forest-index.service
```

Verify:

```bash
systemctl --user status forest-index.service
python3 ~/forest_index.py
```

---

## 24. Why This Matters for The Forest

This is not merely an Obsidian convenience script.

It is an early implementation of:

- local human-readable Leaf Foliage,
- deterministic Forest infrastructure,
- event-driven knowledge updates,
- derived fast retrieval,
- future Maple knowledge stewardship,
- future Tree-to-Tree retrieval,
- separation of deterministic infrastructure from AI reasoning,
- observability-ready services,
- local-first knowledge ownership.

It should evolve rather than be discarded.

---

# End

**Your Data. Your Trees. Your Forest.**
