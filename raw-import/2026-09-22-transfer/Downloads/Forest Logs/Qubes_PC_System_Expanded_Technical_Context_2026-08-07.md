---
title: Qubes OS, Primary PC, AI Runtime, and Home Infrastructure — Expanded Technical Context
aliases:
  - Qubes System Context
  - PC Technical Handoff
  - Forest Workstation Context
tags:
  - qubes
  - pc
  - hardware
  - cherry-ai
  - maple
  - hermes
  - ollama
  - bristlecone
  - nas
  - networking
status: active-reference
updated: 2026-08-07
---

# Qubes OS, Primary PC, AI Runtime, and Home Infrastructure — Expanded Technical Context

> [!important]
> This is a machine/environment continuity packet for an AI or human helping with the user's Qubes workstation, Cherry-AI, Bristlecone Pine, local AI stack, desktop customization, storage, NAS, or networking.
>
> Separate **confirmed values** from **planned/target values**. Do not treat proposed performance settings as already applied.

---


# 0. Latest Machine Delta — 2026-08-07

> [!important]
> This section contains the newest machine state and should override conflicting older snapshots in this file.

## Immediate unresolved issue: connection error after restart

After a nap followed by a reset/restart, the user reported a **connection error** involving the current Bristlecone/Newelle/Hermes path.

Do not assume the earlier gateway/profile repair means this new error is the same issue or is already fixed.

First-line non-destructive checks inside `Cherry-AI`:

```bash
systemctl status ollama
systemctl --user status hermes-bristlecone.service
ollama ps
pgrep -af 'ollama|llama-server|newelle|hermes|python'
```

If Hermes is not healthy:

```bash
systemctl --user restart hermes-bristlecone.service
```

Do **not** rerun `hermes setup` simply because there is a connection error. The known working profile/service path was already repaired previously.

## Current performance priority

The active goal is:

> Make Bristlecone/Hermes and the optional Newelle path as fast as possible while preserving Qubes security, Treewright capability, rollback paths, and local-first behavior.

Hermes remains primary. Newelle is again worth testing/optimizing, but should remain experimental until it can demonstrate reliable response delivery and acceptable latency.

### Confirmed Hermes prompt/tool measurements

```text
CLI before:
  System prompt: 26,238 B
  Tool schemas:  43,090 B
  Tools:         16
  Skills index:  3,680 B

Lean CLI:
  System prompt: 20,994 B
  Tool schemas:  31,532 B
  Tools:         ~14
  Later interactive count: ~15 with Cron retained

API server before:
  System prompt: 17,727 B
  Tool schemas:  40,712 B
  Tools:         25

API server final verified:
  System prompt: 16,864 B
  Tool schemas:  28,188 B
  Tools:         12
```

API-server result:

- ~31% smaller tool schemas.
- ~52% fewer tools.

### Direct Ollama benchmark

```text
Cold:
TOTAL:       14.2 sec
MODEL LOAD:  10.3 sec
PROMPT EVAL: 1.4 sec
GENERATION:  2.5 sec
SPEED:       3.14 tok/s

Warm:
TOTAL:       3.5 sec
MODEL LOAD:  0.5 sec
PROMPT EVAL: 0.4 sec
GENERATION:  2.6 sec
SPEED:       3.08 tok/s
```

This continues to indicate that **Ollama model loading is not the primary multi-minute bottleneck**.

### Additional Hermes tool-combination timings

Retained benchmark order:

```text
file + terminal + todo
reasoning: none
time: 1m 49.64s

file + terminal + skills
reasoning: none
time: 2m 42.40s

file + terminal + skills + todo
time: 2m 49.16s
```

The broad lesson is that tool/schema exposure can have a large effect on first-turn latency even when the underlying model is already usable.

### Newelle stripped benchmark results

```text
Run 1:
  output after 5m 25.65s

Run 2:
  stopped after roughly 15 minutes
  no answer
  FAILED

Run 3:
  Newelle suggestion/welcome prompts after 5m 42.23s
  no Bristlecone answer
  FAILED
```

Current interpretation:

- Newelle itself may introduce additional API-server/UI/streaming overhead.
- The Newelle path should be benchmarked separately from direct Hermes CLI and direct Ollama.
- Do not combine many Newelle/Hermes changes at once.
- Keep Hermes as the reference path so regressions are obvious.

## Current storage topology — user-reported, not yet fully audited

The current physical-storage picture is approximately:

```text
~2.5 TB total installed storage

1 TB SSD
└── Windows system / preserve intact for dual boot

1 TB SSD
└── Mostly games
    └── candidate for future Qubes storage after inspection/backup

500 GB HDD
└── Current Qubes installation appears to live here
    └── reported capacity/free-space behavior is suspicious
```

