# Local Agent Contract

The Agent must:

- execute only signed job plans;
- verify Ed25519 signature before execution;
- reject forbidden actions;
- generate evidence bundle;
- include watermarks;
- avoid storing complete Country Pack;
- avoid reading credentials/cookies/session data;
- support mock executor mode for CI.

The Agent must not:

- generate its own business steps;
- infer country pack logic independently;
- expose pack configs;
- implement Submit/Register in v4.0.
