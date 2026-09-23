"""Canonical runtime-neutral Forest reasoning model."""

from dataclasses import dataclass


REASONING_SCHEMA_VERSION = 1

CANONICAL_REASONING_MODES = (
    "light",
    "normal",
    "deep",
)

DEFAULT_REASONING_MODE = "normal"


_REASONING_MODE_ALIASES = {
    # Phase 14.10 human-facing rename.
    "quick": "light",

    # Earlier migration compatibility.
    "standard": "normal",
}


class ReasoningModeError(ValueError):
    """Raised when a canonical Forest reasoning mode is invalid."""


def normalize_reasoning_mode(
    value,
    *,
    default=DEFAULT_REASONING_MODE,
):
    """Normalize to Light / Normal / Deep.

    Runtime-specific values do not belong in this namespace.
    """

    if value is None:
        value = default

    if not isinstance(value, str):
        raise ReasoningModeError(
            "Reasoning mode must be a string."
        )

    normalized = value.strip().lower()

    if not normalized:
        if default is None:
            raise ReasoningModeError(
                "Reasoning mode cannot be empty."
            )

        normalized = str(
            default
        ).strip().lower()

    normalized = _REASONING_MODE_ALIASES.get(
        normalized,
        normalized,
    )

    if normalized not in CANONICAL_REASONING_MODES:
        raise ReasoningModeError(
            "Unsupported canonical Forest "
            f"reasoning mode: {value!r}."
        )

    return normalized


def _nonnegative_int(
    name,
    value,
):
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < 0
    ):
        raise ValueError(
            f"{name} must be a non-negative integer."
        )

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ReasoningSignals:
    """Immutable prompt-shape signals.

    Raw user text is deliberately not retained.
    """

    character_count: int
    line_count: int
    question_count: int
    code_fence_count: int
    deep_marker_ids: tuple = ()
    quick_marker_ids: tuple = ()
    complexity_score: int = 0
    schema_version: int = REASONING_SCHEMA_VERSION

    def __post_init__(self):
        _nonnegative_int(
            "character_count",
            self.character_count,
        )

        _nonnegative_int(
            "line_count",
            self.line_count,
        )

        _nonnegative_int(
            "question_count",
            self.question_count,
        )

        _nonnegative_int(
            "code_fence_count",
            self.code_fence_count,
        )

        _nonnegative_int(
            "complexity_score",
            self.complexity_score,
        )

        if self.line_count < 1:
            raise ValueError(
                "line_count must be at least 1."
            )

        object.__setattr__(
            self,
            "deep_marker_ids",
            tuple(self.deep_marker_ids),
        )

        object.__setattr__(
            self,
            "quick_marker_ids",
            tuple(self.quick_marker_ids),
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ReasoningRouteDecision:
    """Immutable automatic/explicit routing decision."""

    mode: str
    source: str
    complexity_score: int
    reasons: tuple = ()
    schema_version: int = REASONING_SCHEMA_VERSION

    def __post_init__(self):
        object.__setattr__(
            self,
            "mode",
            normalize_reasoning_mode(
                self.mode
            ),
        )

        if self.source not in (
            "explicit",
            "automatic",
        ):
            raise ValueError(
                "Reasoning decision source must be "
                "'explicit' or 'automatic'."
            )

        _nonnegative_int(
            "complexity_score",
            self.complexity_score,
        )

        object.__setattr__(
            self,
            "reasons",
            tuple(self.reasons),
        )
