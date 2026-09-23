"""Runtime-neutral Forest Model Form binding registry."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .model import (
    ModelFormError,
    normalize_resolved_model_form,
)


MODEL_BINDING_REGISTRY_SCHEMA_VERSION = 1


class ModelBindingRegistryError(ModelFormError):
    """Raised when a Model Form binding registry is invalid."""


def _nonempty_string(
    name,
    value,
):
    if not isinstance(value, str):
        raise ModelBindingRegistryError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelBindingRegistryError(
            f"{name} cannot be empty."
        )

    return normalized


def _normalize_registry_form(
    value,
):
    """Normalize Small / Big at the registry boundary."""

    try:
        return normalize_resolved_model_form(
            value
        )

    except ModelFormError as exc:
        raise ModelBindingRegistryError(
            str(exc)
        ) from exc


def _freeze_value(
    value,
):
    """Recursively freeze YAML-safe runtime configuration."""

    if isinstance(value, Mapping):
        result = {}

        for key, item in value.items():
            key = _nonempty_string(
                "runtime configuration key",
                key,
            )

            result[key] = _freeze_value(
                item
            )

        return MappingProxyType(
            result
        )

    if isinstance(value, (list, tuple)):
        return tuple(
            _freeze_value(item)
            for item in value
        )

    if (
        value is None
        or isinstance(
            value,
            (str, int, float, bool),
        )
    ):
        return value

    raise ModelBindingRegistryError(
        "Runtime configuration values must be "
        "YAML-safe mappings, sequences, scalars, "
        "or null."
    )


def _thaw_value(
    value,
):
    """Return a mutable YAML-safe copy of frozen state."""

    if isinstance(value, Mapping):
        return {
            key: _thaw_value(item)
            for key, item in value.items()
        }

    if isinstance(value, tuple):
        return [
            _thaw_value(item)
            for item in value
        ]

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ModelBinding:
    """One opaque Model Form to runtime binding."""

    binding_id: str
    runtime: Mapping
    schema_version: int = (
        MODEL_BINDING_REGISTRY_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != MODEL_BINDING_REGISTRY_SCHEMA_VERSION
        ):
            raise ModelBindingRegistryError(
                "Unsupported Model Binding "
                "schema version."
            )

        object.__setattr__(
            self,
            "binding_id",
            _nonempty_string(
                "binding_id",
                self.binding_id,
            ),
        )

        if not isinstance(
            self.runtime,
            Mapping,
        ):
            raise ModelBindingRegistryError(
                "Model Binding runtime "
                "must be a mapping."
            )

        frozen_runtime = _freeze_value(
            self.runtime
        )

        adapter = frozen_runtime.get(
            "adapter"
        )

        _nonempty_string(
            "runtime.adapter",
            adapter,
        )

        object.__setattr__(
            self,
            "runtime",
            frozen_runtime,
        )

    @property
    def adapter(self):
        return self.runtime[
            "adapter"
        ]

    def runtime_state(self):
        """Return a fresh mutable runtime-state fragment."""

        return _thaw_value(
            self.runtime
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ModelBindingRegistry:
    """Resolved Model Forms mapped to opaque runtime bindings."""

    form_bindings: Mapping
    bindings: Mapping
    schema_version: int = (
        MODEL_BINDING_REGISTRY_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != MODEL_BINDING_REGISTRY_SCHEMA_VERSION
        ):
            raise ModelBindingRegistryError(
                "Unsupported Model Binding Registry "
                "schema version."
            )

        if not isinstance(
            self.form_bindings,
            Mapping,
        ):
            raise ModelBindingRegistryError(
                "form_bindings must be a mapping."
            )

        if not isinstance(
            self.bindings,
            Mapping,
        ):
            raise ModelBindingRegistryError(
                "bindings must be a mapping."
            )

        normalized_bindings = {}

        for raw_id, binding in self.bindings.items():
            binding_id = _nonempty_string(
                "binding_id",
                raw_id,
            )

            if not isinstance(
                binding,
                ModelBinding,
            ):
                raise ModelBindingRegistryError(
                    "Each binding must be "
                    "a ModelBinding."
                )

            if (
                binding.binding_id
                != binding_id
            ):
                raise ModelBindingRegistryError(
                    "Binding mapping key does not "
                    "match binding.binding_id."
                )

            normalized_bindings[
                binding_id
            ] = binding

        normalized_forms = {}

        for raw_form, raw_binding_id in (
            self.form_bindings.items()
        ):
            form = _normalize_registry_form(
                raw_form
            )

            binding_id = _nonempty_string(
                "binding_id",
                raw_binding_id,
            )

            if (
                binding_id
                not in normalized_bindings
            ):
                raise ModelBindingRegistryError(
                    f"Model Form {form!r} references "
                    "an unknown binding."
                )

            normalized_forms[
                form
            ] = binding_id

        object.__setattr__(
            self,
            "form_bindings",
            MappingProxyType(
                normalized_forms
            ),
        )

        object.__setattr__(
            self,
            "bindings",
            MappingProxyType(
                normalized_bindings
            ),
        )

    def binding_id_for_form(
        self,
        form,
    ):
        form = _normalize_registry_form(
            form
        )

        binding_id = self.form_bindings.get(
            form
        )

        if binding_id is None:
            raise ModelBindingRegistryError(
                f"Model Form {form!r} "
                "has no configured binding."
            )

        return binding_id

    def binding_for_form(
        self,
        form,
    ):
        binding_id = self.binding_id_for_form(
            form
        )

        return self.bindings[
            binding_id
        ]

    def runtime_state_for_form(
        self,
        form,
    ):
        return self.binding_for_form(
            form
        ).runtime_state()


def model_binding_registry_from_mapping(
    value,
):
    """Load a runtime-neutral registry from YAML-safe state."""

    if not isinstance(
        value,
        Mapping,
    ):
        raise ModelBindingRegistryError(
            "Model Binding Registry must be a mapping."
        )

    schema_version = value.get(
        "schema_version",
        MODEL_BINDING_REGISTRY_SCHEMA_VERSION,
    )

    if (
        schema_version
        != MODEL_BINDING_REGISTRY_SCHEMA_VERSION
    ):
        raise ModelBindingRegistryError(
            "Unsupported Model Binding Registry "
            "schema version."
        )

    raw_forms = value.get(
        "forms",
        {},
    )

    raw_bindings = value.get(
        "bindings",
        {},
    )

    if not isinstance(
        raw_forms,
        Mapping,
    ):
        raise ModelBindingRegistryError(
            "forms must be a mapping."
        )

    if not isinstance(
        raw_bindings,
        Mapping,
    ):
        raise ModelBindingRegistryError(
            "bindings must be a mapping."
        )

    bindings = {}

    for raw_id, raw_binding in (
        raw_bindings.items()
    ):
        binding_id = _nonempty_string(
            "binding_id",
            raw_id,
        )

        if not isinstance(
            raw_binding,
            Mapping,
        ):
            raise ModelBindingRegistryError(
                "Each binding entry "
                "must be a mapping."
            )

        runtime = raw_binding.get(
            "runtime"
        )

        bindings[binding_id] = ModelBinding(
            binding_id=binding_id,
            runtime=runtime,
        )

    return ModelBindingRegistry(
        form_bindings=dict(
            raw_forms
        ),
        bindings=bindings,
        schema_version=schema_version,
    )


def model_binding_registry_to_mapping(
    registry,
):
    """Return a YAML-safe representation of the registry."""

    if not isinstance(
        registry,
        ModelBindingRegistry,
    ):
        raise ModelBindingRegistryError(
            "registry must be "
            "ModelBindingRegistry."
        )

    bindings = {}

    for binding_id, binding in (
        registry.bindings.items()
    ):
        bindings[binding_id] = {
            "runtime":
                binding.runtime_state(),
        }

    return {
        "schema_version":
            MODEL_BINDING_REGISTRY_SCHEMA_VERSION,

        "forms":
            dict(registry.form_bindings),

        "bindings":
            bindings,
    }
