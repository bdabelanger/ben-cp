# Vault Cleanup Report — 2026-04-08

> **Run by:** Crypt-Keeper (scheduled Claude task)
> **Vault:** `/Users/benbelanger/GitHub/ben-cp`
> **Procedure:** `skills/crypt-keeper/procedure.md`
> **Action required:** Review flags below and confirm any fixes with Claude Code or Gemma

---

## ✅ Checks Passed

- [x] Check 1 — Orphaned Files ⚠️ 4 flags
- [x] Check 2 — Misplaced Files ✅ Clean
- [x] Check 3 — Missing index.md ⚠️ 3 flags
- [x] Check 4 — Duplicate Files ⚠️ 1 flag
- [x] Check 5 — Stale Status Flags ✅ Clean
- [x] Check 6 — data_sources.md Sync ⚠️ 2 flags
- [x] Check 7 — AGENTS.md Compliance Spot-Check ⚠️ 1 flag

---

## ⚠️ Flags Requiring Ben's Review

### Check 1 — Orphaned Files

Files present in a directory but **not listed in that directory's `index.md`**:

---

**Flag 1.1**
`skills/crypt-keeper/SKILL.md`
Not listed in `skills/crypt-keeper/index.md`. The index lists `index.md`, `procedure.md`, and `report-template.md` — `SKILL.md` and `changelog.md` are absent.

Suggested entry for `skills/crypt-keeper/index.md`:
```
| `SKILL.md` | Cowork skill descriptor — triggers Crypt-Keeper from Cowork sessions |
| `changelog.md` | Detail log for this skill — all structural changes |
```

---

**Flag 1.2**
`skills/crypt-keeper/changelog.md`
Not listed in `skills/crypt-keeper/index.md`. (Same gap as 1.1 — both files missing from the index table.)

---

**Flag 1.3**
`skills/okr-reporting/changelog.md`
Not listed in `skills/okr-reporting/index.md`. The index table covers `procedure.md`, `data_sources.md`, `2026-q2-kr-reference.md`, `notes_datagrid_shortcuts.md`, and `notes_quick_entry.md` — but `changelog.md` is present in the directory and unindexed.

Suggested entry for `skills/okr-reporting/index.md`:
```
| `changelog.md` | Detail log for this skill — all structural changes |
```

---

**Flag 1.4**
`skills/casebook/reporting/` — multiple files not listed in `index.md`
The file at `skills/casebook/reporting/index.md` is a "Schema Relationships & Data Joins" reference doc, not a proper directory index. The following files in that directory have no index entry:
- `casebook-cases.md`
- `casebook-intake.md`
- `casebook-people.md`
- `casebook-tenants.md`
- `casebook-users.md`
- `reveal_bi_syntax.md`
- `reveal_bi_visualizations.md`
- `changelog.md`

Additionally, the file contains a broken path reference:
- `casebook-reporting/reveal_bi_syntax.md` should be `casebook/reporting/reveal_bi_syntax.md`

**Recommendation:** Replace `skills/casebook/reporting/index.md` with a proper directory index (table of contents) and promote the schema joins content to a standalone file (e.g., `schema_joins.md`). Suggested replacement index:

```markdown
# Skill: Casebook Reporting

> Reveal BI reference docs and Casebook entity schemas.
> Last updated: [date]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `index.md` | This file |
| `schema_joins.md` | Core join map and BI modeling strategy |
| `reveal_bi_syntax.md` | Query syntax reference for Reveal BI |
| `reveal_bi_visualizations.md` | Visualization and output formatting |
| `casebook-cases.md` | Case entity schema and key fields |
| `casebook-intake.md` | Intake entity schema |
| `casebook-people.md` | Person entity schema |
| `casebook-tenants.md` | Tenant entity schema — use for tenant segmentation |
| `casebook-users.md` | User entity schema — use for user-level metrics |
| `changelog.md` | Detail log for this subdirectory |
```

---

### Check 2 — Misplaced Files

None. The only `.md` file at `skills/` root is `index.md`, which is correct.

> **Note:** `crypt-keeper.md` exists at the **vault root** (not `skills/`). It is a redirect stub pointing to `skills/crypt-keeper/procedure.md`. See Check 4 for disposition recommendation.

