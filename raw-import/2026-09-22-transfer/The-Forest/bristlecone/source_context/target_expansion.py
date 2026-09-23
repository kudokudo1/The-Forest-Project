\
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
    SourceRegion,
    SourceTarget,
)

from .structure import (
    SourceStructure,
)


SOURCE_TARGET_EXPANSION_MODE = (
    "bounded-ancestor-context"
)


class SourceTargetExpansionError(
    ValueError
):
    """Invalid bounded source-target expansion."""


@dataclass(
    frozen=True,
    slots=True,
)
class SourceTargetExpansion:
    """
    Immutable turn-local structural envelope around
    one SourceTarget.

    target:
        The region selected for this turn.

    ancestor_regions:
        Nearest structural parent first.

    Expansion contains structural references only.
    It does not contain or duplicate source text.
    """

    target: SourceTarget

    ancestor_regions: Tuple[
        SourceRegion,
        ...,
    ] = ()

    max_parent_hops: int = 1

    include_whole_source_parent: bool = False

    mode: str = (
        SOURCE_TARGET_EXPANSION_MODE
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
            raise SourceTargetExpansionError(
                "Unsupported target-expansion "
                "schema version."
            )


        if not isinstance(
            self.target,
            SourceTarget,
        ):
            raise SourceTargetExpansionError(
                "target must be a SourceTarget."
            )


        if (
            not isinstance(
                self.max_parent_hops,
                int,
            )
            or isinstance(
                self.max_parent_hops,
                bool,
            )
            or self.max_parent_hops < 0
        ):
            raise SourceTargetExpansionError(
                "max_parent_hops must be a "
                "non-negative integer."
            )


        if not isinstance(
            self.include_whole_source_parent,
            bool,
        ):
            raise SourceTargetExpansionError(
                "include_whole_source_parent "
                "must be bool."
            )


        try:
            ancestors = tuple(
                self.ancestor_regions
            )

        except TypeError as exc:
            raise SourceTargetExpansionError(
                "ancestor_regions must be "
                "iterable."
            ) from exc


        seen = {
            self.target.region.region_id
        }


        for region in ancestors:

            if not isinstance(
                region,
                SourceRegion,
            ):
                raise SourceTargetExpansionError(
                    "Every ancestor must be "
                    "a SourceRegion."
                )


            if (
                region.source
                != self.target.region.source
            ):
                raise SourceTargetExpansionError(
                    "Expansion regions must belong "
                    "to the target source."
                )


            if (
                region.fingerprint
                != self.target.region.fingerprint
            ):
                raise SourceTargetExpansionError(
                    "Expansion regions must belong "
                    "to the target source version."
                )


            if region.region_id in seen:
                raise SourceTargetExpansionError(
                    "Expansion regions must be "
                    "unique."
                )


            seen.add(
                region.region_id
            )


        if (
            len(ancestors)
            > self.max_parent_hops
        ):
            raise SourceTargetExpansionError(
                "Expansion exceeds "
                "max_parent_hops."
            )


        if (
            not self.include_whole_source_parent
            and any(
                region.is_whole_source
                for region in ancestors
            )
        ):
            raise SourceTargetExpansionError(
                "Whole-source ancestor was "
                "included without permission."
            )


        object.__setattr__(
            self,
            "ancestor_regions",
            ancestors,
        )


        if (
            not isinstance(
                self.mode,
                str,
            )
            or not self.mode.strip()
        ):
            raise SourceTargetExpansionError(
                "mode must be a non-empty string."
            )


    @property
    def target_region(
        self,
    ):
        return self.target.region


    @property
    def parent_hops(
        self,
    ):
        return len(
            self.ancestor_regions
        )


    @property
    def regions(
        self,
    ):
        """
        Priority order for later context assembly:
        exact target first, then nearest ancestors.
        """

        return (
            self.target.region,
            *self.ancestor_regions,
        )


    @property
    def includes_whole_source(
        self,
    ):
        return any(
            region.is_whole_source
            for region in self.regions
        )


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "mode":
                self.mode,

            "target_region_id":
                self.target.region.region_id,

            "ancestor_region_ids":
                tuple(
                    region.region_id
                    for region
                    in self.ancestor_regions
                ),

            "parent_hops":
                self.parent_hops,

            "max_parent_hops":
                self.max_parent_hops,

            "include_whole_source_parent":
                self.include_whole_source_parent,

            "includes_whole_source":
                self.includes_whole_source,
        }


