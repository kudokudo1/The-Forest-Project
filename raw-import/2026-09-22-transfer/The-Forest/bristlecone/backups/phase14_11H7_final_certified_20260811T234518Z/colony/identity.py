"""Pure Forest Colony execution-context identity contracts.

This module describes semantic Tree/Colony identity only.

It deliberately does NOT own:
- model binding identity
- runtime session identity
- adapter identity
- Model Form
- Reasoning
- permissions
- runtime/KV state

Those remain separate Forest/runtime concerns.
"""

from dataclasses import dataclass


COLONY_IDENTITY_SCHEMA_VERSION = 1

LINEAGE_ROLE_ORTET = "ortet"
LINEAGE_ROLE_RAMET = "ramet"

COLONY_LINEAGE_ROLES = (
    LINEAGE_ROLE_ORTET,
    LINEAGE_ROLE_RAMET,
)


class ColonyIdentityError(ValueError):
    """Raised when Colony execution-context identity is invalid."""


def _normalize_required_text(
    field_name,
    value,
):
    if not isinstance(value, str):
        raise ColonyIdentityError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ColonyIdentityError(
            f"{field_name} must not be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ColonyExecutionContext:
    """Semantic identity of one execution context within a Tree.

    tree_id identifies the durable Tree.

    execution_context_id identifies the exact independently operating
    context of that Tree.

    lineage_role describes origin:
        ortet = original lineage context
        ramet = cloned lineage context

    operational_role describes current operational responsibility.

    Lineage role and operational role are intentionally independent.
    An Ortet is not inherently Main, and a Ramet is not inherently
    secondary.
    """

    tree_id: str
    execution_context_id: str
    lineage_role: str
    operational_role: str
    schema_version: int = COLONY_IDENTITY_SCHEMA_VERSION

    def __post_init__(self):
        tree_id = _normalize_required_text(
            "tree_id",
            self.tree_id,
        )

        execution_context_id = _normalize_required_text(
            "execution_context_id",
            self.execution_context_id,
        )

        lineage_role = _normalize_required_text(
            "lineage_role",
            self.lineage_role,
        ).lower()

        operational_role = _normalize_required_text(
            "operational_role",
            self.operational_role,
        )

        if lineage_role not in COLONY_LINEAGE_ROLES:
            raise ColonyIdentityError(
                "lineage_role must be one of: "
                + ", ".join(
                    COLONY_LINEAGE_ROLES
                )
                + "."
            )

        if (
            isinstance(self.schema_version, bool)
            or not isinstance(
                self.schema_version,
                int,
            )
            or self.schema_version
            != COLONY_IDENTITY_SCHEMA_VERSION
        ):
            raise ColonyIdentityError(
                "Unsupported Colony identity schema_version."
            )

        object.__setattr__(
            self,
            "tree_id",
            tree_id,
        )

        object.__setattr__(
            self,
            "execution_context_id",
            execution_context_id,
        )

        object.__setattr__(
            self,
            "lineage_role",
            lineage_role,
        )

        object.__setattr__(
            self,
            "operational_role",
            operational_role,
        )
