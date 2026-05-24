# SBOM and Supply Chain Security

## Required When

- Adding dependencies.
- Updating dependency versions.
- Changing build pipeline.
- Adding third-party SDK.

## Checklist

- [ ] Dependency purpose documented.
- [ ] License acceptable.
- [ ] Maintenance status checked.
- [ ] Known vulnerabilities checked.
- [ ] Lockfile updated intentionally.
- [ ] No install scripts with unreviewed risk.
- [ ] SBOM generated where supported.

## Suggested Commands

```bash
npm audit --omit=dev
pip-audit
```

Use project-specific tooling where available.
