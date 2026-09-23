---
project: The Forest
status: active
created: 2026-08-08
updated: 2026-08-08
tags:
  - the-forest
---
# Qubes OS, PC Hardware, AI Runtime, and Development Environment
## System Snapshot for Bristlecone, Cherry, Maple, and Forest Development

**Snapshot date:** 2026-08-07  
**Purpose:** Give Forest Trees enough hardware, Qubes, runtime, resource, model, and workflow context to make practical development decisions.  
**Important rule for AI readers:** Distinguish host hardware from resources visible inside a qube. Do not assume a device is accessible merely because the physical PC contains it.

---

# 1. Host PC Overview

## Physical host memory

Approximately:

- **32 GB RAM**
- Reported Xen total: approximately **32678 MB**

This host memory is shared between dom0, system/service qubes, Cherry-AI, Maple, Seed-AI, and other running qubes.

Do not assume the full 32 GB is available to one qube.

## CPU

Physical CPU:

**AMD Ryzen 7 3700X 8-Core Processor**

Inside Cherry-AI, the most recent observed allocation was:

- 6 vCPUs
- 1 thread per exposed virtual core
- 6 cores visible to the qube

An earlier work-state script referenced up to 9 vCPUs for Cherry-AI.

vCPU settings may be adjusted by workload.

## GPU

A discrete GPU exists in the broader PC setup, but:

- `nvidia-smi` showed nothing inside Cherry-AI
- `lspci` did not show a usable GPU inside Cherry-AI
- Current AI inference in Cherry-AI is effectively CPU-based

Do not assume GPU acceleration unless passthrough is explicitly configured and verified.

This is one of the largest current AI performance limitations.

---

# 2. Qubes OS Environment

Host OS:

**Qubes OS**

Primary project qubes:

- Cherry-AI
- Maple
- Seed-AI
- dom0

Qubes is used for compartmentalization and security.

---

# 3. Cherry-AI Qube

## Operating system

Inside Cherry-AI:

- Fedora Linux 43
- x86_64

Observed:

```text
NAME="Fedora Linux"
VERSION="43 (Forty Three)"
VERSION_ID=43
```

## Purpose

Cherry-AI is the main AI/runtime qube.

Currently used for:

- Hermes
- Ollama
- Bristlecone
- Newelle
- Local model experiments
- Forest AI runtime work

## Resource configuration

Latest confirmed Qubes preferences:

- `memory`: 8192 MB
- `maxmem`: 16000 MB
- vCPUs: 6 observed in current Xen allocation

Qubes memory balancing can shrink Cherry-AI while idle.

Observed Xen allocations:

- approximately 3571 MB while idle
- approximately 13700 MB under Bristlecone/model load

This confirms dynamic memory expansion is working.

## Dynamic memory behavior

Configured:

```text
memory = 8192 MB
maxmem = 16000 MB
```

Observed idle Xen memory:

~3.5 GB

Observed under AI load:

~13.7 GB

Interpretation:

- Qubes/qmemman reclaimed unused memory while Cherry-AI was idle.
- It returned memory when Ollama/model inference demanded it.
- Memory balancing is currently functioning.

## Swap

Observed Cherry-AI swap:

- approximately **8.8 GiB**
- often **0 B used** during successful Bristlecone model loading

Swap is not equivalent to RAM.

Heavy swapping will severely hurt model response speed.

---

# 4. Maple Qube

## Purpose

Maple is a personal development/project qube.

Used for:

- Git
- Development
- Repository work
- Project files
- Training preparation
- General technical work

## Resource configuration

Confirmed:

- `memory`: 800 MB
- `maxmem`: 8000 MB
- `vCPUs`: 4

Maple can grow dynamically when needed.

During heavy Cherry-AI model work, Maple should remain light or be shut down if host RAM becomes constrained.

---

# 5. Seed-AI Qube

Seed-AI is a clone of Cherry-AI intended for:

- Light training
- Experimental model work
- Isolated Seed model workflows

Recorded Forest Seed Mixed Mode target:

- initial memory: 2048 MB
- maxmem: 6000 MB
- vCPUs: 2

This may be revised as the Base Seed model lab becomes real.

---

# 6. dom0 Constraints

dom0 is the Qubes administrative domain.

Important working constraints:

- No normal copy/paste
- No normal screenshots
- Commands are often manually typed
- Keep dom0 command blocks short and safe
- Avoid using dom0 as a general development workspace
- Do not put AI models, project corpora, or broad agent tooling in dom0

dom0 should primarily manage:

- Qube properties
- Qube lifecycle
- Resource allocation
- Device assignment
- qrexec policy
- Qubes-specific administration

