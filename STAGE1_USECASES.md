# Stage 1 — Expanded Use Cases

## Context
- Python developer, new to agentic AI
- NanoClaw: Docker-isolated, human-in-the-loop, scheduled agents
- Stage 1 goal: real personal/dev value, low risk, build intuition

---

## Use Case 1.1 — Scheduled Code Runner *(original)*
**Problem:** Run Python scripts on a schedule and get notified without babysitting a terminal.

**What the agent does:**
- Pulls latest code from a GitHub repo on a schedule
- Runs the target Python script inside the Docker container
- Sends output summary (pass/fail + key lines) to WhatsApp or Slack

**Why start here:** Simplest possible agent loop. No sensitive data, no approvals needed. Gets you comfortable with NanoClaw scheduling + messaging connector fast.

**Python angle:** Your existing scripts slot straight in — no rewriting needed.

---

## Use Case 1.2 — Google One Storage Cleanup Agent *(anchor use case)*
**Problem:** Google One at >90% of 200GB. Mostly phone photo/video auto-backup. Target: reach 70% (≤140GB), freeing ~40GB+.

### What the agent does (in phases):

#### Phase A — Audit & Report (no deletions yet)
- Connects to Google Photos API
- Scans entire library and produces a report:
  - Total count and size breakdown (photos vs videos)
  - Duplicate candidates (same timestamp, same hash, or near-identical filenames)
  - Blurry / low-quality photos (using Python `Pillow` — Laplacian variance score)
  - Videos over a size/resolution threshold (e.g. >100MB or >1080p)
  - Screenshots (easily identified, often disposable)
  - Burst photos (sequences taken within 1-2 seconds of each other)
- Delivers structured report to you via messaging

#### Phase B — Candidate Review (human-in-the-loop)
- Agent presents batches of candidates with thumbnails or metadata
- You respond: keep / delete / compress
- Agent logs your decisions, never acts without your explicit approval
- This is NanoClaw's approval-gate pattern in practice

#### Phase C — Execution
- Deletes approved items via Google Photos API
- For approved videos: downloads locally into container, compresses with `ffmpeg` (e.g. H.265, target 720p for older recordings), re-uploads, flags original for deletion
- Re-runs audit after execution to confirm new storage level

### Target outcome:
| Category | Estimated saving |
|----------|-----------------|
| Exact duplicates | 5–15GB |
| Burst / near-duplicate photos | 3–8GB |
| Blurry / failed shots | 2–5GB |
| Compressed videos | 10–20GB |
| Screenshots | 1–3GB |
| **Total estimate** | **~20–50GB** |

### Tools / libraries:
- `google-auth`, `google-api-python-client` — Google Photos API
- `Pillow` — image quality scoring
- `imagehash` — perceptual duplicate detection
- `ffmpeg` (via subprocess in container) — video compression
- NanoClaw messaging — approval loop delivery

### Why this is a great Stage 1 use case:
- Real problem, real urgency
- Human-in-the-loop approval is built into NanoClaw — you're learning the pattern on something you care about
- Python-heavy implementation plays to your strengths
- The audit phase alone has immediate value before any agent automation

---

## Use Case 1.3 — Dev Environment Watchdog *(original, refined)*
**Problem:** Scripts, APIs, or services you run locally fail silently.

**What the agent does:**
- Polls a target on a schedule (log file, local API endpoint, or a health-check URL)
- Detects anomalies: error keywords, missing heartbeat, response time spike
- Sends alert with relevant log excerpt to messaging
- Optional: attempts a predefined fix (restart a service, clear a cache) and reports outcome

**Python angle:** Dead simple with `watchdog`, `requests`, and `subprocess`. Swap in any monitoring target.

---

## Use Case 1.4 — File Processing Pipeline *(original, refined)*
**Problem:** Repetitive file transformations (CSV cleaning, PDF extraction, renaming) that you currently do manually.

**What the agent does:**
- Watches an input folder (local or Google Drive)
- On new file: runs your Python transformation script inside the container
- Outputs to a results folder and notifies you with a summary

**Python angle:** Your transformation logic is already Python — the agent is just the trigger + delivery layer.

---

## Use Case 1.5 — Gmail / Google Drive Storage Cleanup Agent
**Problem:** Google One bloat isn't only photos — large email attachments and forgotten Drive files contribute too.

**What the agent does:**
- Scans Gmail for emails with large attachments (>5MB), old newsletters, or unread emails older than 1 year
- Scans Google Drive for large files not opened in 6+ months, duplicate filenames, and orphaned files
- Produces a report grouped by size impact
- Presents candidates for your approval before any deletion
- Complements 1.2 to push storage well below the 70% target

**Tools:** `gmail API`, `google-drive-api`, standard Python

**Why it pairs well with 1.2:** Once you've built the approval loop in 1.2, this reuses the exact same pattern on a different data source.

---

## Suggested Order for Stage 1

| Order | Use Case | Why |
|-------|----------|-----|
| 1st | **1.1 Scheduled runner** | Simplest setup, no sensitive data, proves the NanoClaw loop works |
| 2nd | **1.2 Google One cleanup — Phase A (audit only)** | Real value immediately, no risk, learn Google API auth |
| 3rd | **1.2 Phase B+C** | First real human-in-the-loop agent, uses approval gates |
| 4th | **1.3 Watchdog** | Adds scheduling depth, different tool pattern |
| 5th | **1.5 Gmail/Drive cleanup** | Reuses 1.2 patterns, finishes the storage problem |
| 6th | **1.4 File pipeline** | Rounds out Stage 1, sets up Stage 2 tool-use patterns |

---

## Key Stage 1 Principles to Internalise
- **Audit before act** — always produce a report first, never touch data on first run
- **Approval gates are not optional** — especially on personal data
- **Container isolation** — all ffmpeg, file ops, and API calls happen inside Docker, not on your machine
- **Credentials via OneCLI** — Google API tokens never enter the agent prompt directly

---

## Model Strategy for Stage 1
- **Now–June 14:** Run on Claude Pro (shared subscription pool, barely used). Front-load these use cases now.
- **Post June 15:** Switch to DeepSeek via `/add-opencode` to avoid the $20 Agent SDK credit ceiling.
- The Google Photos audit (1.2 Phase A) is token-light — cheap on any model. The vision/quality-scoring work runs locally in Python (Pillow/imagehash), NOT through the LLM, so model choice barely affects it.
- Heavier reasoning (e.g. deciding *which* near-duplicates to keep) is where model quality shows — fine on DeepSeek, but flag if results feel off and consider routing just that step to Claude.
