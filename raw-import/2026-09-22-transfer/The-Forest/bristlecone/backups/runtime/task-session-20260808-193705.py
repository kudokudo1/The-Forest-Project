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
        self._overlay_build_count = 0
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

        keys = [
            key
            for key in self._skill_overlay_cache
            if key[0] == task_id
        ]

        for key in keys:
            del self._skill_overlay_cache[key]

        return len(keys)

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
