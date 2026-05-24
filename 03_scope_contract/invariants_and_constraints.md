# Invariants and Constraints

## Security invariants

- Private signing keys never leave the Control Plane.
- Local Agent must reject unsigned, expired, wrong-machine, wrong-tenant, wrong-mode jobs.
- Local Agent must not contain the complete Country Pack.
- Local Agent must not execute Submit/Register/Payment/Tax actions in v4.0.
- Evidence must include tenant/job/machine/pack watermarks.

## Operational invariants

- ASYCUDA remains operator-authenticated through normal UI login.
- No login bypass or server-side ASYCUDA integration is introduced.
- Local Agent operates only on foreground UI.
- SafeBrake mode remains default for production-environment verification.

## Commercial constraints

- Agents and local IT vendors receive use rights only, not software ownership.
- Country Pack remains HQ IP.
- License can be revoked remotely.
