# Test Strategy Pyramid

## Unit tests

- Signature validation
- Schema validation
- Machine fingerprint validation
- Forbidden action enforcement
- Evidence manifest generation
- Watermark insertion

## Integration tests

- Control Plane job compile → sign → Agent validate
- License check → revoked machine rejection
- Evidence upload or local evidence export

## Manual QA

- Run local Agent in mock executor mode.
- Verify no Country Pack exists in Agent artifact.
- Verify review bundle contains watermarks.
- Verify forbidden actions are rejected.

## Field tests

Field ASYCUDA tests remain internal-only and must not be run by external vendors without HQ operator control.
