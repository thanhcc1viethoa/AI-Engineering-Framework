# MotionCopyVideo

Công cụ hỗ trợ làm video "copy chuyển động" bằng **Google Flow (Gemini Omni)**: thay nhân vật, trang phục, phụ kiện, mẫu xe (và bối cảnh) trên một hoặc nhiều video gốc, giữ nguyên chuyển động – biểu cảm – nhịp, rồi **ghép nhiều đoạn thành một video dài** mà nhân vật, trang phục, phụ kiện, mẫu xe vẫn **đồng nhất xuyên suốt**.

> Built on the AI Engineering Framework. `Requirement.md` (REQ-MCV-001) is the single source of truth for this project.

## Status

| Stage       | Artifact          | Status |
| ----------- | ----------------- | ------ |
| Requirement | `Requirement.md`  | Draft — chờ người duyệt |
| Prototype   | `motion_copy/`    | Created, smoke tests pass (CLI + UI API) |

## Vì sao cần tool

Flow/Omni chỉ sửa được đoạn ngắn (~10 giây) mỗi lần, và mỗi lần tạo có thể "trôi" mặt, màu áo, mẫu xe. Tool không thay Flow — nó lo phần trước và sau Flow để các đoạn ghép lại khớp nhau.

## Kỹ thuật học từ các repo

| Kỹ thuật | Học từ | Áp dụng trong tool |
| --- | --- | --- |
| Cửa sổ trượt có chồng lấn (sliding window) | Wan2GP / VACE | Shot dài được cắt thành đoạn ≤ 8 s, chồng 0,5 s với đoạn sau |
| Hoà trộn vùng chồng lấn (progressive latent fusion) | MimicMotion | Khi ghép, cross-fade đúng phần chồng lấn → không giật ở mối nối |
| Một ảnh tham chiếu cố định cho mọi khung | Wan2.2-Animate | Bộ ảnh mẫu cố định, cùng thứ tự, cùng số "ingredient" cho mọi đoạn |
| Lấy khung đã đạt làm điều kiện cho đoạn sau | VACE / Wan2GP (khung cuối của cửa sổ trước) | Đoạn neo được duyệt → xuất "anchor frame" làm ingredient liên tục cho mọi đoạn khác |
| Hài hoà ánh sáng/màu (relighting) | Wan2.2-Animate relighting LoRA | Khi ghép, chỉnh màu từng đoạn về thống kê màu của đoạn neo (một phép biến đổi cố định/đoạn, không nhấp nháy) |
| Giữ nhịp theo video gốc | Pose/motion transfer | Mỗi đoạn được ép đúng thời lượng gốc; giữ điểm cắt cảnh gốc; dùng âm thanh gốc |

## Giao diện (khuyên dùng)

**Cách dễ nhất:** bấm đúp `Start-MotionCopyUI.bat` (ở thư mục `MotionCopyVideo`). File này tự kiểm tra Python và ffmpeg, hỏi để cài nếu thiếu, rồi mở giao diện. Dự án lưu ở `D:\Video\MotionCopy` (hoặc `Videos\MotionCopy` nếu máy không có ổ D). Giữ cửa sổ đen mở trong lúc dùng.

Hoặc từ PowerShell:

```powershell
cd 05_Projects\MotionCopyVideo\motion_copy
.\Start-MotionCopyUI.ps1
```

Trình duyệt tự mở `http://127.0.0.1:8765` (chỉ chạy trên máy bạn, không ra Internet). Dự án được lưu ở `%USERPROFILE%\Videos\MotionCopy`.

* **Sơ đồ quy trình** 7 bước ở đầu trang: xanh = xong, viền xanh dương = bước đang làm, viền tím nét đứt = bước làm tay trên Flow. Bấm vào bước để nhảy tới phần đó.
* **Bước 1:** kéo thả video gốc, ảnh nhân vật, trang phục, phụ kiện, mẫu xe, bối cảnh vào từng ô; điền khoá nhân vật → *Lưu cài đặt*.
* **Bước 2:** *Chia đoạn*.
* **Bước 3–5:** mỗi đoạn là một thẻ: ① tải đoạn gốc lên Flow, ② tải ảnh mẫu theo số thứ tự, ③ *Copy prompt*, ④ thả video Flow tải về vào thẻ. Làm thẻ **NEO** trước → *Duyệt làm đoạn neo* → các thẻ còn lại mới mở.
* **Bước 6:** *Kiểm tra* → nhãn PASS/CHECK trên từng thẻ + contact sheet.
* **Bước 7:** *Ghép video* → xem và tải `final.mp4` ngay trên trang.

