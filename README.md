# automation_custom

## Containment Warning

- v4.0 is a Controlled Runtime MVP.
- Local Agent uses `MockActionExecutor`.
- Real Windows/ASYCUDA foreground GUI executor is not implemented in v4.0.
- `v3.1.1 SafeBrake` remains the verified field runtime baseline.
- Do not distribute this repository as an external operator package.

# CustomsOps Autopilot v4.0 Controlled Runtime - Production Implementation Pack for Codex

This repository implements the v4.0 Controlled Runtime MVP production loop from the Codex
construction pack.

It converts the current internal ASYCUDA automation work from a copyable local ZIP into a controlled
automation service with:

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

If shipped as a ZIP, it can be copied, reverse-engineered, or reused by local IT vendors and agents.
This repository defines a production-grade controlled architecture where HQ owns the rules and the
local endpoint only executes signed tasks.

## Current proven baseline

Internal baseline: `v3.1.1 SafeBrake`.

Evidence established in real ASYCUDA environment:

- Line Transaction core fields can be filled through coordinate resolver + field-type actions.
- Line Store button can be triggered.
- SafeBrake can intentionally block Store success by leaving `Kodi i monedhes se fatures` /
  Currency empty.
- Review bundles contain screenshots and ledger evidence.

## v4.0 MVP scope

v4.0 is not a new ASYCUDA feature sprint. It is a control and commercialization-hardening sprint.
This PR is a Controlled Runtime MVP.

Deliver v4.0 as:

1. a server-side control plane that owns country packs and compiles signed jobs;
2. a local Agent that executes only signed job plans;
3. evidence collection and watermarking;
4. license / tenant / machine / expiry enforcement;
5. default `fillOnly` and `safeBrakeStore` modes only;
6. a Local Agent execution boundary that currently uses `MockActionExecutor`.

The real Windows/ASYCUDA foreground GUI executor is not implemented in this PR. The verified
field-runtime baseline remains `v3.1.1 SafeBrake` until GUI executor integration lands.

## Non-goals

- No Submit/Register automation.
- No tax/payment workflow automation.
- No distribution of source ZIP to agents.
- No local plaintext country pack.
- No credential capture, cookie reading, login bypass, or backend request forgery.
- No real Windows/ASYCUDA foreground GUI executor integration in this PR.

## Quality gate

The required GitHub Actions workflow runs:

```text
python 15_automation_scripts/validate_pack.py
ruff check .
pytest -q
bandit -q -r agent control_plane shared
```

## Codex usage

Start with:

```text
17_codex_prompts/CODEX_MASTER_PROMPT.md
```

Then execute the milestone prompts in order.