The user reports that the Qubes side appears roughly half full yet shows only about **10 GB remaining** somewhere. This does not match expected usage from Qubes plus rice/customization and a small number of files.

Do **not** assume the entire 500 GB drive is nearly full. Audit first:

```bash
lsblk -e7 -o NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINTS,MODEL
df -h /
sudo lvs -a -o lv_name,vg_name,lv_size,pool_lv,data_percent,metadata_percent
qvm-pool
qvm-block
```

Important interpretation rule:

- `df -h /` can describe only dom0's root filesystem.
- Qubes VM storage may live in an LVM thin pool.
- A qube's configured maximum size is not automatically equal to physical bytes consumed.
- Read-only inspection comes before formatting or resizing.

### Safest Windows/Qubes drive plan

1. Keep the 1 TB Windows system SSD untouched.
2. Preserve BIOS bootability for Windows.
3. Inspect the second 1 TB game/data SSD from Qubes without formatting.
4. Attach its data partition to a dedicated qube.
5. Mount read-only first.
6. Preserve important game saves, mods, screenshots, non-cloud data, and any other files.
7. Verify copied data.
8. Only then erase/repurpose the second 1 TB SSD as Qubes secondary storage.

Typical inside-qube read-only mount pattern after the correct block device is identified:

```bash
lsblk -f
sudo mkdir -p /mnt/windows
sudo mount -o ro /dev/xvdi /mnt/windows
```

The actual device may be `/dev/xvdi1`, `/dev/xvdj`, or another Qubes-assigned name. Inspect first. If BitLocker is present, do not force-mount it as ordinary NTFS.

## Current spare hardware

### NVIDIA Quadro K4200

Confirmed from the physical card:

```text
NVIDIA Quadro K4200
VRAM: 4 GB
generation: older Kepler-era workstation GPU
```

Current planning interpretation:

- Not a preferred accelerator for the current Ollama/Cherry-AI stack.
- Could be used for experimentation if PCI/IOMMU passthrough is viable.
- Could potentially be repurposed for older media/NAS duties, though its age, power use, codec support, and driver support should be weighed against the NAS's integrated graphics.
- Requires PCIe slot space and its own PCIe power connection.
- It does **not** use a SATA data cable.

### Spare HDD

- An additional HDD is available.
- The user currently does not have a SATA data cable for it.
- A normal SATA HDD needs:
  - SATA data to motherboard.
  - SATA power from PSU.

## Thermal snapshot under active Qubes workload

Observed while Qubes was running three browsers with multiple tabs and ChatGPT:

```text
CPU Tctl:      172 F / ~78 C
CPU Tccd1:     167 F / ~75 C
AMD GPU edge:  127 F / ~53 C
NVMe:          116–125 F / ~47–52 C
jc42 sensors:  108–112 F / ~42–44 C
/dev/sda:       91 F / ~33 C
/dev/sdb:       32 F / ~0 C
```

Interpretation retained:

- CPU: warm but plausible for the active workload.
- GPU: normal.
- NVMe: normal.
- memory-module sensors: normal.
- `/dev/sda`: normal.
- `/dev/sdb` 0 C-equivalent reading: likely invalid/unsupported rather than a real drive temperature.

Storage pressure and service latency are currently higher-priority concerns than these temperatures.

---

# 1. Technical Philosophy

Recommendations should prefer:

- Free software.
- Open source.
- Local-first behavior.
- Self-hosting.
- Privacy.
- Replaceable/modular components.
- Open standards.
- Minimal vendor lock-in.
- One-time purchases over subscriptions when paid software is unavoidable.
- Security-preserving changes.
- Read-only inspection before destructive storage changes.
- Measurement before optimization.
- Rollback paths.
- Small, testable changes.

For Qubes specifically:

- Do not weaken isolation for convenience or speed.
- Avoid adding unnecessary software to dom0.
- Prefer Qubes-native mechanisms and narrow qrexec services.
- Do not give AI unrestricted dom0 or cross-qube authority.

---

# 2. Primary Workstation — Known Hardware

## Confirmed/recorded host context

- **CPU:** AMD Ryzen 7 3700X
- **Host RAM:** approximately 32 GB
- **Host GPU:** AMD Radeon RX 580
- **Xen-visible CPUs:** 8 recorded in the Bristlecone performance context
- **Current Bristlecone inference:** CPU-only
- **GPU exposed to Cherry-AI:** no

> [!note]
> The Ryzen 7 3700X physically has more hardware threads than the recorded Xen-visible value, but the important working value in the current Qubes performance notes is the **8 Xen-visible CPUs** actually being exposed/used in that environment. Verify live before making scheduler/vCPU assumptions.

## Storage information known so far

