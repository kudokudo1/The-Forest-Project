#!/usr/bin/env python3
"""Forest-owned reasoning-control menu.

Engineering identifiers remain:

    auto
    light
    normal
    deep

Forest-language display names are intentionally unresolved.

This UI contains no reasoning-routing logic and never edits
active.yaml directly. All state changes pass through the
TaskSessionManager reasoning-control API.
"""

from pathlib import Path
import argparse
import os
import sys


DEFAULT_ROOT = (
    Path.home()
    / "The-Forest"
    / "bristlecone"
)


def get_root():
    override = os.environ.get(
        "FOREST_ROOT"
    )

    if override:
        return Path(
            override
        ).expanduser().resolve()

    return DEFAULT_ROOT


def title_mode(value):
    if value is None:
        return "None"

    return str(
        value
    ).capitalize()


class ReasoningBackend:
    """Thin presentation wrapper over Forest control APIs."""

    def __init__(
        self,
        root=None,
    ):
        self.root = (
            Path(root).resolve()
            if root is not None
            else get_root()
        )

        repo = str(
            DEFAULT_ROOT
        )

        if repo not in sys.path:
            sys.path.insert(
                0,
                repo,
            )

        from runtime.task_session import (
            TaskSessionManager,
        )

        self.manager = (
            TaskSessionManager(
                forest_root=self.root
            )
        )


    def read(self):
        control = (
            self.manager
            .get_reasoning_control()
            ["control"]
        )

        temporary = (
            control.temporary
        )

        return {
            "baseline_policy":
                control.baseline.policy,

            "baseline_mode":
                control.baseline.mode,

            "temporary_mode":
                (
                    None
                    if temporary is None
                    else temporary.mode
                ),

            "temporary_turns":
                (
                    None
                    if temporary is None
                    else temporary.turns_remaining
                ),

            "temporary_default":
                (
                    control.settings
                    .temporary_turn_default
                ),
        }


    def temporary(
        self,
        mode,
    ):
        return (
            self.manager
            .set_temporary_reasoning_mode(
                mode,
                persist=True,
            )
        )


    def clear_temporary(
        self,
    ):
        return (
            self.manager
            .clear_temporary_reasoning_mode(
                persist=True,
            )
        )


    def pin(
        self,
        mode,
    ):
        return (
            self.manager
            .pin_reasoning_mode(
                mode,
                persist=True,
            )
        )


    def auto(
        self,
    ):
        # Clear the pin while preserving any temporary lease.
        return (
            self.manager
            .set_reasoning_auto_baseline(
                persist=True,
            )
        )


def display_state(state):
    if (
        state["baseline_policy"]
        == "auto"
    ):
        baseline = "Auto"

    else:
        baseline = (
            "Pinned "
            + title_mode(
                state["baseline_mode"]
            )
        )

    if (
        state["temporary_mode"]
        is None
    ):
        temporary = "None"

    else:
        temporary = (
            title_mode(
                state["temporary_mode"]
            )
            + " · "
            + str(
                state["temporary_turns"]
            )
            + " turns remaining"
        )

    return {
        "baseline": baseline,
        "temporary": temporary,
        "default": (
            state[
                "temporary_default"
            ]
        ),
    }


def load_gtk():
    import gi

    errors = []

    for version in (
        "4.0",
        "3.0",
    ):
        try:
            gi.require_version(
                "Gtk",
                version,
            )

            from gi.repository import (
                Gtk,
                Gdk,
            )

            return (
                Gtk,
                Gdk,
                int(
                    version.split(".")[0]
                ),
            )

        except (
            ValueError,
            ImportError,
        ) as exc:
            errors.append(
                f"GTK {version}: {exc}"
            )

    raise RuntimeError(
        "No supported GTK binding found. "
        + " | ".join(errors)
    )