---

# 7. Current AI Runtime Software

## Hermes Agent

Installed:

**Hermes Agent v0.19.1**

Install directory:

`/home/user/.hermes/hermes-agent`

Hermes Python runtime:

**Python 3.11.15**

OpenAI SDK:

**2.24.0**

System Python:

**Python 3.14.6**

Hermes command:

`/home/user/.local/bin/hermes`

## Ollama

Installed:

**Ollama 0.32.5**

Command:

`/usr/local/bin/ollama`

Known models include:

- `qwen3:8b`
- `gemma4:12b`
- `qwen3.5:4b`
- `bristlecone-qwen35:4b-64k`

## Newelle

Installed as Flatpak:

- App ID: `io.github.qwersyk.Newelle`
- Version: **1.4.6**
- License: **GPL-3.0-or-later**
- Installed size: approximately **937.7 MB**
- Runtime: GNOME Platform 50

Observed effective Flatpak permissions:

```text
shared=network;ipc;
sockets=wayland;pulseaudio;fallback-x11;
devices=dri;
```

Session bus:

`org.gnome.Shell.Screencast=talk`

No broad filesystem Flatpak override was shown.

## Development tools

Installed:

- Git 2.55.0
- Python 3.14.6
- Podman 5.8.4

---

# 8. Current Bristlecone Runtime

Hermes profile:

`bristlecone`

Wrapper command:

`bristlecone`

Profile directory:

`~/.hermes/profiles/bristlecone`

Workspace:

`~/The-Forest/bristlecone`

Local Bristlecone API:

`http://127.0.0.1:8643/v1`

Advertised API model:

`bristlecone`

The API is bound to localhost.

Meaning:

- Accessible inside Cherry-AI
- Not automatically accessible from other qubes
- Not automatically remotely accessible
- API key still protects local access

---

# 9. Bristlecone Model

Current custom Ollama model:

`bristlecone-qwen35:4b-64k`

Observed metadata:

```text
architecture: qwen35
parameters: 4.7B
context length: 262144
embedding length: 2560
quantization: Q4_K_M
requires: 0.17.1
```

Capabilities:

- completion
- vision
- tools
- thinking

Configured parameters:

- temperature: 1
- top_k: 20
- top_p: 0.95
- num_ctx: 64000
- presence_penalty: 1.5

License:

Apache License 2.0

---

# 10. Bristlecone Runtime Measurements

During a real Bristlecone request:

Observed `ollama ps`:

- Model: `bristlecone-qwen35:4b-64k`
- Loaded size: approximately **5.6 GB**
- Processor: **100% CPU**
- Context: **64000**
- Keep-alive: several minutes after use

Observed Cherry-AI memory:

- Total visible RAM: approximately **13 GiB**
- Used: approximately **6.8 GiB**
- Available: approximately **6.3 GiB**
- Swap used: **0 B**

Conclusion:

The model fits in Cherry-AI with Qubes dynamic memory expansion.

Primary bottleneck is currently **CPU inference speed**, not RAM exhaustion.

---

# 11. Earlier Model Inventory

## qwen3:8b

- Size: approximately 5.2 GB
- Hermes-reported context: 40,960 tokens

This failed as Bristlecone's main Hermes model because Hermes requires at least 64,000 tokens for the primary agent model.

It remains useful for direct Ollama use, specialist tasks, non-Hermes workloads, and future routing experiments.

## gemma4:12b

- Size: approximately 7.6 GB

This is significantly heavier than the current Bristlecone model.

It should not be kept loaded casually alongside several other large-context models on a 32 GB host.

Potential future use:

- Multimodal review
- Second opinion
- Specialist reasoning
- Experimental tasks

---

# 12. Current Model Strategy

Preferred near-term arrangement:

```text
Bristlecone
→ Qwen3.5 4B 64K model
→ mature working Treewright

Base Seed model
→ smaller raw/base pretrained model
→ protected training laboratory

Optional specialist model
→ small coding/reviewer model
→ loaded on demand
```

The number of Tree identities does not equal the number of loaded models.

Multiple Trees may share one model through separate profiles.

---

# 13. Multi-Model Resource Planning

With 32 GB host RAM, practical behavior depends on:

```text
model size
× context size
× simultaneous requests
× number of loaded models
× active qubes
```

Likely practical:

- Several idle Tree profiles
- One main 4B 64K model
- One smaller Seed model
- One additional small specialist model loaded on demand
- Sequential inference

Less practical:

- Three large models with large contexts generating simultaneously
- Qwen 8B + Gemma 12B + Bristlecone 4B all loaded with large contexts
- Heavy local training plus multiple active inference models

