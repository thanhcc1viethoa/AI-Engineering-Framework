# Requirement

> Requirements specification for the MotionCopyVideo project.
> Instantiated from the frozen `03_Templates/Requirement.md` (v1.1.1).
> This document is the single source of truth for the project's requirements. It is a Draft and requires human review and approval.

---

# Document Information

| Field          | Value                                   |
| -------------- | --------------------------------------- |
| Project Name   | MotionCopyVideo                         |
| Requirement ID | REQ-MCV-001                             |
| Version        | 0.2.0                                   |
| Status         | Draft                                   |
| Author         | AI agent (Claude Code), on user request |
| Owner          | Repository owner                        |
| Reviewer       |                                         |
| Created Date   | 2026-10-17                              |
| Last Updated   | 2026-10-18                              |

---

# Purpose

Produce long "motion copy" videos with Google Flow (Gemini Omni): replace the person, outfit, accessories, vehicle (and optionally background) of one or more source videos while keeping the original motion, expressions and rhythm, then join the generated clips into one longer video in which the model, outfit, accessories and vehicle stay consistent throughout.

* Success criteria: a user can go from source video(s) + an asset folder to one assembled video whose duration, scene cuts and audio match the source, with every clip checked for consistency.

---

# Background

* Current workflow: the user's character channel ("Mây") generates short clips with Nano Banana / Veo 3.1 and edits in Remotion or CapCut.
* Limitation: Veo 3.1 cannot use a source video as motion reference; Gemini Omni in Flow can edit an uploaded video but only short clips (~10 s) per generation, and each generation may drift in face, outfit colour or vehicle shape.
* Motivation: apply techniques from open-source motion-transfer repositories (Wan2.2-Animate, VACE, Wan2GP, MimicMotion) to the steps before and after Flow so that clips join consistently.

---

# Scope

## In Scope

* Split one or more source videos into Flow-sized segments at scene cuts, with overlap inside continuous shots.
* Build a fixed reference pack (one board image per asset category) and a per-segment Flow job sheet (upload file, ordered ingredients, prompt).
* Anchor workflow: after a human approves the anchor clip, export an anchor frame and add it as a continuity ingredient to all other segments.
* Quality check of downloaded clips: duration, colour drift versus the anchor clip, seam difference at overlaps, and a contact sheet for human visual review.
* Assembly: retime to source durations, normalize resolution/fps, colour-match to the anchor, cross-fade overlaps, hard-cut at original cuts, original audio.
* A local web interface showing the workflow as a diagram, with direct upload of source videos, reference images and Flow results.

## Out of Scope

* Automatic calling of Google Flow / Gemini Omni (no public API is relied upon).
* Running local motion-transfer models (Wan2.2-Animate, VACE); a possible later engine, recorded as follow-up.
* Face recognition or automatic identity scoring.
* Subtitles, voice-over and music (remain in Remotion / CapCut).

---

# Stakeholders

| Role          | Name             | Responsibility                       |
| ------------- | ---------------- | ------------------------------------ |
| Product Owner | Repository owner | Approves scope and requirements      |
| Developer     | AI agent         | Implements within approved scope     |
| Reviewer      |                  | Reviews against the Quality Gate     |
| End User      | Repository owner | Produces channel videos              |

---

# Functional Requirements

| ID     | Requirement | Category | Priority | Owner | Source | Status |
| ------ | ----------- | -------- | -------- | ----- | ------ | ------ |
| FR-001 | `prepare` shall detect hard scene cuts and split each source into segments no longer than `max_segment_seconds`. | Functional | Critical | Developer | User Request | Implemented |
| FR-002 | Segments inside one continuous shot shall overlap the next segment by `overlap_seconds`; segments at a scene cut shall not overlap. | Functional | High | Developer | User Request | Implemented |
| FR-003 | `prepare` shall build one board image per non-empty asset category, in the fixed order character, outfit, accessories, prop, background. | Functional | Critical | Developer | User Request | Implemented |
| FR-004 | `prepare` / `jobs` shall write a job sheet listing, per segment, the upload file, ordered ingredients and a prompt including the configured identity lock. | Functional | Critical | Developer | User Request | Implemented |
| FR-005 | The job sheet shall fail with an error when a segment needs more ingredients than `max_ingredients`. | Functional | High | Developer | User Request | Implemented |
| FR-006 | `check --approve-anchor` shall export the anchor frame only on explicit human approval and rebuild the job sheet with it as a continuity ingredient. | Functional | High | Developer | User Request | Implemented |
| FR-007 | `check` shall report per segment: duration, colour similarity to the anchor (output and source), seam difference, status PASS / CHECK / MISSING, and a fix-only regeneration hint for CHECK segments. | Functional | High | Developer | User Request | Implemented |
| FR-008 | `check` shall write one contact sheet with the reference pack and the source-mid, start, mid and end frames of each clip. | Functional | High | Developer | User Request | Implemented |
| FR-009 | `assemble` shall refuse to run while any segment output is missing or shorter than `need / max_stretch`. | Functional | High | Developer | User Request | Implemented |
| FR-010 | `assemble` shall produce one video whose duration equals the total source duration, cross-fading overlaps and hard-cutting at original cuts. | Functional | Critical | Developer | User Request | Implemented |
| FR-011 | `assemble` shall use the original source audio (silence for sources without audio) when `output.audio` is `source`. | Functional | High | Developer | User Request | Implemented |
| FR-012 | `assemble` shall optionally colour-match every clip to the anchor clip with one fixed per-clip transform. | Functional | Medium | Developer | User Request | Implemented |
| FR-013 | A local web UI shall show the seven workflow steps as a diagram with done / current / pending status. | Functional | High | Developer | User Request | Implemented |
| FR-014 | The UI shall accept drag-and-drop upload of source videos, asset images per category and Flow results per segment. | Functional | High | Developer | User Request | Implemented |
| FR-015 | The UI shall run prepare, approve-anchor, check and assemble, and show prompts, ingredients, QC status, contact sheet and final video. | Functional | High | Developer | User Request | Implemented |

