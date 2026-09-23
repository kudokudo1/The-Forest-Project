\
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Tuple

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
    SourceFingerprint,
    SourceRegion,
)
from .snapshot import (
    SourceContentSnapshot,
)


PYTHON_STRUCTURE_KIND = "python-ast-v1"


class SourceStructureError(
    ValueError
):
    """Invalid or unparseable source structure."""


@dataclass(
    frozen=True,
    slots=True,
)
class SourceStructure:
    """
    Immutable objective structure derived from
    one exact SourceContentSnapshot.

    Regions describe source truth.
    They do not say whether a turn needs them.
    """

    fingerprint: SourceFingerprint
    structure_kind: str
    regions: Tuple[
        SourceRegion,
        ...,
    ]

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
            raise SourceStructureError(
                "Unsupported source structure "
                f"schema version: "
                f"{self.schema_version!r}."
            )

        if not isinstance(
            self.fingerprint,
            SourceFingerprint,
        ):
            raise SourceStructureError(
                "fingerprint must be a "
                "SourceFingerprint."
            )

        if (
            not isinstance(
                self.structure_kind,
                str,
            )
            or not self.structure_kind.strip()
        ):
            raise SourceStructureError(
                "structure_kind must be a "
                "non-empty string."
            )

        try:
            regions = tuple(
                self.regions
            )

        except TypeError as exc:
            raise SourceStructureError(
                "regions must be iterable."
            ) from exc

        if not regions:
            raise SourceStructureError(
                "SourceStructure requires "
                "at least one region."
            )

        seen = set()

        for region in regions:
            if not isinstance(
                region,
                SourceRegion,
            ):
                raise SourceStructureError(
                    "Every region must be "
                    "a SourceRegion."
                )

            if (
                region.fingerprint
                != self.fingerprint
            ):
                raise SourceStructureError(
                    "All regions must belong "
                    "to the same fingerprint."
                )

            if (
                region.source
                != self.fingerprint.source
            ):
                raise SourceStructureError(
                    "All regions must belong "
                    "to the same source."
                )

            if region.region_id in seen:
                raise SourceStructureError(
                    "SourceStructure region IDs "
                    "must be unique."
                )

            seen.add(
                region.region_id
            )

        object.__setattr__(
            self,
            "regions",
            regions,
        )


    @property
    def source(
        self,
    ):
        return self.fingerprint.source


    @property
    def region_count(
        self,
    ):
        return len(
            self.regions
        )


    def region_by_id(
        self,
        region_id,
    ):
        for region in self.regions:
            if (
                region.region_id
                == region_id
            ):
                return region

        return None


    def inspect(
        self,
    ):
        counts = {}

        for region in self.regions:
            counts[
                region.region_kind
            ] = (
                counts.get(
                    region.region_kind,
                    0,
                )
                + 1
            )

        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.source.source_id,

            "structure_kind":
                self.structure_kind,

            "region_count":
                self.region_count,

            "region_kind_counts":
                tuple(
                    sorted(
                        counts.items()
                    )
                ),

            "region_ids":
                tuple(
                    region.region_id
                    for region in self.regions
                ),
        }


class PythonSourceStructureBuilder:
    """
    Derive objective Python regions from one
    immutable SourceContentSnapshot.

    Current region types:

    - whole-source
    - python-class
    - python-function
    - python-async-function
    - python-method
    - python-async-method

    This builder performs no filesystem I/O,
    caching, targeting, or runtime interaction.
    """


    @staticmethod
    def _start_line(
        node,
    ):
        lines = [
            node.lineno
        ]

        for decorator in getattr(
            node,
            "decorator_list",
            (),
        ):
            decorator_line = getattr(
                decorator,
                "lineno",
                None,
            )

            if decorator_line is not None:
                lines.append(
                    decorator_line
                )

        return min(
            lines
        )


    @staticmethod
    def _end_line(
        node,
    ):
        value = getattr(
            node,
            "end_lineno",
            None,
        )

        if value is None:
            value = node.lineno

        return value


    @staticmethod
    def _region_kind(
        node,
        parent_scope_kind,
    ):
        if isinstance(
            node,
            ast.ClassDef,
        ):
            return "python-class"

        if isinstance(
            node,
            ast.AsyncFunctionDef,
        ):
            if (
                parent_scope_kind
                == "python-class"
            ):
                return (
                    "python-async-method"
                )

            return (
                "python-async-function"
            )

        if isinstance(
            node,
            ast.FunctionDef,
        ):
            if (
                parent_scope_kind
                == "python-class"
            ):
                return "python-method"

            return "python-function"

        raise SourceStructureError(
            "Unsupported Python structural node."
        )


    def build(
        self,
        snapshot,
    ):
        if not isinstance(
            snapshot,
            SourceContentSnapshot,
        ):
            raise SourceStructureError(
                "snapshot must be a "
                "SourceContentSnapshot."
            )

        try:
            tree = ast.parse(
                snapshot.text,
                filename=(
                    snapshot.source.locator
                ),
            )

        except SyntaxError as exc:
            raise SourceStructureError(
                "Python source could not "
                "be parsed."
            ) from exc

        whole = SourceRegion(
            source=snapshot.source,
            fingerprint=(
                snapshot.fingerprint
            ),
            region_id="python:module",
            region_kind="whole-source",
            label=(
                snapshot.source.display_name
                or snapshot.source.source_id
            ),
        )

        discovered = []


        def visit(
            node,
            *,
            scope_names,
            parent_region_id,
            parent_scope_kind,
        ):
            structural = isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )

            if structural:
                kind = (
                    self._region_kind(
                        node,
                        parent_scope_kind,
                    )
                )

                names = (
                    scope_names
                    + (
                        node.name,
                    )
                )

                qualified_name = ".".join(
                    names
                )

                start_line = (
                    self._start_line(
                        node
                    )
                )

                end_line = (
                    self._end_line(
                        node
                    )
                )

                # Line component prevents collisions
                # when Python deliberately redefines
                # the same name in one lexical scope.
                region_id = (
                    f"{kind}:"
                    f"{qualified_name}"
                    f"@L{start_line}"
                )

                region = SourceRegion(
                    source=snapshot.source,
                    fingerprint=(
                        snapshot.fingerprint
                    ),
                    region_id=region_id,
                    region_kind=kind,
                    start_line=start_line,
                    end_line=end_line,
                    label=qualified_name,
                    parent_region_id=(
                        parent_region_id
                    ),
                )

                discovered.append(
                    region
                )

                for child in node.body:
                    visit(
                        child,
                        scope_names=names,
                        parent_region_id=(
                            region_id
                        ),
                        parent_scope_kind=kind,
                    )

                return

            for child in ast.iter_child_nodes(
                node
            ):
                visit(
                    child,
                    scope_names=scope_names,
                    parent_region_id=(
                        parent_region_id
                    ),
                    parent_scope_kind=(
                        parent_scope_kind
                    ),
                )


        for statement in tree.body:
            visit(
                statement,
                scope_names=(),
                parent_region_id=(
                    whole.region_id
                ),
                parent_scope_kind=None,
            )


        discovered.sort(
            key=lambda region: (
                region.start_line
                if region.start_line
                is not None
                else 0,

                region.end_line
                if region.end_line
                is not None
                else 0,

                region.region_id,
            )
        )


        return SourceStructure(
            fingerprint=(
                snapshot.fingerprint
            ),
            structure_kind=(
                PYTHON_STRUCTURE_KIND
            ),
            regions=(
                whole,
                *discovered,
            ),
        )
