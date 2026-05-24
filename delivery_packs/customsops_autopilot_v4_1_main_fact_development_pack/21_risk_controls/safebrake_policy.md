# SafeBrake Policy

SafeBrake is the default for production-environment validation.

It intentionally prevents final Store/Submit success by leaving a configured required field blank or using another approved blocking mechanism.

Rules:

- SafeBrake must be represented in server-side pack policy.
- Agent must not decide SafeBrake field locally.
- SafeBrake must never be disabled by local operator UI alone.
- StorePass requires explicit later authorization and separate release gate.
