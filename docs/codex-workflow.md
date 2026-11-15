# Codex PC operating workflow (proposed)

## Important: current reality

This repository is **documentation only**. It has no project CLI or running renderer yet. These are the **expected operator steps after implementation**; don't claim they're currently executable.

## Setup / environment gate

- Windows 11 machine: Ryzen 5 5500U, 16 GB RAM, integrated graphics, enough disk on D:; close unneeded apps before benchmark. Do not kill user apps or install system software without permission.
- Verify installed Node, Python/uv, FFmpeg, Git, and Codex image-generation entitlement **from the actual host**. Record versions in report.
- Install only into the project workspace/isolated environment, pin versions/lockfiles. Ask before registry, PATH/system settings, firewall or global software changes.
- Engine candidates must run an identical short benchmark; document measured peak memory and disk.
- Keep project runtime artifacts on D: if available; avoid tracked Git folder for large media.

## Typical creator session

1. Ask Codex to propose topics or supply a title and materials. Record sources and legal status.
2. Codex writes a sourced outline/script; output for human review. Explicit **approve this exact script revision** or request changes.
3. Codex creates a full scene inventory and **12–20 representative boards for a 20–30 min episode** (fewer for a 60-second pilot). Approve board revision (single or batch, per-episode hash).
4. Codex may then select licensed/procedural/generated assets and produce scenes. Rendering remains supervised by Codex PC during MVP; no guaranteed background continuation after it closes.
5. Review 720p preview and QA report. Re-render any scene with defects; after QA, generate fresh 1080p/24 fps final master.
6. Export `episode.mp4`, `episode.srt`, `thumbnail.png`, `youtube-metadata.md`, `CREDITS.md`, `rights-report.md`, `qa-report.md`.
7. User watches/checks and manually uploads. No YouTube integration.

## Run state / recovery

- A stopped Codex session may leave ongoing child processes interrupted. On restart, inspect manifest, verify cached files and resume only missing/invalid steps.
- Limit retries (proposal: max 2 automatic correction passes per scene, then `NEEDS_REVIEW`; final value chosen in implementation). Never loop forever or lower quality to finish.
- Before deletion present a dry-run list. The owner must approve retention duration and irreversible cleanup policy.
- Preserve approved texts, storyboards, reference assets, rights evidence and finished deliverables. Dedupe and archive metadata when pruning cache.

## Example Codex briefing (not a command)

> Read AGENTS.md and docs/spec.md. Work only on the currently approved task in tasks/todo.md. Do not infer that the renderer exists. First show the environment survey, candidate tool licenses, and plan to produce three short 2.5D proofs using the same source material. Do not start full production without explicit script and storyboard approvals; do not spend money. Record tests and deliver real evidence.

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
