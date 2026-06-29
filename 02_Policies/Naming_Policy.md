# Naming Policy

> Canonical naming policy for the AI Engineering Framework.
> This policy defines naming conventions for all repository artifacts.
> Consistent naming improves readability, traceability, automation, and AI-assisted development.
> All repository assets shall follow this policy unless explicitly overridden by repository governance.

---

# Purpose

Define consistent naming conventions across the repository.

Objectives:

* Improve readability.
* Reduce ambiguity.
* Support automation.
* Improve AI retrieval.
* Maintain long-term consistency.

---

# Scope

This policy applies to:

* Repositories
* Directories
* Files
* Documents
* Templates
* Prompts
* Source Code
* Configuration
* APIs
* Databases
* Variables
* Functions
* Classes
* AI Agents
* MCP Servers

---

# General Principles

Names shall be:

* Clear
* Descriptive
* Consistent
* Stable
* Searchable
* Unambiguous

Avoid:

* Abbreviations without definition.
* Temporary names.
* Ambiguous wording.
* Personal naming styles.

---

# Language

Repository naming shall use English.

Exceptions:

* Business terminology officially defined by the project.
* Regulatory references.
* Customer-specific terminology.

---

# Case Conventions

| Item                 | Convention       | Example                  |
| -------------------- | ---------------- | ------------------------ |
| Repository           | Pascal-Case      | AI-Engineering-Framework |
| Directory            | Pascal_Case      | Review_Templates         |
| Markdown File        | Pascal_Case      | Architecture.md          |
| JSON                 | snake_case       | repository_config.json   |
| YAML                 | kebab-case       | release-policy.yaml      |
| Environment Variable | UPPER_SNAKE_CASE | OPENAI_API_KEY           |
| Class                | PascalCase       | ReviewEngine             |
| Interface            | PascalCase       | ReviewProvider           |
| Function             | camelCase        | generateReport()         |
| Variable             | camelCase        | reviewResult             |
| Constant             | UPPER_SNAKE_CASE | MAX_TOKEN_LIMIT          |

---

# Repository Structure Naming

Repository folders should represent responsibility rather than technology.

Examples:

```text
01_Rules
02_Policies
03_Templates
04_Prompts
05_Projects
06_Tools
07_Docs
08_Examples
```

Avoid names such as:

* Misc
* Temp
* New Folder
* Test2
* Final_Final

---

# Document Naming

Documents should use descriptive names.

Recommended:

* Requirement.md
* Architecture.md
* ADR.md
* Review_Form.md
* Review_Report.md
* Review_Prompt.md
* Naming_Policy.md

Avoid:

* Doc1.md
* Notes.md
* Final.md
* New.md

---

# Identifier Naming

Identifiers shall remain stable after publication.

Supported identifiers:

* Requirement ID
* ADR ID
* Architecture ID
* Review ID
* Issue ID
* Change Request ID

Examples:

```text
REQ-001
ADR-012
ARC-005
REV-010
CR-003
```

---

# Version Naming

Version naming shall follow the repository Versioning Policy.

Examples:

```text
Architecture v1.2.0
ADR v1.0.0
Review_Report v2.1.0
```

---

# Branch Naming

Recommended patterns:

```text
feature/<name>
bugfix/<name>
hotfix/<name>
release/<version>
docs/<name>
```

Examples:

```text
feature/review-report
release/v2.0.0
hotfix/version-policy
```

---

# Commit Naming

Commits should follow a consistent convention.

Recommended prefixes:

* feat:
* fix:
* docs:
* refactor:
* test:
* chore:
* perf:
* security:

Examples:

```text
feat: add review report template
docs: update architecture policy
fix: correct version lifecycle
```

---

# Prompt Naming

Prompt files should describe their primary purpose.

Examples:

* Create_Prompt.md
* Review_Prompt.md
* Refactor_Prompt.md
* Research_Prompt.md

Avoid generic names.

---

# AI Naming Guidelines

AI-generated artifacts shall:

* Follow repository naming conventions.
* Avoid random suffixes.
* Avoid timestamps in names unless required.
* Preserve identifier stability.
* Never rename approved artifacts automatically.

---

# Reserved Names

The following names shall not be used for production artifacts:

* temp
* tmp
* new
* final
* final2
* draft-final
* copy
* backup

---

# Compliance

This policy shall remain consistent with:

* Global.md
* Versioning_Policy.md
* Repository Governance
* Documentation Policy

---

# Exceptions

Any naming exception requires:

* Explicit approval.
* Documented justification.
* Traceable decision.

---

# Naming Review Checklist

Verify before approval:

* [ ] Naming is descriptive.
* [ ] Naming follows the defined convention.
* [ ] No ambiguous abbreviations are used.
* [ ] Case conventions are correct.
* [ ] Identifiers are stable.
* [ ] Reserved names are not used.
* [ ] Naming is consistent across the repository.

---

# Approval

| Role     | Name | Date | Status |
| -------- | ---- | ---- | ------ |
| Author   |      |      |        |
| Reviewer |      |      |        |
| Approver |      |      |        |

---

# Version History

| Version | Date       | Author | Notes                           |
| ------- | ---------- | ------ | ------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical naming policy |
