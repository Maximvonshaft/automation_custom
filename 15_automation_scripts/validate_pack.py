#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    '000_READ_THIS_FIRST_FOR_CODEX.md',
    'README.md',
    '17_codex_prompts/CODEX_MASTER_PROMPT.md',
    '03_scope_contract/scope_non_scope.md',
    '03_scope_contract/invariants_and_constraints.md',
    '04_solution_architecture/solution_overview.md',
    '06_engineering_work_plan/execution_brief.md',
    '06_engineering_work_plan/file_level_change_plan.md',
    '07_quality_testing/acceptance_criteria.md',
    '08_security_privacy_compliance/threat_model.md',
    '11_release_change_management/rollback_plan.md',
    '18_schemas/job_plan.schema.json',
    '19_contracts/local_agent_contract.md',
    '21_risk_controls/external_distribution_policy.md',
]
missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print('Missing required files:')
    for p in missing:
        print(' -', p)
    sys.exit(1)
print('CustomsOps v4.0 implementation pack validation passed.')
