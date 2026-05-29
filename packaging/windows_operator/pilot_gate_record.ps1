param(
    [Parameter(Mandatory = $true)]
    [string]$CandidatePackageRoot,
    [Parameter(Mandatory = $true)]
    [string]$CandidateVersion,
    [Parameter(Mandatory = $true)]
    [string]$SourceCommit,
    [Parameter(Mandatory = $true)]
    [string]$OperatorAllowlist,
    [Parameter(Mandatory = $true)]
    [string]$MachineAllowlist,
    [string]$OutputPath = "",
    [string]$EvidenceReferenceFile = "",
    [string]$WindowsLabSmokeReference = "",
    [switch]$LocalQualityGatePassed,
    [switch]$RemoteQualityGatePassed,
    [string]$BusinessOwner = "",
    [string]$ComplianceOwner = "",
    [string]$SupportOwner = "",
    [string]$TechnicalOwner = ""
)

$ErrorActionPreference = "Stop"

Write-Host "CustomsOps Controlled Pilot Gate Record"
Write-Host "CandidatePackageRoot: $CandidatePackageRoot"
Write-Host "CandidateVersion: $CandidateVersion"
Write-Host ""
Write-Host "This script writes a gate record only."
Write-Host "It does not create an external package."
Write-Host "It does not move country pack content."
Write-Host "It does not enable local Excel compilation."
Write-Host ""

if ($SourceCommit -notmatch "^[0-9a-f]{40}$") {
    throw "SourceCommit must be a 40-character lowercase git SHA."
}

if (!(Test-Path $CandidatePackageRoot)) {
    throw "CandidatePackageRoot does not exist: $CandidatePackageRoot"
}

$buildManifest = Join-Path $CandidatePackageRoot "BUILD_MANIFEST.json"
$checksumFile = Join-Path $CandidatePackageRoot "checksums.sha256"

if (!(Test-Path $buildManifest)) {
    throw "BUILD_MANIFEST.json is missing from candidate package root."
}

if (!(Test-Path $checksumFile)) {
    throw "checksums.sha256 is missing from candidate package root."
}

if (!(Test-Path $OperatorAllowlist)) {
    throw "Operator allowlist file is missing: $OperatorAllowlist"
}

if (!(Test-Path $MachineAllowlist)) {
    throw "Machine allowlist file is missing: $MachineAllowlist"
}

if ($EvidenceReferenceFile -and !(Test-Path $EvidenceReferenceFile)) {
    throw "Evidence reference file is missing: $EvidenceReferenceFile"
}

$manifestText = Get-Content -Raw -Path $buildManifest
$manifest = $manifestText | ConvertFrom-Json

if ($manifest.no_finalization_actions -ne $true) {
    throw "Build manifest must declare no_finalization_actions=true."
}

if ($manifest.country_pack_excluded -ne $true) {
    throw "Build manifest must declare country_pack_excluded=true."
}

if ($manifest.local_compilation_disabled -ne $true) {
    throw "Build manifest must declare local_compilation_disabled=true."
}

if ($manifest.source_commit -ne $SourceCommit) {
    throw "Build manifest source_commit does not match requested SourceCommit."
}

if (!$OutputPath) {
    $OutputPath = Join-Path $CandidatePackageRoot "PILOT_GATE_RECORD.json"
}

$record = [ordered]@{
    schema_version = "1.0"
    gate_type = "controlled_pilot_gate_record"
    candidate_version = $CandidateVersion
    source_repo = "https://github.com/Maximvonshaft/automation_custom"
    source_commit = $SourceCommit
    created_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    created_by_host = $env:COMPUTERNAME
    candidate_package_root = (Resolve-Path -Path $CandidatePackageRoot).Path
    build_manifest_path = (Resolve-Path -Path $buildManifest).Path
    checksum_file = (Resolve-Path -Path $checksumFile).Path
    operator_allowlist_file = (Resolve-Path -Path $OperatorAllowlist).Path
    machine_allowlist_file = (Resolve-Path -Path $MachineAllowlist).Path
    approvals = [ordered]@{
        business_owner = $BusinessOwner
        compliance_owner = $ComplianceOwner
        support_owner = $SupportOwner
        technical_owner = $TechnicalOwner
    }
    boundary = [ordered]@{
        source_tree_distributed = $false
        country_pack_included = $false
        local_compilation_enabled = $false
        external_distribution_approved = $false
        raw_sensitive_evidence_included = $false
    }
    qa_evidence = [ordered]@{
        local_quality_gate_passed = [bool]$LocalQualityGatePassed
        remote_quality_gate_passed = [bool]$RemoteQualityGatePassed
        windows_lab_smoke_reference = $(if ($WindowsLabSmokeReference) { $WindowsLabSmokeReference } else { $null })
        evidence_reference_file = $(if ($EvidenceReferenceFile) { (Resolve-Path -Path $EvidenceReferenceFile).Path } else { $null })
    }
    notes = @(
        "Gate record only; not an external distribution approval.",
        "External rollout requires a separate signed approval outside this script.",
        "Raw sensitive evidence must remain outside the repository."
    )
}

$record | ConvertTo-Json -Depth 10 | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Pilot gate record written: $OutputPath"
