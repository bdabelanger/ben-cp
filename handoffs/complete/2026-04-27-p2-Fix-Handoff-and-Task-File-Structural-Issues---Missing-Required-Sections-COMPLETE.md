---
title: 'Implementation Plan: Fix Handoff and Task File Structural Issues - Missing
  Required Sections'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Fix Handoff and Task File Structural Issues - Missing Required Sections

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Resolved structural issues by fixing the handoffs sensor (exclusions, header anchoring, checkbox detection) and patching existing handoff files. verified 0 issues in latest dream report.Scan

---

## Fix Handoff and Task File Structural Issues - Missing Required Sections

## Context

The handoffs sensor found 12 issues across 6 files. The majority are in `tasks/jira.md` and `tasks/asana.md` which are missing multiple required sections. There are also issues with two handoff files created in previous dream runs.

**tasks/jira.md** — missing: `## Execution Steps`, `## Context`, `## Logic`
**tasks/asana.md** — missing: `## Execution Steps`, `## Context`, `## Logic`

**Handoff file issues:**
- `handoffs/2026-04-27-p3-Investigate-Agents-Sensor---False-positives-on-bold-markdown-text.md`: missing `## Logic`, no checkboxes despite READY status
- `handoffs/2026-04-27-p1-Dream-Report---2026-04-26.md`: missing `## Execution Steps`, `## Context`, `## Logic`
- `handoffs/2026-04-27-p2-Fix-Task-Files---Missing-required-sections-in-5-tasks.md`: no checkboxes despite READY status

Note: The two handoff issues in the prior dream report files may be artifacts of how that particular dream run generated its summary handoff — the format may have drifted from the standard.

## Goal

Bring `tasks/jira.md` and `tasks/asana.md` into compliance with the handoff/task file schema. Optionally fix the stale handoff files from the prior dream run if they remain READY.

## Execution Steps

- [ ] Open `tasks/jira.md` — add the missing sections (`## Context`, `## Logic`, `## Execution Steps`) with appropriate placeholder content describing what the Jira task integration task does and how it should be executed.

- [ ] Open `tasks/asana.md` — same treatment: add `## Context`, `## Logic`, `## Execution Steps`.

- [ ] Review the two prior dream handoff files (`2026-04-27-p3-Investigate-Agents-Sensor...` and `2026-04-27-p2-Fix-Task-Files...`). If they are still READY (not yet picked up by Code), either:
   - Add checkboxes to their verification sections, OR
   - Mark them COMPLETE if the work has already been done

- [ ] For the `2026-04-27-p1-Dream-Report---2026-04-26.md` file (last run's morning briefing), consider whether it should be excluded from structural validation since summary handoffs have a different format — add it to a sensor exclusion list if appropriate.

- [ ] Re-run `generate_report(skill='dream')` and confirm handoffs sensor drops to 0 issues.

## Verification Checklist

- [ ] `tasks/jira.md` contains `## Context`, `## Logic`, `## Execution Steps`
- [ ] `tasks/asana.md` contains `## Context`, `## Logic`, `## Execution Steps`
- [ ] `get_report('dream/handoffs.json')` shows 0 issues
- [ ] READY handoff files all have at least one checkbox
