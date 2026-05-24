# Control Plane API Contract

MVP endpoints:

```http
GET /api/v1/healthz
POST /api/v1/machines/register
POST /api/v1/licenses/check
POST /api/v1/jobs/compile
GET /api/v1/jobs/{job_id}
POST /api/v1/jobs/{job_id}/runs/start
POST /api/v1/jobs/{job_id}/runs/{run_id}/evidence
POST /api/v1/admin/machines/{machine_id}/revoke
```

All endpoints must log audit events.
