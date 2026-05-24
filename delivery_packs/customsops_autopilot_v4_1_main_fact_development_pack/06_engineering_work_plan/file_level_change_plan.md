# File-Level Change Plan

Codex must adapt this plan to current `main` without moving country-pack content into `agent/`.

## Add / Modify Control Plane

- `control_plane/app/services/manifest_template_classifier.py`
  - Detect `Sheet1`, `Combine`, `Separate`, and `Simplified`.
  - Return a structured parse report, not executable actions.
- `control_plane/app/services/manifest_parser.py`
  - Parse sanitized fixed-template rows.
  - Reject ambiguous, unsupported, or malformed templates.
- `control_plane/app/services/declaration_builder.py`
  - Build neutral declaration models from parsed rows.
  - Preserve source row references for evidence/audit.
- `control_plane/app/api/manifests.py`
  - Accept manifest uploads or prechecked manifest metadata.
  - Return parse report and declaration model IDs.
- `control_plane/app/services/job_compiler.py`
  - Add declaration-model input path.
  - Keep pack loading and executable action compilation server-side.
- `control_plane/app/services/pack_loader.py`
  - Preserve server-side-only pack boundary.

## Add / Modify Agent

- `agent/customsops_agent/intake.py`
  - Local file hash and template-shape precheck only.
  - No executable step compilation.
- `agent/customsops_agent/executor_interface.py`
  - Define a protocol shared by mock and real executors.
- `agent/customsops_agent/gui_executor.py`
  - Windows-only real GUI executor adapter.
  - Fail closed on non-Windows platforms.
- `agent/customsops_agent/windows_foreground.py`
  - ASYCUDA foreground window guard utilities.
- `agent/customsops_agent/action_executor.py`
  - Keep `MockActionExecutor`.
  - Add routing only after signed-plan validation.
- `agent/customsops_agent/main.py`
  - CLI commands: `intake`, `run`, `package-evidence`.

## Add Schemas

- `shared/schemas/manifest_template_contract.schema.json`
- `shared/schemas/manifest_parse_report.schema.json`
- `shared/schemas/declaration_model.schema.json`

## Add Tests

- `tests/test_manifest_template_classifier.py`
- `tests/test_manifest_parser_combine.py`
- `tests/test_manifest_parser_separate.py`
- `tests/test_declaration_model_builder.py`
- `tests/test_agent_cannot_compile_job_from_excel.py`
- `tests/test_real_gui_executor_boundary.py`
- `tests/test_evidence_manifest_intake_hashes.py`
- `tests/test_pack_not_in_agent.py` additions for packaged artifacts.
- `tests/test_forbidden_actions.py` additions for GUI adapter routing.

## Do Not Add

- No Submit/Register/Payment executors.
- No tax-finalizing actions.
- No real country pack under `agent/`.
- No real customer Excel rows as fixtures.
- No ASYCUDA credential/session/cookie handling.

