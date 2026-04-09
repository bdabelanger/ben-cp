# Vault Cleanup Report — 2026-04-09

> **Run by:** Crypt-Keeper (manual trigger — post-handoff verification)
> **Vault:** `/Users/benbelanger/GitHub/ben-cp`
> **Procedure:** `skills/crypt-keeper/procedure.md`
> **Previous report:** `skills/crypt-keeper/reports/archive/cleanup-report-2026-04-08.md`
> **Action required:** Review flags below and confirm any fixes with Claude Code or Gemma

---

## ✅ Checks Run

- [x] Check 1 — Orphaned Files
- [x] Check 2 — Misplaced Files
- [x] Check 3 — Missing index.md
- [x] Check 4 — Duplicate Files
- [x] Check 5 — Stale Status Flags
- [x] Check 6 — data_sources.md Sync
- [x] Check 7 — AGENTS.md Compliance Spot-Check

---

## ⚠️ Flags Requiring Ben's Review

### Check 1 — Orphaned Files

Eight files are not referenced in their parent directory's `index.md`. Most are `changelog.md` files in skill directories whose `index.md` is a **procedure doc or meta-doc** rather than a proper directory TOC.

**Pattern: index.md ≠ TOC (affects 4 skills)**

The following skill directories have an `index.md` that is a full procedure/SOP document rather than a file-listing TOC. This means new files added to the directory (especially `changelog.md`) are invisible to agent navigation.

| Directory | index.md type | Orphaned files |
| :--- | :--- | :--- |
| `skills/changelog/` | Multi-level changelog procedure | `changelog.md`, `entry_template.md` |
| `skills/project-status-reports/` | Full pipeline runbook | `changelog.md` |
| `skills/rovo/` | Inline SOP text (no Contents table) | `changelog.md`, `rovo-sop.md` |
| `skills/skill-builder/` | "Guide to Documenting Workflows" meta-doc | `changelog.md` |

**Suggested fix pattern** — for each, either:
- **(A)** Prepend a `## 📋 Contents` table to the existing `index.md` listing all files, OR
- **(B)** Rename the current `index.md` to a descriptive name (e.g., `procedure.md`, `guide.md`) and create a new minimal TOC `index.md`

**Additional orphan:**

| File | Issue | Suggested index.md entry |
| :--- | :--- | :--- |
| `skills/casebook/changelog.md` | `casebook/index.md` only lists subdirectories, not files in root of `casebook/` | `\| \`changelog.md\` \| Detail log for this skill \|` |

**Lower priority — pipeline data artifacts (not SOP files):**
- `skills/project-status-reports/inputs/archive/archived_*.md` (6 files) — these are archived pipeline input reports, not SOP documents. No index entry needed, but directory has no index.md (see Check 3).

---

### Check 2 — Misplaced Files

**None.** `skills/index.md` is a proper master skills index — correctly placed. ✅

---

### Check 3 — Missing `index.md`

**11 subdirectories** under `skills/` are missing an `index.md`. Grouped by urgency:

**P1 — Has .md content, agent will miss it without index:**

| Directory | Content found | Draft index.md |
| :--- | :--- | :--- |
| `skills/project-status-reports/scripts/` | `step_0_jira_instructions.md` | See below |

Starter `index.md` for `skills/project-status-reports/scripts/`:
```markdown
# Project Status Reports: Scripts

> Pipeline scripts for the Platform Weekly Status Report automation.
> Last updated: 2026-04-09

---

## 📋 Contents

| File | Description |
| :--- | :--- |
| `step_0_jira_instructions.md` | Manual Jira fetch instructions (fallback for Step 0) |
| `full_run.py` | Orchestrator — runs full pipeline end-to-end |
| `step_0_asana_refresh.py` | Fetches all active Asana projects |
| `step_1_asana_ingest.py` | Filters to Platform team, extracts stage/status/milestones |
| `step_2_atlassian_fetch.py` | Fetches Jira issues and epic estimates |
| `step_2_rovo_context.py` | Rovo qualitative context enrichment |
| `step_3_jira_harvest.py` | Harvests and transforms Jira data |
| `step_4_report_generator.py` | Generates final Markdown report |
| `platform_report.py` | Platform report rendering |
| `render_html.py` | HTML output rendering |
| `update_manifest.py` | Manifest state management |
```

**P2 — Operational archive dirs with .md files (pipeline inputs):**

| Directory | Content found | Recommendation |
| :--- | :--- | :--- |
| `skills/project-status-reports/inputs/archive/` | 6 archived `.md` status reports | Add a minimal `index.md` noting these are read-only historical runs |

**P3 — Operational pipeline dirs (likely contain only json/html/py, no .md):**

| Directory | Notes |
| :--- | :--- |
| `skills/crypt-keeper/reports/` | Has `.gitkeep` + active report slot — operational, not SOP |
| `skills/crypt-keeper/reports/archive/` | Archive only — operational |
| `skills/lumberjack/reports/` | Empty — operational |
| `skills/project-status-reports/inputs/` | Pipeline dir |
| `skills/project-status-reports/inputs/processed/` | Pipeline dir |
| `skills/project-status-reports/inputs/raw/` | Pipeline dir |
| `skills/project-status-reports/logs/` | Pipeline dir |
| `skills/project-status-reports/outputs/` | Pipeline dir |
| `skills/project-status-reports/tests/` | Pipeline dir |

