from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from agent.customsops_agent.machine_identity import (
    assert_machine_registration_active,
    load_machine_registration,
)
from agent.customsops_agent.operator_flow import run_operator_signed_job

SUPPORTED_MANIFEST_SUFFIXES = {".xlsx", ".xlsm"}
FORBIDDEN_FINALIZATION_ACTIONS = ["submit", "register", "payment", "tax_finalize"]
ALLOWED_EXECUTION_MODES = ["fillOnly", "safeBrakeStore"]


@dataclass(frozen=True)
class ManifestPrecheckResult:
    path: str
    suffix: str
    exists: bool
    is_file: bool
    size_bytes: int | None
    sha256: str | None
    is_supported_excel_type: bool
    zip_integrity_ok: bool | None
    workbook_xml_present: bool | None
    decision: str
    reason: str
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OperatorStatusResult:
    machine_registration_path: str
    machine_registration_loaded: bool
    machine_registration_active: bool
    tenant_id: str | None
    machine_id: str | None
    public_key_source: str | None
    public_key_available: bool
    ready_for_signed_job: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def operator_boundary() -> dict[str, Any]:
    return {
        "signed_job_only": True,
        "allowed_execution_modes": ALLOWED_EXECUTION_MODES,
        "forbidden_finalization_actions": FORBIDDEN_FINALIZATION_ACTIONS,
        "local_excel_to_executable_plan_compilation": False,
        "plan_editor": False,
        "country_pack_viewer": False,
        "production_credential_storage": False,
    }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _xlsx_container_status(path: Path) -> tuple[bool, bool, tuple[str, ...]]:
    try:
        with zipfile.ZipFile(path) as archive:
            bad_file = archive.testzip()
            names = set(archive.namelist())
    except zipfile.BadZipFile:
        return False, False, ("Excel container is not a valid ZIP-based workbook.",)

    if bad_file:
        return False, False, (f"Excel container failed CRC check: {bad_file}",)

    workbook_xml_present = "xl/workbook.xml" in names
    if not workbook_xml_present:
        return True, False, ("Excel workbook metadata xl/workbook.xml is missing.",)

    return True, True, ()


def precheck_manifest(manifest_path: Path) -> ManifestPrecheckResult:
    """Run superficial local manifest checks without parsing rows or compiling GUI steps."""

    path = manifest_path.expanduser()
    suffix = path.suffix.lower()
    exists = path.exists()
    is_file = path.is_file() if exists else False
    size_bytes = path.stat().st_size if is_file else None
    sha256 = _sha256_file(path) if is_file else None
    is_supported_excel_type = suffix in SUPPORTED_MANIFEST_SUFFIXES

    if not exists:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=False,
            is_file=False,
            size_bytes=None,
            sha256=None,
            is_supported_excel_type=is_supported_excel_type,
            zip_integrity_ok=None,
            workbook_xml_present=None,
            decision="reject",
            reason="Manifest file does not exist.",
        )

    if not is_file:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=True,
            is_file=False,
            size_bytes=None,
            sha256=None,
            is_supported_excel_type=is_supported_excel_type,
            zip_integrity_ok=None,
            workbook_xml_present=None,
            decision="reject",
            reason="Manifest path is not a file.",
        )

    if not is_supported_excel_type:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=True,
            is_file=True,
            size_bytes=size_bytes,
            sha256=sha256,
            is_supported_excel_type=False,
            zip_integrity_ok=None,
            workbook_xml_present=None,
            decision="reject",
            reason="Only .xlsx and .xlsm manifests are accepted for local precheck.",
        )

    if size_bytes == 0:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=True,
            is_file=True,
            size_bytes=size_bytes,
            sha256=sha256,
            is_supported_excel_type=True,
            zip_integrity_ok=False,
            workbook_xml_present=False,
            decision="reject",
            reason="Manifest file is empty.",
        )

    zip_integrity_ok, workbook_xml_present, warnings = _xlsx_container_status(path)
    if not zip_integrity_ok:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=True,
            is_file=True,
            size_bytes=size_bytes,
            sha256=sha256,
            is_supported_excel_type=True,
            zip_integrity_ok=False,
            workbook_xml_present=workbook_xml_present,
            decision="reject",
            reason="Manifest failed ZIP integrity precheck.",
            warnings=warnings,
        )

    if not workbook_xml_present:
        return ManifestPrecheckResult(
            path=str(path),
            suffix=suffix,
            exists=True,
            is_file=True,
            size_bytes=size_bytes,
            sha256=sha256,
            is_supported_excel_type=True,
            zip_integrity_ok=True,
            workbook_xml_present=False,
            decision="reject",
            reason="Manifest does not look like an Excel workbook.",
            warnings=warnings,
        )

    return ManifestPrecheckResult(
        path=str(path),
        suffix=suffix,
        exists=True,
        is_file=True,
        size_bytes=size_bytes,
        sha256=sha256,
        is_supported_excel_type=True,
        zip_integrity_ok=True,
        workbook_xml_present=True,
        decision="accept",
        reason="Local superficial precheck passed. HQ Control Plane must parse and compile.",
        warnings=(
            "Local precheck does not parse rows, resolve country packs, "
            "or compile executable GUI steps.",
        ),
    )


