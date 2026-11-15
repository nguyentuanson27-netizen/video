# MVP task checklist — 8 task, đi thẳng tới video 60 giây

**Trạng thái:** /plan, chưa build. SPEC đã merge; yêu cầu người dùng: **tối giản, chạy MVP trước**. Các `studio.py`, `scenes/`, `work/` bên dưới là file **dự kiến**, chưa tồn tại. Mỗi task là một PR/phiên làm việc nhỏ, thường ≤5 file code/tài liệu trọng tâm.

## M01 — Render được một cảnh 2.5D (10–20 giây)

**Mục tiêu:** Không nghiên cứu dài dòng; kiểm tra Windows/FFmpeg và dùng một renderer phù hợp tạo được video có camera/parallax.

**Tiêu chí nghiệm thu:**
- [ ] Ghi phiên bản runtime/FFmpeg, RAM/ổ trống, engine được chọn, cách chạy và quyền dùng.
- [ ] Video 10–20 giây 720p có **chuyển động 2.5D thực**, ffprobe nhận đúng video stream; có log thời gian và tài nguyên cơ bản.
- [ ] Nếu Lemo-Opuscar không thực thi được, mô tả lỗi và thử một phương án đơn giản thay thế; không viết hệ thống adapter.

**Kiểm chứng:** Chạy lệnh render thật trên Windows, `ffprobe`, xem clip và lưu 1 ảnh khung hình minh họa.  
**Phụ thuộc:** Không.  
**File dự kiến:** một script scene/renderer, cấu hình tối thiểu, README (≤3–5 file).  
**Điểm dừng:** Chưa có clip chạy thật thì không làm demo hàng loạt.

## M02 — Ba demo phong cách và người dùng chọn một

**Mục tiêu:** Từ renderer M01, tạo 3 demo khác nhau nhưng cùng một đoạn nội dung/nhân vật để so sánh dễ.

**Tiêu chí nghiệm thu:**
- [ ] 3 clip MP4, mỗi clip khoảng 8–15 giây 720p, có parallax/camera và không chỉ trượt ảnh toàn khung.
- [ ] Có contact sheet/reference và nhận xét chất lượng, thời gian render, nguồn asset.
- [ ] Người dùng chọn 1 phong cách, lưu lựa chọn trong `style.md`.

**Kiểm chứng:** ffprobe từng demo; xem 3 clip; xác nhận của người dùng.  
**Phụ thuộc:** M01.  
**File dự kiến:** 3 scene/style config hoặc 1 scene + 3 config, `style.md` (≤5 file).  
**Điểm dừng:** Không tiếp tục sản xuất pilot nếu chưa chốt style.

## M03 — Chọn tác phẩm, viết script 60 giây và duyệt

**Mục tiêu:** Một tác phẩm văn học thuộc phạm vi công cộng, tóm tắt + bình luận nguyên bản bằng tiếng Việt.

**Tiêu chí nghiệm thu:**
- [ ] Có tên tác phẩm/phiên bản, đường dẫn nguồn, ghi chú quyền **bản gốc và bản dịch riêng**; không tự copy bản dịch còn bản quyền.
- [ ] `script.md` có lời thuyết minh phù hợp khoảng 60 giây, ý kiến phân tích riêng, nguồn cho các luận điểm quan trọng.
- [ ] Chủ dự án nói rõ **duyệt script phiên bản này** trong Codex PC; agent ghi ngày và SHA-256 hoặc mã revision đơn giản vào `approvals.md`. Script đổi thì hỏi lại.

**Kiểm chứng:** Người dùng đọc kịch bản; so nguồn; kiểm tra bản được duyệt khớp file hiện tại.  
**Phụ thuộc:** M02 (có thể nghiên cứu nguồn sớm).  
**File dự kiến:** `episodes/pilot/script.md`, `sources.md`, `approvals.md` (3 file).  
**Điểm dừng:** Không sang voice/storyboard bản cuối trước khi script được duyệt.

## M04 — Giọng kể tiếng Việt, WAV và timing thật

**Mục tiêu:** Lấy giọng phù hợp, không phải xây hệ TTS tổng quát.

**Tiêu chí nghiệm thu:**
- [ ] Xác định một TTS tiếng Việt miễn phí/quyền sử dụng sẵn, kiểm tra quyền dùng thương mại và **người dùng đồng ý giọng thử**. Nếu chưa được đồng ý, ghi `VOICE_PENDING` và dừng.
- [ ] Xuất WAV lời kể, đo thời lượng lời đọc thật; chỉnh script hoặc nhịp nếu cần **và hỏi duyệt lại nếu sửa nội dung**.
- [ ] Lưu bảng timing đơn giản theo câu/cảnh và SRT nháp dựa trên âm thanh, không ước lượng suông.

**Kiểm chứng:** Nghe WAV; ffprobe duration; so transcript/timing/SRT nháp.  
**Phụ thuộc:** M03.  
**File dự kiến:** một script TTS/timing, một file timing/SRT nháp, hướng dẫn voice (≤3 file, WAV trong `work/`).  
**Điểm dừng:** Không có voice hợp lệ thì không dựng video final.

