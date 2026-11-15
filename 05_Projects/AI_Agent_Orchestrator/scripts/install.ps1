<#
    install.ps1 — Requirement.md FR-022.

    Installs backend and mcp_server Python dependencies and builds the React
    dashboard. Run once after Phase 1's environment survey has confirmed
    Python and Node.js are present (Antigravity_Build_Guide.md section 4).

    NOT executed by Claude in this build: written in a Linux cloud container
    with no Windows PowerShell available to run it against. Run it for real
    on the target Windows machine and report back any error.
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

function Install-PythonComponent {
    param([Parameter(Mandatory = $true)][string]$Name)

    $Dir = Join-Path $ProjectRoot $Name
    Write-Host "== Installing $Name =="
    Push-Location $Dir
    try {
        if (-not (Test-Path ".venv")) {
            python -m venv .venv
        }
        & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
        & ".\.venv\Scripts\pip.exe" install -r requirements.txt
    } finally {
        Pop-Location
    }
}

Install-PythonComponent -Name "backend"
Install-PythonComponent -Name "mcp_server"

Write-Host "== Installing frontend dependencies and building the dashboard =="
Push-Location (Join-Path $ProjectRoot "frontend")
try {
    npm install
    npm run build
} finally {
    Pop-Location
}

$EnvFile = Join-Path $ProjectRoot "config\.env"
$EnvExample = Join-Path $ProjectRoot "config\.env.example"
if (-not (Test-Path $EnvFile)) {
    Copy-Item $EnvExample $EnvFile
    Write-Host "== Created config\.env from .env.example =="
    Write-Host "Edit it now: set DASHBOARD_PASSWORD and DASHBOARD_JWT_SECRET before starting (FR-025/FR-026)."
}

Write-Host "Install complete."
