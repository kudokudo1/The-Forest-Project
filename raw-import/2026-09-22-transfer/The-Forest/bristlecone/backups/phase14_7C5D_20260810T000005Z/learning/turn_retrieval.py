"""Turn-safe historical learning-record retrieval.

This module bridges:

- one immutable captured ContextRouteStamp,
- Task-local sticky record pools,
- the Forest-shared immutable snapshot provider.

A retained turn may READ compatible sticky state and may
retrieve its historical misses through the shared provider.

It deliberately never writes a retained turn's records back
into Task-sticky state.
"""

from __future__ import annotations

from dataclasses import dataclass

from .context_state import (
    ContextRouteStamp,
    ContextRouteState,
)

from .foundation import (
    ForestLearningRecord,
)

from .snapshot_provider import (
    ForestLearningSnapshotProvider,
)


TURN_HISTORICAL_RETRIEVAL_SCHEMA_VERSION = 1


class TurnHistoricalRetrievalError(
    RuntimeError
):
    """Turn historical retrieval failed closed."""


@dataclass(
    frozen=True
)
class TurnHistoricalRetrieval:
    """Exact records visible to one captured turn."""

    schema_version: int

    input_generation: int
    policy_generation: int

    user_context_generation: int
    operational_learning_generation: int

    user_context_records: tuple
    operational_learning_records: tuple

    user_sticky_hit_ids: tuple
    user_provider_load_ids: tuple

    operational_sticky_hit_ids: tuple
    operational_provider_load_ids: tuple


    @property
    def record_count(
        self,
    ):
        return (
            len(
                self.user_context_records
            )
            + len(
                self.operational_learning_records
            )
        )


    @property
    def is_empty(
        self,
    ):
        return (
            self.record_count
            == 0
        )


    def inspect(
        self,
    ):
        """Describe retrieval structure without record contents."""

        return {
            "schema_version": (
                self.schema_version
            ),
            "input_generation": (
                self.input_generation
            ),
            "policy_generation": (
                self.policy_generation
            ),
            "user_context_generation": (
                self.user_context_generation
            ),
            "operational_learning_generation": (
                self.operational_learning_generation
            ),
            "user_context_record_ids": tuple(
                record.record_id
                for record
                in self.user_context_records
            ),
            "operational_learning_record_ids": tuple(
                record.record_id
                for record
                in self.operational_learning_records
            ),
            "user_sticky_hit_ids": (
                self.user_sticky_hit_ids
            ),
            "user_provider_load_ids": (
                self.user_provider_load_ids
            ),
            "operational_sticky_hit_ids": (
                self.operational_sticky_hit_ids
            ),
            "operational_provider_load_ids": (
                self.operational_provider_load_ids
            ),
            "record_count": (
                self.record_count
            ),
        }


