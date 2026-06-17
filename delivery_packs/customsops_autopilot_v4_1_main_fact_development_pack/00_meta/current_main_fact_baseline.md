# Current `main` Fact Baseline

## Baseline

- Repository: `Maximvonshaft/automation_custom`
- Main commit: `45fd4a9f5f95247432814293bced96badc80cd10`
- Tag created for the merged MVP: `v4.0-controlled-runtime-mvp`

## Confirmed Code Facts

1. `README.md` states v4.0 is a Controlled Runtime MVP and that the real Windows/ASYCUDA
   foreground GUI executor is not implemented in v4.0.
2. `agent/customsops_agent/action_executor.py` contains only `MockActionExecutor`, which validates
   allowed action names and records mocked ledger entries.
3. `agent/customsops_agent/signed_plan.py` validates Ed25519 signature, tenant, machine, mode,
   expiry, and action allowlist before returning a plan.
4. `agent/customsops_agent/main.py` runs signed plans through `MockActionExecutor` and then creates
   an evidence bundle.
5. `agent/customsops_agent/forbidden_actions.py` forbids Submit, Register, Payment,
   `tax_finalize`, credential reads, and backend request actions.
6. `control_plane/app/services/job_compiler.py` compiles server-side pack fields and values into
   short-lived job plans and appends `store_line_safebrake` in `safeBrakeStore` mode.
7. `control_plane/app/services/pack_loader.py` loads country-pack files from
   `control_plane/packs/**`; the Agent does not load pack files.
8. `tests/test_pack_not_in_agent.py` fails if `agent/` contains `packs/`, pack-rule YAML/JSON
   filenames, Albania ASYCUDA pack markers, or obvious country-pack content.
9. `tests/test_v4_mvp_boundary.py` documents that `MockActionExecutor` is intentional for v4.0 and
   that real GUI execution is not present.
10. Existing CI runs pack validation, Ruff, Pytest, and Bandit.

## Development Implication

v4.1 must add two capabilities without weakening the v4.0 control boundary:

- server-side manifest intake, parsing, and declaration model building;
- Windows-only GUI executor adapter behind existing signed-plan validation.

The Agent may precheck/hash a dragged file, but executable ASYCUDA step compilation remains
server-side.

