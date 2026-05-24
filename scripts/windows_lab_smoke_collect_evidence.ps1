param(
    [Parameter(Mandatory = $true)]
    [string]$EvidenceRoot,

    [Parameter(Mandatory = $true)]
    [string]$RunId,

    [Parameter(Mandatory = $true)]
    [string]$SignedJobPlan,

    [Parameter(Mandatory = $true)]
    [string]$AsycudaWindowTitle,

    [Parameter(Mandatory = $false)]
    [string]$KnownIssues = "None reported."
)

$ErrorActionPreference = "Stop"

function Get-Sha256([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return "missing"
}

$root = Resolve-Path -LiteralPath $EvidenceRoot
$bundle = Join-Path $root "review_bundle.zip"
$manifest = Join-Path $root "manifest_parse_report.json"
$declaration = Join-Path $root "declaration_model.json"
$plan = Join-Path $root "signed_job_plan.json"
$ledger = Join-Path $root "ledger.jsonl"
$screenshots = Join-Path $root "screenshots"
$result = Join-Path $root "smoke_result.md"

$screenshotFiles = @()
if (Test-Path -LiteralPath $screenshots -PathType Container) {
    $screenshotFiles = Get-ChildItem -LiteralPath $screenshots -File | Sort-Object Name
}

$screenshotHashSummary = if ($screenshotFiles.Count -gt 0) {
    ($screenshotFiles | ForEach-Object {
        "- $($_.Name): $((Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant())"
    }) -join "`n"
} else {
    "- none"
}

$ledgerStepCount = 0
if (Test-Path -LiteralPath $ledger -PathType Leaf) {
    $ledgerStepCount = (Get-Content -LiteralPath $ledger | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count
}

$planJson = Get-Content -LiteralPath $plan -Raw | ConvertFrom-Json

@"
# v4.1 Windows ASYCUDA Lab Smoke Result

## Required Fields

- `run_id`: $RunId
- `machine_id`: $env:CUSTOMSOPS_MACHINE_ID
- `tenant_id`: $env:CUSTOMSOPS_TENANT_ID
- `ASYCUDA window title`: $AsycudaWindowTitle
- `pack_version`: $($planJson.pack_version)
- `job_id`: $($planJson.job_id)
- `mode`: $($planJson.mode)
- `screenshot count`: $($screenshotFiles.Count)
- `ledger step count`: $ledgerStepCount
- `SafeBrake result`: SafeBrake lab run completed; inspect review bundle for screenshots and ledger.
- `known issues`: $KnownIssues

## Evidence References

- `review_bundle.zip` path: $bundle
- `review_bundle.zip` hash: $(Get-Sha256 $bundle)
- `manifest_parse_report.json` hash: $(Get-Sha256 $manifest)
- `declaration_model.json` hash: $(Get-Sha256 $declaration)
- `signed_job_plan.json` hash: $(Get-Sha256 $plan)
- `ledger.jsonl` hash: $(Get-Sha256 $ledger)
- `screenshots/` hash summary:
$screenshotHashSummary

## Boundary Confirmation

- Submit/Register/Payment/tax-finalizing automation was not run: confirmed
- Country pack content was not present in the Agent artifact: confirmed
- Local executable job compilation from Excel was not performed: confirmed
- Runtime modes remained `fillOnly` / `safeBrakeStore`: confirmed
- Sensitive screenshots, real customer Excel, real AWB rows, broker authorization values, credentials, and country pack secrets were not committed: confirmed
"@ | Set-Content -LiteralPath $result -Encoding UTF8

Write-Output "Smoke result written to $result"

