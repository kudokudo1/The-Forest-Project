"""Compose one immutable instruction snapshot for a routed turn.

Flow:

captured ContextRouteStamp
    -> TurnHistoricalRetrievalBridge
    -> exact historical records
    -> LayeredHotContextAssembler
    -> immutable instruction string

This module does not route context, mutate sticky state,
read Cold storage directly, or contact a runtime.
"""

from __future__ import annotations

from dataclasses import dataclass

from .context_state import (
    ContextRouteStamp,
    ContextRouteState,
)

from .hot_context import (
    HotContextAssembly,
    LayeredHotContextAssembler,
)

from .turn_retrieval import (
    TurnHistoricalRetrieval,
    TurnHistoricalRetrievalBridge,
)


TURN_INSTRUCTION_SCHEMA_VERSION = 1


class TurnInstructionCompositionError(
    RuntimeError
):
    """One captured turn could not be composed safely."""


@dataclass(
    frozen=True
)
class TurnInstructionComposition:
    """Immutable instructions and provenance for one turn."""

    schema_version: int

    input_generation: int
    policy_generation: int

    user_context_generation: int
    operational_learning_generation: int

    instructions: str

    user_context_record_ids: tuple
    operational_learning_record_ids: tuple

    section_names: tuple
    character_count: int

    user_sticky_hit_ids: tuple
    user_provider_load_ids: tuple

    operational_sticky_hit_ids: tuple
    operational_provider_load_ids: tuple


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != TURN_INSTRUCTION_SCHEMA_VERSION
        ):
            raise TurnInstructionCompositionError(
                "Unsupported Turn Instruction "
                "schema version."
            )

        if not isinstance(
            self.instructions,
            str,
        ):
            raise TurnInstructionCompositionError(
                "instructions must be a string."
            )

        if (
            isinstance(
                self.character_count,
                bool,
            )
            or not isinstance(
                self.character_count,
                int,
            )
            or self.character_count < 0
        ):
            raise TurnInstructionCompositionError(
                "character_count must be "
                "an integer >= 0."
            )

        if (
            self.character_count
            != len(
                self.instructions
            )
        ):
            raise TurnInstructionCompositionError(
                "character_count does not match "
                "instruction length."
            )


    @property
    def record_count(
        self,
    ):
        return (
            len(
                self.user_context_record_ids
            )
            + len(
                self.operational_learning_record_ids
            )
        )


    @property
    def is_empty(
        self,
    ):
        return (
            self.record_count == 0
        )


    def inspect(
        self,
    ):
        """Metadata only; never duplicate instruction contents."""

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
            "record_count": (
                self.record_count
            ),
            "user_context_record_ids": (
                self.user_context_record_ids
            ),
            "operational_learning_record_ids": (
                self.operational_learning_record_ids
            ),
            "section_names": (
                self.section_names
            ),
            "character_count": (
                self.character_count
            ),
            "empty": (
                self.is_empty
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
        }


class TurnInstructionComposer:
    """Compose Hot Context exactly once for one captured turn."""

    __slots__ = (
        "_retrieval_bridge",
        "_assembler",
    )


    def __init__(
        self,
        retrieval_bridge,
        assembler,
    ):
        if not isinstance(
            retrieval_bridge,
            TurnHistoricalRetrievalBridge,
        ):
            raise TypeError(
                "retrieval_bridge must be a "
                "TurnHistoricalRetrievalBridge."
            )

        if not isinstance(
            assembler,
            LayeredHotContextAssembler,
        ):
            raise TypeError(
                "assembler must be a "
                "LayeredHotContextAssembler."
            )

        self._retrieval_bridge = (
            retrieval_bridge
        )

        self._assembler = assembler


    @property
    def retrieval_bridge(
        self,
    ):
        return self._retrieval_bridge


    @property
    def assembler(
        self,
    ):
        return self._assembler


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
    def _validate_alignment(
        retrieval,
        assembly,
    ):
        if not isinstance(
            retrieval,
            TurnHistoricalRetrieval,
        ):
            raise TurnInstructionCompositionError(
                "retrieval result has the "
                "wrong type."
            )

        if not isinstance(
            assembly,
            HotContextAssembly,
        ):
            raise TurnInstructionCompositionError(
                "Hot Context assembly has "
                "the wrong type."
            )

        retrieval_user_ids = tuple(
            record.record_id
            for record
            in retrieval.user_context_records
        )

        retrieval_operational_ids = tuple(
            record.record_id
            for record
            in retrieval.operational_learning_records
        )

        if (
            assembly.user_context_record_ids
            != retrieval_user_ids
        ):
            raise TurnInstructionCompositionError(
                "Assembler User Context IDs do not "
                "match historical retrieval."
            )

        if (
            assembly.operational_learning_record_ids
            != retrieval_operational_ids
        ):
            raise TurnInstructionCompositionError(
                "Assembler Operational Learning IDs "
                "do not match historical retrieval."
            )


    def compose_from_retrieval(
        self,
        retrieval,
    ):
        """Assemble one already-resolved historical turn."""

        if not isinstance(
            retrieval,
            TurnHistoricalRetrieval,
        ):
            raise TypeError(
                "retrieval must be a "
                "TurnHistoricalRetrieval."
            )

        assembly = (
            self._assembler.assemble(
                retrieval.user_context_records,
                retrieval.operational_learning_records,
            )
        )

        self._validate_alignment(
            retrieval,
            assembly,
        )

        return TurnInstructionComposition(
            schema_version=(
                TURN_INSTRUCTION_SCHEMA_VERSION
            ),
            input_generation=(
                retrieval.input_generation
            ),
            policy_generation=(
                retrieval.policy_generation
            ),
            user_context_generation=(
                retrieval.user_context_generation
            ),
            operational_learning_generation=(
                retrieval
                .operational_learning_generation
            ),
            instructions=(
                assembly.prompt
            ),
            user_context_record_ids=(
                assembly
                .user_context_record_ids
            ),
            operational_learning_record_ids=(
                assembly
                .operational_learning_record_ids
            ),
            section_names=(
                assembly.section_names
            ),
            character_count=(
                assembly.character_count
            ),
            user_sticky_hit_ids=(
                retrieval.user_sticky_hit_ids
            ),
            user_provider_load_ids=(
                retrieval.user_provider_load_ids
            ),
            operational_sticky_hit_ids=(
                retrieval
                .operational_sticky_hit_ids
            ),
            operational_provider_load_ids=(
                retrieval
                .operational_provider_load_ids
            ),
        )


    def compose(
        self,
        context_state,
        stamp,
    ):
        """Retrieve and assemble one captured turn exactly once."""

        self._validate_inputs(
            context_state,
            stamp,
        )

        retrieval = (
            self._retrieval_bridge.resolve(
                context_state,
                stamp,
            )
        )

        return self.compose_from_retrieval(
            retrieval
        )