- At least two 1 TB SSDs associated with the Windows/Qubes migration plan.
- One 1 TB Windows SSD should remain untouched to preserve the current Windows installation.
- A second 1 TB Windows/data SSD may eventually be repurposed for Qubes storage after files are copied and verified.
- Active AI models, indexes, repositories, and caches should ideally live on fast SSD storage.
- Archives/backups can move to the future Log Cabin/NAS where appropriate.

Exact full workstation drive inventory should be re-audited before storage redesign.

---

# 3. Operating System

- **Host OS:** Qubes OS
- **Recorded version:** Qubes OS **4.3.1**
- **Desktop base:** XFCE
- **Tiling WM:** i3

Qubes is not incidental to the setup; it is the central isolation/security architecture for the workstation and The Forest.

---

# 4. Core Qubes Security Architecture

## Normal Cherry-AI network path

```text
Cherry-AI -> sys-firewall -> sys-net -> Internet
```

Keep this chain unless a deliberate, security-reviewed architecture change is made.

Do **not** connect Cherry-AI directly to `sys-net` just for speed.

Do not disable required:

- qrexec.
- Qubes GUI services.
- Firewall.
- NetVM networking.
- Update proxy/services.
- Device services.
- Permission controls.
- Approval controls.
- Recovery mechanisms.

## AI access boundary

Bristlecone/Hermes running in Cherry-AI ordinarily sees **Cherry-AI only**.

It should not automatically:

- Read Maple's files.
- Control Maple GUI applications.
- Inspect every other qube.
- Run unrestricted commands in dom0.
- Directly administer the host.

Cross-qube actions should use narrowly scoped qrexec/policy services where practical.

Examples of desirable narrow services:

```text
return Git status
run tests in approved repository
copy approved file
return limited system diagnostic
request selected Foliage
```

Avoid creating a broad remote shell merely because it is convenient.

---

# 5. Qube Inventory / Roles

## dom0

- Host/control domain.
- Administration only.
- Keep minimal.
- Avoid installing unnecessary software.
- Commands may need to be typed manually; keep dom0 command sequences short and explain them.

## Maple

- Fedora-based personal/development workspace.
- Primary user/work qube.
- Primary development environment for Project Digital Cross/The Forest.
- Main Seed-training workspace in planned Seed workflows.
- Can potentially host a lightweight Maple-local AI.
- Should not compete with Bristlecone unnecessarily during heavy CPU work.

## Cherry-AI

- Primary AI qube.
- Hosts the Hermes/Ollama/Bristlecone stack.
- Central local AI control environment.
- Fedora 42 was recorded during setup.
- Current inference is CPU-only.
- No GPU passthrough currently.
- Networked through `sys-firewall`/`sys-net`.

## Sugar

- Gaming qube.
- Should be shut down during heavy Bristlecone/AI work when not needed.

## Honey

- Work qube.
- Should be shut down during heavy Bristlecone/AI work when not needed.

## Cedar

- Untrusted/security-related qube role depending on context.
- Separate from the conceptual Cedar security Tree, though the naming intentionally aligns with Forest security terminology.

## Pine

- Whonix/disposable/privacy-oriented qube.
- May also be described in older notes as a Whonix DVM.
- Not the same as Bristlecone Pine.

## Seed-AI

- Future/planned qube for the smallest/newest Seed during mixed Seed training.
- Do not assume it exists or is complete until user confirmation.

## Standard service qubes

Relevant Qubes service qubes include:

- `sys-net`
- `sys-firewall`
- `sys-usb` when present
- Whonix service qubes when used
- other VPN/research/media/helper qubes depending on current state

---

# 6. Cherry-AI — Historical and Current Setup Facts

Known setup details:

- Qube name: `Cherry-AI`
- Fedora 42 recorded during setup.
- Root disk expanded from **20 GB to 80 GB**.
- `qrexec_timeout` was set to **600 seconds** during setup.
- CPU inference only.
- No GPU passthrough.
- Networking through `sys-firewall` and `sys-net`.
- Hermes later became operational.
- Podman later became operational.
- Ollama later became operational.
- Cherry-AI autostarts in the later performance configuration.

Historical setup notes that still said "install Ollama" are superseded by the later working state.

---

# 7. Primary AI Stack

Current/retained architecture:

```text
Qubes OS
└── Cherry-AI
    ├── Hermes Agent
    │   └── Bristlecone Pine profile
    ├── Ollama
    │   └── bristlecone-qwen35:4b-64k
    ├── Podman
    └── optional/paused interfaces or future services
```

## Hermes

- Primary orchestration/agent interface.
- Preferred over Newelle for daily Bristlecone work.
- Handles agent behavior, tools, skills, orchestration, and future routing.

## Ollama

- Primary model server.
- Local.
- Operational.