The current main concurrency limitation may be CPU more than RAM.

---

# 14. CPU Speed Considerations

Current Bristlecone inference is CPU-only.

Symptoms:

- 100% CPU in `ollama ps`
- Model loaded successfully
- RAM available
- No swap
- Slow agent-style responses

Reasons:

- Qwen3.5 4.7B model
- 64K context
- Hermes system prompt
- Tool schemas
- Skills
- CPU-only generation

Potential speed improvements:

- Reduce prompt/tool overhead
- Disable unused tools
- Disable unused skills
- Use low/no reasoning for routine tasks
- Keep model loaded
- Increase vCPU allocation where safe
- Use a smaller fast model for simple work
- Use a GPU or separate model server later

---

# 15. Hermes Prompt-Size Observation

A recent Bristlecone prompt-size screen showed approximately:

System prompt total:

**23,206 B**

Major blocks:

- Skills index: approximately 6,886 B
- Memory: 0 B
- User profile: 0 B

Prompt tiers:

- Stable identity/guidance/skills: approximately 19,324 B
- Context / AGENTS.md / cwd files: approximately 3,784 B
- Volatile memory/profile/timestamp: approximately 94 B

Tool schemas:

**44,800 B**  
**27 tools**

Large tool/schema groups included:

- session_search
- browser
- file
- skills
- terminal
- delegation
- memory
- clarify
- code_execution
- tts
- todo
- vision

Bristlecone's startup prompt and tool schemas are relatively large for a CPU-only 4B model.

Optimization opportunity:

- Remove tools he does not need
- Trim skill index
- Keep essential development tools
- Avoid unrelated skills
- Use separate profiles/toolsets for different modes

---

# 16. Known Hermes Optimization Benchmarks

Earlier Bristlecone/Hermes tests with reasoning `none`:

`file,terminal`

~41 seconds

`file,terminal,todo`

1 minute 49.64 seconds

`file,terminal,skills`

2 minutes 42.40 seconds

`file,terminal,skills,todo`

2 minutes 49.16 seconds

Conclusion:

Tool-schema size and skill overhead materially affect response latency on the current CPU-only setup.

---

# 17. Newelle Performance History

Earlier stripped Newelle tests:

- Run 1: output after 5 minutes 25.65 seconds
- Run 2: stopped after roughly 15 minutes with no answer
- Run 3: welcome/suggestion prompts after 5 minutes 42.23 seconds but no Bristlecone answer

Conclusion:

The Newelle path has historically been significantly slower than direct Hermes on this hardware/configuration.

Current strategy:

- Keep Hermes as primary agent runtime
- Use Newelle as optional Bark/interface
- Avoid duplicate prompts/tools
- Trim Newelle and Hermes overlap

---

# 18. Newelle Optimizations Already Used

Previously disabled in Newelle to reduce duplication:

- Agent
- File Operations
- RAG
- Read Websites
- Search
- Execute Command
- Generate Image
- Long-Term Memory
- Web Search
- Wake-word
- Auto chat-name generation
- Parallel Tool Execution

Text-to-Speech was kept enabled.

Newelle should not duplicate Hermes tools unless there is a clear reason.

---

# 19. Hermes Toolset Optimization History

A trimmed Bristlecone profile was previously benchmarked.

Earlier API-server prompt:

- system prompt: 17,727 B
- tool schemas: 40,712 B
- 25 tools

Later final trimmed API-server prompt:

- system prompt: 16,864 B
- tool schemas: 28,188 B
- 12 tools

This showed that trimming toolsets can significantly reduce prompt overhead.

Relevant direction:

> Restore a Bristlecone-specific minimal toolset rather than leaving all 27 current tools enabled.

---

# 20. Recommended Bristlecone Essential Toolset

Likely essentials:

- file
- terminal
- skills
- memory
- todo/task tracking
- code execution where needed
- limited session search if useful

Optional/on-demand:

- browser
- vision
- TTS
- delegation
- extra messaging platforms
- unrelated cloud tools

Goal:

Keep the default working prompt small, then activate specialist tools only when required.

---

# 21. Reasoning Modes

## Quick Mode

For simple edits, routine checks, short questions, and low-risk work.

Use:

- no reasoning or low reasoning
- minimal toolset
- smaller/faster model when possible

## Deep Mode

For architecture, debugging, complex coding, security review, training design, and multi-document comparison.

Use:

- higher reasoning
- full development toolset
- larger context or stronger model

Long-term goal:

Automatically switch modes based on task complexity, then return to Quick Mode afterward.

---

