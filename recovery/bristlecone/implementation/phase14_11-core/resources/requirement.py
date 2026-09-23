"""Runtime-neutral Forest resource-requirement contract."""

from dataclasses import dataclass
from typing import Optional

from .model import ResourceRequest


RESOURCE_REQUIREMENT_SCHEMA_VERSION = 1


class ResourceRequirementError(ValueError):
    """Raised when a Forest ResourceRequirement is invalid."""


def _nonempty_string(name, value):
    if not isinstance(value, str):
        raise ResourceRequirementError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ResourceRequirementError(
            f"{name} cannot be empty."
        )

    return normalized


def _optional_nonnegative_int(
    name,
    value,
):
    """Normalize a minimum resource requirement.

    None means the required amount is unknown.

    Zero means the operation explicitly requires none
    of this resource beyond its existing baseline.
    """

    if value is None:
        return None

    if (
        isinstance(value, bool)
        or not isinstance(value, int)
    ):
        raise ResourceRequirementError(
            f"{name} must be a nonnegative integer "
            "or None."
        )

    if value < 0:
        raise ResourceRequirementError(
            f"{name} cannot be negative."
        )

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ResourceRequirement:
    """Minimum measurable resources needed for an exact request.

    The exact ResourceRequest is retained so requirements cannot
    accidentally be applied to a different semantic request.

    None means a requirement is unknown / not established.
    Zero means that resource is explicitly not required beyond
    the existing baseline.

    This object does not grant permission, inspect availability,
    define policy ceilings, schedule resources, select runtime
    sessions, or rewrite Model Form / Reasoning.
    """

    request: ResourceRequest
    source: str

    memory_mib: Optional[int] = None
    accelerator_memory_mib: Optional[int] = None
    cpu_threads: Optional[int] = None

    schema_version: int = (
        RESOURCE_REQUIREMENT_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != RESOURCE_REQUIREMENT_SCHEMA_VERSION
        ):
            raise ResourceRequirementError(
                "Unsupported ResourceRequirement "
                "schema version."
            )

        if not isinstance(
            self.request,
            ResourceRequest,
        ):
            raise ResourceRequirementError(
                "request must be ResourceRequest."
            )

        object.__setattr__(
            self,
            "source",
            _nonempty_string(
                "source",
                self.source,
            ),
        )

        for name in (
            "memory_mib",
            "accelerator_memory_mib",
            "cpu_threads",
        ):
            object.__setattr__(
                self,
                name,
                _optional_nonnegative_int(
                    name,
                    getattr(self, name),
                ),
            )
