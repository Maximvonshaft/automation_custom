# ruff: noqa: I001
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from agent.customsops_agent import evidence_reference, operator_cli


SCREENSHOT_CONTENT = "customer-visible screenshot placeholder"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_evidence_bundle(path: Path) -> dict:
    screenshot_hash = _sha256_text(SCREENSHOT_CONTENT)
    ledger = json.dumps([{"step": 1, "action": "screenshot"}], sort_keys=True)
    ledger_hash = _sha256_text(ledger)
    manifest = {
        "tenant_id": "tenant_demo",
        "machine_id": "machine_demo",
        "job_id": "job_demo",
        "run_id": "run_demo",
        "pack_id": "albania_asycuda_internal_lab",
        "pack_version": "4.1-lab",
        "mode": "safeBrakeStore",
        "agent_version": "4.0.0",
        "files": ["screenshot_001.txt", "ledger.json"],
        "hashes": {
            "screenshot_001.txt": screenshot_hash,
            "ledger.json": ledger_hash,
        },
        "watermark": "tenant_demo|machine_demo|job_demo|run_demo",
    }
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("screenshot_001.txt", SCREENSHOT_CONTENT)
        archive.writestr("ledger.json", ledger)
        archive.writestr("evidence_manifest.json", json.dumps(manifest, sort_keys=True))
    return manifest


def test_build_evidence_reference_is_reference_only(tmp_path: Path):
    bundle = tmp_path / "evidence.zip"
    manifest = _write_evidence_bundle(bundle)

    reference = evidence_reference.build_evidence_reference(bundle)
    serialized = json.dumps(reference, sort_keys=True)

    assert reference["schema_version"] == evidence_reference.EVIDENCE_REFERENCE_SCHEMA_VERSION
    assert reference["reference_type"] == "local_evidence_bundle_reference"
    assert reference["run_context"]["tenant_id"] == manifest["tenant_id"]
    assert reference["run_context"]["machine_id"] == manifest["machine_id"]
    assert reference["run_context"]["job_id"] == manifest["job_id"]
    assert reference["run_context"]["mode"] == "safeBrakeStore"
    assert reference["evidence_bundle"]["content_included"] is False
    assert reference["evidence_manifest"]["content_included"] is False
    assert reference["policy"]["reference_only"] is True
    assert reference["policy"]["raw_artifacts_uploaded"] is False
    assert reference["policy"]["screenshot_content_included"] is False
    assert reference["policy"]["requires_hq_review"] is True
    assert SCREENSHOT_CONTENT not in serialized


def test_screenshot_artifacts_are_hash_references_only(tmp_path: Path):
    bundle = tmp_path / "evidence.zip"
    _write_evidence_bundle(bundle)

    reference = evidence_reference.build_evidence_reference(bundle)
    screenshots = reference["screenshot_artifacts"]

    assert len(screenshots) == 1
    assert screenshots[0]["file_name"] == "screenshot_001.txt"
    assert screenshots[0]["content_included"] is False
    assert screenshots[0]["redaction_required_before_upload"] is True
    assert screenshots[0]["sha256"] == _sha256_text(SCREENSHOT_CONTENT)


def test_support_diagnostics_are_referenced_by_hash_only(tmp_path: Path):
    bundle = tmp_path / "evidence.zip"
    diagnostics = tmp_path / "support_diagnostics_manifest.json"
    _write_evidence_bundle(bundle)
    diagnostics.write_text(
        json.dumps({"sensitive_content_excluded": True}, sort_keys=True),
        encoding="utf-8",
    )

    reference = evidence_reference.build_evidence_reference(
        bundle,
        support_diagnostics_manifest_path=diagnostics,
    )

    assert reference["support_diagnostics"]["available"] is True
    assert reference["support_diagnostics"]["content_included"] is False
    assert reference["support_diagnostics"]["file_name"] == diagnostics.name
    assert reference["support_diagnostics"]["sha256"] is not None
    assert "sensitive_content_excluded" not in json.dumps(reference)


def test_missing_evidence_manifest_fails_closed(tmp_path: Path):
    bundle = tmp_path / "broken.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        archive.writestr("ledger.json", "[]")

    with pytest.raises(ValueError, match="missing evidence_manifest"):
        evidence_reference.build_evidence_reference(bundle)


def test_write_evidence_reference_creates_stable_json_file(tmp_path: Path):
    bundle = tmp_path / "evidence.zip"
    output = tmp_path / "reference" / "evidence_reference.json"
    _write_evidence_bundle(bundle)

    result_path = evidence_reference.write_evidence_reference(bundle, output)
    payload = json.loads(result_path.read_text(encoding="utf-8"))

    assert result_path == output
    assert payload["evidence_reference_id"].startswith("evref_")
    assert len(payload["evidence_reference_sha256"]) == 64
    assert payload["evidence_bundle"]["sha256"] is not None


def test_operator_cli_reference_evidence_command(tmp_path: Path):
    bundle = tmp_path / "evidence.zip"
    output = tmp_path / "evidence_reference.json"
    _write_evidence_bundle(bundle)

    exit_code = operator_cli.main(
        [
            "reference-evidence",
            "--evidence-bundle",
            str(bundle),
            "--output-json",
            str(output),
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert payload["policy"]["reference_only"] is True
    assert payload["evidence_bundle"]["content_included"] is False


def test_schema_declares_reference_only_policy():
    schema_path = Path("shared/schemas/evidence_reference.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    policy = schema["properties"]["policy"]["properties"]

    assert policy["reference_only"]["const"] is True
    assert policy["raw_artifacts_uploaded"]["const"] is False
    assert policy["screenshot_content_included"]["const"] is False
