# Sổ Tay Hướng Dẫn Antigravity — Dự án AI_Agent_Orchestrator

> Đưa trực tiếp file này cho Antigravity (chạy trên máy Windows của bạn) làm sổ tay lập trình đầy đủ.
> Nguồn yêu cầu gốc, có đánh số: `Requirement.md` (REQ-001) cùng thư mục — mọi mã FR-xxx/NFR-xxx/AS-xxx nhắc tới bên dưới đều tra được ở đó.
> Antigravity là bên **thực thi code**. Claude (phiên làm việc đám mây) là bên **quản lý/điều phối/kiểm tra**.
> Các thiết kế cụ thể (schema bảng, danh sách endpoint, tham số MCP tool, số mặc định retry/timeout...) trong sổ tay này là **đề xuất thiết kế của Claude** để Antigravity có thể bắt tay vào code ngay — không phải điều khoản cố định. Antigravity/người dùng có thể điều chỉnh, nhưng nếu đổi khác phần khung sườn chính (ví dụ đổi SQLite sang Postgres) thì phải dừng lại hỏi người dùng trước, vì đó là lệch khỏi `Requirement.md`.

---

# 0. Ranh giới bắt buộc — đọc trước khi code bất cứ dòng nào

* Chỉ làm việc trong thư mục dự án này (`05_Projects/AI_Agent_Orchestrator/` trong repo, và `D:\AI_AGENT_SYSTEM` khi triển khai thật trên Windows).
* Không sửa/xóa file ngoài phạm vi trên — đặc biệt không đụng `01_Rules/`, `02_Policies/`, `04_Prompts/`, `03_Templates/`, hay project khác trong `05_Projects/`.
* Không bao giờ ghi API key/secret vào source code, config đã commit, hay log. Tất cả secret đi qua biến môi trường (`config/.env`, không commit — xem `.gitignore`).
* Trước khi: xóa file, ghi đè cấu hình đang có, cài phần mềm mới, mở cổng ra ngoài Internet, hoặc làm bất kỳ việc gì ngoài phạm vi — **dừng lại, hỏi người dùng xác nhận**. Không tự quyết.
* Không chạy Antigravity (khi tự nó bị Orchestrator gọi lại ở Giai đoạn 5) ở chế độ bỏ qua toàn bộ kiểm soát quyền.
* Không tuyên bố một giai đoạn "xong" nếu chưa chạy thử thật và thấy kết quả thật — không suy đoán kết quả.
* Không cài lại phần mềm đã có sẵn và đang chạy tốt trên máy (Python, Node, v.v.) — chỉ kiểm tra và tái sử dụng.
* Nếu thiếu thông tin để quyết định (vd: Antigravity CLI có chế độ non-interactive hay không, hạn mức Muse4AI) — **dừng và báo lại**, không tự đoán. Các điểm này đã được đánh dấu AS-001 → AS-004 trong `Requirement.md`.

---

# 1. Tổng quan kiến trúc

```
USER
 ├── Claude Desktop ──┐
 └── Web Dashboard ───┤
                       ▼
            AI ORCHESTRATOR (backend/, FastAPI)
            ├── Task Manager         (FR-003)
            ├── Agent Manager        (FR-004)
            ├── Workflow Manager     (FR-005)
            ├── SQLite (database/)   (NFR-002)
            ├── Logging (logs/)      (NFR-004)
            └── Report Generator     (FR-020)
                       │
         ┌─────────────┼───────────────┬──────────────┐
         ▼             ▼               ▼              ▼
  agents/antigravity agents/muse  agents/python   agents/qa
  (Antigravity CLI)  (Muse4AI)    (automation)    (QA check)
```

MCP Server (`mcp_server/`) là cổng duy nhất để Claude Desktop nói chuyện với Orchestrator (FR-006, FR-011). Dashboard (`frontend/`) nói chuyện với backend qua REST + WebSocket (FR-019).

---

# 2. Cấu trúc thư mục (đã khởi tạo sẵn trong repo)

