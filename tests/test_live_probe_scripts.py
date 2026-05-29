from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_live_probe_scripts_exist():
    expected = {
        SCRIPTS / "live_probe_runner.py",
        SCRIPTS / "live_probe_foreground.ps1",
        SCRIPTS / "live_probe_click_paste.ps1",
        SCRIPTS / "live_probe_tab_chain.ps1",
    }

    assert [path for path in expected if not path.exists()] == []


def test_live_probe_runner_keeps_probe_actions_non_finalizing():
    script = _read(SCRIPTS / "live_probe_runner.py")

    assert "click_paste" in script
    assert "hotkey" in script
    assert "screenshot" in script
    assert "fillOnly" in script
    assert "reference-evidence" not in script
    assert "payment" not in script
    assert "tax_finalize" not in script
    assert "backend_request" not in script


def test_live_probe_runner_uses_runtime_machine_fingerprint():
    script = _read(SCRIPTS / "live_probe_runner.py")

    assert "machine_fingerprint_sha256()" in script
    assert "machine_registration.json" in script
    assert "run_operator_signed_job" in script
    assert "write_evidence_reference" in script


def test_click_paste_and_tab_chain_wrappers_require_coordinates():
    click_paste = _read(SCRIPTS / "live_probe_click_paste.ps1")
    tab_chain = _read(SCRIPTS / "live_probe_tab_chain.ps1")

    assert "[Parameter(Mandatory = $true)]" in click_paste
    assert "[Parameter(Mandatory = $true)]" in tab_chain
    assert "--x $X" in click_paste
    assert "--y $Y" in click_paste
    assert "--x $X" in tab_chain
    assert "--y $Y" in tab_chain


def test_live_probe_wrappers_use_focus_delay_before_running():
    for script_name in [
        "live_probe_foreground.ps1",
        "live_probe_click_paste.ps1",
        "live_probe_tab_chain.ps1",
    ]:
        script = _read(SCRIPTS / script_name)
        assert "FocusDelaySeconds" in script
        assert "Start-Sleep -Seconds $FocusDelaySeconds" in script
        assert "scripts\\live_probe_runner.py" in script
