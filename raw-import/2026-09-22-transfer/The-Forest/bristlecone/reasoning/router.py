"""Deterministic Forest Light / Normal / Deep router."""

import re

from .model import (
    ReasoningRouteDecision,
    ReasoningSignals,
    normalize_reasoning_mode,
)


_DEEP_MARKERS = {
    "debugging": (
        "debug",
        "troubleshoot",
        "root cause",
        "stack trace",
        "traceback",
    ),

    "architecture": (
        "architecture",
        "architectural",
        "system design",
    ),

    "concurrency": (
        "race condition",
        "concurrency",
        "concurrent",
        "thread safety",
        "single-flight",
    ),

    "migration": (
        "migration",
        "migrate",
        "refactor",
    ),

    "security": (
        "security audit",
        "security review",
        "threat model",
        "vulnerability",
    ),

    "optimization": (
        "benchmark",
        "optimize",
        "optimization",
        "performance bottleneck",
    ),

    "analysis": (
        "analyze",
        "investigate",
        "tradeoff",
        "trade-off",
        "compare approaches",
    ),

    "multi-step": (
        "step by step",
        "multi-step",
        "multiple steps",
    ),
}


_QUICK_MARKERS = {
    "brief": (
        "brief",
        "short answer",
        "one sentence",
    ),

    "quick": (
        "quick",
        "quickly",
        "just tell me",
    ),

    "simple": (
        "simple answer",
        "keep it simple",
    ),
}


def _matched_marker_ids(
    normalized_message,
    marker_groups,
):
    found = []

    for marker_id, phrases in marker_groups.items():
        if any(
            phrase in normalized_message
            for phrase in phrases
        ):
            found.append(
                marker_id
            )

    return tuple(found)


class ReasoningSignalExtractor:

    def extract(
        self,
        message,
    ):
        if not isinstance(message, str):
            raise ValueError(
                "Reasoning input must be a string."
            )

        if not message.strip():
            raise ValueError(
                "Reasoning input cannot be empty."
            )

        normalized = re.sub(
            r"\s+",
            " ",
            message.lower(),
        ).strip()

        character_count = len(
            message
        )

        line_count = max(
            1,
            len(message.splitlines()),
        )

        question_count = (
            message.count("?")
        )

        code_fence_count = (
            message.count("```")
        )

        deep_marker_ids = (
            _matched_marker_ids(
                normalized,
                _DEEP_MARKERS,
            )
        )

        quick_marker_ids = (
            _matched_marker_ids(
                normalized,
                _QUICK_MARKERS,
            )
        )

        score = 0

        if character_count >= 2000:
            score += 2
        elif character_count >= 800:
            score += 1

        if line_count >= 20:
            score += 1

        if code_fence_count:
            score += 1

        if question_count >= 3:
            score += 1

        score += min(
            3,
            len(deep_marker_ids),
        )

        return ReasoningSignals(
            character_count=character_count,
            line_count=line_count,
            question_count=question_count,
            code_fence_count=code_fence_count,
            deep_marker_ids=deep_marker_ids,
            quick_marker_ids=quick_marker_ids,
            complexity_score=score,
        )


class DeterministicReasoningRouter:

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
            raise TypeError(
                "signals must be ReasoningSignals."
            )

        if explicit_mode is not None:
            return ReasoningRouteDecision(
                mode=normalize_reasoning_mode(
                    explicit_mode
                ),
                source="explicit",
                complexity_score=(
                    signals.complexity_score
                ),
                reasons=(
                    "explicit-user-override",
                ),
            )

        if signals.complexity_score >= 3:
            return ReasoningRouteDecision(
                mode="deep",
                source="automatic",
                complexity_score=(
                    signals.complexity_score
                ),
                reasons=(
                    "multiple-complexity-signals",
                ),
            )

        tiny_simple = (
            signals.complexity_score == 0
            and signals.character_count <= 240
            and signals.line_count <= 4
            and signals.question_count <= 1
            and signals.code_fence_count == 0
        )

        light_marker = (
            bool(signals.quick_marker_ids)
            and signals.complexity_score <= 1
            and not signals.deep_marker_ids
            and signals.code_fence_count == 0
        )

        if tiny_simple or light_marker:
            return ReasoningRouteDecision(
                mode="light",
                source="automatic",
                complexity_score=(
                    signals.complexity_score
                ),
                reasons=(
                    (
                        "small-simple-turn"
                        if tiny_simple
                        else "light-response-marker"
                    ),
                ),
            )

        return ReasoningRouteDecision(
            mode="normal",
            source="automatic",
            complexity_score=(
                signals.complexity_score
            ),
            reasons=(
                "moderate-or-uncertain-complexity",
            ),
        )


class ForestReasoningRouter:

    def __init__(
        self,
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
        signals = (
            self.extractor.extract(
                message
            )
        )

        return self.router.route(
            signals,
            explicit_mode=explicit_mode,
        )
