from __future__ import annotations

import pythoncom
import win32com.client


class ExcelBridgeError(RuntimeError):
    """Raised when Excel automation cannot complete a requested operation."""


def _excel_app():
    try:
        pythoncom.CoInitialize()
        return win32com.client.GetActiveObject("Excel.Application")
    except Exception as exc:  # pragma: no cover - depends on local Excel
        raise ExcelBridgeError("Excel desktop is not running or is not available through COM.") from exc


def _workbook(app, workbook_name: str | None = None):
    if workbook_name:
        for workbook in app.Workbooks:
            if workbook.Name == workbook_name or workbook.FullName == workbook_name:
                return workbook
        available = [workbook.Name for workbook in app.Workbooks]
        raise ExcelBridgeError(f"Workbook not found: {workbook_name}. Available: {available}")

    try:
        return app.ActiveWorkbook
    except Exception as exc:
        raise ExcelBridgeError("No active workbook is available.") from exc


def _worksheet(workbook, worksheet_name: str | None = None):
    if worksheet_name:
        try:
            return workbook.Worksheets(worksheet_name)
        except Exception as exc:
            names = [sheet.Name for sheet in workbook.Worksheets]
            raise ExcelBridgeError(f"Worksheet not found: {worksheet_name}. Available: {names}") from exc

    try:
        return workbook.ActiveSheet
    except Exception as exc:
        raise ExcelBridgeError("No active worksheet is available.") from exc


def _normalize_values(value):
    if value is None:
        return []

    if not isinstance(value, tuple):
        return [[value]]

    if value and not isinstance(value[0], tuple):
        return [list(value)]

    return [list(row) for row in value]


def _shape(values):
    if not values:
        return {"rows": 0, "columns": 0}
    return {"rows": len(values), "columns": max(len(row) for row in values)}


def _top_left_address(address: str):
    return address.split(":", 1)[0]


def list_workbooks():
    app = _excel_app()
    return [{"name": workbook.Name, "path": workbook.FullName} for workbook in app.Workbooks]


def get_active_workbook():
    app = _excel_app()
    workbook = _workbook(app)
    if workbook is None:
        raise ExcelBridgeError("No active workbook is available.")
    return {"name": workbook.Name, "path": workbook.FullName}


def list_worksheets(workbook_name: str | None = None):
    app = _excel_app()
    workbook = _workbook(app, workbook_name)
    return [sheet.Name for sheet in workbook.Worksheets]


def get_selected_range():
    app = _excel_app()
    selection = app.Selection
    values = _normalize_values(selection.Value)
    return {
        "workbook": app.ActiveWorkbook.Name if app.ActiveWorkbook else None,
        "worksheet": app.ActiveSheet.Name if app.ActiveSheet else None,
        "address": selection.Address,
        "shape": _shape(values),
        "values": values,
    }


def read_range(address: str, workbook_name: str | None = None, worksheet_name: str | None = None):
    app = _excel_app()
    workbook = _workbook(app, workbook_name)
    worksheet = _worksheet(workbook, worksheet_name)
    excel_range = worksheet.Range(address)
    values = _normalize_values(excel_range.Value)
    return {
        "workbook": workbook.Name,
        "worksheet": worksheet.Name,
        "address": excel_range.Address,
        "shape": _shape(values),
        "values": values,
    }


def write_range(
    address: str,
    values: list[list[object]],
    workbook_name: str | None = None,
    worksheet_name: str | None = None,
    confirm: bool = False,
):
    if not values or not all(isinstance(row, list) for row in values):
        raise ExcelBridgeError("Values must be a non-empty two-dimensional array.")

    preview = {
        "workbook": workbook_name,
        "worksheet": worksheet_name,
        "address": address,
        "shape": _shape(values),
        "values": values,
        "confirmed": confirm,
    }

    if not confirm:
        preview["status"] = "preview_only"
        preview["message"] = "No Excel changes were made. Repeat with confirm=true to write these values."
        return preview

    app = _excel_app()
    workbook = _workbook(app, workbook_name)
    worksheet = _worksheet(workbook, worksheet_name)
    row_count = len(values)
    column_count = max(len(row) for row in values)
    top_left = worksheet.Range(_top_left_address(address))

    for row_index, row in enumerate(values, start=1):
        for column_index in range(1, column_count + 1):
            worksheet.Cells(top_left.Row + row_index - 1, top_left.Column + column_index - 1).Value = (
                row[column_index - 1] if column_index <= len(row) else None
            )

    written_range = worksheet.Range(top_left, worksheet.Cells(top_left.Row + row_count - 1, top_left.Column + column_count - 1))

    return {
        "workbook": workbook.Name,
        "worksheet": worksheet.Name,
        "address": written_range.Address,
        "shape": {"rows": row_count, "columns": column_count},
        "status": "written",
    }
