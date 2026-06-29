# Review Report

> Canonical review report for the AI Engineering Framework.
> This document records the outcome of a completed review.
> Every review shall produce exactly one Review Report.
> The report summarizes findings from the corresponding Review Form and shall remain immutable after approval except through versioned revisions.

---

# Document Information

| Field            | Value                       |
| ---------------- | --------------------------- |
| Report ID        |                             |
| Review ID        |                             |
| Artifact Name    |                             |
| Artifact Path    |                             |
| Artifact Version |                             |
| Review Type      |                             |
| Report Version   |                             |
| Status           | Draft / Approved / Archived |
| Reviewer         |                             |
| Review Date      |                             |

---

# Executive Summary

Provide a concise summary of the review.

Include:

* Overall quality
* Major findings
* Overall recommendation
* Final decision

Maximum recommended length:

10–15 sentences.

---

# Review Scope

## Reviewed

Describe the reviewed artifact(s).

## Excluded

Describe any excluded scope.

## References

List supporting documents.

Examples:

* Requirement.md
* Architecture.md
* ADR.md
* Review_Form.md
* Repository Rules

---

# Overall Result

| Field          | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Overall Score  |                                                         |
| Quality Gate   | Pass / Fail                                             |
| Final Decision | PASS / PASS WITH MINOR CHANGES / REVIEW REQUIRED / FAIL |
| Confidence     | High / Medium / Low                                     |

---

# Decision Justification

Explain why the final decision was reached. The decision shall be evidence-based and traceable.

Reference:

* Overall Score
* Quality Gate
* Critical Findings
* Major Findings
* Risk Assessment

---

# Category Scores

| Category              | Score | Status | Notes |
| --------------------- | ----: | ------ | ----- |
| Architecture          |       |        |       |
| Engineering Quality   |       |        |       |
| Maintainability       |       |        |       |
| Scalability           |       |        |       |
| AI Compatibility      |       |        |       |
| Context Management    |       |        |       |
| Token Efficiency      |       |        |       |
| Security              |       |        |       |
| Performance           |       |        |       |
| Documentation         |       |        |       |
| Consistency           |       |        |       |
| Repository Compliance |       |        |       |
| Dependency Management |       |        |       |
| Versioning            |       |        |       |
| Future Expansion      |       |        |       |

---

# Strengths

Document the major strengths identified during the review.

| ID    | Description | Evidence |
| ----- | ----------- | -------- |
| S-001 |             |          |

---

# Findings

Document issues requiring attention.

| ID    | Severity                 | Description | Evidence | Recommendation |
| ----- | ------------------------ | ----------- | -------- | -------------- |
| F-001 | Critical / Major / Minor |             |          |                |

---

# Conflict Detection

Detect and document conflicts between requirements, architecture documents, ADRs, repository rules, and existing standards.

| Conflict ID | Sources | Impact | Recommendation |
| ----------- | ------- | ------ | -------------- |
|             |         |        |                |

If no conflicts exist, explicitly state:

> No conflicts identified.

---

# Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
|      |            |        |            |

Summarize the overall residual risk.

---

# Improvement Plan

| ID     | Action | Priority                       | Owner | Target Version | Status |
| ------ | ------ | ------------------------------ | ----- | -------------- | ------ |
| IP-001 |        | Critical / High / Medium / Low |       |                |        |

---

# Quality Gate Evaluation

Verify mandatory quality gates.

| Gate             | Required | Actual | Result |
| ---------------- | -------- | ------ | ------ |
| Architecture     | ≥ 9      |        |        |
| Security         | ≥ 9      |        |        |
| Maintainability  | ≥ 9      |        |        |
| AI Compatibility | ≥ 9      |        |        |
| Token Efficiency | ≥ 8      |        |        |
| Overall Score    | ≥ 90     |        |        |

---

# Compliance Verification

Verify compliance with:

* Requirement.md
* Architecture.md
* ADR.md
* Global.md
* Repository Rules
* Security Requirements

Record any non-compliance.

---

# Traceability

Link the review to repository artifacts.

| Artifact     | Reference |
| ------------ | --------- |
| Requirement ID       |           |
| Architecture ID      |           |
| ADR ID               |           |
| Review Form ID       |           |
| Review Prompt Version |          |
| Issue ID             |           |
| Commit ID            |           |
| Pull Request         |           |

Every review should be traceable to repository artifacts.

---

# Evidence Summary

Summarize the evidence used during the review to support auditability.

| Evidence Source | Description |
| --------------- | ----------- |
| Requirement     |             |
| Architecture    |             |
| ADR             |             |
| Repository Rule |             |
| Previous Review |             |

---

# Follow-up Actions

Document required actions after the review.

| Action | Owner | Due Date | Status |
| ------ | ----- | -------- | ------ |
|        |       |          |        |

---

# Recommendations Summary

Summarize recommendations, aligned with the Improvement Plan.

## Immediate Actions

*

## Short-term Improvements

*

## Long-term Improvements

*

---

# Review Metrics

| Metric              | Value |
| ------------------- | ----- |
| Review Duration     |       |
| Review Iteration    |       |
| Issues Identified   |       |
| Critical Findings   |       |
| Major Findings      |       |
| Minor Findings      |       |
| Issues Resolved     |       |
| Issues Remaining    |       |
| Categories Reviewed |       |
| Categories Passed   |       |
| Categories Failed   |       |
| Average Score       |       |
| Highest Score       |       |
| Lowest Score        |       |

---

# Lessons Learned

Document knowledge gained during the review.

## What Worked Well

*

## What Should Improve

*

## Recommendations

*

---

# Decision Consistency Check

Verify the review is internally consistent. Document any inconsistency.

* Final Decision matches Overall Score.
* Final Decision matches Quality Gate.
* Findings support the Decision.
* Risks are consistent with the Decision.
* Improvement Plan addresses identified issues.

---

# Approval

| Role              | Name | Date | Status |
| ----------------- | ---- | ---- | ------ |
| Reviewer          |      |      |        |
| Quality Assurance |      |      |        |
| Approver          |      |      |        |

---

# Notes

Additional review information not covered elsewhere.

---

# Version Compatibility

Future versions of `Review_Report.md` should remain backward compatible whenever practical.

Breaking structural changes require a version increment.

---

# Version History

| Version | Date       | Author | Notes                                                                                                                                                                  |
| ------- | ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical review report template                                                                                                                            |
| 1.1.0   | 2026-06-29 |        | Added Decision Justification, Conflict Detection, Decision Consistency Check, Evidence Summary, Recommendations Summary, Version Compatibility; expanded Traceability and Review Metrics |
