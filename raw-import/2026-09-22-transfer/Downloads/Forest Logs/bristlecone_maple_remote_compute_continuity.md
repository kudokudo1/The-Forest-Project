# Bristlecone, Maple, and Remote Compute Node — Continuity Record

**Created:** August 6, 2026  
**Purpose:** Restore context in ChatGPT or another AI about the discussion concerning Qubes vCPU allocation, Maple training, and using a second computer as a remote CPU/GPU/storage node.

---

## 1. Current System Context

### Main Qubes computer

- Qubes OS version observed: **4.3.1**
- Host memory available to Xen: approximately **32 GB**
- Xen-visible CPU count: **8**
- CPU topology observed: **8 cores, one thread per core**
- Host graphics card identified: **AMD Radeon RX 580**
- Cherry-AI currently does not appear to have direct GPU access.
- Ollama inference in Cherry-AI is currently **CPU-only**.

### Cherry-AI / Bristlecone

- Cherry-AI is the qube hosting Bristlecone Pine.
- Bristlecone is the first Tree and acts as a Treewright.
- Current model observed: `bristlecone-qwen35:4b-64k`
- Model size observed: approximately **5.6 GB**
- Context setting observed: **64,000 tokens**
- Current normal Cherry-AI setting: **9 vCPUs**
- Cherry-AI memory settings previously observed:
  - Initial memory: **8192 MB**
  - Maximum memory: **16000 MB**
- Ollama's active worker used approximately **6.3 GB RAM** during observation.
- Hermes was running and used comparatively little memory.
- Newelle was not running during the process inspection.
- No accidental duplicate primary model server was identified. The visible `llama-server` process was Ollama's own worker.

### Maple

- Maple is the user's personal qube and is being considered as the controller for training Seeds or another AI.
- Maple currently has:
  - **4 vCPUs**
  - Initial memory previously observed: **800 MB**
  - Maximum memory previously observed: **8000 MB**
- The user can copy and paste commands into Maple and Cherry-AI.
- The user cannot copy and paste into dom0, so dom0 commands should remain short or medium length and suitable for manual typing.

---

## 2. Important vCPU Explanation

A Qubes `vCPU` is not a permanently reserved physical core.

Xen schedules virtual CPUs across the host's real CPU cores. This means the total configured vCPU count across all qubes may exceed the eight physical cores.

Example:

```text
Physical host cores: 8

Cherry-AI: 9 vCPUs
Maple: 4 vCPUs
Service qubes: additional vCPUs
```

This is called **CPU oversubscription**.

The ninth Cherry-AI vCPU does not create a ninth physical core. It gives the guest another schedulable execution thread. When several qubes are CPU-heavy at the same time, their virtual CPUs compete for the same eight real cores.

### Practical meaning

- Idle vCPUs consume very little actual CPU time.
- Busy vCPUs compete for physical execution time.
- More vCPUs can sometimes improve utilization.
- Too many busy vCPUs can cause context switching, cache contention, heat, lower responsiveness, and worse total efficiency.
- Configured vCPU totals do not need to add up to eight.
- Simultaneously active CPU-heavy workloads should be benchmarked rather than guessed.

---

## 3. Cherry-AI vCPU Benchmark

A repeatable Ollama benchmark was run with Cherry-AI at nine and eight vCPUs.

### Nine vCPUs

- Cold run: approximately **4.67 tokens/second**
- Warm runs: approximately **5.58 and 6.03 tokens/second**
- Average including cold run: approximately **5.43 tokens/second**
- Warm average: approximately **5.81 tokens/second**

### Eight vCPUs

- Runs: approximately **2.85, 2.89, and 2.78 tokens/second**
- Average: approximately **2.84 tokens/second**

### Current interpretation

Eight vCPUs performed much worse in this test, so nine vCPUs remains the **provisional normal Bristlecone setting**.

However, the difference was unusually large for a one-vCPU change. Possible influences include:

- Ollama thread selection
- Model state
- CPU frequency
- temperature
- other running qubes
- cold-versus-warm conditions
- scheduling differences

Therefore, nine vCPUs should be treated as provisionally best for normal Bristlecone-only use, not as a universal rule.

---

## 4. Proposed Resource Profiles

### Normal Bristlecone Work State

Purpose: maximize Bristlecone responsiveness.

Tentative configuration:

```text
Cherry-AI: 9 vCPUs
Maple: light or idle
Maple training: off
Unused qubes: stopped
```

### Maple Training Work State

Purpose: prioritize training on Maple or a training node.

Preferred approach:

```text
Cherry-AI: stopped, or its Ollama model unloaded
Maple: 6-8 vCPUs, subject to benchmarking
Unused qubes: stopped
```

Stopping Cherry-AI or unloading Bristlecone's model helps more than simply reducing Cherry-AI by one or two vCPUs because it frees both CPU activity and several gigabytes of RAM.

### Mixed AI Work State

