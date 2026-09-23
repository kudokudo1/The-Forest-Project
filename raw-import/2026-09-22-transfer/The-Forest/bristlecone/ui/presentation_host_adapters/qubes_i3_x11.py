#!/usr/bin/env python3
"""Forest Qubes / i3 / X11 host presentation adapter.

This is authoritative Forest source intended for reviewed
installation into trusted Qubes dom0.

It contains presentation behavior only.

It does not own:
- reasoning state
- Tree state
- Hermes state
- model state
- Forest permissions
- portable presentation policy

The portable request originates in ui/presentation.py.
"""

from pathlib import Path
import argparse
import json
import os
import re
import shutil
import subprocess
import time


ADAPTER_ID = "qubes-i3-x11"


# Approved surfaces are explicit rather than allowing arbitrary
# qvm-run commands from host presentation code.
APPROVED_SURFACES = {
    "reasoning-menu": {
        "qube": "Cherry-AI",

        "window_class":
            "Cherry-AI:reasoning_menu.py",

        "title_prefix":
            "Forest Reasoning",

        "remote_launcher":
            (
                "/home/user/The-Forest/bristlecone/"
                "bin/forest-reasoning-menu"
            ),

        "modes": {
            "temporary":
                "--temporary",

            "baseline":
                "--baseline",
        },
    },
}


STATE_ROOT = (
    Path.home()
    / ".local"
    / "state"
    / "the-forest"
    / "presentation"
)


WINDOW_TIMEOUT_SECONDS = 45.0
POLL_SECONDS = 0.05


def command_path(name):
    return shutil.which(
        name
    )


def required_commands():
    return (
        "qvm-run",
        "i3-msg",
        "xrandr",
    )


def require_host_commands():
    missing = [
        name
        for name in required_commands()
        if command_path(name) is None
    ]

    if missing:
        raise RuntimeError(
            "Missing required host command(s): "
            + ", ".join(missing)
        )


def run(
    argv,
    *,
    check=True,
):
    return subprocess.run(
        argv,
        check=check,
        capture_output=True,
        text=True,
    )


def surface_spec(
    surface_id,
):
    try:
        return APPROVED_SURFACES[
            surface_id
        ]

    except KeyError as exc:
        raise ValueError(
            "Unknown or unapproved Forest surface: "
            + str(surface_id)
        ) from exc


# ============================================================
# I3 TREE
# ============================================================

def i3_tree():
    result = run(
        [
            "i3-msg",
            "-t",
            "get_tree",
        ]
    )

    return json.loads(
        result.stdout
    )


def walk_tree(node):
    yield node

    for key in (
        "nodes",
        "floating_nodes",
    ):
        for child in (
            node.get(key)
            or ()
        ):
            yield from walk_tree(
                child
            )


def node_rect(node):
    rect = (
        node.get("rect")
        or {}
    )

    return {
        "x": int(
            rect.get("x", 0)
        ),

        "y": int(
            rect.get("y", 0)
        ),

        "width": int(
            rect.get("width", 0)
        ),

        "height": int(
            rect.get("height", 0)
        ),
    }


def focused_window_rect(tree):
    for node in walk_tree(
        tree
    ):
        if not node.get(
            "focused"
        ):
            continue

        rect = node_rect(
            node
        )

        if (
            rect["width"] > 0
            and rect["height"] > 0
        ):
            return rect

    return None


def node_matches_surface(
    node,
    surface_id,
):
    spec = surface_spec(
        surface_id
    )

    props = (
        node.get(
            "window_properties"
        )
        or {}
    )

    window_class = (
        props.get("class")
        or ""
    )

    title = (
        node.get("name")
        or ""
    )

    return (
        window_class
        == spec["window_class"]
        and title.startswith(
            spec["title_prefix"]
        )
    )


def surface_windows(
    tree,
    surface_id,
):
    windows = []

    for node in walk_tree(
        tree
    ):
        if not node_matches_surface(
            node,
            surface_id,
        ):
            continue

        windows.append(
            {
                "con_id":
                    node.get("id"),

                "window_id":
                    node.get("window"),

                "title":
                    node.get("name"),

                "floating":
                    node.get("floating"),

                "rect":
                    node_rect(
                        node
                    ),
            }
        )

    return windows


# ============================================================
# MONITOR GEOMETRY
# ============================================================

MONITOR_RE = re.compile(
    r"(?P<width>\d+)/\d+"
    r"x(?P<height>\d+)/\d+"
    r"\+(?P<x>-?\d+)"
    r"\+(?P<y>-?\d+)"
)


