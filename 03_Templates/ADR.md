# Architecture Decision Record (ADR)

> Canonical Architecture Decision Record for the AI Engineering Framework.
> Every significant architectural decision shall be documented using this template.
> Architecture shall evolve through explicit ADRs rather than undocumented changes.
> ADRs are immutable records. New decisions supersede previous ADRs instead of modifying them.

---

# Document Information

| Field         | Value                                         |
| ------------- | --------------------------------------------- |
| ADR ID        |                                               |
| Title         |                                               |
| Project       |                                               |
| Version       |                                               |
| Status        | Proposed / Under Review / Accepted / Implemented / Superseded / Deprecated |
| Author        |                                               |
| Reviewer      |                                               |
| Decision Date |                                               |
| Last Updated  |                                               |

---

# Decision Summary

Provide a concise summary of the architectural decision.

Maximum recommended length:

5–10 sentences.

---

# Context

Describe the problem that requires this decision.

Include:

* Background
* Existing limitations
* Constraints
* Business context
* Technical context

---

# Problem Statement

Clearly define the architectural problem.

Avoid discussing implementation.

---

# Decision

Describe the selected architectural decision.

State exactly what has been decided.

---

# Decision Classification

Classify the decision. Every ADR shall belong to at least one category.

* Business Decision
* Architecture Decision
* Technology Decision
* Security Decision
* AI Decision
* Infrastructure Decision
* Operational Decision

---

# Decision Priority

Indicate the architectural importance of the decision.

* Critical
* High
* Medium
* Low

---

# Decision Lifecycle

The decision follows a standardized lifecycle, consistent with repository governance.

* Proposed
* Under Review
* Accepted
* Implemented
* Superseded
* Deprecated

---

# Decision Ownership

Make architectural ownership explicit.

* Decision Owner
* Technical Owner
* Business Owner

---

# Decision Drivers

List the primary reasons for this decision.

Examples:

* Business Requirements
* Non-Functional Requirements
* Security
* Performance
* Scalability
* Maintainability
* AI Compatibility
* Cost
* Schedule

---

# Alternatives Considered

Document every significant alternative.

| Alternative | Advantages | Disadvantages | Reason Rejected |
| ----------- | ---------- | ------------- | --------------- |
|             |            |               |                 |

Every major alternative should be evaluated.

---

# Decision Criteria

Evaluate the selected decision against explicit criteria.

Examples:

* Cost
* Complexity
* Performance
* Security
* Maintainability
* AI Compatibility
* Operational Impact
* Long-Term Sustainability

---

# Decision Rationale

Explain why the chosen option is preferred.

Include:

* Trade-offs
* Risks accepted
* Benefits gained
* Design philosophy

---

# Trade-off Matrix

Document trade-offs explicitly and measurably.

| Criterion | Selected Option | Trade-off |
| --------- | --------------- | --------- |
|           |                 |           |

---

# Consequences

Describe the expected consequences.

## Positive

*

## Negative

*

## Risks

*

---

# Impact Assessment

Evaluate the impact of this decision.

| Area          | Impact |
| ------------- | ------ |
| Architecture  |        |
| Development   |        |
| Testing       |        |
| Operations    |        |
| Security      |        |
| AI Agents     |        |
| Documentation |        |

For architectural planning, also assess impact over time and risk.

| Area          | Short-term | Long-term | Risk |
| ------------- | ---------- | --------- | ---- |
| Architecture  |            |           |      |
| Development   |            |           |      |
| Operations    |            |           |      |
| Security      |            |           |      |
| AI Agents     |            |           |      |

---

# Dependencies

List dependencies introduced by this decision.

Examples:

* Technologies
* Libraries
* External Services
* Infrastructure
* Other ADRs

Track architectural relationships between decisions so they remain traceable.

| Relationship   | ADR ID |
| -------------- | ------ |
| Depends On ADR |        |
| Blocks ADR     |        |
| Related ADR    |        |

---

# Compliance

Verify compliance with:

* Requirement.md
* Architecture.md
* Global.md
* Repository Rules
* Security Requirements

---

# Traceability

Link this ADR to repository artifacts.

| Artifact     | Reference |
| ------------ | --------- |
| Requirement  |           |
| Architecture |           |
| Review       |           |
| Issue        |           |
| Commit       |           |
| Pull Request |           |

---

# AI Considerations

Describe how this decision affects AI systems.

Include:

* Prompt Strategy
* Context Management
* Tool Usage
* MCP Integration
* Memory Strategy
* Hallucination Risk
* Token Efficiency
* Prompt Compatibility
* Context Size Impact
* Token Cost
* Memory Impact
* AI Maintainability
* Multi-Agent Compatibility

---

# Validation

Describe how this decision will be validated.

Supported methods:

* Architecture Review
* Prototype
* Benchmark
* Test
* Production Validation

---

# Success Criteria

Document measurable criteria indicating the decision is successful.

| Metric | Target | Validation Method |
| ------ | ------ | ----------------- |
|        |        |                   |

---

# Rollback Strategy

Define how this decision can be reversed if necessary.

Include:

* Rollback Trigger
* Rollback Procedure
* Recovery Plan

---

# Review History

| Review | Reviewer | Result | Date |
| ------ | -------- | ------ | ---- |

---

# Superseded By

If replaced, reference the new ADR.

| ADR ID | Reason |
| ------ | ------ |

Leave blank if still active.

---

# Related ADRs

List related architectural decisions.

| ADR ID | Relationship |
| ------ | ------------ |

---

# Open Questions

Document unresolved architectural questions.

| ID | Question | Owner | Status |
| -- | -------- | ----- | ------ |

---

# Change Log

| Version | Date | Author | Summary |
| ------- | ---- | ------ | ------- |

---

# Approval

| Role      | Name | Date | Status |
| --------- | ---- | ---- | ------ |
| Architect |      |      |        |
| Reviewer  |      |      |        |
| Approver  |      |      |        |

---

# Notes

Additional information not covered elsewhere.

---

# ADR Review Checklist

Verify before approval:

- [ ] Is the problem clearly defined?
- [ ] Are alternatives evaluated?
- [ ] Is the rationale justified?
- [ ] Are trade-offs documented?
- [ ] Are requirements referenced?
- [ ] Is the decision traceable?
- [ ] Are risks identified?
- [ ] Is rollback defined?
- [ ] Are AI impacts documented?

---

# Version History

| Version | Date       | Author | Notes                                                                                                                                                                          |
| ------- | ---------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical ADR template                                                                                                                                             |
| 1.1.0   | 2026-06-29 |        | Added Decision Classification, Priority, Lifecycle, Ownership, Criteria, Trade-off Matrix, Success Criteria, Rollback Strategy, ADR Review Checklist; expanded Impact Assessment, Dependencies, and AI Considerations |
