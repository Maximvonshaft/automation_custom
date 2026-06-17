# Data Contract Guardrails

## Excel intake contract

- Accepted file type: `.xlsx`.
- Required P0 sheets: at least one of `Combine` or `Separate`.
- Supported P0 parsing: `Combine`, `Separate`.
- P1 parsing: `Simplified`.
- Real customer rows must not be committed.

## Declaration model contract

The parser emits neutral `declaration_model.json`, not executable GUI actions.

Minimum fields:

- `source_file_hash`
- `template_contract_version`
- `source_sheet`
- `source_row_number`
- `awb`
- `hs_code`
- `quantity`
- `gross_weight_kg`
- `net_weight_kg`
- `invoice_value`
- `currency`
- `origin_country`
- `recipient_name`
- `recipient_address`
- `goods_description`
- `customs_description`

Tenant/country constants such as office code, truck data, and authorization reference are not taken from Excel unless policy explicitly allows.
