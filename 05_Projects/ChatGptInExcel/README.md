# ChatGptInExcel

A personal Windows Excel MCP bridge that lets ChatGPT operate on open Excel desktop workbooks.

> Built on the AI Engineering Framework. This project follows the frozen foundation (`v1.0-foundation`) and its templates.

## Status

| Stage         | Artifact          | Status |
| ------------- | ----------------- | ------ |
| Requirement   | `Requirement.md`  | Draft  |
| Architecture  | `Architecture.md` | Draft  |
| Decisions     | `ADR/` (ADR-0001..0006) | Accepted / Superseded as documented |
| Prototype     | `mcp_excel_bridge/` | Created |
| Optional UI   | `addin/` | Created |

## Single Source of Truth

`Requirement.md` (REQ-001) is the single source of truth for this project.

## Summary

* Primary integration: local MCP server.
* Excel access: Excel desktop COM automation on Windows.
* Safety: writes require explicit confirmation.
* Optional helper: the existing Excel add-in shell remains available for manual prompt workflow.

## Run The MCP Bridge

Open Excel first, then:

```powershell
cd 05_Projects/ChatGptInExcel/mcp_excel_bridge
.\Start-ExcelMcp.ps1
```

Configure your MCP-compatible ChatGPT/client surface to run `server.py` as documented in `mcp_excel_bridge/README.md`.

## Optional Excel Add-in Shell

The helper add-in shell lives in `addin/`.

```powershell
cd 05_Projects/ChatGptInExcel/addin
.\Start-ExcelAddin.ps1
```
