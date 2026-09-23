# Bristlecone Pine Performance Optimization — Continuity & Next Steps

**Date:** 2026-08-06  
**Environment:** Qubes OS 4.3.1  
**Primary AI Qube:** `Cherry-AI`  
**Primary user/work Qube:** `Maple`  
**Hermes profile:** `bristlecone`  
**Model:** `bristlecone-qwen35:4b-64k`  
**Runtime:** Ollama + Hermes Agent  
**Current inference mode:** CPU-only

---

## 1. Current Goal

Improve Bristlecone Pine's real-world response speed without weakening the Qubes security model or removing the capabilities needed for its Treewright role.

The main performance problem currently being investigated is:

> **The first Hermes response after Cherry-AI is restarted can take about 5–6+ minutes, while later responses are much faster.**

Direct Ollama testing now shows that the model itself only takes about **10 seconds to cold-load**, so the several-minute delay is most likely caused by Hermes processing a very large initial agent prompt/context rather than Ollama loading the model.

---

# 2. Current Optimization Plan

## Next Steps — in order

- [ ] **1. Measure the current Hermes prompt breakdown**
  ```bash
  hermes -p bristlecone prompt-size
  ```
  Record:
  - system prompt size
  - tool schema size
  - skills index size
  - total approximate prompt/context overhead

- [ ] **2. Build a lean Quick Bristlecone configuration**
  - Keep only tools needed for ordinary work, coding, files, memory, continuity, and basic debugging.
  - Avoid loading broad/specialized tool schemas into routine requests.
  - Keep skills installed but disable unnecessary ones.
  - Target a much smaller first-turn prompt than the current setup.

- [ ] **3. Keep a Deep Bristlecone configuration**
  - Preserve the full Treewright feature set for complex work.
  - Use it for:
    - architecture
    - difficult debugging
    - large multi-file work
    - research-heavy tasks
    - risky or complex changes
    - long-context work
  - Deep Mode can retain the full **64K context**.

- [ ] **4. Reduce Quick Mode's context window**
  - Current model context: **64K**
  - Proposed Quick Mode starting target: approximately **32K**
  - Deep Mode remains **64K**
  - Benchmark before deciding whether 32K should be reduced further.

- [ ] **5. Modify `forest-normal-mode` so it does not restart Cherry-AI unnecessarily**
  - Current mode switching can restart Cherry-AI.
  - Restarting the qube destroys the warm model/KV/prefix state.
  - If Cherry-AI is already running with the correct resources, Normal Mode should ideally leave it running.
  - Only restart when resource changes actually require it.

- [ ] **6. Consider automatic Bristlecone warm-up after a required restart**
  - After Cherry-AI boots and Hermes/Ollama are ready, send a tiny background warm-up request.
  - This would make the expensive initial Hermes prompt evaluation happen before the user needs the first real answer.
  - Only add this after Quick/Deep prompt optimization so we do not hide an avoidable performance problem.

- [ ] **7. Re-run cold vs. warm benchmarks**
  Compare:
  - Direct Ollama cold request
  - Direct Ollama warm request
  - Hermes Quick cold first request
  - Hermes Quick warm request
  - Hermes Deep cold first request
  - Hermes Deep warm request

- [ ] **8. Decide final mode defaults from measured results**
  Suggested end state:
  - **Quick Mode:** low reasoning, smaller context, lean toolset, routine/low-risk work
  - **Deep Mode:** high reasoning, larger context, broader tools, difficult Treewright work

---

# 3. Performance Evidence Collected

## Direct Ollama Benchmark

A direct request was sent to:

```text
http://127.0.0.1:11434/api/generate
```

Prompt:

```text
Reply with only: OK
```

### Cold run

```text
TOTAL:       14.2 sec
MODEL LOAD:  10.3 sec
PROMPT EVAL: 1.4 sec
GENERATION:  2.5 sec
SPEED:       3.14 tok/s
```

### Warm run

```text
TOTAL:       3.5 sec
MODEL LOAD:  0.5 sec
PROMPT EVAL: 0.4 sec
GENERATION:  2.6 sec
SPEED:       3.08 tok/s
```

