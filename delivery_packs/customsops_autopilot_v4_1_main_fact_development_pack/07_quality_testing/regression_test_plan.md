# Regression Test Plan

Run after every PR:

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

Additional Windows lab tests are required before packaging a real Agent:

- ASYCUDA foreground window guard.
- SafeBrake fill-only execution.
- SafeBrake Store blocked by expected missing currency field.
- Evidence bundle screenshot/ledger parity with v3.1.1.
