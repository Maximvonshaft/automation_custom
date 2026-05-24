# Data Migration Plan

Use this only if data model changes are required.

## Migration Summary

- Migration needed: Yes / No
- Backfill needed: Yes / No
- Downtime needed: Yes / No
- Reversible: Yes / No

## Plan

| Step | Action | Owner | Verification | Rollback |
|---|---|---|---|---|
| 1 | Add nullable column | Engineer | migration passes | drop column if safe |

## Data Safety

- [ ] Backup considered
- [ ] Migration tested locally/staging
- [ ] Backward compatibility confirmed
- [ ] Rollback plan documented
