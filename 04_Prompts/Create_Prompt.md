# Create Prompt

> Canonical implementation prompt for designing a new repository artifact.
> This prompt defines the mandatory engineering requirements for implementing a single artifact within the AI Engineering Framework.
> The implementation agent shall integrate the artifact into the existing framework without redesigning approved components.

---

# Objective

Implement exactly ONE repository artifact.

The artifact shall integrate into the existing repository architecture without redesigning approved components.

The implementation shall prioritize:

* Repository consistency
* Engineering quality
* Maintainability
* AI compatibility
* Traceability
* Deterministic output

---

# Repository Context

| Field             | Value                          |
| ----------------- | ------------------------------ |
| Repository        | AI Engineering Framework       |
| Repository Status | Foundation and Templates ready |
| Architecture      | Stable                         |

Approved artifacts may only receive patch-level corrections unless explicitly instructed otherwise, in accordance with the Versioning Policy.

---

# Current Task

| Field             | Value                                                         |
| ----------------- | ------------------------------------------------------------- |
| Artifact Name     |                                                               |
| Artifact Category | Rule / Policy / Template / Prompt / Project / Tool / Document |
| Repository Path   |                                                               |
| Target Version    |                                                               |
| Artifact Status   | Draft                                                         |

---

# Existing Repository Context

Before implementation, identify all existing repository artifacts related to this artifact.

At minimum, consider:

* Global Rules
* Naming Policy
* Versioning Policy
* Repository Governance (if available)
* Requirement
* Architecture
* ADR
* Review Form
* Review Report
* Artifact Revision Request

The implementation SHALL integrate with these artifacts.

The implementation SHALL NOT duplicate their responsibilities.

---

# Purpose

Clearly define:

* Why this artifact exists.
* What repository problem it solves.
* What responsibility it owns.
* Why this responsibility belongs exclusively to this artifact.

---

# Repository Integration

Describe how this artifact interacts with other repository artifacts.

Identify:

* Inputs
* Outputs
* Dependencies
* Relationships
* Required references
* Workflow position

Avoid duplicated responsibilities.

---

# Scope Definition

## In Scope

List every responsibility owned by this artifact.

## Out of Scope

List everything intentionally excluded.

Out-of-scope responsibilities shall remain owned by other artifacts.

---

# Design Requirements

The artifact shall:

* be modular
* be deterministic
* be maintainable
* be reviewable
* be traceable
* be AI-friendly
* minimize ambiguity
* minimize duplicated information
* use clear Markdown hierarchy
* remain suitable for long-term repository evolution

---

# Repository Constraints

The implementation SHALL NOT:

* redesign repository architecture
* modify approved artifacts beyond approved patch-level corrections
* invent repository rules
* invent engineering requirements
* duplicate existing responsibilities
* merge unrelated concepts
* change repository workflow
* remove approved terminology
* introduce undocumented assumptions

---

# Decision Rules

When implementation decisions are required and explicit guidance is unavailable, the implementation agent SHALL apply the following rules in the listed order.

## Rule 1 — Preserve Repository Architecture

Repository architecture takes precedence over implementation convenience.

The implementation SHALL NOT redesign, restructure, or reinterpret the approved repository architecture.

## Rule 2 — Preserve Approved Artifacts

Approved artifacts SHALL be treated as authoritative.

Do not modify, replace, reinterpret, or duplicate approved artifacts beyond approved patch-level corrections unless explicitly instructed.

## Rule 3 — Follow Repository Governance

When multiple repository artifacts appear applicable, follow the precedence defined by Repository Governance.

If Repository Governance is unavailable, preserve existing repository behavior and report the ambiguity instead of making assumptions.

## Rule 4 — Preserve Ownership

Each repository artifact owns a specific responsibility.

Do not transfer, duplicate, merge, or redefine responsibilities between artifacts.

## Rule 5 — Preserve Terminology

Approved repository terminology SHALL remain unchanged.

Do not:

* rename approved concepts
* introduce alternative terminology
* replace existing identifiers
* create synonyms for approved repository terms

Terminology consistency takes precedence over stylistic preference.

## Rule 6 — Minimize Assumptions

The implementation SHALL NOT invent:

* repository rules
* engineering requirements
* architectural decisions
* workflow changes
* undocumented relationships

If required information is unavailable, explicitly report the missing information.

## Rule 7 — Resolve Ambiguity Conservatively

When multiple valid interpretations exist, select the interpretation that introduces the fewest repository changes.

If no safe interpretation exists, stop and report the ambiguity.

