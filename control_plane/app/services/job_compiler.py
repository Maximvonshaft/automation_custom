from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from control_plane.app.core.security import assert_actions_allowed, assert_mode_allowed


class JobCompiler:
    def compile_job(
        self,
        *,
        tenant_id: str,
        machine_id: str,
        pack: dict,
        mode: str,
        values: dict[str, str],
        ttl_minutes: int = 15,
    ) -> dict:
        assert_mode_allowed(mode)
        now = datetime.now(UTC)
        steps = self._compile_steps(pack=pack, mode=mode, values=values)
        assert_actions_allowed(steps)
        return {
            "job_id": f"job_{uuid4().hex}",
            "tenant_id": tenant_id,
            "machine_id": machine_id,
            "pack_id": pack["field_map"]["pack_id"],
            "pack_version": str(pack["field_map"]["version"]),
            "mode": mode,
            "issued_at": now.isoformat(),
            "expires_at": (now + timedelta(minutes=ttl_minutes)).isoformat(),
            "steps": steps,
            "signature": "",
        }

    def _compile_steps(self, *, pack: dict, mode: str, values: dict[str, str]) -> list[dict]:
        fields = pack["field_map"]["fields"]
        steps: list[dict] = []
        step_number = 1
        for field_key, value in values.items():
            if field_key not in fields:
                raise ValueError(f"Unknown field key for pack: {field_key}")
            field = fields[field_key]
            steps.append(
                {
                    "step": step_number,
                    "field_key": field_key,
                    "action": "click_paste",
                    "x": int(field["x"]),
                    "y": int(field["y"]),
                    "value": value,
                    "label": field.get("label", field_key),
                }
            )
            step_number += 1
        if mode == "safeBrakeStore":
            store = pack["safebrake"]["store_button"]
            steps.append(
                {
                    "step": step_number,
                    "action": "store_line_safebrake",
                    "x": int(store["x"]),
                    "y": int(store["y"]),
                    "label": "SafeBrake Store",
                }
            )
        return steps

