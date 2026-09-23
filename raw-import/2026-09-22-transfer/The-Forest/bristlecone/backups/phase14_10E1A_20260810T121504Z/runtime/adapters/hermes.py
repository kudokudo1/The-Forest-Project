"""Hermes runtime adapter for The Forest."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
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
        forest_root=None,
        api_base_url=None,
        api_timeout=30,
        turn_timeout=900,
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

        self.forest_root = (
            Path(forest_root)
            if forest_root is not None
            else Path(__file__).resolve().parents[2]
        )

        self.api_base_url = (
            str(api_base_url).rstrip("/")
            if api_base_url is not None
            else (
                "http://"
                + "127.0.0.1:8643"
            )
        )

        self.api_timeout = float(
            api_timeout
        )

        # Model turns may legitimately take much
        # longer than lightweight session API calls.
        self.turn_timeout = float(
            turn_timeout
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

    @staticmethod
    def _atomic_restore_file(
        path,
        backup_path,
    ):
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

            os.replace(
                tmp_path,
                path,
            )

        except Exception:
            if (
                tmp_path is not None
                and tmp_path.exists()
            ):
                tmp_path.unlink()

            raise

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

    def apply_toolsets_exact(
        self,
        runtime_toolsets,
        state,
    ):
        """Set configurable Hermes toolsets exactly.

        This is an authoritative working-set operation,
        not an additive temporary overlay.
        """

        if not isinstance(
            runtime_toolsets,
            list,
        ):
            raise RuntimeAdapterError(
                "runtime_toolsets must be a list."
            )

        desired = self._unique(
            [
                str(item)
                for item in runtime_toolsets
            ]
        )

        runtime_api = (
            self._load_toolset_runtime(state)
        )

        invalid = [
            item
            for item in desired
            if item
            not in runtime_api["configurable"]
        ]

        if invalid:
            raise RuntimeAdapterError(
                "Hermes does not expose these "
                "exact toolsets as configurable: "
                f"{invalid}"
            )

        config = runtime_api[
            "load_config"
        ]()

        baseline = self._configurable_toolsets(
            runtime_api,
            config,
        )

        transaction = {
            "adapter":
                self.adapter_name,

            "transaction_type":
                "exact_toolsets",

            "platform":
                runtime_api["platform"],

            "baseline_toolsets":
                baseline,

            "desired_toolsets":
                desired,

            "backup_path":
                None,

            "applied":
                False,

            "restored":
                False,
        }

        if set(desired) == set(baseline):
            return transaction

        backup_dir = (
            self.forest_root
            / "backups"
            / "hermes-exact"
        )

        backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%S-%fZ"
        )

        backup_path = (
            backup_dir
            / f"config-{stamp}.yaml"
        )

        config_path = runtime_api[
            "config_path"
        ]

        if not config_path.exists():
            raise RuntimeAdapterError(
                "Hermes config does not exist: "
                f"{config_path}"
            )

        backup_path.write_bytes(
            config_path.read_bytes()
        )

        transaction[
            "backup_path"
        ] = str(
            backup_path
        )

        try:
            runtime_api[
                "save_platform_tools"
            ](
                config,
                runtime_api["platform"],
                set(desired),
            )

            runtime_api[
                "save_config"
            ](
                config
            )

            verify = runtime_api[
                "load_config"
            ]()

            saved = self._configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(desired):
                raise RuntimeAdapterError(
                    "Exact Hermes activation "
                    "verification failed: expected "
                    f"{sorted(desired)}, found "
                    f"{sorted(saved)}"
                )

            transaction[
                "applied"
            ] = True

            return transaction

        except Exception as exc:
            # The backup represents the runtime truth
            # that existed before this transaction.
            # Restore it even if the failing write may
            # only have been partial.
            self._atomic_restore_file(
                config_path,
                backup_path,
            )

            try:
                rollback_config = runtime_api[
                    "load_config"
                ]()

                rolled_back = (
                    self._configurable_toolsets(
                        runtime_api,
                        rollback_config,
                    )
                )

                if (
                    set(rolled_back)
                    != set(baseline)
                ):
                    raise RuntimeAdapterError(
                        "Exact Hermes activation "
                        "failed and rollback "
                        "verification also failed: "
                        f"expected baseline "
                        f"{sorted(baseline)}, found "
                        f"{sorted(rolled_back)}"
                    )

            except Exception as rollback_exc:
                if isinstance(
                    rollback_exc,
                    RuntimeAdapterError,
                ):
                    raise rollback_exc from exc

                raise RuntimeAdapterError(
                    "Exact Hermes activation "
                    "failed and rollback could "
                    "not be verified: "
                    f"{rollback_exc}"
                ) from exc

            if isinstance(
                exc,
                RuntimeAdapterError,
            ):
                raise

            raise RuntimeAdapterError(
                "Exact Hermes activation "
                f"failed: {exc}"
            ) from exc

    def restore_toolsets_exact(
        self,
        transaction,
        state,
    ):
        """Restore the baseline from an exact transaction."""

        if not isinstance(
            transaction,
            dict,
        ):
            raise RuntimeAdapterError(
                "Exact transaction must be a mapping."
            )

        if (
            transaction.get(
                "transaction_type"
            )
            != "exact_toolsets"
        ):
            raise RuntimeAdapterError(
                "Transaction is not an "
                "exact_toolsets transaction."
            )

        if transaction.get(
            "restored"
        ):
            return transaction

        if not transaction.get(
            "applied"
        ):
            transaction[
                "restored"
            ] = True

            return transaction

        runtime_api = (
            self._load_toolset_runtime(state)
        )

        baseline = transaction.get(
            "baseline_toolsets",
            [],
        )

        if not isinstance(
            baseline,
            list,
        ):
            raise RuntimeAdapterError(
                "Transaction baseline_toolsets "
                "must be a list."
            )

        backup_text = transaction.get(
            "backup_path"
        )

        backup_path = (
            Path(backup_text)
            if backup_text
            else None
        )

        config_path = runtime_api[
            "config_path"
        ]

        try:
            config = runtime_api[
                "load_config"
            ]()

            runtime_api[
                "save_platform_tools"
            ](
                config,
                runtime_api["platform"],
                set(baseline),
            )

            runtime_api[
                "save_config"
            ](
                config
            )

            verify = runtime_api[
                "load_config"
            ]()

            saved = self._configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(baseline):
                raise RuntimeAdapterError(
                    "Exact Hermes restoration "
                    "verification failed: expected "
                    f"{sorted(baseline)}, found "
                    f"{sorted(saved)}"
                )

        except Exception as exc:
            if (
                backup_path is not None
                and backup_path.exists()
            ):
                self._atomic_restore_file(
                    config_path,
                    backup_path,
                )

                try:
                    fallback_config = runtime_api[
                        "load_config"
                    ]()

                    fallback = (
                        self._configurable_toolsets(
                            runtime_api,
                            fallback_config,
                        )
                    )

                    if (
                        set(fallback)
                        != set(baseline)
                    ):
                        raise RuntimeAdapterError(
                            "Exact Hermes restoration "
                            "fallback verification "
                            "failed: expected "
                            f"{sorted(baseline)}, found "
                            f"{sorted(fallback)}"
                        )

                except Exception as fallback_exc:
                    if isinstance(
                        fallback_exc,
                        RuntimeAdapterError,
                    ):
                        raise fallback_exc from exc

                    raise RuntimeAdapterError(
                        "Exact Hermes restoration "
                        "failed and backup fallback "
                        "could not be verified: "
                        f"{fallback_exc}"
                    ) from exc

            if isinstance(
                exc,
                RuntimeAdapterError,
            ):
                raise

            raise RuntimeAdapterError(
                "Exact Hermes restoration "
                f"failed: {exc}"
            ) from exc

        transaction[
            "restored"
        ] = True

        return transaction

    def begin_temporary_toolsets(
        self,
        runtime_toolsets,
        state,
    ):
        if not isinstance(
            runtime_toolsets,
            list,
        ):
            raise RuntimeAdapterError(
                "runtime_toolsets must be a list."
            )

        requested = self._unique(
            [
                str(item)
                for item in runtime_toolsets
            ]
        )

        runtime_api = (
            self._load_toolset_runtime(state)
        )

        invalid = [
            item
            for item in requested
            if item
            not in runtime_api["configurable"]
        ]

        if invalid:
            raise RuntimeAdapterError(
                "Hermes does not expose these "
                "temporary toolsets as configurable: "
                f"{invalid}"
            )

        config = runtime_api[
            "load_config"
        ]()

        baseline = self._configurable_toolsets(
            runtime_api,
            config,
        )

        desired = self._unique(
            baseline + requested
        )

        transaction = {
            "adapter": self.adapter_name,
            "platform":
                runtime_api["platform"],
            "baseline_toolsets":
                baseline,
            "requested_toolsets":
                requested,
            "desired_toolsets":
                desired,
            "backup_path":
                None,
            "applied":
                False,
            "restored":
                False,
        }

        if desired == baseline:
            return transaction

        backup_dir = (
            self.forest_root
            / "backups"
            / "hermes-temporary"
        )

        backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%S-%fZ"
        )

        backup_path = (
            backup_dir
            / f"config-{stamp}.yaml"
        )

        config_path = runtime_api[
            "config_path"
        ]

        if not config_path.exists():
            raise RuntimeAdapterError(
                "Hermes config does not exist: "
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
            runtime_api[
                "save_platform_tools"
            ](
                config,
                runtime_api["platform"],
                set(desired),
            )

            runtime_api[
                "save_config"
            ](
                config
            )

            config_written = True

            verify = runtime_api[
                "load_config"
            ]()

            saved = self._configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(desired):
                raise RuntimeAdapterError(
                    "Temporary Hermes activation "
                    "verification failed: expected "
                    f"{sorted(desired)}, found "
                    f"{sorted(saved)}"
                )

            transaction["applied"] = True

            return transaction

        except Exception as exc:
            if config_written:
                self._atomic_restore_file(
                    config_path,
                    backup_path,
                )

            if isinstance(
                exc,
                RuntimeAdapterError,
            ):
                raise

            raise RuntimeAdapterError(
                "Temporary Hermes activation "
                f"failed: {exc}"
            ) from exc

    def restore_temporary_toolsets(
        self,
        transaction,
        state,
    ):
        if not isinstance(
            transaction,
            dict,
        ):
            raise RuntimeAdapterError(
                "Temporary transaction "
                "must be a mapping."
            )

        if transaction.get(
            "restored"
        ):
            return transaction

        if not transaction.get(
            "applied"
        ):
            transaction[
                "restored"
            ] = True

            return transaction

        runtime_api = (
            self._load_toolset_runtime(state)
        )

        baseline = transaction.get(
            "baseline_toolsets",
            [],
        )

        if not isinstance(
            baseline,
            list,
        ):
            raise RuntimeAdapterError(
                "Transaction baseline_toolsets "
                "must be a list."
            )

        backup_text = transaction.get(
            "backup_path"
        )

        backup_path = (
            Path(backup_text)
            if backup_text
            else None
        )

        try:
            config = runtime_api[
                "load_config"
            ]()

            runtime_api[
                "save_platform_tools"
            ](
                config,
                runtime_api["platform"],
                set(baseline),
            )

            runtime_api[
                "save_config"
            ](
                config
            )

            verify = runtime_api[
                "load_config"
            ]()

            saved = self._configurable_toolsets(
                runtime_api,
                verify,
            )

            if set(saved) != set(baseline):
                raise RuntimeAdapterError(
                    "Temporary Hermes restoration "
                    "verification failed: expected "
                    f"{sorted(baseline)}, found "
                    f"{sorted(saved)}"
                )

        except Exception as exc:
            if (
                backup_path is not None
                and backup_path.exists()
            ):
                self._atomic_restore_file(
                    runtime_api[
                        "config_path"
                    ],
                    backup_path,
                )

            if isinstance(
                exc,
                RuntimeAdapterError,
            ):
                raise

            raise RuntimeAdapterError(
                "Temporary Hermes restoration "
                f"failed: {exc}"
            ) from exc

        transaction[
            "restored"
        ] = True

        return transaction

    def _validate_session_runtime(
        self,
        state,
    ):
        """Validate Forest state before Hermes API work."""

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

        platform = runtime.get(
            "platform"
        )

        if adapter_name != self.adapter_name:
            raise RuntimeAdapterError(
                "Hermes session operations require "
                "the hermes runtime adapter."
            )

        if platform != "api_server":
            raise RuntimeAdapterError(
                "Hermes session operations require "
                f"'api_server', not {platform!r}."
            )

        hermes_home = os.environ.get(
            "HERMES_HOME"
        )

        if not hermes_home:
            raise RuntimeAdapterError(
                "HERMES_HOME is not set."
            )

        if (
            Path(hermes_home).resolve()
            != self.profile_home.resolve()
        ):
            raise RuntimeAdapterError(
                "HERMES_HOME does not point to "
                f"the {self.profile_name!r} profile."
            )

    def _ensure_repo_path(self):
        repo_text = str(
            self.repo
        )

        if repo_text not in sys.path:
            sys.path.insert(
                0,
                repo_text,
            )

    def _resolve_api_key(
        self,
        state,
    ):
        """Resolve API_SERVER_KEY inside Hermes profile scope."""

        self._validate_session_runtime(
            state
        )

        self._ensure_repo_path()

        try:
            from gateway.run import (
                _profile_runtime_scope,
            )

            from agent.secret_scope import (
                get_secret,
            )

            from hermes_cli.auth import (
                has_usable_secret,
            )

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes profile/auth helpers could "
                f"not be imported: {exc}"
            ) from exc

        try:
            with _profile_runtime_scope(
                self.profile_home
            ):
                key = (
                    get_secret(
                        "API_SERVER_KEY",
                        "",
                    )
                    or ""
                )

                if not has_usable_secret(
                    key,
                    min_length=16,
                ):
                    raise RuntimeAdapterError(
                        "No usable profile-scoped "
                        "API_SERVER_KEY was resolved."
                    )

                return key

        except RuntimeAdapterError:
            raise

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes profile-scoped API "
                "authentication failed: "
                f"{type(exc).__name__}"
            ) from exc

    def _api_request(
        self,
        method,
        path,
        state,
        payload=None,
        expected_statuses=(200,),
        timeout=None,
    ):
        """Perform an authenticated Hermes API request."""

        key = self._resolve_api_key(
            state
        )

        body = None

        headers = {
            "Accept": "application/json",
            "Authorization":
                f"Bearer {key}",
        }

        if payload is not None:
            body = json.dumps(
                payload
            ).encode(
                "utf-8"
            )

            headers[
                "Content-Type"
            ] = "application/json"

        url = (
            self.api_base_url
            + path
        )

        request = urllib.request.Request(
            url,
            data=body,
            headers=headers,
            method=str(method).upper(),
        )

        # Explicitly disable proxy use for the
        # loopback Hermes gateway.
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({})
        )

        try:
            with opener.open(
                request,
                timeout=(
                    self.api_timeout
                    if timeout is None
                    else float(timeout)
                ),
            ) as response:
                status = int(
                    response.status
                )

                raw = response.read()

                response_headers = dict(
                    response.headers.items()
                )

        except urllib.error.HTTPError as exc:
            raw = exc.read()

            try:
                detail = raw.decode(
                    "utf-8",
                    errors="replace",
                )

            except Exception:
                detail = "<unreadable response>"

            error_code = None

            try:
                parsed_error = json.loads(
                    detail
                )

                error_data = (
                    parsed_error.get(
                        "error"
                    )
                    if isinstance(
                        parsed_error,
                        dict,
                    )
                    else None
                )

                if isinstance(
                    error_data,
                    dict,
                ):
                    raw_error_code = (
                        error_data.get(
                            "code"
                        )
                    )

                    if raw_error_code is not None:
                        error_code = str(
                            raw_error_code
                        )

            except Exception:
                pass

            raise RuntimeAdapterError(
                "Hermes API request failed: "
                f"{method} {path} returned "
                f"HTTP {exc.code}: {detail[:500]}",
                status_code=int(
                    exc.code
                ),
                error_code=error_code,
                method=str(
                    method
                ).upper(),
                path=str(
                    path
                ),
            ) from exc

        except urllib.error.URLError as exc:
            raise RuntimeAdapterError(
                "Hermes API could not be reached at "
                f"{self.api_base_url}: {exc.reason}"
            ) from exc

        if status not in expected_statuses:
            raise RuntimeAdapterError(
                "Hermes API returned unexpected "
                f"status {status} for "
                f"{method} {path}."
            )

        if raw:
            try:
                data = json.loads(
                    raw.decode("utf-8")
                )

            except Exception as exc:
                raise RuntimeAdapterError(
                    "Hermes API returned invalid JSON "
                    f"for {method} {path}."
                ) from exc

        else:
            data = None

        return {
            "status": status,
            "data": data,
            "headers": response_headers,
        }

    @staticmethod
    def _session_id_from_response(
        response_data,
    ):
        if not isinstance(
            response_data,
            dict,
        ):
            return None

        session = response_data.get(
            "session"
        )

        if isinstance(
            session,
            dict,
        ):
            value = (
                session.get("id")
                or session.get("session_id")
            )

            if value:
                return str(value)

        value = (
            response_data.get("id")
            or response_data.get("session_id")
        )

        if value:
            return str(value)

        return None

    def _configured_default_model(
        self,
        state,
    ):
        """Return this Hermes profile's configured default model."""

        runtime_api = (
            self._load_toolset_runtime(
                state
            )
        )

        try:
            config = runtime_api[
                "load_config"
            ]()

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes configuration could not "
                f"be loaded for session creation: {exc}"
            ) from exc

        model_config = config.get(
            "model",
            {},
        )

        if not isinstance(
            model_config,
            dict,
        ):
            raise RuntimeAdapterError(
                "Hermes model configuration "
                "must be a mapping."
            )

        model_name = model_config.get(
            "default"
        )

        if model_name is None:
            raise RuntimeAdapterError(
                "Hermes profile has no configured "
                "default model."
            )

        model_name = str(
            model_name
        ).strip()

        if not model_name:
            raise RuntimeAdapterError(
                "Hermes profile default model "
                "cannot be empty."
            )

        return model_name

    def create_session(
        self,
        state,
        task_id=None,
    ):
        model_name = (
            self._configured_default_model(
                state
            )
        )

        response = self._api_request(
            "POST",
            "/api/sessions",
            state,
            payload={
                "model": model_name,
            },
            expected_statuses=(201,),
        )

        session_id = (
            self._session_id_from_response(
                response["data"]
            )
        )

        if not session_id:
            raise RuntimeAdapterError(
                "Hermes created a session but "
                "returned no session ID."
            )

        return {
            "adapter": self.adapter_name,
            "session_id": session_id,
            "task_id": task_id,
            "model": model_name,
            "session": response["data"],
        }

    def get_session(
        self,
        session_id,
        state,
    ):
        session_id = str(
            session_id
        ).strip()

        if not session_id:
            raise RuntimeAdapterError(
                "session_id cannot be empty."
            )

        encoded = urllib.parse.quote(
            session_id,
            safe="",
        )

        response = self._api_request(
            "GET",
            f"/api/sessions/{encoded}",
            state,
            expected_statuses=(200,),
        )

        returned_id = (
            self._session_id_from_response(
                response["data"]
            )
            or session_id
        )

        return {
            "adapter": self.adapter_name,
            "session_id": returned_id,
            "session": response["data"],
        }

    def _session_chat_payload(
        self,
        message,
        instructions=None,
    ):
        """Build a Hermes persisted-chat request body.

        Hermes owns the accepted request schema, so
        probe its own parser rather than duplicating
        that private schema in Forest.
        """

        self._ensure_repo_path()

        try:
            from gateway.platforms.api_server import (
                _session_chat_user_message,
            )

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes persisted-chat parser could "
                f"not be imported: {exc}"
            ) from exc

        sentinel = str(
            message
        )

        candidates = [
            {
                "message": sentinel,
            },
            {
                "user_message": sentinel,
            },
            {
                "input": sentinel,
            },
            {
                "message": {
                    "role": "user",
                    "content": sentinel,
                },
            },
            {
                "messages": [
                    {
                        "role": "user",
                        "content": sentinel,
                    }
                ],
            },
        ]

        selected = None

        for candidate in candidates:
            try:
                parsed, error = (
                    _session_chat_user_message(
                        candidate
                    )
                )

            except Exception:
                continue

            if (
                error is None
                and isinstance(parsed, str)
                and parsed == sentinel
            ):
                selected = dict(
                    candidate
                )
                break

        if selected is None:
            raise RuntimeAdapterError(
                "Hermes persisted-chat request "
                "schema could not be determined."
            )

        if instructions is not None:
            if not isinstance(
                instructions,
                str,
            ):
                raise RuntimeAdapterError(
                    "instructions must be a string "
                    "or None."
                )

            selected[
                "instructions"
            ] = instructions

        return selected

    @staticmethod
    def _header_value(
        headers,
        name,
    ):
        wanted = str(
            name
        ).lower()

        for key, value in (
            headers or {}
        ).items():
            if str(key).lower() == wanted:
                return str(value)

        return None

    def is_stale_session_error(
        self,
        exc,
    ):
        """Recognize Hermes's persisted-session stale error."""

        return (
            isinstance(
                exc,
                RuntimeAdapterError,
            )
            and exc.status_code == 404
            and exc.error_code
                == "session_not_found"
        )

    def send_turn(
        self,
        session_id,
        message,
        state,
        instructions=None,
        reasoning_mode=None,
    ):
        session_id = str(
            session_id
        ).strip()

        if not session_id:
            raise RuntimeAdapterError(
                "session_id cannot be empty."
            )

        if not isinstance(
            message,
            str,
        ):
            raise RuntimeAdapterError(
                "message must be a string."
            )

        if not message.strip():
            raise RuntimeAdapterError(
                "message cannot be empty."
            )

        encoded = urllib.parse.quote(
            session_id,
            safe="",
        )

        payload = (
            self._session_chat_payload(
                message,
                instructions=instructions,
            )
        )


        if reasoning_mode is not None:
            try:
                from reasoning.model import (
                    normalize_reasoning_mode,
                )

                canonical_reasoning_mode = (
                    normalize_reasoning_mode(
                        reasoning_mode
                    )
                )

            except Exception as exc:
                raise RuntimeAdapterError(
                    "Invalid Forest reasoning "
                    "mode for Hermes runtime: "
                    f"{reasoning_mode!r}."
                ) from exc

            reasoning_effort = {
                "quick": "low",
                "normal": "medium",
                "deep": "high",
            }[
                canonical_reasoning_mode
            ]

            existing_model_options = (
                payload.get(
                    "model_options"
                )
            )

            if existing_model_options is None:
                model_options = {}

            elif isinstance(
                existing_model_options,
                dict,
            ):
                model_options = dict(
                    existing_model_options
                )

            else:
                raise RuntimeAdapterError(
                    "Hermes model_options must "
                    "be a mapping."
                )

            model_options[
                "reasoning_effort"
            ] = reasoning_effort

            payload[
                "model_options"
            ] = model_options

        response = self._api_request(
            "POST",
            f"/api/sessions/{encoded}/chat",
            state,
            payload=payload,
            expected_statuses=(200,),
            timeout=self.turn_timeout,
        )

        data = response[
            "data"
        ]

        if not isinstance(
            data,
            dict,
        ):
            raise RuntimeAdapterError(
                "Hermes persisted chat returned "
                "an invalid response mapping."
            )

        body_session_id = data.get(
            "session_id"
        )

        if body_session_id is not None:
            body_session_id = str(
                body_session_id
            )

        header_session_id = (
            self._header_value(
                response["headers"],
                "X-Hermes-Session-Id",
            )
        )

        if (
            body_session_id
            and header_session_id
            and body_session_id
            != header_session_id
        ):
            raise RuntimeAdapterError(
                "Hermes returned conflicting "
                "effective session IDs."
            )

        effective_session_id = (
            body_session_id
            or header_session_id
            or session_id
        )

        message_data = data.get(
            "message",
            {},
        )

        if isinstance(
            message_data,
            dict,
        ):
            assistant_content = (
                message_data.get(
                    "content",
                    "",
                )
                or ""
            )
        else:
            assistant_content = ""

        if not isinstance(
            assistant_content,
            str,
        ):
            assistant_content = str(
                assistant_content
            )

        return {
            "adapter":
                self.adapter_name,

            "requested_session_id":
                session_id,

            "session_id":
                effective_session_id,

            "session_rotated":
                effective_session_id
                != session_id,

            "message":
                assistant_content,

            "usage":
                data.get("usage"),

            "runtime":
                data.get("runtime"),

            "response":
                data,
        }

    def end_session(
        self,
        session_id,
        state,
    ):
        session_id = str(
            session_id
        ).strip()

        if not session_id:
            raise RuntimeAdapterError(
                "session_id cannot be empty."
            )

        encoded = urllib.parse.quote(
            session_id,
            safe="",
        )

        response = self._api_request(
            "DELETE",
            f"/api/sessions/{encoded}",
            state,
            expected_statuses=(200,),
        )

        data = response["data"]

        ended = bool(
            isinstance(data, dict)
            and data.get("deleted")
        )

        return {
            "adapter": self.adapter_name,
            "session_id": session_id,
            "ended": ended,
            "response": data,
        }

    def build_skill_overlay(
        self,
        runtime_skills,
        task_id=None,
    ):
        if not isinstance(
            runtime_skills,
            list,
        ):
            raise RuntimeAdapterError(
                "runtime_skills must be a list."
            )

        runtime_skills = self._unique(
            [
                str(item)
                for item in runtime_skills
            ]
        )

        repo_text = str(
            self.repo
        )

        if repo_text not in sys.path:
            sys.path.insert(
                0,
                repo_text,
            )

        try:
            from agent.skill_commands import (
                build_preloaded_skills_prompt,
            )

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes Skill loader could not "
                f"be imported: {exc}"
            ) from exc

        try:
            prompt, loaded, missing = (
                build_preloaded_skills_prompt(
                    runtime_skills,
                    task_id=task_id,
                )
            )

        except Exception as exc:
            raise RuntimeAdapterError(
                "Hermes Skill overlay generation "
                f"failed: {exc}"
            ) from exc

        if missing:
            raise RuntimeAdapterError(
                "Missing runtime Skills: "
                f"{missing}"
            )

        if loaded != runtime_skills:
            raise RuntimeAdapterError(
                "Unexpected loaded Skills: "
                f"{loaded}"
            )

        return prompt
