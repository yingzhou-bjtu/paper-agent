#Requires -Version 5.1
# paper-agent env setup guide (Windows)
# Usage: .\bin\setup-env.ps1

$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$Root = Split-Path -Parent $PSScriptRoot

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $Python) {
    Write-Error "python or python3 was not found on PATH. Install Python 3 first."
}

& $Python.Source (Join-Path $Root "scripts\setup_env.py") @args
exit $LASTEXITCODE
