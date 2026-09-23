"""Runtime-session identity for The Forest.

A runtime session is identified on the Forest side by:

    execution_context_id + model binding_id

Adapter name is implementation identity, not session identity.
Runtime session_id is the runtime-owned live session identifier.
"""

from collections.abc import Mapping
from dataclasses import dataclass


class RuntimeSessionIdentityError(ValueError):
    """Invalid Forest runtime-session identity."""


def _nonempty_string(
    value,
    field_name,
):
    if not isinstance(value, str):
        raise RuntimeSessionIdentityError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise RuntimeSessionIdentityError(
            f"{field_name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeSessionIdentity:
    """Forest identity for one runtime-session slot.

    The pair is intentionally independent of:

    - adapter name
    - runtime session ID
    - vendor/model name
    - Tree presentation terminology
    """

    execution_context_id: str
    binding_id: str

    def __post_init__(self):
        object.__setattr__(
            self,
            "execution_context_id",
            _nonempty_string(
                self.execution_context_id,
                "execution_context_id",
            ),
        )

        object.__setattr__(
            self,
            "binding_id",
            _nonempty_string(
                self.binding_id,
                "binding_id",
            ),
        )

    @property
    def key(self):
        """Return the canonical in-memory identity pair."""
        return (
            self.execution_context_id,
            self.binding_id,
        )


def runtime_session_identity_from_mapping(
    value,
):
    """Build a runtime-session identity from a mapping."""

    if not isinstance(value, Mapping):
        raise RuntimeSessionIdentityError(
            "Runtime session identity "
            "must be a mapping."
        )

    return RuntimeSessionIdentity(
        execution_context_id=value.get(
            "execution_context_id"
        ),
        binding_id=value.get(
            "binding_id"
        ),
    )


def runtime_session_identity_to_mapping(
    identity,
):
    """Return a plain serialization-safe mapping."""

    if not isinstance(
        identity,
        RuntimeSessionIdentity,
    ):
        raise RuntimeSessionIdentityError(
            "Expected RuntimeSessionIdentity."
        )

    return {
        "execution_context_id":
            identity.execution_context_id,

        "binding_id":
            identity.binding_id,
    }