class BoundedSourceTargetExpander:
    """
    Add only bounded structural ancestors around an
    already-selected SourceTarget.

    The expander never adds:

    - siblings;
    - children;
    - unrelated regions;
    - whole-source ancestry unless explicitly
      permitted.

    It performs no file I/O, parsing, caching,
    source-text extraction, or runtime/model calls.
    """


    @staticmethod
    def _require_structure(
        structure,
    ):
        if not isinstance(
            structure,
            SourceStructure,
        ):
            raise SourceTargetExpansionError(
                "structure must be a "
                "SourceStructure."
            )


    @staticmethod
    def _require_target(
        target,
    ):
        if not isinstance(
            target,
            SourceTarget,
        ):
            raise SourceTargetExpansionError(
                "target must be a "
                "SourceTarget."
            )


    @staticmethod
    def _require_hops(
        max_parent_hops,
    ):
        if (
            not isinstance(
                max_parent_hops,
                int,
            )
            or isinstance(
                max_parent_hops,
                bool,
            )
            or max_parent_hops < 0
        ):
            raise SourceTargetExpansionError(
                "max_parent_hops must be a "
                "non-negative integer."
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
            raise SourceTargetExpansionError(
                f"{field_name} must be bool."
            )


    @staticmethod
    def _validate_target_membership(
        structure,
        target,
    ):
        region = structure.region_by_id(
            target.region.region_id
        )


        if region is None:
            raise SourceTargetExpansionError(
                "Target region does not belong "
                "to this SourceStructure."
            )


        if (
            region
            != target.region
        ):
            raise SourceTargetExpansionError(
                "Target region ID resolves to "
                "different structural truth."
            )


        if (
            target.region.source
            != structure.source
        ):
            raise SourceTargetExpansionError(
                "Target source does not match "
                "SourceStructure."
            )


        if (
            target.region.fingerprint
            != structure.fingerprint
        ):
            raise SourceTargetExpansionError(
                "Target source version does not "
                "match SourceStructure."
            )


    def expand(
        self,
        structure,
        target,
        *,
        max_parent_hops=1,
        include_whole_source_parent=False,
    ):
        self._require_structure(
            structure
        )

        self._require_target(
            target
        )

        self._require_hops(
            max_parent_hops
        )

        self._require_bool(
            include_whole_source_parent,
            field_name=(
                "include_whole_source_parent"
            ),
        )


        self._validate_target_membership(
            structure,
            target,
        )


        ancestors = []


        # Protect against malformed/cyclic structural
        # graphs. The target itself is already visited.
        visited = {
            target.region.region_id
        }


        current = target.region


        while (
            len(ancestors)
            < max_parent_hops
        ):
            parent_id = (
                current.parent_region_id
            )


            if parent_id is None:
                break


            if parent_id in visited:
                raise SourceTargetExpansionError(
                    "Cycle detected in source "
                    "region parent hierarchy."
                )


            parent = structure.region_by_id(
                parent_id
            )


            if parent is None:
                raise SourceTargetExpansionError(
                    "Source region references a "
                    "missing structural parent."
                )


            if (
                parent.source
                != structure.source
                or parent.fingerprint
                != structure.fingerprint
            ):
                raise SourceTargetExpansionError(
                    "Structural parent belongs to "
                    "different source truth."
                )


            # Whole-source is deliberately an
            # escalation boundary.
            if (
                parent.is_whole_source
                and not include_whole_source_parent
            ):
                break


            visited.add(
                parent.region_id
            )

            ancestors.append(
                parent
            )


            current = parent


            if parent.is_whole_source:
                break


        return SourceTargetExpansion(
            target=target,
            ancestor_regions=tuple(
                ancestors
            ),
            max_parent_hops=(
                max_parent_hops
            ),
            include_whole_source_parent=(
                include_whole_source_parent
            ),
        )
