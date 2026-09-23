---
title: "The Forest — Phase 14.11 Checkpoint"
project: "The Forest"
tree: "Bristlecone Pine"
phase: "14.11"
checkpoint_status: "L.8 closed; L.9 active"
checkpoint_date_local: "2026-08-12"
utc_artifact_dates_extend_into: "2026-08-13"
format: "Obsidian-compatible Markdown"
---

# The Forest — Phase 14.11 Checkpoint

> **Purpose:** Preserve the complete working state of Bristlecone Pine / The Forest Phase 14.11 work: architecture, code/artifacts, benchmarks, hashes, certifications, failures, conflicts, lessons learned, current stopping point, and everything still left to do.

## 1. Executive Status

Current stopping point: **Phase 14.11L.9 — Recovery Cost**.

| Subphase | Status | Notes |
|---|---:|---|
| L.0 Benchmark foundation | ✅ | Complete |
| L.1 Forest control path | ✅ A+B | Complete |
| L.2 Cold Small | ✅ A+B | Complete |
| L.3 Warm Small | ▶ A ✅ / B deferred | Certification debt |
| L.4 Same-session reuse | ✅ A+B | Complete |
| L.5 Multi-context | ▶ A ✅ / B pending | Certification debt |
| L.6 Reasoning | ✅ A+B | CLOSED |
| L.7 Workshop surface | ✅ A+B | CLOSED |
| L.8 Resource Governor | ✅ A+B | CLOSED |
| L.9 Recovery cost | ▶ ACTIVE | A/B control benchmark passed |
| L.10 Sustained/repeated-turn | ⬜ | Not started |
| L.11 Comparative analysis | ⬜ | Not started |
| L.12 Optimization recommendations | ⬜ | Not started |
| L.13 Independent benchmark certification | ⬜ | Not started |
| L.14 Final checkpoint | ⬜ | Not started |

### Exact resume point

Completed immediately before this checkpoint:

- L.9 recovery architecture reconnaissance.
- Confirmed the frozen-session ensure path trusts Forest's `(execution_context_id, binding_id)` session mapping without probing Hermes.
- Confirmed deleting only the Hermes session can create a genuine stale-session condition while Forest still points to the stale session.
- Created and ran `phase14_11L9/recovery_control_benchmark.py`.
- L.9A/B control-path benchmark passed.
- Beginning with L.9, raw individual timing samples are retained for independent recomputation.
- A full L.9C `hermes_session_cost.py` harness was drafted in chat, but **creation/compile/execution has not yet been confirmed**.

**Resume at L.9C real Hermes session create/end cost.**

---

## 2. Canonical Forest Doctrine

- **The Forest is not an AI app with a forest theme. It is an AI ecosystem whose metaphor is the interface.**
- **Trees decide what would be useful. Spirit decides what is allowed.**
- **Forest keeps memory of work; runtime keeps only what it needs to perform efficiently.**
- **Users manipulate Tree concepts; Forest manipulates AI infrastructure.**
- **A Tree is not its model.**
- **Tree identity belongs to the Forest; model intelligence is a replaceable runtime resource.**
- **The Forest gets deeper as you wonder.**
- **The Forest owns meaning. The adapter owns translation.**
- **Simple on the surface. Precise underneath. Inspectable when desired.**
- **Retain cheaply. Activate selectively. Share aggressively.**
- **Compute follows active demand, not Tree ownership.**
- **Speculation must never become permission speculation.**
- **Shared capability, separate activation.**

Bristlecone Pine healthy-state phrase:

> **Pine is fine.**

### Spirit

Spirit is the deterministic authority for permissions, security policy, action authority, help/menus/command references, and other deterministic controls.

---

## 3. Colony / Clone / Runtime Identity

A Colony = Tree + all Clones/Ramets.

- **Ortet**: original lineage context.
- **Ramet**: clone.
- **Main**: operational role independent from lineage.

Runtime identity fields:

- `tree_id`
- `execution_context_id`
- `binding_id`
- `session_id`

Meaning:

- `execution_context_id` = which Ortet/Ramet/Clone context is working.
- `binding_id` = which Small/Big runtime configuration is selected.
- `session_id` = actual live runtime session.

Frozen invariant:

```text
runtime session identity = (execution_context_id, binding_id)
```

Multiple contexts may share the same model binding and resident model weights while keeping separate runtime sessions/KV/control.

---

## 4. Reasoning / Workshop / Model Form Independence

### Reasoning

- Light
- Normal
- Deep

### Workshop

Examples:

- Research
- Design
- Code/Debug
- Model
- future task-specific Workshops

### Model Form

- Small
- Big

Invariants:

```text
Deep != Big
Big != Deep
Workshop != Model Form
```

