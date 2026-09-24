"""Stable Forest UI action identities.

Actions describe WHAT the user wants to do.

Keys, buttons, gestures, host shortcuts, and future interfaces
describe HOW the user invokes the action.

The action identity must remain stable when a keybinding changes.
"""

ACTION_TEMP_RESUME = (
    "reasoning.temporary.resume-baseline"
)

ACTION_TEMP_LIGHT = (
    "reasoning.temporary.light"
)

ACTION_TEMP_NORMAL = (
    "reasoning.temporary.normal"
)

ACTION_TEMP_DEEP = (
    "reasoning.temporary.deep"
)

ACTION_BASELINE_AUTO = (
    "reasoning.baseline.auto"
)

ACTION_BASELINE_LIGHT = (
    "reasoning.baseline.pin-light"
)

ACTION_BASELINE_NORMAL = (
    "reasoning.baseline.pin-normal"
)

ACTION_BASELINE_DEEP = (
    "reasoning.baseline.pin-deep"
)

ACTION_CANCEL = (
    "reasoning.menu.cancel"
)


ACTION_DEFINITIONS = {
    ACTION_TEMP_RESUME: {
        "scope": "temporary",
        "label": "Resume baseline",
    },

    ACTION_TEMP_LIGHT: {
        "scope": "temporary",
        "label": "Light",
    },

    ACTION_TEMP_NORMAL: {
        "scope": "temporary",
        "label": "Normal",
    },

    ACTION_TEMP_DEEP: {
        "scope": "temporary",
        "label": "Deep",
    },

    ACTION_BASELINE_AUTO: {
        "scope": "baseline",
        "label": "Auto",
    },

    ACTION_BASELINE_LIGHT: {
        "scope": "baseline",
        "label": "Pin Light",
    },

    ACTION_BASELINE_NORMAL: {
        "scope": "baseline",
        "label": "Pin Normal",
    },

    ACTION_BASELINE_DEEP: {
        "scope": "baseline",
        "label": "Pin Deep",
    },

    ACTION_CANCEL: {
        "scope": "common",
        "label": "Cancel",
    },
}


def actions_for_menu(
    menu_mode,
):
    if menu_mode not in (
        "temporary",
        "baseline",
    ):
        raise ValueError(
            "menu_mode must be temporary or baseline"
        )

    return tuple(
        action_id
        for action_id, definition
        in ACTION_DEFINITIONS.items()
        if definition["scope"]
        in (
            menu_mode,
            "common",
        )
    )
