from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path


ROOT = Path("/home/user/The-Forest/bristlecone")
BENCH = ROOT / "benchmarks/phase14_11L"

HARNESS = (
    ROOT
    / "certification/phase14_11L7/surface_trial.py"
)

OUTPUT = (
    BENCH
    / "l7_surface_summary.json"
)

FROZEN_ACTIVE_SHA = (
    "6b8fb9b44757917c1889a7368d43f393"
    "165080d248cdb3d9c5982aad53b270e5"
)

MODEL = "bristlecone-qwen35:4b-64k"

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
        "toolsets_during": [
            "file",
            "terminal",
        ],
        "overlay_bytes": 0,
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
        "toolsets_during": [
            "code_execution",
            "file",
            "terminal",
        ],
        "overlay_bytes": 0,
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
        "toolsets_during": [
            "file",
            "terminal",
        ],
        "overlay_bytes": 14554,
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
        "toolsets_during": [
            "code_execution",
            "file",
            "terminal",
        ],
        "overlay_bytes": 25357,
    },
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def require(
    condition: bool,
    message: str,
) -> None:
    if not condition:
        raise RuntimeError(message)


def same_members(
    actual,
    expected,
) -> bool:
    return sorted(actual) == sorted(expected)


def stats(values):
    return {
        "count": len(values),
        "median_s": statistics.median(values),
        "mean_s": statistics.mean(values),
        "stdev_s": statistics.stdev(values),
        "min_s": min(values),
        "max_s": max(values),
    }


require(
    HARNESS.exists(),
    f"Missing L.7 harness: {HARNESS}",
)

require(
    not OUTPUT.exists(),
    f"Refusing to overwrite existing summary: {OUTPUT}",
)


records = []
raw_hashes = {}

seen_tasks = set()
seen_contexts = set()
seen_sessions = set()

common_phase = None
common_scenario = None
common_message = None


print("=== L.7 CERTIFICATION ANALYZER ===")
print()


