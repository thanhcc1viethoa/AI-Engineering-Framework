# Architecture

> Technical architecture for the ChatGptInExcel project.
> Instantiated from the frozen `03_Templates/Architecture.md` (v1.1.0).
> This architecture satisfies the approved requirements in `Requirement.md` (REQ-001, v0.3.1) and remains traceable to them.
> REQ-001 is Approved; this architecture remains Draft pending its own technical review and approval.

---

# Document Information

| Field           | Value                    |
| --------------- | ------------------------ |
| Project Name    | ChatGptInExcel           |
| Architecture ID | ARC-001                  |
| Version         | 0.5.1                    |
| Status          | Draft                    |
| Author          |                          |
| Architect       |                          |
| Reviewer        |                          |
| Created Date    | 2026-06-29               |
| Last Updated    | 2026-06-30               |
| Requirement Ref | REQ-001 (v0.3.1, Approved) |

---

# Purpose

Define a local, personal Windows architecture that lets ChatGPT operate on Excel desktop workbooks through an MCP server and Excel bridge.

* Design goals: local MCP integration, direct workbook read/write tools, explicit write confirmation, no unofficial ChatGPT web automation.
* Technical objectives: expose bounded Excel tools to ChatGPT; use Excel desktop COM automation for workbook access; avoid unattended destructive changes.
* Quality attributes: security, maintainability, AI compatibility, reliability, local operability.
* Architectural vision: ChatGPT calls MCP tools; the local MCP server delegates workbook operations to an Excel bridge running on the user's Windows machine.

---

# Scope

## In Scope

* Local MCP server for personal Windows use.
* Excel desktop bridge using local automation.
* MCP tools for listing workbooks, listing worksheets, reading ranges, and writing ranges.
* Explicit confirmation for write operations.
* Local diagnostics without logging workbook content.
* Existing Excel add-in shell as optional helper UI.

## Out of Scope

* Direct ChatGPT account login inside an Excel add-in.
* Browser automation, scraping, or reuse of consumer ChatGPT web sessions.
* AppSource publishing, organizational deployment, marketplace packaging, or enterprise rollout.
* Non-Excel Office hosts in this version.
* Cloud workbook access through Microsoft Graph in the MVP.
* Model fine-tuning or self-hosted models.

---

# Architecture Drivers

* AI tool integration - ChatGPT needs a supported tool boundary to operate on Excel.
* Local personal use - workbook access happens on the user's machine.
* Safety - write operations must be confirmed before mutation.
* Privacy - only explicitly requested ranges are returned through MCP.
* Maintainability - tool contracts are small, testable, and versionable.

---

# Design Principles

* Local First - the Excel bridge runs on the user's computer.
* Explicit Context - tools read only requested workbook, worksheet, and range data.
* Confirm Before Write - no workbook mutation occurs without explicit confirmation.
* No Unofficial ChatGPT Automation - do not automate the ChatGPT web UI or reuse browser sessions.
* Tool Boundary First - ChatGPT interacts through MCP tools, not hidden UI behavior.

---

# Architectural Constraints

* The MVP targets Windows with Excel desktop installed.
* Excel must be running for local COM automation against open workbooks.
* ChatGPT or another client must support connecting to the local MCP server.
* Workbook write operations require explicit confirmation.
* Direct ChatGPT login inside the Excel add-in remains out of scope until an official provider path exists.

---

# System Context

* External User - personal Excel user.
* External System - ChatGPT or another MCP-compatible AI client.
* Internal Systems - local MCP server, Excel bridge, optional Excel add-in shell.
* Major Interfaces - MCP stdio/transport between AI client and server; Excel COM automation between bridge and Excel desktop.

---

# High-Level Architecture

ChatGPT calls tools exposed by a local MCP server. The MCP server validates tool arguments, applies safety rules, and delegates Excel operations to a local Excel bridge. The Excel bridge uses Excel desktop automation to inspect or update open workbooks.

```text
User
  -> ChatGPT / MCP client
    -> Local MCP Server
      -> Excel Bridge
        -> Excel Desktop Workbook
```

---

# Component Architecture

| Component | Responsibility | Inputs | Outputs | Public Interfaces | Dependencies |
| --------- | -------------- | ------ | ------- | ----------------- | ------------ |
| MCP Client | User-facing AI conversation and tool invocation | User prompts | Tool calls, AI responses | MCP client configuration | ChatGPT or compatible client |
| Local MCP Server | Expose Excel tools, validate arguments, enforce safety rules | MCP tool calls | Tool results | MCP tools | Python, MCP SDK |
| Excel Bridge | Read/write open Excel workbooks | Workbook, worksheet, range, values | Workbook data or mutation result | Python module API | pywin32, Excel desktop |
| Excel Desktop | Host user workbooks | User workbooks | Workbook state | COM automation | Microsoft Excel |
| Optional Excel Add-in Shell | Helper UI for personal workflow | User input | Prompt helper output | Office.js task pane | Local HTTPS server |

