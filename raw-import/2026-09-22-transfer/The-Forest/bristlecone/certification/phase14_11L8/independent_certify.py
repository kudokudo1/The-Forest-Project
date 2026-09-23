from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from resources.availability import ResourceAvailability
from resources.budget import ResourceBudget
from resources.evaluation import ResourceEvaluationPipeline
from resources.governor import evaluate_resource_request
from resources.model import ResourceRequest
from resources.requirement import ResourceRequirement


ROOT = Path("/home/user/The-Forest/bristlecone")

A_ARCHIVE = (
    ROOT
    / "backups"
    / "phase14_11L8_A_governor_certified_20260813T005056Z"
)

EXPECTED_A_MANIFEST_SHA = (
    "aa2c724800b9774e272bf01a7e2227d169590feb2150bad27999a900040a0978"
)

EXPECTED_CORE_RAW_SHA = (
    "2c9e70239070edac150646fe00f75593fea1baf7522ccbb182b32860ee47cb91"
)

EXPECTED_RESIDENCY_RAW_SHA = (
    "243c92316063a368712d690eb06b1fd636d571e881e812b572358e1682e8b166"
)

EXPECTED_SUMMARY_SHA = (
    "7f51d85b38cb705cb495bfb56a142bc65d0f85d3f7905774ea7eab2e937ce3a5"
)

EXPECTED_CORE_HARNESS_SHA = (
    "f8ab314952c95fb01b2f5b0295eb89da605d6708e436e665c704d997dd7991f5"
)

EXPECTED_RESIDENCY_HARNESS_SHA = (
    "e7c50bac53094207562af09b470a030abef400eeb283bbc510c8d8531605035d"
)

