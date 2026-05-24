from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class CountryPackLoader:
    def __init__(self, packs_root: Path) -> None:
        self.packs_root = packs_root

    def load_pack(self, pack_id: str) -> dict[str, Any]:
        pack_dir = self.packs_root / pack_id
        field_map_path = pack_dir / "field_map.example.yaml"
        safebrake_path = pack_dir / "safebrake_policy.example.yaml"
        if not field_map_path.exists() or not safebrake_path.exists():
            raise FileNotFoundError(f"Country pack is incomplete: {pack_id}")
        return {
            "pack_id": pack_id,
            "field_map": yaml.safe_load(field_map_path.read_text(encoding="utf-8")),
            "safebrake": yaml.safe_load(safebrake_path.read_text(encoding="utf-8")),
        }

