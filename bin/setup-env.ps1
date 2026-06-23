# paper-agent 环境配置向导 (Windows)
# 用法: .\bin\setup-env.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $Python) {
    Write-Error "未找到 python 或 python3，请先安装 Python 3。"
}

& $Python.Source (Join-Path $Root "scripts\setup_env.py") @args
exit $LASTEXITCODE
