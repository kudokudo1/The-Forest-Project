"""Phase 14.11L benchmark baseline records.

A baseline observes benchmark conditions only.

It does not:
- submit Forest turns
- create runtime sessions
- invoke Hermes inference
- load/unload Ollama models
- change Forest state
"""

from __future__ import annotations

import hashlib
import json
import os

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .environment import (
    BenchmarkEnvironment,
    capture_environment,
)


ROOT = Path("/home/user/The-Forest")
BRISTLECONE = ROOT / "bristlecone"

METHODOLOGY = (
    BRISTLECONE
    / "benchmarks/phase14_11L/METHODOLOGY.md"
)

ACTIVE_STATE = (
    BRISTLECONE
    / "state/active.yaml"
)

PRODUCTION_FILES = (
    "bristlecone/runtime/task_session.py",
    "bristlecone/runtime/session_store.py",
    "bristlecone/runtime/session_identity.py",
    "bristlecone/runtime/adapters/hermes.py",
    "bristlecone/resources/live_providers.py",
    "bristlecone/model_form/bindings.yaml",
)


def sha256_file(
    path: str | Path,
) -> str:
    """Return SHA256 for one file."""

    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


@dataclass(
    frozen=True,
    slots=True,
)
class BenchmarkBaseline:
    """One immutable L benchmark baseline."""

    schema_version: int
    record_type: str
    phase: str

    recorded_at_utc: str

    methodology_sha256: str
    active_yaml_sha256: str

    production_sha256: dict[str, str]

    environment: dict[str, Any]

    model_form_under_test: str
    binding_under_test: str

    big_execution_allowed: bool

    notes: tuple[str, ...]

    def __post_init__(
        self,
    ) -> None:
        if self.schema_version != 1:
            raise ValueError(
                "Unsupported baseline schema version."
            )

        if self.record_type != "benchmark_baseline":
            raise ValueError(
                "Invalid baseline record_type."
            )

        if self.phase != "14.11L.0":
            raise ValueError(
                "Invalid baseline phase."
            )

        if self.big_execution_allowed:
            raise ValueError(
                "Phase L baseline must not authorize Big."
            )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """Return JSON-serializable baseline."""

        value = asdict(self)

        value["notes"] = list(
            self.notes
        )

        return value


def capture_baseline(
) -> BenchmarkBaseline:
    """Capture one passive L.0 benchmark baseline."""

    environment: BenchmarkEnvironment = (
        capture_environment()
    )

    production_sha256 = {
        relative: sha256_file(
            ROOT / relative
        )
        for relative in PRODUCTION_FILES
    }

    return BenchmarkBaseline(
        schema_version=1,
        record_type="benchmark_baseline",
        phase="14.11L.0",

        recorded_at_utc=
            environment.recorded_at_utc,

        methodology_sha256=
            sha256_file(
                METHODOLOGY
            ),

        active_yaml_sha256=
            sha256_file(
                ACTIVE_STATE
            ),

        production_sha256=
            production_sha256,

        environment=
            environment.to_dict(),

        model_form_under_test=
            "small",

        binding_under_test=
            "binding-0001",

        big_execution_allowed=
            False,

        notes=(
            "passive-environment-baseline",
            "no-runtime-turn",
            "no-model-load",
            "big-execution-forbidden",
        ),
    )


def write_baseline_jsonl(
    path: str | Path,
    baseline: BenchmarkBaseline,
) -> None:
    """Append one durable baseline JSON record."""

    if not isinstance(
        baseline,
        BenchmarkBaseline,
    ):
        raise TypeError(
            "baseline must be BenchmarkBaseline."
        )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = json.dumps(
        baseline.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
    )

    with path.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(payload)
        handle.write("\n")
        handle.flush()
        os.fsync(
            handle.fileno()
        )
