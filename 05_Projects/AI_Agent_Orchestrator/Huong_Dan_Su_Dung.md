# Hướng Dẫn Sử Dụng — AI Agent Orchestrator

> Dành cho người vận hành (bạn), sau khi code đã có trên máy Windows.
> Nếu phần cài đặt/khởi động dưới đây báo lỗi khác với mô tả, đó là vì các script PowerShell trong `scripts/` được viết trong môi trường không có Windows để chạy thử thật (xem `README.md` mục Status) — ghi lại lỗi và đưa cho Claude để sửa.

---

## 0. Trước khi bắt đầu

Cần có trên máy Windows:

* Python 3.10+ và pip
* Node.js 18+ và npm
* (Tùy chọn, để dùng thật agent code) Antigravity CLI đã đăng nhập
* (Tùy chọn, để dùng thật agent video) Ứng dụng [Muse4AI](https://muse4ai.andrewbabo.com) đã cài và đăng nhập tài khoản Meta Muse của bạn — đây là app chạy ngay trên máy bạn (cổng mặc định `127.0.0.1:47821`), không phải một tài khoản cloud riêng
* Claude Desktop đã cài

Lấy code về máy (mở PowerShell hoặc Git Bash):

```powershell
git clone https://github.com/thanhcc1viethoa/AI-Engineering-Framework.git
cd AI-Engineering-Framework
git checkout ccr-af9e22f6-rhzlvb
cd 05_Projects\AI_Agent_Orchestrator
```

(Nếu bạn muốn triển khai đúng theo thiết kế ban đầu ở `D:\AI_AGENT_SYSTEM`, copy toàn bộ thư mục `AI_Agent_Orchestrator` này sang đó sau khi clone.)

---

## 0.1. Cài đặt & cấu hình Muse4AI (nếu muốn dùng agent video)

Muse4AI (`github.com/andrew-babo/muse4ai`) là một **ứng dụng Windows riêng, cài độc lập** với dự án này — nó tự động hóa phiên Meta Muse bạn đã đăng nhập, và là thứ Orchestrator gọi tới khi bạn giao việc cho agent `muse`. Bỏ qua mục này nếu bạn chưa cần tạo video.

### Cài đặt

**Cách 1 — nhanh nhất:** vào https://muse4ai.andrewbabo.com/download, tải installer, chạy. Windows sẽ cảnh báo "file chưa ký" — chọn **More info → Run anyway**. App sẽ tự kiểm tra và cài bản mới từ **Settings › About**, không cần quay lại trang tải.

**Cách 2 — chạy từ source** (cần Node.js 22+):

```powershell
git clone https://github.com/andrew-babo/muse4ai.git
cd muse4ai\desktop
npm install
npm run build
npm start
```

App mở ra, phục vụ API tại `http://127.0.0.1:47821`.

### Cấu hình

1. Trong app, vào **Accounts**, thêm tài khoản Meta Muse của bạn (đăng nhập qua giao diện trong app; phiên đăng nhập chỉ lưu trên máy bạn, ở `%APPDATA%\MuseStudio`).
2. Vào **Settings › API & agent**:
   - Bấm tạo **API key** — dạng `msk_...`, **chỉ hiện một lần**, copy lưu lại ngay (ví dụ dán tạm vào `config\.env` của `AI_Agent_Orchestrator`).
   - Màn hình này cũng có sẵn đoạn JSON để dán thẳng vào cấu hình agent khác nếu cần.
   - (Tùy chọn, không bắt buộc) Dùng OAuth thay vì key: agent redirect tới app, bạn duyệt bằng mã 6 số hiện trên màn hình — không cần copy gì cả.
3. (Tùy chọn) Nếu agent chạy ở máy/cloud khác (không cùng máy với Muse4AI), bật **Remote access** (Quick tunnel / tunnel riêng / domain riêng) trong Settings — bình thường (agent chạy cùng máy, như `AI_Agent_Orchestrator`) thì **không cần** bước này.

### Dùng trực tiếp trong app (không qua AI agent)

* **Studio** — viết prompt, đính kèm ảnh tham chiếu nếu cần, bấm chạy.
* **Queue** — xem job đang chạy, trạng thái, ảnh/video xem trước.
* **Library** — toàn bộ ảnh/video đã tạo, tìm kiếm được.

### Kiểm tra kết nối API (trước khi dùng qua Orchestrator)

```powershell
curl http://127.0.0.1:47821/v1/health
curl http://127.0.0.1:47821/v1/status -H "Authorization: Bearer msk_YOUR_KEY"
```

* `health` không cần key — trả lời nghĩa là app đang mở.
* `status` trả `401` nghĩa là key sai/thiếu; lỗi kết nối nghĩa là app chưa mở, hoặc API server bị tắt trong Settings, hoặc bạn đã đổi cổng khác `47821`.

### Nối với dự án `AI_Agent_Orchestrator`

Chỉ cần điền vào `config\.env` của dự án này:

```
MUSE4AI_API_KEY=msk_...        # key thật bạn vừa tạo
MUSE4AI_BASE_URL=http://127.0.0.1:47821/v1   # giữ mặc định nếu không đổi cổng
```

rồi dùng như mô tả ở mục 3/4 bên dưới (Dashboard hoặc Claude Desktop) — không cần cấu hình gì thêm phía Muse4AI.

---

## 1. Cài đặt lần đầu

```powershell
.\scripts\install.ps1
```

Lệnh này sẽ: tạo virtual environment + cài thư viện cho `backend/` và `mcp_server/`, cài và build `frontend/`, và tự tạo file `config\.env` từ `config\.env.example` nếu chưa có.

**Mở `config\.env` và điền ít nhất 2 dòng này** (bắt buộc để đăng nhập Dashboard và dùng MCP):

```
DASHBOARD_PASSWORD=<chọn một mật khẩu>
DASHBOARD_JWT_SECRET=<một chuỗi ngẫu nhiên dài, ví dụ 32+ ký tự>
```

Các dòng khác (`MUSE4AI_API_KEY`, `ANTIGRAVITY_CLI_PATH`, ...) điền khi nào bạn thật sự dùng tới agent đó — để trống vẫn chạy được, chỉ riêng task gửi cho agent đó sẽ báo lỗi rõ ràng thay vì giả vờ chạy.

---

## 2. Khởi động hệ thống

```powershell
.\scripts\start.ps1
```

Script sẽ khởi động:

* **Backend** tại `http://127.0.0.1:8000`
* **Dashboard** tại `http://127.0.0.1:5173`

Lưu ý: script này **không** khởi động `mcp_server` — Claude Desktop tự làm việc đó (xem mục 4).

Kiểm tra backend sống chưa:

```powershell
curl http://127.0.0.1:8000/system/status
```

---

## 3. Dùng qua Dashboard

Mở trình duyệt vào `http://127.0.0.1:5173`, nhập mật khẩu bạn đặt ở `DASHBOARD_PASSWORD`.

| Trang | Dùng để |
| ----- | ------- |
| **Tổng quan** | Xem nhanh số agent, số task đang chạy/xong/lỗi, số video — cập nhật realtime |
| **Giám sát Agent** | Xem 5 agent (Claude, Antigravity, Muse, Python, QA) đang rảnh hay bận, lỗi gần nhất |
| **Quản lý nhiệm vụ** | **Tự tạo task thủ công** (không cần qua Claude Desktop): chọn agent, nhập payload JSON, bấm "Tạo nhiệm vụ"; xem kết quả, dừng task đang chạy |
| **Workflow** | Nhập `workflow_id` để xem sơ đồ các bước và trạng thái từng bước |
| **Quản lý video** | Danh sách các task gửi cho Muse Agent |
| **Log hệ thống** | Xem log backend trực tiếp, để debug khi có lỗi |
| **Cài đặt** | Xem cấu hình hiện tại (chỉ xem — sửa thật trong `config\.env` rồi `restart.ps1`) |

**Ví dụ tự tạo một task thử ở trang "Quản lý nhiệm vụ"** (không cần Antigravity/Muse4AI, dùng ngay được):
- Tên nhiệm vụ: `Thử liệt kê thư mục`
- Agent: `python`
- Payload: `{"action": "list_directory", "path": "C:\\Users"}`

Task sẽ chuyển từ QUEUED → RUNNING → COMPLETED trong vài giây, bấm "Xem kết quả" để thấy danh sách file thật.

---

## 4. Dùng qua Claude Desktop

### Cấu hình một lần

Mở file `%APPDATA%\Claude\claude_desktop_config.json`, thêm (không xóa entry khác nếu có):

```json
{
  "mcpServers": {
    "ai-agent-orchestrator": {
      "command": "D:\\AI_AGENT_SYSTEM\\mcp_server\\.venv\\Scripts\\python.exe",
      "args": ["D:\\AI_AGENT_SYSTEM\\mcp_server\\main.py"]
    }
  }
}
```

(Sửa đường dẫn `D:\AI_AGENT_SYSTEM` thành nơi bạn thực sự đặt code.) Khởi động lại Claude Desktop. MCP server cần `config\.env` có `DASHBOARD_PASSWORD` để tự đăng nhập vào backend — nhớ backend (`start.ps1`) đã chạy trước đó.

### Dùng hàng ngày

Bạn **chat bình thường bằng tiếng Việt** với Claude Desktop, Claude sẽ tự quyết định gọi tool nào. Ví dụ:

* "Giao cho Antigravity viết một hàm Python tính giai thừa, lưu vào dự án demo."
* "Hệ thống đang có bao nhiêu task đang chạy?"
* "Task `task-xxxx` xong chưa, kết quả ra sao?"
* "Tạo một video về biển hoàng hôn." (Muse tự quyết định thời lượng/độ phân giải — không có tham số chỉnh những thứ này)
* "Hủy task `task-xxxx` đi."

Claude sẽ gọi đúng tool tương ứng (`submit_task`, `get_system_status`, `get_task_result`, `create_video`, `cancel_task`...) và trả lời bạn bằng ngôn ngữ tự nhiên dựa trên kết quả thật nhận về.

---

## 5. Dừng / khởi động lại

```powershell
.\scripts\stop.ps1       # dừng backend + dashboard
.\scripts\restart.ps1    # dừng rồi khởi động lại — dùng sau khi sửa config\.env
```

---

## 6. Tự khởi động cùng Windows (chỉ bật sau khi đã dùng ổn định)

Chưa có script tự động bật — theo đúng thiết kế, việc này cần bạn xác nhận thủ công một lần (xem `Antigravity_Build_Guide.md` mục 13.2, hai lựa chọn: Task Scheduler hoặc NSSM). `scripts\health_check.ps1` dùng để tự phát hiện và khởi động lại khi hệ thống bị treo — chạy định kỳ qua Task Scheduler.

---

## 7. Khi gặp lỗi

1. Xem trang **Log hệ thống** trên Dashboard, hoặc trực tiếp file `logs\orchestrator.log`.
2. Chạy `.\scripts\health_check.ps1` để kiểm tra backend còn sống không.
3. Nếu một task cụ thể bị `FAILED`, bấm "Xem kết quả" trong Quản lý nhiệm vụ để đọc `error_message` — thường nói rõ thiếu gì (ví dụ: "Antigravity CLI not available" nghĩa là chưa cài/đăng nhập `agy`, hoặc `ANTIGRAVITY_CLI_PATH` trong `.env` sai).
4. Mang log/lỗi đó quay lại đây, tôi sẽ sửa code.

---

## Giới hạn hiện tại cần biết

* **Antigravity**: dùng **CLI** (`agy`), không phải app **Antigravity Desktop** (bản 2.0) — Desktop là GUI/điều khiển giọng nói cho người dùng trực tiếp, không có API cho chương trình khác gọi. Adapter đã sửa theo cú pháp headless thật của Google (`agy --print "..." --print-timeout ...`), nhưng vẫn **chưa chạy thử trên CLI thật** (môi trường code không có `agy`). Có rủi ro đã biết: một số báo cáo nói `agy --print` có thể treo hoặc không in gì khi output bị pipe (đúng cách adapter đang gọi) — nếu task Antigravity bị treo hoặc trả về rỗng dù code đã chạy, khả năng cao là lỗi này, không phải lỗi logic của adapter. Lần đầu dùng thật, chạy `agy --help` để đối chiếu, báo lỗi cho tôi để sửa.
* **Muse4AI**: adapter (`agents/muse/adapter.py`) đã được viết đúng theo tài liệu API thật của [github.com/andrew-babo/muse4ai](https://github.com/andrew-babo/muse4ai) (không còn là đoán), có test giả lập xác nhận gửi/nhận đúng định dạng. Vẫn **chưa chạy được với app Muse4AI thật** (cần máy Windows có cài app + tài khoản Muse đăng nhập) — lần đầu dùng thật, báo lại lỗi (nếu có) để tôi đối chiếu với tài liệu và sửa.
* **6 script PowerShell**: viết cẩn thận nhưng chưa chạy thử thật lần nào (môi trường code không có Windows).
