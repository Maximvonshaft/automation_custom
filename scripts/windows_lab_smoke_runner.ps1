param(
    [Parameter(Mandatory = $true)]
    [string]$SignedJobPlan,

    [Parameter(Mandatory = $false)]
    [string]$PublicKeyPem,

    [Parameter(Mandatory = $true)]
    [string]$AsycudaWindowTitle,

    [Parameter(Mandatory = $false)]
    [string]$EvidenceRoot = ".\outputs\windows_lab_smoke",

    [Parameter(Mandatory = $false)]
    [string]$ManifestParseReport,

    [Parameter(Mandatory = $false)]
    [string]$DeclarationModel,

    [Parameter(Mandatory = $false)]
    [string]$KnownIssues = "None reported."
)

$ErrorActionPreference = "Stop"

$prepareArgs = @{
    AsycudaWindowTitle = $AsycudaWindowTitle
}
if (-not [string]::IsNullOrWhiteSpace($PublicKeyPem)) {
    $prepareArgs.PublicKeyPem = $PublicKeyPem
}
& "$PSScriptRoot\windows_lab_smoke_prepare_env.ps1" @prepareArgs

if (-not (Test-Path -LiteralPath $SignedJobPlan -PathType Leaf)) {
    throw "Signed job plan was not found: $SignedJobPlan"
}

$resolvedEvidenceRoot = New-Item -ItemType Directory -Force -Path $EvidenceRoot
$runId = "lab_" + (Get-Date -Format "yyyyMMdd_HHmmss")
$env:CUSTOMSOPS_AGENT_EVIDENCE_ROOT = $resolvedEvidenceRoot.FullName

$python = @'
import json
import os
from pathlib import Path

from agent.customsops_agent.action_executor import choose_executor
from agent.customsops_agent.evidence_v311_adapter import write_v311_review_bundle
from agent.customsops_agent.signed_plan import validate_signed_plan
from shared.signing.ed25519 import load_public_key_pem
from shared.watermark import watermark_text

signed_job_plan = Path(os.environ["LAB_SIGNED_JOB_PLAN"])
evidence_root = Path(os.environ["LAB_EVIDENCE_ROOT"])
window_title = os.environ["LAB_ASYCUDA_WINDOW_TITLE"]
run_id = os.environ["LAB_RUN_ID"]
tenant_id = os.environ["CUSTOMSOPS_TENANT_ID"]
machine_id = os.environ["CUSTOMSOPS_MACHINE_ID"]
parse_report_path = os.environ.get("LAB_PARSE_REPORT")
declaration_model_path = os.environ.get("LAB_DECLARATION_MODEL")

plan = json.loads(signed_job_plan.read_text(encoding="utf-8"))
if plan.get("mode") not in {"fillOnly", "safeBrakeStore"}:
    raise SystemExit("Only fillOnly and safeBrakeStore modes are allowed.")

public_key = load_public_key_pem(os.environ["CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM"])
validated = validate_signed_plan(
    plan,
    public_key=public_key,
    expected_tenant_id=tenant_id,
    expected_machine_id=machine_id,
)

for step in validated["steps"]:
    if step.get("action") in {"submit", "register", "payment", "tax_finalize"}:
        raise SystemExit(f"Forbidden action in signed plan: {step.get('action')}")

pre_screenshot = evidence_root / "lab_pre_run.png"
post_screenshot = evidence_root / "lab_post_run.png"
executor = choose_executor(use_real_gui=True, foreground_window_title=window_title)
executor.backend.screenshot(pre_screenshot)
ledger_entries = executor.execute(validated["steps"])
executor.backend.screenshot(post_screenshot)

parse_report = {"accepted": True, "template_type": "lab", "errors": [], "warnings": []}
if parse_report_path:
    parse_report = json.loads(Path(parse_report_path).read_text(encoding="utf-8"))

declaration_model = {"declaration_id": "lab_smoke_not_committed", "items": []}
if declaration_model_path:
    declaration_model = json.loads(Path(declaration_model_path).read_text(encoding="utf-8"))

watermark = watermark_text(tenant_id, machine_id, validated["job_id"], run_id)
bundle = write_v311_review_bundle(
    root=evidence_root,
    job_plan=validated,
    parse_report=parse_report,
    declaration_model=declaration_model,
    ledger_entries=ledger_entries,
    watermark=watermark,
    screenshot_paths=[pre_screenshot, post_screenshot],
)
print(str(bundle))
'@

$env:LAB_SIGNED_JOB_PLAN = (Resolve-Path -LiteralPath $SignedJobPlan).Path
$env:LAB_EVIDENCE_ROOT = $resolvedEvidenceRoot.FullName
$env:LAB_ASYCUDA_WINDOW_TITLE = $AsycudaWindowTitle
$env:LAB_RUN_ID = $runId
if ($ManifestParseReport) {
    $env:LAB_PARSE_REPORT = (Resolve-Path -LiteralPath $ManifestParseReport).Path
}
if ($DeclarationModel) {
    $env:LAB_DECLARATION_MODEL = (Resolve-Path -LiteralPath $DeclarationModel).Path
}

$python | python -

& "$PSScriptRoot\windows_lab_smoke_collect_evidence.ps1" `
    -EvidenceRoot $resolvedEvidenceRoot.FullName `
    -RunId $runId `
    -SignedJobPlan $SignedJobPlan `
    -AsycudaWindowTitle $AsycudaWindowTitle `
    -KnownIssues $KnownIssues

Write-Output "Windows ASYCUDA lab smoke complete. Evidence root: $($resolvedEvidenceRoot.FullName)"
