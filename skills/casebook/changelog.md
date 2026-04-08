# Casebook Changelog

> Detail log for `skills/casebook/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

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
- `skills/casebook/subscriptions/index.md` — fully documented: auth, 1 MCP tool, 4 unexposed API functions including write op flag, key files
- `skills/casebook/index.md` — updated directory names, added port column
- `AGENTS.md` — vault tree updated

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
