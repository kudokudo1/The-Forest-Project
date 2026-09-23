from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path("/home/user/The-Forest/bristlecone")
BENCH = ROOT / "benchmarks/phase14_11L"

CORE = (
    BENCH
    / "l8_governor_raw.json"
)

RESIDENCY = (
    BENCH
    / "l8_residency_effect_raw.json"
)

OUTPUT = (
    BENCH
    / "l8_governor_summary.json"
)

CORE_HARNESS = (
    ROOT
    / "certification/phase14_11L8/governor_benchmark.py"
)

RESIDENCY_HARNESS = (
    ROOT
    / "certification/phase14_11L8/residency_effect.py"
)

EXPECTED_CORE_SHA = (
    "2c9e70239070edac150646fe00f75593"
    "fea1baf7522ccbb182b32860ee47cb91"
)

EXPECTED_RESIDENCY_SHA = (
    "243c92316063a368712d690eb06b1fd63"
    "6d571e881e812b572358e1682e8b166"
)

EXPECTED_SOURCE_FILES = {
    "governor":
        "resources/governor.py",
    "evaluation":
        "resources/evaluation.py",
    "live_providers":
        "resources/live_providers.py",
    "model":
        "resources/model.py",
    "requirement":
        "resources/requirement.py",
    "budget":
        "resources/budget.py",
    "availability":
        "resources/availability.py",
    "decision":
        "resources/decision.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def require(
    condition: bool,
    message: str,
) -> None:
    if not condition:
        raise RuntimeError(message)


print("=== PHASE 14.11L.8 A CERTIFICATION ===")
print()


# ------------------------------------------------------------
# FILE IDENTITY
# ------------------------------------------------------------

for path in (
    CORE,
    RESIDENCY,
    CORE_HARNESS,
    RESIDENCY_HARNESS,
):
    require(
        path.exists(),
        f"Missing required file: {path}",
    )


require(
    sha256(CORE) == EXPECTED_CORE_SHA,
    "Core L.8 raw artifact SHA mismatch",
)

require(
    sha256(RESIDENCY)
    == EXPECTED_RESIDENCY_SHA,
    "Residency raw artifact SHA mismatch",
)

require(
    not OUTPUT.exists(),
    f"Refusing to overwrite existing summary: {OUTPUT}",
)

print("PASS core raw SHA")
print("PASS residency raw SHA")


core = json.loads(
    CORE.read_text()
)

resident = json.loads(
    RESIDENCY.read_text()
)


# ------------------------------------------------------------
# CORE BENCHMARK IDENTITY
# ------------------------------------------------------------

require(
    core["phase"] == "14.11L.8",
    "Wrong core phase",
)

require(
    core["scenario"]
    == "resource-governor-performance",
    "Wrong core scenario",
)

require(
    core["status"] == "success",
    "Core benchmark status is not success",
)

require(
    core["real_inference_executed"] is False,
    "Core benchmark unexpectedly executed inference",
)

require(
    core["runtime_session_created"] is False,
    "Core benchmark unexpectedly created runtime session",
)

require(
    core["production_state_modified"] is False,
    "Core benchmark reports production mutation",
)


expected_iterations = {
    "pure_policy_per_case": 20000,
    "live_availability": 1000,
    "live_budget": 5000,
    "live_requirement": 20,
    "whole_live_pipeline": 20,
}

require(
    core["iterations"] == expected_iterations,
    "Core iteration counts changed",
)

print("PASS core benchmark identity")


# ------------------------------------------------------------
# PURE GOVERNOR POLICY
# ------------------------------------------------------------

expected_cases = {
    "approve":
        "approve",
    "budget-deny-deferrable":
        "deny",
    "budget-deny-nondeferrable":
        "deny",
    "unknown-requirement-defer":
        "defer",
    "unknown-requirement-deny":
        "deny",
    "insufficient-availability-defer":
        "defer",
    "insufficient-availability-deny":
        "deny",
    "unknown-availability-defer":
        "defer",
    "unknown-availability-deny":
        "deny",
}

cases = core["pure_policy_cases"]

require(
    set(cases) == set(expected_cases),
    "Pure-policy case inventory changed",
)


for name, expected_outcome in expected_cases.items():
    case = cases[name]

    require(
        case["expected_outcome"]
        == expected_outcome,
        f"{name}: wrong outcome",
    )

    require(
        case["timing"]["count"] == 20000,
        f"{name}: wrong timing count",
    )

    require(
        case["timing"]["median_ns"] >= 0,
        f"{name}: invalid median",
    )

    print(
        f"PASS {name}: "
        f"{expected_outcome}"
    )


