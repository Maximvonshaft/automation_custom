# CODEX TASK 02 — Declaration Model Builder

Convert parsed manifest rows into neutral declaration models.

Minimum fields:

- source_file_hash
- template_contract_version
- source_sheet
- source_row_number
- awb
- hs_code
- quantity
- gross_weight_kg
- net_weight_kg
- invoice_value
- currency
- origin_country
- recipient_name
- recipient_address
- goods_description
- customs_description

Rules:

- Office code, authorisation reference, truck data, Store coordinates, and SafeBrake policy come from server-side Country Pack / tenant config.
- Declaration model is not executable GUI plan.
