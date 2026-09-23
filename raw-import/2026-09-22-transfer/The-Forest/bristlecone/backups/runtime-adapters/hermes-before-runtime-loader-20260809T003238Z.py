"""Hermes runtime adapter for The Forest.

Hermes-specific behavior will be moved here incrementally from
TaskSessionManager.  This initial file deliberately contains no live
Hermes operations yet.
"""

from __future__ import annotations

from .base import BaseRuntimeAdapter


class HermesRuntimeAdapter(BaseRuntimeAdapter):
    """Translate Forest runtime requests into Hermes operations."""

    adapter_name = "hermes"

    def verify_runtime(self, state):
        raise NotImplementedError(
            "Hermes runtime verification has not been extracted yet."
        )

    def get_active_toolsets(self, state):
        raise NotImplementedError(
            "Hermes toolset inspection has not been extracted yet."
        )

    def begin_temporary_toolsets(
        self,
        runtime_toolsets,
        state,
    ):
        raise NotImplementedError(
            "Hermes temporary toolset activation has not been "
            "extracted yet."
        )

    def restore_temporary_toolsets(
        self,
        transaction,
        state,
    ):
        raise NotImplementedError(
            "Hermes temporary toolset restoration has not been "
            "extracted yet."
        )

    def build_skill_overlay(
        self,
        runtime_skills,
        task_id=None,
    ):
        raise NotImplementedError(
            "Hermes Skill overlay generation has not been extracted yet."
        )
