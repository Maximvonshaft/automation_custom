from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook

from control_plane.app.services.albania_excel_template_parser import (
    TemplateDefaults,
    parse_broker_excel_template,
)

HEADERS_ROW_1 = [
    "Nr.r.",
    "Malli/  Produkti",
    "Kodi",
    "Sasia",
    "Pesha",
    "Çmimi/$",
    "Origjina prej nga vije ",
    "Derguesi/ shitësi ",
    "Pranuesi",
    "Adresa",
    "Verejtje",
    "HsCode",
    "Carton number",
    "出现次数",
    "合并货值",
    "欧元货值",
    "Value (ALL)",
    "关税税率",
    "税率HS code",
    "关税",
    "增值税",
    "总税额（美元）",
    "总税额",
    "提示",
    "总重量(kg)",
    "货物描述",
    "报关货描",
]
HEADERS_ROW_2 = [
    "Nr.r.",
    "Malli/  Produkti",
    "Kodi",
    "Sasia",
    "Pesha",
    "Çmimi/$",
    "Origjina prej nga vije ",
    "Derguesi/ shitësi ",
    "Pranuesi",
    "Adresa",
    "Verejtje",
    "HsCode",
    "Carton number",
    "Frequency / Count",
    "Consolidated Value",
    "Value (EUR)",
    "Value (ALL)",
    "Duty Rate",
    "HS Code / Tariff Code",
    "Customs Duty",
    "VAT",
    "Total Tax (USD)",
    "Total Tax Amount",
    "Remarks / Notes",
    "Total Weight (kg)",
    "Description of Goods",
    "Description of Goods",
]


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
        2,
        30,
        25,
        2500,
        0,
        "85189000",
        0,
        0,
        0,
        0,
        "",
        0.55,
        "Speaker Gauge*1",
        "Speaker Gauge 3PC",
    ])
    sheet.append([
        2,
        "Speaker Gauge*2",
        "AL0002",
        2,
        0.35,
        20,
        "CN",
        "Speedaf",
        "",
        "Tirana",
        "",
        "851890*2",
        "CARTON1",
    ])
    sheet.append([
        3,
        "Water Timer*1",
        "AL0003",
        1,
        0.3,
        15,
        "CN",
        "Speedaf",
        "Recipient B",
        "Durres",
        "",
        "903289*1",
        "CARTON2",
        1,
        15,
        13,
        1300,
        0,
        "90328900",
        0,
        0,
        0,
        0,
        "",
        0.3,
        "Water Timer*1",
        "Water Timer 1PC",
    ])
    workbook.save(path)


def test_parse_broker_excel_template_detects_consolidated_groups(tmp_path: Path):
    workbook_path = tmp_path / "broker_template.xlsx"
    _make_template(workbook_path)

    result = parse_broker_excel_template(
        workbook_path,
        defaults=TemplateDefaults(
            authorization_reference="AUTH-1",
            truck_registration_plate_number="TRUCK-1",
        ),
    )

    assert result.group_count == 2
    first = result.groups[0]
    assert first.start_row == 3
    assert first.end_row == 4
    assert first.item_count == 2
    assert first.document_reference == "AL0001"
    assert first.document_references == ("AL0001", "AL0002")
    assert first.customs_tariff_1 == "85189000"
    assert first.statistical_quantity == "3"
    assert first.total_weight == "0.55"
    assert first.invoice_value == "30"
    assert first.declaration["goods_description"] == "Speaker Gauge 3PC"
    assert first.declaration["currency"] == ""
    assert first.declaration["authorization_reference"] == "AUTH-1"
    assert first.declaration["truck_registration_plate_number"] == "TRUCK-1"


def test_parse_broker_excel_template_warns_when_required_defaults_missing(tmp_path: Path):
    workbook_path = tmp_path / "broker_template.xlsx"
    _make_template(workbook_path)

    result = parse_broker_excel_template(workbook_path)

    assert any("authorization_reference" in warning for warning in result.groups[0].warnings)
    assert any(
        "truck_registration_plate_number" in warning
        for warning in result.groups[0].warnings
    )
