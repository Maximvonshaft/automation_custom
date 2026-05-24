# Codex Master Prompt — CustomsOps Autopilot v4.0 Controlled Runtime

You are the final implementation engineer for CustomsOps Autopilot v4.0 Controlled Runtime.

## Objective

Convert the existing internal ASYCUDA blackbox automation package from a distributable local ZIP into a controlled automation service.

## Architecture to implement

1. HQ Control Plane
2. Local Operator Agent
3. Server-side Country Pack
4. Job Plan Compiler
5. Signed Job Plan verification
6. Evidence Bundle Collector
7. License / machine binding / kill switch

## Mandatory constraints

- Do not distribute the full Country Pack to the local Agent.
- Do not include Albania field coordinates or business mapping in the Agent artifact.
- Do not implement Submit/Register/Payment automation in v4.0.
- Do not read ASYCUDA credentials, cookies, sessions, browser history, or passwords.
- Do not bypass ASYCUDA login or use backend request forgery.
- Agent must reject unsigned/expired/wrong-machine/wrong-tenant/wrong-mode jobs.
- Evidence must be watermarked.

## Deliverable

Implement the smallest production-grade v4.0 system that proves controlled execution:

- Control Plane can compile a SafeBrake signed job.
- Agent can validate and execute a signed job in mock mode and real executor-ready mode.
- Evidence bundle is generated with watermark.
- Invalid jobs are rejected.
- Agent artifact does not include complete pack.

## Output required

- Branch name
- Commit SHA
- PR URL
- Changed files
- Test results
- Security review notes
- Known limitations
- Rollback plan
