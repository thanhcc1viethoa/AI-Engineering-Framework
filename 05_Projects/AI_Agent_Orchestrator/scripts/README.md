# scripts

Windows operation scripts: `install.ps1`, `start.ps1`, `stop.ps1`, `restart.ps1`, `health_check.ps1`, `backup_config.ps1`. `_lib.ps1` is a shared helper (parses `config/.env`), dot-sourced by the others — not run directly.

(Named `backup_config.ps1`, not `backup.ps1` as the master prompt originally said: "backup" alone is a reserved name under `02_Policies/Naming_Policy.md` "Reserved Names".)

`start.ps1`/`stop.ps1` manage only the backend and the built dashboard. The MCP server is launched by Claude Desktop itself over stdio (see `claude_desktop_config.json` in `Antigravity_Build_Guide.md` section 10), not by these scripts.

These scripts were written in a Linux cloud container with no Windows PowerShell available to run them — they have not been executed. Run `install.ps1` then `start.ps1` for real on the target machine and report any error back.

Owning requirements: FR-022 to FR-024 in `../Requirement.md`.
