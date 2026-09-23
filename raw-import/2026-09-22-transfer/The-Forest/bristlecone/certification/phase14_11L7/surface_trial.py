from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import time
from pathlib import Path

from runtime.task_session import TaskSessionManager
from resources.live_providers import (
    build_live_small_resource_governor,
)


ROOT = Path("/home/user/The-Forest/bristlecone")

BENCH = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
)

ACTIVE = (
    ROOT
    / "state"
    / "active.yaml"
)

EXPECTED_ACTIVE_SHA = (
    "6b8fb9b44757917c1889a7368d43f393"
    "165080d248cdb3d9c5982aad53b270e5"
)

MODEL = "bristlecone-qwen35:4b-64k"

MESSAGE = "Reply only with: L2-COLD-01"

BASE_TOOLSETS = [
    "file",
    "terminal",
]

SURFACES = {
    "a": {
        "label": "baseline",
        "ready": [],
        "temporary_toolsets": [],
        "runtime_skills": [],
        "canonical_skills": [],
    },

    "b": {
        "label": "tool",
        "ready": [
            "code-execution",
        ],
        "temporary_toolsets": [
            "code_execution",
        ],
        "runtime_skills": [],
        "canonical_skills": [],
    },

    "c": {
        "label": "skill",
        "ready": [
            "debugging",
        ],
        "temporary_toolsets": [],
        "runtime_skills": [
            "systematic-debugging",
        ],
        "canonical_skills": [
            "debugging",
        ],
    },

    "d": {
        "label": "full",
        "ready": [
            "code-execution",
            "debugging",
            "testing",
        ],
        "temporary_toolsets": [
            "code_execution",
        ],
        "runtime_skills": [
            "systematic-debugging",
            "test-driven-development",
        ],
        "canonical_skills": [
            "debugging",
            "testing",
        ],
    },
}