Resource pressure must not silently rewrite Model Form or Reasoning. Unsupported exact execution should approve/defer/deny rather than silently downgrade semantics.

---

## 5. Current Runtime / Model Configuration

### Small

```text
binding: binding-0001
model:   bristlecone-qwen35:4b-64k
Hermes profile: bristlecone
platform: api_server
```

Observed:

```text
Ollama residency size: ~5.6 GB
context:               64000
processor:             100% CPU
```

Conservative Small memory floor:

```text
6144 MiB
```

### Big boundary

Recorded candidate:

```text
mistralai/Mistral-Small-4-119B-2603-NVFP4
```

Big was boundary-certified but **never executed on this hardware**.

---

## 6. Frozen Production Hashes

```text
bristlecone/runtime/task_session.py
d666cb1471b568bf43db4255f5e84e98c1ea502af467e1e2670e4a93dc364991

bristlecone/runtime/session_store.py
3c3449fa878920ea27f39b6216cf38a687d09a08da1d5b57af68c1a2f4beb48f

bristlecone/runtime/session_identity.py
8a1d668e898dc2df7b60fd5099be0cf42dd2d4c864cbe163164f0a061a777353

bristlecone/runtime/adapters/hermes.py
a09949eead5cb9772aca312c91630703c7ff8ce43df778730279445b25635084

bristlecone/resources/live_providers.py
40b49375dbe014b27b6fc5696bccf74274864e42953c473b42ffe10a3c552299

bristlecone/model_form/bindings.yaml
74110afd51de7ceddd02948d0430b0f9f1b5443a6eaaaa0b8a6e4164a52b0583
```

Persistent `active.yaml` SHA:

```text
6b8fb9b44757917c1889a7368d43f393165080d248cdb3d9c5982aad53b270e5
```

---

## 7. Pre-L Benchmark Phase Status

- **14.11F Resource/Governor semantics** — certified.
- **14.11G Automatic Escalation** — closed, `63 PASS`.
- **14.11H Colony runtime/share semantics** — complete.
- **14.11I Fake Adapter** — complete, `33 PASS`.
- **14.11J Real Small** — complete/frozen.
- **14.11K Real Big boundary** — complete/frozen; Big not executed.

---

# 8. Phase L Benchmark Results

## L.1 Forest Control Path

```text
explicit median:  ~0.000877 s
automatic median: ~0.000887 s
```

Conclusion: negligible relative to inference.

Status: A+B complete.

## L.2 Cold Small

```text
229.430562429 s
164.270725926 s
141.777837884 s

median = 164.270725926 s
```

Status: A+B complete.

## L.3 Warm Small

```text
85.508143341 s
41.349474192 s
169.996093683 s
32.029349374 s
42.701828285 s

median = 42.701828285 s
```

Status: A complete; B deferred.

## L.4 Same-session reuse

```text
153.481200115 s
44.451019889 s
31.749168953 s
188.200975222 s
40.419116390 s

median = 44.451019889 s
```

Conclusion: no meaningful median advantage established.

Status: A+B complete.

## L.5 Multi-context

Five sequential/concurrent matched pairs.

Findings:

- isolation works;
- shared residency works;
- concurrent slower in 4/5 pairs;
- one pair showed the opposite extreme;
- **do not claim concurrency is faster**.

A archive:

```text
phase14_11L5_A_multicontext_certified_20260812T152526Z
```

Status: A complete; B pending.

---

# 9. L.6 Reasoning Performance

Configuration:

```text
Small
binding-0001
fixed prompt: Reply only with: L2-COLD-01
warm
fresh Task/context/session
persist=False
interleaved Light → Normal → Deep
```

Hermes mapping:

```text
Light  → low
Normal → medium
Deep   → high
```

Results:

```text
Light
median 75.879709192 s
mean   103.352293831 s
stdev  103.379349470 s

Normal
median 51.113125039 s
mean   64.460301213 s
stdev  41.648640777 s

Deep
median 36.872109413 s
mean   74.160230828 s
stdev  92.596184454 s
```

Conclusion: no clean monotonic latency relationship because inference variance dominates.

Certification:

```text
A: phase14_11L6_A_reasoning_certified_20260812T172100Z
B: phase14_11L6_B_independent_certified_20260812T172604Z
```

Status: CLOSED.

---

# 10. L.7 Workshop / Tool Surface

Status: A+B CLOSED.

Controlled Code/Debug surfaces:

```text
A baseline
Ready []
toolsets file,terminal
Skills none

B extra tool
Ready [code-execution]
toolsets file,terminal,code_execution
Skills none

C Skill
Ready [debugging]
toolsets file,terminal
Skill systematic-debugging
overlay 14554 bytes

D full
Ready [code-execution,debugging,testing]
toolsets file,terminal,code_execution
Skills systematic-debugging,test-driven-development
overlay 25357 bytes
```

