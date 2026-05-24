# Release Gate

## Must be true before PR Ready

- Scope matches this pack.
- CI green remotely.
- No Submit/Register/Payment automation.
- No pack content in `agent/`.
- Real customer data absent from fixtures.
- v4.1 PR explicitly states GUI executor integration maturity.
- SafeBrake remains default.
- Non-Windows execution fails closed for real GUI mode.

## Must be true before external deployment

- Compiled Agent artifact inspected.
- Country pack not present in artifact.
- Machine license flow tested.
- Evidence upload tested.
- Kill switch tested.
- Operator SOP approved.