## Podman

- Operational container component in the local AI stack.

## Newelle

- Optional/paused.
- Earlier Newelle integration was slow/unreliable.
- Do not make it part of the required daily path unless deliberately reactivated.

---

# 8. Bristlecone Pine Runtime

## Profile

```text
bristlecone
```

## Model

```text
bristlecone-qwen35:4b-64k
```

## Context

```text
64000
```

## Runtime

```text
Ollama + Hermes Agent
```

## Current inference

```text
CPU-only
```

## Model process evidence

During slow cold Hermes requests, `ollama ps` showed approximately:

```text
MODEL:     bristlecone-qwen35:4b-64k
SIZE:      ~5.6 GB
PROCESSOR: 100% CPU
CONTEXT:   64000
```

---

# 9. Direct Ollama Performance Evidence

Direct request target:

```text
http://127.0.0.1:11434/api/generate
```

Simple test prompt:

```text
Reply with only: OK
```

Recorded cold run:

```text
TOTAL:       14.2 sec
MODEL LOAD:  10.3 sec
PROMPT EVAL: 1.4 sec
GENERATION:  2.5 sec
SPEED:       3.14 tok/s
```

Recorded warm run:

```text
TOTAL:       3.5 sec
MODEL LOAD:  0.5 sec
PROMPT EVAL: 0.4 sec
GENERATION:  2.6 sec
SPEED:       3.08 tok/s
```

Important diagnosis:

- Ollama/model cold loading itself is not responsible for the multi-minute first Hermes response.
- The bigger bottleneck is Hermes cold prompt/context prefill on CPU.

---

# 10. Hermes Cold-Start Diagnosis

Observed pattern:

- First Hermes request after restart may take roughly **5–6+ minutes**.
- Later responses can be much faster.
- Hermes was observed with around **14K tokens already in context** before/during routine work.
- Full model context is 64K.
- CPU must evaluate the large system/tool/skill/memory/project prefix before the first visible token.

Approximate real-world simple Hermes timings observed during investigation included:

```text
~6 min
~1 min 30 sec
~6 min 40 sec
~40 sec
```

The exact number varied, but the cold-vs-warm pattern was consistent.

Most important current diagnosis:

```text
Primary bottleneck:
Hermes cold prompt/context prefill

Not primary bottleneck:
Ollama model loading from disk
```

---

# 11. Hermes Profile / Startup Repair

A Bristlecone profile launch issue was previously repaired.

Problem symptoms included:

```bash
hermes -p bristlecone
```

returning:

```text
Hermes isn't configured yet -- no API keys or providers found.
```

There were two launcher paths observed:

```text
/home/user/.local/bin/hermes
/home/user/.hermes/hermes-agent/hermes
```

Directly launching the repo script outside its venv produced a missing `dotenv` error.

Working Hermes gateway service pattern:

```text
WorkingDirectory=/home/user/.hermes/hermes-agent
ExecStart=/home/user/.hermes/hermes-agent/venv/bin/python /home/user/.hermes/hermes-agent/hermes -p bristlecone gateway run
```

A stray config typo/character was fixed.

Later, a YAML indentation error was also fixed so `api_server:` aligned correctly beneath `platform_toolsets:` with `cli:` and `discord:`. After repair, Hermes correctly parsed the profile and prompt-size reporting again showed the real model rather than `model=unset`.

Important rule:

> Do not rerun `hermes setup` unless a real new problem proves setup/configuration is missing.

---

# 12. Bristlecone Gateway / Autostart

Cherry-AI autostarts.

Ollama service:

```text
/usr/local/bin/ollama serve
```

Hermes user service:

```text
~/.config/systemd/user/hermes-bristlecone.service
```

Useful checks:

```bash
systemctl --user status hermes-bristlecone.service
```

Restart:

```bash
systemctl --user restart hermes-bristlecone.service
```

The service has been tested as an autostarting user service.

---

# 13. Ollama Keepalive — Confirmed

Configured:

```text
OLLAMA_KEEP_ALIVE=15m
```

Verified behavior:

- Model loads on first request.
- Stays loaded for about 15 idle minutes.
- Unloads afterward.
- Keepalive survives a Cherry-AI restart as a service configuration.
- A full qube shutdown still removes the model from RAM, so warm state cannot survive a shutdown.

Do not confuse earlier proposed `30m` values with the later verified `15m` configuration.

---

# 14. Hermes Prompt / Tool Optimization — Confirmed Measurements

## Earlier CLI state

Approximately:

```text
System prompt: 26,238 B
Tool schemas:  43,090 B
Tools:         16
Skills index:  3,680 B
```

Large tool schemas included things such as:

- computer_use
- session_search
- file
- skills
- terminal
- memory
- clarify
- code_execution
- tts
- vision

