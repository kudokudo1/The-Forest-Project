from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path("/home/user/The-Forest/bristlecone")

BENCH = (
    ROOT
    / "benchmarks"
    / "phase14_11L"
)

BACKUPS = (
    ROOT
    / "backups"
)

OUTPUT = (
    BENCH
    / "l11_evidence_inventory.json"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


PHASES = {
    "L.0": {
        "status":
            "foundation-certified",

        "certification":
            "foundation",

        "a_status":
            None,

        "b_status":
            None,

        "archives": [
            "phase14_11L0_foundation_certified_20260812T112730Z",
        ],

        "notes": [
            (
                "Benchmark foundation predates "
                "the A/B certification split."
            ),
        ],
    },

    "L.1": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L1_B_independent_certified_20260812T122013Z",
        ],

        "notes": [
            (
                "Legacy archive layout predates "
                "standardized separately named "
                "Terminal A backup directories."
            ),
            (
                "Independent Terminal B "
                "certification archive is present."
            ),
        ],
    },

    "L.2": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L2_A_cold_small_certified_20260812T122635Z",
            "phase14_11L2_B_independent_certified_20260812T123909Z",
        ],

        "notes": [],
    },

    "L.3": {
        "status":
            "partially-certified",

        "certification":
            "A-only",

        "a_status":
            "complete",

        "b_status":
            "deferred",

        "archives": [
            "phase14_11L3_A_warm_small_certified_20260812T125544Z",
        ],

        "notes": [
            "Terminal B certification remains deferred.",
        ],
    },

    "L.4": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L4_A_same_session_certified_20260812T134845Z",
            "phase14_11L4_B_independent_certified_20260812T135338Z",
        ],

        "notes": [],
    },

    "L.5": {
        "status":
            "partially-certified",

        "certification":
            "A-only",

        "a_status":
            "complete",

        "b_status":
            "pending",

        "archives": [
            "phase14_11L5_A_multicontext_certified_20260812T152526Z",
        ],

        "notes": [
            "Terminal B certification remains pending.",
        ],
    },

    "L.6": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L6_A_reasoning_certified_20260812T172100Z",
            "phase14_11L6_B_independent_certified_20260812T172604Z",
        ],

        "notes": [],
    },

    "L.7": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L7_A_surface_certified_20260813T000538Z",
            "phase14_11L7_B_independent_certified_20260813T000909Z",
        ],

        "notes": [],
    },

    "L.8": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L8_A_governor_certified_20260813T005056Z",
            "phase14_11L8_B_independent_certified_20260813T005320Z",
        ],

        "notes": [],
    },

    "L.9": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L9_A_recovery_certified_20260813T023040Z",
            "phase14_11L9_B_independent_certified_20260813T024209Z",
        ],

        "notes": [],
    },

    "L.10": {
        "status":
            "certified",

        "certification":
            "A+B",

        "a_status":
            "complete",

        "b_status":
            "complete",

        "archives": [
            "phase14_11L10_A_sustained_certified_20260813T033046Z",
            "phase14_11L10_B_independent_certified_20260813T033550Z",
        ],

        "notes": [],
    },
}


def phase_number(label):
    return int(
        label.split(".")[1]
    )


def benchmark_files_for_phase(number):
    results = []

    pattern = re.compile(
        rf"^l{number}_"
    )

    for path in sorted(
        BENCH.iterdir()
    ):
        if (
            path.is_file()
            and pattern.match(
                path.name
            )
        ):
            results.append(
                {
                    "name":
                        path.name,

                    "sha256":
                        sha256(path),

                    "size_bytes":
                        path.stat().st_size,
                }
            )

    return results


def anchor_for_archive(archive):
    candidates = (
        "MANIFEST.sha256",
        "SHA256SUMS",
        "SHA256SUMS.txt",
    )

    for name in candidates:
        path = (
            archive
            / name
        )

        if path.is_file():
            return path

    return None


def validate_checksum_anchor(
    archive,
    anchor,
):
    result = subprocess.run(
        [
            "sha256sum",
            "-c",
            anchor.name,
        ],
        cwd=archive,
        capture_output=True,
        text=True,
    )

    return {
        "returncode":
            result.returncode,

        "valid":
            result.returncode == 0,

        "stdout":
            result.stdout,

        "stderr":
            result.stderr,
    }


require(
    BENCH.is_dir(),
    f"Missing benchmark directory: {BENCH}",
)

require(
    BACKUPS.is_dir(),
    f"Missing backup directory: {BACKUPS}",
)

require(
    not OUTPUT.exists(),
    (
        "Refusing to overwrite existing "
        f"L.11 inventory: {OUTPUT}"
    ),
)


print(
    "=== L.11A EVIDENCE INVENTORY ==="
)


