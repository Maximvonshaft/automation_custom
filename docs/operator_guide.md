# Operator Guide

The local Agent runs only short-lived, tenant-bound, machine-bound, Ed25519-signed job plans.

Allowed v4.0 modes:

- `fillOnly`: fill fields and stop before Store.
- `safeBrakeStore`: fill fields and invoke Store with the SafeBrake-required blank field intact.

Operators must sign in to ASYCUDA themselves and confirm the foreground ASYCUDA window before any
real executor is enabled. The Agent does not read credentials, cookies, browser history, or sessions.

