# /plan — MVP AI Video Studio (tối giản, 60 giây)

**Trạng thái:** Đề xuất để review, **chưa có code chạy**. Cơ sở: [SPEC v1](../docs/spec.md) đã merge, yêu cầu mới nhất của chủ dự án: *ưu tiên có MVP chạy thật, không over-engineer, không xây bảo mật phức tạp*.  
**Mốc đầu tiên:** 3 demo phong cách 2.5D thực sự chuyển động → người dùng chọn style → 1 pilot **60 giây** với giọng đọc tiếng Việt, nhạc/SFX, phụ đề và bản MP4 1080p/24fps.

## 1. Definition of MVP (không phải sản phẩm 30 phút)

Một lượt chạy qua **Codex PC trên Windows** được coi là MVP đạt khi:

1. Có **3 video demo khác nhau** (mỗi video khoảng 8–15 giây, 720p, có parallax/camera 2.5D thực) và người dùng chọn 1 phong cách.
2. Dùng **1 tác phẩm văn học xác minh thuộc phạm vi công cộng**. Có kịch bản tiếng Việt khoảng 60 giây, phần tóm tắt + nhận xét riêng, các luận điểm quan trọng kèm nguồn.
3. Người dùng **duyệt kịch bản** và **duyệt storyboard** qua Codex PC. Ghi vào file Markdown: thời điểm, bản nội dung/hash được duyệt; thay đổi nội dung thì phải hỏi duyệt lại. Đây là checkpoint công việc, **không cần chữ ký số, tài khoản, service hay cơ chế chống agent giả mạo** trong MVP.
4. Có giọng TTS tiếng Việt được người dùng đồng ý dùng thử và có quyền sử dụng phù hợp, đo thời lượng thật trước storyboard. Nếu chưa có giọng được chấp thuận thì **dừng ở VOICE_PENDING**, không làm giả voice hay âm thầm chọn giọng cuối.
5. Tạo preview 720p; bản cuối **1920×1080/24fps render lại từ scene nguồn** (không upscale), có giọng, nhạc/SFX và phụ đề đồng bộ; xuất **MP4, SRT, thumbnail, title/description và ghi chú nguồn/quyền**.
6. Người dùng xem hết pilot, chấp nhận chất lượng; có thể **chỉ render lại 1 scene lỗi**, không phải làm lại từ đầu. Không có chi phí mới, không tự đăng YouTube.

Không cam kết video 20–30 phút hay ≥1 video/ngày trong MVP.

## 2. Quyết định giảm độ phức tạp

| Làm trong MVP | KHÔNG làm trước pilot |
| --- | --- |
| Một công cụ render khả thi sau thử 10–20 giây | Framework adapter/plugin cho nhiều engine |
| Script/scene đơn giản + FFmpeg + file Markdown/JSON tối thiểu | Database, queue server, scheduler, Windows service |
| Codex PC điều khiển tuần tự, 1 worker | Web UI, multi-agent dispatcher, cloud GPU |
| Hai lần duyệt qua chat Codex + ghi hash/tên bản | Ký approval, audit service, auth/role, event-sourcing |
| Nguồn và quyền asset ghi trong 1 file | Rights management platform, full source-claim database |
| Hash đơn giản để nhận diện scene cần làm lại | Cache phân tán, tự động dọn/xóa dữ liệu |
| Kiểm tra bằng ffprobe + xem/nghe pilot | CI phức tạp, telemetry, metrics service |
| Sử dụng quota miễn phí/đã có quyền, xử lý offline khi có thể | Tự đăng YouTube hoặc trả phí API |

**Giữ những rào chắn tối thiểu:** không tự chi tiền, không đưa file riêng lên dịch vụ khác nếu chưa được phép, không dùng asset/tác phẩm mơ hồ bản quyền, không bỏ qua hai lần duyệt, không coi video lỗi là hoàn tất.

## 3. Công nghệ và thư mục — linh hoạt, không lock sớm

