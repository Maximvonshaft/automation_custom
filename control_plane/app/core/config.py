from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("CUSTOMSOPS_ENV", "local")
    signing_private_key_pem: str | None = os.getenv("CUSTOMSOPS_SIGNING_PRIVATE_KEY_PEM")
    packs_root: Path = Path(os.getenv("CUSTOMSOPS_PACKS_ROOT", "control_plane/packs"))
    evidence_root: Path = Path(os.getenv("CUSTOMSOPS_EVIDENCE_ROOT", "evidence/server"))


settings = Settings()

