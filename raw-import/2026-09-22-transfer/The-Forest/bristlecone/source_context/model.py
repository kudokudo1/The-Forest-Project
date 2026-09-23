\
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple, Union


SOURCE_CONTEXT_SCHEMA_VERSION = 1


FingerprintScalar = Union[
    str,
    int,
    bool,
    None,
]


class SourceContextModelError(
    ValueError
):
    """Invalid runtime-neutral Source Context model."""


def _required_text(
    value,
    *,
    field_name,
):
    if not isinstance(
        value,
        str,
    ):
        raise SourceContextModelError(
            f"{field_name} must be a string."
        )

    if not value.strip():
        raise SourceContextModelError(
            f"{field_name} must not be empty."
        )

    return value


def _optional_text(
    value,
    *,
    field_name,
):
    if value is None:
        return None

    return _required_text(
        value,
        field_name=field_name,
    )


def _validate_schema_version(
    value,
):
    if (
        value
        != SOURCE_CONTEXT_SCHEMA_VERSION
    ):
        raise SourceContextModelError(
            "Unsupported Source Context "
            f"schema version: {value!r}."
        )


def _freeze_fingerprint_components(
    value,
):
    if not isinstance(
        value,
        (
            tuple,
            list,
        ),
    ):
        raise SourceContextModelError(
            "fingerprint components must "
            "be a sequence of key/value pairs."
        )

    result = []
    names = set()

    for item in value:
        if not isinstance(
            item,
            (
                tuple,
                list,
            ),
        ):
            raise SourceContextModelError(
                "Each fingerprint component "
                "must be a key/value pair."
            )

        if len(item) != 2:
            raise SourceContextModelError(
                "Each fingerprint component "
                "must contain exactly two values."
            )

        name = _required_text(
            item[0],
            field_name=(
                "fingerprint component name"
            ),
        )

        component = item[1]

        if not isinstance(
            component,
            (
                str,
                int,
                bool,
                type(None),
            ),
        ):
            raise SourceContextModelError(
                "Fingerprint component values "
                "must be str, int, bool, or None."
            )

        if name in names:
            raise SourceContextModelError(
                "Fingerprint component names "
                "must be unique."
            )

        names.add(
            name
        )

        result.append(
            (
                name,
                component,
            )
        )

    if not result:
        raise SourceContextModelError(
            "A SourceFingerprint requires "
            "at least one component."
        )

    # Fingerprint equality must not depend on the
    # caller's component ordering.
    result.sort(
        key=lambda item: item[0]
    )

    return tuple(
        result
    )


@dataclass(
    frozen=True,
    slots=True,
)
class SourceIdentity:
    """
    Stable identity of an authoritative source.

    This object describes WHAT the source is.
    It deliberately says nothing about which
    current turn considers it relevant.
    """

    source_id: str
    source_kind: str
    locator: str

    display_name: Optional[str] = field(
        default=None,
        compare=False,
    )

    schema_version: int = (
        SOURCE_CONTEXT_SCHEMA_VERSION
    )


    def __post_init__(
        self,
    ):
        _validate_schema_version(
            self.schema_version
        )

        _required_text(
            self.source_id,
            field_name="source_id",
        )

        _required_text(
            self.source_kind,
            field_name="source_kind",
        )

        _required_text(
            self.locator,
            field_name="locator",
        )

        _optional_text(
            self.display_name,
            field_name="display_name",
        )


    @property
    def identity_key(
        self,
    ):
        return (
            self.source_kind,
            self.source_id,
            self.locator,
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.source_id,

            "source_kind":
                self.source_kind,

            "locator":
                self.locator,

            "display_name":
                self.display_name,
        }


@dataclass(
    frozen=True,
    slots=True,
)
class SourceFingerprint:
    """
    Exact observed version of a SourceIdentity.

    Components are immutable, canonicalized,
    and suitable for conversion into ordinary
    CacheCoordinator dependency mappings.

    Example local-file components:

        (
            ("mtime_ns", 123456789),
            ("size", 4096),
        )
    """

    source: SourceIdentity
    method: str

    components: Tuple[
        Tuple[
            str,
            FingerprintScalar,
        ],
        ...,
    ]

    schema_version: int = (
        SOURCE_CONTEXT_SCHEMA_VERSION
    )


    def __post_init__(
        self,
    ):
        _validate_schema_version(
            self.schema_version
        )

        if not isinstance(
            self.source,
            SourceIdentity,
        ):
            raise SourceContextModelError(
                "source must be a "
                "SourceIdentity."
            )

        _required_text(
            self.method,
            field_name="method",
        )

        frozen = (
            _freeze_fingerprint_components(
                self.components
            )
        )

        object.__setattr__(
            self,
            "components",
            frozen,
        )


    def dependency_dict(
        self,
    ):
        return dict(
            self.components
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.source.source_id,

            "method":
                self.method,

            "components":
                self.components,
        }


