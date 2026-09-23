\
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import os
from pathlib import Path
from typing import Optional, Union

from .model import (
    SOURCE_CONTEXT_SCHEMA_VERSION,
    SourceFingerprint,
)
from .observation import (
    LocalSourceObservationError,
    LocalSourceObserver,
)


class SourceSnapshotError(
    ValueError
):
    """Unable to produce one stable source snapshot."""


class SourceChangedDuringReadError(
    SourceSnapshotError
):
    """Authoritative source changed during snapshot read."""


@dataclass(
    frozen=True,
    slots=True,
)
class SourceContentSnapshot:
    """
    Immutable text snapshot of one exact observed
    local source version.

    The text is content truth for this snapshot.
    The fingerprint describes the observed source
    version associated with that content.
    """

    fingerprint: SourceFingerprint
    text: str
    encoding: str
    content_sha256: str
    byte_count: int
    character_count: int
    line_count: int

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
            raise SourceSnapshotError(
                "Unsupported source snapshot "
                f"schema version: "
                f"{self.schema_version!r}."
            )

        if not isinstance(
            self.fingerprint,
            SourceFingerprint,
        ):
            raise SourceSnapshotError(
                "fingerprint must be a "
                "SourceFingerprint."
            )

        if not isinstance(
            self.text,
            str,
        ):
            raise SourceSnapshotError(
                "text must be a string."
            )

        if (
            not isinstance(
                self.encoding,
                str,
            )
            or not self.encoding.strip()
        ):
            raise SourceSnapshotError(
                "encoding must be a "
                "non-empty string."
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
            raise SourceSnapshotError(
                "content_sha256 must be "
                "a SHA-256 hex digest."
            )

        for name, value in (
            (
                "byte_count",
                self.byte_count,
            ),
            (
                "character_count",
                self.character_count,
            ),
            (
                "line_count",
                self.line_count,
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
                raise SourceSnapshotError(
                    f"{name} must be a "
                    "non-negative integer."
                )

        if (
            self.character_count
            != len(
                self.text
            )
        ):
            raise SourceSnapshotError(
                "character_count does not "
                "match snapshot text."
            )

        expected_lines = (
            len(
                self.text.splitlines()
            )
        )

        if (
            self.line_count
            != expected_lines
        ):
            raise SourceSnapshotError(
                "line_count does not match "
                "snapshot text."
            )


    @property
    def source(
        self,
    ):
        return self.fingerprint.source


    def inspect(
        self,
    ):
        return {
            "schema_version":
                self.schema_version,

            "source_id":
                self.source.source_id,

            "source_kind":
                self.source.source_kind,

            "locator":
                self.source.locator,

            "fingerprint_method":
                self.fingerprint.method,

            "encoding":
                self.encoding,

            "content_sha256":
                self.content_sha256,

            "byte_count":
                self.byte_count,

            "character_count":
                self.character_count,

            "line_count":
                self.line_count,
        }


class LocalSourceSnapshotReader:
    """
    Read one stable local-file snapshot.

    The reader verifies both metadata versioning
    and open-file identity before publishing
    content.

    It does not parse, target, cache, or send
    source content to a runtime.
    """


    def __init__(
        self,
        observer=None,
    ):
        if observer is None:
            observer = (
                LocalSourceObserver()
            )

        if not isinstance(
            observer,
            LocalSourceObserver,
        ):
            raise SourceSnapshotError(
                "observer must be a "
                "LocalSourceObserver."
            )

        self._observer = observer


    @staticmethod
    def _stat_signature(
        stat,
    ):
        return (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
        )


    @staticmethod
    def _fingerprint_matches_stat(
        fingerprint,
        stat,
    ):
        dependencies = (
            fingerprint.dependency_dict()
        )

        return (
            dependencies.get(
                "size"
            )
            == stat.st_size
            and dependencies.get(
                "mtime_ns"
            )
            == stat.st_mtime_ns
        )


    def _read_bytes(
        self,
        handle,
    ):
        return handle.read()


    def read(
        self,
        path: Union[
            str,
            Path,
        ],
        *,
        source_id: Optional[str] = None,
        display_name: Optional[str] = None,
        encoding: str = "utf-8",
    ) -> SourceContentSnapshot:

        if (
            not isinstance(
                encoding,
                str,
            )
            or not encoding.strip()
        ):
            raise SourceSnapshotError(
                "encoding must be a "
                "non-empty string."
            )

        try:
            before = (
                self._observer.observe(
                    path,
                    source_id=source_id,
                    display_name=display_name,
                )
            )

        except LocalSourceObservationError as exc:
            raise SourceSnapshotError(
                str(exc)
            ) from exc

        resolved = Path(
            before.source.locator
        )

        try:
            path_stat_before = (
                resolved.stat()
            )

        except OSError as exc:
            raise SourceSnapshotError(
                "Source metadata became "
                "unavailable before read."
            ) from exc

        if not self._fingerprint_matches_stat(
            before,
            path_stat_before,
        ):
            raise SourceChangedDuringReadError(
                "Source changed between "
                "observation and read."
            )

        try:
            with resolved.open(
                "rb"
            ) as handle:

                fd_stat_before = os.fstat(
                    handle.fileno()
                )

                if (
                    self._stat_signature(
                        path_stat_before
                    )
                    != self._stat_signature(
                        fd_stat_before
                    )
                ):
                    raise (
                        SourceChangedDuringReadError(
                            "Source identity changed "
                            "while opening."
                        )
                    )

                content = self._read_bytes(
                    handle
                )

                fd_stat_after = os.fstat(
                    handle.fileno()
                )

        except SourceChangedDuringReadError:
            raise

        except OSError as exc:
            raise SourceSnapshotError(
                "Source contents could "
                "not be read."
            ) from exc

        if not isinstance(
            content,
            bytes,
        ):
            raise SourceSnapshotError(
                "_read_bytes() must "
                "return bytes."
            )

        if (
            self._stat_signature(
                fd_stat_before
            )
            != self._stat_signature(
                fd_stat_after
            )
        ):
            raise SourceChangedDuringReadError(
                "Source changed while "
                "contents were being read."
            )

        if (
            len(
                content
            )
            != fd_stat_after.st_size
        ):
            raise SourceChangedDuringReadError(
                "Read byte count does not "
                "match stable source size."
            )

        try:
            path_stat_after = (
                resolved.stat()
            )

        except OSError as exc:
            raise SourceChangedDuringReadError(
                "Source disappeared or changed "
                "after read."
            ) from exc

        if (
            self._stat_signature(
                fd_stat_after
            )
            != self._stat_signature(
                path_stat_after
            )
        ):
            raise SourceChangedDuringReadError(
                "Source path changed while "
                "snapshot was being created."
            )

        try:
            after = (
                self._observer.observe(
                    resolved,
                    source_id=(
                        before.source.source_id
                    ),
                    display_name=(
                        before.source.display_name
                    ),
                )
            )

        except LocalSourceObservationError as exc:
            raise SourceChangedDuringReadError(
                "Source became unavailable "
                "after read."
            ) from exc

        if after != before:
            raise SourceChangedDuringReadError(
                "Source fingerprint changed "
                "during read."
            )

        if not self._fingerprint_matches_stat(
            after,
            path_stat_after,
        ):
            raise SourceChangedDuringReadError(
                "Final source observation "
                "does not match file metadata."
            )

        try:
            text = content.decode(
                encoding,
                errors="strict",
            )

        except (
            LookupError,
            UnicodeDecodeError,
        ) as exc:
            raise SourceSnapshotError(
                "Source content could not "
                f"be decoded as {encoding!r}."
            ) from exc

        return SourceContentSnapshot(
            fingerprint=after,
            text=text,
            encoding=encoding,
            content_sha256=(
                sha256(
                    content
                ).hexdigest()
            ),
            byte_count=len(
                content
            ),
            character_count=len(
                text
            ),
            line_count=len(
                text.splitlines()
            ),
        )
