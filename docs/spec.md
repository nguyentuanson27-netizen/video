# SPEC v1 — AI Video Studio

**Status:** Proposed; requires human review/approval before implementation.  
**Date:** 2026-11-15.  
**Owner/user:** Solo creator operating Codex PC on Windows.

## 1. Objective and success

Develop an AI-assisted production workflow for monetizable **Vietnamese narrated animated storytelling** on YouTube: original summaries and analyses of literary works or historically sourced events, illustrated in a consistent cinematic storybook **2.5D** visual style.

**North star:** 20–30 minute episodes; aspirational throughput **≥1 episode/day**, subject to quality. A working **60-second pilot** is the first proof, preceded by **three animated style demos**. A failure to hit daily throughput is not permission to ship defective media.

## 2. User and entry points

- Solo creator supplies a title/topic, optional EPUB/PDF/TXT/notes, may accept AI topic proposals.
- Source-first: user materials prioritized; external sources allowed and logged; do not invent claims/sources.
- Two content classes: **literature** (summary + meaningful original interpretation) and **history** (facts + sourced interpretation; reenactments must be disclosed).
- Vietnamese narration with a consistent channel voice, **exact voice TBD**; user supplies choice later.
- User reviews individual episodes or batches via Codex PC; no web dashboard.
- Upload is **manual**. Pipeline provides publication assets and rights report, never publishes.

## 3. Functional requirements (MUST)

| ID | Requirement | Observable acceptance |
| --- | --- | --- |
| FR-01 | Ingest topic or user-provided sources | Topic and source record persisted; unsupported/unreadable input reported, not silently ignored |
| FR-02 | Research and fact-check | Important claims map to source IDs, URLs/file references and checked status; unknowns surfaced |
| FR-03 | Draft original Vietnamese narrative + analysis | Script has sections, claim references, estimated duration; no long verbatim copyrighted excerpts |
| FR-04 | Script approval gate | Owner-triggered approval event bound to the exact script digest; an agent-authored file/state cannot grant approval; script edits invalidate script and downstream approval |
| FR-05 | Storyboard + scene plan | Plan duration from **measured authorized Vietnamese TTS** before final board sign-off; full 20–30 min has ~12–20 representative boards plus a complete shot plan; 60 s pilot may use fewer |
| FR-06 | Storyboard approval gate | Separate human approval bound to storyboard, approved script and voice timing digests; material scene/story/voice-timing changes invalidate it; purely technical rerenders need QA, not fresh board approval |
| FR-07 | 2.5D visuals | Multi-layer parallax, camera/light/weather, restrained character animation; per-beat intensity chosen by agent; no static-only slideshow as success |
| FR-08 | Asset generation and reuse | Existing rights-cleared assets prioritized; generate when needed under valid entitlement; provenance/rights recorded |
| FR-09 | Vietnamese narration | Replaceable commercial-use-permitted TTS adapter; provisional voice requires human consent; `VOICE_PENDING` blocks final board approval/pilot render; actual timings align scenes/subtitles |
| FR-10 | Music and SFX | Licensed samples or self-synthesized audio; no unknown-license music; ducking under narration |
| FR-11 | Scene render and resume | Each scene independently addressable, cache keyed by versioned inputs; interrupted jobs can resume; errors isolated |
| FR-12 | Preview/final | Preview **1280×720**; final **1920×1080, 24 fps**, rerender from source; MP4 H.264/AAC target, SRT, thumbnail, title, description, credits |
| FR-13 | Quality control | ffprobe duration/resolution/codec and frame/audio/subtitle/rights checks; classify defects, attempt bounded **corrective changes and rerenders** (not blind retry), then `NEEDS_REVIEW` |
| FR-14 | Copyright and publish gate | A rights report shows work/translation/source/media licenses, conflicts and human review needs; unresolved conflicts block publish-ready |
| FR-15 | Storage and cleanup | Raw/source/approvals protected; bounded cache retention; dry-run cleanup and recovery plan |
| FR-16 | Batch approval / queue | Multiple episodes can await approvals; only revision-matching approved episodes enter full render queue |
| FR-17 | No unapproved expense | No new subscription, usage-billed API call, purchase or other charge without explicit human approval; use existing free/entitled quota only within verified terms; exhaustion → pause + report |
| FR-18 | User manual publishing | Export YouTube-ready artifacts; no YouTube API/upload |
| FR-19 | AI engine evaluation | Same acceptance test on candidates; decide engine by actual 2.5D demo and resource evidence, not popularity |
| FR-20 | Agent control | Interactive in Codex PC for MVP, project-scoped installs allowed, system modifications require approval; no daemon prerequisite |

### Approval, voice and release gates

1. A script approval only counts when the owner explicitly confirms the **displayed script digest/revision** through a trusted interactive confirmation step; an agent may *request* approval but must not manufacture the approval event.
2. After script approval, obtain consent for a voice sample and measure real narration duration. Without an authorized voice, record `VOICE_PENDING` and allow preliminary board drafts only, **not final storyboard approval or pilot render**.
3. The board approval binds to the **approved script + storyboard + narration timing**. If changing voice alters timings, update the plan and reapprove affected boards; non-semantic rendering corrections do not automatically invalidate editorial approval.
4. Rights clearance and final media QA are separate checks; neither script nor board approval provides copyright clearance. A creator can manually upload only after the package passes the publication-readiness gate.
5. Plain JSON/JSONL alone is **not tamper-resistant**. Implementation must isolate/protect the owner-confirmation path from autonomous agent writes and test forged/stale approvals. Until such a path exists, the gate is a design requirement, not an enforced protection.

## 4. Non-functional requirements (MUST)