## Lean CLI after cleanup

Verified approximately:

```text
System prompt: 20,994 B
Tool schemas:  31,532 B
Tools:         14
```

Cron was intentionally retained afterward, so interactive CLI tool count became approximately:

```text
15 tools
```

Hermes Computer Use and Hermes TTS were disabled from the lean CLI configuration during optimization.

## API server before cleanup

```text
System prompt: 17,727 B
Tool schemas:  40,712 B
Tools:         25
```

## API server final verified measurement

```text
System prompt: 16,864 B
Tool schemas:  28,188 B
Tools:         12
```

This API trimming was confirmed complete.

Approximate effect:

- ~31% smaller tool schemas.
- ~52% fewer API tools.

---

# 15. Hermes Tool Philosophy

Keep capabilities directly useful to Treewright work.

Useful core categories include:

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

Cron was intentionally kept because its idle overhead is small and only actual scheduled AI work creates meaningful compute load.

General rule:

- Keep tools task-relevant.
- Disable optional tools instead of deleting them where possible.
- Avoid showing every tool schema to every prompt.
- Specialized capabilities should eventually be routed through workshops.

---

# 16. TTS / Voice — Current Desired Direction

During lean optimization, Hermes TTS was intentionally disabled.

The user now wants to add TTS back as an **optional toggle**, not always-on behavior.

Desired usage:

- Turn speech on while leaving the terminal to do another task.
- Turn it off when working directly with Hermes.
- Avoid hearing long code blocks/log output.
- Potentially trigger/replay old messages later.
- Potentially bind voice controls to i3 hotkeys.
- Keep normal text response unchanged.

Future ideal Forest speech modes:

```text
OFF
FULL
SMART
BRIEF
```

SMART should skip or summarize:

- Code blocks.
- Long logs.
- Tables.
- URLs.
- Repetitive terminal output.

Replay of old text should ideally call the TTS engine directly rather than asking the LLM to regenerate the message.

Potential i3 hotkey concept discussed:

```text
Super + Shift + V  → toggle TTS
Super + Shift + X  → speech off
Super + Shift + R  → read/replay selected text
Super + Shift + S  → stop speech
```

These bindings are a design direction; do not assume they are implemented yet.

---

# 17. Qubes Work-State / i3 Numpad Modes

Numpad 1–4 were tested successfully.

## Numpad 1 — forest-normal-mode

Recorded baseline:

```text
Cherry-AI:
  memory = 8192 MB
  maxmem = 16000 MB
  vcpus  = 9

Maple:
  memory = 800 MB
  maxmem = 8000 MB
  vcpus  = 4
```

Known issue:

- Current/earlier script behavior can restart qubes.
- Restarting Cherry-AI destroys warm Bristlecone/model prefix state.
- Future optimization should avoid restarting Cherry-AI when the current resources are already suitable.

## Numpad 2 — pine-cone-mode

Bristlecone-focused work state.

## Numpad 3 — maple-seed-mode

Maple-focused Seed-training work state.

## Numpad 4 — forest-mixed-mode

Recorded target:

```text
Cherry-AI:
  memory = 8192 MB
  maxmem = 12000 MB
  vcpus  = 4

Maple:
  memory = 6144 MB
  maxmem = 12000 MB
  vcpus  = 4
```

## Numpad 5 — future Seed-AI mode

Pending.

Planned architecture:

```text
Maple
  = primary training workspace

Cherry-AI
  = progressed Cherry Seed teacher/reviewer

Seed-AI
  = newest/smallest Seed under training
```

Proposed resources:

```text
Maple:
  memory = 12288 MB
  maxmem = 16000 MB
  vcpus  = 4

Cherry-AI:
  memory = 6144 MB
  maxmem = 9000 MB
  vcpus  = 3

Seed-AI:
  memory = 2048 MB
  maxmem = 6000 MB
  vcpus  = 2
```

Do not mark Numpad 5 complete until it is created and tested.

---

# 18. Qubes Resource Guidance

When optimizing:

- Audit first.
- Record current values.
- Shut down unused app qubes during heavy AI work.
- Keep service qubes stable.
- Avoid assigning every CPU to Cherry-AI.
- Leave capacity for dom0, sys-net, sys-firewall, and the active workspace.
- Measure qmemman behavior/memory pressure.
- Watch for swap.
- Watch for model unloading.
- Watch for storage pressure.
- Avoid unnecessary background services inside app qubes.
- Keep active AI data on fast SSD.
- Do not run active retrieval indexes from slow NAS storage if latency matters.

Useful audit commands in dom0:

