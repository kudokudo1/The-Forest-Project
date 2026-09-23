# Bristlecone Pine — Resource Governor and Colony Runtime Reconciliation

Status: **RECONCILED — CERTIFIED**

## Resource Request / Governor

The surviving current `resources/` package is selected as the recovered Phase 14.11 resource-governance implementation.

Every current Python file in the package has at least one exact certified backup match:

- resources/__init__.py
- resources/availability.py
- resources/budget.py
- resources/decision.py
- resources/evaluation.py
- resources/governor.py
- resources/live_providers.py
- resources/model.py
- resources/request_preparation.py
- resources/requirement.py

Several have exact matches in the later Phase 14.11L.8 governor certification archive.

### Certified semantic boundary

Reasoning -> Model Form -> exact ResourceRequest -> Governor -> APPROVE / DEFER / DENY -> runtime execution only if allowed.

The Governor may decide whether the requested resources can be granted. It does **not** silently rewrite Reasoning or Model Form.

### L.8 A+B certification

L.8 Terminal A records pure Governor approve median 2.795 µs, live availability median 22.843 µs, nonresident residency-aware requirement median 373.534 µs, whole live Small Governor median 449.952 µs, and resident residency-aware requirement median 406.455 µs.

Certified fail-closed behavior includes DEFER vs DENY based on may_defer for unknown requirements, insufficient availability, or unknown availability, while a zero-requirement request bypasses availability and is approved.

Terminal B independently verified artifact integrity, the Governor semantic matrix, provider ordering, zero-requirement bypass, and residency calculation.

Historical timing values are preserved as evidence, not predictions for the modern Post-Apollo runtime.

## Colony runtime semantics

Selected: colony/__init__.py and colony/identity.py. Both current files are byte-identical to certified Phase 14.11H snapshots.

The already-promoted H.7 final certification establishes that a Colony is one Tree plus its Clones/Ramets; tree_id is durable Tree/Colony identity; execution_context_id identifies one Ortet/Ramet execution context; runtime session identity is execution_context_id + binding_id; model-weight residency may be shared while live session/control/KV state remains separate; Model Form, Reasoning, Task, Workshop, temporary capability state, and lifecycle operations remain execution-context local.

## Recovery conclusion

Resource Governor and Colony runtime semantics are grounded in current files that match certified snapshots plus explicit certification records. Modern Rust reconstruction should preserve these boundaries and re-run certification against the new runtime/hardware.