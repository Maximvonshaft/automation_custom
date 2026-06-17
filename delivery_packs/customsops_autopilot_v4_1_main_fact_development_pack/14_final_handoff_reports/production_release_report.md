# v4.1 Production Release Report Template

## Release Identity

- Release:
- Commit:
- Tag:
- Environment:
- Release owner:
- Windows lab evidence location:

## Scope Confirmation

- v4.1 integrates manifest intake and real Windows GUI executor adapter.
- Runtime modes remain `fillOnly` and `safeBrakeStore`.
- SafeBrake remains the default validation mode.
- Submit/Register/Payment/tax-finalizing automation is not included.
- Country pack content is not present in the Agent package.

## Required Evidence

| Check | Result | Evidence |
|---|---|---|
| Pack validation | pass/fail | CI link |
| Ruff | pass/fail | CI link |
| Pytest | pass/fail | CI link |
| Bandit | pass/fail | CI link |
| Agent package inspection | pass/fail | artifact scan |
| Windows GUI lab smoke | pass/fail | screenshots + ledger |
| SafeBrake preservation | pass/fail | evidence bundle |
| Rollback plan | ready/not ready | release owner |

## Final Status

Successful / Rolled back / Partially released / Monitoring

