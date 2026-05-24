from __future__ import annotations

from pathlib import Path

SCRIPT_DIR = Path("scripts")


def test_windows_lab_smoke_scripts_exist():
    expected = {
        "windows_lab_smoke_runner.ps1",
        "windows_lab_smoke_prepare_env.ps1",
        "windows_lab_smoke_collect_evidence.ps1",
    }
    assert expected <= {path.name for path in SCRIPT_DIR.glob("windows_lab_smoke_*.ps1")}


def test_runner_documents_required_parameters_and_fail_closed_boundaries():
    runner = (SCRIPT_DIR / "windows_lab_smoke_runner.ps1").read_text(encoding="utf-8")
    prepare = (SCRIPT_DIR / "windows_lab_smoke_prepare_env.ps1").read_text(encoding="utf-8")

    for token in [
        "SignedJobPlan",
        "PublicKeyPem",
        "AsycudaWindowTitle",
        "EvidenceRoot",
        "CUSTOMSOPS_TENANT_ID",
        "CUSTOMSOPS_MACHINE_ID",
        "CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM",
        "fillOnly",
        "safeBrakeStore",
    ]:
        assert token in runner or token in prepare

    assert "Windows ASYCUDA lab smoke can run only on Windows" in prepare
    assert "must contain ASYCUDA" in prepare
    assert "submit" in runner
    assert "register" in runner
    assert "payment" in runner
    assert "tax_finalize" in runner


def test_runbook_contains_single_command_and_sensitive_artifact_warning():
    runbook = Path("docs/v4.1_windows_lab_smoke_operator_runbook.md").read_text(
        encoding="utf-8"
    )
    assert ".\\scripts\\windows_lab_smoke_runner.ps1" in runbook
    assert "-SignedJobPlan" in runbook
    assert "-PublicKeyPem" in runbook
    assert "-AsycudaWindowTitle" in runbook
    assert "-EvidenceRoot" in runbook
    assert "Do not commit the actual `review_bundle.zip` or screenshots" in runbook
    assert "Do not run Submit/Register/Payment/tax-finalizing automation" in runbook


def test_filled_example_is_sanitized_and_hash_only():
    example = Path(
        "docs/v4.1_windows_lab_smoke_result_template_filled.example.md"
    ).read_text(encoding="utf-8")
    assert "sanitized example" in example.lower()
    assert "review_bundle.zip` hash" in example
    assert "screenshot_001.png" in example
    assert "real customer" in example.lower()
    assert "confirmed" in example

