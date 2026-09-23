"""Canonical runtime-neutral Forest resource-request model."""

from dataclasses import dataclass

from model_form.model import (
    normalize_resolved_model_form,
)
from reasoning.model import (
    normalize_reasoning_mode,
)


RESOURCE_REQUEST_SCHEMA_VERSION = 1

RESOURCE_PRIORITIES = (
    "background",
    "standard",
    "interactive",
)


class ResourceRequestError(ValueError):
    """Raised when a Forest ResourceRequest is invalid."""


def _nonempty_string(name, value):
    if not isinstance(value, str):
        raise ResourceRequestError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ResourceRequestError(
            f"{name} cannot be empty."
        )

    return normalized


def normalize_resource_priority(value):
    """Normalize a runtime-neutral Forest resource priority."""

    if not isinstance(value, str):
        raise ResourceRequestError(
            "Resource priority must be a string."
        )

    normalized = value.strip().lower()

    if normalized not in RESOURCE_PRIORITIES:
        raise ResourceRequestError(
            "Resource priority must be "
            "'background', 'standard', or 'interactive'."
        )

    return normalized


def _normalize_reasons(value):
    if not isinstance(value, tuple):
        raise ResourceRequestError(
            "Resource request reasons must be a tuple."
        )

    normalized = []

    for reason in value:
        normalized.append(
            _nonempty_string(
                "Resource request reason",
                reason,
            )
        )

    return tuple(normalized)


@dataclass(
    frozen=True,
    slots=True,
)
class ResourceRequest:
    """Frozen semantic resource intent for one Forest operation.

    This object says what semantic execution is being requested.
    It does not grant permission, schedule hardware, select a
    runtime session, or translate into vendor/runtime controls.

    Resource pressure must not silently rewrite model_form or
    reasoning_mode. A Governor may later approve, defer, or deny
    this request; semantic fallback requires a new explicit request.
    """

    task_id: str
    execution_context_id: str
    model_form: str
    reasoning_mode: str
    priority: str
    source: str

    reasons: tuple = ()
    may_defer: bool = True

    schema_version: int = (
        RESOURCE_REQUEST_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != RESOURCE_REQUEST_SCHEMA_VERSION
        ):
            raise ResourceRequestError(
                "Unsupported ResourceRequest "
                "schema version."
            )

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
            "execution_context_id",
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            ),
        )

        try:
            model_form = (
                normalize_resolved_model_form(
                    self.model_form
                )
            )
        except ValueError as exc:
            raise ResourceRequestError(
                "ResourceRequest contains an invalid "
                "resolved Model Form."
            ) from exc

        object.__setattr__(
            self,
            "model_form",
            model_form,
        )

        try:
            reasoning_mode = (
                normalize_reasoning_mode(
                    self.reasoning_mode
                )
            )
        except ValueError as exc:
            raise ResourceRequestError(
                "ResourceRequest contains an invalid "
                "Forest reasoning mode."
            ) from exc

        object.__setattr__(
            self,
            "reasoning_mode",
            reasoning_mode,
        )

        object.__setattr__(
            self,
            "priority",
            normalize_resource_priority(
                self.priority
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
            "reasons",
            _normalize_reasons(
                self.reasons
            ),
        )

        if type(self.may_defer) is not bool:
            raise ResourceRequestError(
                "may_defer must be bool."
            )
