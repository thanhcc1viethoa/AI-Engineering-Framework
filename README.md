# AI Engineering Framework

## Vision

Build software with AI in a predictable, maintainable and reviewable way.

This repository is not an application.

It is an engineering framework used to develop high-quality software with AI assistants such as:

* Claude Code
* OpenAI Codex
* GPT
* Gemini
* GitHub Copilot

---

# Objectives

* Standardize AI-assisted software development
* Reduce AI hallucination
* Reduce maintenance cost
* Improve code quality
* Improve documentation quality
* Reuse engineering knowledge

---

# Repository Structure

```text
01_Rules/          Engineering rules and standards

02_Policies/       Governance policies

03_Templates/      Reusable engineering templates

04_Prompts/        Reusable AI prompts

05_Projects/       Project templates and real projects

06_Tools/          Automation tooling (governance-check.js)

07_Docs/           Repository documentation

08_Examples/       Worked examples (full /create → /review → /revise cycle)

.claude/           Claude Code commands (/create, /review, /revise)

.codex/            Codex configuration (reserved)

.github/           CI workflows (governance check on push / pull request)
```

---

# Development Workflow

Requirement

↓

Architecture

↓

Review

↓

Implementation

↓

Testing

↓

Documentation

↓

Release

---

# Tooling

The workflow is executable, not only documented.

| Entry point                  | What it does                                                        |
| ----------------------------- | -------------------------------------------------------------------- |
| `/create` (Claude Code)       | Creates one artifact per `04_Prompts/Create_Prompt.md`               |
| `/review` (Claude Code)       | Reviews an artifact against the Quality Gate per `04_Prompts/Review_Prompt.md` |
| `/revise` (Claude Code)       | Applies an approved Artifact Revision Request per `04_Prompts/Revision_Prompt.md` |
| `npm run governance:check`    | Mechanically enforces rules already defined in `01_Rules/` and `02_Policies/` (exit 0 clean / 1 violations / 2 tool failure) |
| GitHub Actions                | Runs the governance check on every push and pull request to `main`   |

A complete worked example of the cycle (including an honest first-review failure) lives in `08_Examples/Governance_Check_Tool/`.

Agent context for Claude Code sessions is provided by `CLAUDE.md` at the repository root.

---

# Principles

* Simplicity first
* Documentation first
* Review before implementation
* Human decides
* AI assists

---

# Current Version

Framework Version:

V1.0 Foundation