---

### Check 3 — Missing index.md

**Flag 3.1**
`skills/skill-builder/mappings/` — no `index.md`
Contains `status_mapping.md`. Referenced by multiple KR SOPs and `skills/skill-builder/index.md` but has no directory index of its own.

Suggested starter `index.md`:
```markdown
# Skill Builder: Mappings

> Reusable business logic and transformation rules.
> Last updated: [date]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `status_mapping.md` | Status string → Green/Yellow/Red mapping logic |
```

---

**Flag 3.2**
`skills/skill-builder/styles/` — no `index.md`
Contains `emoji_key.md`. Referenced by multiple KR SOPs and `skills/skill-builder/index.md` but has no directory index.

Suggested starter `index.md`:
```markdown
# Skill Builder: Styles

> Visual presentation standards — emoji keys, progress bars, formatting.
> Last updated: [date]

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `emoji_key.md` | Standard emoji usage across all skill outputs |
```

---

**Flag 3.3**
`skills/skill-builder/rules/` — no `index.md` and directory is empty
This directory is listed in `skills/skill-builder/index.md` by implication (the index references `mappings/` and `styles/` but not `rules/`). The directory exists but contains nothing.

**Recommendation:** Either add a stub `index.md` to mark intent, or remove the empty directory. Flag for Ben to decide.

---

### Check 4 — Duplicate Files

**Flag 4.1**
`crypt-keeper.md` (vault root) vs `skills/crypt-keeper/procedure.md`

The vault root file is a redirect stub with 151 bytes of content:
```
# crypt-keeper.md — MOVED
> This file is a redirect stub. Full content lives at:
> **`skills/crypt-keeper/procedure.md`**
```

The actual procedure lives correctly at `skills/crypt-keeper/procedure.md`.

**Recommendation:** The root stub is no longer needed now that `SKILL.md` and `index.md` in `skills/crypt-keeper/` handle discovery. Ben should confirm deletion of `crypt-keeper.md` at vault root. Per `AGENTS.md`: "Never create files at vault root (except `AGENTS.md`, `GEMMA.md`, `changelog.md`)." This file violates that rule.

---

### Check 5 — Stale Status Flags

None. All launch dates in `2026-q2-kr-reference.md` and KR SOPs are future-dated as of 2026-04-08:

| KR | Next date | Status |
| :--- | :--- | :--- |
| Notes Datagrid (GA live) | 2026-04-09 | ⏳ Pending — not yet past |
| Notes WLV (Beta) | 2026-06-25 | ⏳ Future |
| Notes WLV (GA) | 2026-07-27 | ⏳ Future |
| Locked/Signed Notes (Beta) | 2026-07-27 | ⏳ Future |
| Service Plan Datagrid (GA) | 2026-05-28 | ⏳ Future |
| Bulk Import Notes (GA) | 2026-07-13 | ⏳ Future |

> **Watch item:** Notes Datagrid GA goes live **tomorrow (2026-04-09)**. The first April baseline pull window opens then. No flag required today — but the next Crypt-Keeper run (2026-04-14) should verify that `2026-q2-kr-reference.md` has been updated to reflect `⏳ Pending first pull` → a confirmed baseline value.

---

### Check 6 — data_sources.md Sync

**Flag 6.1**
`DB / external_user_invitations` table — referenced in `2026-q2-kr-reference.md` for three Portal KRs (Portal Invitations Sent, Invitation Acceptance, Person Profile Updates) but **not inventoried** in `skills/okr-reporting/data_sources.md`.

- KR SOP reference: `2026-q2-kr-reference.md` — Portal KRs section
- Suggested addition to `data_sources.md` under a new **Database (Direct)** section:

```markdown
### Database (Direct)
Delegated query via Data team. Used for Portal KRs pending data model confirmation.

| Table / Source | Used For | KR |
| :--- | :--- | :--- |
| `external_user_invitations` | Invitation sent/accepted counts | Portal — Invitations Sent, Invitation Acceptance |
| Session data (TBD) | Person login confirmation | Portal — Invitation Acceptance |
```

---

