# Test Commands

Codex should adapt commands to the actual repository. Baseline commands:

```bash
python -m pytest -q
python -m ruff check .
python -m compileall .
python 15_automation_scripts/validate_pack.py
```

Required targeted tests:

```bash
python -m pytest tests/test_job_plan_signature.py -q
python -m pytest tests/test_forbidden_actions.py -q
python -m pytest tests/test_evidence_watermark.py -q
python -m pytest tests/test_pack_not_in_agent.py -q
```
