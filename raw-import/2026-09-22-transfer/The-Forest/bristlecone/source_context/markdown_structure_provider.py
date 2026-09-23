\
from __future__ import annotations

from threading import (
    Condition,
    RLock,
)

from cache import (
    CacheCoordinator,
    CacheKey,
)

from .snapshot import (
    SourceContentSnapshot,
)

from .structure import (
    SourceStructure,
)

from .markdown_structure import (
    MARKDOWN_STRUCTURE_KIND,
    MarkdownSourceStructureBuilder,
    MarkdownStructureError,
)


MARKDOWN_STRUCTURE_CACHE_SCHEMA_VERSION = 1

MARKDOWN_STRUCTURE_CACHE_NAMESPACE = (
    "source-context"
)

MARKDOWN_STRUCTURE_CACHE_TYPE = (
    "markdown-structure"
)


class MarkdownStructureProviderError(
    ValueError
):
    """Invalid derived Markdown structure request."""


class MarkdownSourceStructureProvider:
    """
    Shared provider for immutable Markdown source
    structures.

    The provider:

    - consumes immutable SourceContentSnapshot;
    - shares derived heading structure through the
      Forest CacheCoordinator;
    - single-flights identical concurrent builds;
    - keeps exact source versions independently
      cacheable.

    It performs no filesystem reads and makes no
    turn-local relevance decisions.
    """


    def __init__(
        self,
        cache_coordinator=None,
        builder=None,
    ):
        if cache_coordinator is None:
            cache_coordinator = (
                CacheCoordinator()
            )

        if not isinstance(
            cache_coordinator,
            CacheCoordinator,
        ):
            raise MarkdownStructureProviderError(
                "cache_coordinator must be a "
                "CacheCoordinator."
            )

        if builder is None:
            builder = (
                MarkdownSourceStructureBuilder()
            )

        if not isinstance(
            builder,
            MarkdownSourceStructureBuilder,
        ):
            raise MarkdownStructureProviderError(
                "builder must be a "
                "MarkdownSourceStructureBuilder."
            )

        self._cache_coordinator = (
            cache_coordinator
        )

        self._builder = builder

        self._condition = Condition(
            RLock()
        )

        self._inflight = set()


    @property
    def cache_coordinator(
        self,
    ):
        return self._cache_coordinator


    @staticmethod
    def _validate_snapshot(
        snapshot,
    ):
        if not isinstance(
            snapshot,
            SourceContentSnapshot,
        ):
            raise MarkdownStructureProviderError(
                "snapshot must be a "
                "SourceContentSnapshot."
            )


    @classmethod
    def _cache_key(
        cls,
        snapshot,
    ):
        cls._validate_snapshot(
            snapshot
        )

        fingerprint = (
            snapshot.fingerprint
        )

        return CacheKey(
            namespace=(
                MARKDOWN_STRUCTURE_CACHE_NAMESPACE
            ),
            cache_type=(
                MARKDOWN_STRUCTURE_CACHE_TYPE
            ),
            identity=(
                snapshot.source.source_id,
                MARKDOWN_STRUCTURE_KIND,
                fingerprint.method,
                fingerprint.components,
                snapshot.content_sha256,
            ),
        )


    @staticmethod
    def _dependencies(
        snapshot,
    ):
        return (
            snapshot.fingerprint
            .dependency_dict()
        )


    @staticmethod
    def _valid_cached_structure(
        entry,
        snapshot,
    ):
        if entry is None:
            return None

        value = getattr(
            entry,
            "value",
            None,
        )

        if not isinstance(
            value,
            SourceStructure,
        ):
            return None

        if (
            value.structure_kind
            != MARKDOWN_STRUCTURE_KIND
        ):
            return None

        if (
            value.fingerprint
            != snapshot.fingerprint
        ):
            return None

        if (
            value.source
            != snapshot.source
        ):
            return None

        return value


    def _cached(
        self,
        key,
        dependencies,
        snapshot,
    ):
        entry = (
            self._cache_coordinator.get(
                key,
                dependencies=dependencies,
                schema_version=(
                    MARKDOWN_STRUCTURE_CACHE_SCHEMA_VERSION
                ),
            )
        )

        return (
            self._valid_cached_structure(
                entry,
                snapshot,
            )
        )


    def structure_for(
        self,
        snapshot,
    ):
        self._validate_snapshot(
            snapshot
        )

        key = self._cache_key(
            snapshot
        )

        dependencies = (
            self._dependencies(
                snapshot
            )
        )


        cached = self._cached(
            key,
            dependencies,
            snapshot,
        )

        if cached is not None:
            return cached


        # ------------------------------------------
        # EXACT-SNAPSHOT SINGLE-FLIGHT
        # ------------------------------------------

        with self._condition:

            while key in self._inflight:

                self._condition.wait()

                cached = self._cached(
                    key,
                    dependencies,
                    snapshot,
                )

                if cached is not None:
                    return cached


            cached = self._cached(
                key,
                dependencies,
                snapshot,
            )

            if cached is not None:
                return cached


            self._inflight.add(
                key
            )


        try:
            try:
                structure = (
                    self._builder.build(
                        snapshot
                    )
                )

            except MarkdownStructureError:
                raise

            except Exception as exc:
                raise MarkdownStructureProviderError(
                    "Markdown source structure "
                    "could not be built."
                ) from exc


            if not isinstance(
                structure,
                SourceStructure,
            ):
                raise MarkdownStructureProviderError(
                    "Markdown structure builder "
                    "returned an invalid result."
                )


            if (
                structure.structure_kind
                != MARKDOWN_STRUCTURE_KIND
            ):
                raise MarkdownStructureProviderError(
                    "Markdown structure builder "
                    "returned the wrong kind."
                )


            if (
                structure.fingerprint
                != snapshot.fingerprint
            ):
                raise MarkdownStructureProviderError(
                    "Markdown structure builder "
                    "returned a mismatched "
                    "fingerprint."
                )


            if (
                structure.source
                != snapshot.source
            ):
                raise MarkdownStructureProviderError(
                    "Markdown structure builder "
                    "returned a mismatched source."
                )


            self._cache_coordinator.put(
                key,
                structure,
                dependencies=dependencies,
                schema_version=(
                    MARKDOWN_STRUCTURE_CACHE_SCHEMA_VERSION
                ),
                display_name=(
                    "Markdown Source Structure"
                ),
                metadata={
                    "source_id":
                        snapshot.source.source_id,

                    "structure_kind":
                        MARKDOWN_STRUCTURE_KIND,

                    "fingerprint_method":
                        snapshot.fingerprint.method,

                    "content_sha256":
                        snapshot.content_sha256,
                },
            )

            return structure


        finally:
            with self._condition:
                self._inflight.discard(
                    key
                )

                self._condition.notify_all()


    def inspect(
        self,
    ):
        with self._condition:
            return {
                "cache_namespace":
                    MARKDOWN_STRUCTURE_CACHE_NAMESPACE,

                "cache_type":
                    MARKDOWN_STRUCTURE_CACHE_TYPE,

                "schema_version":
                    MARKDOWN_STRUCTURE_CACHE_SCHEMA_VERSION,

                "inflight_count":
                    len(
                        self._inflight
                    ),
            }
