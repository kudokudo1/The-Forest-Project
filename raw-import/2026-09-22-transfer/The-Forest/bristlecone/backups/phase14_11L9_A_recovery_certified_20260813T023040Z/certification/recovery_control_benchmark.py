from __future__ import annotations

import hashlib
import importlib.util
import json
import statistics
import time
from pathlib import Path


ROOT = Path(
    "/home/user/The-Forest/bristlecone"
)

TEST_SOURCE = (
    ROOT
    / "tests"
    / "test_model_form_retry_task_session_integration.py"
)

OUTPUT = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
    / "l9_recovery_control_raw.json"
)

PAIRS = 500
WARMUP_PAIRS = 20
CLASSIFIER_ITERATIONS = 10_000


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def stats(values):
    require(
        values,
        "Cannot summarize empty timing list",
    )

    ordered = sorted(values)
    count = len(ordered)

    p95_index = min(
        count - 1,
        max(
            0,
            (95 * count + 99) // 100 - 1,
        ),
    )

    return {
        "count":
            count,
        "median_ns":
            statistics.median(ordered),
        "mean_ns":
            statistics.mean(ordered),
        "stdev_ns":
            (
                statistics.stdev(ordered)
                if count > 1
                else 0.0
            ),
        "min_ns":
            ordered[0],
        "max_ns":
            ordered[-1],
        "p95_ns":
            ordered[p95_index],
        "median_us":
            statistics.median(ordered)
            / 1_000,
        "mean_us":
            statistics.mean(ordered)
            / 1_000,
    }


def clear_adapter_history(adapter):
    for name in (
        "create_calls",
        "send_calls",
        "classifier_calls",
        "end_calls",
    ):
        value = getattr(
            adapter,
            name,
            None,
        )

        if isinstance(value, list):
            value.clear()


def load_retry_module():
    spec = (
        importlib.util.spec_from_file_location(
            "phase14_11L9_retry_scaffold",
            TEST_SOURCE,
        )
    )

    require(
        spec is not None
        and spec.loader is not None,
        "Could not load retry integration test module",
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


require(
    TEST_SOURCE.exists(),
    f"Missing retry scaffold: {TEST_SOURCE}",
)

require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing artifact: "
        f"{OUTPUT}"
    ),
)


retry = load_retry_module()


# ============================================================
# DIRECT STALE CLASSIFIER COST
# ============================================================

print(
    "=== L.9A STALE CLASSIFIER ==="
)

with retry.manager_fixture() as (
    manager,
    adapter,
):
    stale_exc = (
        retry.SyntheticStaleSessionError(
            "L.9 classifier stale"
        )
    )

    nonstale_exc = (
        retry.SyntheticRuntimeFailure(
            "L.9 classifier nonstale"
        )
    )

    classifier_stale_ns = []
    classifier_nonstale_ns = []

    for _ in range(
        CLASSIFIER_ITERATIONS
    ):
        start = time.perf_counter_ns()

        classified = (
            adapter.is_stale_session_error(
                stale_exc
            )
        )

        end = time.perf_counter_ns()

        require(
            classified is True,
            "Stale classifier rejected stale exception",
        )

        classifier_stale_ns.append(
            end - start
        )

    for _ in range(
        CLASSIFIER_ITERATIONS
    ):
        start = time.perf_counter_ns()

        classified = (
            adapter.is_stale_session_error(
                nonstale_exc
            )
        )

        end = time.perf_counter_ns()

        require(
            classified is False,
            "Stale classifier accepted non-stale exception",
        )

        classifier_nonstale_ns.append(
            end - start
        )


classifier_stale_stats = stats(
    classifier_stale_ns
)

classifier_nonstale_stats = stats(
    classifier_nonstale_ns
)

print(
    "PASS stale classifier median:",
    f"{classifier_stale_stats['median_us']:.3f} us",
)

print(
    "PASS non-stale classifier median:",
    f"{classifier_nonstale_stats['median_us']:.3f} us",
)


