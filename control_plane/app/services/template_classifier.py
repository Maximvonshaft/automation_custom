from __future__ import annotations

from typing import Any

from control_plane.app.services.manifest_intake import classify_workbook


def classify_template(workbook: dict[str, list[dict[str, Any]]]) -> dict[str, object]:
    template_type = classify_workbook(workbook)
    return {
        "template_type": template_type,
        "sheets": list(workbook.keys()),
        "required_headers": [
            "awb",
            "hs_code",
            "quantity",
            "weight",
            "value",
            "origin",
            "description",
        ],
    }

