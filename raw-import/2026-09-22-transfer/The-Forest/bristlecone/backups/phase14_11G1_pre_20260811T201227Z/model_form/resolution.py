"""Per-turn Forest Model Form resolution.

This module resolves Model Form exactly once for one
meaningful execution-context turn, then freezes the
selected runtime binding for reuse by session creation,
stale-session recovery, and retry.

It performs no runtime I/O.
"""

from dataclasses import dataclass
from typing import Optional

from .model import (
    ModelFormDecision,
    ModelFormError,
    normalize_resolved_model_form,
)

from .control import (
    ModelFormControlState,
)

from .registry import (
    ModelBinding,
    ModelBindingRegistry,
    ModelBindingRegistryError,
)


class ModelFormResolutionError(ModelFormError):
    """Model Form could not be resolved for a turn."""


def _optional_nonempty_string(
    value,
    field_name,
):
    if value is None:
        return None

    if not isinstance(value, str):
        raise ModelFormResolutionError(
            f"{field_name} must be a string "
            "or None."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelFormResolutionError(
            f"{field_name} cannot be empty "
            "when provided."
        )

    return normalized


def _resolved_form_input(
    value,
    field_name,
):
    """Normalize one explicit Small / Big input."""

    if value is None:
        return None

    try:
        return normalize_resolved_model_form(
            value
        )

    except ModelFormError as exc:
        raise ModelFormResolutionError(
            f"{field_name} must resolve to "
            "Small or Big."
        ) from exc


@dataclass(
    frozen=True,
    slots=True,
)
class FrozenModelFormTurn:
    """Frozen Model Form execution choice for one turn.

    ModelFormDecision remains runtime-neutral.

    ModelBinding supplies the immutable runtime
    configuration selected exactly once for this turn.

    A retry must reuse this object rather than resolving
    Model Form or consulting the registry again.
    """

    decision: ModelFormDecision
    binding: ModelBinding
    task_id: Optional[str] = None

    def __post_init__(self):
        if not isinstance(
            self.decision,
            ModelFormDecision,
        ):
            raise ModelFormResolutionError(
                "decision must be "
                "ModelFormDecision."
            )

        if not isinstance(
            self.binding,
            ModelBinding,
        ):
            raise ModelFormResolutionError(
                "binding must be ModelBinding."
            )

        normalized_task_id = (
            _optional_nonempty_string(
                self.task_id,
                "task_id",
            )
        )

        object.__setattr__(
            self,
            "task_id",
            normalized_task_id,
        )

    @property
    def execution_context_id(self):
        return (
            self.decision
            .execution_context_id
        )

    @property
    def form(self):
        return self.decision.form

    @property
    def source(self):
        return self.decision.source

    @property
    def reasons(self):
        return self.decision.reasons

    @property
    def binding_id(self):
        return self.binding.binding_id

    @property
    def adapter(self):
        return self.binding.adapter

    @property
    def runtime_state(self):
        """Return a detached mutable runtime-state copy."""
        return self.binding.runtime_state()


def resolve_model_form_turn(
    control,
    registry,
    *,
    task_id=None,
    exact_form=None,
    automatic_form=None,
):
    """Resolve and freeze Model Form exactly once.

    Precedence:

        exact-turn override
        matching Task override
        pinned baseline
        supplied Auto-policy result
        Small safe default

    `automatic_form` is deliberately supplied by the
    caller. The automatic escalation router belongs to
    a later phase and is not implemented here.

    Availability is determined by registry lookup after
    form resolution. An explicitly selected unbound form
    fails rather than silently becoming another form.
    """

    if not isinstance(
        control,
        ModelFormControlState,
    ):
        raise ModelFormResolutionError(
            "control must be "
            "ModelFormControlState."
        )

    if not isinstance(
        registry,
        ModelBindingRegistry,
    ):
        raise ModelFormResolutionError(
            "registry must be "
            "ModelBindingRegistry."
        )

    task_id = _optional_nonempty_string(
        task_id,
        "task_id",
    )

    exact_form = _resolved_form_input(
        exact_form,
        "exact_form",
    )

    automatic_form = _resolved_form_input(
        automatic_form,
        "automatic_form",
    )

    resolved_form = None
    source = None
    reasons = ()

    # ----------------------------------------------
    # 1. Exact-turn override
    # ----------------------------------------------

    if exact_form is not None:
        resolved_form = exact_form
        source = "exact_turn"
        reasons = (
            "exact_turn_override",
        )

    # ----------------------------------------------
    # 2. Matching Task override
    # ----------------------------------------------

    elif (
        control.task_override
        is not None
        and task_id is not None
        and control.task_override.task_id
        == task_id
    ):
        resolved_form = (
            control.task_override.form
        )

        source = "task_override"

        reasons = (
            "matching_task_override",
        )

    # ----------------------------------------------
    # 3. Pinned baseline
    # ----------------------------------------------

    elif control.baseline.policy == "pinned":
        resolved_form = (
            control.baseline.form
        )

        source = "pinned_baseline"

        reasons = (
            "pinned_baseline",
        )

    # ----------------------------------------------
    # 4. Auto policy result
    # ----------------------------------------------

    elif automatic_form is not None:
        resolved_form = automatic_form
        source = "auto_policy"

        reasons = (
            "automatic_form_supplied",
        )

    # ----------------------------------------------
    # 5. Safe default while Auto router is absent
    # ----------------------------------------------

    else:
        resolved_form = "small"
        source = "safe_default"

        reasons = (
            "auto_without_escalation_router",
            "small_safe_default",
        )

    try:
        decision = ModelFormDecision(
            form=resolved_form,
            source=source,
            execution_context_id=(
                control.execution_context_id
            ),
            reasons=reasons,
        )

    except ModelFormError as exc:
        raise ModelFormResolutionError(
            "Could not create frozen "
            "Model Form decision."
        ) from exc

    # Resolve the binding exactly once.
    #
    # From this point onward, runtime preparation,
    # session creation, and retry must reuse this
    # binding rather than consulting the registry again.
    try:
        binding = registry.binding_for_form(
            decision.form
        )

    except ModelBindingRegistryError as exc:
        raise ModelFormResolutionError(
            "Resolved Model Form "
            f"{decision.form!r} has no "
            "available runtime binding."
        ) from exc

    return FrozenModelFormTurn(
        decision=decision,
        binding=binding,
        task_id=task_id,
    )
