"""Runtime-neutral automatic Model Form routing contracts."""

from dataclasses import dataclass

from .registry import (
    normalize_resolved_model_form,
)


class AutomaticModelFormRoutingError(
    ValueError
):
    """Raised when automatic Model Form routing data is invalid."""


def _nonempty_string(
    field_name,
    value,
):
    """Return one stripped nonempty semantic string."""

    if not isinstance(
        value,
        str,
    ):
        raise AutomaticModelFormRoutingError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise AutomaticModelFormRoutingError(
            f"{field_name} must be nonempty."
        )

    return normalized


def _recommendation_form(
    value,
):
    """Require one resolved Small/Big Model Form."""

    try:
        form = normalize_resolved_model_form(
            value
        )

    except Exception as exc:
        raise AutomaticModelFormRoutingError(
            "form must be a resolved Model Form."
        ) from exc

    if form not in (
        "small",
        "big",
    ):
        raise AutomaticModelFormRoutingError(
            "Automatic recommendation form "
            "must be Small or Big."
        )

    return form


def _recommendation_reasons(
    value,
):
    """Require an ordered nonempty tuple of semantic reasons."""

    if not isinstance(
        value,
        tuple,
    ):
        raise AutomaticModelFormRoutingError(
            "reasons must be a tuple."
        )

    if not value:
        raise AutomaticModelFormRoutingError(
            "reasons must contain at least one reason."
        )

    normalized = []

    for index, reason in enumerate(
        value
    ):
        normalized.append(
            _nonempty_string(
                f"reasons[{index}]",
                reason,
            )
        )

    return tuple(
        normalized
    )


@dataclass(
    frozen=True,
    slots=True,
)
class AutomaticModelFormRecommendation:
    """One Task/context-local recommendation from the Auto router.

    This object expresses usefulness only.

    It does not contain:
    - Model Form precedence;
    - Model Form semantic source;
    - runtime bindings or sessions;
    - Governor permission;
    - resource availability;
    - Reasoning control mutation.
    """

    task_id: str
    execution_context_id: str
    form: str
    reasons: tuple[str, ...]


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

        form = _recommendation_form(
            self.form
        )

        reasons = _recommendation_reasons(
            self.reasons
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

        object.__setattr__(
            self,
            "form",
            form,
        )

        object.__setattr__(
            self,
            "reasons",
            reasons,
        )
