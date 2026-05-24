# Rollout Plan

## Rollout Type

- Direct release
- Feature-flagged release
- Canary release
- Pilot release
- Internal-only release

## Steps

| Step | Audience | Action | Verification | Rollback Trigger |
|---|---|---|---|---|
| 1 | internal | deploy/enable | smoke pass | smoke fail |
| 2 | pilot | increase flag | metrics healthy | error spike |
| 3 | all | full rollout | SLO healthy | incident |
