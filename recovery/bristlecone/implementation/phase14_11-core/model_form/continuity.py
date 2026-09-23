"""Forest-level continuity for a Model Form transition.

ModelFormContinuity combines the already-frozen Forest
instruction composition with the already-completed portable
conversation for one Task/execution context.

It contains no runtime session, adapter, model name,
binding, KV cache, or mutable routing state.
"""

from dataclasses import dataclass

from runtime.conversation_continuity import (
    ConversationContinuity,
)
from turn_composition import (
    ForestTurnInstructionComposition,
)


MODEL_FORM_CONTINUITY_SCHEMA_VERSION = 1


class ModelFormContinuityError(
    ValueError
):
    """Invalid Model Form continuity envelope."""


def _nonempty_string(
    name,
    value,
):
    if not isinstance(
        value,
        str,
    ):
        raise ModelFormContinuityError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ModelFormContinuityError(
            f"{name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ModelFormContinuity:
    """Immutable Forest-owned continuity for one turn.

    The instruction composition represents the exact
    already-assembled informational basis for the current
    meaningful turn.

    Conversation continuity contains only previously
    completed public exchanges. The current in-flight
    message is deliberately absent.
    """

    execution_context_id: str
    task_id: str
    turn_instructions: (
        ForestTurnInstructionComposition
    )
    conversation: ConversationContinuity
    schema_version: int = (
        MODEL_FORM_CONTINUITY_SCHEMA_VERSION
    )

    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != MODEL_FORM_CONTINUITY_SCHEMA_VERSION
        ):
            raise ModelFormContinuityError(
                "Unsupported Model Form "
                "continuity schema version."
            )

        execution_context_id = (
            _nonempty_string(
                "execution_context_id",
                self.execution_context_id,
            )
        )

        task_id = _nonempty_string(
            "task_id",
            self.task_id,
        )

        if not isinstance(
            self.turn_instructions,
            ForestTurnInstructionComposition,
        ):
            raise ModelFormContinuityError(
                "turn_instructions must be "
                "ForestTurnInstructionComposition."
            )

        if not isinstance(
            self.conversation,
            ConversationContinuity,
        ):
            raise ModelFormContinuityError(
                "conversation must be "
                "ConversationContinuity."
            )

        if (
            self.conversation.execution_context_id
            != execution_context_id
        ):
            raise ModelFormContinuityError(
                "Conversation continuity belongs "
                "to a different execution context."
            )

        if (
            self.conversation.task_id
            != task_id
        ):
            raise ModelFormContinuityError(
                "Conversation continuity belongs "
                "to a different Task."
            )

        object.__setattr__(
            self,
            "execution_context_id",
            execution_context_id,
        )

        object.__setattr__(
            self,
            "task_id",
            task_id,
        )

    @property
    def instructions(
        self,
    ):
        """Exact already-frozen Forest instruction string."""

        return self.turn_instructions.instructions

    @property
    def exchange_count(
        self,
    ):
        return self.conversation.exchange_count

    def inspect(
        self,
    ):
        """Metadata only; never duplicate continuity contents."""

        return {
            "schema_version":
                self.schema_version,

            "execution_context_id":
                self.execution_context_id,

            "task_id":
                self.task_id,

            "instruction_character_count":
                self.turn_instructions.character_count,

            "source_packet_count":
                self.turn_instructions.source_packet_count,

            "conversation_exchange_count":
                self.conversation.exchange_count,
        }
