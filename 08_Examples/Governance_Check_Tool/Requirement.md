# Requirement

> Worked example for `08_Examples/`, produced with `/create Requirement "Governance Check Tool"`.
> Demonstrates `03_Templates/Requirement.md` filled for a small, real repository artifact: `06_Tools/governance-check.js`.
> This is illustrative documentation, not a governed project artifact; see Notes.

---

# Document Information

| Field          | Value                                   |
| -------------- | ---------------------------------------- |
| Project Name   | Governance Check Tool                    |
| Requirement ID | REQ-EX-001                               |
| Version        | 1.1.0                                    |
| Status         | Draft                                    |
| Author         | AI Engineering Framework (worked example) |
| Owner          | Repository Owner                         |
| Reviewer       |                                           |
| Created Date   | 2026-07-04                                |
| Last Updated   | 2026-07-04                                |

---

# Purpose

Mechanically enforce a small subset of rules that already exist in `01_Rules/Global.md` and `02_Policies/*.md`, which were previously enforced only through human/AI review discipline.

* Why: `Repository_Roadmap.md` and `Repository_Audit_Report.md` note the repository has no tooling backstop for its own rules.
* Expected outcome: a script that fails fast (non-zero exit) when a tracked file violates an already-written rule.
* Business value: reduces the chance that a known class of violation (e.g. committed dependency directories) reaches `main` undetected.
* Success criteria: see Acceptance Criteria.

---

# Background

Before this requirement, `06_Tools/` contained only a `.gitkeep` file. Every rule in `Global.md` and `Naming_Policy.md` was enforced solely by manual review. `05_Projects/ChatGptInExcel` shows this gap in practice: its `Project_Bootstrap.md` records committed `node_modules/` and a committed `server.log` as open governance gaps (G-006) that manual review had not yet caught.

---

# Scope

## In Scope

* Scan git-tracked files for reserved/generic document names (`Naming_Policy.md`).
* Flag tracked paths inside dependency/build directories (`Global.md` Repository Hygiene).
* Flag `Version History` entries using a version number with a leading zero (`Versioning_Policy.md`).
* Expose the check as `npm run governance:check` and run it in CI.

## Out of Scope

* Automating the full Definition of Done (requires human judgment: acceptance criteria met, human sign-off).
* Secret scanning.
* Any check not already defined as a rule elsewhere in the repository.

Anything not listed in **In Scope** is outside this requirement.

---

# Requirement Classification

* Operational Requirements
* AI Requirements

---

# Requirement Lifecycle

Draft (current stage for this worked example).

---

# Priority Model

Critical / High / Medium / Low / Optional, applied below.

---

# Stakeholders

| Role          | Name                | Responsibility                       |
| ------------- | ------------------- | ------------------------------------- |
| Sponsor       | Repository Owner     | Owns repository governance            |
| Product Owner | Repository Owner     | Prioritizes tooling backlog           |
| Architect     | —                    | Not required for this scope           |
| Developer     | Implementation Agent | Implements and maintains the script  |
| Reviewer      | —                    | Reviews this requirement              |
| End User      | Repository Owner     | Runs the check locally and in CI      |

---

# Functional Requirements

| ID     | Requirement                                                                                  | Category                | Priority | Owner            | Source              | Status      |
| ------ | --------------------------------------------------------------------------------------------- | ------------------------ | -------- | ----------------- | -------------------- | ----------- |
| FR-001 | The tool shall list all git-tracked files and report any whose name matches a reserved name.   | Operational Requirements | High     | Repository Owner | Naming_Policy.md     | Implemented |
| FR-002 | The tool shall flag any tracked path inside a dependency/build directory (e.g. `node_modules`). | Operational Requirements | Critical | Repository Owner | Global.md            | Implemented |
| FR-003 | The tool shall flag `Version History` entries whose version number has a leading zero.         | Operational Requirements | Medium   | Repository Owner | Versioning_Policy.md | Implemented |
| FR-004 | The tool shall exit with a non-zero status when any violation is found.                        | AI Requirements           | High     | Repository Owner | Global.md            | Implemented |

Rules: one requirement per row, atomic, testable, unambiguous.

---

