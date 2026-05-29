from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from control_plane.app.services.albania_excel_template_parser import (
    TemplateDefaults,
    parse_broker_excel_template,
)
from control_plane.app.services.albania_line_transaction_compiler import build_unsigned_job_plan


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@dataclass(frozen=True)
class BatchCompileOptions:
    tenant_id: str
    machine_id: str
    job_prefix: str = "job_albania_template"
    include_store_safebrake: bool = False
    defaults: TemplateDefaults = TemplateDefaults()


@dataclass(frozen=True)
class CompiledBatch:
    manifest_path: Path
    plan_paths: tuple[Path, ...]
    group_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_path": str(self.manifest_path),
            "plan_paths": [str(path) for path in self.plan_paths],
            "group_count": self.group_count,
        }


def _plan_file_name(index: int, group_id: str) -> str:
    safe_group_id = "".join(
        char if char.isalnum() or char in {"-", "_"} else "_"
        for char in group_id
    )
    return f"{index:03d}_{safe_group_id}.json"


def compile_broker_excel_batch(
    excel_path: Path,
    output_dir: Path,
    *,
    options: BatchCompileOptions,
) -> CompiledBatch:
    if not options.defaults.authorization_reference:
        raise ValueError("authorization_reference is required for batch compilation.")
    if not options.defaults.truck_registration_plate_number:
        raise ValueError("truck_registration_plate_number is required for batch compilation.")

    parse_result = parse_broker_excel_template(excel_path, defaults=options.defaults)
    out_dir = output_dir.expanduser()
    plans_dir = out_dir / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, Any]] = []
    plan_paths: list[Path] = []
    for group in parse_result.groups:
        job_id = f"{options.job_prefix}_{group.group_index:03d}_{group.group_id}"
        plan = build_unsigned_job_plan(
            group.declaration,
            tenant_id=options.tenant_id,
            machine_id=options.machine_id,
            job_id=job_id,
            include_store_safebrake=options.include_store_safebrake,
        )
        plan_path = plans_dir / _plan_file_name(group.group_index, group.group_id)
        _write_json(plan_path, plan)
        plan_paths.append(plan_path)

        entries.append(
            {
                "group_id": group.group_id,
                "group_index": group.group_index,
                "source_rows": [group.start_row, group.end_row],
                "item_count": group.item_count,
                "recipient_name": group.recipient_name,
                "document_reference": group.document_reference,
                "document_references": list(group.document_references),
                "customs_tariff_1": group.customs_tariff_1,
                "statistical_quantity": group.statistical_quantity,
                "invoice_value": group.invoice_value,
                "total_weight": group.total_weight,
                "currency_intentionally_blank": group.declaration.get("currency", "") == "",
                "job_id": job_id,
                "plan_path": str(plan_path),
                "mode": plan["mode"],
                "step_count": len(plan["steps"]),
                "warnings": list(group.warnings),
            }
        )

    manifest = {
        "schema_version": "1.0",
        "generated_at_utc": _utc_now(),
        "source_excel": str(excel_path.expanduser()),
        "sheet_name": parse_result.sheet_name,
        "tenant_id": options.tenant_id,
        "machine_id": options.machine_id,
        "mode": "safeBrakeStore" if options.include_store_safebrake else "fillOnly",
        "group_count": parse_result.group_count,
        "defaults": asdict(options.defaults),
        "safe_brake": {
            "currency_intentionally_blank": True,
            "store_safebrake_included": options.include_store_safebrake,
        },
        "entries": entries,
    }
    manifest_path = out_dir / "batch_manifest.json"
    _write_json(manifest_path, manifest)
    return CompiledBatch(
        manifest_path=manifest_path,
        plan_paths=tuple(plan_paths),
        group_count=parse_result.group_count,
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Compile broker Excel template into Albania job plans"
    )
    parser.add_argument("--excel", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--tenant-id", default="tenant_demo")
    parser.add_argument("--machine-id", default="machine_demo")
    parser.add_argument("--job-prefix", default="job_albania_template")
    parser.add_argument("--include-store-safebrake", action="store_true")
    parser.add_argument("--customs-office", default="AL111000")
    parser.add_argument("--authorization-reference", required=True)
    parser.add_argument("--means-transport-code-1", default="50")
    parser.add_argument("--means-transport-country-from", default="RS")
    parser.add_argument("--truck-registration-plate-number", required=True)
    parser.add_argument("--means-transport-country-to", default="AL")
    parser.add_argument("--customs-tariff-2", default="000")
    parser.add_argument("--document-date", default="")
    args = parser.parse_args()

    defaults = TemplateDefaults(
        customs_office=args.customs_office,
        authorization_reference=args.authorization_reference,
        means_transport_code_1=args.means_transport_code_1,
        means_transport_country_from=args.means_transport_country_from,
        truck_registration_plate_number=args.truck_registration_plate_number,
        means_transport_country_to=args.means_transport_country_to,
        customs_tariff_2=args.customs_tariff_2,
        document_date=args.document_date,
    )
    compiled = compile_broker_excel_batch(
        args.excel,
        args.out_dir,
        options=BatchCompileOptions(
            tenant_id=args.tenant_id,
            machine_id=args.machine_id,
            job_prefix=args.job_prefix,
            include_store_safebrake=args.include_store_safebrake,
            defaults=defaults,
        ),
    )
    print(json.dumps(compiled.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
