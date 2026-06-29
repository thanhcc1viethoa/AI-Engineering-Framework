# Requirement

> Canonical requirements specification for the AI Engineering Framework.
> Every project shall define its requirements using this template before architecture, implementation, or AI-assisted development begins.
> This document is the single source of truth for project requirements.

---

# Document Information

| Field          | Value                                  |
| -------------- | -------------------------------------- |
| Project Name   |                                        |
| Requirement ID |                                        |
| Version        |                                        |
| Status         | Draft / Review / Approved / Deprecated |
| Author         |                                        |
| Owner          |                                        |
| Reviewer       |                                        |
| Created Date   |                                        |
| Last Updated   |                                        |

---

# Purpose

Describe the business objective of the project.

Include:

* Why the project exists.
* Expected outcomes.
* Business value.
* Success criteria.

---

# Background

Describe the context that led to this project.

Include:

* Existing problems.
* Current workflow.
* Existing limitations.
* Motivation.

---

# Scope

## In Scope

List all functionality included in this project.

---

## Out of Scope

Explicitly list what is excluded.

Anything not listed in **In Scope** should be considered outside the project.

---

# Requirement Classification

Classify every requirement into one of the following categories to improve organization, traceability, and AI retrieval.

* Business Requirements
* Functional Requirements
* Non-Functional Requirements
* Technical Requirements
* Compliance Requirements
* Operational Requirements
* AI Requirements

---

# Requirement Lifecycle

Every requirement follows a standardized lifecycle. These statuses are reusable across all projects.

* Draft
* Proposed
* Approved
* Implemented
* Verified
* Deprecated

---

# Priority Model

Apply this priority model consistently to every requirement throughout the document.

* Critical
* High
* Medium
* Low
* Optional

---

# Stakeholders

| Role          | Name | Responsibility |
| ------------- | ---- | -------------- |
| Sponsor       |      |                |
| Product Owner |      |                |
| Architect     |      |                |
| Developer     |      |                |
| Reviewer      |      |                |
| End User      |      |                |

---

# Functional Requirements

List every functional requirement.

| ID     | Requirement | Category | Priority                                   | Owner | Source | Status |
| ------ | ----------- | -------- | ------------------------------------------ | ----- | ------ | ------ |
| FR-001 |             |          | Critical / High / Medium / Low / Optional |       |        |        |

Rules:

* One requirement per row.
* Atomic.
* Testable.
* Unambiguous.

Source examples: User Request, Business Requirement, ADR, Regulation, Issue, Contract.

---

# Non-Functional Requirements

Examples:

* Performance
* Reliability
* Security
* Scalability
* Availability
* Maintainability
* Portability
* Accessibility

| ID      | Requirement | Target |
| ------- | ----------- | ------ |
| NFR-001 |             |        |

---

# Requirement Rationale

Document why each requirement exists so intent is clear to humans and AI, not only its implementation.

| ID     | Business Value | Reason | Expected Impact |
| ------ | -------------- | ------ | --------------- |
| FR-001 |                |        |                 |

---

# Requirement Dependencies

Track relationships between requirements so they remain traceable.

| ID     | Depends On | Blocks | Related Requirements |
| ------ | ---------- | ------ | -------------------- |
| FR-001 |            |        |                      |

---

# Requirement Validation

Define how each requirement will be objectively verified.

Supported validation methods:

* Review
* Inspection
* Test
* Demonstration
* Analysis

| ID     | Validation Method | Verified |
| ------ | ----------------- | -------- |
| FR-001 |                   |          |

---

# Business Rules

Document all mandatory business constraints.

Examples:

* Validation rules
* Approval rules
* Naming conventions
* Compliance requirements

---

# Assumptions

Document assumptions made during planning.

Every assumption should be validated later. Assumptions must not remain permanently unverified.

| ID     | Assumption | Validation Status | Validation Method | Validation Date | Reviewer |
| ------ | ---------- | ----------------- | ----------------- | --------------- | -------- |
| AS-001 |            |                   |                   |                 |          |

---

# Constraints

Document known constraints.

Examples:

* Budget
* Timeline
* Technology
* Platform
* Team
* Regulations

---

# Dependencies

List dependencies.

Examples:

* External APIs
* Third-party libraries
* Internal systems
* Infrastructure
* Vendor services

---

# Risks

| ID    | Risk | Likelihood | Impact | Mitigation |
| ----- | ---- | ---------- | ------ | ---------- |
| R-001 |      |            |        |            |

---

# Acceptance Criteria

Define measurable completion criteria.

Each criterion should be verifiable.

| ID     | Acceptance Criterion | Validation Method |
| ------ | -------------------- | ----------------- |
| AC-001 |                      |                   |

---

# Success Metrics

Define measurable project success indicators.

Examples:

* Performance targets
* Accuracy
* Cost reduction
* Time savings
* User satisfaction

| ID     | Metric | Target | Measurement Method | Frequency |
| ------ | ------ | ------ | ------------------ | --------- |
| SM-001 |        |        |                    |           |

---

# AI Context

Provide the context AI agents need to act consistently and reduce hallucinations.

| Field               | Value |
| ------------------- | ----- |
| Relevant Documents  |       |
| Prompt Dependencies |       |
| Repository Rules    |       |
| Known Constraints   |       |
| Expected Outputs    |       |
| Context Priority    |       |

---

# Traceability

Reference related repository artifacts.

| Artifact     | Reference |
| ------------ | --------- |
| ADR          |           |
| Architecture |           |
| Review       |           |
| Issue        |           |
| Commit       |           |

## Requirement Traceability Matrix (RTM)

The RTM is the primary traceability mechanism for the repository. Link every requirement to its related artifacts.

| Requirement ID | Parent Requirement | Architecture | ADR | Review | Test | Issue | Commit |
| -------------- | ------------------ | ------------ | --- | ------ | ---- | ----- | ------ |
| FR-001         |                    |              |     |        |      |       |        |

---

# Change Log

| Version | Date | Author | Summary |
| ------- | ---- | ------ | ------- |

---

# Requirement Change Control

All requirement changes must be controlled and traceable.

| CR ID  | Requirement ID | Description | Reason | Impact Analysis | Approval | Version |
| ------ | -------------- | ----------- | ------ | --------------- | -------- | ------- |
| CR-001 |                |             |        |                 |          |         |

---

# Approval

| Role     | Name | Date | Approval Date | Status |
| -------- | ---- | ---- | ------------- | ------ |
| Author   |      |      |               |        |
| Reviewer |      |      |               |        |
| Approver |      |      |               |        |

---

# Notes

Additional information not covered elsewhere.

---

# Version History

| Version | Date       | Author | Notes                                                                                                                                                                                       |
| ------- | ---------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical requirement template                                                                                                                                                     |
| 1.1.0   | 2026-06-29 |        | Added Requirement Classification, Lifecycle, Priority Model, Ownership/Source, Rationale, Dependencies, Validation, RTM, Change Control, AI Context; structured Success Metrics and Assumption Validation |
| 1.1.1   | 2026-06-29 |        | Added Category (FR), Requirement ID (Change Control), Parent Requirement (RTM), Validation Method (Acceptance Criteria), Approval Date (Approval), and Author (Version History) columns      |
