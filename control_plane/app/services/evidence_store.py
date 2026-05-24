from __future__ import annotations

from pathlib import Path
from shutil import copy2


class EvidenceStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def store_bundle(self, bundle_path: Path, tenant_id: str, job_id: str) -> Path:
        target_dir = self.root / tenant_id / job_id
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / bundle_path.name
        copy2(bundle_path, target)
        return target

