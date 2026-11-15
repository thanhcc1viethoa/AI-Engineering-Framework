# Requirement

> Requirements specification for the AI_Agent_Orchestrator project.
> Instantiated from the frozen `03_Templates/Requirement.md` (v1.1.1).
> This document is the single source of truth for the project's requirements and shall be approved before architecture or implementation.

---

# Document Information

| Field          | Value                                  |
| -------------- | -------------------------------------- |
| Project Name   | AI_Agent_Orchestrator                  |
| Requirement ID | REQ-001                                |
| Version        | 0.1.0                                  |
| Status         | Draft                                  |
| Author         |                                        |
| Owner          |                                        |
| Reviewer       |                                        |
| Created Date   | 2026-11-15                             |
| Last Updated   | 2026-11-15                             |

---

# Purpose

Provide a Windows-hosted multi-agent orchestration system in which Claude acts as the managing agent, dispatching work to specialized executor agents (a coding agent via Google Antigravity CLI, a video-generation agent via Muse4AI/Meta Muse, a Python automation agent, and a QA agent) and reporting consolidated results back to the user through Claude Desktop and a web dashboard.

* Why the project exists: let the user issue one high-level request and have it decomposed, executed by the right specialized agent, quality-checked, and reported on automatically, instead of operating each tool manually.
* Expected outcomes: a running Orchestrator (backend + MCP server + dashboard) on the user's Windows machine that can accept a request from Claude Desktop or the dashboard, execute it through one or more agents, and return a verified result.
* Business value: reduces manual coordination between separate AI/automation tools (coding, video generation, scripting, QA) into a single managed workflow.
* Success criteria: the 12 criteria defined in **Acceptance Criteria** below are all met.

---

# Background

The user currently has separate tools (Claude Desktop, an Antigravity coding agent/IDE, a Muse4AI/Meta Muse video account, ad-hoc Python scripts) with no central coordination layer, task history, or automated quality check between them.

* Existing problems: no shared task queue or history across tools; no automatic hand-off between a coding task and a QA check; no single dashboard to see what every agent is doing.
* Current workflow: the user or Claude invokes each tool manually and manually tracks progress and results.
* Existing limitations: no persistence of task/agent state, no background service, no autostart with Windows, no web visibility into agent activity.
* Motivation: the user supplied a complete design ("MASTER PROMPT – TRIỂN KHAI HỆ THỐNG AI AGENT ORCHESTRATOR TRÊN WINDOWS") specifying the target architecture, phased delivery plan, and acceptance criteria for this system; this document formalizes that request as a governed Requirement per the repository's `/create` workflow.

---

# Scope

## In Scope

* A Python + FastAPI backend ("AI Orchestrator") providing: Task Manager, Task Queue (SQLite-backed), Agent Manager, Workflow Manager, SQLite database, logging, and report generation.
* An MCP Server exposing exactly the tools listed in **FR-006** to Claude Desktop.
* Integration with the Google Antigravity CLI as the coding/execution agent, invoked only through its documented CLI or non-interactive interface.
* Integration with Muse4AI / Meta Muse as the video-generation agent, via its officially documented API/MCP.
* A Python Automation Agent that executes automation tasks dispatched by the Orchestrator.
* A QA Agent that checks the output of completed tasks/workflows.
* A React web dashboard (7 pages, see **FR-012**–**FR-018**) communicating with the backend over REST API and WebSocket.
* SQLite-backed persistence of tasks, agents, and history.
* Windows background operation: install/start/stop/restart/health-check/backup PowerShell scripts, and autostart with Windows after testing passes.
* Security controls: no hardcoded secrets, path validation before write/delete, confirmation gates on destructive or out-of-scope actions, no unsolicited internet exposure.
* A phased delivery plan (10 phases) with verification between phases, starting with a Windows environment survey.

## Out of Scope

* Any Antigravity control path other than its documented CLI or officially supported non-interactive interface (no undocumented/reverse-engineered API control).
* Any Muse4AI/Meta Muse behavior (video limits, duration, resolution, rate limits) not confirmed from the user's actual account and official documentation.
* Exposing the Orchestrator API or dashboard to the public internet.
* Installing software that duplicates an already-installed, working component.
* Modifying or deleting any existing MCP Server configuration without explicit user confirmation.
* Any component of this repository's own governance tooling (`02_Policies/`, `04_Prompts/`, `06_Tools/`) — those remain owned by the repository, not by this project.