# Non-Functional Requirements

| ID      | Requirement                                                  | Target                              | Validation Method                     |
| ------- | ------------------------------------------------------------- | ------------------------------------ | -------------------------------------- |
| NFR-001 | Runtime dependency footprint                                   | Zero third-party npm packages        | Inspection of `package.json` and imports |
| NFR-002 | Execution time on this repository's current tracked file count | Completes in under 5 seconds         | Test — measured via CI job duration     |
| NFR-003 | Behavior when git input is unavailable or malformed            | Fails gracefully: one clear error line, no stack trace, exit code 2 | Test — run with an invalid `GIT_DIR`    |

---

# Requirement Rationale

| ID     | Business Value                    | Reason                                             | Expected Impact                       |
| ------ | ---------------------------------- | --------------------------------------------------- | -------------------------------------- |
| FR-001 | Prevents reserved-name artifacts    | Naming_Policy.md already forbids these names        | Fewer naming violations reach `main`   |
| FR-002 | Prevents committed build artifacts | Global.md already forbids committing generated output | Repeats of the ChatGptInExcel G-006 gap are caught before merge |
| FR-003 | Prevents malformed version numbers | Versioning_Policy.md already forbids leading zeros  | Cleaner, parseable version history     |
| FR-004 | Enables CI enforcement             | A passive report without a failing exit code cannot block a merge | CI can gate on the result |

---

# Requirement Dependencies

| ID     | Depends On | Blocks | Related Requirements |
| ------ | ---------- | ------ | --------------------- |
| FR-004 | FR-001, FR-002, FR-003 |        |                        |

---

# Requirement Validation

| ID     | Validation Method | Verified |
| ------ | ------------------ | -------- |
| FR-001 | Test               | Yes — see `Requirement_Review_Report.md` Evidence Summary |
| FR-002 | Test               | Yes |
| FR-003 | Test               | Yes |
| FR-004 | Test               | Yes |
| NFR-003 | Test              | Yes — invalid `GIT_DIR` run, see RR-EX-002 Evidence Summary |

---

# Business Rules

* The tool must be read-only; it shall never modify repository files.
* The tool must only check rules that already exist in an approved repository artifact; it shall not invent new policy.

---

# Assumptions

| ID     | Assumption                                     | Validation Status | Validation Method | Validation Date | Reviewer |
| ------ | ----------------------------------------------- | ------------------ | ------------------ | ---------------- | -------- |
| AS-001 | `git` is available in the execution environment | Validated           | Test                | 2026-07-04        |          |

---

# Constraints

* Must run on Node.js 20+ using only built-in modules (no `npm install` step).
* Must run in GitHub Actions `ubuntu-latest` without additional network access.

---

# Dependencies

* Node.js 20+ (built-in `fs`, `path`, `child_process` only).
* Git CLI (`git ls-files`).

---

# Architecture Overview

The tool is a single script with four internal components, executed in sequence:

| Component            | Responsibility                                                     |
| --------------------- | --------------------------------------------------------------------- |
| Tracked-file lister   | Obtains the authoritative file list via `git ls-files`; on failure, exits gracefully per NFR-003 |
| Rule checkers         | One independent function per enforced rule (reserved names / dependency paths, generic document names, version-format) |
| Reporter              | Aggregates violations into an itemized, rule-cited list               |
| Exit-code contract    | `0` = clean, `1` = violations found, `2` = tool could not run          |

New rules are added as new checker functions; no existing checker is modified. This section documents the existing structure and is intentionally proportionate to the tool's size — a separate `Architecture.md` remains unwarranted (see Notes).

---

# Risks

| ID    | Risk                                                            | Likelihood | Impact | Mitigation                                                        |
| ----- | ----------------------------------------------------------------- | ---------- | ------ | -------------------------------------------------------------------- |
| R-001 | Mechanical checks only cover a subset of the Definition of Done   | High       | Medium | Human review remains mandatory per `Global.md` Review section        |
| R-002 | Overly strict naming rules could produce false positives          | Medium     | Medium | Checks are scoped to explicit, literal rules already written in policy, not inferred style rules |

---

# Acceptance Criteria