`special` was excluded as unresolved.

Persistent source intentionally carried:

```text
active_ready = ["debugging"]
task_sticky_skills = ["debugging"]
```

L.7 neutralized only an **in-memory persist=False benchmark copy**:

```text
active_ready = []
task_sticky_skills = []
temporary_capabilities = []
```

Persistent state was not modified.

Real-turn configuration:

```text
Small
binding-0001
Normal → Hermes medium
warm
fresh Task/context/session
persist=False
5 interleaved A→B→C→D sets
20 measured real inference turns
```

Corrected harness SHA:

```text
4ba7d460167269851b9c9d1f6ac966c9228b59d189b76f6178b63b57758cdedb
```

Summary:

```text
bristlecone/benchmarks/phase14_11L/l7_surface_summary.json
SHA a388736294fe4c24caed7f0aeeb2b875481b39ab65508692240ef3aac6cfa418
```

### L.7 raw turn times

```text
A:
129.719346900
228.600509840
246.529720959
124.686041473
224.609125841

B:
134.959032113
189.462367399
118.600829528
195.791776264
226.115520626

C:
229.016639620
164.289985605
241.721057840
200.307306890
197.040299153

D:
331.175307632
300.544201935
543.318880843
446.213415749
327.808480592
```

Statistics:

```text
A median224.609125841 mean190.828949003 stdev58.693344677
B median189.462367399 mean172.985905186 stdev44.771969829
C median200.307306890 mean206.475057822 stdev30.236730841
D median331.175307632 mean389.812057350 stdev102.465750433
```

Paired:

```text
B-A median +1.506394785 mean -17.843043817; B slower 3/5
C-A median -4.808663119 mean +15.646108819; C slower 2/5
D-A median +201.455960732 mean +198.983108348; D slower 5/5
D-B median +196.216275519 mean +216.826152164; D slower 5/5
D-C median +136.254216330 mean +183.336999529; D slower 5/5
```

Activation + exit medians:

```text
A 0.020217682 s
B 0.711531220 s
C 0.136165004 s
D 0.768246054 s
```

Interpretation:

- one extra tool did not show a stable turn-latency effect;
- one Skill did not show a stable turn-latency effect;
- D was slower in every matched set;
- D changes multiple dimensions, so do not attribute its slowdown to one component;
- Workshop switch itself remains sub-second;
- most penalty appears in model-turn execution.

Warnings:

- some optional Hermes plugins emitted missing-`httpx` warnings during D activation;
- warnings happened before timed inference and did not invalidate the benchmark.

Warm precondition failures:

- some attempts found Small expired;
- harness stopped before Task/inference/artifact;
- those attempts were not counted;
- unmeasured prewarm restored residency.

Certification:

```text
A archive:
bristlecone/backups/phase14_11L7_A_surface_certified_20260813T000538Z

A manifest:
990cc2cab7a223a737d20ca454e47ad739b9ae9a2efe577d074e03b2fa3cfcbc

B archive:
bristlecone/backups/phase14_11L7_B_independent_certified_20260813T000909Z

B report:
03f5939d5491d188ae996bb675fad3f6a6beceecb8f1a7eb3f4d68817403262d

B manifest:
53dc2d0b76ece05c691059c6fcef16228a50f5d2115ccb5b86a4ed8dbbcb42ee
```

B validated 20/20 semantic checks with no inference/production modification.

---

# 11. L.8 Resource Governor Performance

Status: A+B CLOSED.

Implemented files:

```text
bristlecone/certification/phase14_11L8/governor_benchmark.py
bristlecone/certification/phase14_11L8/residency_effect.py
bristlecone/certification/phase14_11L8/analyze_governor.py
bristlecone/certification/phase14_11L8/independent_certify.py
```

Artifacts:

```text
bristlecone/benchmarks/phase14_11L/l8_governor_raw.json
bristlecone/benchmarks/phase14_11L/l8_residency_effect_raw.json
bristlecone/benchmarks/phase14_11L/l8_governor_summary.json
```

## ResourceRequest

Valid priorities:

```text
background
standard
interactive
```

Frozen request contains task/context/model form/reasoning/priority/source/reasons/`may_defer`.

It does not grant permission, schedule hardware, select a session, or silently rewrite semantics.

## ResourceRequirement

```text
None = unknown requirement
0    = explicitly none beyond baseline
N    = known minimum
```

## ResourceBudget

```text
None = no explicit ceiling
0    = explicit zero ceiling
N    = explicit maximum
```

Live Small budget currently has all ceilings `None`.

## ResourceAvailability

```text
None = unknown/not measured
0    = measured exactly zero
```

Live Small availability:

- `/proc/meminfo` `MemAvailable`
- CPU affinity / `os.cpu_count()`
- accelerator = 0