Purpose: keep Bristlecone available while Maple trains.

Initial configurations to benchmark:

```text
Balanced:
Cherry-AI: 3-4 vCPUs
Maple: 3-4 vCPUs
```

```text
Training priority:
Cherry-AI: 2-3 vCPUs
Maple: 5-6 vCPUs
```

Both AIs will be slower than when running alone.

### Decision status

- **Nine vCPUs for normal Bristlecone use:** provisional preference
- **Dedicated training profile:** recommended
- **Mixed-mode allocation:** not yet benchmarked
- **Final Maple training resources:** not yet determined

---

## 5. Second Computer as Additional Compute

### Zero-RAM limitation

A second computer cannot provide useful CPU cores with no real RAM installed.

The motherboard needs compatible physical RAM to:

- complete POST
- initialize firmware
- boot an operating system
- run networking software
- run training or inference programs

USB flash drives cannot replace boot-time system RAM.

### Flash drives

A flash drive may be used as:

- a Linux boot device
- storage
- emergency swap after Linux boots

It is not a useful substitute for physical RAM.

Using several flash drives as swap would likely produce:

- extremely slow performance
- system pauses
- high write wear
- unreliable training
- increased risk of failure if a drive disconnects

### Minimum viable second computer

The second computer needs:

- compatible physical RAM
- CPU and motherboard
- working power supply
- cooling
- bootable USB drive or SSD
- Ethernet
- optional working GPU and drivers

Even a small amount of RAM can make it useful for light support tasks. Serious model training may require substantially more RAM and possibly VRAM.

---

## 6. What Ethernet Provides

Ethernet does not merge the two motherboards or make the second CPU appear as additional Xen cores.

Instead, it provides a fast communication channel for:

- remote commands
- SSH sessions
- prompts and responses
- model API requests
- datasets
- checkpoints
- model files
- training logs
- shared folders
- completed results
- remote desktop traffic

Correct mental model:

```text
Maple or Cherry-AI
        |
        | Ethernet
        v
Remote computer performs the job
        |
        | results, logs, files
        v
Maple or Cherry-AI
```

The remote CPU and GPU remain owned by the second computer. Programs using those resources execute on the second computer.

---

## 7. How the Second Computer Could Feel Seamless

The second computer must boot its own operating system, but it does not need its own permanent keyboard, mouse, or monitor.

### Initial setup

During installation, the user may:

- connect the second computer to another monitor input
- use the monitor's Source/Input button
- temporarily attach a keyboard and mouse

### Normal daily use

After setup, run the second machine headlessly and access it from Maple through:

- SSH terminal
- a web dashboard
- remote desktop
- mounted shared folders
- an API such as remote Ollama

Example:

```text
Maple desktop
├── normal Maple applications
├── SSH terminal controlling training node
├── mounted remote files
└── optional remote desktop window
```

The user can then use normal desktop switching such as **Alt+Tab** because the remote session is displayed inside a Maple window.

The experience may feel like another application or workstation, but the systems remain technically separate.

---

## 8. Recommended Remote Node Roles

### Remote Training Node

Maple remains the controller while the second computer runs the full training job.

Install on the remote computer as needed:

- lightweight Linux
- GPU drivers
- Python
- PyTorch
- Unsloth
- training dependencies
- local model and dataset storage

Maple can:

1. prepare a job
2. send it to the node
3. start it over SSH or an API
4. monitor progress
5. retrieve checkpoints and results

### Remote AI Inference Node

Install:

- lightweight Linux
- GPU drivers
- Ollama or another model server
- required models

Hermes or Newelle can send model requests to the remote server. The answer returns to the local interface.

### Remote Support Node

The second computer could also handle:

- embeddings
- retrieval indexing
- code compilation
- testing
- document processing
- conversion jobs
- background automation
- storage

### Distributed training

PyTorch can combine multiple computers in a distributed training job, but that is more complex. Each node still needs its own software, RAM, and network configuration.

The recommended first step is whole-job offloading, not multi-node distributed training.

---

## 9. File and Storage Access

Remote storage can be made visible inside Maple using:

- SSH/SFTP
- `rsync`
- NFS
- Samba
- a controlled web interface

Possible layout:

```text
Training-Node/
├── datasets/
├── models/
├── checkpoints/
├── logs/
└── completed/
```

For large training jobs, copy datasets and models to the remote node's local SSD before running. Constantly reading large files over Ethernet may reduce performance.

---

## 10. Dedicated Qubes Connector Decision

A dedicated low-resource AppVM is recommended instead of allowing Maple to communicate directly with the remote node at all times.

Possible names:

- `Compute-Bridge`
- `Maple-Link`
- `Training-Gate`

### Recommended architecture

```text
Maple
  |
  | approved qrexec/file transfer
  v
Compute-Bridge AppVM
  |
  | tightly restricted network connection
  v
Remote Training Node
```

### Purpose of the connector qube

