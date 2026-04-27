---
title: Implementation Plan Create SKILL.md for Dream Cycle
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Create SKILL.md for Dream Cycle

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Created skills/dream/SKILL.md with the full operating procedure for the Dream Cycle. Verified via get_skill.Scan

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

The Dream cycle's full operational instructions currently live inside the scheduled task prompt in Cowork. The goal is to move them into a `SKILL.md` file in the vault so they're version-controlled, editable, and readable by any agent — and the scheduled task prompt becomes a thin launcher.

## Goal

Create `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/dream/SKILL.md` with the full Dream cycle operating procedure.

## Content

Write the following content exactly to `skills/dream/SKILL.md`:

```markdown
# Dream Cycle — Skill

> **Trigger:** Nightly automated run (22:00) or manual invocation
> **Agent:** Cowork (Claude)
> **Purpose:** Run all vault health sensors, triage findings, fix low-risk issues directly, create handoffs for Code, and raise Asana tasks for Ben.

---

## Overview

The Dream cycle is the vault's nightly health loop. It runs 11 sensors against the vault, analyzes the results, and routes work to the right destination — fixing trivial issues in-place, handing non-trivial work to Code, and surfacing decisions to Ben. Ben's morning briefing is a `Dream Report` handoff waiting for him when he signs in.

---

## Step 1 — Generate the Report

\`\`\`
generate_report(skill='dream')
\`\`\`

Runs all 11 sensors and writes results to `reports/dream/`.

---

## Step 2 — Read the Report

\`\`\`
get_report(path='dream/report.md')
\`\`\`

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

### Bucket B — Handoff for Code
Anything touching more than ~3 files, requiring script changes, or needing a PR:
- Ghost link cleanup (bulk path corrections)
- Structural violations in agent or handoff files
- Directory boundary issues (drift)
- Sensor logic fixes

### Bucket C — Asana task for Ben
Decisions or risks that require human judgment:
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
- `title` — imperative, specific. **Plain hyphens only — no em-dashes, en-dashes, or special characters**
- `priority` — P1 for broken sensors, P2 for structural issues, P3 for housekeeping
- `assigned_to` — Code
- Body must include: Context, Goal, Execution Steps, Verification checklist
- Max 5 handoffs per run — group related issues

**Naming examples:**
✅ `Fix Ghost Links in intelligence/product/releases/`
✅ `Add Missing Index Files to 14 Directories`
❌ `Fix Ghost Links — intelligence/` (em-dash)
❌ `Fix Ghost Links - intelligence/` (space-hyphen-space causes triple-dash in filename)

---

## Step 7 — Raise Asana Tasks for Ben (Bucket C)

- Assign to Ben
- Due: tomorrow's date
- Include enough context to act without re-reading sensor data

---

## Step 8 — Verify (Optional)

If you made direct fixes, re-run `generate_report(skill='dream')` and confirm the relevant sensor improved. Note before/after counts in the Dream Report.

---

## Step 9 — Write the Dream Report Handoff

Create one final handoff using `add_handoff`:

- **title:** `Dream Report` (no date — the filename prefix handles it)
- **assigned_to:** Ben
- **priority:** P1

Content:
- Sensor status table (from `report.md`)
- What you fixed directly (Bucket A)
- Handoffs created for Code (Bucket B) — titles only
- Asana tasks raised for Ben (Bucket C) — titles only
- Notable observations

This is Ben's morning briefing. He reads it first thing at 8am.

---

## Constraints

- Do NOT edit files in `src/` or `orchestration/` — those are Code's domain
- Do NOT create more than 5 handoffs per run
- Do NOT raise Asana tasks for issues you can fix directly
- Keep handoffs focused — one discrete problem per handoff
- If a sensor errors out entirely, note it in the Dream Report and move on
```

## Verification

- `skills/dream/SKILL.md` exists and is readable via `get_skill(relativePath='dream/SKILL.md')`
