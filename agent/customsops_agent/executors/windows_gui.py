from __future__ import annotations

import platform
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed
from agent.customsops_agent.window_foreground import assert_asycuda_foreground_window


class GuiBackend(Protocol):
    def click(self, x: int, y: int) -> None: ...

    def paste(self, value: str) -> None: ...

    def hotkey(self, keys: list[str]) -> None: ...

    def screenshot(self, path: Path) -> Path: ...


class PyAutoGuiBackend:
    def click(self, x: int, y: int) -> None:
        import pyautogui

        pyautogui.click(x=x, y=y)

    def paste(self, value: str) -> None:
        import pyautogui
        import pyperclip

        pyperclip.copy(value)
        pyautogui.hotkey("ctrl", "v")

    def hotkey(self, keys: list[str]) -> None:
        import pyautogui

        pyautogui.hotkey(*keys)

    def screenshot(self, path: Path) -> Path:
        import pyautogui

        path.parent.mkdir(parents=True, exist_ok=True)
        image = pyautogui.screenshot()
        image.save(path)
        return path


@dataclass
class WindowsGuiExecutor:
    foreground_window_title: str
    backend: GuiBackend | None = None
    platform_name: str = field(default_factory=platform.system)
    ledger: list[dict] = field(default_factory=list)
    active_window_title_provider: Callable[[], str] | None = None

    def __post_init__(self) -> None:
        if self.platform_name != "Windows":
            raise RuntimeError("Real GUI execution is Windows-only")
        self._assert_foreground()
        if self.backend is None:
            self.backend = PyAutoGuiBackend()

    def _assert_foreground(self) -> str:
        return assert_asycuda_foreground_window(
            self.foreground_window_title,
            active_window_title_provider=self.active_window_title_provider,
        )

    def execute(self, steps: list[dict]) -> list[dict]:
        for step in steps:
            self._assert_foreground()
            action = step["action"]
            assert_agent_action_allowed(action)
            handler = getattr(self, f"execute_{action}", None)
            if handler is None:
                raise ValueError(f"Unsupported GUI action: {action}")
            handler(step)
        return self.ledger

    def _record(self, step: dict, status: str = "executed") -> None:
        entry = {
            "step": step["step"],
            "action": step["action"],
            "field_key": step.get("field_key"),
            "label": step.get("label"),
            "status": status,
        }
        if step.get("artifact_path"):
            entry["artifact_path"] = str(step["artifact_path"])
        self.ledger.append(entry)

    def execute_wait(self, step: dict) -> None:
        duration_seconds = float(step.get("duration_seconds", 0.1))
        time.sleep(max(duration_seconds, 0.0))
        self._record(step)

    def execute_click(self, step: dict) -> None:
        self.backend.click(int(step["x"]), int(step["y"]))
        self._record(step)

    def execute_paste(self, step: dict) -> None:
        self.backend.paste(str(step.get("value", "")))
        self._record(step)

    def execute_click_paste(self, step: dict) -> None:
        self.backend.click(int(step["x"]), int(step["y"]))
        self.backend.paste(str(step.get("value", "")))
        self._record(step)

    def execute_hotkey(self, step: dict) -> None:
        self.backend.hotkey([str(key) for key in step.get("keys", [])])
        self._record(step)

    def execute_screenshot(self, step: dict) -> None:
        path = Path(str(step.get("path", "evidence/screenshots/screenshot.png")))
        captured_path = self.backend.screenshot(path)
        recorded_step = dict(step)
        recorded_step["artifact_path"] = str(captured_path)
        self._record(recorded_step)

    def execute_store_line_safebrake(self, step: dict) -> None:
        self.backend.click(int(step["x"]), int(step["y"]))
        self._record(step, status="safebrake_store_attempted")
