# CLAUDE.md — NanoClaw Learning Project

## Who I Am
- Experienced Python developer (strong fundamentals, comfortable with terminals, Docker, GitHub)
- New to AI and Agentic patterns — learning by doing
- Goal: progress through 3 stages of NanoClaw use cases (personal automation → agentic concepts → client/product)

## Project Goal
Build hands-on experience with NanoClaw as a security-first agentic framework.
Reference article: https://thenewstack.io/nanoclaw-openclaw-agent-security/
NanoClaw repo: https://nanoclaw.dev

---

## How to Help Me

### Always
- Assume strong Python knowledge — no need to explain basic syntax or patterns
- Explain AI/Agentic concepts clearly — I'm new here, don't assume familiarity
- Prefer working code over theory; I learn by building
- Flag security implications explicitly — this is central to why I chose NanoClaw over alternatives

### Never
- Don't skip the "why" on agentic patterns — the mental model matters
- Don't suggest workarounds that break container isolation or bypass credential proxying
- Don't overwhelm with options — ask a clarifying question if the path isn't clear

---

## Current Stage
**Stage 1 — Personal/Dev Task Automation**

### Stage 1 Use Cases (in order)
- [ ] 1.1 Scheduled code runner (repo pull → Python script → messaging notification)
- [ ] 1.2 Google One storage cleanup (audit → candidate review → delete/compress) ← ANCHOR
- [ ] 1.3 Dev environment watchdog (log/API monitor → anomaly alert)
- [ ] 1.4 File processing pipeline (drop file → transform → report)
- [ ] 1.5 Gmail/Drive storage cleanup (reuses 1.2 approval pattern)

### Google One Cleanup Target
- Current: >90% of 200GB (~180GB+)
- Target: ≤70% (≤140GB)
- Must free: ~40GB+
- Approach: audit first, human approves all deletions/compressions
- Key libs: Pillow, imagehash, ffmpeg, Google Photos/Gmail/Drive APIs

### Stage 2 (next)
- [ ] 2.1 Multi-turn memory agent
- [ ] 2.2 Tool-use patterns
- [ ] 2.3 Human-in-the-loop approval flow

### Stage 3 (later)
- [ ] 3.1 Per-customer isolated agent instance
- [ ] 3.2 Scheduled reporting agent
- [ ] 3.3 Approval-gated workflow automation

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

**Phase 1 (now–June 14, 2026): Claude Pro.**
- Agent SDK usage currently shares my Pro pool (5h/7d limits), which I've barely used.
- Front-loading learning now while it's effectively covered by my subscription.
- Must NOT have ANTHROPIC_API_KEY set (would force pay-as-you-go billing instead of subscription).

**June 15, 2026 cutover:**
- Agent SDK splits to a separate $20/mo Pro credit (API rates, no rollover).
- Claim credit via email (~June 8).
- Watch for retired model IDs (claude-sonnet-4-20250514, claude-opus-4-20250514) + renamed SDK packages.

**Phase 2 (post June 15): switch brain to DeepSeek (cloud).**
- Powering NanoClaw + other experiments with DeepSeek to avoid the $20 ceiling.
- Path: `/add-opencode` → AGENT_PROVIDER=opencode → DeepSeek (direct API or via OpenRouter).
- When helping me post-cutover, assume DeepSeek is the default model unless I say otherwise.
- DeepSeek note: strong cheap reasoning, but watch tool-call/reasoning_content quirks on multi-step loops (esp. via OpenRouter).

---

## Progress Log
_Update this as use cases are completed_

| Stage | Use Case | Status | Notes |
|-------|----------|--------|-------|
| 1 | 1.1 Scheduled runner | ✅ Complete | Typhoon Jangmi monitor — JMA + Open-Meteo APIs, map gen, 10-min cron, danger alerts. Node.js in container. |
| 1 | 1.2 Google One cleanup — Phase A (audit) | 🔧 In progress | Step 0 done. Photos API blocked (Mar 2025 restriction). Pivot: Gmail + Drive audit instead. See docs/plans/1.2-phase-a-google-one-audit.md v2. Storage confirmed at 205GB/200GB (over quota). |
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
