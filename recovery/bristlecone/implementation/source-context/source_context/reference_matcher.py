\
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
    SourceTarget,
)

from .structure import (
    SourceStructure,
)

from .targeting import (
    DeterministicSourceTargeter,
    SourceTargetAmbiguityError,
    SourceTargetNotFoundError,
)


SOURCE_REFERENCE_MATCH_MODE = (
    "exact-structural-reference"
)


class SourceReferenceMatchError(
    ValueError
):
    """Invalid deterministic source-reference match."""


def _canonical_signals(
    signals,
):
    """
    Canonicalize source-reference signals using the
    same observable conventions as Forest's current
    deterministic Learning matchers:

    - strings only;
    - strip surrounding whitespace;
    - reject empty values;
    - preserve case;
    - preserve first-seen ordering;
    - deduplicate after stripping.
    """

    if isinstance(
        signals,
        str,
    ):
        raise SourceReferenceMatchError(
            "signals must be a collection of "
            "non-empty strings, not one string."
        )

    try:
        values = tuple(
            signals
        )

    except TypeError as exc:
        raise SourceReferenceMatchError(
            "signals must be an iterable of "
            "non-empty strings."
        ) from exc


    canonical = []
    seen = set()


    for value in values:

        if not isinstance(
            value,
            str,
        ):
            raise SourceReferenceMatchError(
                "Every signal must be a "
                "non-empty string."
            )


        value = value.strip()


        if not value:
            raise SourceReferenceMatchError(
                "Every signal must be a "
                "non-empty string."
            )


        if value in seen:
            continue


        seen.add(
            value
        )

        canonical.append(
            value
        )


    return tuple(
        canonical
    )


@dataclass(
    frozen=True,
    slots=True,
)
class SourceReferenceMatch:
    """
    Immutable turn-local result of deterministic
    structural source-reference matching.
    """

    requested_signals: Tuple[
        str,
        ...,
    ]

    matched_signals: Tuple[
        str,
        ...,
    ]

    unmatched_signals: Tuple[
        str,
        ...,
    ]

    ambiguous_signals: Tuple[
        str,
        ...,
    ]

    targets: Tuple[
        SourceTarget,
        ...,
    ]

    mode: str = (
        SOURCE_REFERENCE_MATCH_MODE
    )

    schema_version: int = (
        SOURCE_CONTEXT_SCHEMA_VERSION
    )


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != SOURCE_CONTEXT_SCHEMA_VERSION
        ):
            raise SourceReferenceMatchError(
                "Unsupported source-reference "
                "match schema version."
            )


        requested = _canonical_signals(
            self.requested_signals
        )

        matched = _canonical_signals(
            self.matched_signals
        )

        unmatched = _canonical_signals(
            self.unmatched_signals
        )

        ambiguous = _canonical_signals(
            self.ambiguous_signals
        )


        object.__setattr__(
            self,
            "requested_signals",
            requested,
        )

        object.__setattr__(
            self,
            "matched_signals",
            matched,
        )

        object.__setattr__(
            self,
            "unmatched_signals",
            unmatched,
        )

        object.__setattr__(
            self,
            "ambiguous_signals",
            ambiguous,
        )


        try:
            targets = tuple(
                self.targets
            )

        except TypeError as exc:
            raise SourceReferenceMatchError(
                "targets must be iterable."
            ) from exc


        for target in targets:
            if not isinstance(
                target,
                SourceTarget,
            ):
                raise SourceReferenceMatchError(
                    "Every target must be "
                    "a SourceTarget."
                )


        object.__setattr__(
            self,
            "targets",
            targets,
        )


        if (
            not isinstance(
                self.mode,
                str,
            )
            or not self.mode.strip()
        ):
            raise SourceReferenceMatchError(
                "mode must be a non-empty string."
            )


        categories = (
            set(matched),
            set(unmatched),
            set(ambiguous),
        )


        if (
            categories[0]
            & categories[1]
            or categories[0]
            & categories[2]
            or categories[1]
            & categories[2]
        ):
            raise SourceReferenceMatchError(
                "matched, unmatched, and ambiguous "
                "signals must be disjoint."
            )


        classified = (
            categories[0]
            | categories[1]
            | categories[2]
        )


        if classified != set(
            requested
        ):
            raise SourceReferenceMatchError(
                "Every requested signal must be "
                "classified exactly once."
            )


    @property
    def target_count(
        self,
    ):
        return len(
            self.targets
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "mode":
                self.mode,

            "requested_signals":
                self.requested_signals,

            "matched_signals":
                self.matched_signals,

            "unmatched_signals":
                self.unmatched_signals,

            "ambiguous_signals":
                self.ambiguous_signals,

            "target_count":
                self.target_count,

            "target_region_ids":
                tuple(
                    target.region.region_id
                    for target in self.targets
                ),
        }


