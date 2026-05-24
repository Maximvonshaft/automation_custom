# Logging, Metrics, and Evidence Spec

## Run context must include

- run_id
- tenant_id
- machine_id
- operator_id if available
- input_file_hash
- template_contract_version
- parse_report_hash
- declaration_model_hash
- signed_job_plan_hash
- pack_id
- pack_version
- mode
- started_at / finished_at

## Ledger event must include

- step
- action
- field_key
- label
- before_screenshot hash if available
- after_screenshot hash if available
- status
- error code/message

## Metrics

- manifests_uploaded_total
- manifests_rejected_total
- job_plans_signed_total
- job_plans_rejected_total
- agent_runs_total
- safebrake_store_attempts_total
- forbidden_action_rejections_total