def parse_monitors(text):
    monitors = []

    for line in text.splitlines():
        match = MONITOR_RE.search(
            line
        )

        if match is None:
            continue

        values = {
            key: int(value)
            for key, value
            in match.groupdict().items()
        }

        monitors.append(
            {
                **values,

                "primary":
                    "+*" in line,

                "raw":
                    line.strip(),
            }
        )

    return monitors


def current_monitors():
    result = run(
        [
            "xrandr",
            "--listmonitors",
        ]
    )

    monitors = parse_monitors(
        result.stdout
    )

    if not monitors:
        raise RuntimeError(
            "Could not determine monitor geometry."
        )

    return monitors


def intersection_area(
    rect,
    monitor,
):
    left = max(
        rect["x"],
        monitor["x"],
    )

    top = max(
        rect["y"],
        monitor["y"],
    )

    right = min(
        rect["x"]
        + rect["width"],

        monitor["x"]
        + monitor["width"],
    )

    bottom = min(
        rect["y"]
        + rect["height"],

        monitor["y"]
        + monitor["height"],
    )

    if (
        right <= left
        or bottom <= top
    ):
        return 0

    return (
        (right - left)
        * (bottom - top)
    )


def monitor_for_rect(
    rect,
    monitors,
):
    ranked = sorted(
        monitors,
        key=lambda monitor:
            intersection_area(
                rect,
                monitor,
            ),
        reverse=True,
    )

    if (
        ranked
        and intersection_area(
            rect,
            ranked[0],
        ) > 0
    ):
        return ranked[0]

    for monitor in monitors:
        if monitor.get(
            "primary"
        ):
            return monitor

    return monitors[0]


def center_over(
    anchor,
    width,
    height,
):
    return {
        "x":
            anchor["x"]
            + (
                anchor["width"]
                - width
            ) // 2,

        "y":
            anchor["y"]
            + (
                anchor["height"]
                - height
            ) // 2,

        "width":
            width,

        "height":
            height,
    }


def clamp_to_monitor(
    rect,
    monitor,
):
    width = rect[
        "width"
    ]

    height = rect[
        "height"
    ]

    max_x = (
        monitor["x"]
        + max(
            0,
            monitor["width"]
            - width,
        )
    )

    max_y = (
        monitor["y"]
        + max(
            0,
            monitor["height"]
            - height,
        )
    )

    return {
        **rect,

        "x":
            min(
                max(
                    rect["x"],
                    monitor["x"],
                ),
                max_x,
            ),

        "y":
            min(
                max(
                    rect["y"],
                    monitor["y"],
                ),
                max_y,
            ),
    }


# ============================================================
# MACHINE-LOCAL POSITION STATE
# ============================================================

def position_file(
    surface_id,
):
    # surface_id comes only from the approved registry.
    surface_spec(
        surface_id
    )

    return (
        STATE_ROOT
        / f"{surface_id}.json"
    )


def read_saved_position(
    surface_id,
):
    path = position_file(
        surface_id
    )

    if not path.exists():
        return None

    try:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return {
            "x": int(
                data["x"]
            ),

            "y": int(
                data["y"]
            ),
        }

    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
    ):
        return None


def save_position(
    surface_id,
    rect,
):
    path = position_file(
        surface_id
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "schema_version": 1,

        "adapter_id":
            ADAPTER_ID,

        "surface_id":
            surface_id,

        "x":
            int(
                rect["x"]
            ),

        "y":
            int(
                rect["y"]
            ),

        "saved_at_unix":
            time.time(),
    }

    temp = path.with_name(
        path.name + ".tmp"
    )

    temp.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    os.replace(
        temp,
        path,
    )


def reset_position(
    surface_id,
):
    path = position_file(
        surface_id
    )

    try:
        path.unlink()

    except FileNotFoundError:
        pass


# ============================================================
# I3 WINDOW CONTROL
# ============================================================

def i3_window_command(
    window,
    command,
):
    con_id = window.get(
        "con_id"
    )

    if con_id is None:
        raise RuntimeError(
            "Forest window has no i3 container ID."
        )

    result = run(
        [
            "i3-msg",
            f'[con_id="{con_id}"]',
            command,
        ],
        check=False,
    )

    try:
        response = json.loads(
            result.stdout
        )

    except ValueError:
        response = []

    if (
        result.returncode != 0
        or not response
        or not all(
            item.get(
                "success",
                False,
            )
            for item in response
        )
    ):
        raise RuntimeError(
            "i3 could not apply Forest "
            "presentation command: "
            + command
        )


