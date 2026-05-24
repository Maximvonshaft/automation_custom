from __future__ import annotations

from dataclasses import dataclass, field

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
