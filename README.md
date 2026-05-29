# automation_custom

## Current Status

- `v4.1` is an internal Release Candidate after local quality gates and Windows ASYCUDA Lab Smoke evidence under SafeBrake.
- `v4.2` milestone implementation is complete through the controlled pilot gate.
- Merged v4.2 milestones cover packaging boundaries, Windows operator package skeleton, machine registration/binding, signed-job-only operator flow, Operator UX shell, evidence reference metadata, and controlled pilot gate records.
- External operator package distribution is still not approved.
- Do not distribute this repository as an external operator package.

## Containment Warning

- Local execution remains signed-job-only.
- Runtime modes remain `fillOnly` and `safeBrakeStore`.
- No Submit/Register/Payment/tax-finalizing automation is approved.
- No country pack content may be moved into `agent/`.
- No local Excel-to-executable-plan compilation is allowed.
- No raw screenshot, ledger, evidence bundle, production ASYCUDA credential, broker authorization value, real customer Excel file, or real AWB row may be committed.
- A pilot gate record is not an external rollout approval.

# CustomsOps Autopilot Controlled Runtime

This repository converts the internal ASYCUDA automation work from a copyable local ZIP into a controlled automation architecture with:

- HQ Control Plane
- Local Operator Agent
- server-side Country Packs
- signed one-time Job Plans
- license / machine binding
- SafeBrake execution modes
- evidence bundle collection
- evidence reference metadata
- controlled pilot gate records
- kill switch / revocation

## Why this exists

The automation contains valuable know-how:

- ASYCUDA blackbox field coordinates
- field-type actions
- dropdown resolver logic
- Albania Line Transaction business mapping
- SafeBrake Store validation flow
- review bundle and evidence flow

If shipped as a loose source ZIP, it can be copied, reverse-engineered, or reused by local IT vendors and agents. This repository defines a controlled architecture where HQ owns the rules and the local endpoint only executes signed tasks.

## Current proven baseline

Internal baseline: `v3.1.1 SafeBrake` and `v4.1` internal Release Candidate.

Evidence established in a real ASYCUDA environment:

- Line Transaction core fields can be filled through coordinate resolver + field-type actions.
- Line Store button can be triggered.
- SafeBrake can intentionally block Store success by leaving `Kodi i monedhes se fatures` / Currency empty.
- Review bundles contain screenshots and ledger evidence.
- Windows ASYCUDA Lab Smoke evidence passed for field fill, Store SafeBrake, and evidence bundle.

## v4.2 controlled operator package track

Current target: convert the internal release candidate into a controlled operator package model where operators can run supervised ASYCUDA foreground automation without receiving the source tree, country packs, coordinates, business mapping, or SafeBrake policy internals.

Merged milestones:

1. Packaging boundary audit.
2. Windows operator package skeleton.
3. Machine registration and machine binding contract.
4. Signed-job-only operator flow.
5. Operator UX shell for status, superficial manifest precheck, and signed-job execution.
6. Evidence reference model for hash-only HQ review metadata.
7. Controlled pilot gate for allowlists, checksum review, approval placeholders, and rollback/disable controls.

Remaining approval outside implementation:

1. Separate external rollout approval, if ever needed.

## Operator shell commands

Status:

```text
python -m agent.customsops_agent.operator_cli status --machine-registration <path> --public-key-pem <path>
```

Manifest superficial precheck:

```text
python -m agent.customsops_agent.operator_cli precheck-manifest --manifest <manifest.xlsx>
```

Run signed job:

```text
python -m agent.customsops_agent.operator_cli run-signed-job --signed-job-plan <signed_job_plan.json> --machine-registration <path> --public-key-pem <path> --evidence-root <path>
```

Create reference-only evidence metadata:

```text
python -m agent.customsops_agent.operator_cli reference-evidence --evidence-bundle <evidence_bundle.zip> --output-json <evidence_reference.json>
```

After editable install, the console entrypoint is:

```text
customsops-operator status --machine-registration <path> --public-key-pem <path>
```

## Controlled pilot gate

M7 adds a gate record workflow only:

```text
packaging/windows_operator/pilot_gate_record.ps1
```

The gate record checks candidate manifest/checksum inputs and references operator and machine allowlists. It does not create an installer, approve external rollout, include country packs, or enable local Excel compilation.

## Non-goals

- No Submit/Register automation.
- No tax/payment workflow automation.
- No distribution of source ZIP to agents.
- No local plaintext country pack.
- No local Excel-to-executable-plan compiler.
- No network evidence upload in Milestone 6.
- No raw screenshot content in evidence references.
- No external rollout approval in Milestone 7.
- No credential capture, cookie reading, login bypass, or backend request forgery.
- No production external operator package approval in implementation PRs.

## Quality gate

Required validation command set:

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

## Codex usage

Start with:

```text
17_codex_prompts/CODEX_MASTER_PROMPT.md
```

Then execute milestone prompts in order.
