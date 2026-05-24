# Current State Findings

## Proven

- ASYCUDA can be driven as a blackbox foreground UI when geometry is locked.
- Coordinate resolver + field-type actions are effective for the verified Line Transaction slice.
- SafeBrake mode can intentionally prevent Store success by leaving Currency empty.
- Review bundles provide usable evidence: screenshots, ledger, run context.

## Not acceptable for external distribution

- Current internal packages include Python source code and PowerShell scripts.
- Field coordinates and country-specific business mappings are visible.
- A local IT vendor could copy the ZIP and reproduce core logic.
- There is no tenant, machine, expiry, or revocation enforcement.

## Required transition

Move from local all-in-one ZIP to controlled runtime:

- server-side pack ownership;
- signed job plans;
- machine-bound execution;
- evidence upload;
- local Agent without complete business rules.
