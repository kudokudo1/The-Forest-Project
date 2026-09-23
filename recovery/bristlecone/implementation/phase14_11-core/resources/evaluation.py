"""Runtime-neutral Forest resource evaluation composition."""

from dataclasses import dataclass

from .availability import ResourceAvailability
from .budget import ResourceBudget
from .decision import GovernorDecision
from .governor import evaluate_resource_request
from .model import ResourceRequest
from .requirement import ResourceRequirement


class ResourceEvaluationError(RuntimeError):
    """Raised when resource-evaluation composition is invalid."""


def _provider(
    value,
    field_name,
):
    """Require one callable resource provider."""

    if not callable(value):
        raise ResourceEvaluationError(
            f"{field_name} must be callable."
        )

    return value


def evaluate_resource_request_with_providers(
    request,
    *,
    requirement_provider,
    budget_provider,
    availability_provider,
    source="forest-resource-governor",
):
    """Evaluate one exact ResourceRequest through typed providers.

    This function performs composition only.

    It does not:
    - resolve Model Form;
    - resolve Reasoning;
    - inspect hardware itself;
    - invent resource quantities;
    - create runtime sessions;
    - perform scheduling;
    - rewrite or downgrade the request.
    """

    if not isinstance(
        request,
        ResourceRequest,
    ):
        raise ResourceEvaluationError(
            "request must be ResourceRequest."
        )

    requirement_provider = _provider(
        requirement_provider,
        "requirement_provider",
    )

    budget_provider = _provider(
        budget_provider,
        "budget_provider",
    )

    availability_provider = _provider(
        availability_provider,
        "availability_provider",
    )


    try:
        requirement = requirement_provider(
            request
        )

    except Exception as exc:
        raise ResourceEvaluationError(
            "Resource requirement provider failed."
        ) from exc


    if not isinstance(
        requirement,
        ResourceRequirement,
    ):
        raise ResourceEvaluationError(
            "Resource requirement provider must "
            "return ResourceRequirement."
        )


    if requirement.request is not request:
        raise ResourceEvaluationError(
            "ResourceRequirement does not belong "
            "to the exact ResourceRequest."
        )


    try:
        budget = budget_provider(
            request
        )

    except Exception as exc:
        raise ResourceEvaluationError(
            "Resource budget provider failed."
        ) from exc


    if not isinstance(
        budget,
        ResourceBudget,
    ):
        raise ResourceEvaluationError(
            "Resource budget provider must "
            "return ResourceBudget."
        )


    try:
        availability = availability_provider(
            request
        )

    except Exception as exc:
        raise ResourceEvaluationError(
            "Resource availability provider failed."
        ) from exc


    if not isinstance(
        availability,
        ResourceAvailability,
    ):
        raise ResourceEvaluationError(
            "Resource availability provider must "
            "return ResourceAvailability."
        )


    try:
        decision = evaluate_resource_request(
            request,
            requirement,
            budget,
            availability,
            source=source,
        )

    except Exception as exc:
        raise ResourceEvaluationError(
            "Forest resource Governor evaluation failed."
        ) from exc


    if not isinstance(
        decision,
        GovernorDecision,
    ):
        raise ResourceEvaluationError(
            "Forest resource Governor must return "
            "GovernorDecision."
        )


    if decision.request is not request:
        raise ResourceEvaluationError(
            "GovernorDecision does not belong "
            "to the exact ResourceRequest."
        )


    return decision


@dataclass(
    frozen=True,
    slots=True,
)
class ResourceEvaluationPipeline:
    """Callable provider composition for the F.5B Governor seam."""

    requirement_provider: object
    budget_provider: object
    availability_provider: object
    source: str = "forest-resource-governor"


    def __post_init__(
        self,
    ):
        _provider(
            self.requirement_provider,
            "requirement_provider",
        )

        _provider(
            self.budget_provider,
            "budget_provider",
        )

        _provider(
            self.availability_provider,
            "availability_provider",
        )


    def __call__(
        self,
        request,
    ):
        return (
            evaluate_resource_request_with_providers(
                request,
                requirement_provider=
                    self.requirement_provider,
                budget_provider=
                    self.budget_provider,
                availability_provider=
                    self.availability_provider,
                source=self.source,
            )
        )
