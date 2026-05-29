from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_OPERATOR = ROOT / "packaging" / "windows_operator"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_read(path))


def test_pilot_gate_record_schema_enforces_control_boundaries():
    schema = _json(ROOT / "shared" / "schemas" / "pilot_gate_record.schema.json")
    boundary = schema["properties"]["boundary"]["properties"]

    assert boundary["source_tree_distributed"]["const"] is False
    assert boundary["country_pack_included"]["const"] is False
    assert boundary["local_compilation_enabled"]["const"] is False
    assert boundary["external_distribution_approved"]["const"] is False
    assert boundary["raw_sensitive_evidence_included"]["const"] is False


def test_pilot_gate_script_writes_record_only_and_checks_manifest_boundaries():
    script = _read(WINDOWS_OPERATOR / "pilot_gate_record.ps1")

    assert "Controlled Pilot Gate Record" in script
    assert "writes a gate record only" in script
    assert "does not create an external package" in script
    assert "does not move country pack content" in script
    assert "does not enable local Excel compilation" in script
    assert "BUILD_MANIFEST.json" in script
    assert "checksums.sha256" in script
    assert "no_finalization_actions" in script
    assert "country_pack_excluded" in script
    assert "local_compilation_disabled" in script
    assert "PILOT_GATE_RECORD.json" in script


def test_operator_and_machine_allowlist_examples_default_to_not_approved():
    operator_allowlist = _json(WINDOWS_OPERATOR / "operator_allowlist.example.json")
    machine_allowlist = _json(WINDOWS_OPERATOR / "machine_allowlist.example.json")

    assert operator_allowlist["operators"][0]["approved"] is False
    assert machine_allowlist["machines"][0]["approved"] is False
    assert operator_allowlist["operators"][0]["operator_id"] == "operator_demo_001"
    assert machine_allowlist["machines"][0]["operator_id"] == "operator_demo_001"


def test_controlled_pilot_gate_docs_state_non_approval_and_required_controls():
    doc = _read(ROOT / "docs" / "v4.2_controlled_pilot_gate.md")

    assert "not a production approval" in doc
    assert "not an external rollout approval" in doc
    assert "operator allowlist" in doc
    assert "machine allowlist" in doc
    assert "PILOT_GATE_RECORD.json" in doc
    assert "source_tree_distributed" in doc
    assert "country_pack_included" in doc
    assert "local_compilation_enabled" in doc
    assert "external_distribution_approved" in doc


def test_operator_package_note_template_requires_empty_fields_to_block_pilot_use():
    doc = _read(ROOT / "docs" / "v4.2_operator_package_note_template.md")

    assert "does not approve external distribution" in doc
    assert "Approved operator IDs" in doc
    assert "Approved machine IDs" in doc
    assert "An empty approval field means" in doc
    assert "not approved for pilot use" in doc


def test_pilot_rollback_disable_runbook_blocks_shortcuts():
    doc = _read(ROOT / "docs" / "v4.2_pilot_rollback_disable.md")

    assert "Stop issuing new signed job plans" in doc
    assert "disabled" in doc
    assert "revoked" in doc
    assert "Remove the machine from the pilot machine allowlist" in doc
    assert "Do not" in doc
    assert "ship source trees as a quick patch" in doc
    assert "copy country pack content to local machines" in doc
    assert "bypass machine binding" in doc