@dataclass(
    frozen=True,
    slots=True,
)
class SourceRegion:
    """
    Objective bounded structure inside one
    exact observed source version.

    A SourceRegion is shareable knowledge.
    It does NOT contain a turn-specific
    relevance decision.
    """

    source: SourceIdentity
    fingerprint: SourceFingerprint

    region_id: str
    region_kind: str

    start_line: Optional[int] = None
    end_line: Optional[int] = None

    label: Optional[str] = None
    parent_region_id: Optional[str] = None

    schema_version: int = (
        SOURCE_CONTEXT_SCHEMA_VERSION
    )


    def __post_init__(
        self,
    ):
        _validate_schema_version(
            self.schema_version
        )

        if not isinstance(
            self.source,
            SourceIdentity,
        ):
            raise SourceContextModelError(
                "source must be a "
                "SourceIdentity."
            )

        if not isinstance(
            self.fingerprint,
            SourceFingerprint,
        ):
            raise SourceContextModelError(
                "fingerprint must be a "
                "SourceFingerprint."
            )

        if (
            self.fingerprint.source
            != self.source
        ):
            raise SourceContextModelError(
                "SourceRegion source and "
                "fingerprint source must match."
            )

        _required_text(
            self.region_id,
            field_name="region_id",
        )

        _required_text(
            self.region_kind,
            field_name="region_kind",
        )

        _optional_text(
            self.label,
            field_name="label",
        )

        _optional_text(
            self.parent_region_id,
            field_name="parent_region_id",
        )

        if (
            self.start_line is None
        ) != (
            self.end_line is None
        ):
            raise SourceContextModelError(
                "start_line and end_line "
                "must either both be set "
                "or both be None."
            )

        if self.start_line is not None:
            if (
                not isinstance(
                    self.start_line,
                    int,
                )
                or isinstance(
                    self.start_line,
                    bool,
                )
            ):
                raise SourceContextModelError(
                    "start_line must be "
                    "an integer."
                )

            if (
                not isinstance(
                    self.end_line,
                    int,
                )
                or isinstance(
                    self.end_line,
                    bool,
                )
            ):
                raise SourceContextModelError(
                    "end_line must be "
                    "an integer."
                )

            if self.start_line < 1:
                raise SourceContextModelError(
                    "start_line must be >= 1."
                )

            if (
                self.end_line
                < self.start_line
            ):
                raise SourceContextModelError(
                    "end_line must be >= "
                    "start_line."
                )


    @property
    def is_whole_source(
        self,
    ):
        return (
            self.start_line is None
            and self.end_line is None
        )


    @property
    def line_count(
        self,
    ):
        if self.start_line is None:
            return None

        return (
            self.end_line
            - self.start_line
            + 1
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.source.source_id,

            "fingerprint_method":
                self.fingerprint.method,

            "region_id":
                self.region_id,

            "region_kind":
                self.region_kind,

            "start_line":
                self.start_line,

            "end_line":
                self.end_line,

            "line_count":
                self.line_count,

            "label":
                self.label,

            "parent_region_id":
                self.parent_region_id,
        }


@dataclass(
    frozen=True,
    slots=True,
)
class SourceTarget:
    """
    Turn-local relevance decision pointing at
    an objective SourceRegion.

    SourceRegion may be Colony-shared.
    SourceTarget must not be blindly shared
    between turns or Clones.
    """

    region: SourceRegion

    selection_method: str
    reason: str

    required: bool = False

    schema_version: int = (
        SOURCE_CONTEXT_SCHEMA_VERSION
    )


    def __post_init__(
        self,
    ):
        _validate_schema_version(
            self.schema_version
        )

        if not isinstance(
            self.region,
            SourceRegion,
        ):
            raise SourceContextModelError(
                "region must be a "
                "SourceRegion."
            )

        _required_text(
            self.selection_method,
            field_name="selection_method",
        )

        _required_text(
            self.reason,
            field_name="reason",
        )

        if not isinstance(
            self.required,
            bool,
        ):
            raise SourceContextModelError(
                "required must be bool."
            )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.region.source.source_id,

            "region_id":
                self.region.region_id,

            "selection_method":
                self.selection_method,

            "reason":
                self.reason,

            "required":
                self.required,
        }
