"""Forest runtime adapters.

Runtime adapters translate Forest runtime requests into
runtime-specific operations without exposing those implementation
details to the Forest core.
"""

from .base import (
    BaseRuntimeAdapter,
    RuntimeAdapterError,
)

__all__ = [
    "BaseRuntimeAdapter",
    "RuntimeAdapterError",
]
