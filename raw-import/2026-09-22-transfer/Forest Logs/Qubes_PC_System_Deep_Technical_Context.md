---
title: Qubes OS, PC Hardware, Local AI, Desktop, Storage, and Network — Deep Technical Context
aliases:
  - Qubes Deep Technical Handoff
  - Primary PC System Context
  - Forest Workstation Technical Context
tags:
  - qubes
  - hardware
  - pc
  - cherry-ai
  - maple
  - bristlecone
  - hermes
  - ollama
  - i3
  - polybar
  - storage
  - nas
  - networking
status: active-reference
updated: 2026-08-07
---

# Qubes OS, PC Hardware, Local AI, Desktop, Storage, and Network — Deep Technical Context

> [!important]
> This file is focused on the user's Qubes workstation, PC hardware, qube layout, AI runtime, desktop customization, storage, NAS, and networking.
>
> Keep **confirmed values**, **observed values**, and **planned values** distinct. Verify live hardware/resource values before making performance or destructive-storage decisions.

---

# 1. Technical Philosophy

Preferred direction:

- Free.
- Open source.
- Local-first.
- Offline-capable.
- Self-hosted where practical.
- Privacy-focused.
- Modular.
- Replaceable.
- Open standards.
- Minimal vendor lock-in.
- One-time purchases over subscriptions when paid software is unavoidable.
- Security-preserving.
- Measured rather than guessed.
- Reversible.
- Documented.

For Qubes specifically:

- Do not weaken isolation for convenience.
- Do not install unnecessary software in dom0.
- Prefer Qubes-native mechanisms.
- Prefer narrow qrexec services.
- Do not give AI unrestricted host/cross-qube authority.
- Use read-only inspection before destructive storage changes.
- Change one major variable at a time during performance tuning.

---

# 2. Primary PC Hardware

## CPU

Recorded:

```text
AMD Ryzen 7 3700X
```

Important note:

The CPU physically has more threads than some Qubes observations showed, but performance work recorded:

```text
8 Xen-visible CPUs
```

Another observation described:

```text
8 cores / one thread per core visible to Xen
```

Verify live before scheduler/vCPU decisions.

## RAM

Recorded host memory:

```text
~32 GB
```

## GPU

Recorded host GPU:

```text
AMD Radeon RX 580
```

Current Cherry-AI state:

```text
GPU passthrough: no
AI inference: CPU-only
```

Exact GPU VRAM/IOMMU-group details should be verified before passthrough planning.

---

# 3. Qubes OS

Recorded:

```text
Qubes OS 4.3.1
```

Desktop base:

```text
XFCE
```

Tiling window manager:

```text
i3
```

Qubes is central to the user's security and AI architecture.

---

# 4. Qube Inventory

## dom0

Role:

- Host/control domain.
- Administration only.

Rules:

- Keep minimal.
- Avoid unnecessary packages.
- Do not run routine AI software.
- Do not use for routine password-manager work.
- Do not expose to unrestricted AI control.
- Use short/medium manually typeable commands when possible.

The user generally cannot copy/paste commands directly into dom0, so instructions should be practical for manual entry.

## Maple

Role:

- Personal qube.
- Primary development qube.
- Project Digital Cross work.
- Git/GitHub.
- User-facing browser/terminal.
- Possible Seed Nursery/training controller.

Base:

```text
Fedora-based
```

Recorded resources in one continuity snapshot:

```text
vCPUs: 4
Initial memory: ~800 MB
Maximum memory: ~8000 MB
```

These values should be rechecked before optimization.

## Cherry-AI

Role:

- Primary AI qube.
- Bristlecone Pine runtime.
- Hermes.
- Ollama.
- Forest AI development/testing.

Recorded OS:

```text
Fedora 42
```

Recorded resources in one snapshot:

```text
vCPUs: 9
Initial memory: 8192 MB
Maximum memory: 16000 MB
```

Observed Ollama worker RAM during testing:

```text
~6.3 GB
```

Hermes used comparatively little RAM.

Current AI inference:

```text
CPU-only
```

