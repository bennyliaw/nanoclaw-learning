# NanoClaw Learning Project — Handoff Notes

## Background
- Came from reading: https://thenewstack.io/nanoclaw-openclaw-agent-security/
- NanoClaw is a security-first, container-isolated agentic framework built as a lean replacement for OpenClaw (which collapsed under 800k+ lines of code and poor security practices)
- Key repo: https://nanoclaw.dev
- User profile: **Experienced Python developer, new to AI/Agentic**

## Why NanoClaw
- OpenClaw had credential leaks, bloated codebase, unvetted packages
- NanoClaw: Docker-isolated, credential-proxied (OneCLI), human-in-the-loop approvals, ~25 lines per agent
- Four core primitives: coding agent + persistent bash session + messaging connector + internet access

---

## Learning Roadmap

### Stage 1 — Personal/Dev Task Automation (START HERE)
Goal: get comfortable with NanoClaw's setup, Docker model, and scheduling

| # | Use Case | Skills Practised |
|---|----------|-----------------|
| 1 | Scheduled code runner (pull repo → run Python → notify via WhatsApp/Slack) | Scheduling, messaging connector |
| 2 | Dev environment watchdog (monitor logs/API, alert on anomalies) | Tool use, persistent session |
| 3 | File processing pipeline (drop file → transform → report back) | Python integration, sandboxing |

### Stage 2 — Learn Agentic Concepts Hands-On
Goal: understand state, tool use, and human-in-the-loop patterns

| # | Use Case | Concept Learned |
|---|----------|----------------|
| 1 | Multi-turn memory agent | State management across sessions |
| 2 | Tool-use patterns (search, file, API) | LLM tool reasoning |
| 3 | Human-in-the-loop approval flow | Security model, scoped permissions |

### Stage 3 — Build for Clients/Product
Goal: productise agentic workflows

| # | Use Case | Value |
|---|----------|-------|
| 1 | Per-customer agent instance (isolated, scoped to client data) | Multi-tenant architecture |
| 2 | Scheduled reporting agent (pull data → Claude summary → deliver) | Sellable as a service |
| 3 | Approval-gated workflow automation | Enterprise-ready pattern |

---

## Key Architecture Notes
- Always start with the security model, not the features
- Container isolation = load-bearing wall, not decoration
- Credentials never enter the agent environment directly (OneCLI proxy)
- Human-in-the-loop gates required for sensitive actions (email, calendar, etc.)
- NanoClaw runs from source, not binary — read the code, that's the point

## Tools / Integrations to Know
- **Messaging**: Vercel Chat SDK (covers ~15-20 apps)
- **Credential proxy**: OneCLI (Agent Vault — injects creds at request time, agents never hold raw keys)
- **Containers**: Docker (default), Docker Sandboxes micro-VM (extra isolation), Apple Container (Mac-only opt-in)
- **LLM (default)**: Anthropic Claude via official Claude Agent SDK
- **LLM (alternative)**: OpenCode provider path (`/add-opencode`) → OpenRouter, DeepSeek, Google, OpenAI; or `/add-ollama-provider` for local models. Provider is configurable PER agent group.

---

## Model & Billing Strategy (IMPORTANT)

### Phase 1 — Now through June 14, 2026: Claude Pro (shared pool)
- Before June 15, NanoClaw (Agent SDK) usage draws from the SAME pool as Claude.ai chat — i.e. your normal Pro 5h / 7d limits.
- Pro limits currently barely used → **front-load learning now, it's effectively free under existing subscription.**
- Authenticate via subscription, NOT an API key (an ANTHROPIC_API_KEY env var would force pay-as-you-go billing).
- Push hard on Stage 1 (esp. Google Photos audit — token-light) before the cutover.

### June 15, 2026 cutover
- Agent SDK / claude -p / third-party agents split into a SEPARATE monthly credit pool: Pro = $20/mo, billed at API rates, no rollover.
- Interactive Claude.ai chat + terminal Claude Code stay on normal subscription limits.
- Watch for Anthropic's claim email (~June 8); claim the credit once.
- Breaking change same day: model IDs `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire; SDK packages renamed. If NanoClaw pins these, expect a fix (Claude Code auto-diagnoses on install failure).

### Phase 2 — Post June 15: switch brain to DeepSeek (cloud)
- Plan: power NanoClaw + other experimental projects with DeepSeek to avoid the $20 SDK credit ceiling.
- Integration path: `/add-opencode` skill → sets `AGENT_PROVIDER=opencode`, routes via OpenCode config (NOT the Anthropic Agent SDK).
- Two routing options:
  - **Direct DeepSeek API**: DeepSeek console → create API key → OpenCode `/connect` DeepSeek → select model (e.g. DeepSeek V4 Pro). Cheapest, single provider.
  - **Via OpenRouter**: one `sk-or-...` key → access DeepSeek + fallback models, centralized budget caps, auto-failover if rate-limited. More flexible, small markup.
- DeepSeek is the current "bang-for-buck" reasoning leader — well-suited to multi-step agent loops.
- Provider is per-agent-group, so you can MIX: keep Claude for tasks needing top reasoning, DeepSeek for high-volume/experimental work.

### Recommended split by stage
| Stage | Phase 1 (now–Jun 14) | Phase 2 (post Jun 15) |
|-------|----------------------|------------------------|
| 1 — Personal/dev + Google cleanup | Claude Pro (shared pool) | DeepSeek via OpenCode |
| 2 — Agentic concepts | Claude Pro (shared pool) | DeepSeek; Claude for tricky reasoning |
| 3 — Client/product | (not yet) | DeepSeek default; evaluate dedicated API key / Max if scaling |

---

## Next Steps (in order)
1. Install NanoClaw from source (`git clone` + `bash nanoclaw.sh`), get Docker running
2. Verify it's authenticating via Pro subscription (no stray ANTHROPIC_API_KEY)
3. Connect one messaging app (WhatsApp or Slack)
4. Build Use Case 1.1: scheduled Python runner
5. Front-load Stage 1 before June 15 while usage rides Pro limits
6. Watch for credit-claim email (~June 8); claim it
7. Post June 15: run `/add-opencode`, wire up DeepSeek (direct or via OpenRouter), test on a low-stakes agent group first
8. Progress through Stage 1 fully before moving to Stage 2
