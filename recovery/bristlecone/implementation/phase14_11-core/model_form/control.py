"""Execution-context-local Forest Model Form control state."""

from dataclasses import dataclass
from typing import Optional

from .model import (
    ModelFormError,
    normalize_resolved_model_form,
)


MODEL_FORM_CONTROL_SCHEMA_VERSION = 1

# Compatibility fallback only.
#
# The core does not attach presentation meaning such as
# "Main", "Ortet", "Clone", or "Ramet" to this identifier.
#
# A future execution-context lifecycle subsystem may issue
# persistent opaque IDs instead.
DEFAULT_EXECUTION_CONTEXT_ID = "ctx-default"

MODEL_FORM_BASELINE_POLICIES = (
    "auto",
    "pinned",
)


class ModelFormControlError(ModelFormError):
    """Raised when Forest Model Form control state is invalid."""


def _normalize_control_form(value):
    """Normalize a resolved form at the control API boundary."""

    try:
        return normalize_resolved_model_form(
            value
        )

    except ModelFormError as exc:
        raise ModelFormControlError(
            str(exc)
        ) from exc


def _nonempty_string(
    name,
    value,
):
    if not isinstance(value, str):
        raise ModelFormControlError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelFormControlError(
            f"{name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ModelFormBaseline:
    """Durable baseline for one execution context."""

    policy: str = "auto"
    form: Optional[str] = None

    def __post_init__(self):
        if not isinstance(
            self.policy,
            str,
        ):
            raise ModelFormControlError(
                "Model Form baseline policy "
                "must be a string."
            )

        policy = (
            self.policy
            .strip()
            .lower()
        )

        if (
            policy
            not in MODEL_FORM_BASELINE_POLICIES
        ):
            raise ModelFormControlError(
                "Model Form baseline policy must "
                "be 'auto' or 'pinned'."
            )

        object.__setattr__(
            self,
            "policy",
            policy,
        )

        if policy == "auto":
            if self.form is not None:
                raise ModelFormControlError(
                    "Auto Model Form baseline "
                    "cannot contain a resolved form."
                )

            return

        if self.form is None:
            raise ModelFormControlError(
                "Pinned Model Form baseline "
                "requires Small or Big."
            )

        object.__setattr__(
            self,
            "form",
            _normalize_control_form(
                self.form
            ),
        )


@dataclass(
    frozen=True,
    slots=True,
)
class TaskModelFormOverride:
    """Task-scoped Small / Big override.

    Model Form temporary behavior is tied to a Task ID.
    It is deliberately not a turn-counted lease.
    """

    task_id: str
    form: str

    def __post_init__(self):
        object.__setattr__(
            self,
            "task_id",
            _nonempty_string(
                "task_id",
                self.task_id,
            ),
        )

        object.__setattr__(
            self,
            "form",
            _normalize_control_form(
                self.form
            ),
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ModelFormControlState:
    """Model Form control owned by one execution context."""

    execution_context_id: str = (
        DEFAULT_EXECUTION_CONTEXT_ID
    )

    baseline: ModelFormBaseline = (
        ModelFormBaseline()
    )

    task_override: Optional[
        TaskModelFormOverride
    ] = None

    schema_version: int = (
        MODEL_FORM_CONTROL_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != MODEL_FORM_CONTROL_SCHEMA_VERSION
        ):
            raise ModelFormControlError(
                "Unsupported Model Form control "
                "schema version."
            )

        object.__setattr__(
            self,
            "execution_context_id",
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            ),
        )

        if not isinstance(
            self.baseline,
            ModelFormBaseline,
        ):
            raise ModelFormControlError(
                "baseline must be ModelFormBaseline."
            )

        if (
            self.task_override is not None
            and not isinstance(
                self.task_override,
                TaskModelFormOverride,
            )
        ):
            raise ModelFormControlError(
                "task_override must be "
                "TaskModelFormOverride or None."
            )


def _require_control(
    control,
):
    if not isinstance(
        control,
        ModelFormControlState,
    ):
        raise ModelFormControlError(
            "control must be "
            "ModelFormControlState."
        )


def default_model_form_control(
    execution_context_id=(
        DEFAULT_EXECUTION_CONTEXT_ID
    ),
):
    return ModelFormControlState(
        execution_context_id=(
            execution_context_id
        ),
    )


def set_auto_baseline(
    control,
):
    """Set Auto without disturbing a Task override."""

    _require_control(
        control
    )

    return ModelFormControlState(
        execution_context_id=(
            control.execution_context_id
        ),

        baseline=ModelFormBaseline(
            policy="auto",
            form=None,
        ),

        task_override=control.task_override,
    )


def set_pinned_baseline(
    control,
    form,
):
    """Pin Small or Big without disturbing a Task override."""

    _require_control(
        control
    )

    return ModelFormControlState(
        execution_context_id=(
            control.execution_context_id
        ),

        baseline=ModelFormBaseline(
            policy="pinned",
            form=form,
        ),

        task_override=control.task_override,
    )


def set_task_override(
    control,
    task_id,
    form,
):
    """Start or replace this context's Task-scoped override."""

    _require_control(
        control
    )

    return ModelFormControlState(
        execution_context_id=(
            control.execution_context_id
        ),

        baseline=control.baseline,

        task_override=TaskModelFormOverride(
            task_id=task_id,
            form=form,
        ),
    )


def clear_task_override(
    control,
    *,
    task_id=None,
):
    """Clear Task override, optionally guarded by Task ID."""

    _require_control(
        control
    )

    override = control.task_override

    if override is None:
        return control

    if task_id is not None:
        expected = _nonempty_string(
            "task_id",
            task_id,
        )

        if override.task_id != expected:
            raise ModelFormControlError(
                "Task override belongs to a "
                "different Task ID."
            )

    return ModelFormControlState(
        execution_context_id=(
            control.execution_context_id
        ),

        baseline=control.baseline,
        task_override=None,
    )


def model_form_control_to_mapping(
    control,
):
    """Return YAML-safe runtime-neutral durable state."""

    _require_control(
        control
    )

    task_override = None

    if control.task_override is not None:
        task_override = {
            "task_id":
                control.task_override.task_id,

            "form":
                control.task_override.form,
        }

    return {
        "schema_version":
            MODEL_FORM_CONTROL_SCHEMA_VERSION,

        "execution_context_id":
            control.execution_context_id,

        "baseline": {
            "policy":
                control.baseline.policy,

            "form":
                control.baseline.form,
        },

        "task_override":
            task_override,
    }


def model_form_control_from_mapping(
    value,
    *,
    execution_context_id=None,
):
    """Load one execution context's durable control state."""

    if value is None:
        return default_model_form_control(
            execution_context_id=(
                execution_context_id
                if execution_context_id is not None
                else DEFAULT_EXECUTION_CONTEXT_ID
            )
        )

    if not isinstance(
        value,
        dict,
    ):
        raise ModelFormControlError(
            "model_form_control must be a mapping."
        )

    schema_version = value.get(
        "schema_version",
        MODEL_FORM_CONTROL_SCHEMA_VERSION,
    )

    if (
        schema_version
        != MODEL_FORM_CONTROL_SCHEMA_VERSION
    ):
        raise ModelFormControlError(
            "Unsupported model_form_control "
            "schema version."
        )

    stored_context_id = value.get(
        "execution_context_id",
        DEFAULT_EXECUTION_CONTEXT_ID,
    )

    stored_context_id = _nonempty_string(
        "execution_context_id",
        stored_context_id,
    )

    if execution_context_id is not None:
        requested_context_id = _nonempty_string(
            "execution_context_id",
            execution_context_id,
        )

        if requested_context_id != stored_context_id:
            raise ModelFormControlError(
                "Stored Model Form control belongs "
                "to a different execution context."
            )

    baseline_raw = value.get(
        "baseline",
        {
            "policy": "auto",
            "form": None,
        },
    )

    if not isinstance(
        baseline_raw,
        dict,
    ):
        raise ModelFormControlError(
            "model_form_control.baseline "
            "must be a mapping."
        )

    baseline = ModelFormBaseline(
        policy=baseline_raw.get(
            "policy",
            "auto",
        ),
        form=baseline_raw.get(
            "form"
        ),
    )

    override_raw = value.get(
        "task_override"
    )

    task_override = None

    if override_raw is not None:
        if not isinstance(
            override_raw,
            dict,
        ):
            raise ModelFormControlError(
                "model_form_control.task_override "
                "must be a mapping or null."
            )

        task_override = TaskModelFormOverride(
            task_id=override_raw.get(
                "task_id"
            ),
            form=override_raw.get(
                "form"
            ),
        )

    return ModelFormControlState(
        execution_context_id=(
            stored_context_id
        ),
        baseline=baseline,
        task_override=task_override,
    )