# 22. Model Keep-Alive

Earlier Ollama keep-alive behavior was set to approximately **15 minutes** for Bristlecone/Pine Cone workflows.

A keep-alive avoids paying the model-load cost on every prompt.

Recommended:

- Keep Bristlecone loaded during active sessions
- Allow unload during idle periods
- Do not keep every specialist model resident unnecessarily

---

# 23. Qubes Work-State Scripts

## forest-normal-mode

Earlier verified target:

Cherry-AI:
- memory: 8192 MB
- maxmem: 16000 MB
- 9 vCPUs

Maple:
- memory: 800 MB
- maxmem: 8000 MB
- 4 vCPUs

## pine-cone-mode

Restores Ollama and Hermes, keeps the model unloaded until first use, and supports keep-alive behavior.

## maple-seed-mode

Stops Newelle/Hermes, unloads model, frees memory, and prioritizes Maple training.

## forest-mixed-mode

Used when 2–3 qubes are active for mixed review/training.

## Forest Seed Mixed Mode

Recorded target:

Maple:
- 12288 MB initial
- 16000 MB max
- 4 vCPUs

Cherry-AI:
- 6144 MB initial
- 9000 MB max
- 3 vCPUs

Seed-AI:
- 2048 MB initial
- 6000 MB max
- 2 vCPUs

This target may need revision now that Bristlecone uses a 64K model.

---

# 24. i3 / Desktop Environment

Qubes desktop:

- XFCE + i3

Terminal:

- kitty

Shell:

- zsh
- oh-my-zsh
- powerlevel10k

Additional desktop tools:

- rofi
- fastfetch
- nitrogen
- picom compositor
- glx backend

Transparency has been configured for Maple and dom0 kitty through picom rules.

---

# 25. i3 Work-State Hotkeys

With Num Lock OFF:

- Numpad 1 → Forest Normal
- Numpad 2 → Pine Cone
- Numpad 3 → Maple Seed
- Numpad 4 → Forest Mixed
- Numpad 5 → intended Seed Mixed Mode

---

# 26. Desktop / Media Context

Past plans include:

- Separate media modules for Spotify/music
- Separate module for YouTube/video
- Local audio/video playback integration
- mpv selected as preferred media player
- Rofi-based media controls later
- Customized top-bar behavior

Future Forest Bark interfaces should fit the existing desktop rather than replace it with a generic full-screen UI.

---

# 27. File and Screenshot Constraints

## Cherry-AI and Maple

- Normal copy/paste
- Normal screenshot/image sharing
- Longer terminal commands are practical

## dom0

- No normal copy/paste
- No normal screenshot workflow
- Commands should be concise and manually typable

---

# 28. Cross-Qube File Transfer

Do not assume a file in Maple exists in Cherry-AI.

Use Qubes-supported transfer mechanisms.

A real example occurred when the Bristlecone Seed ZIP existed in Maple and had to be copied into Cherry-AI before planting.

---

# 29. Bristlecone Seed Installation Snapshot

Seed package:

`BRISTLECONE-PINE-NEWELLE-SEED-0.0.2.zip`

The package was:

- copied into Cherry-AI
- extracted
- verified with SHA256SUMS
- planted successfully

Created:

`~/.hermes/profiles/bristlecone`

and:

`~/The-Forest/bristlecone`

A private API key was generated locally.

API:

`http://127.0.0.1:8643/v1`

The health endpoint passed.

The models endpoint advertises:

`bristlecone`

---

# 30. Bristlecone API Behavior

Observed health response:

```json
{
  "status": "ok",
  "platform": "hermes-agent",
  "version": "0.19.1"
}
```

Newelle connection:

- Provider: OpenAI API
- Endpoint: `http://127.0.0.1:8643/v1/`
- Model: `bristlecone`
- API key: private locally generated key

Do not confuse this with Ollama backend:

`http://127.0.0.1:11434/v1`

Correct chain:

```text
Newelle
→ Bristlecone Hermes API :8643
→ Bristlecone profile
→ Ollama :11434
→ bristlecone-qwen35:4b-64k
```

---

# 31. Localhost Security Boundary

`127.0.0.1` binds the API locally inside Cherry-AI.

It is not automatically reachable from Maple, dom0, another computer, or the internet.

Future remote access should require explicit architecture and authentication.

Do not bind Bristlecone to `0.0.0.0` casually.

---

# 32. Current Primary Bottlenecks

Most important performance bottlenecks:

1. CPU-only inference
2. 64K context size
3. Large Hermes tool schemas
4. Large skills index
5. Duplicate Newelle/Hermes capabilities
6. Long system prompt
7. Model loading when keep-alive expires
8. Too many simultaneously active tools/models

