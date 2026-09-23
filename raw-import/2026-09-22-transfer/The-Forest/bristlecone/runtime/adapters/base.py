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


class RuntimeContinuityUnsupportedError(
    RuntimeAdapterError
):
    """Runtime cannot bootstrap a session from Forest continuity."""


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
    def apply_toolsets_exact(
        self,
        runtime_toolsets,
        state,
    ):
        """Set runtime toolsets to exactly the desired set.

        Return a transaction containing enough information
        to restore the prior runtime state.
        """

    @abstractmethod
    def restore_toolsets_exact(
        self,
        transaction,
        state,
    ):
        """Restore a prior exact-toolset transaction."""

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

    def create_session_with_continuity(
        self,
        state,
        continuity,
        task_id=None,
    ):
        """Create a runtime session from portable Forest continuity.

        This is an optional runtime capability.

        Adapters that can translate ModelFormContinuity into a
        newly created runtime-owned session should override this
        method.

        The default deliberately fails closed. A runtime that does
        not support continuity bootstrap must never silently create
        an empty session and discard Forest conversation history.
        """

        raise RuntimeContinuityUnsupportedError(
            "This runtime adapter does not support "
            "portable Forest continuity bootstrap."
        )


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
        reasoning_mode=None,
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
