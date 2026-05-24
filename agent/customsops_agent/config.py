from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    tenant_id: str = os.getenv("CUSTOMSOPS_TENANT_ID", "tenant_demo")
    machine_id: str = os.getenv("CUSTOMSOPS_MACHINE_ID", "machine_demo")
    public_key_pem: str = os.getenv("CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM", "")
    evidence_root: Path = Path(os.getenv("CUSTOMSOPS_AGENT_EVIDENCE_ROOT", "evidence/agent"))
    agent_version: str = "4.0.0"

