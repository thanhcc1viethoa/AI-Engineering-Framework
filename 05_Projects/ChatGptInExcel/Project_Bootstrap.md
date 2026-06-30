# Project Bootstrap

> Project Bootstrap plan for **ChatGptInExcel**, the first production project built on the AI Engineering Framework.
> This is a planning artifact (living document). It contains **no application code**.
> It realizes Repository Roadmap milestone **M6 — First project instance established** and Phase **P6 — Projects**.
> It preserves the approved, frozen framework foundation (`v1.0-foundation`, ADR-0001) and does not modify any frozen artifact.

---

# Document Information

| Field          | Value                                  |
| -------------- | -------------------------------------- |
| Project Name   | ChatGptInExcel                         |
| Document ID    | BOOT-001                               |
| Version        | 0.1.0                                  |
| Status         | Draft                                  |
| Author         |                                        |
| Owner          | User                                   |
| Created Date   | 2026-06-30                             |
| Last Updated   | 2026-06-30                             |
| Requirement Ref| REQ-001 (v0.3.0, Draft)                |
| Architecture Ref| ARC-001 (v0.5.0, Draft)               |

---

# 1. Reusable Framework Components

The frozen foundation (`v1.0-foundation`) is the reuse surface. Every project artifact below is **instantiated from**, not copied or modified.

| Framework Component | Path | Baseline | Reuse in This Project |
| ------------------- | ---- | -------- | --------------------- |
| Global Engineering Rules | `01_Rules/Global.md` | 2.0.1 | Inherited baseline; Definition of Done, security, change-scope rules apply directly |
| Repository Governance | `02_Policies/Repository_Governance.md` | 1.1.0 | Roles, authority hierarchy, approval process, ADR integration |
| Versioning Policy | `02_Policies/Versioning_Policy.md` | 1.1.0 | Artifact versions, lifecycle states (Draft→Approved→Released) |
| Naming Policy | `02_Policies/Naming_Policy.md` | 1.0.0 | Directory and artifact naming |
| Requirement Template | `03_Templates/Requirement.md` | 1.1.1 | Already instantiated → `Requirement.md` (REQ-001) |
| Architecture Template | `03_Templates/Architecture.md` | 1.1.0 | Already instantiated → `Architecture.md` (ARC-001) |
| ADR Template | `03_Templates/ADR.md` | 1.1.0 | Used for `ADR/ADR-000x-*.md` |
| Review Form / Report | `03_Templates/Review_Form.md`, `Review_Report.md` | 1.0.1 / 1.1.0 | Used for technical/architecture reviews |
| Artifact Revision Request | `03_Templates/Artifact_Revision_Request.md` | 1.2.0 | Required for any change to a frozen artifact |
| Create / Review / Revision Prompts | `04_Prompts/*.md` | 1.1.0 / 1.2.0 / 1.2.0 | Drive artifact creation, review, and revision |

**Conclusion:** the project has full template and process coverage. No framework gap blocks the project. All blockers below are *project-level* artifact gaps.

---

# 2. Recommended Project Structure under `05_Projects/`

The current layout mixes governance docs at the project root with an `addin/` shell that has committed `node_modules/` and log files (a Global Rules violation). The recommended canonical structure for a framework project:

```text
05_Projects/<ProjectName>/
  README.md                  Project overview and status
  Requirement.md             REQ-xxx  (single source of truth)
  Architecture.md            ARC-xxx
  Project_Bootstrap.md       This planning document
  Project_Rules.md           (optional) local rules; may only add/strengthen, never relax
  .gitignore                 Excludes node_modules, logs, build output, secrets
  ADR/                       ADR-000x-*.md  (immutable decision records)
  reviews/                   Review Reports (technical, architecture, security)
  docs/                      Setup, operations, MCP client configuration
  src/                        Application code (created later, not now)
  tests/                      Test suites and fixtures
  tools/                      Project-local scripts/automation
  addin/                      Optional Excel task-pane helper (node_modules gitignored)
```

For the **current MCP-server architecture (ARC-001 v0.5.0)**, `src/` and `tests/` are expected to be Python:

```text
src/chatgpt_excel_mcp/
  __init__.py
  server.py        MCP server + tool registration
  excel_bridge.py  pywin32 / COM workbook access
  tools/           one handler per MCP tool contract
  safety.py        confirm-before-write enforcement
tests/             unit + acceptance tests (AC-001..AC-006)
pyproject.toml     pinned deps + lockfile (Global Rules: pin + lockfile)
```

> Note: `src/`, `tests/`, and scaffolding are **listed for structure only** and are **not created in this bootstrap** (objective 7 — no application code yet).

---

# 3. First Production-Ready Project Definition

**ChatGptInExcel** — a personal, local Windows bridge that lets ChatGPT (or any MCP-compatible client) read from and write to open Excel desktop workbooks through a local MCP server, with explicit confirmation before any mutation.

