# Giọng thử tiếng Việt

**Giọng thử:** Quang Sơn, nam miền Trung. Chủ dự án chọn ngày 2026-11-16 trong [Codex](approvals.md). [Demo của nhà phát hành](https://huggingface.co/spaces/pnnbao-ump/VieNeu-TTS-v3-Turbo)

## Quyền sử dụng và môi trường

- VieNeu-TTS v3 Turbo, model `pnnbao-ump/VieNeu-TTS-v3-Turbo`, revision `61b85e3d937fbbacb387714180e8182823512523`. Model card xác nhận Apache-2.0 bao gồm preset đi kèm, có sự đồng ý của người nói hoặc bên giữ quyền, và cho phép dùng âm thanh sinh từ những preset này trong video thương mại, kể cả video bật kiếm tiền. Giữ ghi công VieNeu-TTS, Phạm Nguyễn Ngọc Bảo và tên preset trong credits. [Model card và điều khoản sử dụng](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo/blob/61b85e3d937fbbacb387714180e8182823512523/README.md)
- Lượt chạy cục bộ dùng SDK `vieneu==3.7.1`, ONNX Runtime 1.32.0 trên CPU và SEA-G2P 0.10.0. Codec MOSS-Audio-Tokenizer-Nano-ONNX dùng revision `ceff0d0749bfb3fa2d61149794ec6feef0d1e1ae`, Apache-2.0. [Tài liệu SDK](https://pypi.org/project/vieneu/3.7.1/) · [Model card codec](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX)

## Bản thử và cách tái hiện

Chạy trong repo Windows. Bước fetch tải các tệp model công khai. Bước tạo WAV đọc script và chạy suy luận cục bộ ở chế độ offline.

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: vieneu==3.7.1
.\.venv\Scripts\python.exe narration.py --fetch-models
.\.venv\Scripts\python.exe narration.py
ffprobe -v error -show_entries 'stream=codec_name,sample_rate,channels,duration' -of json work/pilot/narration.wav
```

Bản đọc thử có 13 đoạn nguồn dài tổng cộng 41,680 giây, trước cắt khoảng trống và chỉnh nhịp bằng FFmpeg `atempo=0.84`. WAV ghép thử dài 56,952125 giây, mono PCM 16-bit, 48 kHz. Bản thử, SRT và file `narration-timing.json` lưu ở `work/pilot/`.

## Kiểm tra bản thử

- FFmpeg giải mã hết WAV. FFplay có mã thoát 0 với SDL dummy. Đo loudness tích hợp −22,0 LUFS và true peak −3,0 dBFS. SHA-256 của WAV là `5f4378d0a47521ec108740f11dc9bcfe43e88ea36de78b1a92be5bd9a04f772e`.
- 13 cue SRT trùng phần lời của kịch bản được duyệt. Mốc tăng dần, không chồng, khớp số mẫu của đoạn ghép và nằm trong thời lượng WAV. Thử đổi nội dung kịch bản và trạng thái giọng sang `VOICE_PENDING` trong bản sao tạm. Cả hai bị từ chối.
- Nhận dạng cục bộ với Whisper-small và PhoWhisper-small trả về nhiều khác biệt ở lời kể. Ví dụ gần giây 14, PhoWhisper nhận “Gió Bắc ào tới” thành “gió bắt áo tới”. Kết quả cả bản lần lượt đạt 40,4% và 71,9% độ tương đồng chuỗi tiếng, gồm các phần ASR có thể tự chèn trong khoảng lặng. Đây là chỉ số so khớp bản chép tự động. [Whisper-small](https://huggingface.co/Systran/faster-whisper-small) · [PhoWhisper](https://github.com/VinAIResearch/PhoWhisper) · [Bản CT2 dùng cho phép thử](https://huggingface.co/qbsmlabs/PhoWhisper-small)
- Đã đối chiếu với các đoạn nguồn chưa chỉnh nhịp, thử hai bản SDK và bộ phiên âm, checkpoint ONNX cũ hơn, thay đổi sampling và PyTorch CPU. Các bản thử ngắn vẫn có sai khác ở cụm quan trọng như “phân thắng bại” và “quất phần phật”. Log lưu trong `work/m04-*.log`. Phiên Codex kiểm tra bằng phát lại và nhận dạng cục bộ. M04 chờ chủ dự án nghe để xác nhận giọng thử.
