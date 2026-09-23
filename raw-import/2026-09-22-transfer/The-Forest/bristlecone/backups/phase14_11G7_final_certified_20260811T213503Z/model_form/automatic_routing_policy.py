"""Pure automatic Model Form escalation policy."""

from .automatic_routing import (
    AutomaticModelFormRecommendation,
)
from .automatic_routing_evidence import (
    AutomaticModelFormRoutingInput,
)


class AutomaticModelFormPolicyError(
    ValueError
):
    """Raised when normalized routing evidence is contradictory."""


_SIGNAL_VALUES = {
    "task_complexity":
        frozenset(
            (
                "low",
                "normal",
                "high",
            )
        ),

    "known_small_failure":
        frozenset(
            (
                "absent",
                "present",
            )
        ),

    "small_capability_suitability":
        frozenset(
            (
                "sufficient",
                "insufficient",
                "unknown",
            )
        ),
}


_ESCALATION_REASONS = (
    (
        "task_complexity",
        "high",
        "high_task_complexity",
    ),
    (
        "known_small_failure",
        "present",
        "known_small_failure",
    ),
    (
        "small_capability_suitability",
        "insufficient",
        "small_capability_insufficient",
    ),
)


def _recognized_evidence_values(
    routing_input,
):
    """Return validated recognized evidence by semantic signal.

    Unknown evidence signals are deliberately ignored so that
    unrelated or future evidence cannot accidentally trigger Big.

    A recognized signal with an unsupported or contradictory value
    fails closed rather than silently changing routing semantics.
    """

    values = {}

    for item in routing_input.evidence:
        allowed = _SIGNAL_VALUES.get(
            item.signal
        )

        if allowed is None:
            continue

        if item.value not in allowed:
            raise AutomaticModelFormPolicyError(
                f"Unsupported value {item.value!r} "
                f"for recognized routing signal "
                f"{item.signal!r}."
            )

        previous = values.get(
            item.signal
        )

        if (
            previous is not None
            and previous != item.value
        ):
            raise AutomaticModelFormPolicyError(
                f"Conflicting values for routing "
                f"signal {item.signal!r}."
            )

        values[
            item.signal
        ] = item.value

    return values


def recommend_automatic_model_form(
    routing_input,
):
    """Recommend Small or Big from normalized usefulness evidence.

    Policy:
    - high task complexity recommends Big;
    - known Small semantic failure recommends Big;
    - evidence that Small lacks a required capability recommends Big;
    - otherwise recommend Small.

    Effective Reasoning is observation-only. Its mode never
    mechanically selects Model Form.

    This function performs no runtime, resource, Governor,
    binding, session, hardware, or persistence work.
    """

    if not isinstance(
        routing_input,
        AutomaticModelFormRoutingInput,
    ):
        raise AutomaticModelFormPolicyError(
            "routing_input must be "
            "AutomaticModelFormRoutingInput."
        )

    values = _recognized_evidence_values(
        routing_input
    )

    reasons = []

    for (
        signal,
        trigger_value,
        reason,
    ) in _ESCALATION_REASONS:

        if (
            values.get(signal)
            == trigger_value
        ):
            reasons.append(
                reason
            )

    if reasons:
        form = "big"
        recommendation_reasons = tuple(
            reasons
        )

    else:
        form = "small"
        recommendation_reasons = (
            "no_big_escalation_evidence",
        )

    return AutomaticModelFormRecommendation(
        task_id=routing_input.task_id,
        execution_context_id=
            routing_input.execution_context_id,
        form=form,
        reasons=recommendation_reasons,
    )
