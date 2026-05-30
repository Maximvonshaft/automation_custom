from __future__ import annotations

import json
from pathlib import Path

from agent.customsops_agent.executors.windows_gui import WindowsGuiExecutor
from agent.customsops_agent.forbidden_actions import FORBIDDEN_ACTIONS
from control_plane.app.services.albania_line_transaction_compiler import (
    compile_steps_from_declaration,
    load_sample_values,
)

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = (
    ROOT
    / "control_plane"
    / "packs"
    / "asycuda_albania_line_transaction"
    / "v3_1_safebrake"
)


class FakeGuiBackend:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def click(self, x: int, y: int) -> None:
        self.calls.append(("click", x, y))

    def paste(self, value: str) -> None:
        self.calls.append(("paste", value))

    def hotkey(self, keys: list[str]) -> None:
        self.calls.append(("hotkey", keys))

    def screenshot(self, path):  # pragma: no cover - not used here
        self.calls.append(("screenshot", path))
        return path


def test_action_schema_allows_clear_before_paste_actions():
    schema = json.loads((ROOT / "shared" / "schemas" / "action.schema.json").read_text())
    actions = set(schema["properties"]["action"]["enum"])

    assert "clear_paste" in actions
    assert "click_clear_paste" in actions


def test_windows_gui_executor_clears_before_paste():
    backend = FakeGuiBackend()
    executor = WindowsGuiExecutor(
        foreground_window_title="ASYCUDAWorld",
        backend=backend,
        platform_name="Windows",
        active_window_title_provider=lambda: "ASYCUDAWorld - zhani:lule",
    )

    executor.execute(
        [
            {
                "step": 1,
                "action": "clear_paste",
                "value": "ALI2025",
                "field_key": "f02_authorization_reference",
            },
            {
                "step": 2,
                "action": "click_clear_paste",
                "x": 61,
                "y": 563,
                "value": "85176200",
                "field_key": "f07_customs_tariff_1",
            },
        ]
    )

    assert backend.calls == [
        ("hotkey", ["ctrl", "a"]),
        ("paste", "ALI2025"),
        ("click", 61, 563),
        ("hotkey", ["ctrl", "a"]),
        ("paste", "85176200"),
    ]


def test_albania_compiler_uses_pr27_coordinates_and_clear_paste():
    sample = load_sample_values(PACK_DIR)
    steps = compile_steps_from_declaration(sample, pack_dir=PACK_DIR)

    by_field = {step.get("field_key"): step for step in steps if step.get("field_key")}

    assert by_field["f02_authorization_reference"]["value"] == "ALI2025"
    assert by_field["f02_authorization_reference"]["action"] == "click_clear_paste"
    assert by_field["f02_authorization_reference"]["x"] == 111
    assert by_field["f02_authorization_reference"]["y"] == 444

    assert by_field["f07_customs_tariff_1"]["action"] == "click_clear_paste"
    assert by_field["f07_customs_tariff_1"]["x"] == 61
    assert by_field["f07_customs_tariff_1"]["y"] == 563

    f09 = by_field["f09_statistical_quantity_keyboard"]
    assert f09["action"] == "click_clear_paste"
    assert f09["x"] == 388
    assert f09["y"] == 561

    assert by_field["f18_invoice_value"]["x"] == 395
    assert by_field["f18_invoice_value"]["y"] == 764
    assert by_field["f20_document_reference"]["x"] == 106
    assert by_field["f20_document_reference"]["y"] == 822

    assert "f19_safebrake_currency_skip" not in by_field
    assert not ({step["action"] for step in steps} & FORBIDDEN_ACTIONS)