**Flag 6.2**
`GA /portal page view (proxy)` — referenced in `2026-q2-kr-reference.md` for the Portal Invitation Acceptance KR as a proxy source, but not listed in `data_sources.md` GA events table.

- KR SOP reference: `2026-q2-kr-reference.md`, Portal — Invitation Acceptance section
- Suggested addition to the Google Analytics table in `data_sources.md`:

```markdown
| `/portal` page view (proxy) | Proxy — Portal login confirmation | ⚠️ Not a formal GA event — URL-based; confirm with Engineering | Portal — Invitation Acceptance |
```

> **Note:** Both flags 6.1 and 6.2 are for Portal KRs that are currently `🛑 Blocked` pending data model confirmation. Low urgency — but inventory should be kept current even for blocked KRs so the sources are documented when they unblock.

---

### Check 7 — AGENTS.md Compliance Spot-Check

The 3 most recently modified files (excluding `reports/`):

| File | Modified | Path OK | Indexed | Naming OK |
| :--- | :--- | :--- | :--- | :--- |
| `skills/crypt-keeper/SKILL.md` | 2026-04-08 16:27 | ✅ | ❌ Not in `crypt-keeper/index.md` | ⚠️ See note |
| `skills/casebook/admin/index.md` | 2026-04-08 16:15 | ✅ | ✅ Listed as `admin/` in `casebook/index.md` | ✅ |
| `skills/project-status-reports/index.md` | 2026-04-08 15:32 | ✅ | ✅ Listed in `skills/index.md` | ✅ |

**Flag 7.1**
`skills/crypt-keeper/SKILL.md` — not referenced in `skills/crypt-keeper/index.md`.
This is the same finding as Flag 1.1. File is correctly placed but orphaned from its directory index.

**Naming note:** `SKILL.md` uses all-caps rather than the underscore convention (`AGENTS.md` Section 4). This appears to be a Cowork-specific convention for skill descriptors (similar to `AGENTS.md` itself). No action needed on naming — but worth Ben confirming whether `SKILL.md` files should be treated as exempt from the underscore rule, and whether that exception should be documented in `AGENTS.md`.

---

## 📊 Vault Stats

| Metric | Count |
| :--- | :--- |
| Total .md files scanned | ~40 |
| Skill directories with index.md | 8 / 8 (top-level) |
| Sub-subdirectories missing index.md | 3 (mappings/, styles/, rules/) |
| Files orphaned from index | 4 |
| Misplaced files | 0 |
| Root-level violations (AGENTS.md) | 1 (`crypt-keeper.md`) |
| Stale status flags | 0 |
| data_sources.md gaps | 2 |
| AGENTS.md compliance violations | 1 (same as Flag 1.1) |

---

## 🔜 Suggested Next Actions

- **High priority:** Fix `skills/casebook/reporting/index.md` — current content is a schema joins reference doc masquerading as a directory index. Eight files in that directory are invisible to any agent that relies on the index (Flag 1.4). Assign to Claude Code.

- **Medium priority:** Add `SKILL.md` and `changelog.md` to `skills/crypt-keeper/index.md` (Flags 1.1, 1.2, 7.1). Quick edit.

- **Medium priority:** Add `changelog.md` to `skills/okr-reporting/index.md` (Flag 1.3). Quick edit.

- **Medium priority:** Delete `crypt-keeper.md` at vault root — it violates the AGENTS.md rule against root-level files and is now a dead stub (Flag 4.1). Ben confirms, Claude Code deletes.

- **Low priority:** Add starter `index.md` to `skills/skill-builder/mappings/` and `skills/skill-builder/styles/` (Flags 3.1, 3.2). Decide whether to keep or remove the empty `rules/` directory (Flag 3.3).

- **Low priority:** Add Portal DB sources and `/portal` page view proxy to `data_sources.md` (Flags 6.1, 6.2). Unblocks together with Portal data model confirmation — no rush.

- **Low priority:** Confirm whether `SKILL.md` files are exempt from the underscore naming convention and document the exception in `AGENTS.md` if so (Flag 7.1 naming note).

- **Watch (next run 2026-04-14):** Notes Datagrid GA goes live 2026-04-09. Verify `2026-q2-kr-reference.md` has a confirmed baseline value by next Monday's run.
