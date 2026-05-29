from __future__ import annotations

import json
import zipfile

from agent.customsops_agent.evidence_bundle import EvidenceBundleCollector


def test_evidence_bundle_contains_watermark_and_hashes(tmp_path, signed_plan):
    bundle = EvidenceBundleCollector(tmp_path, "4.0.0").collect(
        signed_plan, [{"step": 1, "action": "click_paste", "status": "mocked"}]
    )
    assert bundle.exists()
    with zipfile.ZipFile(bundle) as archive:
        manifest = json.loads(archive.read("evidence_manifest.json").decode("utf-8"))
        screenshot = archive.read("screenshot_001.txt").decode("utf-8")
    assert "CUSTOMSOPS CONTROLLED EVIDENCE" in screenshot
    assert manifest["watermark"].startswith("CUSTOMSOPS CONTROLLED EVIDENCE")
    assert manifest["screenshot_source"] == "mock"
    assert "ledger.json" in manifest["hashes"]


def test_evidence_bundle_includes_real_gui_screenshot_artifact(tmp_path, signed_plan):
    screenshot_path = tmp_path / "real_gui_capture.png"
    screenshot_path.write_bytes(b"real gui screenshot bytes")

    bundle = EvidenceBundleCollector(tmp_path / "bundle_root", "4.0.0").collect(
        signed_plan,
        [
            {
                "step": 1,
                "action": "screenshot",
                "status": "executed",
                "artifact_path": str(screenshot_path),
            }
        ],
    )

    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read("evidence_manifest.json").decode("utf-8"))
        screenshot_bytes = archive.read("real_gui_capture.png")
        ledger = json.loads(archive.read("ledger.json").decode("utf-8"))

    assert "real_gui_capture.png" in names
    assert "screenshot_001.txt" not in names
    assert screenshot_bytes == b"real gui screenshot bytes"
    assert manifest["screenshot_source"] == "real_gui"
    assert "real_gui_capture.png" in manifest["hashes"]
    assert ledger[0]["artifact_path"] == str(screenshot_path)