---

# Requirement Classification

This project's requirements span:

* Business Requirements
* Functional Requirements
* Non-Functional Requirements
* Technical Requirements
* Operational Requirements
* AI Requirements

No Compliance Requirements were specified in the source request.

---

# Requirement Lifecycle

* Draft
* Proposed
* Approved
* Implemented
* Verified
* Deprecated

---

# Priority Model

* Critical
* High
* Medium
* Low
* Optional

---

# Stakeholders

| Role          | Name | Responsibility |
| ------------- | ---- | --------------- |
| Sponsor       |      | Owns the request and final acceptance |
| Product Owner |      | Confirms scope and acceptance criteria |
| Architect     |      | Defines Architecture.md and ADRs for this project |
| Developer     |      | Implements each phase |
| Reviewer      |      | Reviews each produced artifact against the Quality Gate |
| End User      |      | Operates the system on the target Windows machine |

---

# Functional Requirements

| ID     | Requirement | Category | Priority | Owner | Source | Status |
| ------ | ----------- | -------- | -------- | ----- | ------ | ------ |
| FR-001 | Survey the target Windows machine (OS version, CPU, RAM, disk incl. target drive free space, Python/pip, Node.js/npm, Antigravity IDE, Antigravity CLI, Claude Desktop, Muse4AI, existing MCP Server configs, potentially conflicting running processes) via PowerShell before any installation, and produce a written environment report. | Technical | Critical | | User Request | Draft |
| FR-002 | Create the install directory structure (backend, frontend, mcp_server, agents/{antigravity,muse,python,qa}, workflows, projects, output/{videos,code,reports}, database, logs, config, scripts, backup) under the install root. | Technical | Critical | | User Request | Draft |
| FR-003 | Implement a Task Manager module persisting tasks with fields Task ID, Task Name, Description, Assigned Agent, Priority, Status, Created At, Started At, Completed At, Result, Error Message, Output Path, and status values PENDING, QUEUED, RUNNING, WAITING, COMPLETED, FAILED, CANCELLED. | Functional | Critical | | User Request | Draft |
| FR-004 | Implement an Agent Manager module registering Claude Manager, Antigravity Agent, Muse Agent, Python Agent, and QA Agent, each with ID, Name, Type, Status, Capabilities, Current Task, Last Active, Error Log. | Functional | Critical | | User Request | Draft |
| FR-005 | Implement a Workflow Manager that decomposes one incoming request into an ordered set of tasks, assigns each task to the appropriate agent, and supports sequential execution plus parallel execution for independent tasks. | Functional | Critical | | User Request | Draft |
| FR-006 | Implement an MCP Server exposing exactly these tools to Claude Desktop, each with a documented description, parameters, types, and return schema, implementing only functionality that is actually built: `submit_task`, `get_task_status`, `get_task_result`, `list_tasks`, `cancel_task`, `get_agent_status`, `list_agents`, `execute_workflow`, `create_video`, `get_video_status`, `get_system_status`. | Technical | Critical | | User Request | Draft |
| FR-007 | Integrate the Antigravity CLI as the coding/execution agent: verify installation and login, verify current CLI syntax/parameters, use its non-interactive mode if supported, dispatch tasks from Python, receive structured results, log execution, track duration, handle timeouts and errors, and allow a controlled re-run of a failed task. Each task is scoped to an authorized project directory; Antigravity's full permission-bypass mode shall not be used. | Technical | High | | User Request | Draft |
| FR-008 | Integrate Muse4AI/Meta Muse as the video agent via its officially documented API/MCP: verify connection and status, submit a video-generation request, receive a job ID, poll status, download the completed video into `output/videos` when the API supports it, and log errors and duration. Duplicate concurrent video-generation submissions for the same request shall be prevented. | Technical | High | | User Request | Draft |
| FR-009 | Implement a Python Automation Agent that executes automation tasks dispatched by the Orchestrator and returns a structured result. | Functional | Medium | | User Request | Draft |
| FR-010 | Implement a QA Agent that inspects the output of a completed task or workflow step and returns a pass/fail quality verdict before Claude finalizes its report. | Functional | High | | User Request | Draft |
| FR-011 | Connect Claude Desktop to the Orchestrator exclusively through the MCP Server tools defined in FR-006. | Technical | Critical | | User Request | Draft |
| FR-012 | Web Dashboard — Overview page: total agents, active agents, running tasks, completed tasks, failed tasks, videos created. | Functional | High | | User Request | Draft |
| FR-013 | Web Dashboard — Agent Monitor page: real-time status per agent. | Functional | High | | User Request | Draft |
| FR-014 | Web Dashboard — Task Manager page: create task, view tasks, search, filter by status, view result, stop a task, view history. | Functional | High | | User Request | Draft |
| FR-015 | Web Dashboard — Workflow page: diagram of a workflow's steps and the relationships between agents. | Functional | Medium | | User Request | Draft |
| FR-016 | Web Dashboard — Video Manager page: video name, creation time, status, file path, duration, and the originating generation request info. | Functional | Medium | | User Request | Draft |
| FR-017 | Web Dashboard — System Logs page: live system log and error monitoring. | Functional | Medium | | User Request | Draft |
| FR-018 | Web Dashboard — Settings page: API configuration, agent configuration, working directories, resource limits. | Functional | Medium | | User Request | Draft |
| FR-019 | Dashboard-to-backend communication shall use REST API for requests and WebSocket for real-time updates. | Technical | High | | User Request | Draft |
| FR-020 | Orchestration loop: for each request, Claude shall analyze the goal, decompose it into tasks, select agents, submit tasks via MCP, track progress, retrieve results, evaluate results, request fixes from the responsible agent within a bounded retry limit, and produce a final report. Completion shall never be declared without verifying the actual task result. | Functional | Critical | | User Request | Draft |
| FR-021 | Enforce bounded limits on fix-retry count, task execution time, and concurrent task count. Exact numeric values are not specified in the source request and shall be defined in Architecture.md (see AS-004). | Non-Functional | High | | User Request | Draft |
| FR-022 | Provide PowerShell scripts `install.ps1`, `start.ps1`, `stop.ps1`, `restart.ps1`, `health_check.ps1`, `backup_config.ps1` (named `backup_config.ps1`, not `backup.ps1`, per Naming_Policy.md — see Notes), starting services in the correct dependency order. | Technical | High | | User Request | Draft |
| FR-023 | Configure the Orchestrator services to autostart with Windows, enabled only after testing passes. | Technical | High | | User Request | Draft |
| FR-024 | Detect a hung/stuck process and perform a controlled, safe automatic restart. | Non-Functional | Medium | | User Request | Draft |
| FR-025 | Require authentication before the web dashboard can be used. | Non-Functional | Critical | | User Request | Draft |
| FR-026 | Store all API keys/secrets via environment variables or a secrets store; never hardcode them in source code and never write them to logs. | Non-Functional | Critical | | User Request | Draft |
| FR-027 | Restrict filesystem access to authorized project/output directories; block arbitrary command execution; validate every path before a write or delete. | Non-Functional | Critical | | User Request | Draft |
| FR-028 | Back up existing configuration before any configuration change. | Non-Functional | High | | User Request | Draft |
| FR-029 | The Orchestrator API/dashboard shall not be exposed beyond localhost unless separately requested and approved by the user. | Non-Functional | Critical | | User Request | Draft |
| FR-030 | Destructive operations, software installation, system configuration changes, or any action outside the authorized scope require explicit user confirmation before execution. | Non-Functional | Critical | | User Request | Draft |
| FR-031 | Implementation shall proceed only through the 10 defined phases (environment survey; directory/Python/Node setup; backend+DB; MCP server; Antigravity integration; Muse4AI integration; Claude Desktop integration; web dashboard; full system test; background/autostart), with each phase's results checked, files inventoried, tests run, and defects fixed before the next phase begins. | Operational | Critical | | User Request | Draft |
| FR-032 | Existing installed software and existing MCP Server configurations shall be detected and reused; they shall not be deleted or overwritten without explicit user confirmation. | Operational | Critical | | User Request | Draft |

