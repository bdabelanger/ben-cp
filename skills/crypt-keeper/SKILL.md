---
name: crypt-keeper
description: Weekly vault quality watchdog for the ben-cp vault. Runs 7 structural checks and produces a flagged report for Ben's review. Use when asked to run crypt-keeper, do a vault check, or audit the ben-cp vault. Never auto-fixes — flags only.
---

# Crypt-Keeper — Vault Quality Watchdog

## Pre-Flight

Before running any checks:
1. Read `AGENTS.md` — confirms current vault structure and naming rules
2. Confirm `reports/` directory exists — create it with a `.gitkeep` stub if not
3. Note today's date for the report filename

All paths are absolute: `/Users/benbelanger/GitHub/ben-cp/`

---

## Checks (Run in Order)

### Check 1 — Orphaned Files
List all `.md` files under `skills/`. For each, verify it is referenced in its
parent directory's `index.md`. Flag any with no index entry.

**Output:** file path + suggested index.md entry text

### Check 2 — Misplaced Files
List `.md` files sitting directly at `skills/` root (not in a subdirectory).
Flag any that appear to be KR-specific SOPs or skill documents.

**Output:** file path + suggested correct destination

### Check 3 — Missing index.md
For each subdirectory under `skills/`, confirm `index.md` exists. Draft a
starter `index.md` for any gap found — include in report, do not write it.

**Output:** directory path + drafted starter index.md content

### Check 4 — Duplicate / Near-Duplicate Files
Scan for files with similar names across the vault. Flag pairs covering the
same KR, topic, or skill. Recommend which to keep — do not act.

**Output:** file pair + recommendation

### Check 5 — Stale Status Flags
Scan all skill files for: `🛑 Blocked`, `🟡 Proxy`, `⏳ Pending`,
`Beta [date]`, `GA [date]`. Cross-reference dates against today. Flag any
whose launch date has passed but status hasn't been updated.

**Output:** file, KR name, current status, suggested update

### Check 6 — data_sources.md Sync
Read `skills/okr-reporting/data_sources.md`. Cross-reference against all KR
SOPs in `okr-reporting/`. Flag any data source or GA event mentioned in a KR
SOP that is missing from the inventory.

**Output:** missing source + which KR SOP references it

### Check 7 — AGENTS.md Compliance Spot-Check
Identify the 3 most recently modified files in the vault (excluding reports/).
For each, verify:
- Correct path per AGENTS.md file placement rules
- Referenced in parent directory's index.md
- Filename uses underscores (not hyphens or camelCase)

**Output:** file path + any violations found

---

## Report Output

Write the completed report to:
`/Users/benbelanger/GitHub/ben-cp/reports/cleanup-report-[YYYY-MM-DD].md`

Use the template at `skills/crypt-keeper/report-template.md`.

---

## Constraints

- Read before every write — no exceptions
- Never delete, move, or modify vault files
- Use absolute paths starting with `/Users/benbelanger/GitHub/ben-cp/`
- If AGENTS.md does not exist, stop and report as a critical blocker