```bash
qvm-ls --fields NAME,STATE,MEMORY,VCPUS,NETVM
qvm-prefs <QUBE_NAME> memory
qvm-prefs <QUBE_NAME> maxmem
qvm-prefs <QUBE_NAME> vcpus
qvm-prefs <QUBE_NAME> autostart
```

Inside Cherry-AI:

```bash
free -h
df -h
ps -eo pid,comm,%cpu,%mem --sort=-%mem | head -n 25
pgrep -af 'ollama|llama-server|newelle|hermes|python'
```

Do not change settings during the initial baseline capture.

---

# 19. Quick / Deep Performance Direction

Current desired end-state:

## Quick

- Smaller context.
- Lean tools.
- Lower reasoning.
- Faster first response.
- Preserve essential project continuity.

A later performance plan proposed starting around **32K** for Quick and benchmarking downward/upward.

Earlier broad planning also considered 8K–16K Quick and 16K–32K Standard. Treat these as experimental ranges, not final values.

## Deep

- 64K context retained when justified.
- Higher reasoning.
- Broader Treewright capabilities.
- Architecture/debugging/research use.

The final sizes should be benchmark-driven.

---

# 20. Desktop / Terminal Environment

Primary tools:

- kitty terminal.
- zsh.
- oh-my-zsh.
- Powerlevel10k.
- rofi.
- fastfetch.
- nitrogen.
- picom.
- polybar.
- xfce4-screenshooter.
- i3.
- XFCE.

## Terminal colors

- Maple: orange.
- dom0: white.
- Cherry: purple.

## Prompt preferences

- Cyan line above the prompt.
- Preferred prompt characters: **✦ ❯❯**
- Brackets around the tilde only.
- Clean/custom appearance.

## Font

- gohu requested for Maple's kitty terminal.

## Transparency

Picom:

```text
backend: GLX
```

Desired opacity around **85%** for:

- Maple kitty.
- dom0 kitty.

## i3 appearance

- Border pixel: 1.
- Thin visual separation.

Earlier Q menu/window-manager tweaks had issues and may need cautious revalidation rather than assuming prior commands worked.

---

# 21. Polybar

Recorded version:

```text
3.7.1
```

Moved from `xfce4-panel` toward Polybar.

Modules include or are planned to include:

- Launcher.
- Power.
- Notifications.
- Workspaces.
- Clock.
- System info.
- Media info.

Earlier notification module work remained pending.

Goal includes showing media titles across qubes, including Firefox media where practical.

---

# 22. Media Design

The user wants two distinct media concepts/modules:

## Video/anime

- Anime playback.
- Regular YouTube video playback.

## Music

- Spotify.
- Music on YouTube.
- Local audio.
- Local video/audio files.

The user did not want a full set of media controls permanently in the panel; controls may later live in a rofi UI.

Media players considered:

- VLC.
- Pragha.
- Celluloid.
- mpv.

Chosen:

> **mpv**

Goal:

- Customize mpv to match the terminal/desktop appearance.
- Use transparency/theme integration where practical.

---

# 23. Storage / Windows Dual-Drive Plan

Safest retained plan:

1. Leave one 1 TB Windows SSD completely untouched.
2. Preserve the current Windows installation.
3. Select Windows via BIOS boot menu when necessary.
4. Access the second 1 TB Windows SSD from Qubes without formatting it initially.
5. Attach the data partition to a dedicated qube.
6. Mount read-only first.
7. Copy/verify important files.
8. Only after verification, erase/repurpose the second SSD as Qubes storage if desired.

Typical read-only mount after block attachment:

```bash
lsblk -f
sudo mkdir -p /mnt/windows
sudo mount -o ro /dev/xvdi /mnt/windows
```

The actual Qubes-attached block device may not be `/dev/xvdi`; inspect first.

---

# 24. Local AI / Seed Training Hardware Reality

Current host:

- ~32 GB RAM.
- CPU-only Cherry-AI inference.
- RX 580 exists on host but is not passed through to Cherry-AI.
- Heavy simultaneous AI work can cause CPU/RAM contention.

PyTorch/Unsloth notes:

- Installing them does not make CPU-only LLM training fast.
- CPU-only is still useful for:
  - dataset preparation,
  - behavioral testing,
  - small evaluations,
  - conversion experiments,
  - learning workflows.
- LoRA/QLoRA becomes much more practical with suitable GPU access.
- GPU passthrough should not be attempted casually.
- Before any passthrough:
  - identify exact GPU(s),
  - VRAM,
  - monitor connections,
  - IOMMU groups,
  - Qubes compatibility,
  - rollback plan.

Preferred training architecture is an isolated **Model Workshop** rather than polluting stable Cherry-AI or everyday Maple with every experimental dependency.

---

# 25. Seed Nursery Role Split

Conceptual split:

