# Codex PC operating workflow (proposed)

## Important: current reality

This repository is **documentation only**. It has no project CLI or running renderer yet. These are the **expected operator steps after implementation**; don't claim they're currently executable.

## Setup / environment gate

- **User-reported** Windows PC, Ryzen 5 5500U, 16 GB RAM, integrated AMD GPU. Verify actual Windows version, free RAM, disk locations and free space on this machine before choosing workspace; do not assume a `D:` drive exists. Do not kill user apps or install system software without permission.
- Verify installed Node, Python/uv, FFmpeg, Git, and Codex image-generation entitlement **from the actual host**. Record versions in report.
- Install only into the project workspace/isolated environment, pin versions/lockfiles. Ask before registry, PATH/system settings, firewall or global software changes.
- Engine candidates must run an identical short benchmark; document measured peak memory and disk.
- Place large runtime artifacts on a **measured** local drive with sufficient capacity; keep large media outside Git tracking.

## Typical creator session

1. Ask Codex to propose topics or supply a title and materials. Record sources and legal status.
2. Codex writes a sourced outline/script; output for human review. The owner explicitly approves **this exact script revision** through a protected confirmation path, or requests changes. Codex cannot write its own approval proof.
3. Select an authorized Vietnamese TTS sample with owner consent and **measure actual line durations**. If voice unavailable, keep `VOICE_PENDING`; a preliminary board can be drafted, but final storyboard approval and pilot render remain blocked.
4. Codex creates a full scene inventory and **12–20 representative boards for a 20–30 min episode** (fewer for a 60-second pilot). The owner approves board revision tied to the script **and voice timing** (single or batch, per-episode hash).
5. Codex may then select licensed/procedural/generated assets and produce scenes. Rendering remains supervised by Codex PC during MVP; no guaranteed background continuation after it closes.
6. Review 720p preview and QA report. Diagnose/correct defective scene(s) within bounded attempts; after QA, generate fresh 1080p/24 fps final master.
7. Export `episode.mp4`, `episode.srt`, `thumbnail.png`, `youtube-metadata.md`, `CREDITS.md`, `rights-report.md`, `qa-report.md` only when rights and media checks pass.
8. User watches/checks and manually uploads. No YouTube integration.

## Run state / recovery

- A stopped Codex session may leave ongoing child processes interrupted. On restart, inspect manifest, verify cached files and resume only missing/invalid steps.
- Limit correction/rerender passes (proposal: at most 2 per scene, then `NEEDS_REVIEW`; final value chosen in implementation). Log **which defect was found and what changed**; do not rerun identical inputs endlessly or lower quality to finish.
- Before deletion present a dry-run list. The owner must approve retention duration and irreversible cleanup policy.
- Preserve approved texts, storyboards, reference assets, rights evidence and finished deliverables. Dedupe and archive metadata when pruning cache.

## Example Codex briefing (not a command)

> Read AGENTS.md and docs/spec.md. Work only on the currently approved task in tasks/todo.md. Do not infer that the renderer exists. First show the environment survey, candidate tool licenses, and plan to produce three short 2.5D proofs using the same source material. Do not start full production without explicit script and storyboard approvals; do not spend money. Record tests and deliver real evidence.

## Human approval and private-source boundary

The user must take an explicit action to confirm a displayed revision/hash. A generated chat answer, an agent-edited manifest and a manually typed `APPROVED` flag are not sufficient by themselves. The eventual implementation must choose an owner-controlled confirmation path and test stale/forged records; **none exists yet in this spec-only repo**. Do not start full production until it does.

By default, locally uploaded manuscripts/notes remain local; ask permission before sending their contents to ChatGPT, a cloud TTS/image service or any other external provider. Capture provider name and what will be shared; do not paste private documents into logs or PRs.

## Operational failures

| Symptom | Action |
| --- | --- |
| Free quota exhausted | Pause, retain cache and suggest lawful free fallback |
| Missing TTS/voice selection | Keep `VOICE_PENDING`, request owner's choice before publication master; temporary voice needs explicit labelling |
| License status unknown | `BLOCKED_RIGHTS` — do not mark ready |
| OOM/disk shortage | Stop, log, clean only safe temp, reduce workers (not output quality) |
| Scene sync defect | Rerender affected scene, compare voice timings and SRT |
| Final video invalid | Preserve source/master, fail QA; no publication-ready artifact |

## Status reporting

After each checkpoint Codex reports: accomplished artifacts, file paths, time/cost/RAM observations, tests run, issues and next approval. Distinguish evidence from forecasts.
