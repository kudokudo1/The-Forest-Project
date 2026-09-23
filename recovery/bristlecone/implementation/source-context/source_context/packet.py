\
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
    SourceFingerprint,
    SourceIdentity,
    SourceRegion,
)

from .snapshot import (
    SourceContentSnapshot,
)

from .target_expansion import (
    SourceTargetExpansion,
)


SOURCE_PACKET_MODE = (
    "bounded-target-source"
)


class SourcePacketError(
    ValueError
):
    """Invalid source packet assembly."""


class SourcePacketBudgetError(
    SourcePacketError
):
    """Selected source truth exceeds packet budget."""


@dataclass(
    frozen=True,
    slots=True,
)
class SourcePacketFragment:
    """
    One non-overlapping exact source-text fragment.

    region_ids records every explicitly targeted
    region represented by this fragment.
    """

    source: SourceIdentity
    fingerprint: SourceFingerprint

    region_ids: Tuple[
        str,
        ...,
    ]

    start_line: int
    end_line: int

    text: str

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
            raise SourcePacketError(
                "Unsupported packet-fragment "
                "schema version."
            )


        if not isinstance(
            self.source,
            SourceIdentity,
        ):
            raise SourcePacketError(
                "source must be SourceIdentity."
            )


        if not isinstance(
            self.fingerprint,
            SourceFingerprint,
        ):
            raise SourcePacketError(
                "fingerprint must be "
                "SourceFingerprint."
            )


        if (
            self.fingerprint.source
            != self.source
        ):
            raise SourcePacketError(
                "fragment fingerprint/source "
                "mismatch."
            )


        try:
            region_ids = tuple(
                self.region_ids
            )

        except TypeError as exc:
            raise SourcePacketError(
                "region_ids must be iterable."
            ) from exc


        if not region_ids:
            raise SourcePacketError(
                "fragment requires at least "
                "one target region ID."
            )


        seen = set()

        for region_id in region_ids:

            if (
                not isinstance(
                    region_id,
                    str,
                )
                or not region_id.strip()
            ):
                raise SourcePacketError(
                    "region_ids must contain "
                    "non-empty strings."
                )


            if region_id in seen:
                raise SourcePacketError(
                    "fragment region_ids must "
                    "be unique."
                )


            seen.add(
                region_id
            )


        object.__setattr__(
            self,
            "region_ids",
            region_ids,
        )


        for name, value in (
            (
                "start_line",
                self.start_line,
            ),
            (
                "end_line",
                self.end_line,
            ),
        ):
            if (
                not isinstance(
                    value,
                    int,
                )
                or isinstance(
                    value,
                    bool,
                )
                or value < 1
            ):
                raise SourcePacketError(
                    f"{name} must be a "
                    "positive integer."
                )


        if (
            self.end_line
            < self.start_line
        ):
            raise SourcePacketError(
                "end_line cannot precede "
                "start_line."
            )


        if not isinstance(
            self.text,
            str,
        ):
            raise SourcePacketError(
                "fragment text must be str."
            )


    @property
    def line_count(
        self,
    ):
        return (
            self.end_line
            - self.start_line
            + 1
        )


    @property
    def character_count(
        self,
    ):
        return len(
            self.text
        )


