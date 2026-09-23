from __future__ import annotations

import hashlib
import json
import statistics
import time
import urllib.request
from pathlib import Path

from resources.live_providers import (
    MIB_BYTES,
    SMALL_MEMORY_REQUIREMENT_MIB,
    SMALL_MODEL_NAME,
    small_requirement_provider,
)
from resources.model import ResourceRequest


ROOT = Path("/home/user/The-Forest/bristlecone")

OUTPUT = (
    ROOT
    / "benchmarks/phase14_11L/l8_residency_effect_raw.json"
)

ITERATIONS = 20


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


require(
    not OUTPUT.exists(),
    f"Refusing to overwrite existing artifact: {OUTPUT}",
)


request = ResourceRequest(
    task_id="l8-resident-small",
    execution_context_id="ctx-l8-resident-small",
    model_form="small",
    reasoning_mode="normal",
    priority="standard",
    source="phase14_11L8-residency",
    reasons=(
        "Resident requirement benchmark",
    ),
    may_defer=False,
)


print("=== L.8 RESIDENT SMALL EFFECT ===")


# ------------------------------------------------------------
# Confirm exact Small residency through the same Ollama endpoint
# used by the production requirement provider.
# ------------------------------------------------------------

with urllib.request.urlopen(
    "http://127.0.0.1:11434/api/ps",
    timeout=2,
) as response:
    payload = json.load(response)


models = payload.get(
    "models",
    [],
)

match = None

for model in models:
    if SMALL_MODEL_NAME in (
        model.get("name"),
        model.get("model"),
    ):
        match = model
        break


require(
    match is not None,
    (
        "Small is not resident. "
        "Resident benchmark cannot run."
    ),
)


resident_bytes = match.get(
    "size"
)

require(
    isinstance(resident_bytes, int)
    and not isinstance(resident_bytes, bool)
    and resident_bytes >= 0,
    "Resident Small size is invalid.",
)


# ------------------------------------------------------------
# Independently calculate what production should require.
# ------------------------------------------------------------

calibrated_bytes = (
    SMALL_MEMORY_REQUIREMENT_MIB
    * MIB_BYTES
)

remaining_bytes = max(
    0,
    calibrated_bytes - resident_bytes,
)

expected_memory_mib = (
    remaining_bytes
    + MIB_BYTES
    - 1
) // MIB_BYTES


print(
    "Model:",
    SMALL_MODEL_NAME,
)

print(
    "Resident size bytes:",
    resident_bytes,
)

print(
    "Calibrated floor MiB:",
    SMALL_MEMORY_REQUIREMENT_MIB,
)

print(
    "Expected remaining requirement MiB:",
    expected_memory_mib,
)


# ------------------------------------------------------------
# Measure the real residency-aware requirement provider.
# ------------------------------------------------------------

timings_ns = []
memory_values = []


for _ in range(
    ITERATIONS
):
    start = time.perf_counter_ns()

    result = (
        small_requirement_provider(
            request
        )
    )

    end = time.perf_counter_ns()

    timings_ns.append(
        end - start
    )

    memory_values.append(
        result.memory_mib
    )

    require(
        result.memory_mib
        == expected_memory_mib,
        "Resident memory requirement mismatch.",
    )

    require(
        result.accelerator_memory_mib == 0,
        "Accelerator requirement changed.",
    )

    require(
        result.cpu_threads == 1,
        "CPU requirement changed.",
    )


median_ns = statistics.median(
    timings_ns
)

mean_ns = statistics.mean(
    timings_ns
)

stdev_ns = statistics.stdev(
    timings_ns
)


print()
print(
    "=== RESIDENT REQUIREMENT RESULT ==="
)

print(
    "Observed memory MiB values:",
    sorted(
        set(memory_values)
    ),
)

print(
    "Median provider latency:",
    f"{median_ns / 1000:.3f} us",
)

print(
    "Mean provider latency:",
    f"{mean_ns / 1000:.3f} us",
)


# ------------------------------------------------------------
# Freeze evidence.
# ------------------------------------------------------------

payload = {
    "phase":
        "14.11L.8",
    "scenario":
        "residency-aware-requirement-effect",
    "model":
        SMALL_MODEL_NAME,
    "resident":
        True,
    "resident_size_bytes":
        resident_bytes,
    "calibrated_floor_mib":
        SMALL_MEMORY_REQUIREMENT_MIB,
    "expected_remaining_requirement_mib":
        expected_memory_mib,
    "observed_memory_mib_values":
        sorted(
            set(memory_values)
        ),
    "accelerator_memory_mib":
        0,
    "cpu_threads":
        1,
    "iterations":
        ITERATIONS,
    "provider_timing": {
        "median_ns":
            median_ns,
        "mean_ns":
            mean_ns,
        "stdev_ns":
            stdev_ns,
        "median_us":
            median_ns / 1000,
        "mean_us":
            mean_ns / 1000,
    },
    "comparison_nonresident_requirement_mib":
        6144,
    "real_inference_executed_by_this_script":
        False,
    "production_state_modified":
        False,
    "status":
        "success",
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
print("Evidence:")
print(OUTPUT)

print()
print("Evidence SHA256:")
print(
    sha256(OUTPUT)
)

print()
print(
    "L.8 RESIDENCY EFFECT: PASS"
)
