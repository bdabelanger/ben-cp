---
title: Dream Cycle — Skill
type: skill
domain: skills/dream
---


# Dream Cycle — Skill

> **Trigger:** Nightly automated run (22:00) or manual invocation
> **Agent:** Cowork (Claude)
> **Purpose:** Run all repo health sensors, triage findings, fix low-risk issues directly, and create handoffs for Code/Cowork (avoiding Asana tasks).

---

## Overview

The Dream cycle is the repo's nightly health loop. It runs all sensors against the repo, analyzes results, routes work to the right destination, then harvests fresh data (tasks, status, intelligence) so everything is current by morning. Ben's briefing is a `Dream Report` handoff waiting for him when he signs in.

Terminal output during the run stays terse — no narration until the final handoff is written.

---

## Step 1 — Generate the Report

```
generate_report(skill='dream')
```

Runs all sensors and writes results to `reports/dream/`.

---

## Step 2 — Read the Report

```
get_report(path='dream/report.md')
```

Read the summary first, then pull individual sensor JSONs for any WARN or FAIL sensors:

| Sensor | Path | What it checks |
| :----- | :--- | :------------- |
| pulse | `dream/pulse.json` | Directories missing `index.md` |
| links | `dream/links.json` | Broken internal references (ghost links) |
| frontmatter | `dream/frontmatter.json` | Missing or malformed frontmatter |
| drift | `dream/drift.json` | Unsanctioned directories |
| handoffs | `dream/handoffs.json` | Handoff structural issues |
| index | `dream/index.json` | Shadow files and ghost refs in indexes |
| agents | `dream/agents.json` | Unknown agent references |
| tasks | `dream/tasks.json` | Task file audit |
| changelog | `dream/changelog.json` | Changelog currency |
| context | `dream/context.json` | Large files / token risk |
| access | `dream/access.json` | Recently touched files |

---

## Step 3 — Check for a Prior Run

Call `list_handoffs(status='READY')` and check if a `Dream Report` handoff already exists from today. If one does:
- Review what handoffs and Asana tasks were already created
- Only act on new findings not already covered
- Archive the prior Dream Report before writing your own: mark it complete with summary `"Superseded by current run"`

---

## Step 4 — Triage

For each WARN or FAIL sensor, read the full JSON and sort every finding into one of three buckets:

### Bucket A — Fix directly
Low-risk, deterministic corrections with no downstream risk:
- Stale index entries pointing to moved files
- Minor metadata fixes on intelligence records
- Missing `index.md` files that are trivially creatable (stub only)
- Frontmatter field corrections (wrong type, empty required field)
- Root changelog sync (summarizing completed handoffs)

### Bucket B — Handoff for Code
Anything touching more than ~3 files, requiring script changes, or needing a PR:
- Ghost link cleanup (bulk path corrections)
- Structural violations in agent or handoff files
- Directory boundary issues (drift)
- Sensor logic fixes

### Bucket C — Handoff for Cowork (Human Decision Required)
Decisions or risks that require human judgment. Create a P2 handoff for Cowork instead of an Asana task:
- Files over 750KB needing archival decisions
- Ambiguous drift (unsanctioned dirs that might be intentional)
- Sensor failures with no clear explanation
- Systemic patterns Ben should know about

---

## Step 5 — Execute Direct Fixes (Bucket A)

Use ben-cp MCP tools to apply corrections. Log each fix for the Dream Report handoff.

---

## Step 6 — Create Handoffs for Code (Bucket B)

Use `add_handoff` for each discrete fix area.

**Handoff standards:**
- `title` — imperative, specific. **Plain hyphens only — no em-dashes, en-dashes, or special characters, no slashes**
- `priority` — P1 for broken sensors, P2 for structural issues, P3 for housekeeping
- `assigned_to` — Code
- Body must include: Context, Goal, Execution Steps, Verification checklist
- Max 5 handoffs per run — group related issues

**Naming examples:**
✅ `Fix Ghost Links in Q2 Project Intelligence`
✅ `Add Missing Index Files to 14 Directories`
❌ `Fix Ghost Links — intelligence/` (em-dash, slash)
❌ `Fix Ghost Links - intelligence/` (space-hyphen-space causes triple-dash in filename)

---

## Step 7 — Create Handoffs for Cowork (Bucket C)

- Assign to Cowork
- Priority: P2
- Use the imperative slug: `Decide: [Specific Risk]`
- Include enough context to act without re-reading sensor data

---

## Step 8 — Verify (Optional)

If you made direct fixes, re-run `generate_report(skill='dream')` and confirm the relevant sensor improved. Note before/after counts in the Dream Report.

---

## Step 9 — Harvest Fresh Data

All four pipelines (status, tasks, intelligence harvest, intelligence scan) run automatically inside `generate_report`. You do not need to run any of them manually.

Log any pipeline failures surfaced in the Dream Report. Do not block on failures — note and move on.

---

## Step 10 — Intelligence Refresh

After the harvest, scan for intelligence records with missing or stale source files:

```
python3 skills/intelligence/run.py --scan
```

For each orphaned source file found:
- If it has an obvious matching intelligence record → flag in Dream Report for Code to link
- If it has no matching record → create a handoff for Code to parse and ingest it (counts toward the 5 handoff cap)

---

## Step 11 — Write the Dream Report Handoff

Create one final handoff using `add_handoff`:

- **title:** `Dream Report` (no date — the filename prefix handles it)
- **assigned_to:** Code
- **priority:** P1

The handoff should be professional and concise — no narrative, no prose. Use the following structure:

---

### NREM — For Cowork

*Authored by Cowork. This section is the cycle record — not for Code to act on.*

**Sensor Summary** — table with columns: Sensor, Status, Detail. One row per sensor.

**Direct Fixes Applied** — bulleted list of any Bucket A fixes made during the run, or "None."

**Handoffs for Cowork (Bucket C)** — titles only, or "None."

**Pipeline Results** — table with columns: Pipeline, Result, Notes.

**Notable** — brief bullets for anything an agent or human should be aware of that didn't generate a task or handoff.

---

### REM — For Code

*This is your action list. Pick up each handoff below in priority order and execute it. No other interpretation needed.*

**Handoffs for Code** — table with columns: Title, Priority. One row per handoff created.

---

---

## Step 11.5 — Update Root Changelog

If the `changelog` sensor flags **unlogged_changes**, or if significant milestones (handoff completions) occurred:
1. Review the `handoffs/complete/` files from the last 24h.
2. Draft a summary of major changes and structural improvements.
3. Update the root `changelog.md` with a new version entry and date.
4. If work is routine maintenance, append to the existing version entry.

---

## Step 12 — Log the Run

Create a run log in `agents/logs/` using `add_intelligence`:
- **domain:** `agents/logs`
- **name:** `YYYY-MM-DD-dream-cycle`
- **title:** `Dream Cycle Run Log — YYYY-MM-DD`
- **metadata:**
    - `type: log`
    - `agent: Cowork`
    - `run: dream`

Content:
- Execution timestamp
- Sensor status summary
- Total fixes/handoffs/tasks generated
- Harvest results (pipelines run, failures, orphans found)
- Any significant errors encountered

---

## Constraints

- Do NOT edit files in `src/` or `orchestration/` — those are Code's domain
- Do NOT create more than 5 handoffs per run
- Do NOT create handoffs for issues you can fix directly
- Keep handoffs focused — one discrete problem per handoff
- If a sensor errors out entirely, note it in the Dream Report and move on
- Handoff titles must not contain slashes, em-dashes, en-dashes, or special characters — plain hyphens only
