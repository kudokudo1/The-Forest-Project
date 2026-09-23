"""Runtime-neutral Forest resource-availability contract."""

from dataclasses import dataclass
from typing import Optional


RESOURCE_AVAILABILITY_SCHEMA_VERSION = 1


class ResourceAvailabilityError(ValueError):
    """Raised when Forest resource availability is invalid."""


def _nonempty_string(name, value):
    if not isinstance(value, str):
        raise ResourceAvailabilityError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ResourceAvailabilityError(
            f"{name} cannot be empty."
        )

    return normalized


def _optional_nonnegative_int(
    name,
    value,
):
    """Normalize a measured quantity.

    None means unknown / not measured.

    Zero means measured availability is exactly zero.
    """

    if value is None:
        return None

    if (
        isinstance(value, bool)
        or not isinstance(value, int)
    ):
        raise ResourceAvailabilityError(
            f"{name} must be a nonnegative integer "
            "or None."
        )

    if value < 0:
        raise ResourceAvailabilityError(
            f"{name} cannot be negative."
        )

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ResourceAvailability:
    """Observed resource availability at one point in time.

    None means Forest does not currently know the available
    quantity for that resource dimension.

    Zero means the quantity was measured and none is available.

    This object reports observations only. It does not define
    policy, grant permission, compare against ResourceBudget,
    choose Model Form or Reasoning, or schedule runtime work.
    """

    source: str

    memory_mib: Optional[int] = None
    accelerator_memory_mib: Optional[int] = None
    cpu_threads: Optional[int] = None

    schema_version: int = (
        RESOURCE_AVAILABILITY_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != RESOURCE_AVAILABILITY_SCHEMA_VERSION
        ):
            raise ResourceAvailabilityError(
                "Unsupported ResourceAvailability "
                "schema version."
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