## Governor policy order

```text
1 known requirement exceeds explicit budget → DENY
2 unknown requirement → DEFER if may_defer else DENY
3 positive requirement + unknown/insufficient availability → DEFER if may_defer else DENY
4 otherwise → APPROVE
```

Zero requirement bypasses availability for that dimension.

Priority currently does not alter pure Governor outcome.

## Provider order

```text
requirement
→ budget
→ availability
→ pure Governor
```

Typed/identity checks occur between stages.

## Live Small provider constants

```text
SMALL_MODEL_FORM = "small"
SMALL_BINDING_ID = "binding-0001"
SMALL_MODEL_NAME = "bristlecone-qwen35:4b-64k"
SMALL_MEMORY_REQUIREMENT_MIB = 6144
SMALL_ACCELERATOR_MEMORY_REQUIREMENT_MIB = 0
SMALL_CPU_THREAD_REQUIREMENT = 1
```

Residency lookup:

```text
http://127.0.0.1:11434/api/ps
```

Requirement logic:

```text
query unavailable → conservative 6144 MiB
model absent       → 6144 MiB
model resident     → ceil(max(0, calibrated bytes - resident bytes) / MiB)
```

Residency affects requirement, not availability.

## L.8 synthetic cases

```text
approve
budget deny deferrable
budget deny nondeferrable
unknown requirement defer
unknown requirement deny
insufficient availability defer
insufficient availability deny
unknown availability defer
unknown availability deny
zero-requirement bypass
priority background/standard/interactive
```

All expected semantics passed.

## L.8 performance

```text
Pure Governor approve median:       2.795 µs
Live availability median:          22.843 µs
Live budget median:                 1.713 µs
Nonresident requirement median:   373.534 µs
Whole live Governor median:       449.952 µs
Resident requirement median:      406.455 µs
```

Whole live path:

```text
~0.450 ms
```

Conclusion: Governor is not a meaningful user-visible latency bottleneck. Ollama residency observation dominates its tiny live cost.

Live benchmark state:

```text
MemAvailable: 10095 MiB
CPU threads:  9
accelerator:  0
whole pipeline: approve 20/20
```

## Nonresident proof

Read-only `ollama ps`:

```text
Resident models: none
```

Requirement:

```text
memory_mib 6144
accelerator_memory_mib 0
cpu_threads 1
```

## Resident proof

Unmeasured prewarm established Small residency.

Exact resident bytes:

```text
5,646,906,816
```

Calibrated floor:

```text
6144 MiB
```

Expected remaining:

```text
759 MiB
```

Production observed:

```text
[759]
```

20/20 matched.

Therefore:

```text
nonresident → 6144 MiB
resident    → 759 MiB
```

## L.8 hashes

```text
Core raw:
2c9e70239070edac150646fe00f75593fea1baf7522ccbb182b32860ee47cb91

Residency raw:
243c92316063a368712d690eb06b1fd636d571e881e812b572358e1682e8b166

Core harness:
f8ab314952c95fb01b2f5b0295eb89da605d6708e436e665c704d997dd7991f5

Residency harness:
e7c50bac53094207562af09b470a030abef400eeb283bbc510c8d8531605035d

A summary:
7f51d85b38cb705cb495bfb56a142bc65d0f85d3f7905774ea7eab2e937ce3a5
```

A archive:

```text
bristlecone/backups/phase14_11L8_A_governor_certified_20260813T005056Z
```

A manifest:

```text
aa2c724800b9774e272bf01a7e2227d169590feb2150bad27999a900040a0978
```

B archive:

```text
/home/user/The-Forest/bristlecone/backups/phase14_11L8_B_independent_certified_20260813T005320Z
```

B report:

```text
e7a60dd91bf937f9505f2b3f9427b021c0c021a14ca2a4e33d491026aec49713
```

B manifest:

```text
c69adb23c29fdb5c30eb21de31c35380eccdf83f120c960297c4dcfd1e68246c
```

B verified A archive 15/15 files, production-source integrity, semantic matrix, priority behavior, provider order, residency math, and A/raw consistency with no inference or Ollama mutation.

### L.8 limitation

L.8 kept aggregate timing statistics but not every per-iteration sample. B could verify the frozen metrics but could not reconstruct the original medians from first principles.

**Permanent fix starting L.9:** raw artifacts retain every individual timing sample.

---

# 12. L.9 Recovery Cost — Architecture

Status: ACTIVE.

Production recovery is explicitly one-shot and frozen-semantics preserving.

Sequence:

```text
frozen Model Form + Reasoning
→ selected session S
→ send_turn(S)
→ exception
→ classify stale?
→ non-stale: escape
→ stale: rebuild same frozen execution view
→ create replacement R
→ rotate Forest context+binding S → R
→ retry exact turn once
→ success: session_recovered=True
→ second failure: escape immediately
```

