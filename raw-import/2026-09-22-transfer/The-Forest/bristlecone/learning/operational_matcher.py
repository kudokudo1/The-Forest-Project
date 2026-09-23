"""Deterministic matcher for Warm Operational Learning.

This component consumes canonical Task-routing information
and selects relevant Operational Learning record IDs from the
Warm Operational Learning Index.

It deliberately does NOT:

- parse raw user language
- call an AI model
- load authoritative learning records
- perform semantic search
- persist routing decisions
- enforce Spirit policy

Scope is an eligibility boundary.

General lessons are always eligible. Scoped lessons are only
eligible when their exact canonical scope key is supplied.

Examples of canonical scope keys:

    workshop:code-debug
    tree:maple
    clone:mail-worker

Kind and tag matching is exact. Canonicalization belongs to
the Task-routing layer above this matcher.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .indexes import (
    LEARNING_INDEX_SCHEMA_VERSION,
    ForestLearningIndexProvider,
)


OPERATIONAL_MATCH_SCHEMA_VERSION = 2


class OperationalLearningMatchError(
    RuntimeError
):
    """Raised when matching input or Warm state is invalid."""


def _canonical_strings(
    values,
    *,
    field_name,
):
    """Validate and de-duplicate canonical strings."""

    if isinstance(
        values,
        str,
    ):
        raise OperationalLearningMatchError(
            f"{field_name} must be a collection "
            "of canonical strings, not one raw string."
        )

    try:
        items = tuple(
            values
        )

    except TypeError as exc:
        raise OperationalLearningMatchError(
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
            raise OperationalLearningMatchError(
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

    return tuple(
        result
    )


def _index_ids(
    mapping,
    key,
    *,
    field_name,
):
    """Return one validated ID set from a Warm index."""

    value = mapping.get(
        key
    )

    if value is None:
        return set()

    if not isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):
        raise OperationalLearningMatchError(
            f"{field_name} entry {key!r} "
            "must be a list or tuple."
        )

    result = set()

    for record_id in value:
        if (
            not isinstance(
                record_id,
                str,
            )
            or not record_id.strip()
        ):
            raise OperationalLearningMatchError(
                f"{field_name} entry {key!r} "
                "contains an invalid record ID."
            )

        result.add(
            record_id.strip()
        )

    return result


@dataclass(
    frozen=True
)
class OperationalLearningMatch:
    """Warm-only Operational Learning routing result."""

    schema_version: int

    operational_learning_generation: int

    requested_kinds: Tuple[str, ...]
    requested_tags: Tuple[str, ...]
    requested_scope_keys: Tuple[str, ...]

    eligible_scope_keys: Tuple[str, ...]

    matched_kinds: Tuple[str, ...]
    unmatched_kinds: Tuple[str, ...]

    matched_tags: Tuple[str, ...]
    unmatched_tags: Tuple[str, ...]

    record_ids: Tuple[str, ...]


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != OPERATIONAL_MATCH_SCHEMA_VERSION
        ):
            raise OperationalLearningMatchError(
                "Unsupported Operational Learning "
                "Match schema version."
            )

        if (
            isinstance(
                self.operational_learning_generation,
                bool,
            )
            or not isinstance(
                self.operational_learning_generation,
                int,
            )
            or self.operational_learning_generation < 0
        ):
            raise OperationalLearningMatchError(
                "operational_learning_generation "
                "must be an integer >= 0."
            )


    @property
    def has_matches(
        self,
    ):
        return bool(
            self.record_ids
        )


class OperationalLearningMatcher:
    """Cheap exact matcher over the Warm Learning index."""

    def __init__(
        self,
        index_provider,
    ):
        if not isinstance(
            index_provider,
            ForestLearningIndexProvider,
        ):
            raise OperationalLearningMatchError(
                "index_provider must be "
                "ForestLearningIndexProvider."
            )

        self.index_provider = (
            index_provider
        )


    def match(
        self,
        *,
        kinds=(),
        tags=(),
        scope_keys=(),
    ):
        """Select relevant and scope-eligible record IDs.

        A record must satisfy BOTH:

        1. relevance:
           match at least one requested kind or tag

        2. scope:
           be General or belong to one explicitly supplied
           canonical scope key

        No kinds and no tags means no relevance request, so
        this function returns no records rather than loading
        every eligible lesson.
        """

        requested_kinds = (
            _canonical_strings(
                kinds,
                field_name="kinds",
            )
        )

        requested_tags = (
            _canonical_strings(
                tags,
                field_name="tags",
            )
        )

        requested_scopes = (
            _canonical_strings(
                scope_keys,
                field_name="scope_keys",
            )
        )


        # "general" is implicit and should not need to be
        # repeatedly supplied by every caller.
        requested_scopes = tuple(
            scope
            for scope in requested_scopes
            if scope != "general"
        )

        eligible_scope_keys = (
            "general",
            *requested_scopes,
        )


        index = (
            self.index_provider
            .operational_learning_index()
        )


        if not isinstance(
            index,
            dict,
        ):
            raise OperationalLearningMatchError(
                "Operational Learning Index "
                "must be a mapping."
            )


        if (
            index.get(
                "schema_version"
            )
            != LEARNING_INDEX_SCHEMA_VERSION
        ):
            raise OperationalLearningMatchError(
                "Unsupported Operational Learning "
                "Index schema version."
            )


        operational_learning_generation = (
            index.get(
                "operational_learning_generation"
            )
        )

        if (
            isinstance(
                operational_learning_generation,
                bool,
            )
            or not isinstance(
                operational_learning_generation,
                int,
            )
            or operational_learning_generation < 0
        ):
            raise OperationalLearningMatchError(
                "Operational Learning Index has "
                "invalid operational_learning_generation."
            )


        by_kind = index.get(
            "by_kind"
        )

        by_scope = index.get(
            "by_scope"
        )

        by_tag = index.get(
            "by_tag"
        )


        for field_name, mapping in (
            (
                "by_kind",
                by_kind,
            ),
            (
                "by_scope",
                by_scope,
            ),
            (
                "by_tag",
                by_tag,
            ),
        ):
            if not isinstance(
                mapping,
                dict,
            ):
                raise OperationalLearningMatchError(
                    f"{field_name} must be a mapping."
                )


        # --------------------------------------------------
        # Scope eligibility
        # --------------------------------------------------

        eligible_ids = set()

        for scope_key in eligible_scope_keys:
            eligible_ids.update(
                _index_ids(
                    by_scope,
                    scope_key,
                    field_name="by_scope",
                )
            )


        # --------------------------------------------------
        # Kind matching
        #
        # A signal only counts as matched if it has at least
        # one record that survives the scope boundary.
        # --------------------------------------------------

        matched_kinds = []
        unmatched_kinds = []

        selected_ids = set()


        for kind in requested_kinds:
            candidate_ids = (
                _index_ids(
                    by_kind,
                    kind,
                    field_name="by_kind",
                )
                & eligible_ids
            )

            if candidate_ids:
                matched_kinds.append(
                    kind
                )

                selected_ids.update(
                    candidate_ids
                )

            else:
                unmatched_kinds.append(
                    kind
                )


        # --------------------------------------------------
        # Tag matching
        # --------------------------------------------------

        matched_tags = []
        unmatched_tags = []


        for tag in requested_tags:
            candidate_ids = (
                _index_ids(
                    by_tag,
                    tag,
                    field_name="by_tag",
                )
                & eligible_ids
            )

            if candidate_ids:
                matched_tags.append(
                    tag
                )

                selected_ids.update(
                    candidate_ids
                )

            else:
                unmatched_tags.append(
                    tag
                )


        return OperationalLearningMatch(
            schema_version=(
                OPERATIONAL_MATCH_SCHEMA_VERSION
            ),
            operational_learning_generation=(
                operational_learning_generation
            ),
            requested_kinds=(
                requested_kinds
            ),
            requested_tags=(
                requested_tags
            ),
            requested_scope_keys=(
                requested_scopes
            ),
            eligible_scope_keys=tuple(
                eligible_scope_keys
            ),
            matched_kinds=tuple(
                matched_kinds
            ),
            unmatched_kinds=tuple(
                unmatched_kinds
            ),
            matched_tags=tuple(
                matched_tags
            ),
            unmatched_tags=tuple(
                unmatched_tags
            ),
            record_ids=tuple(
                sorted(
                    selected_ids
                )
            ),
        )
