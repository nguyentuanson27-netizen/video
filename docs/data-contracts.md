# Data contracts v1 (proposed)

> **Sau MVP, chỉ để tham khảo.** Đối với pilot 60 giây, **không viết JSON Schema, event-sourcing hoặc approval attestation service**. Dùng các file `episodes/pilot/{script.md,sources.md,storyboard.md,approvals.md}`; trong `approvals.md` ghi user đã duyệt gì trong Codex PC, thời điểm và hash/revision để tránh nhầm bản. Thêm `work/` cho WAV/ảnh/video tạm. Nếu pilot thành công rồi cần queue/multi-episode, mới đánh giá hợp đồng JSON bên dưới. Xem [MVP plan](../tasks/plan.md).

These are **future design contracts**, not existing JSON Schema or implemented API. Do **not** build them as prerequisites for MVP. JSON examples are illustrative; no production command loads them yet.

## Version and identities

- Every manifest declares `schema_version: "1"`, immutable `episode_id`, `revision`, `created_at` UTC.
- Version/hash the script, boards, style bible, source ledger and renderer input before work starts.
- Never interpret missing approval fields as approved. Hash includes relevant referenced files. Workflow/approval status in a manifest is **derived**, never authoritative proof of a human decision.
- Use file paths relative to allowed episode/workspace root; reject `..`, absolute paths and symlink escapes.

## Episode manifest example

```json
{
  "schema_version": "1",
  "episode_id": "pilot-001",
  "revision": 1,
  "kind": "literature",
  "target_seconds": 60,
  "language": "vi-VN",
  "script": {"path": "script.md", "sha256": "<content-sha256>"},
  "storyboard": {"path": "storyboard.json", "sha256": "<content-sha256>"},
  "style_version": "pending-selection",
  "workflow_state": "BOARD_DRAFT",
  "approval_log_path": "approvals/events.jsonl",
  "render_profile": {"preview": "1280x720@24", "final": "1920x1080@24"},
  "scenes": [
    {"id": "s001", "spec_path": "scenes/s001.json", "status": "PENDING"}
  ],
  "rights_status": "PENDING_REVIEW"
}
```

## Approval events

**Future only:** This event structure is an example for batch processing. MVP uses a human-confirmed Markdown checklist plus file hash; it is not tamper-resistant and does not need cryptographic proof or a separate writer.

```json
{
  "schema_version": "1",
  "episode_id": "pilot-001",
  "gate": "SCRIPT",
  "decision": "APPROVED",
  "actor": "human-owner",
  "timestamp_utc": "2026-11-15T12:00:00Z",
  "script_sha256": "<script-sha256>",
  "storyboard_sha256": null,
  "voice_timing_sha256": null,
  "confirmation_method": "owner-interactive-confirmation",
  "notes": "Owner confirmed displayed digest; example only"
}
```

`gate` ∈ `SCRIPT | STORYBOARD | RIGHTS`; `decision` ∈ `APPROVED | REJECTED | NEEDS_CHANGES`. A storyboard event must contain **non-null** storyboard and voice-timing hashes and match the currently approved script. `RIGHTS` is a separate review gate; it cannot waive an actual missing commercial-use right. A generated assistant message or agent-created event does not constitute approval. No attestation mechanism is needed for the personal, single-episode MVP; explicit owner confirmation in Codex PC remains required.

## Source and claim records

```json
{
  "source_id": "src-001",
  "title": "Primary-source edition",
  "locator": "public URL or relative local file reference",
  "accessed_at_utc": "2026-11-15T12:00:00Z",
  "work_author": "Author name",
  "edition_translation": "Original edition / translator if relevant",
  "rights": {"status": "UNVERIFIED", "license": null, "evidence_locator": null}
}
```

```json
{
  "claim_id": "clm-001",
  "text": "Factual assertion",
  "kind": "FACT",
  "source_ids": ["src-001"],
  "locator_detail": "page/chapter/paragraph/time",
  "confidence": "VERIFIED",
  "review_notes": ""
}
```

`kind` ∈ `FACT | INTERPRETATION | DRAMATIZATION`. `confidence` ∈ `VERIFIED | CONTESTED | UNVERIFIED`. Avoid pretending numerical probabilities are objectively measured. Important historical assertions require credible evidence; interpretations need separate labels.

## Scene and artifacts

```json
{
  "schema_version": "1",
  "scene_id": "s001",
  "duration_seconds": 12.0,
  "narration_segments": ["line-01", "line-02"],
  "asset_ids": ["asset-background-01", "asset-hero-01"],
  "layers": [{"asset_id": "asset-background-01", "z": 0, "parallax": 0.2}],
  "camera": [{"time": 0, "zoom": 1}, {"time": 12, "zoom": 1.08}],
  "motion_intensity": "LOW",
  "renderer_adapter": "TBD"
}
```

An artifact record includes `scene_id`, `render_profile`, `input_digest`, `output_path`, `sha256`, `ffprobe_metadata`, `qa_status`, `attempt`, `error_reason` if failed, and corrective-action notes when a defect is repaired. Use an atomic rename to change status from candidate to validated.

## Asset rights/provenance

Every asset has `asset_id`, `origin` (`USER | LICENSED | GENERATED | PROCEDURAL`), `locator`, `content_sha256`, `license_name`, `commercial_use_confirmed`, `evidence`, `generation_tool_version` if relevant, and attribution requirements. `UNKNOWN` rights blocks use for monetized output.

## Cleanup records

Dry-run reports `candidate_path`, `reason`, `size`, `age`, `referenced_by`, `protected`. Only derived, unreferenced, non-protected data may be removed. Never delete approved source, approval logs, license proof or sole copy of final master. Retention duration is undecided until approved.
