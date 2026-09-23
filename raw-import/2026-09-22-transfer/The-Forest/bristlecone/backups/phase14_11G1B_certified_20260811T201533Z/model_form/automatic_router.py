"""Pure contracts for automatic Model Form escalation.

This module belongs to Phase 14.11G.

It does not:
- resolve Model Form precedence;
- resolve or mutate Reasoning;
- inspect ResourceRequest / Governor state;
- inspect runtime adapters or sessions;
- perform capability resolution;
- freeze a Model Form turn;
- perform runtime work.

The automatic router consumes Forest-level semantic signals and
produces only a Small/Big recommendation with stable reasons.
"""

from dataclasses import dataclass
from typing import Optional

from .model import normalize_resolved_model_form


AUTOMATIC_MODEL_FORM_SCHEMA_VERSION = 1


class AutomaticModelFormRoutingError(ValueError):
    """Invalid automatic Model Form routing contract."""


def _nonempty_string(
    field_name,
    value,
):
    if (
        not isinstance(value, str)
        or not value.strip()
    ):
        raise AutomaticModelFormRoutingError(
            f"{field_name} must be a non-empty string."
        )

    return value.strip()


def _optional_nonempty_string(
    field_name,
    value,
):
    if value is None:
        return None

    return _nonempty_string(
        field_name,
        value,
    )


def _string_tuple(
    field_name,
    value,
    *,
    allow_empty=True,
):
    if isinstance(value, str):
        raise AutomaticModelFormRoutingError(
            f"{field_name} must be an iterable "
            "of strings, not one string."
        )

    try:
        items = tuple(value)

    except TypeError as exc:
        raise AutomaticModelFormRoutingError(
            f"{field_name} must be an iterable "
            "of non-empty strings."
        ) from exc

    normalized = []

    for item in items:
        normalized.append(
            _nonempty_string(
                field_name,
                item,
            )
        )

    result = tuple(normalized)

    if (
        not allow_empty
        and not result
    ):
        raise AutomaticModelFormRoutingError(
            f"{field_name} cannot be empty."
        )

    if len(set(result)) != len(result):
        raise AutomaticModelFormRoutingError(
            f"{field_name} cannot contain duplicates."
        )

    return result


@dataclass(
    frozen=True,
    slots=True,
)
class AutomaticModelFormSignals:
    """Forest-level inputs for one automatic Model Form decision.

    execution_context_id keeps routing local to the exact Tree/Clone
    execution context.

    task_id is optional because Model Form Auto may exist without an
    active Task-scoped override.

    message is the current meaningful user/task input. Complexity is
    derived by routing policy rather than stored as authoritative state.

    reasoning_mode is already resolved for this meaningful turn.
    This contract never resolves Reasoning itself.

    current_form is optional context about the currently active resolved
    form. It is not an explicit override and does not replace canonical
    Model Form precedence.

    workshop_id and capability IDs remain canonical Forest concepts.
    Runtime adapters, toolset names, and runtime Skill names are excluded.

    known_small_failure is semantic evidence that Small has already failed
    for the relevant work. It is not a resource-pressure signal.
    """

    execution_context_id: str
    message: str
    reasoning_mode: str

    task_id: Optional[str] = None
    current_form: Optional[str] = None
    workshop_id: Optional[str] = None

    general_capability_ids: tuple[str, ...] = ()
    ready_capability_ids: tuple[str, ...] = ()

    known_small_failure: bool = False

    schema_version: int = (
        AUTOMATIC_MODEL_FORM_SCHEMA_VERSION
    )

    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != AUTOMATIC_MODEL_FORM_SCHEMA_VERSION
        ):
            raise AutomaticModelFormRoutingError(
                "Unsupported automatic Model Form "
                "signal schema version."
            )

        object.__setattr__(
            self,
            "execution_context_id",
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            ),
        )

        object.__setattr__(
            self,
            "message",
            _nonempty_string(
                "message",
                self.message,
            ),
        )

        object.__setattr__(
            self,
            "reasoning_mode",
            _nonempty_string(
                "reasoning_mode",
                self.reasoning_mode,
            ),
        )

        object.__setattr__(
            self,
            "task_id",
            _optional_nonempty_string(
                "task_id",
                self.task_id,
            ),
        )

        current_form = self.current_form

        if current_form is not None:
            try:
                current_form = (
                    normalize_resolved_model_form(
                        current_form
                    )
                )

            except Exception as exc:
                raise AutomaticModelFormRoutingError(
                    "current_form must be a resolved "
                    "Small or Big Model Form."
                ) from exc

        object.__setattr__(
            self,
            "current_form",
            current_form,
        )

        object.__setattr__(
            self,
            "workshop_id",
            _optional_nonempty_string(
                "workshop_id",
                self.workshop_id,
            ),
        )

        object.__setattr__(
            self,
            "general_capability_ids",
            _string_tuple(
                "general_capability_ids",
                self.general_capability_ids,
            ),
        )

        object.__setattr__(
            self,
            "ready_capability_ids",
            _string_tuple(
                "ready_capability_ids",
                self.ready_capability_ids,
            ),
        )

        if not isinstance(
            self.known_small_failure,
            bool,
        ):
            raise AutomaticModelFormRoutingError(
                "known_small_failure must be bool."
            )


@dataclass(
    frozen=True,
    slots=True,
)
class AutomaticModelFormRecommendation:
    """Pure Small/Big recommendation from the automatic router.

    The existing Model Form resolver remains responsible for precedence
    and for assigning the final ModelFormDecision source.

    Reasons are required so every automatic recommendation is auditable.
    """

    execution_context_id: str
    form: str
    reasons: tuple[str, ...]

    schema_version: int = (
        AUTOMATIC_MODEL_FORM_SCHEMA_VERSION
    )

    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != AUTOMATIC_MODEL_FORM_SCHEMA_VERSION
        ):
            raise AutomaticModelFormRoutingError(
                "Unsupported automatic Model Form "
                "recommendation schema version."
            )

        object.__setattr__(
            self,
            "execution_context_id",
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            ),
        )

        try:
            form = normalize_resolved_model_form(
                self.form
            )

        except Exception as exc:
            raise AutomaticModelFormRoutingError(
                "form must resolve to Small or Big."
            ) from exc

        object.__setattr__(
            self,
            "form",
            form,
        )

        object.__setattr__(
            self,
            "reasons",
            _string_tuple(
                "reasons",
                self.reasons,
                allow_empty=False,
            ),
        )