```text
Maple / Seed Nursery
├── behavioral Seed configurations
├── dataset creation/cleaning
├── test conversations
├── small evaluation batches
├── candidate versions
└── reproducible logs

Cherry-AI / Bristlecone
├── designs improvements
├── reviews datasets
├── diagnoses failures
├── creates corrections
├── compares candidates
└── recommends promotion/rollback

User
├── approves training data
├── approves high-impact actions
└── decides when a candidate is stable
```

Avoid Maple's trainer and Bristlecone writing the same live files simultaneously.

Prefer:

- Git branches.
- Candidate directories.
- Immutable run folders.
- Rollback points.

---

# 26. NAS / Log Cabin — Separate Hardware

Do not confuse the NAS hardware with the main Ryzen workstation.

Known NAS/home-lab hardware:

- Acer mini PC intended as first NAS.
- Third small PC available.
- Spare GPU with DisplayPort-only output.
- Seagate HDD inside mini PC.
- Multiple HDDs/SSDs.
- Two drives were not detected during an earlier session.
- Additional case and motherboard available.
- DisplayPort-to-HDMI/AV cable discussed.
- One beep on boot was observed.
- HDMI failed in one configuration while DisplayPort worked.

Long-term NAS/Log Cabin roles:

- Backups.
- Media.
- Smart-home hub.
- Home-security hub.
- Memory library.
- Cross-device files.
- Remote Cherry/Forest access.
- Durable storage.

Final NAS OS/security architecture is not yet settled.

---

# 27. Home Network — Known Topology and Troubleshooting Context

Provider:

- Comcast/Xfinity.
- Coax-based connection.

Known equipment:

- Netgear CM500 modem.
- Netgear router devices.
- TP-Link switch downstairs.
- Tall router upstairs.
- SolarCity box.
- Coax cabling.
- Blue Ethernet cable to SolarCity box; orange link light observed.
- Tan cable goes outside.

Observed/history:

- Coax goes to the tall router.
- Ethernet connects modem/router equipment.
- TP-Link switch is used for downstairs devices.
- Home previously had a small thin black box with older router equipment.
- Main PC used to connect through the router but that stopped working.
- Wi-Fi works upstairs.
- Downstairs Acer/main PC had Ethernet trouble through current switch arrangement.
- Acer could see some Wi-Fi networks but not the home SSID.
- Home does not have conventional Ethernet runs through the walls.
- Coax/network conversion equipment is part of the environment.
- User prefers troubleshooting existing equipment before buying more or calling Comcast when possible.

---

# 28. Remote / Garden Direction

Long term, The Forest should support:

- Local-only use.
- Optional remote access.
- Optional Garden/device sync.
- Secure cross-device services.
- Potted Plants on mobile.
- Potential workload handoff from phone to desktop/server.
- Headscale was discussed as a possible later networking component.

Do not assume remote access is currently fully implemented.

---

# 29. Obsidian / Local Knowledge Role in the Technical Stack

Obsidian is being actively set up as:

- Current Markdown knowledge base.
- Cross-Qube knowledge transport.
- Multi-model context source.
- Early Seed Training source.
- Prototype for future Leaf Foliage.

Important architecture:

- Durable knowledge should remain normal files/Markdown where possible.
- Derived search/vector indexes should be rebuildable.
- Sync should remain optional.
- AI access should be permission-scoped.
- A master vault should not automatically be fully exposed to every Tree/qube.

---

# 30. Global Technical Interaction Notes

Useful collaboration rules:

- Keep commands short in dom0 because they may be manually typed.
- Longer copy/paste blocks are acceptable in Maple and Cherry-AI.
- Explain risky commands before execution.
- Preserve user data.
- Read-only first for important/unknown drives.
- Do not repeat questions whose answers are already known.
- Do not mark a change complete until the user confirms it worked.
- Preserve Qubes boundaries.
- Prefer local CLI output over assumptions about Hermes.
- Record original values before changing performance settings.
- Keep a known-working baseline.
- In technical conversation, if the user's phone autocorrect produces **"wine"** where the context clearly indicates Qubes, interpret it as **Qubes**.

---

# 31. High-Value Live Checks for a Future AI

Before giving exact resource/performance commands, collect or confirm:

## dom0 / host

```bash
qvm-ls --fields NAME,STATE,MEMORY,VCPUS,NETVM
qubes-dom0-update --action=list  # only if actually needed; do not update blindly
```

For important qubes:

```bash
qvm-prefs <QUBE> memory
qvm-prefs <QUBE> maxmem
qvm-prefs <QUBE> vcpus
qvm-prefs <QUBE> autostart
```

## Cherry-AI

```bash
free -h
df -h
ollama ps
systemctl status ollama
systemctl --user status hermes-bristlecone.service
pgrep -af 'ollama|llama-server|newelle|hermes|python'
```

