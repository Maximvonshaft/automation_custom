from datetime import UTC, datetime, timedelta

import pytest

from agent.customsops_agent.machine_identity import (
    assert_machine_registration_active,
    machine_fingerprint_sha256,
    parse_machine_registration,
)
from agent.customsops_agent.signed_plan import validate_signed_plan
from control_plane.app.services.job_signer import JobSigner
from shared.signing.ed25519 import generate_private_key


def _registration(status: str = "active") -> dict:
    return {
        "tenant_id": "tenant_demo",
        "machine_id": "machine_demo",
        "machine_fingerprint_sha256": "a" * 64,
        "agent_version": "4.0.0",
        "operator_package_version": "0.0.0-skeleton",
        "registration_status": status,
        "registered_at_utc": "2026-05-28T00:00:00Z",
    }


def _signed_plan(machine_id: str = "machine_demo") -> tuple[dict, object]:
    private_key = generate_private_key()
    plan = {
        "job_id": "job_machine_binding_test",
        "tenant_id": "tenant_demo",
        "machine_id": machine_id,
        "mode": "safeBrakeStore",
        "pack_id": "albania_asycuda_internal_lab",
        "pack_version": "4.1-lab",
        "issued_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "expires_at": (datetime.now(UTC) + timedelta(hours=1))
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "steps": [{"action": "screenshot", "args": {"path": "post.png"}}],
    }
    return JobSigner(private_key).sign(plan), private_key.public_key()


def test_machine_fingerprint_is_deterministic_for_same_parts():
    parts = {
        "node": "host-a",
        "system": "Windows",
        "release": "11",
        "machine": "AMD64",
        "mac": "abc",
    }

    assert machine_fingerprint_sha256(parts) == machine_fingerprint_sha256(parts)
    assert len(machine_fingerprint_sha256(parts)) == 64


def test_parse_active_machine_registration():
    registration = parse_machine_registration(_registration("active"))

    assert registration.tenant_id == "tenant_demo"
    assert registration.machine_id == "machine_demo"
    assert registration.is_active is True
    assert registration.is_revoked is False
    assert_machine_registration_active(registration)


@pytest.mark.parametrize("status", ["pending", "revoked", "disabled"])
def test_machine_registration_non_active_status_fails_closed(status: str):
    registration = parse_machine_registration(_registration(status))

    with pytest.raises(ValueError):
        assert_machine_registration_active(registration)


def test_machine_registration_rejects_missing_required_field():
    data = _registration("active")
    del data["machine_id"]

    with pytest.raises(ValueError, match="missing required fields"):
        parse_machine_registration(data)


def test_machine_registration_rejects_invalid_fingerprint():
    data = _registration("active")
    data["machine_fingerprint_sha256"] = "not-a-sha256"

    with pytest.raises(ValueError, match="fingerprint"):
        parse_machine_registration(data)


def test_signed_plan_machine_binding_rejects_wrong_machine():
    plan, public_key = _signed_plan(machine_id="other_machine")

    with pytest.raises(ValueError, match="machine mismatch"):
        validate_signed_plan(
            plan,
            public_key=public_key,
            expected_tenant_id="tenant_demo",
            expected_machine_id="machine_demo",
        )


def test_signed_plan_machine_binding_accepts_registered_machine():
    registration = parse_machine_registration(_registration("active"))
    assert_machine_registration_active(registration)
    plan, public_key = _signed_plan(machine_id=registration.machine_id)

    validated = validate_signed_plan(
        plan,
        public_key=public_key,
        expected_tenant_id=registration.tenant_id,
        expected_machine_id=registration.machine_id,
    )

    assert validated["machine_id"] == "machine_demo"
