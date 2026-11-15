# Implementation task list (future work, not yet started)

**Precondition:** SPEC and plan human-approved. Each slice affects ≤5 files. Commands are finalized after toolchain spike. No boxes below are checked.

## T01 — Environment and permission survey
- [ ] Report OS, RAM/free disk, Node/Python/FFmpeg, Codex image access and 0-cost constraints.
- [ ] No global installations or account charges.
- **Verify:** Captured command output + machine facts; record versions and workspace.
- **Depends:** SPEC approval. **Scope:** 1–2 files (survey/report).

## T02 — Engine spike contract
- [ ] Define same short scene, demo output + logging/ffprobe and rights/cost scoring across candidates.
- [ ] Assess Lemo-Opuscar explicitly; benchmark **at least two viable candidates** if available. If a candidate cannot run, record the reason rather than inventing a successful benchmark.
- **Verify:** reproducible instructions, outputs/logs for each candidate. **Depends:** T01. **Scope:** 3–5 files.

## T03 — Engine decision
- [ ] Rank actual visual fidelity, controllability, costs, machine load and maintainability.
- [ ] Owner approves selected engine, pin commit/version.
- **Verify:** signed-off ADR with video samples/benchmark. **Depends:** T02. **Scope:** 1–2 files.

## T04 — Shared channel/art direction model
- [ ] Define reusable style/characters/assets contract for 2.5D and three candidate treatments.
- [ ] Each asset has rights/provenance metadata.
- **Verify:** validator + sample references. **Depends:** T03. **Scope:** 3–5 files.

## T05 — Three animated style demos
- [ ] Produce three real short MP4 demos with 2.5D parallax/motion; each has preview frames.
- [ ] Record exact input, render time and quality issues; owner selects one.
- **Verify:** ffprobe + actual viewing + approval record. **Depends:** T04. **Scope:** separate scenes/tasks of ≤5 files.

## T06 — Minimal manifest schema, source and claim ledger
- [ ] Establish minimal versioned episode/source/claim/approval-event contracts needed by the pilot; validate topic/document input and legal status of public-domain original + translation.
- [ ] Map major claims to primary/reliable references; private inputs remain local absent external-provider consent.
- **Verify:** schema and path validation tests, rejected untrusted approval records, human source review. **Depends:** T01, T05. **Scope:** 3–5 files.

## T07 — Script and trusted owner-approval gate
- [ ] Write 60 s Vietnamese script with analysis, claim IDs and revision digest.
- [ ] Implement an explicit owner-confirmation path **separate from automatic Codex writes**, rejecting agent-generated/stale approval; invalidate on script edit.
- **Verify:** fail-closed tests for unsigned/forged/stale approval, valid owner action and revision invalidation. **Depends:** T06. **Scope:** 3–5 files.

## T08 — Vietnamese narration adapter and timing
- [ ] Produce authorized Vietnamese TTS sample under permitted commercial terms; measure actual per-line duration and draft SRT; consent from owner for provisional voice.
- [ ] If unavailable, mark `VOICE_PENDING` and do not approve final storyboard; changing voice/timing recomputes shot plan.
- **Verify:** listen to sample, check timing data and rights, negative test for missing voice. **Depends:** T07. **Scope:** 3–5 files.

## T09 — Storyboard and approval gate
- [ ] Produce proportional pilot boards and detailed scene plan based on approved script **and measured voice timing**.
- [ ] Explicit owner board approval binds script/board/timing hashes; material changes invalidate it; no production without both approvals.
- **Verify:** missing/stale/forged approval tests and owner board signoff. **Depends:** T07, T08. **Scope:** 3–5 files.

## T10 — Scene renderer and cache
- [ ] Render 2+ independent scenes using chosen engine with versioned inputs.
- [ ] 720p preview / fresh 1080p/24fps master, atomic validated outputs, cache digest and basic stop/resume.
- **Verify:** ffprobe, frame samples, changed-input rerender and interrupted run. **Depends:** T05, T08, T09. **Scope:** 3–5 files.

## T11 — Audio, assembly and media QA
- [ ] Mix voice/music/SFX, export subtitle, combine scenes, generate YouTube package.
- [ ] Check audio intelligibility/sync, video stream, black frames, license state.
- **Verify:** real 60 s MP4 playback + ffprobe + QA report; block invalid output. **Depends:** T10. **Scope:** 3–5 files.

## T12 — Retry/recovery
- [ ] Diagnose and correct defects within bounded attempts, proving interrupted jobs resume without rerendering verified scenes.
- [ ] Failed or uncertain scenes become `NEEDS_REVIEW`, not PASS.
- **Verify:** deliberately interrupt, rerun, compare file hashes/logs. **Depends:** T10, T11. **Scope:** 3–5 files.

## T13 — Cleanup and retention
- [ ] Propose cache TTL/size and obtain approval; implement safe dry-run.
- [ ] Preserve protected sources, approvals, legal evidence and final masters.
- **Verify:** fixture-based deletion exclusions, dry-run review, recovery test. **Depends:** T12. **Scope:** 3–5 files.

## T14 — Scale experiment and go/no-go
- [ ] Bench 2–3 min and 5 min, only then plan long-form 20–30 min.
- [ ] Compare sustained speed with desired ≥1 video/day without sacrificing quality.
- **Verify:** playable media, benchmarks, explicit human go/no-go. **Depends:** T11–T13. **Scope:** reports/bench scripts ≤5 files each.

## Review checkpoints

- After T03: engine decision approval.
- After T05: visual style approval.
- After T07: script approval.
- After T09: storyboard approval.
- After T11: pilot QA review.
- Before T13 destructive cleanup: retention policy approval.
- Before long-form rollout: benchmark evidence and human go/no-go.

All tasks must satisfy [DoD](../docs/verification.md). Revisit scope rather than marking an unfinished task complete.
