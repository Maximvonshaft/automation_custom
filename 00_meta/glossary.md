# Glossary

- **Control Plane**: HQ-owned server-side service that manages tenants, machines, packs, jobs, signatures, evidence, and kill switch.
- **Local Agent**: Minimal local executable that controls the ASYCUDA foreground UI according to a signed job plan.
- **Country Pack**: Server-side rules for one customs system/country, including field maps, coordinate maps, dropdown rules, business mapping, SafeBrake policy, and error map.
- **Job Plan**: A short-lived, signed, machine-bound execution plan compiled by the Control Plane.
- **SafeBrake**: A deliberate risk-control mode that fills validated fields and triggers system validation while leaving an agreed mandatory field empty to prevent real Store/Submit success.
- **Evidence Bundle**: ZIP containing screenshots, ledger, run context, watermark metadata, and final report.
- **Watermark**: Tenant/job/machine/pack identifiers included in reports and metadata for traceability.
