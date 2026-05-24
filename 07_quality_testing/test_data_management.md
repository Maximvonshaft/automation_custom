# Test Data Management

## Rules

- Do not use real customer PII in tests.
- Use deterministic fixtures where possible.
- Use tenant-specific data for tenant isolation tests.
- Clean up created test data.
- Avoid tests that depend on external unstable services.

## Test Data Table

| Data Set | Purpose | Source | Contains PII? | Cleanup |
|---|---|---|---|---|
| TBD | UI workflow | fixture | No | automatic |
