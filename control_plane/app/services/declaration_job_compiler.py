from __future__ import annotations

from typing import Any

from control_plane.app.services.job_compiler import JobCompiler


def declaration_values(declaration_model: dict[str, Any]) -> dict[str, str]:
    first_item = declaration_model["items"][0]
    server_defaults = declaration_model.get("server_defaults", {})
    values = {
        "office_code": str(server_defaults.get("office_code", "AL001")),
        "authorisation_reference": str(
            server_defaults.get("authorisation_reference", "SAFEBRAKE-AUTH")
        ),
        "transport_mode": str(server_defaults.get("transport_mode", "3")),
        "truck_registration": str(server_defaults.get("truck_registration", "SAFEBRAKE-TRUCK")),
        "document_reference": first_item["document_reference"],
        "invoice_number": first_item["awb"],
        "hs_code": first_item["hs_code"],
        "quantity": str(first_item["quantity"]),
        "statistical_quantity": str(first_item["statistical_quantity"]),
        "gross_weight": str(first_item["gross_weight"]),
        "net_weight": str(first_item["net_weight"]),
        "invoice_value": str(first_item["invoice_value"]),
        "origin": first_item["origin"],
        "description": first_item["description"],
    }
    currency = server_defaults.get("currency_code")
    if currency:
        values["currency_code"] = str(currency)
    return values


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
        if len(declaration_model["items"]) > 1:
            raise NotImplementedError(
                "Multi-item declaration compilation is out of scope for PR #3"
            )
        values = declaration_values(declaration_model)
        if mode == "safeBrakeStore":
            values.pop("currency_code", None)
        return self.job_compiler.compile_job(
            tenant_id=tenant_id,
            machine_id=machine_id,
            pack=pack,
            mode=mode,
            values=values,
            ttl_minutes=ttl_minutes,
        )