Rules:

* One requirement per row.
* Atomic.
* Testable.
* Unambiguous.

---

# Non-Functional Requirements

| ID      | Requirement | Target |
| ------- | ----------- | ------ |
| NFR-001 | Platform support | Windows 10/11 only |
| NFR-002 | State durability | Task/agent state persists in SQLite across service restarts |
| NFR-003 | Operability for a non-specialist user | Every manual step is written in Vietnamese with exact PowerShell commands or exact UI click locations; the user is never asked to guess a path |
| NFR-004 | Observability | Every agent action, task state transition, and error is logged with a timestamp |
| NFR-005 | Resource economy | No component is installed that duplicates an already-installed, working component; free/open-source software is preferred |
| NFR-006 | Localization | The dashboard UI is in Vietnamese |
| NFR-007 | Least privilege | Each Antigravity task is scoped to a single authorized project directory, not the whole filesystem |

---

# Requirement Rationale

| ID     | Business Value | Reason | Expected Impact |
| ------ | --------------- | ------ | ---------------- |
| FR-001 | Prevents wasted work | Installing before knowing the machine's real state risks conflicting with existing tools or exceeding available resources | Avoids rework and accidental damage to existing setup |
| FR-006 | Enables Claude Desktop control | Claude Desktop can only reach the Orchestrator through MCP tools | Without it, no orchestration from Claude Desktop is possible |
| FR-020 | Ensures trustworthy reporting | The user requires that completion never be claimed without verification | Prevents false "done" reports |
| FR-025–FR-030 | Protects the user's machine and credentials | The system runs with real filesystem and API access on the user's own PC | Reduces risk of credential leakage, data loss, or unauthorized system change |
| FR-031 | Manages a large build safely | The source request explicitly forbids building everything before testing | Each phase is verified before risk compounds into the next |

