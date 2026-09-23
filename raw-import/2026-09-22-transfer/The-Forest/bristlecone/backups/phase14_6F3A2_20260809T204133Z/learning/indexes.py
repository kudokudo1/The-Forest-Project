"""Warm derived indexes for Forest Learning and User Context.

These indexes are disposable derived state.

Authoritative truth remains in learning/records.jsonl.

Deleting these indexes may make the Forest slower, but must
never make it forget Operational Learning or User Context.

The indexes are Forest-owned and runtime-neutral. Hermes,
Ollama, llama.cpp, or another runtime should not need to know
how these records are indexed.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from cache import (
    CacheCoordinator,
    CacheKey,
)

from .foundation import (
    ForestLearningStore,
)


LEARNING_INDEX_SCHEMA_VERSION = 1


class ForestLearningIndexError(
    RuntimeError
):
    """Raised when derived learning indexes are invalid."""


class ForestLearningIndexProvider:
    """Build and reuse warm Forest learning/context indexes."""

    def __init__(
        self,
        forest_root,
        *,
        cache_coordinator=None,
    ):
        self.forest_root = Path(
            forest_root
        )

        self.store = ForestLearningStore(
            self.forest_root
        )

        self.cache = (
            cache_coordinator
            or CacheCoordinator()
        )


    # --------------------------------------------------
    # Source dependency fingerprint
    # --------------------------------------------------

    def _source_dependencies(
        self,
    ):
        """Cheap fingerprint of authoritative record state."""

        path = self.store.path

        try:
            stat = path.stat()

        except FileNotFoundError:
            return {
                "records": {
                    "exists": False,
                }
            }

        return {
            "records": {
                "exists": True,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        }


    # --------------------------------------------------
    # Stable derived build
    # --------------------------------------------------

    def _get_or_build(
        self,
        *,
        cache_type,
        display_name,
        builder,
    ):
        """Return a stable cached derivation.

        If the authoritative JSONL changes while an index is
        being built, rebuild once against the newer state.

        If it changes repeatedly, return the most recent
        derived result without caching it. Authoritative state
        always wins over cache convenience.
        """

        key = CacheKey(
            namespace="forest",
            cache_type=cache_type,
            identity=("global",),
        )

        before = (
            self._source_dependencies()
        )

        cached = self.cache.get(
            key,
            dependencies=before,
        )

        if cached is not None:
            return deepcopy(
                cached.value
            )

        value = builder()

        after = (
            self._source_dependencies()
        )

        if before != after:
            before = after
            value = builder()

            after = (
                self._source_dependencies()
            )

            if before != after:
                # Source is changing too quickly to certify
                # this derived snapshot for reuse.
                return deepcopy(
                    value
                )

        self.cache.put(
            key,
            deepcopy(
                value
            ),
            dependencies=after,
            display_name=display_name,
            metadata={
                "schema_version": (
                    LEARNING_INDEX_SCHEMA_VERSION
                ),
                "record_count": value[
                    "record_count"
                ],
            },
        )

        return deepcopy(
            value
        )


    # --------------------------------------------------
    # Operational Learning
    # --------------------------------------------------

    def operational_learning_index(
        self,
    ):
        """Return the Warm Operational Learning index."""

        return self._get_or_build(
            cache_type=(
                "operational-learning-index"
            ),
            display_name=(
                "Operational Learning Index"
            ),
            builder=(
                self._build_operational_index
            ),
        )


    def _build_operational_index(
        self,
    ):
        records = (
            self.store
            .current_operational_learning()
        )

        by_kind = {}
        by_scope = {}
        by_tag = {}

        for record in records:
            by_kind.setdefault(
                record.operational_kind,
                [],
            ).append(
                record.record_id
            )

            if (
                record.scope_type
                == "general"
            ):
                scope_key = "general"

            else:
                scope_key = (
                    f"{record.scope_type}:"
                    f"{record.scope_id}"
                )

            by_scope.setdefault(
                scope_key,
                [],
            ).append(
                record.record_id
            )

            for tag in set(
                record.tags
            ):
                by_tag.setdefault(
                    tag,
                    [],
                ).append(
                    record.record_id
                )

        return {
            "schema_version": (
                LEARNING_INDEX_SCHEMA_VERSION
            ),
            "record_count": len(
                records
            ),
            "by_kind": {
                key: tuple(
                    sorted(values)
                )
                for key, values
                in sorted(
                    by_kind.items()
                )
            },
            "by_scope": {
                key: tuple(
                    sorted(values)
                )
                for key, values
                in sorted(
                    by_scope.items()
                )
            },
            "by_tag": {
                key: tuple(
                    sorted(values)
                )
                for key, values
                in sorted(
                    by_tag.items()
                )
            },
        }


    # --------------------------------------------------
    # User Context Trigger Index
    # --------------------------------------------------

    def context_trigger_index(
        self,
    ):
        """Return the Warm Context Trigger Index."""

        return self._get_or_build(
            cache_type=(
                "context-trigger-index"
            ),
            display_name=(
                "Context Trigger Index"
            ),
            builder=(
                self._build_context_trigger_index
            ),
        )


    def _build_context_trigger_index(
        self,
    ):
        records = (
            self.store
            .current_user_context()
        )

        routes = {}

        # Generation represents EVERY durable User Context
        # change, including retirement of a record that is
        # no longer present in current_user_context().
        #
        # Route Stamps must become stale whenever durable
        # User Context changes, not only when active records
        # happen to carry a newer generation.
        user_context_generation = (
            self.store.user_context_generation()
        )

        tagged_record_ids = set()

        for record in records:
            for tag in set(
                record.routing_tags
            ):
                tagged_record_ids.add(
                    record.record_id
                )

                route = routes.setdefault(
                    tag,
                    {
                        "record_ids": [],
                        "record_types": set(),
                        "must_check": False,
                    },
                )

                route[
                    "record_ids"
                ].append(
                    record.record_id
                )

                route[
                    "record_types"
                ].add(
                    record.record_type
                )

                # Phase 14's deterministic MUST CHECK
                # rule is deliberately narrow:
                #
                # only an explicit HARD user constraint
                # creates mandatory context retrieval.
                #
                # Spirit may later add richer policy.
                if (
                    record.record_type
                    == "user-constraint"
                    and record.strength
                    == "hard"
                ):
                    route[
                        "must_check"
                    ] = True

        frozen_routes = {}

        for tag, route in sorted(
            routes.items()
        ):
            frozen_routes[
                tag
            ] = {
                "mode": (
                    "must-check"
                    if route[
                        "must_check"
                    ]
                    else "check"
                ),
                "record_ids": tuple(
                    sorted(
                        set(
                            route[
                                "record_ids"
                            ]
                        )
                    )
                ),
                "record_types": tuple(
                    sorted(
                        route[
                            "record_types"
                        ]
                    )
                ),
            }

        return {
            "schema_version": (
                LEARNING_INDEX_SCHEMA_VERSION
            ),
            "record_count": len(
                records
            ),
            "user_context_generation": (
                user_context_generation
            ),
            "routes": frozen_routes,
            "untagged_record_count": (
                len(records)
                - len(
                    tagged_record_ids
                )
            ),
        }


    # --------------------------------------------------
    # Invalidation
    # --------------------------------------------------

    def invalidate(
        self,
    ):
        """Discard both derived Warm indexes."""

        removed = 0

        for cache_type in (
            "operational-learning-index",
            "context-trigger-index",
        ):
            removed += (
                self.cache.invalidate(
                    namespace="forest",
                    cache_type=cache_type,
                )
            )

        return removed
