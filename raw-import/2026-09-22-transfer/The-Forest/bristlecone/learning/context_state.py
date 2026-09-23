"""Ephemeral Context Route State for one active Task.

The state combines:

- a Context Route Stamp
- Task-Sticky User Context
- Task-Sticky Operational Learning

Core rule:

    conversation changes invalidate routing;
    execution steps do not.

A new meaningful user input invalidates the Route Stamp but
provisionally retains sticky records. Those retained records
cannot be reused until the NEW routing decision selects them
again.

User Context and Operational Learning have independent
durable generations, so each sticky pool can become stale
without unnecessarily discarding the other.

Nothing in this module is durable.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Tuple

from .context_matcher import (
    ContextTriggerMatch,
)

from .foundation import (
    ForestLearningRecord,
)

from .operational_matcher import (
    OperationalLearningMatch,
)


CONTEXT_ROUTE_STAMP_SCHEMA_VERSION = 1


class ContextRouteStateError(
    RuntimeError
):
    """Raised when ephemeral Task context state is invalid."""


def _generation(
    name,
    value,
):
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value < 0
    ):
        raise ContextRouteStateError(
            f"{name} must be an integer >= 0."
        )

    return value


def _string_tuple(
    values,
    *,
    field_name,
    sort_values=False,
):
    if isinstance(
        values,
        str,
    ):
        raise ContextRouteStateError(
            f"{field_name} must be a collection "
            "of strings, not one string."
        )

    try:
        items = tuple(
            values
        )

    except TypeError as exc:
        raise ContextRouteStateError(
            f"{field_name} must be iterable."
        ) from exc

    result = []
    seen = set()

    for value in items:
        if (
            not isinstance(
                value,
                str,
            )
            or not value.strip()
        ):
            raise ContextRouteStateError(
                f"{field_name} entries must be "
                "non-empty strings."
            )

        clean = value.strip()

        if clean in seen:
            continue

        seen.add(
            clean
        )

        result.append(
            clean
        )

    if sort_values:
        result.sort()

    return tuple(
        result
    )


@dataclass(
    frozen=True
)
class ContextRouteStamp:
    """Tiny memo of one completed routing decision."""

    schema_version: int

    input_generation: int

    user_context_generation: int
    operational_learning_generation: int
    policy_generation: int

    context_mode: str

    context_requested_signals: Tuple[str, ...]
    context_matched_signals: Tuple[str, ...]
    context_must_check_signals: Tuple[str, ...]

    user_context_record_ids: Tuple[str, ...]

    operational_requested_kinds: Tuple[str, ...]
    operational_requested_tags: Tuple[str, ...]
    operational_scope_keys: Tuple[str, ...]

    operational_learning_record_ids: Tuple[str, ...]


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != CONTEXT_ROUTE_STAMP_SCHEMA_VERSION
        ):
            raise ContextRouteStateError(
                "Unsupported Context Route Stamp "
                "schema version."
            )

        for name in (
            "input_generation",
            "user_context_generation",
            "operational_learning_generation",
            "policy_generation",
        ):
            _generation(
                name,
                getattr(
                    self,
                    name,
                ),
            )

        if self.context_mode not in {
            "none",
            "check",
            "must-check",
        }:
            raise ContextRouteStateError(
                "context_mode must be none, "
                "check, or must-check."
            )

        for field_name in (
            "context_requested_signals",
            "context_matched_signals",
            "context_must_check_signals",
            "operational_requested_kinds",
            "operational_requested_tags",
            "operational_scope_keys",
        ):
            object.__setattr__(
                self,
                field_name,
                _string_tuple(
                    getattr(
                        self,
                        field_name,
                    ),
                    field_name=field_name,
                ),
            )

        for field_name in (
            "user_context_record_ids",
            "operational_learning_record_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _string_tuple(
                    getattr(
                        self,
                        field_name,
                    ),
                    field_name=field_name,
                    sort_values=True,
                ),
            )


    @classmethod
    def from_matches(
        cls,
        *,
        input_generation,
        policy_generation,
        context_match,
        operational_match,
    ):
        """Build a stamp directly from both Warm match results."""

        if not isinstance(
            context_match,
            ContextTriggerMatch,
        ):
            raise ContextRouteStateError(
                "context_match must be "
                "ContextTriggerMatch."
            )

        if not isinstance(
            operational_match,
            OperationalLearningMatch,
        ):
            raise ContextRouteStateError(
                "operational_match must be "
                "OperationalLearningMatch."
            )

        return cls(
            schema_version=(
                CONTEXT_ROUTE_STAMP_SCHEMA_VERSION
            ),
            input_generation=(
                input_generation
            ),
            user_context_generation=(
                context_match
                .user_context_generation
            ),
            operational_learning_generation=(
                operational_match
                .operational_learning_generation
            ),
            policy_generation=(
                policy_generation
            ),
            context_mode=(
                context_match.mode
            ),
            context_requested_signals=(
                context_match.requested_signals
            ),
            context_matched_signals=(
                context_match.matched_signals
            ),
            context_must_check_signals=(
                context_match.must_check_signals
            ),
            user_context_record_ids=(
                context_match.record_ids
            ),
            operational_requested_kinds=(
                operational_match.requested_kinds
            ),
            operational_requested_tags=(
                operational_match.requested_tags
            ),
            operational_scope_keys=(
                operational_match.requested_scope_keys
            ),
            operational_learning_record_ids=(
                operational_match.record_ids
            ),
        )


    def is_valid_for(
        self,
        *,
        input_generation,
        user_context_generation,
        operational_learning_generation,
        policy_generation,
    ):
        return (
            self.input_generation
            == input_generation
            and self.user_context_generation
            == user_context_generation
            and self.operational_learning_generation
            == operational_learning_generation
            and self.policy_generation
            == policy_generation
        )


@dataclass(
    frozen=True
)
class StickyRecordLookup:
    """Already-loaded records plus IDs still requiring Cold load."""

    records: Tuple[
        ForestLearningRecord,
        ...
    ]

    missing_record_ids: Tuple[str, ...]


    @property
    def complete(
        self,
    ):
        return not self.missing_record_ids


class ContextRouteState:
    """Task-local route and dual sticky pools.

    Ownership is established by the caller holding this object,
    so Tree/Clone identity is intentionally not embedded here.
    """

    def __init__(
        self,
        *,
        input_generation=0,
        policy_generation=0,
    ):
        self._lock = RLock()

        self._input_generation = _generation(
            "input_generation",
            input_generation,
        )

        self._policy_generation = _generation(
            "policy_generation",
            policy_generation,
        )

        self._route_stamp = None

        self._sticky_user_context_generation = None
        self._sticky_user_context = {}

        self._sticky_operational_generation = None
        self._sticky_operational_learning = {}


    @property
    def input_generation(
        self,
    ):
        with self._lock:
            return self._input_generation


    @property
    def policy_generation(
        self,
    ):
        with self._lock:
            return self._policy_generation


    @property
    def route_stamp(
        self,
    ):
        with self._lock:
            return self._route_stamp


    def capture_turn_route(
        self,
    ):
        """Capture the current immutable route for one turn.

        The returned ContextRouteStamp is frozen and may be
        retained by an in-flight turn even after a later
        meaningful input replaces the Task's current route.
        """

        with self._lock:
            stamp = self._route_stamp

            if stamp is None:
                raise ContextRouteStateError(
                    "Cannot capture a turn route "
                    "before current input is routed."
                )

            return stamp


    def _validate_turn_snapshot_unlocked(
        self,
        stamp,
    ):
        """Validate a retained turn snapshot.

        Input generation is deliberately NOT compared with the
        Task's current input generation. A later turn beginning
        must not invalidate an already-running turn.

        Relevant policy change DOES invalidate the snapshot.
        """

        if not isinstance(
            stamp,
            ContextRouteStamp,
        ):
            raise ContextRouteStateError(
                "Turn snapshot must be "
                "ContextRouteStamp."
            )

        if (
            stamp.policy_generation
            != self._policy_generation
        ):
            raise ContextRouteStateError(
                "Turn snapshot policy generation "
                "is no longer current."
            )

        return stamp


    @property
    def sticky_user_context_count(
        self,
    ):
        with self._lock:
            return len(
                self._sticky_user_context
            )


    @property
    def sticky_operational_learning_count(
        self,
    ):
        with self._lock:
            return len(
                self._sticky_operational_learning
            )


    # --------------------------------------------------
    # Input / execution lifecycle
    # --------------------------------------------------

    def begin_meaningful_input(
        self,
    ):
        """New conversational input invalidates routing only."""

        with self._lock:
            self._input_generation += 1

            self._route_stamp = None

            return self._input_generation


    def note_execution_step(
        self,
    ):
        """Tool/reasoning steps do not invalidate routing."""

        with self._lock:
            return self._input_generation


    # --------------------------------------------------
    # Policy lifecycle
    # --------------------------------------------------

    def set_policy_generation(
        self,
        generation,
    ):
        """Relevant policy change invalidates all loaded context."""

        generation = _generation(
            "policy_generation",
            generation,
        )

        with self._lock:
            if (
                generation
                == self._policy_generation
            ):
                return False

            self._policy_generation = generation
            self._route_stamp = None

            self._clear_user_context_unlocked()
            self._clear_operational_unlocked()

            return True


    # --------------------------------------------------
    # Route lifecycle
    # --------------------------------------------------

    def commit_route(
        self,
        stamp,
    ):
        if not isinstance(
            stamp,
            ContextRouteStamp,
        ):
            raise ContextRouteStateError(
                "stamp must be ContextRouteStamp."
            )

        with self._lock:
            if (
                stamp.input_generation
                != self._input_generation
            ):
                raise ContextRouteStateError(
                    "Route Stamp input generation "
                    "does not match current Task input."
                )

            if (
                stamp.policy_generation
                != self._policy_generation
            ):
                raise ContextRouteStateError(
                    "Route Stamp policy generation "
                    "does not match current policy."
                )

            self._route_stamp = stamp

            return stamp


    def commit_matches(
        self,
        *,
        context_match,
        operational_match,
    ):
        """Build and commit a stamp from both Warm matchers."""

        with self._lock:
            stamp = ContextRouteStamp.from_matches(
                input_generation=(
                    self._input_generation
                ),
                policy_generation=(
                    self._policy_generation
                ),
                context_match=context_match,
                operational_match=(
                    operational_match
                ),
            )

            self._route_stamp = stamp

            return stamp


    def reusable_route(
        self,
        *,
        user_context_generation,
        operational_learning_generation,
    ):
        """Return stamp only while all freshness clocks match.

        Sticky pools are independently invalidated even when
        there is currently no Route Stamp.
        """

        user_generation = _generation(
            "user_context_generation",
            user_context_generation,
        )

        operational_generation = _generation(
            "operational_learning_generation",
            operational_learning_generation,
        )

        with self._lock:
            if (
                self._sticky_user_context_generation
                is not None
                and (
                    self._sticky_user_context_generation
                    != user_generation
                )
            ):
                self._clear_user_context_unlocked()

            if (
                self._sticky_operational_generation
                is not None
                and (
                    self._sticky_operational_generation
                    != operational_generation
                )
            ):
                self._clear_operational_unlocked()

            stamp = self._route_stamp

            if stamp is None:
                return None

            if not stamp.is_valid_for(
                input_generation=(
                    self._input_generation
                ),
                user_context_generation=(
                    user_generation
                ),
                operational_learning_generation=(
                    operational_generation
                ),
                policy_generation=(
                    self._policy_generation
                ),
            ):
                self._route_stamp = None
                return None

            return stamp


    # --------------------------------------------------
    # Internal route checks
    # --------------------------------------------------

    def _require_route_unlocked(
        self,
    ):
        stamp = self._route_stamp

        if stamp is None:
            raise ContextRouteStateError(
                "Sticky context cannot be used "
                "before current input is routed."
            )

        return stamp


    # --------------------------------------------------
    # User Context sticky pool
    # --------------------------------------------------

    def remember_user_context(
        self,
        records,
        *,
        user_context_generation,
    ):
        generation = _generation(
            "user_context_generation",
            user_context_generation,
        )

        try:
            records = tuple(
                records
            )

        except TypeError as exc:
            raise ContextRouteStateError(
                "records must be iterable."
            ) from exc

        with self._lock:
            stamp = self._require_route_unlocked()

            if (
                stamp.user_context_generation
                != generation
            ):
                raise ContextRouteStateError(
                    "User Context generation does "
                    "not match current Route Stamp."
                )

            allowed_ids = set(
                stamp.user_context_record_ids
            )

            if (
                self._sticky_user_context_generation
                != generation
            ):
                self._clear_user_context_unlocked()

                self._sticky_user_context_generation = (
                    generation
                )

            for record in records:
                if not isinstance(
                    record,
                    ForestLearningRecord,
                ):
                    raise ContextRouteStateError(
                        "Sticky User Context must contain "
                        "ForestLearningRecord values."
                    )

                if not record.is_user_context:
                    raise ContextRouteStateError(
                        "Operational Learning cannot enter "
                        "the User Context sticky pool."
                    )

                if (
                    record.record_id
                    not in allowed_ids
                ):
                    raise ContextRouteStateError(
                        "User Context record was not "
                        "selected by current routing."
                    )

                self._sticky_user_context[
                    record.record_id
                ] = record

            return len(
                records
            )


    def lookup_sticky_user_context(
        self,
        record_ids,
        *,
        user_context_generation,
    ):
        requested = _string_tuple(
            record_ids,
            field_name="record_ids",
            sort_values=True,
        )

        generation = _generation(
            "user_context_generation",
            user_context_generation,
        )

        with self._lock:
            stamp = self._require_route_unlocked()

            if (
                stamp.user_context_generation
                != generation
            ):
                self._clear_user_context_unlocked()

                raise ContextRouteStateError(
                    "User Context generation does "
                    "not match current Route Stamp."
                )

            allowed_ids = set(
                stamp.user_context_record_ids
            )

            if not set(
                requested
            ).issubset(
                allowed_ids
            ):
                raise ContextRouteStateError(
                    "Sticky User Context lookup requested "
                    "records not selected by current route."
                )

            if (
                self._sticky_user_context_generation
                != generation
            ):
                self._clear_user_context_unlocked()

                return StickyRecordLookup(
                    records=(),
                    missing_record_ids=(
                        requested
                    ),
                )

            found = []
            missing = []

            for record_id in requested:
                record = (
                    self._sticky_user_context
                    .get(
                        record_id
                    )
                )

                if record is None:
                    missing.append(
                        record_id
                    )

                else:
                    found.append(
                        record
                    )

            return StickyRecordLookup(
                records=tuple(
                    found
                ),
                missing_record_ids=tuple(
                    missing
                ),
            )


    def lookup_sticky_user_context_for_snapshot(
        self,
        stamp,
        record_ids,
    ):
        """Read compatible sticky User Context for one turn.

        Unlike lookup_sticky_user_context(), this method does
        not require the supplied snapshot to remain the Task's
        current Route Stamp.

        Generation mismatch returns misses but NEVER clears or
        downgrades another turn's newer sticky pool.
        """

        requested = _string_tuple(
            record_ids,
            field_name="record_ids",
            sort_values=True,
        )

        with self._lock:
            stamp = (
                self._validate_turn_snapshot_unlocked(
                    stamp
                )
            )

            allowed_ids = set(
                stamp.user_context_record_ids
            )

            if not set(
                requested
            ).issubset(
                allowed_ids
            ):
                raise ContextRouteStateError(
                    "Turn snapshot User Context lookup "
                    "requested records not selected "
                    "by that turn."
                )

            if (
                self._sticky_user_context_generation
                != stamp.user_context_generation
            ):
                return StickyRecordLookup(
                    records=(),
                    missing_record_ids=requested,
                )

            found = []
            missing = []

            for record_id in requested:
                record = (
                    self._sticky_user_context.get(
                        record_id
                    )
                )

                if record is None:
                    missing.append(
                        record_id
                    )

                else:
                    found.append(
                        record
                    )

            return StickyRecordLookup(
                records=tuple(
                    found
                ),
                missing_record_ids=tuple(
                    missing
                ),
            )


    # --------------------------------------------------
    # Operational Learning sticky pool
    # --------------------------------------------------

    def remember_operational_learning(
        self,
        records,
        *,
        operational_learning_generation,
    ):
        generation = _generation(
            "operational_learning_generation",
            operational_learning_generation,
        )

        try:
            records = tuple(
                records
            )

        except TypeError as exc:
            raise ContextRouteStateError(
                "records must be iterable."
            ) from exc

        with self._lock:
            stamp = self._require_route_unlocked()

            if (
                stamp.operational_learning_generation
                != generation
            ):
                raise ContextRouteStateError(
                    "Operational Learning generation "
                    "does not match current Route Stamp."
                )

            allowed_ids = set(
                stamp.operational_learning_record_ids
            )

            if (
                self._sticky_operational_generation
                != generation
            ):
                self._clear_operational_unlocked()

                self._sticky_operational_generation = (
                    generation
                )

            for record in records:
                if not isinstance(
                    record,
                    ForestLearningRecord,
                ):
                    raise ContextRouteStateError(
                        "Sticky Operational Learning must "
                        "contain ForestLearningRecord values."
                    )

                if (
                    record.record_type
                    != "operational-learning"
                ):
                    raise ContextRouteStateError(
                        "User Context cannot enter the "
                        "Operational Learning sticky pool."
                    )

                if (
                    record.record_id
                    not in allowed_ids
                ):
                    raise ContextRouteStateError(
                        "Operational Learning record was "
                        "not selected by current routing."
                    )

                self._sticky_operational_learning[
                    record.record_id
                ] = record

            return len(
                records
            )


    def lookup_sticky_operational_learning(
        self,
        record_ids,
        *,
        operational_learning_generation,
    ):
        requested = _string_tuple(
            record_ids,
            field_name="record_ids",
            sort_values=True,
        )

        generation = _generation(
            "operational_learning_generation",
            operational_learning_generation,
        )

        with self._lock:
            stamp = self._require_route_unlocked()

            if (
                stamp.operational_learning_generation
                != generation
            ):
                self._clear_operational_unlocked()

                raise ContextRouteStateError(
                    "Operational Learning generation "
                    "does not match current Route Stamp."
                )

            allowed_ids = set(
                stamp.operational_learning_record_ids
            )

            if not set(
                requested
            ).issubset(
                allowed_ids
            ):
                raise ContextRouteStateError(
                    "Sticky Operational lookup requested "
                    "records not selected by current route."
                )

            if (
                self._sticky_operational_generation
                != generation
            ):
                self._clear_operational_unlocked()

                return StickyRecordLookup(
                    records=(),
                    missing_record_ids=(
                        requested
                    ),
                )

            found = []
            missing = []

            for record_id in requested:
                record = (
                    self._sticky_operational_learning
                    .get(
                        record_id
                    )
                )

                if record is None:
                    missing.append(
                        record_id
                    )

                else:
                    found.append(
                        record
                    )

            return StickyRecordLookup(
                records=tuple(
                    found
                ),
                missing_record_ids=tuple(
                    missing
                ),
            )


    def lookup_sticky_operational_learning_for_snapshot(
        self,
        stamp,
        record_ids,
    ):
        """Read compatible sticky Operational Learning.

        A later conversational turn may replace the Task's
        current route while this snapshot remains valid.

        Generation mismatch produces misses and never mutates
        another turn's sticky state.
        """

        requested = _string_tuple(
            record_ids,
            field_name="record_ids",
            sort_values=True,
        )

        with self._lock:
            stamp = (
                self._validate_turn_snapshot_unlocked(
                    stamp
                )
            )

            allowed_ids = set(
                stamp.operational_learning_record_ids
            )

            if not set(
                requested
            ).issubset(
                allowed_ids
            ):
                raise ContextRouteStateError(
                    "Turn snapshot Operational lookup "
                    "requested records not selected "
                    "by that turn."
                )

            if (
                self._sticky_operational_generation
                != stamp.operational_learning_generation
            ):
                return StickyRecordLookup(
                    records=(),
                    missing_record_ids=requested,
                )

            found = []
            missing = []

            for record_id in requested:
                record = (
                    self._sticky_operational_learning.get(
                        record_id
                    )
                )

                if record is None:
                    missing.append(
                        record_id
                    )

                else:
                    found.append(
                        record
                    )

            return StickyRecordLookup(
                records=tuple(
                    found
                ),
                missing_record_ids=tuple(
                    missing
                ),
            )


    # --------------------------------------------------
    # Clearing
    # --------------------------------------------------

    def clear_route(
        self,
    ):
        with self._lock:
            had_route = (
                self._route_stamp
                is not None
            )

            self._route_stamp = None

            return had_route


    def _clear_user_context_unlocked(
        self,
    ):
        count = len(
            self._sticky_user_context
        )

        self._sticky_user_context.clear()

        self._sticky_user_context_generation = None

        return count


    def clear_sticky_user_context(
        self,
    ):
        with self._lock:
            return self._clear_user_context_unlocked()


    def _clear_operational_unlocked(
        self,
    ):
        count = len(
            self._sticky_operational_learning
        )

        self._sticky_operational_learning.clear()

        self._sticky_operational_generation = None

        return count


    def clear_sticky_operational_learning(
        self,
    ):
        with self._lock:
            return self._clear_operational_unlocked()


    def clear_all(
        self,
    ):
        """Task-end cleanup."""

        with self._lock:
            self._route_stamp = None

            user_count = (
                self._clear_user_context_unlocked()
            )

            operational_count = (
                self._clear_operational_unlocked()
            )

            return {
                "user_context": user_count,
                "operational_learning": operational_count,
            }


    # --------------------------------------------------
    # Inspection
    # --------------------------------------------------

    def inspect(
        self,
    ):
        """Metadata only; never expose context contents."""

        with self._lock:
            stamp = self._route_stamp

            return {
                "input_generation": (
                    self._input_generation
                ),
                "policy_generation": (
                    self._policy_generation
                ),
                "route_present": (
                    stamp is not None
                ),
                "route_user_context_generation": (
                    None
                    if stamp is None
                    else (
                        stamp.user_context_generation
                    )
                ),
                "route_operational_learning_generation": (
                    None
                    if stamp is None
                    else (
                        stamp
                        .operational_learning_generation
                    )
                ),
                "route_user_context_record_count": (
                    0
                    if stamp is None
                    else len(
                        stamp.user_context_record_ids
                    )
                ),
                "route_operational_record_count": (
                    0
                    if stamp is None
                    else len(
                        stamp
                        .operational_learning_record_ids
                    )
                ),
                "sticky_user_context_generation": (
                    self._sticky_user_context_generation
                ),
                "sticky_user_context_count": len(
                    self._sticky_user_context
                ),
                "sticky_operational_learning_generation": (
                    self._sticky_operational_generation
                ),
                "sticky_operational_learning_count": len(
                    self._sticky_operational_learning
                ),
            }
