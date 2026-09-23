"""Phase 14.11L.1 Forest control-path benchmark.

Executable benchmark harness.

Uses:
- production TaskSession control path
- production Small binding registry
- deterministic FakeRuntimeAdapter
- RecordingGovernor("approve")
- persist=False
- no real Hermes inference
- no model loading
"""

from __future__ import annotations

import importlib.util
import json
import math
import statistics
import sys

from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter_ns


ROOT = Path("/home/user/The-Forest")
B = ROOT / "bristlecone"

sys.path.insert(
    0,
    str(B),
)

from benchmarks.environment import (  # noqa: E402
    capture_environment,
)
from benchmarks.records import (  # noqa: E402
    BenchmarkTrial,
    append_jsonl,
)


FIXTURE_FILE = (
    B
    / "tests"
    / "test_model_form_governor_task_session_integration.py"
)

OUTPUT = (
    B
    / "benchmarks"
    / "phase14_11L"
    / "l1_control_path.jsonl"
)

SUMMARY = (
    B
    / "benchmarks"
    / "phase14_11L"
    / "l1_control_path_summary.json"
)

WARMUPS = 5
MEASURED = 20

MESSAGE = "L.1 control-path benchmark fixture"
INSTRUCTIONS = "L.1 fixed benchmark instruction"