@dataclass(
    frozen=True,
    slots=True,
)
class SourcePacket:
    """
    Immutable bounded source context for one exact
    source version.

    Explicit targets contribute source text.

    Ancestors are retained as structural breadcrumbs
    only unless they were also explicitly targeted.
    """

    source: SourceIdentity
    fingerprint: SourceFingerprint
    content_sha256: str

    fragments: Tuple[
        SourcePacketFragment,
        ...,
    ]

    target_region_ids: Tuple[
        str,
        ...,
    ]

    ancestor_region_ids: Tuple[
        str,
        ...,
    ]

    ancestor_labels: Tuple[
        str,
        ...,
    ]

    source_character_count: int
    source_line_count: int

    max_characters: int
    max_lines: int

    mode: str = SOURCE_PACKET_MODE

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
            raise SourcePacketError(
                "Unsupported source-packet "
                "schema version."
            )


        if not isinstance(
            self.source,
            SourceIdentity,
        ):
            raise SourcePacketError(
                "source must be SourceIdentity."
            )


        if not isinstance(
            self.fingerprint,
            SourceFingerprint,
        ):
            raise SourcePacketError(
                "fingerprint must be "
                "SourceFingerprint."
            )


        if (
            self.fingerprint.source
            != self.source
        ):
            raise SourcePacketError(
                "packet fingerprint/source "
                "mismatch."
            )


        if (
            not isinstance(
                self.content_sha256,
                str,
            )
            or len(
                self.content_sha256
            ) != 64
        ):
            raise SourcePacketError(
                "content_sha256 must be a "
                "SHA-256 hex digest."
            )


        try:
            fragments = tuple(
                self.fragments
            )

        except TypeError as exc:
            raise SourcePacketError(
                "fragments must be iterable."
            ) from exc


        for fragment in fragments:

            if not isinstance(
                fragment,
                SourcePacketFragment,
            ):
                raise SourcePacketError(
                    "Every fragment must be a "
                    "SourcePacketFragment."
                )


            if (
                fragment.source
                != self.source
                or fragment.fingerprint
                != self.fingerprint
            ):
                raise SourcePacketError(
                    "All fragments must belong "
                    "to the packet source version."
                )


        object.__setattr__(
            self,
            "fragments",
            fragments,
        )


        target_ids = tuple(
            self.target_region_ids
        )

        ancestor_ids = tuple(
            self.ancestor_region_ids
        )

        ancestor_labels = tuple(
            self.ancestor_labels
        )


        if (
            len(ancestor_ids)
            != len(ancestor_labels)
        ):
            raise SourcePacketError(
                "ancestor IDs and labels must "
                "have equal length."
            )


        for values, field_name in (
            (
                target_ids,
                "target_region_ids",
            ),
            (
                ancestor_ids,
                "ancestor_region_ids",
            ),
        ):
            seen = set()

            for value in values:

                if (
                    not isinstance(
                        value,
                        str,
                    )
                    or not value.strip()
                ):
                    raise SourcePacketError(
                        f"{field_name} must "
                        "contain non-empty strings."
                    )


                if value in seen:
                    raise SourcePacketError(
                        f"{field_name} must "
                        "contain unique values."
                    )


                seen.add(
                    value
                )


        for label in ancestor_labels:

            if (
                not isinstance(
                    label,
                    str,
                )
            ):
                raise SourcePacketError(
                    "ancestor_labels must "
                    "contain strings."
                )


        object.__setattr__(
            self,
            "target_region_ids",
            target_ids,
        )

        object.__setattr__(
            self,
            "ancestor_region_ids",
            ancestor_ids,
        )

        object.__setattr__(
            self,
            "ancestor_labels",
            ancestor_labels,
        )


        for name, value in (
            (
                "source_character_count",
                self.source_character_count,
            ),
            (
                "source_line_count",
                self.source_line_count,
            ),
            (
                "max_characters",
                self.max_characters,
            ),
            (
                "max_lines",
                self.max_lines,
            ),
        ):
            if (
                not isinstance(
                    value,
                    int,
                )
                or isinstance(
                    value,
                    bool,
                )
                or value < 0
            ):
                raise SourcePacketError(
                    f"{name} must be a "
                    "non-negative integer."
                )


        actual_characters = sum(
            fragment.character_count
            for fragment in fragments
        )

        actual_lines = sum(
            fragment.line_count
            for fragment in fragments
        )


        if (
            actual_characters
            != self.source_character_count
        ):
            raise SourcePacketError(
                "source_character_count does "
                "not match packet fragments."
            )


        if (
            actual_lines
            != self.source_line_count
        ):
            raise SourcePacketError(
                "source_line_count does not "
                "match packet fragments."
            )


        if (
            self.source_character_count
            > self.max_characters
        ):
            raise SourcePacketBudgetError(
                "Packet exceeds character budget."
            )


        if (
            self.source_line_count
            > self.max_lines
        ):
            raise SourcePacketBudgetError(
                "Packet exceeds line budget."
            )


        if (
            not isinstance(
                self.mode,
                str,
            )
            or not self.mode.strip()
        ):
            raise SourcePacketError(
                "mode must be a non-empty string."
            )


    @property
    def text(
        self,
    ):
        """
        Exact selected source text in source order.

        No prompt formatting is applied here.
        """

        return "".join(
            fragment.text
            for fragment in self.fragments
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "mode":
                self.mode,

            "source_id":
                self.source.source_id,

            "content_sha256":
                self.content_sha256,

            "target_region_ids":
                self.target_region_ids,

            "ancestor_region_ids":
                self.ancestor_region_ids,

            "ancestor_labels":
                self.ancestor_labels,

            "fragment_ranges":
                tuple(
                    (
                        fragment.start_line,
                        fragment.end_line,
                        fragment.region_ids,
                    )
                    for fragment
                    in self.fragments
                ),

            "source_character_count":
                self.source_character_count,

            "source_line_count":
                self.source_line_count,

            "max_characters":
                self.max_characters,

            "max_lines":
                self.max_lines,
        }