inventory = {}


for label in sorted(
    PHASES,
    key=phase_number,
):
    definition = PHASES[
        label
    ]

    number = phase_number(
        label
    )

    print()
    print(
        f"--- {label} ---"
    )

    phase_record = {
        "status":
            definition[
                "status"
            ],

        "certification":
            definition[
                "certification"
            ],

        "a_status":
            definition[
                "a_status"
            ],

        "b_status":
            definition[
                "b_status"
            ],

        "notes":
            list(
                definition[
                    "notes"
                ]
            ),

        "benchmark_files":
            benchmark_files_for_phase(
                number
            ),

        "archives":
            [],
    }


    for archive_name in (
        definition[
            "archives"
        ]
    ):
        archive = (
            BACKUPS
            / archive_name
        )

        require(
            archive.is_dir(),
            (
                "Missing certified archive: "
                f"{archive}"
            ),
        )

        anchor = anchor_for_archive(
            archive
        )

        require(
            anchor is not None,
            (
                "No supported checksum "
                f"anchor in {archive}"
            ),
        )

        validation = (
            validate_checksum_anchor(
                archive,
                anchor,
            )
        )

        require(
            validation[
                "valid"
            ],
            (
                "Checksum validation failed "
                f"for {archive_name}\n"
                f"{validation['stdout']}\n"
                f"{validation['stderr']}"
            ),
        )

        archive_record = {
            "name":
                archive_name,

            "anchor_file":
                anchor.name,

            "anchor_sha256":
                sha256(
                    anchor
                ),

            "checksum_validation":
                "PASS",

            "file_count":
                sum(
                    1
                    for path
                    in archive.rglob("*")
                    if path.is_file()
                ),
        }

        phase_record[
            "archives"
        ].append(
            archive_record
        )

        print(
            "PASS archive:",
            archive_name,
        )

        print(
            "  anchor:",
            anchor.name,
        )

        print(
            "  anchor SHA256:",
            archive_record[
                "anchor_sha256"
            ],
        )


    print(
        "Certification:",
        definition[
            "certification"
        ],
    )

    print(
        "Benchmark files:",
        len(
            phase_record[
                "benchmark_files"
            ]
        ),
    )


    inventory[
        label
    ] = phase_record


# Foundation files that do not use l0_ naming.
foundation_files = []

for name in (
    "METHODOLOGY.md",
    "baseline.jsonl",
):
    path = (
        BENCH
        / name
    )

    require(
        path.is_file(),
        (
            "Missing foundation benchmark "
            f"file: {name}"
        ),
    )

    foundation_files.append(
        {
            "name":
                name,

            "sha256":
                sha256(path),

            "size_bytes":
                path.stat().st_size,
        }
    )


inventory[
    "L.0"
][
    "benchmark_files"
] = foundation_files


fully_ab = [
    label
    for label, record
    in inventory.items()
    if record[
        "certification"
    ]
    == "A+B"
]

a_only = [
    label
    for label, record
    in inventory.items()
    if record[
        "certification"
    ]
    == "A-only"
]


payload = {
    "phase":
        "14.11L.11",

    "subphase":
        "L.11A",

    "status":
        "success",

    "purpose":
        "canonical-frozen-evidence-inventory",

    "archive_integrity_formats_supported": [
        "SHA256SUMS",
        "SHA256SUMS.txt",
        "MANIFEST.sha256",
    ],

    "phase_inventory":
        inventory,

    "certification_summary": {
        "fully_a_plus_b":
            fully_ab,

        "a_only":
            a_only,

        "b_deferred": [
            "L.3"
        ],

        "b_pending": [
            "L.5"
        ],

        "foundation":
            [
                "L.0"
            ],
    },

    "comparative_analysis_policy": {
        "use_certified_evidence_when_available":
            True,

        "allow_a_only_evidence":
            True,

        "a_only_evidence_must_be_labeled":
            True,

        "do_not_treat_different_measurement_boundaries_as_identical":
            True,

        "do_not_infer_speedup_from_noisy_whole_turn_samples":
            True,
    },

    "inference_executed":
        False,

    "runtime_mutation":
        False,

    "persistent_production_state_modified":
        False,
}


OUTPUT.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


print()
print(
    "=== L.11A SUMMARY ==="
)

print(
    "A+B:",
    fully_ab,
)

print(
    "A-only:",
    a_only,
)

print(
    "B deferred:",
    [
        "L.3"
    ],
)

print(
    "B pending:",
    [
        "L.5"
    ],
)

print()
print(
    "Inventory:",
    OUTPUT,
)

print()
print(
    "Inventory SHA256:",
    sha256(
        OUTPUT
    ),
)

print()
print(
    "PHASE 14.11L.11A EVIDENCE INVENTORY: PASS"
)
