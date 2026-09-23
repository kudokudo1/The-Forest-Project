"""Canonical Phase 14.11L benchmark records."""

from __future__ import annotations

import json
import os

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(
    frozen=True,
    slots=True,
)
class BenchmarkTrial:
    """One immutable benchmark observation."""

    schema_version: int

    run_id: str
    phase: str
    scenario: str
    trial: int

    recorded_at_utc: str
    prompt_id: str

    execution_context_id: str
    binding_id: str

    model_form: str
    reasoning_mode: str
    workshop: str | None

    session_mode: str
    residency_mode: str
    persistence: bool

    status: str

    total_turn_ns: int | None = None
    forest_pre_runtime_ns: int | None = None
    runtime_interval_ns: int | None = None
    forest_post_runtime_ns: int | None = None

    response_chars: int | None = None
    exclusion_reason: str | None = None

    notes: tuple[str, ...] = ()

    def __post_init__(
        self,
    ) -> None:
        if self.schema_version != 1:
            raise ValueError(
                "Unsupported benchmark schema version."
            )

        text_fields = (
            "run_id",
            "phase",
            "scenario",
            "recorded_at_utc",
            "prompt_id",
            "execution_context_id",
            "binding_id",
            "model_form",
            "reasoning_mode",
            "session_mode",
            "residency_mode",
            "status",
        )

        for field_name in text_fields:
            value = getattr(
                self,
                field_name,
            )

            if (
                not isinstance(value, str)
                or not value.strip()
            ):
                raise ValueError(
                    f"{field_name} must be "
                    "a non-empty string."
                )

        if (
            not isinstance(self.trial, int)
            or self.trial < 1
        ):
            raise ValueError(
                "trial must be an integer >= 1."
            )

        if self.workshop is not None:
            if (
                not isinstance(
                    self.workshop,
                    str,
                )
                or not self.workshop.strip()
            ):
                raise ValueError(
                    "workshop must be None or "
                    "a non-empty string."
                )

        timing_fields = (
            "total_turn_ns",
            "forest_pre_runtime_ns",
            "runtime_interval_ns",
            "forest_post_runtime_ns",
        )

        for field_name in timing_fields:
            value = getattr(
                self,
                field_name,
            )

            if value is not None:
                if (
                    not isinstance(value, int)
                    or value < 0
                ):
                    raise ValueError(
                        f"{field_name} must be "
                        "None or a non-negative integer."
                    )

        if self.response_chars is not None:
            if (
                not isinstance(
                    self.response_chars,
                    int,
                )
                or self.response_chars < 0
            ):
                raise ValueError(
                    "response_chars must be None "
                    "or a non-negative integer."
                )

        if self.exclusion_reason is not None:
            if (
                not isinstance(
                    self.exclusion_reason,
                    str,
                )
                or not self.exclusion_reason.strip()
            ):
                raise ValueError(
                    "exclusion_reason must be "
                    "None or non-empty."
                )

        if not isinstance(
            self.notes,
            tuple,
        ):
            raise TypeError(
                "notes must be a tuple."
            )

        for note in self.notes:
            if (
                not isinstance(note, str)
                or not note.strip()
            ):
                raise ValueError(
                    "notes must contain only "
                    "non-empty strings."
                )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """Return JSON-serializable record data."""

        data = asdict(self)

        data["notes"] = list(
            self.notes
        )

        return data


def append_jsonl(
    path: str | Path,
    trial: BenchmarkTrial,
) -> None:
    """Append exactly one trial as one JSON line.

    This write should occur outside the measured
    turn interval.

    fsync is intentional so a completed benchmark
    observation is durable after the call returns.
    """

    if not isinstance(
        trial,
        BenchmarkTrial,
    ):
        raise TypeError(
            "trial must be BenchmarkTrial."
        )

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = json.dumps(
        trial.to_dict(),
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


def read_jsonl(
    path: str | Path,
) -> tuple[dict[str, Any], ...]:
    """Read canonical benchmark JSONL records."""

    path = Path(path)

    records = []

    with path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        for line_number, line in enumerate(
            handle,
            start=1,
        ):
            line = line.strip()

            if not line:
                continue

            try:
                value = json.loads(line)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Invalid benchmark JSONL at "
                    f"line {line_number}."
                ) from exc

            if not isinstance(
                value,
                dict,
            ):
                raise ValueError(
                    "Benchmark JSONL records "
                    "must be JSON objects."
                )

            records.append(value)

    return tuple(records)
