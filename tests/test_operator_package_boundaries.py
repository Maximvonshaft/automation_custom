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
    assert manifest["milestone"] == "v4.2-milestone-1-packaging-boundary-audit"


def test_operator_package_manifest_keeps_country_pack_server_only():
    rules = _manifest()["classification_rules"]

    server_only = rules["server_only"]
    candidates = rules["operator_local_candidate"]

    assert "control_plane/**" in server_only
    assert "control_plane/packs/**" in server_only
    assert not any(path.startswith("control_plane/") for path in candidates)
    assert not any("packs" in path.lower() for path in candidates)


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