require(
    core["zero_requirement_bypass"]
    == "approve",
    "Zero-requirement bypass failed",
)

require(
    core["priority_outcomes"]
    == {
        "background": "approve",
        "standard": "approve",
        "interactive": "approve",
    },
    "Priority semantic result changed",
)

print("PASS zero-requirement bypass")
print("PASS current priority semantics")


# ------------------------------------------------------------
# LIVE AVAILABILITY
# ------------------------------------------------------------

live_availability = (
    core["live_availability"]
)

require(
    live_availability["timing"]["count"]
    == 1000,
    "Wrong availability observation count",
)

require(
    live_availability["memory_mib_min"]
    == 10095,
    "Unexpected observed minimum MemAvailable",
)

require(
    live_availability["memory_mib_max"]
    == 10095,
    "Unexpected observed maximum MemAvailable",
)

require(
    live_availability["cpu_threads"]
    == [9],
    "Unexpected available CPU threads",
)

require(
    live_availability["accelerator_memory_mib"]
    == 0,
    "Unexpected accelerator availability",
)

print("PASS live availability observation")


# ------------------------------------------------------------
# LIVE BUDGET
# ------------------------------------------------------------

live_budget = core["live_budget"]

require(
    live_budget["timing"]["count"] == 5000,
    "Wrong live budget count",
)

require(
    live_budget["memory_mib"] is None
    and live_budget["accelerator_memory_mib"] is None
    and live_budget["cpu_threads"] is None,
    "Live Small unexpectedly has explicit ceilings",
)

print("PASS live no-explicit-budget semantics")


# ------------------------------------------------------------
# NONRESIDENT REQUIREMENT
# ------------------------------------------------------------

live_requirement = (
    core["live_requirement"]
)

require(
    live_requirement["timing"]["count"] == 20,
    "Wrong nonresident requirement count",
)

require(
    live_requirement["memory_mib_values"]
    == [6144],
    "Nonresident Small requirement changed",
)

require(
    live_requirement["accelerator_memory_mib"]
    == 0,
    "Nonresident accelerator requirement changed",
)

require(
    live_requirement["cpu_threads"] == 1,
    "Nonresident CPU requirement changed",
)

print(
    "PASS nonresident Small requirement: "
    "6144 MiB"
)


# ------------------------------------------------------------
# WHOLE LIVE PIPELINE
# ------------------------------------------------------------

pipeline = (
    core["whole_live_pipeline"]
)

require(
    pipeline["timing"]["count"] == 20,
    "Wrong whole-pipeline count",
)

require(
    pipeline["outcomes"]
    == {"approve": 20},
    "Whole live pipeline did not approve 20/20",
)

print("PASS whole live Governor: approve 20/20")


# ------------------------------------------------------------
# RESIDENT SMALL EFFECT
# ------------------------------------------------------------

require(
    resident["phase"] == "14.11L.8",
    "Wrong residency phase",
)

require(
    resident["scenario"]
    == "residency-aware-requirement-effect",
    "Wrong residency scenario",
)

require(
    resident["status"] == "success",
    "Residency benchmark status is not success",
)

require(
    resident["resident"] is True,
    "Resident condition was not established",
)

require(
    resident["model"]
    == "bristlecone-qwen35:4b-64k",
    "Wrong resident model",
)

require(
    resident["resident_size_bytes"]
    == 5646906816,
    "Exact resident Small byte size changed",
)

require(
    resident["calibrated_floor_mib"]
    == 6144,
    "Calibrated Small floor changed",
)

require(
    resident[
        "expected_remaining_requirement_mib"
    ] == 759,
    "Independent resident calculation changed",
)

require(
    resident["observed_memory_mib_values"]
    == [759],
    "Production resident requirement did not equal 759 MiB",
)

require(
    resident["comparison_nonresident_requirement_mib"]
    == 6144,
    "Nonresident comparison changed",
)

require(
    resident["accelerator_memory_mib"] == 0,
    "Resident accelerator requirement changed",
)

require(
    resident["cpu_threads"] == 1,
    "Resident CPU requirement changed",
)

require(
    resident["iterations"] == 20,
    "Wrong resident observation count",
)

require(
    resident[
        "real_inference_executed_by_this_script"
    ] is False,
    "Residency measurement script executed inference",
)

require(
    resident["production_state_modified"] is False,
    "Residency script reports production mutation",
)

