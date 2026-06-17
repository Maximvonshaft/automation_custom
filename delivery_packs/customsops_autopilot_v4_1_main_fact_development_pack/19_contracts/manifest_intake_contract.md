# Manifest Intake Contract

## Input

- `.xlsx` workbook uploaded/dragged by operator.
- P0 sheets: `Combine`, `Separate`.
- P1 sheets: `Simplified`, `Sheet1`.

## Local Agent responsibility

- Accept file path.
- Compute SHA-256.
- Optionally perform non-authoritative shape precheck.
- Submit to Control Plane or pass file to authorized intake path.
- Must not compile ASYCUDA executable steps.

## Control Plane responsibility

- Template classification.
- Header validation.
- Parsing.
- Declaration model creation.
- Country Pack compilation.
- Job signing.

## Output

- manifest_parse_report.json
- declaration_model.json
- signed_job_plan.json
- evidence-ready run context
