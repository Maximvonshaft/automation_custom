# Post-release Smoke Tests

## Smoke Test Template

| Smoke ID | Step | Expected Result | Owner | Status |
|---|---|---|---|---|
| SM-001 | Open affected page | page loads | QA/Release owner | Draft |
| SM-002 | Execute critical action | success feedback shown | QA/Release owner | Draft |
| SM-003 | Trigger safe error case | actionable error shown | QA/Release owner | Draft |
| SM-004 | Check logs/metrics | no abnormal spike | Release owner | Draft |

## Rules

- Smoke tests run after deployment.
- Failures trigger go/no-go decision.
- Severe failure triggers rollback.
