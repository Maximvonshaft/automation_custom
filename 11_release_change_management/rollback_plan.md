# Rollback Plan

## Control Plane rollback

1. Stop new job compilation.
2. Revoke affected pack version.
3. Disable affected API version if needed.
4. Restore previous server image/database backup.
5. Notify operators to stop runs.

## Agent rollback

1. Revoke bad Agent version in Control Plane.
2. Disable job issuance to that version.
3. Reinstall previous Agent.
4. Validate with mock signed job.

## Emergency stop

Set tenant or machine status to `revoked` or `suspended`.
