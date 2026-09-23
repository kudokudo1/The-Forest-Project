"""Forest-shared immutable learning-record snapshot provider."""

from __future__ import annotations

from threading import (
    Condition,
    RLock,
)

from cache.coordinator import (
    CacheCoordinator,
)

from cache.entry import (
    CacheKey,
)

from .foundation import (
    ForestLearningError,
    ForestLearningRecord,
    ForestLearningStore,
)


LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION = 1

SNAPSHOT_CACHE_TYPE = (
    "learning-record-snapshot"
)

RESOLUTION_CACHE_TYPE = (
    "learning-record-resolution"
)

USER_CONTEXT_DOMAIN = (
    "user-context"
)

OPERATIONAL_LEARNING_DOMAIN = (
    "operational-learning"
)

_MISSING_REVISION = 0


class ForestLearningSnapshotProvider:
    """Share immutable historical records across callers.

    Relevance selection happens elsewhere.

    This provider resolves the authoritative record visible
    at one captured durable generation.

    Cache layers:

    resolution:
        (domain, record_id, generation)
        -> exact revision

    snapshot:
        (record_id, revision)
        -> immutable ForestLearningRecord

    Identical Cold misses are single-flighted by historical
    request key.
    """

    __slots__ = (
        "_store",
        "_cache_coordinator",
        "_condition",
        "_inflight",
    )


    def __init__(
        self,
        store,
        cache_coordinator=None,
    ):
        if not isinstance(
            store,
            ForestLearningStore,
        ):
            raise TypeError(
                "ForestLearningSnapshotProvider "
                "requires a ForestLearningStore."
            )

        if (
            cache_coordinator is not None
            and not isinstance(
                cache_coordinator,
                CacheCoordinator,
            )
        ):
            raise TypeError(
                "cache_coordinator must be a "
                "CacheCoordinator or None."
            )

        self._store = store

        self._cache_coordinator = (
            cache_coordinator
            if cache_coordinator is not None
            else CacheCoordinator()
        )

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
    def _validate_record_id(
        record_id,
    ):
        if (
            not isinstance(
                record_id,
                str,
            )
            or not record_id.strip()
        ):
            raise ForestLearningError(
                "record_id cannot be empty."
            )

        return record_id


    @staticmethod
    def _validate_generation(
        generation,
        *,
        field_name,
    ):
        if (
            isinstance(
                generation,
                bool,
            )
            or not isinstance(
                generation,
                int,
            )
            or generation < 0
        ):
            raise ForestLearningError(
                f"{field_name} must be "
                "an integer >= 0."
            )

        return generation


    @staticmethod
    def _record_matches_domain(
        record,
        domain,
    ):
        if not isinstance(
            record,
            ForestLearningRecord,
        ):
            return False

        if domain == USER_CONTEXT_DOMAIN:
            return record.is_user_context

        if (
            domain
            == OPERATIONAL_LEARNING_DOMAIN
        ):
            return (
                record.record_type
                == "operational-learning"
            )

        return False


    @staticmethod
    def _resolution_key(
        domain,
        record_id,
        generation,
    ):
        return CacheKey(
            namespace="forest",
            cache_type=(
                RESOLUTION_CACHE_TYPE
            ),
            identity=(
                domain,
                record_id,
                generation,
            ),
        )


    @staticmethod
    def _snapshot_key(
        record_id,
        revision,
    ):
        return CacheKey(
            namespace="forest",
            cache_type=(
                SNAPSHOT_CACHE_TYPE
            ),
            identity=(
                record_id,
                revision,
            ),
        )


    def _invalidate_resolution(
        self,
        key,
    ):
        self._cache_coordinator.invalidate(
            namespace=key.namespace,
            cache_type=key.cache_type,
            identity_prefix=(
                key.identity
            ),
        )


    def _invalidate_snapshot(
        self,
        key,
    ):
        self._cache_coordinator.invalidate(
            namespace=key.namespace,
            cache_type=key.cache_type,
            identity_prefix=(
                key.identity
            ),
        )


    def _cached_result(
        self,
        domain,
        record_id,
        generation,
    ):
        resolution_key = (
            self._resolution_key(
                domain,
                record_id,
                generation,
            )
        )

        resolution_entry = (
            self._cache_coordinator.get(
                resolution_key,
                schema_version=(
                    LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
                ),
            )
        )

        if resolution_entry is None:
            return (
                False,
                None,
            )

        revision = (
            resolution_entry.value
        )

        if revision == _MISSING_REVISION:
            return (
                True,
                None,
            )

        if (
            isinstance(
                revision,
                bool,
            )
            or not isinstance(
                revision,
                int,
            )
            or revision <= 0
        ):
            self._invalidate_resolution(
                resolution_key
            )

            return (
                False,
                None,
            )

        snapshot_key = (
            self._snapshot_key(
                record_id,
                revision,
            )
        )

        snapshot_entry = (
            self._cache_coordinator.get(
                snapshot_key,
                schema_version=(
                    LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
                ),
            )
        )

        if snapshot_entry is None:
            return (
                False,
                None,
            )

        record = snapshot_entry.value

        if (
            not self._record_matches_domain(
                record,
                domain,
            )
            or record.record_id
            != record_id
            or record.revision
            != revision
        ):
            self._invalidate_resolution(
                resolution_key
            )

            self._invalidate_snapshot(
                snapshot_key
            )

            return (
                False,
                None,
            )

        return (
            True,
            record,
        )


    def _current_generation(
        self,
        domain,
    ):
        if domain == USER_CONTEXT_DOMAIN:
            return (
                self._store
                .user_context_generation()
            )

        if (
            domain
            == OPERATIONAL_LEARNING_DOMAIN
        ):
            return (
                self._store
                .operational_learning_generation()
            )

        raise ForestLearningError(
            "Unsupported learning-record domain."
        )


    def _historical_load(
        self,
        domain,
        record_id,
        generation,
    ):
        if domain == USER_CONTEXT_DOMAIN:
            return (
                self._store
                .get_user_context_at_generation(
                    record_id,
                    generation,
                )
            )

        if (
            domain
            == OPERATIONAL_LEARNING_DOMAIN
        ):
            return (
                self._store
                .get_operational_learning_at_generation(
                    record_id,
                    generation,
                )
            )

        raise ForestLearningError(
            "Unsupported learning-record domain."
        )


    def _canonical_snapshot(
        self,
        domain,
        record,
    ):
        """Return the one shared object for an exact revision."""

        snapshot_key = (
            self._snapshot_key(
                record.record_id,
                record.revision,
            )
        )

        existing = (
            self._cache_coordinator.get(
                snapshot_key,
                schema_version=(
                    LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
                ),
            )
        )

        if existing is not None:
            cached = existing.value

            if (
                self._record_matches_domain(
                    cached,
                    domain,
                )
                and cached.record_id
                == record.record_id
                and cached.revision
                == record.revision
            ):
                return cached

            # A malformed derived entry is disposable.
            self._invalidate_snapshot(
                snapshot_key
            )

        self._cache_coordinator.put(
            snapshot_key,
            record,
            schema_version=(
                LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
            ),
            display_name=(
                "Immutable Forest learning "
                "record snapshot"
            ),
            metadata={
                "record_type": (
                    record.record_type
                ),
                "revision": (
                    record.revision
                ),
                "status": (
                    record.status
                ),
            },
        )

        return record


    def _cache_loaded_result(
        self,
        domain,
        record_id,
        generation,
        record,
    ):
        resolution_key = (
            self._resolution_key(
                domain,
                record_id,
                generation,
            )
        )

        if record is None:
            self._cache_coordinator.put(
                resolution_key,
                _MISSING_REVISION,
                schema_version=(
                    LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
                ),
                display_name=(
                    "Historical learning "
                    "record resolution"
                ),
                metadata={
                    "domain": domain,
                    "generation": generation,
                    "found": False,
                },
            )

            return None

        if (
            not self._record_matches_domain(
                record,
                domain,
            )
            or record.record_id
            != record_id
        ):
            raise ForestLearningError(
                "Authoritative historical "
                "lookup returned a "
                "mismatched record."
            )

        record_generation = (
            record.user_context_generation
            if domain
            == USER_CONTEXT_DOMAIN
            else (
                record
                .operational_learning_generation
            )
        )

        if (
            record_generation <= 0
            or record_generation
            > generation
        ):
            raise ForestLearningError(
                "Authoritative historical "
                "lookup returned a record "
                "outside the requested "
                "generation."
            )

        # Reuse an already-cached exact revision if
        # another generation resolved to it first.
        record = (
            self._canonical_snapshot(
                domain,
                record,
            )
        )

        # Resolution is written only after the exact
        # immutable snapshot is available.
        self._cache_coordinator.put(
            resolution_key,
            record.revision,
            schema_version=(
                LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
            ),
            display_name=(
                "Historical learning "
                "record resolution"
            ),
            metadata={
                "domain": domain,
                "generation": generation,
                "found": True,
                "revision": (
                    record.revision
                ),
            },
        )

        return record


    def _get_at_generation(
        self,
        domain,
        record_id,
        generation,
        *,
        generation_field,
    ):
        record_id = (
            self._validate_record_id(
                record_id
            )
        )

        generation = (
            self._validate_generation(
                generation,
                field_name=(
                    generation_field
                ),
            )
        )

        # Generation zero means this domain had no
        # authoritative state yet.
        if generation == 0:
            return None

        found, record = (
            self._cached_result(
                domain,
                record_id,
                generation,
            )
        )

        if found:
            return record

        flight_key = (
            domain,
            record_id,
            generation,
        )

        # The Condition protects only in-flight
        # coordination. Cold storage reads occur
        # outside this lock.
        with self._condition:

            while (
                flight_key
                in self._inflight
            ):
                self._condition.wait()

                found, record = (
                    self._cached_result(
                        domain,
                        record_id,
                        generation,
                    )
                )

                if found:
                    return record

            self._inflight.add(
                flight_key
            )

        try:
            # Cache may have filled while this caller
            # was becoming the leader.
            found, record = (
                self._cached_result(
                    domain,
                    record_id,
                    generation,
                )
            )

            if found:
                return record

            current_generation = (
                self._current_generation(
                    domain
                )
            )

            # Do not permanently cache an answer for a
            # generation that has not happened yet.
            if (
                generation
                > current_generation
            ):
                raise ForestLearningError(
                    f"{generation_field} "
                    f"{generation} is ahead "
                    "of authoritative "
                    f"generation "
                    f"{current_generation}."
                )

            record = (
                self._historical_load(
                    domain,
                    record_id,
                    generation,
                )
            )

            return (
                self._cache_loaded_result(
                    domain,
                    record_id,
                    generation,
                    record,
                )
            )

        finally:
            with self._condition:
                self._inflight.discard(
                    flight_key
                )

                self._condition.notify_all()


    def user_context_at_generation(
        self,
        record_id,
        user_context_generation,
    ):
        return self._get_at_generation(
            USER_CONTEXT_DOMAIN,
            record_id,
            user_context_generation,
            generation_field=(
                "user_context_generation"
            ),
        )


    def operational_learning_at_generation(
        self,
        record_id,
        operational_learning_generation,
    ):
        return self._get_at_generation(
            OPERATIONAL_LEARNING_DOMAIN,
            record_id,
            operational_learning_generation,
            generation_field=(
                "operational_learning_generation"
            ),
        )


    def inspect(
        self,
    ):
        """Return structure only, never record contents."""

        with self._condition:
            inflight_count = len(
                self._inflight
            )

        cache_entries = [
            entry
            for entry
            in self._cache_coordinator.inspect()
            if (
                entry["cache_type"]
                in {
                    SNAPSHOT_CACHE_TYPE,
                    RESOLUTION_CACHE_TYPE,
                }
            )
        ]

        return {
            "schema_version": (
                LEARNING_SNAPSHOT_CACHE_SCHEMA_VERSION
            ),
            "inflight_count": (
                inflight_count
            ),
            "cache_entry_count": len(
                cache_entries
            ),
            "cache_entries": (
                cache_entries
            ),
        }