- send SSH commands
- upload datasets
- download checkpoints
- contact a remote Ollama or training API
- monitor jobs
- limit the remote machine's relationship with Maple
- isolate files received from the remote machine
- enforce destination and port restrictions

### Initial resource target

Tentative starting allocation:

```text
vCPUs: 1
Memory: 400-600 MB
Max memory: 1000-2000 MB
```

Increase only if encryption, compression, mounted shares, or large transfers become a measured bottleneck.

### Type of qube

Use an ordinary **AppVM**, not a `sys-*` qube, because it does not initially need to provide networking to other qubes.

Start with the normal Fedora template for easier setup. Consider a minimal template later after the workflow is proven.

### Network restrictions

Eventually restrict the connector qube to:

- the training node's local IP
- SSH, likely TCP port 22
- the specific remote AI API port
- a file-sharing port only when required

All unrelated network access should remain blocked when practical.

### Tradeoff

Direct Maple access:

- simpler
- slightly fewer transfer steps
- creates a more direct trust relationship

Dedicated connector qube:

- stronger isolation
- clearer permissions
- small RAM cost
- one additional file-transfer step

### Tentative decision

Use:

```text
Maple -> Compute-Bridge -> Remote Training Node
```

This is the preferred design because it fits Qubes and Forest compartmentalization principles.

---

## 11. Proposed Forest Architecture

```text
Main Qubes computer
├── Cherry-AI
│   ├── Bristlecone Pine
│   ├── Hermes
│   └── Ollama
├── Maple
│   └── training controller / project workspace
├── Compute-Bridge
│   ├── SSH
│   ├── rsync/SFTP
│   ├── remote APIs
│   └── restricted network rules
└── sys-firewall -> sys-net
          |
          | Ethernet / LAN
          v
Remote Training Node
├── lightweight Linux
├── CPU
├── GPU
├── physical RAM
├── SSD or USB boot device
├── local datasets and models
├── Ollama, when used for inference
├── PyTorch/Unsloth, when used for training
└── SSH/API/file-transfer services
```

---

## 12. Principles to Preserve

- Keep Qubes isolation intact.
- Do not connect Cherry-AI directly to `sys-net` for speed.
- Keep `sys-firewall` in the network path.
- Prefer local-first, private, free, open-source, and self-hostable tools.
- Do not disable approval or security controls for performance.
- Do not expose experimental inference RPC services to the public internet.
- Use authenticated and restricted communication.
- Benchmark changes rather than assuming they help.
- Keep rollback paths for resource and network changes.
- Keep the remote node's permissions narrower than Maple's full permissions.
- Scan or review returned files before trusting them.

---

## 13. Open Questions

These decisions remain unresolved:

- What CPU, motherboard, GPU, and RAM type are in the second computer?
- How much compatible RAM can be installed today?
- Does the second computer have an SSD?
- Does its GPU support the intended training or inference framework?
- Will the node primarily train, run inference, index data, or do several roles?
- What local Ethernet speed is available?
- Will the remote node run continuously or only on demand?
- What Linux distribution should be used?
- What exact shared-file method should be used?
- What IP address and firewall rules should be assigned?
- What memory and vCPU allocation should `Compute-Bridge` use after benchmarking?
- Should Maple connect to the bridge through manual Qubes file copy at first or a custom qrexec service later?
- What mixed Cherry-AI/Maple resource allocation performs best?
- Should Bristlecone's 64K context be reduced for normal tasks?

---

## 14. Recommended Next Steps

1. Restore and confirm Cherry-AI at nine vCPUs for normal Bristlecone use.
2. Identify the second computer's motherboard, CPU, RAM type, GPU, storage, and power supply.
3. Install compatible physical RAM.
4. Boot a lightweight Linux system from USB or SSD.
5. Connect the second computer to the local network by Ethernet.
6. Assign it a stable local hostname and IP.
7. Enable SSH with key-based authentication.
8. Test remote access from a temporary qube first.
9. Create the dedicated `Compute-Bridge` AppVM.
10. Restrict `Compute-Bridge` to the remote node and required ports.
11. Test sending and receiving a small file.
12. Test running a simple remote command.
13. Decide whether the first real workload will be:
    - remote inference
    - a training job
    - code compilation/testing
    - retrieval indexing
14. Benchmark the remote workload against running it locally.
15. Create Normal Bristlecone, Maple Training, and Mixed AI work states only after tests produce reliable values.

---

## 15. Continuity Instruction for Another AI

Treat this document as the authoritative continuity record for the discussion about:

- Qubes vCPU oversubscription
- Cherry-AI and Maple resource sharing
- Maple training profiles
- adding a second computer as a remote compute node
- headless access over Ethernet
- seamless file and command transfer
- using a dedicated `Compute-Bridge` AppVM

Do not claim that the remote computer's CPU or GPU becomes local Qubes hardware. It remains a separate node that receives jobs and returns results.

Do not mark tentative decisions as implemented until the user confirms they were configured and tested.
