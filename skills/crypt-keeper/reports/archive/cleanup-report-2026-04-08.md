# Vault Cleanup Report — 2026-04-08

> **Run by:** Crypt-Keeper (scheduled Claude task)
> **Vault:** `/Users/benbelanger/GitHub/ben-cp`
> **Procedure:** `skills/crypt-keeper/procedure.md`
> **Action required:** Review flags below and confirm any fixes with Claude Code or Gemma

---

## ✅ Checks Summary

- [x] Check 1 — Orphaned Files ⚠️ 4 flags
- [x] Check 2 — Misplaced Files ⚠️ 3 flags (new: CLAUDE.md, README.md, crypt-keeper.md)
- [x] Check 3 — Missing index.md ⚠️ 3 flags
- [x] Check 4 — Duplicate / Near-Duplicate Files ⚠️ 1 flag
- [x] Check 5 — Stale Status Flags ✅ Clean (watch: Notes Datagrid GA live 2026-04-09)
- [x] Check 6 — data_sources.md Sync ⚠️ 2 flags
- [x] Check 7 — AGENTS.md Compliance Spot-Check ⚠️ 1 flag

> **Note:** 5 open handoffs from today's earlier session cover Flags 1.1–1.4, 3.1–3.3, 4.1, 6.1–6.2, and 7.1. New flags this run: **2.2** (CLAUDE.md) and **2.3** (README.md) — not previously flagged.

---

## ⚠️ Flags Requiring Ben's Review

### Check 1 — Orphaned Files

Files present in a directory but **not listed in that directory's `index.md`**. All 4 flags covered by open handoff `2026-04-08-fix-orphaned-index-entries.md`.

---

**Flag 1.1** — `skills/crypt-keeper/SKILL.md`
Not listed in `skills/crypt-keeper/index.md`. Index covers `index.md`, `procedure.md`, `report-template.md` only.

Suggested entries:
```
| `SKILL.md`    | Cowork/scheduled task skill descriptor — entry point for automated runs |
| `changelog.md`| Detail log for this skill — all structural changes |
```

---

**Flag 1.2** — `skills/crypt-keeper/changelog.md`
Not listed in `skills/crypt-keeper/index.md`. (Same index gap as 1.1.)

---

**Flag 1.3** — `skills/okr-reporting/changelog.md`
Not listed in `skills/okr-reporting/index.md`. Index covers `procedure.md`, `data_sources.md`, `2026-q2-kr-reference.md`, `notes_datagrid_shortcuts.md`, `notes_quick_entry.md` — `changelog.md` absent.

Suggested entry:
```
| `changelog.md` | Detail log for this skill — all structural changes |
```

---

**Flag 1.4** — `skills/casebook/reporting/index.md` is not a real index
The file contains "Schema Relationships & Data Joins" reference content — not a directory TOC. All 8 files in the directory are invisible to agents relying on the index:

- `casebook-cases.md`, `casebook-intake.md`, `casebook-people.md`, `casebook-tenants.md`, `casebook-users.md`
- `reveal_bi_syntax.md`, `reveal_bi_visualizations.md`, `changelog.md`

Also contains stale path references: `casebook-reporting/` (old) instead of `casebook/reporting/` (current).

**Covered by:** open handoff `2026-04-08-fix-casebook-reporting-index.md`.

---

### Check 2 — Misplaced Files

AGENTS.md states: **"Never create files at vault root (except `AGENTS.md`, `GEMMA.md`, `changelog.md`)."**

---

**Flag 2.1** — `crypt-keeper.md` (vault root)
Dead redirect stub pointing to `skills/crypt-keeper/procedure.md`. Violates root placement rule.
**Covered by:** open handoff `2026-04-08-fix-orphaned-index-entries.md` (Task 3).

---

**Flag 2.2** ⚠️ NEW — `CLAUDE.md` (vault root)
Not listed in AGENTS.md exemptions. Content: Claude Code agent directive stub ("Read AGENTS.md before doing anything else in this vault. [Handoff check instructions]").

**Decision needed:** If this is an intentional Claude Code entry-point convention (analogous to `GEMMA.md`), add it to the AGENTS.md exemption list. If redundant with `AGENTS.md`, delete it.

