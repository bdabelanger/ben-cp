# SOP: Status Report Orchestrator (Final)

> [!IMPORTANT]
> ⚡ **KICKSTART** — Run from the repo root:
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
> The pipeline runs fully automated — no agent tool calls required. Requires `ASANA_API_TOKEN`, `ATLASSIAN_USER_EMAIL`, and `ATLASSIAN_API_TOKEN` in the environment (loaded from `.env` at repo root).

---

## Goal
Manage the multi-step relay for the Platform Weekly Status report using `manifest.json` as the state-of-record.

---

## 🔄 Step 0: Asana Refresh (Automated via Script)

`full_run.py` automatically calls `step_0_asana_refresh.py` at the start of every run. It fetches all active projects for the Product team from the Asana API and writes them to:

```
inputs/raw/asana_all_projects.json
```

The script paginates automatically and pulls the full custom fields payload needed by Step 1 (Stage, Team, JIRA Link, milestones, etc.).

**Failure behavior:** If Step 0 fails (e.g. bad token), the pipeline logs a warning and continues with the existing cached file — it is non-fatal as long as `asana_all_projects.json` exists.

> [!IMPORTANT]
> **Credentials Required**
> `ASANA_API_TOKEN` — your Asana personal access token (`.env` at repo root)
>
> If Step 0 throws a 401, verify your token at app.asana.com → Profile → Apps → Personal access tokens.

---

## 🔄 Step 2: Jira Fetch (Automated via Script)

This step has been fully automated to avoid LLM context-window limits. When `full_run.py` executes, it will automatically call `step_2_atlassian_fetch.py`.

It securely uses standard Atlassian API tokens to run the necessary JQL queries for any missing epics and writes the data directly to disk:

```
inputs/raw/jira/{KEY}.json        e.g.  inputs/raw/jira/CBP-2736.json
inputs/raw/jira/{KEY}_epic.json   e.g.  inputs/raw/jira/CBP-2736_epic.json
```

The `_epic.json` file contains the epic-level `timeoriginalestimate` used by the time balance bar.

> [!IMPORTANT]
> **Credentials Required**
> The environment must have the following variables set (via `.env` at repo root):
> `ATLASSIAN_USER_EMAIL` — your Atlassian account email
> `ATLASSIAN_API_TOKEN` — your Atlassian API token
>
> If the fetch step throws a 401 or 403 HTTP error, the pipeline will fail hard. Verify these credentials before running.

---

## 🖼️ Reference Output (Sample)
*Use this as the "puzzle on the box" — your final output should mirror this level of detail and formatting.*

```markdown
# Platform Weekly Status — April 5, 2026

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
1. [Notes - Notes datagrid](...) ([CBP-2736](...)) is in **GA** — 18 done · 8 in progress · 4 to do.
2. [Services - Service plan datagrid](...) ([CBP-3066](...)) is in **Development** — 0 done · 7 in progress · 1 to do.

## 🟢 Active Projects

### [Notes - Notes datagrid](...) · [CBP-2736](...)
33.1d estimated · 18.2d actual · 4.4d remaining (68%)
* ✅ QA Start - Mar 20
* ⚠️ UAT Start - Apr 3
* ⚠️ GA - Apr 9

**Done:** 18 issues
6.0d estimated · 3.5d actual

**In Progress:** 8 issues · ~4.4d est remaining
- [CBP-3150](...) — Full summary text — Tuan
  In development · 1.0d estimated · No actual 👀 · P2 · 2026-4-2
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
- **Ticket progress**: Real-scale UTF-8. 1 char per ticket. `▓` = Done (green), `▒` = In Progress (blue), `░` = To Do (gray).
- **Time balance**: Bar width = `max(epic estimate, actual + remaining)`. Blue = actual, dark blue = remaining (red if projected overage), gray = slack. Label: `Xd estimated · Yd actual · Zd remaining (N%)`. Prefix: `⚠️` if actual alone exceeds estimate, `⚠️` if combined projects to exceed, `👀` at 90–100%.

---

## 🔄 Execution Macro (Summary)

```
python3 project-status-reports/scripts/full_run.py --force
```

The orchestrator handles the entire pipeline autonomously end-to-end:
1. `--force` wipes `inputs/raw/jira/` and resets the manifest (archives old processed files).
2. `full_run.py` invokes **Step 0** (Asana Refresh) — live fetch of all Product team projects into `asana_all_projects.json`. Non-fatal if it fails; falls back to cached file.
3. `full_run.py` invokes **Step 1** (Asana Ingest) — filters to Platform team, extracts stage/status/milestones/jira links.
4. `full_run.py` invokes **Step 2** (Jira Fetch) — fetches child issues and epic-level estimates per CBP key.
5. `full_run.py` cascades into **Step 3** (Harvest) and **Step 4** (Report Generation).
