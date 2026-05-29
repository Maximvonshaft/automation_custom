param(
    [string]$RunRoot = "",
    [string]$ForegroundWindowTitle = "ASYCUDAWorld",
    [int]$FocusDelaySeconds = 8
)

$ErrorActionPreference = "Stop"

if (!$RunRoot) {
    $RunRoot = Join-Path (Get-Location) ("outputs\live_probe_foreground_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
}

Write-Host "Put ASYCUDA foreground window in focus within $FocusDelaySeconds seconds."
Start-Sleep -Seconds $FocusDelaySeconds

& ".\.venv\Scripts\python.exe" "scripts\live_probe_runner.py" `
    --probe foreground `
    --run-root $RunRoot `
    --foreground-window-title $ForegroundWindowTitle

Write-Host "Live foreground probe complete. RunRoot: $RunRoot"
