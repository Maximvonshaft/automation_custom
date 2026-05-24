from __future__ import annotations

from dataclasses import dataclass, field

from agent.customsops_agent.executors.base import ActionExecutor
from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed


@dataclass
class MockActionExecutor:
    """Intentional v4.0 MVP executor boundary.

    Real Windows/ASYCUDA foreground GUI execution remains out of scope for this PR. The verified
    field runtime baseline remains v3.1.1 SafeBrake until that integration lands.
    """

    ledger: list[dict] = field(default_factory=list)

    def execute(self, steps: list[dict]) -> list[dict]:
        for step in steps:
            assert_agent_action_allowed(step["action"])
            self.ledger.append(
                {
                    "step": step["step"],
                    "action": step["action"],
                    "field_key": step.get("field_key"),
                    "label": step.get("label"),
                    "status": "mocked",
                }
            )
        return self.ledger


def choose_executor(
    *, use_real_gui: bool, foreground_window_title: str | None = None
) -> ActionExecutor:
    if not use_real_gui:
        return MockActionExecutor()
    from agent.customsops_agent.executors.windows_gui import WindowsGuiExecutor

    if foreground_window_title is None:
        raise ValueError("Foreground window title is required for real GUI execution")
    return WindowsGuiExecutor(foreground_window_title=foreground_window_title)
