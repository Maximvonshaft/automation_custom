from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from uuid import uuid4

from agent.customsops_agent.ledger import write_ledger
from agent.customsops_agent.screenshot import capture_mock_screenshot
from shared.watermark import watermark_text


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class EvidenceBundleCollector:
    def __init__(self, root: Path, agent_version: str) -> None:
        self.root = root
        self.agent_version = agent_version

    def collect(self, plan: dict, ledger_entries: list[dict]) -> Path:
        run_id = f"run_{uuid4().hex}"
        bundle_dir = self.root / plan["tenant_id"] / plan["job_id"] / run_id
        bundle_dir.mkdir(parents=True, exist_ok=True)
        watermark = watermark_text(plan["tenant_id"], plan["machine_id"], plan["job_id"], run_id)
        screenshot = capture_mock_screenshot(bundle_dir / "screenshot_001.txt", watermark)
        ledger = write_ledger(bundle_dir / "ledger.json", ledger_entries)
        files = [screenshot.name, ledger.name]
        manifest = {
            "tenant_id": plan["tenant_id"],
            "machine_id": plan["machine_id"],
            "job_id": plan["job_id"],
            "run_id": run_id,
            "pack_id": plan["pack_id"],
            "pack_version": plan["pack_version"],
            "mode": plan["mode"],
            "agent_version": self.agent_version,
            "files": files,
            "hashes": {path.name: _sha256(path) for path in [screenshot, ledger]},
            "watermark": watermark,
        }
        manifest_path = bundle_dir / "evidence_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        zip_path = bundle_dir.with_suffix(".zip")
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for artifact in [screenshot, ledger, manifest_path]:
                archive.write(artifact, artifact.name)
        return zip_path

