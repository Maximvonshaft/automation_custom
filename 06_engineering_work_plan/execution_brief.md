# Execution Brief

## Task
Build CustomsOps Autopilot v4.0 Controlled Runtime.

## Goal
Replace copyable internal ZIP distribution with controlled local Agent + HQ Control Plane + signed job plan architecture.

## Current baseline
Internal v3.1.1 SafeBrake can fill ASYCUDA Line Transaction slice and trigger SafeBrake Store validation. Treat v3.1.1 as internal-only source of behavior, not external distribution format.

## Required deliverables

1. Control Plane MVP.
2. Local Agent signed-plan executor.
3. Server-side Albania Pack placeholder/migration path.
4. Job Plan schema and signer/verifier.
5. Evidence bundle watermarking.
6. License/machine/tenant checks.
7. Kill switch.
8. Tests and release docs.

## Non-negotiables

- No full pack on local agent.
- No unsigned job execution.
- No Submit/Register/Payment actions.
- No source ZIP for external distribution.
