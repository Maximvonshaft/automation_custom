# Engineer / Codex Execution Prompt

You are implementing CustomsOps Autopilot v4.0 Controlled Runtime.

Read these first:

1. `000_READ_THIS_FIRST_FOR_CODEX.md`
2. `03_scope_contract/scope_non_scope.md`
3. `04_solution_architecture/solution_overview.md`
4. `06_engineering_work_plan/file_level_change_plan.md`
5. `07_quality_testing/acceptance_criteria.md`

Rules:

1. Do not distribute source ZIP or plaintext Country Pack to local agent.
2. Do not implement Submit/Register/Payment automation.
3. Do not store or read ASYCUDA credentials, cookies, or sessions.
4. Implement signed job plan verification before any action execution.
5. Implement mode enforcement and reject forbidden actions.
6. Add tests for negative security cases, not only happy path.
7. Produce a final report with changed files, tests run, risks, and rollback plan.

Output required:

- branch name
- commit SHA
- changed files
- architecture summary
- tests run and results
- security controls implemented
- remaining risks
- rollback plan
