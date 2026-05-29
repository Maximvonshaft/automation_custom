param(
    [Parameter(Mandatory = $true)]
    [int]$X,
    [Parameter(Mandatory = $true)]
    [int]$Y,
    [string]$Value = "SANITIZED_CLICK_PASTE_DO_NOT_SUBMIT",
    [string]$RunRoot = "",
    [string]$ForegroundWindowTitle = "ASYCUDAWorld",
    [int]$FocusDelaySeconds = 8
)

$ErrorActionPreference = "Stop"

if (!$RunRoot) {
    $RunRoot = Join-Path (Get-Location) ("outputs\live_probe_click_paste_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
}

Write-Host "Put ASYCUDA page in focus within $FocusDelaySeconds seconds."
Write-Host "Target coordinate: X=$X Y=$Y"
Start-Sleep -Seconds $FocusDelaySeconds

& ".\.venv\Scripts\python.exe" "scripts\live_probe_runner.py" `
    --probe click-paste `
    --run-root $RunRoot `
    --foreground-window-title $ForegroundWindowTitle `
    --x $X `
    --y $Y `
    --value $Value

Write-Host "Live click-paste probe complete. RunRoot: $RunRoot"
