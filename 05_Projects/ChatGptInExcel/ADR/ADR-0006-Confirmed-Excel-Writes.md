# Architecture Decision Record (ADR)

> ADR-0006 (ChatGptInExcel) - Require explicit confirmation for workbook write operations.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field | Value |
| ----- | ----- |
| ADR ID | ADR-0006 |
| Title | Confirmed Excel write operations |
| Project | ChatGptInExcel |
| Version | 1.0.0 |
| Status | Accepted |
| Author | |
| Reviewer | |
| Decision Date | 2026-06-30 |
| Last Updated | 2026-06-30 |

---

# Decision Summary

All workbook write operations exposed through MCP require explicit confirmation. If confirmation is absent, the tool returns a preview and does not mutate Excel.

---

# Context

ChatGPT-generated writes can be useful but may also overwrite workbook data. The personal assistant must protect the user's workbook from accidental mutation.

---

# Problem Statement

How should the MCP bridge prevent accidental or unintended Excel writes?

---

# Decision

Require write tools to accept an explicit confirmation flag. Destructive tools such as sheet deletion are not exposed in the MVP.

---

# Decision Classification

* Security Decision
* AI Decision
* Architecture Decision

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
| Unrestricted writes | Fastest UX | Unsafe; high risk of workbook damage | Rejected |
| Confirmed writes | Useful and controlled | Requires one extra step | Chosen |
| Read-only MVP | Safest | Does not satisfy direct Excel operation goal | Rejected |

---

# Decision Rationale

Confirmed writes balance usefulness and safety. The AI can prepare proposed changes, but the user retains control before mutation.

---

# Consequences

## Positive

* Prevents accidental workbook mutation.
* Creates an auditable preview-before-write flow.

## Negative

* Adds friction to write workflows.

## Risks

* Users may confirm incorrect writes; clear previews are required.

---

# Impact Assessment

| Area | Impact |
| ---- | ------ |
| Architecture | Write tools include confirmation gate |
| Development | Tool implementation must support dry-run previews |
| Testing | Must test confirm=false and confirm=true behavior |
| Operations | User reviews proposed writes |
| Security | Reduces unintended mutation risk |
| AI Agents | AI must request confirmation before final write |
| Documentation | Tool docs must explain confirmation |

---

# Compliance

Consistent with REQ-001 (FR-005, NFR-003), Global Rules, and repository security principles.

---

# Traceability

| Artifact | Reference |
| -------- | --------- |
| Requirement | REQ-001 (FR-005, NFR-003) |
| Architecture | ARC-001 (AD-006) |
| Review | Architecture_Decision_Review.md |
| Issue | AI-003 |
| Commit | |

---

# AI Considerations

The AI client should first call write tools with `confirm=false`, summarize the preview to the user, and call again with `confirm=true` only after user approval.

---

# Validation

* `write_range(confirm=false)` returns preview only.
* `write_range(confirm=true)` mutates the target test range.

---

# Success Criteria

| Metric | Target | Validation Method |
| ------ | ------ | ----------------- |
| Dry-run write leaves workbook unchanged | Pass | Test |
| Confirmed write updates target range | Pass | Test |

---

# Rollback Strategy

Disable write tools or run the MCP server in read-only mode if confirmed writes prove unsafe.

---

# Approval

| Role | Name | Date | Status |
| ---- | ---- | ---- | ------ |
| Architect | | | |
| Reviewer | | | |
| Approver | | | |

---

# Version History

| Version | Date | Author | Notes |
| ------- | ---- | ------ | ----- |
| 1.0.0 | 2026-06-30 | | Accepted: explicit confirmation for Excel write operations |
