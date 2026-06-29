# Repository Governance

> Canonical governance policy for the AI Engineering Framework.
> This policy defines repository ownership, authority, and approval governance across all repository artifacts.
> It establishes who may create, review, approve, and release artifacts, and how authority is resolved when rules conflict.
> Detailed technical rules remain owned by their dedicated policies; this document governs authority and process, not implementation detail.

---

# Purpose

Define repository-level governance for the AI Engineering Framework.

Objectives:

* Establish repository ownership and authority.
* Define the roles that govern repository artifacts.
* Define how artifacts are approved and controlled.
* Resolve authority when repository rules conflict.
* Preserve repository integrity and traceability.

This policy governs authority and process. It does not redefine responsibilities already owned by other approved artifacts.

---

# Scope

This policy applies to:

* All repository artifacts.
* All contributors, reviewers, approvers, and implementation agents.
* All changes to approved repository content.

This policy does not define:

* Version numbering rules — see `Versioning_Policy.md`.
* Naming conventions — see `Naming_Policy.md`.
* Review methodology — see `Review_Form.md` and `Review_Prompt.md`.
* Software architecture, template formats, or prompt implementation.

These responsibilities remain owned by their existing artifacts.

---

# Governance Principles

The repository is governed by the following principles.

* Single source of truth — each responsibility is owned by exactly one artifact.
* Approval before change — approved content changes only through an approved revision.
* Traceability — every change shall remain reconstructable.
* No duplication — responsibilities shall not be duplicated across artifacts.
* Human authority — final authority always belongs to a human approver, never an AI agent.
* Determinism — governance shall be applied consistently and predictably.
* Least change — prefer the smallest change that satisfies an approved requirement.
* Backward compatibility — preserve compatibility whenever practical.

---

# Repository Roles

The repository defines the following governance roles. A single person may hold multiple roles unless repository governance restricts it.

| Role                  | Responsibility                                              | Authority                                  |
| --------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| Repository Owner      | Overall accountability for repository integrity             | Final authority over all governance        |
| Maintainer            | Day-to-day repository consistency and structure             | Enforces governance and policies           |
| Architect             | Owns architecture and architectural decisions               | Approves architectural change              |
| Reviewer              | Evaluates artifacts against the Review Standard             | Recommends approval status                 |
| Author                | Creates and revises artifacts                               | Proposes changes within approved scope     |
| Approver              | Grants formal approval                                      | Approves artifacts and revisions           |
| Implementation Agent  | Implements artifacts and revisions per repository prompts   | None; acts only within approved scope      |

The Implementation Agent (including AI agents) holds no autonomous authority and shall act only within the approved scope.

---

# Artifact Ownership

Each repository responsibility is owned by exactly one artifact. Ownership shall not be duplicated or transferred without an approved revision.

| Responsibility                       | Owning Artifact                              |
| ------------------------------------ | -------------------------------------------- |
| Repository governance and authority  | `Repository_Governance.md`                   |
| Repository-wide baseline rules       | Global Rules                                 |
| Version numbering and lifecycle      | `Versioning_Policy.md`                       |
| Naming conventions                   | `Naming_Policy.md`                           |
| Requirements                         | `Requirement.md`                             |
| Architecture                         | `Architecture.md`                            |
| Architectural decisions              | `ADR.md`                                     |
| Review methodology                   | `Review_Form.md`, `Review_Prompt.md`         |
| Review outcomes                      | `Review_Report.md`                           |
| Artifact creation                    | `Create_Prompt.md`                           |
| Artifact revision                    | `Revision_Prompt.md`, `Artifact_Revision_Request.md` |

An artifact shall not assume a responsibility owned by another artifact.

---

# Authority Hierarchy

When repository rules conflict, authority is resolved in the following order. A more specific and higher-authority rule overrides a lower one.

1. Explicit Human Instructions
2. Repository Governance (this document)
3. Repository Policies (Versioning, Naming, and other approved policies)
4. Local Project Rules
5. Global Rules
6. Prompts and Templates