---

# Requirement Dependencies

| ID     | Depends On | Blocks | Related Requirements |
| ------ | ---------- | ------ | --------------------- |
| FR-002 | FR-001 | FR-003–FR-032 | — |
| FR-003 | FR-002 | FR-005, FR-006 | FR-004 |
| FR-004 | FR-002 | FR-005, FR-006 | FR-003 |
| FR-005 | FR-003, FR-004 | FR-006, FR-020 | — |
| FR-006 | FR-003, FR-004, FR-005 | FR-011, FR-020 | — |
| FR-007 | FR-001, FR-002 | FR-005, FR-020 | — |
| FR-008 | FR-001, FR-002 | FR-005, FR-020 | — |
| FR-011 | FR-006 | FR-020 | — |
| FR-012–FR-018 | FR-003, FR-004, FR-019 | — | — |
| FR-019 | FR-003, FR-004 | FR-012–FR-018 | — |
| FR-020 | FR-005, FR-006, FR-007, FR-008, FR-009, FR-010 | — | FR-021 |
| FR-022, FR-023 | FR-003–FR-019 (system functional) | — | FR-024 |
| FR-031 | — | All | Governs delivery order of all FRs |

---

# Requirement Validation

| ID     | Validation Method | Verified |
| ------ | ------------------ | -------- |
| FR-001 | Inspection of the environment report produced from the survey script output | No |
| FR-006 | Test — call each of the 11 MCP tools from Claude Desktop and confirm documented behavior | No |
| FR-007 | Demonstration — dispatch one real coding task to Antigravity and confirm a structured result is returned | No |
| FR-008 | Demonstration — generate one real test video via Muse4AI and confirm the job completes | No |
| FR-020 | Demonstration — submit one multi-step request end-to-end and confirm Claude's final report matches verified task results | No |
| FR-022, FR-023 | Test — stop and restart all services, then reboot the machine, and confirm autostart | No |
| All others | Review / Test per Architecture-defined test plan | No |

---

# Business Rules

* No API key, token, or credential shall appear in source code, configuration committed to version control, or log output.
* Any action that deletes data, installs software, changes system configuration, or reaches outside the authorized project/output directories requires explicit user confirmation before execution.
* An existing, working installed component or MCP configuration shall be reused, never silently replaced.
* Antigravity shall never be run in a mode that disables its own permission checks.
* The Orchestrator shall not declare a task or workflow complete without verifying its actual result.

