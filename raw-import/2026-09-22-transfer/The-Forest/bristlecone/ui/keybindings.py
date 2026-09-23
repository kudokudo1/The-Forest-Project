"""Configurable Forest UI keybindings.

This file controls in-window Forest UI bindings.

It does NOT define desktop-global shortcuts such as i3 bindsym.
Those belong to presentation/host adapters.

Default bindings are defaults, not architecture.
"""

from pathlib import Path
import json
import os
import re

from ui.actions import (
    ACTION_DEFINITIONS,
    ACTION_TEMP_RESUME,
    ACTION_TEMP_LIGHT,
    ACTION_TEMP_NORMAL,
    ACTION_TEMP_DEEP,
    ACTION_BASELINE_AUTO,
    ACTION_BASELINE_LIGHT,
    ACTION_BASELINE_NORMAL,
    ACTION_BASELINE_DEEP,
    ACTION_CANCEL,
    actions_for_menu,
)


SCHEMA_VERSION = 1


DEFAULT_BINDINGS = {
    ACTION_TEMP_RESUME:
        "backtick",

    ACTION_TEMP_LIGHT:
        "1",

    ACTION_TEMP_NORMAL:
        "2",

    ACTION_TEMP_DEEP:
        "3",

    ACTION_BASELINE_AUTO:
        "backtick",

    ACTION_BASELINE_LIGHT:
        "1",

    ACTION_BASELINE_NORMAL:
        "2",

    ACTION_BASELINE_DEEP:
        "3",

    ACTION_CANCEL:
        "escape",
}


DISPLAY_KEYS = {
    "backtick": "~",
    "escape": "Esc",
    "enter": "Enter",
    "space": "Space",
    "tab": "Tab",
    "backspace": "Backspace",
    "delete": "Delete",
    "pageup": "Page Up",
    "pagedown": "Page Down",
}


GTK_KEY_ALIASES = {
    "grave": "backtick",

    "Escape": "escape",

    "Return": "enter",
    "KP_Enter": "enter",

    "space": "space",

    "Tab": "tab",
    "ISO_Left_Tab": "tab",

    "BackSpace": "backspace",
    "Delete": "delete",

    "Left": "left",
    "Right": "right",
    "Up": "up",
    "Down": "down",

    "Home": "home",
    "End": "end",

    "Page_Up": "pageup",
    "Page_Down": "pagedown",

    # Keypad aliases intentionally normalize to the
    # equivalent digit for in-window controls.
    "KP_0": "0",
    "KP_Insert": "0",

    "KP_1": "1",
    "KP_End": "1",

    "KP_2": "2",
    "KP_Down": "2",

    "KP_3": "3",
    "KP_Next": "3",
    "KP_Page_Down": "3",

    "KP_4": "4",
    "KP_Left": "4",

    "KP_5": "5",
    "KP_Begin": "5",

    "KP_6": "6",
    "KP_Right": "6",

    "KP_7": "7",
    "KP_Home": "7",

    "KP_8": "8",
    "KP_Up": "8",

    "KP_9": "9",
    "KP_Page_Up": "9",
}


def config_path():
    override = os.environ.get(
        "FOREST_KEYBINDINGS_FILE"
    )

    if override:
        return Path(
            override
        ).expanduser()

    config_home = os.environ.get(
        "XDG_CONFIG_HOME"
    )

    if config_home:
        base = Path(
            config_home
        ).expanduser()

    else:
        base = (
            Path.home()
            / ".config"
        )

    return (
        base
        / "the-forest"
        / "ui"
        / "keybindings.json"
    )


def normalize_user_key(
    value,
):
    value = str(
        value
    ).strip()

    aliases = {
        "`": "backtick",
        "grave": "backtick",
        "backtick": "backtick",

        "esc": "escape",
        "escape": "escape",

        "return": "enter",
        "enter": "enter",

        "space": "space",
        "tab": "tab",

        "pgup": "pageup",
        "pageup": "pageup",

        "pgdn": "pagedown",
        "pagedown": "pagedown",

        "del": "delete",
        "delete": "delete",

        "backspace": "backspace",

        "left": "left",
        "right": "right",
        "up": "up",
        "down": "down",

        "home": "home",
        "end": "end",
    }

    lower = value.lower()

    if lower in aliases:
        return aliases[
            lower
        ]

    if len(value) == 1:
        return value.lower()

    if re.fullmatch(
        r"f(?:[1-9]|1[0-2])",
        lower,
    ):
        return lower

    raise ValueError(
        "Unsupported single-key binding: "
        + repr(value)
    )


