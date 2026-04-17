# Claude Code Implementation Plan: Changelog Fact-Check Fixes

> **Prepared by:** Claude Code (2026-04-08)
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — changelog inaccuracies mislead agents loading session context
> **Source report:** manual fact-check; Changelog Auditor skill created at `skills/changelog/`
> **v1.0**
> **STATUS**: ✅ COMPLETE

All 8 tasks executed. `handoff/complete/` naming fixed for 2 files (added -COMPLETE suffix). `p2-crypt-keeper-root-exemptions` confirmed already done. Root changelog 1.4.1 phantom path corrected (`reports/archive/` → `skills/knowledge/reports/archive/`). Root 1.5.0 expanded with missing infrastructure changes. Casebook changelog 1.1.0 count corrected (4 → 3 unexposed). Stale Next Tasks annotated in 1.2.0 and 1.3.0. `skills/index.md` and `AGENTS.md` already had lumberjack entries — Task 7 was pre-done. Changelog entries written via `write_changelog_entry` (root 1.6.0 + 5 subdirectory logs).

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

A manual changelog audit (Changelog Auditor's first informal run) found 6 categories of issues
in root `changelog.md` and `skills/casebook/changelog.md`. None are P1 (agent navigation
is fine), but stale tool names and phantom entries will mislead agents loading session
context. Also: 2 files in `handoff/complete/` are missing the `-COMPLETE` suffix, and
one open handoff (`p2-crypt-keeper-root-exemptions`) may already be done.

---

## Execution Order

1. **Task 1** — Fix `handoff/complete/` naming
2. **Task 2** — Verify `p2-crypt-keeper-root-exemptions` handoff status
3. **Task 3** — Fix phantom `reports/archive/` entry in root changelog 1.4.1
4. **Task 4** — Add missing root changelog entries for today's unlogged work
5. **Task 5** — Fix casebook changelog 1.1.0 wrong count
6. **Task 6** — Annotate stale Next Tasks in root changelog
7. **Task 7** — Update `skills/index.md` and `AGENTS.md` for lumberjack
8. **Task 8** — Write changelog and mark complete

---

## Task 1: Fix handoff/complete/ Naming

Two files are missing the `-COMPLETE` suffix:

```
handoff/complete/2026-04-08-changelog-refactor.md
handoff/complete/2026-04-09-consolidate-project-status-reports.md
```

Rename both:
```
mv handoff/complete/2026-04-08-changelog-refactor.md \
   handoff/complete/2026-04-08-changelog-refactor-COMPLETE.md

mv handoff/complete/2026-04-09-consolidate-project-status-reports.md \
   handoff/complete/2026-04-09-consolidate-project-status-reports-COMPLETE.md
```

Confirm both now end in `-COMPLETE.md`.

---

## Task 2: Verify p2-crypt-keeper-root-exemptions Handoff

Read `handoff/2026-04-08-p2-crypt-keeper-root-exemptions.md`.

Then read `AGENTS.md` — check whether `CLAUDE.md` and `README.md` are already in the
root exemptions list.

- If already done: update STATUS to ✅ COMPLETE, move to `handoff/complete/`
- If not done: leave open, execute it

---

## Task 3: Fix Phantom reports/archive/ Entry

Root changelog `1.4.1` states:
> `skills/knowledge/reports/` and `reports/archive/` directories created

`reports/archive/` does not exist on disk. Two options:

**Option A (preferred):** Create the directory so the entry is accurate:
```
mkdir /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/reports/archive
```
Add a `.gitkeep` if needed to track in git.

**Option B:** Remove the phrase from the 1.4.1 entry.

Read `changelog.md` first, then edit — use Option A unless the directory was never
intended.

---

## Task 4: Add Missing Root Changelog Entries

The following work from 2026-04-08 has no root changelog entry. Add them — one combined
entry is fine since they're all infrastructure work. Read `changelog.md` first, find the
current highest version (should be 1.4.1), bump to 1.5.0 (minor — new skill + tool upgrades).

Entry to prepend below `## [Unreleased]`:

```markdown
## [1.5.0] — Changelog Auditor Skill + Infrastructure Cleanup (2026-04-08)

**Detail logs:**
- `skills/changelog/changelog.md`
- `skills/changelog/changelog.md` (if exists)

**Changes:**
- `skills/changelog/` — new skill created: changelog auditing (7 checks, flag-only, companion to Vault Auditor)
- `skills/handoff/index.md` + `skills/changelog/index.md` + `skills/changelog/entry_template.md` — bidirectional handoff ↔ changelog cross-reference added
- `src/ben-cp.ts` — `write_changelog_entry` upgraded: `subdirectories` array (replaces single `subdirectory`), `handoff` param, `get_changelog` scope param, `failed_actions` surfaced at root level
- `src/ben-cp.ts` — `package.json` build script fixed: `tsc -p tsconfig.json` (was broken inline flags)
- `handoff/complete/` — subdirectory created; all COMPLETE handoffs migrated out of root
- `casebook-admin-mcp/src/casebook-mcp.ts` — server name corrected: `casebook-admin-api` → `casebook-admin-mcp`
- `casebook-billing-mcp/src/casebook-mcp.ts` — server name corrected: `casebook-billing-api` → `casebook-subscriptions-mcp`
- `casebook-billing-mcp/package.json` — name updated: `casebook-billing-mcp` → `casebook-subscriptions-mcp`
- Both `package.json` descriptions corrected: SSE/Express, not stdio

**Next Tasks:**
1. Run Changelog Auditor after each multi-skill session
2. Rename `casebook-billing-mcp` GitHub repo → `casebook-subscriptions-mcp`, then mv local dir
```

---

## Task 5: Fix Casebook Changelog Wrong Count

Read `skills/casebook/changelog.md`. Find entry `1.1.0`.

It says: `1 MCP tool, 4 unexposed API functions` for subscriptions.
Correct value: **3 unexposed** (`fetchSubscriptionCompanies`, `chargebeeUpdateSubscriptionItems`, `generateUsagePivotTable`).

Edit that line to say `3 unexposed API functions`.

---

## Task 6: Annotate Stale Next Tasks

Two Next Tasks are stale — work already done in later entries:

**In root 1.3.0:**
> "Decide whether to expose form config functions or `chargebeeUpdateSubscriptionItems` as MCP tools"

This was completed in 1.4.0. Append `_(completed in 1.4.0)_` after the line.

**In root 1.2.0:**
> "Populate `skills/casebook/admin-mcp/index.md`..."
> "Populate `skills/casebook/billing-mcp/index.md`..."

Directories were renamed and populated in 1.3.0. Append `_(completed in 1.3.0 as admin/ and subscriptions/)_` after each.

Read `changelog.md` before any edits.

---

## Task 7: Update skills/index.md and AGENTS.md for Changelog Auditor

**Read `skills/index.md` first.** Add lumberjack row to the Skills table:
```
| `lumberjack/` | Changelog auditing — accuracy, completeness, cross-reference checks |
```

**Read `AGENTS.md` first.** Add `lumberjack/` to the vault structure tree under `skills/`:
```
    ├── lumberjack/              ← changelog auditing (accuracy + completeness checks)
```

---

## Task 8: Changelog + Completion

Write changelog entries:
- `skills/changelog/changelog.md` — note this handoff was executed, tasks completed
- Root `changelog.md` — already handled in Task 4 (1.5.0 entry covers the lumberjack creation)

Then mark this file complete:
1. Update STATUS to `✅ COMPLETE — [date]`
2. Add summary paragraph
3. Add `**Changelog:** 1.5.0 — 2026-04-09`
4. Move to `handoff/complete/2026-04-08-p2-changelog-factcheck-COMPLETE.md`

---

## Notes for This Agent

- Read before every write — no exceptions
- Tasks 3–6 all touch `changelog.md` — batch reads carefully, don't overwrite between edits
- Task 6 annotations should be minimal inline notes, not rewrites of the entries
- Historical entries (1.1.0 referencing `wrap-up/`) describe what was true at the time — do not rewrite them, they are accurate history. Only annotate if they actively mislead.
- `reports/archive/` in Task 3: Option A (create the dir) is preferred — keeps the changelog accurate without editing it
