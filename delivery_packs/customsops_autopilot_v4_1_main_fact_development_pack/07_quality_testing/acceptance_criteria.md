# Acceptance Criteria

## Manifest Intake

- Fixed Excel template is classified as `Sheet1`, `Combine`, `Separate`, or `Simplified`.
- Unsupported workbook shapes fail with a structured parse report.
- Parser tests use sanitized fixtures only.
- Local Agent may hash and precheck a file but cannot compile executable ASYCUDA actions.

## Declaration Model

- Declaration model preserves source row lineage and validation errors.
- Declaration model contains no GUI coordinates, country-pack rules, dropdown rules, or SafeBrake
  policy internals.
- Control Plane can compile signed jobs from declaration models.

## GUI Executor

- Real GUI executor path is Windows-only.
- Non-Windows real GUI execution fails closed.
- GUI adapter is invoked only after signed-plan validation succeeds.
- ASYCUDA foreground window must be operator-confirmed before GUI actions run.
- Submit/Register/Payment/tax-finalizing actions remain forbidden.

## SafeBrake and Evidence

- `fillOnly` and `safeBrakeStore` remain the only modes.
- SafeBrake default behavior is preserved.
- Evidence bundles include watermarked screenshots, ledger, hashes, and manifest metadata.
- Evidence remains review-compatible with v3.1.1 screenshot/ledger expectations.

## Packaging

- Agent package contains no `packs/` directory.
- Agent package contains no `field_map`, `coordinate_map`, `business_mapping`, `dropdown_rules`,
  `safebrake_policy`, or `error_map` YAML/JSON files.
- Agent package contains no Albania ASYCUDA country-pack content or obvious rule names.

