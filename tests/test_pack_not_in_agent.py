from __future__ import annotations

from pathlib import Path

FORBIDDEN_PACK_FILE_STEMS = {
    "field_map",
    "coordinate_map",
    "business_mapping",
    "dropdown_rules",
    "safebrake_policy",
    "error_map",
}
FORBIDDEN_PACK_SUFFIXES = {".yaml", ".yml", ".json"}
FORBIDDEN_AGENT_CONTENT = {
    "albania_asycuda",
    "asycuda field coordinates",
    "dropdown resolver",
    "business mapping",
    "kodi i monedhes se fatures",
    "currency code intentionally omitted",
    "blocked_success_reason",
}


def test_agent_does_not_contain_packs_directory():
    forbidden_dirs = [
        path for path in Path("agent").rglob("*") if path.is_dir() and path.name == "packs"
    ]
    assert forbidden_dirs == []


def test_agent_does_not_contain_country_pack_rule_files():
    forbidden_files = []
    for path in Path("agent").rglob("*"):
        if not path.is_file() or path.suffix.lower() not in FORBIDDEN_PACK_SUFFIXES:
            continue
        stem = path.stem.lower()
        if any(rule_name in stem for rule_name in FORBIDDEN_PACK_FILE_STEMS):
            forbidden_files.append(path.as_posix())

    assert forbidden_files == []


def test_agent_does_not_contain_country_pack_rule_content():
    offending_files = []
    for path in Path("agent").rglob("*"):
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        if any(marker in content for marker in FORBIDDEN_AGENT_CONTENT):
            offending_files.append(path.as_posix())

    assert offending_files == []


def test_control_plane_packs_remain_server_side_only():
    assert Path("control_plane/packs").is_dir()
    assert not Path("agent/packs").exists()
