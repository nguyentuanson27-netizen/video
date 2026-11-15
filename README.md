# AI Video Studio

> **MVP trên Windows.** Xem tiến độ và kết quả render trong [checklist](tasks/todo.md).

Hệ thống hỗ trợ **Codex PC trên Windows** sản xuất video YouTube kể chuyện minh họa điện ảnh **2.5D**, dài **20–30 phút**, tóm tắt và phân tích tiểu thuyết/văn học hoặc sự kiện lịch sử. Người dùng duyệt **kịch bản** và **storyboard** trước khi render. AI tạo ra video, thumbnail, phụ đề, tiêu đề/mô tả; **người dùng tự đăng**.

## Mục tiêu và nguyên tắc

- **Chất lượng quan trọng hơn sản lượng**. Mục tiêu hướng tới ≥1 video/ngày là mục tiêu tối ưu, không phải cam kết hoặc lý do bỏ QA.
- **Ngân sách biến đổi gần 0 đồng**: dùng phần mềm/asset hợp pháp, quota tạo ảnh đã có; không tự mua, nâng cấp hoặc gọi dịch vụ tính phí.
- **Một phong cách kênh**: cinematic storybook 2.5D; thử **3 demo phong cách** có chuyển động thực trước khi chọn bản sắc cuối.
- **Nội dung có căn cứ**: ưu tiên tài liệu người dùng cung cấp, nghiên cứu bổ sung; kiểm chứng luận điểm quan trọng và lưu nguồn; tránh nhầm dữ kiện lịch sử với tái hiện.
- **Bản quyền**: kiểm tra tác phẩm gốc, bản dịch, hình ảnh, nhạc, SFX và quyền thương mại trước khi phát hành.
- **Thử nhỏ trước**: 3 demo → pilot **60 giây** trên tác phẩm văn học thuộc phạm vi công cộng → mở rộng dần.
- **Codex PC** điều phối, không xây web dashboard hay Windows service trong MVP.
- **Preview 720p**, render cuối **1080p/24 FPS** từ nguồn, không upscale preview.
- Từng scene có thể kiểm tra, dựng lại độc lập và khôi phục; xóa cache có kiểm soát, không xóa dữ liệu đã duyệt.
- **Phê duyệt là thao tác thực sự của người dùng**, không phải file JSON do agent tự viết; giọng đọc/timing phải sẵn sàng trước khi khóa storyboard.

## Trạng thái hiện tại

| Hạng mục | Trạng thái |
| --- | --- |
| Phỏng vấn yêu cầu | Đã chốt phần lớn; ghi trong SPEC |
| Renderer 2.5D | Pillow và FFmpeg |
| TTS tiếng Việt và bản sắc kênh | Chờ chọn và duyệt |
| MP4 pilot | Theo các checkpoint trong [checklist](tasks/todo.md) |

## Render cảnh kỹ thuật M01

Chạy từ thư mục repo trong PowerShell trên Windows. Cần Python 3.11+ và `ffmpeg` (có `libx264`) cùng `ffprobe` trên PATH.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt
.\.venv\Scripts\python.exe studio.py --help
.\.venv\Scripts\python.exe studio.py
ffprobe -v error -count_frames -show_entries 'format=duration,size:stream=codec_name,codec_type,width,height,pix_fmt,r_frame_rate,nb_read_frames' -of json work/m01-valley.mp4
ffmpeg -v info -xerror -i work/m01-valley.mp4 -vf 'blackdetect=d=0.08:pix_th=0.10' -f null NUL
ffmpeg -y -v error -ss 6 -i work/m01-valley.mp4 -frames:v 1 -update 1 work/m01-frame.png
```

Mặc định tạo `work/m01-valley.mp4` dài 12 giây, 1280×720, 24 fps. Có thể dùng `--duration` để chọn thời lượng nguyên từ 10 đến 20 giây. Cảnh tự vẽ gồm năm lớp từ bầu trời đến rặng cây trước máy quay. Mỗi lớp có mức dịch chuyển và zoom riêng. Python truyền lần lượt từng frame cho FFmpeg nên bản render không cần thư mục hàng trăm ảnh trung gian.

## Render ba demo M02

```powershell
foreach ($style in 'moonlit', 'ink-print', 'paper-cut') {
    .\.venv\Scripts\python.exe studio.py --demo $style
    if ($LASTEXITCODE -ne 0) { break }
    ffprobe -v error -count_frames -show_entries 'format=duration:stream=codec_name,width,height,r_frame_rate,nb_read_frames' -of json "work/demo-$style.mp4"
    if ($LASTEXITCODE -ne 0) { break }
}
```

Mỗi lệnh tạo một clip 12 giây ở 1280×720, 24 fps. Xem [ba phương án và trạng thái lựa chọn](style.md).

## Định hướng kiến trúc

```text
User topic / documents
  → research + claim ledger → outline → script → [APPROVAL: SCRIPT]
  → confirmed permitted Vietnamese TTS + measured timings → scene/shot plan
  → storyboard (pilot 3–6 hình; 12–20 cho video dài) → [APPROVAL: STORYBOARD]
  → asset có quyền sử dụng → scene renderer (một engine) → QA/sửa lỗi → scene clips
  → episode assembly → final QA → MP4/SRT/thumbnail/metadata/credits
```

Xem [architecture](docs/architecture.md) và [data contracts](docs/data-contracts.md).

## Cấu trúc repo dự kiến

```text
AGENTS.md                       # Quy tắc Codex
docs/                           # SPEC, ADR, vận hành, quyền, verification
tasks/                          # Plan và task breakdown
studio.py                       # Runner Pillow / FFmpeg
scenes/                         # Nguồn cảnh
episodes/pilot/                 # script.md, storyboard.md, sources.md, approvals.md
work/                           # WAV/MP4/cache cục bộ, gitignored
```

**Không commit**: API keys, tài liệu riêng tư, video lớn, cache/frames, model, token, file tạm. Tham khảo [gitignore](.gitignore).

## Tài liệu

- [SPEC & acceptance criteria](docs/spec.md)
- [Architecture & engine selection](docs/architecture.md)
- [Data contracts / approvals](docs/data-contracts.md)
- [Codex PC operator workflow](docs/codex-workflow.md)
- [Rights, fact checking & provenance](docs/rights-and-sources.md)
- [QA & Definition of Done](docs/verification.md)
- [Assumptions, decisions & ADR](docs/assumptions-and-decisions.md)
- [Lean MVP /plan — 8 tasks](tasks/plan.md), [task checklist](tasks/todo.md)

## License

Chưa chọn license mã nguồn cho repo này. **Không tự suy ra MIT** từ thư viện bên ngoài. Khi tích hợp Lemo-Opuscar hoặc asset khác, phải kiểm tra điều khoản từng thành phần; tham khảo [rights policy](docs/rights-and-sources.md). Phim thương mại và quyền với bản dịch/tài liệu nguồn là các vấn đề riêng.

## Đóng góp

Đề xuất thay đổi qua PR; yêu cầu/spec, quyết định kiến trúc và quality gate phải được cập nhật trước khi triển khai. Không merge tài liệu này như bằng chứng engine đã hoạt động.
