# Assumptions, decisions and open issues

## Confirmed interview outcomes (grouped; 34 questions)

- **Goal:** original Vietnamese narrative summaries **with analysis**, covering literature/novels and genuine historical events; monetizable YouTube, user manually uploads.
- **Content input:** user documents and public research both permitted; AI may propose topics; important claims grounded in recorded sources.
- **Format:** single channel style = cinematic illustrated **2.5D**; motion intensity adapts to story; three animated demos before choosing the specific look; assets reused or generated with valid rights.
- **Production:** **20–30 min** target, optimistic ≥1/day, but **quality takes priority**; preview 720p, final 1080p/24fps.
- **Operator:** Codex **PC on Windows**, no dashboard; script and storyboard approvals, individually or in batch; storyboard overview 12–20 frames for long-form episodes; no auto-publish.
- **Audio:** Vietnamese AI TTS, specific voice deferred; licensed library + procedural music/SFX.
- **Costs:** near-zero variable cost, free/local/available entitlement; no automatic spending; machine may run 24/7 but MVP does not require autonomous daemon after Codex closes.
- **Retention:** short-lived raw/render/cache data with safe cleanup; provenance, approvals and protected source preserved.
- **Pilot:** public-domain literary work, 3 concept demos first, then 60 s video.
- **Autonomy:** Codex may install project-scope dependencies, ask before system changes; engine decided after comparison; auto-fix scenes, bounded retry then human review.

## Explicit assumptions pending review

- [ ] First pilot topic/title is **not yet named**. This is an input needed for the pilot, not a blocker for the spec.
- [ ] "Public domain" must be verified for the actual **original and specific translation** in relevant jurisdictions. No title chosen by assumption.
- [ ] Channel voice is still open. A temporary licensed voice may be used only if its provenance is clear and owner agrees before publication.
- [ ] User says Codex/ChatGPT can generate images; exact local tooling, quotas and commercial rights **unverified**.
- [ ] Retention TTL, disk limit and deletion rules require explicit approval before any destructive tool.
- [ ] No app/web service; manifest-based coordination is a proposal, not an existing system.
- [ ] Target target cadence is best-effort; throughput cannot be guaranteed on 16 GiB/iGPU without benchmark.
- [ ] Proposed language/CLI structure may change after engine trials. Avoid freezing framework versions prematurely.

## Architecture decision record ADR-0001 (proposed)

- **Title:** Repo-owned, scene-isolated, engine-neutral video production with Codex PC
- **Status:** Proposed; awaiting SPEC/plan approval
- **Date:** 2026-11-15
- **Context:** Long-form illustrated storytelling at near-zero cost, on one Windows workstation, with human approvals.
- **Decision:** Keep story/scene/rights state in repo-owned versioned manifests. Render each scene via a swappable adapter selected after real tests; preserve scene cache and independent QA. User runs Codex PC; no daemon/dashboard in MVP.
- **Alternatives considered:** fork Lemo-Opuscar immediately; one monolithic 30-min browser render; Godot/MCP as mandatory; microservices/dashboard/paid cloud workers.
- **Consequences:** Easier testability and reruns, avoids premature vendor coupling, but needs a small coordinator and careful cache/approval semantics.
- **Evidence required:** Three demos on actual machine, same-source engine comparison, 60-second pilot and human style choice.

## Decision log follow-ups

| Decision | Status | Owner / gate |
| --- | --- | --- |
| SPEC v1 & implementation plan | Proposed | Human reviews this PR |
| Final 2.5D style | Open | Human selects after 3 demos |
| Engine + dependency versions | Open | Agent benchmarks; human approves |
| Vietnamese channel voice | Open | Human sends/selects later |
| Pilot literary work and translation | Open | Agent proposes clearance evidence; human confirms |
| Cleanup retention TTL | Open | Agent proposes; human approves |
| Publishing rights for each episode | Per-episode gate | Human reviews unresolved risks; no automatic upload |
