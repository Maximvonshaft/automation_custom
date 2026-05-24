from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/kill-switch/{tenant_id}/{machine_id}")
def revoke_machine(tenant_id: str, machine_id: str) -> dict[str, object]:
    return {"tenant_id": tenant_id, "machine_id": machine_id, "status": "revoked"}

