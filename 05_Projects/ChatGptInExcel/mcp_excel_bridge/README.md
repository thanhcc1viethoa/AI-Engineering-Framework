# Excel MCP Bridge

Local MCP server that lets ChatGPT or another MCP-compatible client operate on open Excel desktop workbooks.

## Scope

MVP tools:

* `list_workbooks`
* `get_active_workbook`
* `list_worksheets`
* `get_selected_range`
* `read_range`
* `write_range`

`write_range` is safe by default. With `confirm=false`, it returns a preview and does not write to Excel. Set `confirm=true` only after reviewing the preview.

## Requirements

* Windows
* Microsoft Excel desktop
* Python 3.11+
* MCP-compatible client

## Install

```powershell
cd 05_Projects/ChatGptInExcel/mcp_excel_bridge
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

Open Excel first, then run:

```powershell
.\Start-ExcelMcp.ps1
```

For stdio MCP client configuration, use:

```json
{
  "mcpServers": {
    "excel": {
      "command": "C:\\Users\\TUF F17\\AI-Engineering-Framework\\05_Projects\\ChatGptInExcel\\mcp_excel_bridge\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\TUF F17\\AI-Engineering-Framework\\05_Projects\\ChatGptInExcel\\mcp_excel_bridge\\server.py"
      ]
    }
  }
}
```

Adjust paths if the repository is moved.

## HTTP transport (for the ChatGPT app)

The ChatGPT app connects to **remote** MCP servers over HTTPS; it cannot launch a
local stdio process. To use it from the ChatGPT app, run the bridge in HTTP mode
and expose it with a tunnel.

```powershell
.\Start-ExcelMcpHttp.ps1
```

This serves the streamable-HTTP MCP endpoint on `http://127.0.0.1:8765` at a
secret path, and prints the local URL plus a bearer token. Secrets are generated
once and stored in `.http-secrets.json` (gitignored).

Environment overrides:

* `EXCEL_MCP_TRANSPORT` - `stdio` (default) or `http`
* `EXCEL_MCP_HOST` / `EXCEL_MCP_PORT` - bind address (default `127.0.0.1:8765`)
* `EXCEL_MCP_PATH` - secret endpoint path (default `/mcp`)
* `EXCEL_MCP_TOKEN` - if set, `Authorization: Bearer <token>` is required

Expose it (Excel must be running) with, for example:

```powershell
cloudflared tunnel --url http://127.0.0.1:8765
```

Then in ChatGPT (Settings -> Connectors -> Developer mode -> Add custom
connector) register:

```
https://<tunnel-host>/mcp/<secret-path-segment>
```

Set the connector authentication to **None**; the unguessable path protects the
endpoint. The ChatGPT connector UI cannot send a custom `Authorization` header,
so leave `EXCEL_MCP_TOKEN` unset for the ChatGPT app (keep it for Agents/API
clients or local testing, which can send the header).

> Security note: this exposes local Excel read/write to the public internet
> behind a secret URL over HTTPS. It deviates from the local-only posture in
> `Requirement.md` (NFR-002). Stop the tunnel when you are not using it, and keep
> `write_range` confirmation (`confirm=true`) in place.

## Safety

* Read tools should use explicit workbook, worksheet, and range arguments.
* Write tools require `confirm=true`.
* Destructive tools are not implemented in the MVP.
* Workbook contents are not logged by default.