for trial in range(1, 6):
    for surface in ("a", "b", "c", "d"):
        spec = SURFACES[surface]

        path = (
            BENCH
            / f"l7_surface_{surface}_trial{trial}_raw.json"
        )

        require(
            path.exists(),
            f"Missing raw artifact: {path.name}",
        )

        data = json.loads(
            path.read_text()
        )

        raw_hashes[path.name] = sha256_path(path)

        prefix = f"{surface.upper()}{trial}"

        require(
            data["surface"] == surface,
            f"{prefix}: wrong surface",
        )

        require(
            data["trial"] == trial,
            f"{prefix}: wrong trial",
        )

        require(
            data["workshop"] == "code-debug",
            f"{prefix}: wrong Workshop",
        )

        require(
            data["status"] == "success",
            f"{prefix}: status is not success",
        )

        require(
            data["model_form"] == "small",
            f"{prefix}: model form is not Small",
        )

        require(
            data["binding_id"] == "binding-0001",
            f"{prefix}: unexpected binding",
        )

        require(
            data["persist"] is False,
            f"{prefix}: persist is not False",
        )

        require(
            data["requested_reasoning_mode"] == "normal",
            f"{prefix}: requested reasoning is not Normal",
        )

        require(
            data["result_reasoning_mode"] == "normal",
            f"{prefix}: result reasoning is not Normal",
        )

        require(
            data["expected_hermes_reasoning_effort"] == "medium",
            f"{prefix}: Hermes effort is not medium",
        )

        require(
            data["session_created"] is True,
            f"{prefix}: session was not freshly created",
        )

        require(
            data["session_reused"] is False,
            f"{prefix}: session was reused",
        )

        require(
            data["session_recovered"] is False,
            f"{prefix}: session was recovered",
        )

        require(
            data["cleanup_performed"] is False,
            f"{prefix}: cleanup occurred inside measurement",
        )

        require(
            data["active_yaml_sha"] == FROZEN_ACTIVE_SHA,
            f"{prefix}: frozen active.yaml hash changed",
        )

        require(
            data["persistent_source_active_ready"]
            == ["debugging"],
            f"{prefix}: frozen Ready source changed",
        )

        require(
            data["persistent_source_task_sticky_skills"]
            == ["debugging"],
            f"{prefix}: frozen sticky Skills changed",
        )

        require(
            data["benchmark_neutral_active_ready"] == [],
            f"{prefix}: benchmark Ready view not neutral",
        )

        require(
            data["benchmark_neutral_task_sticky_skills"] == [],
            f"{prefix}: benchmark sticky view not neutral",
        )

        require(
            same_members(
                data["base_toolsets"],
                BASE_TOOLSETS,
            ),
            f"{prefix}: wrong base toolsets",
        )

        require(
            same_members(
                data["ready"],
                spec["ready"],
            ),
            f"{prefix}: wrong temporary Ready surface",
        )

        require(
            same_members(
                data["temporary_toolsets"],
                spec["temporary_toolsets"],
            ),
            f"{prefix}: wrong temporary toolsets",
        )

        require(
            same_members(
                data["runtime_skills"],
                spec["runtime_skills"],
            ),
            f"{prefix}: wrong runtime Skills",
        )

        require(
            same_members(
                data["canonical_skills"],
                spec["canonical_skills"],
            ),
            f"{prefix}: wrong canonical Skills",
        )

        require(
            same_members(
                data["toolsets_during"],
                spec["toolsets_during"],
            ),
            f"{prefix}: wrong live toolsets during turn",
        )

        require(
            same_members(
                data["toolsets_after_turn_before_exit"],
                spec["toolsets_during"],
            ),
            f"{prefix}: temporary toolsets changed during turn",
        )

        require(
            same_members(
                data["toolsets_after_restore"],
                BASE_TOOLSETS,
            ),
            f"{prefix}: toolsets were not restored",
        )

        require(
            data["toolset_count_during"]
            == len(spec["toolsets_during"]),
            f"{prefix}: wrong toolset count",
        )

        require(
            data["skill_count"]
            == len(spec["runtime_skills"]),
            f"{prefix}: wrong Skill count",
        )

        require(
            data["skill_overlay_bytes"]
            == spec["overlay_bytes"],
            f"{prefix}: wrong Skill overlay size",
        )

        if spec["overlay_bytes"] == 0:
            require(
                data["skill_overlay_hash"] is None,
                f"{prefix}: unexpected Skill overlay hash",
            )
        else:
            require(
                bool(data["skill_overlay_hash"]),
                f"{prefix}: missing Skill overlay hash",
            )

        require(
            data["skill_overlay_cache_hit"] is False,
            f"{prefix}: unexpected Skill overlay cache hit",
        )

        require(
            data["task_id"] not in seen_tasks,
            f"{prefix}: duplicate Task ID",
        )

        require(
            data["execution_context_id"] not in seen_contexts,
            f"{prefix}: duplicate execution context",
        )

        require(
            data["session_id"] not in seen_sessions,
            f"{prefix}: duplicate runtime session",
        )

        expected_context = (
            f"ctx-l7-{surface}-{trial:02d}"
        )

        require(
            data["execution_context_id"]
            == expected_context,
            f"{prefix}: unexpected execution context",
        )

        seen_tasks.add(
            data["task_id"]
        )
        seen_contexts.add(
            data["execution_context_id"]
        )
        seen_sessions.add(
            data["session_id"]
        )

        before_text = "\n".join(
            data["resident_before"]
        )

        after_text = "\n".join(
            data["resident_after"]
        )

        require(
            MODEL in before_text,
            f"{prefix}: Small was not warm before trial",
        )

        require(
            MODEL in after_text,
            f"{prefix}: Small was not resident after trial",
        )

        if common_phase is None:
            common_phase = data["phase"]
            common_scenario = data["scenario"]
            common_message = data["message"]
        else:
            require(
                data["phase"] == common_phase,
                f"{prefix}: phase changed",
            )
            require(
                data["scenario"] == common_scenario,
                f"{prefix}: scenario changed",
            )
            require(
                data["message"] == common_message,
                f"{prefix}: message changed",
            )

        records.append(
            {
                "surface": surface,
                "trial": trial,
                "turn_duration_s":
                    data["turn_duration_s"],
                "activation_enter_s":
                    data["activation_enter_s"],
                "activation_exit_s":
                    data["activation_exit_s"],
                "activation_overhead_s":
                    data["activation_enter_s"]
                    + data["activation_exit_s"],
                "surface_cycle_s":
                    data["surface_cycle_s"],
                "session_id":
                    data["session_id"],
                "task_id":
                    data["task_id"],
                "execution_context_id":
                    data["execution_context_id"],
                "skill_overlay_bytes":
                    data["skill_overlay_bytes"],
                "skill_overlay_hash":
                    data["skill_overlay_hash"],
                "skill_bindings":
                    data["skill_bindings"],
            }
        )

        print(
            f"PASS {prefix}: "
            f"{data['turn_duration_s']:.9f} s"
        )


require(
    len(records) == 20,
    "Expected exactly 20 certified records",
)


print()
print("20 / 20 semantic validations passed.")


by_surface = {
    surface: sorted(
        [
            record
            for record in records
            if record["surface"] == surface
        ],
        key=lambda record: record["trial"],
    )
    for surface in ("a", "b", "c", "d")
}


surface_stats = {}

for surface, surface_records in by_surface.items():
    turns = [
        record["turn_duration_s"]
        for record in surface_records
    ]

    enters = [
        record["activation_enter_s"]
        for record in surface_records
    ]

    exits = [
        record["activation_exit_s"]
        for record in surface_records
    ]

    overheads = [
        record["activation_overhead_s"]
        for record in surface_records
    ]

    surface_stats[surface] = {
        "label": SURFACES[surface]["label"],
        "turn": stats(turns),
        "activation_enter": stats(enters),
        "activation_exit": stats(exits),
        "activation_overhead": stats(overheads),
        "skill_overlay_bytes":
            SURFACES[surface]["overlay_bytes"],
        "runtime_skills":
            SURFACES[surface]["runtime_skills"],
        "temporary_toolsets":
            SURFACES[surface]["temporary_toolsets"],
    }


