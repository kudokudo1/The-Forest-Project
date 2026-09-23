#!/usr/bin/env python3

from pathlib import Path
import sys
import hashlib
import copy
import uuid
import os
import tempfile
from datetime import datetime, timezone
import yaml


class TaskSessionError(RuntimeError):
    pass


class TaskSessionManager:
    """Forest-owned Task Session state resolver.

    V0 is deliberately read-only:
    - reads Forest active state
    - normalizes Task Session state
    - validates canonical Skill IDs
    - resolves runtime Skill IDs through the active adapter

    V0 does NOT:
    - write active.yaml
    - create Hermes sessions
    - call the Hermes API
    - generate Skill prompt overlays
    """

    def __init__(self, forest_root=None):
        if forest_root is None:
            forest_root = Path(__file__).resolve().parents[1]

        self.forest = Path(forest_root)
        self._skill_overlay_cache = {}
        self._temporary_skill_overlay_cache = {}
        self._overlay_build_count = 0
        self._temporary_overlay_build_count = 0
        self.state_file = self.forest / "state" / "active.yaml"
        self.registry_file = (
            self.forest / "capabilities" / "registry.yaml"
        )

    @staticmethod
    def _load_yaml(path):
        if not path.exists():
            raise TaskSessionError(
                f"Required Forest file does not exist: {path}"
            )

        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)

        if not isinstance(data, dict):
            raise TaskSessionError(
                f"Expected YAML mapping in: {path}"
            )

        return data

    @staticmethod
    def _unique(items):
        seen = set()
        result = []

        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)

        return result

    def _atomic_write_yaml(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                delete=False,
            ) as tmp:
                yaml.safe_dump(
                    data,
                    tmp,
                    sort_keys=False,
                )
                tmp.flush()
                os.fsync(tmp.fileno())
                tmp_path = Path(tmp.name)

            os.replace(tmp_path, path)

        except Exception:
            if tmp_path is not None and tmp_path.exists():
                tmp_path.unlink()
            raise

    def persist_state(self, state):
        if not isinstance(state, dict):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        # Validate Task Session structure before writing.
        self.normalize_task_session(state)
        self._atomic_write_yaml(self.state_file, state)
        return state

    def load_state(self):
        return self._load_yaml(self.state_file)

    def load_registry(self):
        return self._load_yaml(self.registry_file)

    def load_adapter(self, name):
        path = self.forest / "adapters" / f"{name}.yaml"
        return self._load_yaml(path)

    def normalize_task_session(self, state):
        raw = state.get("task_session")

        if raw is None:
            raw = {}

        if not isinstance(raw, dict):
            raise TaskSessionError(
                "state.task_session must be a mapping."
            )

        raw_skills = raw.get("task_sticky_skills", [])

        if raw_skills is None:
            raw_skills = []

        if not isinstance(raw_skills, list):
            raise TaskSessionError(
                "task_sticky_skills must be a list."
            )

        canonical_skills = []

        for item in raw_skills:
            if isinstance(item, str):
                canonical = item

            elif isinstance(item, dict):
                canonical = item.get("canonical_id")

                if not canonical:
                    raise TaskSessionError(
                        "Task-Sticky Skill mapping is missing "
                        "canonical_id."
                    )

            else:
                raise TaskSessionError(
                    "Each Task-Sticky Skill must be either "
                    "a canonical ID string or a mapping."
                )

            canonical_skills.append(str(canonical))

        temporary = raw.get("temporary_capabilities", [])

        if temporary is None:
            temporary = []

        if not isinstance(temporary, list):
            raise TaskSessionError(
                "temporary_capabilities must be a list."
            )

        return {
            "id": raw.get("id"),
            "status": raw.get("status", "inactive"),
            "started_at": raw.get("started_at"),
            "updated_at": raw.get("updated_at"),
            "task_sticky_skills": self._unique(
                canonical_skills
            ),
            "temporary_capabilities": self._unique(
                [str(item) for item in temporary]
            ),
        }

    def resolve_task_sticky_skills(self, state, task_session):
        runtime = state.get("runtime", {})

        if not isinstance(runtime, dict):
            raise TaskSessionError(
                "state.runtime must be a mapping."
            )

        adapter_name = runtime.get("adapter")

        if not adapter_name:
            raise TaskSessionError(
                "No runtime adapter is configured."
            )

        adapter = self.load_adapter(adapter_name)
        registry = self.load_registry()

        capabilities = registry.get("capabilities", {})
        skill_map = adapter.get("skills", {})
        unresolved_map = adapter.get("unresolved", {})

        resolved = []

        for canonical_id in task_session[
            "task_sticky_skills"
        ]:
            capability = capabilities.get(canonical_id)

            if not isinstance(capability, dict):
                raise TaskSessionError(
                    f"Unknown Forest capability: "
                    f"{canonical_id}"
                )

            if capability.get("kind") != "skill":
                raise TaskSessionError(
                    f"{canonical_id} is not registered "
                    "as a Skill."
                )

            mapping = skill_map.get(canonical_id)

            if not isinstance(mapping, dict):
                unresolved = unresolved_map.get(canonical_id)

                if isinstance(unresolved, dict):
                    reason = unresolved.get(
                        "reason",
                        "No runtime Skill mapping.",
                    )
                else:
                    reason = "No runtime Skill mapping."

                raise TaskSessionError(
                    f"Cannot resolve Skill "
                    f"{canonical_id}: {reason}"
                )

            runtime_id = mapping.get("target")

            if not runtime_id:
                raise TaskSessionError(
                    f"Adapter mapping for {canonical_id} "
                    "has no target."
                )

            resolved.append(
                {
                    "canonical_id": canonical_id,
                    "runtime_id": str(runtime_id),
                    "adapter": adapter_name,
                }
            )

        return resolved

    def authorize_temporary_capabilities(
        self,
        state,
        task_session,
    ):
        workshop_id = state.get("workshop")

        if not workshop_id:
            raise TaskSessionError(
                "No active Forest Workshop is configured."
            )

        workshop_file = (
            self.forest
            / "workshops"
            / f"{workshop_id}.yaml"
        )

        workshop = self._load_yaml(workshop_file)
        registry = self.load_registry()

        capabilities = registry.get("capabilities", {})
        general_ready = set(
            registry.get("general_ready", [])
        )
        workshop_core = set(
            workshop.get("core", [])
        )
        workshop_ready = set(
            workshop.get("ready", [])
        )

        result = {
            "authorized": [],
            "already_active": [],
            "workshop": str(workshop_id),
        }

        for canonical_id in task_session[
            "temporary_capabilities"
        ]:
            capability = capabilities.get(canonical_id)

            if not isinstance(capability, dict):
                raise TaskSessionError(
                    f"Unknown Forest capability: "
                    f"{canonical_id}"
                )

            if canonical_id in workshop_core:
                result["already_active"].append({
                    "canonical_id": canonical_id,
                    "source": "workshop_core",
                })
                continue

            if canonical_id in general_ready:
                result["authorized"].append({
                    "canonical_id": canonical_id,
                    "source": "general_ready",
                })
                continue

            if canonical_id in workshop_ready:
                result["authorized"].append({
                    "canonical_id": canonical_id,
                    "source": "workshop_ready",
                })
                continue

            raise TaskSessionError(
                f"Temporary capability {canonical_id} "
                f"is not authorized for Workshop "
                f"{workshop_id}."
            )

        return result

    def resolve_temporary_capabilities(
        self,
        state,
        task_session,
    ):
        runtime = state.get("runtime", {})

        if not isinstance(runtime, dict):
            raise TaskSessionError(
                "state.runtime must be a mapping."
            )

        adapter_name = runtime.get("adapter")

        if not adapter_name:
            raise TaskSessionError(
                "No runtime adapter is configured."
            )

        adapter = self.load_adapter(adapter_name)
        registry = self.load_registry()

        capabilities = registry.get("capabilities", {})
        capability_map = adapter.get("capabilities", {})
        skill_map = adapter.get("skills", {})
        unresolved_map = adapter.get("unresolved", {})

        resolved = {
            "all": [],
            "toolsets": [],
            "contexts": [],
            "skills": [],
            "capabilities": [],
        }

        bucket_for_kind = {
            "toolset": "toolsets",
            "context": "contexts",
            "skill": "skills",
            "capability": "capabilities",
        }

        for canonical_id in task_session[
            "temporary_capabilities"
        ]:
            capability = capabilities.get(canonical_id)

            if not isinstance(capability, dict):
                raise TaskSessionError(
                    f"Unknown Forest capability: "
                    f"{canonical_id}"
                )

            kind = capability.get("kind")

            if kind not in bucket_for_kind:
                raise TaskSessionError(
                    f"Unsupported capability kind for "
                    f"{canonical_id}: {kind}"
                )

            if kind == "skill":
                mapping = skill_map.get(canonical_id)
            else:
                mapping = capability_map.get(canonical_id)

            if not isinstance(mapping, dict):
                unresolved = unresolved_map.get(
                    canonical_id
                )

                if isinstance(unresolved, dict):
                    reason = unresolved.get(
                        "reason",
                        "No runtime mapping.",
                    )
                else:
                    reason = "No runtime mapping."

                raise TaskSessionError(
                    f"Cannot resolve temporary "
                    f"capability {canonical_id} "
                    f"({kind}): {reason}"
                )

            runtime_id = mapping.get("target")

            if not runtime_id:
                raise TaskSessionError(
                    f"Adapter mapping for "
                    f"{canonical_id} has no target."
                )

            item = {
                "canonical_id": canonical_id,
                "runtime_id": str(runtime_id),
                "adapter": adapter_name,
                "kind": kind,
            }

            resolved["all"].append(item)
            resolved[
                bucket_for_kind[kind]
            ].append(item)

        return resolved

    def plan_temporary_activation(
        self,
        state=None,
        task_session=None,
    ):
        if state is None:
            state = self.load_state()

        if task_session is None:
            task_session = self.normalize_task_session(state)

        authorization = (
            self.authorize_temporary_capabilities(
                state,
                task_session,
            )
        )

        authorized_ids = [
            item["canonical_id"]
            for item in authorization["authorized"]
        ]

        activation_session = dict(task_session)
        activation_session["temporary_capabilities"] = (
            authorized_ids
        )

        resolved = self.resolve_temporary_capabilities(
            state,
            activation_session,
        )

        if resolved["capabilities"]:
            names = [
                item["canonical_id"]
                for item in resolved["capabilities"]
            ]
            raise TaskSessionError(
                "Temporary generic capabilities require "
                f"a dedicated runtime handler: {names}"
            )

        runtime_toolsets = self._unique(
            [
                item["runtime_id"]
                for item in resolved["toolsets"]
            ]
            + [
                item["runtime_id"]
                for item in resolved["contexts"]
            ]
        )

        return {
            "workshop": authorization["workshop"],
            "authorized": authorization["authorized"],
            "already_active": authorization["already_active"],
            "runtime_toolsets": runtime_toolsets,
            "skill_bindings": resolved["skills"],
            "resolved": resolved,
        }


    def _load_hermes_toolset_runtime(self, state):
        runtime = state.get("runtime", {})

        if not isinstance(runtime, dict):
            raise TaskSessionError(
                "state.runtime must be a mapping."
            )

        adapter_name = runtime.get("adapter")
        platform = runtime.get("platform")

        if adapter_name != "hermes":
            raise TaskSessionError(
                "Temporary Hermes toolset activation requires "
                "the hermes runtime adapter."
            )

        if platform != "api_server":
            raise TaskSessionError(
                f"Refusing temporary Hermes activation because "
                f"runtime platform is {platform!r}, not "
                "'api_server'."
            )

        expected_home = (
            Path.home()
            / ".hermes"
            / "profiles"
            / "bristlecone"
        )

        hermes_home = os.environ.get("HERMES_HOME")

        if not hermes_home:
            raise TaskSessionError(
                "HERMES_HOME is not set."
            )

        if (
            Path(hermes_home).resolve()
            != expected_home.resolve()
        ):
            raise TaskSessionError(
                "HERMES_HOME does not point to the "
                "Bristlecone Hermes profile."
            )

        repo = (
            Path.home()
            / ".hermes"
            / "hermes-agent"
        )

        repo_text = str(repo)

        if repo_text not in sys.path:
            sys.path.insert(0, repo_text)

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
            raise TaskSessionError(
                "Hermes toolset configuration helpers "
                f"could not be imported: {exc}"
            ) from exc

        configurable = {
            str(key)
            for key, _, _ in CONFIGURABLE_TOOLSETS
        }

        return {
            "platform": platform,
            "home": expected_home,
            "config_path": expected_home / "config.yaml",
            "load_config": load_config,
            "save_config": save_config,
            "save_platform_tools": _save_platform_tools,
            "configurable": configurable,
        }

    @staticmethod
    def _atomic_restore_file(path, backup_path):
        payload = backup_path.read_bytes()
        tmp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=path.parent,
                delete=False,
            ) as tmp:
                tmp.write(payload)
                tmp.flush()
                os.fsync(tmp.fileno())
                tmp_path = Path(tmp.name)

            os.replace(tmp_path, path)

        except Exception:
            if (
                tmp_path is not None
                and tmp_path.exists()
            ):
                tmp_path.unlink()

            raise

    def _hermes_configurable_toolsets(
        self,
        runtime_api,
        config,
    ):
        raw = (
            config
            .get("platform_toolsets", {})
            .get(runtime_api["platform"], [])
        )

        if not isinstance(raw, list):
            raise TaskSessionError(
                "Hermes platform toolsets must be a list."
            )

        return self._unique(
            [
                str(item)
                for item in raw
                if str(item)
                in runtime_api["configurable"]
            ]
        )

    def begin_temporary_runtime_toolsets(
        self,
        plan,
        state=None,
    ):
        if state is None:
            state = self.load_state()

        if not isinstance(plan, dict):
            raise TaskSessionError(
                "Temporary activation plan must be a mapping."
            )

        requested = plan.get("runtime_toolsets", [])

        if not isinstance(requested, list):
            raise TaskSessionError(
                "plan.runtime_toolsets must be a list."
            )

        requested = self._unique(
            [str(item) for item in requested]
        )

        runtime_api = self._load_hermes_toolset_runtime(
            state
        )

        invalid = [
            item
            for item in requested
            if item not in runtime_api["configurable"]
        ]

        if invalid:
            raise TaskSessionError(
                "Hermes does not expose these temporary "
                f"toolsets as configurable: {invalid}"
            )

        config = runtime_api["load_config"]()

        baseline = self._hermes_configurable_toolsets(
            runtime_api,
            config,
        )

        desired = self._unique(
            baseline + requested
        )

        transaction = {
            "adapter": "hermes",
            "platform": runtime_api["platform"],
            "baseline_toolsets": baseline,
            "requested_toolsets": requested,
            "desired_toolsets": desired,
            "backup_path": None,
            "applied": False,
            "restored": False,
        }

        if desired == baseline:
            return transaction

        backup_dir = (
            self.forest
            / "backups"
            / "hermes-temporary"
        )
        backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%S-%fZ"
        )

        backup_path = (
            backup_dir
            / f"config-{stamp}.yaml"
        )

        config_path = runtime_api["config_path"]

        if not config_path.exists():
            raise TaskSessionError(
                f"Hermes config does not exist: "
                f"{config_path}"
            )

        backup_path.write_bytes(
            config_path.read_bytes()
        )

        transaction["backup_path"] = str(
            backup_path
        )

        config_written = False

        try:
            runtime_api["save_platform_tools"](
                config,
                runtime_api["platform"],
                set(desired),
            )

            runtime_api["save_config"](config)
            config_written = True

            verify = runtime_api["load_config"]()

            saved = self._hermes_configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(desired):
                raise TaskSessionError(
                    "Temporary Hermes activation "
                    f"verification failed: expected "
                    f"{sorted(desired)}, found "
                    f"{sorted(saved)}"
                )

            transaction["applied"] = True
            return transaction

        except Exception:
            if config_written:
                self._atomic_restore_file(
                    config_path,
                    backup_path,
                )

            raise

    def restore_temporary_runtime_toolsets(
        self,
        transaction,
        state=None,
    ):
        if not isinstance(transaction, dict):
            raise TaskSessionError(
                "Temporary transaction must be a mapping."
            )

        if transaction.get("restored"):
            return transaction

        if not transaction.get("applied"):
            transaction["restored"] = True
            return transaction

        if state is None:
            state = self.load_state()

        runtime_api = self._load_hermes_toolset_runtime(
            state
        )

        baseline = transaction.get(
            "baseline_toolsets",
            [],
        )

        if not isinstance(baseline, list):
            raise TaskSessionError(
                "Transaction baseline_toolsets "
                "must be a list."
            )

        backup_text = transaction.get("backup_path")
        backup_path = (
            Path(backup_text)
            if backup_text
            else None
        )

        try:
            config = runtime_api["load_config"]()

            runtime_api["save_platform_tools"](
                config,
                runtime_api["platform"],
                set(baseline),
            )

            runtime_api["save_config"](config)

            verify = runtime_api["load_config"]()

            saved = self._hermes_configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(baseline):
                raise TaskSessionError(
                    "Temporary Hermes restoration "
                    f"verification failed: expected "
                    f"{sorted(baseline)}, found "
                    f"{sorted(saved)}"
                )

        except Exception:
            if (
                backup_path is not None
                and backup_path.exists()
            ):
                self._atomic_restore_file(
                    runtime_api["config_path"],
                    backup_path,
                )

            raise

        transaction["restored"] = True
        return transaction

    def _build_hermes_skill_overlay(
        self,
        runtime_skills,
        task_id=None,
    ):
        repo = (
            Path.home()
            / ".hermes"
            / "hermes-agent"
        )

        repo_text = str(repo)
        if repo_text not in sys.path:
            sys.path.insert(0, repo_text)

        try:
            from agent.skill_commands import build_preloaded_skills_prompt
        except Exception as exc:
            raise TaskSessionError(
                "Hermes Skill loader could not be imported: "
                f"{exc}"
            ) from exc

        prompt, loaded, missing = (
            build_preloaded_skills_prompt(
                runtime_skills,
                task_id=task_id,
            )
        )

        if missing:
            raise TaskSessionError(
                f"Missing runtime Skills: {missing}"
            )

        if loaded != runtime_skills:
            raise TaskSessionError(
                f"Unexpected loaded Skills: {loaded}"
            )

        return prompt

    @staticmethod
    def _now_utc():
        return datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        )

    @staticmethod
    def _new_task_id():
        stamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ"
        )
        suffix = uuid.uuid4().hex[:8]
        return f"forest-task-{stamp}-{suffix}"

    def start_task(self, state=None, persist=False):
        if state is None:
            state = self.load_state()

        working = copy.deepcopy(state)
        current = self.normalize_task_session(working)

        if current.get("status") == "active":
            raise TaskSessionError(
                "A Forest Task Session is already active: "
                f"{current.get('id')}"
            )

        now = self._now_utc()
        task_id = self._new_task_id()

        working["task_session"] = {
            "id": task_id,
            "status": "active",
            "started_at": now,
            "updated_at": now,
            "task_sticky_skills": list(current["task_sticky_skills"]),
            "temporary_capabilities": list(current["temporary_capabilities"]),
        }

        if persist:
            self.persist_state(working)

        return {
            "state": working,
            "task_session": working["task_session"],
        }

    def _discard_task_cache(self, task_id):
        if not task_id:
            return 0

        discarded = 0

        for cache in (
            self._skill_overlay_cache,
            self._temporary_skill_overlay_cache,
        ):
            keys = [
                key
                for key in cache
                if key[0] == task_id
            ]

            for key in keys:
                del cache[key]

            discarded += len(keys)

        return discarded

    def end_task(self, state=None, persist=False):
        if state is None:
            state = self.load_state()

        working = copy.deepcopy(state)
        current = self.normalize_task_session(working)

        task_id = current.get("id")

        if current.get("status") != "active" or not task_id:
            raise TaskSessionError(
                "No active Forest Task Session to end."
            )

        discarded = self._discard_task_cache(task_id)
        now = self._now_utc()

        working["task_session"] = {
            "id": None,
            "status": "inactive",
            "started_at": None,
            "updated_at": now,
            "task_sticky_skills": list(current["task_sticky_skills"]),
            "temporary_capabilities": list(current["temporary_capabilities"]),
        }

        if persist:
            self.persist_state(working)

        return {
            "state": working,
            "task_session": working["task_session"],
            "ended_task_id": task_id,
            "cache_entries_discarded": discarded,
        }

    def prepare_temporary_skill_overlay(
        self,
        state=None,
        task_session=None,
        plan=None,
    ):
        if state is None:
            state = self.load_state()

        if task_session is None:
            task_session = self.normalize_task_session(state)

        if plan is None:
            plan = self.plan_temporary_activation(
                state=state,
                task_session=task_session,
            )

        bindings = plan.get("skill_bindings", [])

        if not isinstance(bindings, list):
            raise TaskSessionError(
                "plan.skill_bindings must be a list."
            )

        if not bindings:
            return {
                "prompt": "",
                "overlay_hash": None,
                "canonical_skills": [],
                "runtime_skills": [],
                "adapter": None,
                "cache_hit": False,
                "build_count":
                    self._temporary_overlay_build_count,
            }

        adapters = self._unique(
            [
                item["adapter"]
                for item in bindings
            ]
        )

        if len(adapters) != 1:
            raise TaskSessionError(
                "Mixed runtime adapters in one temporary "
                "Skill overlay are not supported yet."
            )

        adapter_name = adapters[0]

        canonical_skills = self._unique(
            [
                item["canonical_id"]
                for item in bindings
            ]
        )

        runtime_skills = self._unique(
            [
                item["runtime_id"]
                for item in bindings
            ]
        )

        task_id = task_session.get("id")

        cache_key = (
            task_id,
            adapter_name,
            tuple(runtime_skills),
        )

        cached = self._temporary_skill_overlay_cache.get(
            cache_key
        )

        if cached is not None:
            result = dict(cached)
            result["cache_hit"] = True
            result["build_count"] = (
                self._temporary_overlay_build_count
            )
            return result

        if adapter_name != "hermes":
            raise TaskSessionError(
                f"No temporary Skill overlay builder "
                f"exists for adapter: {adapter_name}"
            )

        prompt = self._build_hermes_skill_overlay(
            runtime_skills,
            task_id=task_id,
        )

        overlay_hash = hashlib.sha256(
            prompt.encode("utf-8")
        ).hexdigest()

        self._temporary_overlay_build_count += 1

        cached = {
            "prompt": prompt,
            "overlay_hash": overlay_hash,
            "canonical_skills": canonical_skills,
            "runtime_skills": runtime_skills,
            "adapter": adapter_name,
        }

        self._temporary_skill_overlay_cache[
            cache_key
        ] = cached

        result = dict(cached)
        result["cache_hit"] = False
        result["build_count"] = (
            self._temporary_overlay_build_count
        )
        return result

    def prepare_turn_skill_overlay(
        self,
        state=None,
        task_session=None,
        plan=None,
    ):
        if state is None:
            state = self.load_state()

        if task_session is None:
            task_session = self.normalize_task_session(state)

        if plan is None:
            plan = self.plan_temporary_activation(
                state=state,
                task_session=task_session,
            )

        sticky = self.prepare_task_sticky_overlay(
            state=state,
            task_session=task_session,
        )

        temporary = self.prepare_temporary_skill_overlay(
            state=state,
            task_session=task_session,
            plan=plan,
        )

        prompt_parts = [
            prompt
            for prompt in (
                sticky["prompt"],
                temporary["prompt"],
            )
            if prompt
        ]

        prompt = "\n\n".join(prompt_parts)

        canonical_skills = self._unique(
            sticky["canonical_skills"]
            + temporary["canonical_skills"]
        )

        runtime_skills = self._unique(
            sticky["runtime_skills"]
            + temporary["runtime_skills"]
        )

        overlay_hash = (
            hashlib.sha256(
                prompt.encode("utf-8")
            ).hexdigest()
            if prompt
            else None
        )

        return {
            "prompt": prompt,
            "overlay_hash": overlay_hash,
            "canonical_skills": canonical_skills,
            "runtime_skills": runtime_skills,
            "sticky": sticky,
            "temporary": temporary,
        }

    def prepare_task_sticky_overlay(
        self,
        state=None,
        task_session=None,
    ):
        if state is None:
            state = self.load_state()

        if task_session is None:
            task_session = self.normalize_task_session(state)

        resolved = self.resolve_task_sticky_skills(
            state,
            task_session,
        )

        if not resolved:
            return {
                "prompt": "",
                "overlay_hash": None,
                "canonical_skills": [],
                "runtime_skills": [],
                "adapter": None,
                "cache_hit": False,
                "build_count": self._overlay_build_count,
            }

        adapters = self._unique(
            [item["adapter"] for item in resolved]
        )

        if len(adapters) != 1:
            raise TaskSessionError(
                "Mixed runtime adapters in one Skill overlay "
                "are not supported yet."
            )

        adapter_name = adapters[0]
        canonical_skills = [
            item["canonical_id"] for item in resolved
        ]
        runtime_skills = [
            item["runtime_id"] for item in resolved
        ]

        task_id = task_session.get("id")

        cache_key = (
            task_id,
            adapter_name,
            tuple(runtime_skills),
        )

        cached = self._skill_overlay_cache.get(
            cache_key
        )

        if cached is not None:
            result = dict(cached)
            result["cache_hit"] = True
            result["build_count"] = self._overlay_build_count
            return result

        if adapter_name != "hermes":
            raise TaskSessionError(
                f"No Skill overlay builder exists for "
                f"adapter: {adapter_name}"
            )

        prompt = self._build_hermes_skill_overlay(
            runtime_skills,
            task_id=task_id,
        )

        overlay_hash = hashlib.sha256(
            prompt.encode("utf-8")
        ).hexdigest()

        self._overlay_build_count += 1

        cached = {
            "prompt": prompt,
            "overlay_hash": overlay_hash,
            "canonical_skills": canonical_skills,
            "runtime_skills": runtime_skills,
            "adapter": adapter_name,
        }

        self._skill_overlay_cache[cache_key] = cached

        result = dict(cached)
        result["cache_hit"] = False
        result["build_count"] = self._overlay_build_count
        return result

    def inspect(self):
        state = self.load_state()
        task_session = self.normalize_task_session(state)

        resolved = self.resolve_task_sticky_skills(
            state,
            task_session,
        )

        print("TASK SESSION MANAGER V0")
        print("=" * 52)

        print("Workshop:", state.get("workshop"))
        print("Reasoning:", state.get("reasoning"))
        print("Model form:", state.get("model_form"))

        print()
        print("Task Session ID:", task_session["id"])
        print("Status:", task_session["status"])

        print()
        print("Canonical Task-Sticky Skills:")

        if task_session["task_sticky_skills"]:
            for name in task_session[
                "task_sticky_skills"
            ]:
                print(f"  - {name}")
        else:
            print("  (none)")

        print()
        print("Resolved runtime Skills:")

        if resolved:
            for binding in resolved:
                print(
                    f"  - {binding['canonical_id']} "
                    f"-> {binding['runtime_id']} "
                    f"({binding['adapter']})"
                )
        else:
            print("  (none)")

        print()
        print("Temporary capabilities:")

        if task_session["temporary_capabilities"]:
            for name in task_session[
                "temporary_capabilities"
            ]:
                print(f"  - {name}")
        else:
            print("  (none)")

        print()
        print(
            "Portable state uses canonical Skill IDs: PASS"
        )
        print(
            "Runtime Skill IDs derived from adapter: PASS"
        )
        print("State modified: NO")
        print("Runtime/API modified: NO")

        return {
            "state": state,
            "task_session": task_session,
            "resolved_skills": resolved,
        }


def main():
    try:
        manager = TaskSessionManager()
        manager.inspect()

    except TaskSessionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
