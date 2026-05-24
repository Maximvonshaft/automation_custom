from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from control_plane.app.core.config import settings
from control_plane.app.core.signing import load_or_create_private_key
from control_plane.app.services.job_compiler import JobCompiler
from control_plane.app.services.job_signer import JobSigner
from control_plane.app.services.pack_loader import CountryPackLoader

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobCompileRequest(BaseModel):
    tenant_id: str
    machine_id: str
    pack_id: str = "albania_asycuda"
    mode: str = "fillOnly"
    values: dict[str, str]


@router.post("/compile")
def compile_job(request: JobCompileRequest) -> dict:
    try:
        pack = CountryPackLoader(settings.packs_root).load_pack(request.pack_id)
        plan = JobCompiler().compile_job(
            tenant_id=request.tenant_id,
            machine_id=request.machine_id,
            pack=pack,
            mode=request.mode,
            values=request.values,
        )
        private_key = load_or_create_private_key(settings.signing_private_key_pem)
        return JobSigner(private_key).sign(plan)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

