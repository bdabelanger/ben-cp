---
title: 'Claude Code Implementation Plan: Fix Orphaned Index Entries + Root Stub'
type: handoff
domain: handoffs/complete
---


# Claude Code Implementation Plan: Fix Orphaned Index Entries + Root Stub

> **Prepared by:** Claude (Cowork session, 2026-04-08)
> **Source:** Vault Auditor report `reports/knowledge-report-2026-04-08.md` flags 1.1, 1.2, 1.3, 4.1
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **v1.0**
> **STATUS**: ✅ COMPLETE

All three tasks executed. `skills/knowledge/index.md` updated with SKILL.md, changelog.md, and reports/ entries. `skills/okr-reporting/index.md` updated with changelog.md entry. `crypt-keeper.md` root stub deleted via `git rm` (confirmed as redirect-only). `vault-cleanup.md` was not present at root — no action needed.

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

Vault Auditor's first run flagged four quick fixes:
- `skills/knowledge/index.md` is missing entries for `SKILL.md` and `changelog.md`
- `skills/okr-reporting/index.md` is missing an entry for `changelog.md`
- `crypt-keeper.md` at vault root is a dead redirect stub violating AGENTS.md rules

All are small targeted edits. No new files needed.

---

## Execution Order

1. **Task 1** — Add `SKILL.md` and `changelog.md` to `skills/knowledge/index.md`
2. **Task 2** — Add `changelog.md` to `skills/okr-reporting/index.md`
3. **Task 3** — Delete `crypt-keeper.md` at vault root
4. **Task 4** — Final audit and completion report

---

## Task 1: Update skills/knowledge/index.md

**Read first:** `skills/knowledge/index.md`

Add two rows to the contents table:

```
| `SKILL.md` | Cowork/scheduled task skill descriptor — entry point for automated runs |
| `changelog.md` | Detail log for this skill — all structural changes |
```

---

## Task 2: Update skills/okr-reporting/index.md

**Read first:** `skills/okr-reporting/index.md`

Add one row to the contents table:

```
| `changelog.md` | Detail log for this skill — all structural changes |
```

---

## Task 3: Delete crypt-keeper.md at vault root

**Read first:** `crypt-keeper.md` — confirm it is the redirect stub (should contain only "MOVED" notice pointing to `skills/knowledge/procedure.md`)

If confirmed as stub, delete it:
```
git rm /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/crypt-keeper.md
```

Also check `vault-cleanup.md` at vault root — if it is similarly a dead redirect stub, delete it too:
```
git rm /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/vault-cleanup.md
```

---

## Task 4: Final Audit

1. Read `skills/knowledge/index.md` — confirm both new entries present
2. Read `skills/okr-reporting/index.md` — confirm changelog.md entry present
3. Confirm `crypt-keeper.md` no longer exists at vault root
4. Write changelog entry using `write_changelog_entry`

```
## Completion Report

**Files modified:**
- skills/knowledge/index.md — added SKILL.md and changelog.md entries
- skills/okr-reporting/index.md — added changelog.md entry

**Files deleted:**
- crypt-keeper.md (vault root) — dead redirect stub
- vault-cleanup.md (vault root) — dead redirect stub (if confirmed)

**Flags for Ben:** [anything unexpected]
```
