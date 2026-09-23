"""Runtime-neutral Forest resource-budget contract."""

from dataclasses import dataclass
from typing import Optional


RESOURCE_BUDGET_SCHEMA_VERSION = 1


class ResourceBudgetError(ValueError):
    """Raised when a Forest ResourceBudget is invalid."""


def _nonempty_string(name, value):
    if not isinstance(value, str):
        raise ResourceBudgetError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ResourceBudgetError(
            f"{name} cannot be empty."
        )

    return normalized


def _optional_nonnegative_int(
    name,
    value,
):
    if value is None:
        return None

    if (
        isinstance(value, bool)
        or not isinstance(value, int)
    ):
        raise ResourceBudgetError(
            f"{name} must be a nonnegative integer "
            "or None."
        )

    if value < 0:
        raise ResourceBudgetError(
            f"{name} cannot be negative."
        )

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ResourceBudget:
    """Maximum resources Forest permits an operation to consume.

    None means this budget establishes no explicit ceiling for
    that resource dimension.

    This object does not describe current availability, perform
    hardware probing, choose Model Form or Reasoning, grant an
    operation permission, or schedule runtime resources.
    """

    source: str

    memory_mib: Optional[int] = None
    accelerator_memory_mib: Optional[int] = None
    cpu_threads: Optional[int] = None

    schema_version: int = (
        RESOURCE_BUDGET_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != RESOURCE_BUDGET_SCHEMA_VERSION
        ):
            raise ResourceBudgetError(
                "Unsupported ResourceBudget "
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
