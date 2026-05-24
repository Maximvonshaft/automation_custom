# API Contract Guardrails

The Control Plane API must be versioned under `/api/v1`.

Required endpoints:

- `GET /api/v1/healthz`
- `POST /api/v1/machines/register`
- `POST /api/v1/licenses/check`
- `POST /api/v1/jobs/compile`
- `GET /api/v1/jobs/{job_id}`
- `POST /api/v1/jobs/{job_id}/runs/start`
- `POST /api/v1/jobs/{job_id}/runs/{run_id}/evidence`
- `POST /api/v1/admin/machines/{machine_id}/revoke`
- `POST /api/v1/admin/tenants/{tenant_id}/suspend`

Contracts must include explicit error codes for:

- invalid signature
- expired job
- machine mismatch
- tenant mismatch
- revoked machine
- unauthorized mode
- pack disabled
