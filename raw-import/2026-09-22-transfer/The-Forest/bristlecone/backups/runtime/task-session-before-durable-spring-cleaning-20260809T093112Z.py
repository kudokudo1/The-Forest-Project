#!/usr/bin/env python3

from pathlib import Path
import sys
import hashlib
import copy
import uuid
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
import yaml
import time


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

    def __init__(
        self,
        forest_root=None,
        runtime_adapter=None,
    ):
        if forest_root is None:
            forest_root = Path(__file__).resolve().parents[1]

        self.forest = Path(forest_root)
        self.runtime_adapter = runtime_adapter
        self._skill_overlay_cache = {}
        self._temporary_skill_overlay_cache = {}
        self._overlay_build_count = 0
        self._temporary_overlay_build_count = 0
        self.state_file = self.forest / "state" / "active.yaml"
        self.winter_tasks_dir = (
            self.forest
            / "state"
            / "tasks"
            / "winter"
        )
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

    @contextmanager
    def _state_write_lock(self):
        """Serialize active.yaml compare-and-write operations."""

        lock_file = self.state_file.with_name(
            f".{self.state_file.name}.lock"
        )

        lock_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            import fcntl
        except ImportError as exc:
            raise TaskSessionError(
                "Forest state locking requires fcntl "
                "on this runtime."
            ) from exc

        with lock_file.open(
            "a+",
            encoding="utf-8",
        ) as handle:
            fcntl.flock(
                handle.fileno(),
                fcntl.LOCK_EX,
            )

            try:
                yield
            finally:
                fcntl.flock(
                    handle.fileno(),
                    fcntl.LOCK_UN,
                )

    def persist_state(self, state):
        if not isinstance(state, dict):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        # Validate Task Session structure before writing.
        self.normalize_task_session(state)

        with self._state_write_lock():
            self._atomic_write_yaml(
                self.state_file,
                state,
            )

        return state

    def load_state(self):
        return self._load_yaml(self.state_file)

    def load_registry(self):
        return self._load_yaml(self.registry_file)

    def load_adapter(self, name):
        path = self.forest / "adapters" / f"{name}.yaml"
        return self._load_yaml(path)

    def _runtime_adapter_for_state(self, state):
        """Return an injected or Forest-selected runtime adapter."""

        if self.runtime_adapter is not None:
            return self.runtime_adapter

        try:
            from .adapters.factory import (
                create_runtime_adapter,
            )

        except ImportError:
            from runtime.adapters.factory import (
                create_runtime_adapter,
            )

        try:
            return create_runtime_adapter(
                state,
                forest_root=self.forest,
            )

        except TaskSessionError:
            raise

        except Exception as exc:
            raise TaskSessionError(
                "Forest could not resolve the configured "
                f"runtime adapter: {exc}"
            ) from exc

    def get_active_runtime_toolsets(self, state):
        """Read active toolsets through the selected runtime adapter."""

        adapter = self._runtime_adapter_for_state(
            state
        )

        if adapter is None:
            raise TaskSessionError(
                "No runtime adapter was provided to "
                "TaskSessionManager."
            )

        getter = getattr(
            adapter,
            "get_active_toolsets",
            None,
        )

        if not callable(getter):
            raise TaskSessionError(
                "The runtime adapter does not provide "
                "get_active_toolsets()."
            )

        try:
            return getter(state)

        except TaskSessionError:
            raise

        except Exception as exc:
            adapter_name = getattr(
                adapter,
                "adapter_name",
                type(adapter).__name__,
            )

            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                f"could not read active toolsets: {exc}"
            ) from exc

    def _normalize_task_lifecycle(
        self,
        raw,
    ):
        """Normalize Forest Task seasonal lifecycle metadata."""

        lifecycle = raw.get(
            "lifecycle"
        )

        if lifecycle is None:
            lifecycle = {}

        if not isinstance(
            lifecycle,
            dict,
        ):
            raise TaskSessionError(
                "task_session.lifecycle must be "
                "a mapping."
            )

        allowed_seasons = {
            "summer",
            "fall",
            "winter",
            "spring",
        }

        season = lifecycle.get(
            "season"
        )

        # Backward compatibility:
        #
        # Old Forest state files predate seasons.
        # Active Tasks naturally map to Summer.
        # Inactive state naturally maps to Winter.
        if season is None:
            season = (
                "summer"
                if raw.get(
                    "status",
                    "inactive",
                ) == "active"
                else "winter"
            )

        if not isinstance(
            season,
            str,
        ):
            raise TaskSessionError(
                "Task lifecycle season must be "
                "a string."
            )

        season = season.strip().lower()

        if season not in allowed_seasons:
            raise TaskSessionError(
                "Unknown Task lifecycle season: "
                f"{season!r}."
            )

        previous_season = lifecycle.get(
            "previous_season"
        )

        if previous_season is not None:
            if not isinstance(
                previous_season,
                str,
            ):
                raise TaskSessionError(
                    "previous_season must be a "
                    "string or null."
                )

            previous_season = (
                previous_season
                .strip()
                .lower()
            )

            if (
                previous_season
                not in allowed_seasons
            ):
                raise TaskSessionError(
                    "Unknown previous Task season: "
                    f"{previous_season!r}."
                )

        entered_at = lifecycle.get(
            "entered_at"
        )

        if entered_at is None:
            entered_at = (
                raw.get("updated_at")
                or raw.get("started_at")
            )

        return {
            "season":
                season,

            "previous_season":
                previous_season,

            "entered_at":
                entered_at,
        }

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

        raw_runtime_sessions = raw.get(
            "runtime_sessions",
            {},
        )

        if raw_runtime_sessions is None:
            raw_runtime_sessions = {}

        if not isinstance(raw_runtime_sessions, dict):
            raise TaskSessionError(
                "runtime_sessions must be a mapping."
            )

        runtime_sessions = {}

        for adapter_name, entry in (
            raw_runtime_sessions.items()
        ):
            if not isinstance(entry, dict):
                raise TaskSessionError(
                    "Each runtime session must be "
                    "a mapping."
                )

            adapter_name = str(adapter_name).strip()

            if not adapter_name:
                raise TaskSessionError(
                    "Runtime session adapter name "
                    "cannot be empty."
                )

            session_id = entry.get("session_id")
            previous_session_id = entry.get(
                "previous_session_id"
            )

            runtime_sessions[adapter_name] = {
                "session_id": (
                    str(session_id)
                    if session_id is not None
                    else None
                ),
                "previous_session_id": (
                    str(previous_session_id)
                    if previous_session_id is not None
                    else None
                ),
                "updated_at": entry.get("updated_at"),
            }

        return {
            "id": raw.get("id"),
            "status": raw.get("status", "inactive"),
            "lifecycle":
                self._normalize_task_lifecycle(
                    raw
                ),
            "started_at": raw.get("started_at"),
            "updated_at": raw.get("updated_at"),
            "task_sticky_skills": self._unique(
                canonical_skills
            ),
            "temporary_capabilities": self._unique(
                [str(item) for item in temporary]
            ),
            "runtime_sessions": runtime_sessions,
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


    def _build_runtime_skill_overlay(
        self,
        state,
        adapter_name,
        runtime_skills,
        task_id=None,
    ):
        """Build a Skill overlay through the selected runtime adapter."""

        runtime_adapter = (
            self._runtime_adapter_for_state(
                state
            )
        )

        selected_name = getattr(
            runtime_adapter,
            "adapter_name",
            type(runtime_adapter).__name__,
        )

        if selected_name != adapter_name:
            raise TaskSessionError(
                "Skill binding adapter does not match "
                "the selected Forest runtime adapter: "
                f"{adapter_name!r} != "
                f"{selected_name!r}"
            )

        builder = getattr(
            runtime_adapter,
            "build_skill_overlay",
            None,
        )

        if not callable(builder):
            raise TaskSessionError(
                f"Runtime adapter {selected_name!r} "
                "does not provide "
                "build_skill_overlay()."
            )

        try:
            return builder(
                runtime_skills,
                task_id=task_id,
            )

        except TaskSessionError:
            raise

        except Exception as exc:
            raise TaskSessionError(
                f"Runtime adapter {selected_name!r} "
                "could not build the Skill overlay: "
                f"{exc}"
            ) from exc

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
            "lifecycle": {
                "season": "summer",
                "previous_season": None,
                "entered_at": now,
            },
            "started_at": now,
            "updated_at": now,
            "task_sticky_skills": list(current["task_sticky_skills"]),
            "temporary_capabilities": list(current["temporary_capabilities"]),
            "runtime_sessions": {},
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

    def transition_task_season(
        self,
        season,
        state=None,
        persist=False,
    ):
        """Move the active Forest Task into a new season.

        Summer, Fall, and Spring are active Task seasons.

        Winter currently represents dormancy and is
        entered through end_task(). This keeps Task status
        and seasonal lifecycle consistent until durable
        retired-Task storage is implemented.
        """

        if state is None:
            state = self.load_state()

        working = copy.deepcopy(
            state
        )

        current = (
            self.normalize_task_session(
                working
            )
        )

        task_id = current.get(
            "id"
        )

        if (
            current.get("status")
            != "active"
            or not task_id
        ):
            raise TaskSessionError(
                "No active Forest Task Session "
                "to transition."
            )

        if not isinstance(
            season,
            str,
        ):
            raise TaskSessionError(
                "Task season must be a string."
            )

        season = season.strip().lower()

        allowed_active_seasons = {
            "summer",
            "fall",
            "spring",
        }

        if season == "winter":
            raise TaskSessionError(
                "Winter is the dormant Task state. "
                "Use end_task() to enter Winter."
            )

        if (
            season
            not in allowed_active_seasons
        ):
            raise TaskSessionError(
                "Unknown active Task season: "
                f"{season!r}."
            )

        current_lifecycle = current[
            "lifecycle"
        ]

        current_season = (
            current_lifecycle[
                "season"
            ]
        )

        # Do not rewrite active.yaml when nothing changed.
        if season == current_season:
            return {
                "state":
                    working,

                "task_session":
                    current,

                "task_id":
                    task_id,

                "from_season":
                    current_season,

                "season":
                    current_season,

                "changed":
                    False,
            }

        now = self._now_utc()

        working[
            "task_session"
        ][
            "lifecycle"
        ] = {
            "season":
                season,

            "previous_season":
                current_season,

            "entered_at":
                now,
        }

        working[
            "task_session"
        ][
            "updated_at"
        ] = now

        normalized = (
            self.normalize_task_session(
                working
            )
        )

        if persist:
            self.persist_state(
                working
            )

        return {
            "state":
                working,

            "task_session":
                normalized,

            "task_id":
                task_id,

            "from_season":
                current_season,

            "season":
                season,

            "changed":
                True,
        }

    def _winter_task_file(
        self,
        task_id,
    ):
        """Return the durable file for one dormant Task."""

        task_id = str(
            task_id
        ).strip()

        if not task_id:
            raise TaskSessionError(
                "Winter Task ID cannot be empty."
            )

        if (
            "/" in task_id
            or "\\" in task_id
            or Path(task_id).name != task_id
        ):
            raise TaskSessionError(
                "Winter Task ID is not a safe filename."
            )

        return (
            self.winter_tasks_dir
            / f"{task_id}.yaml"
        )

    def _build_winter_task_record(
        self,
        state,
        current,
        retired_at,
    ):
        """Build the durable dormant representation of a Task."""

        task_id = current.get(
            "id"
        )

        if not task_id:
            raise TaskSessionError(
                "Cannot build Winter record "
                "without a Task ID."
            )

        previous_season = (
            current[
                "lifecycle"
            ][
                "season"
            ]
        )

        winter_task = copy.deepcopy(
            current
        )

        winter_task[
            "status"
        ] = "dormant"

        winter_task[
            "lifecycle"
        ] = {
            "season":
                "winter",

            "previous_season":
                previous_season,

            "entered_at":
                retired_at,
        }

        winter_task[
            "updated_at"
        ] = retired_at

        # This is a lightweight record of what was useful
        # when the Task went dormant. Spring Cleaning can
        # inspect it later without automatically restoring
        # everything wholesale.
        activation_snapshot = {}

        for key in (
            "workshop",
            "active_general",
            "active_ready",
            "reasoning",
            "model_form",
        ):
            if key in state:
                activation_snapshot[
                    key
                ] = copy.deepcopy(
                    state[
                        key
                    ]
                )

        return {
            "schema_version": 1,
            "record_type":
                "forest_winter_task",
            "tree":
                state.get(
                    "tree"
                ),
            "task_id":
                task_id,
            "retired_at":
                retired_at,

            # Machine-only ordering value. The readable
            # retired_at timestamp remains the primary
            # human-facing representation.
            "retired_order":
                time.time_ns(),
            "task_session":
                winter_task,
            "activation_snapshot":
                activation_snapshot,
        }

    def list_winter_tasks(
        self,
    ):
        """Return lightweight summaries of dormant Tasks.

        Full Task records stay on disk until explicitly
        requested. Discovery uses retired_order when
        available so multiple Tasks retired in the same
        human-readable second still sort correctly.
        """

        if not self.winter_tasks_dir.exists():
            return []

        summaries = []

        for path in self.winter_tasks_dir.glob(
            "forest-task-*.yaml"
        ):
            try:
                record = self._load_yaml(
                    path
                )

                if not isinstance(
                    record,
                    dict,
                ):
                    continue

                if (
                    record.get(
                        "record_type"
                    )
                    != "forest_winter_task"
                ):
                    continue

                task = record.get(
                    "task_session"
                )

                if not isinstance(
                    task,
                    dict,
                ):
                    continue

                normalized = (
                    self.normalize_task_session(
                        {
                            "task_session":
                                task
                        }
                    )
                )

                if (
                    normalized[
                        "lifecycle"
                    ][
                        "season"
                    ]
                    != "winter"
                ):
                    continue

                if (
                    normalized.get(
                        "status"
                    )
                    != "dormant"
                ):
                    continue

                snapshot = record.get(
                    "activation_snapshot",
                    {},
                )

                if not isinstance(
                    snapshot,
                    dict,
                ):
                    snapshot = {}

                runtime_sessions = (
                    normalized.get(
                        "runtime_sessions",
                        {},
                    )
                )

                retired_order = record.get(
                    "retired_order"
                )

                if not isinstance(
                    retired_order,
                    int,
                ):
                    # Legacy Winter records predate
                    # precise retirement ordering.
                    retired_order = 0

                summaries.append(
                    {
                        "task_id":
                            normalized.get(
                                "id"
                            ),

                        "tree":
                            record.get(
                                "tree"
                            ),

                        "retired_at":
                            record.get(
                                "retired_at"
                            ),

                        "entered_winter_at":
                            normalized[
                                "lifecycle"
                            ][
                                "entered_at"
                            ],

                        "previous_season":
                            normalized[
                                "lifecycle"
                            ][
                                "previous_season"
                            ],

                        "workshop":
                            snapshot.get(
                                "workshop"
                            ),

                        "reasoning":
                            snapshot.get(
                                "reasoning"
                            ),

                        "model_form":
                            snapshot.get(
                                "model_form"
                            ),

                        "runtime_adapters":
                            sorted(
                                runtime_sessions.keys()
                            ),

                        "file":
                            str(path),

                        # Internal sorting value removed
                        # before results leave this method.
                        "_retired_order":
                            retired_order,
                    }
                )

            except Exception:
                # One damaged Winter record must not make
                # the entire dormant Task list unusable.
                continue

        summaries.sort(
            key=lambda item: (
                item[
                    "_retired_order"
                ],
                str(
                    item.get(
                        "retired_at"
                    )
                    or ""
                ),
                str(
                    item.get(
                        "task_id"
                    )
                    or ""
                ),
            ),
            reverse=True,
        )

        for item in summaries:
            item.pop(
                "_retired_order",
                None,
            )

        return summaries

    def _remove_winter_task_file(
        self,
        path,
    ):
        """Remove one dormant Task record after Spring wake."""

        path = Path(path)

        if path.exists():
            path.unlink()

        return not path.exists()

    def begin_spring_cleaning(
        self,
        task_id,
        state=None,
        persist=False,
    ):
        """Wake one dormant Task into Spring.

        Spring restores Task identity and preserved runtime
        lineage, but activation_snapshot remains advisory.

        Workshop/tool/Skill/reasoning restoration is left
        to later selective Spring Cleaning logic.
        """

        if state is None:
            state = self.load_state()

        working = copy.deepcopy(state)

        current = self.normalize_task_session(
            working
        )

        if (
            current.get("status") != "inactive"
            or current.get("id") is not None
        ):
            raise TaskSessionError(
                "Spring Cleaning requires the "
                "active Forest Task slot to be empty."
            )

        task_id = str(task_id).strip()

        if not task_id:
            raise TaskSessionError(
                "Spring Cleaning requires a Task ID."
            )

        winter_file = self._winter_task_file(
            task_id
        )

        winter_file_removed = False
        winter_cleanup_error = None

        # ----------------------------------------------
        # PERSISTENT SPRING WAKE
        # ----------------------------------------------

        if persist:
            with self._state_write_lock():
                latest = self.load_state()

                latest_current = (
                    self.normalize_task_session(
                        latest
                    )
                )

                if (
                    latest_current.get("status")
                    != "inactive"
                    or latest_current.get("id")
                    is not None
                ):
                    raise TaskSessionError(
                        "Forest Task slot changed "
                        "before Spring Cleaning."
                    )

                record = self.load_winter_task(
                    task_id
                )

                record_tree = record.get("tree")
                current_tree = latest.get("tree")

                if (
                    record_tree is not None
                    and current_tree is not None
                    and str(record_tree)
                    != str(current_tree)
                ):
                    raise TaskSessionError(
                        "Winter Task belongs to a "
                        "different Tree."
                    )

                now = self._now_utc()

                spring_task = copy.deepcopy(
                    record["task_session"]
                )

                spring_task["status"] = "active"

                spring_task["lifecycle"] = {
                    "season": "spring",
                    "previous_season": "winter",
                    "entered_at": now,
                }

                spring_task["updated_at"] = now

                activated = copy.deepcopy(
                    latest
                )

                activated["task_session"] = (
                    spring_task
                )

                # LOSS-AVERSE ORDERING:
                #
                # Active Spring copy FIRST.
                # Winter copy removal SECOND.
                #
                # A crash may leave a duplicate,
                # but never a lost Task.
                self._atomic_write_yaml(
                    self.state_file,
                    activated,
                )

                working = activated

                try:
                    winter_file_removed = (
                        self._remove_winter_task_file(
                            winter_file
                        )
                    )

                except Exception as exc:
                    # Spring is already durable.
                    # Duplicate cleanup failure must not
                    # undo the successful wake.
                    winter_cleanup_error = str(exc)
                    winter_file_removed = False

        # ----------------------------------------------
        # NON-PERSISTENT SPRING PREVIEW
        # ----------------------------------------------

        else:
            record = self.load_winter_task(
                task_id
            )

            record_tree = record.get("tree")
            current_tree = working.get("tree")

            if (
                record_tree is not None
                and current_tree is not None
                and str(record_tree)
                != str(current_tree)
            ):
                raise TaskSessionError(
                    "Winter Task belongs to a "
                    "different Tree."
                )

            now = self._now_utc()

            spring_task = copy.deepcopy(
                record["task_session"]
            )

            spring_task["status"] = "active"

            spring_task["lifecycle"] = {
                "season": "spring",
                "previous_season": "winter",
                "entered_at": now,
            }

            spring_task["updated_at"] = now

            working["task_session"] = (
                spring_task
            )

        activation_snapshot = record.get(
            "activation_snapshot",
            {},
        )

        if not isinstance(
            activation_snapshot,
            dict,
        ):
            activation_snapshot = {}

        normalized = (
            self.normalize_task_session(
                working
            )
        )

        return {
            "state": working,
            "task_session": normalized,
            "task_id": task_id,
            "season": "spring",
            "from_season": "winter",

            "activation_snapshot":
                copy.deepcopy(
                    activation_snapshot
                ),

            "runtime_sessions":
                copy.deepcopy(
                    normalized[
                        "runtime_sessions"
                    ]
                ),

            "winter_file":
                str(winter_file),

            "winter_file_removed":
                winter_file_removed,

            "winter_cleanup_error":
                winter_cleanup_error,

            "persisted":
                bool(persist),
        }

    def load_winter_task(
        self,
        task_id,
    ):
        """Load and validate one dormant Winter Task."""

        path = self._winter_task_file(
            task_id
        )

        if not path.exists():
            raise TaskSessionError(
                "Winter Task does not exist: "
                f"{task_id}"
            )

        record = self._load_yaml(
            path
        )

        if not isinstance(
            record,
            dict,
        ):
            raise TaskSessionError(
                "Winter Task record must "
                "be a mapping."
            )

        if (
            record.get(
                "record_type"
            )
            != "forest_winter_task"
        ):
            raise TaskSessionError(
                "Invalid Winter Task record type."
            )

        task = record.get(
            "task_session"
        )

        if not isinstance(
            task,
            dict,
        ):
            raise TaskSessionError(
                "Winter Task is missing "
                "task_session."
            )

        normalized = (
            self.normalize_task_session(
                {
                    "task_session":
                        task
                }
            )
        )

        if (
            str(
                normalized.get("id")
            )
            != str(task_id)
        ):
            raise TaskSessionError(
                "Winter Task ID does not match "
                "its filename."
            )

        if (
            normalized[
                "lifecycle"
            ][
                "season"
            ]
            != "winter"
        ):
            raise TaskSessionError(
                "Dormant Task is not in Winter."
            )

        if (
            normalized.get(
                "status"
            )
            != "dormant"
        ):
            raise TaskSessionError(
                "Winter Task status must "
                "be dormant."
            )

        return record

    def end_task(
        self,
        state=None,
        persist=False,
    ):
        """End the active Task and place it into Winter.

        With persistence enabled, the dormant Winter
        record is written BEFORE active.yaml is cleared.

        This intentionally prefers a recoverable duplicate
        after a crash over possible Task loss.
        """

        if state is None:
            state = self.load_state()

        working = copy.deepcopy(
            state
        )

        current = (
            self.normalize_task_session(
                working
            )
        )

        task_id = current.get(
            "id"
        )

        if (
            current.get("status")
            != "active"
            or not task_id
        ):
            raise TaskSessionError(
                "No active Forest Task Session to end."
            )

        expected_task_id = str(
            task_id
        )

        winter_record = None
        winter_file = None
        winter_persisted = False

        # ------------------------------------------------
        # PERSISTENT RETIREMENT
        # ------------------------------------------------

        if persist:
            # Use the same lock as active.yaml writers so
            # another Forest writer cannot change the Task
            # between our Winter snapshot and active clear.
            with self._state_write_lock():
                latest = self.load_state()

                latest_current = (
                    self.normalize_task_session(
                        latest
                    )
                )

                latest_task_id = (
                    latest_current.get(
                        "id"
                    )
                )

                if (
                    latest_current.get(
                        "status"
                    )
                    != "active"
                    or not latest_task_id
                ):
                    raise TaskSessionError(
                        "Active Forest Task changed "
                        "before Winter retirement."
                    )

                if (
                    str(latest_task_id)
                    != expected_task_id
                ):
                    raise TaskSessionError(
                        "Forest Task generation changed "
                        "before Winter retirement."
                    )

                now = self._now_utc()

                winter_record = (
                    self._build_winter_task_record(
                        latest,
                        latest_current,
                        now,
                    )
                )

                winter_file = (
                    self._winter_task_file(
                        expected_task_id
                    )
                )

                # LOSS-AVERSE ORDERING:
                #
                # 1. Durable Winter copy first.
                # 2. Clear active slot second.
                #
                # A crash between these writes may leave a
                # duplicate Task, but cannot erase the Task.
                self._atomic_write_yaml(
                    winter_file,
                    winter_record,
                )

                winter_persisted = True

                retired_runtime_sessions = (
                    copy.deepcopy(
                        latest_current[
                            "runtime_sessions"
                        ]
                    )
                )

                cleared = copy.deepcopy(
                    latest
                )

                cleared[
                    "task_session"
                ] = {
                    "id":
                        None,

                    "status":
                        "inactive",

                    "lifecycle": {
                        "season":
                            "winter",

                        "previous_season":
                            latest_current[
                                "lifecycle"
                            ][
                                "season"
                            ],

                        "entered_at":
                            now,
                    },

                    "started_at":
                        None,

                    "updated_at":
                        now,

                    "task_sticky_skills":
                        list(
                            latest_current[
                                "task_sticky_skills"
                            ]
                        ),

                    "temporary_capabilities":
                        list(
                            latest_current[
                                "temporary_capabilities"
                            ]
                        ),

                    "runtime_sessions":
                        {},
                }

                self._atomic_write_yaml(
                    self.state_file,
                    cleared,
                )

                working = cleared
                current = latest_current

        # ------------------------------------------------
        # NON-PERSISTENT / IN-MEMORY RETIREMENT
        # ------------------------------------------------

        else:
            now = self._now_utc()

            winter_record = (
                self._build_winter_task_record(
                    working,
                    current,
                    now,
                )
            )

            retired_runtime_sessions = (
                copy.deepcopy(
                    current[
                        "runtime_sessions"
                    ]
                )
            )

            working[
                "task_session"
            ] = {
                "id":
                    None,

                "status":
                    "inactive",

                "lifecycle": {
                    "season":
                        "winter",

                    "previous_season":
                        current[
                            "lifecycle"
                        ][
                            "season"
                        ],

                    "entered_at":
                        now,
                },

                "started_at":
                    None,

                "updated_at":
                    now,

                "task_sticky_skills":
                    list(
                        current[
                            "task_sticky_skills"
                        ]
                    ),

                "temporary_capabilities":
                    list(
                        current[
                            "temporary_capabilities"
                        ]
                    ),

                "runtime_sessions":
                    {},
            }

        # Only discard in-memory Task caches after the
        # durable state transition has succeeded.
        discarded = self._discard_task_cache(
            task_id
        )

        return {
            "state":
                working,

            "task_session":
                working[
                    "task_session"
                ],

            "ended_task_id":
                task_id,

            "ended_lifecycle":
                copy.deepcopy(
                    working[
                        "task_session"
                    ][
                        "lifecycle"
                    ]
                ),

            "winter_record":
                copy.deepcopy(
                    winter_record
                ),

            "winter_file":
                (
                    str(winter_file)
                    if winter_file
                    is not None
                    else None
                ),

            "winter_persisted":
                winter_persisted,

            "cache_entries_discarded":
                discarded,

            "retired_runtime_sessions":
                retired_runtime_sessions,
        }


    def _active_runtime_task(
        self,
        state,
    ):
        """Return the normalized active Forest Task."""

        task_session = (
            self.normalize_task_session(
                state
            )
        )

        task_id = task_session.get(
            "id"
        )

        if (
            task_session.get("status")
            != "active"
            or not task_id
        ):
            raise TaskSessionError(
                "Runtime session operations require "
                "an active Forest Task Session."
            )

        return task_session

    @staticmethod
    def _runtime_adapter_name(
        runtime_adapter,
    ):
        adapter_name = getattr(
            runtime_adapter,
            "adapter_name",
            None,
        )

        if not adapter_name:
            raise TaskSessionError(
                "Runtime adapter does not expose "
                "adapter_name."
            )

        return str(
            adapter_name
        )

    def _write_runtime_session_binding(
        self,
        working,
        adapter_name,
        session_id,
        previous_session_id=None,
    ):
        """Write one runtime binding into Forest Task state."""

        session_id = str(
            session_id
        ).strip()

        if not session_id:
            raise TaskSessionError(
                "Runtime session ID cannot be empty."
            )

        if previous_session_id is not None:
            previous_session_id = str(
                previous_session_id
            ).strip()

            if not previous_session_id:
                previous_session_id = None

        task_session = working.get(
            "task_session"
        )

        if not isinstance(
            task_session,
            dict,
        ):
            raise TaskSessionError(
                "state.task_session must be a mapping."
            )

        runtime_sessions = task_session.get(
            "runtime_sessions"
        )

        if runtime_sessions is None:
            runtime_sessions = {}
            task_session[
                "runtime_sessions"
            ] = runtime_sessions

        if not isinstance(
            runtime_sessions,
            dict,
        ):
            raise TaskSessionError(
                "task_session.runtime_sessions "
                "must be a mapping."
            )

        now = self._now_utc()

        runtime_sessions[
            adapter_name
        ] = {
            "session_id":
                session_id,

            "previous_session_id":
                previous_session_id,

            "updated_at":
                now,
        }

        task_session[
            "updated_at"
        ] = now

        return runtime_sessions[
            adapter_name
        ]

    def _capture_runtime_persist_guard(
        self,
        working,
        adapter_name,
    ):
        """Capture persisted Task/session generation before I/O."""

        working_task = self._active_runtime_task(
            working
        )

        expected_task_id = working_task["id"]

        with self._state_write_lock():
            persisted = self.load_state()

            persisted_task = (
                self.normalize_task_session(
                    persisted
                )
            )

            if (
                persisted_task.get("status")
                != "active"
                or persisted_task.get("id")
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Persistent runtime operation refused: "
                    "the supplied Forest Task is not the "
                    "currently active persisted Task."
                )

            persisted_binding = (
                persisted_task[
                    "runtime_sessions"
                ].get(
                    adapter_name
                )
            )

            persisted_session_id = None

            if isinstance(
                persisted_binding,
                dict,
            ):
                persisted_session_id = (
                    persisted_binding.get(
                        "session_id"
                    )
                )

                if persisted_session_id:
                    persisted_session_id = str(
                        persisted_session_id
                    )

        return {
            "task_id":
                expected_task_id,

            "adapter":
                adapter_name,

            "session_id":
                persisted_session_id,
        }

    def _persist_runtime_binding_guarded(
        self,
        working,
        guard,
    ):
        """CAS-merge one runtime binding into latest active.yaml."""

        if not isinstance(
            guard,
            dict,
        ):
            raise TaskSessionError(
                "Runtime persistence guard must "
                "be a mapping."
            )

        target_task = self._active_runtime_task(
            working
        )

        expected_task_id = guard.get(
            "task_id"
        )

        adapter_name = str(
            guard.get("adapter")
            or ""
        ).strip()

        expected_session_id = guard.get(
            "session_id"
        )

        if expected_session_id is not None:
            expected_session_id = str(
                expected_session_id
            )

        if (
            not adapter_name
            or target_task["id"]
            != expected_task_id
        ):
            raise TaskSessionError(
                "Runtime persistence guard does not "
                "match the supplied Forest Task."
            )

        source_binding = (
            target_task[
                "runtime_sessions"
            ].get(
                adapter_name
            )
        )

        if not isinstance(
            source_binding,
            dict,
        ):
            raise TaskSessionError(
                "No runtime binding is available "
                "to persist."
            )

        source_session_id = source_binding.get(
            "session_id"
        )

        if not source_session_id:
            raise TaskSessionError(
                "Runtime binding has no session_id."
            )

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self.normalize_task_session(
                    latest
                )
            )

            if (
                latest_task.get("status")
                != "active"
                or latest_task.get("id")
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Stale Forest Task generation: "
                    "active.yaml changed before "
                    "runtime binding commit."
                )

            latest_binding = (
                latest_task[
                    "runtime_sessions"
                ].get(
                    adapter_name
                )
            )

            latest_session_id = None

            if isinstance(
                latest_binding,
                dict,
            ):
                latest_session_id = (
                    latest_binding.get(
                        "session_id"
                    )
                )

                if latest_session_id:
                    latest_session_id = str(
                        latest_session_id
                    )

            if (
                latest_session_id
                != expected_session_id
            ):
                raise TaskSessionError(
                    "Stale runtime binding: "
                    f"expected persisted "
                    f"{adapter_name!r} session "
                    f"{expected_session_id!r}, "
                    f"found {latest_session_id!r}."
                )

            latest_task[
                "runtime_sessions"
            ][
                adapter_name
            ] = copy.deepcopy(
                source_binding
            )

            latest_task[
                "updated_at"
            ] = (
                target_task.get(
                    "updated_at"
                )
                or self._now_utc()
            )

            latest[
                "task_session"
            ] = latest_task

            self.normalize_task_session(
                latest
            )

            self._atomic_write_yaml(
                self.state_file,
                latest,
            )

        return latest

    @staticmethod
    def _best_effort_end_runtime_sessions(
        runtime_adapter,
        session_ids,
        state,
    ):
        """Best-effort cleanup for sessions created by failed commits."""

        ender = getattr(
            runtime_adapter,
            "end_session",
            None,
        )

        if not callable(
            ender
        ):
            return

        seen = set()

        for session_id in session_ids:
            if not session_id:
                continue

            session_id = str(
                session_id
            )

            if session_id in seen:
                continue

            seen.add(
                session_id
            )

            try:
                ender(
                    session_id,
                    state,
                )
            except Exception:
                pass

    def ensure_runtime_session(
        self,
        state=None,
        persist=False,
    ):
        """Create or reuse the Task's runtime session.

        Forest owns the binding. The runtime adapter
        owns creation of the runtime-specific session.

        Persistent writes use the Forest Task ID and
        prior persisted runtime session as a guarded
        compare-and-swap boundary.
        """

        if state is None:
            state = self.load_state()

        working = copy.deepcopy(
            state
        )

        task_session = (
            self._active_runtime_task(
                working
            )
        )

        runtime_adapter = (
            self._runtime_adapter_for_state(
                working
            )
        )

        adapter_name = (
            self._runtime_adapter_name(
                runtime_adapter
            )
        )

        persist_guard = None

        if persist:
            persist_guard = (
                self._capture_runtime_persist_guard(
                    working,
                    adapter_name,
                )
            )

        existing = (
            task_session[
                "runtime_sessions"
            ].get(
                adapter_name
            )
        )

        if isinstance(
            existing,
            dict,
        ):
            existing_id = existing.get(
                "session_id"
            )

            if existing_id:
                existing_id = str(
                    existing_id
                )

                if (
                    persist
                    and persist_guard[
                        "session_id"
                    ] != existing_id
                ):
                    working = (
                        self._persist_runtime_binding_guarded(
                            working,
                            persist_guard,
                        )
                    )

                    task_session = (
                        self._active_runtime_task(
                            working
                        )
                    )

                return {
                    "state":
                        working,

                    "task_session":
                        task_session,

                    "adapter":
                        adapter_name,

                    "session_id":
                        existing_id,

                    "created":
                        False,

                    "reused":
                        True,

                    "runtime_result":
                        None,
                }

        creator = getattr(
            runtime_adapter,
            "create_session",
            None,
        )

        if not callable(
            creator
        ):
            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                "does not provide create_session()."
            )

        try:
            created = creator(
                working,
                task_id=task_session[
                    "id"
                ],
            )

        except TaskSessionError:
            raise

        except Exception as exc:
            raise TaskSessionError(
                f"Runtime adapter "
                f"{adapter_name!r} could not "
                f"create a runtime session: {exc}"
            ) from exc

        if not isinstance(
            created,
            dict,
        ):
            raise TaskSessionError(
                "Runtime session creation must "
                "return a mapping."
            )

        returned_adapter = created.get(
            "adapter",
            adapter_name,
        )

        if str(
            returned_adapter
        ) != adapter_name:
            raise TaskSessionError(
                "Runtime session creation returned "
                "a mismatched adapter."
            )

        session_id = created.get(
            "session_id"
        )

        if not session_id:
            raise TaskSessionError(
                "Runtime adapter created a session "
                "without returning session_id."
            )

        session_id = str(
            session_id
        )

        binding = (
            self._write_runtime_session_binding(
                working,
                adapter_name,
                session_id,
                previous_session_id=None,
            )
        )

        if persist:
            try:
                working = (
                    self._persist_runtime_binding_guarded(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                self._best_effort_end_runtime_sessions(
                    runtime_adapter,
                    [session_id],
                    working,
                )
                raise

            binding = (
                self._active_runtime_task(
                    working
                )[
                    "runtime_sessions"
                ][
                    adapter_name
                ]
            )

        return {
            "state":
                working,

            "task_session":
                self.normalize_task_session(
                    working
                ),

            "adapter":
                adapter_name,

            "session_id":
                binding[
                    "session_id"
                ],

            "created":
                True,

            "reused":
                False,

            "runtime_result":
                created,
        }

    def send_runtime_turn(
        self,
        message,
        state=None,
        instructions=None,
        persist=False,
    ):
        """Send a turn and update Forest runtime binding.

        When persistence is requested, any newly created
        or not-yet-persisted runtime binding is committed
        before the potentially long runtime/model call.

        Normal same-session warm turns remain write-free.
        """

        if state is None:
            state = self.load_state()

        initial = copy.deepcopy(
            state
        )

        initial_adapter = (
            self._runtime_adapter_for_state(
                initial
            )
        )

        initial_adapter_name = (
            self._runtime_adapter_name(
                initial_adapter
            )
        )

        persist_guard = None

        if persist:
            persist_guard = (
                self._capture_runtime_persist_guard(
                    initial,
                    initial_adapter_name,
                )
            )

        ensured = (
            self.ensure_runtime_session(
                state=initial,
                persist=False,
            )
        )

        working = ensured[
            "state"
        ]

        runtime_adapter = (
            self._runtime_adapter_for_state(
                working
            )
        )

        adapter_name = (
            self._runtime_adapter_name(
                runtime_adapter
            )
        )

        if (
            adapter_name
            != ensured["adapter"]
            or adapter_name
            != initial_adapter_name
        ):
            raise TaskSessionError(
                "Runtime adapter changed while "
                "preparing the Task turn."
            )

        requested_session_id = str(
            ensured[
                "session_id"
            ]
        )

        initial_requested_session_id = (
            requested_session_id
        )

        session_recovered = False
        recovery_from_session_id = None
        recovery_session_id = None
        recovery_runtime_result = None

        preturn_binding_persisted = False
        recovery_binding_persisted = False

        # Crash-consistency boundary:
        #
        # If this runtime session is newer than the
        # binding currently in active.yaml, persist it
        # BEFORE entering the runtime/model call.
        if (
            persist
            and persist_guard[
                "session_id"
            ] != requested_session_id
        ):
            try:
                working = (
                    self._persist_runtime_binding_guarded(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                # The runtime session was never made
                # durable in Forest, so a session created
                # by this call may safely be cleaned up.
                if ensured["created"]:
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [requested_session_id],
                        working,
                    )
                raise

            preturn_binding_persisted = True

            # Any later rotation CAS must now compare
            # against the binding we just committed.
            persist_guard = {
                "task_id":
                    persist_guard[
                        "task_id"
                    ],

                "adapter":
                    persist_guard[
                        "adapter"
                    ],

                "session_id":
                    requested_session_id,
            }

            # The guarded merge returns the newest
            # persisted Forest state. Re-resolve the
            # runtime adapter from that state.
            runtime_adapter = (
                self._runtime_adapter_for_state(
                    working
                )
            )

            current_adapter_name = (
                self._runtime_adapter_name(
                    runtime_adapter
                )
            )

            if (
                current_adapter_name
                != adapter_name
            ):
                raise TaskSessionError(
                    "Runtime adapter changed during "
                    "pre-turn binding persistence."
                )

        sender = getattr(
            runtime_adapter,
            "send_turn",
            None,
        )

        if not callable(
            sender
        ):
            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                "does not provide send_turn()."
            )

        try:
            result = sender(
                requested_session_id,
                message,
                working,
                instructions=instructions,
            )

        except Exception as exc:
            classifier = getattr(
                runtime_adapter,
                "is_stale_session_error",
                None,
            )

            stale_session = False

            if callable(
                classifier
            ):
                try:
                    stale_session = bool(
                        classifier(exc)
                    )
                except Exception:
                    stale_session = False

            if not stale_session:
                raise

            # ------------------------------------------
            # ONE-SHOT STALE SESSION RECOVERY
            # ------------------------------------------

            recovery_from_session_id = (
                requested_session_id
            )

            creator = getattr(
                runtime_adapter,
                "create_session",
                None,
            )

            if not callable(creator):
                raise TaskSessionError(
                    f"Runtime adapter {adapter_name!r} "
                    "cannot recover a stale session "
                    "because create_session() is unavailable."
                ) from exc

            active_task = (
                self._active_runtime_task(
                    working
                )
            )

            try:
                created = creator(
                    working,
                    task_id=active_task["id"],
                )

            except Exception as create_exc:
                raise TaskSessionError(
                    f"Runtime adapter "
                    f"{adapter_name!r} could not "
                    "create a replacement session: "
                    f"{create_exc}"
                ) from create_exc

            if not isinstance(created, dict):
                raise TaskSessionError(
                    "Replacement runtime-session "
                    "creation must return a mapping."
                )

            returned_adapter = created.get(
                "adapter",
                adapter_name,
            )

            if str(returned_adapter) != adapter_name:
                raise TaskSessionError(
                    "Replacement runtime session "
                    "returned a mismatched adapter."
                )

            replacement_session_id = (
                created.get("session_id")
            )

            if not replacement_session_id:
                raise TaskSessionError(
                    "Replacement runtime session "
                    "returned no session_id."
                )

            replacement_session_id = str(
                replacement_session_id
            )

            recovery_session_id = (
                replacement_session_id
            )

            recovery_runtime_result = created

            self._write_runtime_session_binding(
                working,
                adapter_name,
                replacement_session_id,
                previous_session_id=
                    recovery_from_session_id,
            )

            # Persist replacement before retrying.
            if persist:
                try:
                    working = (
                        self._persist_runtime_binding_guarded(
                            working,
                            persist_guard,
                        )
                    )

                except Exception:
                    # Replacement was never made durable.
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [replacement_session_id],
                        working,
                    )
                    raise

                recovery_binding_persisted = True

                # Any later rotation now compares against
                # the replacement, not the stale ID.
                persist_guard = {
                    "task_id":
                        persist_guard["task_id"],

                    "adapter":
                        persist_guard["adapter"],

                    "session_id":
                        replacement_session_id,
                }

                runtime_adapter = (
                    self._runtime_adapter_for_state(
                        working
                    )
                )

                current_adapter_name = (
                    self._runtime_adapter_name(
                        runtime_adapter
                    )
                )

                if current_adapter_name != adapter_name:
                    raise TaskSessionError(
                        "Runtime adapter changed during "
                        "stale-session recovery."
                    )

                sender = getattr(
                    runtime_adapter,
                    "send_turn",
                    None,
                )

                if not callable(sender):
                    raise TaskSessionError(
                        f"Runtime adapter "
                        f"{adapter_name!r} lost "
                        "send_turn() during recovery."
                    )

            requested_session_id = (
                replacement_session_id
            )

            session_recovered = True

            # Deliberately one-shot:
            # a second stale failure escapes.
            try:
                result = sender(
                    requested_session_id,
                    message,
                    working,
                    instructions=instructions,
                )

            except Exception:
                if not persist:
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [replacement_session_id],
                        working,
                    )

                raise

        if not isinstance(
            result,
            dict,
        ):
            raise TaskSessionError(
                "Runtime send_turn() must "
                "return a mapping."
            )

        returned_adapter = result.get(
            "adapter",
            adapter_name,
        )

        if str(
            returned_adapter
        ) != adapter_name:
            raise TaskSessionError(
                "Runtime turn returned a "
                "mismatched adapter."
            )

        effective_session_id = (
            result.get(
                "session_id"
            )
        )

        if not effective_session_id:
            raise TaskSessionError(
                "Runtime turn returned no "
                "effective session_id."
            )

        effective_session_id = str(
            effective_session_id
        )

        current_task = (
            self._active_runtime_task(
                working
            )
        )

        current_binding = (
            current_task[
                "runtime_sessions"
            ].get(
                adapter_name,
                {},
            )
        )

        previous_session_id = (
            current_binding.get(
                "previous_session_id"
            )
            if isinstance(
                current_binding,
                dict,
            )
            else None
        )

        rotated = (
            effective_session_id
            != requested_session_id
        )

        if rotated:
            previous_session_id = (
                requested_session_id
            )

        binding = (
            self._write_runtime_session_binding(
                working,
                adapter_name,
                effective_session_id,
                previous_session_id=
                    previous_session_id,
            )
        )

        rotation_binding_persisted = False

        if (
            persist
            and persist_guard is not None
            and persist_guard[
                "session_id"
            ] != binding[
                "session_id"
            ]
        ):
            try:
                working = (
                    self._persist_runtime_binding_guarded(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                # requested_session_id was already
                # durable. Only the uncommitted rotated
                # child is eligible for cleanup.
                if (
                    effective_session_id
                    != requested_session_id
                ):
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [effective_session_id],
                        working,
                    )
                raise

            rotation_binding_persisted = True

            binding = (
                self._active_runtime_task(
                    working
                )[
                    "runtime_sessions"
                ][
                    adapter_name
                ]
            )

        return {
            "state":
                working,

            "task_session":
                self.normalize_task_session(
                    working
                ),

            "adapter":
                adapter_name,

            "session_created":
                bool(
                    ensured[
                        "created"
                    ]
                    or session_recovered
                ),

            "initial_session_created":
                ensured[
                    "created"
                ],

            "session_reused":
                ensured[
                    "reused"
                ],

            "initial_requested_session_id":
                initial_requested_session_id,

            "requested_session_id":
                requested_session_id,

            "session_id":
                binding[
                    "session_id"
                ],

            "previous_session_id":
                binding[
                    "previous_session_id"
                ],

            "session_rotated":
                rotated,

            "binding_persisted":
                (
                    preturn_binding_persisted
                    or recovery_binding_persisted
                    or rotation_binding_persisted
                ),

            "binding_persisted_before_turn":
                preturn_binding_persisted,

            "session_recovered":
                session_recovered,

            "recovery_from_session_id":
                recovery_from_session_id,

            "recovery_session_id":
                recovery_session_id,

            "recovery_binding_persisted":
                recovery_binding_persisted,

            "recovery_runtime_result":
                recovery_runtime_result,

            "message":
                result.get(
                    "message",
                    "",
                ),

            "runtime_result":
                result,
        }

    @contextmanager
    def temporary_turn(
        self,
        temporary_capabilities,
        state=None,
        task_session=None,
    ):
        if state is None:
            state = self.load_state()

        if task_session is None:
            task_session = self.normalize_task_session(
                state
            )

        if (
            task_session.get("status") != "active"
            or not task_session.get("id")
        ):
            raise TaskSessionError(
                "A temporary turn requires an active "
                "Forest Task Session with a Task ID."
            )

        if temporary_capabilities is None:
            temporary_capabilities = []

        if not isinstance(
            temporary_capabilities,
            (list, tuple),
        ):
            raise TaskSessionError(
                "temporary_capabilities must be "
                "a list or tuple."
            )

        turn_session = dict(task_session)

        turn_session["temporary_capabilities"] = (
            self._unique(
                [
                    str(item)
                    for item in temporary_capabilities
                ]
            )
        )

        plan = self.plan_temporary_activation(
            state=state,
            task_session=turn_session,
        )

        # Build prompt layers before changing Hermes.
        # If Skill preparation fails, the runtime
        # remains untouched.
        overlay = self.prepare_turn_skill_overlay(
            state=state,
            task_session=turn_session,
            plan=plan,
        )

        transaction = None
        turn_runtime_adapter = (
            self._runtime_adapter_for_state(
                state
            )
        )

        try:
            if plan["runtime_toolsets"]:
                try:
                    transaction = (
                        turn_runtime_adapter
                        .begin_temporary_toolsets(
                            plan["runtime_toolsets"],
                            state,
                        )
                    )

                except TaskSessionError:
                    raise

                except Exception as exc:
                    adapter_name = getattr(
                        turn_runtime_adapter,
                        "adapter_name",
                        type(
                            turn_runtime_adapter
                        ).__name__,
                    )

                    raise TaskSessionError(
                        f"Runtime adapter "
                        f"{adapter_name!r} could not "
                        f"begin temporary toolsets: "
                        f"{exc}"
                    ) from exc

            yield {
                "task_session": turn_session,
                "plan": plan,
                "overlay": overlay,
                "transaction": transaction,
            }

        finally:
            if transaction is not None:
                try:
                    (
                        turn_runtime_adapter
                        .restore_temporary_toolsets(
                            transaction,
                            state,
                        )
                    )

                except TaskSessionError:
                    raise

                except Exception as exc:
                    adapter_name = getattr(
                        turn_runtime_adapter,
                        "adapter_name",
                        type(
                            turn_runtime_adapter
                        ).__name__,
                    )

                    raise TaskSessionError(
                        f"Runtime adapter "
                        f"{adapter_name!r} could not "
                        f"restore temporary toolsets: "
                        f"{exc}"
                    ) from exc

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

        prompt = self._build_runtime_skill_overlay(
            state,
            adapter_name,
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

        prompt = self._build_runtime_skill_overlay(
            state,
            adapter_name,
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
