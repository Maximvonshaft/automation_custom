from __future__ import annotations

FORBIDDEN_ACTIONS = {
    "submit",
    "register",
    "payment",
    "tax_finalize",
    "credential_read",
    "backend_request",
}
ALLOWED_ACTIONS = {
    "click",
    "paste",
    "click_paste",
    "hotkey",
    "wait",
    "screenshot",
    "store_line_safebrake",
}


def assert_agent_action_allowed(action: str) -> None:
    if action in FORBIDDEN_ACTIONS or action not in ALLOWED_ACTIONS:
        raise ValueError(f"Agent rejected unsupported or forbidden action: {action}")
