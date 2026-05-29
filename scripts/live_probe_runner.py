from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from agent.customsops_agent.evidence_reference import write_evidence_reference
from agent.customsops_agent.machine_identity import machine_fingerprint_sha256
from agent.customsops_agent.operator_flow import run_operator_signed_job
from control_plane.app.services.job_signer import JobSigner
from shared.signing.ed25519 import generate_private_key, private_key_to_pem, public_key_to_pem


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _utc_expiry(hours: int = 2) -> str:
    return (
        datetime.now(UTC)
        + timedelta(hours=hours)
    ).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _registration() -> dict[str, Any]:
    return {
        "tenant_id": "tenant_demo",
        "machine_id": "machine_demo",
        "machine_fingerprint_sha256": machine_fingerprint_sha256(),
        "agent_version": "4.0.0",
        "operator_package_version": "0.0.0-live-probe-script",
        "registration_status": "active",
        "registered_at_utc": _utc_now(),
        "public_key_id": "local-demo-key",
    }


def _base_plan(job_id: str, pack_id: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "tenant_id": "tenant_demo",
        "machine_id": "machine_demo",
        "mode": "fillOnly",
        "pack_id": pack_id,
        "pack_version": "v4.3-live-probe",
        "issued_at": _utc_now(),
        "expires_at": _utc_expiry(),
        "steps": steps,
    }


def _foreground_steps() -> list[dict[str, Any]]:
    return [
        {"step": 1, "action": "wait", "duration_seconds": 0.1, "label": "foreground wait"},
        {"step": 2, "action": "screenshot", "label": "foreground screenshot"},
    ]


def _click_paste_steps(x: int, y: int, value: str) -> list[dict[str, Any]]:
    return [
        {"step": 1, "action": "wait", "duration_seconds": 0.3, "label": "prepared page"},
        {
            "step": 2,
            "action": "click_paste",
            "field_key": "coordinate_safe_test_field",
            "x": x,
            "y": y,
            "value": value,
            "label": "click safe field and paste sanitized value",
        },
        {"step": 3, "action": "screenshot", "label": "click paste screenshot"},
    ]


def _tab_chain_steps(x: int, y: int, count: int) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = [
        {"step": 1, "action": "wait", "duration_seconds": 0.3, "label": "prepared tab page"},
        {
            "step": 2,
            "action": "click_paste",
            "field_key": "tab_chain_field_1",
            "x": x,
            "y": y,
            "value": "TC_FIELD_01_DO_NOT_SUBMIT",
            "label": "click field 1 and paste",
        },
    ]
    next_step = 3
    for index in range(2, count + 1):
        steps.append({"step": next_step, "action": "hotkey", "keys": ["tab"], "label": f"tab to field {index}"})
        next_step += 1
        steps.append(
            {
                "step": next_step,
                "action": "paste",
                "field_key": f"tab_chain_field_{index}",
                "value": f"TC_FIELD_{index:02d}_DO_NOT_SUBMIT",
                "label": f"paste field {index}",
            }
        )
        next_step += 1
    steps.append({"step": next_step, "action": "screenshot", "label": "tab chain screenshot"})
    return steps


def _build_plan(args: argparse.Namespace) -> dict[str, Any]:
    if args.probe == "foreground":
        return _base_plan(
            "job_v43_live_foreground_probe",
            "live_foreground_probe_no_field_write",
            _foreground_steps(),
        )
    if args.probe == "click-paste":
        return _base_plan(
            "job_v43_guarded_click_paste_probe",
            "guarded_click_paste_probe_no_save",
            _click_paste_steps(args.x, args.y, args.value),
        )
    if args.probe == "tab-chain":
        return _base_plan(
            "job_v43_guarded_tab_chain_probe",
            "guarded_tab_chain_probe_no_save",
            _tab_chain_steps(args.x, args.y, args.count),
        )
    raise ValueError(f"Unsupported probe: {args.probe}")


def run(args: argparse.Namespace) -> int:
    run_root = args.run_root.expanduser()
    run_root.mkdir(parents=True, exist_ok=True)
    machine_registration = run_root / "machine_registration.json"
    public_key_pem = run_root / "trusted_public_key.pem"
    private_key_pem = run_root / "demo_private_key_DO_NOT_USE_IN_PROD.pem"
    signed_job_plan = run_root / f"signed_job_plan_{args.probe}.json"
    run_result = run_root / f"run_result_{args.probe}.json"
    evidence_reference = run_root / "evidence_reference.json"

    private_key = generate_private_key()
    public_key = private_key.public_key()
    private_key_pem.write_text(private_key_to_pem(private_key), encoding="ascii")
    public_key_pem.write_text(public_key_to_pem(public_key), encoding="ascii")
    _write_json(machine_registration, _registration())

    plan = _build_plan(args)
    signed = JobSigner(private_key).sign(plan)
    _write_json(signed_job_plan, signed)

    try:
        evidence_bundle = run_operator_signed_job(
            signed_job_plan=signed_job_plan,
            machine_registration_path=machine_registration,
            public_key_path=public_key_pem,
            evidence_root=run_root / "evidence",
            use_real_gui=True,
            foreground_window_title=args.foreground_window_title,
        )
        _write_json(
            run_result,
            {
                "result": "completed",
                "probe": args.probe,
                "evidence_bundle": str(evidence_bundle),
            },
        )
        write_evidence_reference(evidence_bundle, evidence_reference)
    except Exception as exc:
        _write_json(
            run_result,
            {
                "result": "failed",
                "probe": args.probe,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
            },
        )
        raise

    print(json.dumps({"result": "completed", "run_root": str(run_root), "evidence_reference": str(evidence_reference)}, indent=2))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run controlled ASYCUDA live probes")
    parser.add_argument("--probe", choices=["foreground", "click-paste", "tab-chain"], required=True)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--foreground-window-title", default="ASYCUDAWorld")
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--value", default="SANITIZED_CLICK_PASTE_DO_NOT_SUBMIT")
    return parser


def main() -> int:
    return run(_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
