"""Live resource providers for locally executed Forest requests.

The providers in this module observe or describe resources only.
They do not select Model Form, change Reasoning, schedule work,
load models, create runtime sessions, or grant permission.

Phase 14.11J calibrated binding-0001 / Small against:
    bristlecone-qwen35:4b-64k
    Ollama runtime residency: 5.6 GB
    observed MemAvailable delta: 5311 MiB
    runtime: 100% CPU
    context: 64000

The 6144 MiB requirement is a conservative operational floor,
not an assertion that the model's exact allocation is 6144 MiB.
"""

from __future__ import annotations

import os
from pathlib import Path

from .availability import ResourceAvailability
from .budget import ResourceBudget
from .evaluation import ResourceEvaluationPipeline
from .model import ResourceRequest
from .requirement import ResourceRequirement


SMALL_MODEL_FORM = "small"

SMALL_BINDING_ID = "binding-0001"

SMALL_MODEL_NAME = (
    "bristlecone-qwen35:4b-64k"
)

SMALL_MEMORY_REQUIREMENT_MIB = 6144

SMALL_ACCELERATOR_MEMORY_REQUIREMENT_MIB = 0

SMALL_CPU_THREAD_REQUIREMENT = 1


class LiveResourceProviderError(
    ValueError,
):
    """Raised when live resource observation cannot be trusted."""


def _small_request(
    request,
):
    if not isinstance(
        request,
        ResourceRequest,
    ):
        raise LiveResourceProviderError(
            "request must be ResourceRequest."
        )

    if request.model_form != SMALL_MODEL_FORM:
        raise LiveResourceProviderError(
            "This provider currently supports only "
            "the calibrated Small model form."
        )

    return request


def small_requirement_provider(
    request,
):
    """Return the calibrated requirement for current Small."""

    request = _small_request(
        request
    )

    return ResourceRequirement(
        request=request,
        source=(
            "binding-0001-small-calibration-"
            "2026-08-11"
        ),
        memory_mib=(
            SMALL_MEMORY_REQUIREMENT_MIB
        ),
        accelerator_memory_mib=(
            SMALL_ACCELERATOR_MEMORY_REQUIREMENT_MIB
        ),
        cpu_threads=(
            SMALL_CPU_THREAD_REQUIREMENT
        ),
    )


def no_explicit_budget_provider(
    request,
):
    """Return Forest's current lack of explicit resource ceilings."""

    _small_request(
        request
    )

    return ResourceBudget(
        source=(
            "forest-no-explicit-small-"
            "resource-ceiling"
        ),
        memory_mib=None,
        accelerator_memory_mib=None,
        cpu_threads=None,
    )


def _available_memory_mib():
    """Read Linux MemAvailable from /proc/meminfo."""

    path = Path(
        "/proc/meminfo"
    )

    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except OSError as exc:
        raise LiveResourceProviderError(
            "Could not read /proc/meminfo."
        ) from exc

    for line in lines:
        if not line.startswith(
            "MemAvailable:"
        ):
            continue

        parts = line.split()

        if (
            len(parts) < 2
            or not parts[1].isdigit()
        ):
            break

        kib = int(
            parts[1]
        )

        return kib // 1024

    raise LiveResourceProviderError(
        "Linux MemAvailable was not available."
    )


def _available_cpu_threads():
    """Return CPU threads schedulable by this process."""

    try:
        threads = len(
            os.sched_getaffinity(0)
        )
    except (
        AttributeError,
        OSError,
    ):
        threads = (
            os.cpu_count()
        )

    if (
        not isinstance(threads, int)
        or isinstance(threads, bool)
        or threads <= 0
    ):
        raise LiveResourceProviderError(
            "Could not establish available CPU threads."
        )

    return threads


def live_small_availability_provider(
    request,
):
    """Observe resources available to current local Small."""

    _small_request(
        request
    )

    return ResourceAvailability(
        source="linux-live-small-observation",
        memory_mib=(
            _available_memory_mib()
        ),
        # Small is calibrated as CPU-only.  Its accelerator
        # requirement is explicitly zero.
        accelerator_memory_mib=0,
        cpu_threads=(
            _available_cpu_threads()
        ),
    )


def build_live_small_resource_governor():
    """Build the real resource Governor pipeline for Small."""

    return ResourceEvaluationPipeline(
        requirement_provider=(
            small_requirement_provider
        ),
        budget_provider=(
            no_explicit_budget_provider
        ),
        availability_provider=(
            live_small_availability_provider
        ),
        source=(
            "forest-live-small-resource-governor"
        ),
    )
