from __future__ import annotations

import json
from pathlib import Path

from agent.customsops_agent.action_executor import MockActionExecutor
from agent.customsops_agent.config import AgentConfig
from agent.customsops_agent.evidence_bundle import EvidenceBundleCollector
from agent.customsops_agent.signed_plan import validate_signed_plan
from shared.signing.ed25519 import load_public_key_pem


def run_signed_job(plan_path: Path, config: AgentConfig) -> Path:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    public_key = load_public_key_pem(config.public_key_pem)
    validated = validate_signed_plan(
        plan,
        public_key=public_key,
        expected_tenant_id=config.tenant_id,
        expected_machine_id=config.machine_id,
    )
    ledger = MockActionExecutor().execute(validated["steps"])
    return EvidenceBundleCollector(config.evidence_root, config.agent_version).collect(
        validated, ledger
    )