---

# MCP Tool Contracts

| Tool | Purpose | Mutation | Confirmation Required |
| ---- | ------- | -------- | --------------------- |
| `list_workbooks` | Return open Excel workbook names | No | No |
| `list_worksheets` | Return worksheet names for a workbook | No | No |
| `get_active_workbook` | Return the active workbook name | No | No |
| `get_selected_range` | Return selected range address and values | No | No |
| `read_range` | Return values from a specified range | No | No |
| `write_range` | Write values to a specified range | Yes | Yes |

Write tools return a preview when `confirm=false`; they mutate Excel only when `confirm=true`.

---

# Technology Decisions

| Technology | Purpose | Alternatives Considered | Selection Reason |
| ---------- | ------- | ----------------------- | ---------------- |
| MCP server | ChatGPT-to-tool integration boundary | Excel add-in direct ChatGPT login, browser automation | Official tool-style integration model; avoids unsupported login automation |
| Python | Local bridge implementation | Node.js, .NET | Strong Windows automation ecosystem; simple local scripts |
| pywin32 / COM | Excel desktop automation | Microsoft Graph, Office.js add-in bridge | Direct access to open desktop workbooks for personal Windows use |
| Existing Excel add-in shell | Optional helper UI | Remove add-in | Useful as a manual fallback, but no longer core architecture |

---

# Data Architecture

* Data Sources: workbook names, worksheet names, selected ranges, explicitly requested cell ranges.
* Data Ownership: user owns workbook data.
* Data Flow: Excel desktop -> Excel Bridge -> MCP Server -> ChatGPT/MCP Client; write flow returns through MCP Server -> Excel Bridge -> Excel desktop.
* Storage: no workbook content persisted by default.
* Retention: transient tool-call data only.

Data classification:

* Public - none by default.
* Internal - local configuration.
* Confidential - workbook data returned by read tools.
* Secret - no provider secrets stored by the MVP bridge.

---

# Integration Architecture

| System | Interface | Protocol | Direction |
| ------ | --------- | -------- | --------- |
| ChatGPT / MCP Client | MCP tools | MCP stdio/transport | Client <-> Local MCP Server |
| Local MCP Server | Python module API | In-process | MCP Server <-> Excel Bridge |
| Excel Desktop | COM automation | Local Windows COM | Excel Bridge <-> Excel |

---

# Security Architecture

* Authentication - delegated to the MCP client surface; the local bridge does not authenticate to ChatGPT.
* Authorization - local-only use; write operations require explicit confirmation.
* Secrets Management - no OpenAI API key, service key, or ChatGPT session token is stored in the MVP.
* Privacy - tools read only user-specified workbook context.
* Audit Logging - log operation metadata locally; do not log cell contents.
* Destructive Operations - not exposed in MVP.

---

# AI Architecture

* Tool Usage - ChatGPT interacts with Excel through MCP tools.
* Context Management - range reads are explicit and bounded.
* Hallucination Mitigation - tool results include workbook, worksheet, range, and dimensions.
* Token Efficiency - avoid whole-workbook reads; return compact value arrays.
* Guardrails - write requests require confirmation and preview before mutation.

---

# Deployment Architecture

* Runtime Environment - local Python MCP server on Windows.
* Infrastructure - local machine only; no cloud deployment required.
* Configuration Management - MCP client config points to the local server command.
* Distribution - repository files and local setup script.
* Optional Add-in - existing Excel task pane shell can remain installed for manual prompt workflow.

---

# Failure Recovery

* Excel not running - return a clear error.
* Workbook not found - return available workbook names.
* Worksheet/range invalid - return a clear validation error.
* Write rejected - return preview only and leave workbook unchanged.
* Bridge failure - restart local MCP server and retry.

---

# Architecture Decisions

| Decision ID | Decision | Related ADR | Related Requirement | Status | Rationale |
| ----------- | -------- | ----------- | ------------------- | ------ | --------- |
| AD-001 | BFF proxy with server-side OpenAI key | ADR-0001 (supersession pending) | Former FR-002 | Superseded | Direct Excel add-in ChatGPT login/API path is no longer primary |
| AD-002 | Office.js cross-host task pane | ADR-0002 (supersession pending) | Former FR-001 | Superseded | Scope changed to Excel MCP bridge; add-in shell is optional |
| AD-003 | SSE streaming for add-in response | ADR-0003 (supersession pending) | Former NFR-003 | Superseded | ChatGPT interaction now happens through MCP client/tool calls |
| AD-004 | Use a local MCP server as the ChatGPT-to-Excel integration boundary | Pending reconciliation | FR-001 | Accepted | Supported tool boundary for AI-to-Excel operations |
| AD-005 | Use Excel desktop COM automation for personal Windows workbook access | Pending reconciliation | FR-002, FR-003, FR-004, FR-005 | Accepted | Direct access to open Excel desktop workbooks |
| AD-006 | Require confirmation for workbook write operations | Pending reconciliation | FR-005, NFR-003 | Accepted | Prevents unintended workbook mutation |

