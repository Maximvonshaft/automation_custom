from __future__ import annotations

from pathlib import Path

from control_plane.app.services.declaration_job_compiler import DeclarationJobCompiler
from control_plane.app.services.pack_loader import CountryPackLoader


def test_compiles_declaration_model_to_server_side_signed_plan_payload():
    pack = CountryPackLoader(Path("control_plane/packs")).load_pack("albania_asycuda")
    declaration_model = {
        "declaration_id": "decl_test",
        "template_type": "Combine",
        "items": [
            {
                "source_row": 1,
                "awb": "SANITIZED-AWB-001",
                "document_reference": "SANITIZED-AWB-001",
                "hs_code": "610910",
                "quantity": 2,
                "statistical_quantity": 2,
                "gross_weight": 4.5,
                "net_weight": 4.0,
                "invoice_value": 120,
                "origin": "AL",
                "description": "sanitized cotton shirts",
            }
        ],
        "source": {"manifest_sha256": "0" * 64, "filename": "sanitized.xlsx"},
        "server_defaults": {"currency_code": "EUR"},
    }
    plan = DeclarationJobCompiler().compile_declaration_job(
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        pack=pack,
        mode="safeBrakeStore",
        declaration_model=declaration_model,
    )
    assert plan["tenant_id"] == "tenant_demo"
    assert plan["machine_id"] == "machine_demo"
    assert plan["mode"] == "safeBrakeStore"
    assert plan["steps"][-1]["action"] == "store_line_safebrake"
    field_keys = [step.get("field_key") for step in plan["steps"]]
    assert "document_reference" in field_keys
    assert "hs_code" in field_keys
    assert "quantity" in field_keys
    assert "statistical_quantity" in field_keys
    assert "gross_weight" in field_keys
    assert "net_weight" in field_keys
    assert "invoice_value" in field_keys
    assert "origin" in field_keys
    assert "description" in field_keys
    assert "currency_code" not in field_keys


def test_declaration_job_action_sequence_is_v311_safebrake_compatible():
    pack = CountryPackLoader(Path("control_plane/packs")).load_pack("albania_asycuda")
    declaration_model = {
        "declaration_id": "decl_test",
        "template_type": "Combine",
        "items": [
            {
                "source_row": 1,
                "awb": "SANITIZED-AWB-001",
                "document_reference": "SANITIZED-AWB-001",
                "hs_code": "610910",
                "quantity": 2,
                "statistical_quantity": 2,
                "gross_weight": 4.5,
                "net_weight": 4.0,
                "invoice_value": 120,
                "origin": "AL",
                "description": "sanitized cotton shirts",
            }
        ],
        "source": {"manifest_sha256": "0" * 64, "filename": "sanitized.xlsx"},
        "server_defaults": {"currency_code": "EUR"},
    }
    plan = DeclarationJobCompiler().compile_declaration_job(
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        pack=pack,
        mode="safeBrakeStore",
        declaration_model=declaration_model,
    )
    assert [step["step"] for step in plan["steps"]] == list(range(1, len(plan["steps"]) + 1))
    assert plan["steps"][0]["field_key"] == "office_code"
    assert plan["steps"][1]["field_key"] == "authorisation_reference"
    assert plan["steps"][-1]["action"] == "store_line_safebrake"


def test_fill_only_includes_server_side_currency_when_configured():
    pack = CountryPackLoader(Path("control_plane/packs")).load_pack("albania_asycuda")
    declaration_model = {
        "declaration_id": "decl_test",
        "template_type": "Combine",
        "items": [
            {
                "source_row": 1,
                "awb": "SANITIZED-AWB-001",
                "document_reference": "SANITIZED-AWB-001",
                "hs_code": "610910",
                "quantity": 2,
                "statistical_quantity": 2,
                "gross_weight": 4.5,
                "net_weight": 4.0,
                "invoice_value": 120,
                "origin": "AL",
                "description": "sanitized cotton shirts",
            }
        ],
        "source": {"manifest_sha256": "0" * 64, "filename": "sanitized.xlsx"},
        "server_defaults": {"currency_code": "EUR"},
    }
    plan = DeclarationJobCompiler().compile_declaration_job(
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        pack=pack,
        mode="fillOnly",
        declaration_model=declaration_model,
    )
    assert "currency_code" in [step.get("field_key") for step in plan["steps"]]