No direct GPU access recorded.

## Sugar

Role:

```text
Gaming
```

Recommendation during heavy AI work:

- Shut down when not needed.

## Honey

Role:

```text
Work
```

Recommendation during heavy AI work:

- Shut down when not needed.

## Cedar

Role:

- Untrusted/security-related qube depending on context.

Note:

This is separate from the conceptual Cedar security Tree/service identity, though the naming is intentionally related.

## Pine

Earlier retained role:

- Whonix/disposable-personal style role.

---

# 5. Networking Architecture

Normal Cherry-AI path:

```text
Cherry-AI -> sys-firewall -> sys-net -> Internet
```

Do not connect Cherry-AI directly to `sys-net` simply for performance.

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

---

# 6. Cross-Qube AI Boundary

Bristlecone/Hermes in Cherry-AI ordinarily sees only Cherry-AI.

It should not automatically:

- Read Maple files.
- Control Maple GUI.
- Inspect every qube.
- Run arbitrary dom0 commands.
- Administer hardware.
- Pull secrets from other qubes.
- Obtain broad remote shells.

Preferred future narrow qrexec operations:

```text
return Git status
run tests in approved repository
copy approved file
return limited diagnostic
request selected Foliage
perform approved build step
```

All dom0-related AI operations should be narrow, logged, permission-gated, and reviewable.

---

# 7. Git / SSH in Qubes

## Maple

Git author:

```text
kudokudo1
```

Git email:

```text
maple@kudostarstudios.com
```

Default branch:

```text
main
```

SSH:

```text
~/.ssh/id_ed25519_maple
~/.ssh/id_ed25519_maple.pub
```

GitHub SSH test succeeded.

## Cherry-AI

Git author:

```text
kudokudo1
```

Git email:

```text
cherry@kudostarstudios.com
```

SSH:

```text
~/.ssh/id_ed25519_cherry
~/.ssh/id_ed25519_cherry.pub
```

GitHub SSH test succeeded.

GitHub repository remote:

```text
git@github.com:kudokudo1/The-Forest-Project.git
```

Private key contents must never be shared.

---

# 8. Local AI Stack

## Hermes

Primary orchestration/agent layer.

Preferred daily interface for Bristlecone.

Responsibilities:

- Agent behavior.
- Skills.
- Tools.
- Orchestration.
- Future mode routing.
- Workshop routing.
- Multi-model integration.

## Ollama

Primary local model server.

Status:

```text
Operational
```

## Podman

Status:

```text
Operational
```

## Newelle

Status:

```text
Optional / paused
```

Reason:

- Slow.
- Unreliable.
- Not required for daily Bristlecone operation.

---

# 9. Bristlecone Pine Runtime

Profile:

```text
bristlecone
```

Model:

```text
bristlecone-qwen35:4b-64k
```

Model size observed:

```text
~5.6 GB
```

Context:

```text
64,000 tokens
```

Processor:

```text
100% CPU during observed Ollama work
```

Healthy status phrase:

```text
Pine is fine.
```

Role:

```text
Treewright
```

---

# 10. Hermes Prompt / Tool Optimization

Confirmed improvements:

Unnecessary Hermes skills were disabled.

Trimmed API server:

```text
System prompt: 16,864 B
Tool schemas: 28,188 B
Tools: 12
```

Earlier API result:

```text
System prompt: 17,727 B
Tool schemas: 40,712 B
Tools: 25
```

Trimmed CLI measurement recorded:

```text
System prompt: 20,994 B
Tool schemas: 31,532 B
```

A YAML syntax issue in:

```text
~/.hermes/profiles/bristlecone/config.yaml
```

was fixed by aligning `api_server:` properly under `platform_toolsets:`.

---

# 11. Bristlecone Performance Benchmarks

Recorded tests:

```text
file,terminal,todo
reasoning=none
1m 49.64s
```

```text
file,terminal,skills
reasoning=none
2m 42.40s
```

```text
file,terminal,skills,todo
2m 49.16s
```

Newelle stripped-down path:

```text
Run 1: 5m 25.65s to output
Run 2: failed after ~15m
Run 3: UI prompts after 5m 42.23s, no Bristlecone answer
```

Conclusion:

- Hermes should remain Bristlecone's primary interface.
- Newelle remains paused.

---

# 12. vCPU Model and Oversubscription

A Qubes vCPU is not a dedicated physical core.

Example:

```text
Physical/Xen-visible cores: 8

Cherry-AI: 9 vCPUs
Maple: 4 vCPUs
service qubes: additional vCPUs
```

This is CPU oversubscription.

Meaning:

- Idle vCPUs use little real CPU.
- Busy vCPUs compete.
- More vCPUs can improve utilization.
- Too many busy vCPUs can increase context switching.
- Cache contention can worsen.
- Heat and responsiveness may worsen.
- Performance must be benchmarked.

Do not assume configured vCPU totals must equal physical core count.

---

# 13. Planned AI Modes

Reasoning dimension:

```text
Quick
Standard
Deep
```

Workshop dimension:

```text
Code
Research
System
Model
Retrieval
Memory
```

These should be routed independently.

## Quick

Intended:

- Small context.
- Minimal reasoning.
- Minimal tools.
- Fast responses.

## Standard

Intended:

- Moderate context.
- Normal reasoning.
- Task-appropriate tools.

## Deep

Intended:

- 64K context when justified.
- Higher reasoning.
- Architecture/debugging/research use.
- Still limited to required workshop/tools.

Final sizes/settings should be benchmark-driven.

---

# 14. Planned Workshops

Potential isolated Qubes/workshops:

```text
Model Workshop
Seed Nursery
Retrieval Workshop
Research Workshop
Code Workshop
System Workshop
Memory Workshop
```

Purpose:

- Dependency isolation.
- Permission separation.
- Resource separation.
- Testing.
- Rollback.
- Avoid contaminating stable Cherry-AI.

Model-weight training tools like PyTorch/Unsloth should preferably go into an isolated Model Workshop.

---

# 15. Desktop / Terminal Stack

Primary tools:

```text
kitty
zsh
oh-my-zsh
Powerlevel10k
rofi
fastfetch
nitrogen
picom
polybar
xfce4-screenshooter
i3
XFCE
mpv
```

---

# 16. Terminal Visual Identity

## Maple

Color:

```text
orange
```

## dom0

Color:

```text
white
```

## Cherry-AI

Color:

```text
purple
```

## Prompt

Preferred prompt characters:

```text
✦ ❯❯
```

Preferences:

- Cyan line above prompt.
- Brackets around tilde only.
- Minimal/clean spacing.
- Commands begin near the chevrons.
- Customized but readable.

## Font

Requested:

```text
gohu
```

for Maple kitty.

---

# 17. Transparency / Compositor

Picom backend:

```text
glx
```

Desired opacity:

```text
~85%
```

for:

- Maple kitty.
- dom0 kitty.

i3 border:

```text
pixel 1
```

Goal:

- Thin visual separation.
- Minimal borders.
- Terminal-focused look.

---

# 18. Polybar

Recorded version:

```text
3.7.1
```

Migration:

```text
xfce4-panel -> Polybar
```

Modules include/planned:

- App launcher.
- Power.
- Notifications.
- Workspaces.
- Clock.
- System info.
- Media info.

Notification module was previously not fully working.

Goal:

- Media titles from browsers/qubes where practical.
- Firefox media included.

---

# 19. Media Architecture

The user wants two distinct media concepts.

## Video/anime

Includes:

- Anime.
- Regular YouTube/video content.

## Music

Includes:

- Spotify.
- YouTube music.
- Local audio.
- Local video/audio files.

The user does not want full media controls permanently in the panel.

Controls may later live in:

```text
rofi
```

Chosen player:

```text
mpv
```

Goal:

- Theme mpv to match terminal/desktop.
- Transparency/integration where practical.

---

# 20. Browser / Screenshot Context

Browsers mentioned:

- Mullvad Browser.
- Firefox.

