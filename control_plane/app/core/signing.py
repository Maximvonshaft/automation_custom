from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from shared.signing.ed25519 import generate_private_key, load_private_key_pem


def load_or_create_private_key(private_key_pem: str | None) -> Ed25519PrivateKey:
    if private_key_pem:
        return load_private_key_pem(private_key_pem)
    return generate_private_key()

