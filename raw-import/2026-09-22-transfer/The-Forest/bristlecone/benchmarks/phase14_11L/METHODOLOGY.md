# Phase 14.11L — Runtime Performance Certification

## Purpose

Phase 14.11L measures the performance of the already-certified
Forest runtime architecture.

L does not redefine runtime semantics.

J answered:

> Does Real Small execute correctly?

K answered:

> Does Forest remain safe when Big is unavailable?

L answers:

> Where does runtime time go, how stable is it, and what can be
> optimized without violating Forest semantics?

---

## Core benchmark rule

Measure first.

Optimize second.

Do not modify production runtime behavior merely to improve a
benchmark result.

Any optimization proposed in L.12 must preserve the certified
semantic invariants from Phases J and K.

---

## Runtime under test

Primary runtime:

- Model Form: Small
- Binding: binding-0001
- Adapter: Hermes
- Profile: bristlecone
- Platform: api_server

Big is outside the execution scope of Phase L on this machine.

The 119B candidate must not be loaded or benchmarked.

---

## Timing clock

Elapsed durations use:

`time.perf_counter_ns()`

Reasons:

- monotonic
- high resolution
- appropriate for elapsed-time measurement
- unaffected by ordinary wall-clock adjustments

UTC wall-clock timestamps may be recorded only for run identity,
logs, and correlation.

Wall-clock timestamps are not authoritative latency measurements.

---

## Timing boundaries

The benchmark model uses these conceptual boundaries:

T0
Benchmark submits work to Forest.

T1
Forest has completed pre-runtime semantic/control work and reaches
the runtime boundary.

T2
Runtime/model work begins where observable.

T3
Runtime/model work completes.

T4
Forest completes post-runtime work and returns the final result.

Derived measurements:

- forest_pre_runtime_ns = T1 - T0
- runtime_interval_ns = T3 - T1
- forest_post_runtime_ns = T4 - T3
- total_turn_ns = T4 - T0

Where the adapter/runtime exposes trustworthy finer boundaries,
Phase L may additionally record:

- session_lookup_ns
- session_create_ns
- runtime_handoff_ns
- time_to_first_output_ns
- generation_ns
- persistence_ns
- cleanup_ns

A measurement must not claim a finer boundary than the runtime
actually exposes.

---

## Measurement doctrine

### 1. One variable at a time

When comparing two runs, change only the benchmark dimension being
tested whenever practical.

Examples:

- cold versus warm
- new session versus reused session
- Light versus Normal versus Deep Reasoning
- Workshop A versus Workshop B
- Governor absent versus Governor evaluation

### 2. Preserve semantic identity

Benchmark optimization must not silently change:

- Task
- execution_context_id
- Reasoning
- Workshop
- Model Form
- binding
- routing decision
- permissions

A faster result produced by weaker semantics is not a valid
optimization result.

### 3. Distinguish cold and warm state

Cold and warm measurements must never be mixed into one statistic.

Cold means the benchmark explicitly verifies the required
non-resident/non-reused starting condition for that scenario.

Warm means the required runtime/model/session state is already
available and verified.

### 4. Distinguish model residency from session reuse

These are independent:

- model weights may be resident
- runtime session may or may not already exist

Therefore record both.

### 5. Do not average unlike runs

Different Reasoning modes, Workshops, Model Forms, session states,
or residency states belong to different benchmark series.

---

## Run classes

### Deterministic control-path microbenchmark

Purpose:

Measure Forest-only or fake-runtime overhead where possible.

Target:

- 5 warm-up iterations
- 20 measured iterations

Primary statistic:

- median

Also report:

- minimum
- maximum
- mean
- standard deviation
- p90 when sample size supports it

---

### Real cold Small benchmark

Purpose:

Measure first-use cost from a verified cold runtime/model state.

Target:

- minimum 3 measured runs

Each run must independently re-establish and verify the cold
starting condition.

Cold-reset time itself is not included in turn latency unless the
scenario explicitly measures reset cost.

---

### Real warm Small benchmark

Purpose:

Measure steady-state Small runtime cost with model residency already
established.

Target:

- 5 measured runs minimum

Warm-up turns must be recorded but excluded from the measured
series.

---

### Same-session reuse benchmark

Purpose:

Measure the cost difference between runtime-session creation and
reuse.