Mullvad Browser had a default-browser issue after a qube rename and was later installed/fixed.

Firefox is used for media.

Screenshot tool:

```text
xfce4-screenshooter
```

---

# 21. Storage / Windows Plan

Known context:

- At least two 1 TB SSDs involved in Windows/Qubes storage planning.

Safest retained plan:

1. Leave one 1 TB Windows SSD completely untouched.
2. Preserve existing Windows installation.
3. Boot Windows via BIOS when needed.
4. Access the second 1 TB Windows/data SSD from Qubes without formatting it first.
5. Attach only the needed block device/partition to a dedicated qube.
6. Mount read-only first.
7. Copy and verify needed files.
8. Only after backup/verification, repurpose second SSD for Qubes storage if desired.

Typical mount pattern:

```bash
lsblk -f
sudo mkdir -p /mnt/windows
sudo mount -o ro /dev/xvdi /mnt/windows
```

The device name may differ. Inspect before mounting.

Do not format or repartition until verified backups exist.

---

# 22. Storage Placement Strategy

Prefer fast SSD for:

- Active models.
- Indexes.
- Git repositories.
- Embeddings.
- Active caches.
- Training scratch space.

Future NAS can hold:

- Archives.
- Backups.
- Media.
- Old models.
- Old datasets.
- Leaf Litter.
- Git mirrors.
- Portable Plant libraries.

---

# 23. NAS / Log Cabin

Future NAS goals:

- Backup.
- Media.
- Smart-home services.
- Forest storage.
- Forgejo.
- Vaultwarden.
- Model/archive storage.
- Optional Garden services.

Security:

- Least privilege.
- Do not expose all storage to Cherry-AI.
- Use dedicated accounts.
- Prefer narrow shares.
- Separate backups from active AI write access.

---

# 24. Home Network Context

Known troubleshooting history:

- Home uses coax-related networking.
- A tall router was connected through coax.
- Ethernet links to modem/other networking equipment.
- TP-Link equipment serves downstairs devices.
- Netgear devices were inspected.
- A Netgear CM500 was identified.
- A blue Ethernet cable went to a SolarCity box.
- A tan cable went outside.
- An older small black box was previously part of the network.
- The Acer NAS machine could see some Wi-Fi networks but not the home SSID.

Home topology needs a clean re-audit before relying on the NAS.

Useful future task:

Create a network map showing:

```text
ISP/coax
modem
router
MoCA/coax adapters
switches
TP-Link
Netgear
SolarCity device
Acer NAS
Qubes workstation
Wi-Fi APs
```

---

# 25. Acer NAS Direction

The Acer machine is intended as a future NAS / infrastructure node.

Current issue retained:

- Can detect some Wi-Fi networks.
- Does not currently detect the home Wi-Fi SSID reliably.

Preferred long-term NAS connection:

- Wired Ethernet when possible.
- Stable LAN addressing.
- Avoid depending on weak/unreliable Wi-Fi for core storage.

---

# 26. Remote Compute Node Concept

A second computer may later act as:

- CPU node.
- GPU node.
- Storage node.
- Model-training node.
- Remote inference node.

The primary Qubes system could remain the controller.

Important:

- Do not weaken Qubes isolation to integrate remote compute.
- Use authenticated network services.
- Keep role boundaries.
- Prefer dedicated services over broad shell access.

---

# 27. AI Resource Reality

Current workstation constraints:

```text
~32 GB host RAM
8 Xen-visible CPUs recorded
RX 580 not passed through
Cherry-AI CPU-only
```

Implications:

- Large context windows can be slow.
- Concurrent AI workloads can compete heavily.
- Qubes service qubes also require resources.
- Maple and Cherry heavy tasks should be coordinated.
- Shut down Sugar/Honey when unnecessary during large AI work.
- Optimize orchestration/retrieval before fine-tuning.

---

# 28. Model Training Direction

Seeds may eventually receive model-weight training.

Preferred initial direction:

```text
LoRA / QLoRA
```

Potential tools:

```text
PyTorch
Unsloth
```

Do not install experimental ML dependencies into stable Cherry-AI just for convenience.

