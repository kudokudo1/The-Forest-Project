"""Runtime-neutral portable conversation continuity.

Forest owns completed public conversation exchanges above
any individual runtime session.

This state may later be used to establish continuity when
changing Model Form, replacing a stale runtime session, or
moving between compatible runtime implementations.

It deliberately contains no runtime/session identity,
model internals, KV cache, hidden reasoning, or tool replay.
"""

from dataclasses import dataclass


CONVERSATION_CONTINUITY_SCHEMA_VERSION = 1


class ConversationContinuityError(
    ValueError
):
    """Invalid portable conversation continuity."""


def _nonempty_string(
    name,
    value,
):
    if not isinstance(
        value,
        str,
    ):
        raise ConversationContinuityError(
            f"{name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ConversationContinuityError(
            f"{name} cannot be empty."
        )

    return normalized


@dataclass(
    frozen=True,
    slots=True,
)
class ConversationExchange:
    """One completed public user/assistant exchange.

    This is not an execution log.

    Tool calls, hidden reasoning, runtime events, and the
    current in-flight turn do not belong here.
    """

    user_message: str
    assistant_message: str

    def __post_init__(
        self,
    ):
        user_message = _nonempty_string(
            "user_message",
            self.user_message,
        )

        if not isinstance(
            self.assistant_message,
            str,
        ):
            raise ConversationContinuityError(
                "assistant_message "
                "must be a string."
            )

        object.__setattr__(
            self,
            "user_message",
            user_message,
        )

        # Preserve assistant text exactly.
        #
        # Empty text is permitted because a successful
        # runtime turn may legitimately produce no public
        # textual content.
        object.__setattr__(
            self,
            "assistant_message",
            self.assistant_message,
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ConversationContinuity:
    """Immutable Forest-owned completed conversation.

    exchanges are ordered oldest -> newest.

    The current meaningful turn is intentionally excluded.
    It may be appended only after successful completion.
    """

    execution_context_id: str
    task_id: str
    exchanges: tuple = ()
    schema_version: int = (
        CONVERSATION_CONTINUITY_SCHEMA_VERSION
    )

    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != CONVERSATION_CONTINUITY_SCHEMA_VERSION
        ):
            raise ConversationContinuityError(
                "Unsupported conversation "
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

        try:
            exchanges = tuple(
                self.exchanges
            )

        except TypeError as exc:
            raise ConversationContinuityError(
                "exchanges must be iterable."
            ) from exc

        if not all(
            isinstance(
                exchange,
                ConversationExchange,
            )
            for exchange in exchanges
        ):
            raise ConversationContinuityError(
                "Every continuity exchange must "
                "be ConversationExchange."
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

        object.__setattr__(
            self,
            "exchanges",
            exchanges,
        )

    @property
    def exchange_count(
        self,
    ):
        return len(
            self.exchanges
        )

    @property
    def is_empty(
        self,
    ):
        return self.exchange_count == 0

    def inspect(
        self,
    ):
        """Metadata only; never duplicate conversation text."""

        return {
            "schema_version":
                self.schema_version,

            "execution_context_id":
                self.execution_context_id,

            "task_id":
                self.task_id,

            "exchange_count":
                self.exchange_count,

            "user_character_count":
                sum(
                    len(
                        exchange.user_message
                    )
                    for exchange
                    in self.exchanges
                ),

            "assistant_character_count":
                sum(
                    len(
                        exchange.assistant_message
                    )
                    for exchange
                    in self.exchanges
                ),

            "empty":
                self.is_empty,
        }
