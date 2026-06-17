# CODEX TASK 00 — Main Fact Audit

Audit current `main` before coding.

Verify:

- `README.md` still states v4.0 Controlled Runtime MVP.
- `MockActionExecutor` still exists and is not silently replaced without tests.
- signed plan validation still gates execution.
- forbidden actions remain forbidden.
- country pack remains under `control_plane/packs` only.

Produce a short `docs/v4.1_fact_audit.md` with findings.
