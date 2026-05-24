# CI Required Checks Policy

Required before merge:

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```

GitHub Actions must be restored and green. Local validation is not sufficient for release approval.
