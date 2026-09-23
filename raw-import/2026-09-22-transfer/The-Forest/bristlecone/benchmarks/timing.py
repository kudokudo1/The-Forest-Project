"""Monotonic benchmark timing primitives.

This module measures elapsed time only.

It deliberately contains no Forest runtime, Hermes,
Ollama, model, TaskSession, or persistence behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable


class BenchmarkTimingError(ValueError):
    """Raised when a benchmark timeline is invalid."""


@dataclass(
    frozen=True,
    slots=True,
)
class TimelineMark:
    """One named monotonic timestamp."""

    label: str
    timestamp_ns: int


class MonotonicTimeline:
    """Record named monotonic timing boundaries."""

    def __init__(
        self,
        *,
        clock: Callable[[], int] = perf_counter_ns,
    ):
        if not callable(clock):
            raise TypeError(
                "clock must be callable."
            )

        self._clock = clock
        self._marks: dict[str, int] = {}
        self._order: list[str] = []

    def mark(
        self,
        label: str,
    ) -> int:
        """Record one unique timing boundary."""

        if not isinstance(label, str):
            raise TypeError(
                "label must be a string."
            )

        label = label.strip()

        if not label:
            raise BenchmarkTimingError(
                "label must not be empty."
            )

        if label in self._marks:
            raise BenchmarkTimingError(
                f"Timing mark already exists: {label}"
            )

        timestamp_ns = self._clock()

        if not isinstance(timestamp_ns, int):
            raise TypeError(
                "clock must return integer nanoseconds."
            )

        if self._order:
            previous = self._marks[
                self._order[-1]
            ]

            if timestamp_ns < previous:
                raise BenchmarkTimingError(
                    "Benchmark clock moved backwards."
                )

        self._marks[label] = timestamp_ns
        self._order.append(label)

        return timestamp_ns

    def timestamp_ns(
        self,
        label: str,
    ) -> int:
        """Return one recorded timestamp."""

        try:
            return self._marks[label]

        except KeyError as exc:
            raise BenchmarkTimingError(
                f"Unknown timing mark: {label}"
            ) from exc

    def duration_ns(
        self,
        start: str,
        end: str,
    ) -> int:
        """Return elapsed nanoseconds between marks."""

        start_ns = self.timestamp_ns(start)
        end_ns = self.timestamp_ns(end)

        if end_ns < start_ns:
            raise BenchmarkTimingError(
                "End mark precedes start mark."
            )

        return end_ns - start_ns

    def freeze(
        self,
    ) -> tuple[TimelineMark, ...]:
        """Return an immutable ordered snapshot."""

        return tuple(
            TimelineMark(
                label=label,
                timestamp_ns=self._marks[label],
            )
            for label in self._order
        )
