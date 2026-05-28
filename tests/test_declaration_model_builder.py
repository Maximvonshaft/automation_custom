from __future__ import annotations

from control_plane.app.services.declaration_model_builder import build_declaration_model
from control_plane.app.services.manifest_intake import parse_manifest


def test_builds_declaration_model_with_lineage_and_hash():
    manifest, _report = parse_manifest(
        {
            "Combine": [
                {
                    "awb": "SANITIZED-AWB-001",
                    "hs_code": "610910",
                    "quantity": "2",
                    "statistical_quantity": "2",
                    "gross_weight": "4.5",
                    "net_weight": "4.0",
                    "invoice_value": "120.00",
                    "origin": "AL",
                    "description": "sanitized cotton shirts",
                }
            ]
        }
    )
    model = build_declaration_model(
        manifest, manifest_bytes=b"sanitized fixture", filename="sanitized.xlsx"
    )
    assert model["declaration_id"].startswith("decl_")
    assert model["template_type"] == "Combine"
    assert model["items"][0]["source_row"] == 1
    assert model["items"][0]["awb"] == "SANITIZED-AWB-001"
    assert model["items"][0]["document_reference"] == "SANITIZED-AWB-001"
    assert model["items"][0]["hs_code"] == "610910"
    assert model["items"][0]["quantity"] == 2
    assert model["items"][0]["statistical_quantity"] == 2
    assert model["items"][0]["gross_weight"] == 4.5
    assert model["items"][0]["net_weight"] == 4.0
    assert model["items"][0]["invoice_value"] == 120
    assert model["items"][0]["origin"] == "AL"
    assert "sanitized cotton shirts" in model["items"][0]["description"]
    assert model["source"]["manifest_sha256"]


def test_declaration_model_contains_no_gui_coordinates_or_pack_rules():
    manifest, _report = parse_manifest(
        {
            "Separate": [
                {
                    "awb": "SANITIZED-AWB-002",
                    "hs_code": "420221",
                    "quantity": 1,
                    "gross_weight": 0.8,
                    "invoice_value": 80,
                    "origin": "AL",
                    "description": "sanitized bag",
                }
            ]
        }
    )
    model = build_declaration_model(manifest, manifest_bytes=b"sanitized fixture")
    model_text = str(model).lower()
    assert "coordinate" not in model_text
    assert "dropdown" not in model_text
    assert "safebrake_policy" not in model_text


def test_builds_declaration_model_from_non_merge_frontline_shape():
    manifest, _report = parse_manifest(
        {
            "Separate": [
                {
                    "description": "sanitized product description",
                    "awb": "SANITIZED-KODI-003",
                    "quantity": 3,
                    "gross_weight": 1.25,
                    "invoice_value": 90.5,
                    "origin": "CN",
                    "hs_code": "61091000",
                    "statistical_quantity": 3,
                }
            ]
        }
    )

    model = build_declaration_model(
        manifest,
        manifest_bytes=b"sanitized non-merge fixture",
        filename="sanitized_non_merge_sheet3.xlsx",
    )

    item = model["items"][0]
    assert item["document_reference"] == "SANITIZED-KODI-003"
    assert item["hs_code"] == "61091000"
    assert item["quantity"] == 3
    assert item["statistical_quantity"] == 3
    assert item["gross_weight"] == 1.25
    assert item["net_weight"] == 1.25
    assert item["invoice_value"] == 90.5
    assert item["origin"] == "CN"
    assert "sanitized product description" in item["description"]
