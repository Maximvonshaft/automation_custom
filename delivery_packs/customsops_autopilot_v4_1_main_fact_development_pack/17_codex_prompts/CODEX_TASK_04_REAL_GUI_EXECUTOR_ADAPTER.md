# CODEX TASK 04 — Real GUI Executor Adapter

Introduce a Windows-only real GUI executor adapter behind signed-plan validation.

Required interface:

- execute_click
- execute_paste
- execute_hotkey
- execute_screenshot
- execute_store_line_safebrake

Rules:

- Non-Windows real execution fails closed.
- Mock tests are acceptable in CI.
- v3.1.1 SafeBrake field-runtime behavior is the functional reference.
- Do not add Submit/Register/Payment actions.
- Do not let executor know full country pack semantics beyond signed step instructions.
