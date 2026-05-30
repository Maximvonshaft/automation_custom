# Albania ASYCUDA Line Transaction v3.1.1 SafeBrake Coordinate Pack

## Purpose

This server-side pack imports the verified v3.1.1 SafeBrake geometry assets from the uploaded package:

```text
asycuda-blackbox-autopilot-v3.1.1-safebrake-geometry-fix-flat.zip
```

The local operator package must not contain this pack. The Local Agent should only receive signed job plans compiled by the control plane.

## Source of truth

Primary source config:

```text
configs/field_sequence.albania_line_transaction.frontline_business20.v3_1_safebrake.yaml
```

SHA-256:

```text
0dde62c498df27fa0d63c8929f819f4acfddf3563e9b1136e560872c5531f473
```

Supporting source evidence:

```text
ONE_CLICK_FILL20_SAFEBRAKE_STORE_V31.ps1
tools/line_store_after_fill_v311.py
README_V3_1_SAFEBRAKE.md
README_V3_1_1_SAFEBRAKE_GEOMETRY_FIX.md
FINAL_TECHNICAL_STATUS.md
```

## Imported field geometry

The pack contains 20 ordered v3.1 SafeBrake fields. It includes click coordinates, keyboard-only paste steps, skip fields, and field-specific notes.

Important geometry facts:

```text
Line Transaction child Store icon: x=62 y=151
Window activation: SW_MAXIMIZE + SetForegroundWindow
Currency / Monedha: intentionally blank
```

## SafeBrake rule

Invoice currency is intentionally not filled. This is a safety fuse. The expected Store result is a validation error for missing invoice currency, not a successful line save.

Do not reinterpret the blank currency field as missing data.

## Local Agent boundary

This pack is server-side only. Do not copy it into `agent/` or an operator package.

The Local Agent remains signed-job-only. It should execute compiled and signed steps only.

## Compiler

The minimal compiler entrypoint is:

```powershell
python -m control_plane.app.services.albania_line_transaction_compiler --sample --out outputs/albania_v311_plan.json
```

For a SafeBrake Store probe:

```powershell
python -m control_plane.app.services.albania_line_transaction_compiler --sample --include-store-safebrake --out outputs/albania_v311_safebrake_plan.json
```

Signing remains a separate control-plane responsibility.
