"""Compatibility facade for Operational Learning.

The authoritative implementation now lives in
learning.foundation.

This module preserves the earlier public import names while
preventing a second independent learning store from existing.
"""

from .foundation import (
    FOREST_RECORD_SCHEMA_VERSION,
    LEGACY_LESSON_KINDS,
    RECORD_STATUSES,
    SCOPE_TYPES,
    ForestLearningError,
    ForestLearningRecord,
    ForestLearningStore,
    RecordRevisionConflict,
)


OPERATIONAL_LEARNING_SCHEMA_VERSION = (
    FOREST_RECORD_SCHEMA_VERSION
)

LESSON_KINDS = LEGACY_LESSON_KINDS
LESSON_SCOPES = SCOPE_TYPES
LESSON_STATUSES = RECORD_STATUSES

OperationalLearningError = (
    ForestLearningError
)

OperationalLesson = (
    ForestLearningRecord
)

OperationalLearningStore = (
    ForestLearningStore
)


__all__ = [
    "OPERATIONAL_LEARNING_SCHEMA_VERSION",
    "LESSON_KINDS",
    "LESSON_SCOPES",
    "LESSON_STATUSES",
    "OperationalLearningError",
    "OperationalLesson",
    "OperationalLearningStore",
    "RecordRevisionConflict",
]