def normalize_gtk_key_name(
    name,
):
    if name in GTK_KEY_ALIASES:
        return GTK_KEY_ALIASES[
            name
        ]

    value = str(
        name
    )

    if len(value) == 1:
        return value.lower()

    lower = value.lower()

    if re.fullmatch(
        r"f(?:[1-9]|1[0-2])",
        lower,
    ):
        return lower

    return lower.replace(
        "_",
        "",
    )


def display_key(
    token,
):
    return DISPLAY_KEYS.get(
        token,
        token.upper()
        if len(token) == 1
        else token,
    )


def _load_override_mapping(
    path,
):
    if not path.exists():
        return {}

    try:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except (
        OSError,
        ValueError,
        TypeError,
    ) as exc:
        raise ValueError(
            "Could not read Forest keybindings: "
            + str(exc)
        ) from exc

    if not isinstance(
        data,
        dict,
    ):
        raise ValueError(
            "Keybinding file must contain "
            "a JSON object."
        )

    if (
        data.get(
            "schema_version"
        )
        != SCHEMA_VERSION
    ):
        raise ValueError(
            "Unsupported keybinding schema."
        )

    raw = data.get(
        "bindings",
        {},
    )

    if not isinstance(
        raw,
        dict,
    ):
        raise ValueError(
            "bindings must be a JSON object."
        )

    result = {}

    for action_id, key in raw.items():
        if action_id not in ACTION_DEFINITIONS:
            raise ValueError(
                "Unknown Forest action in "
                "keybinding file: "
                + str(action_id)
            )

        result[
            action_id
        ] = normalize_user_key(
            key
        )

    return result


def validate_bindings(
    bindings,
):
    expected = set(
        ACTION_DEFINITIONS
    )

    if set(bindings) != expected:
        raise ValueError(
            "Keybinding map does not exactly "
            "match registered Forest actions."
        )

    for menu_mode in (
        "temporary",
        "baseline",
    ):
        seen = {}

        for action_id in actions_for_menu(
            menu_mode
        ):
            key = bindings[
                action_id
            ]

            other = seen.get(
                key
            )

            if other is not None:
                raise ValueError(
                    "Keybinding conflict in "
                    f"{menu_mode} menu: "
                    f"{key!r} is assigned to "
                    f"{other!r} and "
                    f"{action_id!r}"
                )

            seen[
                key
            ] = action_id


class ReasoningKeyBindingRegistry:

    def __init__(
        self,
        path=None,
    ):
        self.path = (
            Path(path).expanduser()
            if path is not None
            else config_path()
        )

        self.reload()


    def reload(
        self,
    ):
        overrides = (
            _load_override_mapping(
                self.path
            )
        )

        bindings = dict(
            DEFAULT_BINDINGS
        )

        bindings.update(
            overrides
        )

        validate_bindings(
            bindings
        )

        self.overrides = overrides
        self.bindings = bindings

        return self


    def binding_for(
        self,
        action_id,
    ):
        if action_id not in self.bindings:
            raise KeyError(
                action_id
            )

        return self.bindings[
            action_id
        ]


    def display_for(
        self,
        action_id,
    ):
        return display_key(
            self.binding_for(
                action_id
            )
        )


    def bindings_for_menu(
        self,
        menu_mode,
    ):
        return {
            action_id:
                self.binding_for(
                    action_id
                )

            for action_id
            in actions_for_menu(
                menu_mode
            )
        }


    def action_for_gtk_key(
        self,
        menu_mode,
        gtk_key_name,
    ):
        token = normalize_gtk_key_name(
            gtk_key_name
        )

        for action_id in actions_for_menu(
            menu_mode
        ):
            if (
                self.binding_for(
                    action_id
                )
                == token
            ):
                return action_id

        return None


    def all_bindings(
        self,
    ):
        return dict(
            self.bindings
        )


    def set_binding(
        self,
        action_id,
        key,
    ):
        if action_id not in ACTION_DEFINITIONS:
            raise ValueError(
                "Unknown Forest action: "
                + str(action_id)
            )

        normalized = normalize_user_key(
            key
        )

        candidate_overrides = dict(
            self.overrides
        )

        candidate_overrides[
            action_id
        ] = normalized

        candidate = dict(
            DEFAULT_BINDINGS
        )

        candidate.update(
            candidate_overrides
        )

        validate_bindings(
            candidate
        )

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "schema_version":
                SCHEMA_VERSION,

            "bindings":
                candidate_overrides,
        }

        temp = self.path.with_name(
            self.path.name + ".tmp"
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
            self.path,
        )

        self.reload()

        return normalized


    def reset(
        self,
    ):
        try:
            self.path.unlink()

        except FileNotFoundError:
            pass

        self.reload()
