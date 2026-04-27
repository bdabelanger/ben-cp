---
title: Implementation Plan Fix Expose Dream Report Output via ben-cp MCP
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Fix: Expose Dream Report Output via ben-cp MCP

> **Prepared by:** Code (Gemini) (2026-04-26)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-26

Completed all technical and documentation fixes. Exchanged stale generate_report paths for orchestration/utilities/, deployed get_report tool to production build, and updated AGENTS.md and README.md with Google Drive sync latency warnings.

---

## Fix: Expose Dream Report Output via ben-cp MCP

> **Prepared by:** Cowork (Claude) (2026-04-25)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS: 🔲 READY**

---

## Context

During the 2026-04-25 session, Cowork (Claude) needed to read the nightly dream report output (`reports/dream/daily-report.md`) in order to embed it into a Gemma smoke test handoff.

Two problems surfaced:

### Problem 1: `generate_report` pointed at a stale path

The `generate_report` MCP tool (skill: `dream`) attempted to invoke:
```
tools/intelligence/report.py
```
This path no longer exists. Per changelog v1.17.0, all scripts were migrated to `orchestration/utilities/`. The tool has not been updated to reflect this. As a result, `generate_report` returned a hard error and could not be used to run or read the dream pipeline.

### Problem 2: No ben-cp MCP tool for reading pipeline outputs

The `get_intelligence` tool is scoped to `intelligence/` only. The `get_handoff` tool is scoped to `orchestration/handoff/` only. There is no ben-cp MCP tool that can read files from `reports/`.

This forced Cowork to fall back to `mcp__filesystem__read_text_file` with a raw absolute path — a brittle workaround that:
- Exposes internal Google Drive mount paths to the agent context
- Breaks if the vault is moved or remounted
- Bypasses the ben-cp abstraction layer entirely
- Is not reliable on Google Drive due to sync latency (files may not be flushed to disk at the moment of read, causing stale or missing content)

### Problem 3: Google Drive sync latency

The vault lives on Google Drive (`/Users/benbelanger/My Drive (.../ben-cp`). Direct filesystem reads of pipeline outputs are unreliable because Google Drive does not guarantee immediate local availability of recently written files. The dream report written by the pipeline may not be readable via filesystem tools until Drive has synced — this is an intermittent failure mode with no clear error signal.

---

## Requested Changes

### Fix 1: Update `generate_report` tool path for `dream` skill
Update the ben-cp MCP server configuration so that `generate_report(skill='dream')` invokes:
```
orchestration/utilities/intelligence/report.py
```
instead of the stale `tools/intelligence/report.py`.

### Fix 2: Add `get_report` (or extend an existing tool) to read pipeline outputs
Add a purpose-built MCP tool — or extend `get_intelligence` — to allow reading files from `reports/`. Suggested interface:
```
get_report(scope='dream')         → reads reports/dream/daily-report.md
get_report(scope='dream', file='daily-report.md')  → explicit file
```
This keeps Cowork fully within the ben-cp abstraction layer and eliminates the filesystem workaround.

### Fix 3 (Optional but recommended): Note Google Drive latency risk in MCP server docs
Add a note in the ben-cp server README or AGENTS.md that direct filesystem reads of `reports/` are unreliable on Google Drive due to sync latency. Agents should always use MCP tools (once Fix 2 is in place) rather than raw filesystem access for pipeline outputs.

---

## Acceptance Criteria

- `generate_report(skill='dream')` runs successfully without a path error
- Cowork can read `daily-report.md` via a ben-cp MCP tool without using `mcp__filesystem__read_text_file`
- No raw Google Drive absolute paths appear in agent tool calls for routine vault operations
