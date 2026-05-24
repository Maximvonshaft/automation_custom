from __future__ import annotations

import pytest

from control_plane.app.services.manifest_intake import parse_manifest
from control_plane.app.services.template_classifier import classify_template


def sanitized_workbook(sheet: str = "Combine") -> dict:
    return {
        sheet: [
            {
                "awb": "SANITIZED-AWB-001",
                "hs_code": "610910",
                "quantity": "2",
                "weight": "4.5",
                "value": "120.00",
                "origin": "AL",
                "description": "sanitized cotton shirts",
            }
        ]
    }


@pytest.mark.parametrize("sheet", ["Sheet1", "Combine", "Simplified", "Separate"])
def test_classifies_supported_manifest_sheets(sheet):
    contract = classify_template(sanitized_workbook(sheet))
    assert contract["template_type"] == sheet
    assert "awb" in contract["required_headers"]


@pytest.mark.parametrize("sheet", ["Combine", "Separate"])
def test_parses_p0_manifest_templates(sheet):
    manifest, report = parse_manifest(sanitized_workbook(sheet))
    assert manifest.template_type == sheet
    assert report == {
        "template_type": sheet,
        "accepted": True,
        "row_count": 1,
        "errors": [],
        "warnings": [],
    }


def test_rejects_missing_required_headers():
    with pytest.raises(ValueError, match="Missing required header"):
        parse_manifest({"Combine": [{"awb": "SANITIZED-AWB-001"}]})

