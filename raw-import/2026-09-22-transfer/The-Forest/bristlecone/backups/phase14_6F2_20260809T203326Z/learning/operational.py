"""Durable Operational Learning for Project Forest.

Operational Learning is authoritative Forest state.

Caches, indexes, embeddings, and prepared lesson context
must remain derived from this durable store.

The current source-of-truth format is append-only JSONL.
Each line is one immutable lesson revision.
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
    replace,
)
from datetime import (
    datetime,
    timezone,
)
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    Tuple,
)
import fcntl
import json
import os
import uuid


OPERATIONAL_LEARNING_SCHEMA_VERSION = 1


LESSON_KINDS = frozenset(
    {
        "mistake",
        "success",
        "user-correction",
        "environment",
        "constraint",
        "procedure",
        "observation",
    }
)


LESSON_SCOPES = frozenset(
    {
        "general",
        "workshop",
        "tree",
        "clone",
    }
)


LESSON_STATUSES = frozenset(
    {
        "active",
        "superseded",
        "retired",
    }
)


class OperationalLearningError(
    RuntimeError
):
    """Raised when durable learning state is invalid."""


def _utc_now():
    return (
        datetime.now(
            timezone.utc
        )
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    )


def _validate_timestamp(
    value,
):
    if not isinstance(
        value,
        str,
    ):
        raise OperationalLearningError(
            "recorded_at must be a string."
        )

    text = value.strip()

    if not text:
        raise OperationalLearningError(
            "recorded_at cannot be empty."
        )

    try:
        parsed = datetime.fromisoformat(
            text.replace(
                "Z",
                "+00:00",
            )
        )

    except ValueError as exc:
        raise OperationalLearningError(
            "recorded_at must be ISO-8601."
        ) from exc

    if parsed.tzinfo is None:
        raise OperationalLearningError(
            "recorded_at must include timezone."
        )


def _string_tuple(
    name,
    values,
):
    if values is None:
        return ()

    if not isinstance(
        values,
        (
            list,
            tuple,
        ),
    ):
        raise OperationalLearningError(
            f"{name} must be a list or tuple."
        )

    result = []

    for value in values:
        if not isinstance(
            value,
            str,
        ):
            raise OperationalLearningError(
                f"{name} entries must be strings."
            )

        value = value.strip()

        if not value:
            raise OperationalLearningError(
                f"{name} entries cannot be empty."
            )

        result.append(
            value
        )

    return tuple(
        result
    )


@dataclass(
    frozen=True
)
class OperationalLesson:
    """One immutable revision of a learned lesson."""

    schema_version: int
    lesson_id: str
    revision: int
    recorded_at: str

    lesson_kind: str

    scope_type: str
    scope_id: Optional[str]

    summary: str
    detail: str

    confidence: float
    status: str

    learned_by_tree: Optional[str]
    learned_by_clone: Optional[str]

    source_refs: Tuple[str, ...]
    tags: Tuple[str, ...]

    metadata: Dict[str, Any]


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != OPERATIONAL_LEARNING_SCHEMA_VERSION
        ):
            raise OperationalLearningError(
                "Unsupported Operational Learning "
                "schema version: "
                f"{self.schema_version}"
            )

        if not isinstance(
            self.lesson_id,
            str,
        ) or not self.lesson_id.strip():
            raise OperationalLearningError(
                "lesson_id cannot be empty."
            )

        if (
            not isinstance(
                self.revision,
                int,
            )
            or isinstance(
                self.revision,
                bool,
            )
            or self.revision < 1
        ):
            raise OperationalLearningError(
                "revision must be an integer >= 1."
            )

        _validate_timestamp(
            self.recorded_at
        )

        if (
            self.lesson_kind
            not in LESSON_KINDS
        ):
            raise OperationalLearningError(
                "Unknown lesson_kind: "
                f"{self.lesson_kind!r}"
            )

        if (
            self.scope_type
            not in LESSON_SCOPES
        ):
            raise OperationalLearningError(
                "Unknown scope_type: "
                f"{self.scope_type!r}"
            )

        if self.scope_type == "general":
            if self.scope_id is not None:
                raise OperationalLearningError(
                    "General lessons must not "
                    "have scope_id."
                )

        else:
            if (
                not isinstance(
                    self.scope_id,
                    str,
                )
                or not self.scope_id.strip()
            ):
                raise OperationalLearningError(
                    f"{self.scope_type} lessons "
                    "require scope_id."
                )

        if (
            not isinstance(
                self.summary,
                str,
            )
            or not self.summary.strip()
        ):
            raise OperationalLearningError(
                "summary cannot be empty."
            )

        if not isinstance(
            self.detail,
            str,
        ):
            raise OperationalLearningError(
                "detail must be a string."
            )

        if (
            isinstance(
                self.confidence,
                bool,
            )
            or not isinstance(
                self.confidence,
                (
                    int,
                    float,
                ),
            )
            or not (
                0.0
                <= float(
                    self.confidence
                )
                <= 1.0
            )
        ):
            raise OperationalLearningError(
                "confidence must be between "
                "0.0 and 1.0."
            )

        if (
            self.status
            not in LESSON_STATUSES
        ):
            raise OperationalLearningError(
                "Unknown lesson status: "
                f"{self.status!r}"
            )

        for name, value in (
            (
                "learned_by_tree",
                self.learned_by_tree,
            ),
            (
                "learned_by_clone",
                self.learned_by_clone,
            ),
        ):
            if (
                value is not None
                and (
                    not isinstance(
                        value,
                        str,
                    )
                    or not value.strip()
                )
            ):
                raise OperationalLearningError(
                    f"{name} must be a "
                    "non-empty string or None."
                )

        object.__setattr__(
            self,
            "source_refs",
            _string_tuple(
                "source_refs",
                self.source_refs,
            ),
        )

        object.__setattr__(
            self,
            "tags",
            _string_tuple(
                "tags",
                self.tags,
            ),
        )

        if not isinstance(
            self.metadata,
            dict,
        ):
            raise OperationalLearningError(
                "metadata must be a mapping."
            )

        # Fail early if metadata cannot be persisted
        # as portable JSON.
        try:
            json.dumps(
                self.metadata,
                ensure_ascii=False,
            )

        except (
            TypeError,
            ValueError,
        ) as exc:
            raise OperationalLearningError(
                "metadata must be JSON-serializable."
            ) from exc


    @classmethod
    def create(
        cls,
        *,
        summary,
        lesson_kind,
        scope_type="general",
        scope_id=None,
        detail="",
        confidence=1.0,
        learned_by_tree=None,
        learned_by_clone=None,
        source_refs=(),
        tags=(),
        metadata=None,
        lesson_id=None,
    ):
        """Create revision 1 of a lesson."""

        return cls(
            schema_version=(
                OPERATIONAL_LEARNING_SCHEMA_VERSION
            ),
            lesson_id=(
                lesson_id
                or (
                    "lesson-"
                    + uuid.uuid4().hex
                )
            ),
            revision=1,
            recorded_at=_utc_now(),
            lesson_kind=lesson_kind,
            scope_type=scope_type,
            scope_id=scope_id,
            summary=summary,
            detail=detail,
            confidence=float(
                confidence
            ),
            status="active",
            learned_by_tree=(
                learned_by_tree
            ),
            learned_by_clone=(
                learned_by_clone
            ),
            source_refs=tuple(
                source_refs
            ),
            tags=tuple(
                tags
            ),
            metadata=dict(
                metadata
                or {}
            ),
        )


    def revise(
        self,
        **changes,
    ):
        """Create the next immutable revision."""

        forbidden = {
            "schema_version",
            "lesson_id",
            "revision",
            "recorded_at",
        }

        unexpected = (
            forbidden
            & set(
                changes
            )
        )

        if unexpected:
            raise OperationalLearningError(
                "Revision cannot replace "
                "identity fields: "
                + ", ".join(
                    sorted(
                        unexpected
                    )
                )
            )

        if "source_refs" in changes:
            changes[
                "source_refs"
            ] = tuple(
                changes[
                    "source_refs"
                ]
            )

        if "tags" in changes:
            changes[
                "tags"
            ] = tuple(
                changes[
                    "tags"
                ]
            )

        if "metadata" in changes:
            changes[
                "metadata"
            ] = dict(
                changes[
                    "metadata"
                ]
            )

        return replace(
            self,
            revision=(
                self.revision
                + 1
            ),
            recorded_at=_utc_now(),
            **changes,
        )


    def to_dict(
        self,
    ):
        data = asdict(
            self
        )

        data[
            "source_refs"
        ] = list(
            self.source_refs
        )

        data[
            "tags"
        ] = list(
            self.tags
        )

        return data


    @classmethod
    def from_dict(
        cls,
        data,
    ):
        if not isinstance(
            data,
            dict,
        ):
            raise OperationalLearningError(
                "Lesson record must be a mapping."
            )

        expected = {
            "schema_version",
            "lesson_id",
            "revision",
            "recorded_at",
            "lesson_kind",
            "scope_type",
            "scope_id",
            "summary",
            "detail",
            "confidence",
            "status",
            "learned_by_tree",
            "learned_by_clone",
            "source_refs",
            "tags",
            "metadata",
        }

        actual = set(
            data
        )

        missing = (
            expected
            - actual
        )

        extra = (
            actual
            - expected
        )

        if missing:
            raise OperationalLearningError(
                "Lesson record missing fields: "
                + ", ".join(
                    sorted(
                        missing
                    )
                )
            )

        if extra:
            raise OperationalLearningError(
                "Lesson record contains unknown fields: "
                + ", ".join(
                    sorted(
                        extra
                    )
                )
            )

        return cls(
            schema_version=data[
                "schema_version"
            ],
            lesson_id=data[
                "lesson_id"
            ],
            revision=data[
                "revision"
            ],
            recorded_at=data[
                "recorded_at"
            ],
            lesson_kind=data[
                "lesson_kind"
            ],
            scope_type=data[
                "scope_type"
            ],
            scope_id=data[
                "scope_id"
            ],
            summary=data[
                "summary"
            ],
            detail=data[
                "detail"
            ],
            confidence=float(
                data[
                    "confidence"
                ]
            ),
            status=data[
                "status"
            ],
            learned_by_tree=data[
                "learned_by_tree"
            ],
            learned_by_clone=data[
                "learned_by_clone"
            ],
            source_refs=tuple(
                data[
                    "source_refs"
                ]
            ),
            tags=tuple(
                data[
                    "tags"
                ]
            ),
            metadata=dict(
                data[
                    "metadata"
                ]
            ),
        )


class OperationalLearningStore:
    """Append-only authoritative Operational Learning."""

    def __init__(
        self,
        forest_root,
    ):
        self.forest_root = Path(
            forest_root
        )

        self.directory = (
            self.forest_root
            / "learning"
            / "operational"
        )

        self.path = (
            self.directory
            / "lessons.jsonl"
        )

        self.lock_path = (
            self.directory
            / ".lessons.lock"
        )


    def _ensure_directory(
        self,
    ):
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
            mode=0o700,
        )


    def _locked_handle(
        self,
        exclusive,
    ):
        self._ensure_directory()

        handle = self.lock_path.open(
            "a+",
            encoding="utf-8",
        )

        try:
            os.chmod(
                self.lock_path,
                0o600,
            )

            fcntl.flock(
                handle.fileno(),
                (
                    fcntl.LOCK_EX
                    if exclusive
                    else fcntl.LOCK_SH
                ),
            )

        except Exception:
            handle.close()
            raise

        return handle


    def _read_all_unlocked(
        self,
    ):
        if not self.path.exists():
            return []

        lessons = []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as handle:
            for line_number, line in enumerate(
                handle,
                start=1,
            ):
                text = line.strip()

                if not text:
                    continue

                try:
                    raw = json.loads(
                        text
                    )

                except json.JSONDecodeError as exc:
                    raise OperationalLearningError(
                        "Invalid Operational Learning "
                        "JSON at line "
                        f"{line_number}."
                    ) from exc

                try:
                    lesson = (
                        OperationalLesson
                        .from_dict(
                            raw
                        )
                    )

                except OperationalLearningError as exc:
                    raise OperationalLearningError(
                        "Invalid Operational Learning "
                        "record at line "
                        f"{line_number}: {exc}"
                    ) from exc

                lessons.append(
                    lesson
                )

        return lessons


    def all_revisions(
        self,
    ):
        """Return every immutable stored revision."""

        lock = self._locked_handle(
            exclusive=False
        )

        try:
            return tuple(
                self._read_all_unlocked()
            )

        finally:
            fcntl.flock(
                lock.fileno(),
                fcntl.LOCK_UN,
            )

            lock.close()


    def latest(
        self,
    ):
        """Return current/latest revision of each lesson."""

        revisions = self.all_revisions()

        latest = {}

        for lesson in revisions:
            existing = latest.get(
                lesson.lesson_id
            )

            if (
                existing is None
                or lesson.revision
                > existing.revision
            ):
                latest[
                    lesson.lesson_id
                ] = lesson

        return tuple(
            latest[
                lesson_id
            ]
            for lesson_id
            in sorted(
                latest
            )
        )


    def get(
        self,
        lesson_id,
    ):
        """Return the latest revision for one lesson."""

        if (
            not isinstance(
                lesson_id,
                str,
            )
            or not lesson_id.strip()
        ):
            raise OperationalLearningError(
                "lesson_id cannot be empty."
            )

        result = None

        for lesson in self.all_revisions():
            if (
                lesson.lesson_id
                != lesson_id
            ):
                continue

            if (
                result is None
                or lesson.revision
                > result.revision
            ):
                result = lesson

        return result


    def append(
        self,
        lesson,
    ):
        """Durably append exactly one valid revision."""

        if not isinstance(
            lesson,
            OperationalLesson,
        ):
            raise OperationalLearningError(
                "append() requires OperationalLesson."
            )

        lock = self._locked_handle(
            exclusive=True
        )

        try:
            revisions = (
                self._read_all_unlocked()
            )

            previous = None

            for candidate in revisions:
                if (
                    candidate.lesson_id
                    != lesson.lesson_id
                ):
                    continue

                if (
                    previous is None
                    or candidate.revision
                    > previous.revision
                ):
                    previous = candidate

            if previous is None:
                expected_revision = 1

            else:
                expected_revision = (
                    previous.revision
                    + 1
                )

            if (
                lesson.revision
                != expected_revision
            ):
                raise OperationalLearningError(
                    "Lesson revision conflict for "
                    f"{lesson.lesson_id!r}: "
                    f"expected {expected_revision}, "
                    f"received {lesson.revision}."
                )

            encoded = (
                json.dumps(
                    lesson.to_dict(),
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            ).encode(
                "utf-8"
            )

            fd = os.open(
                self.path,
                (
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_APPEND
                ),
                0o600,
            )

            try:
                os.write(
                    fd,
                    encoded,
                )

                os.fsync(
                    fd
                )

            finally:
                os.close(
                    fd
                )

            os.chmod(
                self.path,
                0o600,
            )

        finally:
            fcntl.flock(
                lock.fileno(),
                fcntl.LOCK_UN,
            )

            lock.close()

        return lesson
