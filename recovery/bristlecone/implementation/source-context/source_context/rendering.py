\
from __future__ import annotations

from dataclasses import dataclass
import json

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
)

from .packet import (
    SourcePacket,
)


SOURCE_PACKET_RENDER_FORMAT = (
    "forest-source-context-v1"
)


class SourcePacketRenderError(
    ValueError
):
    """Invalid deterministic packet rendering."""


class SourcePacketRenderBudgetError(
    SourcePacketRenderError
):
    """Rendered packet exceeds authorized size."""


@dataclass(
    frozen=True,
    slots=True,
)
class RenderedSourcePacket:
    """
    Immutable rendering of one SourcePacket.

    The packet remains authoritative selection
    truth. This object records the exact stable
    presentation prepared for later composition.
    """

    packet: SourcePacket

    text: str

    fence_character: str
    fence_length: int

    include_locator: bool

    max_rendered_characters: int

    format_version: str = (
        SOURCE_PACKET_RENDER_FORMAT
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
            raise SourcePacketRenderError(
                "Unsupported rendered-source "
                "schema version."
            )


        if not isinstance(
            self.packet,
            SourcePacket,
        ):
            raise SourcePacketRenderError(
                "packet must be SourcePacket."
            )


        if not isinstance(
            self.text,
            str,
        ):
            raise SourcePacketRenderError(
                "text must be str."
            )


        if (
            self.fence_character
            not in {
                "`",
                "~",
            }
        ):
            raise SourcePacketRenderError(
                "fence_character must be "
                "backtick or tilde."
            )


        if (
            not isinstance(
                self.fence_length,
                int,
            )
            or isinstance(
                self.fence_length,
                bool,
            )
            or self.fence_length < 3
        ):
            raise SourcePacketRenderError(
                "fence_length must be an "
                "integer of at least 3."
            )


        if not isinstance(
            self.include_locator,
            bool,
        ):
            raise SourcePacketRenderError(
                "include_locator must be bool."
            )


        if (
            not isinstance(
                self.max_rendered_characters,
                int,
            )
            or isinstance(
                self.max_rendered_characters,
                bool,
            )
            or self.max_rendered_characters < 0
        ):
            raise SourcePacketRenderError(
                "max_rendered_characters must "
                "be a non-negative integer."
            )


        if (
            len(self.text)
            > self.max_rendered_characters
        ):
            raise SourcePacketRenderBudgetError(
                "Rendered source packet exceeds "
                "character budget."
            )


        if (
            not isinstance(
                self.format_version,
                str,
            )
            or not self.format_version.strip()
        ):
            raise SourcePacketRenderError(
                "format_version must be a "
                "non-empty string."
            )


    @property
    def character_count(
        self,
    ):
        return len(
            self.text
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "format_version":
                self.format_version,

            "source_id":
                self.packet.source.source_id,

            "content_sha256":
                self.packet.content_sha256,

            "target_region_ids":
                self.packet.target_region_ids,

            "ancestor_region_ids":
                self.packet.ancestor_region_ids,

            "fragment_count":
                len(
                    self.packet.fragments
                ),

            "fence_character":
                self.fence_character,

            "fence_length":
                self.fence_length,

            "include_locator":
                self.include_locator,

            "character_count":
                self.character_count,

            "max_rendered_characters":
                self.max_rendered_characters,
        }


class DeterministicSourcePacketRenderer:
    """
    Render SourcePacket as stable human-readable
    source context.

    Rendering rules:

    - provenance is explicit;
    - target IDs are explicit;
    - ancestor breadcrumbs are explicit;
    - fragment line ranges are explicit;
    - selected source text is preserved exactly;
    - local locator/path disclosure is opt-in;
    - source cannot close its own outer code fence;
    - rendered output has its own hard character
      budget and is never silently truncated.

    This layer performs no file I/O, caching,
    targeting, parsing, or runtime interaction.
    """


    @staticmethod
    def _require_packet(
        packet,
    ):
        if not isinstance(
            packet,
            SourcePacket,
        ):
            raise SourcePacketRenderError(
                "packet must be SourcePacket."
            )


    @staticmethod
    def _require_budget(
        value,
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
            raise SourcePacketRenderError(
                "max_rendered_characters must "
                "be a non-negative integer."
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
            raise SourcePacketRenderError(
                f"{field_name} must be bool."
            )


    @staticmethod
    def _metadata(
        value,
    ):
        """
        JSON encoding keeps arbitrary metadata on
        one deterministic line and escapes control
        characters without altering source text.
        """

        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(
                ",",
                ":",
            ),
        )


    @staticmethod
    def _longest_run(
        text,
        marker,
    ):
        longest = 0
        current = 0

        for character in text:

            if character == marker:
                current += 1

                longest = max(
                    longest,
                    current,
                )

            else:
                current = 0


        return longest


    @classmethod
    def _choose_fence(
        cls,
        packet,
    ):
        selected_text = "".join(
            fragment.text
            for fragment
            in packet.fragments
        )


        backtick_run = (
            cls._longest_run(
                selected_text,
                "`",
            )
        )

        tilde_run = (
            cls._longest_run(
                selected_text,
                "~",
            )
        )


        # Pick the marker requiring the shorter
        # safe fence. Stable tie-break: backtick.
        if backtick_run <= tilde_run:
            marker = "`"
            longest = backtick_run

        else:
            marker = "~"
            longest = tilde_run


        length = max(
            3,
            longest + 1,
        )


        return (
            marker,
            length,
        )


    def render(
        self,
        packet,
        *,
        max_rendered_characters,
        include_locator=False,
    ):
        self._require_packet(
            packet
        )

        self._require_budget(
            max_rendered_characters
        )

        self._require_bool(
            include_locator,
            field_name="include_locator",
        )


        (
            fence_character,
            fence_length,
        ) = self._choose_fence(
            packet
        )


        fence = (
            fence_character
            * fence_length
        )


        parts = []


        def line(
            value="",
        ):
            parts.append(
                str(value)
                + "\n"
            )


        # ------------------------------------------
        # PROVENANCE
        # ------------------------------------------

        line(
            "=== FOREST SOURCE CONTEXT v1 ==="
        )

        line(
            "source_id: "
            + self._metadata(
                packet.source.source_id
            )
        )

        line(
            "source_kind: "
            + self._metadata(
                packet.source.source_kind
            )
        )

        line(
            "display_name: "
            + self._metadata(
                packet.source.display_name
            )
        )


        if include_locator:

            line(
                "locator: "
                + self._metadata(
                    packet.source.locator
                )
            )


        line(
            "content_sha256: "
            + self._metadata(
                packet.content_sha256
            )
        )

        line(
            "selected_source_characters: "
            f"{packet.source_character_count}"
        )

        line(
            "selected_source_lines: "
            f"{packet.source_line_count}"
        )

        line(
            "packet_character_budget: "
            f"{packet.max_characters}"
        )

        line(
            "packet_line_budget: "
            f"{packet.max_lines}"
        )


        # ------------------------------------------
        # TARGETS
        # ------------------------------------------

        line("targets:")

        for region_id in (
            packet.target_region_ids
        ):
            line(
                "- "
                + self._metadata(
                    region_id
                )
            )


        # ------------------------------------------
        # ANCESTOR BREADCRUMBS
        #
        # Packet order is nearest parent first.
        # ------------------------------------------

        line(
            "ancestors_nearest_first:"
        )


        if not packet.ancestor_region_ids:

            line("- none")


        else:

            for (
                region_id,
                label,
            ) in zip(
                packet.ancestor_region_ids,
                packet.ancestor_labels,
            ):

                line(
                    "- label="
                    + self._metadata(
                        label
                    )
                    + " region_id="
                    + self._metadata(
                        region_id
                    )
                )


        # ------------------------------------------
        # FRAGMENTS
        # ------------------------------------------

        line(
            "fragment_count: "
            f"{len(packet.fragments)}"
        )


        for index, fragment in enumerate(
            packet.fragments,
            start=1,
        ):

            line()

            line(
                f"--- fragment {index}: "
                f"lines {fragment.start_line}-"
                f"{fragment.end_line} ---"
            )

            line(
                "region_ids: "
                + self._metadata(
                    fragment.region_ids
                )
            )

            line(
                fence
                + "source"
            )


            # Exact selected source bytes have
            # already been decoded by the safe
            # snapshot layer. Do not alter them.
            parts.append(
                fragment.text
            )


            # Closing Markdown fence must begin on
            # a new line. This newline is rendering
            # syntax, not part of fragment.text.
            if (
                fragment.text
                and not fragment.text.endswith(
                    "\n"
                )
            ):
                parts.append(
                    "\n"
                )


            line(
                fence
            )


        line()
        line(
            "=== END FOREST SOURCE CONTEXT ==="
        )


        rendered_text = "".join(
            parts
        )


        if (
            len(rendered_text)
            > max_rendered_characters
        ):
            raise SourcePacketRenderBudgetError(
                "Rendered source packet exceeds "
                "the authorized character budget."
            )


        return RenderedSourcePacket(
            packet=packet,
            text=rendered_text,
            fence_character=(
                fence_character
            ),
            fence_length=(
                fence_length
            ),
            include_locator=(
                include_locator
            ),
            max_rendered_characters=(
                max_rendered_characters
            ),
        )
