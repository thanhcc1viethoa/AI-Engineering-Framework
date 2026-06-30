import win32com.client

import excel_bridge


def main():
    app = win32com.client.Dispatch("Excel.Application")
    app.Visible = False
    workbook = app.Workbooks.Add()
    worksheet = workbook.Worksheets(1)
    worksheet.Name = "SmokeTest"
    worksheet.Range("A1").Value = "hello"
    worksheet.Range("B1").Value = 42

    try:
        print("workbooks=", [w["name"] for w in excel_bridge.list_workbooks()])
        print("sheets=", excel_bridge.list_worksheets(workbook.Name))
        print("read=", excel_bridge.read_range("A1:B1", workbook.Name, "SmokeTest"))
        print("preview=", excel_bridge.write_range("A2:B2", [["ok", 1]], workbook.Name, "SmokeTest", confirm=False)["status"])
        print("after_preview=", excel_bridge.read_range("A2:B2", workbook.Name, "SmokeTest")["values"])
        print("write=", excel_bridge.write_range("A2:B2", [["ok", 1]], workbook.Name, "SmokeTest", confirm=True))
        print("after_write=", excel_bridge.read_range("A2:B2", workbook.Name, "SmokeTest")["values"])
    finally:
        workbook.Close(SaveChanges=False)
        app.Quit()


if __name__ == "__main__":
    main()
