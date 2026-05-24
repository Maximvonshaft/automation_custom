from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/evidence", tags=["evidence"])


@router.post("/manifest")
def accept_evidence_manifest(manifest: dict) -> dict[str, object]:
    return {"accepted": True, "job_id": manifest.get("job_id"), "run_id": manifest.get("run_id")}

