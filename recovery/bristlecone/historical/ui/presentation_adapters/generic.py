"""Generic GTK fallback presentation adapter."""

from .base import (
    PresentationPlan,
    WindowPresentationAdapter,
)


class GenericGtkPresentationAdapter(
    WindowPresentationAdapter
):
    """Safe fallback adapter.

    Handles only properties that belong naturally to the GTK
    surface itself.

    Desktop/window-manager behavior is deferred for a richer
    adapter when one exists.
    """

    adapter_id = "gtk-generic"


    def plan(
        self,
        request,
    ):
        applied = [
            "application-identity",
            "decorated",
            "resizable",
        ]

        deferred = []

        if (
            request.placement_policy
            != "system"
        ):
            deferred.append(
                "placement:"
                + request.placement_policy
            )

        if (
            request.floating_policy
            != "system"
        ):
            deferred.append(
                "floating:"
                + request.floating_policy
            )

        if (
            request.raise_policy
            != "system"
        ):
            deferred.append(
                "raise:"
                + request.raise_policy
            )

        if request.remember_position:
            deferred.append(
                "remember-position"
            )

        if request.keep_visible:
            deferred.append(
                "keep-visible"
            )

        if request.opacity is not None:
            deferred.append(
                "opacity"
            )

        return PresentationPlan(
            adapter_id=self.adapter_id,

            environment=(
                self.environment()
            ),

            applied_in_process=tuple(
                applied
            ),

            deferred=tuple(
                deferred
            ),

            unsupported=(),
        )


    def prepare_window(
        self,
        window,
        request,
    ):
        """Apply only portable GTK-owned properties."""

        applied = []

        setter = getattr(
            window,
            "set_decorated",
            None,
        )

        if callable(setter):
            setter(
                request.decorated
            )

            applied.append(
                "decorated"
            )

        setter = getattr(
            window,
            "set_resizable",
            None,
        )

        if callable(setter):
            setter(
                request.resizable
            )

            applied.append(
                "resizable"
            )

        return tuple(
            applied
        )
