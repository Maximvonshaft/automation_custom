# Assumptions and Decisions Log

## Decisions

1. Do not distribute the current Python/PowerShell ZIP externally.
2. Keep Albania ASYCUDA Country Pack server-side.
3. Local Agent executes only signed job plans.
4. Use Ed25519 signatures. Private key stays server-side; public key is embedded in the Agent.
5. Machine binding, tenant binding, expiry, and allowed execution mode are mandatory checks.
6. Default allowed modes for v4.0 are `fillOnly` and `safeBrakeStore`.
7. `storePass`, `submitArmed`, Register, Submit, Payment, or Tax-triggering flows are explicitly out of scope.
8. SafeBrake is a commercial safety feature, not a workaround.

## Assumptions

- ASYCUDA remains a blackbox desktop UI.
- Local execution is required because ASYCUDA runs on the operator workstation.
- Field maps and coordinates are high-value IP and must not be exposed to agents or local IT vendors.
- Network may be intermittent, so short offline leases are allowed, but permanent offline operation is forbidden.
