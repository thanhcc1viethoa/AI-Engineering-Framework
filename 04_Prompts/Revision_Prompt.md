# Revision Prompt

> Canonical implementation prompt for revising an approved repository artifact.
> This prompt defines how an implementation agent shall apply an approved Artifact Revision Request.
> The implementation agent shall preserve repository integrity while implementing only the requested changes.

---

# Objective

Revise exactly ONE approved repository artifact.

The revision SHALL implement only the approved changes.

The revision SHALL preserve repository consistency.

---

# Inputs

The implementation agent SHALL receive:

* Original Artifact
* Artifact Revision Request
* Review Report
* Repository Context
* Related Repository Policies (if applicable)

Do not proceed if any mandatory input is missing.

---

# Revision Scope

The implementation SHALL modify ONLY the sections listed under In Scope in the Artifact Revision Request.

Everything listed under Out of Scope shall remain unchanged.

If the requested revision conflicts with the approved scope, stop and report the conflict instead of making assumptions.

---

# Revision Strategy

Follow the implementation strategy specified in the Artifact Revision Request.

If no strategy is specified, use Patch.

The implementation SHALL NOT change the selected strategy without explicit approval.

Apply only the selected strategy, using the corresponding implementation rules below.

## Patch

Apply minimal changes that preserve the existing implementation.

* Modify only the approved In Scope sections.
* Do not restructure existing content.
* Increment the patch version per the Versioning Policy.

## Merge

Integrate approved improvements while preserving every approved section.

* Preserve all approved content and section order whenever practical.
* Insert or extend sections only; do not perform a full rewrite.
* Never downgrade the version.
* If new content conflicts with approved content, preserve the approved content and report the conflict.
* Increment the minor version when new sections or capabilities are added.

## Refactor

Improve internal structure without changing responsibilities or external behavior.

* Preserve every responsibility, identifier, and external reference.
* Do not alter approved terminology.
* Increment the patch version for a compatible refactor, or the major version for a breaking refactor, per the Versioning Policy.

## Replace

Replace an approved section with a newly approved implementation.

* Permitted only with explicit architectural approval.
* Preserve version history; never delete prior versions.
* Increment the version per the Versioning Policy.

---

# Responsibilities

The implementation SHALL:

* implement every approved requested change
* preserve repository architecture
* preserve traceability
* preserve existing identifiers
* preserve approved terminology
* preserve Markdown structure
* preserve repository workflow
* preserve version history

---

# Prohibited Actions

The implementation SHALL NOT:

* redesign architecture
* modify unrelated sections
* remove approved content
* invent repository rules
* invent new requirements
* rename repository artifacts
* change repository structure
* introduce undocumented changes
* perform speculative improvements

---

# Versioning

Follow the repository Versioning Policy.

Update the version only when required.

Version increments shall match the approved revision type.

---

# Traceability

Maintain all existing references.

Update only the references affected by the approved revision.

Do not remove historical traceability.

---

# Decision Rules

When revision decisions are required and explicit guidance is unavailable, the implementation agent SHALL apply the following rules in the listed order.

## Rule 1 — Preserve Approved Scope

The approved Revision Scope takes precedence over implementation convenience.

Do not modify any section outside the approved In Scope definition.

## Rule 2 — Preserve Repository Architecture

Do not redesign, restructure, reinterpret, or extend the approved repository architecture.

## Rule 3 — Preserve Approved Content

Approved content SHALL remain authoritative.

Do not rewrite approved content unless explicitly required by the approved revision request.

## Rule 4 — Preserve Traceability

Every approved reference, identifier, relationship, and historical record SHALL remain reconstructable after revision.

## Rule 5 — Preserve Terminology

Do not rename approved repository concepts.

Do not introduce alternative terminology.

Maintain terminology consistency throughout the artifact.

## Rule 6 — Minimize Assumptions

Do not invent:

* repository rules
* engineering requirements
* review findings
* revision scope
* implementation intent

If required information is missing, stop and report the missing information.

## Rule 7 — Resolve Ambiguity Conservatively

When multiple valid revisions are possible, implement the revision that produces the smallest repository impact.

If ambiguity cannot be resolved safely, stop and report the conflict.

## Rule 8 — Preserve Determinism

Equivalent inputs SHALL produce equivalent revised artifacts.

Avoid subjective interpretation.

## Rule 9 — Preserve Repository Consistency

Every revision shall remain consistent with:

* Global Rules
* Naming Policy
* Versioning Policy
* Repository Governance
* Related Approved Artifacts

## Rule 10 — Prefer Minimal Change

Implement the minimum change required to satisfy the approved revision request.

Avoid opportunistic improvements.

---

# Decision Priority

Apply decisions in the following order.

1. Approved Revision Scope
2. Repository Architecture
3. Repository Governance
4. Approved Repository Artifacts
5. Traceability
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
4. Report the conflict.
5. Await further instruction if necessary.

---

# Decision Process

Before implementing a revision, evaluate the following sequence.

## Step 1 — Approved Scope

Verify the approved Revision Scope.

## Step 2 — Repository Architecture

Verify the repository architecture remains unchanged.

## Step 3 — Content Ownership

Verify approved content ownership.

## Step 4 — Traceability

Verify traceability.

## Step 5 — Versioning

Verify versioning impact.

## Step 6 — Terminology

Verify terminology consistency.

## Step 7 — Repository Impact

Verify repository dependencies.

## Step 8 — Implementation

Implement only approved changes.

## Step 9 — Validation

Execute Self Validation.

## Step 10 — Completion

Produce the updated artifact only after every previous step succeeds.

---

# Required Deliverables

Produce only:

1. Updated Artifact
2. Updated Version History
3. Summary of Changes
4. Modified Sections
5. Updated Traceability (if applicable)

Do not produce additional repository artifacts.

---

# Self Validation

Before presenting the updated artifact, verify:

## Scope

- [ ] Every approved revision implemented.
- [ ] No unapproved modification introduced.

## Repository

- [ ] Repository architecture preserved.
- [ ] Repository terminology preserved.
- [ ] Repository workflow unchanged.

## Traceability

- [ ] References remain valid.
- [ ] Existing identifiers preserved.
- [ ] Version history updated correctly.

## Documentation

- [ ] Markdown formatting preserved.
- [ ] Section order preserved.
- [ ] Heading hierarchy preserved.

## Quality

- [ ] No duplicated content introduced.
- [ ] No obsolete content left behind.
- [ ] No new review findings introduced.

If any validation fails, correct the artifact before producing the final result.

---

# Completion Rule

The revision is complete only when:

* Every approved change has been implemented.
* No unrelated content has been modified.
* Repository consistency has been preserved.
* Self Validation passes successfully.

---

# Version Compatibility

Future revisions of this prompt should remain backward compatible whenever practical.

Breaking changes require an explicit version increment.

---

# Version History

| Version | Date       | Notes                            |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-06-29 | Initial canonical revision prompt |
| 1.1.0   | 2026-06-29 | Added Decision Rules, Decision Priority, Conflict Handling, and Decision Process |
| 1.2.0   | 2026-06-29 | Added Revision Strategy section supporting Patch / Merge / Refactor / Replace, absorbing the merge implementation guidance |
