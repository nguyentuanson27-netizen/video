# Giọng thử tiếng Việt

**Trạng thái:** `VOICE_PENDING` · Chờ chủ dự án đồng ý một giọng dựng sẵn.

| Giọng | Đặc điểm theo nhà phát hành |
| --- | --- |
| Ngọc Huyền | Nữ, miền Bắc, đọc tự nhiên |
| Quang Sơn | Nam, miền Trung, đọc tự nhiên |

Cả hai có trong danh sách của [demo công khai VieNeu-TTS v3 Turbo](https://huggingface.co/spaces/pnnbao-ump/VieNeu-TTS-v3-Turbo). Có thể chọn tên giọng và nghe bằng văn bản mẫu điền sẵn trên trang.

## Quyền sử dụng và môi trường

- VieNeu-TTS v3 Turbo, model `pnnbao-ump/VieNeu-TTS-v3-Turbo`, revision `61b85e3d937fbbacb387714180e8182823512523`. Model card xác nhận Apache-2.0 bao gồm preset đi kèm, có sự đồng ý của người nói hoặc bên giữ quyền, và cho phép dùng âm thanh sinh từ những preset này trong video thương mại, kể cả video bật kiếm tiền. Giữ ghi công VieNeu-TTS, Phạm Nguyễn Ngọc Bảo và tên preset trong credits. [Model card và điều khoản sử dụng](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo/blob/61b85e3d937fbbacb387714180e8182823512523/README.md)
- Đường chạy thử sẽ dùng SDK `vieneu==3.7.1`, ONNX Runtime trên CPU, FP32. Toàn bộ lời đọc của pilot sẽ được xử lý cục bộ bằng preset dựng sẵn. [Tài liệu SDK 3.7.1](https://pypi.org/project/vieneu/3.7.1/)
- Ngày 2026-11-16, `pip install --dry-run --only-binary=:all: vieneu==3.7.1` giải được các wheel cho Python 3.11/Windows hiện tại, gồm SDK 3.7.1 và ONNX Runtime 1.32.0. Báo cáo cục bộ là `work/m04-vieneu-resolve.json`. Chưa chạy inference hoặc đo WAV.