| ID     | Acceptance Criterion                                                                  | Validation Method |
| ------ | --------------------------------------------------------------------------------------- | ------------------ |
| AC-001 | Running the tool against the current repository exits `0`.                              | Test               |
| AC-002 | Running the tool against a repository containing one seeded reserved-name file exits `1` and names the exact file. | Test               |

---

# Success Metrics

| ID     | Metric                                                        | Target | Measurement Method | Frequency  |
| ------ | ---------------------------------------------------------------- | ------ | -------------------- | ---------- |
| SM-001 | Naming_Policy.md / Global.md Repository Hygiene violations merged to `main` after CI adoption | 0      | CI run outcome        | Continuous |

---

# AI Context

| Field               | Value                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| Relevant Documents  | `01_Rules/Global.md`, `02_Policies/Naming_Policy.md`, `02_Policies/Versioning_Policy.md`          |
| Prompt Dependencies | `04_Prompts/Create_Prompt.md`                                                                     |
| Repository Rules    | Global.md Repository Hygiene; Naming_Policy.md Reserved Names; Versioning_Policy.md Version Format |
| Known Constraints   | Must not invent new repository rules; must remain dependency-free                                |
| Expected Outputs    | Exit code plus an itemized, rule-cited violation list                                            |
| Context Priority    | Global.md > Naming_Policy.md > Versioning_Policy.md                                               |

---

# Traceability

| Artifact     | Reference                                        |
| ------------ | -------------------------------------------------- |
| ADR          | None — scope too small to warrant an ADR           |
| Architecture | None — see Notes                                    |
| Review       | `Requirement_Review_Report.md` (this example)       |
| Issue        |                                                     |
| Commit       |                                                     |

## Requirement Traceability Matrix (RTM)

| Requirement ID | Parent Requirement | Architecture | ADR  | Review                          | Test                                 | Issue | Commit |
| --------------- | ------------------- | ------------- | ---- | -------------------------------- | -------------------------------------- | ----- | ------ |
| FR-001          |                      |               |      | Requirement_Review_Report.md     | Manual run, see Review Evidence Summary |       |        |
| FR-002          |                      |               |      | Requirement_Review_Report.md     | Manual run, see Review Evidence Summary |       |        |
| FR-003          |                      |               |      | Requirement_Review_Report.md     | Manual run, see Review Evidence Summary |       |        |
| FR-004          |                      |               |      | Requirement_Review_Report.md     | Manual run, see Review Evidence Summary |       |        |

---

# Change Log

| Version | Date       | Author | Summary          |
| ------- | ---------- | ------ | ----------------- |
| 1.0.0   | 2026-07-04 |        | Initial version   |
| 1.1.0   | 2026-07-04 |        | Applied ARR-EX-001: added NFR-003, NFR Validation Method column, Architecture Overview section |

---

# Requirement Change Control

None yet.

---

# Approval

| Role     | Name | Date | Approval Date | Status |
| -------- | ---- | ---- | -------------- | ------ |
| Author   |      |      |                |        |
| Reviewer |      |      |                |        |
| Approver |      |      |                |        |

---

# Notes

This document is a worked example for `08_Examples/`, showing what `/create` produces when pointed at `04_Prompts/Create_Prompt.md` and `03_Templates/Requirement.md`. It intentionally documents a requirement for a tool that was implemented first (see `06_Tools/governance-check.js`), which reverses the framework's normal Requirement → Architecture → Implementation order. This reversal is acceptable only because:

* This is reference documentation, not a real project, and is not subject to the implementation gate in `Repository_Governance.md`.
* The tool's scope is small enough that no `Architecture.md` is warranted (no components, no data flow, no deployment topology to document).

It has not gone through human approval and shall not be cited as an approved repository artifact.

---

# Version History

| Version | Date       | Author | Notes                                          |
| ------- | ---------- | ------ | ------------------------------------------------ |
| 1.0.0   | 2026-07-04 |        | Initial worked example produced via `/create`   |
| 1.1.0   | 2026-07-04 |        | Applied ARR-EX-001 via `/revise` (Merge strategy): RC-001 NFR-003, RC-002 Validation Method column, RC-003 Architecture Overview |
