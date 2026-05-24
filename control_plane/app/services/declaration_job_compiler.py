from __future__ import annotations

from typing import Any

from control_plane.app.services.job_compiler import JobCompiler


def declaration_values(declaration_model: dict[str, Any]) -> dict[str, str]:
    first_item = declaration_model["items"][0]
    return {
        "invoice_number": first_item["awb"],
        "gross_weight": str(first_item["weight"]),
    }


class DeclarationJobCompiler:
    def __init__(self, job_compiler: JobCompiler | None = None) -> None:
        self.job_compiler = job_compiler or JobCompiler()

    def compile_declaration_job(
        self,
        *,
        tenant_id: str,
        machine_id: str,
        pack: dict[str, Any],
        mode: str,
        declaration_model: dict[str, Any],
        ttl_minutes: int = 15,
    ) -> dict[str, Any]:
        if not declaration_model.get("items"):
            raise ValueError("Declaration model contains no items")
        return self.job_compiler.compile_job(
            tenant_id=tenant_id,
            machine_id=machine_id,
            pack=pack,
            mode=mode,
            values=declaration_values(declaration_model),
            ttl_minutes=ttl_minutes,
        )

