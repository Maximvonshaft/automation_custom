from __future__ import annotations

from fastapi import APIRouter, HTTPException

from control_plane.app.services.declaration_model_builder import build_declaration_model
from control_plane.app.services.manifest_intake import parse_manifest

router = APIRouter(prefix="/manifests", tags=["manifests"])


@router.post("/parse")
def parse_manifest_payload(payload: dict) -> dict:
    try:
        workbook = payload["workbook"]
        manifest_bytes = str(workbook).encode("utf-8")
        manifest, report = parse_manifest(workbook)
        declaration_model = build_declaration_model(
            manifest,
            manifest_bytes=manifest_bytes,
            filename=payload.get("filename", "manifest.xlsx"),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"parse_report": report, "declaration_model": declaration_model}