## Important conclusion

The model's cold load is only about **10 seconds**.

Therefore, the **5–6 minute first-message delay in Hermes is not caused primarily by Ollama loading the model from disk**.

---

# 4. Hermes Cold-Start Evidence

During a slow first Hermes request, Hermes showed messages similar to:

```text
waiting on bristlecone-qwen35:4b-64k
210s with no output yet
```

At the same time, `ollama ps` showed:

```text
bristlecone-qwen35:4b-64k
SIZE:      5.6 GB
PROCESSOR: 100% CPU
CONTEXT:   64000
```

Hermes also showed approximately:

```text
14.1K / 64K
```

before or during routine requests.

This strongly suggests that Hermes is sending a large initial prompt made up of:

- system instructions
- tool schemas
- skill index
- memory/context instructions
- agent behavior instructions
- session/project context

The CPU then has to evaluate that large prefix before producing the first visible token.

Once that prefix/model state is warm, later responses become dramatically faster.

---

# 5. Approximate Real-World Hermes Timing Observed

A series of simple requests such as:

```text
reply to this message with just ok
```

produced roughly:

```text
~6 minutes
~1 minute 30 seconds
~6 minutes 40 seconds
~40 seconds
```

The exact times varied, but the pattern was consistent:

> **Cold/first requests were extremely slow; later requests were much faster.**

This is more important than any single timing result.

---

# 6. Hardware / Qubes Context

## Host

- CPU: AMD Ryzen 7 3700X
- Xen-visible CPUs: 8
- Host RAM: about 32 GB
- Host GPU: AMD Radeon RX 580

## Cherry-AI

- AI inference is currently **CPU-only**
- No GPU is exposed to Cherry-AI
- Normal baseline:
  - memory: 8192 MB
  - maxmem: 16000 MB
  - vCPUs: 9

## Maple

Normal baseline:

- memory: 800 MB
- maxmem: 8000 MB
- vCPUs: 4

Important note:

> Xen vCPUs are schedulable virtual CPUs. Assigning more total vCPUs than physical cores is allowed, but simultaneous CPU-heavy qubes still compete for the same physical CPU resources.

---

# 7. Ollama Configuration Already Completed

## Model

```text
bristlecone-qwen35:4b-64k
```

## Context

```text
64000
```

## Keepalive

Configured:

```text
OLLAMA_KEEP_ALIVE=15m
```

Behavior verified:

- Model loads on first request.
- It stays loaded for approximately 15 idle minutes.
- It unloads afterward.
- Keepalive survives a Cherry-AI restart because it is configured in the Ollama systemd service.
- A full Cherry-AI shutdown still removes the loaded model from RAM, so keepalive cannot preserve warm state across qube shutdown.

---

# 8. Hermes Startup / Profile Repair

A Hermes profile-launch problem was diagnosed and repaired.

## Symptoms

Running:

```bash
hermes -p bristlecone
```

initially returned:

```text
Hermes isn't configured yet -- no API keys or providers found.
```

There were also two launcher paths:

```text
/home/user/.local/bin/hermes
/home/user/.hermes/hermes-agent/hermes
```

Directly executing the repository script produced:

```text
ModuleNotFoundError: No module named 'dotenv'
```

because it was being launched outside the Hermes virtual environment.

## Working service launcher

The Hermes gateway systemd service uses:

```text
WorkingDirectory=/home/user/.hermes/hermes-agent
ExecStart=/home/user/.hermes/hermes-agent/venv/bin/python /home/user/.hermes/hermes-agent/hermes -p bristlecone gateway run
```

## Final cause of the profile issue

A stray configuration typo/character in the Bristlecone configuration was found and corrected.

After correction, Hermes successfully launched interactively and showed:

```text
Profile: bristlecone
Model: bristlecone-qwen35:4b-64k
```

Do **not** re-run `hermes setup` unless a new problem proves it is necessary.

---

# 9. Hermes Tool Optimization Completed So Far

