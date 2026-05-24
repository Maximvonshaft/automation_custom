# CODEX MASTER PROMPT - v4.1 Drag-and-Drop Manifest Runtime + Real GUI Executor

You are implementing CustomsOps Autopilot v4.1 from `main` commit
`45fd4a9f5f95247432814293bced96badc80cd10`.

## Current Repository Facts

- `main` is v4.0 Controlled Runtime MVP.
- Local Agent currently uses `MockActionExecutor`.
- Real Windows/ASYCUDA foreground GUI execution is not implemented.
- Signed-plan validation already exists and must remain in front of every executor path.
- Control Plane compiles job plans using server-side pack values.
- Pack isolation tests already protect `agent/`.
- v3.1.1 SafeBrake is the verified field-runtime baseline.

## Product Target

Operator drags a fixed Excel template into the software. The Control Plane parses it, builds a
declaration model, compiles a signed SafeBrake job plan server-side, the Windows Agent validates and
executes it through foreground GUI actions, and the Agent produces a watermarked evidence bundle.

## Hard Boundaries

- No Submit/Register/Payment/tax-finalizing automation.
- No country pack content in `agent/`.
- No local executable job compilation from Excel.
- No real customer data committed.
- SafeBrake remains default.
- Modes remain `fillOnly` and `safeBrakeStore`.
- Real GUI execution is Windows-only and fail-closed outside controlled Windows execution.

## Required Final Verification

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

