from __future__ import annotations

from datetime import UTC, datetime

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from agent.customsops_agent.forbidden_actions import assert_agent_action_allowed
from shared.signing.ed25519 import unsigned_payload, verify_payload
from shared.time import parse_utc_datetime


def validate_signed_plan(
    plan: dict,
    *,
    public_key: Ed25519PublicKey,
    expected_tenant_id: str,
    expected_machine_id: str,
    allowed_modes: set[str] | None = None,
) -> dict:
    allowed_modes = allowed_modes or {"fillOnly", "safeBrakeStore"}
    signature = plan.get("signature")
    if not signature:
        raise ValueError("Job plan is unsigned")
    if not verify_payload(unsigned_payload(plan), signature, public_key):
        raise ValueError("Job plan signature verification failed")
    if plan["tenant_id"] != expected_tenant_id:
        raise ValueError("Job plan tenant mismatch")
    if plan["machine_id"] != expected_machine_id:
        raise ValueError("Job plan machine mismatch")
    if plan["mode"] not in allowed_modes:
        raise ValueError(f"Job plan mode is not allowed: {plan['mode']}")
    if parse_utc_datetime(plan["expires_at"]) <= datetime.now(UTC):
        raise ValueError("Job plan expired")
    for step in plan["steps"]:
        assert_agent_action_allowed(step["action"])
    return plan

