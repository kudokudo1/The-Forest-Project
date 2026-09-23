"""Pure deterministic Forest resource-governor policy."""

from .availability import ResourceAvailability
from .budget import ResourceBudget
from .decision import GovernorDecision
from .model import ResourceRequest
from .requirement import ResourceRequirement


RESOURCE_DIMENSIONS = (
    "memory_mib",
    "accelerator_memory_mib",
    "cpu_threads",
)


class ResourceGovernorError(ValueError):
    """Raised when Governor evaluation inputs are invalid."""


def _decision(
    request,
    outcome,
    source,
    reasons,
):
    return GovernorDecision(
        request=request,
        outcome=outcome,
        source=source,
        reasons=tuple(reasons),
    )


def evaluate_resource_request(
    request,
    requirement,
    budget,
    availability,
    *,
    source="forest-resource-governor",
):
    """Return a pure GovernorDecision for one exact request.

    Policy order:

    1. Known requirement beyond an explicit budget -> deny.
    2. Unknown requirement -> defer when permitted, else deny.
    3. Positive requirement with unknown/insufficient current
       availability -> defer when permitted, else deny.
    4. Otherwise -> approve.

    Budget None means no explicit ceiling.
    Requirement None means required quantity is unknown.
    Availability None means current free quantity is unknown.

    A zero requirement needs no availability measurement.

    This function never rewrites Model Form or Reasoning and
    performs no scheduling, runtime I/O, hardware probing, model
    loading, or resource mutation.
    """

    if not isinstance(
        request,
        ResourceRequest,
    ):
        raise ResourceGovernorError(
            "request must be ResourceRequest."
        )

    if not isinstance(
        requirement,
        ResourceRequirement,
    ):
        raise ResourceGovernorError(
            "requirement must be ResourceRequirement."
        )

    if requirement.request is not request:
        raise ResourceGovernorError(
            "ResourceRequirement does not belong to "
            "the exact ResourceRequest."
        )

    if not isinstance(
        budget,
        ResourceBudget,
    ):
        raise ResourceGovernorError(
            "budget must be ResourceBudget."
        )

    if not isinstance(
        availability,
        ResourceAvailability,
    ):
        raise ResourceGovernorError(
            "availability must be ResourceAvailability."
        )

    if not isinstance(source, str):
        raise ResourceGovernorError(
            "source must be a string."
        )

    source = source.strip()

    if not source:
        raise ResourceGovernorError(
            "source cannot be empty."
        )

    budget_violations = []

    for name in RESOURCE_DIMENSIONS:
        required = getattr(
            requirement,
            name,
        )

        ceiling = getattr(
            budget,
            name,
        )

        if (
            required is not None
            and ceiling is not None
            and required > ceiling
        ):
            budget_violations.append(
                (
                    f"{name} requirement "
                    f"{required} exceeds policy "
                    f"ceiling {ceiling}."
                )
            )

    if budget_violations:
        return _decision(
            request,
            "deny",
            source,
            budget_violations,
        )

    unknown_requirements = [
        name
        for name in RESOURCE_DIMENSIONS
        if getattr(
            requirement,
            name,
        ) is None
    ]

    if unknown_requirements:
        reasons = [
            (
                "Resource requirement is unknown for: "
                + ", ".join(
                    unknown_requirements
                )
                + "."
            )
        ]

        if request.may_defer:
            reasons.append(
                "Request permits deferral."
            )

            return _decision(
                request,
                "defer",
                source,
                reasons,
            )

        reasons.append(
            "Request does not permit deferral."
        )

        return _decision(
            request,
            "deny",
            source,
            reasons,
        )

    unknown_availability = []
    insufficient_availability = []

    for name in RESOURCE_DIMENSIONS:
        required = getattr(
            requirement,
            name,
        )

        available = getattr(
            availability,
            name,
        )

        if required == 0:
            continue

        if available is None:
            unknown_availability.append(
                name
            )

            continue

        if available < required:
            insufficient_availability.append(
                (
                    f"{name} availability "
                    f"{available} is below "
                    f"requirement {required}."
                )
            )

    if (
        unknown_availability
        or insufficient_availability
    ):
        reasons = []

        if unknown_availability:
            reasons.append(
                (
                    "Resource availability is unknown for: "
                    + ", ".join(
                        unknown_availability
                    )
                    + "."
                )
            )

        reasons.extend(
            insufficient_availability
        )

        if request.may_defer:
            reasons.append(
                "Request permits deferral."
            )

            return _decision(
                request,
                "defer",
                source,
                reasons,
            )

        reasons.append(
            "Request does not permit deferral."
        )

        return _decision(
            request,
            "deny",
            source,
            reasons,
        )

    return _decision(
        request,
        "approve",
        source,
        (
            "Resource requirement fits policy "
            "budget and current availability.",
        ),
    )
