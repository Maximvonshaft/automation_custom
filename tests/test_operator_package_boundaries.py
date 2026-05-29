from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "packaging" / "operator_package_manifest.json"


def _manifest() -> dict:
    import json

    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_operator_package_manifest_exists_and_is_not_release_package():
    manifest = _manifest()

    assert manifest["package_name"] == "customsops-controlled-operator-package"
    assert manifest["status"] == "boundary_manifest_only_not_a_release_package"
    assert manifest["milestone"] == "v4.2-milestone-7-controlled-pilot-gate"


def test_operator_package_manifest_keeps_country_pack_server_only():
    rules = _manifest()["classification_rules"]

    server_only = rules["server_only"]
    candidates = rules["operator_local_candidate"]

    assert "control_plane/**" in server_only
    assert "control_plane/packs/**" in server_only
    assert not any(path.startswith("control_plane/") for path in candidates)
    assert not any("packs" in path.lower() for path in candidates)


def test_operator_package_manifest_classifies_operator_cli_as_local_candidate():
    candidates = set(_manifest()["classification_rules"]["operator_local_candidate"])
    docs = set(_manifest()["classification_rules"]["docs_only_internal"])

    assert "agent/customsops_agent/operator_cli.py" in candidates
    assert "docs/v4.2_operator_ux_shell.md" in docs


def test_operator_package_manifest_classifies_evidence_reference_model():
    candidates = set(_manifest()["classification_rules"]["operator_local_candidate"])
    docs = set(_manifest()["classification_rules"]["docs_only_internal"])

    assert "agent/customsops_agent/evidence_reference.py" in candidates
    assert "shared/schemas/evidence_reference.schema.json" in candidates
    assert "docs/v4.2_evidence_reference_model.md" in docs


def test_operator_package_manifest_classifies_controlled_pilot_gate():
    candidates = set(_manifest()["classification_rules"]["operator_local_candidate"])
    docs = set(_manifest()["classification_rules"]["docs_only_internal"])

    assert "shared/schemas/pilot_gate_record.schema.json" in candidates
    assert "packaging/windows_operator/pilot_gate_record.ps1" in candidates
    assert "packaging/windows_operator/operator_allowlist.example.json" in candidates
    assert "packaging/windows_operator/machine_allowlist.example.json" in candidates
    assert "docs/v4.2_controlled_pilot_gate.md" in docs
    assert "docs/v4.2_operator_package_note_template.md" in docs
    assert "docs/v4.2_pilot_rollback_disable.md" in docs


def test_operator_package_manifest_excludes_sensitive_artifact_patterns():
    excluded = set(_manifest()["classification_rules"]["excluded"])

    required_exclusions = {
        "outputs/**",
        "lab/**",
        "*.zip",
        "*.xlsx",
        "*.xls",
        "*.xlsm",
        "*.pem",
        "*.key",
        "*.p12",
        "*.pfx",
        "*.env",
        "*.log",
    }

    assert required_exclusions <= excluded


def test_operator_package_manifest_declares_forbidden_runtime_actions():
    manifest = _manifest()

    assert set(manifest["allowed_modes"]) == {"fillOnly", "safeBrakeStore"}
    assert {"submit", "register", "payment", "tax_finalize"} <= set(
        manifest["forbidden_actions"]
    )


def test_operator_package_manifest_marks_server_compilers_forbidden():
    forbidden = "\n".join(_manifest()["forbidden_in_operator_package"]).lower()

    assert "declaration_job_compiler.py" in forbidden
    assert "job_compiler.py" in forbidden
    assert "field_map.example.yaml" in forbidden
    assert "safebrake_policy.example.yaml" in forbidden
    assert "signing private key" in forbidden
    assert "production credentials" in forbidden


def test_operator_ux_shell_declares_no_local_compiler_or_sensitive_views():
    ux = _manifest()["operator_ux_shell"]

    assert ux["status_command"] is True
    assert ux["manifest_superficial_precheck"] is True
    assert ux["run_signed_job_command"] is True
    assert ux["plan_editor"] is False
    assert ux["country_pack_viewer"] is False
    assert ux["local_excel_to_executable_plan_compilation"] is False


def test_evidence_reference_model_declares_reference_only_policy():
    evidence_reference = _manifest()["evidence_reference_model"]

    assert evidence_reference["reference_only"] is True
    assert evidence_reference["raw_artifacts_uploaded"] is False
    assert evidence_reference["screenshot_content_included"] is False
    assert evidence_reference["support_diagnostics_content_included"] is False
    assert evidence_reference["requires_hq_review"] is True


def test_controlled_pilot_gate_declares_record_only_policy():
    gate = _manifest()["controlled_pilot_gate"]

    assert gate["gate_record_only"] is True
    assert gate["requires_operator_allowlist"] is True
    assert gate["requires_machine_allowlist"] is True
    assert gate["requires_build_manifest"] is True
    assert gate["requires_checksum_file"] is True
    assert gate["external_distribution_approved"] is False
