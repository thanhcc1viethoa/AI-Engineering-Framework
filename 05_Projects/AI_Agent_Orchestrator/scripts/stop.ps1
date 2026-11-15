<#
    stop.ps1 — Requirement.md FR-022.

    Stops exactly the processes start.ps1 started, using their recorded PID
    files — never a blanket taskkill by process name (Requirement.md FR-027).

    NOT executed by Claude in this build — see install.ps1's note.
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LogsDir = Join-Path $ProjectRoot "logs"

foreach ($Name in @("backend", "frontend")) {
    $PidFile = Join-Path $LogsDir "$Name.pid"
    if (-not (Test-Path $PidFile)) {
        Write-Host "$Name has no PID file — nothing to stop."
        continue
    }

    $ProcId = Get-Content $PidFile
    if (Get-Process -Id $ProcId -ErrorAction SilentlyContinue) {
        Stop-Process -Id $ProcId -Force
        Write-Host "$Name stopped (PID $ProcId)."
    } else {
        Write-Host "$Name was not running (stale PID $ProcId)."
    }
    Remove-Item $PidFile -Force
}
