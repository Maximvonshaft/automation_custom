from __future__ import annotations

import json
import zipfile
from pathlib import Path

from agent.customsops_agent import operator_cli


def _write_registration(path: Path, status: str = "active") -> None:
    path.write_text(
        json.dumps(
            {
                "tenant_id": "tenant_demo",
                "machine_id": "machine_demo",
                "machine_fingerprint_sha256": "a" * 64,
                "agent_version": "4.0.0",
                "operator_package_version": "0.0.0-skeleton",
                "registration_status": status,
                "registered_at_utc": "2026-05-28T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )


def _write_minimal_xlsx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types />")
        archive.writestr("xl/workbook.xml", "<workbook />")


def test_operator_boundary_disables_local_compilation_and_sensitive_views():
    boundary = operator_cli.operator_boundary()

    assert boundary["signed_job_only"] is True
    assert boundary["local_excel_to_executable_plan_compilation"] is False
    assert boundary["plan_editor"] is False
    assert boundary["country_pack_viewer"] is False
    assert boundary["production_credential_storage"] is False
    assert set(boundary["allowed_execution_modes"]) == {"fillOnly", "safeBrakeStore"}
    assert {"submit", "register", "payment", "tax_finalize"} <= set(
        boundary["forbidden_finalization_actions"]
    )


def test_manifest_precheck_rejects_unsupported_file_type(tmp_path: Path):
    manifest = tmp_path / "manifest.csv"
    manifest.write_text("awb,hs\n", encoding="utf-8")

    result = operator_cli.precheck_manifest(manifest)

    assert result.decision == "reject"
    assert result.is_supported_excel_type is False
    assert result.sha256 is not None
    assert result.zip_integrity_ok is None


def test_manifest_precheck_accepts_valid_excel_container_without_parsing_rows(tmp_path: Path):
    manifest = tmp_path / "manifest.xlsx"
    _write_minimal_xlsx(manifest)

    result = operator_cli.precheck_manifest(manifest)

    assert result.decision == "accept"
    assert result.is_supported_excel_type is True
    assert result.zip_integrity_ok is True
    assert result.workbook_xml_present is True
    assert result.sha256 is not None
    assert "does not parse rows" in " ".join(result.warnings)


def test_manifest_precheck_rejects_corrupt_excel_container(tmp_path: Path):
    manifest = tmp_path / "manifest.xlsx"
    manifest.write_text("not a zip workbook", encoding="utf-8")

    result = operator_cli.precheck_manifest(manifest)

    assert result.decision == "reject"
    assert result.zip_integrity_ok is False
    assert result.workbook_xml_present is False


def test_operator_status_ready_when_registration_active_and_public_key_file_present(tmp_path: Path):
    registration_path = tmp_path / "machine_registration.json"
    public_key_path = tmp_path / "trusted_public_key.pem"
    _write_registration(registration_path, "active")
    public_key_path.write_text("-----BEGIN PUBLIC KEY-----\nplaceholder\n-----END PUBLIC KEY-----\n", encoding="ascii")

    result = operator_cli.inspect_operator_status(
        machine_registration_path=registration_path,
        public_key_path=public_key_path,
    )

    assert result.machine_registration_loaded is True
    assert result.machine_registration_active is True
    assert result.public_key_available is True
    assert result.ready_for_signed_job is True
    assert result.errors == ()


def test_operator_status_fails_closed_for_pending_registration(tmp_path: Path):
    registration_path = tmp_path / "machine_registration.json"
    public_key_path = tmp_path / "trusted_public_key.pem"
    _write_registration(registration_path, "pending")
    public_key_path.write_text("-----BEGIN PUBLIC KEY-----\nplaceholder\n-----END PUBLIC KEY-----\n", encoding="ascii")

    result = operator_cli.inspect_operator_status(
        machine_registration_path=registration_path,
        public_key_path=public_key_path,
    )

    assert result.machine_registration_loaded is True
    assert result.machine_registration_active is False
    assert result.public_key_available is True
    assert result.ready_for_signed_job is False
    assert any("not active" in error for error in result.errors)


def test_cli_status_returns_nonzero_when_not_ready(tmp_path: Path):
    registration_path = tmp_path / "machine_registration.json"
    output_path = tmp_path / "status.json"
    _write_registration(registration_path, "revoked")

    exit_code = operator_cli.main(
        [
            "status",
            "--machine-registration",
            str(registration_path),
            "--public-key-pem",
            str(tmp_path / "missing.pem"),
            "--output-json",
            str(output_path),
        ]
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 2
    assert payload["status"]["ready_for_signed_job"] is False
    assert payload["operator_boundary"]["signed_job_only"] is True