## M05 — Storyboard và lần duyệt thứ hai

**Mục tiêu:** Kế hoạch cảnh dựa trên lời đọc thật và style đã chọn.

**Tiêu chí nghiệm thu:**
- [ ] Tạo **3–6** storyboard frame đại diện cho pilot 60 giây (quy tắc **12–20 frame** dành cho video dài về sau).
- [ ] Mỗi cảnh nêu hình ảnh/layer, chuyển động camera, thời điểm bắt đầu/kết thúc và câu voice tương ứng.
- [ ] Người dùng duyệt storyboard trong Codex PC; ghi ngày và revision/hash của board + script/timing vào `approvals.md`.

**Kiểm chứng:** Xem từng frame; cộng thời lượng các cảnh khớp voice; kiểm tra hash đã duyệt.  
**Phụ thuộc:** M04.  
**File dự kiến:** `episodes/pilot/storyboard.md`, file ảnh tham chiếu trong `work/`, cập nhật `approvals.md` (≤3 file theo dõi).  
**Điểm dừng:** Board chưa duyệt thì không render toàn bộ pilot.

## M06 — Preview 60 giây 720p có đầy đủ lời và nhạc

**Mục tiêu:** Một tuyến hoàn chỉnh từ kịch bản được duyệt → cảnh → lồng tiếng → MP4 preview.

**Tiêu chí nghiệm thu:**
- [ ] Dựng ít nhất 3 cảnh, có chiều sâu 2.5D/camera chuyển động và chuyển cảnh đúng nhịp kể.
- [ ] Ghép voice đã duyệt, nhạc/SFX hợp pháp (có thể rất ít nhạc), mix giọng rõ ràng; tạo `preview.mp4` 1280×720/24fps với phụ đề SRT.
- [ ] Không bị cảnh đen bất ngờ, im tiếng, phụ đề lệch nghiêm trọng; có thể xác định scene gây lỗi.

**Kiểm chứng:** ffprobe preview; **xem/nghe hết 60 giây**, đối chiếu SRT; sửa tối thiểu một lỗi nếu phát hiện.  
**Phụ thuộc:** M05.  
**File dự kiến:** render/assemble script, scene configs và SRT (≤3–5 file; media trong `work/`).

## M07 — Video cuối 1080p + gói đăng thủ công

**Mục tiêu:** Tạo bản sản xuất thật, không upscale preview.

**Tiêu chí nghiệm thu:**
- [ ] Render lại các scene từ nguồn tại **1920×1080/24fps**, ghép MP4 H.264/AAC với giọng rõ, đủ khoảng 60 giây.
- [ ] Xuất `episode.srt`, `thumbnail.png`, `youtube-metadata.md` (title/description), `credits-and-rights.md` (nguồn tác phẩm, asset, voice, nhạc).
- [ ] File final đọc được bằng ffprobe; không đánh dấu sẵn sàng nếu có quyền thương mại chưa rõ hoặc chất lượng lỗi.

**Kiểm chứng:** ffprobe độ phân giải/fps/codec; xem/nghe toàn bộ bản final; so SRT và checklist nguồn.  
**Phụ thuộc:** M06.  
**File dự kiến:** bổ sung final profile và script export, metadata Markdown (≤3–5 file; output trong `work/`).

## M08 — Sửa đúng một cảnh, chạy lại và bàn giao

**Mục tiêu:** Bằng chứng rằng MVP có thể sửa, không bắt đầu lại từ đầu khi lỗi.

**Tiêu chí nghiệm thu:**
- [ ] Có lệnh/quy trình render **một scene**, rồi assemble lại mà giữ các scene không đổi (skip theo file/checksum đơn giản).
- [ ] Khi scene lỗi, ghi nguyên nhân, sửa tối đa vài lượt hợp lý; chưa đạt thì **NEEDS_REVIEW**, không tự nhận PASS.
- [ ] README có lệnh **thực tế đã chạy** để tái hiện demo, preview, final; kèm kết quả QA và những gì chưa kiểm chứng.

**Kiểm chứng:** Cố ý sửa một scene, render lại, kiểm tra scene còn lại không đổi; phát lại final và đối chiếu ffprobe.  
**Phụ thuộc:** M07.  
**File dự kiến:** một thay đổi nhỏ trong render script, README và `qa-notes.md` (≤3 file).

## Checklist Done cho MVP

- [ ] 3 demo chuyển động, user chọn style
- [ ] 2 lần duyệt script + storyboard, đúng phiên bản
- [ ] 1 tác phẩm phù hợp quyền thương mại và lời bình nguyên bản
- [ ] Voice Việt được người dùng đồng ý, có timing thực
- [ ] 60s preview 720p, final 1080p/24fps **từ nguồn**
- [ ] MP4/SRT/thumbnail/metadata/credits; không có thanh toán tự động
- [ ] Phát hết video; ffprobe kiểm tra stream; thử sửa/render lại một scene
- [ ] Có hướng dẫn tái hiện; không nhận bừa kết quả chưa chạy

Sau đó mới mở backlog cho video 2–3 phút → 5 phút → 20–30 phút. Xem [plan](plan.md).
