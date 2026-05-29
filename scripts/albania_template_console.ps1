$ErrorActionPreference = "Stop"

cd (Split-Path -Parent $PSScriptRoot)

& ".\.venv\Scripts\python.exe" -m control_plane.app.services.albania_template_console