print(
    "PASS resident Small requirement: "
    "759 MiB"
)

print(
    "PASS residency-aware requirement effect"
)


# ------------------------------------------------------------
# SOURCE INTEGRITY
# ------------------------------------------------------------

recorded_source_hashes = (
    core["source_sha256"]
)

require(
    set(recorded_source_hashes)
    == set(EXPECTED_SOURCE_FILES),
    "Recorded production source inventory changed",
)


for name, relative_path in (
    EXPECTED_SOURCE_FILES.items()
):
    path = ROOT / relative_path

    require(
        path.exists(),
        f"Missing production source: {relative_path}",
    )

    current_sha = sha256(path)

    require(
        current_sha
        == recorded_source_hashes[name],
        (
            f"Production source changed since "
            f"L.8 measurement: {relative_path}"
        ),
    )


print("PASS production source integrity")


# ------------------------------------------------------------
# DERIVED CERTIFICATION SUMMARY
# ------------------------------------------------------------

summary = {
    "phase":
        "14.11L.8",
    "certification":
        "A",
    "result":
        "PASS",
    "core_raw_sha256":
        sha256(CORE),
    "residency_raw_sha256":
        sha256(RESIDENCY),
    "harnesses": {
        "governor_benchmark": {
            "path":
                str(
                    CORE_HARNESS.relative_to(ROOT)
                ),
            "sha256":
                sha256(CORE_HARNESS),
        },
        "residency_effect": {
            "path":
                str(
                    RESIDENCY_HARNESS.relative_to(ROOT)
                ),
            "sha256":
                sha256(RESIDENCY_HARNESS),
        },
    },
    "core_performance": {
        "pure_governor_approve_median_us":
            cases["approve"]
            ["timing"]["median_us"],
        "live_availability_median_us":
            live_availability
            ["timing"]["median_us"],
        "live_budget_median_us":
            live_budget
            ["timing"]["median_us"],
        "nonresident_requirement_median_us":
            live_requirement
            ["timing"]["median_us"],
        "whole_live_pipeline_median_us":
            pipeline
            ["timing"]["median_us"],
    },
    "residency_effect": {
        "nonresident_requirement_mib":
            6144,
        "resident_size_bytes":
            5646906816,
        "resident_requirement_mib":
            759,
        "resident_provider_median_us":
            resident["provider_timing"]
            ["median_us"],
    },
    "semantic_results": {
        "pure_policy_case_count":
            len(cases),
        "zero_requirement_bypass":
            "approve",
        "priority_outcomes":
            core["priority_outcomes"],
        "live_pipeline_approve_count":
            20,
        "live_pipeline_decision_count":
            20,
    },
    "execution_notes": {
        "core_real_inference":
            False,
        "residency_script_real_inference":
            False,
        "controlled_unmeasured_prewarm_used":
            True,
        "persistent_production_state_modified":
            False,
        "transient_runtime_residency_intentionally_changed":
            True,
    },
    "source_sha256":
        recorded_source_hashes,
}


OUTPUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print()
print("=== L.8 CERTIFIED PERFORMANCE ===")

print(
    "Pure Governor approve median:",
    f"{summary['core_performance']['pure_governor_approve_median_us']:.3f} us",
)

print(
    "Live availability median:",
    f"{summary['core_performance']['live_availability_median_us']:.3f} us",
)

print(
    "Live budget median:",
    f"{summary['core_performance']['live_budget_median_us']:.3f} us",
)

print(
    "Nonresident requirement median:",
    f"{summary['core_performance']['nonresident_requirement_median_us']:.3f} us",
)

print(
    "Whole live Governor median:",
    f"{summary['core_performance']['whole_live_pipeline_median_us']:.3f} us",
)

print(
    "Resident requirement median:",
    f"{summary['residency_effect']['resident_provider_median_us']:.3f} us",
)

print()
print(
    "Nonresident requirement MiB:",
    6144,
)

print(
    "Resident requirement MiB:",
    759,
)

print()
print("Core harness SHA256:")
print(
    summary["harnesses"]
    ["governor_benchmark"]
    ["sha256"]
)

print()
print("Residency harness SHA256:")
print(
    summary["harnesses"]
    ["residency_effect"]
    ["sha256"]
)

print()
print("Summary:")
print(OUTPUT)

print()
print("Summary SHA256:")
print(
    sha256(OUTPUT)
)

print()
print(
    "PHASE 14.11L.8 A CERTIFICATION: PASS"
)