---

# Assumptions

| ID     | Assumption | Validation Status | Validation Method | Validation Date | Reviewer |
| ------ | ---------- | ------------------ | ------------------ | ----------------- | -------- |
| AS-001 | The Google Antigravity CLI (`agy`) exists on the target machine, is licensed/logged in, and supports a non-interactive/headless execution mode suitable for programmatic dispatch. | Unvalidated | Inspection (Phase 1 survey) + Demonstration (Phase 5) | | |
| AS-002 | Muse4AI exposes an officially documented API/MCP with account-specific quotas (video count, duration, resolution, rate limits) sufficient for this project's needs. | Unvalidated | Inspection of the user's account + official documentation (Phase 6) | | |
| AS-003 | The target Windows machine's actual specifications (OS build, CPU, RAM, free disk space on the install drive, installed Python/Node versions, existing MCP Server configurations, running services) are unknown to this session. This Claude Code session runs in an isolated cloud container with no filesystem or network access to the user's Windows machine, and no Remote Control connection to it is currently established. | Unvalidated | User executes the Phase 1 PowerShell survey script locally and returns its output | | |
| AS-004 | Numeric bounds for maximum fix-retry count, maximum task execution time, and maximum concurrent tasks (FR-021) are not specified in the source request. | Unvalidated | To be defined in Architecture.md and confirmed with the user | | |

---

# Constraints

* Technology: Python + FastAPI backend, SQLite database/queue, React frontend, REST + WebSocket transport, MCP protocol. No substitution without explicit instruction.
* Install root: `D:\AI_AGENT_SYSTEM`. If drive `D:` does not exist or lacks sufficient free space, Phase 1 shall propose an alternate location for user confirmation before any directory is created.
* Execution access: implementing and testing on the physical Windows machine requires either (a) a live Remote Control connection from this session to that machine, or (b) the user executing provided PowerShell scripts locally and returning the output.
* No deletion or overwrite of an existing MCP Server configuration without explicit user confirmation.
* No installation of software that duplicates an already-installed, working component.
* Platform: Windows 10/11 only.

---

# Dependencies

| Dependency | Type | Notes |
| ---------- | ---- | ----- |
| Google Antigravity CLI (`agy`) | External tool | Availability/capabilities unverified — see AS-001 |
| Muse4AI / Meta Muse account and API/MCP | External service | Availability/quotas unverified — see AS-002 |
| Claude Desktop | External application | Runs on the user's Windows machine |
| Python + pip | Runtime prerequisite | Presence/version confirmed in Phase 1 |
| Node.js + npm | Runtime prerequisite | Presence/version confirmed in Phase 1 |
| SQLite | Embedded database | Bundled with the backend |
| FastAPI | Backend framework | — |
| React | Frontend framework | — |

---

# Risks

| ID    | Risk | Likelihood | Impact | Mitigation |
| ----- | ---- | ---------- | ------ | ---------- |
| R-001 | Antigravity CLI may not support a non-interactive mode suitable for programmatic control | Medium | High | Verify in Phase 5 before building the integration; fall back to the documented interactive workflow if unsupported |
| R-002 | Muse4AI quotas or costs are lower than needed for repeated testing | Medium | Medium | Confirm quota before automated test loops; prevent duplicate submissions (FR-008) |
| R-003 | The target machine lacks sufficient disk/RAM once surveyed | Low | High | Phase 1 survey gates every later phase |
| R-004 | No live Remote Control connection slows iteration to a manual copy/paste loop | High | Medium | Provide complete, copy-paste-ready PowerShell scripts per phase (NFR-003) |
| R-005 | Project scope (10 phases, 5 agent types, full dashboard) risks partial or unverified delivery | Medium | High | Enforce FR-031 phase gating with verification before proceeding |

---

# Acceptance Criteria

