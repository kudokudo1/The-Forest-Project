"""Runtime-neutral cache entry definitions.

Caches are derived state, never authoritative Forest state.
An incompatible entry may always be discarded and rebuilt.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Hashable, Mapping, Optional, Tuple


CACHE_ENTRY_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class CacheKey:
    """Stable technical identity for one derived cache value."""

    namespace: str
    cache_type: str
    identity: Tuple[Hashable, ...]

    def __post_init__(self):
        if not isinstance(self.namespace, str) or not self.namespace:
            raise ValueError(
                "Cache namespace must be a non-empty string."
            )

        if not isinstance(self.cache_type, str) or not self.cache_type:
            raise ValueError(
                "Cache type must be a non-empty string."
            )

        if not isinstance(self.identity, tuple):
            raise TypeError(
                "Cache identity must be a tuple."
            )

        try:
            hash(self.identity)
        except TypeError as exc:
            raise TypeError(
                "Cache identity must contain only hashable values."
            ) from exc


@dataclass
class CacheEntry:
    """One disposable, dependency-aware cache entry."""

    key: CacheKey
    value: Any

    dependencies: Dict[str, Any] = field(
        default_factory=dict
    )

    schema_version: int = CACHE_ENTRY_SCHEMA_VERSION

    display_name: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    def matches(
        self,
        dependencies: Optional[Mapping[str, Any]] = None,
        schema_version: Optional[int] = None,
    ):
        """Return True only when the cached derivation is reusable."""

        if schema_version is None:
            schema_version = CACHE_ENTRY_SCHEMA_VERSION

        if self.schema_version != schema_version:
            return False

        if dependencies is not None:
            if self.dependencies != dict(dependencies):
                return False

        return True