class SourceReferenceMatcher:
    """
    Match canonical turn signals against one
    objective SourceStructure.

    Resolution precedence:

    1. exact region_id
    2. exact unique structural label
    3. ambiguous exact label
    4. unmatched

    This matcher performs no fuzzy matching,
    semantic similarity, parsing, filesystem I/O,
    shared-cache mutation, or runtime/model calls.
    """


    def __init__(
        self,
        targeter=None,
    ):
        if targeter is None:
            targeter = (
                DeterministicSourceTargeter()
            )


        if not isinstance(
            targeter,
            DeterministicSourceTargeter,
        ):
            raise SourceReferenceMatchError(
                "targeter must be a "
                "DeterministicSourceTargeter."
            )


        self._targeter = targeter


    @staticmethod
    def _require_structure(
        structure,
    ):
        if not isinstance(
            structure,
            SourceStructure,
        ):
            raise SourceReferenceMatchError(
                "structure must be a "
                "SourceStructure."
            )


    @staticmethod
    def _require_bool(
        value,
        *,
        field_name,
    ):
        if not isinstance(
            value,
            bool,
        ):
            raise SourceReferenceMatchError(
                f"{field_name} must be bool."
            )

        return value


    def match(
        self,
        structure,
        signals,
        *,
        required=True,
    ):
        self._require_structure(
            structure
        )

        self._require_bool(
            required,
            field_name="required",
        )


        requested = _canonical_signals(
            signals
        )


        matched = []
        unmatched = []
        ambiguous = []

        targets = []

        targeted_region_ids = set()


        for signal in requested:

            # --------------------------------------
            # 1. EXACT REGION ID
            #
            # Region IDs are authoritative and take
            # precedence over labels.
            # --------------------------------------

            region = structure.region_by_id(
                signal
            )


            if region is not None:

                target = (
                    self._targeter
                    .target_region_id(
                        structure,
                        signal,
                        reason=(
                            "canonical turn signal "
                            "matched exact region_id"
                        ),
                        required=required,
                    )
                )


                matched.append(
                    signal
                )


                if (
                    target.region.region_id
                    not in targeted_region_ids
                ):
                    targeted_region_ids.add(
                        target.region.region_id
                    )

                    targets.append(
                        target
                    )


                continue


            # --------------------------------------
            # 2. EXACT STRUCTURAL LABEL
            # --------------------------------------

            try:
                target = (
                    self._targeter
                    .target_exact_label(
                        structure,
                        signal,
                        reason=(
                            "canonical turn signal "
                            "matched exact unique "
                            "structural label"
                        ),
                        required=required,
                    )
                )


            except SourceTargetAmbiguityError:

                ambiguous.append(
                    signal
                )

                continue


            except SourceTargetNotFoundError:

                unmatched.append(
                    signal
                )

                continue


            matched.append(
                signal
            )


            if (
                target.region.region_id
                not in targeted_region_ids
            ):
                targeted_region_ids.add(
                    target.region.region_id
                )

                targets.append(
                    target
                )


        return SourceReferenceMatch(
            requested_signals=requested,
            matched_signals=tuple(
                matched
            ),
            unmatched_signals=tuple(
                unmatched
            ),
            ambiguous_signals=tuple(
                ambiguous
            ),
            targets=tuple(
                targets
            ),
        )
