# Threat Model

## Assets

- Server-side country pack, coordinates, dropdown rules, business mappings, SafeBrake policy, and
  error maps.
- Signing private key.
- Signed job plans.
- Manifest files and declaration models.
- Evidence bundles, screenshots, and ledgers.
- Operator Agent artifact.

## Threats

1. Agent package leaks country-pack knowledge.
2. Operator or vendor modifies local code to compile actions from Excel.
3. Unsigned or expired job is executed.
4. Wrong tenant or wrong machine executes a job.
5. GUI executor accidentally triggers Submit/Register/Payment/tax-finalizing workflow.
6. Real customer manifest data is committed as a fixture.
7. Evidence is generated without watermark or hashes.
8. Non-Windows environment attempts real GUI execution.
9. Agent reads credentials, cookies, browser sessions, or ASYCUDA backend APIs.

## Controls

- Preserve current signed-plan validation before execution.
- Keep country-pack loading in Control Plane only.
- Add package-inspection tests for Agent artifacts.
- Keep allowed modes to `fillOnly` and `safeBrakeStore`.
- Keep forbidden action checks in Control Plane compiler and Agent executor path.
- Use sanitized fixtures only.
- Require watermarked evidence bundles with hashes.
- Gate real GUI executor to Windows and fail closed elsewhere.
- Keep ASYCUDA interaction limited to operator-confirmed foreground GUI actions.

## Residual Risk

The first real GUI executor integration must be validated on a controlled Windows lab workstation
before any production release. GitHub Actions can validate boundaries and unit behavior, but cannot
prove real ASYCUDA foreground behavior by itself.

