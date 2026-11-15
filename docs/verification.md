# Verification and Definition of Done

> **MVP ưu tiên:** Chỉ cần bằng chứng thực tế của 3 demo style và pilot 60 giây (ffprobe + xem/nghe hết video), hash bản đã duyệt, nguồn/quyền asset, thử sửa một scene. Các mục schema/auth/forged-event/retention automation bên dưới là **kiểm thử cho phiên bản mở rộng**, không phải blocker để tạo pilot. Theo [MVP plan](../tasks/plan.md).

**State:** Verification plan for future code. No runtime tests or video-render verification have run for this documentation PR.

## SPEC/Docs PR gate

- [ ] README clearly identifies project as not yet implemented, links all necessary docs.
- [ ] SPEC covers objective, structure, commands reality, code conventions, tests, boundaries and acceptance.
- [ ] Human script/storyboard checkpoints theo revision/hash, quyền asset cơ bản, chi phí bằng 0 và engine TBD nhất quán.
- [ ] Tasks are dependencies-first, each has measurable acceptance and verification.
- [ ] No secret, private source document or unlicensed media checked in.
- [ ] No broken relative links across **all** Markdown documents; illustrative fenced JSON blocks parse, Markdown fences are balanced.
- [ ] No claim that runtime is working without evidence.

## Future implementation gates

### Unit/contract
- Manifest schema rejects missing IDs, unsafe paths, invalid profiles and inconsistent revisions.
- Script/board/voice timing thay đổi đáng kể phải xin duyệt lại; MVP chỉ kiểm tra hash/revision tránh nhầm bản, không triển khai chống giả mạo/xác thực.
- Concurrent/incomplete render cannot promote partial artifact; cache key changes on source/assets/style/profile.
- Retry is bounded; no successful state is inferred from process exit alone.
- Cleanup dry-run excludes approved materials, original references, licenses and masters.

### Integration/media
- Render one real scene and two-scene sequence; ffprobe validates duration, 1280×720 preview and **1920×1080 @24fps final generated from source**.
- Interrupt between scene renders and resume; only missing/invalid scenes re-render.
- Authorized, commercially permitted Vietnamese voice selected before final storyboard approval; narration intelligible, measured timings align to approved shot plan and SRT; audio ducking verified by listening and measurements.
- Subtitles visible, not cut off, readable and timed to voice.
- Contact sheets and actual playback show non-slideshow motion, no unexpected blank frames, continuity and no severe visual artifacts.
- Rights report complete and no unresolved license status for publish-ready package.
- Failed QA → classify defect, record corrective change and rerender; after bounded failure `NEEDS_REVIEW`, never fake PASS. A blind identical retry does not count as a fix.

### Performance and cost
- Record **measured** FPS/seconds per produced minute, RSS/total RAM, CPU, disk, render workers and 720p/1080p comparison on actual Windows host.
- No promise of ≥1 video/day without sustained full-episode measurements.
- Inspect actual free/existing entitlements and billing terms before invoking tools; never authorize incremental spending or send private user sources to external services without permission.

## Pilot publication readiness checklist

Do **not** mark the 60-second pilot ready for manual upload unless all are true:

- Script/board/timing khớp bản người dùng đã duyệt trong Codex PC; ghi rõ revision trong `approvals.md`.
- Final source-rendered MP4 is **1920×1080 at 24 fps** and has an audible, clear Vietnamese narration track; audio/video streams are valid by ffprobe.
- The entire pilot has been played and inspected; no unexpected blank frames, clipped narration, unreadable subtitles, severe character discontinuity or stuck static slideshow.
- SRT text matches narration and its timestamps stay synchronized (exact tolerances must be benchmarked/defined by the implementation, not invented in SPEC).
- Rights ledger lists the original work, edition/translation, every incorporated asset and voice/music license; unresolved commercial rights = blocked.
- Thumbnail, title, description, subtitle, credits, rights and QA reports are present and linked to the exact output revision.
- If any criterion fails: `NEEDS_REVIEW` or `BLOCKED_RIGHTS`, **not** release-ready.

## Ship/merge policy

- Documentation PR: review consistency/link existence, **no runtime CI claim**.
- Engine spike PR: measured video evidence + command/log + licensing analysis.
- MVP pilot PR: end-to-end real media, ffprobe, manual audio/visual review and reproduction steps.
- Human reviews SPEC and plan before production implementation.
- For every future code PR report actual commands executed, output and failure paths.
- DoD: correctness, security, maintainability, integration, documentation, reversibility and human review; never substitute prose for test evidence.