def _public_key_status(public_key_path: Path | None) -> tuple[str | None, bool, tuple[str, ...]]:
    if public_key_path is not None:
        path = public_key_path.expanduser()
        if path.is_file() and path.stat().st_size > 0:
            return str(path), True, ()
        return str(path), False, ("Trusted public key PEM file is missing or empty.",)

    public_key_pem = os.getenv("CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM", "")
    if public_key_pem.strip():
        return "CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM", True, ()
    return None, False, ("Trusted public key PEM is not configured.",)


def inspect_operator_status(
    *, machine_registration_path: Path | None = None, public_key_path: Path | None = None
) -> OperatorStatusResult:
    errors: list[str] = []
    warnings: list[str] = [
        "Execution is signed-job-only.",
        "Allowed modes are fillOnly and safeBrakeStore.",
        "This shell has no plan editor, country pack viewer, or local Excel compiler.",
    ]

    registration_path_label = (
        str(machine_registration_path) if machine_registration_path else "<default>"
    )
    machine_registration_loaded = False
    machine_registration_active = False
    tenant_id: str | None = None
    machine_id: str | None = None

    try:
        registration = load_machine_registration(machine_registration_path)
        machine_registration_loaded = True
        tenant_id = registration.tenant_id
        machine_id = registration.machine_id
        assert_machine_registration_active(registration)
        machine_registration_active = True
    except FileNotFoundError as exc:
        missing_file = exc.filename or registration_path_label
        errors.append(f"Machine registration file not found: {missing_file}")
    except ValueError as exc:
        errors.append(f"Machine registration rejected: {exc}")
    except OSError as exc:
        errors.append(f"Machine registration could not be read: {exc}")

    public_key_source, public_key_available, public_key_errors = _public_key_status(public_key_path)
    errors.extend(public_key_errors)

    ready = machine_registration_active and public_key_available
    return OperatorStatusResult(
        machine_registration_path=registration_path_label,
        machine_registration_loaded=machine_registration_loaded,
        machine_registration_active=machine_registration_active,
        tenant_id=tenant_id,
        machine_id=machine_id,
        public_key_source=public_key_source,
        public_key_available=public_key_available,
        ready_for_signed_job=ready,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def _emit_json(payload: dict[str, Any], output_json: Path | None = None) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True)
    if output_json is not None:
        output_path = output_json.expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
        return
    print(text)


def _open_evidence_location(path: Path) -> bool:
    startfile = getattr(os, "startfile", None)
    if startfile is None:
        return False
    target = path.parent if path.suffix == ".zip" else path
    startfile(str(target))
    return True


def _handle_status(args: argparse.Namespace) -> int:
    result = inspect_operator_status(
        machine_registration_path=args.machine_registration,
        public_key_path=args.public_key_pem,
    )
    _emit_json(
        {
            "status": result.to_dict(),
            "operator_boundary": operator_boundary(),
        },
        args.output_json,
    )
    return 0 if result.ready_for_signed_job else 2


def _handle_precheck_manifest(args: argparse.Namespace) -> int:
    result = precheck_manifest(args.manifest)
    _emit_json(
        {
            "manifest_precheck": result.to_dict(),
            "operator_boundary": operator_boundary(),
        },
        args.output_json,
    )
    return 0 if result.decision == "accept" else 2


def _handle_run_signed_job(args: argparse.Namespace) -> int:
    status = inspect_operator_status(
        machine_registration_path=args.machine_registration,
        public_key_path=args.public_key_pem,
    )
    if not status.ready_for_signed_job:
        _emit_json(
            {
                "result": "rejected",
                "reason": "Operator shell is not ready for signed job execution.",
                "status": status.to_dict(),
                "operator_boundary": operator_boundary(),
            },
            args.output_json,
        )
        return 2

    evidence_bundle = run_operator_signed_job(
        signed_job_plan=args.signed_job_plan,
        machine_registration_path=args.machine_registration,
        public_key_path=args.public_key_pem,
        evidence_root=args.evidence_root,
        use_real_gui=args.real_gui,
        foreground_window_title=args.foreground_window_title,
    )
    opened = _open_evidence_location(evidence_bundle) if args.open_evidence_folder else False
    _emit_json(
        {
            "result": "completed",
            "evidence_bundle": str(evidence_bundle),
            "evidence_folder_opened": opened,
            "operator_boundary": operator_boundary(),
        },
        args.output_json,
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CustomsOps controlled operator shell")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Check local operator readiness")
    status.add_argument("--machine-registration", type=Path)
    status.add_argument("--public-key-pem", type=Path)
    status.add_argument("--output-json", type=Path)
    status.set_defaults(func=_handle_status)

    precheck = subparsers.add_parser(
        "precheck-manifest", help="Run superficial local Excel manifest precheck"
    )
    precheck.add_argument("--manifest", required=True, type=Path)
    precheck.add_argument("--output-json", type=Path)
    precheck.set_defaults(func=_handle_precheck_manifest)

    run = subparsers.add_parser("run-signed-job", help="Run an HQ-issued signed job plan")
    run.add_argument("--signed-job-plan", required=True, type=Path)
    run.add_argument("--machine-registration", required=True, type=Path)
    run.add_argument("--public-key-pem", required=True, type=Path)
    run.add_argument("--evidence-root", type=Path, default=Path("evidence/operator"))
    run.add_argument("--real-gui", action="store_true")
    run.add_argument("--foreground-window-title")
    run.add_argument("--open-evidence-folder", action="store_true")
    run.add_argument("--output-json", type=Path)
    run.set_defaults(func=_handle_run_signed_job)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
