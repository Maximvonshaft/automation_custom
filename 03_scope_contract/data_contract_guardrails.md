# Data Contract Guardrails

## Entities

- Tenant
- Machine
- License
- CountryPack
- Job
- Run
- EvidenceBundle
- AuditEvent

## Required IDs

All operational records must include:

- `tenant_id`
- `machine_id`
- `job_id`
- `run_id`
- `pack_id`
- `pack_version`
- `mode`
- `created_at`
- `expires_at`

## Sensitive data

Do not store ASYCUDA passwords, cookies, session tokens, or operator credentials.

## Evidence retention

Evidence retention policy must be configurable by tenant and default to a conservative internal audit retention period.
