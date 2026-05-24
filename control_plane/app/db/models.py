from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    tenant_id: str
    machine_id: str
    active: bool = True


@dataclass(frozen=True)
class License:
    tenant_id: str
    machine_id: str
    status: str
    allowed_modes: tuple[str, ...]
    expires_at: str

