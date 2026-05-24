# SafeBrake Policy

SafeBrake intentionally leaves a configured mandatory field empty so that the customs system blocks Store success through its native validation.

For Albania ASYCUDA current SafeBrake field:

- `Kodi i monedhes se fatures` / Currency / Monedha

Rules:

- SafeBrake must never be silently disabled.
- `storePass` must be a distinct future mode.
- SafeBrake Store result must be captured with before/after screenshots.
- If SafeBrake unexpectedly succeeds, the Agent must flag `UNEXPECTED_STORE_SUCCESS` and halt.
