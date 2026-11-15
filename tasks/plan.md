# Implementation plan — after SPEC approval

**Status:** proposed / no implementation yet. Dependency direction: discovery → 3 demos → human style choice → pilot → recovery → scaling. Do not code this in the documentation PR.

## Phase 0 — Repo bootstrap (documentation)

- **Deliverable:** README, AGENTS, SPEC, architecture, contracts, rights, workflow, verification, tasks.
- **Gate:** Human reviews/approves this documentation PR. No runtime claim.

## Phase 1 — Ground truth and engine assessment

1. Host survey and project-scoped installation permissions; record Node/Python/FFmpeg/GPU/RAM/paths and image entitlement.
2. Assess Lemo-Opuscar and other candidate engines, investigate current official docs/licensing. Log candidates rejected as incompatible, and pin tested versions.
3. Design common micro-storyboard 10–20 s and run each candidate with same subject and visual constraints; collect actual frames, MP4, logs, ffprobe and peak resource numbers.
4. Review decision matrix; user approves engine. No spending.

**Checkpoint:** Candidate comparison with measured data and no claim of 30 min throughput.

## Phase 2 — 3 style demos

1. Define three distinct **cinematic 2.5D** treatments without pixel art, with character/setting reference and image rights.
2. Generate/obtain legitimate layered assets; keep asset registry and deterministic style bible drafts.
3. Produce true short animations and contact sheets (camera/parallax/environmental/limited character motion).
4. Review with owner; one winning style approved.

**Checkpoint:** Three playable demos; consistent chosen visual rules.

## Phase 3 — Pilot 60 seconds

1. Propose actual public-domain work; verify original/translation; prepare source/claim ledger.
2. Draft Vietnamese summary + analysis; obtain **owner-confirmed script approval** for exact revision.
3. Obtain owner-authorized, licensed Vietnamese sample TTS; measure durations and generate timing map. If no suitable voice, set `VOICE_PENDING` and block final board approval/render.
4. Produce shot plan and storyboard proportionate to 60 s using real narration timing; obtain **board approval** bound to script, boards and voice timing.
5. Render several scenes, audio/SFX, preview 720p; full QA; rerender 1080p from source. Refuse agent-authored/stale approval events.
6. Export MP4/SRT/thumbnail/metadata/credits/rights/QA only if rights/media gates pass; owner manual upload.

**Checkpoint:** 60-second artifact with demonstrated image/audio sync and cleared assets; failed QA isn't PASS.

## Phase 4 — Reliability

1. Harden the minimal manifest/approval schema established during the pilot: invalid revision, forged approval, inconsistent TTS timing, crash recovery and negative-path tests.
2. Render cache keys, crash-resume and bounded retry.
3. Cost/quota and disk guards; rights gate; cleanup policy dry-run and protected files.
4. Repeat one-scene rerender and interrupted run; verify no unintended data loss.

**Checkpoint:** Real resume and targeted rerender proof; user approves cleanup policy.

## Phase 5 — Scaling

Produce 2–3 minute multi-scene sample, then 5-minute chapter, finally 20–30 min episode if benchmarks and visual quality meet threshold. Record measured capacity vs desired ≥1/day. Consider worker service/parallelism **only after** evidence.

## Major risks and mitigations

- Free image limitations: reuse assets, procedural 2.5D where effective, pause on quota.
- Voice quality/commercial terms: provider adapter, test sample, licensing checkpoint.
- Copyright: work/translation/license records and per-episode rights gate.
- RAM/iGPU limitations: start one worker, 720p preview, separate final.
- Long rendering: scene isolation/cache, no monolithic job.
- AI-generated inconsistencies: channel bible, recurring refs, scene QA.
- User approval mismatch: revision digests plus **owner-controlled confirmation**; reject forged/stale events and invalidate on material edits.
- Private source leakage: local-first processing and destination-specific consent before external AI/TTS/image calls.

## Plan acceptance

Every implementation task in [todo.md](todo.md) has dependencies, narrow file scope, measurable acceptance and verification. **Plan approval is distinct from SPEC approval** under gated workflow. No implementation until both approved.
