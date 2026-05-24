# Severity and Priority Taxonomy

## Severity

| Severity | Meaning | Example |
|---|---|---|
| S0 | Production outage, data loss, security breach | Users cannot access system |
| S1 | Core workflow broken | Customer cannot submit ticket |
| S2 | Major degradation with workaround | AI reply unavailable but manual reply works |
| S3 | Minor defect | Copy error, minor layout issue |
| S4 | Cosmetic/no direct impact | Spacing inconsistency |

## Priority

| Priority | Meaning | SLA |
|---|---|---|
| P0 | Stop-the-line | fix before release or hotfix now |
| P1 | Must fix before production | current release blocker |
| P2 | Should fix soon | next sprint/release |
| P3 | Nice-to-have | backlog |
| P4 | Archive/reference | no action now |

## Risk Class

| Risk | Required Controls |
|---|---|
| R1 | Peer review only |
| R2 | Peer review + automated tests |
| R3 | Peer review + tests + rollback plan |
| R4 | Security/privacy review + release gate |
| R5 | Formal approval + rollback drill + monitoring window |