RAM is currently less critical than CPU for the working 4B Bristlecone model.

---

# 33. Best Near-Term Optimization Plan

Recommended order:

1. Confirm Bristlecone direct Hermes response is stable
2. Reduce Hermes tools from current 27 toward a minimal Bristlecone toolset
3. Reduce skill index to development-relevant skills
4. Disable duplicate Newelle tools/prompts
5. Use low/no reasoning for normal conversation
6. Keep Bristlecone loaded during work sessions
7. Test 6 vs 8 vCPU performance
8. Measure response latency after each change
9. Add a smaller fast model only after prompt/tool optimization
10. Add Base Seed model separately
11. Avoid loading Gemma 12B concurrently unless there is enough headroom
12. Consider GPU/model-server hardware only after measuring the optimized CPU path

---

# 34. Hardware Upgrade Guidance

Current system is adequate for:

- Forest prototype
- Bristlecone
- Spirit prototype
- Local memory/retrieval
- Cherry/Maple profile development
- Base Seed experiments
- TTS
- Sequential multi-model work

A future comfortable full single-user Forest target may be:

- 64 GB RAM
- modern 8–16 core CPU
- 16 GB+ GPU VRAM
- fast SSD

A heavier multi-user/development server target may be:

- 64–128 GB RAM
- 24 GB+ VRAM
- dedicated model server
- separate NAS/Log Cabin storage

These are targets, not current requirements.

---

# 35. Preferred Future Architecture

A scalable Forest should avoid tying one model to every Tree.

```text
Trees
├── Bristlecone
├── Cherry
├── Maple
├── Cedar
└── future Trees
       ↓
Forest Model Router
├── Fast general model
├── Deep reasoning model
├── Coding model
├── Reviewer model
├── Vision model
└── Base Seed lab
```

This allows many Tree identities with only a few loaded model engines.

---

# 36. Second-PC / NAS Direction

Another PC is intended for NAS/storage and possible future compute use.

Long-term possibility:

```text
Main Qubes workstation
├── Trees
├── Spirit
├── permissions
├── private user interaction
└── Bark

Separate compute/server machine
├── Ollama
├── GPU
├── larger models
└── model routing

NAS / Log Cabin
├── archives
├── Logs
├── backups
├── models
└── Seed Vaults
```

This could scale The Forest without replacing the current workstation.

---

# 37. Software Preference

General project preference:

- Free/open-source where practical
- Self-hostable
- Local-first
- Avoid subscriptions
- Prefer one-time purchases over recurring fees
- Preserve user ownership
- Keep cloud services optional

---

# 38. Autocorrect Note

In technical conversations, the user's phone sometimes changes:

**Qubes** → **wine**

When "wine" appears in a Qubes-related technical context, consider whether "Qubes" was intended.

---

# 39. Current Operational Summary

At this snapshot:

- Qubes host has ~32 GB RAM
- Cherry-AI can grow to ~16 GB
- Maple can grow to ~8 GB
- Cherry-AI currently uses CPU inference
- Bristlecone runs a Qwen3.5-class 4.7B Q4_K_M model
- Bristlecone context is 64K
- Loaded Bristlecone runtime observed ~5.6 GB
- Cherry-AI expanded to ~13 GB under load
- No swap was needed during that observed load
- Hermes 0.19.1 is active
- Ollama 0.32.5 is active
- Newelle 1.4.6 is installed
- Bristlecone API is local-only on port 8643
- Biggest speed opportunity is trimming Hermes/Newelle overhead and unnecessary tools/skills

---

# 40. Guidance for Future Trees Reading This File

Before suggesting resource changes:

1. Check current `free -h`
2. Check `ollama ps`
3. Check current Qubes preferences
4. Check whether models are actually loaded
5. Check whether swap is being used
6. Check CPU usage
7. Check tool/prompt size
8. Distinguish host RAM from qube RAM
9. Avoid assuming GPU access
10. Prefer measured changes over guesses

Before changing Qubes resource settings:

- Keep dom0 commands concise
- Confirm the target qube is shut down when required
- Preserve known-good work-state scripts
- Avoid starving dom0/system qubes
- Do not give every qube its maximum allocation simultaneously

Before adding a model:

- Record model size
- Record context requirement
- Record license
- Record quantization
- Record role
- Record expected memory
- Measure actual loaded memory after first run

Before declaring success:

- Verify the API
- Verify the model
- Verify context
- Verify memory
- Verify no swap pressure
- Verify the correct Tree profile is responding

When all required checks pass:

**Pine is fine.**
