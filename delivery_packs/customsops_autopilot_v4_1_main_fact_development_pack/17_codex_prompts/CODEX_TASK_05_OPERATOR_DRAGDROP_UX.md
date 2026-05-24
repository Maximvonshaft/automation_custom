# CODEX TASK 05 — Operator Drag-and-Drop UX

Implement the operator intake shell.

Minimum acceptable v4.1 UX:

```text
customsops_agent intake --file manifest.xlsx
customsops_agent run --job signed_job_plan.json
```

If desktop GUI is feasible, scaffold drag-and-drop window, but CLI is acceptable for v4.1.

UX must show:

- file name
- SHA-256
- template classification result
- number of parsed rows
- selected mode
- evidence bundle path

Do not expose coordinates, pack rules, or business mapping.
