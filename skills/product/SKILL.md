---
name: product
description: PM-facing skill group managing planning, status reporting, and OKR measurement. Presided over by the Strategic PM — a PMM-trained strategic intelligence operating across all product sub-skills.
---

# SKILL: Product Domain

> **Role:** PM-facing intelligence and reporting authority
> **Presiding Agent:** Strategic PM
> **Entry point:** `skills/product/index.md`
> Last updated: 2026-04-12

---

## Sub-skills

| Sub-skill | Agent | Cadence |
| :--- | :--- | :--- |
| `status-reports/` | Strategic PM | Weekly |
| `okr-reporting/` | Strategic PM | Weekly / On-change |

---

## Execution Sequence

Before executing any product sub-skill, an agent MUST:
1. Read `skills/product/character.md` — load the Strategic PM persona
2. Read `skills/collaboration/captains-log.md` — establish human user's ground truth
3. Read yesterday's Digest in `skills/dream/outputs/` — establish crew context

## The Strategic PM Convention (Session Planning)

At the start of any complex session touching product skills:
1. Create `notes.md` in the target sub-skill directory using `skills/product/report.md`
2. Identify all dependencies and risks before the first write
3. Delete `notes.md` after the final changelog entry of the session

**Lingering `notes.md` files** without same-day commits are flagged by Changelog Auditor as stale plans and escalated to Roz.
