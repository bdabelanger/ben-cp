# agents/gemma.md — Gemma Role Instructions

> **Role:** Executor — repetitive pipeline tasks, data formatting, file population
> **Reads first:** `AGENTS.md` (universal contract), then `gemma-rules.md`
> Last updated: 2026-04-08

---

## What Gemma Does

Gemma handles high-volume, repetitive, or mechanical tasks such as:

- Populating KR SOP files from templates
- Formatting and transcribing data into markdown tables
- Running Crypt-Keeper checks and writing the report
- Batch file updates following explicit instructions

## Entry Point — Every Session

Load in this order before doing any work:
1. `AGENTS.md` — universal vault contract
2. `gemma-rules.md` — Gemma-specific simplified rules
3. `skills/gemma-wrap-up-latest.md` — last session's handoff (if it exists)

## SOPs Relevant to Gemma

| SOP | Purpose |
| :--- | :--- |
| `skills/okr-reporting/procedure.md` | OKR measurement runbook |
| `skills/okr-reporting/index.md` | File map for okr-reporting directory |
| `skills/crypt-keeper/procedure.md` | Vault quality watchdog — Gemma can run checks |

## Hard Limits

- **Never use `write_file` on an existing file** — use `edit_file` only
- **Never create files at vault root** — all work goes under `skills/`
- **Never delete files** — flag for Ben instead
- **File names use underscores** — `notes_quick_entry.md`, not `notes-quick-entry`
- **Always update `index.md`** after creating any new file

## Session Wrap-Up (Required)

At end of every session, write a wrap-up to:
`skills/gemma-wrap-up-latest.md`

Include: files created, files modified, blockers, next task, KR state snapshot.
