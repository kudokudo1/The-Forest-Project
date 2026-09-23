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
HERMES_REPO = HOME / ".hermes" / "hermes-agent"

sys.path.insert(0, str(HERMES_REPO))

from hermes_cli.config import load_config, save_config
from hermes_cli.tools_config import (
    _save_platform_tools,
    CONFIGURABLE_TOOLSETS,
)

REGISTRY_FILE = FOREST / "capabilities" / "registry.yaml"
ADAPTER_FILE = FOREST / "adapters" / "hermes.yaml"
WORKSHOP_DIR = FOREST / "workshops"
STATE_FILE = FOREST / "state" / "active.yaml"

BACKUP_DIR = FOREST / "backups" / "hermes-config"


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
        help="Resolve and display changes without modifying Hermes",
    )

    args = parser.parse_args()

    workshop_file = WORKSHOP_DIR / f"{args.workshop}.yaml"

    if not workshop_file.exists():
        print(f"ERROR: Unknown Workshop: {args.workshop}")
        sys.exit(1)

    registry = load_yaml(REGISTRY_FILE)
    adapter = load_yaml(ADAPTER_FILE)
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

    active_ids = unique(
        list(workshop.get("core", []))
        + list(args.general)
        + list(args.ready)
    )

    tool_map = adapter.get("capabilities", {})
    skill_map = adapter.get("skills", {})
    unresolved_map = adapter.get("unresolved", {})

    hermes_tools = []
    hermes_skills = []
    unresolved = []

    for name in active_ids:
        if name not in capabilities:
            unresolved.append(
                (name, "not defined in capability registry")
            )
            continue

        kind = capabilities[name].get("kind")

        if kind == "skill":
            mapping = skill_map.get(name)

            if mapping:
                hermes_skills.append(mapping["target"])
            elif name in unresolved_map:
                unresolved.append(
                    (name, unresolved_map[name]["reason"].strip())
                )
            else:
                unresolved.append(
                    (name, "no Hermes Skill mapping")
                )

        else:
            mapping = tool_map.get(name)

            if mapping:
                hermes_tools.append(mapping["target"])
            elif name in unresolved_map:
                unresolved.append(
                    (name, unresolved_map[name]["reason"].strip())
                )
            else:
                unresolved.append(
                    (name, "no Hermes toolset mapping")
                )

    hermes_tools = unique(hermes_tools)
    hermes_skills = unique(hermes_skills)

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
        print("\nHermes Skills:")
        for name in hermes_skills:
            print(f"  - {name}")

        print(
            "\nERROR: Individual live Skill activation "
            "has not been implemented yet."
        )
        print(
            "The Workshop was NOT changed."
        )
        sys.exit(4)

    if unresolved:
        print("\nUNRESOLVED:")
        for name, reason in unresolved:
            print(f"  - {name}: {reason}")

        print("\nThe Workshop was NOT changed.")
        sys.exit(5)

    state = load_yaml(STATE_FILE)
    platform = state["runtime"]["platform"]

    if platform != "api_server":
        print(
            f"\nERROR: Refusing live change because runtime platform "
            f"is {platform!r}, not 'api_server'."
        )
        sys.exit(6)

    print(f"\nHermes platform: {platform}")

    if args.dry_run:
        print("\nDRY RUN")
        print("No files were modified.")
        print("\nRESULT: Workshop resolves safely.")
        return

    hermes_home = os.environ.get("HERMES_HOME")

    expected_home = (
        HOME / ".hermes" / "profiles" / "bristlecone"
    )

    if not hermes_home:
        print("\nERROR: HERMES_HOME is not set.")
        sys.exit(7)

    if Path(hermes_home).resolve() != expected_home.resolve():
        print("\nERROR: HERMES_HOME points to the wrong profile:")
        print(f"  {hermes_home}")
        print("\nExpected:")
        print(f"  {expected_home}")
        sys.exit(8)

    config_path = expected_home / "config.yaml"

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = BACKUP_DIR / f"config-{stamp}.yaml"

    shutil.copy2(config_path, backup_path)

    config_written = False

    try:
        config = load_config()

        _save_platform_tools(
            config,
            platform,
            set(hermes_tools),
        )

        save_config(config)

        config_written = True

        verify = load_config()

        raw_saved = (
            verify
            .get("platform_toolsets", {})
            .get(platform, [])
        )

        if not isinstance(raw_saved, list):
            raise RuntimeError(
                "platform_toolsets.api_server is not a list"
            )

        configurable_keys = {
            key for key, _, _ in CONFIGURABLE_TOOLSETS
        }

        saved_configurable = (
            set(map(str, raw_saved))
            & configurable_keys
        )

        desired = set(hermes_tools)

        if saved_configurable != desired:
            raise RuntimeError(
                "Hermes verification failed: "
                f"expected {sorted(desired)}, "
                f"found {sorted(saved_configurable)}"
            )

        state["workshop"] = args.workshop
        state["active_general"] = list(args.general)
        state["active_ready"] = list(args.ready)

        state["runtime"]["adapter"] = "hermes"
        state["runtime"]["platform"] = platform

        state["last_applied"] = {
            "hermes_toolsets": hermes_tools,
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

        atomic_write_yaml(STATE_FILE, state)

    except Exception as exc:
        if config_written:
            shutil.copy2(backup_path, config_path)

        print("\nERROR: Workshop activation failed.")
        print(exc)
        print("\nHermes config restored from:")
        print(backup_path)
        sys.exit(9)

    print("\nRESULT: Workshop activated successfully.")
    print("\nHermes toolsets now:")
    for name in hermes_tools:
        print(f"  - {name}")

    print("\nBackup:")
    print(backup_path)

    print(
        "\nForest state and Hermes configuration are synchronized."
    )


if __name__ == "__main__":
    main()
