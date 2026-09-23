#!/usr/bin/env python3

"""
Bounded Forest -> Hermes profile bridge.

This file is executed with the Hermes virtual-environment
Python, never imported into Forest's system Python.

Allowed operations:
    default_model
    api_key

Input/output:
    exactly one JSON request on stdin
    exactly one JSON response on stdout

The helper never contacts the Hermes gateway or Ollama.
"""

from pathlib import Path
import json
import os
import sys


SCHEMA_VERSION = 1

ALLOWED_OPERATIONS = {
    "default_model",
    "api_key",
}


def _request():
    value = json.load(
        sys.stdin
    )

    if not isinstance(
        value,
        dict,
    ):
        raise RuntimeError(
            "Bridge request must be a mapping."
        )

    if (
        value.get("schema_version")
        != SCHEMA_VERSION
    ):
        raise RuntimeError(
            "Unsupported bridge schema version."
        )

    operation = value.get(
        "operation"
    )

    if (
        operation
        not in ALLOWED_OPERATIONS
    ):
        raise RuntimeError(
            "Bridge operation is not allowed."
        )

    profile_name = str(
        value.get(
            "profile_name",
            "",
        )
    ).strip()

    profile_home_text = str(
        value.get(
            "profile_home",
            "",
        )
    ).strip()

    if not profile_name:
        raise RuntimeError(
            "profile_name is required."
        )

    if not profile_home_text:
        raise RuntimeError(
            "profile_home is required."
        )

    profile_home = (
        Path(
            profile_home_text
        )
        .expanduser()
        .resolve()
    )

    if not profile_home.is_dir():
        raise RuntimeError(
            "Hermes profile directory "
            "does not exist."
        )

    if (
        profile_home.name
        != profile_name
    ):
        raise RuntimeError(
            "Hermes profile name/path "
            "identity mismatch."
        )

    # Forest's subprocess spawner must give Hermes
    # the exact profile home. Do not silently fall
    # back to ~/.hermes.
    ambient_home = (
        os.environ.get(
            "HERMES_HOME"
        )
    )

    if not ambient_home:
        raise RuntimeError(
            "Bridge child HERMES_HOME "
            "was not supplied."
        )

    if (
        Path(
            ambient_home
        ).expanduser().resolve()
        != profile_home
    ):
        raise RuntimeError(
            "Bridge child HERMES_HOME "
            "does not match requested profile."
        )

    return (
        operation,
        profile_name,
        profile_home,
    )


def _run():
    (
        operation,
        profile_name,
        profile_home,
    ) = _request()


    # Import Hermes-native dependencies ONLY inside
    # the Hermes virtual environment.
    from hermes_constants import (
        get_hermes_home,
        set_hermes_home_override,
        reset_hermes_home_override,
    )

    from agent.secret_scope import (
        build_profile_secret_scope,
        get_secret,
        set_secret_scope,
        reset_secret_scope,
    )

    from hermes_cli.env_loader import (
        hydrate_profile_secret_sources,
    )


    home_token = None
    secret_token = None

    try:
        # Reproduce the isolation primitives used
        # by Hermes's own profile runtime scope.
        home_token = (
            set_hermes_home_override(
                str(
                    profile_home
                )
            )
        )

        resolved_home = (
            Path(
                get_hermes_home()
            ).resolve()
        )

        if (
            resolved_home
            != profile_home
        ):
            raise RuntimeError(
                "Hermes home override did "
                "not resolve requested profile."
            )


        hydrate_profile_secret_sources(
            profile_home
        )


        secret_token = (
            set_secret_scope(
                build_profile_secret_scope(
                    profile_home
                )
            )
        )


        if operation == "default_model":
            from hermes_cli.config import (
                load_config,
            )

            config = load_config()

            if not isinstance(
                config,
                dict,
            ):
                raise RuntimeError(
                    "Hermes configuration "
                    "is not a mapping."
                )

            model_config = config.get(
                "model",
                {},
            )

            if not isinstance(
                model_config,
                dict,
            ):
                raise RuntimeError(
                    "Hermes model configuration "
                    "is not a mapping."
                )

            model = str(
                model_config.get(
                    "default",
                    "",
                )
            ).strip()

            if not model:
                raise RuntimeError(
                    "Hermes profile has no "
                    "configured default model."
                )

            return {
                "model":
                    model,

                "profile":
                    profile_name,
            }


        if operation == "api_key":
            # This import is intentionally performed
            # only in Hermes's venv, where Hermes's
            # own dependencies such as httpx exist.
            from hermes_cli.auth import (
                has_usable_secret,
            )

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
                raise RuntimeError(
                    "No usable profile-scoped "
                    "API_SERVER_KEY was resolved."
                )

            return {
                "api_key":
                    key,

                "profile":
                    profile_name,
            }


        raise RuntimeError(
            "Unreachable bridge operation."
        )


    finally:
        if secret_token is not None:
            reset_secret_scope(
                secret_token
            )

        if home_token is not None:
            reset_hermes_home_override(
                home_token
            )


def main():
    try:
        result = _run()

        payload = {
            "ok":
                True,

            "schema_version":
                SCHEMA_VERSION,

            "result":
                result,
        }

        print(
            json.dumps(
                payload,
                separators=(",", ":"),
            )
        )

        return 0


    except Exception as exc:
        # Never serialize request contents or
        # credentials into error output.
        payload = {
            "ok":
                False,

            "schema_version":
                SCHEMA_VERSION,

            "error_type":
                type(exc).__name__,

            "error":
                str(exc)[:500],
        }

        print(
            json.dumps(
                payload,
                separators=(",", ":"),
            )
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