SOURCE_MAP = {
    "governor":
        "governor.py",
    "evaluation":
        "evaluation.py",
    "live_providers":
        "live_providers.py",
    "model":
        "model.py",
    "requirement":
        "requirement.py",
    "budget":
        "budget.py",
    "availability":
        "availability.py",
    "decision":
        "decision.py",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def make_request(
    name,
    *,
    may_defer,
    priority="standard",
):
    return ResourceRequest(
        task_id=f"l8b-{name}",
        execution_context_id=f"ctx-l8b-{name}",
        model_form="small",
        reasoning_mode="normal",
        priority=priority,
        source="phase14_11L8-B",
        reasons=("Independent certification",),
        may_defer=may_defer,
    )


def make_requirement(
    request,
    *,
    memory,
    accelerator=0,
    cpu=1,
):
    return ResourceRequirement(
        request=request,
        source="l8b-requirement",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


def make_budget(
    *,
    memory=None,
    accelerator=None,
    cpu=None,
):
    return ResourceBudget(
        source="l8b-budget",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


def make_availability(
    *,
    memory,
    accelerator=0,
    cpu=8,
):
    return ResourceAvailability(
        source="l8b-availability",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


print("=== PHASE 14.11L.8 B INDEPENDENT CERTIFIER ===")
print()


# ============================================================
# A ARCHIVE + MANIFEST
# ============================================================

require(
    A_ARCHIVE.is_dir(),
    f"Missing A archive: {A_ARCHIVE}",
)

manifest = (
    A_ARCHIVE
    / "SHA256SUMS.txt"
)

require(
    manifest.exists(),
    "A manifest missing",
)

manifest_sha = sha256(
    manifest
)

require(
    manifest_sha
    == EXPECTED_A_MANIFEST_SHA,
    "A manifest SHA mismatch",
)

print("PASS A manifest SHA")


entries = {}

for raw_line in (
    manifest.read_text().splitlines()
):
    line = raw_line.strip()

    if not line:
        continue

    digest, name = line.split(
        maxsplit=1
    )

    name = name.strip()

    if name.startswith("*"):
        name = name[1:]

    if name.startswith("./"):
        name = name[2:]

    require(
        name not in entries,
        f"Duplicate manifest entry: {name}",
    )

    entries[name] = digest


expected_files = {
    "CERTIFICATION.txt",
    "l8_governor_summary.json",
    "certification/governor_benchmark.py",
    "certification/residency_effect.py",
    "certification/analyze_governor.py",
    "raw/l8_governor_raw.json",
    "raw/l8_residency_effect_raw.json",
}

for filename in SOURCE_MAP.values():
    expected_files.add(
        f"source/{filename}"
    )


require(
    set(entries) == expected_files,
    (
        "A archive inventory mismatch: "
        f"expected {len(expected_files)}, "
        f"got {len(entries)}"
    ),
)


for name, expected_digest in sorted(
    entries.items()
):
    path = A_ARCHIVE / name

    require(
        path.exists(),
        f"Manifest file missing: {name}",
    )

    require(
        sha256(path)
        == expected_digest,
        f"Manifest hash mismatch: {name}",
    )


print(
    "PASS A archive contents:",
    f"{len(entries)} / {len(expected_files)} files",
)


# ============================================================
# FROZEN A ANCHORS
# ============================================================

core_path = (
    A_ARCHIVE
    / "raw/l8_governor_raw.json"
)

resident_path = (
    A_ARCHIVE
    / "raw/l8_residency_effect_raw.json"
)

summary_path = (
    A_ARCHIVE
    / "l8_governor_summary.json"
)

core_harness = (
    A_ARCHIVE
    / "certification/governor_benchmark.py"
)

resident_harness = (
    A_ARCHIVE
    / "certification/residency_effect.py"
)


require(
    sha256(core_path)
    == EXPECTED_CORE_RAW_SHA,
    "Core raw SHA mismatch",
)

require(
    sha256(resident_path)
    == EXPECTED_RESIDENCY_RAW_SHA,
    "Residency raw SHA mismatch",
)

require(
    sha256(summary_path)
    == EXPECTED_SUMMARY_SHA,
    "A summary SHA mismatch",
)

require(
    sha256(core_harness)
    == EXPECTED_CORE_HARNESS_SHA,
    "Core harness SHA mismatch",
)

require(
    sha256(resident_harness)
    == EXPECTED_RESIDENCY_HARNESS_SHA,
    "Residency harness SHA mismatch",
)


print("PASS frozen A anchor hashes")


core = json.loads(
    core_path.read_text()
)

resident = json.loads(
    resident_path.read_text()
)

summary = json.loads(
    summary_path.read_text()
)


# ============================================================
# PRODUCTION SOURCE INTEGRITY
# ============================================================

recorded_source_hashes = (
    core["source_sha256"]
)

require(
    set(recorded_source_hashes)
    == set(SOURCE_MAP),
    "Core raw source inventory mismatch",
)


for key, filename in (
    SOURCE_MAP.items()
):
    archived = (
        A_ARCHIVE
        / "source"
        / filename
    )

    live = (
        ROOT
        / "resources"
        / filename
    )

    archived_sha = sha256(
        archived
    )

    live_sha = sha256(
        live
    )

    require(
        archived_sha
        == recorded_source_hashes[key],
        (
            f"Archived source differs from "
            f"measurement source: {filename}"
        ),
    )

    require(
        live_sha
        == archived_sha,
        (
            f"Production source changed since "
            f"A freeze: {filename}"
        ),
    )


print("PASS frozen/live production source integrity")


# ============================================================
# INDEPENDENT GOVERNOR SEMANTIC MATRIX
# ============================================================

cases = [
    (
        "approve",
        False,
        1024,
        None,
        8192,
        "approve",
    ),
    (
        "budget-deny-deferrable",
        True,
        6144,
        4096,
        16384,
        "deny",
    ),
    (
        "budget-deny-nondeferrable",
        False,
        6144,
        4096,
        16384,
        "deny",
    ),
    (
        "unknown-requirement-defer",
        True,
        None,
        None,
        8192,
        "defer",
    ),
    (
        "unknown-requirement-deny",
        False,
        None,
        None,
        8192,
        "deny",
    ),
    (
        "insufficient-availability-defer",
        True,
        1024,
        None,
        512,
        "defer",
    ),
    (
        "insufficient-availability-deny",
        False,
        1024,
        None,
        512,
        "deny",
    ),
    (
        "unknown-availability-defer",
        True,
        1024,
        None,
        None,
        "defer",
    ),
    (
        "unknown-availability-deny",
        False,
        1024,
        None,
        None,
        "deny",
    ),
]


independent_outcomes = {}


for (
    name,
    may_defer,
    required_memory,
    budget_memory,
    available_memory,
    expected,
) in cases:
    req = make_request(
        name,
        may_defer=may_defer,
    )

    decision = evaluate_resource_request(
        req,
        make_requirement(
            req,
            memory=required_memory,
        ),
        make_budget(
            memory=budget_memory,
        ),
        make_availability(
            memory=available_memory,
        ),
        source="phase14_11L8-B-pure",
    )

    require(
        decision.outcome
        == expected,
        (
            f"{name}: expected {expected}, "
            f"got {decision.outcome}"
        ),
    )

    independent_outcomes[name] = (
        decision.outcome
    )

    print(
        f"PASS {name}: "
        f"{decision.outcome}"
    )


# ============================================================
# ZERO-REQUIREMENT BYPASS
# ============================================================

zero_request = make_request(
    "zero-bypass",
    may_defer=False,
)

zero_decision = evaluate_resource_request(
    zero_request,
    make_requirement(
        zero_request,
        memory=0,
        accelerator=0,
        cpu=1,
    ),
    make_budget(),
    make_availability(
        memory=None,
        accelerator=None,
        cpu=1,
    ),
    source="phase14_11L8-B-zero",
)


require(
    zero_decision.outcome
    == "approve",
    "Independent zero-requirement bypass failed",
)

print(
    "PASS zero-requirement bypass: approve"
)


# ============================================================
# PRIORITY CHECK
# ============================================================

priority_outcomes = {}

for priority in (
    "background",
    "standard",
    "interactive",
):
    req = make_request(
        f"priority-{priority}",
        may_defer=False,
        priority=priority,
    )

    result = evaluate_resource_request(
        req,
        make_requirement(
            req,
            memory=1024,
        ),
        make_budget(),
        make_availability(
            memory=8192,
        ),
        source="phase14_11L8-B-priority",
    )

    priority_outcomes[
        priority
    ] = result.outcome


require(
    priority_outcomes
    == {
        "background": "approve",
        "standard": "approve",
        "interactive": "approve",
    },
    "Independent priority semantics changed",
)

print(
    "PASS priority semantics:",
    priority_outcomes,
)


# ============================================================
# INDEPENDENT PROVIDER-ORDER CHECK
# ============================================================

order = []

order_request = make_request(
    "provider-order",
    may_defer=False,
)


def requirement_provider(req):
    order.append(
        "requirement"
    )

    return make_requirement(
        req,
        memory=1024,
    )


def budget_provider(req):
    order.append(
        "budget"
    )

    return make_budget()


def availability_provider(req):
    order.append(
        "availability"
    )

    return make_availability(
        memory=8192,
    )


pipeline = ResourceEvaluationPipeline(
    requirement_provider=
        requirement_provider,
    budget_provider=
        budget_provider,
    availability_provider=
        availability_provider,
    source="phase14_11L8-B-pipeline",
)


pipeline_decision = pipeline(
    order_request
)


require(
    order == [
        "requirement",
        "budget",
        "availability",
    ],
    (
        "Provider execution order changed: "
        f"{order}"
    ),
)

require(
    pipeline_decision.outcome
    == "approve",
    "Synthetic composed pipeline did not approve",
)


print(
    "PASS provider order: "
    "requirement -> budget -> availability -> Governor"
)


# ============================================================
# INDEPENDENT RESIDENCY MATH
# ============================================================

resident_bytes = (
    resident["resident_size_bytes"]
)

floor_mib = (
    resident["calibrated_floor_mib"]
)

mib_bytes = 1024 * 1024

calibrated_bytes = (
    floor_mib
    * mib_bytes
)

remaining_bytes = max(
    0,
    calibrated_bytes
    - resident_bytes,
)

independent_remaining_mib = (
    remaining_bytes
    + mib_bytes
    - 1
) // mib_bytes


require(
    floor_mib == 6144,
    "Calibrated floor is not 6144 MiB",
)

require(
    resident_bytes
    == 5646906816,
    "Resident byte value changed",
)

require(
    independent_remaining_mib
    == 759,
    (
        "Independent residency math did not "
        "produce 759 MiB"
    ),
)

require(
    resident[
        "expected_remaining_requirement_mib"
    ] == independent_remaining_mib,
    "Residency artifact expected value mismatch",
)

require(
    resident[
        "observed_memory_mib_values"
    ] == [759],
    "Residency artifact observed value mismatch",
)

require(
    resident[
        "comparison_nonresident_requirement_mib"
    ] == 6144,
    "Nonresident comparison mismatch",
)


print(
    "PASS independent residency math: "
    "6144 MiB -> 759 MiB"
)


# ============================================================
# RAW CORE SEMANTICS
# ============================================================

require(
    core["status"]
    == "success",
    "Core raw status failed",
)

require(
    core["real_inference_executed"]
    is False,
    "Core raw reports inference",
)

require(
    core["runtime_session_created"]
    is False,
    "Core raw reports runtime session",
)

require(
    core["production_state_modified"]
    is False,
    "Core raw reports production mutation",
)

require(
    core["whole_live_pipeline"]
    ["outcomes"]
    == {
        "approve": 20,
    },
    "Core live pipeline did not approve 20/20",
)

require(
    core["live_requirement"]
    ["memory_mib_values"]
    == [6144],
    "Core nonresident requirement mismatch",
)

require(
    core["live_availability"]
    ["cpu_threads"]
    == [9],
    "Core CPU-thread observation mismatch",
)

require(
    core["live_budget"]
    ["memory_mib"]
    is None,
    "Core unexpectedly has RAM budget ceiling",
)

require(
    core["priority_outcomes"]
    == priority_outcomes,
    "A/B priority semantic disagreement",
)


for name, expected in (
    independent_outcomes.items()
):
    require(
        core["pure_policy_cases"]
        [name]
        ["expected_outcome"]
        == expected,
        (
            f"A/B semantic disagreement: "
            f"{name}"
        ),
    )


print(
    "PASS A/B raw semantic agreement"
)


# ============================================================
# SUMMARY CONSISTENCY
#
# L.8 raw files retain aggregate timing statistics, not each
# individual timing sample. Therefore B can verify that the
# frozen A summary faithfully carries the frozen raw metrics,
# but cannot reconstruct the original sample medians.
# ============================================================

performance = (
    summary["core_performance"]
)

require(
    performance[
        "pure_governor_approve_median_us"
    ]
    ==
    core["pure_policy_cases"]
    ["approve"]
    ["timing"]
    ["median_us"],
    "A summary pure-Governor median mismatch",
)

require(
    performance[
        "live_availability_median_us"
    ]
    ==
    core["live_availability"]
    ["timing"]
    ["median_us"],
    "A summary availability median mismatch",
)

require(
    performance[
        "live_budget_median_us"
    ]
    ==
    core["live_budget"]
    ["timing"]
    ["median_us"],
    "A summary budget median mismatch",
)

require(
    performance[
        "nonresident_requirement_median_us"
    ]
    ==
    core["live_requirement"]
    ["timing"]
    ["median_us"],
    "A summary requirement median mismatch",
)

require(
    performance[
        "whole_live_pipeline_median_us"
    ]
    ==
    core["whole_live_pipeline"]
    ["timing"]
    ["median_us"],
    "A summary pipeline median mismatch",
)

require(
    summary["residency_effect"]
    ["resident_provider_median_us"]
    ==
    resident["provider_timing"]
    ["median_us"],
    "A summary resident-provider median mismatch",
)

require(
    summary["residency_effect"]
    ["nonresident_requirement_mib"]
    == 6144,
    "A summary nonresident requirement mismatch",
)

require(
    summary["residency_effect"]
    ["resident_requirement_mib"]
    == 759,
    "A summary resident requirement mismatch",
)

require(
    summary["result"]
    == "PASS",
    "A summary result is not PASS",
)


print(
    "PASS A summary faithfully matches "
    "frozen raw aggregate statistics"
)


# ============================================================
# WRITE B EVIDENCE
# ============================================================

stamp = datetime.now(
    timezone.utc
).strftime(
    "%Y%m%dT%H%M%SZ"
)

B_ARCHIVE = (
    ROOT
    / "backups"
    / f"phase14_11L8_B_independent_certified_{stamp}"
)

require(
    not B_ARCHIVE.exists(),
    "B archive already exists",
)

B_ARCHIVE.mkdir(
    parents=True,
)


report = {
    "phase":
        "14.11L.8",
    "certifier":
        "B-independent",
    "source_a_archive":
        str(
            A_ARCHIVE.relative_to(ROOT)
        ),
    "source_a_manifest_sha256":
        manifest_sha,
    "core_raw_sha256":
        sha256(core_path),
    "residency_raw_sha256":
        sha256(resident_path),
    "a_summary_sha256":
        sha256(summary_path),
    "independent_semantic_outcomes":
        independent_outcomes,
    "independent_priority_outcomes":
        priority_outcomes,
    "provider_order": [
        "requirement",
        "budget",
        "availability",
        "Governor",
    ],
    "independent_residency_calculation": {
        "calibrated_floor_mib":
            floor_mib,
        "resident_size_bytes":
            resident_bytes,
        "remaining_requirement_mib":
            independent_remaining_mib,
    },
    "frozen_performance_metrics": {
        "pure_governor_approve_median_us":
            performance[
                "pure_governor_approve_median_us"
            ],
        "live_availability_median_us":
            performance[
                "live_availability_median_us"
            ],
        "live_budget_median_us":
            performance[
                "live_budget_median_us"
            ],
        "nonresident_requirement_median_us":
            performance[
                "nonresident_requirement_median_us"
            ],
        "whole_live_pipeline_median_us":
            performance[
                "whole_live_pipeline_median_us"
            ],
        "resident_requirement_median_us":
            summary["residency_effect"]
            ["resident_provider_median_us"],
    },
    "timing_sample_recomputation": {
        "performed":
            False,
        "reason":
            (
                "Frozen L.8 raw artifacts retain "
                "aggregate timing statistics, not "
                "individual per-iteration timing samples."
            ),
    },
    "real_inference_executed":
        False,
    "ollama_residency_changed":
        False,
    "production_state_modified":
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


certification_text = f"""\
PHASE 14.11L.8 — B INDEPENDENT CERTIFICATION

A source archive:
{report["source_a_archive"]}

A manifest SHA256:
{manifest_sha}

Core raw SHA256:
{sha256(core_path)}

Residency raw SHA256:
{sha256(resident_path)}

A summary SHA256:
{sha256(summary_path)}

A archive integrity:
PASS

Frozen/live production source integrity:
PASS

Independent Governor semantic matrix:
PASS

Independent zero-requirement bypass:
PASS

Independent priority semantics:
PASS

Independent provider-order check:
PASS

Independent residency calculation:
6144 MiB -> 759 MiB
PASS

A summary / raw aggregate-statistic agreement:
PASS

Per-iteration timing-sample recomputation:
NOT POSSIBLE FROM FROZEN ARTIFACT
Reason:
L.8 stores aggregate timing statistics rather than individual
per-iteration timing samples.

This limitation does not invalidate the frozen measurements;
B independently verifies their artifact integrity and A-summary
consistency but does not claim to reconstruct the original
sample medians.

Real inference executed by B:
NO

Ollama residency changed by B:
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
    certification_text
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
            f"{sha256(path)}  "
            f"{path.name}\n"
        )
        for path in sorted(
            files_to_hash,
            key=lambda item: item.name,
        )
    )
)


print()
print(
    "Independent Governor semantics: PASS"
)

print(
    "Independent provider order: PASS"
)

print(
    "Independent residency math: PASS"
)

print(
    "A/raw aggregate-statistic agreement: PASS"
)

print()
print("B archive:")
print(B_ARCHIVE)

print()
print("B report SHA256:")
print(
    sha256(report_path)
)

print()
print("B manifest SHA256:")
print(
    sha256(manifest_b)
)

print()
print(
    "PHASE 14.11L.8 B INDEPENDENT CERTIFICATION: PASS"
)
