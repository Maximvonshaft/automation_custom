from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path
from uuid import uuid4

from agent.customsops_agent.ledger import write_ledger
from agent.customsops_agent.screenshot import capture_mock_screenshot
from shared.watermark import watermark_text


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_artifact_name(source: Path, fallback_name: str) -> str:
    suffix = source.suffix or Path(fallback_name).suffix
    stem = source.stem or Path(fallback_name).stem
    safe_stem = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in stem)
    return f"{safe_stem}{suffix}" if safe_stem else fallback_name


def _collect_screenshot_artifacts(bundle_dir: Path, ledger_entries: list[dict]) -> list[Path]:
    artifacts: list[Path] = []
    used_names: set[str] = set()
    screenshot_index = 1

    for entry in ledger_entries:
        if entry.get("action") != "screenshot" or not entry.get("artifact_path"):
            continue
        source = Path(str(entry["artifact_path"]))
        if not source.is_file():
            continue
        artifact_name = _safe_artifact_name(source, f"screenshot_{screenshot_index:03d}.png")
        while artifact_name in used_names:
            screenshot_index += 1
            artifact_name = f"screenshot_{screenshot_index:03d}{source.suffix or '.png'}"
        target = bundle_dir / artifact_name
        shutil.copy2(source, target)
        artifacts.append(target)
        used_names.add(artifact_name)
        screenshot_index += 1

    return artifacts


class EvidenceBundleCollector:
    def __init__(self, root: Path, agent_version: str) -> None:
        self.root = root
        self.agent_version = agent_version

    def collect(self, plan: dict, ledger_entries: list[dict]) -> Path:
        run_id = f"run_{uuid4().hex}"
        bundle_dir = self.root / plan["tenant_id"] / plan["job_id"] / run_id
        bundle_dir.mkdir(parents=True, exist_ok=True)
        watermark = watermark_text(plan["tenant_id"], plan["machine_id"], plan["job_id"], run_id)
        screenshot_artifacts = _collect_screenshot_artifacts(bundle_dir, ledger_entries)
        if not screenshot_artifacts:
            screenshot_artifacts = [
                capture_mock_screenshot(bundle_dir / "screenshot_001.txt", watermark)
            ]
        ledger = write_ledger(bundle_dir / "ledger.json", ledger_entries)
        artifacts = [*screenshot_artifacts, ledger]
        manifest = {
            "tenant_id": plan["tenant_id"],
            "machine_id": plan["machine_id"],
            "job_id": plan["job_id"],
            "run_id": run_id,
            "pack_id": plan["pack_id"],
            "pack_version": plan["pack_version"],
            "mode": plan["mode"],
            "agent_version": self.agent_version,
            "files": [path.name for path in artifacts],
            "hashes": {path.name: _sha256(path) for path in artifacts},
            "watermark": watermark,
            "screenshot_source": "real_gui" if screenshot_artifacts[0].suffix != ".txt" else "mock",
        }
        manifest_path = bundle_dir / "evidence_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        zip_path = bundle_dir.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for artifact in [*artifacts, manifest_path]:
                archive.write(artifact, artifact.name)
        return zip_path
