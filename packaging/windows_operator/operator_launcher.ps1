param(
    [string]$PackageRoot = $PSScriptRoot,
    [Parameter(Mandatory = $true)]
    [string]$SignedJobPlan,
    [Parameter(Mandatory = $true)]
    [string]$MachineRegistration,
    [Parameter(Mandatory = $true)]
    [string]$PublicKeyPem,
    [string]$EvidenceRoot = ".\evidence\operator",
    [string]$ForegroundWindowTitle = "",
    [switch]$RealGui,
    [switch]$OpenEvidenceFolder,
    [string]$OutputJson = ""
)

$ErrorActionPreference = "Stop"

Write-Host "CustomsOps Operator Package Launcher"
Write-Host "PackageRoot: $PackageRoot"
Write-Host ""
Write-Host "This launcher accepts HQ-issued signed job plans only."
Write-Host "It does not compile executable job plans from Excel."
Write-Host "It does not run Submit/Register/Payment/tax-finalizing automation."
Write-Host ""

$manifest = Join-Path $PackageRoot "BUILD_MANIFEST.json"
if (Test-Path $manifest) {
    Write-Host "Build manifest found: $manifest"
} else {
    Write-Host "Build manifest not found. Treating this as a non-release/dev skeleton run."
}

$argsList = @(
    "-m",
    "agent.customsops_agent.operator_cli",
    "run-signed-job",
    "--signed-job-plan",
    $SignedJobPlan,
    "--machine-registration",
    $MachineRegistration,
    "--public-key-pem",
    $PublicKeyPem,
    "--evidence-root",
    $EvidenceRoot
)

if ($RealGui) {
    $argsList += "--real-gui"
}

if ($ForegroundWindowTitle) {
    $argsList += "--foreground-window-title"
    $argsList += $ForegroundWindowTitle
}

if ($OpenEvidenceFolder) {
    $argsList += "--open-evidence-folder"
}

if ($OutputJson) {
    $argsList += "--output-json"
    $argsList += $OutputJson
}

python @argsList
