from __future__ import annotations

import pytest

from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed
from control_plane.app.core.security import assert_actions_allowed


def test_agent_rejects_submit_action():
    with pytest.raises(ValueError, match="forbidden"):
        assert_agent_action_allowed("submit")


def test_control_plane_rejects_forbidden_compiled_action():
    with pytest.raises(ValueError, match="Forbidden action"):
        assert_actions_allowed([{"step": 1, "action": "payment"}])

