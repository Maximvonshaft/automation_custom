# Uploaded Excel Template Findings

Observed workbook: `235-97877625.xlsx`.

Sheets:

- `Sheet1`: manifest-level header content, including `FLETEDERGESA E MALLIT`, date, and manifest number.
- `Combine`: A:AA, detailed consolidated declaration rows.
- `Simplified`: A:N, simplified rows.
- `Separate`: A:AA, separate declaration rows.

P0 columns observed in `Combine` / `Separate`:

- `Kodi` / AWB / document reference
- `Sasia` / quantity
- `Pesha` / weight
- `Çmimi/$` / value
- `Origjina prej nga vije` / origin country
- `Pranuesi` / recipient
- `Adresa` / address
- `HsCode`
- `Frequency / Count`
- `Consolidated Value`
- `HS Code / Tariff Code`
- `Total Tax Amount`
- `Total Weight (kg)`
- `Description of Goods`

Rule: do not commit real rows as fixtures. Only sanitized rows may be committed.
