# Assumptions and Decisions Log

| ID | Type | Decision / Assumption | Rationale | Status |
|---|---|---|---|---|
| D-001 | Decision | v4.1 implements Excel drag-and-drop manifest intake as a first-class product workflow. | User product direction is operator drags fixed Excel template into software. | Accepted |
| D-002 | Decision | Agent may inspect uploaded Excel shape/hash but must not compile executable ASYCUDA job plan locally. | Protect country pack and business logic from agents/local IT. | Accepted |
| D-003 | Decision | Control Plane owns template parsing, declaration model building, pack compilation, signing. | HQ control and anti-copy architecture. | Accepted |
| D-004 | Decision | Real GUI executor is Windows-only and gated behind validated signed job plan. | ASYCUDA blackbox UI is local Windows foreground automation. | Accepted |
| D-005 | Decision | SafeBrake remains default. | Avoid unintended Store/Submit/tax consequences. | Accepted |
| A-001 | Assumption | `235-97877625.xlsx` structure is a representative Albania manifest template. | Uploaded as useful frontline template sample. | To validate with sanitized fixtures |
| A-002 | Assumption | `Combine` and `Separate` are P0 sheets; `Simplified` is P1. | They contain detailed line data needed for declaration model. | Accepted |