- Trên máy Windows thật: kiểm tra Python/Node, FFmpeg/ffprobe, RAM và ổ trống bằng lệnh thật. Không giả định ổ D: hoặc phiên bản Windows.
- Thử tạo **một scene chuyển động 2.5D 10–20 giây** bằng giải pháp nhẹ nhất khả dụng. Có thể dùng Lemo-Opuscar nếu chạy tốt; nếu không, dùng HTML Canvas/JS + FFmpeg (hoặc giải pháp đơn giản hơn được chứng minh). **Chọn một cách chạy được**, không bắt buộc benchmark nhiều engine.
- Khi chọn xong, thêm đúng lệnh setup/render/test vào README; mọi lệnh dưới đây chỉ là **giao diện mong muốn**, chưa có trong repo.
- Gợi ý giữ nhỏ: `studio.py` hoặc `scripts/` cho bước điều khiển; `scenes/` chứa scene nguồn; `episodes/pilot/` chứa `script.md`, `storyboard.md`, `approvals.md`, `sources.md`; `work/` chứa asset/WAV/MP4/log không đưa lên Git. Nếu engine thực tế thuận tiện hơn với JS, dùng JS; **không viết cả Python và JS coordinator trùng chức năng**.
- Dùng một cách đặt tên và cấu hình đơn giản nhất, chưa cần JSON Schema, versioned API hoặc manifest phức tạp.

## 4. Dependency graph (mỗi task một lát cắt kiểm chứng được)

```text
M01: máy + scene 10–20s chạy được
  └─ M02: 3 demo phong cách → [BẠN CHỌN STYLE]
       └─ M03: tác phẩm hết bản quyền + kịch bản → [BẠN DUYỆT SCRIPT]
            └─ M04: TTS tiếng Việt + đo timing
                 └─ M05: storyboard + timing → [BẠN DUYỆT BOARD]
                      └─ M06: bản preview 60s / 720p
                           └─ M07: final 1080p + SRT/thumbnail/metadata
                                └─ M08: fix 1 scene + QA + hướng dẫn chạy lại
```

Tài liệu nguồn có thể nghiên cứu song song với demo, nhưng **không sản xuất pilot** trước khi chốt phong cách và hai nội dung cần duyệt.

## 5. Checkpoints & bằng chứng

- **Sau M01:** có MP4 ngắn 2.5D chạy được trên máy, ffprobe đọc được, ghi công cụ/phiên bản và thời gian render. Nếu không đạt, thử **một** phương án thay thế phù hợp trước khi mở rộng.
- **Sau M02:** ba file demo + hình tham chiếu + người dùng chọn style. Không cần UI riêng.
- **Sau M03:** người dùng xác nhận *đúng phiên bản kịch bản*, có nguồn và tình trạng bản quyền rõ.
- **Sau M04–M05:** có WAV/timing/SRT nháp, storyboard khớp lời kể và bạn duyệt storyboard.
- **Sau M06:** xem/nghe đầy đủ preview 60 giây, có nhiều scene chuyển động; nếu lỗi thì sửa cảnh lỗi.
- **Sau M07–M08:** MP4 cuối 1080p/24fps với audio, SRT, thumbnail, metadata, nguồn và QA; dùng ffprobe + xem/nghe hết video; thử render lại đúng một scene.

**Không khai báo 'test passed' nếu chưa chạy.** Đọc [task checklist](todo.md), [verification](../docs/verification.md). Không tự merge implementation PR.

## 6. Rủi ro / cách xử lý tối giản

| Rủi ro | Cách xử lý |
| --- | --- |
| Lemo/renderer nặng trên RAM 16 GB | Chỉ 1 worker; thử 10–20s; đổi engine nếu thực sự không chạy được |
| Không gọi tạo ảnh được từ Codex PC | Dùng ảnh chủ dự án xuất từ ChatGPT hoặc asset/procedural có quyền sử dụng, không giả định API có sẵn |
| Chưa chọn giọng thuyết minh | Xin duyệt giọng thử; không có thì dừng M04/M05 |
| Tác phẩm/bản dịch chưa rõ quyền | Dùng bản gốc thuộc phạm vi công cộng và tự viết lời bình tiếng Việt; lưu đường dẫn tham chiếu |
| Hết hạn mức / cần trả phí | Dừng và báo, không mua quota |
| Lỗi âm thanh/khung hình | Chỉ sửa/render lại cảnh gặp lỗi, xem lại thành phẩm |
| Máy đóng Codex PC | Tiếp tục thủ công từ file đã có; không bảo đảm chạy nền |
| Dọn dữ liệu | Chưa tự động xóa; dọn thủ công sau khi backup file cần thiết |

## 7. Sau MVP — backlog riêng (chưa lập task)

- 2–3 phút → 5 phút → 20–30 phút, đo hiệu năng rồi mới nghĩ tới 1 video/ngày.
- Duyệt/lên hàng đợi theo lô và chạy 24/7 độc lập.
- Source/rights registry nâng cao, cache/cleanup tự động, nhiều TTS/engine adapter nếu có nhu cầu thật.
- YouTube API, dashboard, multi-machine, cloud render.

**Next action:** Review plan PR, rồi chạy **M01**. Không xây các phần trong backlog khi M01–M08 chưa đạt.
