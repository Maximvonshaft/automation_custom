from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from control_plane.app.db.models import Machine
from control_plane.app.db.session import registry

router = APIRouter(prefix="/machines", tags=["machines"])


class MachineRegistration(BaseModel):
    tenant_id: str
    machine_id: str


@router.post("")
def register_machine(request: MachineRegistration) -> dict[str, object]:
    machine = Machine(tenant_id=request.tenant_id, machine_id=request.machine_id)
    registry.machines[(machine.tenant_id, machine.machine_id)] = machine
    return {
        "tenant_id": machine.tenant_id,
        "machine_id": machine.machine_id,
        "active": machine.active,
    }
