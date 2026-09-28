# CLAUDE.md — NanoClaw Learning Project

**Status: PAUSED (28 Sep 2026).** NanoClaw is one agent framework among several
(a more secure OpenClaw alternative), not a must-have, so it's parked until a project
or freelance engagement actually needs it. Don't resume the use cases below
unprompted.

## Two folders — don't confuse them

- **`~/dev/nanoclaw-learning/`** (this repo, `github.com/bennyliaw/nanoclaw-learning`,
  private) — learning notes only.
- **`github.com/bennyliaw/nanoclaw`** (public fork of `nanocoai/nanoclaw`, 28 Sep 2026) —
  the NanoClaw software. `main` tracks upstream; Ben's customisations (Telegram channel +
  photo patch, single-instance guard, `claude-usage` skill, Ollama benchmark notes) are on
  branch **`ben/local-2.0.72`**, based on 2.0.72.
- **`~/dev/nanoclaw/`** — the local working copy of that fork (renamed from
  `~/dev/nanoclaw-v2` on 28 Sep 2026; `origin` = the fork, `upstream` = nanocoai). It
  carries over the git-ignored state of the last install, which exists **only here**:
  `.env` (API keys, Telegram bot token), `groups/` (agent prompts, conversations, the
  Google One audit output), `data/` (NanoClaw DB, Telegram pairings), `logs/`.
- **The launchd service is disabled.** It was still running on 28 Sep, crash-looping
  every 15 min because Docker wasn't running. Its plist is parked at
  `~/dev/nanoclaw/data/launchd-disabled/com.nanoclaw-v2-63b11145.plist` and still points
  at the old `nanoclaw-v2` path; fix the paths before loading it again.

## On resuming — do these first

1. **Work in `~/dev/nanoclaw`** (already wired: `origin` = fork, `upstream` = nanocoai —
   the layout the `update-nanoclaw` skill expects). Start Docker first.
2. **Bring `ben/local-2.0.72` forward.** It is based on 2.0.72; upstream was 2.4.0,
   1,175 commits ahead (27 Sep). Start from fork `main`, then `/update-nanoclaw` or
   cherry-pick the branch commits.
3. **Upstream PR candidates**, both written by Ben (details in `patches/PATCH-NOTES.md`
   and commit `d73ec3f` on the branch):
   - Telegram inline-photo patch (`sendPhoto` for images instead of `sendDocument`).
   - Single-instance PID guard — a second host process was killing the first's containers.
4. **`groups/main/CLAUDE.local.md` is upstream's old v1 text**, renamed by v2's
   one-time migration (`src/claude-md-compose.ts`); it names tools v2 doesn't have.
   Rewrite or delete it before using the `main` group.

## Who I Am
- Experienced Python developer (strong fundamentals, comfortable with terminals, Docker, GitHub)
- New to AI and agentic patterns when this project started (June 2026) — learned them here by doing; now paused to focus on other tools
- Goal: progress through 3 stages of NanoClaw use cases (personal automation → agentic concepts → client/product)

## Project Goal
Build hands-on experience with NanoClaw as a security-first agentic framework.
Reference article: https://thenewstack.io/nanoclaw-openclaw-agent-security/
NanoClaw repo: https://nanoclaw.dev

---

## How to Help Me

### Always
- Assume strong Python knowledge — no need to explain basic syntax or patterns
- Explain AI/agentic concepts clearly where they're specific to NanoClaw — the basics are familiar by now
- Prefer working code over theory; I learn by building
- Flag security implications explicitly — this is central to why I chose NanoClaw over alternatives

### Never
- Don't skip the "why" on agentic patterns — the mental model matters
- Don't suggest workarounds that break container isolation or bypass credential proxying
- Don't overwhelm with options — ask a clarifying question if the path isn't clear

---

## Current Stage
**Stage 1 — Personal/Dev Task Automation**

### Stage 1 Use Cases (in order — status lives in the Progress Log below)
- 1.1 Scheduled code runner (repo pull → Python script → messaging notification)
- 1.2 Google One storage cleanup (audit → candidate review → delete/compress) ← ANCHOR
- 1.3 Dev environment watchdog (log/API monitor → anomaly alert)
- 1.4 File processing pipeline (drop file → transform → report)
- 1.5 Gmail/Drive storage cleanup (reuses 1.2 approval pattern)

### Google One Cleanup Target
- Current: >90% of 200GB (~180GB+)
- Target: ≤70% (≤140GB)
- Must free: ~40GB+
- Approach: audit first, human approves all deletions/compressions
- Key libs: Pillow, imagehash, ffmpeg, Google Photos/Gmail/Drive APIs

### Stage 2 (next)
- 2.1 Multi-turn memory agent
- 2.2 Tool-use patterns
- 2.3 Human-in-the-loop approval flow

### Stage 3 (later)
- 3.1 Per-customer isolated agent instance
- 3.2 Scheduled reporting agent
- 3.3 Approval-gated workflow automation

---

## Key Concepts to Reinforce as We Go
- Container isolation (Docker) — why it's non-negotiable for autonomous agents
- Credential proxying (OneCLI) — how tokens stay out of the agent environment
- Tool use — how LLMs decide which tools to call and when
- State/memory — how agents maintain context across sessions
- Human-in-the-loop — when to approve vs. automate

## Architecture Reminders
- NanoClaw runs from source — readable codebase is a feature, not a limitation
- Four primitives: coding agent + persistent bash + messaging + internet
- An agent can be written in ~25 lines
- Vercel Chat SDK handles messaging integrations
- Provider is per-agent-group — I can mix Claude and DeepSeek across different agents

---

## Model & Billing Strategy

Agent SDK usage has a separate $20/mo Pro credit (API rates, no rollover) since 15 Jun
2026. The plan on resuming was to run the brain on DeepSeek (cloud) to stay off that
ceiling. Whether that switch was made before the project paused is unconfirmed —
check the provider before assuming one.
- Path: `/add-opencode` → AGENT_PROVIDER=opencode → DeepSeek (direct API or via OpenRouter).
- DeepSeek note: strong cheap reasoning, but watch tool-call/reasoning_content quirks on multi-step loops (esp. via OpenRouter).

---

## Progress Log
_Update this as use cases are completed_

| Stage | Use Case | Status | Notes |
|-------|----------|--------|-------|
| 1 | 1.1 Scheduled runner | ✅ Complete | Typhoon Jangmi monitor — JMA + Open-Meteo APIs, map gen, 10-min cron, danger alerts. Node.js in container. |
| 1 | 1.2 Google One cleanup — Phase A (audit) | ✅ Complete | Gmail + Drive audit (Photos API blocked Mar 2025). Nano-orchestrated audit.py via OneCLI proxy. Storage: 214.8GB/214.7GB (100%). Gmail top offenders = newsletters ~8-9MB each. Drive = 596MB videos. Photos+Gmail = 214.2GB. |
| 1 | 1.2 Google One cleanup — Phase B+C (approve+execute) | 🔲 Not started | |
| 1 | 1.3 Watchdog | 🔲 Not started | |
| 1 | 1.4 File pipeline | 🔲 Not started | |
| 1 | 1.5 Gmail/Drive cleanup | 🔲 Not started | Reuses 1.2 pattern |
| 2 | 2.1 Memory agent | 🔲 Not started | |
| 2 | 2.2 Tool-use | 🔲 Not started | |
| 2 | 2.3 HITL approvals | 🔲 Not started | |
| 3 | 3.1 Per-customer | 🔲 Not started | |
| 3 | 3.2 Reporting agent | 🔲 Not started | |
| 3 | 3.3 Approval-gated | 🔲 Not started | |