Suggested AGENTS.md update if retaining:
```
Never create files at vault root (except `AGENTS.md`, `CLAUDE.md`, `GEMMA.md`, `changelog.md`).
```

---

**Flag 2.3** ⚠️ NEW — `README.md` (vault root)
Not listed in AGENTS.md exemptions. Content: standard GitHub repo description. This is expected GitHub convention and should stay at root.

**Suggested action:** Add `README.md` to the AGENTS.md exemption list — no deletion needed, just document it.

Suggested AGENTS.md update:
```
Never create files at vault root (except `AGENTS.md`, `CLAUDE.md`, `GEMMA.md`, `README.md`, `changelog.md`).
```

---

### Check 3 — Missing index.md

All 3 flags covered by open handoff `2026-04-08-fix-skill-builder-subdirs.md`.

---

**Flag 3.1** — `skills/skill-builder/mappings/` — no `index.md`
Contains `status_mapping.md`. Referenced by multiple KR SOPs, no directory index.

Suggested starter index:
```markdown
# Skill Builder: Mappings
> Reusable business logic and transformation rules for skill outputs.
> Last updated: 2026-04-08

## 📋 Contents
| File | Description |
| :--- | :--- |
| `status_mapping.md` | Status string → Green/Yellow/Red mapping logic |
```

---

**Flag 3.2** — `skills/skill-builder/styles/` — no `index.md`
Contains `emoji_key.md`. No directory index.

Suggested starter index:
```markdown
# Skill Builder: Styles
> Visual presentation standards — emoji keys, progress bars, formatting.
> Last updated: 2026-04-08

## 📋 Contents
| File | Description |
| :--- | :--- |
| `emoji_key.md` | Standard emoji usage across all skill outputs |
```

---

**Flag 3.3** — `skills/skill-builder/rules/` — empty directory, no `index.md`
Directory exists, contains nothing. Not referenced in `skills/skill-builder/index.md`.
**Recommended:** Remove with `git rm -r`. Covered by open handoff.

---

### Check 4 — Duplicate / Near-Duplicate Files

---

**Flag 4.1** — `crypt-keeper.md` (vault root) vs `skills/crypt-keeper/procedure.md`
Root file is a dead redirect stub. Actual procedure correctly located at `skills/crypt-keeper/procedure.md`. Same as Flag 2.1.
**Covered by:** open handoff `2026-04-08-fix-orphaned-index-entries.md` (Task 3).

---

### Check 5 — Stale Status Flags

**None.** All launch dates future-dated as of 2026-04-08.

| KR | Next date | Current status |
| :--- | :--- | :--- |
| Notes Datagrid (GA live) | 2026-04-09 | ⏳ Pending — not yet past |
| Notes WLV (Beta) | 2026-06-25 | ⏳ Future |
| Notes WLV (GA) | 2026-07-27 | ⏳ Future |
| Locked/Signed Notes (Beta) | 2026-07-27 | ⏳ Future |
| Service Plan Datagrid (GA) | 2026-05-28 | ⏳ Future |
| Bulk Import Notes (GA) | 2026-07-13 | ⏳ Future |

> **⚠️ Watch item (next run):** Notes Datagrid GA goes live **2026-04-09**. Q2 baseline pull window opens then. Next run (2026-04-15) should verify `2026-q2-kr-reference.md` has a confirmed baseline value replacing `⏳ Pending first full-month GA pull`.

---

### Check 6 — data_sources.md Sync

Both flags covered by open handoff `2026-04-08-fix-data-sources-and-agents.md`.

---

**Flag 6.1** — `DB / external_user_invitations` not inventoried in `data_sources.md`
Referenced in `2026-q2-kr-reference.md` (Portal Invitations Sent, Invitation Acceptance, Person Profile Updates). Missing from inventory.

Suggested addition — new **Database (Direct)** section:
```markdown
### Database (Direct) — Portal KRs
| Table / Source | Used For | KR | Status |
| :--- | :--- | :--- | :--- |
| `external_user_invitations` | Invitation sent/accepted counts | Portal — Invitations Sent, Invitation Acceptance | 🛑 Blocked |
| Session data (TBD) | Person login confirmation | Portal — Invitation Acceptance | 🛑 Blocked |
```

