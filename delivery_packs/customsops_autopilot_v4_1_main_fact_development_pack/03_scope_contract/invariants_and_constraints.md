# Invariants and Constraints

- `control_plane/packs/**` remains server-side only.
- Agent must validate signed job plans before execution.
- Agent must reject unsupported or forbidden actions.
- `fillOnly` and `safeBrakeStore` are the only supported modes.
- Real GUI executor must fail closed outside Windows unless running mocks in tests.
- Evidence bundle must include file hash, template version, declaration_model hash, job_plan hash, run id, tenant id, machine id, pack version, and mode.
- SafeBrake must remain default for production-environment tests.
