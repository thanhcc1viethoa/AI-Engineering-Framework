<#
    health_check.ps1 — Requirement.md FR-024.

    Polls GET /system/status (no auth required — see backend/auth.py). If it
    does not answer, restarts the Orchestrator, up to -MaxRestartAttempts
    times, tracked in logs\health_check_restart_count.txt, so a genuinely
    broken install fails loudly instead of restart-looping forever.

    Intended to be run on a schedule (e.g. every few minutes via Task
    Scheduler) once Phase 9 testing has passed.

    NOT executed by Claude in this build — see install.ps1's note.
#>

param(
    [int]$MaxRestartAttempts = 3,
    [int]$TimeoutSeconds = 5
)

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ScriptDir
. (Join-Path $ScriptDir "_lib.ps1")

$EnvValues = Get-OrchestratorEnv -ProjectRoot $ProjectRoot
$BackendHost = Get-EnvValue $EnvValues "ORCHESTRATOR_HOST" "127.0.0.1"
$BackendPort = Get-EnvValue $EnvValues "ORCHESTRATOR_PORT" "8000"

$LogsDir = Join-Path $ProjectRoot "logs"
New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null
$StateFile = Join-Path $LogsDir "health_check_restart_count.txt"

try {
    $Response = Invoke-WebRequest -Uri "http://${BackendHost}:${BackendPort}/system/status" `
        -TimeoutSec $TimeoutSeconds -UseBasicParsing
    if ($Response.StatusCode -eq 200) {
        Write-Host "Orchestrator healthy."
        if (Test-Path $StateFile) { Remove-Item $StateFile -Force }
        exit 0
    }
} catch {
    Write-Host "Orchestrator did not respond: $($_.Exception.Message)"
}

$RestartCount = 0
if (Test-Path $StateFile) { $RestartCount = [int](Get-Content $StateFile) }

if ($RestartCount -ge $MaxRestartAttempts) {
    Write-Warning "Orchestrator unhealthy after $RestartCount restart attempts — giving up. Check logs\backend.err.log."
    exit 1
}

Write-Host "Restarting Orchestrator (attempt $($RestartCount + 1) of $MaxRestartAttempts)..."
& (Join-Path $ScriptDir "restart.ps1")
Set-Content -Path $StateFile -Value ($RestartCount + 1)
