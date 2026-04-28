# Implementation Plan: Fix Agents Sensor False Positives and Shadow File Index Gaps

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully resolved false positives in the agents sensor by excluding index.md files from author format checks. Also cleared shadow file and ghost ref findings in the index sensor by updating handoffs/index.md and confirming agents/index.md was already accurate. Verified with clean sensor runs (0 findings).Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/Scan

---

## Context

Two issues from the 2026-04-27 Dream cycle agents and index sensors:

### Issue 1 — Agents sensor false positives

The `agents` sensor flagged two files for `invalid_agent_format`:

| File | Flagged Value | Expected |
|---|---|---|
| `agents/sessions/index.md` | `date: YYYY-MM-DD` | `Name (Model)` |
| `agents/logs/index.md` | `date: YYYY-MM-DD` | `Name (Model)` |

These files are **schema documentation files** — they contain YAML code blocks showing the template format for session/log entries. The sensor is incorrectly reading the code block content as live frontmatter metadata.

The sensor needs to be updated to skip parsing of YAML inside fenced code blocks (` ```yaml ... ``` `), or to exclude `index.md` files from the agent format check since they are registry/documentation files, not agent records.

### Issue 2 — Shadow files not in index

The `index` sensor found 5 shadow files (files that exist on disk but are not listed in their directory's `index.md`):

- `agents/cowork.md` — not in `agents/index.md`
- `agents/local.md` — not in `agents/index.md`
- `agents/code.md` — not in `agents/index.md`
- `handoffs/2026-04-27-p3-Fix-script-ref-issues-flagged-by-scripts-sensor.md` — not in `handoffs/index.md`
- `handoffs/2026-04-27-p3-Restructure-reports-dream-nest-sensor-data.md` — not in `handoffs/index.md`

## Execution Steps

### For Issue 1
1. Locate the agents sensor script (likely `reports/dream/src/sensors/agents.py` or equivalent).
2. Add logic to skip content inside fenced code blocks when scanning for agent format fields.
3. Alternatively, add `index.md` to an exclusion list for the agent format check.
4. Re-run and confirm `agents/sessions/index.md` and `agents/logs/index.md` no longer appear as findings.

### For Issue 2
1. Read `agents/index.md` — add entries for `cowork.md`, `local.md`, and `code.md`.
2. Read `handoffs/index.md` — add entries for the two 2026-04-27 handoff files.
3. Re-run and confirm `index` sensor shadow file count drops.

## Verification

- `agents` sensor shows 0 issues.
- `index` sensor shadow file count drops by at least 5.