def load_fixture():
    spec = (
        importlib.util.spec_from_file_location(
            "forest_l1_fixture",
            FIXTURE_FILE,
        )
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load L.1 fixture."
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    return module


fixture = load_fixture()


def utc_now():
    return (
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


def percentile_nearest_rank(
    values,
    percentile,
):
    ordered = sorted(values)

    rank = math.ceil(
        percentile
        * len(ordered)
    )

    index = max(
        0,
        rank - 1,
    )

    return ordered[index]


def summarize(
    values,
):
    return {
        "n": len(values),
        "median_ns":
            int(statistics.median(values)),
        "mean_ns":
            statistics.mean(values),
        "min_ns":
            min(values),
        "max_ns":
            max(values),
        "stdev_ns":
            (
                statistics.stdev(values)
                if len(values) > 1
                else 0.0
            ),
        "p90_ns":
            percentile_nearest_rank(
                values,
                0.90,
            ),
    }


def assert_idle_environment(
    environment,
    label,
):
    if environment.ollama_resident_models:
        raise RuntimeError(
            f"{label}: model unexpectedly resident."
        )

    if environment.llama_server_pids:
        raise RuntimeError(
            f"{label}: llama-server unexpectedly active."
        )

    if environment.runtime_socket_lines:
        raise RuntimeError(
            f"{label}: runtime socket unexpectedly active."
        )


def send_one(
    manager,
    *,
    governor,
    task_id,
    execution_context_id,
    explicit_small,
):
    kwargs = {
        "state":
            fixture.active_state(
                task_id
            ),

        "instructions":
            INSTRUCTIONS,

        "reasoning_mode":
            "normal",

        "persist":
            False,

        "execution_context_id":
            execution_context_id,

        "automatic_model_form_evidence":
            (),

        "resource_governor":
            governor,

        "resource_priority":
            "standard",

        "resource_request_source":
            "l1-control-path-benchmark",

        "resource_request_reasons":
            (
                "performance_measurement",
            ),

        "resource_may_defer":
            True,
    }

    if explicit_small:
        kwargs["model_form"] = "small"

    return manager.send_runtime_turn(
        MESSAGE,
        **kwargs,
    )


def router_preflight():
    """Prove explicit and Auto paths differ as intended."""

    import model_form.automatic_routing_policy as policy

    original = (
        policy.recommend_automatic_model_form
    )

    calls = []

    def counted(value):
        calls.append(value)
        return original(value)

    policy.recommend_automatic_model_form = counted

    try:
        # Explicit Small must bypass automatic routing.
        with fixture.manager_fixture() as (
            manager,
            adapter,
        ):
            governor = (
                fixture.RecordingGovernor(
                    "approve"
                )
            )

            send_one(
                manager,
                governor=governor,
                task_id="task-l1-preflight-explicit",
                execution_context_id=
                    "ctx-l1-preflight-explicit",
                explicit_small=True,
            )

            if calls:
                raise RuntimeError(
                    "Explicit Small unexpectedly "
                    "called automatic router."
                )

            if len(governor.requests) != 1:
                raise RuntimeError(
                    "Explicit preflight Governor mismatch."
                )

            if (
                governor.requests[0].model_form
                != "small"
            ):
                raise RuntimeError(
                    "Explicit Small did not remain Small."
                )

        # Auto path must invoke router exactly once.
        with fixture.manager_fixture() as (
            manager,
            adapter,
        ):
            governor = (
                fixture.RecordingGovernor(
                    "approve"
                )
            )

            before = len(calls)

            send_one(
                manager,
                governor=governor,
                task_id="task-l1-preflight-auto",
                execution_context_id=
                    "ctx-l1-preflight-auto",
                explicit_small=False,
            )

            after = len(calls)

            if after - before != 1:
                raise RuntimeError(
                    "Automatic Small preflight did not "
                    "route exactly once."
                )

            if len(governor.requests) != 1:
                raise RuntimeError(
                    "Auto preflight Governor mismatch."
                )

            if (
                governor.requests[0].model_form
                != "small"
            ):
                raise RuntimeError(
                    "Automatic route did not resolve Small."
                )

    finally:
        policy.recommend_automatic_model_form = (
            original
        )


def run_series(
    *,
    scenario,
    explicit_small,
):
    measured = []

    with fixture.manager_fixture() as (
        manager,
        adapter,
    ):
        if (
            type(adapter).__name__
            != "FakeRuntimeAdapter"
        ):
            raise RuntimeError(
                "L.1 requires FakeRuntimeAdapter."
            )

        total_trials = (
            WARMUPS
            + MEASURED
        )

        for index in range(
            1,
            total_trials + 1,
        ):
            is_warmup = (
                index <= WARMUPS
            )

            measured_trial = (
                index - WARMUPS
            )

            task_id = (
                f"task-l1-{scenario}-{index:03d}"
            )

            execution_context_id = (
                f"ctx-l1-{scenario}-{index:03d}"
            )

            governor = (
                fixture.RecordingGovernor(
                    "approve"
                )
            )

            before_create = len(
                adapter.create_calls
            )

            before_send = len(
                adapter.send_calls
            )

            before_end = len(
                adapter.end_calls
            )

            # -------------------------------
            # MEASURED INTERVAL
            # -------------------------------
            start_ns = perf_counter_ns()

            result = send_one(
                manager,
                governor=governor,
                task_id=task_id,
                execution_context_id=
                    execution_context_id,
                explicit_small=
                    explicit_small,
            )

            end_ns = perf_counter_ns()
            # -------------------------------
            # END MEASURED INTERVAL
            # -------------------------------

            elapsed_ns = (
                end_ns - start_ns
            )

            if len(governor.requests) != 1:
                raise RuntimeError(
                    "Governor request count mismatch."
                )

            request = governor.requests[0]

            if request.model_form != "small":
                raise RuntimeError(
                    "Measured turn did not remain Small."
                )

            if request.reasoning_mode != "normal":
                raise RuntimeError(
                    "Measured Reasoning changed."
                )

            if (
                request.execution_context_id
                != execution_context_id
            ):
                raise RuntimeError(
                    "Execution context changed."
                )

            if request.task_id != task_id:
                raise RuntimeError(
                    "Task identity changed."
                )

            if (
                len(adapter.create_calls)
                != before_create + 1
            ):
                raise RuntimeError(
                    "Expected one fake session creation."
                )

            if (
                len(adapter.send_calls)
                != before_send + 1
            ):
                raise RuntimeError(
                    "Expected one fake send."
                )

            if (
                len(adapter.end_calls)
                != before_end
            ):
                raise RuntimeError(
                    "Unexpected fake session end."
                )

            if not isinstance(
                result,
                dict,
            ):
                raise RuntimeError(
                    "Unexpected runtime result."
                )

            if is_warmup:
                continue

            measured.append(
                elapsed_ns
            )

            trial = BenchmarkTrial(
                schema_version=1,

                run_id=(
                    f"L1-{scenario}-"
                    f"{measured_trial:03d}"
                ),

                phase="14.11L.1",

                scenario=scenario,

                trial=measured_trial,

                recorded_at_utc=
                    utc_now(),

                prompt_id=
                    "L1-control-path-v1",

                execution_context_id=
                    execution_context_id,

                binding_id=
                    "binding-0001",

                model_form="small",

                reasoning_mode="normal",

                workshop=None,

                session_mode=
                    "new-fake-session",

                residency_mode=
                    "fake-runtime-no-model",

                persistence=False,

                status="measured",

                total_turn_ns=
                    elapsed_ns,

                notes=(
                    "fake-runtime",
                    "governor-approve",
                    (
                        "explicit-small"
                        if explicit_small
                        else "automatic-small"
                    ),
                ),
            )

            append_jsonl(
                OUTPUT,
                trial,
            )

    return summarize(
        measured
    )


def main():
    if OUTPUT.exists():
        raise RuntimeError(
            "L.1 output already exists; "
            "refusing to append duplicate series."
        )

    if SUMMARY.exists():
        raise RuntimeError(
            "L.1 summary already exists."
        )

    before = capture_environment()

    assert_idle_environment(
        before,
        "before benchmark",
    )

    router_preflight()

    explicit = run_series(
        scenario="explicit_small",
        explicit_small=True,
    )

    automatic = run_series(
        scenario="automatic_small",
        explicit_small=False,
    )

    after = capture_environment()

    assert_idle_environment(
        after,
        "after benchmark",
    )

    summary = {
        "schema_version": 1,
        "phase": "14.11L.1",
        "prompt_id": "L1-control-path-v1",
        "warmups_per_series": WARMUPS,
        "measured_per_series": MEASURED,

        "explicit_small":
            explicit,

        "automatic_small":
            automatic,

        "median_delta_ns":
            (
                automatic["median_ns"]
                - explicit["median_ns"]
            ),

        "environment_before":
            before.to_dict(),

        "environment_after":
            after.to_dict(),

        "safety": {
            "runtime_adapter":
                "FakeRuntimeAdapter",
            "real_inference":
                False,
            "model_load":
                False,
            "big_execution":
                False,
            "persistence":
                False,
        },
    }

    SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== 14.11L.1 CONTROL-PATH RESULT ==="
    )

    print()
    print(
        "Explicit Small:",
        json.dumps(
            explicit,
            indent=2,
            sort_keys=True,
        ),
    )

    print()
    print(
        "Automatic Small:",
        json.dumps(
            automatic,
            indent=2,
            sort_keys=True,
        ),
    )

    print()
    print(
        "Median automatic - explicit delta (ns):",
        summary["median_delta_ns"],
    )

    print()
    print(
        "JSONL records:",
        len(
            OUTPUT.read_text(
                encoding="utf-8"
            ).splitlines()
        ),
    )

    print(
        "Real inference:",
        False,
    )

    print(
        "Big execution:",
        False,
    )

    print()
    print(
        "L.1 benchmark status: 0"
    )


if __name__ == "__main__":
    main()
