# AI_Agent_Orchestrator

A Windows-hosted multi-agent orchestration system: Claude manages, Antigravity CLI codes, Muse4AI generates video, a Publisher Agent posts that video to YouTube/TikTok/Instagram, a Python agent automates, a QA agent checks output — coordinated through an MCP Server and a web dashboard.

## Status

| Artifact | Status |
| -------- | ------ |
| `Requirement.md` (REQ-001) | Draft — pending human review via `/review` |
| `Architecture.md` | Not yet created (this README + code stand in for it until drafted) |
| Backend (`backend/`) | Implemented and tested in this build — 37/37 pytest passing |
| MCP Server (`mcp_server/`) | Implemented — all 14 tools (11 original + publish_video/get_publish_status + review_task) verified end-to-end against a running backend |
| Dashboard (`frontend/`) | Implemented — all 7 pages verified in a real browser (Playwright), builds cleanly |
| Antigravity adapter (`agents/antigravity/`) | Code written, **not verified against a real `agy` CLI** — see AS-001. Implements a REVIEW gate (FR-037/FR-038): a successful run is never auto-COMPLETED, it waits for `review_task` (approve/reject with feedback) or a Dashboard click — verified with 7 tests (mocked CLI). |
| Muse4AI adapter (`agents/muse/`) | Rewritten against Muse4AI's real, public API contract ([github.com/andrew-babo/muse4ai](https://github.com/andrew-babo/muse4ai)) and verified against a mock server replaying it — **not yet run against a live Muse4AI instance** (needs the user's Windows PC + a signed-in Muse account). See AS-002. |
| Publisher Agent (`agents/publisher/`) | YouTube/TikTok/Instagram adapters written against each platform's real, public API docs and verified against mocked HTTP (19 tests) — **none run against a live account/app**; Instagram also has a real unsolved gap (needs a public `video_url`, not a local file). See AS-005–AS-007. |
| Windows scripts (`scripts/*.ps1`) | Written, **not executed** — no Windows/PowerShell available in this build environment |

This was built in a Linux cloud container with no access to the target Windows
machine, Antigravity CLI, or a Muse4AI account. Everything above marked
"verified" was actually run and checked in this container; everything marked
"not verified" is implemented to the documented interface but needs a real
run on the target machine to confirm.

### Known gaps to close before this is production-ready

* `execute_workflow` runs all steps concurrently (bounded by `MAX_CONCURRENT_TASKS`); `TaskCreate` has no dependency field yet, so a workflow with strictly ordered, dependent steps isn't modeled — needs a schema addition once `Architecture.md` is drafted.
* `MAX_CONCURRENT_TASKS` / `MAX_TASK_TIMEOUT_SECONDS` / `MAX_FIX_RETRIES` defaults (`config/.env.example`) are Claude's proposed values (AS-004) — not specified in the original request.
* Dashboard auth is a single shared password (`DASHBOARD_PASSWORD`), appropriate for one operator, not multiple accounts.
* Instagram publishing needs an already-public `video_url`; this project does not host a locally generated video anywhere public (see FR-036, R-007).
* A TikTok app is forced to `SELF_ONLY` (private) posts, and a Google Cloud project to private/unlisted uploads, until each passes that platform's own review/audit — a platform rule, not a bug here.

## Directory Structure

| Path | Purpose |
| ---- | ------- |
| `backend/` | FastAPI Orchestrator: Task/Agent/Workflow Manager, SQLite, logging, reports |
| `frontend/` | React web dashboard (7 pages) |
| `mcp_server/` | MCP tools exposed to Claude Desktop |
| `agents/antigravity/` | Adapter to the Antigravity CLI (coding agent) |
| `agents/muse/` | Adapter to [Muse4AI](https://github.com/andrew-babo/muse4ai) (local app that automates the user's own Meta Muse session; video agent) |
| `agents/python/` | Python automation agent |
| `agents/qa/` | QA agent |
| `agents/publisher/` | Adapters to YouTube Data API v3, TikTok Content Posting API, and the Instagram Graph API (posts a generated video) |
| `workflows/` | Stored workflow (task graph) definitions |
| `projects/` | Per-task authorized working directories for Antigravity |
| `output/videos`, `output/code`, `output/reports` | Generated artifacts (not committed — see `.gitignore`) |
| `database/` | SQLite database file (not committed) |
| `logs/` | Runtime logs (not committed) |
| `config/` | Non-secret configuration |
| `scripts/` | Windows install/start/stop/restart/health-check/backup scripts |
| `backup/` | Configuration backups (not committed) |

Each code/doc directory has its own `README.md` pointing to the Functional Requirement IDs it implements, in `Requirement.md`.

## Running it locally (any OS, for development/testing)

```bash
cp config/.env.example config/.env
# edit config/.env: set DASHBOARD_PASSWORD and DASHBOARD_JWT_SECRET

cd backend && python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests/ -v          # 37 tests, should all pass
PYTHONPATH=.. .venv/bin/python -m pytest ../agents/muse/ ../agents/publisher/ -v   # 19 more adapter contract tests
uvicorn main:app --host 127.0.0.1 --port 8000 &

cd ../mcp_server && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py                      # run manually, or let Claude Desktop launch it (Phase 7)

cd ../frontend && npm install
npm run dev                         # http://127.0.0.1:5173
```

On Windows, `scripts/install.ps1` and `scripts/start.ps1` automate the backend/frontend half of this (not `mcp_server`, which Claude Desktop launches itself) — see `scripts/README.md`.

## Where to Start

* **How to use the running system**: `Huong_Dan_Su_Dung.md` (Vietnamese).
* Full requirements: `Requirement.md` (REQ-001).
* Instructions to hand to Antigravity for implementation: `Antigravity_Build_Guide.md`.

This production deployment target on the user's machine is `D:\AI_AGENT_SYSTEM` (or a confirmed alternate drive) — see `Requirement.md` Constraints. The source of truth for the code lives in this repository folder and is deployed/installed there.
