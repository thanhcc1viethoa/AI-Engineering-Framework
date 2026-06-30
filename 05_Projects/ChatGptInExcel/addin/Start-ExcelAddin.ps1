$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path "node_modules")) {
  npm install
}

npm run certs
npm run validate

$serverLog = Join-Path $PSScriptRoot "server.log"
$serverErr = Join-Path $PSScriptRoot "server.err.log"

$existing = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if (-not $existing) {
  Start-Process -FilePath "npm.cmd" -ArgumentList "start" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $serverLog -RedirectStandardError $serverErr
  Start-Sleep -Seconds 2
}

npm run excel
