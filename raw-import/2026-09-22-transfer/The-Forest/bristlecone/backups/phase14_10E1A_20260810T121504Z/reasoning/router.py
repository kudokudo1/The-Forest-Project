from .model import (
    ReasoningModeError,
    ReasoningRouteDecision,
    ReasoningSignals,
    normalize_reasoning_mode,
)


# Marker IDs are Forest-owned semantic hints.
# The phrases themselves are deliberately small,
# transparent, deterministic, and replaceable.
_DEEP_MARKERS = (
    (
        "debugging",
        (
            "debug",
            "troubleshoot",
            "root cause",
            "stack trace",
            "traceback",
        ),
    ),
    (
        "architecture",
        (
            "architecture",
            "architectural",
            "system design",
        ),
    ),
    (
        "concurrency",
        (
            "race condition",
            "concurrency",
            "concurrent",
            "thread safety",
            "single-flight",
        ),
    ),
    (
        "migration",
        (
            "migration",
            "migrate",
            "refactor",
        ),
    ),
    (
        "security",
        (
            "security audit",
            "security review",
            "threat model",
            "vulnerability",
        ),
    ),
    (
        "optimization",
        (
            "benchmark",
            "optimize",
            "optimization",
            "performance bottleneck",
        ),
    ),
    (
        "analysis",
        (
            "analyze",
            "investigate",
            "tradeoff",
            "trade-off",
            "compare approaches",
        ),
    ),
    (
        "multi-step",
        (
            "step by step",
            "multi-step",
            "multiple steps",
        ),
    ),
)


_QUICK_MARKERS = (
    (
        "brief",
        (
            "brief",
            "short answer",
            "one sentence",
        ),
    ),
    (
        "quick",
        (
            "quick",
            "quickly",
            "just tell me",
        ),
    ),
    (
        "simple",
        (
            "simple answer",
            "keep it simple",
        ),
    ),
)


class ReasoningSignalExtractor:
    """
    Convert raw turn text into small,
    immutable, non-content-bearing signals.
    """

    def extract(self, message):
        if not isinstance(message, str):
            raise ReasoningModeError(
                "Reasoning signal input must "
                "be a string."
            )

        if not message.strip():
            raise ReasoningModeError(
                "Reasoning signal input cannot "
                "be empty."
            )

        normalized = " ".join(
            message.lower().split()
        )

        deep_ids = tuple(
            marker_id
            for marker_id, phrases
            in _DEEP_MARKERS
            if any(
                phrase in normalized
                for phrase in phrases
            )
        )

        quick_ids = tuple(
            marker_id
            for marker_id, phrases
            in _QUICK_MARKERS
            if any(
                phrase in normalized
                for phrase in phrases
            )
        )

        character_count = len(message)

        line_count = (
            message.count("\n")
            + 1
        )

        question_count = (
            message.count("?")
        )

        code_fence_count = (
            message.count("```")
        )

        score = 0

        # Message breadth.
        if character_count >= 2000:
            score += 2
        elif character_count >= 800:
            score += 1

        # Structural complexity.
        if line_count >= 20:
            score += 1

        if code_fence_count:
            score += 1

        if question_count >= 3:
            score += 1

        # Semantic complexity is capped so a
        # pile of related words cannot create
        # an unbounded score.
        score += min(
            3,
            len(deep_ids),
        )

        return ReasoningSignals(
            character_count=character_count,
            line_count=line_count,
            question_count=question_count,
            code_fence_count=code_fence_count,
            deep_marker_ids=deep_ids,
            quick_marker_ids=quick_ids,
            complexity_score=score,
        )


class DeterministicReasoningRouter:
    """
    Forest-owned Quick / Normal / Deep router.

    Explicit mode always wins.

    Automatic routing intentionally favors
    Normal when signals are uncertain.
    """

    DEEP_THRESHOLD = 3

    def route(
        self,
        signals,
        *,
        explicit_mode=None,
    ):
        if not isinstance(
            signals,
            ReasoningSignals,
        ):
            raise ReasoningModeError(
                "Router requires "
                "ReasoningSignals."
            )

        if explicit_mode is not None:
            mode = normalize_reasoning_mode(
                explicit_mode
            )

            return ReasoningRouteDecision(
                mode=mode,
                source="explicit",
                complexity_score=(
                    signals.complexity_score
                ),
                reasons=(
                    "explicit-user-or-policy-override",
                ),
            )

        score = signals.complexity_score

        if score >= self.DEEP_THRESHOLD:
            return ReasoningRouteDecision(
                mode="deep",
                source="automatic",
                complexity_score=score,
                reasons=(
                    "complexity-threshold",
                    *signals.deep_marker_ids,
                ),
            )

        # Quick is deliberately conservative.
        #
        # A genuinely tiny turn with no
        # complexity evidence can use Quick.
        tiny_simple_turn = (
            score == 0
            and signals.character_count <= 240
            and signals.line_count <= 4
            and signals.question_count <= 1
            and signals.code_fence_count == 0
        )

        # A direct request for brevity is a weak
        # Quick preference, but cannot override
        # substantial complexity evidence.
        brief_low_complexity_turn = (
            bool(signals.quick_marker_ids)
            and score <= 1
            and not signals.deep_marker_ids
            and signals.code_fence_count == 0
        )

        if (
            tiny_simple_turn
            or brief_low_complexity_turn
        ):
            reasons = ["low-complexity-turn"]

            reasons.extend(
                signals.quick_marker_ids
            )

            return ReasoningRouteDecision(
                mode="quick",
                source="automatic",
                complexity_score=score,
                reasons=tuple(reasons),
            )

        return ReasoningRouteDecision(
            mode="normal",
            source="automatic",
            complexity_score=score,
            reasons=(
                "balanced-default",
                *signals.deep_marker_ids,
            ),
        )


class ForestReasoningRouter:
    """
    Convenience facade.

    Signal extraction remains distinct from
    routing so future classifiers can consume
    the same canonical signal representation.
    """

    def __init__(
        self,
        *,
        extractor=None,
        router=None,
    ):
        self.extractor = (
            extractor
            if extractor is not None
            else ReasoningSignalExtractor()
        )

        self.router = (
            router
            if router is not None
            else DeterministicReasoningRouter()
        )

    def decide(
        self,
        message,
        *,
        explicit_mode=None,
    ):
        signals = self.extractor.extract(
            message
        )

        return self.router.route(
            signals,
            explicit_mode=explicit_mode,
        )
