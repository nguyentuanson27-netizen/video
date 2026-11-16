# Duyệt pilot

## Kịch bản

**Trạng thái:** `SCRIPT_APPROVED`

Ngày 2026-11-16 (UTC+07:00), chủ dự án trả lời “duyệt” trong Codex ngay sau khi được hỏi duyệt `script-v1`.

Bản gửi duyệt ngày 2026-11-16 (UTC+07:00) là [`script-v1`](script.md), SHA-256 `2b7ff06a75d428151121b4b8266d6221a41089fa07a7866664436d0c7038a5a4`. Hash tính trên toàn bộ nội dung UTF-8 của `script.md` với xuống dòng chuẩn hóa thành LF để dùng được trên Windows và trong Git.

## Giọng thử

**Trạng thái:** `VOICE_TRIAL_APPROVED`

Ngày 2026-11-16 (UTC+07:00), chủ dự án chọn **Quang Sơn** để thử đọc `script-v1`. Đây là preset dựng sẵn của [VieNeu-TTS v3 Turbo](voice.md).

**Bản đọc được chấp nhận:** `VOICE_READY`. Ngày 2026-11-16 (UTC+07:00), sau khi nhận bản WAV và ghi chú kiểm tra, chủ dự án xác nhận đây là giọng địa phương và yêu cầu “tiếp tục đi”.

- WAV `work/pilot/narration.wav`, SHA-256 `5f4378d0a47521ec108740f11dc9bcfe43e88ea36de78b1a92be5bd9a04f772e`.
- [Timing 13 cue](narration-timing.json), SHA-256 UTF-8 LF `8069808bbfa6af842f15e05bfc5cc324720c295f44c111f52548707b7aa07879`.

## Storyboard

**Trạng thái:** `BOARD_PENDING`

Bản gửi duyệt ngày 2026-11-16 (UTC+07:00) là [`board-v1`](storyboard.md). SHA-256 UTF-8 LF của storyboard `c9ea0dca3c2cae71de0eedf9351a2e01dc53b6bc3b7b05d03d6e87bae58f4b0b`. Bản này gắn với `script-v1` (`2b7ff06a75d428151121b4b8266d6221a41089fa07a7866664436d0c7038a5a4`) và timing Quang Sơn (`8069808bbfa6af842f15e05bfc5cc324720c295f44c111f52548707b7aa07879`).