def find_surface_window(
    surface_id,
    con_id,
):
    tree = i3_tree()

    for window in surface_windows(
        tree,
        surface_id,
    ):
        if (
            window["con_id"]
            == con_id
        ):
            return window

    return None


def wait_for_new_surface_window(
    surface_id,
    previous_ids,
):
    deadline = (
        time.monotonic()
        + WINDOW_TIMEOUT_SECONDS
    )

    while (
        time.monotonic()
        < deadline
    ):
        tree = i3_tree()

        for window in surface_windows(
            tree,
            surface_id,
        ):
            if (
                window["con_id"]
                not in previous_ids
            ):
                return window

        time.sleep(
            POLL_SECONDS
        )

    raise RuntimeError(
        "Timed out waiting for Forest surface: "
        + surface_id
    )


# ============================================================
# QUBES LAUNCH BRIDGE
# ============================================================

def build_qvm_run_command(
    surface_id,
    mode,
):
    spec = surface_spec(
        surface_id
    )

    try:
        mode_argument = (
            spec["modes"][
                mode
            ]
        )

    except KeyError as exc:
        raise ValueError(
            "Unsupported surface mode: "
            + str(mode)
        ) from exc

    qvm_run = command_path(
        "qvm-run"
    ) or "qvm-run"

    return [
        qvm_run,

        "--quiet",
        "--autostart",
        "--gui",
        "--no-shell",

        spec["qube"],

        spec["remote_launcher"],

        mode_argument,
    ]


def launch_surface(
    surface_id,
    mode,
):
    command = build_qvm_run_command(
        surface_id,
        mode,
    )

    return subprocess.Popen(
        command,

        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,

        start_new_session=True,
    )


# ============================================================
# PLACEMENT POLICY IMPLEMENTATION
#
# Portable policy:
#   focused-window
#   floating preferred
#   raise preferred
#   remember position
#   keep visible
#
# This adapter supplies those capabilities for i3/X11.
# ============================================================

def choose_position(
    surface_id,
    window_rect,
    focused_before,
    monitors,
):
    saved = read_saved_position(
        surface_id
    )

    if saved is not None:
        candidate = {
            **window_rect,

            "x":
                saved["x"],

            "y":
                saved["y"],
        }

        if any(
            intersection_area(
                candidate,
                monitor,
            ) > 0
            for monitor in monitors
        ):
            monitor = monitor_for_rect(
                candidate,
                monitors,
            )

            return (
                clamp_to_monitor(
                    candidate,
                    monitor,
                ),
                True,
            )

    anchor = (
        focused_before
        if focused_before is not None
        else monitors[0]
    )

    candidate = center_over(
        anchor,
        window_rect["width"],
        window_rect["height"],
    )

    monitor = monitor_for_rect(
        candidate,
        monitors,
    )

    return (
        clamp_to_monitor(
            candidate,
            monitor,
        ),
        False,
    )


def manage_surface(
    surface_id,
    mode,
):
    require_host_commands()

    tree_before = i3_tree()

    focused_before = (
        focused_window_rect(
            tree_before
        )
    )

    previous_ids = {
        window["con_id"]
        for window in surface_windows(
            tree_before,
            surface_id,
        )
    }

    launch_surface(
        surface_id,
        mode,
    )

    window = (
        wait_for_new_surface_window(
            surface_id,
            previous_ids,
        )
    )

    # Prefer an i3 for_window rule so the surface is
    # floating from the instant i3 manages it.
    #
    # Fall back to floating it here when that host rule is
    # unavailable. Avoid the extra command and delay when the
    # window is already floating.
    already_floating = (
        window.get("floating")
        in (
            "user_on",
            "auto_on",
        )
    )

    if not already_floating:
        i3_window_command(
            window,
            "floating enable",
        )

        time.sleep(
            0.05
        )

        refreshed = (
            find_surface_window(
                surface_id,
                window["con_id"],
            )
        )

        if refreshed is not None:
            window = refreshed

    monitors = current_monitors()

    target, restored = choose_position(
        surface_id,
        window["rect"],
        focused_before,
        monitors,
    )

    i3_window_command(
        window,
        (
            "move position "
            f'{target["x"]} px '
            f'{target["y"]} px, '
            "focus"
        ),
    )

    # If a previously stored position became invalid,
    # replace it with the safe recovered position.
    if (
        read_saved_position(
            surface_id
        )
        is not None
        and not restored
    ):
        save_position(
            surface_id,
            target,
        )

    initial_position = {
        "x":
            target["x"],

        "y":
            target["y"],
    }

    last_saved = (
        read_saved_position(
            surface_id
        )
    )

    # Observe this exact surface until it closes.
    # A user move becomes machine-local remembered state.
    while True:
        current = (
            find_surface_window(
                surface_id,
                window["con_id"],
            )
        )

        if current is None:
            break

        rect = current["rect"]

        current_position = {
            "x":
                rect["x"],

            "y":
                rect["y"],
        }

        if (
            current_position
            != initial_position
            and current_position
            != last_saved
        ):
            save_position(
                surface_id,
                rect,
            )

            last_saved = (
                current_position
            )

        time.sleep(
            0.20
        )