Recovery does not reroute/re-resolve Model Form or Reasoning.

### Hermes stale classifier

Stale only if:

```text
RuntimeAdapterError
status_code == 404
error_code == "session_not_found"
```

### Hermes runtime calls

```text
create_session:
POST /api/sessions

send_turn:
POST /api/sessions/{session_id}/chat

end_session:
DELETE /api/sessions/{session_id}
```

Reasoning translation remains:

```text
light→low
normal→medium
deep→high
```

## Critical stale-trigger proof

The same-form send path calls:

```python
ensure_runtime_session(
    state=initial,
    persist=False,
    frozen_turn=frozen_turn,
)
```

With a frozen turn, this delegates to:

```python
_ensure_runtime_session_for_frozen_turn(...)
```

That helper reads the Forest context+binding mapping. If it finds an existing session ID, it returns:

```text
created=False
reused=True
runtime_result=None
session_id=existing_id
```

It does **not** probe Hermes.

Therefore the production-native real stale benchmark is valid:

```text
Forest binding → S
delete only Hermes S
Forest still points to S
next frozen ensure reuses S
send_turn(S)
real 404/session_not_found
real recovery
replacement R
binding rotates S→R
retry once
```

No production monkeypatch is required.

---

# 13. L.9 Benchmark Matrix

## L.9A Recovery control-path performance

Controlled fake adapter, zero inference.

Compare:

```text
normal success
vs
stale → classify → replacement → retry
```

## L.9B One-retry enforcement

Cases:

```text
stale → stale
stale → runtime failure
```

Require:

```text
send calls:       2
session creations:2 total (initial + one replacement)
classifier calls: 1
second error:     escapes
```

## L.9C Real Hermes session cost

Real:

```text
create_session()
end_session()
```

No chat/inference.

## L.9D Genuine real stale Small recovery

Planned:

```text
Small / binding-0001
Normal → medium
create/bind S
delete Hermes S only
leave Forest binding
send real turn
require real 404/session_not_found
require replacement R
require R != S
require session_recovered=True
preserve Small/Normal/binding/context/task
```

## L.9E Matched normal vs recovered

Initial plan:

```text
3 interleaved pairs
```

because real model variance is already huge and the control-path overhead is tiny.

---

# 14. L.9A/B Implemented Code and Results

Implemented:

```text
bristlecone/certification/phase14_11L9/recovery_control_benchmark.py
```

Evidence:

```text
bristlecone/benchmarks/phase14_11L/l9_recovery_control_raw.json
```

Design:

```text
classifier:
10000 stale
10000 non-stale

unmeasured warmup:
20 normal/recovery pairs

measured:
500 normal/recovery pairs
alternating pair order
all individual timings retained
```

Existing certified fake scaffold reused:

```text
bristlecone/tests/test_model_form_retry_task_session_integration.py
```

It records:

```text
create_calls
send_calls
classifier_calls
end_calls
```

and supports deterministic:

```text
ok
stale
fail
```

### Results

```text
stale classifier median:     0.160 µs
non-stale classifier median: 0.181 µs

normal control median:       860.426 µs
recovery control median:     931.828 µs
paired recovery overhead:     71.605 µs

recovery slower:
465 / 500 pairs = 93%
```

One-retry tests:

```text
stale → stale
PASS

stale → failure
PASS
```

Both verified exactly one recovery cycle.

No inference.

No persistent production modification.

Hashes:

```text
L.9 control harness:
4eaa7b4ce6153973f55566fa7087b5aed0b758fc58216aed4c2d4e61869c9eab

L.9 control raw:
944c68ded31899f29b5ae1ef6d0f55cca1451b3f065f6e124ccea7bf018a3553
```

---

# 15. Real Hermes Scaffold Reused from L.7

Manager:

```python
manager = TaskSessionManager(
    forest_root=ROOT,
)
```

Load state:

```python
configured_state = manager.load_state()
```

Adapter:

```python
runtime_adapter = (
    manager._runtime_adapter_for_state(
        configured_state
    )
)
```

Verify Hermes:

```python
if getattr(
    runtime_adapter,
    "adapter_name",
    None,
) != "hermes":
    raise RuntimeError(...)
```

Fresh in-memory task:

```python
started = manager.start_task(
    state=benchmark_source_state,
    persist=False,
)
```

Real Small turn:

```python
result = manager.send_runtime_turn(
    MESSAGE,
    state=state,
    instructions=...,
    reasoning_mode="normal",
    persist=False,
    execution_context_id=context,
    model_form="small",
    resource_governor=governor,
    resource_priority="standard",
    resource_request_source=...,
    resource_request_reasons=(...,),
    resource_may_defer=False,
)
```

