# SOP: Status Report Orchestrator (Final)

> [!IMPORTANT]
> ⚡ **KICKSTART** — Run from the scripts directory:
>
> ```
> cd project-status-reports/scripts
> python3 full_run.py
> ```
>
> It will print exact instructions for every step, including the exact JQL and save path for each Jira epic. Follow the printed instructions literally.

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

## 🔄 Step 2: Jira Fetch (Agent-Side)

`full_run.py` will pause and print exact instructions when this step is needed. Follow them literally. Summary of what it will ask:

### 2a. For each epic key listed in the pause output:

Call **`searchJiraIssuesUsingJql`** (Atlassian MCP) **once per epic** using the JQL printed for that epic:

```
project = CBP AND issuetype != QAFE AND (
  issuekey = {KEY}
  OR "Epic Link" = {KEY}
  OR parent = {KEY}
) ORDER BY updated DESC
```

Request these fields: `summary, status, assignee, priority, issuetype, parent, timeoriginalestimate, timespent, fixVersions, created, updated`

Max results: 100

### 2b. Save each result to its own file

Each epic gets its own file — **do not merge or overwrite between epics**:

```
inputs/raw/jira/{KEY}.json     e.g.  inputs/raw/jira/CBP-2736.json
```

The file must be a valid JSON array of issue objects.

> [!WARNING]
> **Strict Validation:** The resulting JSON array MUST NOT be empty. If Jira returns 0 issues, stop and check the JQL or credentials before proceeding.

### 2c. After all epics are saved

Run `full_run.py` again — it will detect the raw files and auto-run harvest + synthesis:
```
python3 full_run.py
```

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

**In Progress:** 8 issues · ~12.5d est remaining
- [CBP-3150](https://casecommons.atlassian.net/browse/CBP-3150) — Summary — Tuan · In development · 1.0d est / 0.5d act · P2 · v2.4
```

---

## 🛠️ Tooling Rules (STRICT)

### 1. Mode Detection
- **Single-project mode**: Ben shares an Asana project URL. Pass it as an argument: `python3 full_run.py https://app.asana.com/0/...`
- **Batch mode**: No URL argument. Fetches all Platform team projects (GID `1208820967756799`).

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
- `⚠️ At risk`: Date in future AND previous milestone was ❌.
- `🎯 On track`: Date in future and none of the above.
- `❓ Not set`: Date field is missing.

### 4. Progress Bars
- **Progress**: Real-scale UTF-8. 1 char per ticket. `▓` = Done, `▒` = In Progress, `░` = To Do.
- **Time Balance**: `█████░░░░░ act / est (pct%)`. Use `⚠️` prefix if over budget.

---

## 🔄 Execution Macro (Summary)

```
full_run.py → [pauses] → agent calls searchJiraIssuesUsingJql per epic → full_run.py again
```

1. `full_run.py` — runs step 1 (Asana filter), pauses with exact Jira fetch instructions per epic
2. Agent calls `searchJiraIssuesUsingJql` once per epic, saves each to `inputs/raw/jira/{KEY}.json`
3. `full_run.py` again — detects raw files, auto-runs harvest, renders final report
