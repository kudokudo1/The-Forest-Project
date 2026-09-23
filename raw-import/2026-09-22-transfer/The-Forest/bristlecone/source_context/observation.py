\
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Optional, Union

from .model import (
    SourceFingerprint,
    SourceIdentity,
)


LOCAL_FILE_FINGERPRINT_METHOD = "stat-size-mtime-v1"


class LocalSourceObservationError(
    ValueError
):
    """Invalid or unavailable local source."""


class LocalSourceObserver:
    """
    Observe local filesystem sources without
    reading their contents.

    Responsibilities:

    - canonicalize a local file path;
    - produce stable path-addressed identity;
    - capture derived freshness dependencies.

    Non-responsibilities:

    - reading source contents;
    - parsing source structure;
    - choosing relevant regions;
    - managing derived-cache entries;
    - runtime/Hermes interaction.
    """


    @staticmethod
    def _canonical_file_path(
        path,
    ):
        try:
            candidate = Path(
                path
            ).expanduser()

        except Exception as exc:
            raise LocalSourceObservationError(
                "Local source path could "
                "not be interpreted."
            ) from exc

        try:
            resolved = candidate.resolve(
                strict=True
            )

        except FileNotFoundError as exc:
            raise LocalSourceObservationError(
                "Local source does not exist: "
                f"{candidate}"
            ) from exc

        except OSError as exc:
            raise LocalSourceObservationError(
                "Local source path could not "
                f"be resolved: {candidate}"
            ) from exc

        if not resolved.is_file():
            raise LocalSourceObservationError(
                "Local source must be a "
                f"regular file: {resolved}"
            )

        return resolved


    @staticmethod
    def _default_source_id(
        locator,
    ):
        digest = sha256(
            locator.encode(
                "utf-8"
            )
        ).hexdigest()

        return (
            "local-file:"
            + digest
        )


    def observe(
        self,
        path: Union[
            str,
            Path,
        ],
        *,
        source_id: Optional[str] = None,
        display_name: Optional[str] = None,
    ) -> SourceFingerprint:

        resolved = (
            self._canonical_file_path(
                path
            )
        )

        locator = str(
            resolved
        )

        if source_id is None:
            source_id = (
                self._default_source_id(
                    locator
                )
            )

        if display_name is None:
            display_name = (
                resolved.name
            )

        source = SourceIdentity(
            source_id=source_id,
            source_kind="file",
            locator=locator,
            display_name=display_name,
        )

        try:
            stat = resolved.stat()

        except OSError as exc:
            raise LocalSourceObservationError(
                "Local source metadata "
                "could not be observed: "
                f"{resolved}"
            ) from exc

        return SourceFingerprint(
            source=source,
            method=(
                LOCAL_FILE_FINGERPRINT_METHOD
            ),
            components=(
                (
                    "size",
                    stat.st_size,
                ),
                (
                    "mtime_ns",
                    stat.st_mtime_ns,
                ),
            ),
        )
