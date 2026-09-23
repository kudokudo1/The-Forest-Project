#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import argparse
import os
import shutil
import sys
import tempfile
import yaml

HOME = Path.home()
FOREST = HOME / "The-Forest" / "bristlecone"

# Forest owns canonical capability resolution.
sys.path.insert(0, str(FOREST))

from capabilities.resolver import (
    ForestCapabilityResolver,
    CapabilityResolutionError,
)

from runtime.adapters.factory import (
    create_runtime_adapter,
)

REGISTRY_FILE = FOREST / "capabilities" / "registry.yaml"
WORKSHOP_DIR = FOREST / "workshops"
STATE_FILE = FOREST / "state" / "active.yaml"



def load_yaml(path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def unique(items):
    seen = set()
    result = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result


def atomic_write_yaml(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
    ) as tmp:
        yaml.safe_dump(data, tmp, sort_keys=False)
        tmp_path = Path(tmp.name)

    os.replace(tmp_path, path)


def main():
    parser = argparse.ArgumentParser(
        description="Resolve and activate a Bristlecone Workshop."
    )

    parser.add_argument(
        "workshop",
        help="research, design, code-debug, or model",
    )

    parser.add_argument(
        "--general",
        nargs="*",
        default=[],
        help="General Ready capabilities to activate",
    )

    parser.add_argument(
        "--ready",
        nargs="*",
        default=[],
        help="Workshop Ready capabilities to activate",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve and display changes without modifying the runtime",
    )

    args = parser.parse_args()

    workshop_file = WORKSHOP_DIR / f"{args.workshop}.yaml"

    if not workshop_file.exists():
        print(f"ERROR: Unknown Workshop: {args.workshop}")
        sys.exit(1)

    registry = load_yaml(REGISTRY_FILE)
    # Read runtime identity from portable
    # Forest state. Runtime implementation details
    # remain behind the adapter boundary.
    state = load_yaml(
        STATE_FILE
    )

    runtime = state.get(
        "runtime",
        {},
    )

    if not isinstance(
        runtime,
        dict,
    ):
        print(
            "ERROR: state.runtime must be a mapping."
        )
        sys.exit(6)

    adapter_name = runtime.get(
        "adapter"
    )

    if not adapter_name:
        print(
            "ERROR: state.runtime.adapter "
            "is not configured."
        )
        sys.exit(6)

    adapter_name = str(
        adapter_name
    )

    resolver = ForestCapabilityResolver(
        FOREST
    )
    workshop = load_yaml(workshop_file)

    capabilities = registry["capabilities"]
    general_ready = set(registry.get("general_ready", []))
    workshop_ready = set(workshop.get("ready", []))

    for name in args.general:
        if name not in general_ready:
            print(
                f"ERROR: {name!r} is not in the General Ready rack."
            )
            sys.exit(2)

    for name in args.ready:
        if name not in workshop_ready:
            print(
                f"ERROR: {name!r} is not Ready in "
                f"{workshop['name']!r}."
            )
            sys.exit(3)

    try:
        resolution = resolver.resolve(
            args.workshop,
            general=list(
                args.general
            ),
            ready=list(
                args.ready
            ),
            adapter_name=adapter_name,
            require_resolved=False,
        )

    except CapabilityResolutionError as exc:
        print(
            f"ERROR: {exc}"
        )
        sys.exit(5)

    active_ids = list(
        resolution[
            "canonical_active_ids"
        ]
    )

    hermes_tools = list(
        resolution[
            "runtime"
        ][
            "toolsets"
        ]
    )

    hermes_skills = list(
        resolution[
            "runtime"
        ][
            "skills"
        ]
    )

    skill_bindings = list(
        resolution[
            "runtime"
        ][
            "skill_bindings"
        ]
    )

    unresolved = [
        (
            item.get(
                "canonical_id"
            ),
            item.get(
                "reason",
                "unresolved",
            ),
        )
        for item in resolution[
            "unresolved"
        ]
    ]

    print()
    print(f"WORKSHOP: {workshop['name']}")
    print("=" * 52)

    print("\nForest active capabilities:")
    for name in active_ids:
        if name in workshop.get("core", []):
            source = "CORE"
        elif name in args.general:
            source = "GENERAL"
        else:
            source = "READY"

        print(f"  {source:7} {name}")

    print("\nHermes toolsets:")
    for name in hermes_tools:
        print(f"  - {name}")

    if not hermes_tools:
        print("  (none)")

    if hermes_skills:
        print("\nHermes Task-Sticky Skills:")
        for binding in skill_bindings:
            print(
                f"  - {binding['canonical_id']} "
                f"-> {binding['runtime_id']}"
            )

    if unresolved:
        print("\nUNRESOLVED:")
        for name, reason in unresolved:
            print(f"  - {name}: {reason}")

        print("\nThe Workshop was NOT changed.")
        sys.exit(5)

    platform = runtime.get(
        "platform"
    )

    print(
        f"\nRuntime adapter: {adapter_name}"
    )

    if platform is not None:
        print(
            f"Runtime platform: {platform}"
        )

    if args.dry_run:
        print("\nDRY RUN")
        print("No files were modified.")
        print("\nRESULT: Workshop resolves safely.")
        return

    runtime_adapter = create_runtime_adapter(
        state,
        forest_root=FOREST,
    )

    transaction = None
    backup_path = None

    try:
        # The runtime adapter owns the actual
        # runtime-specific transaction.
        transaction = (
            runtime_adapter
            .apply_toolsets_exact(
                list(
                    hermes_tools
                ),
                state,
            )
        )

        # Verify through the adapter contract rather
        # than reading Hermes configuration directly.
        actual_toolsets = (
            runtime_adapter
            .get_active_toolsets(
                state
            )
        )

        if (
            set(
                actual_toolsets
            )
            != set(
                hermes_tools
            )
        ):
            raise RuntimeError(
                "Runtime verification failed: "
                f"expected "
                f"{sorted(hermes_tools)}, "
                f"found "
                f"{sorted(actual_toolsets)}"
            )

        state["workshop"] = (
            args.workshop
        )

        state["active_general"] = (
            list(
                args.general
            )
        )

        state["active_ready"] = (
            list(
                args.ready
            )
        )

        task_session = state.get(
            "task_session"
        )

        if not isinstance(
            task_session,
            dict,
        ):
            task_session = {}

            state[
                "task_session"
            ] = task_session

        task_session[
            "task_sticky_skills"
        ] = [
            binding[
                "canonical_id"
            ]
            for binding
            in skill_bindings
        ]

        state[
            "runtime"
        ][
            "adapter"
        ] = runtime_adapter.adapter_name

        state[
            "runtime"
        ][
            "platform"
        ] = platform

        # Keep the current state schema unchanged
        # during this migration. These legacy names
        # can be generalized separately later.
        state["last_applied"] = {
            "toolsets":
                hermes_tools,

            "skills":
                hermes_skills,

            "timestamp":
                datetime.now().isoformat(
                    timespec="seconds"
                ),
        }

        # Runtime has been verified first.
        # Only now may Forest claim the state.
        atomic_write_yaml(
            STATE_FILE,
            state,
        )

        backup_path = (
            transaction.get(
                "backup_path"
            )
            if isinstance(
                transaction,
                dict,
            )
            else None
        )

    except Exception as exc:
        rollback_error = None

        # If exact activation returned a transaction,
        # the runtime changed successfully enough that
        # we own responsibility for restoring it.
        if transaction is not None:
            try:
                runtime_adapter.restore_toolsets_exact(
                    transaction,
                    state,
                )

            except Exception as restore_exc:
                rollback_error = restore_exc

        print(
            "\nERROR: Workshop activation failed."
        )

        print(
            exc
        )

        if rollback_error is None:
            print(
                "\nRuntime restored to the "
                "pre-activation baseline."
            )

        else:
            print(
                "\nCRITICAL: Runtime rollback "
                "also failed."
            )

            print(
                rollback_error
            )

        sys.exit(9)

    print("\nRESULT: Workshop activated successfully.")
    print("\nHermes toolsets now:")
    for name in hermes_tools:
        print(f"  - {name}")

    print("\nBackup:")

    if backup_path:
        print(
            backup_path
        )

    else:
        print(
            "(not required; runtime already "
            "matched the desired toolset set)"
        )

    print(
        "\nForest state and runtime configuration are synchronized."
    )


if __name__ == "__main__":
    main()
