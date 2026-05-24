from __future__ import annotations

from agent.customsops_agent.signed_plan import validate_signed_plan
from shared.signing.ed25519 import load_public_key_pem


def test_agent_accepts_valid_signed_plan(signed_plan, signing_keypair):
    _private_key, public_key_pem = signing_keypair
    validated = validate_signed_plan(
        signed_plan,
        public_key=load_public_key_pem(public_key_pem),
        expected_tenant_id="tenant_demo",
        expected_machine_id="machine_demo",
    )
    assert validated["job_id"].startswith("job_")


def test_agent_rejects_tampered_plan(signed_plan, signing_keypair):
    _private_key, public_key_pem = signing_keypair
    tampered = dict(signed_plan)
    tampered["tenant_id"] = "tenant_other"
    try:
        validate_signed_plan(
            tampered,
            public_key=load_public_key_pem(public_key_pem),
            expected_tenant_id="tenant_other",
            expected_machine_id="machine_demo",
        )
    except ValueError as exc:
        assert "signature" in str(exc)
    else:
        raise AssertionError("Tampered plan was accepted")

