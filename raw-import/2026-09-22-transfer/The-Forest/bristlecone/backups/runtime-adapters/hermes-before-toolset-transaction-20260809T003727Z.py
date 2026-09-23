"""Hermes runtime adapter for The Forest."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .base import (
    BaseRuntimeAdapter,
    RuntimeAdapterError,
)


class HermesRuntimeAdapter(BaseRuntimeAdapter):
    """Translate Forest runtime requests into Hermes operations."""

    adapter_name = "hermes"

    def __init__(
        self,
        profile_name="bristlecone",
        profile_home=None,
        repo=None,
    ):
        self.profile_name = str(profile_name)

        self.profile_home = (
            Path(profile_home)
            if profile_home is not None
            else (
                Path.home()
                / ".hermes"
                / "profiles"
                / self.profile_name
            )
        )

        self.repo = (
            Path(repo)
            if repo is not None
            else (
                Path.home()
                / ".hermes"
                / "hermes-agent"
            )
        )

    @staticmethod
    def _unique(items):
        result = []
        seen = set()

        for item in items:
            if item in seen:
                continue

            seen.add(item)
            result.append(item)

        return result

    def _load_toolset_runtime(self, state):
        runtime = state.get("runtime", {})

        if not isinstance(runtime, dict):
            raise RuntimeAdapterError(
                "state.runtime must be a mapping."
            )

        adapter_name = runtime.get("adapter")
        platform = runtime.get("platform")

        if adapter_name != self.adapter_name:
            raise RuntimeAdapterError(
                "Hermes runtime operations require "
                "the hermes runtime adapter."
            )

        if platform != "api_server":
            raise RuntimeAdapterError(
                "Refusing Hermes runtime operation because "
                f"runtime platform is {platform!r}, not "
                "'api_server'."
            )

        expected_home = self.profile_home

        hermes_home = os.environ.get(
            "HERMES_HOME"
        )

        if not hermes_home:
            raise RuntimeAdapterError(
                "HERMES_HOME is not set."
            )

        if (
            Path(hermes_home).resolve()
            != expected_home.resolve()
        ):
            raise RuntimeAdapterError(
                "HERMES_HOME does not point to the "
                f"{self.profile_name!r} Hermes profile."
            )

        repo_text = str(self.repo)

        if repo_text not in sys.path:
            sys.path.insert(
                0,
                repo_text,
            )

        try:
            from hermes_cli.config import (
                load_config,
                save_config,
            )

            from hermes_cli.tools_config import (
                _save_platform_tools,
                CONFIGURABLE_TOOLSETS,
            )

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes toolset configuration helpers "
                f"could not be imported: {exc}"
            ) from exc

        configurable = {
            str(key)
            for key, _, _
            in CONFIGURABLE_TOOLSETS
        }

        return {
            "platform": platform,
            "home": expected_home,
            "config_path":
                expected_home / "config.yaml",
            "load_config": load_config,
            "save_config": save_config,
            "save_platform_tools":
                _save_platform_tools,
            "configurable": configurable,
        }

    def _configurable_toolsets(
        self,
        runtime_api,
        config,
    ):
        raw = (
            config
            .get("platform_toolsets", {})
            .get(
                runtime_api["platform"],
                [],
            )
        )

        if not isinstance(raw, list):
            raise RuntimeAdapterError(
                "Hermes platform toolsets "
                "must be a list."
            )

        return self._unique(
            [
                str(item)
                for item in raw
                if str(item)
                in runtime_api["configurable"]
            ]
        )

    def verify_runtime(self, state):
        runtime_api = (
            self._load_toolset_runtime(state)
        )

        config = runtime_api[
            "load_config"
        ]()

        active = self._configurable_toolsets(
            runtime_api,
            config,
        )

        return {
            "adapter": self.adapter_name,
            "platform":
                runtime_api["platform"],
            "profile_name":
                self.profile_name,
            "profile_home":
                str(runtime_api["home"]),
            "config_path":
                str(runtime_api["config_path"]),
            "configurable_count":
                len(
                    runtime_api[
                        "configurable"
                    ]
                ),
            "active_toolsets":
                active,
        }

    def get_active_toolsets(self, state):
        runtime_api = (
            self._load_toolset_runtime(state)
        )

        config = runtime_api[
            "load_config"
        ]()

        return self._configurable_toolsets(
            runtime_api,
            config,
        )

    def begin_temporary_toolsets(
        self,
        runtime_toolsets,
        state,
    ):
        raise NotImplementedError(
            "Hermes temporary toolset activation "
            "has not been extracted yet."
        )

    def restore_temporary_toolsets(
        self,
        transaction,
        state,
    ):
        raise NotImplementedError(
            "Hermes temporary toolset restoration "
            "has not been extracted yet."
        )

    def build_skill_overlay(
        self,
        runtime_skills,
        task_id=None,
    ):
        raise NotImplementedError(
            "Hermes Skill overlay generation "
            "has not been extracted yet."
        )