class SourcePacketAssembler:
    """
    Assemble bounded source content from turn-local
    target expansions.

    Rules:

    - explicit targets contribute text;
    - overlapping target ranges are unioned;
    - target text is never silently truncated;
    - ancestors are breadcrumbs only;
    - ancestors do not implicitly contribute their
      full source ranges;
    - whole-source text appears only when the
      whole-source region itself is an explicit
      target.

    The assembler performs no file I/O, parsing,
    caching, or runtime/model interaction.
    """


    @staticmethod
    def _require_snapshot(
        snapshot,
    ):
        if not isinstance(
            snapshot,
            SourceContentSnapshot,
        ):
            raise SourcePacketError(
                "snapshot must be a "
                "SourceContentSnapshot."
            )


    @staticmethod
    def _require_budget(
        value,
        *,
        field_name,
    ):
        if (
            not isinstance(
                value,
                int,
            )
            or isinstance(
                value,
                bool,
            )
            or value < 0
        ):
            raise SourcePacketError(
                f"{field_name} must be a "
                "non-negative integer."
            )


    @staticmethod
    def _region_interval(
        snapshot,
        region,
    ):
        if (
            region.source
            != snapshot.source
            or region.fingerprint
            != snapshot.fingerprint
        ):
            raise SourcePacketError(
                "Region belongs to a different "
                "source snapshot."
            )


        if region.is_whole_source:

            if snapshot.line_count == 0:
                raise SourcePacketError(
                    "Empty whole-source snapshots "
                    "cannot produce line fragments."
                )

            return (
                1,
                snapshot.line_count,
            )


        start = region.start_line
        end = region.end_line


        if (
            start is None
            or end is None
        ):
            raise SourcePacketError(
                "Non-whole-source region lacks "
                "line boundaries."
            )


        if (
            start < 1
            or end < start
            or end > snapshot.line_count
        ):
            raise SourcePacketError(
                "Region line bounds fall outside "
                "the immutable source snapshot."
            )


        return (
            start,
            end,
        )


    @staticmethod
    def _canonical_expansions(
        expansions,
    ):
        if isinstance(
            expansions,
            SourceTargetExpansion,
        ):
            expansions = (
                expansions,
            )


        try:
            values = tuple(
                expansions
            )

        except TypeError as exc:
            raise SourcePacketError(
                "expansions must be iterable."
            ) from exc


        if not values:
            raise SourcePacketError(
                "At least one target expansion "
                "is required."
            )


        for expansion in values:

            if not isinstance(
                expansion,
                SourceTargetExpansion,
            ):
                raise SourcePacketError(
                    "Every expansion must be a "
                    "SourceTargetExpansion."
                )


        return values


    @staticmethod
    def _merge_target_ranges(
        ranges,
    ):
        """
        Merge only overlapping ranges.

        Adjacent but non-overlapping targets stay
        distinct so structural boundaries remain
        inspectable.
        """

        ordered = sorted(
            ranges,
            key=lambda item: (
                item[0],
                item[1],
                item[2],
            ),
        )


        merged = []


        for (
            start,
            end,
            region_id,
        ) in ordered:

            if (
                not merged
                or start
                > merged[-1][1]
            ):
                merged.append(
                    [
                        start,
                        end,
                        [
                            region_id,
                        ],
                    ]
                )

                continue


            current = merged[-1]

            current[1] = max(
                current[1],
                end,
            )


            if region_id not in current[2]:
                current[2].append(
                    region_id
                )


        return tuple(
            (
                start,
                end,
                tuple(region_ids),
            )
            for (
                start,
                end,
                region_ids,
            ) in merged
        )


    @staticmethod
    def _slice_lines(
        lines,
        start_line,
        end_line,
    ):
        return "".join(
            lines[
                start_line - 1:
                end_line
            ]
        )


    def assemble(
        self,
        snapshot,
        expansions,
        *,
        max_characters,
        max_lines,
    ):
        self._require_snapshot(
            snapshot
        )

        self._require_budget(
            max_characters,
            field_name="max_characters",
        )

        self._require_budget(
            max_lines,
            field_name="max_lines",
        )


        expansions = (
            self._canonical_expansions(
                expansions
            )
        )


        target_ranges = []
        target_region_ids = []

        ancestor_region_ids = []
        ancestor_labels = []

        seen_targets = set()
        seen_ancestors = set()


        for expansion in expansions:

            target = (
                expansion.target.region
            )


            if (
                target.source
                != snapshot.source
                or target.fingerprint
                != snapshot.fingerprint
            ):
                raise SourcePacketError(
                    "Target expansion belongs "
                    "to a different source version."
                )


            if (
                target.region_id
                not in seen_targets
            ):
                seen_targets.add(
                    target.region_id
                )

                target_region_ids.append(
                    target.region_id
                )


                start, end = (
                    self._region_interval(
                        snapshot,
                        target,
                    )
                )


                target_ranges.append(
                    (
                        start,
                        end,
                        target.region_id,
                    )
                )


            for ancestor in (
                expansion.ancestor_regions
            ):

                if (
                    ancestor.source
                    != snapshot.source
                    or ancestor.fingerprint
                    != snapshot.fingerprint
                ):
                    raise SourcePacketError(
                        "Expansion ancestor belongs "
                        "to different source truth."
                    )


                # If this ancestor was explicitly
                # targeted elsewhere, its text will
                # already be represented by the
                # target-union logic.
                if (
                    ancestor.region_id
                    in seen_ancestors
                ):
                    continue


                seen_ancestors.add(
                    ancestor.region_id
                )

                ancestor_region_ids.append(
                    ancestor.region_id
                )

                ancestor_labels.append(
                    ancestor.label
                    or ancestor.region_id
                )


        merged_ranges = (
            self._merge_target_ranges(
                target_ranges
            )
        )


        lines = snapshot.text.splitlines(
            keepends=True
        )


        if (
            len(lines)
            != snapshot.line_count
        ):
            raise SourcePacketError(
                "Snapshot line accounting changed "
                "during packet assembly."
            )


        fragments = []


        for (
            start,
            end,
            region_ids,
        ) in merged_ranges:

            fragment_text = (
                self._slice_lines(
                    lines,
                    start,
                    end,
                )
            )


            fragments.append(
                SourcePacketFragment(
                    source=snapshot.source,
                    fingerprint=(
                        snapshot.fingerprint
                    ),
                    region_ids=region_ids,
                    start_line=start,
                    end_line=end,
                    text=fragment_text,
                )
            )


        source_character_count = sum(
            fragment.character_count
            for fragment in fragments
        )

        source_line_count = sum(
            fragment.line_count
            for fragment in fragments
        )


        # Fail closed. C.4 deliberately does not
        # silently truncate selected source truth.
        if (
            source_character_count
            > max_characters
        ):
            raise SourcePacketBudgetError(
                "Explicit target source exceeds "
                "the packet character budget."
            )


        if (
            source_line_count
            > max_lines
        ):
            raise SourcePacketBudgetError(
                "Explicit target source exceeds "
                "the packet line budget."
            )


        return SourcePacket(
            source=snapshot.source,
            fingerprint=(
                snapshot.fingerprint
            ),
            content_sha256=(
                snapshot.content_sha256
            ),
            fragments=tuple(
                fragments
            ),
            target_region_ids=tuple(
                target_region_ids
            ),
            ancestor_region_ids=tuple(
                ancestor_region_ids
            ),
            ancestor_labels=tuple(
                ancestor_labels
            ),
            source_character_count=(
                source_character_count
            ),
            source_line_count=(
                source_line_count
            ),
            max_characters=max_characters,
            max_lines=max_lines,
        )