- **Quality above speed.** Defects in claims, visual continuity, sync, audio, rights or output integrity block completion.
- **Machine budget:** User-reported Windows PC, Ryzen 5 5500U, integrated AMD GPU, 16 GB RAM. **Exact Windows edition, available RAM, disk letters/free space and installed tools are unverified**; capture them during the host survey. Start with one renderer worker and 720p previews; select storage path from measured free space.
- **Performance:** report measured render seconds per video minute, peak RSS/RAM, temp/free disk and failures for all engine candidates. No asserted performance target without benchmark.
- **Reliability:** atomic writes where possible, deterministic per-scene inputs, idempotent reruns, no partial file marked ready, observable transitions/attempt limits.
- **Security:** sandbox inputs and dependencies, protect secrets, vet downloads, check rights, avoid unattended spend or destructive cleanup.
- **Consistency:** stable characters/background palette/typography; a versioned channel style bible and asset references used across scenes.
- **Evidence:** actual outputs with metadata and human checkpoint records, not success prose alone.

## 5. MVP scope and milestones

1. **SPEC/PLAN approval:** documentation and architecture decisions only.
2. **Engine/TTS/visual discovery spike:** install project-scoped dependencies; bench on Windows. Include Lemo-Opuscar as candidate, not presumed winner.
3. **Three 2.5D style demos:** distinct visual treatments with actual motion; user selects channel style.
4. **60-second public-domain literature pilot:** documented sources/translation rights; script approval → **authorized voice and measured timings** → board approval → scene render → preview → final master/QA.
5. **Resumability and retention:** prove rerender-one-scene; smoke resume; no accidental source deletion.
6. **Scaling experiments:** 2–3 min, 5 min chapter and eventually 20–30 min episode only after quality/performance evidence.

## 6. Out of scope (MVP)

- Producing a real 20–30 min episode within the first PR.
- Guaranteed one video per day; paid service provisioning; training custom generative models.
- Web dashboard, Windows service/scheduler, distributed cloud workers, auto-posting YouTube.
- Full body anime combat, full lip-sync of all speaking characters, generic game engine recreation.
- Copying entire copyrighted novels, infringing visual adaptation, bypassing website auth/paywalls.
- Public API or persistent database without a demonstrated requirement.

## 7. Project structure (planned)

```
AGENTS.md  README.md  docs/  tasks/
schemas/episode.schema.json
pipeline/{research,script,storyboard,voice,assets,render,verify,assemble}.py
tests/{unit,contract,integration}/
episodes/<slug>/{manifest.json,script.md,claims.json,storyboard.json,approvals/events.jsonl}
runtime/{cache,assets,renders,logs}/  # ignored, local
```

**Not implemented yet.** Language and runner interfaces are provisional, to be selected in engine spike. No framework/dependency pinned in SPEC.

## 8. Commands and conventions

At SPEC stage there is no executable build/test/render command. Later implementation PR must add reproducible **exact commands** and a `--help` contract for setup, one-scene render, full pilot, verification and cleanup; document OS/shell support. Prefer Python stdlib orchestration + JS rendering only if the spike proves that architecture.

Example *proposed* CLI contract (do **not** run as available): `python -m pipeline pilot --episode <id> --preview`, `python -m pipeline verify --episode <id>`. Contract will be finalized during implementation.

Use descriptive snake_case for Python, kebab-case for paths, UTC ISO timestamps, stable IDs, JSON schemas for external boundaries, explicit error states, source IDs rather than free-text citations.

## 9. Tests and quality gates

- Unit: schema, duration arithmetic, hash invalidation, state transitions, cache key, bounded retry, cleanup selection.
- Contract: renderer/TTS adapter input-output, rights records, ffprobe metadata parse, asset provenance.
- Integration: generate two small scenes, stop/resume, reject forged/stale approval event, change script or material voice timings invalidates affected approval, render only approved revision, deterministic partial rerender.
- Media: human review of sampled frames, transitions, audible narration and captions; full playback of pilot at final resolution.
- Rights/security: malformed uploads, path traversal, missing credentials, unknown license, unavailable free quota, invalid source URL → safe failure.
- All implementation work subject to [verification](verification.md) and the project Definition of Done.

## 10. Decisions pending

1. **Channel voice:** owner will provide/choose later. Pilot may use a clearly labeled temporary authorized TTS, but this cannot silently become final voice.
2. **Pilot work:** select a public-domain original and verify its particular Vietnamese translation separately; choose before scripting.
3. **Engine winner and versions:** benchmark candidate pipelines (Lemo-Opuscar, browser-canvas/Remotion, other justified lightweight 2.5D approach); must record observed render artifacts and licenses.
4. **Chosen visual style:** owner approves 1 of 3 demos.
5. **Image generation access:** user reports ChatGPT/Codex entitlement; confirm whether Codex PC actually exposes a suitable image-generation workflow, account quotas and commercial terms. ChatGPT entitlement alone does **not** prove programmatic Codex access; consider owner-provided exports if absent.
6. **Retention period:** propose cache TTL and size cap during implementation, human approval before destructive cleanup.
7. **Release rights/legal:** confirm jurisdiction, source legal status and music/voice commercial terms for each episode. Approval is not legal clearance.
8. **Engineering toolchain and host:** confirm Windows version, local disk/memory capacity, shell/runtime and dependency versions during spike.
9. **Approval proof:** choose a real owner-operated confirmation method whose records the autonomous agent cannot forge; document trust limits before writing the approval gate.

## 11. Human acceptance of SPEC

This PR is the review gate for SPEC/README/plan. **Merging docs is not approval of engine selection or a claim that tests passed.** Implementation starts only after the user expressly approves SPEC and tasks.
