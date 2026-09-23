"""Deterministic matcher for Warm User Context routes.

This layer does NOT:

- parse raw user language
- call an AI model
- load User Context records
- decide permissions
- enforce Spirit policy
- persist routing decisions

It receives already-canonical Task signals such as:

    software
    recommendation
    food
    shopping

and asks the Warm Context Trigger Index whether those
signals require User Context retrieval.

The result contains IDs and routing metadata only. Actual
User Context remains Cold until a later layer retrieves only
the matched records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .indexes import (
    LEARNING_INDEX_SCHEMA_VERSION,
    ForestLearningIndexProvider,
)


CONTEXT_TRIGGER_MATCH_SCHEMA_VERSION = 1


MATCH_MODES = frozenset(
    {
        "none",
        "check",
        "must-check",
    }
)


class ContextTriggerMatchError(
    RuntimeError
):
    """Raised when trigger input or Warm state is invalid."""


def _canonical_signals(
    signals,
):
    """Validate and de-duplicate canonical Task signals.

    Signals are deliberately NOT case-folded or semantically
    expanded here.

    Canonicalization belongs to the Task-routing layer.
    Exact matching here prevents this low-level component
    from inventing relevance.
    """

    if isinstance(
        signals,
        str,
    ):
        raise ContextTriggerMatchError(
            "signals must be a collection of canonical "
            "signal strings, not one raw string."
        )

    try:
        values = tuple(
            signals
        )

    except TypeError as exc:
        raise ContextTriggerMatchError(
            "signals must be iterable."
        ) from exc

    result = []
    seen = set()

    for value in values:
        if (
            not isinstance(
                value,
                str,
            )
            or not value.strip()
        ):
            raise ContextTriggerMatchError(
                "Every signal must be a non-empty string."
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

    return tuple(
        result
    )


def _string_collection(
    value,
    *,
    field_name,
):
    if not isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        raise ContextTriggerMatchError(
            f"{field_name} must be a list or tuple."
        )

    result = []

    for item in value:
        if (
            not isinstance(
                item,
                str,
            )
            or not item.strip()
        ):
            raise ContextTriggerMatchError(
                f"{field_name} must contain "
                "non-empty strings."
            )

        result.append(
            item.strip()
        )

    return tuple(
        result
    )


@dataclass(
    frozen=True
)
class ContextTriggerMatch:
    """Minimal routing result suitable for a future Route Stamp."""

    schema_version: int

    user_context_generation: int

    requested_signals: Tuple[str, ...]
    matched_signals: Tuple[str, ...]
    unmatched_signals: Tuple[str, ...]

    must_check_signals: Tuple[str, ...]

    record_ids: Tuple[str, ...]
    record_types: Tuple[str, ...]

    mode: str


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != CONTEXT_TRIGGER_MATCH_SCHEMA_VERSION
        ):
            raise ContextTriggerMatchError(
                "Unsupported Context Trigger "
                "Match schema version."
            )

        if (
            isinstance(
                self.user_context_generation,
                bool,
            )
            or not isinstance(
                self.user_context_generation,
                int,
            )
            or self.user_context_generation < 0
        ):
            raise ContextTriggerMatchError(
                "user_context_generation must "
                "be an integer >= 0."
            )

        if self.mode not in MATCH_MODES:
            raise ContextTriggerMatchError(
                f"Unknown match mode: {self.mode!r}"
            )


    @property
    def requires_context(
        self,
    ):
        return self.mode != "none"


    @property
    def must_check(
        self,
    ):
        return self.mode == "must-check"


class ContextTriggerMatcher:
    """Cheap exact matcher over the Warm Context Trigger Index.

    The index provider is injected explicitly so Tree/Clone
    callers can share the same Forest CacheCoordinator through
    their shared provider infrastructure.
    """

    def __init__(
        self,
        index_provider,
    ):
        if not isinstance(
            index_provider,
            ForestLearningIndexProvider,
        ):
            raise ContextTriggerMatchError(
                "index_provider must be "
                "ForestLearningIndexProvider."
            )

        self.index_provider = (
            index_provider
        )


    def match(
        self,
        signals,
    ):
        """Match canonical Task signals without loading records."""

        requested = (
            _canonical_signals(
                signals
            )
        )

        index = (
            self.index_provider
            .context_trigger_index()
        )

        if not isinstance(
            index,
            dict,
        ):
            raise ContextTriggerMatchError(
                "Context Trigger Index must be a mapping."
            )

        if (
            index.get(
                "schema_version"
            )
            != LEARNING_INDEX_SCHEMA_VERSION
        ):
            raise ContextTriggerMatchError(
                "Unsupported Context Trigger "
                "Index schema version."
            )

        generation = index.get(
            "user_context_generation"
        )

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
            raise ContextTriggerMatchError(
                "Context Trigger Index has invalid "
                "user_context_generation."
            )

        routes = index.get(
            "routes"
        )

        if not isinstance(
            routes,
            dict,
        ):
            raise ContextTriggerMatchError(
                "Context Trigger Index routes "
                "must be a mapping."
            )

        matched = []
        unmatched = []
        mandatory = []

        record_ids = set()
        record_types = set()

        for signal in requested:
            route = routes.get(
                signal
            )

            if route is None:
                unmatched.append(
                    signal
                )

                continue

            if not isinstance(
                route,
                dict,
            ):
                raise ContextTriggerMatchError(
                    f"Route {signal!r} must "
                    "be a mapping."
                )

            mode = route.get(
                "mode"
            )

            if mode not in {
                "check",
                "must-check",
            }:
                raise ContextTriggerMatchError(
                    f"Route {signal!r} has "
                    f"invalid mode {mode!r}."
                )

            route_ids = (
                _string_collection(
                    route.get(
                        "record_ids"
                    ),
                    field_name=(
                        f"route {signal!r} record_ids"
                    ),
                )
            )

            route_types = (
                _string_collection(
                    route.get(
                        "record_types"
                    ),
                    field_name=(
                        f"route {signal!r} record_types"
                    ),
                )
            )

            matched.append(
                signal
            )

            if mode == "must-check":
                mandatory.append(
                    signal
                )

            record_ids.update(
                route_ids
            )

            record_types.update(
                route_types
            )

        if mandatory:
            overall_mode = "must-check"

        elif matched:
            overall_mode = "check"

        else:
            overall_mode = "none"

        return ContextTriggerMatch(
            schema_version=(
                CONTEXT_TRIGGER_MATCH_SCHEMA_VERSION
            ),
            user_context_generation=(
                generation
            ),
            requested_signals=(
                requested
            ),
            matched_signals=tuple(
                matched
            ),
            unmatched_signals=tuple(
                unmatched
            ),
            must_check_signals=tuple(
                mandatory
            ),
            record_ids=tuple(
                sorted(
                    record_ids
                )
            ),
            record_types=tuple(
                sorted(
                    record_types
                )
            ),
            mode=overall_mode,
        )
