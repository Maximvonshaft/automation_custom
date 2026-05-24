# Backward Compatibility Contract

## Compatibility Requirements

- Existing routes should not break unless redirected.
- Existing API clients must continue to work.
- Existing user roles must retain expected access.
- Existing saved data must render correctly.
- Existing tests should pass without weakening assertions.

## Compatibility Checklist

- [ ] Routes checked
- [ ] API contract checked
- [ ] DB schema checked
- [ ] Existing data rendering checked
- [ ] RBAC checked
- [ ] Feature flag/rollback checked
