from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

EVIDENCE_REFERENCE_SCHEMA_VERSION = "1.0"
EVIDENCE_MANIFEST_NAME = "evidence_manifest.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _load_manifest_from_bundle(evidence_bundle_path: Path) -> tuple[dict[str, Any], str, list[str]]:
    if not evidence_bundle_path.is_file():
        raise ValueError(f"Evidence bundle does not exist: {evidence_bundle_path}")

    try:
        with zipfile.ZipFile(evidence_bundle_path) as archive:
            bad_file = archive.testzip()
            if bad_file:
                raise ValueError(f"Evidence bundle failed CRC check: {bad_file}")
            names = sorted(archive.namelist())
            if EVIDENCE_MANIFEST_NAME not in names:
                raise ValueError("Evidence bundle is missing evidence_manifest.json")
            manifest_bytes = archive.read(EVIDENCE_MANIFEST_NAME)
    except zipfile.BadZipFile as exc:
        raise ValueError("Evidence bundle is not a valid ZIP file") from exc

    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Evidence manifest is not valid JSON") from exc

    return manifest, _sha256_bytes(manifest_bytes), names


def _support_diagnostics_reference(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {
            "available": False,
            "content_included": False,
            "file_name": None,
            "sha256": None,
        }
    if not path.is_file():
        raise ValueError(f"Support diagnostics manifest does not exist: {path}")
    return {
        "available": True,
        "content_included": False,
        "file_name": path.name,
        "sha256": _sha256_file(path),
    }


def _screenshot_references(artifact_hashes: dict[str, str]) -> list[dict[str, Any]]:
    screenshots: list[dict[str, Any]] = []
    for file_name, sha256 in sorted(artifact_hashes.items()):
        if "screenshot" not in file_name.lower():
            continue
        screenshots.append(
            {
                "file_name": file_name,
                "sha256": sha256,
                "content_included": False,
                "redaction_required_before_upload": True,
            }
        )
    return screenshots


def build_evidence_reference(
    evidence_bundle_path: Path,
    *,
    support_diagnostics_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Create a reference-only evidence record from a local evidence ZIP.

    The returned payload contains hashes and run metadata only. It does not upload or embed raw
    screenshots, ledgers, manifests, or diagnostic content.
    """

    bundle_path = evidence_bundle_path.expanduser()
    manifest, manifest_sha256, bundle_entries = _load_manifest_from_bundle(bundle_path)
    artifact_hashes = dict(sorted((manifest.get("hashes") or {}).items()))

    reference: dict[str, Any] = {
        "schema_version": EVIDENCE_REFERENCE_SCHEMA_VERSION,
        "reference_type": "local_evidence_bundle_reference",
        "run_context": {
            "tenant_id": manifest.get("tenant_id"),
            "machine_id": manifest.get("machine_id"),
            "job_id": manifest.get("job_id"),
            "run_id": manifest.get("run_id"),
            "mode": manifest.get("mode"),
            "pack_id": manifest.get("pack_id"),
            "pack_version": manifest.get("pack_version"),
            "agent_version": manifest.get("agent_version"),
        },
        "evidence_bundle": {
            "file_name": bundle_path.name,
            "size_bytes": bundle_path.stat().st_size,
            "sha256": _sha256_file(bundle_path),
            "content_included": False,
        },
        "evidence_manifest": {
            "file_name": EVIDENCE_MANIFEST_NAME,
            "sha256": manifest_sha256,
            "content_included": False,
        },
        "artifact_hashes": artifact_hashes,
        "bundle_entries": bundle_entries,
        "screenshot_artifacts": _screenshot_references(artifact_hashes),
        "support_diagnostics": _support_diagnostics_reference(
            support_diagnostics_manifest_path.expanduser()
            if support_diagnostics_manifest_path is not None
            else None
        ),
        "policy": {
            "reference_only": True,
            "raw_artifacts_uploaded": False,
            "screenshot_content_included": False,
            "requires_hq_review": True,
        },
    }

    identity_material = {
        "bundle_sha256": reference["evidence_bundle"]["sha256"],
        "manifest_sha256": reference["evidence_manifest"]["sha256"],
        "run_context": reference["run_context"],
    }
    reference["evidence_reference_id"] = "evref_" + _sha256_bytes(
        _canonical_bytes(identity_material)
    )[:24]
    reference_hash_material = dict(reference)
    reference["evidence_reference_sha256"] = _sha256_bytes(
        _canonical_bytes(reference_hash_material)
    )
    return reference


def write_evidence_reference(
    evidence_bundle_path: Path,
    output_path: Path,
    *,
    support_diagnostics_manifest_path: Path | None = None,
) -> Path:
    reference = build_evidence_reference(
        evidence_bundle_path,
        support_diagnostics_manifest_path=support_diagnostics_manifest_path,
    )
    output = output_path.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(reference, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output
