from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from control_plane.app.services.job_compiler import JobCompiler
from control_plane.app.services.job_signer import JobSigner
from control_plane.app.services.pack_loader import CountryPackLoader
from shared.signing.ed25519 import generate_private_key, public_key_to_pem


@pytest.fixture
def signing_keypair():
    private_key = generate_private_key()
    return private_key, public_key_to_pem(private_key.public_key())


@pytest.fixture
def signed_plan(signing_keypair):
    private_key, _public_key_pem = signing_keypair
    pack = CountryPackLoader(packs_root=Path("control_plane/packs")).load_pack("albania_asycuda")
    plan = JobCompiler().compile_job(
        tenant_id="tenant_demo",
        machine_id="machine_demo",
        pack=pack,
        mode="safeBrakeStore",
        values={"invoice_number": "INV-100", "gross_weight": "42"},
    )
    return JobSigner(private_key).sign(plan)


@pytest.fixture
def expired_plan(signed_plan, signing_keypair):
    private_key, _public_key_pem = signing_keypair
    plan = dict(signed_plan)
    plan["expires_at"] = (datetime.now(UTC) - timedelta(minutes=1)).isoformat()
    return JobSigner(private_key).sign(plan)
