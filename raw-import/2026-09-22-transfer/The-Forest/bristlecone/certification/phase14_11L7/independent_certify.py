from __future__ import annotations

import hashlib
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/home/user/The-Forest/bristlecone")

A_ARCHIVE = (
    ROOT
    / "backups"
    / "phase14_11L7_A_surface_certified_20260813T000538Z"
)

EXPECTED_A_MANIFEST_SHA = (
    "990cc2cab7a223a737d20ca454e47ad739b9ae9a2efe577d074e03b2fa3cfcbc"
)

EXPECTED_HARNESS_SHA = (
    "4ba7d460167269851b9c9d1f6ac966c9228b59d189b76f6178b63b57758cdedb"
)

EXPECTED_SUMMARY_SHA = (
    "a388736294fe4c24caed7f0aeeb2b875481b39ab65508692240ef3aac6cfa418"
)

EXPECTED_ACTIVE_SHA = (
    "6b8fb9b44757917c1889a7368d43f393165080d248cdb3d9c5982aad53b270e5"
)

MODEL = "bristlecone-qwen35:4b-64k"

SURFACES = {
    "a": {
        "ready": [],
        "temporary_toolsets": [],
        "runtime_skills": [],
        "toolsets_during": [
            "file",
            "terminal",
        ],
        "overlay_bytes": 0,
    },
    "b": {
        "ready": [
            "code-execution",
        ],
        "temporary_toolsets": [
            "code_execution",
        ],
        "runtime_skills": [],
        "toolsets_during": [
            "code_execution",
            "file",
            "terminal",
        ],
        "overlay_bytes": 0,
    },
    "c": {
        "ready": [
            "debugging",
        ],
        "temporary_toolsets": [],
        "runtime_skills": [
            "systematic-debugging",
        ],
        "toolsets_during": [
            "file",
            "terminal",
        ],
        "overlay_bytes": 14554,
    },
    "d": {
        "ready": [
            "code-execution",
            "debugging",
            "testing",
        ],
        "temporary_toolsets": [
            "code_execution",
        ],
        "runtime_skills": [
            "systematic-debugging",
            "test-driven-development",
        ],
        "toolsets_during": [
            "code_execution",
            "file",
            "terminal",
        ],
        "overlay_bytes": 25357,
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def same_members(actual, expected) -> bool:
    return sorted(actual) == sorted(expected)


def close(actual, expected) -> bool:
    return math.isclose(
        actual,
        expected,
        rel_tol=0.0,
        abs_tol=1e-9,
    )


def metric_stats(values):
    return {
        "count": len(values),
        "median_s": statistics.median(values),
        "mean_s": statistics.mean(values),
        "stdev_s": statistics.stdev(values),
        "min_s": min(values),
        "max_s": max(values),
    }


print("=== PHASE 14.11L.7 B INDEPENDENT CERTIFIER ===")
print()

require(
    A_ARCHIVE.is_dir(),
    f"A archive missing: {A_ARCHIVE}",
)

manifest = A_ARCHIVE / "SHA256SUMS.txt"

require(
    manifest.exists(),
    "A archive manifest missing",
)

manifest_sha = sha(manifest)

require(
    manifest_sha == EXPECTED_A_MANIFEST_SHA,
    "A archive manifest SHA does not match frozen value",
)

print("PASS A archive manifest SHA")
print(manifest_sha)


# ------------------------------------------------------------
# VERIFY EVERY FILE LISTED IN A MANIFEST
# ------------------------------------------------------------

manifest_entries = {}

for raw_line in manifest.read_text().splitlines():
    line = raw_line.strip()

    if not line:
        continue

    digest, name = line.split(maxsplit=1)

    name = name.strip()

    if name.startswith("*"):
        name = name[1:]

    if name.startswith("./"):
        name = name[2:]

    require(
        name not in manifest_entries,
        f"Duplicate manifest entry: {name}",
    )

    manifest_entries[name] = digest


expected_files = {
    "CERTIFICATION.txt",
    "l7_surface_summary.json",
    "certification/analyze_surface.py",
    "certification/surface_trial.py",
}

for trial in range(1, 6):
    for surface in ("a", "b", "c", "d"):
        expected_files.add(
            f"raw/l7_surface_{surface}_trial{trial}_raw.json"
        )


require(
    set(manifest_entries) == expected_files,
    (
        "A manifest file set differs from expected L.7 bundle.\n"
        f"Expected: {len(expected_files)}\n"
        f"Manifest: {len(manifest_entries)}"
    ),
)


for name, expected_digest in sorted(
    manifest_entries.items()
):
    path = A_ARCHIVE / name

    require(
        path.exists(),
        f"Manifest file missing: {name}",
    )

    actual_digest = sha(path)

    require(
        actual_digest == expected_digest,
        f"Manifest mismatch: {name}",
    )


print(
    f"PASS manifest contents: "
    f"{len(manifest_entries)} / {len(expected_files)} files"
)


# ------------------------------------------------------------
# FROZEN HARNESS + SUMMARY
# ------------------------------------------------------------

harness = (
    A_ARCHIVE
    / "certification"
    / "surface_trial.py"
)

summary_path = (
    A_ARCHIVE
    / "l7_surface_summary.json"
)

require(
    sha(harness) == EXPECTED_HARNESS_SHA,
    "Frozen L.7 harness SHA mismatch",
)

require(
    sha(summary_path) == EXPECTED_SUMMARY_SHA,
    "Frozen L.7 summary SHA mismatch",
)

print("PASS frozen harness SHA")
print("PASS frozen summary SHA")


summary = json.loads(
    summary_path.read_text()
)


# ------------------------------------------------------------
# INDEPENDENT RAW ARTIFACT VALIDATION
# ------------------------------------------------------------

records = {}

seen_tasks = set()
seen_contexts = set()
seen_sessions = set()

raw_hashes = {}

common_message = None


for trial in range(1, 6):
    for surface in ("a", "b", "c", "d"):
        label = f"{surface.upper()}{trial}"

        path = (
            A_ARCHIVE
            / "raw"
            / f"l7_surface_{surface}_trial{trial}_raw.json"
        )

        data = json.loads(
            path.read_text()
        )

        raw_hashes[path.name] = sha(path)

        spec = SURFACES[surface]

        require(
            data["surface"] == surface,
            f"{label}: surface mismatch",
        )

        require(
            data["trial"] == trial,
            f"{label}: trial mismatch",
        )

        require(
            data["status"] == "success",
            f"{label}: status not success",
        )

        require(
            data["workshop"] == "code-debug",
            f"{label}: wrong Workshop",
        )

        require(
            data["model_form"] == "small",
            f"{label}: not Small",
        )

        require(
            data["binding_id"] == "binding-0001",
            f"{label}: wrong binding",
        )

        require(
            data["persist"] is False,
            f"{label}: persist not False",
        )

        require(
            data["requested_reasoning_mode"] == "normal",
            f"{label}: requested reasoning not Normal",
        )

        require(
            data["result_reasoning_mode"] == "normal",
            f"{label}: result reasoning not Normal",
        )

        require(
            data["expected_hermes_reasoning_effort"] == "medium",
            f"{label}: Hermes effort not medium",
        )

        require(
            data["session_created"] is True,
            f"{label}: fresh session not created",
        )

        require(
            data["session_reused"] is False,
            f"{label}: session reused",
        )

        require(
            data["session_recovered"] is False,
            f"{label}: session recovered",
        )

        require(
            data["cleanup_performed"] is False,
            f"{label}: cleanup occurred inside measurement",
        )

        require(
            data["active_yaml_sha"] == EXPECTED_ACTIVE_SHA,
            f"{label}: frozen active.yaml changed",
        )

        require(
            data["persistent_source_active_ready"]
            == ["debugging"],
            f"{label}: persistent Ready changed",
        )

        require(
            data["persistent_source_task_sticky_skills"]
            == ["debugging"],
            f"{label}: persistent sticky Skill changed",
        )

        require(
            data["benchmark_neutral_active_ready"] == [],
            f"{label}: benchmark Ready not neutral",
        )

        require(
            data["benchmark_neutral_task_sticky_skills"] == [],
            f"{label}: benchmark sticky Skills not neutral",
        )

        require(
            same_members(
                data["base_toolsets"],
                ["file", "terminal"],
            ),
            f"{label}: base toolsets mismatch",
        )

        require(
            same_members(
                data["ready"],
                spec["ready"],
            ),
            f"{label}: Ready surface mismatch",
        )

        require(
            same_members(
                data["temporary_toolsets"],
                spec["temporary_toolsets"],
            ),
            f"{label}: temporary toolsets mismatch",
        )

        require(
            same_members(
                data["runtime_skills"],
                spec["runtime_skills"],
            ),
            f"{label}: runtime Skills mismatch",
        )

        require(
            same_members(
                data["toolsets_during"],
                spec["toolsets_during"],
            ),
            f"{label}: live toolsets mismatch",
        )

        require(
            same_members(
                data["toolsets_after_turn_before_exit"],
                spec["toolsets_during"],
            ),
            f"{label}: toolsets changed during turn",
        )

        require(
            same_members(
                data["toolsets_after_restore"],
                ["file", "terminal"],
            ),
            f"{label}: base toolsets not restored",
        )

        require(
            data["skill_overlay_bytes"]
            == spec["overlay_bytes"],
            f"{label}: overlay size mismatch",
        )

        if spec["overlay_bytes"] == 0:
            require(
                data["skill_overlay_hash"] is None,
                f"{label}: unexpected overlay hash",
            )
        else:
            require(
                bool(data["skill_overlay_hash"]),
                f"{label}: missing overlay hash",
            )

        require(
            data["skill_overlay_cache_hit"] is False,
            f"{label}: unexpected Skill overlay cache hit",
        )

        require(
            data["task_id"] not in seen_tasks,
            f"{label}: duplicate Task",
        )

        require(
            data["execution_context_id"] not in seen_contexts,
            f"{label}: duplicate execution context",
        )

        require(
            data["session_id"] not in seen_sessions,
            f"{label}: duplicate runtime session",
        )

        require(
            data["execution_context_id"]
            == f"ctx-l7-{surface}-{trial:02d}",
            f"{label}: context ID mismatch",
        )

        before = "\n".join(
            data["resident_before"]
        )

        after = "\n".join(
            data["resident_after"]
        )

        require(
            MODEL in before,
            f"{label}: Small not warm before turn",
        )

        require(
            MODEL in after,
            f"{label}: Small not resident after turn",
        )

        if common_message is None:
            common_message = data["message"]
        else:
            require(
                data["message"] == common_message,
                f"{label}: benchmark message changed",
            )

        seen_tasks.add(
            data["task_id"]
        )

        seen_contexts.add(
            data["execution_context_id"]
        )

        seen_sessions.add(
            data["session_id"]
        )

        records[
            (surface, trial)
        ] = data

        print(
            f"PASS {label}: "
            f"{data['turn_duration_s']:.9f} s"
        )


require(
    len(records) == 20,
    "Independent certifier did not obtain 20 records",
)

require(
    len(seen_tasks) == 20,
    "Expected 20 unique Tasks",
)

require(
    len(seen_contexts) == 20,
    "Expected 20 unique execution contexts",
)

require(
    len(seen_sessions) == 20,
    "Expected 20 unique runtime sessions",
)


# ------------------------------------------------------------
# INDEPENDENT STATISTICS
# ------------------------------------------------------------

surface_stats = {}

for surface in ("a", "b", "c", "d"):
    turns = [
        records[
            (surface, trial)
        ]["turn_duration_s"]
        for trial in range(1, 6)
    ]

    overheads = [
        (
            records[
                (surface, trial)
            ]["activation_enter_s"]
            +
            records[
                (surface, trial)
            ]["activation_exit_s"]
        )
        for trial in range(1, 6)
    ]

    surface_stats[surface] = {
        "turn": metric_stats(turns),
        "activation_overhead":
            metric_stats(overheads),
    }


def paired(left: str, right: str):
    values = [
        (
            records[
                (left, trial)
            ]["turn_duration_s"]
            -
            records[
                (right, trial)
            ]["turn_duration_s"]
        )
        for trial in range(1, 6)
    ]

    return {
        "differences_s": values,
        "median_difference_s":
            statistics.median(values),
        "mean_difference_s":
            statistics.mean(values),
        "stdev_difference_s":
            statistics.stdev(values),
        "left_slower_count":
            sum(value > 0 for value in values),
        "left_faster_count":
            sum(value < 0 for value in values),
        "ties":
            sum(value == 0 for value in values),
    }


paired_stats = {
    "b_minus_a": paired("b", "a"),
    "c_minus_a": paired("c", "a"),
    "d_minus_a": paired("d", "a"),
    "d_minus_b": paired("d", "b"),
    "d_minus_c": paired("d", "c"),
}


# ------------------------------------------------------------
# COMPARE B CALCULATIONS AGAINST FROZEN A SUMMARY
# ------------------------------------------------------------

for surface in ("a", "b", "c", "d"):
    a_turn = (
        summary["surface_statistics"]
        [surface]["turn"]
    )

    b_turn = (
        surface_stats[surface]["turn"]
    )

    for field in (
        "median_s",
        "mean_s",
        "stdev_s",
        "min_s",
        "max_s",
    ):
        require(
            close(
                a_turn[field],
                b_turn[field],
            ),
            (
                f"{surface.upper()}: "
                f"A/B turn statistic mismatch: {field}"
            ),
        )

    a_overhead = (
        summary["surface_statistics"]
        [surface]["activation_overhead"]
    )

    b_overhead = (
        surface_stats[surface]["activation_overhead"]
    )

    require(
        close(
            a_overhead["median_s"],
            b_overhead["median_s"],
        ),
        (
            f"{surface.upper()}: "
            "A/B activation-overhead median mismatch"
        ),
    )


for name, b_values in paired_stats.items():
    a_values = (
        summary["paired_statistics"][name]
    )

    for field in (
        "median_difference_s",
        "mean_difference_s",
        "stdev_difference_s",
    ):
        require(
            close(
                a_values[field],
                b_values[field],
            ),
            f"{name}: A/B statistic mismatch: {field}",
        )

    for field in (
        "left_slower_count",
        "left_faster_count",
        "ties",
    ):
        require(
            a_values[field]
            == b_values[field],
            f"{name}: A/B count mismatch: {field}",
        )


require(
    summary["raw_artifact_hashes"] == raw_hashes,
    "A summary raw-artifact hashes do not match frozen raw files",
)

require(
    summary["harness"]["sha256"]
    == EXPECTED_HARNESS_SHA,
    "A summary harness SHA mismatch",
)

require(
    paired_stats["d_minus_a"]["left_slower_count"] == 5,
    "D was not slower than A in all five sets",
)

require(
    paired_stats["d_minus_b"]["left_slower_count"] == 5,
    "D was not slower than B in all five sets",
)

require(
    paired_stats["d_minus_c"]["left_slower_count"] == 5,
    "D was not slower than C in all five sets",
)


print()
print("=== B INDEPENDENT SURFACE STATISTICS ===")

for surface in ("a", "b", "c", "d"):
    values = surface_stats[surface]["turn"]

    print(
        f"{surface.upper()} "
        f"median={values['median_s']:.9f} "
        f"mean={values['mean_s']:.9f} "
        f"stdev={values['stdev_s']:.9f}"
    )


print()
print("=== B INDEPENDENT PAIRED RESULTS ===")

for name, values in paired_stats.items():
    print(
        f"{name}: "
        f"median={values['median_difference_s']:.9f} "
        f"mean={values['mean_difference_s']:.9f} "
        f"left_slower={values['left_slower_count']}/5"
    )


print()
print("=== B ACTIVATION OVERHEAD MEDIANS ===")

for surface in ("a", "b", "c", "d"):
    value = (
        surface_stats[surface]
        ["activation_overhead"]
        ["median_s"]
    )

    print(
        f"{surface.upper()}: "
        f"{value:.9f} s"
    )


# ------------------------------------------------------------
# WRITE SEPARATE B CERTIFICATION EVIDENCE
# ------------------------------------------------------------

stamp = datetime.now(
    timezone.utc
).strftime(
    "%Y%m%dT%H%M%SZ"
)

B_ARCHIVE = (
    ROOT
    / "backups"
    / f"phase14_11L7_B_independent_certified_{stamp}"
)

require(
    not B_ARCHIVE.exists(),
    "B certification archive already exists",
)

B_ARCHIVE.mkdir(
    parents=True,
)


report = {
    "phase": "14.11L.7",
    "certifier": "B-independent",
    "source_a_archive":
        str(A_ARCHIVE.relative_to(ROOT)),
    "source_a_manifest_sha256":
        manifest_sha,
    "source_a_summary_sha256":
        sha(summary_path),
    "source_harness_sha256":
        sha(harness),
    "measurement_count":
        len(records),
    "unique_task_count":
        len(seen_tasks),
    "unique_execution_context_count":
        len(seen_contexts),
    "unique_runtime_session_count":
        len(seen_sessions),
    "surface_statistics":
        surface_stats,
    "paired_statistics":
        paired_stats,
    "findings": {
        "b_slower_than_a_sets":
            paired_stats["b_minus_a"]
            ["left_slower_count"],
        "c_slower_than_a_sets":
            paired_stats["c_minus_a"]
            ["left_slower_count"],
        "d_slower_than_a_sets":
            paired_stats["d_minus_a"]
            ["left_slower_count"],
        "d_slower_than_b_sets":
            paired_stats["d_minus_b"]
            ["left_slower_count"],
        "d_slower_than_c_sets":
            paired_stats["d_minus_c"]
            ["left_slower_count"],
    },
    "production_state_modified":
        False,
    "real_inference_executed":
        False,
    "result":
        "PASS",
}


report_path = (
    B_ARCHIVE
    / "independent_certification.json"
)

report_path.write_text(
    json.dumps(
        report,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


cert_text = f"""\
PHASE 14.11L.7 — B INDEPENDENT CERTIFICATION

Source A archive:
{report["source_a_archive"]}

A manifest SHA256:
{manifest_sha}

A summary SHA256:
{sha(summary_path)}

Frozen harness SHA256:
{sha(harness)}

Raw measurements independently validated:
20 / 20

Unique Tasks:
20

Unique execution contexts:
20

Unique runtime sessions:
20

Independent statistical recomputation:
PASS

A/B statistical agreement:
PASS

D slower than A:
5 / 5 matched sets

D slower than B:
5 / 5 matched sets

D slower than C:
5 / 5 matched sets

Real inference executed by B:
NO

Production state modified by B:
NO

FINAL B RESULT:
PASS
"""

(
    B_ARCHIVE
    / "CERTIFICATION.txt"
).write_text(
    cert_text
)


manifest_b = (
    B_ARCHIVE
    / "SHA256SUMS.txt"
)

files_to_hash = [
    B_ARCHIVE
    / "CERTIFICATION.txt",
    report_path,
]

manifest_b.write_text(
    "".join(
        (
            f"{sha(path)}  "
            f"{path.name}\n"
        )
        for path in sorted(
            files_to_hash,
            key=lambda item: item.name,
        )
    )
)


print()
print("A/B independent statistics agreement: PASS")
print("20 / 20 independent semantic validations: PASS")
print()
print("B archive:")
print(B_ARCHIVE)
print()
print("B report SHA256:")
print(sha(report_path))
print()
print("B manifest SHA256:")
print(sha(manifest_b))
print()
print("PHASE 14.11L.7 B INDEPENDENT CERTIFICATION: PASS")
