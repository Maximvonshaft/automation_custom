from __future__ import annotations

import base64
import json
from copy import deepcopy
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def canonical_json(payload: dict[str, Any]) -> bytes:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return encoded.encode("utf-8")


def unsigned_payload(plan: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(plan)
    payload.pop("signature", None)
    return payload


def generate_private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


def private_key_to_pem(private_key: Ed25519PrivateKey) -> str:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")


def public_key_to_pem(public_key: Ed25519PublicKey) -> str:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def load_private_key_pem(pem: str) -> Ed25519PrivateKey:
    key = serialization.load_pem_private_key(pem.encode("ascii"), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("Expected Ed25519 private key")
    return key


def load_public_key_pem(pem: str) -> Ed25519PublicKey:
    key = serialization.load_pem_public_key(pem.encode("ascii"))
    if not isinstance(key, Ed25519PublicKey):
        raise TypeError("Expected Ed25519 public key")
    return key


def sign_payload(payload: dict[str, Any], private_key: Ed25519PrivateKey) -> str:
    signature = private_key.sign(canonical_json(payload))
    return base64.urlsafe_b64encode(signature).decode("ascii")


def verify_payload(payload: dict[str, Any], signature: str, public_key: Ed25519PublicKey) -> bool:
    try:
        decoded_signature = base64.urlsafe_b64decode(signature.encode("ascii"))
        public_key.verify(decoded_signature, canonical_json(payload))
    except (InvalidSignature, ValueError):
        return False
    return True
