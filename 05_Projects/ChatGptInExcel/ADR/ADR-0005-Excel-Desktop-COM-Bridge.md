# Architecture Decision Record (ADR)

> ADR-0005 (ChatGptInExcel) - Use Excel desktop COM automation for personal Windows workbook access.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field | Value |
| ----- | ----- |
| ADR ID | ADR-0005 |
| Title | Excel desktop COM automation for workbook access |
| Project | ChatGptInExcel |
| Version | 1.0.0 |
| Status | Accepted |
| Author | |
| Reviewer | |
| Decision Date | 2026-06-30 |
| Last Updated | 2026-06-30 |

---

# Decision Summary

The local MCP server will access Excel desktop workbooks through a Python Excel bridge using Windows COM automation. This targets the user's personal Windows machine and open Excel workbooks.

---

# Context

The user wants ChatGPT to operate on Excel workbooks on their computer. For a personal Windows MVP, Excel desktop COM automation provides direct local access to open workbooks without requiring OneDrive, Microsoft Graph, or an Excel add-in bridge.

---

# Problem Statement

How should the local MCP server read and write the user's Excel workbooks?

---

# Decision

Use Python with `pywin32` to automate Excel desktop through COM.

---

# Decision Classification

* Technology Decision
* Architecture Decision
* Operational Decision

---

# Decision Priority

High.

---

# Decision Lifecycle

Accepted.

---

# Alternatives Considered

| Alternative | Advantages | Disadvantages | Reason Rejected |
| ----------- | ---------- | ------------- | --------------- |
| Microsoft Graph Excel API | Cloud-native | Requires Microsoft auth and workbook in OneDrive/SharePoint | Not aligned with personal open-desktop-workbook MVP |
| Office.js add-in bridge | Uses existing add-in shell | Requires local communication between add-in and server | More complex than needed for MVP |
| Excel COM automation | Direct open workbook access on Windows | Windows and Excel desktop specific | Chosen |

---

# Decision Rationale

COM automation is the fastest practical path for a personal Windows Excel assistant. It keeps workbook operations local and allows direct interaction with open workbooks.

---

# Consequences

## Positive

* Direct access to open Excel desktop workbooks.
* No cloud workbook requirement.
* Simple MVP implementation.

## Negative

* Windows-only.
* Requires Excel desktop installed and running.

## Risks

* COM automation can be brittle if Excel is busy or modal dialogs are open.

---

# Impact Assessment

| Area | Impact |
| ---- | ------ |
| Architecture | Adds Excel Bridge component |
| Development | Adds Python/pywin32 dependency |
| Testing | Requires Excel desktop validation |
| Operations | User runs bridge locally |
| Security | Workbook access is local but powerful |
| AI Agents | Tools can inspect workbook state |
| Documentation | Windows setup required |

---

# Compliance

Consistent with REQ-001 v0.3.0 and ARC-001 v0.5.0.

---

# Traceability

| Artifact | Reference |
| -------- | --------- |
| Requirement | REQ-001 (FR-002, FR-003, FR-004, FR-005) |
| Architecture | ARC-001 (AD-005) |
| Review | Architecture_Decision_Review.md |
| Issue | AI-002 |
| Commit | |

---

# AI Considerations

Tool descriptions must make workbook, worksheet, and range arguments explicit. The AI client should avoid broad or destructive operations and should request specific ranges.

---

# Validation

* Open Excel.
* Run bridge.
* List open workbooks.
* Read a known range.
* Write a confirmed value to a test range.

---

# Success Criteria

| Metric | Target | Validation Method |
| ------ | ------ | ----------------- |
| Open workbook listing | Pass | Demonstration |
| Range read | Pass | Test |
| Confirmed range write | Pass | Test |

---

# Rollback Strategy

Use the optional Excel add-in helper workflow or revisit Microsoft Graph if COM automation proves unsuitable.

---

# Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | | | |
| Reviewer | | | |
| Approver | | | |

---

# Supersedes

| ADR ID   | Reason |
| -------- | ------ |
| ADR-0002 | Excel access no longer uses the Office.js cross-host task pane; workbook operations are performed through desktop COM automation invoked by the local MCP server. |

---

# Version History

| Version | Date | Author | Notes |
| ------- | ---- | ------ | ----- |
| 1.0.0 | 2026-06-30 | | Accepted: Excel desktop COM bridge for personal Windows use |
