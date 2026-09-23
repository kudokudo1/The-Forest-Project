"""Model Form handoff semantics.

A handoff records an actual change in effective Model Form
for one Forest execution context.

It deliberately contains no runtime adapter, vendor model,
session ID, KV cache, or continuity payload.

Runtime execution remains represented by FrozenModelFormTurn.
Continuity is defined separately.
"""

from dataclasses import dataclass

from .model import (
    ModelFormError,
    normalize_resolved_model_form,
)


MODEL_FORM_HANDOFF_SCHEMA_VERSION = 1


class ModelFormHandoffError(
    ModelFormError
):
    """Invalid Model Form handoff."""


def _nonempty_string(
    name,
    value,
):
    if not isinstance(
        value,
        str,
    ):
        raise ModelFormHandoffError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelFormHandoffError(
            f"{name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ModelFormHandoff:
    """One semantic Small/Big execution-form transition.

    A handoff preserves Tree, execution-context, and Task
    identity while recording that the effective execution
    form changed.

    Small -> Small and Big -> Big are not handoffs.
    """

    execution_context_id: str
    task_id: str
    from_form: str
    to_form: str
    source: str
    reasons: tuple = ()
    schema_version: int = (
        MODEL_FORM_HANDOFF_SCHEMA_VERSION
    )

    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != MODEL_FORM_HANDOFF_SCHEMA_VERSION
        ):
            raise ModelFormHandoffError(
                "Unsupported Model Form "
                "handoff schema version."
            )

        execution_context_id = (
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            )
        )

        task_id = _nonempty_string(
            "task_id",
            self.task_id,
        )

        try:
            from_form = (
                normalize_resolved_model_form(
                    self.from_form
                )
            )

            to_form = (
                normalize_resolved_model_form(
                    self.to_form
                )
            )

        except ModelFormError as exc:
            raise ModelFormHandoffError(
                "Model Form handoff forms "
                "must resolve to Small or Big."
            ) from exc

        if from_form == to_form:
            raise ModelFormHandoffError(
                "Model Form handoff requires "
                "an actual form change."
            )

        source = _nonempty_string(
            "source",
            self.source,
        )

        try:
            reasons = tuple(
                self.reasons
            )

        except TypeError as exc:
            raise ModelFormHandoffError(
                "reasons must be iterable."
            ) from exc

        normalized_reasons = tuple(
            _nonempty_string(
                "reason",
                reason,
            )
            for reason in reasons
        )

        object.__setattr__(
            self,
            "execution_context_id",
            execution_context_id,
        )

        object.__setattr__(
            self,
            "task_id",
            task_id,
        )

        object.__setattr__(
            self,
            "from_form",
            from_form,
        )

        object.__setattr__(
            self,
            "to_form",
            to_form,
        )

        object.__setattr__(
            self,
            "source",
            source,
        )

        object.__setattr__(
            self,
            "reasons",
            normalized_reasons,
        )
