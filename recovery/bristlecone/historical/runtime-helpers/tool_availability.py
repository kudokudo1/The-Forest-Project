"""Forest-native tool availability provider.

This module is intentionally DORMANT by default.

While Hermes owns runtime tool availability, this provider
must not probe tools or maintain a competing availability
cache.

The provider exists as the Forest-native replacement path
for runtimes that do not supply equivalent availability
caching.

Architecture:

    capability exists
        ↓
    shared infrastructure availability
        ↓
    Tree / Clone permission evaluation
        ↓
    Spirit resource arbitration when required

Infrastructure availability is deliberately Clone-neutral.
Clone-specific authorization belongs above this layer.

Availability state is volatile runtime truth, not durable
Forest knowledge. It is therefore memory-only and TTL-based.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import (
    Condition,
    RLock,
)
from typing import (
    Callable,
    Dict,
    Hashable,
    Optional,
    Protocol,
    Tuple,
)
import time


DEFAULT_AVAILABILITY_TTL_SECONDS = 30.0


class ToolAvailabilityError(
    RuntimeError
):
    """Base error for tool availability providers."""


class ToolAvailabilityProviderInactive(
    ToolAvailabilityError
):
    """Raised when the dormant Forest provider is used."""


class ToolAvailabilityProbeError(
    ToolAvailabilityError
):
    """Raised when a tool probe returns invalid state."""


@dataclass(
    frozen=True
)
class AvailabilityContext:
    """Infrastructure context that can change availability.

    Clone identity is intentionally absent.

    If two Clones use the same capability through the same
    runtime and Soil/environment generation, they may reuse
    the same infrastructure availability result.
    """

    capability_id: str
    runtime_id: str
    environment_id: str
    environment_generation: Optional[Hashable] = None

    def __post_init__(
        self,
    ):
        for name in (
            "capability_id",
            "runtime_id",
            "environment_id",
        ):
            value = getattr(
                self,
                name,
            )

            if (
                not isinstance(
                    value,
                    str,
                )
                or not value.strip()
            ):
                raise ToolAvailabilityError(
                    f"{name} must be a "
                    "non-empty string."
                )

        generation = (
            self.environment_generation
        )

        if generation is not None:
            try:
                hash(
                    generation
                )

            except TypeError as exc:
                raise ToolAvailabilityError(
                    "environment_generation "
                    "must be hashable."
                ) from exc


@dataclass(
    frozen=True
)
class AvailabilityResult:
    """Result returned to availability callers."""

    available: bool
    from_cache: bool


@dataclass
class _AvailabilityEntry:
    """Internal volatile TTL entry."""

    available: bool
    expires_at: float


class ToolAvailabilityProvider(
    Protocol
):
    """Provider contract for runtime availability."""

    def check(
        self,
        context: AvailabilityContext,
        probe: Callable[[], bool],
    ) -> AvailabilityResult:
        ...


class ForestToolAvailabilityProvider:
    """Shared, Clone-compatible Forest TTL provider.

    The provider starts disabled.

    Important properties:

    - memory-only
    - short TTL
    - no disk persistence
    - no Tree/Clone identity in cache key
    - concurrent callers for the same key share one probe
    - different capability/environment keys may probe
      independently
    """

    def __init__(
        self,
        *,
        ttl_seconds=(
            DEFAULT_AVAILABILITY_TTL_SECONDS
        ),
        enabled=False,
        clock=None,
    ):
        if (
            isinstance(
                ttl_seconds,
                bool,
            )
            or not isinstance(
                ttl_seconds,
                (
                    int,
                    float,
                ),
            )
            or ttl_seconds < 0
        ):
            raise ToolAvailabilityError(
                "ttl_seconds must be >= 0."
            )

        self._ttl_seconds = float(
            ttl_seconds
        )

        self._enabled = bool(
            enabled
        )

        self._clock = (
            clock
            or time.monotonic
        )

        self._entries: Dict[
            AvailabilityContext,
            _AvailabilityEntry,
        ] = {}

        self._inflight = set()

        self._lock = RLock()

        self._condition = Condition(
            self._lock
        )


    @property
    def enabled(
        self,
    ):
        return self._enabled


    @property
    def ttl_seconds(
        self,
    ):
        return self._ttl_seconds


    def set_enabled(
        self,
        enabled,
    ):
        """Activate or dormantly disable this provider.

        Disabling clears volatile entries so a later runtime
        switch cannot revive stale availability state.
        """

        enabled = bool(
            enabled
        )

        with self._condition:
            if not enabled:
                self._entries.clear()

            self._enabled = enabled

            self._condition.notify_all()


    def _require_enabled(
        self,
    ):
        if not self._enabled:
            raise ToolAvailabilityProviderInactive(
                "Forest tool availability provider "
                "is dormant."
            )


    def _cached_result_unlocked(
        self,
        context,
        now,
    ):
        entry = self._entries.get(
            context
        )

        if entry is None:
            return None

        if (
            entry.expires_at
            <= now
        ):
            self._entries.pop(
                context,
                None,
            )

            return None

        return AvailabilityResult(
            available=entry.available,
            from_cache=True,
        )


    def check(
        self,
        context,
        probe,
    ):
        """Return infrastructure availability.

        For one cache key, concurrent callers coordinate so
        only one caller performs the underlying probe.
        """

        if not isinstance(
            context,
            AvailabilityContext,
        ):
            raise ToolAvailabilityError(
                "context must be "
                "AvailabilityContext."
            )

        if not callable(
            probe
        ):
            raise ToolAvailabilityError(
                "probe must be callable."
            )

        with self._condition:
            self._require_enabled()

            while True:
                now = self._clock()

                cached = (
                    self._cached_result_unlocked(
                        context,
                        now,
                    )
                )

                if cached is not None:
                    return cached

                if (
                    context
                    not in self._inflight
                ):
                    self._inflight.add(
                        context
                    )

                    break

                self._condition.wait()

                self._require_enabled()


        # Perform the potentially slow probe outside the
        # provider lock. Other capability/environment keys
        # remain free to probe concurrently.
        try:
            available = probe()

            if not isinstance(
                available,
                bool,
            ):
                raise ToolAvailabilityProbeError(
                    "Availability probe must return bool."
                )

        except Exception:
            with self._condition:
                self._inflight.discard(
                    context
                )

                self._condition.notify_all()

            raise


        with self._condition:
            # Runtime policy may have disabled the provider
            # while the external probe was running.
            self._require_enabled()

            now = self._clock()

            self._entries[
                context
            ] = _AvailabilityEntry(
                available=available,
                expires_at=(
                    now
                    + self._ttl_seconds
                ),
            )

            self._inflight.discard(
                context
            )

            self._condition.notify_all()

            return AvailabilityResult(
                available=available,
                from_cache=False,
            )


    def invalidate(
        self,
        *,
        capability_id=None,
        runtime_id=None,
        environment_id=None,
    ):
        """Invalidate matching volatile entries."""

        with self._condition:
            removed = 0

            for context in list(
                self._entries
            ):
                if (
                    capability_id is not None
                    and context.capability_id
                    != capability_id
                ):
                    continue

                if (
                    runtime_id is not None
                    and context.runtime_id
                    != runtime_id
                ):
                    continue

                if (
                    environment_id is not None
                    and context.environment_id
                    != environment_id
                ):
                    continue

                self._entries.pop(
                    context,
                    None,
                )

                removed += 1

            return removed


    def clear(
        self,
    ):
        """Discard all derived availability state."""

        with self._condition:
            count = len(
                self._entries
            )

            self._entries.clear()

            return count


    def inspect(
        self,
    ):
        """Return metadata-only cache inspection."""

        with self._condition:
            now = self._clock()

            expired = [
                context
                for context, entry
                in self._entries.items()
                if entry.expires_at
                <= now
            ]

            for context in expired:
                self._entries.pop(
                    context,
                    None,
                )

            result = []

            for context, entry in sorted(
                self._entries.items(),
                key=lambda item: (
                    item[0].runtime_id,
                    item[0].environment_id,
                    item[0].capability_id,
                    repr(
                        item[0]
                        .environment_generation
                    ),
                ),
            ):
                result.append(
                    {
                        "capability_id": (
                            context.capability_id
                        ),
                        "runtime_id": (
                            context.runtime_id
                        ),
                        "environment_id": (
                            context.environment_id
                        ),
                        "environment_generation": (
                            context
                            .environment_generation
                        ),
                        "available": (
                            entry.available
                        ),
                        "ttl_remaining_seconds": max(
                            0.0,
                            (
                                entry.expires_at
                                - now
                            ),
                        ),
                    }
                )

            return tuple(
                result
            )
