from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from shared.signing.ed25519 import sign_payload, unsigned_payload


class JobSigner:
    def __init__(self, private_key: Ed25519PrivateKey) -> None:
        self.private_key = private_key

    def sign(self, job_plan: dict) -> dict:
        signed = dict(job_plan)
        signed["signature"] = sign_payload(unsigned_payload(signed), self.private_key)
        return signed

