---
title: Casebook Changelog
type: changelog
domain: intelligence/casebook
---

# Casebook Changelog

> Detail log for `skills/casebook/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

## 2026-04-09 — Execute all 7 outstanding handoffs from 2026-04-08: fix orphaned index entries, fix casebook/reporting/index.md, create skill-builder subdirectory indexes, add Portal data sources + SKILL.md naming exemption, move reports/ into crypt-keeper, document root-level exemptions, and fix changelog fact-check issues.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/knowledge/index.md` — Added SKILL.md, changelog.md, and reports/ entries to contents table; fixed stale reports path reference ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/okr-reporting/index.md` — Added changelog.md entry to contents table ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/crypt-keeper.md` — Deleted root redirect stub via git rm ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook/reporting/schema_joins.md` — Created — moved schema joins content from index.md with fixed paths (casebook-reporting/ → casebook/reporting/) ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook/reporting/index.md` — Replaced schema joins doc with proper directory TOC listing all 9 files ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/skill-builder/mappings/index.md` — Created — new directory TOC for mappings/ ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/skill-builder/styles/index.md` — Created — new directory TOC for styles/ ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/skill-builder/rules/` — Removed empty directory ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/okr-reporting/data_sources.md` — Added Database (Direct) — Portal KRs section + /portal GA proxy row with engineering note ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/AGENTS.md` — Added SKILL.md/AGENTS.md naming exemption; updated repo tree (removed root reports/, added knowledge/reports/); updated File Placement table; root exemptions already had CLAUDE.md and README.md ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/reports/` — Removed root reports/ directory (git rm -r); content already existed in skills/knowledge/reports/ ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/knowledge/procedure.md` — Updated output path from reports/ to skills/knowledge/reports/; added archive step to Pre-Flight ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/handoff/complete/2026-04-08-changelog-refactor-COMPLETE.md` — Renamed from 2026-04-08-changelog-refactor.md (added -COMPLETE suffix) ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/handoff/complete/2026-04-09-consolidate-project-status-reports-COMPLETE.md` — Renamed from 2026-04-09-consolidate-project-status-reports.md (added -COMPLETE suffix) ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/changelog.md` — Fixed 1.4.1 phantom reports/archive/ path; expanded 1.5.0 with missing infrastructure changes; annotated stale Next Tasks in 1.2.0 and 1.3.0 ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/casebook/changelog.md` — Fixed 1.1.0 wrong count: 4 unexposed → 3 unexposed API functions for subscriptions ✅ Complete

**Handoff:** `handoff/2026-04-08-p2-changelog-factcheck-COMPLETE.md`

**Next:** Run Repo Auditor to verify all P1/P2 flags from 2026-04-08 report are resolved


## [1.2.0] — All Unexposed Functions Wired as MCP Tools (2026-04-08)

**Files changed:**
- `skills/casebook/admin/index.md` — removed "unexposed" section; added Form Configurations tool table
- `skills/casebook/subscriptions/index.md` — removed "unexposed" section; all 3 functions now in tools table
- `/Users/benbelanger/GitHub/casebook-admin-mcp/src/casebook-mcp.ts` — added imports + tool defs + handlers for `list_form_configurations`, `get_form_configuration`, `update_form_configuration`
- `/Users/benbelanger/GitHub/casebook-billing-mcp/src/casebook-mcp.ts` — added imports + tool defs + handlers for `fetch_subscription_companies`, `update_subscription_items`, `generate_usage_pivot_table`

**Next:** Add SOPs as specific workflows are documented

## [1.1.0] — Admin and Subscriptions Documented (2026-04-08)

**Files changed:**
- `skills/casebook/admin-mcp/` → `skills/casebook/admin/` — renamed
- `skills/casebook/billing-mcp/` → `skills/casebook/subscriptions/` — renamed
- `skills/casebook/admin/index.md` — fully documented: auth, 7 MCP tools, 3 unexposed API functions, key files
- `skills/casebook/subscriptions/index.md` — fully documented: auth, 1 MCP tool, 3 unexposed API functions including write op flag, key files
- `skills/casebook/index.md` — updated directory names, added port column
- `AGENTS.md` — repo tree updated

**Flags:**
- `chargebeeUpdateSubscriptionItems` in `casebook-billing-mcp/src/casebook-api.ts` is a write op not exposed as an MCP tool — flagged in subscriptions/index.md
- Three form config functions in `casebook-admin-mcp/src/casebook-api.ts` are also unexposed — documented as candidates for future tool wiring

**Next:** Add SOPs to `admin/` and `subscriptions/` as specific workflows are documented

---

## [1.0.0] — Casebook Skill Consolidated (2026-04-08)

**Changes:**
- `skills/casebook-reporting/` moved to `skills/casebook/reporting/` (9 files, git mv)
- `skills/casebook/admin-mcp/index.md` created — stub for casebook-admin-mcp docs
- `skills/casebook/billing-mcp/index.md` created — stub for casebook-billing-mcp docs
- `skills/casebook/index.md` created — TOC for all Casebook skill content

**Handoff:** `handoff/complete/2026-04-08-consolidate-casebook-into-skills-COMPLETE.md`

**TODOs:**
1. Populate `admin-mcp/index.md` with tool descriptions and SOPs
2. Populate `billing-mcp/index.md` with tool descriptions and SOPs
