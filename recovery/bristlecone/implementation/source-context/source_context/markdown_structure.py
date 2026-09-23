\
from __future__ import annotations

from dataclasses import dataclass
import re

from .model import (
    SourceRegion,
)
from .snapshot import (
    SourceContentSnapshot,
)
from .structure import (
    SourceStructure,
    SourceStructureError,
)


MARKDOWN_STRUCTURE_KIND = "markdown-headings-v1"


class MarkdownStructureError(
    SourceStructureError
):
    """Unable to derive Markdown heading structure."""


@dataclass(
    frozen=True,
    slots=True,
)
class _MarkdownHeading:
    start_line: int
    level: int
    label: str | None
    syntax: str


class MarkdownSourceStructureBuilder:
    """
    Deterministically derive objective Markdown
    section regions from one immutable snapshot.

    Supported structural syntax:

    - ATX headings: # through ######
    - Setext level 1: =====
    - Setext level 2: -----
    - fenced code exclusion using backticks
      or tildes

    Region boundaries include the heading and its
    section body, including descendant subsections,
    until the next heading of the same or higher
    structural level.

    No filesystem, cache, targeting, or runtime
    behavior is owned by this layer.
    """


    @staticmethod
    def _leading_spaces(
        line,
    ):
        return (
            len(line)
            - len(
                line.lstrip(" ")
            )
        )


    @staticmethod
    def _fence_run(
        stripped,
    ):
        if not stripped:
            return None

        marker = stripped[0]

        if marker not in {
            "`",
            "~",
        }:
            return None

        count = 0

        for character in stripped:
            if character != marker:
                break

            count += 1

        if count < 3:
            return None

        return (
            marker,
            count,
        )


    @classmethod
    def _outside_fence_mask(
        cls,
        lines,
    ):
        outside = []

        fence_marker = None
        fence_length = 0

        for line in lines:
            indent = cls._leading_spaces(
                line
            )

            stripped = (
                line[indent:]
                if indent <= 3
                else line
            )

            fence = (
                cls._fence_run(
                    stripped
                )
                if indent <= 3
                else None
            )

            if fence_marker is None:
                if fence is not None:
                    fence_marker, fence_length = (
                        fence
                    )

                    outside.append(
                        False
                    )

                    continue

                outside.append(
                    True
                )

                continue


            # We are inside a fenced code block.
            outside.append(
                False
            )

            if fence is None:
                continue

            marker, length = fence

            if (
                marker != fence_marker
                or length < fence_length
            ):
                continue

            remainder = stripped[
                length:
            ]

            if remainder.strip():
                continue

            fence_marker = None
            fence_length = 0


        return tuple(
            outside
        )


    @classmethod
    def _atx_heading(
        cls,
        line,
    ):
        indent = cls._leading_spaces(
            line
        )

        if indent > 3:
            return None

        stripped = line[
            indent:
        ]

        count = 0

        for character in stripped:
            if character != "#":
                break

            count += 1

        if (
            count < 1
            or count > 6
        ):
            return None

        remainder = stripped[
            count:
        ]

        if (
            remainder
            and not remainder[0].isspace()
        ):
            return None

        content = remainder.strip()

        # Optional closing ATX hash sequence.
        content = re.sub(
            r"[ \t]+#+[ \t]*$",
            "",
            content,
        ).rstrip()

        return (
            count,
            content or None,
        )


    @classmethod
    def _setext_level(
        cls,
        line,
    ):
        indent = cls._leading_spaces(
            line
        )

        if indent > 3:
            return None

        stripped = line[
            indent:
        ].strip()

        if not stripped:
            return None

        if re.fullmatch(
            r"=+",
            stripped,
        ):
            return 1

        if re.fullmatch(
            r"-+",
            stripped,
        ):
            return 2

        return None


    @classmethod
    def _discover_headings(
        cls,
        lines,
    ):
        outside = (
            cls._outside_fence_mask(
                lines
            )
        )

        headings = []

        index = 0

        while index < len(
            lines
        ):
            if not outside[
                index
            ]:
                index += 1
                continue


            atx = cls._atx_heading(
                lines[index]
            )

            if atx is not None:
                level, label = atx

                headings.append(
                    _MarkdownHeading(
                        start_line=index + 1,
                        level=level,
                        label=label,
                        syntax="atx",
                    )
                )

                index += 1
                continue


            # Setext requires a nonblank title line
            # immediately followed by an underline.
            if (
                index + 1
                < len(lines)
                and outside[
                    index + 1
                ]
            ):
                title = lines[
                    index
                ]

                title_indent = (
                    cls._leading_spaces(
                        title
                    )
                )

                if (
                    title.strip()
                    and title_indent <= 3
                ):
                    level = (
                        cls._setext_level(
                            lines[
                                index + 1
                            ]
                        )
                    )

                    if level is not None:
                        label = (
                            title.strip()
                            or None
                        )

                        headings.append(
                            _MarkdownHeading(
                                start_line=(
                                    index + 1
                                ),
                                level=level,
                                label=label,
                                syntax="setext",
                            )
                        )

                        # Skip the underline so it is
                        # not considered independently.
                        index += 2
                        continue


            index += 1


        return tuple(
            headings
        )


    @staticmethod
    def _section_end_line(
        headings,
        index,
        document_line_count,
    ):
        current = headings[
            index
        ]

        for candidate in headings[
            index + 1:
        ]:
            if (
                candidate.level
                <= current.level
            ):
                return (
                    candidate.start_line
                    - 1
                )

        return document_line_count


    def build(
        self,
        snapshot,
    ):
        if not isinstance(
            snapshot,
            SourceContentSnapshot,
        ):
            raise MarkdownStructureError(
                "snapshot must be a "
                "SourceContentSnapshot."
            )


        lines = snapshot.text.splitlines()

        headings = (
            self._discover_headings(
                lines
            )
        )


        whole = SourceRegion(
            source=snapshot.source,
            fingerprint=(
                snapshot.fingerprint
            ),
            region_id=(
                "markdown:document"
            ),
            region_kind=(
                "whole-source"
            ),
            label=(
                snapshot.source.display_name
                or snapshot.source.source_id
            ),
        )


        regions = [
            whole
        ]

        # Stack entries:
        # (heading level, region_id)
        hierarchy = []


        for index, heading in enumerate(
            headings
        ):
            while (
                hierarchy
                and hierarchy[-1][0]
                >= heading.level
            ):
                hierarchy.pop()


            parent_region_id = (
                hierarchy[-1][1]
                if hierarchy
                else whole.region_id
            )


            end_line = (
                self._section_end_line(
                    headings,
                    index,
                    len(lines),
                )
            )


            region_id = (
                "markdown-heading:"
                f"L{heading.level}"
                f"@L{heading.start_line}"
            )


            region = SourceRegion(
                source=snapshot.source,
                fingerprint=(
                    snapshot.fingerprint
                ),
                region_id=region_id,
                region_kind=(
                    "markdown-heading"
                ),
                start_line=(
                    heading.start_line
                ),
                end_line=end_line,
                label=heading.label,
                parent_region_id=(
                    parent_region_id
                ),
            )


            regions.append(
                region
            )

            hierarchy.append(
                (
                    heading.level,
                    region_id,
                )
            )


        return SourceStructure(
            fingerprint=(
                snapshot.fingerprint
            ),
            structure_kind=(
                MARKDOWN_STRUCTURE_KIND
            ),
            regions=tuple(
                regions
            ),
        )
