from __future__ import annotations

import platform
from dataclasses import dataclass, field

from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed
from agent.customsops_agent.window_foreground import assert_asycuda_foreground_window


@dataclass
class WindowsGuiExecutor:
    foreground_window_title: str
    ledger: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("Real GUI execution is Windows-only")
        assert_asycuda_foreground_window(self.foreground_window_title)

    def execute(self, steps: list[dict]) -> list[dict]:
        for step in steps:
            action = step["action"]
            assert_agent_action_allowed(action)
            handler = getattr(self, f"execute_{action}", None)
            if handler is None:
                raise ValueError(f"Unsupported GUI action: {action}")
            handler(step)
        return self.ledger

    def _record(self, step: dict, status: str = "executed") -> None:
        self.ledger.append(
            {
                "step": step["step"],
                "action": step["action"],
                "field_key": step.get("field_key"),
                "label": step.get("label"),
                "status": status,
            }
        )

    def execute_click(self, step: dict) -> None:
        self._record(step)

    def execute_paste(self, step: dict) -> None:
        self._record(step)

    def execute_click_paste(self, step: dict) -> None:
        self._record(step)

    def execute_hotkey(self, step: dict) -> None:
        self._record(step)

    def execute_screenshot(self, step: dict) -> None:
        self._record(step)

    def execute_store_line_safebrake(self, step: dict) -> None:
        self._record(step, status="safebrake_store_attempted")

