<#
    backup_config.ps1 — Requirement.md FR-028.
    (Named backup_config.ps1, not backup.ps1: "backup" alone is a reserved
    name under 02_Policies/Naming_Policy.md "Reserved Names".)

    Copies config/ (including the real .env — needed to restore secrets) and
    the SQLite database into backup\<timestamp>\ before a configuration
    change. Run this before editing config\.env or upgrading dependencies.

    NOT executed by Claude in this build — see install.ps1's note.
#>

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Destination = Join-Path $ProjectRoot "backup\$Timestamp"
New-Item -ItemType Directory -Force -Path $Destination | Out-Null

$ConfigDir = Join-Path $ProjectRoot "config"
if (Test-Path $ConfigDir) {
    Copy-Item -Path $ConfigDir -Destination (Join-Path $Destination "config") -Recurse
}

$DatabaseDir = Join-Path $ProjectRoot "database"
if (Test-Path $DatabaseDir) {
    Copy-Item -Path $DatabaseDir -Destination (Join-Path $Destination "database") -Recurse
}

Write-Host "Backup written to $Destination"
