# Hướng dẫn bàn giao cho Antigravity — Dự án AI_Agent_Orchestrator

> Tài liệu này dùng để bạn (người dùng) đưa trực tiếp cho Antigravity (chạy trên máy Windows của bạn) làm hướng dẫn lập trình.
> Nguồn yêu cầu đầy đủ, có đánh số: `Requirement.md` (REQ-001) trong cùng thư mục này — Antigravity nên đọc file đó song song.
> Antigravity là bên **thực thi code**. Claude (trong phiên làm việc đám mây) là bên **quản lý/điều phối** — không tự ý đổi vai trò này.

---

## 0. Ranh giới bắt buộc (đọc trước khi code)

Antigravity CHỈ được làm việc trong phạm vi:

* Thư mục dự án này (`05_Projects/AI_Agent_Orchestrator/` trong repo, và/hoặc `D:\AI_AGENT_SYSTEM` khi triển khai thật).
* Không sửa, xóa bất kỳ file nào ngoài phạm vi trên (đặc biệt: không đụng vào `01_Rules/`, `02_Policies/`, `04_Prompts/`, `03_Templates/`, hay bất kỳ project khác trong `05_Projects/`).

Quy tắc bắt buộc (trích từ `Requirement.md` — Business Rules, FR-025 → FR-030):

* Không bao giờ ghi API key/secret vào source code hoặc log. Dùng biến môi trường (`.env`, không commit — đã có trong `.gitignore`).
* Trước khi xóa file, ghi đè cấu hình, cài phần mềm, hoặc làm bất kỳ việc gì ngoài phạm vi trên — **dừng lại và hỏi người dùng xác nhận**, không tự quyết.
* Không chạy Antigravity (chính nó, khi được Orchestrator gọi lại sau này — xem mục 5) ở chế độ bỏ qua toàn bộ kiểm soát quyền.
* Không tuyên bố một giai đoạn "đã xong" nếu chưa chạy thử và thấy kết quả thật.
* Không cài đặt gì trùng với phần mềm đã có sẵn và đang chạy tốt trên máy.

Nếu thiếu thông tin để quyết định (ví dụ: chưa rõ Antigravity CLI có chế độ non-interactive hay không, chưa rõ hạn mức Muse4AI) — **dừng và báo lại**, không tự đoán. Các điểm chưa xác minh đã được liệt kê ở `Requirement.md` mục **Assumptions** (AS-001 đến AS-004).

---

## 1. Cấu trúc thư mục đã khởi tạo sẵn

```
05_Projects/AI_Agent_Orchestrator/
├── README.md                     ← tổng quan dự án
├── Requirement.md                ← yêu cầu đầy đủ (REQ-001)
├── Antigravity_Build_Guide.md    ← chính là file này
├── backend/                      ← FastAPI: Task/Agent/Workflow Manager, SQLite, log, report
├── frontend/                     ← React dashboard (7 trang)
├── mcp_server/                   ← MCP tools cho Claude Desktop
├── agents/
│   ├── antigravity/               ← adapter gọi Antigravity CLI
│   ├── muse/                      ← adapter gọi Muse4AI
│   ├── python/                    ← Python Automation Agent
│   └── qa/                        ← QA Agent
├── workflows/                    ← định nghĩa workflow (task graph) đã lưu
├── projects/                     ← thư mục làm việc riêng cho từng task Antigravity
├── output/{videos,code,reports}  ← sản phẩm sinh ra (không commit git)
├── database/                     ← file SQLite (không commit git)
├── logs/                         ← log runtime (không commit git)
├── config/                       ← cấu hình không chứa secret
├── scripts/                      ← install/start/stop/restart/health_check/backup .ps1
└── backup/                       ← bản sao lưu cấu hình (không commit git)
```

Mỗi thư mục con đã có `README.md` riêng ghi rõ nó hiện thực Functional Requirement (FR-xxx) nào trong `Requirement.md`.

---

## 2. Nguyên tắc triển khai: làm theo từng giai đoạn, không nhảy cóc (FR-031)

Bắt buộc theo đúng thứ tự 10 giai đoạn sau. Sau mỗi giai đoạn: **chạy thử thật, ghi nhận lỗi, sửa xong rồi mới sang giai đoạn tiếp theo.** Không viết toàn bộ hệ thống rồi mới test một lần.

1. Khảo sát môi trường Windows
2. Thiết lập thư mục, Python venv, Node.js project
3. Backend + Database (Task Manager, Agent Manager, Workflow Manager, SQLite)
4. MCP Server (11 tools)
5. Tích hợp Antigravity CLI (Orchestrator gọi Antigravity CLI làm agent lập trình)
6. Tích hợp Muse4AI
7. Tích hợp Claude Desktop (qua MCP)
8. Web Dashboard (React, 7 trang)
9. Kiểm thử toàn hệ thống
10. Chạy nền + tự khởi động cùng Windows

---

## 3. Giai đoạn 1 — Antigravity tự khảo sát máy (khác với Claude)

Vì Antigravity chạy trực tiếp trên máy Windows của bạn (Claude trong phiên đám mây thì không có quyền truy cập máy này), **Antigravity tự chạy được bước khảo sát này** — không cần đợi Claude soạn script riêng.

Yêu cầu Antigravity chạy trong PowerShell và ghi lại toàn bộ kết quả thành file `output/reports/environment_report.md`:

```powershell
# Hệ điều hành
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture

# CPU / RAM
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object @{N='RAM_GB';E={[math]::Round($_.TotalPhysicalMemory/1GB,2)}}

# Ổ đĩa (đặc biệt ổ D)
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N='Used_GB';E={[math]::Round($_.Used/1GB,2)}}, @{N='Free_GB';E={[math]::Round($_.Free/1GB,2)}}

# Python / pip
python --version; pip --version

# Node.js / npm
node --version; npm --version

# Antigravity CLI — kiểm tra chính nó
agy --version 2>$null; agy --help 2>$null

# Claude Desktop (thư mục cài đặt thường gặp)
Test-Path "$env:LOCALAPPDATA\Programs\Claude"
Test-Path "$env:APPDATA\Claude"

# MCP server hiện có (đừng xóa/ghi đè)
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue

# Tiến trình có thể xung đột cổng mặc định của Orchestrator (ví dụ 8000, 5173)
Get-NetTCPConnection -LocalPort 8000,5173 -ErrorAction SilentlyContinue
```

Sau khi chạy xong:

* Nếu ổ `D:` không tồn tại hoặc dung lượng trống dưới khoảng vài GB, **dừng lại, đề xuất ổ thay thế, hỏi người dùng xác nhận** trước khi tạo `AI_AGENT_SYSTEM` — không tự ý chọn ổ khác.
* Nếu phát hiện cấu hình MCP Server đã tồn tại trong `claude_desktop_config.json`, **không ghi đè** — chỉ thêm entry mới cho Orchestrator của dự án này.
* Dán nội dung `output/reports/environment_report.md` lại cho người dùng mang về cho Claude đối chiếu với `Requirement.md` trước khi sang Giai đoạn 2.

---

## 4. Giai đoạn 2 — Thiết lập dự án

* Tạo virtual environment Python trong `backend/.venv` (hoặc dùng `agents/*` dùng chung một venv ở `backend/.venv` nếu hợp lý).
* Khởi tạo `backend/requirements.txt` tối thiểu: `fastapi`, `uvicorn`, `pydantic`, `websockets`, driver SQLite chuẩn của Python (`sqlite3`, có sẵn trong thư viện chuẩn).
* Khởi tạo `frontend/package.json` bằng công cụ scaffold React tiêu chuẩn (ví dụ Vite + React).
* Khởi tạo `mcp_server/requirements.txt` với SDK MCP chính thức mới nhất (tra tài liệu chính thức, không đoán tên gói).
* Tạo `config/.env.example` liệt kê tên biến môi trường cần thiết (không có giá trị thật).

---

## 5. Giai đoạn 3 → 10 — Tham chiếu trực tiếp Requirement.md

Từ Giai đoạn 3 trở đi, không lặp lại chi tiết ở đây để tránh hai nguồn sự thật mâu thuẫn nhau — Antigravity đọc trực tiếp các mục sau trong `Requirement.md`:

| Giai đoạn | Mục trong Requirement.md |
| --------- | -------------------------- |
| 3. Backend + Database | FR-003, FR-004, FR-005, FR-020, FR-021, NFR-002 |
| 4. MCP Server | FR-006, FR-011 |
| 5. Tích hợp Antigravity CLI | FR-007, AS-001 (CHƯA XÁC MINH — kiểm tra `agy --help` thật kỹ trước khi code, báo lại nếu không có chế độ non-interactive) |
| 6. Tích hợp Muse4AI | FR-008, AS-002 (CHƯA XÁC MINH — kiểm tra tài liệu + tài khoản thật trước khi code) |
| 7. Tích hợp Claude Desktop | FR-011 |
| 8. Web Dashboard | FR-012 đến FR-019 |
| 9. Kiểm thử toàn hệ thống | Acceptance Criteria AC-001 đến AC-012 |
| 10. Chạy nền + tự khởi động | FR-022, FR-023, FR-024 |

Lưu ý đặc biệt cho Giai đoạn 5: Orchestrator (do Antigravity viết) sẽ **gọi lại chính Antigravity CLI** như một sub-process để thực thi task lập trình khác — đây là hai vai trò khác nhau của cùng một công cụ: "Antigravity-người-viết-Orchestrator" và "Antigravity-được-Orchestrator-gọi-làm-agent". Đừng nhầm lẫn hai vai trò này khi thiết kế.

---

## 6. Báo cáo sau mỗi giai đoạn

Sau khi hoàn thành và tự kiểm thử một giai đoạn, Antigravity (hoặc bạn) nên tóm tắt theo mẫu sau rồi dán lại cho Claude để đối chiếu với `Requirement.md` và cập nhật `Architecture.md`/ADR nếu cần:

```
Giai đoạn: <số và tên>
File đã tạo/sửa: <danh sách>
Lệnh đã chạy để kiểm thử: <danh sách>
Kết quả thật (không suy đoán): <...>
Lỗi gặp phải và cách khắc phục: <...>
Việc còn thiếu / cần Claude quyết định: <...>
```

---

## 7. Việc Claude sẽ làm song song

* Khi nhận được báo cáo Giai đoạn 1, Claude sẽ cập nhật `Requirement.md` (đánh dấu AS-003 đã xác minh) và bắt đầu soạn `Architecture.md` chính thức cho dự án.
* Review (`/review`) sẽ được chạy trên từng artifact trước khi nó được coi là Approved, theo đúng Quality Gate của repo (`CLAUDE.md`).
