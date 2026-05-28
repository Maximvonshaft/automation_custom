from __future__ import annotations

import hashlib
import json
import os
import platform
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MachineRegistration:
    tenant_id: str
    machine_id: str
    machine_fingerprint_sha256: str
    agent_version: str
    operator_package_version: str
    registration_status: str
    registered_at_utc: str
    revoked_at_utc: str | None = None
    revocation_reason: str | None = None
    public_key_id: str | None = None

    @property
    def is_active(self) -> bool:
        return self.registration_status == "active"

    @property
    def is_revoked(self) -> bool:
        return self.registration_status in {"revoked", "disabled"}


def default_machine_config_path() -> Path:
    root = os.getenv("CUSTOMSOPS_MACHINE_CONFIG_ROOT")
    if root:
        return Path(root) / "machine_registration.json"
    return Path.home() / ".customsops" / "machine_registration.json"


def collect_machine_fingerprint_parts() -> dict[str, str]:
    return {
        "node": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "mac": f"{uuid.getnode():012x}",
    }


def machine_fingerprint_sha256(parts: dict[str, str] | None = None) -> str:
    parts = parts or collect_machine_fingerprint_parts()
    payload = json.dumps(parts, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_machine_registration(path: Path | None = None) -> MachineRegistration:
    path = path or default_machine_config_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    return parse_machine_registration(data)


def parse_machine_registration(data: dict[str, Any]) -> MachineRegistration:
    required = {
        "tenant_id",
        "machine_id",
        "machine_fingerprint_sha256",
        "agent_version",
        "operator_package_version",
        "registration_status",
        "registered_at_utc",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"Machine registration missing required fields: {missing}")

    status = str(data["registration_status"])
    if status not in {"pending", "active", "revoked", "disabled"}:
        raise ValueError(f"Unsupported machine registration status: {status}")

    fingerprint = str(data["machine_fingerprint_sha256"])
    if len(fingerprint) != 64 or any(char not in "0123456789abcdef" for char in fingerprint):
        raise ValueError("Machine fingerprint must be lowercase SHA-256 hex")

    return MachineRegistration(
        tenant_id=str(data["tenant_id"]),
        machine_id=str(data["machine_id"]),
        machine_fingerprint_sha256=fingerprint,
        agent_version=str(data["agent_version"]),
        operator_package_version=str(data["operator_package_version"]),
        registration_status=status,
        registered_at_utc=str(data["registered_at_utc"]),
        revoked_at_utc=data.get("revoked_at_utc"),
        revocation_reason=data.get("revocation_reason"),
        public_key_id=data.get("public_key_id"),
    )


def assert_machine_registration_active(registration: MachineRegistration) -> None:
    if registration.is_revoked:
        raise ValueError("Machine registration is revoked or disabled")
    if not registration.is_active:
        raise ValueError(f"Machine registration is not active: {registration.registration_status}")
