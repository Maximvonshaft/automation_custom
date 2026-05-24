param(
    [Parameter(Mandatory = $false)]
    [string]$PublicKeyPem,

    [Parameter(Mandatory = $true)]
    [string]$AsycudaWindowTitle
)

$ErrorActionPreference = "Stop"

$isWindowsOs = [System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform(
    [System.Runtime.InteropServices.OSPlatform]::Windows
)
if (-not $isWindowsOs) {
    throw "Windows ASYCUDA lab smoke can run only on Windows."
}

if ([string]::IsNullOrWhiteSpace($env:CUSTOMSOPS_TENANT_ID)) {
    throw "CUSTOMSOPS_TENANT_ID is required."
}

if ([string]::IsNullOrWhiteSpace($env:CUSTOMSOPS_MACHINE_ID)) {
    throw "CUSTOMSOPS_MACHINE_ID is required."
}

if ([string]::IsNullOrWhiteSpace($AsycudaWindowTitle) -or
    $AsycudaWindowTitle.ToUpperInvariant().IndexOf("ASYCUDA") -lt 0) {
    throw "ASYCUDA foreground window title is required and must contain ASYCUDA."
}

if (-not [string]::IsNullOrWhiteSpace($PublicKeyPem)) {
    if (-not (Test-Path -LiteralPath $PublicKeyPem -PathType Leaf)) {
        throw "Public key file was not found: $PublicKeyPem"
    }
    $env:CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM = Get-Content -LiteralPath $PublicKeyPem -Raw
}

if ([string]::IsNullOrWhiteSpace($env:CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM)) {
    throw "CUSTOMSOPS_SIGNING_PUBLIC_KEY_PEM or -PublicKeyPem is required."
}

python -m pip install -e ".[windows]" | Write-Output

Write-Output "Windows lab smoke environment prepared."
