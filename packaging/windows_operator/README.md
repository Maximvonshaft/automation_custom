# CustomsOps Windows Operator Package Skeleton

## Status

This directory is a v4.2 Milestone 2 skeleton only.

It is not an installer, not an external release package, and not approved for operator distribution.

## Purpose

The future Windows Operator Package will provide a controlled local shell for CustomsOps Autopilot execution. It must execute HQ-issued signed job plans only and must not contain server-side country pack logic.

## Included skeleton files

```text
operator_launcher.ps1
package_skeleton.ps1
build_manifest.schema.json
support_diagnostics_manifest.schema.json
```

## Explicit exclusions

The future generated package must not contain:

```text
control_plane/
control_plane/packs/
delivery_packs/
tests/
.git/
lab/
outputs/
*.xlsx
*.pem
*.key
*.p12
*.pfx
*.env
```

## Hard boundaries

- No Submit/Register/Payment/tax-finalizing automation.
- No country pack content in local package.
- No local Excel-to-executable-plan compilation.
- No production credentials.
- No real customer manifests.
- No external distribution from this skeleton.

## Future operator flow

```text
Operator imports Excel
  -> local hash/precheck only
  -> Control Plane parses/compiles signed job
  -> Operator Package receives signed job
  -> Local Agent validates signature/tenant/machine/mode/expiry
  -> ASYCUDA foreground execution under fillOnly/safeBrakeStore
  -> evidence bundle generated and referenced to HQ
```

## Milestone ownership

This skeleton exists to support later implementation of machine binding, signed-job-only operator flow, evidence reference handling, and controlled release packaging.