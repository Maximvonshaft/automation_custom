# Logging / Metrics / Tracing Spec

## Agent logs

- job_id
- run_id
- tenant_id
- machine_id
- mode
- step_count
- action types only, not secrets
- rejection reason if job rejected
- evidence bundle path/hash

## Control Plane metrics

- jobs compiled
- jobs executed
- rejected license checks
- revoked machine attempts
- evidence upload success/failure
- pack version usage

## Alerts

- repeated invalid signature attempts
- repeated wrong-machine attempts
- revoked machine still requesting jobs
- evidence upload failures
