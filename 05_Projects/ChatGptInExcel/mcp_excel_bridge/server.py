from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

import excel_bridge


# Endpoint path for the HTTP transport. Override with a long, secret value
# (e.g. EXCEL_MCP_PATH="/mcp/8f3c...") so the public tunnel URL is unguessable,
# since the ChatGPT connector UI cannot send a custom auth header.
HTTP_PATH = os.environ.get("EXCEL_MCP_PATH", "/mcp")

# Optional bearer token. When set, the HTTP transport requires
# "Authorization: Bearer <token>". Useful for the Agents SDK / API clients and
# local testing. Leave unset for the ChatGPT app connector (which relies on the
# secret path above instead).
HTTP_TOKEN = os.environ.get("EXCEL_MCP_TOKEN")

mcp = FastMCP("excel")


def _tool_error(error: Exception) -> dict[str, str]:
    return {"error": str(error)}


@mcp.tool()
def list_workbooks() -> list[dict[str, Any]] | dict[str, str]:
    """List open Excel desktop workbooks."""
    try:
        return excel_bridge.list_workbooks()
    except Exception as error:
        return _tool_error(error)


@mcp.tool()
def get_active_workbook() -> dict[str, Any] | dict[str, str]:
    """Return the active Excel workbook."""
    try:
        return excel_bridge.get_active_workbook()
    except Exception as error:
        return _tool_error(error)


@mcp.tool()
def list_worksheets(workbook_name: str | None = None) -> list[str] | dict[str, str]:
    """List worksheet names for an open workbook. Uses the active workbook when workbook_name is omitted."""
    try:
        return excel_bridge.list_worksheets(workbook_name)
    except Exception as error:
        return _tool_error(error)


@mcp.tool()
def get_selected_range() -> dict[str, Any] | dict[str, str]:
    """Return the current Excel selection address and values."""
    try:
        return excel_bridge.get_selected_range()
    except Exception as error:
        return _tool_error(error)


@mcp.tool()
def read_range(
    address: str,
    workbook_name: str | None = None,
    worksheet_name: str | None = None,
) -> dict[str, Any] | dict[str, str]:
    """Read values from a specified Excel range such as A1:D10."""
    try:
        return excel_bridge.read_range(address, workbook_name, worksheet_name)
    except Exception as error:
        return _tool_error(error)


@mcp.tool()
def write_range(
    address: str,
    values: list[list[Any]],
    workbook_name: str | None = None,
    worksheet_name: str | None = None,
    confirm: bool = False,
) -> dict[str, Any] | dict[str, str]:
    """Write values to Excel only when confirm=true. With confirm=false, return a preview only."""
    try:
        return excel_bridge.write_range(address, values, workbook_name, worksheet_name, confirm)
    except Exception as error:
        return _tool_error(error)


class BearerAuthMiddleware:
    """Optional ASGI guard that rejects HTTP requests without the bearer token."""

    def __init__(self, app: Any, token: str) -> None:
        self.app = app
        self.expected = f"Bearer {token}"

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        if headers.get(b"authorization", b"").decode() != self.expected:
            await send({
                "type": "http.response.start",
                "status": 401,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({"type": "http.response.body", "body": b"Unauthorized"})
            return

        await self.app(scope, receive, send)


def run_http() -> None:
    import uvicorn

    mcp.settings.streamable_http_path = HTTP_PATH
    app = mcp.streamable_http_app()
    if HTTP_TOKEN:
        app = BearerAuthMiddleware(app, HTTP_TOKEN)

    host = os.environ.get("EXCEL_MCP_HOST", "127.0.0.1")
    port = int(os.environ.get("EXCEL_MCP_PORT", "8765"))
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    transport = os.environ.get("EXCEL_MCP_TRANSPORT", "stdio").lower()
    if transport in ("http", "streamable-http"):
        run_http()
    else:
        mcp.run()
