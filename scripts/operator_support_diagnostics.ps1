param(
    [string]$PackageRoot = (Get-Location).Path,
    [string]$OutputPath = ".\operator_support_diagnostics.json"
)

$ErrorActionPreference = "Stop"

Write-Host "CustomsOps Operator Support Diagnostics (Skeleton)"
Write-Host "PackageRoot: $PackageRoot"
Write-Host "OutputPath : $OutputPath"
Write-Host ""
Write-Host "This skeleton collects non-secret support metadata only."
Write-Host "It must not collect credentials, customer manifests, raw screenshots, private keys, or country pack content."

$evidenceDir = Join-Path $PackageRoot "evidence"
$fileHashes = @()

if (Test-Path $evidenceDir) {
    $fileHashes = Get-ChildItem -Path $evidenceDir -Recurse -File |
        Sort-Object FullName |
        ForEach-Object {
            $hash = Get-FileHash -Algorithm SHA256 -Path $_.FullName
            [ordered]@{
                relative_path = $_.FullName.Substring($PackageRoot.Length).TrimStart("\", "/")
                sha256 = $hash.Hash.ToLower()
            }
        }
}

$manifest = [ordered]@{
    schema_version = "1.0"
    created_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    package_name = "customsops-controlled-operator-package"
    package_version = "0.0.0-skeleton"
    machine_id_present = [bool]$env:CUSTOMSOPS_MACHINE_ID
    tenant_id_present = [bool]$env:CUSTOMSOPS_TENANT_ID
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = "not_collected_by_skeleton"
    evidence_file_hashes = @($fileHashes)
    sensitive_content_excluded = $true
    notes = @(
        "Skeleton diagnostics only.",
        "Does not collect credentials, raw customer manifests, private keys, broker authorization values, or country pack content.",
        "Raw screenshots require separate redaction approval before sharing."
    )
}

$manifest | ConvertTo-Json -Depth 8 | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Diagnostics manifest written: $OutputPath"
Write-Host "Sensitive content excluded: true"