---

**Flag 6.2** — `GA /portal page view (proxy)` not in `data_sources.md`
Referenced in `2026-q2-kr-reference.md` (Portal — Invitation Acceptance) as proxy source. Missing from GA events table.

Suggested addition to GA table:
```
| `/portal` page view (proxy) | Proxy — portal login confirmation (URL-based) | Portal — Invitation Acceptance |
```

> Both 6.1 and 6.2 are for `🛑 Blocked` KRs — low urgency, but inventory these now so they're ready when Portal unblocks.

---

### Check 7 — AGENTS.md Compliance Spot-Check

**3 most recently modified files** (by mtime, excluding `skills/crypt-keeper/reports/`):

| File | Path OK | Indexed | Naming OK | Violation |
| :--- | :--- | :--- | :--- | :--- |
| `skills/handoff/index.md` | ✅ | ✅ (listed as `handoff/` in `skills/index.md`) | ✅ | None |
| `skills/crypt-keeper/SKILL.md` | ✅ | ❌ Not in `crypt-keeper/index.md` | ⚠️ See note | Flag 7.1 = Flag 1.1 |
| `skills/casebook/admin/index.md` | ✅ | ✅ (listed as `admin/` in `casebook/index.md`) | ✅ | None |

---

**Flag 7.1** — `skills/crypt-keeper/SKILL.md` not listed in `skills/crypt-keeper/index.md`
Same as Flag 1.1. Covered by open handoff `2026-04-08-fix-orphaned-index-entries.md`.

**Naming note:** `SKILL.md` uses all-caps. AGENTS.md does not document this as an explicit exemption, creating a false-positive risk in future Crypt-Keeper runs. Covered by open handoff `2026-04-08-fix-data-sources-and-agents.md`.

---

## 📊 Vault Stats

| Metric | Count |
| :--- | :--- |
| Total .md files scanned | 46 |
| Top-level skill dirs with `index.md` | 8 / 8 |
| Sub-subdirectories missing `index.md` | 3 (`mappings/`, `styles/`, `rules/`) |
| Files orphaned from index | 4 |
| Root-level violations (AGENTS.md) | 3 (`crypt-keeper.md`, `CLAUDE.md`, `README.md`) |
| Stale status flags | 0 |
| data_sources.md gaps | 2 |
| AGENTS.md compliance violations | 1 (Flag 7.1 = Flag 1.1) |
| Open handoffs from prior run | 5 |
| Net new flags this run | 2 (Flags 2.2, 2.3) |

---

## 🔜 Suggested Next Actions

**P1 — agent navigation (open handoffs):**
- Fix `casebook/reporting/index.md` — 8 files invisible → `2026-04-08-fix-casebook-reporting-index.md`
- Add `SKILL.md` + `changelog.md` to `crypt-keeper/index.md` → `2026-04-08-fix-orphaned-index-entries.md`
- Add `changelog.md` to `okr-reporting/index.md` → `2026-04-08-fix-orphaned-index-entries.md`

**P2 — structural violations:**
- Delete `crypt-keeper.md` root stub → `2026-04-08-fix-orphaned-index-entries.md`
- Move `reports/` to `skills/crypt-keeper/reports/` → `2026-04-08-p2-move-reports-into-crypt-keeper.md`
- Add `index.md` to `mappings/`, `styles/`; remove `rules/` → `2026-04-08-fix-skill-builder-subdirs.md`
- **NEW:** Confirm `CLAUDE.md` intent → add to AGENTS.md exemptions or delete (Flag 2.2)
- **NEW:** Add `README.md` to AGENTS.md root exemptions (Flag 2.3)

**P3 — data quality (open handoffs):**
- Add Portal sources to `data_sources.md` → `2026-04-08-fix-data-sources-and-agents.md`
- Document `SKILL.md` naming exemption in `AGENTS.md` → `2026-04-08-fix-data-sources-and-agents.md`

**Watch (next run 2026-04-15):**
- Verify Notes Datagrid April baseline pulled and recorded in `2026-q2-kr-reference.md`
- Verify all 5 open handoffs have moved to `handoff/complete/`
