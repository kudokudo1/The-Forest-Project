"""Runtime-independent Forest adapter contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class RuntimeAdapterError(RuntimeError):
    """Raised when a runtime adapter operation fails."""


class BaseRuntimeAdapter(ABC):
    """Minimum runtime contract used by The Forest.

    The Forest owns policy and lifecycle.
    Runtime adapters own runtime-specific execution details.
    """

    adapter_name: str = "base"

    @abstractmethod
    def verify_runtime(self, state):
        """Verify that this runtime is usable."""

    @abstractmethod
    def get_active_toolsets(self, state):
        """Return currently active runtime toolsets."""

    @abstractmethod
    def begin_temporary_toolsets(
        self,
        runtime_toolsets,
        state,
    ):
        """Temporarily activate runtime toolsets."""

    @abstractmethod
    def restore_temporary_toolsets(
        self,
        transaction,
        state,
    ):
        """Restore the runtime after temporary activation."""

    @abstractmethod
    def build_skill_overlay(
        self,
        runtime_skills,
        task_id=None,
    ):
        """Build runtime-specific Skill prompt content."""
