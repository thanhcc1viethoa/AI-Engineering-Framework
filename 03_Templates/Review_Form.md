# Review Form

> Official, project-agnostic review standard for the AI Engineering Framework.
> Applicable to documentation, source code, prompts, templates, architecture,
> configuration, and AI-generated outputs. Copy this form per review; do not
> edit the master template.

---

# Document Information

| Field          | Value |
|----------------|-------|
| Artifact Name  |       |
| Artifact Path  |       |
| Artifact Type  |       |
| Artifact Version |     |
| Author         |       |
| Reviewer       |       |
| Review Date    |       |
| Review ID      |       |

---

# Review Scope

- **In scope:**
- **Out of scope:**
- **Inputs / references:**
- **Objective of this review:**

---

# Review Type

Select all that apply:

- [ ] Architecture Review
- [ ] Documentation Review
- [ ] Code Review
- [ ] Security Review
- [ ] AI Output Review
- [ ] Release Review

---

# Review Summary

| Field            | Value                  |
|------------------|------------------------|
| Overall Score    | ____ / 100             |
| Pass / Fail      | ☐ Pass  ☐ Fail         |
| Confidence Level | ☐ High ☐ Medium ☐ Low  |
| Reviewer         |                        |
| Date             |                        |

**Summary notes:**

---

# Review Criteria

Score each criterion from **0–10**. Record purpose, answers, comments, and
concrete improvement actions. Leave a criterion's score blank only if it is
explicitly marked *Not Applicable* with a justification.

## 1. Architecture

- **Purpose:** Assess whether the structure is sound, modular, and extensible.
- **Evaluation Questions:**
  - Is the structure logical and complete?
  - Are responsibilities clearly separated?
  - Is unnecessary complexity avoided?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 2. Engineering Quality

- **Purpose:** Assess correctness, clarity, and practical soundness.
- **Evaluation Questions:**
  - Are principles and logic clear and correct?
  - Is terminology consistent?
  - Is the work practical and reusable?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 3. Maintainability

- **Purpose:** Assess how easily the artifact can be understood and changed.
- **Evaluation Questions:**
  - Is it easy to update and extend?
  - Is duplication minimized?
  - Is intent easy to follow?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 4. Scalability

- **Purpose:** Assess suitability for growth in size, usage, and reuse.
- **Evaluation Questions:**
  - Does it scale without redesign?
  - Is it easy to reuse and migrate?
  - Are extension points defined?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 5. AI Compatibility

- **Purpose:** Assess how reliably AI agents can understand and act on it.
- **Evaluation Questions:**
  - Can an agent understand the context?
  - Can an agent execute it consistently?
  - Is the hallucination or misinterpretation risk low?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 6. Context Management

- **Purpose:** Assess retrievability and modular structuring of content.
- **Evaluation Questions:**
  - Are sections self-contained and clearly headed?
  - Is content easy to index and retrieve?
  - Is a single source of truth preserved?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 7. Token Efficiency

- **Purpose:** Assess conciseness and economy of context.
- **Evaluation Questions:**
  - Is repetition avoided?
  - Is content modular and loadable selectively?
  - Is formatting lean and machine-friendly?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 8. Security

- **Purpose:** Assess exposure, safety, and least-privilege adherence.
- **Evaluation Questions:**
  - Are there any secrets or sensitive values?
  - Is any unsafe instruction or guidance present?
  - Are least-privilege and secure-by-default applied?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 9. Performance

- **Purpose:** Assess efficiency, navigation, and operational cost.
- **Evaluation Questions:**
  - Is retrieval and navigation efficient?
  - Is complexity kept low?
  - Is operational overhead minimal?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 10. Documentation

- **Purpose:** Assess completeness and clarity of supporting documentation.
- **Evaluation Questions:**
  - Is purpose and usage clearly explained?
  - Is documentation current and accurate?
  - Are examples or contracts provided where useful?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 11. Consistency

- **Purpose:** Assess alignment with established standards and style.
- **Evaluation Questions:**
  - Does it match naming and formatting conventions?
  - Does it match the documentation style?
  - Is it internally consistent?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 12. Repository Compliance

- **Purpose:** Assess adherence to repository structure and process rules.
- **Evaluation Questions:**
  - Is it placed in the correct location?
  - Does it follow branch, commit, and traceability rules?
  - Does it respect declared change scope?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 13. Dependency Management

- **Purpose:** Assess how external dependencies are introduced and controlled.
- **Evaluation Questions:**
  - Are dependencies necessary, vetted, and pinned?
  - Is the dependency surface minimal?
  - Are license and security implications reviewed?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 14. Versioning

- **Purpose:** Assess versioning discipline and traceability.
- **Evaluation Questions:**
  - Is a consistent versioning scheme applied?
  - Is change history recorded?
  - Can any version be traced and reconstructed?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

## 15. Future Expansion

- **Purpose:** Assess readiness for future evolution and automation.
- **Evaluation Questions:**
  - Are extension and override mechanisms defined?
  - Is it easy to automate and integrate?
  - Are future risks anticipated?
- **Score (0-10):**
- **Comments:**
- **Improvement Actions:**

---

# Risk Assessment

| Risk Category      | Identified Risks | Likelihood | Impact |
|--------------------|------------------|------------|--------|
| Technical Risks    |                  |            |        |
| AI Risks           |                  |            |        |
| Maintenance Risks  |                  |            |        |
| Security Risks     |                  |            |        |
| Operational Risks  |                  |            |        |

**Mitigation Plan:**

---

# Quality Gate

The artifact **cannot be approved** unless every threshold below is met:

| Gate             | Threshold | Actual | Pass? |
|------------------|-----------|--------|-------|
| Architecture     | ≥ 9       |        |       |
| Security         | ≥ 9       |        |       |
| Maintainability  | ≥ 9       |        |       |
| AI Compatibility | ≥ 9       |        |       |
| Token Efficiency | ≥ 8       |        |       |
| Overall Score    | ≥ 90      |        |       |

**Gate result:** ☐ All gates passed   ☐ One or more gates failed (approval blocked)

---

# Improvement Plan

| # | Action | Priority | Expected Benefit | Estimated Effort | Responsible | Deadline |
|---|--------|----------|------------------|------------------|-------------|----------|
| 1 |        |          |                  |                  |             |          |
| 2 |        |          |                  |                  |             |          |
| 3 |        |          |                  |                  |             |          |

---

# Final Decision

- [ ] Approved
- [ ] Approved with Changes
- [ ] Needs Revision
- [ ] Rejected

**Justification:**

---

# Lessons Learned

- **What worked well?**
- **What should be improved?**
- **Should this become a repository standard?**

---

# Version History

| Version | Date       | Author | Notes               |
|---------|------------|--------|---------------------|
| 1.0.0   | 2026-06-29 |        | Initial review form |
| 1.0.1   | 2026-06-29 |        | Standardized version history columns to Author / Notes (audit finding A-001) |
