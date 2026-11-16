# MVP task checklist — 8 task, đi thẳng tới video 60 giây

**Trạng thái:** Tiến độ và bằng chứng kiểm chứng ghi dưới từng task. Các đường dẫn `work/` là output cục bộ. Mỗi task là một PR/phiên làm việc nhỏ, thường ≤5 file code/tài liệu trọng tâm.

## M01 — Render được một cảnh 2.5D (10–20 giây)

**Mục tiêu:** Không nghiên cứu dài dòng; kiểm tra Windows/FFmpeg và dùng một renderer phù hợp tạo được video có camera/parallax.

**Tiêu chí nghiệm thu:**
- [x] Ghi phiên bản runtime/FFmpeg, RAM/ổ trống, engine được chọn, cách chạy và quyền dùng.
- [x] Video 10–20 giây 720p có **chuyển động 2.5D thực**, ffprobe nhận đúng video stream; có log thời gian và tài nguyên cơ bản.
- [x] Nếu Lemo-Opuscar không thực thi được, mô tả lỗi và thử một phương án đơn giản thay thế; không viết hệ thống adapter.

**Kiểm chứng:** Chạy lệnh render thật trên Windows, `ffprobe`, xem clip và lưu 1 ảnh khung hình minh họa.  
**Phụ thuộc:** Không.  
**File dự kiến:** một script scene/renderer, cấu hình tối thiểu, README (≤3–5 file).  
**Điểm dừng:** Chưa có clip chạy thật thì không làm demo hàng loạt.

**Bằng chứng ngày 2026-11-16**

