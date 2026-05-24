## Summary

## Scope boundary

- [ ] No Submit/Register/Payment/tax-finalizing automation
- [ ] Country Pack remains server-side
- [ ] Agent does not compile executable plan from Excel locally
- [ ] SafeBrake remains default where applicable

## Verification

```text
python 15_automation_scripts/validate_pack.py
python -m ruff check .
python -m pytest -q
python -m bandit -q -r agent control_plane shared
```
