"""Pure Model Form handoff detection.

Detection compares the last successfully effective Model
Form for one active Task/execution context with the newly
frozen turn.

This module performs no state mutation, persistence,
runtime I/O, session work, or continuity assembly.
"""

from .handoff import (
    ModelFormHandoff,
    ModelFormHandoffError,
)
from .model import (
    ModelFormError,
    normalize_resolved_model_form,
)
from .resolution import (
    FrozenModelFormTurn,
)


def detect_model_form_handoff(
    previous_form,
    frozen_turn,
):
    """Return a semantic handoff or None.

    previous_form must represent the last successfully
    effective form for the SAME active Task and execution
    context represented by frozen_turn.

    None means there is no prior successful form yet.
    That seeds a baseline; it is not a handoff.

    Same-form execution is also not a handoff.
    """

    if not isinstance(
        frozen_turn,
        FrozenModelFormTurn,
    ):
        raise ModelFormHandoffError(
            "frozen_turn must be "
            "FrozenModelFormTurn."
        )

    if not frozen_turn.task_id:
        raise ModelFormHandoffError(
            "Handoff detection requires "
            "a frozen Task identity."
        )

    # First successfully observed form establishes
    # the context-local baseline.
    if previous_form is None:
        return None

    try:
        previous_form = (
            normalize_resolved_model_form(
                previous_form
            )
        )

    except ModelFormError as exc:
        raise ModelFormHandoffError(
            "previous_form must resolve "
            "to Small or Big."
        ) from exc

    # Same effective form means there is no
    # Model Form transition.
    if previous_form == frozen_turn.form:
        return None

    return ModelFormHandoff(
        execution_context_id=(
            frozen_turn.execution_context_id
        ),
        task_id=frozen_turn.task_id,
        from_form=previous_form,
        to_form=frozen_turn.form,
        source=frozen_turn.source,
        reasons=frozen_turn.reasons,
    )