## Rule 8 — Preserve Traceability

Do not remove or invalidate:

* identifiers
* references
* version history
* repository relationships
* review history

Traceability shall remain reconstructable after implementation.

## Rule 9 — Preserve Determinism

Equivalent inputs SHALL produce equivalent outputs.

Avoid:

* inconsistent wording
* unnecessary variation
* subjective interpretation
* hidden assumptions

## Rule 10 — Prefer Explicitness

When choosing between:

* concise vs explicit
* implicit vs documented
* inferred vs referenced

prefer the documented and explicitly traceable solution.

---

# Decision Priority

If multiple rules appear applicable, apply them in the following order:

1. Repository Architecture
2. Repository Governance
3. Approved Artifacts
4. Traceability
5. Responsibility Ownership
6. Repository Policies
7. Terminology Consistency
8. Deterministic Behavior
9. Documentation Quality
10. Implementation Convenience

Lower-priority rules shall never override higher-priority rules.

---

# Conflict Handling

If compliance with one rule prevents compliance with another:

1. Apply the higher-priority rule.
2. Preserve repository integrity.
3. Do not invent a compromise.
4. Report the conflict explicitly.
5. Await further instruction if the conflict cannot be resolved safely.

---

# Decision Process

Before making any implementation decision, the implementation agent SHALL evaluate the following questions in order.

## Step 1 — Repository Consistency

Does the decision preserve the existing repository architecture? If not, stop and report the conflict.

## Step 2 — Responsibility Ownership

Does another approved artifact already own this responsibility? If yes, do not duplicate it.

## Step 3 — Governance

Is there an applicable repository policy or governance rule? If yes, follow it.

## Step 4 — Traceability

Can the decision remain fully traceable? If not, do not implement it.

## Step 5 — Versioning

Does the decision require a version change? If yes, follow the Versioning Policy.

## Step 6 — Documentation

Does the decision reduce documentation quality? If yes, reject the decision.

## Step 7 — AI Compatibility

Does the decision improve deterministic behavior? If multiple valid solutions exist, prefer the most deterministic one.

## Step 8 — Repository Impact

Will the decision affect other artifacts? If yes, document every dependency.

## Step 9 — Validation

Can the completed artifact pass Self Validation? If not, revise the implementation before producing output.

## Step 10 — Completion

Produce the artifact only after every previous step has been satisfied.

---

# Required Deliverable

Produce ONE complete repository-ready Markdown artifact.

Do NOT produce:

* review reports
* approval reports
* revision requests
* implementation guides
* explanations
* commentary

unless explicitly requested.

---

# Self Validation

Before presenting the artifact, verify:

## Repository

- [ ] Repository architecture preserved.
- [ ] Repository terminology consistent.
- [ ] Repository workflow respected.

## Architecture

- [ ] Responsibilities are unique.
- [ ] No architectural conflicts exist.
- [ ] No duplicated ownership exists.

## Documentation

- [ ] Markdown structure is consistent.
- [ ] Required sections are complete.
- [ ] Terminology is internally consistent.

## Traceability

- [ ] Required references are present.
- [ ] Dependencies are documented.
- [ ] Relationships are explicit.

## AI Compatibility

- [ ] Output is deterministic.
- [ ] Headings are parse-friendly.
- [ ] Context switching is minimized.
- [ ] Redundant wording is minimized.

If any validation fails, correct the artifact before producing the final output.

---

# Quality Target

The artifact shall be reviewed using the AI Engineering Framework Review Standard defined in `Review_Form.md`.

The implementation should satisfy the canonical Quality Gate.

| Category         | Target |
| ---------------- | ------ |
| Architecture     | ≥ 9    |
| Security         | ≥ 9    |
| Maintainability  | ≥ 9    |
| AI Compatibility | ≥ 9    |
| Token Efficiency | ≥ 8    |
| Overall Score    | ≥ 90   |

---

# Completion Rule

The implementation is complete only when:

* Every required section exists.
* No duplicated responsibility exists.
* Repository consistency is preserved.
* Traceability is complete.
* Self validation passes.
* The artifact is ready for technical review without additional assumptions.

---

# Version Compatibility

Future revisions of this prompt should remain backward compatible whenever practical.

Breaking changes require an explicit version increment.

---

# Version History

| Version | Date       | Notes                          |
| ------- | ---------- | ------------------------------ |
| 1.0.0   | 2026-06-29 | Initial canonical create prompt |
| 1.1.0   | 2026-06-29 | Added Decision Rules, Decision Priority, Conflict Handling, and Decision Process |
