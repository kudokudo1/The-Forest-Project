from __future__ import annotations

import hashlib
import json
import statistics
import time
from pathlib import Path

from resources.availability import ResourceAvailability
from resources.budget import ResourceBudget
from resources.governor import evaluate_resource_request
from resources.live_providers import (
    build_live_small_resource_governor,
    live_small_availability_provider,
    no_explicit_budget_provider,
    small_requirement_provider,
)
from resources.model import ResourceRequest
from resources.requirement import ResourceRequirement


ROOT = Path("/home/user/The-Forest/bristlecone")
OUTPUT = (
    ROOT
    / "benchmarks/phase14_11L/l8_governor_raw.json"
)

PURE_ITERATIONS = 20_000
AVAILABILITY_ITERATIONS = 1_000
BUDGET_ITERATIONS = 5_000
REQUIREMENT_ITERATIONS = 20
PIPELINE_ITERATIONS = 20


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def request(
    *,
    name,
    may_defer,
    priority="standard",
):
    return ResourceRequest(
        task_id=f"l8-{name}",
        execution_context_id=f"ctx-l8-{name}",
        model_form="small",
        reasoning_mode="normal",
        priority=priority,
        source="phase14_11L8",
        reasons=("Governor benchmark",),
        may_defer=may_defer,
    )


