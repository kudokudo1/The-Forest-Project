"""Forest-owned human reasoning-control policy.

This module is runtime-neutral and contains no persistence I/O.
The Forest lifecycle/state layer owns durable commits.
"""

from dataclasses import dataclass
from typing import Optional
import uuid

from .model import (
    ReasoningModeError,
    normalize_reasoning_mode,
)

from .router import (
    ForestReasoningRouter,
)


REASONING_CONTROL_SCHEMA_VERSION = 1
DEFAULT_TEMPORARY_TURNS = 5


class ReasoningControlError(ValueError):
    """Invalid Forest reasoning-control state."""


def _positive_turn_count(
    value,
    *,
    field,
):
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < 1
    ):
        raise ReasoningControlError(
            f"{field} must be a positive integer."
        )

    return value


@dataclass(
    frozen=True,
    slots=True,
)
class ReasoningBaseline:
    policy: str = "auto"
    mode: Optional[str] = None

    def __post_init__(self):
        policy = str(
            self.policy
        ).strip().lower()

        if policy not in (
            "auto",
            "pinned",
        ):
            raise ReasoningControlError(
                "Baseline policy must be "
                "'auto' or 'pinned'."
            )

        object.__setattr__(
            self,
            "policy",
            policy,
        )

        if policy == "auto":
            if self.mode is not None:
                raise ReasoningControlError(
                    "Auto baseline cannot contain "
                    "a pinned mode."
                )

            return

        if self.mode is None:
            raise ReasoningControlError(
                "Pinned baseline requires a mode."
            )

        try:
            normalized = (
                normalize_reasoning_mode(
                    self.mode
                )
            )
        except ReasoningModeError as exc:
            raise ReasoningControlError(
                "Invalid pinned reasoning mode."
            ) from exc

        object.__setattr__(
            self,
            "mode",
            normalized,
        )