> ADR linkage note (per RR-ARC-001 F-001/F-002/F-003): the existing `ADR/ADR-0004` and `ADR/ADR-0005` files document the superseded design (service-wide OpenAI key; Microsoft Entra ID) and do **not** back AD-004/AD-005; no `ADR-0006` exists yet. The current decisions (AD-004, AD-005, AD-006) are documented inline here and their ADR records — together with formal supersession records for AD-001..AD-003 — are pending the scheduled ADR reconciliation step. No ADRs are created by this revision.

---

# Risks

| ID | Risk | Impact | Mitigation |
| -- | ---- | ------ | ---------- |
| AR-001 | Sensitive workbook data returned to ChatGPT | High | Read only explicit ranges |
| AR-002 | Incorrect write changes workbook | High | Preview plus explicit confirmation |
| AR-003 | Windows/Excel COM dependency limits portability | Medium | Scope MVP to personal Windows Excel desktop |
| AR-004 | MCP client support varies by ChatGPT surface | High | Keep server MCP-compatible and document setup |

---

# Traceability

| Requirement ID | Component | ADR | Notes |
| -------------- | --------- | --- | ----- |
| FR-001 | Local MCP Server | Pending reconciliation | Exposes Excel tools |
| FR-002 | Excel Bridge | Pending reconciliation | Lists open workbooks |
| FR-003 | Excel Bridge | Pending reconciliation | Lists worksheets |
| FR-004 | Excel Bridge | Pending reconciliation | Reads ranges |
| FR-005 | Local MCP Server, Excel Bridge | Pending reconciliation | Confirmed writes |
| FR-006 | Local MCP Server, Excel Bridge | Pending reconciliation | Clear errors |
| FR-007 | Optional Excel Add-in Shell | Pending reconciliation | Helper UI only (optional, non-primary) |

---

# Open Issues

| ID | Description | Owner | Status |
| -- | ----------- | ----- | ------ |
| AI-001 | Confirm available MCP client surface for the user's ChatGPT environment | User | Open |
| AI-002 | Validate local Excel COM bridge against the user's installed Excel version | User | Open |

---

# Change Log

| Version | Date | Author | Summary |
| ------- | ---- | ------ | ------- |
| 0.1.0 | 2026-06-29 | | Initial draft architecture |
| 0.2.0 | 2026-06-29 | | Resolved prior API-key and identity issues |
| 0.3.0 | 2026-06-29 | | Reopened provider authentication design |
| 0.4.0 | 2026-06-29 | | Clarified personal local sideload add-in as required output |
| 0.5.0 | 2026-06-30 | | Changed primary architecture to local MCP server plus Excel desktop bridge |
| 0.5.1 | 2026-06-30 | | Revision per RR-ARC-001 (F-001..F-006): corrected ADR references for AD-004/005/006 and the traceability table to "pending reconciliation"; marked AD-001..003 supersession pending; updated REQ reference to v0.3.1 Approved; corrected Architecture Review Checklist self-attestations. Documentation correction only; no design or decision change; no ADRs created. |

---

# Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | | | |
| Reviewer | | | |
| Approver | | | |

---

# Notes

The Excel add-in shell remains in the repository as a working helper/prototype, but the primary integration path is now MCP-driven ChatGPT-to-Excel tooling.

---

# Architecture Review Checklist

- [x] Are all approved requirements addressed?
- [ ] Are all architecture decisions traceable? — Pending ADR reconciliation (RR-ARC-001 F-001/F-003)
- [ ] Are all ADRs referenced? — Pending ADR reconciliation; current decisions not yet recorded as ADRs (RR-ARC-001 F-002)
- [x] Are interfaces documented?
- [x] Are quality attributes measurable?
- [x] Are AI boundaries defined?
- [x] Is deployment architecture complete?
- [x] Are operational requirements covered?

---

# Version History

| Version | Date | Author | Notes |
| ------- | ---- | ------ | ----- |
| 0.1.0 | 2026-06-29 | | Initial draft architecture for the ChatGptInExcel Office add-in |
| 0.2.0 | 2026-06-29 | | Resolved AI-001 and AI-002 through ADR-0004 and ADR-0005 |
| 0.3.0 | 2026-06-29 | | Reopened provider authentication design; direct ChatGPT account login preferred pending official validation |
| 0.4.0 | 2026-06-29 | | Clarified personal local sideload add-in as the required output |
| 0.5.0 | 2026-06-30 | | Changed primary architecture to local MCP server plus Excel desktop bridge |
| 0.5.1 | 2026-06-30 | | Revision per RR-ARC-001: corrected ADR references and traceability to pending reconciliation; supersession pending for AD-001..003; REQ reference updated to v0.3.1 Approved; checklist self-attestation corrected. No design change; no ADRs created. |
