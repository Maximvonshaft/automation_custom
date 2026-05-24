from __future__ import annotations

import json
from pathlib import Path


def write_ledger(path: Path, entries: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2, sort_keys=True), encoding="utf-8")
    return path