Dòng lệnh bên dưới vẫn dùng được và cho kết quả giống hệt.

## Cài đặt (Windows)

1. Cài ffmpeg: `winget install Gyan.FFmpeg` (mở lại PowerShell).
2. Cài Python 3.10 trở lên.
3. Lần chạy đầu `Start-MotionCopy.ps1` tự tạo `.venv` và cài `requirements.txt`.

## Chuẩn bị thư mục làm việc (ngoài repo)

```
D:\Video\ep05\
  project.json            ← copy từ motion_copy\project.example.json rồi sửa
  source\dap_xe_goc.mp4   ← một hoặc nhiều video gốc (ghép theo thứ tự trong "sources")
  assets\character\       ← ảnh nhân vật (May_master.png, bảng 6 góc...)
  assets\outfit\          ← ảnh trang phục (mã OF trong Kho)
  assets\accessories\     ← phụ kiện (đồng hồ, túi, mũ...)
  assets\bike\            ← ảnh mẫu xe nhiều góc
  assets\background\      ← (tuỳ chọn) ảnh bối cảnh; hoặc chỉ dùng "background_prompt"
```

Mỗi thư mục được gộp thành **một** ảnh bảng có đánh số, vì Flow chỉ nhận ít ingredient (mặc định giới hạn 5). Dán khóa nhân vật Mây vào `identity_lock` / `end_lock`.

## Quy trình

```powershell
cd 05_Projects\MotionCopyVideo\motion_copy
.\Start-MotionCopy.ps1 prepare  D:\Video\ep05\project.json
```

1. **prepare** — dò điểm cắt cảnh, cắt video gốc thành `work\segments\seg_###.mp4`, tạo ảnh bảng `work\refs\`, viết `work\flow_jobs.md` (mỗi đoạn: file upload, ingredient theo thứ tự, prompt).
2. **Flow, đoạn neo trước** (`seg_001`): upload đoạn, gắn ingredient, dán prompt, tạo, tải về `work\outputs\seg_001.mp4`.
3. **check** — `.\Start-MotionCopy.ps1 check D:\Video\ep05\project.json`. Xem `work\qc\contact_sheet.png` (so mặt, nốt ruồi trái, đồng hồ tay trái, đồ, xe). Đạt thì:
   `.\Start-MotionCopy.ps1 check D:\Video\ep05\project.json --approve-anchor` → xuất `anchor_frame.png` và viết lại `flow_jobs.md` (các đoạn còn lại có thêm ingredient liên tục).
4. **Flow, các đoạn còn lại** → tải về `work\outputs\seg_002.mp4`, ...
5. **check** lại → `work\qc\report.md`: đoạn `CHECK` chỉ tạo lại đoạn đó với câu "Fix only: ...". Đoạn `PASS` giữ nguyên.
6. **assemble** — `.\Start-MotionCopy.ps1 assemble D:\Video\ep05\project.json` → `work\final.mp4` (1080×1920, 30 fps, âm thanh gốc). Dựng phụ đề/giọng tiếp bằng Remotion hoặc CapCut.

Tiện ích: `lastframe <video> <ảnh.png>` xuất khung cuối một clip để dùng "Frames to video"/Extend trong Flow khi muốn kéo dài cảnh không có video gốc.

## Giới hạn (nói thẳng)

* Tool **không gọi Flow tự động** — Flow không có API công khai cho Omni; bước tạo vẫn làm tay trên Flow.
* Chỉ số màu và mối nối trong `check` là heuristic: bắt lệch màu áo/xe và giật ở mối nối, **không nhận diện mặt**. Mặt, nốt ruồi, đồng hồ, hình dáng xe do người xem contact sheet quyết định.
* Một đoạn từ Flow ngắn hơn cần quá 15 % (`max_stretch`) sẽ bị từ chối khi ghép — tạo lại dài hơn.
* Chỉ dùng video gốc bạn có quyền sử dụng; giữ nhãn "Nội dung do AI tạo" khi đăng.

## Kiểm tra

```powershell
.\.venv\Scripts\python.exe smoke_test.py
.\.venv\Scripts\python.exe app_smoke_test.py
```

`smoke_test.py` tự tạo video tổng hợp (có cắt cảnh, có/không âm thanh, đường dẫn tiếng Việt), giả lập Flow, chạy `prepare → check → assemble` và kiểm tra video cuối đúng thời lượng, kích thước, có âm thanh.

`app_smoke_test.py` chạy cùng quy trình qua API của giao diện (tải lên, chia đoạn, duyệt neo, kiểm tra, ghép) và kiểm tra chặn đường dẫn ngoài dự án, chặn file sai loại.
