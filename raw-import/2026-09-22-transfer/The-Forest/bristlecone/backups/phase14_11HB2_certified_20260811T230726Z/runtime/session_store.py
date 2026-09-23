"""Forest-side runtime-session storage.

Canonical structure:

    runtime_sessions:
        <execution_context_id>:
            <binding_id>:
                adapter: <adapter_name>
                session_id: <runtime_session_id>
                previous_session_id: <optional>
                updated_at: <optional>

The storage hierarchy deliberately separates:

    execution context
    model/runtime binding
    runtime adapter
    runtime-owned session ID
"""

import copy
from collections.abc import Mapping

from .session_identity import (
    RuntimeSessionIdentity,
    RuntimeSessionIdentityError,
)


class RuntimeSessionStoreError(ValueError):
    """Invalid Forest runtime-session store."""


def _nonempty_string(
    value,
    field_name,
):
    if not isinstance(value, str):
        raise RuntimeSessionStoreError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise RuntimeSessionStoreError(
            f"{field_name} cannot be empty."
        )

    return normalized


def _optional_session_id(
    value,
    field_name,
):
    if value is None:
        return None

    normalized = str(value).strip()

    if not normalized:
        raise RuntimeSessionStoreError(
            f"{field_name} cannot be empty "
            "when provided."
        )

    return normalized


def normalize_runtime_session_entry(
    value,
):
    """Normalize one binding-local runtime session."""

    if not isinstance(value, Mapping):
        raise RuntimeSessionStoreError(
            "Runtime session entry "
            "must be a mapping."
        )

    adapter = _nonempty_string(
        value.get("adapter"),
        "adapter",
    )

    return {
        "adapter":
            adapter,

        "session_id":
            _optional_session_id(
                value.get("session_id"),
                "session_id",
            ),

        "previous_session_id":
            _optional_session_id(
                value.get(
                    "previous_session_id"
                ),
                "previous_session_id",
            ),

        "updated_at":
            value.get("updated_at"),
    }


def normalize_runtime_sessions(
    value,
):
    """Return the canonical nested session store.

    Empty or null storage is valid.

    Non-empty storage must use:

        execution_context_id
            -> binding_id
                -> runtime session entry

    Legacy adapter-keyed storage is intentionally
    not silently reinterpreted as the new schema.
    """

    if value is None:
        return {}

    if not isinstance(value, Mapping):
        raise RuntimeSessionStoreError(
            "runtime_sessions must be a mapping."
        )

    if not value:
        return {}

    normalized = {}

    for execution_context_id, bindings in (
        value.items()
    ):
        execution_context_id = (
            _nonempty_string(
                execution_context_id,
                "execution_context_id",
            )
        )

        if not isinstance(bindings, Mapping):
            raise RuntimeSessionStoreError(
                "Each execution-context runtime "
                "session group must be a mapping."
            )

        normalized_bindings = {}

        for binding_id, entry in (
            bindings.items()
        ):
            try:
                identity = RuntimeSessionIdentity(
                    execution_context_id=
                        execution_context_id,
                    binding_id=binding_id,
                )

            except RuntimeSessionIdentityError as exc:
                raise RuntimeSessionStoreError(
                    "Invalid runtime-session "
                    "identity."
                ) from exc

            canonical_binding_id = (
                identity.binding_id
            )

            if (
                canonical_binding_id
                in normalized_bindings
            ):
                raise RuntimeSessionStoreError(
                    "Duplicate normalized binding_id "
                    f"for {execution_context_id!r}: "
                    f"{canonical_binding_id!r}."
                )

            normalized_bindings[
                canonical_binding_id
            ] = (
                normalize_runtime_session_entry(
                    entry
                )
            )

        if execution_context_id in normalized:
            raise RuntimeSessionStoreError(
                "Duplicate normalized "
                "execution_context_id: "
                f"{execution_context_id!r}."
            )

        normalized[
            execution_context_id
        ] = normalized_bindings

    return normalized


def get_runtime_session_binding(
    runtime_sessions,
    execution_context_id,
    binding_id,
):
    """Return a detached binding entry or None."""

    normalized = normalize_runtime_sessions(
        runtime_sessions
    )

    try:
        identity = RuntimeSessionIdentity(
            execution_context_id=
                execution_context_id,
            binding_id=binding_id,
        )

    except RuntimeSessionIdentityError as exc:
        raise RuntimeSessionStoreError(
            "Invalid runtime-session identity."
        ) from exc

    entry = (
        normalized.get(
            identity.execution_context_id,
            {}
        ).get(
            identity.binding_id
        )
    )

    if entry is None:
        return None

    return copy.deepcopy(entry)


def set_runtime_session_binding(
    runtime_sessions,
    execution_context_id,
    binding_id,
    *,
    adapter,
    session_id,
    previous_session_id=None,
    updated_at=None,
):
    """Return a new store with one binding written."""

    normalized = normalize_runtime_sessions(
        runtime_sessions
    )

    try:
        identity = RuntimeSessionIdentity(
            execution_context_id=
                execution_context_id,
            binding_id=binding_id,
        )

    except RuntimeSessionIdentityError as exc:
        raise RuntimeSessionStoreError(
            "Invalid runtime-session identity."
        ) from exc

    entry = normalize_runtime_session_entry(
        {
            "adapter":
                adapter,

            "session_id":
                session_id,

            "previous_session_id":
                previous_session_id,

            "updated_at":
                updated_at,
        }
    )

    updated = copy.deepcopy(
        normalized
    )

    updated.setdefault(
        identity.execution_context_id,
        {},
    )[
        identity.binding_id
    ] = entry

    return updated


def runtime_session_adapters(
    runtime_sessions,
):
    """Return sorted unique adapter names."""

    normalized = normalize_runtime_sessions(
        runtime_sessions
    )

    adapters = set()

    for bindings in normalized.values():
        for entry in bindings.values():
            adapters.add(
                entry["adapter"]
            )

    return sorted(adapters)
