# Architecture Decision Record (ADR)

> ADR-0002 (ChatGptInExcel) — Use Office.js for a cross-host task pane.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field         | Value                                  |
| ------------- | -------------------------------------- |
| ADR ID        | ADR-0002                               |
| Title         | Use Office.js for a cross-host task pane |
| Project       | ChatGptInExcel                         |
| Version       | 1.0.0                                  |
| Status        | Superseded by ADR-0005                 |
| Author        |                                        |
| Reviewer      |                                        |
| Decision Date | 2026-06-29                             |
| Last Updated  | 2026-06-29                             |

---

# Decision Summary

The add-in is built as an Office Add-in using the Office JavaScript API (Office.js), with a single web code base serving a task pane in both Excel and Word.

---

# Context

* The add-in must run in both Excel and Word (REQ-001, FR-001, NFR-001).
* A web-based add-in deploys centrally and supports desktop and web Office.

---

# Problem Statement

Which Office extensibility technology should host the add-in across Excel and Word?

---

# Decision

Use the Office Add-in model with Office.js. Host-specific operations (reading a selection, inserting content) are isolated behind an Office Host Adapter so the rest of the code base is host-neutral.

---

# Decision Classification

* Architecture Decision
* Technology Decision

---

# Decision Priority

High.

---

# Decision Lifecycle

Accepted.

---

# Alternatives Considered

| Alternative                | Advantages                  | Disadvantages                          | Reason Rejected                    |
| -------------------------- | --------------------------- | -------------------------------------- | ---------------------------------- |
| VSTO / COM add-in          | Deep desktop integration    | Windows-only; per-host; heavier deploy | Not cross-host; no Office on web   |
| Separate native add-ins    | Host-optimized              | Duplicated code per host               | Violates single-source-of-truth    |
| Office.js add-in (chosen)  | One code base; web + desktop | Constrained to Office.js capabilities  | —                                  |

---

# Decision Rationale

* Trade-offs: limited to Office.js capabilities in exchange for one cross-host, centrally deployable code base.
* Benefits gained: Excel + Word from one build; desktop and web support; modern deployment.

---

# Consequences

## Positive

* Single code base across hosts.
* Web-based, centrally deployable.

## Negative

* Bound to Office.js feature coverage.

## Risks

* Host/API differences across Excel/Word and desktop/web — mitigated by the Office Host Adapter and per-host testing.

---

# Impact Assessment

| Area          | Impact                                  |
| ------------- | --------------------------------------- |
| Architecture  | Client built on Office.js + adapter     |
| Development   | One code base; host logic isolated      |
| Operations    | Web hosting + manifest distribution     |

---

# Compliance

Consistent with `01_Rules/Global.md` and REQ-001 (FR-001, NFR-001).

---

# Traceability

| Artifact      | Reference          |
| ------------- | ------------------ |
| Requirement   | REQ-001 (FR-001, NFR-001) |
| Architecture  | ARC-001 (AD-002)   |
| Risk          | AR-003             |

---

# Validation

* Architecture Review.
* Demonstration: the same build runs in Excel and Word.

---

# Approval

| Role      | Name | Date | Status |
| --------- | ---- | ---- | ------ |
| Architect |      |      |        |
| Reviewer  |      |      |        |
| Approver  |      |      |        |

---

# Superseded By

| ADR ID   | Reason |
| -------- | ------ |
| ADR-0005 | Excel access moved from an Office.js task pane to desktop COM automation driven by the local MCP server, so the cross-host Office.js add-in is no longer the access mechanism. |

---

# Version History

| Version | Date       | Author | Notes                              |
| ------- | ---------- | ------ | ---------------------------------- |
| 1.0.0   | 2026-06-29 |        | Accepted: Office.js cross-host task pane |
| 1.1.0   | 2026-06-30 |        | Superseded by ADR-0005 (Excel desktop COM bridge) |
