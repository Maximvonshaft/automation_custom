# Solution Overview

## Target Architecture

```text
Operator Windows Workstation
  drag fixed xlsx manifest
  |
  v
Local Agent Intake Shell
  hash + file-shape precheck only
  no executable ASYCUDA compilation
  |
  v
HQ Control Plane Manifest Intake
  classify + parse + validate template
  |
  v
Declaration Model Builder
  neutral import/declaration model
  no GUI coordinates in response
  |
  v
Country Pack Compiler
  server-side country pack + declaration model -> action steps
  |
  v
Signed Job Plan
  Ed25519 signature
  tenant/machine/mode/expiry bound
  |
  v
Local Windows Agent
  validate signed plan
  enforce window guard
  execute allowed foreground GUI actions
  |
  v
Evidence Bundle
  v3.1.1-compatible screenshots + ledger
  watermark + hashes + manifest
```

## Key Design Decisions

1. The Agent may accept a dragged Excel file for upload/precheck, but must not own the full
   template-to-ASYCUDA mapping.
2. The Control Plane remains the authoritative parser and executable job compiler.
3. The real GUI executor is an adapter behind `validate_signed_plan`; it must not bypass existing
   signature, tenant, machine, expiry, mode, and forbidden-action checks.
4. `MockActionExecutor` remains available for non-Windows tests and dry-run validation.
5. SafeBrake behavior is preserved as the production validation default.

## Failure Stance

The v4.1 Agent fails closed when:

- platform is not Windows and real GUI mode is requested;
- ASYCUDA foreground window is not operator-confirmed;
- signed job validation fails;
- job contains Submit/Register/Payment/tax-finalizing actions;
- evidence capture or ledger write cannot be completed.

