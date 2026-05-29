from __future__ import annotations

import json
from pathlib import Path

import yaml

from agent.customsops_agent.forbidden_actions import FORBIDDEN_ACTIONS
from control_plane.app.services.albania_line_transaction_compiler import (
    build_unsigned_job_plan,
    compile_steps_from_declaration,
    load_coordinate_pack,
    load_sample_values,
)

PACK_DIR = (
    Path(__file__).resolve().parents[1]
    / "control_plane"
    / "packs"
    / "asycuda_albania_line_transaction"
    / "v3_1_safebrake"
)


def test_v311_coordinate_pack_contains_expected_fields_and_safebrake():
    pack = load_coordinate_pack(PACK_DIR)
    field_map = pack["field_map"]
    fields = field_map["fields"]

    assert field_map["pack_id"] == "asycuda_albania_line_transaction"
    assert field_map["pack_version"] == "v3.1.1-safebrake-geometry-fix"
    assert len(fields) == 20
    assert fields[0]["field_key"] == "f01_zyrat_doganore_code"
    assert fields[0]["x"] == 90
    assert fields[0]["y"] == 383

    currency = next(
        field for field in fields if field["field_key"] == "f19_safebrake_currency_skip"
    )
    assert currency["action"] == "skip"
    assert currency["constant"] == ""
    assert currency["risk_level"] == "safety_fuse"
    assert field_map["safe_brake"]["intentionally_blank"] is True


def test_v311_store_safebrake_coordinate_is_imported():
    store = yaml.safe_load((PACK_DIR / "store_safebrake.yaml").read_text(encoding="utf-8"))

    assert store["store_action"] == "store_line_safebrake"
    assert store["x"] == 62
    assert store["y"] == 151
    assert store["safe_brake"]["currency_intentionally_blank"] is True
    assert "SW_MAXIMIZE" in store["activation_method"]


def test_v311_sample_values_leave_currency_blank():
    sample = load_sample_values(PACK_DIR)

    assert sample["zyrat_doganore"] == "AL111000"
    assert sample["customs_tariff_2"] == "000"
    assert sample["currency"] == ""


def test_v311_compiler_omits_currency_and_forbidden_actions():
    sample = load_sample_values(PACK_DIR)
    steps = compile_steps_from_declaration(sample, pack_dir=PACK_DIR)

    actions = [step["action"] for step in steps]
    field_keys = [step.get("field_key") for step in steps]

    assert "f19_safebrake_currency_skip" not in field_keys
    assert not (set(actions) & FORBIDDEN_ACTIONS)
    assert actions[-1] == "screenshot"

    first = steps[0]
    assert first["action"] == "click_paste"
    assert first["field_key"] == "f01_zyrat_doganore_code"
    assert first["x"] == 90
    assert first["y"] == 383

    tariff2 = next(step for step in steps if step.get("field_key") == "f08_customs_tariff_2")
    tariff2_index = steps.index(tariff2)
    assert steps[tariff2_index + 1]["action"] == "hotkey"
    assert steps[tariff2_index + 1]["keys"] == ["tab"]

    statistical = next(
        step for step in steps if step.get("field_key") == "f09_statistical_quantity_keyboard"
    )
    assert statistical["action"] == "paste"
    assert "x" not in statistical
    assert "y" not in statistical


def test_v311_compiler_can_append_safebrake_store_action():
    sample = load_sample_values(PACK_DIR)
    steps = compile_steps_from_declaration(
        sample,
        include_store_safebrake=True,
        pack_dir=PACK_DIR,
    )

    assert steps[-1]["action"] == "store_line_safebrake"
    assert steps[-1]["x"] == 62
    assert steps[-1]["y"] == 151


def test_v311_unsigned_job_plan_uses_expected_mode_and_pack_metadata():
    sample = load_sample_values(PACK_DIR)
    plan = build_unsigned_job_plan(
        sample,
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        job_id="job_test",
        include_store_safebrake=True,
        pack_dir=PACK_DIR,
    )

    assert plan["pack_id"] == "asycuda_albania_line_transaction"
    assert plan["pack_version"] == "v3.1.1-safebrake-geometry-fix"
    assert plan["mode"] == "safeBrakeStore"
    assert plan["steps"][-1]["action"] == "store_line_safebrake"
    assert "signature" not in plan

    json.dumps(plan)
