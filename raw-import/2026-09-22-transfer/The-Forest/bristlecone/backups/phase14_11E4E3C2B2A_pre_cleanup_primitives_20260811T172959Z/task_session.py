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


# Keep Bristlecone-owned packages importable whether this module
# is imported normally or executed directly as a script.
_BRISTLECONE_ROOT = Path(__file__).resolve().parents[1]
_BRISTLECONE_ROOT_TEXT = str(_BRISTLECONE_ROOT)

if _BRISTLECONE_ROOT_TEXT not in sys.path:
    sys.path.insert(0, _BRISTLECONE_ROOT_TEXT)

from cache import CacheCoordinator, CacheKey
from threading import RLock
from learning.context_state import ContextRouteState
from runtime.session_store import (
    RuntimeSessionStoreError,
    get_runtime_session_binding,
    normalize_runtime_sessions,
    runtime_session_adapters,
    set_runtime_session_binding,
)

from model_form import (
    FrozenModelFormTurn,
    ModelBindingRegistryError,
    ModelFormControlError,
    ModelFormResolutionError,
    model_binding_registry_from_mapping,
    model_form_control_from_mapping,
    resolve_model_form_turn,
)


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
        self._cache_coordinator = CacheCoordinator()

        # Ephemeral Context Route State is Task-local.
        # The manager may own more than one Task over its
        # lifetime, so one global route state would allow
        # unrelated Tasks to contaminate one another.
        self._context_route_states_lock = RLock()
        self._context_route_states = {}

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

        self.model_binding_registry_file = (
            self.forest
            / "model_form"
            / "bindings.yaml"
        )

    def _context_route_state_for_task(
        self,
        task_id,
    ):
        """Return the ephemeral route state for one Task.

        Route state is created lazily so inactive or merely
        persisted Tasks consume no Context Route State memory.
        """

        if (
            not isinstance(
                task_id,
                str,
            )
            or not task_id.strip()
        ):
            raise TaskSessionError(
                "Context Route State requires "
                "a non-empty Task ID."
            )

        with self._context_route_states_lock:
            state = self._context_route_states.get(
                task_id
            )

            if state is None:
                state = ContextRouteState()

                self._context_route_states[
                    task_id
                ] = state

            return state


    def _discard_context_route_state(
        self,
        task_id,
    ):
        """Discard one ended Task's ephemeral context."""

        if (
            not isinstance(
                task_id,
                str,
            )
            or not task_id.strip()
        ):
            raise TaskSessionError(
                "Context Route State discard requires "
                "a non-empty Task ID."
            )

        with self._context_route_states_lock:
            state = self._context_route_states.pop(
                task_id,
                None,
            )

        if state is None:
            return False

        state.clear_all()

        return True


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

    def load_model_binding_registry(self):
        """Load the runtime-neutral Model Binding Registry."""

        try:
            raw = self._load_yaml(
                self.model_binding_registry_file
            )

            return (
                model_binding_registry_from_mapping(
                    raw
                )
            )

        except ModelBindingRegistryError as exc:
            raise TaskSessionError(
                "Forest Model Binding Registry "
                f"is invalid: {exc}"
            ) from exc

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

    def _normalize_spring_restoration_decision(
        self,
        raw,
    ):
        """Normalize one durable Spring restoration decision."""

        if raw is None:
            return None

        if not isinstance(
            raw,
            dict,
        ):
            raise TaskSessionError(
                "Spring restoration decision "
                "must be a mapping or null."
            )

        restore = raw.get(
            "restore",
            {},
        )

        leave_dormant = raw.get(
            "leave_dormant",
            {},
        )

        if not isinstance(
            restore,
            dict,
        ):
            raise TaskSessionError(
                "Spring restore selection "
                "must be a mapping."
            )

        if not isinstance(
            leave_dormant,
            dict,
        ):
            raise TaskSessionError(
                "Spring leave_dormant selection "
                "must be a mapping."
            )

        def clean_list(
            mapping,
            key,
        ):
            value = mapping.get(
                key,
                [],
            )

            if value is None:
                return []

            if not isinstance(
                value,
                list,
            ):
                raise TaskSessionError(
                    f"Spring decision {key} "
                    "must be a list."
                )

            return list(
                dict.fromkeys(
                    str(item)
                    for item in value
                    if str(item).strip()
                )
            )

        restore_workshop = restore.get(
            "workshop"
        )

        if (
            restore_workshop is not None
            and not isinstance(
                restore_workshop,
                str,
            )
        ):
            raise TaskSessionError(
                "Spring restore workshop "
                "must be a string or null."
            )

        dormant_workshop = (
            leave_dormant.get(
                "workshop"
            )
        )

        if (
            dormant_workshop is not None
            and not isinstance(
                dormant_workshop,
                str,
            )
        ):
            raise TaskSessionError(
                "Spring dormant workshop "
                "must be a string or null."
            )

        return {
            "decided_at":
                raw.get(
                    "decided_at"
                ),

            "restore": {
                "workshop":
                    restore_workshop,

                "general_capabilities":
                    clean_list(
                        restore,
                        "general_capabilities",
                    ),

                "ready_capabilities":
                    clean_list(
                        restore,
                        "ready_capabilities",
                    ),

                "temporary_capabilities":
                    clean_list(
                        restore,
                        "temporary_capabilities",
                    ),
            },

            "leave_dormant": {
                "workshop":
                    dormant_workshop,

                "general_capabilities":
                    clean_list(
                        leave_dormant,
                        "general_capabilities",
                    ),

                "ready_capabilities":
                    clean_list(
                        leave_dormant,
                        "ready_capabilities",
                    ),

                "temporary_capabilities":
                    clean_list(
                        leave_dormant,
                        "temporary_capabilities",
                    ),

                "reasoning":
                    leave_dormant.get(
                        "reasoning"
                    ),

                "model_form":
                    leave_dormant.get(
                        "model_form"
                    ),
            },
        }

    def _normalize_spring_restoration_application(
        self,
        raw,
    ):
        """Normalize verified Spring restoration reality."""

        if raw is None:
            return None

        if not isinstance(
            raw,
            dict,
        ):
            raise TaskSessionError(
                "Spring restoration application "
                "must be a mapping or null."
            )

        status = raw.get(
            "status",
            "verified",
        )

        if not isinstance(
            status,
            str,
        ):
            raise TaskSessionError(
                "Spring restoration application "
                "status must be a string."
            )

        status = (
            status
            .strip()
            .lower()
        )

        if status != "verified":
            raise TaskSessionError(
                "Unsupported Spring restoration "
                f"application status: {status!r}."
            )

        def clean_list(
            key,
        ):
            value = raw.get(
                key,
                [],
            )

            if value is None:
                return []

            if not isinstance(
                value,
                list,
            ):
                raise TaskSessionError(
                    "Spring restoration application "
                    f"{key} must be a list."
                )

            return self._unique(
                [
                    str(item)
                    for item in value
                    if str(item).strip()
                ]
            )

        workshop = raw.get(
            "workshop"
        )

        if (
            workshop is not None
            and not isinstance(
                workshop,
                str,
            )
        ):
            raise TaskSessionError(
                "Spring restoration application "
                "workshop must be a string or null."
            )

        adapter = raw.get(
            "adapter"
        )

        if (
            adapter is not None
            and not isinstance(
                adapter,
                str,
            )
        ):
            raise TaskSessionError(
                "Spring restoration application "
                "adapter must be a string or null."
            )

        raw_bindings = raw.get(
            "skill_bindings",
            [],
        )

        if raw_bindings is None:
            raw_bindings = []

        if not isinstance(
            raw_bindings,
            list,
        ):
            raise TaskSessionError(
                "Spring restoration application "
                "skill_bindings must be a list."
            )

        skill_bindings = []

        for binding in raw_bindings:
            if not isinstance(
                binding,
                dict,
            ):
                raise TaskSessionError(
                    "Spring restoration application "
                    "Skill bindings must be mappings."
                )

            canonical_id = binding.get(
                "canonical_id"
            )

            runtime_id = binding.get(
                "runtime_id"
            )

            binding_adapter = binding.get(
                "adapter"
            )

            if not (
                isinstance(
                    canonical_id,
                    str,
                )
                and canonical_id.strip()
            ):
                raise TaskSessionError(
                    "Spring Skill binding has no "
                    "canonical_id."
                )

            if not (
                isinstance(
                    runtime_id,
                    str,
                )
                and runtime_id.strip()
            ):
                raise TaskSessionError(
                    "Spring Skill binding has no "
                    "runtime_id."
                )

            if not (
                isinstance(
                    binding_adapter,
                    str,
                )
                and binding_adapter.strip()
            ):
                raise TaskSessionError(
                    "Spring Skill binding has no "
                    "adapter."
                )

            skill_bindings.append(
                {
                    "canonical_id":
                        canonical_id.strip(),

                    "runtime_id":
                        runtime_id.strip(),

                    "adapter":
                        binding_adapter.strip(),
                }
            )

        return {
            "status":
                "verified",

            "applied_at":
                raw.get(
                    "applied_at"
                ),

            "decision_decided_at":
                raw.get(
                    "decision_decided_at"
                ),

            "adapter":
                (
                    adapter.strip()
                    if isinstance(
                        adapter,
                        str,
                    )
                    else None
                ),

            "workshop":
                (
                    workshop.strip()
                    if isinstance(
                        workshop,
                        str,
                    )
                    else None
                ),

            "general_capabilities":
                clean_list(
                    "general_capabilities"
                ),

            "ready_capabilities":
                clean_list(
                    "ready_capabilities"
                ),

            "temporary_capabilities":
                clean_list(
                    "temporary_capabilities"
                ),

            "canonical_active_ids":
                clean_list(
                    "canonical_active_ids"
                ),

            "runtime_toolsets":
                clean_list(
                    "runtime_toolsets"
                ),

            "runtime_skills":
                clean_list(
                    "runtime_skills"
                ),

            "task_sticky_skills":
                clean_list(
                    "task_sticky_skills"
                ),

            "skill_bindings":
                skill_bindings,
        }

    def _normalize_spring_cleaning(
        self,
        raw,
    ):
        """Normalize durable Spring Cleaning metadata."""

        spring = raw.get(
            "spring_cleaning"
        )

        if spring is None:
            return None

        if not isinstance(
            spring,
            dict,
        ):
            raise TaskSessionError(
                "task_session.spring_cleaning "
                "must be a mapping or null."
            )

        status = spring.get(
            "status",
            "cleaning",
        )

        if not isinstance(
            status,
            str,
        ):
            raise TaskSessionError(
                "Spring Cleaning status must "
                "be a string."
            )

        status = status.strip().lower()

        allowed_statuses = {
            "cleaning",
            "completed",
        }

        if status not in allowed_statuses:
            raise TaskSessionError(
                "Unsupported Spring Cleaning "
                f"status: {status}"
            )

        snapshot = spring.get(
            "activation_snapshot",
            {},
        )

        if snapshot is None:
            snapshot = {}

        if not isinstance(
            snapshot,
            dict,
        ):
            raise TaskSessionError(
                "Spring activation_snapshot "
                "must be a mapping."
            )

        return {
            "status":
                status,

            "started_at":
                spring.get(
                    "started_at"
                ),

            "completed_at":
                spring.get(
                    "completed_at"
                ),

            "source_retired_at":
                spring.get(
                    "source_retired_at"
                ),

            "restoration_decision":
                self._normalize_spring_restoration_decision(
                    spring.get(
                        "restoration_decision"
                    )
                ),

            "restoration_application":
                self._normalize_spring_restoration_application(
                    spring.get(
                        "restoration_application"
                    )
                ),

            "activation_snapshot":
                copy.deepcopy(
                    snapshot
                ),
        }


    @staticmethod
    def _normalize_effective_model_forms(
        raw,
    ):
        """Normalize successful Model Form by context.

        This is Forest semantic state, not runtime-session
        state.

        A value may enter this mapping only after a
        successful meaningful turn.
        """

        from model_form import (
            ModelFormError,
            normalize_resolved_model_form,
        )

        if raw is None:
            raw = {}

        if not isinstance(
            raw,
            dict,
        ):
            raise TaskSessionError(
                "effective_model_forms "
                "must be a mapping."
            )

        result = {}

        for (
            raw_context_id,
            raw_form,
        ) in raw.items():
            if not isinstance(
                raw_context_id,
                str,
            ):
                raise TaskSessionError(
                    "effective_model_forms "
                    "context IDs must be strings."
                )

            context_id = (
                raw_context_id.strip()
            )

            if not context_id:
                raise TaskSessionError(
                    "effective_model_forms "
                    "context ID cannot be empty."
                )

            if context_id in result:
                raise TaskSessionError(
                    "effective_model_forms contains "
                    "duplicate normalized context IDs."
                )

            try:
                form = (
                    normalize_resolved_model_form(
                        raw_form
                    )
                )

            except ModelFormError as exc:
                raise TaskSessionError(
                    "effective_model_forms values "
                    "must resolve to Small or Big."
                ) from exc

            result[
                context_id
            ] = form

        return result


    @staticmethod
    def _normalize_conversation_continuity(
        raw,
        *,
        task_id,
    ):
        """Normalize Forest-owned conversation by context.

        Entries contain only completed public exchanges.
        Runtime/session/model state is not represented here.
        """

        from runtime.conversation_continuity import (
            CONVERSATION_CONTINUITY_SCHEMA_VERSION,
            ConversationContinuity,
            ConversationContinuityError,
            ConversationExchange,
        )

        if raw is None:
            raw = {}

        if not isinstance(
            raw,
            dict,
        ):
            raise TaskSessionError(
                "conversation_continuity "
                "must be a mapping."
            )

        if raw:
            if (
                not isinstance(
                    task_id,
                    str,
                )
                or not task_id.strip()
            ):
                raise TaskSessionError(
                    "conversation_continuity "
                    "requires Task identity."
                )

            canonical_task_id = (
                task_id.strip()
            )

        else:
            canonical_task_id = (
                task_id.strip()
                if isinstance(
                    task_id,
                    str,
                )
                and task_id.strip()
                else None
            )

        result = {}

        for (
            raw_context_id,
            entry,
        ) in raw.items():
            if not isinstance(
                raw_context_id,
                str,
            ):
                raise TaskSessionError(
                    "conversation_continuity "
                    "context IDs must be strings."
                )

            context_id = (
                raw_context_id.strip()
            )

            if not context_id:
                raise TaskSessionError(
                    "conversation_continuity "
                    "context ID cannot be empty."
                )

            if context_id in result:
                raise TaskSessionError(
                    "conversation_continuity contains "
                    "duplicate normalized context IDs."
                )

            if not isinstance(
                entry,
                dict,
            ):
                raise TaskSessionError(
                    "Each conversation_continuity "
                    "entry must be a mapping."
                )

            schema_version = entry.get(
                "schema_version",
                CONVERSATION_CONTINUITY_SCHEMA_VERSION,
            )

            entry_context_id = entry.get(
                "execution_context_id",
                context_id,
            )

            entry_task_id = entry.get(
                "task_id",
                canonical_task_id,
            )

            if (
                not isinstance(
                    entry_context_id,
                    str,
                )
                or entry_context_id.strip()
                != context_id
            ):
                raise TaskSessionError(
                    "Conversation continuity "
                    "execution-context identity "
                    "does not match its key."
                )

            if (
                canonical_task_id is None
                or not isinstance(
                    entry_task_id,
                    str,
                )
                or entry_task_id.strip()
                != canonical_task_id
            ):
                raise TaskSessionError(
                    "Conversation continuity "
                    "Task identity does not match "
                    "the active TaskSession."
                )

            raw_exchanges = entry.get(
                "exchanges",
                [],
            )

            if not isinstance(
                raw_exchanges,
                (list, tuple),
            ):
                raise TaskSessionError(
                    "Conversation continuity "
                    "exchanges must be a list."
                )

            exchanges = []

            for raw_exchange in raw_exchanges:
                if not isinstance(
                    raw_exchange,
                    dict,
                ):
                    raise TaskSessionError(
                        "Each conversation exchange "
                        "must be a mapping."
                    )

                if set(
                    raw_exchange
                ) != {
                    "user_message",
                    "assistant_message",
                }:
                    raise TaskSessionError(
                        "Conversation exchange contains "
                        "unexpected or missing fields."
                    )

                try:
                    exchanges.append(
                        ConversationExchange(
                            user_message=(
                                raw_exchange[
                                    "user_message"
                                ]
                            ),
                            assistant_message=(
                                raw_exchange[
                                    "assistant_message"
                                ]
                            ),
                        )
                    )

                except ConversationContinuityError as exc:
                    raise TaskSessionError(
                        "Conversation continuity "
                        f"exchange is invalid: {exc}"
                    ) from exc

            try:
                continuity = (
                    ConversationContinuity(
                        execution_context_id=(
                            context_id
                        ),
                        task_id=(
                            canonical_task_id
                        ),
                        exchanges=tuple(
                            exchanges
                        ),
                        schema_version=(
                            schema_version
                        ),
                    )
                )

            except ConversationContinuityError as exc:
                raise TaskSessionError(
                    "Conversation continuity "
                    f"is invalid: {exc}"
                ) from exc

            result[
                context_id
            ] = {
                "schema_version":
                    continuity.schema_version,

                "execution_context_id":
                    continuity.execution_context_id,

                "task_id":
                    continuity.task_id,

                "exchanges": [
                    {
                        "user_message":
                            exchange.user_message,

                        "assistant_message":
                            exchange.assistant_message,
                    }
                    for exchange
                    in continuity.exchanges
                ],
            }

        return result


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

        if not isinstance(
            raw_runtime_sessions,
            dict,
        ):
            raise TaskSessionError(
                "runtime_sessions must be a mapping."
            )

        # Canonical 14.11D+ storage:
        #
        # execution_context_id
        #   -> binding_id
        #       -> runtime session entry
        #
        # During the cutover, legacy adapter-keyed
        # storage remains readable so an old persisted
        # Task cannot be silently misinterpreted.
        runtime_sessions = {}

        if raw_runtime_sessions:
            canonical_error = None

            try:
                runtime_sessions = (
                    normalize_runtime_sessions(
                        raw_runtime_sessions
                    )
                )

            except RuntimeSessionStoreError as exc:
                canonical_error = exc

                legacy_shape = all(
                    isinstance(entry, dict)
                    and "session_id" in entry
                    and not isinstance(
                        entry.get("session_id"),
                        dict,
                    )
                    for entry
                    in raw_runtime_sessions.values()
                )

                if not legacy_shape:
                    raise TaskSessionError(
                        "runtime_sessions is neither "
                        "canonical context+binding "
                        "storage nor recognized legacy "
                        "adapter-keyed storage."
                    ) from canonical_error

                legacy_sessions = {}

                for adapter_name, entry in (
                    raw_runtime_sessions.items()
                ):
                    adapter_name = str(
                        adapter_name
                    ).strip()

                    if not adapter_name:
                        raise TaskSessionError(
                            "Legacy runtime session "
                            "adapter name cannot be empty."
                        )

                    session_id = entry.get(
                        "session_id"
                    )

                    previous_session_id = (
                        entry.get(
                            "previous_session_id"
                        )
                    )

                    legacy_sessions[
                        adapter_name
                    ] = {
                        "session_id": (
                            str(session_id)
                            if session_id is not None
                            else None
                        ),

                        "previous_session_id": (
                            str(previous_session_id)
                            if (
                                previous_session_id
                                is not None
                            )
                            else None
                        ),

                        "updated_at":
                            entry.get(
                                "updated_at"
                            ),
                    }

                runtime_sessions = legacy_sessions

        return {
            "id": raw.get("id"),
            "status": raw.get("status", "inactive"),
            "lifecycle":
                self._normalize_task_lifecycle(
                    raw
                ),
            "spring_cleaning":
                self._normalize_spring_cleaning(
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

            "runtime_sessions":
                runtime_sessions,

            "effective_model_forms":
                self._normalize_effective_model_forms(
                    raw.get(
                        "effective_model_forms",
                        {},
                    )
                ),

            "conversation_continuity":
                self._normalize_conversation_continuity(
                    raw.get(
                        "conversation_continuity",
                        {},
                    ),
                    task_id=raw.get(
                        "id"
                    ),
                ),
        }

    @staticmethod
    def _effective_model_form_context_id(
        execution_context_id,
    ):
        """Normalize explicit execution-context identity."""

        if (
            not isinstance(
                execution_context_id,
                str,
            )
            or not execution_context_id.strip()
        ):
            raise TaskSessionError(
                "Effective Model Form access "
                "requires an explicit non-empty "
                "execution_context_id."
            )

        return execution_context_id.strip()


    def _effective_model_form_for_context(
        self,
        state,
        execution_context_id,
    ):
        """Read last successfully effective form.

        Returns Small, Big, or None.

        This helper performs no mutation, persistence,
        runtime I/O, or handoff detection.
        """

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        context_id = (
            self._effective_model_form_context_id(
                execution_context_id
            )
        )

        task = self.normalize_task_session(
            state
        )

        forms = task[
            "effective_model_forms"
        ]

        form = forms.get(
            context_id
        )

        if form is None:
            return None

        # normalize_task_session already validated
        # this value. Return the canonical value.
        return form


    def _write_effective_model_form_for_context(
        self,
        state,
        execution_context_id,
        form,
    ):
        """Return detached state with one effective form set.

        This is a state transformation only.

        The caller decides WHEN a Model Form becomes
        authoritative. The live send path must call this
        only after successful model execution.

        No persistence or runtime work occurs here.
        """

        from model_form import (
            ModelFormError,
            normalize_resolved_model_form,
        )

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        context_id = (
            self._effective_model_form_context_id(
                execution_context_id
            )
        )

        try:
            canonical_form = (
                normalize_resolved_model_form(
                    form
                )
            )

        except ModelFormError as exc:
            raise TaskSessionError(
                "Effective Model Form must "
                "resolve to Small or Big."
            ) from exc

        working = copy.deepcopy(
            state
        )

        task = self.normalize_task_session(
            working
        )

        task_id = task.get(
            "id"
        )

        if (
            not isinstance(
                task_id,
                str,
            )
            or not task_id.strip()
        ):
            raise TaskSessionError(
                "Effective Model Form history "
                "requires Task identity."
            )

        forms = copy.deepcopy(
            task[
                "effective_model_forms"
            ]
        )

        previous_form = forms.get(
            context_id
        )

        forms[
            context_id
        ] = canonical_form

        task[
            "effective_model_forms"
        ] = forms

        working[
            "task_session"
        ] = task

        return {
            "state":
                working,

            "execution_context_id":
                context_id,

            "task_id":
                task_id.strip(),

            "previous_form":
                previous_form,

            "form":
                canonical_form,

            "changed":
                previous_form
                != canonical_form,
        }


    def _conversation_continuity_for_context(
        self,
        state,
        execution_context_id,
    ):
        """Read immutable completed conversation for a context.

        An unseen context returns an empty continuity baseline.

        This helper performs no mutation, persistence,
        runtime I/O, replay, or handoff work.
        """

        from runtime.conversation_continuity import (
            ConversationContinuity,
            ConversationExchange,
        )

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        context_id = (
            self._effective_model_form_context_id(
                execution_context_id
            )
        )

        task = self.normalize_task_session(
            state
        )

        task_id = task.get(
            "id"
        )

        if (
            not isinstance(
                task_id,
                str,
            )
            or not task_id.strip()
        ):
            raise TaskSessionError(
                "Conversation continuity access "
                "requires Task identity."
            )

        task_id = task_id.strip()

        entry = (
            task[
                "conversation_continuity"
            ].get(
                context_id
            )
        )

        if entry is None:
            return ConversationContinuity(
                execution_context_id=(
                    context_id
                ),
                task_id=task_id,
                exchanges=(),
            )

        exchanges = tuple(
            ConversationExchange(
                user_message=(
                    raw_exchange[
                        "user_message"
                    ]
                ),
                assistant_message=(
                    raw_exchange[
                        "assistant_message"
                    ]
                ),
            )
            for raw_exchange
            in entry[
                "exchanges"
            ]
        )

        return ConversationContinuity(
            execution_context_id=(
                context_id
            ),
            task_id=task_id,
            exchanges=exchanges,
            schema_version=(
                entry[
                    "schema_version"
                ]
            ),
        )


    def _append_conversation_exchange_for_context(
        self,
        state,
        execution_context_id,
        user_message,
        assistant_message,
    ):
        """Return detached state with one completed exchange appended.

        This is a state transformation only.

        The caller decides WHEN an exchange is complete.
        The live send path must invoke this only after
        successful model execution.

        No persistence, runtime I/O, replay, or handoff
        work occurs here.
        """

        from runtime.conversation_continuity import (
            ConversationContinuity,
            ConversationContinuityError,
            ConversationExchange,
        )

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        context_id = (
            self._effective_model_form_context_id(
                execution_context_id
            )
        )

        working = copy.deepcopy(
            state
        )

        task = self.normalize_task_session(
            working
        )

        task_id = task.get(
            "id"
        )

        if (
            not isinstance(
                task_id,
                str,
            )
            or not task_id.strip()
        ):
            raise TaskSessionError(
                "Conversation continuity history "
                "requires Task identity."
            )

        task_id = task_id.strip()

        try:
            exchange = ConversationExchange(
                user_message=user_message,
                assistant_message=(
                    assistant_message
                ),
            )

        except ConversationContinuityError as exc:
            raise TaskSessionError(
                "Completed conversation exchange "
                f"is invalid: {exc}"
            ) from exc

        existing = (
            self._conversation_continuity_for_context(
                working,
                context_id,
            )
        )

        if existing.task_id != task_id:
            raise TaskSessionError(
                "Conversation continuity crossed "
                "Task identity."
            )

        if (
            existing.execution_context_id
            != context_id
        ):
            raise TaskSessionError(
                "Conversation continuity crossed "
                "execution-context identity."
            )

        updated = ConversationContinuity(
            execution_context_id=(
                context_id
            ),
            task_id=task_id,
            exchanges=(
                existing.exchanges
                + (
                    exchange,
                )
            ),
        )

        conversations = copy.deepcopy(
            task[
                "conversation_continuity"
            ]
        )

        conversations[
            context_id
        ] = {
            "schema_version":
                updated.schema_version,

            "execution_context_id":
                updated.execution_context_id,

            "task_id":
                updated.task_id,

            "exchanges": [
                {
                    "user_message":
                        item.user_message,

                    "assistant_message":
                        item.assistant_message,
                }
                for item
                in updated.exchanges
            ],
        }

        task[
            "conversation_continuity"
        ] = conversations

        working[
            "task_session"
        ] = task

        return {
            "state":
                working,

            "execution_context_id":
                context_id,

            "task_id":
                task_id,

            "previous_exchange_count":
                existing.exchange_count,

            "exchange_count":
                updated.exchange_count,

            "exchange":
                exchange,

            "continuity":
                updated,
        }


    def _prepare_model_form_handoff_continuity(
        self,
        *,
        state,
        frozen_turn,
        previous_form,
        instruction_composition,
    ):
        """Prepare portable continuity for an actual form change.

        Preparation only:

        - no runtime I/O
        - no runtime-session creation
        - no persistence
        - no conversation replay
        - no current-turn conversation append

        The current meaningful turn is added to Forest-owned
        conversation only after successful runtime execution.
        """

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Model Form handoff preparation "
                "requires Forest state."
            )

        if not isinstance(
            frozen_turn,
            FrozenModelFormTurn,
        ):
            raise TaskSessionError(
                "Model Form handoff preparation "
                "requires a FrozenModelFormTurn."
            )

        context_id = (
            self._effective_model_form_context_id(
                frozen_turn.execution_context_id
            )
        )

        expected_task_id = str(
            frozen_turn.task_id
            or ""
        ).strip()

        if not expected_task_id:
            raise TaskSessionError(
                "Model Form handoff preparation "
                "requires frozen Task identity."
            )

        active_task = (
            self._active_runtime_task(
                state
            )
        )

        if (
            str(active_task["id"]).strip()
            != expected_task_id
        ):
            raise TaskSessionError(
                "Model Form handoff preparation "
                "crossed Task identity."
            )

        try:
            from model_form.handoff_detection import (
                detect_model_form_handoff,
            )

            handoff = (
                detect_model_form_handoff(
                    previous_form,
                    frozen_turn,
                )
            )

        except (
            TypeError,
            ValueError,
        ) as exc:
            raise TaskSessionError(
                "Could not detect Model Form handoff."
            ) from exc

        # First successful form establishes a baseline.
        # Same-form execution is also not a handoff.
        if handoff is None:
            return {
                "handoff":
                    None,

                "continuity":
                    None,

                "previous_form":
                    previous_form,

                "form":
                    frozen_turn.form,

                "requires_runtime_bootstrap":
                    False,
            }

        try:
            from turn_composition import (
                ForestTurnInstructionComposition,
            )

        except Exception as exc:
            raise TaskSessionError(
                "Forest turn-composition backend "
                "is unavailable."
            ) from exc

        if not isinstance(
            instruction_composition,
            ForestTurnInstructionComposition,
        ):
            raise TaskSessionError(
                "An actual Model Form handoff "
                "requires the exact frozen "
                "ForestTurnInstructionComposition."
            )

        conversation = (
            self._conversation_continuity_for_context(
                state,
                context_id,
            )
        )

        if (
            conversation.execution_context_id
            != context_id
            or conversation.task_id
            != expected_task_id
        ):
            raise TaskSessionError(
                "Portable conversation continuity "
                "does not match the handoff identity."
            )

        try:
            from model_form.continuity import (
                ModelFormContinuity,
            )

            continuity = (
                ModelFormContinuity(
                    execution_context_id=
                        context_id,

                    task_id=
                        expected_task_id,

                    turn_instructions=
                        instruction_composition,

                    conversation=
                        conversation,
                )
            )

        except (
            TypeError,
            ValueError,
        ) as exc:
            raise TaskSessionError(
                "Could not prepare Model Form "
                "portable continuity."
            ) from exc

        return {
            "handoff":
                handoff,

            "continuity":
                continuity,

            "previous_form":
                handoff.from_form,

            "form":
                handoff.to_form,

            "requires_runtime_bootstrap":
                True,
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

        for cache_type in (
            "skill-overlay",
            "temporary-skill-overlay",
        ):
            discarded += self._cache_coordinator.invalidate(
                cache_type=cache_type,
                identity_prefix=(task_id,),
            )

        return discarded

    def apply_spring_restoration(
        self,
        state=None,
        persist=False,
    ):
        """Apply and verify a durable Spring decision.

        Persistent application follows the truth boundary:

            durable decision
                -> resolve desired working set
                -> apply runtime exactly
                -> verify runtime reality
                -> commit Forest state
                -> record verified application

        Spring remains in Cleaning after this method.
        """

        if state is None:
            state = self.load_state()

        def active_list(
            source_state,
            key,
        ):
            value = source_state.get(
                key,
                [],
            )

            if value is None:
                return []

            if not isinstance(
                value,
                list,
            ):
                raise TaskSessionError(
                    f"state.{key} must be a list."
                )

            return self._unique(
                [
                    str(item)
                    for item in value
                    if str(item).strip()
                ]
            )

        def build_application_plan(
            source_state,
        ):
            task = self.normalize_task_session(
                source_state
            )

            if (
                task.get(
                    "status"
                )
                != "active"
                or task[
                    "lifecycle"
                ][
                    "season"
                ]
                != "spring"
            ):
                raise TaskSessionError(
                    "Spring restoration application "
                    "requires an active Spring Task."
                )

            cleaning = task.get(
                "spring_cleaning"
            )

            if not isinstance(
                cleaning,
                dict,
            ):
                raise TaskSessionError(
                    "Spring Task has no "
                    "Cleaning worksheet."
                )

            decision = (
                self._normalize_spring_restoration_decision(
                    cleaning.get(
                        "restoration_decision"
                    )
                )
            )

            if decision is None:
                raise TaskSessionError(
                    "Spring restoration has not "
                    "been decided yet."
                )

            restore = decision[
                "restore"
            ]

            restore_temporary = list(
                restore[
                    "temporary_capabilities"
                ]
            )

            # Spring may restore temporary capability
            # authorization, but Spring itself does not
            # activate those resources.
            #
            # Temporary toolsets are activated only by
            # temporary_turn() and restored afterward.
            # Temporary Skills remain turn-scoped overlays.

            current_workshop = (
                source_state.get(
                    "workshop"
                )
            )

            restore_workshop = (
                restore.get(
                    "workshop"
                )
            )

            target_workshop = (
                restore_workshop
                if restore_workshop
                is not None
                else current_workshop
            )

            if not (
                isinstance(
                    target_workshop,
                    str,
                )
                and target_workshop.strip()
            ):
                raise TaskSessionError(
                    "Spring restoration has no "
                    "usable target Workshop."
                )

            target_workshop = (
                target_workshop.strip()
            )

            current_general = active_list(
                source_state,
                "active_general",
            )

            restore_general = list(
                restore[
                    "general_capabilities"
                ]
            )

            target_general = self._unique(
                current_general
                + restore_general
            )

            current_ready = active_list(
                source_state,
                "active_ready",
            )

            restore_ready = list(
                restore[
                    "ready_capabilities"
                ]
            )

            # Ready racks belong to Workshops.
            # If Spring changes Workshops, Ready items
            # from the old Workshop cannot simply leak
            # into the restored one.
            if (
                restore_workshop is not None
                and target_workshop
                != current_workshop
            ):
                target_ready = self._unique(
                    restore_ready
                )

            else:
                target_ready = self._unique(
                    current_ready
                    + restore_ready
                )

            runtime = source_state.get(
                "runtime",
                {},
            )

            if not isinstance(
                runtime,
                dict,
            ):
                raise TaskSessionError(
                    "state.runtime must be a mapping."
                )

            adapter_name = runtime.get(
                "adapter"
            )

            if not (
                isinstance(
                    adapter_name,
                    str,
                )
                and adapter_name.strip()
            ):
                raise TaskSessionError(
                    "No runtime adapter is configured."
                )

            adapter_name = adapter_name.strip()

            try:
                from capabilities.resolver import (
                    ForestCapabilityResolver,
                    CapabilityResolutionError,
                )

            except ImportError as exc:
                raise TaskSessionError(
                    "Forest capability resolver "
                    "could not be imported."
                ) from exc

            resolver = ForestCapabilityResolver(
                self.forest,
                cache_coordinator=(
                    self._cache_coordinator
                ),
            )

            try:
                resolution = resolver.resolve(
                    target_workshop,
                    general=target_general,
                    ready=target_ready,
                    adapter_name=adapter_name,
                    require_resolved=True,
                )

            except CapabilityResolutionError as exc:
                raise TaskSessionError(
                    "Spring restoration capability "
                    f"resolution failed: {exc}"
                ) from exc

            restored_skill_ids = [
                binding[
                    "canonical_id"
                ]
                for binding in resolution[
                    "runtime"
                ][
                    "skill_bindings"
                ]
            ]

            final_task_sticky = (
                self._unique(
                    list(
                        task[
                            "task_sticky_skills"
                        ]
                    )
                    + restored_skill_ids
                )
            )

            # ------------------------------------------
            # EARLY TEMPORARY CAPABILITY VALIDATION
            # ------------------------------------------
            #
            # Construct the state that would exist after
            # Spring restoration, then run the existing
            # temporary planner against it.
            #
            # This is authorization/resolution only.
            # It must happen BEFORE any runtime mutation.

            prospective = copy.deepcopy(
                source_state
            )

            prospective[
                "workshop"
            ] = target_workshop

            prospective[
                "active_general"
            ] = list(
                target_general
            )

            prospective[
                "active_ready"
            ] = list(
                target_ready
            )

            prospective[
                "task_session"
            ][
                "task_sticky_skills"
            ] = list(
                final_task_sticky
            )

            prospective[
                "task_session"
            ][
                "temporary_capabilities"
            ] = list(
                restore_temporary
            )

            prospective_task = (
                self.normalize_task_session(
                    prospective
                )
            )

            temporary_plan = (
                self.plan_temporary_activation(
                    state=prospective,
                    task_session=prospective_task,
                )
            )

            if not isinstance(
                temporary_plan,
                dict,
            ):
                raise TaskSessionError(
                    "Temporary activation planner "
                    "must return a mapping."
                )

            if not isinstance(
                temporary_plan.get(
                    "runtime_toolsets",
                    [],
                ),
                list,
            ):
                raise TaskSessionError(
                    "Temporary planner runtime_toolsets "
                    "must be a list."
                )

            if not isinstance(
                temporary_plan.get(
                    "skill_bindings",
                    [],
                ),
                list,
            ):
                raise TaskSessionError(
                    "Temporary planner skill_bindings "
                    "must be a list."
                )

            return {
                "task":
                    task,

                "cleaning":
                    cleaning,

                "decision":
                    decision,

                "target_workshop":
                    target_workshop,

                "target_general":
                    target_general,

                "target_ready":
                    target_ready,

                "target_temporary":
                    restore_temporary,

                "task_sticky_skills":
                    final_task_sticky,

                "resolution":
                    resolution,

                "temporary_plan":
                    temporary_plan,
            }

        # ------------------------------------------------
        # PREVIEW — no runtime or disk mutation
        # ------------------------------------------------

        if not persist:
            preview = build_application_plan(
                copy.deepcopy(
                    state
                )
            )

            return {
                "state":
                    copy.deepcopy(
                        state
                    ),

                "task_id":
                    preview[
                        "task"
                    ][
                        "id"
                    ],

                "decision":
                    copy.deepcopy(
                        preview[
                            "decision"
                        ]
                    ),

                "target": {
                    "workshop":
                        preview[
                            "target_workshop"
                        ],

                    "general_capabilities":
                        list(
                            preview[
                                "target_general"
                            ]
                        ),

                    "ready_capabilities":
                        list(
                            preview[
                                "target_ready"
                            ]
                        ),

                    "temporary_capabilities":
                        list(
                            preview[
                                "target_temporary"
                            ]
                        ),

                    "task_sticky_skills":
                        list(
                            preview[
                                "task_sticky_skills"
                            ]
                        ),
                },

                "resolution":
                    copy.deepcopy(
                        preview[
                            "resolution"
                        ]
                    ),

                "changed":
                    False,

                "persisted":
                    False,

                "runtime_changed":
                    False,

                "resources_activated":
                    False,
            }

        # ------------------------------------------------
        # CAPTURE EXPECTED TASK / DECISION
        # ------------------------------------------------

        expected_task = (
            self.normalize_task_session(
                state
            )
        )

        expected_task_id = (
            expected_task.get(
                "id"
            )
        )

        if (
            expected_task.get(
                "status"
            )
            != "active"
            or expected_task[
                "lifecycle"
            ][
                "season"
            ]
            != "spring"
            or not expected_task_id
        ):
            raise TaskSessionError(
                "Persistent Spring restoration "
                "requires an active Spring Task."
            )

        expected_cleaning = (
            expected_task.get(
                "spring_cleaning"
            )
        )

        if not isinstance(
            expected_cleaning,
            dict,
        ):
            raise TaskSessionError(
                "Spring Task has no "
                "Cleaning worksheet."
            )

        expected_decision = (
            self._normalize_spring_restoration_decision(
                expected_cleaning.get(
                    "restoration_decision"
                )
            )
        )

        if expected_decision is None:
            raise TaskSessionError(
                "Spring restoration has not "
                "been decided yet."
            )

        # ------------------------------------------------
        # DURABLE / RUNTIME TRANSACTION
        # ------------------------------------------------

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self.normalize_task_session(
                    latest
                )
            )

            if (
                latest_task.get(
                    "id"
                )
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Forest Task changed before "
                    "Spring restoration application."
                )

            if (
                latest_task.get(
                    "status"
                )
                != "active"
                or latest_task[
                    "lifecycle"
                ][
                    "season"
                ]
                != "spring"
            ):
                raise TaskSessionError(
                    "Forest Task left Spring before "
                    "restoration application."
                )

            latest_cleaning = (
                latest_task.get(
                    "spring_cleaning"
                )
            )

            if not isinstance(
                latest_cleaning,
                dict,
            ):
                raise TaskSessionError(
                    "Spring Cleaning worksheet "
                    "disappeared before application."
                )

            latest_decision = (
                self._normalize_spring_restoration_decision(
                    latest_cleaning.get(
                        "restoration_decision"
                    )
                )
            )

            if (
                latest_decision
                != expected_decision
            ):
                raise TaskSessionError(
                    "Spring restoration decision "
                    "changed before application."
                )

            plan = build_application_plan(
                latest
            )

            resolution = plan[
                "resolution"
            ]

            desired_toolsets = list(
                resolution[
                    "runtime"
                ][
                    "toolsets"
                ]
            )

            runtime_adapter = (
                self._runtime_adapter_for_state(
                    latest
                )
            )

            selected_adapter = (
                latest.get(
                    "runtime",
                    {}
                ).get(
                    "adapter"
                )
            )

            actual_adapter = (
                self._runtime_adapter_name(
                    runtime_adapter
                )
            )

            if (
                str(
                    actual_adapter
                )
                != str(
                    selected_adapter
                )
            ):
                raise TaskSessionError(
                    "Resolved runtime adapter does "
                    "not match Forest state: "
                    f"{actual_adapter!r} != "
                    f"{selected_adapter!r}."
                )

            transaction = None

            try:
                # --------------------------------------
                # 1. APPLY RUNTIME REALITY
                # --------------------------------------

                transaction = (
                    runtime_adapter
                    .apply_toolsets_exact(
                        desired_toolsets,
                        latest,
                    )
                )

                # --------------------------------------
                # 2. VERIFY RUNTIME REALITY
                # --------------------------------------

                actual_toolsets = (
                    runtime_adapter
                    .get_active_toolsets(
                        latest
                    )
                )

                if (
                    set(
                        actual_toolsets
                    )
                    != set(
                        desired_toolsets
                    )
                ):
                    raise TaskSessionError(
                        "Spring runtime verification "
                        "failed: expected "
                        f"{sorted(desired_toolsets)}, "
                        "found "
                        f"{sorted(actual_toolsets)}."
                    )

                # --------------------------------------
                # 3. BUILD FOREST TRUTH
                # --------------------------------------

                working = copy.deepcopy(
                    latest
                )

                working[
                    "workshop"
                ] = plan[
                    "target_workshop"
                ]

                working[
                    "active_general"
                ] = list(
                    plan[
                        "target_general"
                    ]
                )

                working[
                    "active_ready"
                ] = list(
                    plan[
                        "target_ready"
                    ]
                )

                working[
                    "task_session"
                ][
                    "task_sticky_skills"
                ] = list(
                    plan[
                        "task_sticky_skills"
                    ]
                )

                # Temporary candidates were reviewed
                # by Spring. Those not explicitly
                # restored remain dormant.
                working[
                    "task_session"
                ][
                    "temporary_capabilities"
                ] = list(
                    plan[
                        "target_temporary"
                    ]
                )

                # Validate the final canonical sticky
                # Skill set through the existing Skill
                # resolution path.
                normalized_working_task = (
                    self.normalize_task_session(
                        working
                    )
                )

                self.resolve_task_sticky_skills(
                    working,
                    normalized_working_task,
                )

                now = self._now_utc()

                application = {
                    "status":
                        "verified",

                    "applied_at":
                        now,

                    "decision_decided_at":
                        plan[
                            "decision"
                        ].get(
                            "decided_at"
                        ),

                    "adapter":
                        str(
                            selected_adapter
                        ),

                    "workshop":
                        plan[
                            "target_workshop"
                        ],

                    "general_capabilities":
                        list(
                            plan[
                                "target_general"
                            ]
                        ),

                    "ready_capabilities":
                        list(
                            plan[
                                "target_ready"
                            ]
                        ),

                    "temporary_capabilities":
                        list(
                            plan[
                                "target_temporary"
                            ]
                        ),

                    "canonical_active_ids":
                        list(
                            resolution[
                                "canonical_active_ids"
                            ]
                        ),

                    "runtime_toolsets":
                        desired_toolsets,

                    "runtime_skills":
                        list(
                            resolution[
                                "runtime"
                            ][
                                "skills"
                            ]
                        ),

                    "task_sticky_skills":
                        list(
                            plan[
                                "task_sticky_skills"
                            ]
                        ),

                    "skill_bindings":
                        copy.deepcopy(
                            resolution[
                                "runtime"
                            ][
                                "skill_bindings"
                            ]
                        ),
                }

                normalized_application = (
                    self._normalize_spring_restoration_application(
                        application
                    )
                )

                existing_application = (
                    self._normalize_spring_restoration_application(
                        latest_cleaning.get(
                            "restoration_application"
                        )
                    )
                )

                # Compare semantic application truth
                # without treating timestamp alone as
                # a reason to rewrite active.yaml.
                def application_signature(
                    value,
                ):
                    if value is None:
                        return None

                    comparable = copy.deepcopy(
                        value
                    )

                    comparable.pop(
                        "applied_at",
                        None,
                    )

                    return comparable

                state_already_matches = (
                    latest.get(
                        "workshop"
                    )
                    == plan[
                        "target_workshop"
                    ]
                    and active_list(
                        latest,
                        "active_general",
                    )
                    == plan[
                        "target_general"
                    ]
                    and active_list(
                        latest,
                        "active_ready",
                    )
                    == plan[
                        "target_ready"
                    ]
                    and latest_task[
                        "task_sticky_skills"
                    ]
                    == plan[
                        "task_sticky_skills"
                    ]
                    and latest_task[
                        "temporary_capabilities"
                    ]
                    == plan[
                        "target_temporary"
                    ]
                )

                application_already_matches = (
                    application_signature(
                        existing_application
                    )
                    == application_signature(
                        normalized_application
                    )
                )

                if (
                    state_already_matches
                    and application_already_matches
                ):
                    runtime_changed = bool(
                        isinstance(
                            transaction,
                            dict,
                        )
                        and transaction.get(
                            "applied"
                        )
                    )

                    return {
                        "state":
                            latest,

                        "task_id":
                            latest_task[
                                "id"
                            ],

                        "decision":
                            copy.deepcopy(
                                plan[
                                    "decision"
                                ]
                            ),

                        "application":
                            copy.deepcopy(
                                existing_application
                            ),

                        "changed":
                            False,

                        "persisted":
                            True,

                        "runtime_changed":
                            runtime_changed,

                        "resources_activated":
                            True,
                    }

                working[
                    "task_session"
                ][
                    "spring_cleaning"
                ][
                    "restoration_application"
                ] = copy.deepcopy(
                    normalized_application
                )

                working[
                    "task_session"
                ][
                    "updated_at"
                ] = now

                # Keep runtime realization bookkeeping
                # structurally portable. The configured
                # adapter identity remains authoritative in
                # state.runtime.adapter.
                working[
                    "last_applied"
                ] = {
                    "toolsets":
                        desired_toolsets,

                    "skills":
                        list(
                            resolution[
                                "runtime"
                            ][
                                "skills"
                            ]
                        ),

                    "timestamp":
                        now,
                }

                # Validate the complete Task structure
                # before the atomic write.
                self.normalize_task_session(
                    working
                )

                # We already hold _state_write_lock(),
                # so call the atomic writer directly
                # rather than recursively locking via
                # persist_state().
                self._atomic_write_yaml(
                    self.state_file,
                    working,
                )

            except Exception as exc:
                rollback_error = None

                if transaction is not None:
                    try:
                        runtime_adapter.restore_toolsets_exact(
                            transaction,
                            latest,
                        )

                    except Exception as restore_exc:
                        rollback_error = restore_exc

                if rollback_error is not None:
                    raise TaskSessionError(
                        "Spring restoration failed and "
                        "runtime rollback also failed: "
                        f"{rollback_error}"
                    ) from exc

                if isinstance(
                    exc,
                    TaskSessionError,
                ):
                    raise

                raise TaskSessionError(
                    "Spring restoration application "
                    f"failed: {exc}"
                ) from exc

        return {
            "state":
                working,

            "task_id":
                working[
                    "task_session"
                ][
                    "id"
                ],

            "decision":
                copy.deepcopy(
                    plan[
                        "decision"
                    ]
                ),

            "application":
                copy.deepcopy(
                    normalized_application
                ),

            "changed":
                True,

            "persisted":
                True,

            "runtime_changed":
                bool(
                    isinstance(
                        transaction,
                        dict,
                    )
                    and transaction.get(
                        "applied"
                    )
                ),

            "resources_activated":
                True,
        }

    def complete_spring_cleaning(
        self,
        state=None,
        persist=False,
    ):
        """Finish verified Spring Cleaning and enter Summer.

        Completion performs no runtime mutation. It verifies
        that the durable restoration application still matches
        Forest state and, when persisted, current runtime truth.
        """

        if state is None:
            state = self.load_state()

        def clean_state_list(
            source_state,
            key,
        ):
            value = source_state.get(
                key,
                [],
            )

            if value is None:
                return []

            if not isinstance(
                value,
                list,
            ):
                raise TaskSessionError(
                    f"state.{key} must be a list."
                )

            return self._unique(
                [
                    str(item)
                    for item in value
                    if str(item).strip()
                ]
            )

        def validate_completion(
            source_state,
            verify_runtime=False,
        ):
            task = self.normalize_task_session(
                source_state
            )

            if (
                task.get("status")
                != "active"
                or not task.get("id")
            ):
                raise TaskSessionError(
                    "Spring completion requires "
                    "an active Forest Task."
                )

            season = task[
                "lifecycle"
            ][
                "season"
            ]

            cleaning = task.get(
                "spring_cleaning"
            )

            if not isinstance(
                cleaning,
                dict,
            ):
                raise TaskSessionError(
                    "Task has no Spring Cleaning worksheet."
                )

            cleaning_status = cleaning.get(
                "status"
            )

            already_completed = (
                season == "summer"
                and cleaning_status == "completed"
            )

            if not (
                season == "spring"
                and cleaning_status == "cleaning"
            ) and not already_completed:
                raise TaskSessionError(
                    "Spring completion requires either "
                    "Spring/Cleaning or an already completed "
                    "Summer Task."
                )

            decision = (
                self._normalize_spring_restoration_decision(
                    cleaning.get(
                        "restoration_decision"
                    )
                )
            )

            application = (
                self._normalize_spring_restoration_application(
                    cleaning.get(
                        "restoration_application"
                    )
                )
            )

            if decision is None:
                raise TaskSessionError(
                    "Spring has no durable "
                    "restoration decision."
                )

            if application is None:
                raise TaskSessionError(
                    "Spring has no verified "
                    "restoration application."
                )

            if application.get(
                "status"
            ) != "verified":
                raise TaskSessionError(
                    "Spring restoration application "
                    "is not verified."
                )

            if (
                application.get(
                    "decision_decided_at"
                )
                != decision.get(
                    "decided_at"
                )
            ):
                raise TaskSessionError(
                    "Spring application does not match "
                    "the current restoration decision."
                )

            if (
                source_state.get(
                    "workshop"
                )
                != application.get(
                    "workshop"
                )
            ):
                raise TaskSessionError(
                    "Forest Workshop no longer matches "
                    "the verified Spring application."
                )

            if (
                clean_state_list(
                    source_state,
                    "active_general",
                )
                != application[
                    "general_capabilities"
                ]
            ):
                raise TaskSessionError(
                    "Forest General capabilities no longer "
                    "match the verified Spring application."
                )

            if (
                clean_state_list(
                    source_state,
                    "active_ready",
                )
                != application[
                    "ready_capabilities"
                ]
            ):
                raise TaskSessionError(
                    "Forest Ready capabilities no longer "
                    "match the verified Spring application."
                )

            if (
                task[
                    "task_sticky_skills"
                ]
                != application[
                    "task_sticky_skills"
                ]
            ):
                raise TaskSessionError(
                    "Task-Sticky Skills no longer match "
                    "the verified Spring application."
                )

            if (
                task[
                    "temporary_capabilities"
                ]
                != application[
                    "temporary_capabilities"
                ]
            ):
                raise TaskSessionError(
                    "Temporary capabilities no longer "
                    "match the verified Spring application."
                )

            runtime = source_state.get(
                "runtime",
                {},
            )

            if not isinstance(
                runtime,
                dict,
            ):
                raise TaskSessionError(
                    "state.runtime must be a mapping."
                )

            selected_adapter = runtime.get(
                "adapter"
            )

            if (
                str(selected_adapter)
                != str(
                    application.get(
                        "adapter"
                    )
                )
            ):
                raise TaskSessionError(
                    "Runtime adapter no longer matches "
                    "the verified Spring application."
                )

            resolved_skills = (
                self.resolve_task_sticky_skills(
                    source_state,
                    task,
                )
            )

            runtime_skills = [
                binding[
                    "runtime_id"
                ]
                for binding in resolved_skills
            ]

            if (
                runtime_skills
                != application[
                    "runtime_skills"
                ]
            ):
                raise TaskSessionError(
                    "Runtime Skill resolution no longer "
                    "matches the verified application."
                )

            if verify_runtime:
                runtime_adapter = (
                    self._runtime_adapter_for_state(
                        source_state
                    )
                )

                actual_adapter = (
                    self._runtime_adapter_name(
                        runtime_adapter
                    )
                )

                if (
                    str(actual_adapter)
                    != str(selected_adapter)
                ):
                    raise TaskSessionError(
                        "Resolved runtime adapter differs "
                        "from Forest state."
                    )

                actual_toolsets = (
                    runtime_adapter
                    .get_active_toolsets(
                        source_state
                    )
                )

                if (
                    set(actual_toolsets)
                    != set(
                        application[
                            "runtime_toolsets"
                        ]
                    )
                ):
                    raise TaskSessionError(
                        "Runtime toolsets no longer match "
                        "the verified Spring application: "
                        f"expected "
                        f"{sorted(application['runtime_toolsets'])}, "
                        f"found {sorted(actual_toolsets)}."
                    )

            return {
                "task":
                    task,

                "cleaning":
                    cleaning,

                "decision":
                    decision,

                "application":
                    application,

                "already_completed":
                    already_completed,
            }

        # ----------------------------------------------
        # PREVIEW — structure only, no runtime read/write
        # ----------------------------------------------

        if not persist:
            checked = validate_completion(
                copy.deepcopy(
                    state
                ),
                verify_runtime=False,
            )

            return {
                "state":
                    copy.deepcopy(
                        state
                    ),

                "task_id":
                    checked[
                        "task"
                    ][
                        "id"
                    ],

                "can_complete":
                    True,

                "already_completed":
                    checked[
                        "already_completed"
                    ],

                "changed":
                    False,

                "persisted":
                    False,

                "runtime_mutated":
                    False,
            }

        expected = self.normalize_task_session(
            state
        )

        expected_task_id = expected.get(
            "id"
        )

        expected_cleaning = expected.get(
            "spring_cleaning"
        )

        if not isinstance(
            expected_cleaning,
            dict,
        ):
            raise TaskSessionError(
                "Task has no Spring Cleaning worksheet."
            )

        expected_application = (
            self._normalize_spring_restoration_application(
                expected_cleaning.get(
                    "restoration_application"
                )
            )
        )

        # ----------------------------------------------
        # ATOMIC COMPLETION
        # ----------------------------------------------

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self.normalize_task_session(
                    latest
                )
            )

            if (
                latest_task.get(
                    "id"
                )
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Forest Task changed before "
                    "Spring completion."
                )

            latest_cleaning = latest_task.get(
                "spring_cleaning"
            )

            if not isinstance(
                latest_cleaning,
                dict,
            ):
                raise TaskSessionError(
                    "Spring Cleaning worksheet "
                    "disappeared before completion."
                )

            latest_application = (
                self._normalize_spring_restoration_application(
                    latest_cleaning.get(
                        "restoration_application"
                    )
                )
            )

            if (
                latest_application
                != expected_application
            ):
                raise TaskSessionError(
                    "Spring restoration application "
                    "changed before completion."
                )

            checked = validate_completion(
                latest,
                verify_runtime=True,
            )

            if checked[
                "already_completed"
            ]:
                return {
                    "state":
                        latest,

                    "task_id":
                        latest_task[
                            "id"
                        ],

                    "season":
                        "summer",

                    "cleaning_status":
                        "completed",

                    "changed":
                        False,

                    "persisted":
                        True,

                    "runtime_mutated":
                        False,
                }

            now = self._now_utc()

            working = copy.deepcopy(
                latest
            )

            working[
                "task_session"
            ][
                "spring_cleaning"
            ][
                "status"
            ] = "completed"

            working[
                "task_session"
            ][
                "spring_cleaning"
            ][
                "completed_at"
            ] = now

            working[
                "task_session"
            ][
                "lifecycle"
            ] = {
                "season":
                    "summer",

                "previous_season":
                    "spring",

                "entered_at":
                    now,
            }

            working[
                "task_session"
            ][
                "updated_at"
            ] = now

            # Validate Summer + completed Cleaning before write.
            self.normalize_task_session(
                working
            )

            self._atomic_write_yaml(
                self.state_file,
                working,
            )

        return {
            "state":
                working,

            "task_id":
                working[
                    "task_session"
                ][
                    "id"
                ],

            "season":
                "summer",

            "cleaning_status":
                "completed",

            "changed":
                True,

            "persisted":
                True,

            "runtime_mutated":
                False,
        }

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

        if (
            current_season == "spring"
            and season == "summer"
        ):
            cleaning = current.get(
                "spring_cleaning"
            )

            if (
                not isinstance(
                    cleaning,
                    dict,
                )
                or cleaning.get(
                    "status"
                )
                != "completed"
            ):
                raise TaskSessionError(
                    "Spring Cleaning must be "
                    "completed through "
                    "complete_spring_cleaning() "
                    "before entering Summer."
                )

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
                            self._runtime_adapters_for_sessions(
                                runtime_sessions
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

    def _build_spring_cleaning_state(
        self,
        winter_record,
        started_at,
    ):
        """Build the durable worksheet for Spring Cleaning."""

        snapshot = winter_record.get(
            "activation_snapshot",
            {},
        )

        if snapshot is None:
            snapshot = {}

        if not isinstance(
            snapshot,
            dict,
        ):
            snapshot = {}

        return {
            "status":
                "cleaning",

            "started_at":
                started_at,

            "source_retired_at":
                winter_record.get(
                    "retired_at"
                ),

            "activation_snapshot":
                copy.deepcopy(
                    snapshot
                ),
        }

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

                spring_task[
                    "spring_cleaning"
                ] = self._build_spring_cleaning_state(
                    record,
                    now,
                )

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

            spring_task[
                "spring_cleaning"
            ] = self._build_spring_cleaning_state(
                record,
                now,
            )

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

            "spring_cleaning":
                copy.deepcopy(
                    normalized[
                        "spring_cleaning"
                    ]
                ),

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

    def record_spring_restoration_decision(
        self,
        decision,
        state=None,
        persist=False,
    ):
        """Record Spring choices without activating resources.

        This method records intent only. Workshop, tools,
        reasoning, model form, and runtime activation are
        intentionally untouched.
        """

        if not isinstance(
            decision,
            dict,
        ):
            raise TaskSessionError(
                "Spring restoration decision "
                "must be a mapping."
            )

        if state is None:
            state = self.load_state()

        def build_decision(
            source_state,
        ):
            task = self.normalize_task_session(
                source_state
            )

            if (
                task.get("status")
                != "active"
                or task[
                    "lifecycle"
                ][
                    "season"
                ]
                != "spring"
            ):
                raise TaskSessionError(
                    "Restoration decisions require "
                    "an active Spring Task."
                )

            cleaning = task.get(
                "spring_cleaning"
            )

            if not isinstance(
                cleaning,
                dict,
            ):
                raise TaskSessionError(
                    "Spring Task has no "
                    "Cleaning worksheet."
                )

            plan = self.plan_spring_restoration(
                source_state
            )

            requested = decision.get(
                "restore",
                {},
            )

            if requested is None:
                requested = {}

            if not isinstance(
                requested,
                dict,
            ):
                raise TaskSessionError(
                    "decision.restore "
                    "must be a mapping."
                )

            # ------------------------------------------
            # WORKSHOP
            # ------------------------------------------

            restore_workshop = requested.get(
                "workshop"
            )

            candidate_workshop = (
                plan[
                    "review"
                ][
                    "workshop"
                ]
            )

            if (
                restore_workshop is not None
                and restore_workshop
                != candidate_workshop
            ):
                raise TaskSessionError(
                    "Spring cannot restore an "
                    "unreviewed Workshop."
                )

            # ------------------------------------------
            # CAPABILITY SUBSETS
            # ------------------------------------------

            def selected_subset(
                key,
            ):
                selected = requested.get(
                    key,
                    [],
                )

                if selected is None:
                    selected = []

                if not isinstance(
                    selected,
                    list,
                ):
                    raise TaskSessionError(
                        f"decision.restore.{key} "
                        "must be a list."
                    )

                selected = list(
                    dict.fromkeys(
                        str(item)
                        for item in selected
                        if str(item).strip()
                    )
                )

                candidates = list(
                    plan[
                        "review"
                    ][
                        key
                    ]
                )

                unknown = [
                    item
                    for item in selected
                    if item not in candidates
                ]

                if unknown:
                    raise TaskSessionError(
                        "Spring cannot restore "
                        f"unreviewed {key}: "
                        + ", ".join(
                            unknown
                        )
                    )

                return (
                    selected,
                    candidates,
                )

            (
                restore_general,
                candidate_general,
            ) = selected_subset(
                "general_capabilities"
            )

            (
                restore_ready,
                candidate_ready,
            ) = selected_subset(
                "ready_capabilities"
            )

            (
                restore_temporary,
                candidate_temporary,
            ) = selected_subset(
                "temporary_capabilities"
            )

            restore = {
                "workshop":
                    restore_workshop,

                "general_capabilities":
                    restore_general,

                "ready_capabilities":
                    restore_ready,

                "temporary_capabilities":
                    restore_temporary,
            }

            leave_dormant = {
                "workshop":
                    (
                        candidate_workshop
                        if (
                            candidate_workshop
                            is not None
                            and restore_workshop
                            is None
                        )
                        else None
                    ),

                "general_capabilities":
                    [
                        item
                        for item
                        in candidate_general
                        if item
                        not in restore_general
                    ],

                "ready_capabilities":
                    [
                        item
                        for item
                        in candidate_ready
                        if item
                        not in restore_ready
                    ],

                "temporary_capabilities":
                    [
                        item
                        for item
                        in candidate_temporary
                        if item
                        not in restore_temporary
                    ],

                "reasoning":
                    plan[
                        "leave_dormant"
                    ][
                        "reasoning"
                    ],

                "model_form":
                    plan[
                        "leave_dormant"
                    ][
                        "model_form"
                    ],
            }

            existing = (
                cleaning.get(
                    "restoration_decision"
                )
            )

            existing = (
                self._normalize_spring_restoration_decision(
                    existing
                )
            )

            if (
                existing is not None
                and existing[
                    "restore"
                ]
                == restore
                and existing[
                    "leave_dormant"
                ]
                == leave_dormant
            ):
                return {
                    "task":
                        task,

                    "plan":
                        plan,

                    "decision":
                        existing,

                    "changed":
                        False,
                }

            now = self._now_utc()

            normalized_decision = {
                "decided_at":
                    now,

                "restore":
                    restore,

                "leave_dormant":
                    leave_dormant,
            }

            return {
                "task":
                    task,

                "plan":
                    plan,

                "decision":
                    normalized_decision,

                "changed":
                    True,
            }

        # ----------------------------------------------
        # PREVIEW — MEMORY ONLY
        # ----------------------------------------------

        if not persist:
            working = copy.deepcopy(
                state
            )

            result = build_decision(
                working
            )

            if result[
                "changed"
            ]:
                working[
                    "task_session"
                ][
                    "spring_cleaning"
                ][
                    "restoration_decision"
                ] = copy.deepcopy(
                    result[
                        "decision"
                    ]
                )

            return {
                "state":
                    working,

                "task_id":
                    result[
                        "task"
                    ][
                        "id"
                    ],

                "plan":
                    result[
                        "plan"
                    ],

                "decision":
                    copy.deepcopy(
                        result[
                            "decision"
                        ]
                    ),

                "changed":
                    result[
                        "changed"
                    ],

                "persisted":
                    False,

                "resources_activated":
                    False,
            }

        # ----------------------------------------------
        # DURABLE DECISION
        # ----------------------------------------------

        expected = (
            self.normalize_task_session(
                state
            )
        )

        expected_task_id = (
            expected.get(
                "id"
            )
        )

        if (
            expected.get("status")
            != "active"
            or expected[
                "lifecycle"
            ][
                "season"
            ]
            != "spring"
        ):
            raise TaskSessionError(
                "Spring decision persistence "
                "requires an active Spring Task."
            )

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self.normalize_task_session(
                    latest
                )
            )

            if (
                latest_task.get(
                    "id"
                )
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Forest Task changed before "
                    "Spring decision persistence."
                )

            if (
                latest_task.get(
                    "status"
                )
                != "active"
                or latest_task[
                    "lifecycle"
                ][
                    "season"
                ]
                != "spring"
            ):
                raise TaskSessionError(
                    "Forest Task left Spring before "
                    "decision persistence."
                )

            # Rebuild against latest state while locked.
            result = build_decision(
                latest
            )

            if not result[
                "changed"
            ]:
                return {
                    "state":
                        latest,

                    "task_id":
                        latest_task[
                            "id"
                        ],

                    "plan":
                        result[
                            "plan"
                        ],

                    "decision":
                        copy.deepcopy(
                            result[
                                "decision"
                            ]
                        ),

                    "changed":
                        False,

                    "persisted":
                        True,

                    "resources_activated":
                        False,
                }

            working = copy.deepcopy(
                latest
            )

            working[
                "task_session"
            ][
                "spring_cleaning"
            ][
                "restoration_decision"
            ] = copy.deepcopy(
                result[
                    "decision"
                ]
            )

            working[
                "task_session"
            ][
                "updated_at"
            ] = result[
                "decision"
            ][
                "decided_at"
            ]

            self._atomic_write_yaml(
                self.state_file,
                working,
            )

        return {
            "state":
                working,

            "task_id":
                result[
                    "task"
                ][
                    "id"
                ],

            "plan":
                result[
                    "plan"
                ],

            "decision":
                copy.deepcopy(
                    result[
                        "decision"
                    ]
                ),

            "changed":
                True,

            "persisted":
                True,

            # Intent is now durable.
            # Activation has NOT happened yet.
            "resources_activated":
                False,
        }

    def plan_spring_restoration(
        self,
        state=None,
    ):
        """Plan Spring restoration without changing state.

        The planner is intentionally conservative.
        It separates preserved continuity from resources
        that need renewed justification after Winter.
        """

        if state is None:
            state = self.load_state()

        task = self.normalize_task_session(
            state
        )

        if (
            task.get("status") != "active"
            or task[
                "lifecycle"
            ][
                "season"
            ]
            != "spring"
        ):
            raise TaskSessionError(
                "Selective restoration planning "
                "requires an active Spring Task."
            )

        cleaning = task.get(
            "spring_cleaning"
        )

        if not isinstance(
            cleaning,
            dict,
        ):
            raise TaskSessionError(
                "Spring Task has no durable "
                "Cleaning worksheet."
            )

        snapshot = cleaning.get(
            "activation_snapshot",
            {},
        )

        if not isinstance(
            snapshot,
            dict,
        ):
            snapshot = {}

        def list_value(mapping, key):
            value = mapping.get(
                key,
                []
            )

            if not isinstance(
                value,
                list,
            ):
                return []

            return list(
                dict.fromkeys(
                    str(item)
                    for item in value
                    if str(item).strip()
                )
            )

        previous_general = list_value(
            snapshot,
            "active_general",
        )

        previous_ready = list_value(
            snapshot,
            "active_ready",
        )

        current_general = list_value(
            state,
            "active_general",
        )

        current_ready = list_value(
            state,
            "active_ready",
        )

        task_sticky = list(
            task[
                "task_sticky_skills"
            ]
        )

        temporary = list(
            task[
                "temporary_capabilities"
            ]
        )

        previous_workshop = snapshot.get(
            "workshop"
        )

        current_workshop = state.get(
            "workshop"
        )

        previous_reasoning = snapshot.get(
            "reasoning"
        )

        current_reasoning = state.get(
            "reasoning"
        )

        previous_model_form = snapshot.get(
            "model_form"
        )

        current_model_form = state.get(
            "model_form"
        )

        already_available = {
            "workshop":
                (
                    current_workshop
                    if (
                        previous_workshop
                        is not None
                        and previous_workshop
                        == current_workshop
                    )
                    else None
                ),

            "general_capabilities":
                [
                    item
                    for item
                    in previous_general
                    if item in current_general
                ],

            "ready_capabilities":
                [
                    item
                    for item
                    in previous_ready
                    if item in current_ready
                ],

            "reasoning":
                (
                    current_reasoning
                    if (
                        previous_reasoning
                        is not None
                        and previous_reasoning
                        == current_reasoning
                    )
                    else None
                ),

            "model_form":
                (
                    current_model_form
                    if (
                        previous_model_form
                        is not None
                        and previous_model_form
                        == current_model_form
                    )
                    else None
                ),
        }

        review = {
            "workshop":
                (
                    previous_workshop
                    if (
                        previous_workshop
                        is not None
                        and previous_workshop
                        != current_workshop
                    )
                    else None
                ),

            "general_capabilities":
                [
                    item
                    for item
                    in previous_general
                    if item not in current_general
                ],

            "ready_capabilities":
                [
                    item
                    for item
                    in previous_ready
                    if item not in current_ready
                ],

            # Temporary capabilities remain associated
            # with the Task, but Winter removes their
            # automatic authority to become hot again.
            "temporary_capabilities":
                temporary,
        }

        leave_dormant = {
            # Resource intensity must earn its way back.
            # Old Deep reasoning or Big model form should
            # not resurrect solely because it was used
            # before Winter.
            "reasoning":
                (
                    previous_reasoning
                    if (
                        previous_reasoning
                        is not None
                        and previous_reasoning
                        != current_reasoning
                    )
                    else None
                ),

            "model_form":
                (
                    previous_model_form
                    if (
                        previous_model_form
                        is not None
                        and previous_model_form
                        != current_model_form
                    )
                    else None
                ),
        }

        return {
            "task_id":
                task.get(
                    "id"
                ),

            "season":
                "spring",

            "cleaning_status":
                cleaning.get(
                    "status"
                ),

            "keep": {
                "task_identity":
                    task.get(
                        "id"
                    ),

                "runtime_sessions":
                    copy.deepcopy(
                        task[
                            "runtime_sessions"
                        ]
                    ),

                # Task-Sticky means Forest has already
                # decided these belong to this Task rather
                # than merely to its last hot environment.
                "task_sticky_skills":
                    task_sticky,
            },

            "already_available":
                already_available,

            "review":
                review,

            "leave_dormant":
                leave_dormant,

            "previous_working_set":
                copy.deepcopy(
                    snapshot
                ),

            "current_working_set": {
                "workshop":
                    current_workshop,

                "active_general":
                    current_general,

                "active_ready":
                    current_ready,

                "reasoning":
                    current_reasoning,

                "model_form":
                    current_model_form,
            },

            "policy": {
                "task_sticky":
                    "keep",

                "previous_workshop":
                    "review_if_changed",

                "previous_capabilities":
                    "review_if_not_already_available",

                "temporary_capabilities":
                    "revalidate_before_activation",

                "reasoning":
                    "do_not_restore_from_history_alone",

                "model_form":
                    "do_not_restore_from_history_alone",
            },

            "applied":
                False,
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

        # Context Route State is also Task-local and
        # ephemeral. Discard it only after the same
        # durable Task-end boundary has succeeded.
        self._discard_context_route_state(
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



    def get_reasoning_control(
        self,
        state=None,
    ):
        """Read normalized Tree reasoning-control state."""

        if state is None:
            state = self.load_state()

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        try:
            from reasoning import (
                ReasoningControlError,
                reasoning_control_from_mapping,
                reasoning_control_to_mapping,
            )

            control = (
                reasoning_control_from_mapping(
                    state.get(
                        "reasoning_control"
                    )
                )
            )

        except ReasoningControlError as exc:
            raise TaskSessionError(
                "Invalid durable Forest "
                "reasoning_control state."
            ) from exc

        return {
            "state":
                copy.deepcopy(
                    state
                ),

            "control":
                control,

            "reasoning_control":
                reasoning_control_to_mapping(
                    control
                ),
        }


    def _mutate_reasoning_control(
        self,
        mutator,
        *,
        state=None,
        persist=False,
    ):
        """Apply one human reasoning-control mutation.

        Durable changes use the established Forest pattern:

        lock
          → reload latest active.yaml
          → mutate latest
          → validate
          → atomic YAML write
        """

        if not callable(
            mutator
        ):
            raise TaskSessionError(
                "Reasoning-control mutator "
                "must be callable."
            )

        try:
            from reasoning import (
                ReasoningControlError,
                reasoning_control_from_mapping,
                reasoning_control_to_mapping,
            )

        except Exception as exc:
            raise TaskSessionError(
                "Forest reasoning-control backend "
                "is unavailable."
            ) from exc


        def apply(source):
            if not isinstance(
                source,
                dict,
            ):
                raise TaskSessionError(
                    "Forest state must be a mapping."
                )

            working = copy.deepcopy(
                source
            )

            try:
                current = (
                    reasoning_control_from_mapping(
                        working.get(
                            "reasoning_control"
                        )
                    )
                )

                updated = mutator(
                    current
                )

                mapping = (
                    reasoning_control_to_mapping(
                        updated
                    )
                )

            except ReasoningControlError as exc:
                raise TaskSessionError(
                    "Invalid reasoning-control mutation."
                ) from exc

            changed = (
                working.get(
                    "reasoning_control"
                )
                != mapping
            )

            if changed:
                working[
                    "reasoning_control"
                ] = mapping

            return (
                working,
                updated,
                mapping,
                changed,
            )


        if persist:
            with self._state_write_lock():
                latest = self.load_state()

                (
                    working,
                    updated,
                    mapping,
                    changed,
                ) = apply(
                    latest
                )

                if changed:
                    self.normalize_task_session(
                        working
                    )

                    self._atomic_write_yaml(
                        self.state_file,
                        working,
                    )

            return {
                "state":
                    working,

                "control":
                    updated,

                "reasoning_control":
                    mapping,

                "changed":
                    changed,

                "persisted":
                    True,
            }


        source = (
            self.load_state()
            if state is None
            else state
        )

        (
            working,
            updated,
            mapping,
            changed,
        ) = apply(
            source
        )

        return {
            "state":
                working,

            "control":
                updated,

            "reasoning_control":
                mapping,

            "changed":
                changed,

            "persisted":
                False,
        }


    def set_reasoning_auto_baseline(
        self,
        state=None,
        persist=False,
    ):
        """Clear pin while preserving an active temp lease."""

        from reasoning import (
            set_auto_baseline,
        )

        return self._mutate_reasoning_control(
            set_auto_baseline,
            state=state,
            persist=persist,
        )


    def return_reasoning_to_auto(
        self,
        state=None,
        persist=False,
    ):
        """Clear temporary lease and clear any pin."""

        from reasoning import (
            clear_temporary_mode,
            set_auto_baseline,
        )

        def mutate(control):
            return set_auto_baseline(
                clear_temporary_mode(
                    control
                )
            )

        return self._mutate_reasoning_control(
            mutate,
            state=state,
            persist=persist,
        )


    def pin_reasoning_mode(
        self,
        mode,
        state=None,
        persist=False,
    ):
        """Set durable Light / Normal / Deep baseline."""

        from reasoning import (
            set_pinned_baseline,
        )

        return self._mutate_reasoning_control(
            lambda control:
                set_pinned_baseline(
                    control,
                    mode,
                ),
            state=state,
            persist=persist,
        )


    def set_temporary_reasoning_mode(
        self,
        mode,
        state=None,
        persist=False,
        turns=None,
    ):
        """Start or replace a temporary reasoning lease."""

        from reasoning import (
            set_temporary_mode,
        )

        return self._mutate_reasoning_control(
            lambda control:
                set_temporary_mode(
                    control,
                    mode,
                    turns=turns,
                ),
            state=state,
            persist=persist,
        )


    def clear_temporary_reasoning_mode(
        self,
        state=None,
        persist=False,
    ):
        """Clear temporary lease; reveal baseline."""

        from reasoning import (
            clear_temporary_mode,
        )

        return self._mutate_reasoning_control(
            clear_temporary_mode,
            state=state,
            persist=persist,
        )


    def set_reasoning_temporary_turn_default(
        self,
        turns,
        state=None,
        persist=False,
    ):
        """Change future temporary lease duration."""

        from reasoning import (
            set_temporary_turn_default,
        )

        return self._mutate_reasoning_control(
            lambda control:
                set_temporary_turn_default(
                    control,
                    turns,
                ),
            state=state,
            persist=persist,
        )


    def _commit_successful_model_form_turn(
        self,
        *,
        working,
        frozen_turn,
        user_message,
        assistant_message,
        expected_previous_form,
        turn_control,
        decision,
        persist,
    ):
        """Commit Forest-owned state for one successful frozen turn.

        The runtime/model call MUST already have succeeded.

        One successful turn owns three semantic effects:

        - effective Model Form history
        - completed conversation continuity
        - temporary reasoning-lease consumption

        Persistent commits merge against latest durable state
        under one Forest write lock.
        """

        try:
            from reasoning import (
                ReasoningControlError,
                consume_temporary_turn,
                reasoning_control_from_mapping,
                reasoning_control_to_mapping,
            )

        except Exception as exc:
            raise TaskSessionError(
                "Forest reasoning-control backend "
                "is unavailable."
            ) from exc

        if not isinstance(
            working,
            dict,
        ):
            raise TaskSessionError(
                "Successful-turn commit requires "
                "Forest state."
            )

        context_id = (
            self._effective_model_form_context_id(
                frozen_turn.execution_context_id
            )
        )

        expected_task_id = (
            str(
                frozen_turn.task_id
                or ""
            ).strip()
        )

        if not expected_task_id:
            raise TaskSessionError(
                "Successful-turn commit requires "
                "frozen Task identity."
            )

        working_task = (
            self._active_runtime_task(
                working
            )
        )

        if (
            working_task["id"]
            != expected_task_id
        ):
            raise TaskSessionError(
                "Successful-turn commit crossed "
                "Task identity."
            )

        if (
            expected_previous_form
            not in (
                None,
                "small",
                "big",
            )
        ):
            raise TaskSessionError(
                "Successful-turn commit received "
                "an invalid pre-turn effective form."
            )

        source_previous_form = (
            expected_previous_form
        )

        source_binding = (
            self._runtime_session_binding_for_identity(
                working,
                context_id,
                frozen_turn.binding_id,
            )
        )

        if not isinstance(
            source_binding,
            dict,
        ):
            raise TaskSessionError(
                "Successful-turn commit requires "
                "the frozen runtime-session binding."
            )


        def apply_semantics(source):
            """Apply successful-turn semantics in memory."""

            form_write = (
                self._write_effective_model_form_for_context(
                    source,
                    context_id,
                    frozen_turn.form,
                )
            )

            conversation_write = (
                self._append_conversation_exchange_for_context(
                    form_write["state"],
                    context_id,
                    user_message,
                    assistant_message,
                )
            )

            return (
                form_write,
                conversation_write,
            )


        # --------------------------------------------------
        # IN-MEMORY TURN
        # --------------------------------------------------

        if not persist:
            (
                form_write,
                conversation_write,
            ) = apply_semantics(
                working
            )

            reasoning_finalize = (
                self._finalize_reasoning_control_after_success(
                    working=conversation_write["state"],
                    turn_control=turn_control,
                    decision=decision,
                    persist=False,
                )
            )

            return {
                "state":
                    reasoning_finalize["state"],

                "previous_form":
                    form_write["previous_form"],

                "form":
                    form_write["form"],

                "form_changed":
                    form_write["changed"],

                "previous_exchange_count":
                    conversation_write[
                        "previous_exchange_count"
                    ],

                "exchange_count":
                    conversation_write[
                        "exchange_count"
                    ],

                "reasoning_consumed":
                    reasoning_finalize[
                        "consumed"
                    ],

                "reasoning_superseded":
                    reasoning_finalize[
                        "superseded"
                    ],

                "persisted":
                    False,
            }


        # --------------------------------------------------
        # DURABLE TURN
        # --------------------------------------------------

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self._active_runtime_task(
                    latest
                )
            )

            if (
                latest_task["id"]
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Stale Forest Task generation: "
                    "active Task changed before "
                    "successful-turn commit."
                )

            latest_binding = (
                self._runtime_session_binding_for_identity(
                    latest,
                    context_id,
                    frozen_turn.binding_id,
                )
            )

            if not isinstance(
                latest_binding,
                dict,
            ):
                raise TaskSessionError(
                    "Persisted frozen runtime binding "
                    "disappeared before successful-turn "
                    "commit."
                )

            source_adapter = str(
                source_binding.get(
                    "adapter"
                )
                or ""
            ).strip()

            latest_adapter = str(
                latest_binding.get(
                    "adapter"
                )
                or ""
            ).strip()

            source_session_id = str(
                source_binding.get(
                    "session_id"
                )
                or ""
            )

            latest_session_id = str(
                latest_binding.get(
                    "session_id"
                )
                or ""
            )

            if (
                latest_adapter
                != source_adapter
                or latest_session_id
                != source_session_id
            ):
                raise TaskSessionError(
                    "Stale canonical runtime binding: "
                    "the frozen execution context changed "
                    "before successful-turn commit."
                )

            latest_previous_form = (
                self._effective_model_form_for_context(
                    latest,
                    context_id,
                )
            )

            if (
                latest_previous_form
                != source_previous_form
                and latest_previous_form
                != frozen_turn.form
            ):
                raise TaskSessionError(
                    "Stale effective Model Form: "
                    "a newer successful turn changed "
                    "this execution context to a "
                    "different form before commit."
                )

            (
                form_write,
                conversation_write,
            ) = apply_semantics(
                latest
            )

            committed = (
                conversation_write[
                    "state"
                ]
            )

            reasoning_consumed = False
            reasoning_superseded = False

            if decision.consumes_temporary:
                try:
                    latest_control = (
                        reasoning_control_from_mapping(
                            committed.get(
                                "reasoning_control"
                            )
                        )
                    )

                except ReasoningControlError as exc:
                    raise TaskSessionError(
                        "Invalid latest durable "
                        "reasoning-control state."
                    ) from exc

                latest_lease = (
                    latest_control.temporary
                )

                if (
                    latest_lease is None
                    or latest_lease.lease_id
                    != decision.temporary_lease_id
                ):
                    # A newer user action replaced or
                    # cleared the lease while this turn
                    # was in flight. Preserve that newer
                    # reasoning intent.
                    reasoning_superseded = True

                else:
                    try:
                        updated_control = (
                            consume_temporary_turn(
                                latest_control,
                                decision,
                            )
                        )

                        committed[
                            "reasoning_control"
                        ] = (
                            reasoning_control_to_mapping(
                                updated_control
                            )
                        )

                    except ReasoningControlError as exc:
                        raise TaskSessionError(
                            "Could not consume successful "
                            "turn reasoning lease."
                        ) from exc

                    reasoning_consumed = True

            committed_task = (
                self.normalize_task_session(
                    committed
                )
            )

            committed_task[
                "updated_at"
            ] = self._now_utc()

            committed[
                "task_session"
            ] = committed_task

            self.normalize_task_session(
                committed
            )

            self._atomic_write_yaml(
                self.state_file,
                committed,
            )

        return {
            "state":
                committed,

            "previous_form":
                form_write["previous_form"],

            "form":
                form_write["form"],

            "form_changed":
                form_write["changed"],

            "previous_exchange_count":
                conversation_write[
                    "previous_exchange_count"
                ],

            "exchange_count":
                conversation_write[
                    "exchange_count"
                ],

            "reasoning_consumed":
                reasoning_consumed,

            "reasoning_superseded":
                reasoning_superseded,

            "persisted":
                True,
        }


    def _finalize_reasoning_control_after_success(
        self,
        *,
        working,
        turn_control,
        decision,
        persist,
    ):
        """Consume one temporary lease turn after success.

        The runtime retry/recovery path finishes before this
        method is reached, so stale recovery cannot decrement
        a second time.

        Lease identity prevents an older in-flight turn from
        decrementing a replacement temporary lease.
        """

        try:
            from reasoning import (
                ReasoningControlError,
                consume_temporary_turn,
                reasoning_control_from_mapping,
                reasoning_control_to_mapping,
            )

        except Exception as exc:
            raise TaskSessionError(
                "Forest reasoning-control backend "
                "is unavailable."
            ) from exc


        # Explicit / pinned / automatic reasoning did not
        # consume the temporary lease.
        if not decision.consumes_temporary:
            if not persist:
                return {
                    "state":
                        working,

                    "control":
                        turn_control,

                    "consumed":
                        False,

                    "superseded":
                        False,
                }

            latest = self.load_state()

            try:
                latest_control = (
                    reasoning_control_from_mapping(
                        latest.get(
                            "reasoning_control"
                        )
                    )
                )

            except ReasoningControlError as exc:
                raise TaskSessionError(
                    "Latest durable "
                    "reasoning_control is invalid."
                ) from exc

            return {
                "state":
                    latest,

                "control":
                    latest_control,

                "consumed":
                    False,

                "superseded":
                    False,
            }


        # In-memory / preview semantics.
        if not persist:
            try:
                updated = (
                    consume_temporary_turn(
                        turn_control,
                        decision,
                    )
                )

            except ReasoningControlError as exc:
                raise TaskSessionError(
                    "Could not consume temporary "
                    "reasoning lease."
                ) from exc

            updated_working = copy.deepcopy(
                working
            )

            updated_working[
                "reasoning_control"
            ] = reasoning_control_to_mapping(
                updated
            )

            return {
                "state":
                    updated_working,

                "control":
                    updated,

                "consumed":
                    True,

                "superseded":
                    False,
            }


        # Durable consumption:
        # lock → reload latest → verify lease identity
        # → decrement → atomic write.
        with self._state_write_lock():
            latest = self.load_state()

            try:
                latest_control = (
                    reasoning_control_from_mapping(
                        latest.get(
                            "reasoning_control"
                        )
                    )
                )

            except ReasoningControlError as exc:
                raise TaskSessionError(
                    "Latest durable "
                    "reasoning_control is invalid."
                ) from exc

            latest_lease = (
                latest_control.temporary
            )

            # User changed/cleared/replaced temporary reasoning
            # while this model turn was running.
            #
            # The old turn must never alter the new instruction.
            if (
                latest_lease is None
                or latest_lease.lease_id
                != decision.temporary_lease_id
            ):
                return {
                    "state":
                        latest,

                    "control":
                        latest_control,

                    "consumed":
                        False,

                    "superseded":
                        True,
                }

            try:
                updated = (
                    consume_temporary_turn(
                        latest_control,
                        decision,
                    )
                )

            except ReasoningControlError as exc:
                raise TaskSessionError(
                    "Could not consume latest "
                    "temporary reasoning lease."
                ) from exc

            committed = copy.deepcopy(
                latest
            )

            committed[
                "reasoning_control"
            ] = reasoning_control_to_mapping(
                updated
            )

            self.normalize_task_session(
                committed
            )

            self._atomic_write_yaml(
                self.state_file,
                committed,
            )

        return {
            "state":
                committed,

            "control":
                updated,

            "consumed":
                True,

            "superseded":
                False,
        }


    def prepare_model_form_turn(
        self,
        state,
        *,
        execution_context_id,
        exact_form=None,
        automatic_form=None,
    ):
        """Resolve and freeze Model Form for one turn.

        This preparation step performs no runtime I/O,
        creates no runtime session, and persists no state.

        The execution context is deliberately explicit.
        TaskSessionManager must not silently invent Main,
        Ortet, Ramet, or ctx-default semantics here.
        """

        if state is None:
            state = self.load_state()

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        if (
            not isinstance(
                execution_context_id,
                str,
            )
            or not execution_context_id.strip()
        ):
            raise TaskSessionError(
                "Model Form turn preparation requires "
                "an explicit non-empty "
                "execution_context_id."
            )

        execution_context_id = (
            execution_context_id.strip()
        )

        # This is already the authoritative runtime Task
        # validator. Do not independently reinterpret
        # Task lifecycle state here.
        active_task = self._active_runtime_task(
            state
        )

        task_id = active_task["id"]

        # The legacy scalar state['model_form'] is NOT
        # authoritative Model Form control.
        #
        # Missing new control state intentionally becomes
        # an Auto baseline for this exact execution
        # context through the canonical control loader.
        raw_control = state.get(
            "model_form_control"
        )

        try:
            control = (
                model_form_control_from_mapping(
                    raw_control,
                    execution_context_id=(
                        execution_context_id
                    ),
                )
            )

        except ModelFormControlError as exc:
            raise TaskSessionError(
                "Forest Model Form control "
                f"is invalid: {exc}"
            ) from exc

        registry = (
            self.load_model_binding_registry()
        )

        try:
            return resolve_model_form_turn(
                control,
                registry,
                task_id=task_id,
                exact_form=exact_form,
                automatic_form=automatic_form,
            )

        except ModelFormResolutionError as exc:
            raise TaskSessionError(
                "Forest could not resolve "
                f"Model Form for this turn: {exc}"
            ) from exc

    @staticmethod
    def _execution_state_for_model_form_turn(
        state,
        frozen_turn,
    ):
        """Build an ephemeral runtime view for one frozen turn.

        The caller's Forest state is never mutated.

        Only the returned execution copy receives the
        frozen Model Binding runtime configuration.

        This helper performs no runtime I/O and persists
        nothing.
        """

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        if not isinstance(
            frozen_turn,
            FrozenModelFormTurn,
        ):
            raise TaskSessionError(
                "frozen_turn must be "
                "FrozenModelFormTurn."
            )

        runtime_state = (
            frozen_turn.runtime_state
        )

        if not isinstance(
            runtime_state,
            dict,
        ):
            raise TaskSessionError(
                "Frozen Model Form runtime state "
                "must be a mapping."
            )

        if not runtime_state.get(
            "adapter"
        ):
            raise TaskSessionError(
                "Frozen Model Form runtime state "
                "has no adapter."
            )

        execution_state = copy.deepcopy(
            state
        )

        execution_state["runtime"] = (
            copy.deepcopy(
                runtime_state
            )
        )

        return execution_state


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
    def _runtime_adapters_for_sessions(
        runtime_sessions,
    ):
        """Return adapter names from either session schema.

        Canonical:
            execution_context_id
                -> binding_id
                    -> entry with adapter

        Legacy transition format:
            adapter_name
                -> session entry
        """

        if runtime_sessions is None:
            return []

        if not isinstance(
            runtime_sessions,
            dict,
        ):
            raise TaskSessionError(
                "runtime_sessions must be a mapping."
            )

        if not runtime_sessions:
            return []

        try:
            return runtime_session_adapters(
                runtime_sessions
            )

        except RuntimeSessionStoreError:
            legacy_shape = all(
                isinstance(entry, dict)
                and "session_id" in entry
                for entry
                in runtime_sessions.values()
            )

            if not legacy_shape:
                raise TaskSessionError(
                    "Cannot determine runtime adapters "
                    "from unknown session storage."
                )

            adapters = []

            for adapter_name in runtime_sessions:
                adapter_name = str(
                    adapter_name
                ).strip()

                if not adapter_name:
                    raise TaskSessionError(
                        "Legacy runtime adapter name "
                        "cannot be empty."
                    )

                adapters.append(
                    adapter_name
                )

            return sorted(
                set(adapters)
            )


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

    def _runtime_session_binding_for_identity(
        self,
        working,
        execution_context_id,
        binding_id,
    ):
        """Read one canonical context+binding session.

        execution_context_id identifies the independently
        operating Tree context.

        binding_id identifies the selected model/runtime
        configuration.

        Adapter name is deliberately not used as the
        Forest-side session lookup key.
        """

        self._active_runtime_task(
            working
        )

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
            "runtime_sessions",
            {},
        )

        try:
            return get_runtime_session_binding(
                runtime_sessions,
                execution_context_id,
                binding_id,
            )

        except RuntimeSessionStoreError as exc:
            raise TaskSessionError(
                "Could not read canonical "
                "context+binding runtime session."
            ) from exc


    def _write_runtime_session_binding_for_identity(
        self,
        working,
        execution_context_id,
        binding_id,
        adapter_name,
        session_id,
        previous_session_id=None,
    ):
        """Write one canonical context+binding session.

        The Forest-side session slot is selected by:

            execution_context_id + binding_id

        adapter_name remains runtime implementation
        metadata rather than session identity.
        """

        self._active_runtime_task(
            working
        )

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
            "runtime_sessions",
            {},
        )

        now = self._now_utc()

        try:
            updated = set_runtime_session_binding(
                runtime_sessions,
                execution_context_id,
                binding_id,
                adapter=adapter_name,
                session_id=session_id,
                previous_session_id=
                    previous_session_id,
                updated_at=now,
            )

            binding = get_runtime_session_binding(
                updated,
                execution_context_id,
                binding_id,
            )

        except RuntimeSessionStoreError as exc:
            raise TaskSessionError(
                "Could not write canonical "
                "context+binding runtime session."
            ) from exc

        task_session[
            "runtime_sessions"
        ] = updated

        task_session[
            "updated_at"
        ] = now

        return binding


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

    def _capture_runtime_persist_guard_for_identity(
        self,
        working,
        execution_context_id,
        binding_id,
        adapter_name,
    ):
        """Capture one canonical persisted session generation.

        Session identity is selected by:

            execution_context_id + binding_id

        Adapter remains verified runtime metadata rather
        than the Forest-side storage key.
        """

        working_task = self._active_runtime_task(
            working
        )

        expected_task_id = working_task["id"]

        adapter_name = str(
            adapter_name
        ).strip()

        if not adapter_name:
            raise TaskSessionError(
                "Runtime persistence guard requires "
                "a non-empty adapter name."
            )

        with self._state_write_lock():
            persisted = self.load_state()

            persisted_task = (
                self._active_runtime_task(
                    persisted
                )
            )

            if (
                persisted_task["id"]
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Persistent runtime operation refused: "
                    "the supplied Forest Task is not the "
                    "currently active persisted Task."
                )

            try:
                persisted_binding = (
                    get_runtime_session_binding(
                        persisted_task[
                            "runtime_sessions"
                        ],
                        execution_context_id,
                        binding_id,
                    )
                )

            except RuntimeSessionStoreError as exc:
                raise TaskSessionError(
                    "Could not read persisted canonical "
                    "runtime-session binding."
                ) from exc

            persisted_session_id = None

            if persisted_binding is not None:
                persisted_adapter = str(
                    persisted_binding.get(
                        "adapter"
                    )
                    or ""
                ).strip()

                if (
                    persisted_adapter
                    != adapter_name
                ):
                    raise TaskSessionError(
                        "Persisted runtime binding adapter "
                        "does not match the requested "
                        "runtime adapter."
                    )

                persisted_session_id = (
                    persisted_binding.get(
                        "session_id"
                    )
                )

                if persisted_session_id is not None:
                    persisted_session_id = str(
                        persisted_session_id
                    )

        return {
            "task_id":
                expected_task_id,

            "execution_context_id":
                str(
                    execution_context_id
                ).strip(),

            "binding_id":
                str(
                    binding_id
                ).strip(),

            "adapter":
                adapter_name,

            "session_id":
                persisted_session_id,
        }


    def _persist_runtime_binding_guarded_for_identity(
        self,
        working,
        guard,
    ):
        """CAS-merge one canonical runtime binding.

        The compare-and-swap slot is selected by:

            execution_context_id + binding_id
        """

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

        execution_context_id = str(
            guard.get(
                "execution_context_id"
            )
            or ""
        ).strip()

        binding_id = str(
            guard.get(
                "binding_id"
            )
            or ""
        ).strip()

        adapter_name = str(
            guard.get(
                "adapter"
            )
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
            not execution_context_id
            or not binding_id
            or not adapter_name
            or target_task["id"]
            != expected_task_id
        ):
            raise TaskSessionError(
                "Runtime persistence guard does not "
                "match the supplied Forest Task "
                "and canonical session identity."
            )

        try:
            source_binding = (
                get_runtime_session_binding(
                    target_task[
                        "runtime_sessions"
                    ],
                    execution_context_id,
                    binding_id,
                )
            )

        except RuntimeSessionStoreError as exc:
            raise TaskSessionError(
                "Could not read source canonical "
                "runtime binding."
            ) from exc

        if not isinstance(
            source_binding,
            dict,
        ):
            raise TaskSessionError(
                "No canonical runtime binding "
                "is available to persist."
            )

        source_adapter = str(
            source_binding.get(
                "adapter"
            )
            or ""
        ).strip()

        if source_adapter != adapter_name:
            raise TaskSessionError(
                "Source runtime binding adapter "
                "does not match persistence guard."
            )

        source_session_id = (
            source_binding.get(
                "session_id"
            )
        )

        if not source_session_id:
            raise TaskSessionError(
                "Runtime binding has no session_id."
            )

        source_session_id = str(
            source_session_id
        )

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self._active_runtime_task(
                    latest
                )
            )

            if (
                latest_task["id"]
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Stale Forest Task generation: "
                    "active.yaml changed before "
                    "runtime binding commit."
                )

            try:
                latest_binding = (
                    get_runtime_session_binding(
                        latest_task[
                            "runtime_sessions"
                        ],
                        execution_context_id,
                        binding_id,
                    )
                )

            except RuntimeSessionStoreError as exc:
                raise TaskSessionError(
                    "Could not read latest canonical "
                    "runtime binding."
                ) from exc

            latest_session_id = None

            if latest_binding is not None:
                latest_adapter = str(
                    latest_binding.get(
                        "adapter"
                    )
                    or ""
                ).strip()

                if latest_adapter != adapter_name:
                    raise TaskSessionError(
                        "Stale runtime binding adapter: "
                        "persisted adapter changed before "
                        "runtime binding commit."
                    )

                latest_session_id = (
                    latest_binding.get(
                        "session_id"
                    )
                )

                if latest_session_id is not None:
                    latest_session_id = str(
                        latest_session_id
                    )

            if (
                latest_session_id
                != expected_session_id
            ):
                raise TaskSessionError(
                    "Stale canonical runtime binding: "
                    f"expected session "
                    f"{expected_session_id!r}, "
                    f"found {latest_session_id!r}."
                )

            try:
                latest_task[
                    "runtime_sessions"
                ] = set_runtime_session_binding(
                    latest_task[
                        "runtime_sessions"
                    ],
                    execution_context_id,
                    binding_id,
                    adapter=source_adapter,
                    session_id=
                        source_session_id,
                    previous_session_id=
                        source_binding.get(
                            "previous_session_id"
                        ),
                    updated_at=
                        source_binding.get(
                            "updated_at"
                        ),
                )

            except RuntimeSessionStoreError as exc:
                raise TaskSessionError(
                    "Could not merge canonical "
                    "runtime binding."
                ) from exc

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


    def _rollback_runtime_binding_guarded_for_identity(
        self,
        working,
        guard,
        restore_binding,
    ):
        """CAS-rollback one canonical context+binding slot.

        The durable slot is changed only while it still
        points at the exact session generation described
        by guard.

        restore_binding:
            dict
                Restore the prior canonical binding.

            None
                The target binding did not exist before
                this transaction. Remove only the binding
                introduced by the failed transaction.

        This helper repairs Forest state only. It never
        ends or creates runtime sessions.
        """

        if not isinstance(
            guard,
            dict,
        ):
            raise TaskSessionError(
                "Runtime rollback guard must "
                "be a mapping."
            )

        target_task = (
            self._active_runtime_task(
                working
            )
        )

        expected_task_id = guard.get(
            "task_id"
        )

        execution_context_id = str(
            guard.get(
                "execution_context_id"
            )
            or ""
        ).strip()

        binding_id = str(
            guard.get(
                "binding_id"
            )
            or ""
        ).strip()

        adapter_name = str(
            guard.get(
                "adapter"
            )
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
            not expected_task_id
            or not execution_context_id
            or not binding_id
            or not adapter_name
            or not expected_session_id
        ):
            raise TaskSessionError(
                "Runtime rollback guard is incomplete."
            )

        if (
            str(
                target_task.get(
                    "id"
                )
                or ""
            ).strip()
            != str(
                expected_task_id
            ).strip()
        ):
            raise TaskSessionError(
                "Runtime rollback guard does not "
                "match the supplied active Task."
            )

        canonical_restore = None

        if restore_binding is not None:
            if not isinstance(
                restore_binding,
                dict,
            ):
                raise TaskSessionError(
                    "Runtime rollback restore binding "
                    "must be a mapping or None."
                )

            restore_adapter = str(
                restore_binding.get(
                    "adapter"
                )
                or ""
            ).strip()

            restore_session_id = (
                restore_binding.get(
                    "session_id"
                )
            )

            if restore_session_id is not None:
                restore_session_id = str(
                    restore_session_id
                )

            if (
                not restore_adapter
                or not restore_session_id
            ):
                raise TaskSessionError(
                    "Runtime rollback restore binding "
                    "is incomplete."
                )

            if restore_adapter != adapter_name:
                raise TaskSessionError(
                    "Runtime rollback restore binding "
                    "uses a different adapter."
                )

            canonical_restore = copy.deepcopy(
                restore_binding
            )

        with self._state_write_lock():
            latest = self.load_state()

            latest_task = (
                self.normalize_task_session(
                    latest
                )
            )

            if (
                latest_task.get(
                    "status"
                )
                != "active"
                or latest_task.get(
                    "id"
                )
                != expected_task_id
            ):
                raise TaskSessionError(
                    "Persistent runtime rollback refused: "
                    "the active Forest Task changed."
                )

            runtime_sessions = latest_task.get(
                "runtime_sessions"
            )

            if not isinstance(
                runtime_sessions,
                dict,
            ):
                raise TaskSessionError(
                    "Latest canonical runtime_sessions "
                    "is not a mapping."
                )

            try:
                latest_binding = (
                    get_runtime_session_binding(
                        runtime_sessions,
                        execution_context_id,
                        binding_id,
                    )
                )

            except RuntimeSessionStoreError as exc:
                raise TaskSessionError(
                    "Could not read latest canonical "
                    "runtime binding for rollback."
                ) from exc

            if not isinstance(
                latest_binding,
                dict,
            ):
                raise TaskSessionError(
                    "Stale runtime rollback: "
                    "the target binding disappeared."
                )

            latest_adapter = str(
                latest_binding.get(
                    "adapter"
                )
                or ""
            ).strip()

            latest_session_id = (
                latest_binding.get(
                    "session_id"
                )
            )

            if latest_session_id is not None:
                latest_session_id = str(
                    latest_session_id
                )

            if latest_adapter != adapter_name:
                raise TaskSessionError(
                    "Stale runtime rollback adapter: "
                    "persisted adapter changed before "
                    "rollback."
                )

            if (
                latest_session_id
                != expected_session_id
            ):
                raise TaskSessionError(
                    "Stale runtime rollback session: "
                    f"expected {expected_session_id!r}, "
                    f"found {latest_session_id!r}."
                )

            if canonical_restore is not None:
                try:
                    latest_task[
                        "runtime_sessions"
                    ] = set_runtime_session_binding(
                        runtime_sessions,
                        execution_context_id,
                        binding_id,
                        adapter=
                            canonical_restore[
                                "adapter"
                            ],
                        session_id=
                            canonical_restore[
                                "session_id"
                            ],
                        previous_session_id=
                            canonical_restore.get(
                                "previous_session_id"
                            ),
                        updated_at=
                            canonical_restore.get(
                                "updated_at"
                            ),
                    )

                except RuntimeSessionStoreError as exc:
                    raise TaskSessionError(
                        "Could not restore canonical "
                        "runtime binding."
                    ) from exc

            else:
                # No target binding existed before the
                # failed handoff. Remove only the slot
                # whose generation was verified above.
                context_sessions = (
                    runtime_sessions.get(
                        execution_context_id
                    )
                )

                if not isinstance(
                    context_sessions,
                    dict,
                ):
                    raise TaskSessionError(
                        "Stale runtime rollback: "
                        "execution-context session bucket "
                        "disappeared."
                    )

                if binding_id not in context_sessions:
                    raise TaskSessionError(
                        "Stale runtime rollback: "
                        "binding disappeared before "
                        "removal."
                    )

                context_sessions = copy.deepcopy(
                    context_sessions
                )

                context_sessions.pop(
                    binding_id
                )

                runtime_sessions = copy.deepcopy(
                    runtime_sessions
                )

                if context_sessions:
                    runtime_sessions[
                        execution_context_id
                    ] = context_sessions

                else:
                    runtime_sessions.pop(
                        execution_context_id,
                        None,
                    )

                latest_task[
                    "runtime_sessions"
                ] = runtime_sessions

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

    def _bootstrap_runtime_session_for_model_form_handoff(
        self,
        *,
        state,
        frozen_turn,
        continuity,
    ):
        """Create one fresh target-form session from continuity.

        E4E3B is deliberately detached:

        - no persistent Forest write
        - no user-message send
        - no reasoning consumption
        - no successful-turn semantic commit
        - no retirement of an older target session

        If the target context+binding already has a runtime
        session, its ID is returned as replaced_session_id.
        E4E3C owns persistence and safe retirement.
        """

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Model Form handoff bootstrap "
                "requires Forest state."
            )

        if not isinstance(
            frozen_turn,
            FrozenModelFormTurn,
        ):
            raise TaskSessionError(
                "Model Form handoff bootstrap "
                "requires FrozenModelFormTurn."
            )

        try:
            from model_form.continuity import (
                ModelFormContinuity,
            )

        except Exception as exc:
            raise TaskSessionError(
                "Model Form continuity backend "
                "is unavailable."
            ) from exc

        if not isinstance(
            continuity,
            ModelFormContinuity,
        ):
            raise TaskSessionError(
                "Model Form handoff bootstrap "
                "requires ModelFormContinuity."
            )

        context_id = (
            self._effective_model_form_context_id(
                frozen_turn.execution_context_id
            )
        )

        task_id = str(
            frozen_turn.task_id
            or ""
        ).strip()

        if not task_id:
            raise TaskSessionError(
                "Frozen Model Form turn has "
                "no Task identity."
            )

        if (
            continuity.execution_context_id
            != context_id
            or continuity.task_id
            != task_id
        ):
            raise TaskSessionError(
                "Model Form continuity does not "
                "match the frozen handoff identity."
            )

        working = copy.deepcopy(
            state
        )

        active_task = (
            self._active_runtime_task(
                working
            )
        )

        if (
            str(
                active_task["id"]
            ).strip()
            != task_id
        ):
            raise TaskSessionError(
                "Model Form handoff bootstrap "
                "crossed Task identity."
            )

        execution_state = (
            self._execution_state_for_model_form_turn(
                working,
                frozen_turn,
            )
        )

        runtime_adapter = (
            self._runtime_adapter_for_state(
                execution_state
            )
        )

        adapter_name = (
            self._runtime_adapter_name(
                runtime_adapter
            )
        )

        if (
            adapter_name
            != frozen_turn.adapter
        ):
            raise TaskSessionError(
                "Runtime adapter does not match "
                "the frozen Model Binding."
            )

        existing_binding = (
            self._runtime_session_binding_for_identity(
                working,
                context_id,
                frozen_turn.binding_id,
            )
        )

        replaced_session_id = None

        if existing_binding is not None:
            if not isinstance(
                existing_binding,
                dict,
            ):
                raise TaskSessionError(
                    "Existing target runtime binding "
                    "is not a mapping."
                )

            existing_adapter = str(
                existing_binding.get(
                    "adapter"
                )
                or ""
            ).strip()

            if (
                existing_adapter
                and existing_adapter
                != adapter_name
            ):
                raise TaskSessionError(
                    "Existing target runtime binding "
                    "uses a different adapter."
                )

            old_session_id = (
                existing_binding.get(
                    "session_id"
                )
            )

            if old_session_id is not None:
                replaced_session_id = str(
                    old_session_id
                )

        creator = getattr(
            runtime_adapter,
            "create_session_with_continuity",
            None,
        )

        if not callable(
            creator
        ):
            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                "does not provide continuity bootstrap."
            )

        try:
            from runtime.adapters.base import (
                RuntimeContinuityUnsupportedError,
            )

            created = creator(
                execution_state,
                continuity,
                task_id=task_id,
            )

        except RuntimeContinuityUnsupportedError as exc:
            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                "does not support Model Form "
                "continuity bootstrap."
            ) from exc

        except TaskSessionError:
            raise

        except Exception as exc:
            raise TaskSessionError(
                f"Runtime adapter {adapter_name!r} "
                "could not bootstrap Model Form "
                f"continuity: {exc}"
            ) from exc

        if not isinstance(
            created,
            dict,
        ):
            raise TaskSessionError(
                "Continuity bootstrap must "
                "return a mapping."
            )

        raw_session_id = created.get(
            "session_id"
        )

        session_id = (
            str(
                raw_session_id
            )
            if raw_session_id
            else None
        )

        returned_adapter = created.get(
            "adapter",
            adapter_name,
        )

        if (
            str(
                returned_adapter
            )
            != adapter_name
        ):
            # A newly-created session is not yet bound
            # into Forest state. If the adapter result
            # fails validation and gives us its ID,
            # retire that fresh unbound session.
            #
            # Never retire replaced_session_id here:
            # that is the older canonical target-form
            # session and E4E3C owns its retirement.
            if (
                session_id is not None
                and session_id
                != replaced_session_id
            ):
                self._best_effort_end_runtime_sessions(
                    runtime_adapter,
                    [session_id],
                    execution_state,
                )

            raise TaskSessionError(
                "Continuity bootstrap returned "
                "a mismatched adapter."
            )

        if session_id is None:
            raise TaskSessionError(
                "Continuity bootstrap created "
                "a session without session_id."
            )

        if (
            replaced_session_id is not None
            and session_id
            == replaced_session_id
        ):
            # The adapter failed the fresh-session
            # contract but returned the existing
            # canonical session. Do not destroy it.
            raise TaskSessionError(
                "Model Form handoff bootstrap "
                "must create a fresh runtime session."
            )

        try:
            binding = (
                self._write_runtime_session_binding_for_identity(
                    working,
                    context_id,
                    frozen_turn.binding_id,
                    adapter_name,
                    session_id,
                    previous_session_id=
                        replaced_session_id,
                )
            )

        except Exception:
            self._best_effort_end_runtime_sessions(
                runtime_adapter,
                [session_id],
                execution_state,
            )

            raise

        return {
            "state":
                working,

            "execution_state":
                self._execution_state_for_model_form_turn(
                    working,
                    frozen_turn,
                ),

            "task_session":
                self.normalize_task_session(
                    working
                ),

            "execution_context_id":
                context_id,

            "binding_id":
                frozen_turn.binding_id,

            "adapter":
                adapter_name,

            "session_id":
                binding[
                    "session_id"
                ],

            "previous_session_id":
                binding.get(
                    "previous_session_id"
                ),

            "replaced_session_id":
                replaced_session_id,

            "created":
                True,

            "reused":
                False,

            "continuity_bootstrapped":
                True,

            "runtime_result":
                created,
        }


    def _ensure_runtime_session_for_frozen_turn(
        self,
        *,
        state,
        frozen_turn,
        persist=False,
    ):
        """Create or reuse one frozen context+binding session.

        The Forest-side session identity is:

            execution_context_id + binding_id

        Adapter name is runtime metadata only.

        This D4C1 path is deliberately in-memory only.
        Persistent CAS wiring is certified separately.
        """

        if not isinstance(
            frozen_turn,
            FrozenModelFormTurn,
        ):
            raise TaskSessionError(
                "frozen_turn must be "
                "FrozenModelFormTurn."
            )

        if state is None:
            state = self.load_state()

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        working = copy.deepcopy(
            state
        )

        task_session = (
            self._active_runtime_task(
                working
            )
        )

        active_task_id = str(
            task_session["id"]
        ).strip()

        frozen_task_id = (
            str(
                frozen_turn.task_id
                or ""
            ).strip()
        )

        if not frozen_task_id:
            raise TaskSessionError(
                "Frozen Model Form turn has no "
                "Task identity."
            )

        if frozen_task_id != active_task_id:
            raise TaskSessionError(
                "Frozen Model Form turn belongs "
                "to a different Forest Task."
            )

        execution_context_id = (
            frozen_turn.execution_context_id
        )

        binding_id = (
            frozen_turn.binding_id
        )

        execution_state = (
            self._execution_state_for_model_form_turn(
                working,
                frozen_turn,
            )
        )

        runtime_adapter = (
            self._runtime_adapter_for_state(
                execution_state
            )
        )

        adapter_name = (
            self._runtime_adapter_name(
                runtime_adapter
            )
        )

        expected_adapter = str(
            frozen_turn.adapter
        ).strip()

        if adapter_name != expected_adapter:
            raise TaskSessionError(
                "Resolved runtime adapter does not "
                "match the frozen Model Binding."
            )

        persist_guard = None

        if persist:
            persist_guard = (
                self._capture_runtime_persist_guard_for_identity(
                    working,
                    execution_context_id,
                    binding_id,
                    adapter_name,
                )
            )

        existing = (
            self._runtime_session_binding_for_identity(
                working,
                execution_context_id,
                binding_id,
            )
        )

        if isinstance(
            existing,
            dict,
        ):
            existing_adapter = str(
                existing.get(
                    "adapter"
                )
                or ""
            ).strip()

            if (
                existing_adapter
                and existing_adapter
                != adapter_name
            ):
                raise TaskSessionError(
                    "Existing context+binding session "
                    "has a mismatched adapter."
                )

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
                        self._persist_runtime_binding_guarded_for_identity(
                            working,
                            persist_guard,
                        )
                    )

                    task_session = (
                        self._active_runtime_task(
                            working
                        )
                    )

                    existing = (
                        self._runtime_session_binding_for_identity(
                            working,
                            execution_context_id,
                            binding_id,
                        )
                    )

                    if not isinstance(
                        existing,
                        dict,
                    ):
                        raise TaskSessionError(
                            "Persisted canonical runtime "
                            "binding disappeared after commit."
                        )

                    existing_id = str(
                        existing["session_id"]
                    )

                return {
                    "state":
                        working,

                    "execution_state":
                        self._execution_state_for_model_form_turn(
                            working,
                            frozen_turn,
                        ),

                    "task_session":
                        self.normalize_task_session(
                            working
                        ),

                    "execution_context_id":
                        execution_context_id,

                    "binding_id":
                        binding_id,

                    "model_form":
                        frozen_turn.form,

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
                execution_state,
                task_id=active_task_id,
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

        try:
            binding = (
                self._write_runtime_session_binding_for_identity(
                    working,
                    execution_context_id,
                    binding_id,
                    adapter_name,
                    session_id,
                    previous_session_id=None,
                )
            )

        except Exception:
            self._best_effort_end_runtime_sessions(
                runtime_adapter,
                [session_id],
                execution_state,
            )
            raise

        if persist:
            try:
                working = (
                    self._persist_runtime_binding_guarded_for_identity(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                # The newly created session did not win
                # the Forest CAS boundary. It is therefore
                # not authoritative and may be cleaned up.
                self._best_effort_end_runtime_sessions(
                    runtime_adapter,
                    [session_id],
                    execution_state,
                )
                raise

            binding = (
                self._runtime_session_binding_for_identity(
                    working,
                    execution_context_id,
                    binding_id,
                )
            )

            if not isinstance(
                binding,
                dict,
            ):
                raise TaskSessionError(
                    "Persisted canonical runtime "
                    "binding disappeared after commit."
                )

        return {
            "state":
                working,

            "execution_state":
                self._execution_state_for_model_form_turn(
                    working,
                    frozen_turn,
                ),

            "task_session":
                self.normalize_task_session(
                    working
                ),

            "execution_context_id":
                execution_context_id,

            "binding_id":
                binding_id,

            "model_form":
                frozen_turn.form,

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


    def ensure_runtime_session(
        self,
        state=None,
        persist=False,
        frozen_turn=None,
    ):
        """Create or reuse the Task's runtime session.

        Forest owns the binding. The runtime adapter
        owns creation of the runtime-specific session.

        Persistent writes use the Forest Task ID and
        prior persisted runtime session as a guarded
        compare-and-swap boundary.
        """

        if frozen_turn is not None:
            return (
                self._ensure_runtime_session_for_frozen_turn(
                    state=state,
                    frozen_turn=frozen_turn,
                    persist=persist,
                )
            )

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

    def _send_runtime_turn_for_frozen_model_form(
        self,
        message,
        *,
        execution_context_id,
        state=None,
        instructions=None,
        instruction_composition=None,
        reasoning_mode=None,
        persist=False,
        model_form=None,
        automatic_model_form=None,
    ):
        """Send one normal turn through one frozen Model Form.

        Model Form is resolved exactly once before the
        meaningful-input transition.

        Stale-session recovery is deliberately not handled
        here until 14.11D5.
        """

        if state is None:
            state = self.load_state()

        if not isinstance(
            state,
            dict,
        ):
            raise TaskSessionError(
                "Forest state must be a mapping."
            )

        # For a persistent turn, human controls are resolved
        # from the latest durable Forest state.
        # ----------------------------------------------
        # FROZEN INSTRUCTION COMPOSITION
        # ----------------------------------------------
        if instruction_composition is not None:
            try:
                from turn_composition import (
                    ForestTurnInstructionComposition,
                )

            except Exception as exc:
                raise TaskSessionError(
                    "Forest turn-composition backend "
                    "is unavailable."
                ) from exc

            if not isinstance(
                instruction_composition,
                ForestTurnInstructionComposition,
            ):
                raise TaskSessionError(
                    "instruction_composition must be "
                    "ForestTurnInstructionComposition "
                    "or None."
                )

            composition_instructions = (
                instruction_composition.instructions
            )

            if instructions is None:
                instructions = (
                    composition_instructions
                )

            elif (
                instructions
                is not composition_instructions
            ):
                raise TaskSessionError(
                    "instructions and "
                    "instruction_composition must "
                    "refer to the exact same frozen "
                    "instruction string object."
                )

        control_state = (
            self.load_state()
            if persist
            else state
        )

        # ----------------------------------------------
        # REASONING: resolve exactly once.
        # ----------------------------------------------
        try:
            from reasoning import (
                ReasoningControlError,
                ReasoningModeError,
                reasoning_control_from_mapping,
                resolve_effective_reasoning,
            )

            turn_reasoning_control = (
                reasoning_control_from_mapping(
                    control_state.get(
                        "reasoning_control"
                    )
                )
            )

            reasoning_decision = (
                resolve_effective_reasoning(
                    turn_reasoning_control,
                    message,
                    explicit_mode=reasoning_mode,
                )
            )

        except (
            ReasoningControlError,
            ReasoningModeError,
            ValueError,
        ) as exc:
            raise TaskSessionError(
                "Could not resolve Forest "
                "reasoning control for this turn."
            ) from exc

        resolved_reasoning_mode = (
            reasoning_decision.mode
        )

        # ----------------------------------------------
        # MODEL FORM: resolve exactly once.
        # ----------------------------------------------
        frozen_turn = (
            self.prepare_model_form_turn(
                control_state,
                execution_context_id=
                    execution_context_id,
                exact_form=model_form,
                automatic_form=
                    automatic_model_form,
            )
        )

        # Freeze the previous successful effective form
        # from the same pre-turn control snapshot used
        # to resolve this Model Form decision.
        #
        # Do not derive this later from post-runtime
        # working state: runtime-session persistence may
        # have refreshed that state while this turn was
        # in flight.
        turn_previous_effective_form = (
            self._effective_model_form_for_context(
                control_state,
                frozen_turn.execution_context_id,
            )
        )

        # Prepare portable Model Form handoff continuity
        # from pre-turn Forest truth. This remains pure:
        # no runtime I/O, persistence, or current-turn replay.
        handoff_preparation = (
            self._prepare_model_form_handoff_continuity(
                state=control_state,
                frozen_turn=frozen_turn,
                previous_form=
                    turn_previous_effective_form,
                instruction_composition=
                    instruction_composition,
            )
        )

        model_form_handoff = (
            handoff_preparation[
                "handoff"
            ]
        )

        model_form_continuity = (
            handoff_preparation[
                "continuity"
            ]
        )

        model_form_handoff_required = bool(
            handoff_preparation[
                "requires_runtime_bootstrap"
            ]
        )

        if model_form_handoff_required:
            if (
                model_form_handoff is None
                or model_form_continuity is None
            ):
                raise TaskSessionError(
                    "Model Form handoff preparation "
                    "requires canonical handoff and "
                    "continuity artifacts."
                )

        else:
            if (
                model_form_handoff is not None
                or model_form_continuity is not None
            ):
                raise TaskSessionError(
                    "Non-handoff Model Form turn "
                    "unexpectedly produced handoff "
                    "continuity artifacts."
                )

        # Transaction-local handoff state.
        #
        # C2A records these values but does not yet
        # perform semantic rollback or retirement.
        # Those responsibilities remain E4E3C2B.
        handoff_restore_binding = None
        handoff_replaced_session_id = None
        handoff_bootstrap_session_id = None

        caller_task = (
            self._active_runtime_task(
                state
            )
        )

        if (
            str(caller_task["id"]).strip()
            != str(
                frozen_turn.task_id
                or ""
            ).strip()
        ):
            raise TaskSessionError(
                "Frozen Model Form turn does not "
                "belong to the caller's active Task."
            )

        # Only after both human controls have resolved
        # does this become one meaningful input.
        context_route_state = (
            self._context_route_state_for_task(
                caller_task["id"]
            )
        )

        context_route_state.begin_meaningful_input()

        initial = copy.deepcopy(
            state
        )

        # Preserve existing persistent reasoning behavior:
        # use latest durable reasoning control.
        if persist:
            if (
                "reasoning_control"
                in control_state
            ):
                initial[
                    "reasoning_control"
                ] = copy.deepcopy(
                    control_state[
                        "reasoning_control"
                    ]
                )

            else:
                initial.pop(
                    "reasoning_control",
                    None,
                )

        initial_execution_state = (
            self._execution_state_for_model_form_turn(
                initial,
                frozen_turn,
            )
        )

        runtime_adapter = (
            self._runtime_adapter_for_state(
                initial_execution_state
            )
        )

        adapter_name = (
            self._runtime_adapter_name(
                runtime_adapter
            )
        )

        if adapter_name != frozen_turn.adapter:
            raise TaskSessionError(
                "Runtime adapter does not match "
                "the frozen Model Binding."
            )

        # Capture the persisted generation BEFORE any
        # runtime/session creation.
        persist_guard = None

        if persist:
            persist_guard = (
                self._capture_runtime_persist_guard_for_identity(
                    initial,
                    frozen_turn.execution_context_id,
                    frozen_turn.binding_id,
                    adapter_name,
                )
            )

        # Session selection uses the SAME frozen turn.
        if model_form_handoff_required:
            # Preserve the exact canonical target
            # binding that existed before bootstrap.
            # C2B may use it as the rollback anchor.
            handoff_restore_binding = (
                copy.deepcopy(
                    self._runtime_session_binding_for_identity(
                        initial,
                        frozen_turn.execution_context_id,
                        frozen_turn.binding_id,
                    )
                )
            )

            ensured = (
                self._bootstrap_runtime_session_for_model_form_handoff(
                    state=initial,
                    frozen_turn=frozen_turn,
                    continuity=
                        model_form_continuity,
                )
            )

            handoff_replaced_session_id = (
                ensured.get(
                    "replaced_session_id"
                )
            )

            handoff_bootstrap_session_id = str(
                ensured[
                    "session_id"
                ]
            )

        else:
            # Certified D5 same-form path.
            ensured = self.ensure_runtime_session(
                state=initial,
                persist=False,
                frozen_turn=frozen_turn,
            )

        working = ensured[
            "state"
        ]

        execution_state = ensured[
            "execution_state"
        ]

        runtime_adapter = (
            self._runtime_adapter_for_state(
                execution_state
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
            or current_adapter_name
            != ensured["adapter"]
            or current_adapter_name
            != frozen_turn.adapter
        ):
            raise TaskSessionError(
                "Runtime adapter changed while "
                "preparing the frozen turn."
            )

        requested_session_id = str(
            ensured["session_id"]
        )

        initial_requested_session_id = (
            requested_session_id
        )

        preturn_binding_persisted = False

        # ----------------------------------------------
        # CRASH-CONSISTENCY:
        # persist a newly selected session before model I/O.
        # ----------------------------------------------
        if (
            persist
            and persist_guard[
                "session_id"
            ] != requested_session_id
        ):
            try:
                working = (
                    self._persist_runtime_binding_guarded_for_identity(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                if ensured["created"]:
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [requested_session_id],
                        execution_state,
                    )

                raise

            preturn_binding_persisted = True

            persist_guard = {
                "task_id":
                    persist_guard["task_id"],

                "execution_context_id":
                    frozen_turn.execution_context_id,

                "binding_id":
                    frozen_turn.binding_id,

                "adapter":
                    adapter_name,

                "session_id":
                    requested_session_id,
            }

            # Persistence returned the newest Forest state.
            # Rebuild only the ephemeral runtime view from
            # the SAME frozen turn.
            execution_state = (
                self._execution_state_for_model_form_turn(
                    working,
                    frozen_turn,
                )
            )

            runtime_adapter = (
                self._runtime_adapter_for_state(
                    execution_state
                )
            )

            if (
                self._runtime_adapter_name(
                    runtime_adapter
                )
                != adapter_name
            ):
                raise TaskSessionError(
                    "Runtime adapter changed during "
                    "frozen pre-turn persistence."
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

        # ----------------------------------------------
        # ONE-SHOT FROZEN STALE-SESSION RECOVERY
        # ----------------------------------------------
        #
        # Model Form and reasoning were already resolved.
        # Recovery MUST reuse those exact decisions.
        session_recovered = False
        recovery_from_session_id = None
        recovery_session_id = None
        recovery_runtime_result = None
        recovery_binding_persisted = False

        try:
            result = sender(
                requested_session_id,
                message,
                execution_state,
                instructions=instructions,
                reasoning_mode=
                    resolved_reasoning_mode,
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
                        classifier(
                            exc
                        )
                    )

                except Exception:
                    stale_session = False

            if not stale_session:
                raise

            recovery_from_session_id = (
                requested_session_id
            )

            # Rebuild only the ephemeral execution view.
            # This uses the SAME FrozenModelFormTurn.
            execution_state = (
                self._execution_state_for_model_form_turn(
                    working,
                    frozen_turn,
                )
            )

            runtime_adapter = (
                self._runtime_adapter_for_state(
                    execution_state
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
                or current_adapter_name
                != frozen_turn.adapter
            ):
                raise TaskSessionError(
                    "Runtime adapter changed during "
                    "frozen stale-session recovery."
                ) from exc

            if model_form_handoff_required:
                # A handoff replacement must preserve the same
                # frozen Forest continuity. Ordinary empty
                # create_session() would lose conversation
                # completed before this current user turn.
                try:
                    recovery_handoff_bootstrap = (
                        self._bootstrap_runtime_session_for_model_form_handoff(
                            state=working,
                            frozen_turn=frozen_turn,
                            continuity=
                                model_form_continuity,
                        )
                    )

                except Exception as create_exc:
                    raise TaskSessionError(
                        f"Runtime adapter {adapter_name!r} "
                        "could not create a continuity-backed "
                        "frozen replacement session: "
                        f"{create_exc}"
                    ) from create_exc

                working = (
                    recovery_handoff_bootstrap[
                        "state"
                    ]
                )

                execution_state = (
                    recovery_handoff_bootstrap[
                        "execution_state"
                    ]
                )

                created = (
                    recovery_handoff_bootstrap[
                        "runtime_result"
                    ]
                )

            else:
                creator = getattr(
                    runtime_adapter,
                    "create_session",
                    None,
                )

                if not callable(
                    creator
                ):
                    raise TaskSessionError(
                        f"Runtime adapter "
                        f"{adapter_name!r} cannot "
                        "recover a stale session because "
                        "create_session() is unavailable."
                    ) from exc

                active_task = (
                    self._active_runtime_task(
                        working
                    )
                )

                if (
                    str(
                        active_task["id"]
                    ).strip()
                    != str(
                        frozen_turn.task_id
                        or ""
                    ).strip()
                ):
                    raise TaskSessionError(
                        "Frozen stale-session recovery "
                        "crossed Forest Task identity."
                    ) from exc

                try:
                    created = creator(
                        execution_state,
                        task_id=active_task[
                            "id"
                        ],
                    )

                except Exception as create_exc:
                    raise TaskSessionError(
                        f"Runtime adapter "
                        f"{adapter_name!r} could not "
                        "create a frozen replacement "
                        f"session: {create_exc}"
                    ) from create_exc

            if not isinstance(
                created,
                dict,
            ):
                raise TaskSessionError(
                    "Replacement runtime-session "
                    "creation must return a mapping."
                )

            returned_adapter = created.get(
                "adapter",
                adapter_name,
            )

            if str(
                returned_adapter
            ) != adapter_name:
                raise TaskSessionError(
                    "Replacement runtime session "
                    "returned a mismatched adapter."
                )

            replacement_session_id = (
                created.get(
                    "session_id"
                )
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

            recovery_runtime_result = (
                created
            )

            try:
                self._write_runtime_session_binding_for_identity(
                    working,
                    frozen_turn.execution_context_id,
                    frozen_turn.binding_id,
                    adapter_name,
                    replacement_session_id,
                    previous_session_id=
                        recovery_from_session_id,
                )

            except Exception:
                self._best_effort_end_runtime_sessions(
                    runtime_adapter,
                    [replacement_session_id],
                    execution_state,
                )
                raise

            # Persist replacement BEFORE retrying so a
            # successful retry cannot depend on a session
            # Forest never made durable.
            if persist:
                try:
                    working = (
                        self._persist_runtime_binding_guarded_for_identity(
                            working,
                            persist_guard,
                        )
                    )

                except Exception:
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [replacement_session_id],
                        execution_state,
                    )
                    raise

                recovery_binding_persisted = True

                # Any later runtime rotation compares
                # against the replacement generation.
                persist_guard = {
                    "task_id":
                        persist_guard[
                            "task_id"
                        ],

                    "execution_context_id":
                        frozen_turn.execution_context_id,

                    "binding_id":
                        frozen_turn.binding_id,

                    "adapter":
                        adapter_name,

                    "session_id":
                        replacement_session_id,
                }

            # Whether persistent or in-memory, rebuild the
            # execution view from current Forest state using
            # the SAME frozen turn. Never consult mutable
            # global runtime selection.
            execution_state = (
                self._execution_state_for_model_form_turn(
                    working,
                    frozen_turn,
                )
            )

            runtime_adapter = (
                self._runtime_adapter_for_state(
                    execution_state
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
                or current_adapter_name
                != frozen_turn.adapter
            ):
                raise TaskSessionError(
                    "Runtime adapter changed before "
                    "frozen stale-session retry."
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
                    f"Runtime adapter "
                    f"{adapter_name!r} lost "
                    "send_turn() during frozen recovery."
                )

            requested_session_id = (
                replacement_session_id
            )

            session_recovered = True

            # Deliberately ONE retry.
            #
            # A second failure escapes immediately.
            # No second classification and no second
            # replacement session are allowed.
            try:
                result = sender(
                    requested_session_id,
                    message,
                    execution_state,
                    instructions=instructions,
                    reasoning_mode=
                        resolved_reasoning_mode,
                )

            except Exception:
                if not persist:
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [replacement_session_id],
                        execution_state,
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

        current_binding = (
            self._runtime_session_binding_for_identity(
                working,
                frozen_turn.execution_context_id,
                frozen_turn.binding_id,
            )
        )

        if not isinstance(
            current_binding,
            dict,
        ):
            raise TaskSessionError(
                "Canonical context+binding session "
                "disappeared during the turn."
            )

        previous_session_id = (
            current_binding.get(
                "previous_session_id"
            )
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
            self._write_runtime_session_binding_for_identity(
                working,
                frozen_turn.execution_context_id,
                frozen_turn.binding_id,
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
                    self._persist_runtime_binding_guarded_for_identity(
                        working,
                        persist_guard,
                    )
                )

            except Exception:
                # requested_session_id was already durable.
                # Only an uncommitted rotated child may be
                # cleaned up.
                if (
                    effective_session_id
                    != requested_session_id
                ):
                    self._best_effort_end_runtime_sessions(
                        runtime_adapter,
                        [effective_session_id],
                        execution_state,
                    )

                raise

            rotation_binding_persisted = True

            binding = (
                self._runtime_session_binding_for_identity(
                    working,
                    frozen_turn.execution_context_id,
                    frozen_turn.binding_id,
                )
            )

            if not isinstance(
                binding,
                dict,
            ):
                raise TaskSessionError(
                    "Persisted canonical runtime "
                    "binding disappeared after rotation."
                )

        # Runtime/model execution succeeded.
        #
        # Commit all Forest-owned successful-turn semantics
        # together. Failed runtime attempts never reach here.
        successful_turn_commit = (
            self._commit_successful_model_form_turn(
                working=working,
                frozen_turn=frozen_turn,
                user_message=message,
                assistant_message=result.get(
                    "message",
                    "",
                ),
                expected_previous_form=(
                    turn_previous_effective_form
                ),
                turn_control=turn_reasoning_control,
                decision=reasoning_decision,
                persist=persist,
            )
        )

        working = successful_turn_commit[
            "state"
        ]

        return {
            "state":
                working,

            "task_session":
                self.normalize_task_session(
                    working
                ),

            "execution_context_id":
                frozen_turn.execution_context_id,

            "binding_id":
                frozen_turn.binding_id,

            "model_form":
                frozen_turn.form,

            "model_form_source":
                frozen_turn.source,

            "model_form_reasons":
                frozen_turn.reasons,

            "adapter":
                adapter_name,

            "session_created":
                bool(
                    ensured["created"]
                    or session_recovered
                ),

            "initial_session_created":
                ensured["created"],

            "session_reused":
                ensured["reused"],

            "initial_requested_session_id":
                initial_requested_session_id,

            "requested_session_id":
                requested_session_id,

            "session_id":
                binding["session_id"],

            "previous_session_id":
                binding.get(
                    "previous_session_id"
                ),

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

            "resolved_reasoning_mode":
                resolved_reasoning_mode,
        }


    def send_runtime_turn(
        self,
        message,
        state=None,
        instructions=None,
        instruction_composition=None,
        reasoning_mode=None,
        persist=False,
        execution_context_id=None,
        model_form=None,
        automatic_model_form=None,
    ):
        """Send a turn and update Forest runtime binding.

        When persistence is requested, any newly created
        or not-yet-persisted runtime binding is committed
        before the potentially long runtime/model call.

        Normal same-session warm turns remain write-free.
        """

        
        
        if execution_context_id is not None:
            return (
                self._send_runtime_turn_for_frozen_model_form(
                    message,
                    execution_context_id=
                        execution_context_id,
                    state=state,
                    instructions=instructions,
                    instruction_composition=instruction_composition,
                    reasoning_mode=reasoning_mode,
                    persist=persist,
                    model_form=model_form,
                    automatic_model_form=
                        automatic_model_form,
                )
            )

        if (
            model_form is not None
            or automatic_model_form is not None
        ):
            raise TaskSessionError(
                "Per-turn Model Form controls require "
                "an explicit execution_context_id."
            )

        if state is None:
            state = self.load_state()

        # Resolve Tree-level human reasoning intent exactly once
        # before the meaningful-input context transition.
        #
        # persistent turn:
        #   latest durable reasoning_control
        #
        # in-memory turn:
        #   caller-provided state
        reasoning_state = (
            self.load_state()
            if persist
            else state
        )

        try:
            from reasoning import (
                ReasoningControlError,
                ReasoningModeError,
                reasoning_control_from_mapping,
                resolve_effective_reasoning,
            )

            turn_reasoning_control = (
                reasoning_control_from_mapping(
                    reasoning_state.get(
                        "reasoning_control"
                    )
                )
            )

            reasoning_decision = (
                resolve_effective_reasoning(
                    turn_reasoning_control,
                    message,
                    explicit_mode=reasoning_mode,
                )
            )

        except (
            ReasoningControlError,
            ReasoningModeError,
            ValueError,
        ) as exc:
            raise TaskSessionError(
                "Could not resolve Forest "
                "reasoning control for this turn."
            ) from exc

        resolved_reasoning_mode = (
            reasoning_decision.mode
        )

        # A direct runtime turn is a new meaningful
        # conversational input. Internal execution
        # steps do not call this transition.
        active_context_task = (
            self._active_runtime_task(
                state
            )
        )

        context_route_state = (
            self._context_route_state_for_task(
                active_context_task["id"]
            )
        )

        context_route_state.begin_meaningful_input()

        initial = copy.deepcopy(
            state
        )

        if persist:
            if (
                "reasoning_control"
                in reasoning_state
            ):
                initial[
                    "reasoning_control"
                ] = copy.deepcopy(
                    reasoning_state[
                        "reasoning_control"
                    ]
                )

            else:
                initial.pop(
                    "reasoning_control",
                    None,
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
                reasoning_mode=resolved_reasoning_mode,
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
                    reasoning_mode=resolved_reasoning_mode,
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


        # Runtime/model execution has completed successfully.
        # Only now may one governed temporary turn be consumed.
        reasoning_finalize = (
            self._finalize_reasoning_control_after_success(
                working=working,
                turn_control=turn_reasoning_control,
                decision=reasoning_decision,
                persist=persist,
            )
        )

        working = reasoning_finalize[
            "state"
        ]
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

        cache_key = CacheKey(
            namespace=f"adapter:{adapter_name}",
            cache_type="temporary-skill-overlay",
            identity=(
                task_id,
                tuple(runtime_skills),
            ),
        )

        cache_dependencies = {
            "adapter": adapter_name,
            "runtime_skills": tuple(runtime_skills),
        }

        cached_entry = self._cache_coordinator.get(
            cache_key,
            dependencies=cache_dependencies,
        )

        if cached_entry is not None:
            result = dict(cached_entry.value)
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

        self._cache_coordinator.put(
            cache_key,
            cached,
            dependencies=cache_dependencies,
            display_name="Temporary Skill Overlay",
            metadata={
                "task_id": task_id,
                "adapter": adapter_name,
                "temporary": True,
            },
        )

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

        cache_key = CacheKey(
            namespace=f"adapter:{adapter_name}",
            cache_type="skill-overlay",
            identity=(
                task_id,
                tuple(runtime_skills),
            ),
        )

        cache_dependencies = {
            "adapter": adapter_name,
            "runtime_skills": tuple(runtime_skills),
        }

        cached_entry = self._cache_coordinator.get(
            cache_key,
            dependencies=cache_dependencies,
        )

        if cached_entry is not None:
            result = dict(cached_entry.value)
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

        self._cache_coordinator.put(
            cache_key,
            cached,
            dependencies=cache_dependencies,
            display_name="Task-Sticky Skill Overlay",
            metadata={
                "task_id": task_id,
                "adapter": adapter_name,
            },
        )

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
