# Scope / Non-Scope Contract

## In Scope for v4.1

1. Fixed Excel manifest intake contract.
2. Template classifier for `Sheet1`, `Combine`, `Separate`, and `Simplified`.
3. Server-side parser for sanitized `Combine` and `Separate` manifest rows.
4. Declaration model builder with validation and parse-report output.
5. Signed job-plan compilation from declaration model while keeping pack rules server-side.
6. Executor interface that routes only after signed-plan validation succeeds.
7. Windows-only ASYCUDA foreground GUI executor adapter.
8. SafeBrake preservation for `fillOnly` and `safeBrakeStore` only.
9. Evidence bundle compatibility with v3.1.1 screenshot and ledger review workflows.
10. Local operator intake shell that may hash/precheck files but cannot compile executable steps.
11. Packaging checks proving the operator artifact excludes country-pack files and rule content.

## Out of Scope for v4.1

1. Submit/Register/Payment/tax-finalizing automation.
2. Local country-pack distribution.
3. Local Agent compiling executable ASYCUDA steps from Excel.
4. Real customer Excel rows or production manifest data as committed fixtures.
5. Full batch queue production UI.
6. StorePass or non-SafeBrake Store success without explicit later authorization.
7. ASYCUDA credential capture, cookie/session access, login bypass, or backend request forgery.

## Hard Prohibition

Do not turn v4.1 into an external operator package containing source code, country pack, coordinates,
business mappings, dropdown rules, SafeBrake policy, or error maps.

