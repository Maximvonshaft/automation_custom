from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from shared.watermark import write_watermarked_text_artifact


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_v311_review_bundle(
    *,
    root: Path,
    job_plan: dict,
    parse_report: dict,
    declaration_model: dict,
    ledger_entries: list[dict],
    watermark: str,
    screenshot_paths: list[Path] | None = None,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    screenshots_dir = root / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = root / "ledger.jsonl"
    ledger_path.write_text(
        "\n".join(json.dumps(entry, sort_keys=True) for entry in ledger_entries) + "\n",
        encoding="utf-8",
    )
    run_context_path = root / "run_context.json"
    run_context = {
        "tenant_id": job_plan["tenant_id"],
        "machine_id": job_plan["machine_id"],
        "job_id": job_plan["job_id"],
        "mode": job_plan["mode"],
        "pack_id": job_plan["pack_id"],
        "pack_version": job_plan["pack_version"],
    }
    run_context_path.write_text(json.dumps(run_context, indent=2, sort_keys=True), encoding="utf-8")

    parse_report_path = root / "manifest_parse_report.json"
    parse_report_path.write_text(
        json.dumps(parse_report, indent=2, sort_keys=True), encoding="utf-8"
    )

    declaration_path = root / "declaration_model.json"
    declaration_path.write_text(
        json.dumps(declaration_model, indent=2, sort_keys=True), encoding="utf-8"
    )
    signed_plan_path = root / "signed_job_plan.json"
    signed_plan_path.write_text(json.dumps(job_plan, indent=2, sort_keys=True), encoding="utf-8")

    screenshot_artifacts: list[Path] = []
    if screenshot_paths:
        for index, source in enumerate(screenshot_paths, start=1):
            target = screenshots_dir / f"screenshot_{index:03d}{source.suffix.lower() or '.png'}"
            shutil.copy2(source, target)
            screenshot_artifacts.append(target)
    else:
        screenshot_path = screenshots_dir / "screenshot_001.txt"
        write_watermarked_text_artifact(screenshot_path, "v3.1.1-compatible screenshot", watermark)
        screenshot_artifacts.append(screenshot_path)

    artifacts = [
        ledger_path,
        run_context_path,
        parse_report_path,
        declaration_path,
        signed_plan_path,
        *screenshot_artifacts,
    ]
    metadata_path = root / "watermark_metadata.json"
    metadata = {
        "watermark": watermark,
        "hashes": {
            artifact.relative_to(root).as_posix(): _sha256(artifact) for artifact in artifacts
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    artifacts.append(metadata_path)

    bundle_path = root / "review_bundle.zip"
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for artifact in artifacts:
            archive.write(artifact, artifact.relative_to(root).as_posix())
    return bundle_path