This scaffold should be reused rather than rebuilding TaskSession/Hermes setup from guesses.

---

# 16. L.9C Proposed but NOT Yet Confirmed Executed

Draft target:

```text
bristlecone/certification/phase14_11L9/hermes_session_cost.py
```

Expected artifact:

```text
bristlecone/benchmarks/phase14_11L/l9_hermes_session_cost_raw.json
```

Planned configuration:

```text
warmups:    5
iterations: 50
```

Each sample should retain:

```text
session_id
create_ns
end_ns
round_trip_ns
```

No chat endpoint.

No inference.

No persistent Forest state.

**Do not mark L.9C complete until its compile/run output and hashes are actually observed.**

---

# 17. Conflicts, Errors, and Lessons Learned

## Interactive `exit` closed the terminal

A prior command used:

```bash
exit "$STATUS"
```

inside an interactive shell and closed the terminal.

Permanent rule:

- never use `exit` in interactive command blocks;
- use `STATUS=$?`, `echo`, `false`, or Python `raise RuntimeError`.

## Avoid long model benchmarks through `tee`

Prefer harness-written artifacts/direct output. Long runs through `tee` can create buffering and operational confusion.

## L.7 expired residency attempts

Some L.7 attempts failed:

```text
Warm Small residency precondition failed.
```

They stopped before Task/inference/artifact and were not counted.

## L.7 `httpx` warnings

Optional Hermes plugin warnings occurred before timed D turns. They did not invalidate the benchmark.

## L.8 6144-MiB ambiguity

`[6144]` could have been real nonresidency or conservative unknown fallback. Read-only `ollama ps` proved Small was absent, resolving the ambiguity.

## L.8 missing residency harness file

The assistant accidentally told the user to compile `residency_effect.py` before the creation block had been run.

Observed:

```text
[Errno 2] No such file or directory
compile status: 1
```

No benchmark ran and nothing was contaminated. File was then created correctly.

Permanent workflow:

```text
create
→ compile
→ status 0
→ hash
→ run
```

## L.8 raw timing limitation

Only aggregate stats were retained. B could not recompute medians.

Fix from L.9 onward:

```json
"timings_ns": [...]
```

## L.9 source-output clipping

Several broad dumps were clipped. Narrow `sed`, AST extraction, and targeted grep proved more reliable.

## L.9 wrong helper-path assumption

Initially generic `ensure_runtime_session()` looked decisive. Later discovered frozen turns delegate to `_ensure_runtime_session_for_frozen_turn()`.

Lesson: follow actual production delegation before designing a benchmark trigger.

## L.9 stale trigger deliberately verified

We did not assume deleting Hermes would hit stale recovery. We first proved the frozen ensure helper trusts the Forest binding and does not probe Hermes.

This prevents accidentally benchmarking the wrong recovery mechanism.

---

# 18. Benchmark Methodology Rules

1. Read-only inspection first.
2. Understand exact production path before writing a harness.
3. Do not modify production just to make a benchmark easy.
4. Prefer in-memory state and `persist=False`.
5. Compile before execution.
6. Hash harnesses/artifacts.
7. Record environment/preconditions.
8. Failed preconditions are not measurements.
9. Store every raw timing sample from L.9 onward.
10. Do not run unrelated concurrent real inference.
11. Keep fake/control benchmarks separate from real runtime benchmarks.
12. Preserve exact semantic configuration.
13. Independent B should recompute statistics from raw samples when possible.
14. Explicitly record transient runtime changes separately from persistent production changes.

---

# 19. Current Performance Picture

Forest control layers are cheap:

```text
L.1 control path              ~0.88 ms
L.8 whole live Governor       ~0.450 ms
L.8 pure Governor             ~2.8 µs
L.9 extra recovery controls   ~71.6 µs
```

Real inference remains tens to hundreds of seconds.

Current evidence therefore points to model/runtime generation as the dominant user-visible performance problem, not Forest semantic control, Governor, Workshop switching, or stale-session bookkeeping.

---

# 20. Supported Architectural Conclusions

Supported:

1. Tree identity is Forest-side and independent of runtime session identity.
2. Model Form, Reasoning, and Workshop are independent controls.
3. Forest control overhead is tiny compared with inference.
4. Whole live Governor is sub-millisecond.
5. Pure Governor policy is only a few microseconds.
6. Ollama residency lookup dominates Governor overhead.
7. Residency-aware requirements work: 6144 MiB nonresident → 759 MiB resident.
8. Workshop activation/restoration is much smaller than model inference.
9. Full L.7 D was slower in all matched sets, but multiple dimensions changed.
10. Real inference has high variance.
11. L.5 concurrency was slower in 4/5 pairs.
12. Recovery preserves frozen semantic decisions.
13. Recovery is deliberately one-shot.
14. Synthetic Forest recovery premium is ~71.605 µs median.
15. The stale classifier is effectively negligible.
16. Frozen session ensure trusts the Forest context+binding mapping without probing Hermes.
17. A genuine production stale test can therefore delete only the Hermes session while retaining Forest state.

