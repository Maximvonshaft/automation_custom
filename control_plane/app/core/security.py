from __future__ import annotations

ALLOWED_MODES = {"fillOnly", "safeBrakeStore"}
FORBIDDEN_ACTIONS = {
    "submit",
    "register",
    "payment",
    "tax_finalize",
    "credential_read",
    "backend_request",
}


def assert_mode_allowed(mode: str) -> None:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Mode is not allowed in v4.0: {mode}")


def assert_actions_allowed(steps: list[dict]) -> None:
    forbidden = [step.get("action") for step in steps if step.get("action") in FORBIDDEN_ACTIONS]
    if forbidden:
        raise ValueError(f"Forbidden action(s) in job plan: {', '.join(sorted(set(forbidden)))}")
