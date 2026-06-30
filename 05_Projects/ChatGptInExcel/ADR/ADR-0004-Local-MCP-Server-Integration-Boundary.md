# Architecture Decision Record (ADR)

> ADR-0004 (ChatGptInExcel) - Use a local MCP server as the ChatGPT-to-Excel integration boundary.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field         | Value                                      |
| ------------- | ------------------------------------------ |
| ADR ID        | ADR-0004                                   |
| Title         | Local MCP server as ChatGPT-to-Excel integration boundary |
| Project       | ChatGptInExcel                            |
| Version       | 1.0.0                                      |
| Status        | Accepted                                   |
| Author        |                                            |
| Reviewer      |                                            |
| Decision Date | 2026-06-30                                 |
| Last Updated  | 2026-06-30                                 |

---

# Decision Summary

ChatGPT will operate on Excel through a local MCP server instead of through direct ChatGPT account login inside an Excel add-in. The MCP server exposes bounded Excel tools that a compatible ChatGPT/MCP client can call. This avoids unsupported browser/session automation and creates a clear tool boundary for workbook operations.

---

# Context

The desired product behavior is for ChatGPT to read, analyze, and update Excel workbooks. Direct ChatGPT account login inside a third-party Excel add-in is not an established official public integration path for this project. OpenAI's MCP/tool model supports AI clients invoking external tools, so a local MCP server is the more suitable integration boundary.

---

# Problem Statement

What architecture boundary should allow ChatGPT to operate on Excel workbooks without relying on unsupported ChatGPT web automation?

---

# Decision

Use a local MCP server as the ChatGPT-to-Excel integration boundary.

The server shall expose Excel tools such as:

* `list_workbooks`
* `list_worksheets`
* `get_active_workbook`
* `get_selected_range`
* `read_range`
* `write_range`

---

# Decision Classification

* Architecture Decision
* AI Decision
* Technology Decision

---

# Decision Priority

Critical.

---

# Decision Lifecycle

Accepted.

---

# Alternatives Considered

| Alternative | Advantages | Disadvantages | Reason Rejected |
| ----------- | ---------- | ------------- | --------------- |
| Direct ChatGPT login inside Excel add-in | Desired UX | No confirmed official public delegated auth path; high risk if automated | Blocked pending provider capability |
| OpenAI API key from add-in/backend | Technically viable | Uses API key rather than ChatGPT account/tool workflow | Not the desired interaction model |
| Local MCP server | Supported tool boundary; local; avoids browser automation | Requires local server and MCP client setup | Chosen |

---

# Decision Rationale

MCP gives ChatGPT a structured and auditable way to call tools. It preserves the user's desired direction, where ChatGPT performs Excel operations, while avoiding unsupported ChatGPT session automation. The trade-off is local setup complexity.

---

# Consequences

## Positive

* ChatGPT can call explicit Excel tools.
* No ChatGPT web UI scraping or session reuse.
* Tool contracts are testable and traceable.

## Negative

* Requires local server setup.
* Depends on MCP client availability.

## Risks

* MCP support may vary by ChatGPT surface.

---

# Impact Assessment

| Area | Impact |
| ---- | ------ |
| Architecture | Replaces direct add-in-provider login with MCP tool boundary |
| Development | Adds local MCP server |
| Testing | Requires local tool invocation tests |
| Operations | User runs a local server |
| Security | Tool calls must be bounded and safe |
| AI Agents | ChatGPT uses explicit tools |
| Documentation | Setup instructions required |

---

# Compliance

Consistent with repository governance, Global Rules, and REQ-001 v0.3.0.

---

# Traceability

| Artifact | Reference |
| -------- | --------- |
| Requirement | REQ-001 (FR-001) |
| Architecture | ARC-001 (AD-004) |
| Review | Architecture_Decision_Review.md |
| Issue | AI-001 |
| Commit | |

---

# AI Considerations

The decision makes MCP tool contracts the primary AI integration surface. Prompting must instruct ChatGPT to request only bounded ranges and to use write tools only after user confirmation.

---

# Validation

* Prototype local MCP server.
* Verify tool list and read/write tool behavior.
* Confirm no browser automation is used.

---

# Success Criteria

| Metric | Target | Validation Method |
| ------ | ------ | ----------------- |
| MCP server starts | Pass | Local run |
| Excel tools visible to client | Pass | MCP client inspection |
| No ChatGPT web automation | Pass | Code inspection |

---

# Rollback Strategy

Rollback to the manual Excel add-in helper workflow or a future approved API-key architecture if MCP client setup is not viable.

---

# Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | | | |
| Reviewer | | | |
| Approver | | | |

---

# Supersedes

This decision replaces earlier integration decisions that assumed an Office task-pane add-in talking to a backend service.

| ADR ID   | Reason |
| -------- | ------ |
| ADR-0001 | The backend-for-frontend proxy and server-side OpenAI key are no longer part of the architecture; ChatGPT is the MCP client and no AI credential is handled by this project. |
| ADR-0003 | SSE streaming from a backend to a task pane is removed; the MCP transport now carries client-to-tool communication. |

---

# Version History

| Version | Date | Author | Notes |
| ------- | ---- | ------ | ----- |
| 1.0.0 | 2026-06-30 | | Accepted: local MCP server integration boundary |
