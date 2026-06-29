# Global Engineering Rules

> Canonical, repository-wide baseline standard for the AI Engineering Framework.
> This document defines the mandatory rules inherited by every artifact, prompt, policy, template, and project.
> It defines baseline rules only; governance, versioning, naming, and review methodology are owned by their dedicated artifacts.
> When a local rule conflicts with this document, the stricter rule applies and shall never relax a mandatory baseline rule.

---

# Purpose

Define the repository-wide mandatory baseline rules that govern all engineering work — human or AI-assisted — within this repository.

These rules ensure that every contribution is consistent, reviewable, secure, and maintainable over the long term, independent of any individual project, contributor, or tool.

---

# Scope

These rules apply to:

* All code, configuration, documentation, prompts, templates, and other repository artifacts.
* All contributors, including human engineers, AI agents, and automated systems.
* All branches, environments, and lifecycle stages from creation to retirement.

This document does not define the following, which are owned by their dedicated artifacts:

* Repository governance, authority, roles, and approval workflow — `Repository_Governance.md`.
* Version numbering and lifecycle — `Versioning_Policy.md`.
* Naming conventions — `Naming_Policy.md`.
* Review methodology and scoring — `Review_Form.md` and `Review_Prompt.md`.

This document is project-neutral. Project-specific rules are defined separately and shall never weaken the baseline established here.

---

# Global Principles

The repository is governed by the following baseline principles.

* Repository integrity — preserve the approved repository at all times.
* Single source of truth — avoid duplicated logic, configuration, or knowledge.
* Traceability — every change shall remain reconstructable.
* Determinism — equivalent inputs shall produce equivalent outputs.
* No duplicated ownership — each responsibility belongs to exactly one artifact.
* No undocumented assumptions — state assumptions, contracts, and dependencies openly.
* Human authority over AI — final authority always belongs to a human.
* Repository consistency — follow existing conventions before introducing new ones.
* Clarity over cleverness — optimize for the next reader, not the author.
* Small, reversible changes — prefer incremental, isolated, easily revertible work.
* Fail loudly — surface errors early; never silently swallow failures.
* Automate the repeatable — recurring manual steps should become tooling.

---

# Repository-Wide Mandatory Rules

These rules are mandatory for every contribution.

## Repository Hygiene

* Use a clear, consistent branch and commit convention.
* Keep the main branch always releasable; never commit directly to it.
* Commits must be atomic, with descriptive, imperative-mood messages.
* Do not commit secrets, credentials, build artifacts, or generated output.
* Preserve repository structure; place files in their designated directories.
* Empty structural directories must be retained intentionally (e.g., via a keep file).
* Every change must be traceable to a task, issue, or documented purpose.

## Security

* Never store secrets, tokens, or credentials in the repository.
* Use environment variables or a secrets manager for all sensitive values.
* Validate and sanitize all external input.
* Apply least-privilege access for users, services, and automation.
* Review and pin third-party dependencies; avoid unvetted sources.
* Report and remediate vulnerabilities promptly; do not suppress warnings silently.
* Security-relevant changes require explicit, documented review.

## Review

* All changes require review before merge; self-merge to protected branches is prohibited.
* AI-generated changes receive the same scrutiny as human-authored changes.
* Approve only what you understand and would be willing to maintain.

Review methodology and scoring are defined by `Review_Form.md` and `Review_Prompt.md`.

## Documentation

* Documentation is part of the deliverable, not an afterthought.
* Write in Markdown using clear, hierarchical headings.
* Keep documents concise, current, and free of project-specific coupling unless scoped.
* Update documentation in the same change that alters the behavior it describes.
* Prefer examples and explicit contracts over prose where possible.

## Dependencies

* Introduce dependencies deliberately; prefer the standard library and existing tools first.
* Pin dependency versions and use a committed lockfile for reproducible builds.
* Source dependencies only from trusted, vetted registries.
* Review new and updated dependencies for license, security, and maintenance health.
* Remove unused dependencies promptly; keep the dependency surface minimal.

## Change Scope

* Every change must declare its intended scope and stay within it.
* Modify only what the task requires; avoid unrelated, opportunistic edits.
* Out-of-scope improvements are recorded as follow-up items, not bundled silently.
* Widening scope mid-change requires updating the task and re-confirming intent.

Significant or hard-to-reverse decisions shall be recorded as Architecture Decision Records; see `ADR.md`.

---

# AI Behavioral Constraints

* AI assists; it does not own. Every AI-produced artifact requires human review.
* Determinism and traceability. AI actions must be reproducible and auditable.
* Bounded autonomy. AI operates within explicitly defined scope and permissions.
* No silent assumptions. When context is missing, AI must ask or flag, not guess.
* Source honesty. AI must not fabricate facts, files, results, or references.
* Least change. AI modifies only what the task requires and reports what it did.
* Security-aware by default. AI must not introduce secrets, unsafe code, or unreviewed dependencies.

---

# Repository Consistency Requirements

* Structure documents into small, self-contained, independently retrievable sections.
* Use clear, stable headings so content is easy to index, reference, and reuse.
* Keep each document focused on a single concern to maximize retrieval precision.
* Prefer linking to a single source of truth over inlining duplicated context.
* Be concise; remove repetition and restatement of information defined elsewhere.
* Reference shared principles rather than duplicating them across documents.
* Favor modular, composable content that can be loaded selectively.
* Use consistent, machine-friendly formatting to reduce parsing overhead.
* Preserve repository-wide terminology; do not rename approved concepts.

---

# Relationship with Local Project Rules

Global Rules define the mandatory baseline for the entire repository.

Local Project Rules MAY:

* add project-specific rules
* introduce stricter requirements
* further restrict behavior

Local Project Rules SHALL NOT:

* relax mandatory Global Rules
* override Repository Governance
* conflict with approved repository policies

Where a local rule conflicts with this document, the stricter rule applies. Authority resolution between rules is defined in `Repository_Governance.md`.

---

# Compliance

* Every artifact and contribution shall comply with these baseline rules.
* Humans remain accountable for all merged work, AI-assisted or not; no change reaches a protected branch without human sign-off.
* Non-compliance shall be identified during review and shall block approval.
* Compliance shall remain traceable.

A change satisfies the Definition of Done only when:

- [ ] It fulfills the stated requirements and acceptance criteria.
- [ ] It adheres to the principles and mandatory rules above.
- [ ] It includes or updates relevant tests, and they pass.
- [ ] It includes or updates relevant documentation.
- [ ] It introduces no secrets, regressions, or unaddressed warnings.
- [ ] It has been reviewed and approved by a responsible human.
- [ ] It is merged through the standard process with a traceable history.

---

# Exceptions

Any exception to these baseline rules requires:

* Explicit approval.
* Documented justification.
* Traceable decision.

Exceptions shall not relax mandatory security or governance requirements, and shall not become precedent unless adopted through an approved revision.

---

# Version History

| Version | Date       | Author | Summary                                                                 |
|---------|------------|--------|-------------------------------------------------------------------------|
| 1.0.0   | 2026-06-29 | —      | Initial global engineering rules                                        |
| 1.1.0   | 2026-06-29 | —      | Added Change Scope, Decision Records, Context Management, Token Optimization, Dependency Management, and Versioning Policy sections |
| 2.0.0   | 2026-06-29 | —      | Restructured into repository-wide baseline rules; moved Versioning Policy to `Versioning_Policy.md` and Decision Records to `ADR.md` by reference; preserved all baseline rules without an owning policy (Migration: versioning and decision-record details now live in their owning artifacts) |
