from __future__ import annotations

import json
import zipfile

from agent.customsops_agent.evidence_v311_adapter import write_v311_review_bundle


def test_v311_review_bundle_contains_required_artifacts(tmp_path):
    job_plan = {
        "tenant_id": "tenant_demo",
        "machine_id": "machine_demo",
        "job_id": "job_demo",
        "mode": "safeBrakeStore",
        "pack_id": "albania_asycuda",
        "pack_version": "4.0.0-example",
    }
    bundle = write_v311_review_bundle(
        root=tmp_path,
        job_plan=job_plan,
        parse_report={"accepted": True, "template_type": "Combine", "errors": [], "warnings": []},
        declaration_model={"declaration_id": "decl_demo", "items": []},
        ledger_entries=[{"step": 1, "action": "click_paste", "status": "executed"}],
        watermark="CUSTOMSOPS CONTROLLED EVIDENCE | sanitized",
    )
    assert bundle.name == "review_bundle.zip"
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
        metadata = json.loads(archive.read("watermark_metadata.json").decode("utf-8"))
    assert "ledger.jsonl" in names
    assert "run_context.json" in names
    assert "manifest_parse_report.json" in names
    assert "declaration_model.json" in names
    assert "signed_job_plan.json" in names
    assert "screenshots/screenshot_001.txt" in names
    assert metadata["watermark"].startswith("CUSTOMSOPS CONTROLLED EVIDENCE")
