# Versioning Policy

> Canonical versioning policy for the AI Engineering Framework.
> This policy defines how versions are assigned, managed, and evolved across the repository.
> All repository artifacts shall follow this policy unless explicitly overridden by repository governance.

---

# Purpose

Define a consistent versioning strategy for all repository artifacts.

Objectives:

* Ensure traceability.
* Prevent version ambiguity.
* Support long-term maintenance.
* Enable AI-assisted version management.
* Maintain backward compatibility whenever practical.

---

# Scope

This policy applies to:

* Documentation
* Templates
* Prompts
* Architecture
* ADRs
* Source Code
* Configuration
* AI Agents
* MCP Servers
* Project Templates

---

# Artifact Lifecycle

Define the lifecycle of repository artifacts. Version progression shall be consistent with the artifact lifecycle.

* Draft
* Review
* Approved
* Released
* Deprecated
* Archived

---

# Version Format

Use Semantic Versioning.

```
MAJOR.MINOR.PATCH
```

Examples:

```
1.0.0
1.1.0
1.2.3
2.0.0
```

Leading zeros are not permitted.

---

# Version Definitions

## Major

Increment when:

* Breaking changes are introduced.
* Repository structure changes.
* Architecture changes are incompatible.
* Existing artifacts require migration.

---

## Minor

Increment when:

* New capabilities are added.
* New sections are introduced.
* Existing behavior remains compatible.

---

## Patch

Increment when:

* Documentation corrections.
* Typographical fixes.
* Clarifications.
* Minor improvements.
* No functional change.

---

# Version Compatibility

Artifacts should remain backward compatible whenever practical.

Breaking changes require:

* Major version increment.
* Migration guidance.
* Updated documentation.
* Review approval.

---

# Version Ownership

Each artifact shall define:

* Current Version
* Author
* Reviewer
* Approval Date

Version ownership must be traceable.

---

# Version Governance

Make version ownership explicit by defining responsibility.

* Who may create versions.
* Who may approve versions.
* Who may release versions.

Authorized roles:

* Version Author — creates versions.
* Version Reviewer — reviews versions.
* Version Approver — approves versions.
* Release Authority — authorizes releases.

---

# Version History

Every artifact shall maintain:

| Version | Date | Author | Summary |
| ------- | ---- | ------ | ------- |

Version history shall never be deleted.

---

# Change Classification

Classify every change.

| Type                      | Version Increment |
| ------------------------- | ----------------- |
| Breaking Change           | Major             |
| New Feature               | Minor             |
| Documentation Improvement | Patch             |
| Bug Fix                   | Patch             |
| Refactoring (Compatible)  | Patch             |
| Refactoring (Breaking)    | Major             |

---

# Release Policy

Every released version shall:

* Pass technical review.
* Pass Quality Gate.
* Be approved.
* Be traceable.
* Be committed to version control.

---

# Release Types

Classify each release.

* Development Release
* Internal Release
* Public Release
* Hotfix Release
* Long-Term Support (LTS)

---

# Review Requirements

A version increment shall not occur unless:

* Review completed.
* Review Report approved.
* Quality Gate passed.
* Repository compliance verified.

---

# Version Naming

Use the following format.

```
<Artifact Name> v<Major>.<Minor>.<Patch>
```

Example:

```
Architecture v1.2.0
Review Prompt v1.1.0
Requirement v2.0.0
```

---

# Pre-release Versions

Pre-release identifiers denote versions that are not yet final.

Supported identifiers: Alpha, Beta, RC (Release Candidate).

Use each stage as follows:

* Alpha — early, unstable, feature-incomplete.
* Beta — feature-complete, undergoing validation.
* RC — release candidate, expected final unless defects are found.

Examples:

```
2.0.0-alpha.1
2.0.0-beta.2
2.0.0-rc.1
```

---

# Build Metadata

Build metadata may be appended after a plus sign.

Example:

```text
1.4.0+build.125
```

Build metadata shall not affect semantic version precedence.

---

# Deprecation Policy