def paired(
    left: str,
    right: str,
):
    left_records = by_surface[left]
    right_records = by_surface[right]

    differences = []

    for l_record, r_record in zip(
        left_records,
        right_records,
    ):
        require(
            l_record["trial"] == r_record["trial"],
            f"Trial mismatch in {left}-{right}",
        )

        differences.append(
            l_record["turn_duration_s"]
            - r_record["turn_duration_s"]
        )

    return {
        "definition":
            f"{left.upper()} minus {right.upper()}",
        "differences_s": differences,
        "median_difference_s":
            statistics.median(differences),
        "mean_difference_s":
            statistics.mean(differences),
        "stdev_difference_s":
            statistics.stdev(differences),
        "left_slower_count":
            sum(
                value > 0
                for value in differences
            ),
        "left_faster_count":
            sum(
                value < 0
                for value in differences
            ),
        "ties":
            sum(
                value == 0
                for value in differences
            ),
    }


paired_stats = {
    "b_minus_a": paired("b", "a"),
    "c_minus_a": paired("c", "a"),
    "d_minus_a": paired("d", "a"),
    "d_minus_b": paired("d", "b"),
    "d_minus_c": paired("d", "c"),
}


for surface in ("c", "d"):
    hashes = {
        record["skill_overlay_hash"]
        for record in by_surface[surface]
    }

    require(
        len(hashes) == 1,
        f"Surface {surface.upper()} Skill overlay hash changed",
    )


for surface in ("a", "b", "c", "d"):
    bindings = {
        json.dumps(
            record["skill_bindings"],
            sort_keys=True,
        )
        for record in by_surface[surface]
    }

    require(
        len(bindings) == 1,
        f"Surface {surface.upper()} Skill bindings changed",
    )


summary = {
    "phase": common_phase,
    "scenario": common_scenario,
    "measurement_count": len(records),
    "sets": 5,
    "surfaces": [
        "a",
        "b",
        "c",
        "d",
    ],
    "model": MODEL,
    "model_form": "small",
    "binding_id": "binding-0001",
    "reasoning_mode": "normal",
    "hermes_reasoning_effort": "medium",
    "workshop": "code-debug",
    "message": common_message,
    "persist": False,
    "frozen_active_yaml_sha":
        FROZEN_ACTIVE_SHA,
    "harness": {
        "path": str(
            HARNESS.relative_to(ROOT)
        ),
        "sha256":
            sha256_path(HARNESS),
    },
    "raw_artifact_hashes": raw_hashes,
    "surface_statistics": surface_stats,
    "paired_statistics": paired_stats,
    "observations": {
        "b_vs_a_direction_consistent":
            paired_stats["b_minus_a"]["left_slower_count"]
            in (0, 5),
        "c_vs_a_direction_consistent":
            paired_stats["c_minus_a"]["left_slower_count"]
            in (0, 5),
        "d_slower_than_a_sets":
            paired_stats["d_minus_a"]["left_slower_count"],
        "d_slower_than_b_sets":
            paired_stats["d_minus_b"]["left_slower_count"],
        "d_slower_than_c_sets":
            paired_stats["d_minus_c"]["left_slower_count"],
    },
    "certification": {
        "semantic_validation": "PASS",
        "artifact_count": 20,
        "unique_task_count":
            len(seen_tasks),
        "unique_execution_context_count":
            len(seen_contexts),
        "unique_session_count":
            len(seen_sessions),
        "production_state_modified":
            False,
    },
}


OUTPUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print()
print("=== SURFACE TURN STATISTICS ===")

for surface in ("a", "b", "c", "d"):
    values = surface_stats[surface]["turn"]

    print(
        f"{surface.upper()} "
        f"median={values['median_s']:.9f} "
        f"mean={values['mean_s']:.9f} "
        f"stdev={values['stdev_s']:.9f}"
    )


print()
print("=== PAIRED TURN DIFFERENCES ===")

for name in (
    "b_minus_a",
    "c_minus_a",
    "d_minus_a",
    "d_minus_b",
    "d_minus_c",
):
    values = paired_stats[name]

    print(
        f"{name}: "
        f"median={values['median_difference_s']:.9f} "
        f"mean={values['mean_difference_s']:.9f} "
        f"left_slower="
        f"{values['left_slower_count']}/5"
    )


print()
print("=== ACTIVATION OVERHEAD MEDIANS ===")

for surface in ("a", "b", "c", "d"):
    value = (
        surface_stats[surface]
        ["activation_overhead"]
        ["median_s"]
    )

    print(
        f"{surface.upper()}: "
        f"{value:.9f} s"
    )


print()
print("Harness SHA256:")
print(
    summary["harness"]["sha256"]
)

print()
print("Summary:")
print(OUTPUT)

print()
print("Summary SHA256:")
print(
    sha256_path(OUTPUT)
)

print()
print("L.7 CERTIFICATION ANALYSIS: PASS")