@dataclass(
    frozen=True,
    slots=True,
)
class TemporaryReasoningLease:
    """Temporary reasoning mode with unique lease identity."""

    lease_id: str
    mode: str
    turns_remaining: int

    def __post_init__(self):
        if not isinstance(
            self.lease_id,
            str,
        ):
            raise ReasoningControlError(
                "Temporary reasoning lease_id "
                "must be a string."
            )

        lease_id = (
            self.lease_id.strip()
        )

        if not lease_id:
            raise ReasoningControlError(
                "Temporary reasoning lease_id "
                "cannot be empty."
            )

        object.__setattr__(
            self,
            "lease_id",
            lease_id,
        )

        if self.mode is None:
            raise ReasoningControlError(
                "Temporary reasoning lease "
                "requires a mode."
            )

        try:
            normalized = (
                normalize_reasoning_mode(
                    self.mode
                )
            )

        except ReasoningModeError as exc:
            raise ReasoningControlError(
                "Invalid temporary reasoning mode."
            ) from exc

        object.__setattr__(
            self,
            "mode",
            normalized,
        )

        _positive_turn_count(
            self.turns_remaining,
            field="turns_remaining",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ReasoningControlSettings:
    temporary_turn_default: int = (
        DEFAULT_TEMPORARY_TURNS
    )

    def __post_init__(self):
        _positive_turn_count(
            self.temporary_turn_default,
            field="temporary_turn_default",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ReasoningControlState:
    baseline: ReasoningBaseline = (
        ReasoningBaseline()
    )

    temporary: Optional[
        TemporaryReasoningLease
    ] = None

    settings: ReasoningControlSettings = (
        ReasoningControlSettings()
    )

    schema_version: int = (
        REASONING_CONTROL_SCHEMA_VERSION
    )

    def __post_init__(self):
        if (
            self.schema_version
            != REASONING_CONTROL_SCHEMA_VERSION
        ):
            raise ReasoningControlError(
                "Unsupported reasoning-control "
                "schema version."
            )

        if not isinstance(
            self.baseline,
            ReasoningBaseline,
        ):
            raise ReasoningControlError(
                "baseline must be ReasoningBaseline."
            )

        if (
            self.temporary is not None
            and not isinstance(
                self.temporary,
                TemporaryReasoningLease,
            )
        ):
            raise ReasoningControlError(
                "temporary must be "
                "TemporaryReasoningLease or None."
            )

        if not isinstance(
            self.settings,
            ReasoningControlSettings,
        ):
            raise ReasoningControlError(
                "settings must be "
                "ReasoningControlSettings."
            )


@dataclass(
    frozen=True,
    slots=True,
)
class EffectiveReasoningDecision:
    """Frozen reasoning decision for one meaningful turn."""

    mode: str
    source: str
    consumes_temporary: bool = False
    temporary_lease_id: Optional[str] = None

    def __post_init__(self):
        object.__setattr__(
            self,
            "mode",
            normalize_reasoning_mode(
                self.mode
            ),
        )

        if self.source not in (
            "explicit",
            "temporary",
            "pinned",
            "automatic",
            "fallback",
        ):
            raise ReasoningControlError(
                "Invalid effective reasoning source."
            )

        if self.source == "temporary":
            if not self.consumes_temporary:
                raise ReasoningControlError(
                    "Temporary decision must be "
                    "marked consumable."
                )

            if not isinstance(
                self.temporary_lease_id,
                str,
            ):
                raise ReasoningControlError(
                    "Temporary decision requires "
                    "temporary_lease_id."
                )

            lease_id = (
                self.temporary_lease_id.strip()
            )

            if not lease_id:
                raise ReasoningControlError(
                    "temporary_lease_id cannot be empty."
                )

            object.__setattr__(
                self,
                "temporary_lease_id",
                lease_id,
            )

        else:
            if self.consumes_temporary:
                raise ReasoningControlError(
                    "Only a temporary decision may "
                    "consume a temporary lease."
                )

            if (
                self.temporary_lease_id
                is not None
            ):
                raise ReasoningControlError(
                    "Non-temporary decision cannot "
                    "contain temporary_lease_id."
                )


def _require_control(
    control,
):
    if not isinstance(
        control,
        ReasoningControlState,
    ):
        raise ReasoningControlError(
            "control must be "
            "ReasoningControlState."
        )


def default_reasoning_control():
    return ReasoningControlState()


def set_auto_baseline(
    control,
):
    """Clear pin while preserving a temporary lease."""

    _require_control(
        control
    )

    return ReasoningControlState(
        baseline=ReasoningBaseline(
            policy="auto",
            mode=None,
        ),
        temporary=control.temporary,
        settings=control.settings,
    )


def set_pinned_baseline(
    control,
    mode,
):
    """Change baseline without cancelling temporary work."""

    _require_control(
        control
    )

    return ReasoningControlState(
        baseline=ReasoningBaseline(
            policy="pinned",
            mode=mode,
        ),
        temporary=control.temporary,
        settings=control.settings,
    )


def set_temporary_mode(
    control,
    mode,
    *,
    turns=None,
):
    """Start or replace a temporary reasoning lease."""

    _require_control(
        control
    )

    if mode is None:
        raise ReasoningControlError(
            "Temporary reasoning mode "
            "cannot be None."
        )

    count = (
        control.settings.temporary_turn_default
        if turns is None
        else _positive_turn_count(
            turns,
            field="turns",
        )
    )

    return ReasoningControlState(
        baseline=control.baseline,

        temporary=TemporaryReasoningLease(
            lease_id=uuid.uuid4().hex,
            mode=mode,
            turns_remaining=count,
        ),

        settings=control.settings,
    )


def clear_temporary_mode(
    control,
):
    _require_control(
        control
    )

    return ReasoningControlState(
        baseline=control.baseline,
        temporary=None,
        settings=control.settings,
    )


def set_temporary_turn_default(
    control,
    turns,
):
    """Change future lease length without changing current lease."""

    _require_control(
        control
    )

    count = _positive_turn_count(
        turns,
        field="temporary_turn_default",
    )

    return ReasoningControlState(
        baseline=control.baseline,
        temporary=control.temporary,
        settings=ReasoningControlSettings(
            temporary_turn_default=count,
        ),
    )


def resolve_effective_reasoning(
    control,
    message,
    *,
    explicit_mode=None,
    router=None,
):
    """Resolve one meaningful turn without mutating state."""

    _require_control(
        control
    )

    if explicit_mode is not None:
        return EffectiveReasoningDecision(
            mode=normalize_reasoning_mode(
                explicit_mode
            ),
            source="explicit",
            consumes_temporary=False,
        )

    if control.temporary is not None:
        return EffectiveReasoningDecision(
            mode=control.temporary.mode,
            source="temporary",
            consumes_temporary=True,
            temporary_lease_id=(
                control.temporary.lease_id
            ),
        )

    if control.baseline.policy == "pinned":
        return EffectiveReasoningDecision(
            mode=control.baseline.mode,
            source="pinned",
            consumes_temporary=False,
        )

    selected_router = (
        router
        if router is not None
        else ForestReasoningRouter()
    )

    route = selected_router.decide(
        message
    )

    return EffectiveReasoningDecision(
        mode=route.mode,
        source="automatic",
        consumes_temporary=False,
    )


def consume_temporary_turn(
    control,
    decision,
):
    """Consume exactly one governed meaningful turn."""

    _require_control(
        control
    )

    if not isinstance(
        decision,
        EffectiveReasoningDecision,
    ):
        raise ReasoningControlError(
            "decision must be "
            "EffectiveReasoningDecision."
        )

    if not decision.consumes_temporary:
        return control

    lease = control.temporary

    if lease is None:
        raise ReasoningControlError(
            "Temporary consumption requested "
            "without an active lease."
        )

    if (
        decision.temporary_lease_id
        != lease.lease_id
    ):
        raise ReasoningControlError(
            "Temporary decision belongs to "
            "a different lease."
        )

    if decision.mode != lease.mode:
        raise ReasoningControlError(
            "Temporary decision does not "
            "match active lease mode."
        )

    remaining = (
        lease.turns_remaining - 1
    )

    if remaining == 0:
        return ReasoningControlState(
            baseline=control.baseline,
            temporary=None,
            settings=control.settings,
        )

    return ReasoningControlState(
        baseline=control.baseline,

        temporary=TemporaryReasoningLease(
            lease_id=lease.lease_id,
            mode=lease.mode,
            turns_remaining=remaining,
        ),

        settings=control.settings,
    )


def reasoning_control_to_mapping(
    control,
):
    """Return YAML-safe runtime-neutral durable representation."""

    _require_control(
        control
    )

    temporary = None

    if control.temporary is not None:
        temporary = {
            "lease_id":
                control.temporary.lease_id,

            "mode":
                control.temporary.mode,

            "turns_remaining":
                control.temporary.turns_remaining,
        }

    return {
        "schema_version":
            REASONING_CONTROL_SCHEMA_VERSION,

        "baseline": {
            "policy":
                control.baseline.policy,

            "mode":
                control.baseline.mode,
        },

        "temporary":
            temporary,

        "settings": {
            "temporary_turn_default":
                control.settings.temporary_turn_default,
        },
    }


def reasoning_control_from_mapping(
    value,
):
    """Load durable state.

    Missing/None means Auto baseline, no lease, default 5.
    """

    if value is None:
        return default_reasoning_control()

    if not isinstance(
        value,
        dict,
    ):
        raise ReasoningControlError(
            "reasoning_control must be a mapping."
        )

    schema_version = value.get(
        "schema_version",
        REASONING_CONTROL_SCHEMA_VERSION,
    )

    if (
        schema_version
        != REASONING_CONTROL_SCHEMA_VERSION
    ):
        raise ReasoningControlError(
            "Unsupported reasoning_control "
            "schema version."
        )

    baseline_raw = value.get(
        "baseline",
        {
            "policy": "auto",
            "mode": None,
        },
    )

    if not isinstance(
        baseline_raw,
        dict,
    ):
        raise ReasoningControlError(
            "reasoning_control.baseline "
            "must be a mapping."
        )

    baseline = ReasoningBaseline(
        policy=baseline_raw.get(
            "policy",
            "auto",
        ),

        mode=baseline_raw.get(
            "mode",
        ),
    )

    temporary_raw = value.get(
        "temporary"
    )

    temporary = None

    if temporary_raw is not None:
        if not isinstance(
            temporary_raw,
            dict,
        ):
            raise ReasoningControlError(
                "reasoning_control.temporary "
                "must be a mapping or null."
            )

        if (
            temporary_raw.get("mode")
            is None
        ):
            raise ReasoningControlError(
                "reasoning_control.temporary.mode "
                "is required."
            )

        if (
            temporary_raw.get("lease_id")
            is None
        ):
            raise ReasoningControlError(
                "reasoning_control.temporary.lease_id "
                "is required."
            )

        temporary = TemporaryReasoningLease(
            lease_id=temporary_raw.get(
                "lease_id"
            ),

            mode=temporary_raw.get(
                "mode"
            ),

            turns_remaining=temporary_raw.get(
                "turns_remaining"
            ),
        )

    settings_raw = value.get(
        "settings",
        {},
    )

    if not isinstance(
        settings_raw,
        dict,
    ):
        raise ReasoningControlError(
            "reasoning_control.settings "
            "must be a mapping."
        )

    settings = ReasoningControlSettings(
        temporary_turn_default=(
            settings_raw.get(
                "temporary_turn_default",
                DEFAULT_TEMPORARY_TURNS,
            )
        ),
    )

    return ReasoningControlState(
        baseline=baseline,
        temporary=temporary,
        settings=settings,
    )
