from __future__ import annotations

from pathlib import Path

from agent.customsops_agent.intake import precheck_manifest_file


def test_agent_manifest_intake_hashes_but_cannot_compile_executable_plan(tmp_path):
    manifest_path = tmp_path / "sanitized.xlsx"
    manifest_path.write_bytes(b"sanitized workbook bytes")
    result = precheck_manifest_file(manifest_path)
    assert result["filename"] == "sanitized.xlsx"
    assert result["sha256"]
    assert result["can_compile_executable_plan"] is False


def test_agent_has_no_manifest_compiler_module():
    agent_files = {path.name for path in Path("agent/customsops_agent").rglob("*.py")}
    assert "manifest_compiler.py" not in agent_files
    assert "job_compiler.py" not in agent_files