- **Integration boundary:** local MCP server (AD-004 / ARC-001).
- **Workbook access:** Excel desktop COM automation via `pywin32` (AD-005).
- **Safety model:** confirm-before-write; preview on `confirm=false`, mutate only on `confirm=true` (AD-006).
- **MCP tool surface (6 tools):** `list_workbooks`, `list_worksheets`, `get_active_workbook`, `get_selected_range`, `read_range` (read-only); `write_range` (mutating, confirmation-gated).
- **Out of scope (MVP):** other Office hosts, AppSource/enterprise rollout, direct ChatGPT account login in the add-in, browser automation, cloud/Graph access, model training.

**"Production-ready" for this personal project = Definition of Done (Global Rules) satisfied:**
acceptance criteria AC-001..AC-006 demonstrated/tested; tests present and passing; docs current; no secrets/committed artifacts; Requirement and Architecture **Approved**; human sign-off; clean traceable git history.

---

# 4. Missing Artifacts Required Before Coding

These are the **blockers** that must close before application code begins. Ordered by severity.

| ID | Gap | Severity | Detail / Evidence |
| -- | --- | -------- | ----------------- |
| G-001 | **Requirement not approved** | Critical | `Requirement.md` REQ-001 is **Draft** (v0.3.0). Governance requires requirements approved before architecture/implementation. |
| G-002 | **Architecture not approved** | Critical | `Architecture.md` ARC-001 is **Draft** (v0.5.0), pending REQ-001. |
| G-003 | **ADR layer is out of sync with the architecture** | Critical | `ADR/ADR-0001..0005` all describe the **superseded** design (BFF proxy, Office.js, SSE, service-wide OpenAI key, Entra ID) and are marked *Accepted*. Architecture v0.5.0 marks AD-001/002/003 *Superseded* and points AD-004/AD-005 at the **new** decisions (MCP boundary, COM automation) — but the ADR **files do not contain those new decisions**. New ADRs are needed: (a) local MCP server as integration boundary, (b) Excel COM automation for workbook access, (c) confirm-before-write. Old ADRs must be formally superseded (immutable — supersede, do not edit). |
| G-004 | **Referenced ADR-0006 does not exist** | High | `Architecture.md` AD-006 cites "ADR-0006" for confirm-before-write; no `ADR-0006-*.md` file exists. |
| G-005 | **Stale technical review** | High | `Technical_Review_Report.md` (TR-001, "Approved") reviewed the *old* ADR-0004/0005 (key + Entra ID). The new MCP/COM architecture has had **no technical review**. |
| G-006 | **Committed build artifacts / no project `.gitignore`** | High | `addin/node_modules/` and `addin/server.log`, `server.err.log` are committed — violates Global Rules (no build artifacts/generated output). Entire `ChatGptInExcel/` is currently untracked. |
| G-007 | **No dependency manifest / lockfile for the MCP server** | Medium | New architecture is Python (`pywin32`, MCP SDK) but there is no `pyproject.toml`/`requirements.txt` + lockfile. Global Rules require pinned deps + committed lockfile. |
| G-008 | **No test plan / test artifacts** | Medium | AC-001..AC-006 have no corresponding test artifacts; Definition of Done requires tests. |
| G-009 | **Empty RTM and approvals** | Medium | Requirement RTM and approval tables are unpopulated; traceability not yet established. |
| G-010 | **README status drift** | Low | `README.md` status table says "ADR-0001..0003 Accepted" and predates the MCP pivot; needs to reflect ARC-001 v0.5.0 and the ADR reconciliation. |
| G-011 | **Open architecture issues unresolved** | Low | AI-001 (which MCP client surface the user's ChatGPT supports) and AI-002 (COM bridge vs installed Excel) are still Open and gate real usage. |

---

# 5. Implementation Roadmap & Milestone Plan

Governance-first: artifacts are approved in dependency order (Requirement → Architecture/ADR → review) **before** any code. Milestones PM-3 onward are planned only; this bootstrap stops at PM-0.

| Milestone | Goal | Key Deliverables | Exit Criteria | Closes |
| --------- | ---- | ---------------- | ------------- | ------ |
| **PM-0 Bootstrap** | Align project with governance | This document; gap list; repo hygiene plan | Bootstrap reviewed; gaps agreed | — |
| **PM-1 Requirement Approval** | Lock the requirement baseline | REQ-001 Draft→Approved; RTM populated | Requirement Approved & traceable | G-001, G-009 |
| **PM-2 Architecture & Decisions** | Make the architecture authoritative | New ADRs (MCP boundary, COM, confirm-before-write); supersede old ADRs; ADR-0006 authored; ARC-001 Approved; fresh technical review | Architecture Approved; ADRs consistent; review PASS | G-002, G-003, G-004, G-005 |
| **PM-3 Repo Hygiene & Scaffolding** | Production-ready skeleton (config only, no logic) | `.gitignore`; `pyproject.toml` + lockfile; MCP server skeleton; test harness; CI | Clean tree; deps pinned; empty test suite runs | G-006, G-007 |
| **PM-4 Read Tools (MVP core)** | Bounded read access | `list_workbooks`, `list_worksheets`, `get_active_workbook`, `get_selected_range`, `read_range` | AC-002, AC-003 demonstrated | FR-001..FR-004 |
| **PM-5 Write Path** | Safe mutation | `write_range` with preview + `confirm` gate | AC-004, AC-005 | FR-005, NFR-003 |
| **PM-6 Reliability & Diagnostics** | Graceful failure + local logging | Error contracts; metadata-only logging | AC-006 | FR-006, NFR-004 |
| **PM-7 Test & Acceptance** | Verify against criteria | Unit + acceptance tests for AC-001..AC-006 | All AC pass; DoD met | G-008 |
| **PM-8 Docs & Release** | Personal v1.0 | MCP client setup docs; resolve AI-001/AI-002; README refresh | Released per Versioning Policy | G-010, G-011 |

---

# 6. Risk Assessment

| ID | Risk | Likelihood | Impact | Mitigation |
| -- | ---- | ---------- | ------ | ---------- |
| PR-001 | Coding starts on **Draft/unsynced** artifacts (G-001..G-005), producing untraceable work | High | High | Enforce governance gate: no code before PM-1/PM-2 approvals |
| PR-002 | ADR drift misleads implementers about the real design | High | High | Reconcile ADRs in PM-2 before any scaffolding |
| PR-003 | Sensitive workbook data returned to ChatGPT (AR-001/R-001) | Medium | High | Read only explicit ranges; never log cell contents |
| PR-004 | Incorrect/destructive write (AR-002/R-002) | Medium | High | Preview + explicit confirm; no destructive tools in MVP |
| PR-005 | Windows/Excel COM coupling limits portability (AR-003/R-003) | High | Medium | Scope MVP to personal Windows desktop; isolate COM in `excel_bridge` |
| PR-006 | MCP client support varies by ChatGPT surface (AR-004/R-004, AI-001) | Medium | High | Resolve AI-001 early; keep server MCP-spec-compatible; document setup |
| PR-007 | Committed `node_modules`/logs leak into history and bloat repo (G-006) | High | Medium | Add `.gitignore`, untrack artifacts before first commit |
| PR-008 | Secrets handling regresses to old key-based design | Low | High | New architecture stores no provider secret; keep it that way |

---

# 7. Recommended Next Steps (Implementation Sequence)

1. **Approve this bootstrap** (PM-0) and confirm ChatGptInExcel as the first production project.
2. **PM-1 — Approve REQ-001:** review and move the requirement Draft→Approved; populate the RTM. *(Requirement is the single source of truth; nothing downstream approves before it.)*
3. **PM-2 — Reconcile decisions & approve architecture:** author new ADRs for the MCP boundary, COM automation, and confirm-before-write (and the missing ADR-0006); formally supersede ADR-0001..0003 (and re-target/retire 0004/0005); run a fresh technical review of the MCP/COM architecture; then move ARC-001 Draft→Approved.
4. **PM-3 — Repo hygiene first:** add `.gitignore`, untrack `node_modules/` and logs, add pinned `pyproject.toml` + lockfile, and a runnable (empty) test harness — **still no application logic**.
5. **PM-4 → PM-7 — Build in safety order:** read-only tools → confirmed write path → reliability/diagnostics → acceptance tests against AC-001..AC-006.
6. **PM-8 — Document & release:** resolve AI-001/AI-002, write MCP client setup docs, refresh README, release personal v1.0.

> Governance gate: **steps 4+ (any code) must not begin until PM-1 and PM-2 approvals are recorded.** This bootstrap produces no application code (objective 7).

---

# Traceability

| Artifact | Reference |
| -------- | --------- |
| Requirement | `Requirement.md` (REQ-001, v0.3.0, Draft) |
| Architecture | `Architecture.md` (ARC-001, v0.5.0, Draft) |
| Decisions | `ADR/ADR-0001..0005` (reconciliation required — G-003/G-004) |
| Prior review | `Technical_Review_Report.md` (TR-001 — stale, G-005) |
| Framework roadmap | `07_Docs/Repository_Roadmap.md` (M6 / P6) |
| Foundation freeze | `07_Docs/ADR-0001-Repository-Foundation-Frozen.md` |

---

# Version History

| Version | Date       | Author | Notes |
| ------- | ---------- | ------ | ----- |
| 0.1.0   | 2026-06-30 |        | Initial project bootstrap plan for ChatGptInExcel (first framework project) |
