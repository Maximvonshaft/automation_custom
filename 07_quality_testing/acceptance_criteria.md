# Acceptance Criteria

## Security acceptance

- Agent refuses unsigned job plan.
- Agent refuses job plan with invalid signature.
- Agent refuses expired job plan.
- Agent refuses job plan for another machine.
- Agent refuses job plan for another tenant.
- Agent refuses forbidden actions: Submit/Register/Payment/Tax.
- Agent refuses modes not enabled for tenant/machine.
- Complete Country Pack files are absent from Agent build artifact.

## Functional acceptance

- Control Plane can compile a SafeBrake job from server-side pack stub.
- Control Plane signs the job plan.
- Agent validates and executes a signed dry-run or mock executor plan in CI.
- Agent produces watermarked evidence bundle.
- Evidence bundle includes job_id, tenant_id, machine_id, pack_id, pack_version, mode, agent_version.
- Kill switch causes license check failure.

## Operational acceptance

- Local build creates an executable or reproducible package.
- CI runs unit tests and security checks.
- Deployment runbook exists.
- Rollback plan exists.
- Final report template is completed by engineer.