class ReasoningWindow:

    KEY_GROUPS = {
        "0": {
            "0",
            "KP_0",
            "KP_Insert",
        },

        "1": {
            "1",
            "KP_1",
            "KP_End",
        },

        "2": {
            "2",
            "KP_2",
            "KP_Down",
        },

        "3": {
            "3",
            "KP_3",
            "KP_Page_Down",
            "KP_Next",
        },
    }


    def __init__(
        self,
        *,
        menu_mode,
        backend,
        Gtk,
        Gdk,
        gtk_major,
        application=None,
    ):
        if menu_mode not in (
            "temporary",
            "baseline",
        ):
            raise ValueError(
                "Unknown reasoning menu mode."
            )

        self.menu_mode = menu_mode
        self.backend = backend
        self.Gtk = Gtk
        self.Gdk = Gdk
        self.gtk_major = gtk_major

        if gtk_major >= 4:
            self.window = (
                Gtk.ApplicationWindow(
                    application=application
                )
            )

        else:
            self.window = (
                Gtk.Window()
            )

            self.window.connect(
                "destroy",
                Gtk.main_quit,
            )

        self.window.set_title(
            (
                "Forest Reasoning — Temporary"
                if menu_mode == "temporary"
                else "Forest Reasoning — Baseline"
            )
        )

        self.window.set_default_size(
            420,
            320,
        )

        box = Gtk.Box(
            orientation=(
                Gtk.Orientation.VERTICAL
            ),
            spacing=10,
        )

        for name in (
            "set_margin_top",
            "set_margin_bottom",
            "set_margin_start",
            "set_margin_end",
        ):
            setter = getattr(
                box,
                name,
                None,
            )

            if setter is not None:
                setter(18)

        self.box = box

        if gtk_major >= 4:
            self.window.set_child(
                box
            )

        else:
            self.window.add(
                box
            )

        heading = Gtk.Label(
            label=(
                "Reasoning — Temporary"
                if menu_mode == "temporary"
                else "Reasoning — Baseline"
            )
        )

        heading.set_xalign(
            0.0
        )

        self.add(
            heading
        )

        self.status = Gtk.Label(
            label=""
        )

        self.status.set_xalign(
            0.0
        )

        if gtk_major >= 4:
            self.status.set_wrap(
                True
            )

        else:
            self.status.set_line_wrap(
                True
            )

        self.add(
            self.status
        )

        if menu_mode == "temporary":
            choices = (
                (
                    "0",
                    "Resume baseline",
                    self.backend.clear_temporary,
                ),

                (
                    "1",
                    "Light",
                    lambda:
                        self.backend.temporary(
                            "light"
                        ),
                ),

                (
                    "2",
                    "Normal",
                    lambda:
                        self.backend.temporary(
                            "normal"
                        ),
                ),

                (
                    "3",
                    "Deep",
                    lambda:
                        self.backend.temporary(
                            "deep"
                        ),
                ),
            )

        else:
            choices = (
                (
                    "0",
                    "Auto",
                    self.backend.auto,
                ),

                (
                    "1",
                    "Pin Light",
                    lambda:
                        self.backend.pin(
                            "light"
                        ),
                ),

                (
                    "2",
                    "Pin Normal",
                    lambda:
                        self.backend.pin(
                            "normal"
                        ),
                ),

                (
                    "3",
                    "Pin Deep",
                    lambda:
                        self.backend.pin(
                            "deep"
                        ),
                ),
            )

        self.actions = {}

        for (
            key,
            label,
            callback,
        ) in choices:
            self.actions[
                key
            ] = callback

            button = Gtk.Button(
                label=f"{key}   {label}"
            )

            button.connect(
                "clicked",
                self.clicked,
                callback,
            )

            self.add(
                button
            )

        cancel = Gtk.Label(
            label="Esc   Cancel"
        )

        cancel.set_xalign(
            0.0
        )

        self.add(
            cancel
        )

        self.refresh()

        if gtk_major >= 4:
            controller = (
                Gtk.EventControllerKey()
            )

            controller.connect(
                "key-pressed",
                self.key_pressed_gtk4,
            )

            self.window.add_controller(
                controller
            )

        else:
            self.window.connect(
                "key-press-event",
                self.key_pressed_gtk3,
            )


    def add(
        self,
        widget,
    ):
        if self.gtk_major >= 4:
            self.box.append(
                widget
            )

        else:
            self.box.pack_start(
                widget,
                False,
                False,
                0,
            )


    def refresh(
        self,
    ):
        state = display_state(
            self.backend.read()
        )

        if (
            self.menu_mode
            == "temporary"
        ):
            text = (
                f"Baseline: "
                f"{state['baseline']}\n"
                f"Temporary: "
                f"{state['temporary']}\n"
                f"Duration: "
                f"{state['default']} turns"
            )

        else:
            text = (
                f"Baseline: "
                f"{state['baseline']}\n"
                f"Temporary: "
                f"{state['temporary']}\n"
                f"Temporary default: "
                f"{state['default']} turns"
            )

        self.status.set_text(
            text
        )


    def clicked(
        self,
        button,
        callback,
    ):
        self.run_action(
            callback
        )


    def run_action(
        self,
        callback,
    ):
        try:
            callback()

        except Exception as exc:
            self.status.set_text(
                "Forest control error:\n"
                + str(exc)
            )

            return

        self.close()


    def key_name(
        self,
        keyval,
    ):
        name = self.Gdk.keyval_name(
            keyval
        )

        return (
            ""
            if name is None
            else str(name)
        )


    def dispatch_key(
        self,
        name,
    ):
        if name == "Escape":
            self.close()
            return True

        for (
            number,
            names,
        ) in self.KEY_GROUPS.items():
            if name in names:
                self.run_action(
                    self.actions[
                        number
                    ]
                )

                return True

        return False


    def key_pressed_gtk4(
        self,
        controller,
        keyval,
        keycode,
        state,
    ):
        return self.dispatch_key(
            self.key_name(
                keyval
            )
        )


    def key_pressed_gtk3(
        self,
        window,
        event,
    ):
        return self.dispatch_key(
            self.key_name(
                event.keyval
            )
        )


    def close(
        self,
    ):
        if self.gtk_major >= 4:
            self.window.close()

        else:
            self.window.destroy()


    def show(
        self,
    ):
        if self.gtk_major >= 4:
            self.window.present()

        else:
            self.window.show_all()


