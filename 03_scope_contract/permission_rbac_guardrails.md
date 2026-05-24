# Permission / RBAC Guardrails

Roles:

- `platform_admin`: full control, key rotation, tenant/machine revoke.
- `pack_admin`: edit Country Packs server-side.
- `ops_manager`: compile jobs, review evidence.
- `operator`: run assigned jobs through local Agent only.
- `auditor`: read-only run/evidence access.

Rules:

- Operators cannot access Country Pack definitions.
- Local agents cannot request arbitrary packs or modes.
- `storePass` and `submitArmed` require explicit elevated approval in future versions.
- v4.0 exposes only `fillOnly` and `safeBrakeStore` to operators.
