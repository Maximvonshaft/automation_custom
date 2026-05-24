from __future__ import annotations

from hashlib import sha256
from typing import Any
from uuid import uuid4

from control_plane.app.services.manifest_intake import ManifestTemplate


def _required_text(row: dict[str, Any], key: str) -> str:
    value = str(row.get(key, "")).strip()
    if not value:
        raise ValueError(f"Missing value for {key}")
    return value


def _required_number(row: dict[str, Any], key: str) -> float:
    value = row.get(key)
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric value for {key}") from exc
    if parsed < 0:
        raise ValueError(f"Negative numeric value for {key}")
    return parsed


def build_declaration_model(
    manifest: ManifestTemplate, *, manifest_bytes: bytes, filename: str = "manifest.xlsx"
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, row in enumerate(manifest.rows, start=1):
        normalized = {str(key).strip().lower(): value for key, value in row.items()}
        gross_weight = _required_number(normalized, "gross_weight")
        net_weight = normalized.get("net_weight")
        statistical_quantity = normalized.get("statistical_quantity")
        items.append(
            {
                "source_row": index,
                "awb": _required_text(normalized, "awb"),
                "document_reference": _required_text(normalized, "awb"),
                "hs_code": _required_text(normalized, "hs_code"),
                "quantity": _required_number(normalized, "quantity"),
                "statistical_quantity": (
                    _required_number(normalized, "statistical_quantity")
                    if statistical_quantity not in (None, "")
                    else _required_number(normalized, "quantity")
                ),
                "gross_weight": gross_weight,
                "net_weight": (
                    _required_number(normalized, "net_weight")
                    if net_weight not in (None, "")
                    else gross_weight
                ),
                "invoice_value": _required_number(normalized, "invoice_value"),
                "origin": _required_text(normalized, "origin"),
                "description": " ".join(
                    [
                        _required_text(normalized, "description"),
                        f"HS {_required_text(normalized, 'hs_code')}",
                        f"AWB {_required_text(normalized, 'awb')}",
                    ]
                ),
            }
        )
    return {
        "declaration_id": f"decl_{uuid4().hex}",
        "template_type": manifest.template_type,
        "items": items,
        "source": {
            "manifest_sha256": sha256(manifest_bytes).hexdigest(),
            "filename": filename,
        },
    }
