# Architecture Decision Record (ADR)

> ADR-0001 (ChatGptInExcel) — Backend-for-Frontend proxy with server-side AI credentials.
> Instantiated from the frozen `03_Templates/ADR.md` (v1.1.0).
> ADRs are immutable records; a new ADR supersedes this one rather than editing it.

---

# Document Information

| Field         | Value                                       |
| ------------- | ------------------------------------------- |
| ADR ID        | ADR-0001                                     |
| Title         | Backend-for-Frontend proxy with server-side AI credentials |
| Project       | ChatGptInExcel                               |
| Version       | 1.0.0                                        |
| Status        | Superseded by ADR-0004                       |
| Author        |                                              |
| Reviewer      |                                              |
| Decision Date | 2026-06-29                                   |
| Last Updated  | 2026-06-29                                   |

---

# Decision Summary

All OpenAI requests are routed through a server-side Backend-for-Frontend (BFF). The OpenAI credential is held only by the backend and is never delivered to the Office task-pane client. The client authenticates to the BFF and receives only a short-lived session token.

---

# Context

* The task pane is a web client running inside Office; any secret it holds is recoverable by inspection.
* The OpenAI API key is a Secret-class credential.
* Requirements FR-002 and NFR-002 require secure authentication and no plaintext secrets at rest.

---

# Problem Statement

How should the add-in call the OpenAI API without exposing the OpenAI credential to an untrusted client?

---

# Decision

Introduce a BFF backend that:

* Holds all OpenAI credentials in a server-side secrets manager.
* Authenticates the user and issues a short-lived session token.
* Proxies chat requests to OpenAI and streams responses back.

The client never receives the OpenAI key and stores no secret beyond a short-lived session token.

---

# Decision Classification

* Security Decision
* Architecture Decision

---

# Decision Priority

Critical.

---

# Decision Lifecycle

Accepted.

---

# Alternatives Considered

| Alternative                                   | Advantages           | Disadvantages                              | Reason Rejected                         |
| --------------------------------------------- | -------------------- | ------------------------------------------ | --------------------------------------- |
| Embed a shared OpenAI key in the client       | Simplest             | Key is fully exposed                       | Unacceptable secret exposure            |
| User pastes key, stored in Office settings    | No backend           | Secret stored on client; weak at-rest      | Violates NFR-002                        |
| BFF proxy with server-side key (chosen)       | Key never on client  | Requires backend infrastructure            | —                                       |

---

# Decision Rationale

* Trade-offs: added backend infrastructure in exchange for a secure credential boundary.
* Risks accepted: operating a backend service.
* Benefits gained: no client-side secret, central rate limiting, auditability, and provider abstraction.

---

# Consequences

## Positive

* The OpenAI key is never exposed to the client.
* Central control over usage, logging, and rate limiting.

## Negative

* Requires deploying and operating a backend service.

## Risks

* Backend becomes a critical dependency — mitigated by stateless, horizontally scalable instances.

---

# Impact Assessment

| Area          | Impact                                       |
| ------------- | -------------------------------------------- |
| Architecture  | Adds a BFF tier between client and OpenAI    |
| Security      | Removes client-side secret exposure          |
| Operations    | Adds a service to deploy and monitor         |
| AI Agents     | All AI calls flow through one controlled path |

---

# Compliance

Consistent with `01_Rules/Global.md` (security), `Repository_Governance.md`, and REQ-001 (NFR-002).

---

# Traceability

| Artifact      | Reference          |
| ------------- | ------------------ |
| Requirement   | REQ-001 (FR-002, NFR-002) |
| Architecture  | ARC-001 (AD-001)   |
| Risk          | AR-002             |

---

# Validation

* Architecture Review.
* Inspection: confirm no OpenAI key is present in client traffic or storage.

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
| ADR-0004 | The project pivoted from an Office add-in calling a backend proxy to a local MCP server that ChatGPT operates as its MCP client. No server-side OpenAI credential is handled, so the BFF credential boundary in this ADR no longer applies. |

---

# Version History

| Version | Date       | Author | Notes                              |
| ------- | ---------- | ------ | ---------------------------------- |
| 1.0.0   | 2026-06-29 |        | Accepted: BFF proxy with server-side AI credentials |
| 1.1.0   | 2026-06-30 |        | Superseded by ADR-0004 (local MCP server integration boundary) |
