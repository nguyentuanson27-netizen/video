# Implementation task list (future work, not yet started)

**Precondition:** SPEC and plan human-approved. Each slice affects ≤5 files. Commands are finalized after toolchain spike. No boxes below are checked.

## T01 — Environment and permission survey
- [ ] Report OS, RAM/free disk, Node/Python/FFmpeg, Codex image access and 0-cost constraints.
- [ ] No global installations or account charges.
- **Verify:** Captured command output + machine facts; record versions and workspace.
- **Depends:** SPEC approval. **Scope:** 1–2 files (survey/report).

## T02 — Engine spike contract
- [ ] Define same short scene, demo output + logging/ffprobe and rights/cost scoring across candidates.
- [ ] At least two feasible candidates evaluated, including Lemo-Opuscar.
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

## T06 — Source and claim ledger
- [ ] Validate topic/document input and legal status of public-domain pilot original + translation.
- [ ] Map major claims to primary/reliable references.
- **Verify:** invalid path/source tests, human source review. **Depends:** T01, T05. **Scope:** 3–5 files.

## T07 — Script and approval gate
- [ ] Write 60 s Vietnamese script with analysis, claim IDs, revision digest.
- [ ] Refuse storyboard/full render without human script approval; invalidate on edit.
- **Verify:** state-machine and revision-invalidation tests. **Depends:** T06. **Scope:** 3–5 files.

## T08 — Storyboard and approval gate
- [ ] Produce proportional pilot boards and detailed scene plan, match approved script.
- [ ] Board changes invalidate board approval; no production without both approvals.
- **Verify:** missing/stale approval contract tests and owner board signoff. **Depends:** T07. **Scope:** 3–5 files.

## T09 — Vietnamese narration adapter
- [ ] Produce sample Vietnamese voice under permitted terms; word/line timing and SRT.
- [ ] Voice remains replaceable; chosen channel voice not assumed.
- **Verify:** listen to sample, compare transcript/time stamps, rights review. **Depends:** T07. **Scope:** 3–5 files.

## T10 — Scene renderer and cache
- [ ] Render 2+ independent scenes using chosen engine with versioned inputs.
- [ ] 720p preview / fresh 1080p/24fps master and cache digest.
- **Verify:** ffprobe, frame samples, changed-input rerender. **Depends:** T05, T08, T09. **Scope:** 3–5 files.

## T11 — Audio, assembly and media QA
- [ ] Mix voice/music/SFX, export subtitle, combine scenes, generate YouTube package.
- [ ] Check audio intelligibility/sync, video stream, black frames, license state.
- **Verify:** real 60 s MP4 playback + ffprobe + QA report; block invalid output. **Depends:** T10. **Scope:** 3–5 files.

## T12 — Retry/recovery
- [ ] Bound correction attempts; resume after interruption without rerendering approved scenes.
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
- After T08: storyboard approval.
- After T11: pilot QA review.
- Before T13 destructive cleanup: retention policy approval.
- Before long-form rollout: benchmark evidence and human go/no-go.

All tasks must satisfy [DoD](../docs/verification.md). Revisit scope rather than marking an unfinished task complete.