Do **not** claim:

- Deep is inherently slower than Light.
- same-session reuse provides a meaningful median speedup.
- concurrency is faster.
- one Skill alone explains L.7 D slowdown.
- `code_execution` alone explains L.7 D slowdown.
- Governor is a user-visible latency bottleneck.
- real stale recovery cost is known from L.9A/B alone.
- L.9C/D/E are complete.
- L.3 B or L.5 B are complete.

---

# 21. Work Remaining

## Immediate: L.9C

1. Confirm/create `hermes_session_cost.py`.
2. `py_compile`.
3. Verify status 0.
4. Hash harness.
5. Run.
6. Record create/end/round-trip medians and all raw samples.
7. Hash artifact.

## L.9D

Single genuine real stale Small proof:

```text
create/bind S
delete only Hermes S
Forest keeps S
send real Small/Normal turn
real 404/session_not_found
replacement R
R != S
session_recovered=True
same Small/Normal/task/context/binding
```

Do one proof before repeated pairs.

## L.9E

If L.9D passes:

```text
3 matched normal/recovered pairs
```

Retain all individual timings.

## L.9 A certification

- recompute raw stats;
- validate control benchmark;
- validate one-retry safety;
- validate Hermes session cost;
- validate real recovery fields;
- validate matched comparison;
- check source hashes;
- write summary;
- freeze A archive.

## L.9 B independent certification

- recompute all possible statistics from raw arrays;
- rerun zero-inference semantics;
- verify frozen/source integrity;
- avoid extra inference if frozen artifacts suffice.

Then:

```text
L.9 CLOSED
```

## L.10 Sustained/repeated-turn

Still to design. Likely measure latency drift, session stability, memory/residency changes, runtime growth, recovery frequency, and context/KV effects.

## L.11 Comparative analysis

Combine cold/warm/reuse/multi-context/reasoning/Workshop/Governor/recovery/sustained data.

## L.12 Optimization recommendations

Evidence-driven focus likely includes:

- model/runtime inference speed;
- quantization;
- Ollama vs llama.cpp;
- speculative decoding;
- context sizing;
- Workshop/tool-schema minimization;
- deterministic routing;
- source-context targeting;
- concurrency policy;
- session/runtime caching;
- alternative Small model.

Do not over-optimize already-sub-millisecond Forest control layers.

## L.13 Independent benchmark certification

Resolve/acknowledge certification debt:

```text
L.3 B deferred
L.5 B pending
```

## L.14 Final checkpoint

Freeze complete benchmark dataset, findings, certification archive, optimization plan, limitations, and next implementation phase.

---

# 22. Important Files to Preserve

### L.7

```text
bristlecone/certification/phase14_11L7/surface_trial.py
bristlecone/certification/phase14_11L7/analyze_surface.py
bristlecone/certification/phase14_11L7/independent_certify.py
bristlecone/benchmarks/phase14_11L/l7_surface_*_raw.json
bristlecone/benchmarks/phase14_11L/l7_surface_summary.json
```

### L.8

```text
bristlecone/certification/phase14_11L8/governor_benchmark.py
bristlecone/certification/phase14_11L8/residency_effect.py
bristlecone/certification/phase14_11L8/analyze_governor.py
bristlecone/certification/phase14_11L8/independent_certify.py
bristlecone/benchmarks/phase14_11L/l8_governor_raw.json
bristlecone/benchmarks/phase14_11L/l8_residency_effect_raw.json
bristlecone/benchmarks/phase14_11L/l8_governor_summary.json
```

### L.9 current

```text
bristlecone/certification/phase14_11L9/recovery_control_benchmark.py
bristlecone/benchmarks/phase14_11L/l9_recovery_control_raw.json
```

Next expected:

```text
bristlecone/certification/phase14_11L9/hermes_session_cost.py
bristlecone/benchmarks/phase14_11L/l9_hermes_session_cost_raw.json
bristlecone/certification/phase14_11L9/real_recovery_trial.py
bristlecone/certification/phase14_11L9/analyze_recovery.py
bristlecone/certification/phase14_11L9/independent_certify.py
```

---

# 23. Environment / Working Rules

```text
OS: Qubes OS
active qube: Cherry-AI
Forest root: /home/user/The-Forest
canonical source: /home/user/The-Forest/bristlecone
Hermes: 127.0.0.1:8643
Ollama: 127.0.0.1:11434
Hermes profile: /home/user/.hermes/profiles/bristlecone
```

Important:

```text
/home/user/The-Forest is NOT Git
```

