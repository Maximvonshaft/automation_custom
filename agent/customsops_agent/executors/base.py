from __future__ import annotations

from typing import Protocol


class ActionExecutor(Protocol):
    def execute(self, steps: list[dict]) -> list[dict]:
        """Execute already validated job-plan steps and return ledger entries."""

