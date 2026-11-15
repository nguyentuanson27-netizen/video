# Data contracts v1 (proposed)

These are **design contracts**, not existing JSON Schema or implemented API. Validate and version them in an implementation PR. JSON examples are illustrative; no production command loads them yet.

## Version and identities

- Every manifest declares `schema_version: "1"`, immutable `episode_id`, `revision`, `created_at` UTC.
- Version/hash the script, boards, style bible, source ledger and renderer input before work starts.
- Never interpret missing approval fields as approved. Hash includes relevant referenced files.
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
  "approval_state": "BOARD_DRAFT",
  "render_profile": {"preview": "1280x720@24", "final": "1920x1080@24"},
  "scenes": [
    {"id": "s001", "spec_path": "scenes/s001.json", "status": "PENDING"}
  ],
  "rights_status": "PENDING_REVIEW"
}
```

## Approval events

Store append-only entries, not one mutable `approved: true`. A batch approval operation still writes one event per episode, each tied to exact hashes.

```json
{
  "schema_version": "1",
  "episode_id": "pilot-001",
  "gate": "SCRIPT",
  "decision": "APPROVED",
  "actor": "human-owner",
  "timestamp_utc": "2026-11-15T12:00:00Z",
  "revision_sha256": "<script-sha256>",
  "notes": "Approved via Codex PC"
}
```

`gate` ∈ `SCRIPT | STORYBOARD | RIGHTS`; `decision` ∈ `APPROVED | REJECTED | NEEDS_CHANGES`. A generated assistant message does not constitute approval. Approval record must identify its real source; implementation must never fabricate approvals.

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

An artifact record includes `scene_id`, `render_profile`, `input_digest`, `output_path`, `sha256`, `ffprobe_metadata`, `qa_status`, `attempt`, `error_reason` if failed. Use an atomic rename to change status from candidate to validated.

## Asset rights/provenance

Every asset has `asset_id`, `origin` (`USER | LICENSED | GENERATED | PROCEDURAL`), `locator`, `content_sha256`, `license_name`, `commercial_use_confirmed`, `evidence`, `generation_tool_version` if relevant, and attribution requirements. `UNKNOWN` rights blocks use for monetized output.

## Cleanup records

Dry-run reports `candidate_path`, `reason`, `size`, `age`, `referenced_by`, `protected`. Only derived, unreferenced, non-protected data may be removed. Never delete approved source, approval logs, license proof or sole copy of final master. Retention duration is undecided until approved.
