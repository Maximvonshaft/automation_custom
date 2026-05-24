# CODEX TASK 03 — Signed Job Compiler Extension

Extend Control Plane to compile signed job plans from declaration models.

Requirements:

- Accept declaration model ID or object.
- Load server-side pack.
- Apply pack mapping and SafeBrake policy.
- Compile only allowed actions.
- Sign job plan with existing signing service.
- Preserve tenant, machine, expiry, mode binding.
- Keep `fillOnly` and `safeBrakeStore` as only modes.
