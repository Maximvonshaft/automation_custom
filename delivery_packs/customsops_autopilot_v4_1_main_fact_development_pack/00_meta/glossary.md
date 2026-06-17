# Glossary

- **Agent**: Local Windows runtime that executes signed job plans but does not own country pack rules.
- **Control Plane**: HQ server-side service that owns tenants, machines, country packs, manifest parsing, signed job compilation, evidence collection, and revocation.
- **Country Pack**: Server-side rules containing field maps, coordinates, dropdown rules, SafeBrake policy, and error mapping.
- **Declaration Model**: Neutral JSON output from manifest parsing before GUI execution steps are compiled.
- **SafeBrake**: Safety mode that intentionally leaves a configured required field blank so Store/Submit cannot finalize.
- **Signed Job Plan**: Short-lived tenant-bound, machine-bound, mode-bound executable plan signed by HQ.
