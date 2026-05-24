from __future__ import annotations

import hashlib
from pathlib import Path

ALLOWED_MANIFEST_SUFFIXES = {".xlsx", ".xlsm", ".csv"}


def precheck_manifest_file(path: Path) -> dict[str, object]:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Manifest file not found: {path}")
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_MANIFEST_SUFFIXES:
        raise ValueError(f"Unsupported manifest file type: {suffix}")
    content = path.read_bytes()
    return {
        "filename": path.name,
        "suffix": suffix,
        "size_bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "can_compile_executable_plan": False,
    }

