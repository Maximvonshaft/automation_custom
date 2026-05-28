param(
    [string]$OutputRoot = ".\dist\CustomsOpsOperatorSkeleton",
    [string]$SourceCommit = "0000000000000000000000000000000000000000"
)

$ErrorActionPreference = "Stop"

Write-Host "CustomsOps Windows Operator Package Skeleton Builder"
Write-Host "OutputRoot: $OutputRoot"
Write-Host ""
Write-Host "This script creates a skeleton directory only."
Write-Host "It does not create an external release package."
Write-Host "It does not include country pack content."
Write-Host "It does not include production credentials."
Write-Host "It does not add Submit/Register/Payment/tax-finalizing automation."

if (Test-Path $OutputRoot) {
    Remove-Item -Recurse -Force $OutputRoot
}

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot "diagnostics") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot "evidence") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot "config") | Out-Null

Copy-Item -Path (Join-Path $PSScriptRoot "README.md") -Destination (Join-Path $OutputRoot "README.md") -Force
Copy-Item -Path (Join-Path $PSScriptRoot "operator_launcher.ps1") -Destination (Join-Path $OutputRoot "operator_launcher.ps1") -Force

$manifest = [ordered]@{
    package_name = "customsops-controlled-operator-package"
    package_version = "0.0.0-skeleton"
    source_repo = "https://github.com/Maximvonshaft/automation_custom"
    source_commit = $SourceCommit
    build_timestamp_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    build_host = $env:COMPUTERNAME
    release_classification = "internal_skeleton_only"
    included_files = @(
        "README.md",
        "operator_launcher.ps1"
    )
    excluded_patterns = @(
        "control_plane/**",
        "control_plane/packs/**",
        "delivery_packs/**",
        "tests/**",
        "*.xlsx",
        "*.pem",
        "*.key",
        "*.p12",
        "*.pfx",
        "*.env"
    )
    checksum_file = "checksums.sha256"
    no_finalization_actions = $true
    country_pack_excluded = $true
    local_compilation_disabled = $true
}

$manifestPath = Join-Path $OutputRoot "BUILD_MANIFEST.json"
$manifest | ConvertTo-Json -Depth 8 | Set-Content -Path $manifestPath -Encoding UTF8

$checksumPath = Join-Path $OutputRoot "checksums.sha256"
Get-ChildItem -Path $OutputRoot -Recurse -File |
    Where-Object { $_.FullName -ne $checksumPath } |
    Sort-Object FullName |
    ForEach-Object {
        $hash = Get-FileHash -Algorithm SHA256 -Path $_.FullName
        $relative = Resolve-Path -Path $_.FullName -Relative
        "$($hash.Hash.ToLower())  $relative"
    } | Set-Content -Path $checksumPath -Encoding ASCII

Write-Host "Skeleton created: $OutputRoot"
Write-Host "Manifest: $manifestPath"
Write-Host "Checksums: $checksumPath"
Write-Host "This is not approved for external distribution."