def run_gui(
    menu_mode,
):
    Gtk, Gdk, gtk_major = (
        load_gtk()
    )

    backend = ReasoningBackend()

    if gtk_major >= 4:

        class App(
            Gtk.Application
        ):
            def __init__(self):
                super().__init__(
                    application_id=(
                        "org.theforest."
                        "reasoningmenu"
                    )
                )

                self.menu_window = None


            def do_activate(
                self,
            ):
                self.menu_window = (
                    ReasoningWindow(
                        menu_mode=menu_mode,
                        backend=backend,
                        Gtk=Gtk,
                        Gdk=Gdk,
                        gtk_major=gtk_major,
                        application=self,
                    )
                )

                self.menu_window.show()


        application = App()

        return application.run(
            sys.argv[:1]
        )

    window = ReasoningWindow(
        menu_mode=menu_mode,
        backend=backend,
        Gtk=Gtk,
        Gdk=Gdk,
        gtk_major=gtk_major,
    )

    window.show()

    Gtk.main()

    return 0


def print_status():
    state = display_state(
        ReasoningBackend().read()
    )

    print(
        "Baseline:",
        state["baseline"],
    )

    print(
        "Temporary:",
        state["temporary"],
    )

    print(
        "Temporary default:",
        state["default"],
    )


def check_gui():
    Gtk, Gdk, gtk_major = (
        load_gtk()
    )

    print(
        "PyGObject: AVAILABLE"
    )

    print(
        f"GTK major: {gtk_major}"
    )

    print(
        "Forest GTK menu support: AVAILABLE"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Forest reasoning-control menu"
        )
    )

    group = (
        parser
        .add_mutually_exclusive_group()
    )

    group.add_argument(
        "--temporary",
        action="store_true",
        help=(
            "Open temporary reasoning menu."
        ),
    )

    group.add_argument(
        "--baseline",
        action="store_true",
        help=(
            "Open baseline reasoning menu."
        ),
    )

    group.add_argument(
        "--status",
        action="store_true",
        help=(
            "Print reasoning-control state."
        ),
    )

    group.add_argument(
        "--check-gui",
        action="store_true",
        help=(
            "Verify GTK support without "
            "opening a window."
        ),
    )

    args = parser.parse_args()

    if args.status:
        print_status()
        return 0

    if args.check_gui:
        check_gui()
        return 0

    menu_mode = (
        "baseline"
        if args.baseline
        else "temporary"
    )

    return run_gui(
        menu_mode
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
