"""Stateless deterministic representation of selected Forest context.

The assembler receives authoritative records that have already
been selected by routing and retrieval.

It does not:
- decide relevance
- read Cold storage
- own Task or Clone state
- own caches
- call a runtime
- mutate Forest records

This makes the same assembler safe for concurrent use across
many Tasks and Clones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .foundation import ForestLearningRecord


HOT_CONTEXT_SCHEMA_VERSION = 1


class HotContextAssemblyError(
    RuntimeError
):
    """Selected Hot Context cannot be represented safely."""


def _records_tuple(
    records,
    *,
    field_name,
):
    if isinstance(
        records,
        ForestLearningRecord,
    ):
        raise HotContextAssemblyError(
            f"{field_name} must be an iterable "
            "of records, not one record."
        )

    try:
        return tuple(records)

    except TypeError as exc:
        raise HotContextAssemblyError(
            f"{field_name} must be iterable."
        ) from exc


def _clean_text(
    value,
):
    if value is None:
        return ""

    if not isinstance(
        value,
        str,
    ):
        raise HotContextAssemblyError(
            "Hot Context record text "
            "must be a string."
        )

    return value.strip()


@dataclass(
    frozen=True
)
class HotContextAssembly:
    """Immutable result for one already-routed turn."""

    schema_version: int

    prompt: str

    user_context_record_ids: Tuple[
        str,
        ...
    ]

    operational_learning_record_ids: Tuple[
        str,
        ...
    ]

    section_names: Tuple[
        str,
        ...
    ]

    character_count: int


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != HOT_CONTEXT_SCHEMA_VERSION
        ):
            raise HotContextAssemblyError(
                "Unsupported Hot Context "
                "schema version."
            )

        if not isinstance(
            self.prompt,
            str,
        ):
            raise HotContextAssemblyError(
                "Hot Context prompt "
                "must be a string."
            )

        if (
            isinstance(
                self.character_count,
                bool,
            )
            or not isinstance(
                self.character_count,
                int,
            )
            or self.character_count < 0
        ):
            raise HotContextAssemblyError(
                "character_count must be "
                "an integer >= 0."
            )

        if (
            self.character_count
            != len(self.prompt)
        ):
            raise HotContextAssemblyError(
                "character_count does not "
                "match prompt length."
            )


    @property
    def record_count(
        self,
    ):
        return (
            len(
                self.user_context_record_ids
            )
            + len(
                self.operational_learning_record_ids
            )
        )


    @property
    def is_empty(
        self,
    ):
        return self.record_count == 0


    def inspect(
        self,
    ):
        """Metadata only; never duplicate context contents."""

        return {
            "schema_version":
                self.schema_version,

            "record_count":
                self.record_count,

            "user_context_record_count":
                len(
                    self.user_context_record_ids
                ),

            "operational_learning_record_count":
                len(
                    self.operational_learning_record_ids
                ),

            "section_names":
                self.section_names,

            "character_count":
                self.character_count,

            "empty":
                self.is_empty,
        }


class LayeredHotContextAssembler:
    """Pure formatter for already-selected Forest records."""

    __slots__ = (
        "_max_characters",
    )


    _USER_SECTION_ORDER = (
        (
            "user-correction",
            "User Corrections",
        ),
        (
            "user-constraint",
            "User Constraints",
        ),
        (
            "user-preference",
            "User Preferences",
        ),
        (
            "current-context",
            "Current Context",
        ),
    )


    def __init__(
        self,
        *,
        max_characters=None,
    ):
        if max_characters is not None:
            if (
                isinstance(
                    max_characters,
                    bool,
                )
                or not isinstance(
                    max_characters,
                    int,
                )
                or max_characters <= 0
            ):
                raise HotContextAssemblyError(
                    "max_characters must be None "
                    "or an integer > 0."
                )

        self._max_characters = (
            max_characters
        )


    @property
    def max_characters(
        self,
    ):
        return self._max_characters


    @staticmethod
    def _validate_unique(
        records,
    ):
        seen = set()

        for record in records:
            record_id = record.record_id

            if record_id in seen:
                raise HotContextAssemblyError(
                    "Duplicate Hot Context "
                    f"record ID: {record_id}"
                )

            seen.add(
                record_id
            )


    @staticmethod
    def _render_record(
        record,
        *,
        include_operational_kind=False,
    ):
        summary = _clean_text(
            record.summary
        )

        detail = _clean_text(
            record.detail
        )

        if not summary:
            raise HotContextAssemblyError(
                "Hot Context records require "
                "a non-empty summary."
            )

        prefix = "- "

        if include_operational_kind:
            kind = _clean_text(
                record.operational_kind
            )

            if kind:
                prefix = (
                    f"- [{kind}] "
                )

        rendered = (
            prefix
            + summary
        )

        if (
            detail
            and detail != summary
        ):
            rendered += (
                "\n  "
                + detail
            )

        return rendered


    def assemble(
        self,
        *,
        user_context_records=(),
        operational_learning_records=(),
    ):
        """Return one immutable representation.

        No state from this call is retained on the assembler.
        """

        user_records = _records_tuple(
            user_context_records,
            field_name=(
                "user_context_records"
            ),
        )

        operational_records = _records_tuple(
            operational_learning_records,
            field_name=(
                "operational_learning_records"
            ),
        )


        # ----------------------------------------------
        # Validate User Context boundary.
        # ----------------------------------------------

        for record in user_records:
            if not isinstance(
                record,
                ForestLearningRecord,
            ):
                raise HotContextAssemblyError(
                    "User Context Hot records "
                    "must be ForestLearningRecord "
                    "values."
                )

            if not record.is_user_context:
                raise HotContextAssemblyError(
                    "Operational Learning cannot "
                    "enter the User Context Hot layer."
                )

            if record.status != "active":
                raise HotContextAssemblyError(
                    "Inactive User Context cannot "
                    "enter Hot Context."
                )


        # ----------------------------------------------
        # Validate Operational Learning boundary.
        # ----------------------------------------------

        for record in operational_records:
            if not isinstance(
                record,
                ForestLearningRecord,
            ):
                raise HotContextAssemblyError(
                    "Operational Hot records "
                    "must be ForestLearningRecord "
                    "values."
                )

            if (
                record.record_type
                != "operational-learning"
            ):
                raise HotContextAssemblyError(
                    "User Context cannot enter "
                    "the Operational Learning "
                    "Hot layer."
                )

            if record.status != "active":
                raise HotContextAssemblyError(
                    "Inactive Operational Learning "
                    "cannot enter Hot Context."
                )


        all_records = (
            user_records
            + operational_records
        )


        self._validate_unique(
            all_records
        )


        if not all_records:
            return HotContextAssembly(
                schema_version=(
                    HOT_CONTEXT_SCHEMA_VERSION
                ),
                prompt="",
                user_context_record_ids=(),
                operational_learning_record_ids=(),
                section_names=(),
                character_count=0,
            )


        # ----------------------------------------------
        # Semantic authority buckets.
        # Input order is retained inside each layer.
        # ----------------------------------------------

        user_buckets = {
            record_type: []
            for (
                record_type,
                _
            ) in self._USER_SECTION_ORDER
        }


        for record in user_records:
            try:
                user_buckets[
                    record.record_type
                ].append(
                    record
                )

            except KeyError as exc:
                raise HotContextAssemblyError(
                    "Unsupported User Context "
                    "record type for Hot assembly: "
                    f"{record.record_type!r}"
                ) from exc


        sections = []
        section_names = []


        for (
            record_type,
            display_name,
        ) in self._USER_SECTION_ORDER:

            records = user_buckets[
                record_type
            ]

            if not records:
                continue

            section_names.append(
                display_name
            )

            body = "\n".join(
                self._render_record(
                    record
                )
                for record in records
            )

            sections.append(
                f"## {display_name}\n"
                f"{body}"
            )


        if operational_records:
            display_name = (
                "Operational Learning"
            )

            section_names.append(
                display_name
            )

            body = "\n".join(
                self._render_record(
                    record,
                    include_operational_kind=True,
                )
                for record
                in operational_records
            )

            sections.append(
                f"## {display_name}\n"
                f"{body}"
            )


        # ----------------------------------------------
        # Stable model-facing authority envelope.
        # ----------------------------------------------

        prompt = (
            "## Forest Hot Context\n"
            "Use this remembered context only "
            "where relevant to the current task. "
            "The current user message and active "
            "Forest policy take precedence over "
            "this remembered context.\n\n"
            + "\n\n".join(
                sections
            )
        )


        if (
            self._max_characters
            is not None
            and len(prompt)
            > self._max_characters
        ):
            raise HotContextAssemblyError(
                "Selected Hot Context exceeds "
                "the configured character budget; "
                "records were not silently "
                "truncated."
            )


        return HotContextAssembly(
            schema_version=(
                HOT_CONTEXT_SCHEMA_VERSION
            ),
            prompt=prompt,

            user_context_record_ids=tuple(
                record.record_id
                for record in user_records
            ),

            operational_learning_record_ids=tuple(
                record.record_id
                for record in operational_records
            ),

            section_names=tuple(
                section_names
            ),

            character_count=len(
                prompt
            ),
        )
