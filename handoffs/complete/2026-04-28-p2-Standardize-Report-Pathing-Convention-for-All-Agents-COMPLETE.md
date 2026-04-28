# Standardize Report Pathing Convention for All Agents

> **Prepared by:** Cowork (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

Added list_reports row, cleaned up generate_report (removed hardcoded examples), trimmed get_report to one clean example. Google Drive Sync Latency rule confirmed intact. Changelog written. AGENTS.md Last updated bumped to 2026-04-28.

---

## Context

Three documentation issues were found in the MCP Tools table in `AGENTS.md`:

1. `generate_report` references `platform` as an example domain — this domain does not exist in the repo. Valid domains are discoverable via `list_reports`.
2. `get_report` has no row at all — agents have been guessing the path format and getting it wrong (e.g. `skills/status/report.md`).
3. `list_reports` has no row at all — agents have no documented way to discover valid report domains.

**Note:** The `platform` example also appears in the `generate_report` tool schema description itself — that cannot be fixed here. The fix is documentation-only: teach agents to call `list_reports` first rather than trusting any hardcoded enum example.

The correct path format for `get_report` is relative to `reports/` — e.g. `get_report(path="status/report.md")`. Never prefix with `reports/` or `skills/`.

---

## Goal

Fix the MCP Tools table in `AGENTS.md`:
- Add `list_reports` as the discovery tool (call this first to find valid domains)
- Fix `generate_report` to drop the `platform` example and point to `list_reports`
- Add `get_report` with correct relative path usage

---

## Execution Steps

### Step 1 — Read AGENTS.md
```
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/AGENTS.md
```

### Step 2 — Edit the MCP Tools table

Locate the `generate_report` row. Replace it with these three rows:

**Old:**
```
| `generate_report` | Generate a strategic or platform report (e.g. `platform`, `dream`) |
```

**New:**
```
| `list_reports` | List available report domains. Always call this first if unsure which domain to use — do not guess or rely on examples in tool descriptions. |
| `generate_report` | Run a report pipeline for a domain. Use `list_reports` to confirm valid domains before calling. |
| `get_report` | Read a generated report. Path is relative to `reports/` — e.g. `get_report(path="status/report.md")`. Never prefix with `reports/` or `skills/`. |
```

### Step 3 — Verify Google Drive Sync Latency rule
Confirm the rule under **Google Drive Sync Latency** still reads:
> Always use the purpose-built `get_report` MCP tool.

No edit needed — just confirm it's intact.

### Step 4 — Changelog
Root `changelog.md` entry only (one-line pointer — Handoff Exemption applies).

---

## Acceptance Criteria

- [ ] `list_reports` row added with "call this first" guidance
- [ ] `generate_report` row no longer references `platform` or any hardcoded domain
- [ ] `get_report` row added with correct relative path usage
- [ ] Google Drive Sync Latency rule intact
- [ ] Root changelog entry written
