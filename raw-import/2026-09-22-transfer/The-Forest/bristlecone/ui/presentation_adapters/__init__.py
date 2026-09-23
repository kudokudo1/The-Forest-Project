"""Forest window-presentation adapter registry."""

from .generic import (
    GenericGtkPresentationAdapter,
)


def select_presentation_adapter(
    request=None,
):
    """Select the best available presentation adapter.

    Phase 14.10E.2A.2 intentionally installs only the generic
    GTK fallback.

    Future platform adapters are registered here and selected
    before falling back to GTK-generic.
    """

    return (
        GenericGtkPresentationAdapter()
    )
