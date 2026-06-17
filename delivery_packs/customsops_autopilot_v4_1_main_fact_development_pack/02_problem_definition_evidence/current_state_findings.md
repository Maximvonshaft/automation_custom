# Current State Findings

## Working Baseline

- v3.1.1 proved ASYCUDA SafeBrake field automation in a real environment.
- v4.0 `main` merged the controlled-runtime architecture but executes only through
  `MockActionExecutor`.
- The Control Plane already owns server-side country-pack loading and signed job-plan compilation.
- The Agent already rejects invalid signatures, wrong tenant/machine, expired jobs, wrong modes, and
  forbidden action classes.
- Pack isolation is already covered by tests and must remain a release gate.

## Core Gap

The repository currently has two capabilities that are not yet joined:

```text
v3.1.1 = verified field execution, not controlled-service packaging
v4.0 main = controlled-service architecture, mock execution only
```

v4.1 must unify these through a Windows-only executor adapter, not by copying a portable source ZIP
or moving country-pack logic into the Agent.

## New Product Gap

Operators need a fixed Excel manifest intake workflow. The current code has no manifest classifier,
parser, declaration model, upload API, or drag-and-drop shell. v4.1 must add this workflow with the
Control Plane as the authoritative parser/compiler.

