# Governance Check Tool — Worked Example

This folder demonstrates the complete `/create` → `/review` → `/revise` → `/review` cycle added in `.claude/commands/`, applied to a real repository artifact.

| Step | Command                                                                       | Output                                      |
| ---- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| 1    | `/create Requirement "Governance Check Tool"`                                    | `Requirement.md` (v1.0.0)                      |
| 2    | `/review 08_Examples/Governance_Check_Tool/Requirement.md`                        | `Requirement_Review_Report.md` — RR-EX-001, **REVIEW REQUIRED** (84/100) |
| 3    | `/revise 08_Examples/Governance_Check_Tool/Artifact_Revision_Request.md`          | `Requirement.md` updated to v1.1.0 + `06_Tools/governance-check.js` NFR-003 fix |
| 4    | `/review` (Delta Review mode)                                                     | `Requirement_Review_Report_RR-EX-002.md` — **PASS WITH MINOR CHANGES** (90/100) |

The reviewed subject is `06_Tools/governance-check.js`, the mechanical rule-check script referenced by `npm run governance:check` and by `.github/workflows/governance-check.yml`.

The first review honestly fails the Quality Gate (84/100); the revision then closes the findings and the delta review passes at exactly 90/100, with every raised score citing its evidence. The cycle took two review iterations for a deliberately small artifact — kept visible as real data for the deferred "process tiers" backlog discussion.

Neither document has gone through human approval; both are illustrative only and are not governed project artifacts.