Deprecated versions:

* Shall remain accessible.
* Shall not receive new features.
* May receive critical fixes only.
* Shall reference the replacement version.

---

# Rollback Policy

Rollback restores a previously released version when a release proves defective.

* Rollback Conditions — allowed only when a release fails Quality Gate or causes critical regressions.
* Rollback Approval — requires explicit approval from the Release Authority.
* Version Number Handling — rollback does not decrement version numbers; a new version (typically a hotfix) records the reversal.
* Traceability Requirements — rollback shall remain fully traceable.

Released versions shall never be deleted.

---

# AI Requirements

AI systems shall:

* Never invent version numbers.
* Never skip version increments.
* Never overwrite version history.
* Preserve backward compatibility whenever practical.
* Recommend the correct increment based on the change classification.
* Never downgrade versions automatically.
* Never reuse retired version numbers.
* Never modify released version history.
* Never skip mandatory review before recommending a release.

---

# Repository-wide Version Consistency

Maintain consistent version relationships across documents.

* Architecture version shall reference Requirement version.
* ADR shall reference Architecture version.
* Review Report shall reference reviewed artifact version.
* Project releases shall reference repository versions.

Cross-document version consistency shall be maintained.

| Artifact      | Depends On                |
| ------------- | ------------------------- |
| Requirement   | Repository Version        |
| Architecture  | Requirement Version       |
| ADR           | Architecture Version      |
| Review Report | Reviewed Artifact Version |
| Project       | Repository Release        |

---

# Version Traceability

Every released version shall be fully traceable.

| Artifact         | Reference |
| ---------------- | --------- |
| Requirement ID   |           |
| Architecture ID  |           |
| ADR ID           |           |
| Review Report ID |           |
| Commit ID        |           |
| Pull Request     |           |
| Release Tag      |           |

Every released version shall be reconstructable.

---

# Compatibility Matrix

Explicitly manage expected compatibility relationships between repository artifacts.

| Artifact     | Compatible With | Notes |
| ------------ | --------------- | ----- |
| Requirement  | Architecture    |       |
| Architecture | ADR             |       |
| Templates    | Projects        |       |
| Prompts      | Projects        |       |

---

# Compliance

This policy shall remain consistent with:

* Repository Governance
* Global Rules
* Review Standards
* Release Policy

---

# Exceptions

Any exception requires:

* Explicit approval.
* Documented justification.
* Traceable decision.

---

# Version Review Checklist

Verify before approval:

- [ ] Correct semantic version increment
- [ ] Change classification verified
- [ ] Backward compatibility evaluated
- [ ] Migration guidance provided (if required)
- [ ] Review completed
- [ ] Quality Gate passed
- [ ] Traceability verified
- [ ] Release approved

---

# Practical Examples

Representative scenarios demonstrating correct application of this policy.

* Patch documentation update: fix a typo or clarify wording → `1.2.0` → `1.2.1`.
* Minor feature addition: add a new section while preserving existing content → `1.2.1` → `1.3.0`.
* Major breaking change: remove or restructure content requiring migration → `1.3.0` → `2.0.0` with migration guidance.
* Hotfix release: critical fix on a released version → `2.0.0` → `2.0.1` (Hotfix Release).
* LTS release: a stable version designated for long-term support and critical fixes only → `2.0.0` (Long-Term Support).

---

# Approval

| Role     | Name | Date | Status |
| -------- | ---- | ---- | ------ |
| Author   |      |      |        |
| Reviewer |      |      |        |
| Approver |      |      |        |

---

# Version History

| Version | Date       | Author | Notes                                                                                                                                                                                                                  |
| ------- | ---------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical versioning policy                                                                                                                                                                                  |
| 1.1.0   | 2026-06-29 |        | Added Artifact Lifecycle, Version Governance, Release Types, Pre-release Versions, Build Metadata, Rollback Policy, Repository-wide Version Consistency, Version Traceability, Compatibility Matrix, Version Review Checklist, Practical Examples; expanded AI Requirements |
