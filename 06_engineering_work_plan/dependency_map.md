# Dependency Map

Suggested stack for MVP:

## Control Plane

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic v2
- PostgreSQL for production, SQLite for local dev only
- cryptography or pynacl for Ed25519
- pytest
- ruff
- mypy optional but preferred

## Local Agent

- Python 3.11+
- pyautogui / pywin32 / pywinauto as currently required by runtime
- pillow for screenshots
- pydantic for job validation
- cryptography or pynacl for Ed25519 verification
- zipfile/json standard library for evidence bundles
- Nuitka for external executable build

## Do not add

- dependency that uploads screenshots to third-party SaaS by default
- hidden telemetry
- credential capture libraries
- remote desktop control libraries outside explicit scope
