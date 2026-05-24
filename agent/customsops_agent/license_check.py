from __future__ import annotations

from datetime import UTC, datetime

from shared.time import parse_utc_datetime


def assert_license_active(
    license_response: dict, tenant_id: str, machine_id: str, mode: str
) -> None:
    if license_response["tenant_id"] != tenant_id:
        raise ValueError("License tenant mismatch")
    if license_response["machine_id"] != machine_id:
        raise ValueError("License machine mismatch")
    if license_response["status"] != "active":
        raise ValueError(f"License is not active: {license_response['status']}")
    if mode not in license_response["allowed_modes"]:
        raise ValueError(f"Mode is not licensed: {mode}")
    if parse_utc_datetime(license_response["expires_at"]) <= datetime.now(UTC):
        raise ValueError("License expired")
