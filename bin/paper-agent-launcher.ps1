#Requires -Version 5.1
$Root = Split-Path -Parent $PSScriptRoot
& (Join-Path $Root "bin\paper-agent-guide.ps1") @args
exit $LASTEXITCODE