Terminal A = current production/benchmark work.

Terminal B = independent certifier, usually one subphase behind.

During real Small benchmarks, do not run another unrelated real inference concurrently.

---

# 24. Longer-Term Forest Directions

- local-first;
- free/open-source/self-hostable where practical;
- avoid subscriptions when practical;
- non-Chinese model alternatives prioritized when practical for future core Trees;
- do not disrupt the current Qwen Small baseline before Phase 14 benchmark completion;
- later compare a replacement Small against the exact same benchmark suite.

Long-term memory direction:

```text
raw history
→ detailed summaries
→ episode summaries
→ long-term Leaves
→ embeddings/vector index
→ metadata
→ Roots/knowledge graph
```

Leaf Foliage should remain human-readable, Markdown-first, local-first, and Obsidian-compatible where practical.

Future optimization topics:

- quantization;
- Ollama vs llama.cpp;
- speculative decoding;
- context length;
- deterministic tool routing;
- tiny task-specific Workshops;
- source-context targeting;
- self-improving/evaluation harness;
- Quick vs Deep operating modes.

---

# 25. Exact Resume Commands

First determine whether the proposed L.9C file was actually created:

```bash
cd /home/user/The-Forest

ls -l     bristlecone/certification/phase14_11L9/hermes_session_cost.py
```

If present, compile:

```bash
python -m py_compile     bristlecone/certification/phase14_11L9/hermes_session_cost.py

STATUS=$?

echo
echo "L.9C harness compile status: $STATUS"
```

If status is 0:

```bash
sha256sum     bristlecone/certification/phase14_11L9/hermes_session_cost.py
```

Then run:

```bash
PYTHONPATH="$PWD/bristlecone" python -u     bristlecone/certification/phase14_11L9/hermes_session_cost.py

STATUS=$?

echo
echo "L.9C shell status: $STATUS"
```

Do **not** use `exit "$STATUS"`.

---

# 26. Anchor Hash Summary

### L.7

```text
A manifest
990cc2cab7a223a737d20ca454e47ad739b9ae9a2efe577d074e03b2fa3cfcbc

B report
03f5939d5491d188ae996bb675fad3f6a6beceecb8f1a7eb3f4d68817403262d

B manifest
53dc2d0b76ece05c691059c6fcef16228a50f5d2115ccb5b86a4ed8dbbcb42ee
```

### L.8

```text
Core raw
2c9e70239070edac150646fe00f75593fea1baf7522ccbb182b32860ee47cb91

Residency raw
243c92316063a368712d690eb06b1fd636d571e881e812b572358e1682e8b166

Core harness
f8ab314952c95fb01b2f5b0295eb89da605d6708e436e665c704d997dd7991f5

Residency harness
e7c50bac53094207562af09b470a030abef400eeb283bbc510c8d8531605035d

A summary
7f51d85b38cb705cb495bfb56a142bc65d0f85d3f7905774ea7eab2e937ce3a5

A archive manifest
aa2c724800b9774e272bf01a7e2227d169590feb2150bad27999a900040a0978

B report
e7a60dd91bf937f9505f2b3f9427b021c0c021a14ca2a4e33d491026aec49713

B manifest
c69adb23c29fdb5c30eb21de31c35380eccdf83f120c960297c4dcfd1e68246c
```

### L.9 current

```text
Control harness
4eaa7b4ce6153973f55566fa7087b5aed0b758fc58216aed4c2d4e61869c9eab

Control raw
944c68ded31899f29b5ae1ef6d0f55cca1451b3f065f6e124ccea7bf018a3553
```

---

# 27. Final Checkpoint Summary

The Forest architecture is currently showing a strong separation between semantic control and expensive model execution.

Measured Forest-side operations are tiny:

```text
L.1 control path             ~0.88 ms
L.8 whole live Governor      ~0.450 ms
L.8 pure Governor            ~2.8 µs
L.9 extra recovery controls  ~71.6 µs
```

Meanwhile Small inference remains tens to hundreds of seconds with high variance.

The current evidence supports focusing future optimization effort primarily on the model/runtime path rather than the already-light Forest semantic, Governor, Workshop, and recovery layers.

The project resumes at:

> **Phase 14.11L.9C — real Hermes session create/end cost**

then:

> **L.9D — genuine production stale Small recovery**

then:

> **L.9E — matched normal vs recovered real Small turns**

---

## One-line handoff prompt

> Continue The Forest Phase 14.11 from this checkpoint. Treat all completed hashes/results as frozen evidence. Resume at L.9C real Hermes session create/end cost; do not rerun completed real inference unnecessarily, do not alter production merely to satisfy benchmarks, retain every raw timing sample from L.9 onward, and preserve the frozen Model Form/Reasoning/session-identity invariants documented here.
