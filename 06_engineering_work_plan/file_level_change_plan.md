# File-Level Change Plan

Codex must adapt paths to the actual repository. If the repository is empty, create this structure.

## Shared schemas

```text
shared/schemas/job_plan.schema.json
shared/schemas/action.schema.json
shared/schemas/evidence_manifest.schema.json
shared/schemas/license.schema.json
shared/signing/ed25519.py
shared/watermark.py
```

## Control Plane

```text
control_plane/app/main.py
control_plane/app/core/config.py
control_plane/app/core/security.py
control_plane/app/core/signing.py
control_plane/app/db/session.py
control_plane/app/db/models.py
control_plane/app/api/health.py
control_plane/app/api/machines.py
control_plane/app/api/licenses.py
control_plane/app/api/jobs.py
control_plane/app/api/evidence.py
control_plane/app/api/admin.py
control_plane/app/services/pack_loader.py
control_plane/app/services/job_compiler.py
control_plane/app/services/job_signer.py
control_plane/app/services/evidence_store.py
control_plane/packs/albania_asycuda/README_INTERNAL_ONLY.md
control_plane/packs/albania_asycuda/field_map.example.yaml
control_plane/packs/albania_asycuda/safebrake_policy.example.yaml
```

## Local Agent

```text
agent/customsops_agent/main.py
agent/customsops_agent/config.py
agent/customsops_agent/signed_plan.py
agent/customsops_agent/license_check.py
agent/customsops_agent/machine_fingerprint.py
agent/customsops_agent/action_executor.py
agent/customsops_agent/window_guard.py
agent/customsops_agent/clipboard_executor.py
agent/customsops_agent/screenshot.py
agent/customsops_agent/ledger.py
agent/customsops_agent/evidence_bundle.py
agent/customsops_agent/forbidden_actions.py
agent/build_nuitka.ps1
```

## Tests

```text
tests/test_job_plan_signature.py
tests/test_reject_expired_job.py
tests/test_reject_wrong_machine.py
tests/test_forbidden_actions.py
tests/test_evidence_watermark.py
tests/test_pack_not_in_agent.py
tests/test_safebrake_job_compile.py
```

## Documentation

```text
docs/operator_guide.md
docs/admin_guide.md
docs/security_model.md
docs/release_runbook.md
```
