from __future__ import annotations

from pathlib import Path


def test_agent_does_not_contain_country_pack_files():
    agent_files = [path.name for path in Path("agent").rglob("*") if path.is_file()]
    assert "field_map.example.yaml" not in agent_files
    assert "safebrake_policy.example.yaml" not in agent_files

