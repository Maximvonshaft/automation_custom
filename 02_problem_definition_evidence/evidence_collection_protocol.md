# Evidence Collection Protocol

Every run must generate and preserve:

- `run_context.json`
- `ledger.jsonl`
- screenshots per step
- before/after screenshots for high-risk actions
- `review_report.html` or equivalent summary
- `evidence_manifest.json`
- signed job plan hash
- agent version
- pack ID/version
- tenant ID
- machine ID
- execution mode

Evidence must be watermarked and either uploaded to the Control Plane or packaged as a review bundle when offline.