| ID     | Acceptance Criterion | Validation Method |
| ------ | --------------------- | ------------------ |
| AC-001 | Claude Desktop connects to the MCP Orchestrator. | Demonstration |
| AC-002 | The Web Dashboard is operational. | Demonstration |
| AC-003 | Claude can assign a task to Antigravity. | Demonstration |
| AC-004 | Antigravity completes one trial coding task. | Test |
| AC-005 | Muse4AI connects to the Meta Muse account. | Demonstration |
| AC-006 | At least one trial video is generated. | Test |
| AC-007 | The Python Agent completes one automation task. | Test |
| AC-008 | The QA Agent checks an output. | Test |
| AC-009 | Claude receives results and produces a report. | Review |
| AC-010 | The Task Manager persists history. | Inspection |
| AC-011 | Services can be stopped and restarted. | Test |
| AC-012 | The system does not lose existing configuration or data. | Inspection |

---

# Success Metrics

No success metrics beyond the Acceptance Criteria above were specified in the source request. All 12 Acceptance Criteria (AC-001–AC-012) passing is the defined measure of project success.

---

# AI Context

| Field               | Value |
| ------------------- | ----- |
| Relevant Documents  | `CLAUDE.md`, `01_Rules/Global.md`, `02_Policies/Repository_Governance.md`, `02_Policies/Naming_Policy.md`, `02_Policies/Versioning_Policy.md`, `04_Prompts/Create_Prompt.md`, the user's "MASTER PROMPT – TRIỂN KHAI HỆ THỐNG AI AGENT ORCHESTRATOR TRÊN WINDOWS" (held in conversation history, not yet a repository file) |
| Prompt Dependencies | `04_Prompts/Create_Prompt.md` v1.1.0 |
| Repository Rules    | `01_Rules/Global.md` v2.0.1 |
| Known Constraints   | See **Constraints** section; notably: this Claude Code session runs in an isolated cloud container with no current Remote Control connection to the user's Windows machine |
| Expected Outputs    | `Architecture.md`, one or more `ADR/ADR-####-*.md`, phased implementation code under this project directory |
| Context Priority    | Explicit human instructions > `02_Policies/Repository_Governance.md` > `02_Policies/*` > this Requirement > `01_Rules/Global.md` > `04_Prompts/` / `03_Templates/` |

---

# Traceability

| Artifact     | Reference |
| ------------ | --------- |
| ADR          | None yet |
| Architecture | None yet — to be created after this Requirement is approved |
| Review       | None yet |
| Issue        | None |
| Commit       | This file's introducing commit |

## Requirement Traceability Matrix (RTM)

| Requirement ID | Parent Requirement | Architecture | ADR | Review | Test | Issue | Commit |
| -------------- | ------------------- | ------------- | --- | ------ | ---- | ----- | ------ |
| FR-001 to FR-032 | — | | | | | | |

---

# Change Log

| Version | Date | Author | Summary |
| ------- | ---- | ------ | ------- |
| 0.1.0 | 2026-11-15 | | Initial draft from the user's master prompt |

---

# Requirement Change Control

| CR ID  | Requirement ID | Description | Reason | Impact Analysis | Approval | Version |
| ------ | --------------- | ------------ | ------ | ----------------- | -------- | ------- |

---

# Approval

| Role     | Name | Date | Approval Date | Status |
| -------- | ---- | ---- | -------------- | ------ |
| Author   |      |      |                | Pending |
| Reviewer |      |      |                | Pending |
| Approver |      |      |                | Pending |

---

# Notes

* This Requirement captures the user's master prompt as given, without adding scope it did not specify. Numeric limits (retry counts, timeouts, concurrency) and third-party tool capabilities (Antigravity CLI, Muse4AI) are flagged under **Assumptions** rather than guessed.
* The master prompt named one script `backup.ps1` (FR-022); the implementation uses `backup_config.ps1` instead, because `backup` alone is a reserved name under `02_Policies/Naming_Policy.md` "Reserved Names", which takes precedence over the source request per this repository's authority order.
* Per `01_Rules/Global.md` ("AI assists; it does not own"), this document requires human review and approval before `Architecture.md` is created for this project.

---

# Version History

| Version | Date       | Author | Notes |
| ------- | ---------- | ------ | ----- |
| 0.1.0   | 2026-11-15 |        | Initial draft requirement for AI_Agent_Orchestrator, derived from the user's master prompt |
