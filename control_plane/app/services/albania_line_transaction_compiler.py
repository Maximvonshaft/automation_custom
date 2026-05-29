from __future__ import annotations

import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

PACK_DIR = (
    Path(__file__).resolve().parents[2]
    / "packs"
    / "asycuda_albania_line_transaction"
    / "v3_1_safebrake"
)
SAFE_BRAKE_STORE_ACTION = "store_line_safebrake"


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _utc_expiry(hours: int = 2) -> str:
    return (datetime.now(UTC) + timedelta(hours=hours)).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def load_coordinate_pack(pack_dir: Path = PACK_DIR) -> dict[str, Any]:
    field_map_path = pack_dir / "field_map.yaml"
    store_path = pack_dir / "store_safebrake.yaml"
    return {
        "field_map": yaml.safe_load(field_map_path.read_text(encoding="utf-8")),
        "store_safebrake": yaml.safe_load(store_path.read_text(encoding="utf-8")),
    }


def _numeric_clean(value: Any) -> str:
    text = str(value).strip()
    return re.sub(r"[^0-9.\-]", "", text)


def _resolve_value(field: dict[str, Any], declaration: dict[str, Any]) -> str:
    if "constant" in field:
        return str(field.get("constant") or "")
    source = field.get("source")
    if not source:
        return ""
    value = declaration.get(str(source), "")
    if field.get("transform") == "numeric_clean":
        return _numeric_clean(value)
    return str(value)


def _normalized_action(action: str) -> str:
    if action in {"click_paste_code", "click_paste"}:
        return "click_paste"
    if action in {"paste_code", "paste"}:
        return "paste"
    return action


def compile_steps_from_declaration(
    declaration: dict[str, Any],
    *,
    include_store_safebrake: bool = False,
    pack_dir: Path = PACK_DIR,
) -> list[dict[str, Any]]:
    pack = load_coordinate_pack(pack_dir)
    field_map = pack["field_map"]
    store_safebrake = pack["store_safebrake"]

    steps: list[dict[str, Any]] = []
    step_number = 1

    for field in field_map["fields"]:
        action = _normalized_action(str(field["action"]))
        if action == "skip":
            continue

        value = _resolve_value(field, declaration)
        if field.get("required") and value == "":
            raise ValueError(f"Required field is empty: {field['field_key']}")

        if action == "click_paste":
            step = {
                "step": step_number,
                "action": "click_paste",
                "field_key": field["field_key"],
                "x": int(field["x"]),
                "y": int(field["y"]),
                "value": value,
                "label": field.get("screen_label", field["field_key"]),
            }
        elif action == "paste":
            step = {
                "step": step_number,
                "action": "paste",
                "field_key": field["field_key"],
                "value": value,
                "label": field.get("screen_label", field["field_key"]),
            }
        else:
            raise ValueError(f"Unsupported field action: {action}")

        steps.append(step)
        step_number += 1

        if field.get("after_action") == "tab":
            steps.append(
                {
                    "step": step_number,
                    "action": "hotkey",
                    "keys": ["tab"],
                    "label": f"tab after {field['field_key']}",
                }
            )
            step_number += 1

    steps.append(
        {
            "step": step_number,
            "action": "screenshot",
            "label": "post-fill safebrake evidence screenshot",
        }
    )
    step_number += 1

    if include_store_safebrake:
        steps.append(
            {
                "step": step_number,
                "action": SAFE_BRAKE_STORE_ACTION,
                "x": int(store_safebrake["x"]),
                "y": int(store_safebrake["y"]),
                "label": "Line Transaction child Store SafeBrake probe",
            }
        )

    return steps


def build_unsigned_job_plan(
    declaration: dict[str, Any],
    *,
    tenant_id: str,
    machine_id: str,
    job_id: str,
    include_store_safebrake: bool = False,
    pack_dir: Path = PACK_DIR,
) -> dict[str, Any]:
    pack = load_coordinate_pack(pack_dir)["field_map"]
    mode = "safeBrakeStore" if include_store_safebrake else "fillOnly"
    return {
        "job_id": job_id,
        "tenant_id": tenant_id,
        "machine_id": machine_id,
        "pack_id": pack["pack_id"],
        "pack_version": pack["pack_version"],
        "mode": mode,
        "issued_at": _utc_now(),
        "expires_at": _utc_expiry(),
        "steps": compile_steps_from_declaration(
            declaration,
            include_store_safebrake=include_store_safebrake,
            pack_dir=pack_dir,
        ),
    }


def load_sample_values(pack_dir: Path = PACK_DIR) -> dict[str, str]:
    import csv

    sample_path = pack_dir / "sample_values.csv"
    with sample_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"Expected one sample row, found {len(rows)}")
    return rows[0]


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Compile Albania ASYCUDA v3.1 SafeBrake job plan")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--tenant-id", default="tenant_demo")
    parser.add_argument("--machine-id", default="machine_demo")
    parser.add_argument("--job-id", default="job_albania_v311_safebrake_compiled")
    parser.add_argument("--include-store-safebrake", action="store_true")
    args = parser.parse_args()

    if not args.sample:
        raise SystemExit("Only --sample is implemented in this compiler entrypoint.")

    plan = build_unsigned_job_plan(
        load_sample_values(),
        tenant_id=args.tenant_id,
        machine_id=args.machine_id,
        job_id=args.job_id,
        include_store_safebrake=args.include_store_safebrake,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
