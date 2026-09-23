"""Pure shared-model residency contracts.

Model residency describes a runtime-loaded model/weight instance that
may serve multiple isolated runtime sessions using the same binding.

Residency does NOT own:
- Tree identity
- Colony lineage
- execution-context identity
- Task identity
- runtime session identity
- conversation/KV state
- Reasoning
- Model Form control
- permissions or leases
"""

from dataclasses import dataclass

from .session_identity import (
    RuntimeSessionIdentity,
)


MODEL_RESIDENCY_SCHEMA_VERSION = 1


class ModelResidencyError(ValueError):
    """Raised when model residency state is invalid."""


def _required_text(
    value,
    field_name,
):
    if not isinstance(value, str):
        raise ModelResidencyError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelResidencyError(
            f"{field_name} must not be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class SharedModelResidency:
    """Identity of one shareable loaded model/weight residency.

    residency_id identifies the resident runtime model instance.

    binding_id identifies the immutable Forest runtime/model binding
    that the residency serves.

    adapter identifies the runtime backend hosting the residency.

    Multiple execution contexts may use this same residency when their
    RuntimeSessionIdentity uses this binding, but their sessions remain
    distinct.
    """

    residency_id: str
    binding_id: str
    adapter: str
    schema_version: int = MODEL_RESIDENCY_SCHEMA_VERSION

    def __post_init__(self):
        residency_id = _required_text(
            self.residency_id,
            "residency_id",
        )

        binding_id = _required_text(
            self.binding_id,
            "binding_id",
        )

        adapter = _required_text(
            self.adapter,
            "adapter",
        )

        if (
            isinstance(self.schema_version, bool)
            or not isinstance(
                self.schema_version,
                int,
            )
            or self.schema_version
            != MODEL_RESIDENCY_SCHEMA_VERSION
        ):
            raise ModelResidencyError(
                "Unsupported model residency schema_version."
            )

        object.__setattr__(
            self,
            "residency_id",
            residency_id,
        )

        object.__setattr__(
            self,
            "binding_id",
            binding_id,
        )

        object.__setattr__(
            self,
            "adapter",
            adapter,
        )


def residency_supports_session_identity(
    residency,
    identity,
):
    """Return whether a residency may back this session identity.

    Sharing is determined by binding compatibility only.

    execution_context_id remains deliberately irrelevant to residency
    compatibility so multiple isolated contexts may share weights
    without sharing their runtime sessions.
    """

    if not isinstance(
        residency,
        SharedModelResidency,
    ):
        raise ModelResidencyError(
            "residency must be SharedModelResidency."
        )

    if not isinstance(
        identity,
        RuntimeSessionIdentity,
    ):
        raise ModelResidencyError(
            "identity must be RuntimeSessionIdentity."
        )

    return (
        residency.binding_id
        == identity.binding_id
    )
