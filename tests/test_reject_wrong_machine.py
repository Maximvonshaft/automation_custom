from __future__ import annotations

import pytest

from agent.customsops_agent.signed_plan import validate_signed_plan
from shared.signing.ed25519 import load_public_key_pem


def test_agent_rejects_wrong_machine(signed_plan, signing_keypair):
    _private_key, public_key_pem = signing_keypair
    with pytest.raises(ValueError, match="machine mismatch"):
        validate_signed_plan(
            signed_plan,
            public_key=load_public_key_pem(public_key_pem),
            expected_tenant_id="tenant_demo",
            expected_machine_id="machine_other",
        )

