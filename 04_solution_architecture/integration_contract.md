# Integration Contract

## Local Agent ↔ Control Plane

Transport: HTTPS.

Authentication options for MVP:

- tenant API token for machine registration;
- short-lived machine token after registration;
- signed jobs for execution authorization.

## Offline mode

MVP may support local signed job files, but each job must include:

- expiry
- machine binding
- tenant binding
- mode binding
- pack version
- job ID
- signature

Offline job reuse must be prevented through job ID ledger and local execution lock.
