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

    @abstractmethod
    def create_session(
        self,
        state,
        task_id=None,
    ):
        """Create a runtime-owned session."""

    @abstractmethod
    def get_session(
        self,
        session_id,
        state,
    ):
        """Read a runtime-owned session."""

    @abstractmethod
    def send_turn(
        self,
        session_id,
        message,
        state,
        instructions=None,
    ):
        """Send one turn through a runtime-owned session."""

    @abstractmethod
    def end_session(
        self,
        session_id,
        state,
    ):
        """End or clean up a runtime-owned session."""
