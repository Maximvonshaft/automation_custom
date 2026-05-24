# CustomsOps Autopilot v4.0 Controlled Runtime — Production Implementation Pack for Codex

This is a filled production implementation pack derived from the SSS Ultimate Production Implementation Pack standard.

It converts the current internal ASYCUDA automation work from a copyable local ZIP into a controlled automation service with:

- HQ Control Plane
- Local Operator Agent
- server-side Country Packs
- signed one-time Job Plans
- license / machine binding
- SafeBrake execution modes
- evidence bundle collection
- kill switch / revocation

## Why this exists

The current automation contains valuable know-how:

- ASYCUDA blackbox field coordinates
- field-type actions
- dropdown resolver logic
- Albania Line Transaction business mapping
- SafeBrake Store validation flow
- review bundle and evidence flow

If shipped as a ZIP, it can be copied, reverse-engineered, or reused by local IT vendors and agents. This pack defines a production-grade controlled architecture where HQ owns the rules and the local endpoint only executes signed tasks.

## Current proven baseline

Internal baseline: `v3.1.1 SafeBrake`.

Evidence established in real ASYCUDA environment:

- Line Transaction core fields can be filled through coordinate resolver + field-type actions.
- Line Store button can be triggered.
- SafeBrake can intentionally block Store success by leaving `Kodi i monedhes se fatures` / Currency empty.
- Review bundles contain screenshots and ledger evidence.

## v4.0 scope

v4.0 is not a new ASYCUDA feature sprint. It is a control and commercialization-hardening sprint.

Deliver v4.0 as:

1. a server-side control plane that owns country packs and compiles signed jobs;
2. a local Agent that executes only signed job plans;
3. evidence collection and watermarking;
4. license / tenant / machine / expiry enforcement;
5. default `fillOnly` and `safeBrakeStore` modes only.

## Non-goals

- No Submit/Register automation.
- No tax/payment workflow automation.
- No distribution of source ZIP to agents.
- No local plaintext country pack.
- No credential capture, cookie reading, login bypass, or backend request forgery.

## Codex usage

Start with:

```text
17_codex_prompts/CODEX_MASTER_PROMPT.md
```

Then execute the milestone prompts in order.
