"""Runtime-neutral Forest Governor decision contract."""

from dataclasses import dataclass

from .model import ResourceRequest


GOVERNOR_DECISION_SCHEMA_VERSION = 1

GOVERNOR_OUTCOMES = (
    "approve",
    "defer",
    "deny",
)


class GovernorDecisionError(ValueError):
    """Raised when a Forest GovernorDecision is invalid."""


def _nonempty_string(name, value):
    if not isinstance(value, str):
        raise GovernorDecisionError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise GovernorDecisionError(
            f"{name} cannot be empty."
        )

    return normalized


def normalize_governor_outcome(value):
    """Normalize approve / defer / deny."""

    if not isinstance(value, str):
        raise GovernorDecisionError(
            "Governor outcome must be a string."
        )

    normalized = value.strip().lower()

    if normalized not in GOVERNOR_OUTCOMES:
        raise GovernorDecisionError(
            "Governor outcome must be "
            "'approve', 'defer', or 'deny'."
        )

    return normalized


def _normalize_reasons(value):
    if not isinstance(value, tuple):
        raise GovernorDecisionError(
            "Governor decision reasons must be a tuple."
        )

    normalized = []

    for reason in value:
        normalized.append(
            _nonempty_string(
                "Governor decision reason",
                reason,
            )
        )

    return tuple(normalized)


@dataclass(
    frozen=True,
    slots=True,
)
class GovernorDecision:
    """Immutable resource-governance decision for one request.

    The exact ResourceRequest is retained as the object being
    decided upon.

    This object does not rewrite Model Form or Reasoning,
    schedule resources, select runtime bindings, or perform
    resource measurements.

    Semantic fallback requires a separate explicit request.
    """

    request: ResourceRequest
    outcome: str
    source: str

    reasons: tuple = ()

    schema_version: int = (
        GOVERNOR_DECISION_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != GOVERNOR_DECISION_SCHEMA_VERSION
        ):
            raise GovernorDecisionError(
                "Unsupported GovernorDecision "
                "schema version."
            )

        if not isinstance(
            self.request,
            ResourceRequest,
        ):
            raise GovernorDecisionError(
                "request must be ResourceRequest."
            )

        object.__setattr__(
            self,
            "outcome",
            normalize_governor_outcome(
                self.outcome
            ),
        )

        object.__setattr__(
            self,
            "source",
            _nonempty_string(
                "source",
                self.source,
            ),
        )

        object.__setattr__(
            self,
            "reasons",
            _normalize_reasons(
                self.reasons
            ),
        )
