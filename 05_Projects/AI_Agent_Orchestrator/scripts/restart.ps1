<#
    restart.ps1 — Requirement.md FR-022.
    NOT executed by Claude in this build — see install.ps1's note.
#>

$ErrorActionPreference = "Stop"
$ScriptDir = $PSScriptRoot

& (Join-Path $ScriptDir "stop.ps1")
Start-Sleep -Seconds 2
& (Join-Path $ScriptDir "start.ps1")