# ============================================================
# INSPECTION / SELF TEST
# ============================================================

def probe(
    surface_id,
):
    spec = surface_spec(
        surface_id
    )

    print(
        "adapter_id:",
        ADAPTER_ID,
    )

    print(
        "surface_id:",
        surface_id,
    )

    print(
        "qube:",
        spec["qube"],
    )

    print(
        "window_class:",
        spec["window_class"],
    )

    print(
        "state_file:",
        position_file(
            surface_id
        ),
    )

    print(
        "commands:"
    )

    for name in (
        "qvm-run",
        "i3-msg",
        "xrandr",
        "picom",
    ):
        print(
            " ",
            name,
            "=>",
            command_path(name)
            or "unavailable",
        )

    print(
        "saved_position:",
        read_saved_position(
            surface_id
        ),
    )


def self_test():
    # These dimensions are only a parser/geometry fixture.
    # Runtime monitor geometry is always discovered live.
    sample = """Monitors: 2
 0: +*DisplayPort-2 2560/597x1440/336+0+0  DisplayPort-2
 1: +HDMI-A-0 1360/160x768/90+2560+0  HDMI-A-0
"""

    monitors = parse_monitors(
        sample
    )

    assert len(monitors) == 2

    assert monitors[0][
        "width"
    ] == 2560

    assert monitors[0][
        "height"
    ] == 1440

    assert monitors[0][
        "primary"
    ] is True

    assert monitors[1][
        "x"
    ] == 2560


    anchor = {
        "x": 100,
        "y": 100,
        "width": 1000,
        "height": 800,
    }

    centered = center_over(
        anchor,
        400,
        300,
    )

    assert centered == {
        "x": 400,
        "y": 350,
        "width": 400,
        "height": 300,
    }


    partly_offscreen = {
        "x": 2500,
        "y": 1400,
        "width": 420,
        "height": 320,
    }

    clamped = clamp_to_monitor(
        partly_offscreen,
        monitors[0],
    )

    assert clamped[
        "x"
    ] == 2140

    assert clamped[
        "y"
    ] == 1120


    second_monitor_window = {
        "x": 2700,
        "y": 100,
        "width": 420,
        "height": 320,
    }

    assert (
        monitor_for_rect(
            second_monitor_window,
            monitors,
        )
        == monitors[1]
    )


    command = build_qvm_run_command(
        "reasoning-menu",
        "temporary",
    )

    assert "--autostart" in command
    assert "--gui" in command
    assert "--no-shell" in command
    assert "Cherry-AI" in command
    assert "--temporary" in command


    print(
        "QUBES-I3-X11-SELF-TEST-PASS"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Forest Qubes/i3/X11 "
            "host presentation adapter"
        )
    )

    parser.add_argument(
        "mode",
        nargs="?",
        choices=(
            "temporary",
            "baseline",
        ),
    )

    parser.add_argument(
        "--surface",
        default="reasoning-menu",
    )

    parser.add_argument(
        "--probe",
        action="store_true",
    )

    parser.add_argument(
        "--self-test",
        action="store_true",
    )

    parser.add_argument(
        "--reset-position",
        action="store_true",
    )

    args = parser.parse_args()

    surface_id = args.surface

    # Validate against explicit approved registry.
    surface_spec(
        surface_id
    )

    if args.self_test:
        self_test()
        return 0

    if args.probe:
        probe(
            surface_id
        )

        return 0

    if args.reset_position:
        reset_position(
            surface_id
        )

        print(
            "Saved Forest presentation "
            "position reset:",
            surface_id,
        )

        return 0

    if args.mode is None:
        parser.error(
            "temporary or baseline is required"
        )

    manage_surface(
        surface_id,
        args.mode,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
