from __future__ import annotations

from pathlib import Path

from control_plane.app.services.job_compiler import JobCompiler
from control_plane.app.services.pack_loader import CountryPackLoader


def test_control_plane_compiles_safebrake_job_without_shipping_pack_to_agent():
    pack = CountryPackLoader(Path("control_plane/packs")).load_pack("albania_asycuda")
    plan = JobCompiler().compile_job(
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        pack=pack,
        mode="safeBrakeStore",
        values={"invoice_number": "INV-100"},
    )
    assert plan["mode"] == "safeBrakeStore"
    assert plan["steps"][-1]["action"] == "store_line_safebrake"
    assert plan["pack_id"] == "albania_asycuda"

