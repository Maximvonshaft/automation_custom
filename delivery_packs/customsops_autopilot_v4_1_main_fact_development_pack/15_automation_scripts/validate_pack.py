from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "000_READ_THIS_FIRST_FOR_CODEX.md",
    "README.md",
    "00_meta/current_main_fact_baseline.md",
    "02_problem_definition_evidence/template_excel_findings.md",
    "03_scope_contract/scope_non_scope.md",
    "04_solution_architecture/solution_overview.md",
    "06_engineering_work_plan/file_level_change_plan.md",
    "07_quality_testing/acceptance_criteria.md",
    "08_security_privacy_compliance/threat_model.md",
    "17_codex_prompts/CODEX_MASTER_PROMPT.md",
    "17_codex_prompts/CODEX_TASK_01_MANIFEST_TEMPLATE_INTAKE.md",
    "18_schemas/declaration_model.schema.json",
    "18_schemas/manifest_template_contract.schema.json",
    "19_contracts/manifest_intake_contract.md",
]

FORBIDDEN_PHRASES = [
    "implement submit automation",
    "implement register automation",
    "ship country pack to agent",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        raise SystemExit(f"Missing required file(s): {missing}")
    text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore").lower()
        for p in root.rglob("*.md")
    )
    hits = [phrase for phrase in FORBIDDEN_PHRASES if phrase in text]
    if hits:
        raise SystemExit(f"Forbidden phrase(s) found: {hits}")
    print("CustomsOps v4.1 development pack validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
