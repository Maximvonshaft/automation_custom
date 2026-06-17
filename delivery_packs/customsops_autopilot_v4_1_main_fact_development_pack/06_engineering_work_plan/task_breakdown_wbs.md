# v4.1 Work Breakdown Structure

## Phase 0 - Main Fact Lock

- Confirm base commit `45fd4a9f5f95247432814293bced96badc80cd10`.
- Re-run v4.0 quality gate.
- Confirm `MockActionExecutor` is the only Agent executor in `main`.
- Confirm pack isolation tests pass before v4.1 changes.

## Phase 1 - Manifest Intake Contract

- Define fixed template contract and parse-report schema.
- Add sanitized sample rows only.
- Implement classifier tests before parser implementation.
- Reject unsupported sheets and ambiguous workbook shapes.

## Phase 2 - Declaration Model

- Build neutral declaration model from parsed rows.
- Preserve row lineage and validation errors.
- Keep declaration model free of GUI coordinates and country-pack rules.

## Phase 3 - Server-Side Job Compiler Extension

- Extend `JobCompiler` to accept declaration model input.
- Keep country-pack lookup in Control Plane services.
- Preserve `fillOnly` and `safeBrakeStore`.
- Add regression tests for forbidden actions.

## Phase 4 - Real GUI Executor Adapter

- Introduce executor protocol.
- Add Windows-only GUI adapter behind signed-plan validation.
- Add ASYCUDA foreground window guard.
- Keep `MockActionExecutor` for tests and non-Windows dry runs.

## Phase 5 - Operator Shell and Evidence

- Add drag-and-drop intake shell or CLI equivalent.
- Hash manifest file before upload.
- Preserve v3.1.1 screenshot and ledger review compatibility.
- Ensure evidence bundles remain watermarked and hashed.

## Phase 6 - Packaging and Release Gate

- Build Windows Agent artifact without `control_plane/packs/**`.
- Add artifact inspection tests.
- Require GitHub Actions quality gate and manual Windows lab smoke evidence before release.

