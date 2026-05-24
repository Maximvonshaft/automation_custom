from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SUPPORTED_SHEETS = {"Sheet1", "Combine", "Simplified", "Separate"}
REQUIRED_HEADERS = {
    "awb",
    "hs_code",
    "quantity",
    "weight",
    "value",
    "origin",
    "description",
}


@dataclass(frozen=True)
class ManifestTemplate:
    template_type: str
    rows: list[dict[str, Any]]


def classify_workbook(workbook: dict[str, list[dict[str, Any]]]) -> str:
    available = [sheet for sheet in workbook if sheet in SUPPORTED_SHEETS]
    if not available:
        raise ValueError("Unsupported manifest template: no supported sheet found")
    if "Combine" in available:
        return "Combine"
    if "Separate" in available:
        return "Separate"
    if "Simplified" in available:
        return "Simplified"
    return "Sheet1"


def validate_headers(row: dict[str, Any]) -> list[str]:
    normalized = {key.strip().lower() for key in row}
    return sorted(REQUIRED_HEADERS - normalized)


def parse_manifest(
    workbook: dict[str, list[dict[str, Any]]],
) -> tuple[ManifestTemplate, dict[str, Any]]:
    template_type = classify_workbook(workbook)
    rows = workbook.get(template_type, [])
    errors: list[str] = []
    warnings: list[str] = []
    if not rows:
        errors.append(f"{template_type} sheet is empty")
    else:
        missing = validate_headers(rows[0])
        if missing:
            errors.append(f"Missing required header(s): {', '.join(missing)}")
    accepted = not errors
    report = {
        "template_type": template_type,
        "accepted": accepted,
        "row_count": len(rows),
        "errors": errors,
        "warnings": warnings,
    }
    if not accepted:
        raise ValueError(report["errors"][0])
    return ManifestTemplate(template_type=template_type, rows=rows), report
