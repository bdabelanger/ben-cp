# Crypt-Keeper Changelog

> Detail log for `skills/crypt-keeper/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

---

## [1.2.0] — First Scheduled Run (2026-04-08)

**Report:** `skills/crypt-keeper/reports/cleanup-report-2026-04-08.md`

**Flag counts by check:**
- Check 1 — Orphaned Files: 4 flags (crypt-keeper SKILL.md, changelog.md, okr-reporting changelog.md, casebook/reporting fake index)
- Check 2 — Misplaced Files: 3 flags (crypt-keeper.md root stub, CLAUDE.md, README.md)
- Check 3 — Missing index.md: 3 flags (skill-builder mappings/, styles/, rules/)
- Check 4 — Duplicates: 1 flag (crypt-keeper.md root stub = duplicate of procedure.md)
- Check 5 — Stale Status Flags: 0 flags ✅
- Check 6 — data_sources.md Sync: 2 flags (Portal DB sources, /portal GA proxy)
- Check 7 — AGENTS.md Compliance: 1 flag (SKILL.md not indexed)

**Handoff files created this run:**
- `handoff/2026-04-08-p2-crypt-keeper-root-exemptions.md` — CLAUDE.md + README.md AGENTS.md exemption decisions (new flags 2.2, 2.3)

**Existing open handoffs covering prior flags (5 total):**
- `handoff/2026-04-08-fix-orphaned-index-entries.md` (P1)
- `handoff/2026-04-08-fix-casebook-reporting-index.md` (P1)
- `handoff/2026-04-08-fix-skill-builder-subdirs.md` (P2)
- `handoff/2026-04-08-p2-move-reports-into-crypt-keeper.md` (P2)
- `handoff/2026-04-08-fix-data-sources-and-agents.md` (P3)

**reports/ dir state:** `skills/crypt-keeper/reports/` created this run. Root `reports/cleanup-report-2026-04-08.md` from prior session still exists — will be archived once P2 move handoff executes.

**Next:** Verify all 6 open handoffs complete by 2026-04-15 run. Watch for Notes Datagrid April baseline pull (GA live 2026-04-09).

---

## [1.1.0] - Initial Crypt-Keeper SOP (2026-04-08)

**Files created:**
- `procedure.md` — 7-check vault quality watchdog; flags only, no auto-fix
- `report-template.md` — structured output template for cleanup reports
- `index.md` — TOC

**Current state:** Active — scheduled weekly Monday 9am. No runs yet.

**TODOs:**
1. First scheduled run will validate all 7 checks against live vault state
2. Confirm reports land correctly in `reports/cleanup-report-[YYYY-MM-DD].md`
