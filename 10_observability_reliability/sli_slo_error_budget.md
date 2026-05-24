# SLI / SLO / Error Budget

## MVP SLOs

- Job compile API availability: 99.0% during business hours.
- Evidence upload success: 99.0% for online mode.
- Agent signed-plan rejection correctness: 100% for invalid signatures in tests.
- Forbidden action rejection: 100% in tests.

## Error budget policy

Any regression that permits unsigned or forbidden-action execution consumes full security error budget and blocks release.
