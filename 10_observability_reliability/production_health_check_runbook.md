# Production Health Check Runbook

## Check Sequence

1. Confirm deployed commit/version.
2. Confirm app health endpoint.
3. Confirm affected page loads.
4. Confirm critical API route.
5. Confirm logs have no new error spike.
6. Confirm metrics are within threshold.
7. Confirm support channel has no critical user report.

## Decision

- Healthy: continue monitoring.
- Degraded: keep release, open follow-up if workaround exists.
- Critical: rollback or disable feature flag.
