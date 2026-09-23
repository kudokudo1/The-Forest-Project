from __future__ import annotations

from pathlib import Path
from collections import defaultdict, Counter
import csv
import hashlib
import json


REPO = Path.home() / "Projects" / "The-Forest-Project"

ROOT = (
    REPO
    / "raw-import"
    / "2026-09-22-transfer"
    / "The-Forest"
    / "bristlecone"
)

OUT = REPO / "recovery" / "bristlecone"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def classify(rel: Path) -> str:
    parts = rel.parts
    text = str(rel)
    suffix = rel.suffix.lower()

    if "__pycache__" in parts or suffix == ".pyc":
        return "GENERATED_CACHE"

    if parts and parts[0] == "backups":
        if "certified" in text.lower():
            return "CERTIFIED_BACKUP"
        return "HISTORICAL_BACKUP"

    if parts and parts[0] == "certification":
        return "CERTIFICATION"

    if parts and parts[0] == "tests":
        return "TEST"

    if parts and parts[0] == "benchmarks":
        if suffix == ".py":
            return "BENCHMARK_TOOL"
        return "BENCHMARK_EVIDENCE"

    if parts and parts[0] == "logs":
        return "RUNTIME_LOG"

    if parts and parts[0] == "state":
        return "RUNTIME_STATE"

    if parts and parts[0] == "corpus":
        return "CORPUS"

    if suffix == ".py":
        return "CURRENT_SOURCE"

    if suffix in {".yaml", ".yml", ".json"}:
        return "CURRENT_CONFIG"

    if suffix == ".sh":
        return "CURRENT_SCRIPT"

    if parts and parts[0] == "bin":
        return "CURRENT_SCRIPT"

    if suffix in {".md", ".txt"}:
        return "CURRENT_DOCUMENTATION"

    return "CURRENT_OTHER"


files = []

for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
    rel = path.relative_to(ROOT)
    digest = sha256(path)

    files.append(
        {
            "path": str(rel),
            "absolute_path": str(path),
            "sha256": digest,
            "size": path.stat().st_size,
            "extension": path.suffix.lower(),
            "category": classify(rel),
        }
    )


by_sha = defaultdict(list)

for record in files:
    by_sha[record["sha256"]].append(record)


# ---------------------------------------------------------
# Complete Bristlecone inventory
# ---------------------------------------------------------

all_path = OUT / "ALL-FILES.tsv"

with all_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path",
            "category",
            "size",
            "extension",
            "sha256",
        ],
        delimiter="\t",
    )

    writer.writeheader()

    for record in files:
        writer.writerow(
            {
                "path": record["path"],
                "category": record["category"],
                "size": record["size"],
                "extension": record["extension"],
                "sha256": record["sha256"],
            }
        )


# ---------------------------------------------------------
# Current candidates
# ---------------------------------------------------------

current_categories = {
    "CURRENT_SOURCE",
    "CURRENT_CONFIG",
    "CURRENT_SCRIPT",
    "CURRENT_DOCUMENTATION",
    "CURRENT_OTHER",
    "CORPUS",
}

current = [
    r
    for r in files
    if r["category"] in current_categories
]


current_path = OUT / "CURRENT-CANDIDATES.tsv"

with current_path.open("w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")

    writer.writerow(
        [
            "path",
            "category",
            "size",
            "sha256",
            "exact_match_count",
            "certified_match_count",
            "historical_match_count",
        ]
    )

    for record in current:
        matches = [
            x
            for x in by_sha[record["sha256"]]
            if x["path"] != record["path"]
        ]

        certified = [
            x
            for x in matches
            if x["category"] == "CERTIFIED_BACKUP"
        ]

        historical = [
            x
            for x in matches
            if x["category"] == "HISTORICAL_BACKUP"
        ]

        writer.writerow(
            [
                record["path"],
                record["category"],
                record["size"],
                record["sha256"],
                len(matches),
                len(certified),
                len(historical),
            ]
        )


# ---------------------------------------------------------
# Current Python source → certified/historical exact matches
# ---------------------------------------------------------

current_python = [
    r
    for r in files
    if r["category"] == "CURRENT_SOURCE"
]

match_path = OUT / "CURRENT-PYTHON-MATCHES.tsv"

with match_path.open("w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")

    writer.writerow(
        [
            "current_path",
            "sha256",
            "size",
            "certified_matches",
            "historical_matches",
            "other_exact_matches",
        ]
    )

    for record in current_python:
        matches = [
            x
            for x in by_sha[record["sha256"]]
            if x["path"] != record["path"]
        ]

        certified = sorted(
            x["path"]
            for x in matches
            if x["category"] == "CERTIFIED_BACKUP"
        )

        historical = sorted(
            x["path"]
            for x in matches
            if x["category"] == "HISTORICAL_BACKUP"
        )

        other = sorted(
            x["path"]
            for x in matches
            if x["category"]
            not in {
                "CERTIFIED_BACKUP",
                "HISTORICAL_BACKUP",
            }
        )

        writer.writerow(
            [
                record["path"],
                record["sha256"],
                record["size"],
                json.dumps(certified),
                json.dumps(historical),
                json.dumps(other),
            ]
        )