# ============================================================
# RECOVERY CONTROL-PATH BENCHMARK
#
# Both measurements use a fresh Forest state for the turn.
#
# Normal:
#   create initial fake session
#   send succeeds
#
# Recovery:
#   create initial fake session
#   first send reports stale
#   classify stale
#   create replacement
#   retry succeeds
#
# Therefore paired delta isolates the additional recovery work
# as closely as practical while still executing production
# TaskSession recovery logic.
# ============================================================

print()
print(
    "=== L.9A RECOVERY CONTROL PATH ==="
)

normal_ns = []
recovery_ns = []
paired_delta_ns = []


with retry.manager_fixture() as (
    manager,
    adapter,
):

    def execute_normal(index, prefix):
        adapter.outcomes = [
            "ok",
        ]

        before_create = len(
            adapter.create_calls
        )

        before_send = len(
            adapter.send_calls
        )

        before_classifier = len(
            adapter.classifier_calls
        )

        start = time.perf_counter_ns()

        result = retry.send_turn(
            manager,
            task_id=(
                f"{prefix}-normal-task-{index}"
            ),
            context_id=(
                f"{prefix}-normal-ctx-{index}"
            ),
            reasoning_mode="normal",
            evidence=(),
        )

        end = time.perf_counter_ns()

        new_creates = (
            adapter.create_calls[
                before_create:
            ]
        )

        new_sends = (
            adapter.send_calls[
                before_send:
            ]
        )

        classifier_count = (
            len(adapter.classifier_calls)
            - before_classifier
        )

        require(
            len(new_creates) == 1,
            (
                "Normal control did not create "
                "exactly one initial session"
            ),
        )

        require(
            len(new_sends) == 1,
            (
                "Normal control did not send "
                "exactly once"
            ),
        )

        require(
            classifier_count == 0,
            (
                "Normal control unexpectedly "
                "classified an error"
            ),
        )

        require(
            result.get(
                "session_recovered",
                False,
            )
            is False,
            (
                "Normal control unexpectedly "
                "reports recovery"
            ),
        )

        require(
            new_sends[0]["session_id"]
            == new_creates[0]["session_id"],
            (
                "Normal send did not use "
                "created session"
            ),
        )

        return end - start


    def execute_recovery(index, prefix):
        adapter.outcomes = [
            "stale",
            "ok",
        ]

        before_create = len(
            adapter.create_calls
        )

        before_send = len(
            adapter.send_calls
        )

        before_classifier = len(
            adapter.classifier_calls
        )

        start = time.perf_counter_ns()

        result = retry.send_turn(
            manager,
            task_id=(
                f"{prefix}-recovery-task-{index}"
            ),
            context_id=(
                f"{prefix}-recovery-ctx-{index}"
            ),
            reasoning_mode="normal",
            evidence=(),
        )

        end = time.perf_counter_ns()

        new_creates = (
            adapter.create_calls[
                before_create:
            ]
        )

        new_sends = (
            adapter.send_calls[
                before_send:
            ]
        )

        classifier_count = (
            len(adapter.classifier_calls)
            - before_classifier
        )

        require(
            len(new_creates) == 2,
            (
                "Recovery path did not create "
                "initial + replacement sessions"
            ),
        )

        require(
            len(new_sends) == 2,
            (
                "Recovery path did not perform "
                "initial send + one retry"
            ),
        )

        require(
            classifier_count == 1,
            (
                "Recovery path did not classify "
                "exactly one stale exception"
            ),
        )

        stale_session_id = (
            new_sends[0][
                "session_id"
            ]
        )

        replacement_session_id = (
            new_sends[1][
                "session_id"
            ]
        )

        require(
            stale_session_id
            == new_creates[0][
                "session_id"
            ],
            (
                "Initial stale send used "
                "unexpected session"
            ),
        )

        require(
            replacement_session_id
            == new_creates[1][
                "session_id"
            ],
            (
                "Retry did not use replacement "
                "session"
            ),
        )

        require(
            stale_session_id
            != replacement_session_id,
            (
                "Recovery failed to rotate "
                "session identity"
            ),
        )

        require(
            result.get(
                "session_recovered"
            )
            is True,
            (
                "Successful recovery did not "
                "report session_recovered=True"
            ),
        )

        require(
            result.get(
                "session_id"
            )
            == replacement_session_id,
            (
                "Recovered result does not "
                "use replacement session"
            ),
        )

        return end - start


    # --------------------------------------------------------
    # Unmeasured warmup
    # --------------------------------------------------------

    print(
        "Running unmeasured warmup...",
        flush=True,
    )

    for index in range(
        WARMUP_PAIRS
    ):
        execute_normal(
            index,
            "warmup",
        )

        execute_recovery(
            index,
            "warmup",
        )


    clear_adapter_history(
        adapter
    )


    # --------------------------------------------------------
    # Measured paired run
    #
    # Alternate ordering to reduce systematic order bias.
    # --------------------------------------------------------

    print(
        f"Running {PAIRS} measured pairs...",
        flush=True,
    )

    for index in range(PAIRS):
        if index % 2 == 0:
            normal_value = (
                execute_normal(
                    index,
                    "measured",
                )
            )

            recovery_value = (
                execute_recovery(
                    index,
                    "measured",
                )
            )

        else:
            recovery_value = (
                execute_recovery(
                    index,
                    "measured",
                )
            )

            normal_value = (
                execute_normal(
                    index,
                    "measured",
                )
            )

        normal_ns.append(
            normal_value
        )

        recovery_ns.append(
            recovery_value
        )

        paired_delta_ns.append(
            recovery_value
            - normal_value
        )