```
05_Projects/AI_Agent_Orchestrator/
├── README.md / Requirement.md / Antigravity_Build_Guide.md (file này)
├── backend/        FastAPI: Task/Agent/Workflow Manager, SQLite, log, report
├── frontend/       React dashboard (7 trang)
├── mcp_server/     MCP tools cho Claude Desktop
├── agents/{antigravity,muse,python,qa}/   adapter cho từng agent
├── workflows/      định nghĩa workflow (task graph) đã lưu
├── projects/       thư mục làm việc riêng cho từng task Antigravity
├── output/{videos,code,reports}  sản phẩm sinh ra (không commit git)
├── database/       file SQLite (không commit git)
├── logs/           log runtime (không commit git)
├── config/         cấu hình không chứa secret
├── scripts/        install/start/stop/restart/health_check/backup .ps1
└── backup/         bản sao lưu cấu hình (không commit git)
```

Mỗi thư mục con có `README.md` riêng trỏ về đúng FR-xxx liên quan.

---

# 3. Nguyên tắc: làm theo 10 giai đoạn, không nhảy cóc (FR-031)

Sau mỗi giai đoạn: chạy thử thật → ghi log kết quả → sửa lỗi → rồi mới sang giai đoạn kế. Không viết toàn bộ rồi mới test một lần.

| # | Giai đoạn |
| - | --------- |
| 1 | Khảo sát môi trường Windows |
| 2 | Thiết lập thư mục, Python venv, Node.js project |
| 3 | Backend + Database |
| 4 | MCP Server (11 tools) |
| 5 | Tích hợp Antigravity CLI |
| 6 | Tích hợp Muse4AI |
| 7 | Tích hợp Claude Desktop |
| 8 | Web Dashboard |
| 9 | Kiểm thử toàn hệ thống |
| 10 | Chạy nền + tự khởi động cùng Windows |

---

# 4. GIAI ĐOẠN 1 — Khảo sát môi trường (Antigravity tự chạy)

Antigravity chạy trực tiếp trên máy Windows nên **tự làm được** bước này — không cần đợi script riêng từ Claude. Chạy PowerShell, ghi kết quả vào `output/reports/environment_report.md`:

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

# Claude Desktop
Test-Path "$env:LOCALAPPDATA\Programs\Claude"
Test-Path "$env:APPDATA\Claude"

# MCP server hiện có (đừng xóa/ghi đè)
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue

# Cổng có thể xung đột với Orchestrator (mặc định đề xuất: 8000 backend, 5173 frontend dev, 8765 mcp)
Get-NetTCPConnection -LocalPort 8000,5173,8765 -ErrorAction SilentlyContinue
```

**Quy tắc quyết định:**
* Ổ `D:` không tồn tại hoặc trống dưới ~10 GB → đề xuất ổ thay thế, hỏi xác nhận, KHÔNG tự chọn.
* Đã có entry MCP server khác trong `claude_desktop_config.json` → không ghi đè, chỉ thêm entry mới cho project này ở Giai đoạn 7.
* Thiếu Python/Node → báo cho người dùng cài (link tải chính thức), không tự ý cài nếu chưa xác nhận (FR-030).

Dán `output/reports/environment_report.md` lại cho người dùng mang về Claude trước khi sang Giai đoạn 2.

---

# 5. GIAI ĐOẠN 2 — Thiết lập dự án

```powershell
# Backend: virtual environment
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]" pydantic websockets python-dotenv
pip freeze > requirements.txt

# MCP server: venv riêng (hoặc dùng chung .venv của backend nếu đơn giản hơn)
cd ..\mcp_server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Cài SDK MCP chính thức — tra PyPI để lấy tên/version mới nhất, không đoán
pip install mcp
pip freeze > requirements.txt

