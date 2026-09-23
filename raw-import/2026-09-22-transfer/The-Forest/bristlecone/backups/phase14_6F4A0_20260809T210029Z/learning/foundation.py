"""Durable Forest Learning and User Context.

This module is the authoritative persistence foundation for:

- Operational Learning
- User Preferences
- User Constraints
- User Corrections
- Current User Context

It deliberately does NOT perform semantic retrieval,
automatic learning, prompt injection, Context Trigger
routing, or Spirit/Cedar policy enforcement.

Those systems are built above this source of truth.

Storage is append-only JSONL. Each line is one immutable
record revision.

Derived caches and indexes may be deleted and rebuilt
without losing what the Forest learned or what the user
explicitly told it.
"""

from __future__ import annotations

from contextlib import contextmanager
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
from threading import RLock
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
)
import fcntl
import json
import os
import uuid


FOREST_RECORD_SCHEMA_VERSION = 1


RECORD_TYPES = frozenset(
    {
        "operational-learning",
        "user-preference",
        "user-constraint",
        "user-correction",
        "current-context",
    }
)


USER_CONTEXT_RECORD_TYPES = frozenset(
    {
        "user-preference",
        "user-constraint",
        "user-correction",
        "current-context",
    }
)


OPERATIONAL_KINDS = frozenset(
    {
        "mistake",
        "success",
        "procedure",
        "environment",
        "constraint",
        "observation",
    }
)


# Compatibility with the earlier learning model.
LEGACY_LESSON_KINDS = frozenset(
    set(OPERATIONAL_KINDS)
    | {
        "user-correction",
    }
)


SCOPE_TYPES = frozenset(
    {
        "general",
        "workshop",
        "tree",
        "clone",
    }
)


RECORD_STATUSES = frozenset(
    {
        "active",
        "superseded",
        "retired",
    }
)


RECORD_STRENGTHS = frozenset(
    {
        "normal",
        "strong",
        "hard",
    }
)


_PROCESS_LOCK = RLock()


class ForestLearningError(
    RuntimeError
):
    """Base error for durable Forest learning/context."""


class RecordRevisionConflict(
    ForestLearningError
):
    """Raised when concurrent revisions conflict."""


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
    name,
    value,
    *,
    allow_none=False,
):
    if value is None and allow_none:
        return

    if not isinstance(value, str):
        raise ForestLearningError(
            f"{name} must be a string."
        )

    text = value.strip()

    if not text:
        raise ForestLearningError(
            f"{name} cannot be empty."
        )

    try:
        parsed = datetime.fromisoformat(
            text.replace(
                "Z",
                "+00:00",
            )
        )

    except ValueError as exc:
        raise ForestLearningError(
            f"{name} must be ISO-8601."
        ) from exc

    if parsed.tzinfo is None:
        raise ForestLearningError(
            f"{name} must include timezone."
        )


def _optional_string(
    name,
    value,
):
    if value is None:
        return

    if (
        not isinstance(value, str)
        or not value.strip()
    ):
        raise ForestLearningError(
            f"{name} must be a non-empty "
            "string or None."
        )


def _string_tuple(
    name,
    values,
):
    if values is None:
        return ()

    if not isinstance(
        values,
        (list, tuple),
    ):
        raise ForestLearningError(
            f"{name} must be a list or tuple."
        )

    result = []

    for value in values:
        if (
            not isinstance(value, str)
            or not value.strip()
        ):
            raise ForestLearningError(
                f"{name} entries must be "
                "non-empty strings."
            )

        result.append(
            value.strip()
        )

    return tuple(result)


def _json_mapping(
    name,
    value,
):
    if value is None:
        return {}

    if not isinstance(value, dict):
        raise ForestLearningError(
            f"{name} must be a mapping."
        )

    result = dict(value)

    try:
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
        )

    except (
        TypeError,
        ValueError,
    ) as exc:
        raise ForestLearningError(
            f"{name} must be JSON-serializable."
        ) from exc

    return result


