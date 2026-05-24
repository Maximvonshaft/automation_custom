# Alerting Policy

## Alert Severity

| Alert | Condition | Severity | Action |
|---|---|---|---|
| Critical workflow down | success rate below threshold | SEV1 | page owner |
| Error spike | error rate exceeds threshold | SEV2 | investigate |
| Latency spike | p95 exceeds threshold | SEV3 | monitor/investigate |

## Alert Quality

- Every alert needs owner.
- Every alert needs runbook.
- Avoid noisy alerts without action.