The Hermes prompt/tool load was reduced significantly.

## Before tool cleanup

CLI measurement was approximately:

```text
System prompt: 26,238 B
Tool schemas:  43,090 B
Tools:         16
Skills index:  3,680 B
```

Large tool schemas included:

```text
computer_use
session_search
file
skills
terminal
memory
clarify
code_execution
tts
vision
```

## After cleanup

Approximately:

```text
System prompt: 20,994 B
Tool schemas:  31,532 B
Tools:         14
```

Later, Cron was intentionally retained, so the interactive CLI now shows approximately:

```text
15 tools
```

This is intentional.

## API server optimization

Before:

```text
System prompt: 17,727 B
Tool schemas:  40,712 B
Tools:         25
```

After:

```text
System prompt: 16,864 B
Tool schemas:  28,188 B
Tools:         12
```

That was roughly:

- **31% smaller tool schemas**
- **52% fewer API tools**

---

# 10. Current Hermes Tool Philosophy

Keep tools that directly support Bristlecone's Treewright role.

Useful core capabilities include:

```text
clarify
code_execution
context_engine
cronjob
file
memory
session_search
skills
terminal
vision
web
```

Cron was intentionally kept because:

- its idle cost is low
- it can schedule recurring or delayed Forest work
- only actual scheduled AI jobs create meaningful compute cost

Hermes TTS and computer-use toolsets were disabled from the lean CLI configuration.

Newelle TTS remains enabled by user preference.

---

# 11. Skills Optimization

Hermes originally showed:

```text
31 enabled skills
```

The user began trimming them and the latest screenshot showed:

```text
28 skills
```

Skills are lower priority than tools because the skill index is relatively small and full skill instructions are generally loaded only when needed.

## Skills currently considered useful for Bristlecone

Strong candidates to keep:

```text
hermes-agent
hermes-agent-skill-authoring
opencode
codex
codebase-inspection
architecture-diagram
excalidraw
evaluating-llms-harness
huggingface-hub
llama-cpp
grounded-citations
plan
dogfood
python-debugpy
node-inspect-debugger
requesting-code-review
simplify-code
spike
systematic-debugging
test-driven-development
```

GitHub skills can remain enabled if actively used:

```text
github-auth
github-code-review
github-issues
github-pr-workflow
github-repo-management
```

## Skills considered optional / disable-for-now

```text
claude-code
weights-and-biases
serving-llms-vllm
```

Reasoning:

- **OpenCode** fits the local/open/provider-flexible Forest architecture well.
- **Codex** can be retained as an alternate coding/review worker.
- **Claude Code** is largely redundant unless Anthropic tooling is intentionally added.
- **Weights & Biases** may become useful later for serious Seed experiment tracking.
- **vLLM serving skill** is not currently needed because inference is using Ollama.

Do not uninstall unnecessary skills yet. Prefer **disabled** so they can be re-enabled later.

---

# 12. Current Forest Qubes Modes

## Numpad 1 — `forest-normal-mode`

Baseline:

```text
Cherry-AI:
  memory  = 8192
  maxmem  = 16000
  vcpus   = 9

Maple:
  memory  = 800
  maxmem  = 8000
  vcpus   = 4
```

Current issue:

> The script currently restarts qubes, which destroys warm Bristlecone state.

A future optimization should make Normal Mode avoid restarting Cherry-AI when the qube is already running with suitable resources.

## Numpad 2 — `pine-cone-mode`

Bristlecone-focused mode.

## Numpad 3 — `maple-seed-mode`

Maple-focused Seed training mode.

## Numpad 4 — `forest-mixed-mode`

Current resource target:

```text
Cherry-AI:
  memory  = 8192
  maxmem  = 12000
  vcpus   = 4

Maple:
  memory  = 6144
  maxmem  = 12000
  vcpus   = 4
```

Numpad 1–4 bindings have been tested successfully.

## Numpad 5 — future Seed-AI mode

Still **PENDING**.

Planned architecture:

