# Update AGENTS.md Report Tool Documentation

> **Prepared by:** Cowork (2026-04-28)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

## Context

`get_report` and `generate_report` in `ben-cp.ts` have been updated and rebuilt. Both now use `skill` as the only parameter — consistent, no paths. AGENTS.md still documents the old interface and needs to be updated.

Current state of both tools:
- `generate_report(skill="status"|"dream"|"tasks")` — runs a pipeline
- `get_report(skill="status"|"dream"|"tasks")` — reads the latest report

---

## Execution Steps

### Step 1 — Read AGENTS.md
```
/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/AGENTS.md
```

### Step 2 — Edit the MCP Tools table

Locate the three report rows and replace:

**Old:**
```
| `list_reports` | List available report domains. Always call this first if unsure which domain to use — do not guess or rely on examples in tool descriptions. |
| `generate_report` | Run a report pipeline for a domain. Use `list_reports` to confirm valid domains before calling. |
| `get_report` | Read a generated report. Path is relative to `reports/` — e.g. `get_report(path="status/report.md")`. Never prefix with `reports/` or `skills/`. |
```

**New:**
```
| `list_reports` | List available report domains. |
| `generate_report` | Runs a pipeline to produce a new report. Pass `skill` — e.g. `generate_report(skill="status")`. Valid values: `status`, `dream`, `tasks`. Do NOT use this to read reports. |
| `get_report` | Reads the latest report for a skill. Pass `skill` — e.g. `get_report(skill="status")`. Valid values: `status`, `dream`, `tasks`. Do NOT pass a file path. |
```

### Step 3 — Changelog
Root `changelog.md` entry only (Handoff Exemption applies).

---

## Acceptance Criteria

- [ ] Both `generate_report` and `get_report` rows show `skill` parameter with examples
- [ ] No mention of `path`, `reports/` prefix, or `platform`
- [ ] Root changelog entry written
