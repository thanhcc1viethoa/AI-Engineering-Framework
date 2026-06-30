# Architecture Decision Review

> Review of the revised integration direction for the ChatGptInExcel project.
> This review evaluates how ChatGPT can operate on Excel workbooks without unsupported ChatGPT web-session automation.

---

# Review Scope

## Reviewed Items

* AI-001 - Excel add-in direct ChatGPT login vs MCP-based ChatGPT-to-Excel tools
* AI-002 - Local Excel desktop COM bridge vs Microsoft Graph vs Office.js add-in bridge
* AI-003 - Safety model for write/destructive Excel operations

## References

* `05_Projects/ChatGptInExcel/Requirement.md`
* `05_Projects/ChatGptInExcel/Architecture.md`
* `01_Rules/Global.md`
* `02_Policies/Repository_Governance.md`
* `02_Policies/Versioning_Policy.md`
* `03_Templates/ADR.md`

---

# Issue Analysis

## AI-001 - Integration Boundary

### Problem

The desired experience is for ChatGPT to operate directly on Excel. Direct ChatGPT account login inside an Excel add-in is not currently established as an official public integration path. The architecture needs a supported boundary that lets ChatGPT call Excel operations.

### Feasible Options

1. Excel add-in attempts direct ChatGPT account login.
2. Excel add-in uses OpenAI API key / backend API.
3. ChatGPT calls local MCP tools that operate on Excel.

### Comparison

| Option | Advantages | Disadvantages | Impact |
| ------ | ---------- | ------------- | ------ |
| Direct ChatGPT login in add-in | Desired UX if officially supported | No confirmed public official delegated auth path; high ToS/security risk if automated | Blocked pending provider capability |
| API key / backend API | Technically straightforward | Uses API billing/key rather than ChatGPT account; not the requested interaction model | Viable fallback, but not preferred |
| Local MCP tools | Aligns with ChatGPT tool-calling model; avoids web automation; supports direct Excel operations | Requires MCP client configuration and local server | Best fit for personal ChatGPT-to-Excel workflow |

### Recommendation

Use a local MCP server as the ChatGPT-to-Excel integration boundary.

---

## AI-002 - Excel Access Mechanism

### Problem

The local MCP server needs a way to read and write the user's workbook.

### Feasible Options

1. Excel desktop COM automation through Python/pywin32.
2. Microsoft Graph Excel API.
3. Office.js add-in bridge.

### Comparison

| Option | Advantages | Disadvantages | Impact |
| ------ | ---------- | ------------- | ------ |
| Excel COM automation | Direct access to open desktop workbooks; strong fit for Windows personal use | Windows/Excel desktop specific | Best MVP path |
| Microsoft Graph Excel API | Cloud-native and cleaner for OneDrive/SharePoint files | Requires Microsoft auth and cloud workbook location | Useful future option, not MVP |
| Office.js add-in bridge | Keeps task pane UI relevant | More moving parts; local server/add-in communication complexity | Optional helper, not core |

### Recommendation

Use Excel desktop COM automation for the personal Windows MVP.

---

## AI-003 - Write Safety

### Problem

If ChatGPT can write to Excel, accidental or incorrect writes can damage user workbooks.

### Feasible Options

1. Allow unrestricted writes.
2. Require explicit confirmation for writes.
3. Disable all writes in MVP.

### Comparison

| Option | Advantages | Disadvantages | Impact |
| ------ | ---------- | ------------- | ------ |
| Unrestricted writes | Fastest interaction | Unsafe and hard to trust | Rejected |
| Confirmed writes | Useful while reducing accidental mutation | One extra confirmation step | Recommended |
| Read-only MVP | Safest | Does not satisfy direct Excel operation goal | Too limited |

### Recommendation

Require explicit confirmation for all write operations. Destructive operations are out of scope for MVP.

---

# Technical Recommendation

Create the following ADRs:

* ADR-0004 - Use local MCP server as the ChatGPT-to-Excel integration boundary.
* ADR-0005 - Use Excel desktop COM automation for personal Windows workbook access.
* ADR-0006 - Require explicit confirmation for workbook write operations.

The direction change supersedes the original add-in/backend ADRs:

| Superseded ADR | Replaced By | Reason |
| -------------- | ----------- | ------ |
| ADR-0001 (BFF proxy + server-side key) | ADR-0004 | No backend proxy or server-side AI credential; ChatGPT is the MCP client. |
| ADR-0002 (Office.js cross-host) | ADR-0005 | Excel access moves to desktop COM automation. |
| ADR-0003 (SSE streaming) | ADR-0004 | MCP transport replaces backend-to-task-pane SSE streaming. |

---

# Decision Status

The user has approved changing direction from Excel add-in direct ChatGPT login to MCP-based ChatGPT-to-Excel tooling. The decisions are ready for ADR recording and prototype implementation.
