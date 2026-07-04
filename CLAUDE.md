# AI Engineering Framework — Agent Context

This repository is an engineering framework (process documents + tooling), not an application. Its unit of work is the governed artifact (Requirement, Architecture, ADR, Review Report), produced through the workflow: Requirement → Architecture → Review → Implementation → Testing → Documentation → Release.

## Authority order (from `02_Policies/Repository_Governance.md`)

1. Explicit human instructions
2. `02_Policies/Repository_Governance.md`
3. Repository policies (`02_Policies/`)
4. Local project rules (inside `05_Projects/<project>/`)
5. `01_Rules/Global.md`
6. Prompts and templates (`04_Prompts/`, `03_Templates/`)

## Non-negotiable behavior (defined in `01_Rules/Global.md` — read it before governed work)

* AI assists; it does not own. Every artifact requires human review; final authority is human.
* No silent assumptions — when context is missing, ask or flag, not guess.
* Never invent repository rules, requirements, or version numbers.
* Least change: modify only what the task requires; declare scope and stay in it.
* Never commit secrets, dependency directories, build artifacts, or logs.
* Versioning is SemVer per `02_Policies/Versioning_Policy.md`; never delete Version History.
* Naming per `02_Policies/Naming_Policy.md`; never rename approved artifacts.

## Commands

| Command   | Purpose                                    | Canonical prompt                  |
| --------- | ------------------------------------------- | ---------------------------------- |
| `/create` | Create one new repository artifact           | `04_Prompts/Create_Prompt.md`     |
| `/review` | Review an artifact against the Quality Gate  | `04_Prompts/Review_Prompt.md`     |
| `/revise` | Apply an approved Artifact Revision Request  | `04_Prompts/Revision_Prompt.md`   |

A worked example of the full cycle lives in `08_Examples/Governance_Check_Tool/`.

## Verification

Run `npm run governance:check` (also enforced by CI in `.github/workflows/governance-check.yml`) before considering any change done. Exit codes: 0 = clean, 1 = violations, 2 = tool failure.

## Quality Gate (canonical thresholds, from `03_Templates/Review_Form.md`)

Architecture ≥ 9, Security ≥ 9, Maintainability ≥ 9, AI Compatibility ≥ 9, Token Efficiency ≥ 8, Overall ≥ 90. Artifacts failing any gate cannot be approved.

This file is a pointer map, not a source of truth — the linked documents own their rules. If this file ever conflicts with them, the linked documents win.
