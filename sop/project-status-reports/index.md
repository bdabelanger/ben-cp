# SOP: Status Report Orchestrator (Final)

> [!IMPORTANT]
> ⚡ **KICKSTART** — Run from the scripts directory:
>
> **Fresh weekly run (always use this):**
> ```
> python3 project-status-reports/scripts/full_run.py --force
> ```
>
> **Re-render only (Jira data already fresh, just re-generate the report):**
> ```
> python3 project-status-reports/scripts/full_run.py
> ```
>
> `--force` wipes stale Jira cache and resets the manifest before running. Without it, the pipeline skips re-fetching if processed data already exists from a previous run.
>
> The pipeline runs fully automated — no agent tool calls required. Ensure `JIRA_USER_EMAIL` and `JIRA_API_TOKEN` are exported before running.

---

## Goal
Manage the multi-step relay for the Platform Weekly Status report using `manifest.json` as the state-of-record.

---

## 🔄 Step 2: Jira Fetch (Automated via Script)

This step has been fully automated to avoid LLM context-window limits. When `full_run.py` executes, it will automatically call `step_2_atlassian_fetch.py`.

It securely uses standard Atlassian API tokens to run the necessary JQL queries for any missing epics and writes the data directly to disk:

```
inputs/raw/jira/{KEY}.json     e.g.  inputs/raw/jira/CBP-2736.json
```

> [!IMPORTANT]
> **Credentials Required**
> Before executing the pipeline, the environment must have the following variables exported:
> `JIRA_USER_EMAIL` (e.g. benbelanger@casebook.net)
> `JIRA_API_TOKEN` (the Atlassian API token)
>
> If the Jira fetch step throws a 401 or 403 HTTP error, the pipeline will fail hard. Check these environment credentials before running!

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
python3 project-status-reports/scripts/full_run.py --force
```

The orchestrator handles the entire pipeline autonomously end-to-end:
1. `--force` wipes `inputs/raw/jira/` and resets the manifest (archives old processed files).
2. `full_run.py` invokes Step 1 (Asana Ingest).
3. `full_run.py` invokes Step 2 (Jira Fetch) automatically via `requests` — fetches child issues per epic using `parent in (KEY)` JQL.
4. `full_run.py` cascades into Step 3 (Harvest) and Step 4 (Report Generation).
3. `full_run.py` automatically cascades into Step 3 (Harvest) and Step 4 (Report Generation).
