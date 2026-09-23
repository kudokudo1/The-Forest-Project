"""Prepare a ResourceRequest from already-frozen turn semantics."""

from model_form.resolution import FrozenModelFormTurn
from reasoning.control import EffectiveReasoningDecision

from .model import ResourceRequest


class ResourceRequestPreparationError(ValueError):
    """Raised when frozen turn resource preparation is invalid."""


def _task_id(value):
    if not isinstance(value, str):
        raise ResourceRequestPreparationError(
            "task_id must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ResourceRequestPreparationError(
            "task_id cannot be empty."
        )

    return normalized


def prepare_resource_request(
    *,
    task_id,
    frozen_turn,
    reasoning_decision,
    priority,
    source,
    reasons=(),
    may_defer=True,
):
    """Build resource intent from already-frozen turn decisions.

    This function does not resolve Model Form, resolve Reasoning,
    evaluate Governor policy, inspect hardware, create runtime
    sessions, perform handoff preparation, or persist state.

    Priority, source, reasons, and deferral policy are supplied
    explicitly by the caller. This function does not infer them.
    """

    normalized_task_id = _task_id(
        task_id
    )

    if not isinstance(
        frozen_turn,
        FrozenModelFormTurn,
    ):
        raise ResourceRequestPreparationError(
            "frozen_turn must be FrozenModelFormTurn."
        )

    if not isinstance(
        reasoning_decision,
        EffectiveReasoningDecision,
    ):
        raise ResourceRequestPreparationError(
            "reasoning_decision must be "
            "EffectiveReasoningDecision."
        )

    frozen_task_id = frozen_turn.task_id

    if frozen_task_id is not None:
        frozen_task_id = _task_id(
            frozen_task_id
        )

        if (
            frozen_task_id
            != normalized_task_id
        ):
            raise ResourceRequestPreparationError(
                "Frozen Model Form turn belongs to "
                "a different Task."
            )

    return ResourceRequest(
        task_id=normalized_task_id,
        execution_context_id=(
            frozen_turn.execution_context_id
        ),
        model_form=frozen_turn.form,
        reasoning_mode=reasoning_decision.mode,
        priority=priority,
        source=source,
        reasons=reasons,
        may_defer=may_defer,
    )
