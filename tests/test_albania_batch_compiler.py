from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook

from agent.customsops_agent.forbidden_actions import FORBIDDEN_ACTIONS
from control_plane.app.services.albania_batch_compiler import (
    BatchCompileOptions,
    compile_broker_excel_batch,
)
from control_plane.app.services.albania_excel_template_parser import TemplateDefaults
from tests.test_albania_excel_template_parser import HEADERS_ROW_1, HEADERS_ROW_2


def _make_template(path: Path) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Combine合并订单"
    sheet.append(HEADERS_ROW_1)
    sheet.append(HEADERS_ROW_2)
    sheet.append([
        1,
        "Speaker Gauge*1",
        "AL0001",
        1,
        0.2,
        10,
        "CN",
        "Speedaf",
        "Recipient A",
        "Tirana",
        "",
        "851890*1",
        "CARTON1",
        1,
        10,
        8,
        800,
        0,
        "85189000",
        0,
        0,
        0,
        0,
        "",
        0.2,
        "Speaker Gauge*1",
        "Speaker Gauge 1PC",
    ])
    workbook.save(path)


def test_compile_broker_excel_batch_writes_manifest_and_plans(tmp_path: Path):
    workbook_path = tmp_path / "broker_template.xlsx"
    _make_template(workbook_path)
    output_dir = tmp_path / "compiled"

    compiled = compile_broker_excel_batch(
        workbook_path,
        output_dir,
        options=BatchCompileOptions(
            tenant_id="tenant_demo",
            machine_id="machine_demo",
            include_store_safebrake=True,
            defaults=TemplateDefaults(
                authorization_reference="AUTH-1",
                truck_registration_plate_number="TRUCK-1",
            ),
        ),
    )

    assert compiled.group_count == 1
    assert compiled.manifest_path.exists()
    assert len(compiled.plan_paths) == 1
    plan = json.loads(compiled.plan_paths[0].read_text(encoding="utf-8"))
    manifest = json.loads(compiled.manifest_path.read_text(encoding="utf-8"))

    assert plan["mode"] == "safeBrakeStore"
    assert plan["steps"][-1]["action"] == "store_line_safebrake"
    assert plan["steps"][-1]["x"] == 62
    assert plan["steps"][-1]["y"] == 151
    assert not ({step["action"] for step in plan["steps"]} & FORBIDDEN_ACTIONS)
    assert manifest["group_count"] == 1
    assert manifest["entries"][0]["currency_intentionally_blank"] is True
    assert manifest["entries"][0]["document_references"] == ["AL0001"]


def test_compile_broker_excel_batch_requires_runtime_defaults(tmp_path: Path):
    workbook_path = tmp_path / "broker_template.xlsx"
    _make_template(workbook_path)

    try:
        compile_broker_excel_batch(
            workbook_path,
            tmp_path / "compiled",
            options=BatchCompileOptions(tenant_id="tenant_demo", machine_id="machine_demo"),
        )
    except ValueError as exc:
        assert "authorization_reference" in str(exc)
    else:
        raise AssertionError("Batch compiler accepted missing runtime defaults")
