# READ THIS FIRST - CustomsOps Autopilot v4.1 Development Pack

## Mission

Use this pack to implement **CustomsOps Autopilot v4.1 Drag-and-Drop Manifest Runtime + Real GUI
Executor** on top of current `main` facts.

The target workflow is:

```text
operator drags fixed Excel manifest
  -> Control Plane parses and validates it
  -> Control Plane builds a declaration model
  -> Control Plane compiles a signed SafeBrake job plan
  -> Windows Agent validates the signed plan
  -> Windows Agent executes ASYCUDA foreground GUI steps
  -> Agent produces watermarked evidence compatible with v3.1.1 review
```

## Current Main Facts

Baseline commit:

```text
45fd4a9f5f95247432814293bced96badc80cd10
```

- `main` contains v4.0 Controlled Runtime MVP.
- `agent/customsops_agent/action_executor.py` contains `MockActionExecutor`; no real GUI executor exists.
- `agent/customsops_agent/signed_plan.py` validates signature, tenant, machine, expiry, mode, and action whitelist.
- `control_plane/app/services/job_compiler.py` compiles signed-plan payloads from server-side pack values.
- `control_plane/packs/**` is server-side only and must stay out of `agent/`.
- `tests/test_pack_not_in_agent.py` and `tests/test_v4_mvp_boundary.py` document the containment boundary.
- `v3.1.1 SafeBrake` remains the verified field-runtime baseline.

## Hard Rules

1. Do not implement Submit/Register/Payment/tax-finalizing automation.
2. Do not move `control_plane/packs/**` or real pack content into `agent/`.
3. Do not let the local Agent compile executable job plans from Excel locally.
4. Do not commit real customer manifest data; use sanitized fixtures only.
5. Keep runtime modes limited to `fillOnly` and `safeBrakeStore`.
6. Preserve SafeBrake as the default production validation mode.
7. Real GUI executor must be Windows-only and fail closed outside controlled Windows execution.

## Execute Order

1. `17_codex_prompts/CODEX_MASTER_PROMPT.md`
2. `17_codex_prompts/CODEX_TASK_00_MAIN_FACT_AUDIT.md`
3. `17_codex_prompts/CODEX_TASK_01_MANIFEST_TEMPLATE_INTAKE.md`
4. `17_codex_prompts/CODEX_TASK_02_DECLARATION_MODEL_BUILDER.md`
5. `17_codex_prompts/CODEX_TASK_03_SIGNED_JOB_COMPILER_EXTENSION.md`
6. `17_codex_prompts/CODEX_TASK_04_REAL_GUI_EXECUTOR_ADAPTER.md`
7. `17_codex_prompts/CODEX_TASK_05_OPERATOR_DRAGDROP_UX.md`
8. `17_codex_prompts/CODEX_TASK_06_EVIDENCE_AND_RELEASE_GATE.md`

## Required Validation

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