class TurnHistoricalRetrievalBridge:
    """Resolve exact records for one retained turn snapshot.

    The bridge retains only the Forest-shared snapshot provider.

    ContextRouteState and ContextRouteStamp are supplied for each
    call, so this object carries no Task, Clone, Tree, or turn
    identity between calls.
    """

    __slots__ = (
        "_snapshot_provider",
    )


    def __init__(
        self,
        snapshot_provider,
    ):
        if not isinstance(
            snapshot_provider,
            ForestLearningSnapshotProvider,
        ):
            raise TypeError(
                "TurnHistoricalRetrievalBridge requires "
                "a ForestLearningSnapshotProvider."
            )

        self._snapshot_provider = (
            snapshot_provider
        )


    @property
    def snapshot_provider(
        self,
    ):
        return self._snapshot_provider


    @staticmethod
    def _validate_inputs(
        context_state,
        stamp,
    ):
        if not isinstance(
            context_state,
            ContextRouteState,
        ):
            raise TypeError(
                "context_state must be a "
                "ContextRouteState."
            )

        if not isinstance(
            stamp,
            ContextRouteStamp,
        ):
            raise TypeError(
                "stamp must be a "
                "ContextRouteStamp."
            )


    @staticmethod
    def _validated_record(
        record,
        *,
        record_id,
        domain,
        generation,
    ):
        if not isinstance(
            record,
            ForestLearningRecord,
        ):
            raise TurnHistoricalRetrievalError(
                "Historical retrieval returned "
                "a non-learning record."
            )

        if (
            record.record_id
            != record_id
        ):
            raise TurnHistoricalRetrievalError(
                "Historical retrieval returned "
                "the wrong record ID."
            )

        if domain == "user-context":
            if not record.is_user_context:
                raise TurnHistoricalRetrievalError(
                    "Historical User Context "
                    "retrieval crossed record domains."
                )

            record_generation = (
                record.user_context_generation
            )

        elif (
            domain
            == "operational-learning"
        ):
            if (
                record.record_type
                != "operational-learning"
            ):
                raise TurnHistoricalRetrievalError(
                    "Historical Operational Learning "
                    "retrieval crossed record domains."
                )

            record_generation = (
                record
                .operational_learning_generation
            )

        else:
            raise TurnHistoricalRetrievalError(
                "Unsupported historical "
                "retrieval domain."
            )

        if (
            isinstance(
                record_generation,
                bool,
            )
            or not isinstance(
                record_generation,
                int,
            )
            or record_generation <= 0
            or record_generation > generation
        ):
            raise TurnHistoricalRetrievalError(
                "Retrieved record is outside "
                "the turn's captured generation."
            )

        return record


    def _resolve_user_context(
        self,
        context_state,
        stamp,
    ):
        selected_ids = tuple(
            stamp.user_context_record_ids
        )

        if not selected_ids:
            return (
                (),
                (),
                (),
            )

        sticky = (
            context_state
            .lookup_sticky_user_context_for_snapshot(
                stamp,
                selected_ids,
            )
        )

        by_id = {}
        sticky_ids = []


        for record in sticky.records:
            record_id = (
                record.record_id
            )

            if (
                record_id in by_id
            ):
                raise TurnHistoricalRetrievalError(
                    "Duplicate sticky User Context "
                    "record returned."
                )

            record = self._validated_record(
                record,
                record_id=record_id,
                domain="user-context",
                generation=(
                    stamp
                    .user_context_generation
                ),
            )

            if (
                record_id
                not in selected_ids
            ):
                raise TurnHistoricalRetrievalError(
                    "Sticky User Context returned "
                    "a record not selected by "
                    "this turn."
                )

            by_id[
                record_id
            ] = record

            sticky_ids.append(
                record_id
            )


        provider_ids = []


        for record_id in (
            sticky.missing_record_ids
        ):
            if (
                record_id
                not in selected_ids
            ):
                raise TurnHistoricalRetrievalError(
                    "Sticky User Context lookup "
                    "reported an unselected miss."
                )

            if (
                record_id
                in by_id
            ):
                raise TurnHistoricalRetrievalError(
                    "User Context record reported "
                    "as both sticky hit and miss."
                )

            record = (
                self._snapshot_provider
                .user_context_at_generation(
                    record_id,
                    stamp.user_context_generation,
                )
            )

            if record is None:
                raise TurnHistoricalRetrievalError(
                    "A User Context record selected "
                    "by the captured Route Stamp "
                    "does not exist in authoritative "
                    "history at that generation."
                )

            record = self._validated_record(
                record,
                record_id=record_id,
                domain="user-context",
                generation=(
                    stamp
                    .user_context_generation
                ),
            )

            by_id[
                record_id
            ] = record

            provider_ids.append(
                record_id
            )


        if (
            set(by_id)
            != set(selected_ids)
        ):
            raise TurnHistoricalRetrievalError(
                "User Context retrieval did not "
                "resolve exactly the records "
                "selected by the turn."
            )


        ordered = tuple(
            by_id[
                record_id
            ]
            for record_id
            in selected_ids
        )


        return (
            ordered,
            tuple(
                sticky_ids
            ),
            tuple(
                provider_ids
            ),
        )


    def _resolve_operational_learning(
        self,
        context_state,
        stamp,
    ):
        selected_ids = tuple(
            stamp
            .operational_learning_record_ids
        )

        if not selected_ids:
            return (
                (),
                (),
                (),
            )

        sticky = (
            context_state
            .lookup_sticky_operational_learning_for_snapshot(
                stamp,
                selected_ids,
            )
        )

        by_id = {}
        sticky_ids = []


        for record in sticky.records:
            record_id = (
                record.record_id
            )

            if (
                record_id in by_id
            ):
                raise TurnHistoricalRetrievalError(
                    "Duplicate sticky Operational "
                    "Learning record returned."
                )

            record = self._validated_record(
                record,
                record_id=record_id,
                domain=(
                    "operational-learning"
                ),
                generation=(
                    stamp
                    .operational_learning_generation
                ),
            )

            if (
                record_id
                not in selected_ids
            ):
                raise TurnHistoricalRetrievalError(
                    "Sticky Operational Learning "
                    "returned a record not selected "
                    "by this turn."
                )

            by_id[
                record_id
            ] = record

            sticky_ids.append(
                record_id
            )


        provider_ids = []


        for record_id in (
            sticky.missing_record_ids
        ):
            if (
                record_id
                not in selected_ids
            ):
                raise TurnHistoricalRetrievalError(
                    "Sticky Operational lookup "
                    "reported an unselected miss."
                )

            if (
                record_id
                in by_id
            ):
                raise TurnHistoricalRetrievalError(
                    "Operational record reported "
                    "as both sticky hit and miss."
                )

            record = (
                self._snapshot_provider
                .operational_learning_at_generation(
                    record_id,
                    stamp
                    .operational_learning_generation,
                )
            )

            if record is None:
                raise TurnHistoricalRetrievalError(
                    "An Operational Learning record "
                    "selected by the captured Route "
                    "Stamp does not exist in "
                    "authoritative history at that "
                    "generation."
                )

            record = self._validated_record(
                record,
                record_id=record_id,
                domain=(
                    "operational-learning"
                ),
                generation=(
                    stamp
                    .operational_learning_generation
                ),
            )

            by_id[
                record_id
            ] = record

            provider_ids.append(
                record_id
            )


        if (
            set(by_id)
            != set(selected_ids)
        ):
            raise TurnHistoricalRetrievalError(
                "Operational Learning retrieval "
                "did not resolve exactly the "
                "records selected by the turn."
            )


        ordered = tuple(
            by_id[
                record_id
            ]
            for record_id
            in selected_ids
        )


        return (
            ordered,
            tuple(
                sticky_ids
            ),
            tuple(
                provider_ids
            ),
        )


    def resolve(
        self,
        context_state,
        stamp,
    ):
        """Resolve exact records for one captured turn."""

        self._validate_inputs(
            context_state,
            stamp,
        )

        (
            user_records,
            user_sticky_ids,
            user_provider_ids,
        ) = self._resolve_user_context(
            context_state,
            stamp,
        )

        (
            operational_records,
            operational_sticky_ids,
            operational_provider_ids,
        ) = (
            self
            ._resolve_operational_learning(
                context_state,
                stamp,
            )
        )

        return TurnHistoricalRetrieval(
            schema_version=(
                TURN_HISTORICAL_RETRIEVAL_SCHEMA_VERSION
            ),
            input_generation=(
                stamp.input_generation
            ),
            policy_generation=(
                stamp.policy_generation
            ),
            user_context_generation=(
                stamp.user_context_generation
            ),
            operational_learning_generation=(
                stamp
                .operational_learning_generation
            ),
            user_context_records=(
                user_records
            ),
            operational_learning_records=(
                operational_records
            ),
            user_sticky_hit_ids=(
                user_sticky_ids
            ),
            user_provider_load_ids=(
                user_provider_ids
            ),
            operational_sticky_hit_ids=(
                operational_sticky_ids
            ),
            operational_provider_load_ids=(
                operational_provider_ids
            ),
        )
