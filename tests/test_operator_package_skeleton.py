from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_OPERATOR = ROOT / "packaging" / "windows_operator"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return __import__("json").loads(_read(path))


def test_windows_operator_skeleton_files_exist():
    expected = {
        WINDOWS_OPERATOR / "README.md",
        WINDOWS_OPERATOR / "operator_launcher.ps1",
        WINDOWS_OPERATOR / "package_skeleton.ps1",
        WINDOWS_OPERATOR / "build_manifest.schema.json",
        WINDOWS_OPERATOR / "support_diagnostics_manifest.schema.json",
        ROOT / "scripts" / "operator_support_diagnostics.ps1",
        ROOT / "docs" / "v4.2_operator_package_skeleton.md",
    }

    missing = [str(path) for path in expected if not path.exists()]
    assert missing == []


def test_launcher_is_explicitly_fail_closed_skeleton():
    launcher = _read(WINDOWS_OPERATOR / "operator_launcher.ps1")

    assert "Skeleton" in launcher
    assert "not approved for external operator distribution" in launcher
    assert "Operator launcher skeleton is not wired for production execution" in launcher
    assert "Submit/Register/Payment/tax-finalizing" in launcher
    assert "compile executable job plans from Excel" in launcher
    assert "throw" in launcher.lower()


def test_package_skeleton_declares_controlled_non_release_boundaries():
    script = _read(WINDOWS_OPERATOR / "package_skeleton.ps1")

    assert "internal_skeleton_only" in script
    assert "not create an external release package" in script
    assert "does not include country pack content" in script
    assert "does not add Submit/Register/Payment/tax-finalizing automation" in script
    assert "control_plane/**" in script
    assert "control_plane/packs/**" in script
    assert "*.xlsx" in script
    assert "*.pem" in script
    assert "checksums.sha256" in script


def test_build_manifest_schema_requires_security_booleans():
    schema = _json(WINDOWS_OPERATOR / "build_manifest.schema.json")
    required = set(schema["required"])

    assert "no_finalization_actions" in required
    assert "country_pack_excluded" in required
    assert "local_compilation_disabled" in required
    assert schema["properties"]["no_finalization_actions"]["const"] is True
    assert schema["properties"]["country_pack_excluded"]["const"] is True
    assert schema["properties"]["local_compilation_disabled"]["const"] is True


def test_support_diagnostics_schema_requires_sensitive_content_exclusion():
    schema = _json(WINDOWS_OPERATOR / "support_diagnostics_manifest.schema.json")
    required = set(schema["required"])

    assert "sensitive_content_excluded" in required
    assert "evidence_file_hashes" in required
    assert schema["properties"]["sensitive_content_excluded"]["const"] is True


def test_support_diagnostics_script_hashes_evidence_without_collecting_known_secret_files():
    script = _read(ROOT / "scripts" / "operator_support_diagnostics.ps1")

    assert "evidence" in script
    assert "Get-FileHash" in script
    assert "sensitive_content_excluded = $true" in script
    assert "must not collect credentials" in script
    assert "private keys" in script
    assert "country pack content" in script
    assert "raw screenshots require separate redaction approval" in script.lower()
