# Architecture v1 — Proposed, not yet implemented

## Goals / driving constraints

A solo creator with Codex PC needs consistently high-quality Vietnamese animated storytelling, monetizable rights compliance, resumable scene rendering and near-zero per-video cost on a 16 GiB Windows machine.

**Decision strategy:** engine-neutral orchestration with one chosen renderer adapter after measured three-demo spike; no premature daemon, database or dashboard.

## Logical modules

```text
topics+inputs
   └─ Research / source registry ── claim ledger
         └─ Script writer ── [script approval with hash]
               └─ Voice timing draft + scene/shot planner
                     └─ Storyboard ── [board approval with hash]
                           └─ Asset resolver / license register
                                 └─ Engine adapter ── scene render/cache
                                       └─ scene QA + bounded retry
                                             └─ final assembly + episode QA
                                                   └─ publish package (manual upload)
```

- **Coordinator:** Codex PC uses versioned manifests, does not require a live long-running service for MVP.
- **Content layer:** authoritative source records + evidence for each major claim. Interpretation clearly labeled.
- **Story layer:** script in Vietnamese; per-scene timing driven by actual TTS duration. Approvals are immutable events, never a mutable boolean alone.
- **Art layer:** channel style bible with reference assets, camera grammar, palettes, scene-depth layers; asset hashes, licenses, source and generation metadata.
- **Render layer:** scene adapter with `render(scene, profile) -> artifact + metadata`; 720p review and **fresh** 1080p render from same scene source.
- **Audio:** interchangeable Vietnamese TTS provider; voice WAV per segment, music/SFX and ducking, timestamp source of truth.
- **Assembler:** only consumes validated scene masters; normalizes stream properties before concat/mux; exports full package.
- **QA:** validates duration, sync, screenshots, missing frames, audio, subtitle legibility, rights and traceability. User approval separate from machine checks.

## Engine selection spike (not a predetermined choice)

Compare 2–3 feasible candidates, including [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar), using the same 10–20 s source treatment, audio and target output. Assess:

1. **Visual quality:** multilayer 2.5D depth, parallax, continuous cinematic camera, readable faces/text, non-slideshow.
2. **Agent controllability:** can Codex create/edit frames and scene deterministically without manual GUI dependence?
3. **Reliability:** scene render, isolated failure and rerun, ffprobe-valid output, no missing/blank frames.
4. **Performance:** wall-clock/scene, peak memory, CPU/GPU feasibility, temp disk, render fidelity at 720p and 1080p.
5. **Licensing and cost:** renderer source code, style guidance, sample assets, output and TTS commercial terms.
6. **Maintainability:** clear adapter boundary, minimum dependency complexity, stable API/source.

Record sample video paths, measured evidence, machine version and tradeoffs in a proposed ADR; get owner's approval. **Lemo-Opuscar's documented 30–60 s norm and caveat at >2–3 min make per-scene integration an experiment, not proof it scales to 30 min.** Its code, guidance and sample media have different licenses; read its LICENSE at the exact tested commit.

## Scene contract and boundaries

- Scene source and data lives in project; renderer does not own story/approval state.
- A scene is reproducible from a tuple of `scene_spec_sha`, `style_version`, `asset_hashes`, `voice_timing_version`, `renderer_version`, `render_profile`.
- Content-addressed outputs; atomic promote only after ffprobe/QA success. Failed attempts never overwrite prior approved masters.
- Preview and final are separate output profiles. Don't mistake 720p upscale for final-resolution rendering.
- Orchestrator logs attempts and actionable failure reasons, limits retries and preserves failed artifacts for diagnosis.

## State machine

```text
IDEA → RESEARCHED → SCRIPT_DRAFT → SCRIPT_APPROVED
     → BOARD_DRAFT → BOARD_APPROVED → READY_TO_RENDER
     → RENDERING → QA → READY_FOR_MANUAL_UPLOAD
                        └─ NEEDS_REVIEW / BLOCKED
```

Any edit to approved script or relevant storyboard/asset set invalidates affected downstream approvals. `BLOCKED_RIGHTS` and `BLOCKED_QUOTA` are safe pauses, never routed to the publish-ready state. Batch approval means separate event for each episode+revision.

## Failure modes / safety

- **Incomplete or contradictory sources:** mark claims uncertain and stop script approval if central to narrative.
- **Unlicensed assets/translation:** block publication package; no automated commercial use.
- **Free image quota exhausted:** preserve state, report alternatives, do not purchase.
- **Renderer crash / machine restart:** use manifest and cache to skip verified scenes; rerender failed only.
- **Low disk/memory:** fail safe before large job; single worker default until measured.
- **Inconsistent characters:** style bible + reference sheets; visual review at scene transition level.
- **Untrusted materials:** local sandbox, limit file input sizes/types, no execution from source materials, strict paths, secrets in env outside git.

## Alternatives not selected yet

- **Fork Lemo-Opuscar:** not justified before showing a missing engine capability. Prefer pinned external dependency/adapter and contribute only if needed.
- **One 30 min continuous render:** expensive to restart/debug; scene isolation is required.
- **Microservices/queue DB/cloud fleet:** increases operational/security complexity against near-zero budget and Codex PC-only MVP.
- **Pure image slideshow:** fails stated animation quality target.

## Future scaling — explicitly not MVP

Bench a ~2–3 min multi-scene episode, then a 5 min chapter, then 20–30 min. Add a Windows worker service only if restarting Codex PC becomes actual blocker. Measure throughput before designing parallelism.
