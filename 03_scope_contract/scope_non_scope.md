# Scope / Non-Scope Contract

## In scope for v4.0

1. Control Plane MVP.
2. Local Agent that executes signed job plans.
3. Server-side Albania ASYCUDA Country Pack storage.
4. Job Plan Compiler for `fillOnly` and `safeBrakeStore` modes.
5. Ed25519 signing and verification.
6. Tenant/machine/expiry/mode checks.
7. Evidence bundle watermarking and upload/local packaging.
8. Kill switch / license revocation.
9. CI quality gates and security checks.
10. Documentation for internal deployment and operator workflow.

## Out of scope for v4.0

1. Submit/Register automation.
2. Payment/tax/duty triggering flows.
3. Credential capture, cookie reading, login automation, or ASYCUDA backend request forgery.
4. Distribution of full Country Packs to local machines.
5. Permanent offline licensing.
6. External customer self-service pack authoring.
7. Multi-country rollout beyond Albania Pack scaffolding.

## Hard prohibition

Do not create a distributable green ZIP containing source code + configs + full pack.
