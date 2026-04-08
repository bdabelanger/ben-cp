# Skill: Lumberjack

> **Purpose:** Changelog auditing — accuracy, completeness, and cross-reference checks.
> Companion to Crypt-Keeper (structure) and Changelog (procedure).
> Last updated: 2026-04-08

---

## What Lumberjack Does

Crypt-Keeper checks vault structure. Lumberjack checks the logs.

Runs after sessions with significant work — especially after handoff executions or
multi-skill sessions — to verify changelogs accurately reflect what happened.

---

## When to Run

- After any session where multiple skills were touched
- After a handoff is executed
- Before a Crypt-Keeper run (clean logs → clean report)
- On demand when Ben suspects a gap

---

## Checks

See `procedure.md` for full execution steps.

| Check | What it catches |
| :--- | :--- |
| 1 — Missing entries | Work done this session with no changelog entry |
| 2 — Phantom entries | Entries describing things that don't exist (dirs, files, tools) |
| 3 — Stale Next Tasks | Next Tasks already completed in a later entry — not removed |
| 4 — Inaccurate counts or names | Wrong numbers, wrong paths, superseded tool names |
| 5 — Subdir ↔ root alignment | Subdirectory entries without a root pointer, or vice versa |
| 6 — Handoff cross-reference | COMPLETE handoffs without a changelog entry; entries missing Handoff field |
| 7 — Version sequence | Gaps or duplicates in `[X.Y.Z]` version numbering |

---

## Output

A structured report (not a fix — flag only, same as Crypt-Keeper):

```
skills/lumberjack/reports/lumberjack-report-YYYY-MM-DD.md
```

Flags go to handoffs if actionable. Ben reviews and assigns.

---

## Files

| File | Purpose |
| :--- | :--- |
| `index.md` | This file — TOC and overview |
| `procedure.md` | Step-by-step audit procedure |
| `reports/` | Generated audit reports — never edit manually |
| `changelog.md` | Detail log for this skill |
