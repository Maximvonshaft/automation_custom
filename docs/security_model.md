# Security Model

The Control Plane is the policy and knowledge boundary. The Agent is a generic executor.

Controls implemented in v4.0:

- Ed25519 signature verification over canonical job payloads.
- Tenant, machine, expiry, and mode enforcement.
- Explicit forbidden-action rejection for submit, register, payment, tax, credential, and backend flows.
- Evidence bundle watermarking with hashes.
- Country pack files remain outside the Agent tree.
- `MockActionExecutor` is intentional for the Controlled Runtime MVP. The real Windows/ASYCUDA
  foreground GUI executor is out of scope for this PR.
