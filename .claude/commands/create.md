---
description: Implement a new AI Engineering Framework artifact via the canonical Create Prompt
argument-hint: <artifact-category> <artifact-name-or-path>
---

Follow @04_Prompts/Create_Prompt.md exactly.

Artifact Category and Name: $ARGUMENTS

Before implementing:

1. Identify the matching template in `03_Templates/` for this Artifact Category (e.g. `Requirement.md`, `Architecture.md`, `ADR.md`).
2. Read the "Existing Repository Context" artifacts listed in the Create Prompt that apply to this category (Global Rules, Naming Policy, Versioning Policy, Repository Governance).
3. Apply the Create Prompt's Decision Rules, Decision Priority, and Decision Process without restating them.

Produce only the Required Deliverable defined by the Create Prompt. Stop and report if the Artifact Category, Artifact Name, or Repository Path cannot be determined from the input — do not guess.
