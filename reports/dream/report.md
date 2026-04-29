# Dream Report — 2026-04-29

**Run:** 15:30 · **Sensors:** 12/12 OK · **Duration:** 1.6s

## Sensor Summary

| Sensor | Status | Detail |
|--------|--------|--------|
| reindex | 🟡 | 69 directories, 174 files scanned, 2 unknown taxonomy terms |
| pulse | 🟢 | clean |
| links | 🟡 | 104 files scanned, 9 ghost links |
| frontmatter | 🔴 | 104 files scanned, 50 issues found |
| drift | 🟢 | clean |
| handoffs | 🔴 | 12 files audited, 72 issues found |
| index | 🟢 | clean |
| agents | 🟡 | 106 files scanned, 2 issues found |
| bloat | 🟡 | 258 total files, 2 yellow flags, 516 files touched 24h |
| changelog | 🟢 | clean |
| intelligence | 🟢 | clean |
| scripts | 🟢 | 5 skills checked |

## Highlights

- **9 ghost links** — broken internal references
- **72 handoff issues** — missing sections or stale READY files
- 2 files over 250KB (watch list)

## Ghost Links (sample)

- `intelligence/casebook/overview.md` → `taxonomy.md`
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/overview.md` → `../../../okrs/q2/elevate-notes/overview.md`
- `intelligence/product/projects/q2/integrations-zapier-improvements/overview.md` → `../../../okrs/q2/reduce-admin-burden/overview.md`
- `intelligence/product/projects/q2/portal-client-dashboard/overview.md` → `../../../okrs/q2/reduce-admin-burden/overview.md`
- `intelligence/product/projects/q2/services-service-plan-datagrid-with-bulk-actions/overview.md` → `../../../okrs/q2/planning-services-at-scale/overview.md`
- `intelligence/product/projects/q2/notes-global-notes-wlv-(1210368097846960).md` → `../../okrs/q2/elevate-notes/overview.md`
- `intelligence/product/overview.md` → `okrs/q2/overview.md`
- `intelligence/product/overview.md` → `../casebook/taxonomy.md`
- `skills/handoff/SKILL.md` → `run.py`

## Pipeline Reports

### ⚠️ Asana Data Fetch

`--- Running 01_fetch_projects.py ---`
`[2026-04-29 15:30:17] fetch_asana_projects.py`
`❌ Error running 01_fetch_projects.py`

### ⚠️ My Tasks

[Full report](../tasks/report.md)

_Last synced: 2026-04-28 17:52 · 63 Asana tasks · 50 Jira issues_
**11 overdue tasks** — see full report for details.

### ⚠️ Release Readiness

[Full report](../releasinator/report.md)

Release `Platform-2026-4-2` — 1 repos to bump, 0 leaks

### ⚠️ Platform Status

[Full report](../status/report.md)

1. [Notes - Notes datagrid](#CBP-2736) (GA)
2. [Web applications - Material UI upgrade (all components)](#CBP-2917) (GA)
3. [Enrollment dialog - Bulk Services section](#CBP-2992) (Beta)
4. [Notes - Bulk "General Notes"](#CBP-2752) (Beta)
5. [Notes - Locked Notes](#CBP-2923) (In UAT)
6. [Services - Service plan datagrid with bulk actions](#CBP-3066) (Development)
7. [Services WLV - Bulk actions](#CBP-3121) (Development)
8. [Notes - Bulk Service Notes](#CBP-2924) (Development)
9. [Integrations - Zapier improvements](#CBP-3158) (Development)

### ✅ Intelligence

`   Refreshed: 0`
`   Failed:    0`
`   Skipped:   0`
``
`📉 Performing Token Economy Remediation...`
