# Crypt-Keeper Procedure — Vault Quality Checks

> [!NOTE]
> ⚙️ **STATUS:** Active — v1.0 (2026-04-08)
> **Run by:** Claude (Cowork), scheduled every Monday at 9am
> **Does not auto-fix** — produces a flagged report only
> **Output:** `/Users/benbelanger/GitHub/ben-cp/reports/cleanup-report-[YYYY-MM-DD].md`

---

## 🎯 Goal

Catch structural drift introduced by any agent session (Gemma, Gemini, Claude
Code) since the last run. Produce a clear, actionable report for Ben's review.
Never modify, move, or delete vault files — flag only.

---

## 📋 Pre-Flight

Before running any checks:

1. Read `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — confirms current vault
   structure and naming rules
2. Confirm `/Users/benbelanger/GitHub/ben-cp/reports/` directory exists —
   create it if not (write a `.gitkeep` stub)
3. Note today's date for the report filename

---

## 🗺️ Checks (Run in Order)

### Check 1 — Orphaned Files
List all `.md` files under `skills/`. For each file, verify it is referenced in
its parent directory's `index.md`. Flag any file that has no index entry.

**Output:** file path + suggested index.md entry text

---

### Check 2 — Misplaced Files
List `.md` files sitting directly at `skills/` root (not inside a subdirectory).
Flag any that appear to be KR-specific SOPs or skill documents — they should
be in a subdirectory.

**Output:** file path + suggested correct destination

---

### Check 3 — Missing `index.md`
For each subdirectory under `skills/`, confirm `index.md` exists. Report any
subdirectory missing one. Draft a starter `index.md` for each gap found and
include it in the report as a suggested fix (do not write it — Ben approves
first).

**Output:** directory path + drafted starter index.md content

---

### Check 4 — Duplicate / Near-Duplicate Files
Scan for files with similar names across the entire vault. Flag pairs that
appear to cover the same KR, topic, or skill. Recommend which to keep and
which to archive or delete — but do not act.

**Common pattern to watch for:** files created by Gemma with verbose names
(e.g., `notes_quick_entry_outside_uow_sop.md`) that duplicate a properly named
file (e.g., `notes_quick_entry.md`).

**Output:** file pair + recommendation

---

### Check 5 — Stale Status Flags
Scan all SOP files for these status indicators:
- `🛑 Blocked`
- `🟡 Proxy`
- `⏳ Pending`
- `Pending release`
- `Beta [date]` / `GA [date]`

Cross-reference any dates mentioned against today's date. Flag any item whose
launch date has passed but status has not been updated.

**Output:** file, KR name, original status, suggested updated status

---

### Check 6 — `data_sources.md` Sync
Read `/Users/benbelanger/GitHub/ben-cp/skills/okr-reporting/data_sources.md`.
Cross-reference against all KR-specific SOPs in `okr-reporting/`. Flag any
data source, GA event, or tool mentioned in a KR SOP that is missing from the
master inventory.

**Output:** missing source + which KR SOP references it

---

### Check 7 — `AGENTS.md` Compliance Spot-Check
Identify the 3 most recently modified files in the vault (excluding reports).
For each, verify:
- File is at the correct path per `AGENTS.md` Section 3
- File is referenced in its parent directory's `index.md`
- File naming follows underscore convention (`AGENTS.md` Section 4)

**Output:** file path + any violations found

---

## 📊 Report Output

Write the completed report to:
`/Users/benbelanger/GitHub/ben-cp/reports/cleanup-report-[YYYY-MM-DD].md`

Use the template in `skills/crypt-keeper/report-template.md`.

---

## ⚠️ Constraints

- Read before every write — no exceptions
- Do not delete, move, or modify any vault files
- Do not modify `procedure.md`, `notes_quick_entry.md`, `notes_datagrid_shortcuts.md`,
  or `data_sources.md`
- Use absolute paths starting with `/Users/benbelanger/GitHub/ben-cp/`
- If `AGENTS.md` does not exist (edge case), report as a critical flag and stop

---

## 🔗 References

- Universal agent contract: `/Users/benbelanger/GitHub/ben-cp/AGENTS.md`
- Vault structure: `AGENTS.md` Section 1
- Naming conventions: `AGENTS.md` Section 4
- Report template: `skills/crypt-keeper/report-template.md`
