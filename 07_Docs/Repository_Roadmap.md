# Repository Roadmap

> Canonical planning document for the AI Engineering Framework.
> This roadmap defines repository phases, implementation order, artifact status, dependencies, milestones, and completion criteria.
> It is the single planning reference for repository evolution.
> The roadmap records planning only; it does not redefine responsibilities owned by other approved artifacts.

---

# Purpose

Provide a single, traceable plan for the evolution of the AI Engineering Framework.

Objectives:

* Define the repository development phases.
* Track the status of every repository artifact.
* Record implementation order and dependencies.
* Define milestones, priorities, and completion criteria.
* Support long-term repository evolution.

---

# Scope

This roadmap covers:

* Repository phases and implementation sequence.
* The inventory and status of repository artifacts.
* Dependencies, milestones, priorities, and completion checkpoints.

This roadmap does not define:

* Repository governance — see `Repository_Governance.md`.
* Version numbering — see `Versioning_Policy.md`.
* Naming conventions — see `Naming_Policy.md`.
* Review methodology — see `Review_Form.md` and `Review_Prompt.md`.
* Architecture, template formats, or prompt implementation.

These responsibilities remain owned by their existing artifacts.

---

# Repository Overview

The repository is organized by responsibility, following the structure defined in `Naming_Policy.md`.

| Directory     | Responsibility                                  |
| ------------- | ----------------------------------------------- |
| `01_Rules`    | Repository-wide engineering rules               |
| `02_Policies` | Governance, versioning, and naming policies     |
| `03_Templates`| Canonical artifact templates                    |
| `04_Prompts`  | Canonical implementation and review prompts     |
| `05_Projects` | Project instances built on the framework        |
| `06_Tools`    | Automation, tooling, and integrations           |
| `07_Docs`     | Repository documentation, including this roadmap |
| `08_Examples` | Worked examples and references                  |

---

# Development Phases

| Phase | Focus              | Key Artifacts                                                            | Status      |
| ----- | ------------------ | ----------------------------------------------------------------------- | ----------- |
| P1    | Foundation Rules   | `Global.md`                                                             | Approved    |
| P2    | Policies           | `Versioning_Policy.md`, `Naming_Policy.md`, `Repository_Governance.md`  | Approved    |
| P3    | Templates          | `Requirement.md`, `Architecture.md`, `ADR.md`, `Review_Form.md`, `Review_Report.md`, `Artifact_Revision_Request.md` | Approved |
| P4    | Prompt Standards   | `Create_Prompt.md`, `Review_Prompt.md`, `Revision_Prompt.md`            | Approved    |
| P5    | Documentation      | `Repository_Roadmap.md`                                                 | In Progress |
| P6    | Projects           | `05_Projects`                                                           | Planned     |
| P7    | Tools              | `06_Tools`                                                              | Planned     |
| P8    | Examples           | `08_Examples`                                                           | Planned     |

---

# Artifact Inventory

Status reflects the approved foundation as of this roadmap version.

| Artifact                  | Category | Path                                       | Version | Status      |
| ------------------------- | -------- | ------------------------------------------ | ------- | ----------- |
| Global Engineering Rules  | Rule     | `01_Rules/Global.md`                       | 2.0.0   | Approved    |
| Versioning Policy         | Policy   | `02_Policies/Versioning_Policy.md`         | 1.1.0   | Approved    |
| Naming Policy             | Policy   | `02_Policies/Naming_Policy.md`             | 1.0.0   | Approved    |
| Repository Governance     | Policy   | `02_Policies/Repository_Governance.md`     | 1.1.0   | Approved    |
| Requirement               | Template | `03_Templates/Requirement.md`              | 1.1.1   | Approved    |
| Architecture              | Template | `03_Templates/Architecture.md`             | 1.1.0   | Approved    |
| ADR                       | Template | `03_Templates/ADR.md`                      | 1.1.0   | Approved    |
| Review Form               | Template | `03_Templates/Review_Form.md`              | 1.0.0   | Approved    |
| Review Report             | Template | `03_Templates/Review_Report.md`            | 1.1.0   | Approved    |
| Artifact Revision Request | Template | `03_Templates/Artifact_Revision_Request.md`| 1.2.0   | Approved    |
| Create Prompt             | Prompt   | `04_Prompts/Create_Prompt.md`              | 1.1.0   | Approved    |
| Review Prompt             | Prompt   | `04_Prompts/Review_Prompt.md`              | 1.2.0   | Approved    |
| Revision Prompt           | Prompt   | `04_Prompts/Revision_Prompt.md`            | 1.2.0   | Approved    |
| Repository Roadmap        | Document | `07_Docs/Repository_Roadmap.md`            | 1.0.0   | Draft       |

---

# Dependency Roadmap

Artifacts shall be developed and maintained in dependency order. A dependent artifact shall not be approved before the artifacts it depends on.

* Foundation Rules precede all other artifacts.
* Policies precede Templates and Prompts.
* Templates follow the order Requirement → Architecture → ADR, consistent with the version dependencies in `Versioning_Policy.md`.
* Review Report depends on the artifact it reviews.
* Prompts depend on the Templates and Policies they reference.
* Documentation depends on the artifacts it describes.
* Projects, Tools, and Examples depend on the approved foundation.

---

# Milestones

| Milestone | Description                                  | Status      |
| --------- | -------------------------------------------- | ----------- |
| M1        | Foundation rules and policies approved       | Complete    |
| M2        | Canonical templates approved                 | Complete    |
| M3        | Prompt standards approved                    | Complete    |
| M4        | Repository governance approved               | Complete    |
| M5        | Documentation layer published                | In Progress |
| M5.5      | Repository audit completed                   | Complete    |
| M6        | First project instance established           | Planned     |
| M7        | Tooling and automation introduced            | Planned     |
| M8        | Worked examples published                    | Planned     |

---

# Priorities

| Priority | Focus                                                        |
| -------- | ------------------------------------------------------------ |
| Critical | Preserve consistency and integrity of the approved foundation |
| High     | Complete the documentation layer                             |
| Medium   | Establish the first project instance and core tooling        |
| Low      | Publish worked examples                                      |

Priorities follow the model defined by the repository templates and shall not introduce a new priority scheme.

---

# Completion Criteria

The repository foundation is complete when:

* Every foundation rule, policy, template, and prompt is approved.
* The documentation layer, including this roadmap, is published.
* The artifact inventory is accurate and traceable.
* Cross-references between artifacts remain consistent.
* Every artifact complies with `Repository_Governance.md`.

---

# Future Expansion

Beyond the approved foundation, the repository may expand to include:

* Project instances under `05_Projects`.
* Automation, integrations, and MCP tooling under `06_Tools`.
* Worked examples under `08_Examples`.
* Automated review and continuous validation.

Future expansion shall preserve the approved architecture and shall proceed through approved revisions.

---

# Version History

| Version | Date       | Author | Notes                              |
| ------- | ---------- | ------ | ---------------------------------- |
| 1.0.0   | 2026-06-29 |        | Initial canonical repository roadmap |
