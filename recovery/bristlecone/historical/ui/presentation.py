"""Platform-neutral Forest window presentation contracts.

This module describes what a Forest surface WANTS.

It does not implement a desktop environment, compositor,
window manager, operating system, or Qubes-specific policy.

Platform adapters may satisfy, partially satisfy, or safely
degrade these requests.

Failure to satisfy presentation preferences must never prevent
the underlying Forest feature from functioning.
"""

from dataclasses import dataclass
from typing import Optional


PLACEMENT_POLICIES = (
    "system",
    "focused-window",
    "pointer",
    "screen-center",
    "remember",
    "fixed",
)


PREFERENCE_POLICIES = (
    "system",
    "preferred",
    "required",
    "disabled",
)


@dataclass(frozen=True)
class WindowPresentationRequest:
    """Portable presentation intent for one Forest surface."""

    surface_id: str
    application_id: str
    role: str

    placement_policy: str = "system"

    floating_policy: str = "system"
    raise_policy: str = "system"

    remember_position: bool = False
    keep_visible: bool = True

    decorated: bool = True
    resizable: bool = True

    opacity: Optional[float] = None


    def __post_init__(self):
        if not self.surface_id:
            raise ValueError(
                "surface_id cannot be empty"
            )

        if not self.application_id:
            raise ValueError(
                "application_id cannot be empty"
            )

        if self.placement_policy not in (
            PLACEMENT_POLICIES
        ):
            raise ValueError(
                "Unsupported placement policy: "
                + str(
                    self.placement_policy
                )
            )

        if self.floating_policy not in (
            PREFERENCE_POLICIES
        ):
            raise ValueError(
                "Unsupported floating policy: "
                + str(
                    self.floating_policy
                )
            )

        if self.raise_policy not in (
            PREFERENCE_POLICIES
        ):
            raise ValueError(
                "Unsupported raise policy: "
                + str(
                    self.raise_policy
                )
            )

        if self.opacity is not None:
            if not (
                0.0
                < self.opacity
                <= 1.0
            ):
                raise ValueError(
                    "opacity must be greater "
                    "than 0 and at most 1"
                )


    def to_mapping(self):
        """Return a serialization-friendly representation."""

        return {
            "surface_id":
                self.surface_id,

            "application_id":
                self.application_id,

            "role":
                self.role,

            "placement_policy":
                self.placement_policy,

            "floating_policy":
                self.floating_policy,

            "raise_policy":
                self.raise_policy,

            "remember_position":
                self.remember_position,

            "keep_visible":
                self.keep_visible,

            "decorated":
                self.decorated,

            "resizable":
                self.resizable,

            "opacity":
                self.opacity,
        }


def reasoning_menu_presentation(
    menu_mode,
):
    """Return presentation intent for the Reasoning menu.

    Technical reasoning behavior is deliberately absent here.
    This function controls presentation only.
    """

    if menu_mode not in (
        "temporary",
        "baseline",
    ):
        raise ValueError(
            "menu_mode must be temporary or baseline"
        )

    return WindowPresentationRequest(
        surface_id=(
            "reasoning-menu"
        ),

        application_id=(
            "org.theforest.reasoningmenu"
        ),

        role="utility",

        # Preferred default for capable desktops.
        #
        # Platform adapters decide whether and how this can
        # actually be honored.
        placement_policy=(
            "focused-window"
        ),

        floating_policy=(
            "preferred"
        ),

        raise_policy=(
            "preferred"
        ),

        # This expresses user-experience intent.
        #
        # It does NOT mean the core Forest stores universal
        # X/Y desktop coordinates.
        remember_position=True,

        keep_visible=True,

        decorated=True,

        # Reasoning is a compact control surface rather than
        # a primary workspace.
        resizable=False,

        # Appearance remains unresolved.
        #
        # None means use normal system opacity.
        opacity=None,
    )