# Frontend: scaffold React (Vite)
cd ..\frontend
npm create vite@latest . -- --template react
npm install
```

Tạo `config/.env.example` (không có giá trị thật, chỉ tên biến):

```
ORCHESTRATOR_HOST=127.0.0.1
ORCHESTRATOR_PORT=8000
MCP_PORT=8765
SQLITE_PATH=../database/orchestrator.db
MUSE4AI_API_KEY=
ANTIGRAVITY_CLI_PATH=agy
DASHBOARD_JWT_SECRET=
MAX_CONCURRENT_TASKS=3
MAX_TASK_TIMEOUT_SECONDS=1800
MAX_FIX_RETRIES=3
```

> Các số `MAX_CONCURRENT_TASKS=3`, `MAX_TASK_TIMEOUT_SECONDS=1800`, `MAX_FIX_RETRIES=3` là **đề xuất mặc định** của Claude vì `Requirement.md` (AS-004) chưa quy định con số cụ thể. Để trong `.env` để người dùng chỉnh mà không cần sửa code.

---

# 6. GIAI ĐOẠN 3 — Backend + Database

## 6.1 Schema SQLite (`database/orchestrator.db`)

```sql
CREATE TABLE tasks (
    task_id         TEXT PRIMARY KEY,
    task_name       TEXT NOT NULL,
    description     TEXT,
    assigned_agent  TEXT NOT NULL,          -- antigravity | muse | python | qa
    priority        TEXT NOT NULL DEFAULT 'Medium',  -- Critical|High|Medium|Low|Optional
    status          TEXT NOT NULL DEFAULT 'PENDING', -- PENDING|QUEUED|RUNNING|WAITING|COMPLETED|FAILED|CANCELLED
    payload         TEXT,                   -- JSON: dữ liệu đầu vào riêng của task
    result          TEXT,                   -- JSON: kết quả
    error_message   TEXT,
    output_path     TEXT,
    workflow_id     TEXT,                   -- NULL nếu task độc lập
    created_at      TEXT NOT NULL,
    started_at      TEXT,
    completed_at    TEXT
);

CREATE TABLE agents (
    agent_id        TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    type            TEXT NOT NULL,          -- claude | antigravity | muse | python | qa
    status          TEXT NOT NULL DEFAULT 'IDLE',  -- IDLE|BUSY|OFFLINE|ERROR
    capabilities    TEXT,                   -- JSON array
    current_task    TEXT,                   -- task_id hoặc NULL
    last_active     TEXT,
    error_log       TEXT
);

