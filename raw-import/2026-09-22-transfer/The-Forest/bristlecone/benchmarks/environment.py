"""Passive benchmark environment observation.

This module may inspect host/qube state.

It must not:
- start or stop services
- create runtime sessions
- submit Forest turns
- load or unload models
- mutate Forest state
"""

from __future__ import annotations

import os
import subprocess

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class BenchmarkEnvironment:
    """One immutable passive environment snapshot."""

    recorded_at_utc: str

    cpu_count: int | None
    mem_available_kib: int | None

    load_1m: float | None
    load_5m: float | None
    load_15m: float | None

    hermes_active_state: str | None
    hermes_sub_state: str | None
    hermes_main_pid: int | None

    ollama_resident_models: tuple[str, ...]

    llama_server_pids: tuple[int, ...]

    runtime_socket_lines: tuple[str, ...]

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """Return JSON-serializable snapshot data."""

        value = asdict(self)

        value[
            "ollama_resident_models"
        ] = list(
            self.ollama_resident_models
        )

        value[
            "llama_server_pids"
        ] = list(
            self.llama_server_pids
        )

        value[
            "runtime_socket_lines"
        ] = list(
            self.runtime_socket_lines
        )

        return value


def _run(
    *args: str,
) -> subprocess.CompletedProcess[str]:
    """Run one read-only inspection command."""

    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        check=False,
    )


def parse_mem_available_kib(
    text: str,
) -> int | None:
    """Parse MemAvailable from /proc/meminfo."""

    for line in text.splitlines():
        if not line.startswith(
            "MemAvailable:"
        ):
            continue

        pieces = line.split()

        if len(pieces) < 2:
            return None

        try:
            return int(
                pieces[1]
            )

        except ValueError:
            return None

    return None


def parse_systemctl_properties(
    text: str,
) -> dict[str, str]:
    """Parse systemctl show KEY=VALUE output."""

    values = {}

    for line in text.splitlines():
        if "=" not in line:
            continue

        key, value = line.split(
            "=",
            1,
        )

        values[key] = value

    return values


def parse_ollama_resident_models(
    text: str,
) -> tuple[str, ...]:
    """Return resident model names from ollama ps."""

    lines = [
        line
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return ()

    # First non-empty line is the column header.
    models = []

    for line in lines[1:]:
        pieces = line.split()

        if pieces:
            models.append(
                pieces[0]
            )

    return tuple(models)


def parse_llama_server_pids(
    text: str,
) -> tuple[int, ...]:
    """Parse llama-server PIDs from ps output."""

    pids = []

    for line in text.splitlines():
        if "llama-server" not in line:
            continue

        pieces = line.strip().split(
            maxsplit=1
        )

        if not pieces:
            continue

        try:
            pid = int(
                pieces[0]
            )

        except ValueError:
            continue

        pids.append(pid)

    return tuple(pids)


def capture_environment(
) -> BenchmarkEnvironment:
    """Capture one passive benchmark environment snapshot."""

    recorded_at_utc = (
        datetime.now(
            timezone.utc
        )
        .replace(
            microsecond=0
        )
        .isoformat()
        .replace(
            "+00:00",
            "Z",
        )
    )

    cpu_count = os.cpu_count()

    try:
        meminfo = Path(
            "/proc/meminfo"
        ).read_text(
            encoding="utf-8"
        )

    except OSError:
        mem_available_kib = None

    else:
        mem_available_kib = (
            parse_mem_available_kib(
                meminfo
            )
        )

    try:
        load_1m, load_5m, load_15m = (
            os.getloadavg()
        )

    except OSError:
        load_1m = None
        load_5m = None
        load_15m = None

    hermes = _run(
        "systemctl",
        "--user",
        "show",
        "hermes-bristlecone.service",
        "-p",
        "ActiveState",
        "-p",
        "SubState",
        "-p",
        "MainPID",
    )

    properties = (
        parse_systemctl_properties(
            hermes.stdout
        )
        if hermes.returncode == 0
        else {}
    )

    main_pid = None

    raw_pid = properties.get(
        "MainPID"
    )

    if raw_pid:
        try:
            parsed_pid = int(
                raw_pid
            )

        except ValueError:
            pass

        else:
            if parsed_pid > 0:
                main_pid = parsed_pid

    ollama = _run(
        "ollama",
        "ps",
    )

    resident_models = (
        parse_ollama_resident_models(
            ollama.stdout
        )
        if ollama.returncode == 0
        else ()
    )

    processes = _run(
        "ps",
        "-eo",
        "pid,args",
    )

    llama_server_pids = (
        parse_llama_server_pids(
            processes.stdout
        )
        if processes.returncode == 0
        else ()
    )

    sockets = _run(
        "ss",
        "-tnp",
    )

    runtime_socket_lines = ()

    if sockets.returncode == 0:
        runtime_socket_lines = tuple(
            line.strip()
            for line in sockets.stdout.splitlines()
            if (
                ":8643" in line
                or ":11434" in line
            )
        )

    return BenchmarkEnvironment(
        recorded_at_utc=
            recorded_at_utc,

        cpu_count=
            cpu_count,

        mem_available_kib=
            mem_available_kib,

        load_1m=
            load_1m,

        load_5m=
            load_5m,

        load_15m=
            load_15m,

        hermes_active_state=
            properties.get(
                "ActiveState"
            ),

        hermes_sub_state=
            properties.get(
                "SubState"
            ),

        hermes_main_pid=
            main_pid,

        ollama_resident_models=
            resident_models,

        llama_server_pids=
            llama_server_pids,

        runtime_socket_lines=
            runtime_socket_lines,
    )
