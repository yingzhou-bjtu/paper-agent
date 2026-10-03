#Requires -Version 5.1
# paper-agent CLI guide (Windows)
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$Root = Split-Path -Parent $PSScriptRoot

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $Python) { Write-Error "python or python3 was not found on PATH." }

& $Python.Source (Join-Path $Root "scripts\guide_cli.py") @args
exit $LASTEXITCODE