- Máy Windows 11 Home Single Language build 26200, Ryzen 5 5500U, tổng RAM Windows báo 15,35 GiB với 1,61 GiB khả dụng lúc khảo sát. Ổ C: còn 31,21 GiB (chứa repo và output), D: còn 141,67 GiB. PowerShell 7.6.9, Python 3.11.9, Pillow 12.3.0, FFmpeg/ffprobe 8.0.1 Essentials.
- Renderer chọn Pillow để tổng hợp năm lớp ảnh tự vẽ bằng code và truyền RGB thẳng sang FFmpeg. Một phiên render, libx264 dùng hai luồng. Pillow dùng MIT-CMU, bản FFmpeg cài trên máy dùng GPL v3 trở lên theo `ffmpeg -L`. Repo dùng các công cụ tại chỗ, không phân phối binary, và cảnh thử không dùng ảnh, font hay audio tải về. [Pillow Image](https://pillow.readthedocs.io/en/stable/reference/Image.html), [giấy phép Pillow](https://github.com/python-pillow/Pillow/blob/12.3.0/LICENSE), [FFmpeg rawvideo](https://ffmpeg.org/ffmpeg-formats.html#rawvideo), [giấy phép FFmpeg](https://ffmpeg.org/legal.html).
- Đã khảo sát Lemo-Opuscar tại `3a7132b`. Máy thiếu lệnh `claude` cho đường dùng chính thức. Tài liệu có hướng dùng cho agent khác nhưng chưa chạy thử. Renderer cục bộ đã đạt clip mục tiêu với các phụ thuộc sẵn có nên chọn dùng cho MVP. [Hướng dẫn Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar/tree/3a7132b996be0241c1ea0ab180d519f06e6f10b6).
- Môi trường có công cụ tạo ảnh nhưng chưa xác minh quota hay điều khoản tài khoản và chưa gọi tạo ảnh. Đã tìm được ứng viên TTS Việt chạy cục bộ từ tài liệu upstream. Việc nghe mẫu, xác nhận quyền của giọng cụ thể và xin đồng ý thuộc M04. [Giọng Piper vi_VN vais1000](https://huggingface.co/rhasspy/piper-voices/blob/main/vi/vi_VN/vais1000/medium/MODEL_CARD).
- Chạy `studio.py` theo [README](../README.md). `work/m01-render.log` ghi 46,10 giây render cho 12 giây video (230,5 giây mỗi phút nếu quy đổi từ phép đo này). `work/m01-resources.log` ghi peak working set lấy mẫu của Python 60,5 MiB và FFmpeg 169,3 MiB theo PID. Không ghi frame trung gian ra ổ.
- `work/m01-probe.json` ghi 288 frame H.264 yuv420p ở 1280×720, 24/1 fps, 12,000 giây, 1.205.392 byte. SHA-256 của MP4 là `0f28b65476a808660f54895a342b196b76c86cb204a2634d0e55dab00aa6f1c6`. FFmpeg giải mã đủ 288 frame và bộ lọc blackdetect không phát hiện đoạn đen. Đã đối chiếu sáu khung liên tiếp mỗi hai giây trong `work/m01-motion.png`: thân cây gần máy dịch nhiều hơn mặt hồ và trăng. Đã sửa viền tròn cứng quanh quầng trăng sau lượt xem đầu và render lại. Khung ở giây 6 lưu tại `work/m01-frame.png`.
- `ffplay -autoexit -loglevel error work/m01-valley.mp4` chạy hết với SDL dummy driver, mã thoát 0. `pip check` đạt. CLI `--help` chạy được và `--duration 9` bị từ chối với mã thoát 2. Chưa đo bản 1080p hay dựng âm thanh ở M01.

## M02 — Ba demo phong cách và người dùng chọn một

**Mục tiêu:** Từ renderer M01, tạo 3 demo khác nhau nhưng cùng một đoạn nội dung/nhân vật để so sánh dễ.

**Tiêu chí nghiệm thu:**
- [x] 3 clip MP4, mỗi clip khoảng 8–15 giây 720p, có parallax/camera và không chỉ trượt ảnh toàn khung.
- [x] Có contact sheet/reference và nhận xét chất lượng, thời gian render, nguồn asset.
- [x] Người dùng chọn 1 phong cách, lưu lựa chọn trong `style.md`.

**Kiểm chứng:** ffprobe từng demo; xem 3 clip; xác nhận của người dùng.  
**Phụ thuộc:** M01.  
**File dự kiến:** 3 scene/style config hoặc 1 scene + 3 config, `style.md` (≤5 file).  
**Điểm dừng:** Không tiếp tục sản xuất pilot nếu chưa chốt style.

**Bằng chứng ngày 2026-11-16, demo v3**

- Theo góp ý của chủ dự án, B và C đã được vẽ lại với bố cục riêng ở v2. V3 bổ sung động tác nâng, giữ và hạ đèn, khăn bay, lửa chập chờn và chuyển động mặt nước cho cả ba phong cách.
- Khóa camera khi render thử ở 640×360. Tâm ngọn lửa đi lên 34,5 pixel rồi xuống 30,5 pixel ở cả ba. Vùng nhân vật thay đổi 1.369/1.339 pixel ở A, 839/845 ở B và 964/906 ở C ở hai nhịp. Vùng mặt nước thay đổi tương ứng 596, 398 và 2.571 pixel khi nâng đèn. Vùng trời đối chứng giữ nguyên. Ngưỡng đếm là sai khác độ sáng ít nhất 5 trên 255. Xem GIF cận cảnh `work/m02-v3-fixed-camera.gif` và log `work/m02-v3-fixed-camera.log`, `work/m02-v3-lantern-height.log`.
- Đã render lại cả ba bằng `studio.py --demo <style>` trên máy M01. Mỗi clip có 288 frame H.264 yuv420p ở 1280×720, 24/1 fps, 12,000 giây theo ffprobe.

  | Clip cục bộ | Thời gian render | Kích thước |
  | --- | ---: | ---: |
  | `work/demo-moonlit.mp4` | 89,87 s | 1.318.118 byte |
  | `work/demo-ink-wash.mp4` | 90,80 s | 2.392.985 byte |
  | `work/demo-paper-cut.mp4` | 105,39 s | 2.250.106 byte |

- FFmpeg giải mã đủ 288 frame mỗi clip với `-xerror`. Bộ lọc blackdetect không báo đoạn đen. FFplay với SDL dummy chạy hết cả ba MP4, mã thoát 0. Log và JSON ffprobe có tiền tố `m02-v3-` trong `work/`.
- Đã xem chín khung trích ở giây 1, 6 và 11 trên `work/m02-v3-contact.png`. Cả ba giữ parallax giữa các lớp và thể hiện tư thế cầm đèn thấp, giơ cao, rồi hạ xuống. Sóng cảnh C thay đổi đường viền ở mỗi mốc.
- Ba tệp MP4 có SHA-256 khác nhau. Đã render lại cảnh kỹ thuật bằng `studio.py` và so SHA-256 trùng bản M01. `--demo invalid` trả mã thoát 2, `compileall` và `pip check` đạt.
- Ngày 2026-11-16 (UTC+07:00), chủ dự án xác nhận “chọn B” trong Codex. Đã đối chiếu SHA-256 của clip B v3 và ghi quyết định trong [style.md](../style.md).

## M03 — Chọn tác phẩm, viết script 60 giây và duyệt

**Mục tiêu:** Một tác phẩm văn học thuộc phạm vi công cộng, tóm tắt + bình luận nguyên bản bằng tiếng Việt.

**Tiêu chí nghiệm thu:**
- [x] Có tên tác phẩm/phiên bản, đường dẫn nguồn, ghi chú quyền **bản gốc và bản dịch riêng**; không tự copy bản dịch còn bản quyền.
- [x] `script.md` có lời thuyết minh phù hợp khoảng 60 giây, ý kiến phân tích riêng, nguồn cho các luận điểm quan trọng.
- [x] Chủ dự án nói rõ **duyệt script phiên bản này** trong Codex PC; agent ghi ngày và SHA-256 hoặc mã revision đơn giản vào `approvals.md`. Script đổi thì hỏi lại.

**Kiểm chứng:** Người dùng đọc kịch bản; so nguồn; kiểm tra bản được duyệt khớp file hiện tại.  
**Phụ thuộc:** M02 (có thể nghiên cứu nguồn sớm).  
**File dự kiến:** `episodes/pilot/script.md`, `sources.md`, `approvals.md` (3 file).  
**Điểm dừng:** Không sang voice/storyboard bản cuối trước khi script được duyệt.

**Bằng chứng ngày 2026-11-16**

- Đối chiếu tình tiết *Gió Bắc và Mặt Trời* với bản tiếng Anh của George Fyler Townsend trong eBook số 21. [Nguồn và quyền](../episodes/pilot/sources.md) lưu hồ sơ ấn bản của The Met, tình trạng phạm vi công cộng tại Hoa Kỳ từ Project Gutenberg và căn cứ Điều 27, 43 của văn bản hợp nhất hiện hành tại Việt Nam.
- [Kịch bản tiếng Việt](../episodes/pilot/script.md) gồm bốn đoạn với 35, 33, 29 và 44 tiếng, tổng 141 theo phép đếm trên phần lời đọc. Ước khoảng 60 giây khi đọc 2,6 tiếng/giây và dành khoảng 6 giây cho các nhịp nghỉ. Thời lượng đọc thực tế sẽ đo ở M04.
- Chủ dự án trả lời “duyệt” cho `script-v1` trong Codex. Đã tính lại SHA-256 trên UTF-8 LF và đối chiếu với bản gửi duyệt trong [approvals.md](../episodes/pilot/approvals.md) trước khi ghi `SCRIPT_APPROVED`.

## M04 — Giọng kể tiếng Việt, WAV và timing thật

**Mục tiêu:** Lấy giọng phù hợp, không phải xây hệ TTS tổng quát.

**Tiêu chí nghiệm thu:**
- [x] Xác định một TTS tiếng Việt miễn phí/quyền sử dụng sẵn, kiểm tra quyền dùng thương mại và **người dùng đồng ý giọng thử**. Nếu chưa được đồng ý, ghi `VOICE_PENDING` và dừng.
- [x] Xuất WAV lời kể, đo thời lượng lời đọc thật; chỉnh script hoặc nhịp nếu cần **và hỏi duyệt lại nếu sửa nội dung**.
- [x] Lưu bảng timing đơn giản theo câu/cảnh và SRT nháp dựa trên âm thanh, không ước lượng suông.

**Kiểm chứng:** Nghe WAV; ffprobe duration; so transcript/timing/SRT nháp.  
**Phụ thuộc:** M03.  
**File dự kiến:** một script TTS/timing, một file timing/SRT nháp, hướng dẫn voice (≤3 file, WAV trong `work/`).  
**Điểm dừng:** Không có voice hợp lệ thì không dựng video final.

**Bằng chứng ngày 2026-11-16:** Chủ dự án xác nhận đây là giọng địa phương và yêu cầu tiếp tục với bản Quang Sơn. WAV 56,952125 giây ở 48 kHz có 13 cue khớp văn bản, SRT và số mẫu của đoạn ghép. Hash WAV trùng bản đã gửi. Đã lưu [timing của bản đọc](../episodes/pilot/narration-timing.json) và trạng thái `VOICE_READY` trong [approvals.md](../episodes/pilot/approvals.md). [Lệnh chạy, số đo và kết quả kiểm tra](../episodes/pilot/voice.md).

## M05 — Storyboard và lần duyệt thứ hai

**Mục tiêu:** Kế hoạch cảnh dựa trên lời đọc thật và style đã chọn.

**Tiêu chí nghiệm thu:**
- [x] Tạo **3–6** storyboard frame đại diện cho pilot 60 giây (quy tắc **12–20 frame** dành cho video dài về sau).
- [x] Mỗi cảnh nêu hình ảnh/layer, chuyển động camera, thời điểm bắt đầu/kết thúc và câu voice tương ứng.
- [x] Người dùng duyệt storyboard trong Codex PC; ghi ngày và revision/hash của board + script/timing vào `approvals.md`.

**Kiểm chứng:** Xem từng frame; cộng thời lượng các cảnh khớp voice; kiểm tra hash đã duyệt.  
**Phụ thuộc:** M04.  
**File dự kiến:** `episodes/pilot/storyboard.md`, file ảnh tham chiếu trong `work/`, cập nhật `approvals.md` (≤3 file theo dõi).  
**Điểm dừng:** Board chưa duyệt thì không render toàn bộ pilot.

**Bằng chứng ngày 2026-11-16**

- Chạy `python -m scenes.pilot_board` trong môi trường của repo trên Windows, dựng và xem bốn ảnh RGB 1280×720. Đã sửa nét gió để hai đầu tan dần và giữ hướng nắng nhất quán giữa cảnh 1 và 3. Ảnh tổng hợp ở `work/pilot/storyboard/board-v1.png`. Chạy lại cho cùng SHA-256 ở cả năm PNG. SHA-256 của bốn khung lưu trong [storyboard](../episodes/pilot/storyboard.md).
- Đối chiếu với WAV Quang Sơn và timing bằng Python. Bốn cảnh lần lượt có 326, 358, 286 và 470 khung, tổng 1.440 khung ở 24 fps. Cả 13 cue nằm trong cảnh tương ứng. Ba điểm cắt đều rơi vào khoảng nghỉ giữa các đoạn.
- Chủ dự án trả lời “dựng đi” cho `board-v1`. Đã đối chiếu lại hash storyboard, `script-v1`, timing và WAV trước khi ghi `BOARD_APPROVED` trong [approvals.md](../episodes/pilot/approvals.md).

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

- [x] 3 demo chuyển động, user chọn style
- [x] 2 lần duyệt script + storyboard, đúng phiên bản
- [x] 1 tác phẩm phù hợp quyền thương mại và lời bình nguyên bản
- [x] Voice Việt được người dùng đồng ý, có timing thực
- [ ] 60s preview 720p, final 1080p/24fps **từ nguồn**
- [ ] MP4/SRT/thumbnail/metadata/credits; không có thanh toán tự động
- [ ] Phát hết video; ffprobe kiểm tra stream; thử sửa/render lại một scene
- [ ] Có hướng dẫn tái hiện; không nhận bừa kết quả chưa chạy

Sau đó mới mở backlog cho video 2–3 phút → 5 phút → 20–30 phút. Xem [plan](plan.md).
