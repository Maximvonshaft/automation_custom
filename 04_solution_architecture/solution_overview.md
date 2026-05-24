# Solution Overview

## Target architecture

```text
HQ Control Plane
  - owns tenants, machines, licenses, jobs, packs, evidence
  - compiles job plans from server-side Country Packs
  - signs job plans with Ed25519 private key
  - collects evidence bundles
  - revokes tenants/machines/packs

Local Operator Agent
  - contains generic executor only
  - validates job signature with embedded public key
  - validates tenant/machine/expiry/mode
  - executes limited action grammar against ASYCUDA foreground UI
  - generates watermarked evidence
```

## Key architectural principle

The Agent is a dumb executor. The Control Plane is the brain.

## v4.0 runtime modes

- `fillOnly`: fill fields and stop before Store.
- `safeBrakeStore`: fill fields and trigger Store while a mandatory SafeBrake field remains empty, preventing real success.

## Disallowed action classes

- Submit
- Register
- Payment
- Tax finalization
- Credential extraction
- Backend request forgery
- Local country pack export
