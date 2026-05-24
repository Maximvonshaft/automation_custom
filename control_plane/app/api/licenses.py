from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter
from pydantic import BaseModel

from control_plane.app.db.models import License
from control_plane.app.db.session import registry

router = APIRouter(prefix="/licenses", tags=["licenses"])


class LicenseUpsert(BaseModel):
    tenant_id: str
    machine_id: str
    allowed_modes: list[str] = ["fillOnly", "safeBrakeStore"]
    expires_in_days: int = 30


@router.post("")
def upsert_license(request: LicenseUpsert) -> dict[str, object]:
    expires_at = (datetime.now(UTC) + timedelta(days=request.expires_in_days)).isoformat()
    license_record = License(
        tenant_id=request.tenant_id,
        machine_id=request.machine_id,
        status="active",
        allowed_modes=tuple(request.allowed_modes),
        expires_at=expires_at,
    )
    registry.licenses[(request.tenant_id, request.machine_id)] = license_record
    return {
        "tenant_id": license_record.tenant_id,
        "machine_id": license_record.machine_id,
        "status": license_record.status,
        "allowed_modes": list(license_record.allowed_modes),
        "expires_at": license_record.expires_at,
    }

