# AI_Agent_Orchestrator

A Windows-hosted multi-agent orchestration system: Claude manages, Antigravity CLI codes, Muse4AI generates video, a Python agent automates, a QA agent checks output — coordinated through an MCP Server and a web dashboard.

## Status

| Artifact | Status |
| -------- | ------ |
| `Requirement.md` (REQ-001) | Draft — pending human review via `/review` |
| `Architecture.md` | Not yet created |
| Implementation | Not started |

## Directory Structure

| Path | Purpose |
| ---- | ------- |
| `backend/` | FastAPI Orchestrator: Task/Agent/Workflow Manager, SQLite, logging, reports |
| `frontend/` | React web dashboard (7 pages) |
| `mcp_server/` | MCP tools exposed to Claude Desktop |
| `agents/antigravity/` | Adapter to the Antigravity CLI (coding agent) |
| `agents/muse/` | Adapter to Muse4AI / Meta Muse (video agent) |
| `agents/python/` | Python automation agent |
| `agents/qa/` | QA agent |
| `workflows/` | Stored workflow (task graph) definitions |
| `projects/` | Per-task authorized working directories for Antigravity |
| `output/videos`, `output/code`, `output/reports` | Generated artifacts (not committed — see `.gitignore`) |
| `database/` | SQLite database file (not committed) |
| `logs/` | Runtime logs (not committed) |
| `config/` | Non-secret configuration |
| `scripts/` | Windows install/start/stop/restart/health-check/backup scripts |
| `backup/` | Configuration backups (not committed) |

Each code/doc directory has its own `README.md` pointing to the Functional Requirement IDs it implements, in `Requirement.md`.

## Where to Start

* Full requirements: `Requirement.md` (REQ-001).
* Instructions to hand to Antigravity for implementation: `Antigravity_Build_Guide.md`.

This production deployment target on the user's machine is `D:\AI_AGENT_SYSTEM` (or a confirmed alternate drive) — see `Requirement.md` Constraints. The source of truth for the code lives in this repository folder and is deployed/installed there.