Lower-authority rules shall never override higher-authority rules. Where this hierarchy and another artifact appear to disagree, this hierarchy prevails and the conflict shall be reported.

Global Rules establish the repository-wide baseline that all projects inherit. Local Project Rules may add or further restrict rules for a specific project, and on a project-specific matter the more specific Local Project Rule prevails within that project's scope. Local Project Rules shall not relax repository-wide mandatory rules — such as security or governance requirements — defined by Global Rules or higher authority.

---

# Governance Conflict Resolution

When repository rules or artifacts conflict, resolve the conflict as follows.

1. Apply the highest applicable rule in the Authority Hierarchy.
2. Preserve repository integrity and approved content.
3. Do not invent a compromise.
4. Report the conflict with its sources and impact.
5. Await explicit human instruction when the conflict cannot be resolved safely.

Every conflict and its resolution shall remain traceable.

---

# Governance Decision Process

Before making a governance decision, evaluate the following sequence in order.

## Step 1 — Authority

Confirm the decision is within the deciding role's authority.

## Step 2 — Ownership

Confirm the decision affects only responsibilities owned by the relevant artifact.

## Step 3 — Precedence

Apply the Authority Hierarchy where rules conflict.

## Step 4 — Consistency

Confirm the decision preserves repository consistency and approved content.

## Step 5 — Traceability

Confirm the decision remains reconstructable.

## Step 6 — Approval

Obtain the required approval before the decision takes effect.

If any step cannot be satisfied, stop and report the issue instead of proceeding.

---

# Artifact Lifecycle

Repository artifacts follow the lifecycle defined in `Versioning_Policy.md`. This policy does not introduce a new lifecycle.

* Draft
* Review
* Approved
* Released
* Deprecated
* Archived

Governance controls the transitions between these states through the Approval Process below.

---

# Approval Process

An artifact advances through the lifecycle only with the required authority.

1. The Author produces or revises the artifact (Draft).
2. The artifact is submitted for review (Review).
3. A Reviewer evaluates it using the Review Standard and records the outcome in a Review Report.
4. The Quality Gate defined by the Review Standard shall pass.
5. An Approver grants approval (Approved).
6. The artifact is released in accordance with `Versioning_Policy.md` (Released).

Approval shall be evidence-based and traceable. Review methodology and scoring are defined by `Review_Form.md` and `Review_Prompt.md` and are not redefined here.

---

# ADR Integration

Architectural decisions are governed through Architecture Decision Records.

* Significant architectural decisions shall be recorded in an ADR using `ADR.md`.
* Architecture shall evolve through approved ADRs, not undocumented change.
* The Architect approves architectural decisions; the Approver grants formal repository approval.
* Governance defines only the authority to approve architectural decisions; it does not redefine ADR methodology.

Every ADR shall remain traceable to the requirements and architecture it affects.

---

# Compliance

All repository artifacts shall comply with this governance policy and with the approved repository policies.

* Non-compliance shall be identified during review and shall block approval.
* Compliance shall remain traceable to the responsible artifact and approver.
* Governance compliance may be re-verified whenever repository governance changes.

---

# Exceptions

Any governance exception requires:

* Explicit approval.
* Documented justification.
* Traceable decision.

Exceptions shall not become precedent unless adopted through an approved revision.

---

# Governance Approval

| Role             | Name | Date | Status |
| ---------------- | ---- | ---- | ------ |
| Repository Owner |      |      |        |
| Reviewer         |      |      |        |
| Approver         |      |      |        |

---

# Version History

| Version | Date       | Author | Notes                                  |
| ------- | ---------- | ------ | -------------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical repository governance policy |
| 1.1.0   | 2026-06-29 |        | Added Artifact Ownership, Governance Conflict Resolution, Governance Decision Process, ADR Integration; clarified Global vs Local Project Rules in Authority Hierarchy; renamed Approval to Governance Approval |
