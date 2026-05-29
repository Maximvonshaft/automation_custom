param(
    [Parameter(Mandatory = $true)]
    [int]$X,
    [Parameter(Mandatory = $true)]
    [int]$Y,
    [int]$Count = 5,
    [string]$RunRoot = "",
    [string]$ForegroundWindowTitle = "ASYCUDAWorld",
    [int]$FocusDelaySeconds = 8
)

$ErrorActionPreference = "Stop"

if ($Count -lt 1) {
    throw "Count must be at least 1."
}

if (!$RunRoot) {
    $RunRoot = Join-Path (Get-Location) ("outputs\live_probe_tab_chain_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
}

Write-Host "Put ASYCUDA page in focus within $FocusDelaySeconds seconds."
Write-Host "Start coordinate: X=$X Y=$Y Count=$Count"
Start-Sleep -Seconds $FocusDelaySeconds

& ".\.venv\Scripts\python.exe" "scripts\live_probe_runner.py" `
    --probe tab-chain `
    --run-root $RunRoot `
    --foreground-window-title $ForegroundWindowTitle `
    --x $X `
    --y $Y `
    --count $Count

Write-Host "Live tab-chain probe complete. RunRoot: $RunRoot"
