#Requires -Version 5.1
# paper-agent 命令行引导（Windows）
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $Python) { Write-Error "未找到 python 或 python3。" }

& $Python.Source (Join-Path $Root "scripts\guide_cli.py") @args
exit $LASTEXITCODE
