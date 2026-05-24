# Support Playbook

## Common failures

| Failure | Likely cause | Action |
|---|---|---|
| Template rejected | Missing required headers | Return parse report to operator |
| Job rejected | Signature/expiry/machine mismatch | Reissue job from Control Plane |
| GUI executor refuses | Non-Windows or ASYCUDA not foreground | Confirm Windows lab/agent environment |
| SafeBrake not triggered | Currency was filled or Store not reached | Inspect screenshots and ledger |
| Evidence missing | Packaging/upload failure | Collect local outputs and logs |
