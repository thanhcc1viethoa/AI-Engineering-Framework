<#
    _lib.ps1 — shared helpers, dot-sourced by the other scripts in this folder.
    Not run directly.
#>

function Get-OrchestratorEnv {
    <#
        Parses config/.env into a hashtable, without executing it. Returns an
        empty hashtable if the file does not exist yet (run install.ps1 first).
    #>
    param([Parameter(Mandatory = $true)][string]$ProjectRoot)

    $EnvFile = Join-Path $ProjectRoot "config\.env"
    $Values = @{}
    if (Test-Path $EnvFile) {
        Get-Content $EnvFile | ForEach-Object {
            if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$') {
                $Values[$Matches[1]] = $Matches[2]
            }
        }
    }
    return $Values
}

function Get-EnvValue {
    param($Values, [string]$Key, [string]$Default)
    if ($Values.ContainsKey($Key) -and $Values[$Key]) { return $Values[$Key] }
    return $Default
}
