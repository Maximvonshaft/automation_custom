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
    assert "ledger.json" in manifest["hashes"]