Target:

- 5 reused-session measured turns

The session identity must remain:

`(execution_context_id, binding_id)`

---

### Recovery benchmark

Purpose:

Measure one certified stale-session replacement.

Target:

- minimum 3 measured recovery trials

The benchmark must verify:

- exactly one replacement
- same frozen semantic turn
- no reroute
- no second replacement

---

### Sustained benchmark

Purpose:

Measure drift across repeated normal turns.

Target:

- at least 10 consecutive measured turns

Record per-turn latency instead of reporting only one aggregate.

---

## Primary statistics

For small benchmark samples, median is the primary comparison
statistic.

Always retain individual run records.

Report:

- n
- median
- minimum
- maximum
- mean
- standard deviation

For sufficiently large series, also report percentile values such
as p90.

Never discard a valid slow run merely because it is inconvenient.

If a run is invalid because the environment violated the declared
benchmark condition, preserve it as an excluded run with a reason.

---

## Environment record

Each real-runtime benchmark series should record at least:

- UTC timestamp
- benchmark phase/scenario
- run ID
- trial number
- CPU count available to the qube
- MemAvailable
- load average
- Hermes service state
- Hermes MainPID
- Ollama residency before
- Ollama residency after
- llama-server presence
- execution_context_id
- binding_id
- Model Form
- Reasoning mode
- Workshop
- session mode
- residency mode
- persistence mode

Where practical also record:

- prompt identifier
- response size
- error/recovery classification

---

## Prompt control

Benchmark prompts are fixtures.

A benchmark series must use the exact same prompt unless prompt
complexity is the dimension under test.

Prompt text should be versioned by a stable prompt ID.

Changing wording creates a new benchmark series.

---

## Workshop benchmark rule

Workshop/tool-surface benchmarks must distinguish:

1. tool/workshop exposure overhead
2. actual tool execution overhead

A prompt that invokes no tool may be used to measure schema/context
surface cost.

Actual tool-use latency must be measured separately.

This prevents tool execution time from being mislabeled as Workshop
prompt-surface overhead.

---

## Reasoning benchmark rule

Light, Normal, and Deep are compared using the same:

- prompt
- Model Form
- Workshop
- runtime residency state
- session condition

Reasoning must remain an independent semantic axis.

Deep does not imply Big.

---

## Resource Governor benchmark rule

Governor performance measurements must not weaken or bypass the
Governor contract.

Measure evaluation overhead separately from runtime/model latency
where possible.

DEFER and DENY tests must remain zero-runtime-effect paths.

---

## Excluded runs

An excluded run must be preserved with:

- run ID
- observed measurements
- exclusion reason

Examples:

- model unexpectedly resident during declared cold test
- session unexpectedly reused during declared new-session test
- unrelated high system load invalidated an environment requirement
- runtime failure unrelated to the scenario

Do not delete failed or excluded observations.

---

## Benchmark record format

Canonical machine-readable records will use JSON Lines:

`*.jsonl`

One line represents one benchmark trial.

Benefits:

- append-friendly
- human-readable
- easy to parse with Python
- resilient to partial experiment interruption
- easy to import into later Forest/Leaf analysis

Human-readable summaries may additionally use Markdown.

---

## Phase 14.11L roadmap

- L.0 Benchmark methodology + environment baseline
- L.1 Forest control-path overhead
- L.2 Cold Small runtime
- L.3 Warm Small runtime
- L.4 Same-session reuse
- L.5 Multi-context / shared-residency
- L.6 Reasoning-level benchmark
- L.7 Workshop / tool-surface benchmark
- L.8 Resource Governor benchmark
- L.9 Recovery-cost benchmark
- L.10 Sustained/repeated-turn benchmark
- L.11 Comparative analysis
- L.12 Optimization recommendations
- L.13 Independent benchmark certification
- L.14 Final L checkpoint

---

## Safety boundary inherited from K

Phase L does not execute Big on the current hardware.

Specifically, do not:

- create a production Big binding
- activate the 119B model
- benchmark the 119B model
- silently substitute Small for an explicit Big request

Big performance belongs to a future environment where Big is
actually provisioned and independently authorized.

---

## Optimization principle

A latency improvement counts only when the same semantic contract
is preserved.

The Forest should become faster by reducing unnecessary work,
not by secretly doing less of the requested work.