normal_stats = stats(
    normal_ns
)

recovery_stats = stats(
    recovery_ns
)

delta_stats = stats(
    paired_delta_ns
)


print()
print(
    "PASS normal control median:",
    f"{normal_stats['median_us']:.3f} us",
)

print(
    "PASS recovery control median:",
    f"{recovery_stats['median_us']:.3f} us",
)

print(
    "Paired recovery overhead median:",
    f"{delta_stats['median_us']:.3f} us",
)

print(
    "Recovery slower pairs:",
    sum(
        value > 0
        for value in paired_delta_ns
    ),
    "/",
    PAIRS,
)


# ============================================================
# L.9B — ONE-RETRY ENFORCEMENT
# ============================================================

print()
print(
    "=== L.9B ONE-RETRY ENFORCEMENT ==="
)


# ------------------------------------------------------------
# stale -> stale
# ------------------------------------------------------------

with retry.manager_fixture(
    outcomes=(
        "stale",
        "stale",
    ),
    include_big=True,
) as (
    manager,
    adapter,
):
    caught_second_stale = False

    try:
        retry.send_turn(
            manager,
            task_id=(
                "l9-second-stale-task"
            ),
            context_id=(
                "l9-second-stale-ctx"
            ),
            reasoning_mode="normal",
            evidence=(),
        )

    except (
        retry.SyntheticStaleSessionError
    ):
        caught_second_stale = True


    require(
        caught_second_stale,
        (
            "Second stale error did not "
            "escape recovery"
        ),
    )

    require(
        len(adapter.create_calls) == 2,
        (
            "Second-stale case created "
            "more than one replacement"
        ),
    )

    require(
        len(adapter.send_calls) == 2,
        (
            "Second-stale case performed "
            "more than one retry"
        ),
    )

    require(
        len(adapter.classifier_calls) == 1,
        (
            "Second stale error was "
            "classified into another cycle"
        ),
    )


print(
    "PASS stale -> stale escapes "
    "after exactly one retry"
)


# ------------------------------------------------------------
# stale -> ordinary runtime failure
# ------------------------------------------------------------

