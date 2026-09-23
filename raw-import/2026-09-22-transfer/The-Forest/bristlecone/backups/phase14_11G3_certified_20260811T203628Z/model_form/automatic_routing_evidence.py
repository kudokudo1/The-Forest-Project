"""Normalized evidence for automatic Model Form routing."""

from dataclasses import dataclass

from reasoning.control import (
    EffectiveReasoningDecision,
)


class AutomaticModelFormEvidenceError(
    ValueError
):
    """Raised when normalized Auto-routing evidence is invalid."""


def _nonempty_string(
    field_name,
    value,
):
    """Normalize one required semantic string."""

    if not isinstance(
        value,
        str,
    ):
        raise AutomaticModelFormEvidenceError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise AutomaticModelFormEvidenceError(
            f"{field_name} must be nonempty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class AutomaticModelFormEvidence:
    """One normalized routing fact produced upstream.

    signal:
        The semantic fact category.

    value:
        The normalized semantic value.

    producer:
        The Forest subsystem that established the fact.

    This object must not contain raw runtime exceptions,
    source packets, resource measurements, or Governor state.
    """

    signal: str
    value: str
    producer: str


    def __post_init__(
        self,
    ):
        object.__setattr__(
            self,
            "signal",
            _nonempty_string(
                "signal",
                self.signal,
            ),
        )

        object.__setattr__(
            self,
            "value",
            _nonempty_string(
                "value",
                self.value,
            ),
        )

        object.__setattr__(
            self,
            "producer",
            _nonempty_string(
                "producer",
                self.producer,
            ),
        )


@dataclass(
    frozen=True,
    slots=True,
)
class AutomaticModelFormRoutingInput:
    """Task/context-local evidence supplied to the Auto router.

    Reasoning is already resolved before this object exists.
    The router may observe that exact frozen decision but may
    neither resolve Reasoning again nor mutate its control state.

    evidence contains normalized semantic facts only.
    It may be empty.
    """

    task_id: str
    execution_context_id: str
    reasoning_decision: EffectiveReasoningDecision
    evidence: tuple[AutomaticModelFormEvidence, ...] = ()


    def __post_init__(
        self,
    ):
        task_id = _nonempty_string(
            "task_id",
            self.task_id,
        )

        execution_context_id = (
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            )
        )

        if not isinstance(
            self.reasoning_decision,
            EffectiveReasoningDecision,
        ):
            raise AutomaticModelFormEvidenceError(
                "reasoning_decision must be "
                "EffectiveReasoningDecision."
            )

        if not isinstance(
            self.evidence,
            tuple,
        ):
            raise AutomaticModelFormEvidenceError(
                "evidence must be a tuple."
            )

        for index, item in enumerate(
            self.evidence
        ):
            if not isinstance(
                item,
                AutomaticModelFormEvidence,
            ):
                raise AutomaticModelFormEvidenceError(
                    f"evidence[{index}] must be "
                    "AutomaticModelFormEvidence."
                )

        object.__setattr__(
            self,
            "task_id",
            task_id,
        )

        object.__setattr__(
            self,
            "execution_context_id",
            execution_context_id,
        )
