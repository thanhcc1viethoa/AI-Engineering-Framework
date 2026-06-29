# Artifact Revision Request

> Canonical revision request template for the AI Engineering Framework.
> This template defines how approved artifacts shall be revised after review.
> It standardizes communication between reviewers and implementation agents while preserving repository consistency.
> Every revision request shall be traceable and limited to the approved review scope.

---

# Request Information

| Field            | Value |
| ---------------- | ----- |
| Request ID       |       |
| Artifact Name    |       |
| Artifact Path    |       |
| Artifact Version |       |
| Review Report    |       |
| Reviewer         |       |
| Revision Owner   |       |
| Date             |       |

---

# Revision Purpose

State why this revision is required.

Examples:

* Address review findings.
* Improve maintainability.
* Resolve inconsistencies.
* Clarify documentation.
* Improve AI compatibility.

---

# Revision Scope

## In Scope

List the sections that may be modified.

---

## Out of Scope

List the sections that must remain unchanged.

Anything outside the approved scope shall not be modified.

---

# Revision Type

Select one or more.

- [ ] Documentation Improvement
- [ ] Quality Improvement
- [ ] Architecture Clarification
- [ ] AI Optimization
- [ ] Security Improvement
- [ ] Repository Compliance
- [ ] Version Update
- [ ] Refactoring
- [ ] Bug Fix
- [ ] Other

---

# Revision Strategy

Selecting a Revision Strategy is mandatory. Select exactly one implementation strategy.

- [ ] Patch
- [ ] Merge
- [ ] Refactor
- [ ] Replace

Definitions:

* Patch — Minimal changes that preserve the existing implementation.
* Merge — Integrate approved improvements while preserving existing approved content.
* Refactor — Improve internal structure without changing responsibilities or external behavior.
* Replace — Replace an approved section with a newly approved implementation; requires explicit architectural approval.

---

# Revision Classification

Classify the revision. A revision may belong to multiple classifications.

* Editorial
* Documentation
* Technical
* Architecture
* Security
* AI Optimization
* Repository Governance
* Breaking Change

---

# Revision Priority

Priority determines implementation order.

* Critical
* High
* Medium
* Low

---

# Revision Lifecycle

The revision follows a standardized lifecycle, consistent with repository governance.

* Proposed
* Approved
* In Progress
* Implemented
* Verified
* Closed
* Rejected

---

# Required Changes

Describe each required change.

| ID     | Section | Description | Priority                       |
| ------ | ------- | ----------- | ------------------------------ |
| RC-001 |         |             | Critical / High / Medium / Low |

---

# Findings Reference

Every requested change shall reference a review finding.

| Finding ID | Related Change |
| ---------- | -------------- |
| F-001      | RC-001         |

---

# Traceability

Reference repository artifacts so every revision remains reconstructable.

| Artifact          | Reference |
| ----------------- | --------- |
| Requirement ID    |           |
| Architecture ID   |           |
| ADR ID            |           |
| Review Report ID  |           |
| Commit ID         |           |
| Pull Request      |           |
| Issue ID          |           |
| Change Request ID |           |

---

# Impact Assessment

Evaluate the impact of the revision before implementation.

| Area          | Impact |
| ------------- | ------ |
| Architecture  |        |
| Documentation |        |
| AI Agents     |        |
| Repository    |        |
| Versioning    |        |
| Security      |        |

---

# Risk Assessment

Identify revision risks.

| Risk            | Likelihood | Impact | Mitigation |
| --------------- | ---------- | ------ | ---------- |
| Technical Risk  |            |        |            |
| Repository Risk |            |        |            |
| AI Risk         |            |        |            |
| Regression Risk |            |        |            |

---

# Rollback Plan

Every significant revision shall define how it can be reversed. Rollback shall remain traceable.

* Rollback Trigger
* Rollback Procedure
* Recovery Method

---

# Constraints

The implementation agent shall NOT:

* Rewrite the entire artifact.
* Redesign the architecture.
* Modify unrelated sections.
* Remove approved content.
* Change repository structure.
* Invent requirements.
* Invent repository rules.

---

# Preservation Requirements

The implementation shall preserve:

* Existing architecture.
* Existing intent.
* Existing traceability.
* Existing identifiers.
* Existing version history.
* Existing approvals unless explicitly superseded.

---

# AI Revision Rules

AI shall never:

* Modify unrelated sections.
* Remove approved content.
* Change repository architecture.
* Introduce undocumented changes.
* Ignore revision scope.

---

# Expected Deliverables

The implementation shall provide:

* Updated artifact.
* Updated version history.
* Summary of changes.
* List of modified sections.
* Any required traceability updates.

---

# Validation Requirements

Before completion verify:

- [ ] Requested changes implemented.
- [ ] No unrelated changes introduced.
- [ ] Repository consistency maintained.
- [ ] References updated.
- [ ] Markdown formatting preserved.
- [ ] Version updated correctly.

Record validation evidence for completed revisions.

Examples:

* Review
* Test
* Benchmark
* Demonstration
* Inspection

---

# Success Criteria

The revision is successful when:

* All requested changes are implemented.
* No new review findings are introduced.
* Existing functionality remains unchanged.
* Repository compliance is preserved.

---

# Revision Metrics

Track revision quality.

| Metric                        | Target |
| ----------------------------- | ------ |
| Requested Changes Implemented | 100%   |
| Unrelated Changes             | 0      |
| Review Findings Remaining     | 0      |
| Repository Compliance         | 100%   |

---

# Reviewer Notes

Additional reviewer guidance.

---

# Revision Checklist

Verify before approval:

- [ ] Scope respected
- [ ] Requested changes completed
- [ ] No unrelated modifications
- [ ] Traceability preserved
- [ ] Version updated correctly
- [ ] References updated
- [ ] Review completed
- [ ] Repository compliant

---

# Approval

| Role           | Name | Date | Status |
| -------------- | ---- | ---- | ------ |
| Reviewer       |      |      |        |
| Revision Owner |      |      |        |
| Approver       |      |      |        |

---

# Version Compatibility

Future revisions shall remain backward compatible whenever practical.

Breaking revisions require:

* Explicit approval
* Updated version
* Migration guidance
* Review approval

---

# Version History

| Version | Date       | Author | Notes                                                                                                                                                                              |
| ------- | ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical artifact revision request template                                                                                                                             |
| 1.1.0   | 2026-06-29 |        | Added Revision Classification, Priority, Lifecycle, Traceability, Impact Assessment, Risk Assessment, Rollback Plan, AI Revision Rules, Revision Metrics, Revision Checklist, Version Compatibility; expanded Validation Requirements |
| 1.1.1   | 2026-06-29 |        | Finalization pass: standardized checklist markers to `- [ ]` in Revision Type and Validation Requirements for internal consistency; no functional changes |
| 1.2.0   | 2026-06-29 |        | Added mandatory Revision Strategy field (Patch / Merge / Refactor / Replace) |
