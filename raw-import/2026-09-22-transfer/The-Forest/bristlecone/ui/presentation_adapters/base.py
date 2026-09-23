"""Forest window-presentation adapter interface.

The core presentation contract describes what a Forest surface
wants.

Adapters describe what the current environment can actually do.

The adapter layer must never change the semantics of the Forest
Tool being presented.
"""

from dataclasses import dataclass
from typing import Tuple
import os
import sys


@dataclass(frozen=True)
class PresentationEnvironment:
    """Portable facts about the current graphical environment."""

    platform: str
    session_type: str
    desktop: str
    display_available: bool
    wayland_display_available: bool


    def to_mapping(self):
        return {
            "platform":
                self.platform,

            "session_type":
                self.session_type,

            "desktop":
                self.desktop,

            "display_available":
                self.display_available,

            "wayland_display_available":
                self.wayland_display_available,
        }


def detect_presentation_environment():
    """Inspect generic environment facts only.

    This deliberately does not decide that a particular
    window-manager, compositor, or operating-system integration
    is supported.
    """

    session_type = (
        os.environ
        .get(
            "XDG_SESSION_TYPE",
            "unknown",
        )
        .strip()
        .lower()
        or "unknown"
    )

    desktop = (
        os.environ
        .get(
            "XDG_CURRENT_DESKTOP",
            "",
        )
        .strip()
        or
        os.environ
        .get(
            "DESKTOP_SESSION",
            "",
        )
        .strip()
        or
        "unknown"
    )

    return PresentationEnvironment(
        platform=sys.platform,

        session_type=session_type,

        desktop=desktop,

        display_available=bool(
            os.environ.get(
                "DISPLAY"
            )
        ),

        wayland_display_available=bool(
            os.environ.get(
                "WAYLAND_DISPLAY"
            )
        ),
    )


@dataclass(frozen=True)
class PresentationPlan:
    """Negotiated presentation behavior for one surface.

    applied_in_process:
        Features this adapter can safely apply directly.

    deferred:
        Portable requests requiring a richer platform adapter.

    unsupported:
        Requests known to be unavailable.

    Blocking is intentionally absent. Presentation degradation
    may be reported, but it must not prevent the Forest Tool
    from opening.
    """

    adapter_id: str
    environment: PresentationEnvironment

    applied_in_process: Tuple[str, ...]
    deferred: Tuple[str, ...]
    unsupported: Tuple[str, ...]


    @property
    def degraded(self):
        return bool(
            self.deferred
            or self.unsupported
        )


    @property
    def safe_to_open(self):
        # Architectural invariant:
        # presentation limitations never disable the Tool.
        return True


    def to_mapping(self):
        return {
            "adapter_id":
                self.adapter_id,

            "environment":
                self.environment.to_mapping(),

            "applied_in_process":
                list(
                    self.applied_in_process
                ),

            "deferred":
                list(
                    self.deferred
                ),

            "unsupported":
                list(
                    self.unsupported
                ),

            "degraded":
                self.degraded,

            "safe_to_open":
                self.safe_to_open,
        }


class WindowPresentationAdapter:
    """Base interface for Forest presentation adapters."""

    adapter_id = "abstract"


    def environment(self):
        return (
            detect_presentation_environment()
        )


    def plan(
        self,
        request,
    ):
        raise NotImplementedError


    def prepare_window(
        self,
        window,
        request,
    ):
        """Apply supported in-process window properties.

        Platform adapters may override this, but must preserve
        safe fallback behavior.
        """

        raise NotImplementedError