Use an isolated workshop.

Do not train before an evaluation suite exists.

Do not train blindly on:

- Unreviewed private data.
- Contradictory data.
- Low-quality data.
- Unsafe data.
- Copyrighted datasets without appropriate rights.

---

# 29. Bristlecone Optimization Master Status

Confirmed:

```text
[X] Unnecessary Hermes skills disabled
[X] API toolset trimming completed
[X] CLI profile trimming verified
```

Still pending/partially pending depending on latest live state:

```text
[ ] Qubes/background resource optimization
[ ] Hermes runtime tuning
[ ] Ollama runtime tuning
[ ] Quick/Standard/Deep routing
[ ] Workshop routing
[ ] Structure-aware code retrieval
[ ] Retrieval router
[ ] Hybrid local search
[ ] Caching/reranking/incremental indexing
[ ] Full benchmark suite
[ ] Isolated Unsloth workshop
[ ] Next optimization stage
```

Do not mark pending items complete without explicit confirmation.

---

# 30. Retrieval Direction

Future retrieval should support:

- Structure-aware code retrieval.
- Block-level retrieval.
- Local indexes.
- Hybrid lexical/vector search.
- Incremental indexing.
- Caching.
- Reranking.
- Document retrieval.
- Memory retrieval.
- Forest/Leaf Foliage relationships.
- Narrow retrieval scope per task.

Goal:

Use the smallest relevant context instead of feeding entire repositories/documents into every request.

---

# 31. Local-First Forest Storage

Leaf Foliage/storage architecture should remain:

- Local-first.
- Offline-capable.
- Portable.
- Optional sync.
- Human-readable.
- AI-readable.
- Git-compatible where appropriate.

Users should be able to create portable **Potted Plants** containing selected knowledge and copy them to another device without connecting them online.

Optional Garden/device sync may be added later.

---

# 32. Security / Recovery Rules

Never:

- Put private SSH keys in Git.
- Put passwords/tokens in Git.
- Put `.env` secrets in public repositories.
- Give Cherry unrestricted password-vault access.
- Give Bristlecone broad dom0 access.
- Skip backups before storage changes.
- Disable Qubes isolation just for speed.

Prefer:

- Separate SSH keys per qube.
- Bitwarden for passphrases.
- MFA.
- Offline recovery material.
- Narrow qrexec.
- Separate role emails.
- Git history.
- Read-only first.
- Rollback.

---

# 33. Useful Live Diagnostics for Future Sessions

## Qubes / guest

Inside a qube:

```bash
cat /etc/os-release
nproc
free -h
df -h
lsblk -f
ip addr
ip route
```

## AI

```bash
ollama ps
ps aux --sort=-%mem | head
ps aux --sort=-%cpu | head
```

## Git

```bash
git status
git remote -v
git branch --show-current
git log --oneline --decorate --graph -10
```

## SSH

```bash
ls -la ~/.ssh
ssh -T git@github.com
```

Do not `cat` private key files.

---

# 34. Facts to Re-Verify Before Major Hardware Work

Before GPU passthrough, CPU tuning, or storage redesign, recheck:

- Exact BIOS/UEFI settings.
- IOMMU groups.
- GPU VRAM.
- Which GPU drives which monitor.
- Exact Qubes-visible CPU topology.
- Current Qube resource assignments.
- Full drive inventory.
- SMART health.
- Qubes storage pool layout.
- Network topology.
- NAS Ethernet path.
- Current router/modem/AP models.

---

# 35. Continuity Rules

When using this file:

1. Preserve Qubes security boundaries.
2. Separate confirmed from planned.
3. Do not infer a recommendation was applied.
4. Keep dom0 minimal.
5. Keep Cherry-AI contained.
6. Use narrow cross-qube services.
7. Measure performance.
8. Preserve rollback.
9. Prefer local/open/self-hosted options.
10. Record major changes in Project Digital Cross.
11. Keep Git as the technical source of truth.
12. Keep the active Project Digital Fortress checklist visible during ongoing setup work.

# End
