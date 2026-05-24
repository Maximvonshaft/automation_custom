# ADR-001: Controlled Runtime over Portable ZIP

## Status
Accepted

## Context
The current internal automation package is valuable but copyable. It exposes source code, country-specific field maps, business logic, and execution scripts.

## Decision
Implement CustomsOps Autopilot v4.0 as a controlled runtime:

- Country Packs remain server-side.
- Control Plane compiles signed job plans.
- Local Agent executes only signed plans.
- Evidence is watermarked and collected.

## Consequences

Positive:
- Prevents casual copying.
- Enables license control, billing, revocation, and audit.
- Establishes multi-country scalability.

Negative:
- Requires Control Plane availability or offline lease handling.
- Requires key management and stronger release processes.
