from __future__ import annotations

import platform

import pytest

from agent.customsops_agent.action_executor import choose_executor
from agent.customsops_agent.executors.windows_gui import WindowsGuiExecutor


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
