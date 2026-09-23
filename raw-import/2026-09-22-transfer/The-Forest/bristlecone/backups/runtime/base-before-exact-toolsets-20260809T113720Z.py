"""Runtime-independent Forest adapter contract."""

from __future__ import annotations

from abc import ABC, abstractmethod


class RuntimeAdapterError(RuntimeError):
    """Raised when a runtime adapter operation fails.

    Optional structured metadata lets Forest ask the
    adapter about failure meaning without parsing
    runtime-specific error strings itself.
    """

    def __init__(
        self,
        message,
        *,
        status_code=None,
        error_code=None,
        method=None,
        path=None,
    ):
        super().__init__(message)

        self.status_code = status_code
        self.error_code = error_code
        self.method = method
        self.path = path


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

    def is_stale_session_error(
        self,
        exc,
    ):
        """Return whether an error means a runtime session is stale.

        Runtime-specific adapters may override this.
        The generic/default answer is deliberately False.
        """

        return False

    @abstractmethod
    def end_session(
        self,
        session_id,
        state,
    ):
        """End or clean up a runtime-owned session."""
