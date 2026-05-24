# Threat Model

## Assets

- Albania ASYCUDA Country Pack
- Field coordinate maps
- Dropdown resolver rules
- Business mapping rules
- SafeBrake policy
- Evidence bundles
- Tenant/machine licenses
- Signing private key

## Adversaries

- Local IT vendor attempting to copy or replicate the tool.
- Agent or broker attempting to run automation without authorization.
- Operator attempting to reuse jobs after expiry.
- Insider leaking Country Pack files.

## Controls

- Server-side pack storage.
- Signed job plans.
- Machine and tenant binding.
- Short expiry.
- Kill switch.
- Agent without complete pack.
- Watermarked evidence.
- No external source ZIP.

## Residual risks

- Compiled Agent can still be reverse-engineered. Mitigation: no full Country Pack in Agent.
- Screenshots may reveal field positions. Mitigation: watermark, contractual controls, limited distribution.
- Offline lease misuse. Mitigation: short expiry and job ID reuse prevention.
