from dataclasses import dataclass


REASONING_SCHEMA_VERSION = 1

CANONICAL_REASONING_MODES = (
    "quick",
    "normal",
    "deep",
)

DEFAULT_REASONING_MODE = "normal"

# Migration/convenience aliases only.
# Canonical persisted/returned values remain
# quick / normal / deep.
_REASONING_MODE_ALIASES = {
    "light": "quick",
    "standard": "normal",
}


class ReasoningModeError(ValueError):
    """Invalid canonical Forest reasoning mode."""


def normalize_reasoning_mode(
    value,
    *,
    allow_none=False,
):
    if value is None:
        if allow_none:
            return None

        raise ReasoningModeError(
            "Reasoning mode cannot be None."
        )

    if not isinstance(value, str):
        raise ReasoningModeError(
            "Reasoning mode must be a string."
        )

    normalized = value.strip().lower()

    if not normalized:
        if allow_none:
            return None

        raise ReasoningModeError(
            "Reasoning mode cannot be empty."
        )

    normalized = _REASONING_MODE_ALIASES.get(
        normalized,
        normalized,
    )

    if normalized not in CANONICAL_REASONING_MODES:
        raise ReasoningModeError(
            "Unknown Forest reasoning mode: "
            f"{value!r}. Expected one of "
            "quick, normal, deep."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class ReasoningSignals:
    """
    Immutable turn-local complexity signals.

    Raw user text is deliberately not retained.
    """

    character_count: int
    line_count: int
    question_count: int
    code_fence_count: int
    deep_marker_ids: tuple[str, ...]
    quick_marker_ids: tuple[str, ...]
    complexity_score: int
    schema_version: int = REASONING_SCHEMA_VERSION

    def __post_init__(self):
        for name in (
            "character_count",
            "line_count",
            "question_count",
            "code_fence_count",
            "complexity_score",
        ):
            value = getattr(self, name)

            if (
                not isinstance(value, int)
                or value < 0
            ):
                raise ReasoningModeError(
                    f"{name} must be a "
                    "non-negative integer."
                )

        if self.line_count < 1:
            raise ReasoningModeError(
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


@dataclass(frozen=True, slots=True)
class ReasoningRouteDecision:
    """
    Immutable reasoning decision for one
    meaningful conversational input.
    """

    mode: str
    source: str
    complexity_score: int
    reasons: tuple[str, ...]
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
            raise ReasoningModeError(
                "Reasoning decision source must "
                "be explicit or automatic."
            )

        if (
            not isinstance(
                self.complexity_score,
                int,
            )
            or self.complexity_score < 0
        ):
            raise ReasoningModeError(
                "complexity_score must be a "
                "non-negative integer."
            )

        object.__setattr__(
            self,
            "reasons",
            tuple(self.reasons),
        )
