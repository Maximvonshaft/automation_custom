from __future__ import annotations

import inspect

import pytest

from agent.customsops_agent.action_executor import MockActionExecutor
from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed


def test_mock_action_executor_is_intentional_v4_mvp_boundary():
    assert MockActionExecutor.__name__ == "MockActionExecutor"
    assert "v4.0 MVP executor boundary" in inspect.getdoc(MockActionExecutor)
    assert MockActionExecutor().execute([{"step": 1, "action": "wait", "label": "boundary"}]) == [
        {
            "step": 1,
            "action": "wait",
            "field_key": None,
            "label": "boundary",
            "status": "mocked",
        }
    ]


def test_real_windows_asycuda_gui_executor_is_out_of_scope_for_this_pr():
    agent_sources = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in __import__("pathlib").Path("agent/customsops_agent").rglob("*.py")
    )
    assert "MockActionExecutor" in agent_sources
    assert "RealAsycudaGuiExecutor" not in agent_sources
    assert "WindowsAsycudaGuiExecutor" not in agent_sources


@pytest.mark.parametrize("action", ["submit", "register", "payment", "tax_finalize"])
def test_tax_and_finalization_actions_remain_forbidden(action):
    with pytest.raises(ValueError, match="forbidden"):
        assert_agent_action_allowed(action)
