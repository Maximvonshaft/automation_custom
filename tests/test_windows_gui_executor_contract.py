from __future__ import annotations

import platform

import pytest

from agent.customsops_agent.action_executor import choose_executor
from agent.customsops_agent.executors.windows_gui import WindowsGuiExecutor


class FakeGuiBackend:
    def __init__(self, tmp_path=None):
        self.calls = []
        self.tmp_path = tmp_path

    def click(self, x: int, y: int) -> None:
        self.calls.append(("click", x, y))

    def paste(self, value: str) -> None:
        self.calls.append(("paste", value))

    def hotkey(self, keys: list[str]) -> None:
        self.calls.append(("hotkey", keys))

    def screenshot(self, path):
        self.calls.append(("screenshot", path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fake png")
        return path


def test_mock_executor_is_cross_platform_default():
    executor = choose_executor(use_real_gui=False)
    ledger = executor.execute([{"step": 1, "action": "wait", "label": "dry-run"}])
    assert ledger[0]["status"] == "mocked"


def test_real_gui_executor_fails_closed_on_non_windows():
    if platform.system() == "Windows":
        pytest.skip("Non-Windows fail-closed behavior is covered in Linux CI")
    with pytest.raises(RuntimeError, match="Windows-only"):
        WindowsGuiExecutor(foreground_window_title="ASYCUDA World")


def test_real_gui_executor_requires_foreground_window_title():
    with pytest.raises(ValueError, match="Foreground window title"):
        choose_executor(use_real_gui=True)


def test_windows_gui_executor_invokes_backend_for_supported_actions(tmp_path):
    backend = FakeGuiBackend(tmp_path)
    executor = WindowsGuiExecutor(
        foreground_window_title="ASYCUDA World",
        backend=backend,
        platform_name="Windows",
    )
    screenshot_path = tmp_path / "screenshots" / "shot.png"
    ledger = executor.execute(
        [
            {"step": 1, "action": "click", "x": 10, "y": 20, "label": "click"},
            {"step": 2, "action": "paste", "value": "SANITIZED", "label": "paste"},
            {"step": 3, "action": "hotkey", "keys": ["ctrl", "s"], "label": "hotkey"},
            {"step": 4, "action": "screenshot", "path": str(screenshot_path), "label": "shot"},
        ]
    )
    assert backend.calls == [
        ("click", 10, 20),
        ("paste", "SANITIZED"),
        ("hotkey", ["ctrl", "s"]),
        ("screenshot", screenshot_path),
    ]
    assert [entry["status"] for entry in ledger] == ["executed"] * 4