with retry.manager_fixture(
    outcomes=(
        "stale",
        "fail",
    ),
    include_big=True,
) as (
    manager,
    adapter,
):
    caught_runtime_failure = False

    try:
        retry.send_turn(
            manager,
            task_id=(
                "l9-retry-failure-task"
            ),
            context_id=(
                "l9-retry-failure-ctx"
            ),
            reasoning_mode="normal",
            evidence=(),
        )

    except (
        retry.SyntheticRuntimeFailure
    ):
        caught_runtime_failure = True


    require(
        caught_runtime_failure,
        (
            "Retry runtime failure did "
            "not escape"
        ),
    )

    require(
        len(adapter.create_calls) == 2,
        (
            "Retry-failure case created "
            "more than one replacement"
        ),
    )

    require(
        len(adapter.send_calls) == 2,
        (
            "Retry-failure case performed "
            "more than one retry"
        ),
    )

    require(
        len(adapter.classifier_calls) == 1,
        (
            "Retry failure entered another "
            "classification cycle"
        ),
    )


print(
    "PASS stale -> failure escapes "
    "after exactly one retry"
)


# ============================================================
# FREEZE RAW EVIDENCE
# ============================================================

payload = {
    "phase":
        "14.11L.9",
    "scenarios": [
        "stale-classifier-performance",
        "recovery-control-performance",
        "one-retry-enforcement",
    ],
    "model_inference_executed":
        False,
    "real_runtime_used":
        False,
    "production_task_session_logic_used":
        True,
    "persistent_production_state_modified":
        False,
    "warmup_pairs":
        WARMUP_PAIRS,
    "measured_pairs":
        PAIRS,
    "classifier_iterations":
        CLASSIFIER_ITERATIONS,

    # Raw timing samples are intentionally retained beginning
    # with L.9 so independent certification can recompute
    # every statistic from first principles.
    "classifier": {
        "stale": {
            "timings_ns":
                classifier_stale_ns,
            "stats":
                classifier_stale_stats,
        },
        "nonstale": {
            "timings_ns":
                classifier_nonstale_ns,
            "stats":
                classifier_nonstale_stats,
        },
    },

    "normal_control": {
        "timings_ns":
            normal_ns,
        "stats":
            normal_stats,
    },

    "recovery_control": {
        "timings_ns":
            recovery_ns,
        "stats":
            recovery_stats,
    },

    "paired_recovery_overhead": {
        "timings_ns":
            paired_delta_ns,
        "stats":
            delta_stats,
        "recovery_slower_pairs":
            sum(
                value > 0
                for value
                in paired_delta_ns
            ),
    },

    "one_retry_enforcement": {
        "stale_then_stale": {
            "second_error_escaped":
                True,
            "session_creations":
                2,
            "send_calls":
                2,
            "classifier_calls":
                1,
        },
        "stale_then_runtime_failure": {
            "second_error_escaped":
                True,
            "session_creations":
                2,
            "send_calls":
                2,
            "classifier_calls":
                1,
        },
    },

    "source_sha256": {
        "task_session":
            sha256(
                ROOT
                / "runtime"
                / "task_session.py"
            ),
        "retry_test_scaffold":
            sha256(
                TEST_SOURCE
            ),
    },

    "status":
        "success",
}


OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print()
print(
    "=== L.9A/B RESULT ==="
)

print(
    "Normal control median:",
    f"{normal_stats['median_us']:.3f} us",
)

print(
    "Recovery control median:",
    f"{recovery_stats['median_us']:.3f} us",
)

print(
    "Paired recovery overhead median:",
    f"{delta_stats['median_us']:.3f} us",
)

print(
    "Raw timing samples retained:",
    len(normal_ns),
    "normal +",
    len(recovery_ns),
    "recovery",
)

print(
    "Inference executed: False"
)

print(
    "Persistent production modified: False"
)

print()
print("Evidence:")
print(OUTPUT)

print()
print("Evidence SHA256:")
print(
    sha256(OUTPUT)
)

print()
print(
    "PHASE 14.11L.9 A/B CONTROL BENCHMARK: PASS"
)