def requirement(
    req,
    *,
    memory,
    accelerator=0,
    cpu=1,
):
    return ResourceRequirement(
        request=req,
        source="l8-synthetic-requirement",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


def budget(
    *,
    memory=None,
    accelerator=None,
    cpu=None,
):
    return ResourceBudget(
        source="l8-synthetic-budget",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


def availability(
    *,
    memory,
    accelerator=0,
    cpu=8,
):
    return ResourceAvailability(
        source="l8-synthetic-availability",
        memory_mib=memory,
        accelerator_memory_mib=accelerator,
        cpu_threads=cpu,
    )


def timing_stats(values_ns):
    ordered = sorted(values_ns)
    count = len(ordered)

    p95_index = max(
        0,
        min(
            count - 1,
            int((count * 0.95) + 0.999999) - 1,
        ),
    )

    return {
        "count": count,
        "median_ns": statistics.median(ordered),
        "mean_ns": statistics.mean(ordered),
        "stdev_ns": (
            statistics.stdev(ordered)
            if count > 1
            else 0.0
        ),
        "min_ns": ordered[0],
        "max_ns": ordered[-1],
        "p95_ns": ordered[p95_index],
        "median_us": statistics.median(ordered) / 1_000,
        "mean_us": statistics.mean(ordered) / 1_000,
    }


def benchmark_callable(
    callback,
    iterations,
):
    samples = []

    for _ in range(iterations):
        start = time.perf_counter_ns()
        callback()
        end = time.perf_counter_ns()

        samples.append(
            end - start
        )

    return samples


require(
    not OUTPUT.exists(),
    f"Refusing to overwrite existing artifact: {OUTPUT}",
)


# ============================================================
# L.8A / L.8F — PURE POLICY CASES
# ============================================================

cases = {}


def add_case(
    name,
    *,
    may_defer,
    req_memory,
    budget_memory,
    available_memory,
    expected,
    req_accelerator=0,
    available_accelerator=0,
    req_cpu=1,
    available_cpu=8,
):
    req = request(
        name=name,
        may_defer=may_defer,
    )

    reqmt = requirement(
        req,
        memory=req_memory,
        accelerator=req_accelerator,
        cpu=req_cpu,
    )

    bud = budget(
        memory=budget_memory,
    )

    avail = availability(
        memory=available_memory,
        accelerator=available_accelerator,
        cpu=available_cpu,
    )

    decision = evaluate_resource_request(
        req,
        reqmt,
        bud,
        avail,
        source="phase14_11L8-pure",
    )

    require(
        decision.outcome == expected,
        (
            f"{name}: expected {expected}, "
            f"got {decision.outcome}"
        ),
    )

    def run():
        result = evaluate_resource_request(
            req,
            reqmt,
            bud,
            avail,
            source="phase14_11L8-pure",
        )

        if result.outcome != expected:
            raise RuntimeError(
                f"{name}: outcome changed"
            )

    samples = benchmark_callable(
        run,
        PURE_ITERATIONS,
    )

    cases[name] = {
        "expected_outcome": expected,
        "may_defer": may_defer,
        "requirement_memory_mib": req_memory,
        "budget_memory_mib": budget_memory,
        "availability_memory_mib":
            available_memory,
        "timing": timing_stats(samples),
    }

    print(
        f"PASS {name}: "
        f"{expected} "
        f"median="
        f"{cases[name]['timing']['median_us']:.3f} us"
    )


print("=== L.8 PURE GOVERNOR POLICY ===")

add_case(
    "approve",
    may_defer=False,
    req_memory=1024,
    budget_memory=None,
    available_memory=8192,
    expected="approve",
)

add_case(
    "budget-deny-deferrable",
    may_defer=True,
    req_memory=6144,
    budget_memory=4096,
    available_memory=16384,
    expected="deny",
)

add_case(
    "budget-deny-nondeferrable",
    may_defer=False,
    req_memory=6144,
    budget_memory=4096,
    available_memory=16384,
    expected="deny",
)

add_case(
    "unknown-requirement-defer",
    may_defer=True,
    req_memory=None,
    budget_memory=None,
    available_memory=8192,
    expected="defer",
)

add_case(
    "unknown-requirement-deny",
    may_defer=False,
    req_memory=None,
    budget_memory=None,
    available_memory=8192,
    expected="deny",
)

add_case(
    "insufficient-availability-defer",
    may_defer=True,
    req_memory=1024,
    budget_memory=None,
    available_memory=512,
    expected="defer",
)

add_case(
    "insufficient-availability-deny",
    may_defer=False,
    req_memory=1024,
    budget_memory=None,
    available_memory=512,
    expected="deny",
)

add_case(
    "unknown-availability-defer",
    may_defer=True,
    req_memory=1024,
    budget_memory=None,
    available_memory=None,
    expected="defer",
)

add_case(
    "unknown-availability-deny",
    may_defer=False,
    req_memory=1024,
    budget_memory=None,
    available_memory=None,
    expected="deny",
)


# Zero requirement must not require availability.
zero_req = request(
    name="zero-bypass",
    may_defer=False,
)

zero_requirement = requirement(
    zero_req,
    memory=0,
    accelerator=0,
    cpu=1,
)

zero_budget = budget()

zero_availability = availability(
    memory=None,
    accelerator=None,
    cpu=1,
)

zero_decision = evaluate_resource_request(
    zero_req,
    zero_requirement,
    zero_budget,
    zero_availability,
    source="phase14_11L8-zero-bypass",
)

require(
    zero_decision.outcome == "approve",
    "Zero-requirement bypass failed",
)

print(
    "PASS zero-requirement bypass: approve"
)


# ============================================================
# PRIORITY SEMANTICS
# ============================================================

priority_outcomes = {}

for priority in (
    "background",
    "standard",
    "interactive",
):
    req = request(
        name=f"priority-{priority}",
        may_defer=False,
        priority=priority,
    )

    decision = evaluate_resource_request(
        req,
        requirement(
            req,
            memory=1024,
        ),
        budget(),
        availability(
            memory=8192,
        ),
        source="phase14_11L8-priority",
    )

    priority_outcomes[
        priority
    ] = decision.outcome


require(
    set(priority_outcomes.values())
    == {"approve"},
    (
        "Priority unexpectedly changed "
        "pure Governor approve behavior"
    ),
)

print(
    "PASS priority semantic check:",
    priority_outcomes,
)


# ============================================================
# LIVE REQUEST
# ============================================================

live_request = request(
    name="live-small",
    may_defer=False,
)


# ============================================================
# L.8B — LIVE AVAILABILITY PROVIDER
# ============================================================

print()
print("=== L.8 LIVE AVAILABILITY PROVIDER ===")

availability_samples = []
availability_timings = []

for _ in range(
    AVAILABILITY_ITERATIONS
):
    start = time.perf_counter_ns()

    observed = (
        live_small_availability_provider(
            live_request
        )
    )

    end = time.perf_counter_ns()

    availability_timings.append(
        end - start
    )

    availability_samples.append(
        observed
    )


availability_memories = [
    value.memory_mib
    for value in availability_samples
]

availability_threads = sorted(
    {
        value.cpu_threads
        for value in availability_samples
    }
)

require(
    all(
        value.accelerator_memory_mib == 0
        for value in availability_samples
    ),
    "Live Small accelerator availability changed",
)

availability_stats = timing_stats(
    availability_timings
)

print(
    "PASS live availability:"
)

print(
    " median:",
    f"{availability_stats['median_us']:.3f} us",
)

print(
    " memory MiB range:",
    min(availability_memories),
    "to",
    max(availability_memories),
)

print(
    " CPU threads:",
    availability_threads,
)


# ============================================================
# L.8C — LIVE BUDGET PROVIDER
# ============================================================

print()
print("=== L.8 LIVE BUDGET PROVIDER ===")

budget_timings = []

for _ in range(
    BUDGET_ITERATIONS
):
    start = time.perf_counter_ns()

    live_budget = (
        no_explicit_budget_provider(
            live_request
        )
    )

    end = time.perf_counter_ns()

    budget_timings.append(
        end - start
    )

    require(
        live_budget.memory_mib is None
        and live_budget.accelerator_memory_mib is None
        and live_budget.cpu_threads is None,
        "Live Small budget unexpectedly established a ceiling",
    )


budget_stats = timing_stats(
    budget_timings
)

print(
    "PASS no-explicit-budget:"
)

print(
    " median:",
    f"{budget_stats['median_us']:.3f} us",
)


# ============================================================
# L.8D — RESIDENCY-AWARE REQUIREMENT PROVIDER
# ============================================================

print()
print("=== L.8 LIVE REQUIREMENT PROVIDER ===")

requirement_timings = []
requirement_memories = []

for _ in range(
    REQUIREMENT_ITERATIONS
):
    start = time.perf_counter_ns()

    live_requirement = (
        small_requirement_provider(
            live_request
        )
    )

    end = time.perf_counter_ns()

    requirement_timings.append(
        end - start
    )

    require(
        live_requirement.accelerator_memory_mib == 0,
        "Live Small accelerator requirement changed",
    )

    require(
        live_requirement.cpu_threads == 1,
        "Live Small CPU requirement changed",
    )

    requirement_memories.append(
        live_requirement.memory_mib
    )


requirement_stats = timing_stats(
    requirement_timings
)

print(
    "PASS residency-aware requirement:"
)

print(
    " median:",
    f"{requirement_stats['median_us']:.3f} us",
)

print(
    " memory requirement MiB values:",
    sorted(
        set(requirement_memories)
    ),
)


# ============================================================
# L.8E — WHOLE LIVE GOVERNOR PIPELINE
# ============================================================

print()
print("=== L.8 WHOLE LIVE GOVERNOR PIPELINE ===")

pipeline = (
    build_live_small_resource_governor()
)

pipeline_timings = []
pipeline_outcomes = []

for _ in range(
    PIPELINE_ITERATIONS
):
    start = time.perf_counter_ns()

    decision = pipeline(
        live_request
    )

    end = time.perf_counter_ns()

    pipeline_timings.append(
        end - start
    )

    pipeline_outcomes.append(
        decision.outcome
    )


pipeline_stats = timing_stats(
    pipeline_timings
)

outcome_counts = {
    outcome: pipeline_outcomes.count(
        outcome
    )
    for outcome in sorted(
        set(pipeline_outcomes)
    )
}

print(
    "PASS whole live pipeline:"
)

print(
    " median:",
    f"{pipeline_stats['median_us']:.3f} us",
)

print(
    " outcomes:",
    outcome_counts,
)


# ============================================================
# EVIDENCE
# ============================================================

source_files = {
    name: ROOT / path
    for name, path in {
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
    }.items()
}


payload = {
    "phase": "14.11L.8",
    "scenario":
        "resource-governor-performance",
    "real_inference_executed": False,
    "runtime_session_created": False,
    "production_state_modified": False,
    "iterations": {
        "pure_policy_per_case":
            PURE_ITERATIONS,
        "live_availability":
            AVAILABILITY_ITERATIONS,
        "live_budget":
            BUDGET_ITERATIONS,
        "live_requirement":
            REQUIREMENT_ITERATIONS,
        "whole_live_pipeline":
            PIPELINE_ITERATIONS,
    },
    "pure_policy_cases": cases,
    "zero_requirement_bypass":
        zero_decision.outcome,
    "priority_outcomes":
        priority_outcomes,
    "live_availability": {
        "timing":
            availability_stats,
        "memory_mib_min":
            min(availability_memories),
        "memory_mib_max":
            max(availability_memories),
        "cpu_threads":
            availability_threads,
        "accelerator_memory_mib":
            0,
    },
    "live_budget": {
        "timing":
            budget_stats,
        "memory_mib":
            None,
        "accelerator_memory_mib":
            None,
        "cpu_threads":
            None,
    },
    "live_requirement": {
        "timing":
            requirement_stats,
        "memory_mib_values":
            sorted(
                set(requirement_memories)
            ),
        "accelerator_memory_mib":
            0,
        "cpu_threads":
            1,
    },
    "whole_live_pipeline": {
        "timing":
            pipeline_stats,
        "outcomes":
            outcome_counts,
    },
    "source_sha256": {
        name: sha256(path)
        for name, path
        in source_files.items()
    },
    "status": "success",
}


OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print()
print("=== L.8 RESULT ===")

print(
    "Pure Governor approve median:",
    f"{cases['approve']['timing']['median_us']:.3f} us",
)

print(
    "Live availability median:",
    f"{availability_stats['median_us']:.3f} us",
)

print(
    "Live budget median:",
    f"{budget_stats['median_us']:.3f} us",
)

print(
    "Residency-aware requirement median:",
    f"{requirement_stats['median_us']:.3f} us",
)

print(
    "Whole live pipeline median:",
    f"{pipeline_stats['median_us']:.3f} us",
)

print(
    "Inference executed: False"
)

print(
    "Production state modified: False"
)

print()
print("Evidence:")
print(OUTPUT)

print()
print("Evidence SHA256:")
print(
    sha256(OUTPUT)
)

print()
print("PHASE 14.11L.8 GOVERNOR BENCHMARK: PASS")
