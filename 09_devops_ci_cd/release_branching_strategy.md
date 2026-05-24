# Release Branching Strategy

## Recommended Branches

- `main`: production-ready code.
- `release/<version>`: stabilization branch if release train is used.
- `feat/<scope>`: feature work.
- `fix/<scope>`: bugfix work.
- `hotfix/<scope>`: urgent production fix.

## Rules

- PR into `main` requires quality gate.
- Hotfix still requires minimal testing and rollback plan.
- Release tags should point to audited commits.
