"""Canonical runtime-neutral Forest Model Form model."""

from dataclasses import dataclass


MODEL_FORM_SCHEMA_VERSION = 1

CANONICAL_MODEL_FORM_CONTROLS = (
    "auto",
    "small",
    "big",
)

RESOLVED_MODEL_FORMS = (
    "small",
    "big",
)

DEFAULT_MODEL_FORM_CONTROL = "auto"


class ModelFormError(ValueError):
    """Raised when canonical Forest Model Form state is invalid."""


def normalize_model_form_control(
    value,
    *,
    default=DEFAULT_MODEL_FORM_CONTROL,
):
    """Normalize Forest Model Form control to Auto / Small / Big.

    Runtime-specific model names and adapter values do not
    belong in this namespace.
    """

    if value is None:
        value = default

    if not isinstance(value, str):
        raise ModelFormError(
            "Model Form control must be a string."
        )

    normalized = value.strip().lower()

    if not normalized:
        if default is None:
            raise ModelFormError(
                "Model Form control cannot be empty."
            )

        normalized = str(
            default
        ).strip().lower()

    if (
        normalized
        not in CANONICAL_MODEL_FORM_CONTROLS
    ):
        raise ModelFormError(
            "Unsupported canonical Forest "
            f"Model Form control: {value!r}."
        )

    return normalized


def normalize_resolved_model_form(
    value,
):
    """Normalize a resolved runtime Model Form to Small / Big.

    Auto is intentionally invalid here because Auto is policy,
    not an executable Model Form.
    """

    if not isinstance(value, str):
        raise ModelFormError(
            "Resolved Model Form must be a string."
        )

    normalized = value.strip().lower()

    if not normalized:
        raise ModelFormError(
            "Resolved Model Form cannot be empty."
        )

    if normalized == "auto":
        raise ModelFormError(
            "Auto is Model Form policy, not a "
            "resolved executable Model Form."
        )

    if normalized not in RESOLVED_MODEL_FORMS:
        raise ModelFormError(
            "Unsupported resolved Forest "
            f"Model Form: {value!r}."
        )

    return normalized


def _nonempty_string(
    name,
    value,
):
    if not isinstance(value, str):
        raise ModelFormError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelFormError(
            f"{name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ModelFormDecision:
    """Frozen Model Form decision for one meaningful turn.

    The decision belongs to one execution context. It contains
    no vendor model name, runtime adapter name, or runtime
    session state.
    """

    form: str
    source: str
    execution_context_id: str
    reasons: tuple = ()
    schema_version: int = MODEL_FORM_SCHEMA_VERSION

    def __post_init__(self):
        if (
            self.schema_version
            != MODEL_FORM_SCHEMA_VERSION
        ):
            raise ModelFormError(
                "Unsupported Model Form schema version."
            )

        object.__setattr__(
            self,
            "form",
            normalize_resolved_model_form(
                self.form
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
            "execution_context_id",
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            ),
        )

        reasons = tuple(
            self.reasons
        )

        normalized_reasons = []

        for reason in reasons:
            normalized_reasons.append(
                _nonempty_string(
                    "reason",
                    reason,
                )
            )

        object.__setattr__(
            self,
            "reasons",
            tuple(normalized_reasons),
        )
