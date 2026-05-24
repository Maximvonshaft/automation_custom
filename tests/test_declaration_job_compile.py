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
                "hs_code": "610910",
                "quantity": 2,
                "weight": 4.5,
                "value": 120,
                "origin": "AL",
                "description": "sanitized cotton shirts",
            }
        ],
        "source": {"manifest_sha256": "0" * 64, "filename": "sanitized.xlsx"},
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

