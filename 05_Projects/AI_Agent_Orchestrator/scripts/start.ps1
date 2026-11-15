<#
    start.ps1 — Requirement.md FR-022.

    Starts the Orchestrator backend and serves the built dashboard, in that
    order, tracking each process's PID so stop.ps1 can target it exactly.

    The MCP server is intentionally NOT started here: it talks to Claude
    Desktop over stdio, and Claude Desktop itself launches
    mcp_server/main.py as a subprocess per the claude_desktop_config.json
    entry from Antigravity_Build_Guide.md section 10 — a second, independent
    copy started by this script would not be the one Claude Desktop talks to.

    NOT executed by Claude in this build — see install.ps1's note.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ScriptDir
. (Join-Path $ScriptDir "_lib.ps1")

$LogsDir = Join-Path $ProjectRoot "logs"
New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$EnvValues = Get-OrchestratorEnv -ProjectRoot $ProjectRoot
$BackendHost = Get-EnvValue $EnvValues "ORCHESTRATOR_HOST" "127.0.0.1"
$BackendPort = Get-EnvValue $EnvValues "ORCHESTRATOR_PORT" "8000"
$FrontendPort = "5173"

function Start-Tracked {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string]$ArgumentList,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory
    )

    $PidFile = Join-Path $LogsDir "$Name.pid"
    if (Test-Path $PidFile) {
        $ExistingPid = Get-Content $PidFile
        if (Get-Process -Id $ExistingPid -ErrorAction SilentlyContinue) {
            Write-Host "$Name already running (PID $ExistingPid)."
            return
        }
    }

    $Process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput (Join-Path $LogsDir "$Name.out.log") `
        -RedirectStandardError (Join-Path $LogsDir "$Name.err.log") `
        -WindowStyle Hidden -PassThru

    Set-Content -Path $PidFile -Value $Process.Id
    Write-Host "$Name started (PID $($Process.Id))."
}

$BackendDir = Join-Path $ProjectRoot "backend"
Start-Tracked -Name "backend" `
    -FilePath (Join-Path $BackendDir ".venv\Scripts\python.exe") `
    -ArgumentList "-m uvicorn main:app --host $BackendHost --port $BackendPort" `
    -WorkingDirectory $BackendDir

$FrontendDist = Join-Path $ProjectRoot "frontend\dist"
Start-Tracked -Name "frontend" `
    -FilePath "npx" `
    -ArgumentList "serve -s `"$FrontendDist`" -l $FrontendPort" `
    -WorkingDirectory $ProjectRoot

Write-Host ""
Write-Host "Dashboard:  http://${BackendHost}:${FrontendPort}"
Write-Host "Backend:    http://${BackendHost}:${BackendPort}"
Write-Host "MCP server: launched by Claude Desktop itself (stdio), not by this script."