```text
Maple
  = primary training workspace

Cherry-AI
  = runs a progressed Cherry Seed teacher/reviewer model

Seed-AI
  = runs the newest/smallest Seed under training
```

Bristlecone should **not** be active inside Numpad 5.

Proposed resources:

```text
Maple:
  memory  = 12288
  maxmem  = 16000
  vcpus   = 4

Cherry-AI:
  memory  = 6144
  maxmem  = 9000
  vcpus   = 3

Seed-AI:
  memory  = 2048
  maxmem  = 6000
  vcpus   = 2
```

Do not mark Numpad 5 or Seed-AI setup complete until it is actually created and tested.

---

# 13. Bristlecone Gateway / Autostart Status

Cherry-AI autostarts.

Ollama:

```text
system service
/usr/local/bin/ollama serve
```

Hermes gateway:

```text
~/.config/systemd/user/hermes-bristlecone.service
```

It has been tested as an autostarting user service.

Important service command:

```bash
systemctl --user status hermes-bristlecone.service
```

Restart:

```bash
systemctl --user restart hermes-bristlecone.service
```

---

# 14. Most Important Current Diagnosis

The performance problem has now been narrowed substantially.

## Not the main problem

```text
Ollama cold model loading
```

Measured cold-load time:

```text
~10 seconds
```

That is not enough to explain a 5–6 minute first response.

## Most likely problem

```text
Hermes cold prompt/context prefill
```

Hermes is starting some conversations with around:

```text
~14K tokens already in context
```

while Bristlecone is running a:

```text
64K context window
```

On CPU-only inference, evaluating that large initial prompt can take several minutes.

## Why later messages improve

After the initial large prompt is evaluated:

- model is already loaded
- prefix/KV state is warm
- repeated context can be reused more efficiently
- follow-up messages require less initial work

This matches the observed behavior.

---

# 15. Target End State

The intended performance architecture is:

## Quick Mode

For routine, low-risk work:

```text
lower reasoning
smaller context
lean tool schemas
focused skills
fast startup
preserve project continuity
```

Likely starting context target:

```text
~32K
```

## Deep Mode

For complex/risky/large work:

```text
higher reasoning
64K context
broader tools
full Treewright capability
architecture/debugging/research workflows
```

Quick and Deep aliases/configuration should **not be marked complete until both are created and tested**.

---

# 16. Immediate Resume Point

When continuing this project in another chat or AI, begin here:

1. Run:
   ```bash
   hermes -p bristlecone prompt-size
   ```

2. Record the current post-skill-cleanup prompt sizes.

3. Design the **Quick Bristlecone toolset** from that measurement.

4. Create a Quick configuration with a smaller context target.

5. Preserve the existing Bristlecone configuration as the basis for **Deep Mode**.

6. Benchmark cold and warm first-response times.

7. Modify `forest-normal-mode` so it avoids restarting Cherry-AI unnecessarily.

8. Only after those changes, consider automatic background warm-up.

---

# 17. Rules for Continuing the Optimization

- Do not weaken Qubes isolation for performance.
- Keep:
  ```text
  Cherry-AI -> sys-firewall -> sys-net -> Internet
  ```
- Do not assume a change is complete until it is tested.
- In dom0, keep commands short because commands are manually typed.
- In Maple and Cherry-AI, longer copy/paste command blocks are acceptable.
- Prefer disabling unnecessary Hermes skills instead of uninstalling them.
- Do not run `hermes setup` unless troubleshooting proves configuration is actually missing.
- Treat local CLI output as more authoritative than assumptions about Hermes behavior.
- Measure before changing major performance settings.
- Preserve the ability to restore the known-working baseline.

---

## One-Sentence Continuity Summary

**Bristlecone's several-minute first-response delay has been narrowed from a general CPU/Ollama problem to a likely Hermes cold-context/prompt-prefill bottleneck: direct Ollama cold-loads in ~14 seconds total, while Hermes starts with roughly 14K tokens of agent context, so the next phase is to build a lean Quick Mode, retain a 64K Deep Mode, stop unnecessary Cherry-AI restarts, and benchmark the results.**