# ---------------------------------------------------------
# Current source without a certified exact match
# ---------------------------------------------------------

unmatched = []

for record in current_python:
    matches = [
        x
        for x in by_sha[record["sha256"]]
        if x["path"] != record["path"]
    ]

    certified = [
        x
        for x in matches
        if x["category"] == "CERTIFIED_BACKUP"
    ]

    if not certified:
        unmatched.append(record)


unmatched_path = OUT / "CURRENT-PYTHON-WITHOUT-CERTIFIED-MATCH.tsv"

with unmatched_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path",
            "size",
            "sha256",
        ],
        delimiter="\t",
    )

    writer.writeheader()

    for record in unmatched:
        writer.writerow(
            {
                "path": record["path"],
                "size": record["size"],
                "sha256": record["sha256"],
            }
        )


# ---------------------------------------------------------
# Certified backup inventory
# ---------------------------------------------------------

certified = [
    r
    for r in files
    if r["category"] == "CERTIFIED_BACKUP"
]

certified_path = OUT / "CERTIFIED-BACKUP-FILES.tsv"

with certified_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path",
            "size",
            "extension",
            "sha256",
        ],
        delimiter="\t",
    )

    writer.writeheader()

    for record in certified:
        writer.writerow(
            {
                "path": record["path"],
                "size": record["size"],
                "extension": record["extension"],
                "sha256": record["sha256"],
            }
        )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

categories = Counter(
    record["category"]
    for record in files
)

python_with_certified = 0

for record in current_python:
    matches = [
        x
        for x in by_sha[record["sha256"]]
        if x["path"] != record["path"]
    ]

    if any(
        x["category"] == "CERTIFIED_BACKUP"
        for x in matches
    ):
        python_with_certified += 1


python_without_certified = (
    len(current_python)
    - python_with_certified
)

coverage = (
    (python_with_certified / len(current_python)) * 100
    if current_python
    else 0.0
)

category_lines = "\n".join(
    f"- {category}: {count}"
    for category, count in sorted(categories.items())
)

summary_text = f"""# Bristlecone Recovery Reconciliation

Source:

`raw-import/2026-09-22-transfer/The-Forest/bristlecone/`

This inventory is descriptive recovery evidence.

It does **not** declare any surviving source file canonical.

## Mechanical inventory

- Total recovered Bristlecone files: {len(files)}
- Total recovered Bristlecone bytes: {sum(r["size"] for r in files):,}

## Current Python implementation

The `CURRENT_SOURCE` classification excludes benchmark tools, tests,
certification tooling, backup snapshots, and generated Python caches.

- Current production Python files: {len(current_python)}
- Current production Python bytes: {sum(r["size"] for r in current_python):,}
- Exact certified-match files: {python_with_certified}
- Files without an exact certified match: {python_without_certified}
- Exact-certified coverage: {coverage:.1f}%

## Recovered file categories

{category_lines}

## What an exact certified match means

A current production file with the same SHA-256 as a file preserved in a
certified backup is strong evidence that the current file existed unchanged
at that certified engineering checkpoint.

This is stronger than relying on:

- filenames,
- modification-looking timestamps,
- words such as `final` or `master`,
- narrative checkpoint descriptions,
- or the current filesystem location alone.

## What a missing certified match means

A current file without an exact certified-backup match is **not**
automatically invalid, unfinished, or newer than the certified system.

It means only that exact-content certification has not yet been established
by this mechanical comparison.

Those files require additional reconciliation using:

- engineering chronology,
- checkpoint documents,
- tests,
- manifests and hashes,
- benchmark evidence,
- architecture records,
- dependencies and imports,
- and surrounding certified source.

## Current recovery interpretation

The surviving Bristlecone tree contains both directly certified production
source and source whose authority must be established through broader
evidence.

The reconciliation process therefore separates:

1. files with direct exact-content certification evidence;
2. files requiring contextual reconciliation;
3. certification and benchmark evidence;
4. historical backups;
5. generated/runtime material.

No material is promoted to the clean canonical `bristlecone/` tree solely
because it currently lives at the top level of the recovered Bristlecone
directory.

## Preservation rule

`raw-import/2026-09-22-transfer/` is the frozen archaeological source.

This inventory may read and hash that material, but must not rename, move,
deduplicate, rewrite, or delete it.
"""

summary = OUT / "SUMMARY.md"
summary.write_text(
    summary_text,
    encoding="utf-8",
)

print(f"Wrote {all_path}")
print(f"Wrote {current_path}")
print(f"Wrote {match_path}")
print(f"Wrote {unmatched_path}")
print(f"Wrote {certified_path}")
print(f"Wrote {summary}")