CREATE TABLE workflows (
    workflow_id     TEXT PRIMARY KEY,
    workflow_name   TEXT NOT NULL,
    goal            TEXT NOT NULL,
    task_ids        TEXT NOT NULL,          -- JSON array, đúng thứ tự thực thi
    status          TEXT NOT NULL DEFAULT 'PENDING',
    created_at      TEXT NOT NULL,
    completed_at    TEXT
);
```

Khớp đúng field trong FR-003 (Task) và FR-004 (Agent).

## 6.2 Cấu trúc code backend đề xuất

```
backend/
├── main.py              # khởi tạo FastAPI app, include routers
├── db.py                # kết nối SQLite, migrate schema khi khởi động
├── models.py            # Pydantic models: Task, Agent, Workflow
├── routers/
│   ├── tasks.py         # /tasks/*
│   ├── agents.py        # /agents/*
│   ├── workflows.py     # /workflows/*
│   └── system.py        # /system/*, /ws
├── services/
│   ├── task_manager.py      # FR-003
│   ├── agent_manager.py     # FR-004
│   ├── workflow_manager.py  # FR-005
│   └── report_generator.py  # FR-020
└── logger.py             # ghi logs/orchestrator.log, không ghi secret
```

## 6.3 REST endpoints (nền cho MCP tools ở Giai đoạn 4)

| Method | Path | Mô tả |
| ------ | ---- | ----- |
| POST | `/tasks` | Tạo task mới (submit_task) |
| GET | `/tasks` | Danh sách task, filter theo `status`, `assigned_agent` |
| GET | `/tasks/{task_id}` | Chi tiết + kết quả một task |
| DELETE | `/tasks/{task_id}` | Hủy task (chỉ khi đang PENDING/QUEUED/RUNNING) |
| GET | `/agents` | Danh sách agent |
| GET | `/agents/{agent_id}` | Chi tiết một agent |
| POST | `/workflows` | Tạo + thực thi workflow từ một `goal` |
| GET | `/workflows/{workflow_id}` | Trạng thái workflow |
| GET | `/system/status` | Tổng quan hệ thống (cho Overview + health_check.ps1) |
| WS | `/ws` | Đẩy cập nhật realtime trạng thái task/agent cho Dashboard |

Mỗi endpoint ghi log request/response (trừ giá trị secret) vào `logs/orchestrator.log` (NFR-004).

---

# 7. GIAI ĐOẠN 4 — MCP Server (đúng 11 tool, không thêm/bớt)

Mỗi tool bên dưới gọi thẳng endpoint tương ứng ở mục 6.3. Không tạo tool nào chưa có chức năng thật đứng sau nó (quy tắc trong master prompt gốc).

| Tool | Tham số | Kiểu | Bắt buộc | Trả về |
| ---- | ------- | ---- | -------- | ------ |
| `submit_task` | `task_name`, `description`, `assigned_agent` (enum: antigravity\|muse\|python\|qa), `priority` (enum, mặc định Medium), `payload` (object, dữ liệu riêng của loại agent) | string/string/string/string/object | `task_name`, `description`, `assigned_agent` bắt buộc | `{task_id, status}` |
| `get_task_status` | `task_id` | string | bắt buộc | `{task_id, status, started_at, completed_at}` |
| `get_task_result` | `task_id` | string | bắt buộc | `{task_id, status, result, error_message, output_path}` |
| `list_tasks` | `status` (optional), `assigned_agent` (optional), `limit` (int, mặc định 50) | string/string/int | không | mảng task tóm tắt |
| `cancel_task` | `task_id` | string | bắt buộc | `{task_id, status: "CANCELLED"}` |
| `get_agent_status` | `agent_id` | string | bắt buộc | `{agent_id, name, type, status, current_task, last_active, error_log}` |
| `list_agents` | — | — | — | mảng agent tóm tắt |
| `execute_workflow` | `workflow_name`, `goal`, `steps` (optional — nếu bỏ trống, Workflow Manager tự phân rã `goal`) | string/string/array | `workflow_name`, `goal` bắt buộc | `{workflow_id, task_ids}` |
| `create_video` | `prompt`, `duration_seconds` (optional), `resolution` (optional), `style` (optional) | string/int/string/string | `prompt` bắt buộc | `{task_id, status: "QUEUED"}` |
| `get_video_status` | `task_id` | string | bắt buộc | `{task_id, job_id, status, progress}` |
| `get_system_status` | — | — | — | `{agents_total, agents_active, tasks_running, tasks_completed, tasks_failed, videos_created, uptime_seconds}` |

> Tham số của `create_video`/`get_video_status` có thể cần đổi tên/đơn vị cho khớp API thật của Muse4AI (xem Giai đoạn 6, AS-002) — xác nhận lại tài liệu Muse4AI trước khi chốt.

---

# 8. GIAI ĐOẠN 5 — Tích hợp Antigravity CLI (FR-007)

Lưu ý vai trò kép: **Antigravity-người-viết-Orchestrator** (đang đọc sổ tay này) khác với **Antigravity-bị-Orchestrator-gọi-làm-agent-thực-thi** (đoạn code sắp viết). Đừng nhầm.

Quy trình `agents/antigravity/`:

1. Kiểm tra `agy --version` và trạng thái đăng nhập trước khi dùng.
2. Khi nhận một task `assigned_agent == "antigravity"`: tạo thư mục riêng `projects/<task_id>/`, chỉ cấp quyền Antigravity trong thư mục này (FR-007, NFR-007).
3. Gọi CLI qua `subprocess` ở **chế độ không tương tác** nếu `agy --help` xác nhận có hỗ trợ (AS-001). Nếu không có, dừng lại, báo cho người dùng — không giả định cú pháp.
4. Áp dụng timeout từ `MAX_TASK_TIMEOUT_SECONDS` (mục 5); nếu vượt timeout → kill process, set `status=FAILED`, `error_message="timeout"`.
5. Ghi lại: lệnh đã chạy, thời điểm bắt đầu/kết thúc, stdout/stderr, exit code → vào `logs/` và cột `result`/`error_message` của task.
6. Nếu `exit code != 0` → `status=FAILED`; cho phép chạy lại có kiểm soát tối đa `MAX_FIX_RETRIES` lần (mục 5), mỗi lần retry ghi log riêng.
7. Không bao giờ truyền cờ bỏ qua toàn bộ xác nhận quyền của Antigravity.

---

# 9. GIAI ĐOẠN 6 — Tích hợp Muse4AI / Meta Muse (FR-008)

**Trước khi viết code thật:** đọc tài liệu Muse4AI chính thức mới nhất và thông tin tài khoản thật của người dùng để xác nhận AS-002 (endpoint, tham số, hạn mức). Không đoán URL/tham số.

Khung adapter đề xuất (`agents/muse/`):

```python
def submit_video(prompt: str, **params) -> str:
    """Gửi yêu cầu tạo video, trả về job_id. Ngăn gửi trùng: kiểm tra
    task đang PENDING/QUEUED/RUNNING với cùng prompt trước khi gửi mới."""