---

# Non-Functional Requirements

| ID      | Requirement | Target |
| ------- | ----------- | ------ |
| NFR-001 | Portability | Runs on Windows with non-ASCII (Vietnamese) paths; ffmpeg + Python 3.11+ |
| NFR-002 | Determinism | Same inputs and config produce the same plan and job sheet |
| NFR-003 | Fail loudly | Errors print one clear line; exit codes 0 = ok, 1 = clips need attention, 2 = error |
| NFR-004 | Dependencies | Only numpy and opencv-python-headless, pinned in `requirements.txt` |
| NFR-005 | Security | No credentials stored; no network access by the tool; UI bound to 127.0.0.1 only, file access confined to the project folder, uploads restricted to video/image types |

---

# Requirement Validation

| ID             | Validation Method | Verified |
| -------------- | ----------------- | -------- |
| FR-001..FR-012 | Test (`motion_copy/smoke_test.py`) | Yes — synthetic data, 2026-10-17 |
| FR-013..FR-015 | Test (`motion_copy/app_smoke_test.py`) + visual check of screenshots | Yes — synthetic data, 2026-10-18 |
| FR-007, FR-008 | Demonstration on a real Flow clip | No |
| NFR-001        | Test (non-ASCII paths in smoke test) on Linux; Windows not yet run | Partial |

---

# Assumptions

| ID     | Assumption | Validation Status | Validation Method | Validation Date | Reviewer |
| ------ | ---------- | ----------------- | ----------------- | --------------- | -------- |
| AS-001 | Gemini Omni in Flow can edit an uploaded clip of up to ~10 s while preserving its motion. | Unverified (third-party sources) | Demonstration | | |
| AS-002 | Flow accepts up to 5 reference images (ingredients) per generation. | Unverified (third-party sources) | Demonstration | | |
| AS-003 | Colour-histogram drift is a useful proxy for outfit / vehicle drift between clips. | Unverified | Analysis on real clips | | |

---

# Constraints

* Generation is manual in Google Flow; requires a Google AI subscription with Omni access.
* Only source videos the user has the right to use; output labelled as AI-generated.

---

# Dependencies

* ffmpeg / ffprobe on PATH.
* Python packages: numpy, opencv-python-headless (pinned).
* Google Flow (external, manual).

---

# Risks

| ID    | Risk | Likelihood | Impact | Mitigation |
| ----- | ---- | ---------- | ------ | ---------- |
| R-001 | Flow changes clip length limits or ingredient count. | Medium | Medium | `max_segment_seconds` and `max_ingredients` are configurable. |
| R-002 | Vehicle shape drifts (wheels, pedals). | High | High | Multi-angle prop board, anchor frame, human contact-sheet review, fix-only regeneration. |
| R-003 | Colour heuristic false positives on fast-changing scenes. | Medium | Low | Flag only drift the source does not explain; status is CHECK, human decides. |

---

# Acceptance Criteria

| ID     | Acceptance Criterion | Validation Method |
| ------ | -------------------- | ----------------- |
| AC-001 | Smoke test passes: final duration equals total source duration (±0.15 s), target resolution, audio present. | Test |
| AC-002 | One real episode is produced end to end with Flow and accepted by the owner. | Demonstration |

---

# AI Context

| Field               | Value |
| ------------------- | ----- |
| Relevant Documents  | `README.md`, `motion_copy/project.example.json` |
| Prompt Dependencies | Identity lock text supplied by the user in `project.json` |
| Repository Rules    | `01_Rules/Global.md`, `02_Policies/` |
| Known Constraints   | No Flow API; manual generation step |
| Expected Outputs    | `work/flow_jobs.md`, `work/qc/report.md`, `work/qc/contact_sheet.png`, `work/final.mp4` |
| Context Priority    | This document, then `README.md` |

---

# Change Log

| Version | Date       | Author   | Summary |
| ------- | ---------- | -------- | ------- |
| 0.1.0   | 2026-10-17 | AI agent | Initial draft with prototype |
| 0.2.0   | 2026-10-18 | AI agent | Added local web UI (FR-013..FR-015) on user request |

---

# Approval

| Role     | Name | Date | Approval Date | Status  |
| -------- | ---- | ---- | ------------- | ------- |
| Author   | AI agent | 2026-10-17 | | Drafted |
| Reviewer |      |      |               | Pending |
| Approver |      |      |               | Pending |

---

# Version History

| Version | Date       | Author   | Notes |
| ------- | ---------- | -------- | ----- |
| 0.1.0   | 2026-10-17 | AI agent | Initial draft |
| 0.2.0   | 2026-10-18 | AI agent | Added web UI requirements |