Hermes prompt measurement:

```bash
hermes -p bristlecone prompt-size
```

Do not change settings during baseline collection.

---

# 32. Known Completed vs Pending Snapshot

## Confirmed/working

- Qubes OS workstation.
- Qubes OS 4.3.1 recorded in current performance packet.
- XFCE + i3 environment.
- Cherry-AI exists.
- Maple exists.
- Hermes operational.
- Ollama operational.
- Podman operational.
- Bristlecone profile operational.
- Bristlecone model `bristlecone-qwen35:4b-64k`.
- CPU inference.
- Ollama 15-minute keepalive verified.
- Hermes gateway/autostart service tested.
- Unnecessary Hermes skills/tools trimmed substantially.
- Final API-server prompt/tool measurement verified.
- Numpad 1–4 work-state bindings tested.
- mpv selected as media player.
- Windows-drive preservation/read-only plan established.

## Planned / still evolving

- Quick/Standard/Deep fully implemented routing.
- Automatic routing.
- Seed-AI/Numpad 5.
- Full Qubes resource optimization.
- Native Forest workshops.
- Structure-aware retrieval.
- Leaf Foliage.
- Garden sync.
- Potted Plants.
- Resource Governor.
- Background Maple task system.
- Optional toggleable Hermes/Forest TTS and i3 bindings.
- GPU passthrough/training hardware changes.
- Final NAS architecture.
- Final home network repair.
- Native Forest all-in-one distribution.

## Optional/paused

- Newelle as a daily Bristlecone interface.

---

# 33. Source/Provenance Notes

This technical handoff combines:

- Current conversation context through 2026-08-07.
- `Obsidian_Memory_Export_2026-08-06.md`
- `bristlecone_pine_full_continuity_packet_v1_1.md`
- `bristlecone_performance_continuity_and_next_steps.md`
- Later confirmed Bristlecone tool/prompt trimming and Project Forest continuity.

Use newer direct user statements over conflicting old snapshots.


# Appendix A — Immediate Bristlecone Speed Resume Checklist

Use this order so the connection problem and speed problem are not mixed together.

## A1. Restore/verify connectivity first

Inside `Cherry-AI`:

```bash
systemctl status ollama
systemctl --user status hermes-bristlecone.service
ollama ps
pgrep -af 'ollama|llama-server|newelle|hermes|python'
```

Then verify Hermes profile parsing:

```bash
hermes -p bristlecone prompt-size
```

Expected working identity should resolve to the Bristlecone profile/model rather than `model=unset` or an unconfigured-provider error.

## A2. Preserve the known-good baseline

Before changing more tools, context, memory, or startup behavior, record:

```text
Hermes profile
model
context
reasoning setting
system-prompt bytes
tool-schema bytes
tool count
skills-index bytes
Cherry-AI memory/maxmem/vCPUs
whether model is cold or warm
whether Newelle is in the path
first-token/total response time
```

## A3. Continue Quick / Standard / Deep work

Desired architecture:

### Quick
- Routine low-risk work.
- Lowest practical prompt overhead.
- Lean toolset.
- Smaller context than Deep.
- Low/minimal reasoning.
- Preserve core continuity.

### Standard
- Normal coding/debugging/research.
- Moderate context and verification.
- Normal tool access.

### Deep
- Architecture.
- difficult debugging.
- security-sensitive work.
- large multi-file work.
- 64K context when justified.
- broader tools and higher reasoning.

Do not mark these modes complete until they are actually created and benchmarked.

## A4. Avoid unnecessary Cherry-AI restarts

Current/earlier Qubes mode scripts can restart Cherry-AI. A restart destroys:

- loaded model state,
- KV/prefix cache,
- warm Hermes context,
- any warm Newelle/Hermes connection state.

Optimize mode scripts so they do not restart Cherry-AI when the desired resources are already in effect.

## A5. Warm-up only after structural optimization

Once Quick/Deep prompt/tool design is satisfactory, consider a small automatic warm-up request after a required Cherry-AI boot.

Warm-up should not be used to hide an unnecessarily huge cold prompt.

## A6. Benchmark paths separately

Keep at least these separate:

```text
Direct Ollama
Hermes CLI minimal
Hermes CLI normal
Hermes API server
Newelle -> Hermes/API path
```

This isolates whether latency comes from:

- model runtime,
- Hermes prompt prefill,
- tool schemas,
- skills/context,
- gateway/API server,
- Newelle UI/streaming,
- Qubes resource pressure,
- storage pressure,
- or restart behavior.

---

# Appendix B — Full Bristlecone Performance Continuity Packet (2026-08-06)

The following packet is preserved verbatim as a historical performance handoff. Newer facts in the main body of this file override conflicts.

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