def get_job_status(job_id: str) -> dict:
    """Trả về trạng thái job thật từ Muse4AI (không suy đoán tiến độ)."""

def download_video(job_id: str, dest_dir: str = "../../output/videos") -> str:
    """Tải video khi job hoàn tất và API hỗ trợ tải xuống; trả về đường dẫn file."""
```

Ghi log thời gian submit → complete, lỗi API, và không gửi nhiều request tạo video trùng lặp cho cùng một yêu cầu (quy tắc business rule trong `Requirement.md`).

---

# 10. GIAI ĐOẠN 7 — Tích hợp Claude Desktop (FR-011)

1. Mở `%APPDATA%\Claude\claude_desktop_config.json`.
2. **Không xóa entry `mcpServers` đã có** — chỉ thêm một entry mới, ví dụ:

```json
{
  "mcpServers": {
    "ai-agent-orchestrator": {
      "command": "python",
      "args": ["D:\\AI_AGENT_SYSTEM\\mcp_server\\main.py"]
    }
  }
}
```

(đường dẫn thật thay theo nơi triển khai cuối cùng — xem Giai đoạn 10)

3. Lưu file, khởi động lại Claude Desktop, xác nhận 11 tool xuất hiện trong danh sách MCP tools.
4. Nếu file cấu hình chưa tồn tại — tạo mới, không giả định cấu trúc ngoài key `mcpServers`.

---

# 11. GIAI ĐOẠN 8 — Web Dashboard (FR-012 → FR-019)

Toàn bộ giao diện bằng tiếng Việt (NFR-006). Gợi ý: React Router cho 7 trang, một hook `useOrchestratorSocket()` lắng nghe `/ws` để cập nhật realtime, gọi REST (mục 6.3) cho các thao tác CRUD.

| Trang | Route | Dữ liệu/API chính |
| ----- | ----- | -------------------- |
| Overview | `/` | `GET /system/status` |
| Agent Monitor | `/agents` | `GET /agents` + cập nhật qua WebSocket |
| Task Manager | `/tasks` | `GET/POST/DELETE /tasks` (tạo, xem, tìm kiếm, lọc theo status, dừng) |
| Workflow | `/workflows/:id` | `GET /workflows/{id}` — vẽ sơ đồ bước + agent liên quan |
| Video Manager | `/videos` | lọc `tasks` theo `assigned_agent == "muse"`, hiển thị path trong `output/videos` |
| System Logs | `/logs` | đọc/stream `logs/orchestrator.log` |
| Settings | `/settings` | đọc/ghi `config/` (không hiển thị giá trị secret thật) |

Đăng nhập dashboard bắt buộc trước khi vào bất kỳ trang nào (FR-025) — dùng JWT đơn giản với `DASHBOARD_JWT_SECRET` từ `.env`.

---

# 12. GIAI ĐOẠN 9 — Kiểm thử toàn hệ thống

Chạy từng mục, ghi kết quả thật (đạt/không đạt), không suy đoán:

| AC | Cách kiểm thử |
| -- | -------------- |
| AC-001 | Mở Claude Desktop, gọi `list_agents` qua MCP, nhận phản hồi thật |
| AC-002 | Mở dashboard, đăng nhập, xem trang Overview tải được dữ liệu |
| AC-003 | Gọi `submit_task` với `assigned_agent="antigravity"`, xác nhận task chuyển QUEUED→RUNNING |
| AC-004 | Task Antigravity thật hoàn tất với `status=COMPLETED` và `output_path` tồn tại |
| AC-005 | `agents/muse` kết nối thành công tới tài khoản Muse4AI thật |
| AC-006 | `create_video` sinh ra ít nhất một video thật trong `output/videos` |
| AC-007 | Một task `assigned_agent="python"` chạy xong với kết quả thật |
| AC-008 | QA Agent trả về pass/fail thật cho một output đã có |
| AC-009 | Claude nhận `get_task_result` và tạo báo cáo khớp dữ liệu thật |
| AC-010 | Restart backend, xác nhận lịch sử task trong SQLite còn nguyên |
| AC-011 | Chạy `stop.ps1` rồi `start.ps1`, dịch vụ hoạt động lại bình thường |
| AC-012 | Sau toàn bộ quá trình, cấu hình MCP cũ và dữ liệu cũ trên máy không bị mất |

---

# 13. GIAI ĐOẠN 10 — Chạy nền + tự khởi động Windows (FR-022 → FR-024)

## 13.1 Script (`scripts/`)

* `install.ps1`: tạo venv, `pip install -r requirements.txt` cho `backend/` và `mcp_server/`, `npm install && npm run build` cho `frontend/`.
* `start.ps1`: khởi động theo thứ tự — backend (uvicorn) → mcp_server → phục vụ `frontend/dist` (vd. qua `npx serve` hoặc static file của FastAPI); ghi PID mỗi tiến trình vào `logs/*.pid`.
* `stop.ps1`: đọc file `.pid`, dừng đúng tiến trình đó (không `taskkill` hàng loạt theo tên tiến trình chung chung).
* `restart.ps1`: gọi `stop.ps1` rồi `start.ps1`.
* `health_check.ps1`: gọi `GET /system/status`; nếu không phản hồi trong vài giây, ghi log và tự gọi `restart.ps1` (giới hạn số lần thử lại, tránh vòng lặp khởi động lại vô hạn).
* `backup.ps1`: copy `config/` và file SQLite trong `database/` sang `backup/<timestamp>/` trước khi cho phép thay đổi cấu hình.

## 13.2 Tự khởi động cùng Windows

Chỉ bật **sau khi Giai đoạn 9 đã test đạt toàn bộ**. Hai lựa chọn — chọn cái đơn giản nhất và xác nhận với người dùng trước khi bật:

* **Task Scheduler** (`schtasks`): tạo task chạy `start.ps1` khi đăng nhập Windows (`/sc onlogon`). Dễ gỡ, không cần quyền admin cài service.
* **NSSM** (Non-Sucking Service Manager): đăng ký `start.ps1` thành Windows Service thật, tự chạy kể cả khi chưa đăng nhập. Cần cài thêm NSSM (xác nhận người dùng trước).

Dùng `health_check.ps1` kèm Task Scheduler (chạy lặp mỗi vài phút) để phát hiện tiến trình treo và tự phục hồi (FR-024).

---

# 14. Báo cáo sau mỗi giai đoạn

```
Giai đoạn: <số và tên>
File đã tạo/sửa: <danh sách>
Lệnh đã chạy để kiểm thử: <danh sách>
Kết quả thật (không suy đoán): <...>
Lỗi gặp phải và cách khắc phục: <...>
Việc còn thiếu / cần Claude hoặc người dùng quyết định: <...>
```

Dán báo cáo này lại cho người dùng mang về cho Claude sau mỗi giai đoạn, để đối chiếu với `Requirement.md` và cập nhật `Architecture.md`/ADR nếu thiết kế thực tế khác với sổ tay này.

---

# 15. Việc Claude làm song song (không phải việc của Antigravity)

* Nhận báo cáo Giai đoạn 1 → cập nhật `Requirement.md` (đánh dấu AS-003 đã xác minh) → soạn `Architecture.md` + ADR chính thức cho repo.
* Chạy `/review` trên từng artifact theo Quality Gate của `CLAUDE.md` trước khi coi là Approved.
* Nếu báo cáo bất kỳ giai đoạn nào cho thấy thiết kế trong sổ tay này không khớp thực tế máy/API — Claude sẽ sửa sổ tay và `Requirement.md`, không để hai tài liệu mâu thuẫn nhau.
