"""Forest runtime-adapter selection.

This module chooses a runtime adapter from Forest state.
Runtime-specific implementation stays inside each adapter.
"""

from __future__ import annotations

import os
from pathlib import Path

from .base import RuntimeAdapterError


def create_runtime_adapter(
    state,
    forest_root=None,
):
    """Create the adapter selected by state.runtime."""

    runtime = state.get(
        "runtime",
        {},
    )

    if not isinstance(
        runtime,
        dict,
    ):
        raise RuntimeAdapterError(
            "state.runtime must be a mapping."
        )

    adapter_name = runtime.get(
        "adapter"
    )

    if not adapter_name:
        raise RuntimeAdapterError(
            "state.runtime.adapter is not configured."
        )

    adapter_name = str(
        adapter_name
    )

    if adapter_name == "hermes":
        from .hermes import (
            HermesRuntimeAdapter,
        )

        profile_name = (
            runtime.get("profile")
            or runtime.get("profile_name")
        )

        if not profile_name:
            hermes_home = os.environ.get(
                "HERMES_HOME"
            )

            if hermes_home:
                profile_name = (
                    Path(hermes_home)
                    .expanduser()
                    .name
                )

        if not profile_name:
            raise RuntimeAdapterError(
                "Hermes runtime is configured, but "
                "the profile could not be determined "
                "from Forest state or HERMES_HOME."
            )

        return HermesRuntimeAdapter(
            profile_name=str(
                profile_name
            ),
            forest_root=forest_root,
        )

    raise RuntimeAdapterError(
        "No Forest runtime adapter is registered "
        f"for {adapter_name!r}."
    )