**Ben's call:** Do the P3 pipeline dirs need `index.md`? Recommend exempting operational pipeline subdirs from Check 3 via an AGENTS.md carve-out, similar to how `reports/` are treated.

---

### Check 4 — Duplicate Files

**None.** No duplicate or near-duplicate files found across 53 scanned `.md` files. ✅

---

### Check 5 — Stale Status Flags

**None.** All `🛑 Blocked`, `⏳ Pending`, and `🟡 Proxy` flags are current:
- **Notes Datagrid** — `⏳ Pending first full-month GA pull (GA live 4/9)` — feature live TODAY; awaiting first month of data. Status accurate.
- **Notes WLV** — `🛑 Blocked` — Beta 6/25. Future. ✅
- **Service Plan Datagrid** — `🛑 Blocked` — GA 5/28. Future. ✅
- **Portal KRs** — `🛑 Blocked` — data model unstable, no date. ✅
- **All other flags** — reviewed, no stale dates. ✅

---

### Check 6 — data_sources.md Sync

**2 sources referenced in KR SOPs are missing from `data_sources.md`:**

| Missing Source | Referenced In | KR |
| :--- | :--- | :--- |
| **Zapier Insights** | `2026-q2-kr-reference.md` | Zapier — Custom Fields |
| **Super Admin `API Access` flag** | `2026-q2-kr-reference.md` | Zapier — Custom Fields |

**Suggested addition to `data_sources.md`** — new section after Casebook Admin Reporting:
```markdown
### Zapier Insights (Exploratory)
Engineering input needed before this source is confirmed usable.

| Source | Used For | KR | Status |
| :--- | :--- | :--- | :--- |
| Zapier Insights dashboard | Zapier integration usage by tenant | Zapier — Custom Fields | 🛑 Blocked — Engineering input needed |
| Super Admin `API Access` flag (tenants table) | Zapier entitlement verification | Zapier — Custom Fields | 🛑 Blocked — field location unconfirmed |
```

---

### Check 7 — AGENTS.md Compliance Spot-Check

**3 most recently modified files** (excluding reports):
1. `changelog.md` (root) — ✅ correct placement, correct naming, root document
2. `handoff/complete/2026-04-08-p2-crypt-keeper-root-exemptions-COMPLETE.md` — ✅ correct placement, kebab-case per handoff convention
3. `handoff/complete/2026-04-08-fix-data-sources-and-agents-COMPLETE.md` — ✅ correct placement, kebab-case per handoff convention

**No violations found.** ✅

---

## 📊 Vault Stats

| Metric | Count |
| :--- | :--- |
| Total .md files scanned | 53 |
| Directories with index.md | 15 / 26 total |
| Files orphaned from index | 8 |
| Misplaced files | 0 |
| Stale status flags | 0 |
| data_sources.md gaps | 2 |
| AGENTS.md violations | 0 |

**vs. Previous run (2026-04-08):** 13 total flags → **10 total flags this run**. All P1 flags from prior run resolved. Remaining flags are structural patterns (index.md-as-procedure-doc) and one data_sources gap.

---

## 🔜 Suggested Next Actions

**P1:**
1. `skills/project-status-reports/scripts/` — create `index.md` (draft above)

**P2:**
2. `skills/rovo/` — restructure: rename `index.md` → `rovo-sop.md` procedure (or merge), create proper TOC `index.md` listing both files + `changelog.md`
3. `skills/changelog/`, `skills/skill-builder/`, `skills/project-status-reports/` — prepend a `## 📋 Contents` table to existing `index.md` files to cover orphaned `changelog.md` and other files
4. `skills/casebook/index.md` — add `changelog.md` row to the index
5. `skills/project-status-reports/inputs/archive/` — add minimal `index.md` noting these are read-only historical runs
6. **AGENTS.md decision** — add carve-out exempting operational pipeline subdirs (`inputs/`, `logs/`, `outputs/`, `tests/`, `archive/`) from Check 3. Prevents false positives on every Crypt-Keeper run.

**P3:**
7. `data_sources.md` — add Zapier Insights + Super Admin API Access flag section

---

## 🟢 Improvements vs. Prior Run (Verification)

All 6 open flags from `cleanup-report-2026-04-08.md` are now resolved:

| Prior Flag | Status |
| :--- | :--- |
| 1.1 — `skills/crypt-keeper/index.md` missing SKILL.md + changelog.md | ✅ Fixed |
| 1.2 — `skills/okr-reporting/index.md` missing changelog.md | ✅ Fixed |
| 1.3 — Root `crypt-keeper.md` stub | ✅ Deleted |
| 1.4 — `skills/casebook/reporting/index.md` wrong file type | ✅ Fixed — schema_joins.md created, proper TOC in place |
| 3.x — `skill-builder/mappings/`, `styles/` missing index.md | ✅ Fixed |
| 3.x — `skill-builder/rules/` empty dir | ✅ Removed |
| 6.x — Portal data sources missing from data_sources.md | ✅ Fixed |
| Root `reports/` misplacement | ✅ Fixed — moved to `skills/crypt-keeper/reports/` |
