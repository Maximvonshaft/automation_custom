from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Sequence

from agent.customsops_agent.config import AgentConfig
from agent.customsops_agent.machine_identity import (
    assert_machine_registration_active,
    load_machine_registration,
)
from agent.customsops_agent.main import run_signed_job


def _load_public_key_pem(public_key_path: Path | None = None) -> str:
    if public_key_path is not None:
        return public_key_path.read_text(encoding="ascii")

    public_key_pem = os.getenv("CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM", "")
    if not public_key_pem.strip():
        raise ValueError("Missing trusted signing public key")
    return public_key_pem


def run_operator_signed_job(
    *,
    signed_job_plan: Path,
    machine_registration_path: Path | None = None,
    public_key_path: Path | None = None,
    evidence_root: Path | None = None,
    use_real_gui: bool = False,
    foreground_window_title: str | None = None,
) -> Path:
    """Run a signed HQ job through the local operator boundary.

    This function intentionally does not parse Excel, compile executable steps, or access country packs.
    It loads a local machine registration file, requires the registration to be active, and then delegates
    to the existing signed-plan validation and execution boundary.
    """

    registration = load_machine_registration(machine_registration_path)
    assert_machine_registration_active(registration)

    config = AgentConfig(
        tenant_id=registration.tenant_id,
        machine_id=registration.machine_id,
        public_key_pem=_load_public_key_pem(public_key_path),
        evidence_root=evidence_root or Path("evidence/operator"),
        agent_version=registration.agent_version,
    )

    return run_signed_job(
        signed_job_plan,
        config,
        use_real_gui=use_real_gui,
        foreground_window_title=foreground_window_title,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a CustomsOps signed job through operator flow")
    parser.add_argument("--signed-job-plan", required=True, type=Path)
    parser.add_argument("--machine-registration", type=Path)
    parser.add_argument("--public-key-pem", type=Path)
    parser.add_argument("--evidence-root", type=Path, default=Path("evidence/operator"))
    parser.add_argument("--real-gui", action="store_true")
    parser.add_argument("--foreground-window-title")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    bundle = run_operator_signed_job(
        signed_job_plan=args.signed_job_plan,
        machine_registration_path=args.machine_registration,
        public_key_path=args.public_key_pem,
        evidence_root=args.evidence_root,
        use_real_gui=args.real_gui,
        foreground_window_title=args.foreground_window_title,
    )
    print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
