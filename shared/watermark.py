from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path


def watermark_text(tenant_id: str, machine_id: str, job_id: str, run_id: str) -> str:
    timestamp = datetime.now(UTC).isoformat()
    return (
        f"CUSTOMSOPS CONTROLLED EVIDENCE | tenant={tenant_id} | machine={machine_id} | "
        f"job={job_id} | run={run_id} | captured={timestamp}"
    )


def write_watermarked_text_artifact(path: Path, content: str, watermark: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{watermark}\n\n{content}", encoding="utf-8")
    return path

