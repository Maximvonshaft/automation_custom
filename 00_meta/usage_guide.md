# Usage Guide

## Step 1 — Classify the Change

Use the risk level table:

| Risk | Examples | Required Pack Level |
|---|---|---|
| L1 | copy-only, visual-only, no workflow impact | Lean |
| L2 | UI flow improvement, existing API only | Production |
| L3 | API contract, permission, state machine, data writes | SSS |
| L4 | auth, payment, customer PII, SLA, AI automation, WebCall | SSS + release owner sign-off |
| L5 | irreversible data, compliance, production outage risk | SSS + formal go/no-go + rollback drill |

## Step 2 — Fill the Pack

Do not hand over vague instructions.
Every task must be linked to:
- evidence,
- exact impacted files,
- exact expected behavior,
- acceptance criteria,
- test plan,
- rollback plan.

## Step 3 — Open the PR

The PR must include:
- linked issue,
- summary,
- file-level change list,
- test evidence,
- risk level,
- screenshots where UI is affected,
- rollback plan.

## Step 4 — Gate Before Merge

No merge unless:
- CI passes,
- required reviewers approve,
- acceptance criteria are checked,
- security/privacy checks are completed for applicable scope,
- release plan is clear.

## Step 5 — Verify After Release

After production deployment:
- run smoke tests,
- check logs/metrics,
- verify critical paths,
- watch error rate,
- confirm rollback readiness window.