def sha256(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def ollama_ps():
    completed = subprocess.run(
        [
            "ollama",
            "ps",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    return completed.stdout


def resident_lines(raw):
    lines = [
        line.strip()
        for line in raw.splitlines()
        if line.strip()
    ]

    if (
        lines
        and lines[0].startswith("NAME")
    ):
        lines = lines[1:]

    return lines


def unique_strings(values):
    result = []

    for value in values:
        value = str(value)

        if value not in result:
            result.append(value)

    return result


def same_members(actual, expected):
    actual = unique_strings(actual)
    expected = unique_strings(expected)

    return (
        len(actual) == len(expected)
        and set(actual) == set(expected)
    )


def write_json(path, payload):
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


parser = argparse.ArgumentParser()

parser.add_argument(
    "--surface",
    required=True,
    choices=sorted(SURFACES),
)

parser.add_argument(
    "--trial",
    required=True,
    type=int,
    choices=range(1, 6),
)

args = parser.parse_args()

surface = args.surface
trial = args.trial
spec = SURFACES[surface]

context = (
    f"ctx-l7-{surface}-{trial:02d}"
)

output = (
    BENCH
    / (
        f"l7_surface_{surface}_"
        f"trial{trial}_raw.json"
    )
)

BENCH.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# FAIL CLOSED ON DUPLICATE
# --------------------------------------------------

if output.exists():
    raise RuntimeError(
        f"Evidence already exists: {output}"
    )


# --------------------------------------------------
# FROZEN STATE
# --------------------------------------------------

active_before = sha256(ACTIVE)

if active_before != EXPECTED_ACTIVE_SHA:
    raise RuntimeError(
        "active.yaml changed before L.7 trial."
    )


# --------------------------------------------------
# WARM SMALL PRECONDITION
# --------------------------------------------------

resident_before = resident_lines(
    ollama_ps()
)

print(
    f"=== L.7 SURFACE {surface.upper()} "
    f"({spec['label'].upper()}) — "
    f"TRIAL {trial} ==="
)

print()
print(
    "Resident before:",
    resident_before,
)

if (
    len(resident_before) != 1
    or MODEL not in resident_before[0]
):
    raise RuntimeError(
        "Warm Small residency precondition failed."
    )


# --------------------------------------------------
# FROZEN SOURCE STATE + NEUTRAL BENCHMARK VIEW
# --------------------------------------------------

manager = TaskSessionManager(
    forest_root=ROOT,
)

configured_state = manager.load_state()

if configured_state.get(
    "workshop"
) != "code-debug":
    raise RuntimeError(
        "L.7 requires persistent "
        "Workshop code-debug."
    )

persistent_general = list(
    configured_state.get(
        "active_general",
        [],
    )
    or []
)

persistent_ready = list(
    configured_state.get(
        "active_ready",
        [],
    )
    or []
)

persistent_task = configured_state.get(
    "task_session",
    {},
)

if not isinstance(
    persistent_task,
    dict,
):
    raise RuntimeError(
        "Persistent task_session is not a mapping."
    )

persistent_sticky_skills = list(
    persistent_task.get(
        "task_sticky_skills",
        [],
    )
    or []
)

if persistent_general:
    raise RuntimeError(
        "L.7 frozen source unexpectedly has "
        "active General Ready capabilities."
    )

if persistent_ready != ["debugging"]:
    raise RuntimeError(
        "L.7 frozen source Ready state changed: "
        f"{persistent_ready}"
    )

if persistent_sticky_skills != ["debugging"]:
    raise RuntimeError(
        "L.7 frozen source sticky Skills changed: "
        f"{persistent_sticky_skills}"
    )

runtime_adapter = (
    manager._runtime_adapter_for_state(
        configured_state
    )
)

if (
    getattr(
        runtime_adapter,
        "adapter_name",
        None,
    )
    != "hermes"
):
    raise RuntimeError(
        "L.7 requires Hermes runtime adapter."
    )

base_toolsets_before = list(
    runtime_adapter.get_active_toolsets(
        configured_state
    )
)

if not same_members(
    base_toolsets_before,
    BASE_TOOLSETS,
):
    raise RuntimeError(
        "L.7 live Hermes baseline is not "
        "exactly file + terminal: "
        f"{base_toolsets_before}"
    )


# --------------------------------------------------
# BENCHMARK-ONLY NEUTRAL EXECUTION VIEW
#
# Do not modify persistent Forest state.
#
# The frozen source intentionally carries:
#   active_ready = ["debugging"]
#   task_sticky_skills = ["debugging"]
#
# L.7 needs A/B/C/D to differ only by the
# measured temporary surface, so neutralize those
# two fields in an in-memory persist=False copy.
# --------------------------------------------------

benchmark_source_state = copy.deepcopy(
    configured_state
)

benchmark_source_state[
    "active_ready"
] = []

benchmark_task = benchmark_source_state.get(
    "task_session"
)

if not isinstance(
    benchmark_task,
    dict,
):
    raise RuntimeError(
        "Benchmark task_session is not a mapping."
    )

benchmark_task[
    "task_sticky_skills"
] = []

benchmark_task[
    "temporary_capabilities"
] = []


# --------------------------------------------------
# FRESH TASK / CONTEXT / SESSION
# --------------------------------------------------

started = manager.start_task(
    state=benchmark_source_state,
    persist=False,
)

state = started["state"]

task_session = started[
    "task_session"
]

task_id = task_session["id"]

if list(
    state.get(
        "active_ready",
        [],
    )
    or []
):
    raise RuntimeError(
        "Neutral L.7 execution view unexpectedly "
        "retained active_ready."
    )

if task_session.get(
    "task_sticky_skills",
    [],
):
    raise RuntimeError(
        "Neutral L.7 Task unexpectedly retained "
        "Task-sticky Skills."
    )

if task_session.get(
    "temporary_capabilities",
    [],
):
    raise RuntimeError(
        "Fresh L.7 Task unexpectedly already "
        "contains temporary capabilities."
    )

governor = (
    build_live_small_resource_governor()
)

print("Task:", task_id)
print("Context:", context)
print("Workshop: code-debug")
print(
    "Frozen source Ready:",
    persistent_ready,
)
print(
    "Frozen source sticky Skills:",
    persistent_sticky_skills,
)
print(
    "Benchmark Ready: []"
)
print(
    "Benchmark sticky Skills: []"
)
print("Surface:", surface)
print("Ready:", spec["ready"])
print("Reasoning: normal")
print("Expected Hermes effort: medium")

print()
print(
    "Entering temporary surface...",
    flush=True,
)


# --------------------------------------------------
# TEMPORARY SURFACE + MEASURED TURN
# --------------------------------------------------

enter_start_ns = time.perf_counter_ns()

with manager.temporary_turn(
    spec["ready"],
    state=state,
    task_session=task_session,
) as temporary:

    enter_end_ns = time.perf_counter_ns()

    plan = temporary["plan"]
    overlay = temporary["overlay"]

    plan_toolsets = list(
        plan.get(
            "runtime_toolsets",
            [],
        )
    )

    skill_bindings = list(
        plan.get(
            "skill_bindings",
            [],
        )
    )

    overlay_runtime_skills = list(
        overlay.get(
            "runtime_skills",
            [],
        )
    )

    overlay_canonical_skills = list(
        overlay.get(
            "canonical_skills",
            [],
        )
    )

    overlay_prompt = (
        overlay.get(
            "prompt",
            "",
        )
        or ""
    )

    overlay_hash = overlay.get(
        "overlay_hash"
    )

    overlay_bytes = len(
        overlay_prompt.encode(
            "utf-8"
        )
    )

    # ----------------------------------------------
    # EXACT TEMPORARY PLAN
    # ----------------------------------------------

    if plan.get(
        "workshop"
    ) != "code-debug":
        raise RuntimeError(
            "Temporary plan changed Workshop."
        )

    if not same_members(
        plan_toolsets,
        spec["temporary_toolsets"],
    ):
        raise RuntimeError(
            "Unexpected temporary toolset plan: "
            f"{plan_toolsets}"
        )

    if not same_members(
        overlay_runtime_skills,
        spec["runtime_skills"],
    ):
        raise RuntimeError(
            "Unexpected runtime Skill overlay: "
            f"{overlay_runtime_skills}"
        )

    if not same_members(
        overlay_canonical_skills,
        spec["canonical_skills"],
    ):
        raise RuntimeError(
            "Unexpected canonical Skill overlay: "
            f"{overlay_canonical_skills}"
        )

    if spec["runtime_skills"]:
        if not overlay_prompt:
            raise RuntimeError(
                "Skill surface produced empty prompt."
            )

        if not overlay_hash:
            raise RuntimeError(
                "Skill surface produced no overlay hash."
            )

    else:
        if overlay_prompt:
            raise RuntimeError(
                "Non-Skill surface unexpectedly "
                "produced Skill prompt."
            )

        if overlay_hash is not None:
            raise RuntimeError(
                "Non-Skill surface unexpectedly "
                "produced overlay hash."
            )

    expected_bindings = {
        canonical: runtime
        for canonical, runtime
        in zip(
            spec["canonical_skills"],
            spec["runtime_skills"],
        )
    }

    actual_bindings = {}

    for binding in skill_bindings:
        canonical = binding.get(
            "canonical_id"
        )

        runtime_id = binding.get(
            "runtime_id"
        )

        adapter_name = binding.get(
            "adapter"
        )

        if adapter_name != "hermes":
            raise RuntimeError(
                "Skill binding adapter changed."
            )

        actual_bindings[
            canonical
        ] = runtime_id

    if actual_bindings != expected_bindings:
        raise RuntimeError(
            "Unexpected Skill bindings: "
            f"{actual_bindings}"
        )

    # ----------------------------------------------
    # VERIFY ACTUAL HERMES TOOL SURFACE
    # ----------------------------------------------

    expected_during_toolsets = (
        BASE_TOOLSETS
        + spec[
            "temporary_toolsets"
        ]
    )

    toolsets_during = list(
        runtime_adapter.get_active_toolsets(
            state
        )
    )

    if not same_members(
        toolsets_during,
        expected_during_toolsets,
    ):
        raise RuntimeError(
            "Actual Hermes temporary surface "
            "does not match expectation: "
            f"{toolsets_during}"
        )

    print(
        "Temporary toolsets:",
        plan_toolsets,
    )

    print(
        "Runtime Skills:",
        overlay_runtime_skills,
    )

    print(
        "Skill overlay bytes:",
        overlay_bytes,
    )

    print()
    print(
        "Starting timed runtime turn...",
        flush=True,
    )

    turn_start_ns = time.perf_counter_ns()

    result = manager.send_runtime_turn(
        MESSAGE,
        state=state,

        instructions=(
            overlay_prompt
            if overlay_prompt
            else None
        ),

        reasoning_mode="normal",
        persist=False,
        execution_context_id=context,
        model_form="small",

        resource_governor=governor,
        resource_priority="standard",

        resource_request_source=(
            "phase14_11L7-surface"
        ),

        resource_request_reasons=(
            (
                f"L.7 surface "
                f"{surface.upper()} benchmark"
            ),
        ),

        resource_may_defer=False,
    )

    turn_end_ns = time.perf_counter_ns()

    toolsets_after_turn_before_exit = list(
        runtime_adapter.get_active_toolsets(
            state
        )
    )

    if not same_members(
        toolsets_after_turn_before_exit,
        expected_during_toolsets,
    ):
        raise RuntimeError(
            "Temporary tool surface changed "
            "during measured turn."
        )

    exit_start_ns = time.perf_counter_ns()


exit_end_ns = time.perf_counter_ns()


# --------------------------------------------------
# VERIFY TRANSACTION RESTORATION
# --------------------------------------------------

toolsets_after_restore = list(
    runtime_adapter.get_active_toolsets(
        state
    )
)

if not same_members(
    toolsets_after_restore,
    BASE_TOOLSETS,
):
    raise RuntimeError(
        "Temporary toolsets were not restored: "
        f"{toolsets_after_restore}"
    )


# --------------------------------------------------
# ASSERT RUNTIME SEMANTICS
# --------------------------------------------------

session_id = result.get(
    "session_id"
)

result_reasoning = result.get(
    "reasoning_mode"
)

if result_reasoning is None:
    result_reasoning = result.get(
        "resolved_reasoning_mode"
    )

if result_reasoning is None:
    result_reasoning = result.get(
        "reasoning"
    )

checks = {
    "context":
        result.get(
            "execution_context_id"
        ) == context,

    "session_exists":
        isinstance(
            session_id,
            str,
        )
        and bool(
            session_id.strip()
        ),

    "session_created":
        result.get(
            "session_created"
        ) is True,

    "session_not_reused":
        result.get(
            "session_reused"
        ) is False,

    "session_not_recovered":
        result.get(
            "session_recovered"
        ) is False,

    "binding":
        result.get(
            "binding_id"
        ) == "binding-0001",

    "model_form":
        result.get(
            "model_form"
        ) == "small",
}

if result_reasoning is not None:
    checks[
        "reasoning"
    ] = (
        result_reasoning
        == "normal"
    )

failed_checks = [
    name
    for name, passed
    in checks.items()
    if not passed
]

if failed_checks:
    raise RuntimeError(
        "L.7 runtime semantic checks failed: "
        + ", ".join(
            failed_checks
        )
    )


# --------------------------------------------------
# POST-RUNTIME EVIDENCE
# --------------------------------------------------

resident_after = resident_lines(
    ollama_ps()
)

if (
    len(resident_after) != 1
    or MODEL not in resident_after[0]
):
    raise RuntimeError(
        "Small was not resident after "
        "measured L.7 turn."
    )

active_after = sha256(ACTIVE)

if active_after != active_before:
    raise RuntimeError(
        "active.yaml changed during L.7 trial."
    )


# --------------------------------------------------
# TIMINGS
# --------------------------------------------------

activation_enter_ns = (
    enter_end_ns
    - enter_start_ns
)

turn_duration_ns = (
    turn_end_ns
    - turn_start_ns
)

activation_exit_ns = (
    exit_end_ns
    - exit_start_ns
)

surface_cycle_ns = (
    activation_enter_ns
    + turn_duration_ns
    + activation_exit_ns
)


# --------------------------------------------------
# RAW ARTIFACT
# --------------------------------------------------

payload = {
    "phase":
        "14.11L.7",

    "scenario":
        "warm-small-controlled-tool-skill-surface",

    "surface":
        surface,

    "surface_label":
        spec["label"],

    "trial":
        trial,

    "workshop":
        "code-debug",

    "persistent_source_active_ready":
        persistent_ready,

    "persistent_source_task_sticky_skills":
        persistent_sticky_skills,

    "benchmark_neutral_active_ready":
        [],

    "benchmark_neutral_task_sticky_skills":
        [],

    "ready":
        list(
            spec["ready"]
        ),

    "message":
        MESSAGE,

    "task_id":
        task_id,

    "execution_context_id":
        context,

    "session_id":
        session_id,

    "session_created":
        result.get(
            "session_created"
        ),

    "session_reused":
        result.get(
            "session_reused"
        ),

    "session_recovered":
        result.get(
            "session_recovered"
        ),

    "binding_id":
        result.get(
            "binding_id"
        ),

    "model_form":
        result.get(
            "model_form"
        ),

    "requested_reasoning_mode":
        "normal",

    "result_reasoning_mode":
        result_reasoning,

    "expected_hermes_reasoning_effort":
        "medium",

    "persist":
        False,

    "base_toolsets":
        BASE_TOOLSETS,

    "temporary_toolsets":
        plan_toolsets,

    "toolsets_during":
        toolsets_during,

    "toolsets_after_turn_before_exit":
        toolsets_after_turn_before_exit,

    "toolsets_after_restore":
        toolsets_after_restore,

    "toolset_count_during":
        len(
            unique_strings(
                toolsets_during
            )
        ),

    "canonical_skills":
        overlay_canonical_skills,

    "runtime_skills":
        overlay_runtime_skills,

    "skill_count":
        len(
            overlay_runtime_skills
        ),

    "skill_bindings":
        skill_bindings,

    "skill_overlay_bytes":
        overlay_bytes,

    "skill_overlay_hash":
        overlay_hash,

    "skill_overlay_cache_hit":
        (
            overlay.get(
                "temporary",
                {}
            ).get(
                "cache_hit"
            )
            if isinstance(
                overlay.get(
                    "temporary"
                ),
                dict,
            )
            else None
        ),

    "activation_enter_ns":
        activation_enter_ns,

    "activation_enter_s":
        (
            activation_enter_ns
            / 1_000_000_000
        ),

    "turn_duration_ns":
        turn_duration_ns,

    "turn_duration_s":
        (
            turn_duration_ns
            / 1_000_000_000
        ),

    "activation_exit_ns":
        activation_exit_ns,

    "activation_exit_s":
        (
            activation_exit_ns
            / 1_000_000_000
        ),

    "surface_cycle_ns":
        surface_cycle_ns,

    "surface_cycle_s":
        (
            surface_cycle_ns
            / 1_000_000_000
        ),

    "resident_before":
        resident_before,

    "resident_after":
        resident_after,

    "active_yaml_sha":
        active_after,

    "cleanup_performed":
        False,

    "status":
        "success",
}

write_json(
    output,
    payload,
)


print()
print(
    f"=== L.7 SURFACE "
    f"{surface.upper()} "
    f"TRIAL {trial} RESULT ==="
)

print()
print(
    "Activation enter s:",
    payload[
        "activation_enter_s"
    ],
)

print(
    "Turn duration s:",
    payload[
        "turn_duration_s"
    ],
)

print(
    "Activation exit s:",
    payload[
        "activation_exit_s"
    ],
)

print(
    "Session:",
    session_id,
)

print(
    "session_created:",
    result.get(
        "session_created"
    ),
)

print(
    "session_reused:",
    result.get(
        "session_reused"
    ),
)

print(
    "session_recovered:",
    result.get(
        "session_recovered"
    ),
)

print(
    "binding:",
    result.get(
        "binding_id"
    ),
)

print(
    "model_form:",
    result.get(
        "model_form"
    ),
)

print(
    "reasoning:",
    result_reasoning,
)

print(
    "toolsets during:",
    toolsets_during,
)

print(
    "runtime Skills:",
    overlay_runtime_skills,
)

print(
    "Skill overlay bytes:",
    overlay_bytes,
)

print()
print(
    "Cleanup performed: False"
)

print(
    "Evidence:",
    output,
)

print()
print(
    f"L.7 Surface "
    f"{surface.upper()} "
    f"Trial {trial} status: 0"
)
