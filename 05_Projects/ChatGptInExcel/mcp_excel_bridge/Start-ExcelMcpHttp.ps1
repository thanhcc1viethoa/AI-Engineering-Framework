#requires -Version 5.1
# Starts the Excel MCP bridge over HTTP so a remote MCP client (e.g. the ChatGPT
# app via a public HTTPS tunnel) can call the Excel tools.
#
# Open Excel first. Then run this script, then expose the printed local URL with
# a tunnel (cloudflared / ngrok) and register that HTTPS URL in ChatGPT.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

# Persist a secret path segment + bearer token across runs so the connector URL
# stays stable. This file is gitignored.
$secretsFile = Join-Path $PSScriptRoot ".http-secrets.json"
if (Test-Path $secretsFile) {
  $secrets = Get-Content $secretsFile -Raw | ConvertFrom-Json
} else {
  $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
  function New-Hex([int]$bytes) {
    $b = New-Object byte[] $bytes
    $rng.GetBytes($b)
    ($b | ForEach-Object { $_.ToString("x2") }) -join ""
  }
  $secrets = [PSCustomObject]@{ pathSegment = (New-Hex 16); token = (New-Hex 24) }
  $secrets | ConvertTo-Json | Out-File -FilePath $secretsFile -Encoding utf8
  Write-Host "Generated new secrets in .http-secrets.json" -ForegroundColor Yellow
}

$port = if ($env:EXCEL_MCP_PORT) { $env:EXCEL_MCP_PORT } else { "8765" }
$path = "/mcp/$($secrets.pathSegment)"

$env:EXCEL_MCP_TRANSPORT = "http"
$env:EXCEL_MCP_HOST = "127.0.0.1"
$env:EXCEL_MCP_PORT = $port
$env:EXCEL_MCP_PATH = $path
$env:EXCEL_MCP_TOKEN = $secrets.token

Write-Host ""
Write-Host "Excel MCP bridge (HTTP) starting." -ForegroundColor Green
Write-Host "  Local endpoint : http://127.0.0.1:$port$path"
Write-Host "  Bearer token   : $($secrets.token)"
Write-Host ""
Write-Host "Next: expose it with a tunnel, e.g." -ForegroundColor Cyan
Write-Host "  cloudflared tunnel --url http://127.0.0.1:$port"
Write-Host "Then the ChatGPT connector URL is:  https://<tunnel-host>$path"
Write-Host "(ChatGPT app: set authentication = None; the secret path protects it.)"
Write-Host ""

& $python server.py
