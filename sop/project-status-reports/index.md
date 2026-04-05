# SOP: Status Report Orchestrator (Final)

> [!IMPORTANT]
> ⚡ **KICKSTART** — Run these in order. Do not skip or reorder.
>
> 1. **Reset**: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/update_manifest.py reset`
> 2. **Identify**: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_1_asana_ingest.py`
> 3. **Fetch**: Perform Step 2 (Jira Fetch) manually — see section below. ⬇️
> 4. **Finish**: `python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_3_jira_harvest.py && python3 /Users/benbelanger/GitHub/ben-cp/project-status-reports/scripts/step_4_report_generator.py`

---

## ⛔ STOP — Read Before Calling Any Tools

These are the only correct tools for this pipeline. Do not substitute.

| Step | Correct Tool | Common Wrong Choices (NEVER USE) |
|------|-------------|----------------------------------|
| Jira fetch | `searchJiraIssuesUsingJql` | `searchAtlassian`, `fetchAtlassian`, `getJiraIssue` |
| Asana data | Already on disk from Step 1 — do not re-fetch via MCP | `get_projects`, `get_items_for_portfolio` |
| Confluence | Not part of this pipeline | `searchAtlassian`, `getConfluencePage` |

If you cannot find `searchJiraIssuesUsingJql` in your available tools, **stop and tell the user**. Do not attempt an alternative.

---

## Goal
Manage the multi-step relay for the Platform Weekly Status report using `manifest.json` as the state-of-record.

---

## 🔄 Step 2: Jira Fetch (Agent-Side — Manual)

This step is performed by the agent, not a script. Complete it between KICKSTART steps 2 and 4.

### 2a. Read the Asana output
Read the file written by Step 1:
`/Users/benbelanger/GitHub/ben-cp/project-status-reports/inputs/processed/asana_active_{TODAY}.json`

Extract all `jira_link` values (format: `CBP-XXXX`). These are your Epic keys.

### 2b. Call `searchJiraIssuesUsingJql`

Use this exact tool: **`searchJiraIssuesUsingJql`** (Atlassian MCP).

Build the JQL from the Epic keys you extracted:

```
project = CBP AND issuetype != QAFE AND (
  issuekey in ({EPIC_KEYS})
  OR "Epic Link" in ({EPIC_KEYS})
  OR parent in ({EPIC_KEYS})
)
ORDER BY updated DESC
```

Replace `{EPIC_KEYS}` with a comma-separated list, e.g.: `CBP-2736, CBP-3066, CBP-3150`

Request these fields: `summary, status, assignee, priority, issuetype, parent, timeoriginalestimate, timespent, fixVersions, created, updated`

Fetch up to 100 issues per call. Paginate if `total > 100`.

### 2c. Save the raw result
Write the full issues array to:
`/Users/benbelanger/GitHub/ben-cp/project-status-reports/inputs/raw/jira_issues.json`

This file must be a valid JSON array. Step 3 reads it directly.

---

## 🖼️ Reference Output (Sample)
*Use this as the "puzzle on the box" — your final output should mirror this level of detail and formatting.*

```markdown
# Platform Weekly Status — April 3, 2026

## ⚙️ Data Quality
**Estimates:** 22 of 37 in-progress issues have estimates (59%)
- Blessing: 9/12 (75%)
- Tuan: 4/5 (80%)
- Bisoye: 4/10 (40%) 👀

**Actuals:** 5 of 27 issues in QA have time tracked (19%)
- Bisoye: 3/9 (33%) 👏
- Blessing: 0/10 (0%) 👀

**Unprioritized:** 9 of 37 👀 in-progress issues have no fix version set (24%)

## 📋 Summary
[Notes - Notes datagrid](...) ([CBP-2736](...)) is in **GA** — 18 done · 8 in progress · 4 to do.
[Services - Service plan datagrid](...) ([CBP-3066](...)) is in **Development** — 0 done · 7 in progress · 1 to do.

## 🟢 Active Projects

### [Notes - Notes datagrid](...) · [CBP-2736](...) · GA
`▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒░░░░ 18 done · 8 in progress · 4 to do`
`█████░░░░░ 18.2d act / 33.1d est (55%)`
* ✅ QA - Mar 20
* ⚠️ UAT - Apr 3
* ⚠️ GA - Apr 9

**In Progress:** 8 issues
- [CBP-3150](...) — Summary — Tuan · In development · 1.0d est / 0.5d act · P2 · 2026-4-2
```

---

## 🛠️ Tooling Rules (STRICT)

### 1. Mode Detection
- **Single-project mode**: Ben shares an Asana project URL. Extract the project GID. Run steps scoped entirely to that project.
- **Batch mode**: No project URL is shared. Fetch all Platform team projects (GID `1208820967756799`).

### 2. Status Category Overrides
- `Blocked - Needs Review` → **To Do**
- `Blocked - Third-Party` → **To Do**
- `QA Revise` → **In Progress**
- Exclude `QAFE` issue types from all counts.

### 3. Milestone Status Logic
Evaluate each milestone against today's date AND current Asana Stage:
Rank: `Development=1 → In QA=2 → In UAT=3 → Beta=4 → GA=5`
- `✅ Passed, hit`: Date in past AND current stage rank ≥ milestone's required rank.
- `❌ Passed, missed`: Date in past AND current stage rank < milestone's required rank.
- `⚠️ At risk`: Date in future AND (previous was ❌ OR unassigned proximity).
- `🎯 On track`: Date in future and none of the above.
- `❓ Not set`: Date field is missing.

### 4. Progress Bars
- **Progress**: Real-scale UTF-8. 1 char per ticket. `▓` = Done, `▒` = In Progress, `░` = To Do.
- **Time Balance**: `█████░░░░░ act / est (pct%)`. Use `⚠️` prefix if over budget.

---

## 🔄 Execution Macro (Summary)

```
Step 1 (script) → Step 2 (agent: searchJiraIssuesUsingJql) → Step 3+4 (script)
```

1. `update_manifest.py reset` — clears state
2. `step_1_asana_ingest.py` — filters active Platform projects to disk
3. **Agent reads Asana output → calls `searchJiraIssuesUsingJql` → writes `inputs/raw/jira_issues.json`**
4. `step_3_jira_harvest.py` — cross-references Jira issues against active Asana epics
5. `step_4_report_generator.py` — renders final Markdown report
