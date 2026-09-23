PHASE 14 — LAYERED HOT CONTEXT / PERFORMANCE
│
├── ✅ 14.1 — Prompt / Schema Baseline
│
├── ✅ 14.2 — Cold / Warm Latency Baseline
│
├── ✅ 14.3 — Repeated-Work Map
│
├── ✅ 14.4 — Hot-Turn Audit
│
├── ✅ 14.5 — Forest Cache Architecture
│   │
│   ├── ✅ 14.5A–C — Existing cache audit / classification
│   ├── ✅ 14.5D — CacheCoordinator foundation
│   ├── ✅ 14.5E — Dependency-aware invalidation
│   ├── ✅ 14.5F–G — Skill-overlay migration
│   └── ✅ 14.5H — Final cache architecture verification
│
├── → 14.6 — Core Forest Reuse / Context Infrastructure
│   │
│   ├── ✅ 14.6A — YAML / Manifest Map
│   ├── ✅ 14.6B — Resolver Lifecycle
│   ├── ✅ 14.6C — Integration Points
│   │
│   ├── ✅ 14.6D — Parsed-YAML Cache
│   │
│   ├── ✅ 14.6E — Capability-Resolution Cache
│   │
│   ├── ✅ 14.6F0 — Cache Ownership / Hermes Overlap Audit
│   │
│   ├── ✅ 14.6F0.1 — Dormant Forest Tool-Availability Provider
│   │   │
│   │   ├── Hermes availability cache stays ACTIVE
│   │   ├── Forest replacement stays DORMANT
│   │   ├── shared across Clones where infrastructure is identical
│   │   └── Clone permission remains separate from availability
│   │
│   ├── → 14.6F — Forest Learning + User Context Infrastructure
│   │   │
│   │   ├── ⏸ 14.6F1 — Existing Learning Preflight
│   │   │          COMPLETE
│   │   │
│   │   ├── → 14.6F2 — Durable Learning + User Context Foundation
│   │   │   ├── Operational Learning
│   │   │   ├── User Preferences
│   │   │   ├── User Constraints
│   │   │   ├── User Corrections
│   │   │   ├── Current Context
│   │   │   ├── immutable revision history
│   │   │   ├── provenance / source refs
│   │   │   ├── Tree + Clone origin
│   │   │   ├── General / Workshop / Tree / Clone scope
│   │   │   ├── protection hooks
│   │   │   └── User Context Generation
│   │   │
│   │   ├── □ 14.6F3 — Warm Derived Indexes
│   │   │   ├── Operational Learning Index
│   │   │   └── Context Trigger Index
│   │   │
│   │   └── □ 14.6F4 — Context Routing State
│   │       ├── Context Route Stamp
│   │       ├── input generation
│   │       ├── User Context generation invalidation
│   │       └── Task-Sticky User Context
│   │
│   └── □ 14.6G — 14.6 Integration / Cache Audit
│       ├── verify no duplicate Hermes caching
│       ├── Clone scaling checks
│       ├── cold/warm/hot ownership
│       └── cache-loss rebuild tests
│
├── □ 14.7 — Layered Hot Context Assembler
│   │
│   ├── Base Tree Core
│   ├── matched User Context only
│   ├── relevant Operational Learning only
│   ├── Workshop Core
│   ├── Clone-specific context
│   ├── General / Ready
│   ├── Task-Sticky Skills
│   ├── temporary capabilities
│   ├── relevant Leaves
│   └── current Task
│
├── □ 14.8 — Runtime Cache / Prefix Integration
│   │
│   ├── runtime cache provider contract
│   ├── Hermes provider
│   ├── dormant Forest-native replacement path
│   ├── session/prefix ownership
│   └── leave KV/inference state runtime-owned
│
├── □ 14.9 — Source-Context Targeting
│
├── □ 14.10 — Quick / Normal / Deep
│   └── automatic reasoning-depth selection
│
├── □ 14.11 — Small / Big Model Escalation
│
├── □ 14.12 — Ollama vs. llama.cpp Evaluation
│
├── □ 14.13 — Speculative Decoding Evaluation
│
└── □ 14.14 — Final Performance Benchmark
✅ 14.10A — Hermes reasoning contract
✅ 14.10B — canonical reasoning model
✅ 14.10C — deterministic automatic router
✅ 14.10D — Hermes runtime translation
✅ 14.10E — frozen turn + stale recovery

→ 14.10E.1 — Human Reasoning Control State
   • rename user-facing Quick → Light
   • canonical levels: Light / Normal / Deep
   • Auto is a routing policy, not a reasoning level
   • Auto chooses Light / Normal / Deep
   • durable pinned baseline:
       Auto
       Pin Light
       Pin Normal
       Pin Deep
   • temporary override sits above baseline
   • temporary default = 5 meaningful turns
   • configurable later through Spirit
   • retries/tool calls/recovery do NOT consume turns
   • temporary mode survives ordinary restart
   • pinned baseline survives ordinary restart
   • temporary expiration restores the underlying baseline
   • changing the pinned baseline while temporary is active
     does NOT cancel the temporary lease

   Priority:
       explicit current-turn request
       > temporary lease
       > pinned baseline
       > Auto router
       > Normal fail-safe

→ 14.10E.2 — Native Forest Reasoning Menu
   • Forest-owned, not rofi
   • bare-bones native UI first
   • later restyled into Spirit
   • keyboard and clickable
   • NumLock OFF + Num2 = temporary menu
   • Super + NumLock OFF + Num2 = pinned/baseline menu
   • 0 = Auto
   • 1 = Light
   • 2 = Normal
   • 3 = Deep
   • menu shows current baseline
   • menu shows temporary mode + turns remaining
   • UI contains no reasoning-policy logic itself
   • i3 only launches the Forest menu

□ 14.10F — certification / benchmark
   • automatic Light/Normal/Deep
   • pinned Light
   • pinned Normal
   • pinned Deep
   • temporary lease consumption
   • default 5-turn lease
   • temporary-over-pinned restoration
   • restart persistence
   • stale recovery consumes zero extra turns
   • explicit override precedence
   • deterministic routing
   • routing overhead
   • no Hermes config drift
   • no accidental Task-Sticky Deep