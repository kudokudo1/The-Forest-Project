"""Coordinator for disposable Project Forest cache entries."""

from threading import RLock
from typing import Any, Mapping, Optional

from .entry import (
    CACHE_ENTRY_SCHEMA_VERSION,
    CacheEntry,
    CacheKey,
)


class CacheCoordinator:
    """Own runtime-neutral cache lifecycle mechanics.

    The coordinator deliberately knows nothing about Hermes,
    llama.cpp, Ollama, Leaves, Workshops, or any other specific
    producer. Callers supply namespaces, stable cache types,
    identities, and dependency information.
    """

    def __init__(self):
        self._lock = RLock()
        self._entries = {}

    def put(
        self,
        key,
        value,
        dependencies=None,
        schema_version=CACHE_ENTRY_SCHEMA_VERSION,
        display_name=None,
        metadata=None,
    ):
        """Store one derived value and return its CacheEntry."""

        if not isinstance(key, CacheKey):
            raise TypeError(
                "CacheCoordinator.put() requires a CacheKey."
            )

        entry = CacheEntry(
            key=key,
            value=value,
            dependencies=dict(dependencies or {}),
            schema_version=schema_version,
            display_name=display_name,
            metadata=dict(metadata or {}),
        )

        with self._lock:
            self._entries[key] = entry

        return entry

    def get(
        self,
        key,
        dependencies=None,
        schema_version=CACHE_ENTRY_SCHEMA_VERSION,
    ):
        """Return a reusable entry, or None after invalidating it."""

        if not isinstance(key, CacheKey):
            raise TypeError(
                "CacheCoordinator.get() requires a CacheKey."
            )

        with self._lock:
            entry = self._entries.get(key)

            if entry is None:
                return None

            if not entry.matches(
                dependencies=dependencies,
                schema_version=schema_version,
            ):
                self._entries.pop(key, None)
                return None

            return entry

    def invalidate(
        self,
        namespace=None,
        cache_type=None,
        identity_prefix=None,
    ):
        """Discard entries matching the supplied stable selectors.

        ``identity_prefix`` allows callers to invalidate a logical
        group without knowing anything about cache storage internals.
        For example, a Task-owned cache may use the Task ID as the
        first element of its stable identity.
        """

        if identity_prefix is not None:
            if not isinstance(identity_prefix, tuple):
                raise TypeError(
                    "Cache identity prefix must be a tuple."
                )

        with self._lock:
            keys = []

            for key in self._entries:
                if (
                    namespace is not None
                    and key.namespace != namespace
                ):
                    continue

                if (
                    cache_type is not None
                    and key.cache_type != cache_type
                ):
                    continue

                if identity_prefix is not None:
                    prefix_length = len(identity_prefix)

                    if (
                        key.identity[:prefix_length]
                        != identity_prefix
                    ):
                        continue

                keys.append(key)

            for key in keys:
                self._entries.pop(key, None)

            return len(keys)

    def clear(self):
        """Discard every cache entry."""

        with self._lock:
            count = len(self._entries)
            self._entries.clear()
            return count

    def inspect(self):
        """Describe cached structure without exposing cached values."""

        with self._lock:
            result = []

            for entry in self._entries.values():
                result.append(
                    {
                        "namespace": entry.key.namespace,
                        "cache_type": entry.key.cache_type,
                        "identity": entry.key.identity,
                        "schema_version": entry.schema_version,
                        "dependencies": dict(
                            entry.dependencies
                        ),
                        "display_name": entry.display_name,
                        "metadata": dict(
                            entry.metadata
                        ),
                    }
                )

            return result

    def __len__(self):
        with self._lock:
            return len(self._entries)
