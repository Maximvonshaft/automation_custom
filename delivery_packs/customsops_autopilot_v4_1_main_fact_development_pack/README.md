# CustomsOps Autopilot v4.1 Development Construction Pack

This pack is a production development plan for v4.1, based on the factual `main` code state at:

```text
45fd4a9f5f95247432814293bced96badc80cd10
```

## Purpose

v4.1 will extend the v4.0 Controlled Runtime MVP with:

- fixed Excel manifest drag-and-drop intake;
- server-side manifest parsing and declaration model building;
- signed job-plan compilation from declaration models;
- Windows-only ASYCUDA foreground GUI executor integration;
- evidence bundle compatibility with v3.1.1 screenshots and ledger review patterns;
- SafeBrake preservation as the default controlled validation mode.

## Current Main Facts

- `main` contains the v4.0 Controlled Runtime MVP.
- Local Agent execution is currently `MockActionExecutor`.
- Real Windows/ASYCUDA foreground GUI execution is not implemented in `main`.
- Signed-plan validation already enforces signature, tenant, machine, expiry, mode, and allowed action checks.
- Control Plane job compilation already uses server-side country pack values.
- Pack isolation tests already fail if country-pack content appears under `agent/`.
- `v3.1.1 SafeBrake` remains the verified field-runtime baseline.

## Hard Boundaries

- Do not add Submit/Register/Payment/tax-finalizing automation.
- Do not move country pack content into `agent/`.
- Do not let the Agent compile executable ASYCUDA steps locally from Excel.
- Do not commit real customer manifest data.
- Keep runtime modes limited to `fillOnly` and `safeBrakeStore`.
- Keep the real GUI executor Windows-only and fail-closed outside controlled Windows execution.
- Do not distribute the repository or this pack as an external operator package.

## Execution Order

1. Audit current `main` facts.
2. Implement manifest template intake contract.
3. Build declaration model parser and validator.
4. Extend server-side signed job compiler.
5. Add Windows-only GUI executor adapter behind signed-plan validation.
6. Add operator drag-and-drop shell without exposing country pack content.
7. Preserve evidence bundle compatibility and release gates.

## Required Validation

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

