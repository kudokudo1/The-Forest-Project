\
from __future__ import annotations

from .model import (
    SourceRegion,
    SourceTarget,
)

from .structure import (
    SourceStructure,
)


class SourceTargetingError(
    ValueError
):
    """Invalid deterministic source-target request."""


class SourceTargetNotFoundError(
    SourceTargetingError
):
    """Requested structural source target does not exist."""


class SourceTargetAmbiguityError(
    SourceTargetingError
):
    """Requested structural source target is ambiguous."""


class DeterministicSourceTargeter:
    """
    Turn-local deterministic targeting over an
    already-derived objective SourceStructure.

    Current supported selectors:

    - exact region_id
    - exact unique label

    The targeter performs no:

    - filesystem I/O;
    - parsing;
    - cache mutation;
    - fuzzy/semantic matching;
    - model/runtime calls;
    - silent whole-source fallback.
    """


    @staticmethod
    def _require_structure(
        structure,
    ):
        if not isinstance(
            structure,
            SourceStructure,
        ):
            raise SourceTargetingError(
                "structure must be a "
                "SourceStructure."
            )


    @staticmethod
    def _require_text(
        value,
        *,
        field_name,
    ):
        if (
            not isinstance(
                value,
                str,
            )
            or not value.strip()
        ):
            raise SourceTargetingError(
                f"{field_name} must be a "
                "non-empty string."
            )

        return value


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
            raise SourceTargetingError(
                f"{field_name} must be bool."
            )

        return value


    @classmethod
    def _target(
        cls,
        region,
        *,
        selection_method,
        reason,
        required,
    ):
        if not isinstance(
            region,
            SourceRegion,
        ):
            raise SourceTargetingError(
                "region must be a SourceRegion."
            )

        cls._require_text(
            selection_method,
            field_name="selection_method",
        )

        cls._require_text(
            reason,
            field_name="reason",
        )

        cls._require_bool(
            required,
            field_name="required",
        )

        return SourceTarget(
            region=region,
            selection_method=selection_method,
            reason=reason,
            required=required,
        )


    def target_region_id(
        self,
        structure,
        region_id,
        *,
        reason=(
            "explicit structural region ID"
        ),
        required=True,
    ):
        """
        Select exactly one objective region by its
        deterministic region_id.
        """

        self._require_structure(
            structure
        )

        region_id = self._require_text(
            region_id,
            field_name="region_id",
        )

        region = structure.region_by_id(
            region_id
        )

        if region is None:
            raise SourceTargetNotFoundError(
                "No source region exists with "
                f"region_id {region_id!r}."
            )

        return self._target(
            region,
            selection_method=(
                "explicit-region-id"
            ),
            reason=reason,
            required=required,
        )


    def target_exact_label(
        self,
        structure,
        label,
        *,
        region_kind=None,
        reason=(
            "explicit unique structural label"
        ),
        required=True,
    ):
        """
        Select exactly one objective region by
        exact label.

        If multiple regions have the same label
        after optional region_kind filtering,
        targeting fails closed rather than choosing
        an arbitrary occurrence.
        """

        self._require_structure(
            structure
        )

        label = self._require_text(
            label,
            field_name="label",
        )

        if region_kind is not None:
            region_kind = self._require_text(
                region_kind,
                field_name="region_kind",
            )

        matches = tuple(
            region
            for region in structure.regions
            if (
                region.label == label
                and (
                    region_kind is None
                    or region.region_kind
                    == region_kind
                )
            )
        )

        if not matches:
            suffix = (
                ""
                if region_kind is None
                else (
                    " with region_kind "
                    f"{region_kind!r}"
                )
            )

            raise SourceTargetNotFoundError(
                "No source region exists with "
                f"exact label {label!r}"
                f"{suffix}."
            )

        if len(matches) != 1:
            raise SourceTargetAmbiguityError(
                "Exact source label "
                f"{label!r} matched "
                f"{len(matches)} regions; "
                "use region_id or a more "
                "specific structural reference."
            )

        return self._target(
            matches[0],
            selection_method=(
                "explicit-exact-label"
            ),
            reason=reason,
            required=required,
        )
