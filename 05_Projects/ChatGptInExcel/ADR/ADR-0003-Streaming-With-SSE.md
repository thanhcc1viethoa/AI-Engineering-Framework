# Architecture Decision Record (ADR)

> ADR-0003 (ChatGptInExcel) — Stream AI responses with Server-Sent Events.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field         | Value                                |
| ------------- | ------------------------------------ |
| ADR ID        | ADR-0003                             |
| Title         | Stream AI responses with Server-Sent Events |
| Project       | ChatGptInExcel                       |
| Version       | 1.0.0                                |
| Status        | Superseded by ADR-0004               |
| Author        |                                      |
| Reviewer      |                                      |
| Decision Date | 2026-06-29                           |
| Last Updated  | 2026-06-29                           |

---

# Decision Summary

The backend streams AI output to the task pane token-by-token using Server-Sent Events (SSE), so responses appear progressively and the UI stays responsive.

---

# Context

* NFR-003 requires responsive, streaming output.
* OpenAI supports streamed completions; the BFF relays the stream to the client.

---

# Problem Statement

How should AI output be delivered from the backend to the client to keep the UI responsive?

---

# Decision

Stream tokens from the BFF to the client over SSE for each chat request. The client renders tokens as they arrive and remains interactive throughout.

---

# Decision Classification

* Architecture Decision
* Technology Decision

---

# Decision Priority

Medium.

---

# Decision Lifecycle

Accepted.

---

# Alternatives Considered

| Alternative          | Advantages                | Disadvantages                         | Reason Rejected                   |
| -------------------- | ------------------------- | ------------------------------------- | --------------------------------- |
| Request/response poll | Simple                   | Laggy; no progressive output          | Poor responsiveness               |
| WebSocket            | Bidirectional, real-time  | Overhead; bidirectional not needed    | Unnecessary complexity for one-way |
| SSE (chosen)         | Simple one-way streaming  | One-directional only                  | —                                 |

---

# Decision Rationale

* Trade-offs: one-way only (sufficient here) in exchange for simplicity over WebSocket.
* Benefits gained: progressive rendering, responsive UI, straightforward implementation.

---

# Consequences

## Positive

* Progressive, responsive responses.
* Simpler than WebSocket for one-way streaming.

## Negative

* One-directional; a separate request initiates each stream.

## Risks

* Some proxies/hosts buffer SSE — mitigated by correct headers and host testing.

---

# Impact Assessment

| Area          | Impact                                |
| ------------- | ------------------------------------- |
| Architecture  | BFF exposes an SSE streaming endpoint |
| Development   | Client consumes an event stream       |
| Operations    | Ensure infrastructure passes SSE      |

---

# Compliance

Consistent with `01_Rules/Global.md` and REQ-001 (NFR-003, FR-008).

---

# Traceability

| Artifact      | Reference          |
| ------------- | ------------------ |
| Requirement   | REQ-001 (NFR-003, FR-008) |
| Architecture  | ARC-001 (AD-003)   |

---

# Validation

* Architecture Review.
* Test: responses render progressively without blocking the UI.

---

# Approval

| Role      | Name | Date | Status |
| --------- | ---- | ---- | ------ |
| Architect |      |      |        |
| Reviewer  |      |      |        |
| Approver  |      |      |        |

---

# Superseded By

| ADR ID   | Reason |
| -------- | ------ |
| ADR-0004 | There is no longer a backend streaming to an Office task pane. ChatGPT communicates with the local MCP server over the MCP transport, which handles request/response delivery, so SSE streaming is no longer part of the architecture. |

---

# Version History

| Version | Date       | Author | Notes                              |
| ------- | ---------- | ------ | ---------------------------------- |
| 1.0.0   | 2026-06-29 |        | Accepted: SSE streaming for AI responses |
| 1.1.0   | 2026-06-30 |        | Superseded by ADR-0004 (local MCP server integration boundary) |