@dataclass(
    frozen=True
)
class ForestLearningRecord:
    """One immutable revision of learning/user context."""

    schema_version: int

    record_id: str
    revision: int
    recorded_at: str

    record_type: str
    operational_kind: Optional[str]

    scope_type: str
    scope_id: Optional[str]

    summary: str
    detail: str

    strength: str
    confidence: float
    status: str

    recorded_by_tree: Optional[str]
    recorded_by_clone: Optional[str]

    source_refs: Tuple[str, ...]
    routing_tags: Tuple[str, ...]
    tags: Tuple[str, ...]

    valid_until: Optional[str]

    # Future Spirit / Cedar enforcement hook.
    # This field stores metadata only in Phase 14.
    protection: Dict[str, Any]

    metadata: Dict[str, Any]

    # Positive only for committed User Context revisions.
    # Operational Learning does not advance this counter.
    user_context_generation: int = 0


    def __post_init__(
        self,
    ):
        if (
            self.schema_version
            != FOREST_RECORD_SCHEMA_VERSION
        ):
            raise ForestLearningError(
                "Unsupported schema version: "
                f"{self.schema_version}"
            )

        if (
            not isinstance(self.record_id, str)
            or not self.record_id.strip()
        ):
            raise ForestLearningError(
                "record_id cannot be empty."
            )

        if (
            isinstance(self.revision, bool)
            or not isinstance(self.revision, int)
            or self.revision < 1
        ):
            raise ForestLearningError(
                "revision must be an integer >= 1."
            )

        _validate_timestamp(
            "recorded_at",
            self.recorded_at,
        )

        _validate_timestamp(
            "valid_until",
            self.valid_until,
            allow_none=True,
        )

        if self.record_type not in RECORD_TYPES:
            raise ForestLearningError(
                "Unknown record_type: "
                f"{self.record_type!r}"
            )

        if (
            self.record_type
            == "operational-learning"
        ):
            if (
                self.operational_kind
                not in OPERATIONAL_KINDS
            ):
                raise ForestLearningError(
                    "Operational Learning requires "
                    "a valid operational_kind."
                )

        elif self.operational_kind is not None:
            raise ForestLearningError(
                "Only Operational Learning may "
                "set operational_kind."
            )

        if self.scope_type not in SCOPE_TYPES:
            raise ForestLearningError(
                "Unknown scope_type: "
                f"{self.scope_type!r}"
            )

        if self.scope_type == "general":
            if self.scope_id is not None:
                raise ForestLearningError(
                    "General records must not "
                    "have scope_id."
                )

        elif (
            not isinstance(self.scope_id, str)
            or not self.scope_id.strip()
        ):
            raise ForestLearningError(
                f"{self.scope_type} records "
                "require scope_id."
            )

        if (
            not isinstance(self.summary, str)
            or not self.summary.strip()
        ):
            raise ForestLearningError(
                "summary cannot be empty."
            )

        if not isinstance(self.detail, str):
            raise ForestLearningError(
                "detail must be a string."
            )

        if self.strength not in RECORD_STRENGTHS:
            raise ForestLearningError(
                "Unknown strength: "
                f"{self.strength!r}"
            )

        if (
            isinstance(self.confidence, bool)
            or not isinstance(
                self.confidence,
                (int, float),
            )
            or not (
                0.0
                <= float(self.confidence)
                <= 1.0
            )
        ):
            raise ForestLearningError(
                "confidence must be between "
                "0.0 and 1.0."
            )

        if self.status not in RECORD_STATUSES:
            raise ForestLearningError(
                "Unknown status: "
                f"{self.status!r}"
            )

        _optional_string(
            "recorded_by_tree",
            self.recorded_by_tree,
        )

        _optional_string(
            "recorded_by_clone",
            self.recorded_by_clone,
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
            "routing_tags",
            _string_tuple(
                "routing_tags",
                self.routing_tags,
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

        object.__setattr__(
            self,
            "protection",
            _json_mapping(
                "protection",
                self.protection,
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            _json_mapping(
                "metadata",
                self.metadata,
            ),
        )

        if (
            isinstance(
                self.user_context_generation,
                bool,
            )
            or not isinstance(
                self.user_context_generation,
                int,
            )
            or self.user_context_generation < 0
        ):
            raise ForestLearningError(
                "user_context_generation must "
                "be an integer >= 0."
            )


    @property
    def is_user_context(
        self,
    ):
        return (
            self.record_type
            in USER_CONTEXT_RECORD_TYPES
        )


    # --------------------------------------------------
    # Compatibility properties for the older
    # OperationalLesson API.
    # --------------------------------------------------

    @property
    def lesson_id(
        self,
    ):
        return self.record_id


    @property
    def lesson_kind(
        self,
    ):
        if (
            self.record_type
            == "operational-learning"
        ):
            return self.operational_kind

        if self.record_type == "user-correction":
            return "user-correction"

        return None


    @property
    def learned_by_tree(
        self,
    ):
        return self.recorded_by_tree


    @property
    def learned_by_clone(
        self,
    ):
        return self.recorded_by_clone


    @classmethod
    def create(
        cls,
        *,
        summary,
        record_type=None,
        operational_kind=None,

        # Legacy API aliases.
        lesson_kind=None,

        scope_type="general",
        scope_id=None,
        detail="",
        strength="normal",
        confidence=1.0,

        recorded_by_tree=None,
        recorded_by_clone=None,

        # Legacy API aliases.
        learned_by_tree=None,
        learned_by_clone=None,

        source_refs=(),
        routing_tags=(),
        tags=(),
        valid_until=None,
        protection=None,
        metadata=None,

        record_id=None,

        # Legacy API alias.
        lesson_id=None,
    ):
        """Create an uncommitted revision-one record."""

        if (
            record_id is not None
            and lesson_id is not None
            and record_id != lesson_id
        ):
            raise ForestLearningError(
                "record_id and lesson_id disagree."
            )

        final_id = (
            record_id
            or lesson_id
            or (
                "record-"
                + uuid.uuid4().hex
            )
        )

        if (
            recorded_by_tree is not None
            and learned_by_tree is not None
            and recorded_by_tree
            != learned_by_tree
        ):
            raise ForestLearningError(
                "recorded_by_tree and "
                "learned_by_tree disagree."
            )

        if (
            recorded_by_clone is not None
            and learned_by_clone is not None
            and recorded_by_clone
            != learned_by_clone
        ):
            raise ForestLearningError(
                "recorded_by_clone and "
                "learned_by_clone disagree."
            )

        final_tree = (
            recorded_by_tree
            if recorded_by_tree is not None
            else learned_by_tree
        )

        final_clone = (
            recorded_by_clone
            if recorded_by_clone is not None
            else learned_by_clone
        )

        if lesson_kind is not None:
            if lesson_kind not in LEGACY_LESSON_KINDS:
                raise ForestLearningError(
                    "Unknown legacy lesson_kind: "
                    f"{lesson_kind!r}"
                )

            if lesson_kind == "user-correction":
                inferred_record_type = (
                    "user-correction"
                )

                inferred_operational_kind = None

            else:
                inferred_record_type = (
                    "operational-learning"
                )

                inferred_operational_kind = (
                    lesson_kind
                )

            if (
                record_type is not None
                and record_type
                != inferred_record_type
            ):
                raise ForestLearningError(
                    "record_type conflicts with "
                    "lesson_kind."
                )

            if (
                operational_kind is not None
                and operational_kind
                != inferred_operational_kind
            ):
                raise ForestLearningError(
                    "operational_kind conflicts with "
                    "lesson_kind."
                )

            record_type = inferred_record_type
            operational_kind = (
                inferred_operational_kind
            )

        if record_type is None:
            if operational_kind is not None:
                record_type = (
                    "operational-learning"
                )

            else:
                raise ForestLearningError(
                    "record_type is required."
                )

        return cls(
            schema_version=(
                FOREST_RECORD_SCHEMA_VERSION
            ),
            record_id=final_id,
            revision=1,
            recorded_at=_utc_now(),
            record_type=record_type,
            operational_kind=operational_kind,
            scope_type=scope_type,
            scope_id=scope_id,
            summary=summary,
            detail=detail,
            strength=strength,
            confidence=float(confidence),
            status="active",
            recorded_by_tree=final_tree,
            recorded_by_clone=final_clone,
            source_refs=tuple(source_refs),
            routing_tags=tuple(routing_tags),
            tags=tuple(tags),
            valid_until=valid_until,
            protection=dict(
                protection
                or {}
            ),
            metadata=dict(
                metadata
                or {}
            ),
            user_context_generation=0,
        )


    def revise(
        self,
        **changes,
    ):
        """Create an uncommitted next revision."""

        # Legacy field aliases.
        aliases = {
            "learned_by_tree": "recorded_by_tree",
            "learned_by_clone": "recorded_by_clone",
        }

        for old_name, new_name in aliases.items():
            if old_name not in changes:
                continue

            if (
                new_name in changes
                and changes[new_name]
                != changes[old_name]
            ):
                raise ForestLearningError(
                    f"{old_name} conflicts with "
                    f"{new_name}."
                )

            changes[
                new_name
            ] = changes.pop(
                old_name
            )

        if "lesson_kind" in changes:
            raise ForestLearningError(
                "Record semantic type cannot be "
                "changed through lesson_kind."
            )

        forbidden = {
            "schema_version",
            "record_id",
            "lesson_id",
            "record_type",
            "operational_kind",
            "revision",
            "recorded_at",
            "user_context_generation",
        }

        invalid = (
            forbidden
            & set(changes)
        )

        if invalid:
            raise ForestLearningError(
                "Revision cannot replace immutable "
                "identity/type fields: "
                + ", ".join(
                    sorted(invalid)
                )
            )

        for tuple_field in (
            "source_refs",
            "routing_tags",
            "tags",
        ):
            if tuple_field in changes:
                changes[
                    tuple_field
                ] = tuple(
                    changes[tuple_field]
                )

        for mapping_field in (
            "protection",
            "metadata",
        ):
            if mapping_field in changes:
                changes[
                    mapping_field
                ] = dict(
                    changes[mapping_field]
                )

        return replace(
            self,
            revision=(
                self.revision
                + 1
            ),
            recorded_at=_utc_now(),
            user_context_generation=0,
            **changes,
        )


    def to_dict(
        self,
    ):
        data = asdict(self)

        for field in (
            "source_refs",
            "routing_tags",
            "tags",
        ):
            data[field] = list(
                data[field]
            )

        return data


    @classmethod
    def from_dict(
        cls,
        data,
    ):
        if not isinstance(data, dict):
            raise ForestLearningError(
                "Stored record must be a mapping."
            )

        expected = {
            "schema_version",
            "record_id",
            "revision",
            "recorded_at",
            "record_type",
            "operational_kind",
            "scope_type",
            "scope_id",
            "summary",
            "detail",
            "strength",
            "confidence",
            "status",
            "recorded_by_tree",
            "recorded_by_clone",
            "source_refs",
            "routing_tags",
            "tags",
            "valid_until",
            "protection",
            "metadata",
            "user_context_generation",
        }

        actual = set(data)

        missing = expected - actual
        extra = actual - expected

        if missing:
            raise ForestLearningError(
                "Stored record missing fields: "
                + ", ".join(
                    sorted(missing)
                )
            )

        if extra:
            raise ForestLearningError(
                "Stored record has unknown fields: "
                + ", ".join(
                    sorted(extra)
                )
            )

        return cls(
            schema_version=data[
                "schema_version"
            ],
            record_id=data[
                "record_id"
            ],
            revision=data[
                "revision"
            ],
            recorded_at=data[
                "recorded_at"
            ],
            record_type=data[
                "record_type"
            ],
            operational_kind=data[
                "operational_kind"
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
            strength=data[
                "strength"
            ],
            confidence=float(
                data["confidence"]
            ),
            status=data[
                "status"
            ],
            recorded_by_tree=data[
                "recorded_by_tree"
            ],
            recorded_by_clone=data[
                "recorded_by_clone"
            ],
            source_refs=tuple(
                data["source_refs"]
            ),
            routing_tags=tuple(
                data["routing_tags"]
            ),
            tags=tuple(
                data["tags"]
            ),
            valid_until=data[
                "valid_until"
            ],
            protection=dict(
                data["protection"]
            ),
            metadata=dict(
                data["metadata"]
            ),
            user_context_generation=data[
                "user_context_generation"
            ],
        )


class ForestLearningStore:
    """Append-only source of truth for learning/context."""

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
        )

        self.path = (
            self.directory
            / "records.jsonl"
        )

        self.lock_path = (
            self.directory
            / ".records.lock"
        )


    def _ensure_directory(
        self,
    ):
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
            mode=0o700,
        )


    @contextmanager
    def _locked(
        self,
        *,
        exclusive,
    ):
        """Coordinate threads and independent processes."""

        self._ensure_directory()

        with _PROCESS_LOCK:
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

                yield

            finally:
                try:
                    fcntl.flock(
                        handle.fileno(),
                        fcntl.LOCK_UN,
                    )

                finally:
                    handle.close()


    def _read_all_unlocked(
        self,
    ):
        if not self.path.exists():
            return []

        records = []

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
                    raw = json.loads(text)

                except json.JSONDecodeError as exc:
                    raise ForestLearningError(
                        "Invalid Forest learning JSON "
                        f"at line {line_number}."
                    ) from exc

                try:
                    record = (
                        ForestLearningRecord
                        .from_dict(raw)
                    )

                except ForestLearningError as exc:
                    raise ForestLearningError(
                        "Invalid Forest record at line "
                        f"{line_number}: {exc}"
                    ) from exc

                records.append(record)

        return records


    @staticmethod
    def _latest_map(
        records,
    ):
        latest = {}

        for record in records:
            previous = latest.get(
                record.record_id
            )

            if (
                previous is None
                or record.revision
                > previous.revision
            ):
                latest[
                    record.record_id
                ] = record

        return latest


    @staticmethod
    def _context_generation(
        records,
    ):
        return max(
            (
                record.user_context_generation
                for record in records
            ),
            default=0,
        )


    def all_revisions(
        self,
    ):
        with self._locked(
            exclusive=False
        ):
            return tuple(
                self._read_all_unlocked()
            )


    def latest(
        self,
    ):
        records = self.all_revisions()
        latest = self._latest_map(records)

        return tuple(
            latest[record_id]
            for record_id in sorted(latest)
        )


    def get(
        self,
        record_id,
    ):
        if (
            not isinstance(record_id, str)
            or not record_id.strip()
        ):
            raise ForestLearningError(
                "record_id cannot be empty."
            )

        with self._locked(
            exclusive=False
        ):
            records = (
                self._read_all_unlocked()
            )

            return (
                self._latest_map(records)
                .get(record_id)
            )


    def user_context_generation(
        self,
    ):
        with self._locked(
            exclusive=False
        ):
            return self._context_generation(
                self._read_all_unlocked()
            )


    def current_user_context(
        self,
    ):
        return tuple(
            record
            for record in self.latest()
            if (
                record.is_user_context
                and record.status == "active"
            )
        )


    def current_operational_learning(
        self,
    ):
        return tuple(
            record
            for record in self.latest()
            if (
                record.record_type
                == "operational-learning"
                and record.status == "active"
            )
        )


    def append(
        self,
        record,
    ):
        """Commit exactly one immutable revision."""

        if not isinstance(
            record,
            ForestLearningRecord,
        ):
            raise ForestLearningError(
                "append() requires "
                "ForestLearningRecord."
            )

        with self._locked(
            exclusive=True
        ):
            records = (
                self._read_all_unlocked()
            )

            latest = self._latest_map(
                records
            )

            previous = latest.get(
                record.record_id
            )

            if previous is None:
                expected_revision = 1

            else:
                expected_revision = (
                    previous.revision
                    + 1
                )

                if (
                    previous.record_type
                    != record.record_type
                ):
                    raise ForestLearningError(
                        "A record cannot change "
                        "semantic record_type."
                    )

            if (
                record.revision
                != expected_revision
            ):
                raise RecordRevisionConflict(
                    "Record revision conflict for "
                    f"{record.record_id!r}: "
                    f"expected {expected_revision}, "
                    f"received {record.revision}."
                )

            context_generation = (
                self._context_generation(records)
            )

            if record.is_user_context:
                committed = replace(
                    record,
                    user_context_generation=(
                        context_generation + 1
                    ),
                )

            else:
                committed = replace(
                    record,
                    user_context_generation=0,
                )

            encoded = (
                json.dumps(
                    committed.to_dict(),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")

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
                offset = 0

                while offset < len(encoded):
                    written = os.write(
                        fd,
                        encoded[offset:],
                    )

                    if written <= 0:
                        raise ForestLearningError(
                            "Durable record write "
                            "did not make progress."
                        )

                    offset += written

                os.fsync(fd)

            finally:
                os.close(fd)

            os.chmod(
                self.path,
                0o600,
            )

            return committed
