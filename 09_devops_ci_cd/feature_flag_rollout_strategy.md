# Feature Flag and Rollout Strategy

## When Required

Feature flag is recommended for:
- high-risk UI workflow changes,
- new AI/automation behavior,
- WebCall/WebChat behavior,
- permission-sensitive functions,
- data-writing changes.

## Rollout Plan

| Stage | Audience | Percentage | Duration | Exit Criteria |
|---|---|---:|---|---|
| Internal | staff/admin | 0-5% | TBD | smoke pass |
| Pilot | selected users | 5-25% | TBD | error rate acceptable |
| Gradual | broader users | 25-75% | TBD | SLO healthy |
| Full | all users | 100% | TBD | no blocker |

## Kill Switch

- Flag name:
- Owner:
- How to disable:
- Verification after disable:
