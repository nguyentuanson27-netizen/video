# AI Video Studio

> **Status: SPEC v1 đã merge; kế hoạch MVP tối giản đang review — documentation only.** Chưa có pipeline chạy được, engine chưa được chọn và chưa có video pilot được kiểm chứng.

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
| Đặc tả, kiến trúc, kế hoạch | Có tài liệu để review |
| Lựa chọn engine, TTS tiếng Việt, bản sắc kênh | **Chưa xác nhận**, cần benchmark/duyệt |
| Mã thực thi, CLI sản xuất, tests runtime | **Chưa triển khai** |
| MP4 pilot hoặc bằng chứng render trên máy Windows | **Chưa có** |

## Bắt đầu từ đây

1. Đọc [SPEC v1](docs/spec.md), đặc biệt mục **Open decisions**, và [assumptions](docs/assumptions-and-decisions.md).
2. Duyệt đặc tả trước khi mở PR implementation.
3. Cho Codex PC đọc [AGENTS.md](AGENTS.md) và [hướng dẫn vận hành](docs/codex-workflow.md).
4. Thực hiện [kế hoạch MVP 60 giây (8 task)](tasks/plan.md) và [task checklist](tasks/todo.md). **Không xây DB/queue, engine adapters, secure approval service trước pilot.**
5. Theo [bộ tiêu chí kiểm chứng](docs/verification.md) và [quy định bản quyền](docs/rights-and-sources.md).

**Chưa có lệnh `install`, `build`, `render` hoặc `test` nào thuộc project hoạt động**. Không chạy lệnh tưởng tượng. Các lệnh benchmark được viết trong plan chỉ là lệnh dự kiến, cần cập nhật sau khi chọn engine và tạo runner.

## Định hướng kiến trúc

```text
User topic / documents
  → research + claim ledger → outline → script → [APPROVAL: SCRIPT]
  → confirmed permitted Vietnamese TTS + measured timings → scene/shot plan
  → storyboard (pilot 3–6 hình; 12–20 cho video dài) → [APPROVAL: STORYBOARD]
  → asset registry → scene renderer (engine adapter) → QA/retry → per-scene masters
  → episode assembly → final QA → MP4/SRT/thumbnail/metadata/credits
```

Xem [architecture](docs/architecture.md) và [data contracts](docs/data-contracts.md). Lemo-Opuscar là **ứng viên**, không phải engine bắt buộc; benchmark phải có video từ máy thực và log tài nguyên.

## Cấu trúc repo dự kiến

```text
AGENTS.md                       # Quy tắc Codex
docs/                           # SPEC, ADR, vận hành, quyền, verification
tasks/                          # Plan và task breakdown
schemas/                        # JSON Schema (giai đoạn build)
pipeline/                       # Orchestration/adapters (giai đoạn build)
tests/                          # Contract/unit/integration (giai đoạn build)
episodes/<slug>/                # Manifest, script, approval, nguồn (giai đoạn build)
runtime/                        # Cache/output cục bộ, gitignored (giai đoạn build)
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
