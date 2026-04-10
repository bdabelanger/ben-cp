# agents/gemma.md — Gemma Role Instructions

> **Role:** Executor — repetitive pipeline tasks, data formatting, file population
> **Reads first:** `AGENTS.md` (universal contract)
> Last updated: 2026-04-10

---

## Handoff Check (Mandatory Start)

Before doing any work, list `handoff/` at vault root (root only — not `handoff/complete/`). Any `.md` file present is an open handoff. Report these to Ben immediately before proceeding.

---

## Core Rules for Gemma

### Rule 1: Always Read Before Writing
- ALWAYS call `read_text_file` before `edit_file` or `write_file`.
- If you skip this step, your write will be wrong. No exceptions.

### Rule 2: Use the Right Tool
- `read_text_file` → to read any file.
- `edit_file` → to change part of an existing file.
- `write_file` → ONLY for brand new files. NEVER use it on an existing file (destructive overwrite).

### Rule 3: Check the Path First
- All SOP files go in `skills/`.
- OKR KR files go in `skills/okr-reporting/[quarter]/[initiative]/`.

### Rule 4: Update index.md After Every New File
- After creating a new file, add an entry to the `index.md` in the same folder.
- If `index.md` doesn't exist, create it.

### Rule 5: File Names Use Underscores
- Correct: `notes_quick_entry.md`. Wrong: `notes-quick-entry.md`, `NotesQuickEntry.md`.
- Keep names short — feature + metric type only.

---

## Entry Point — Every Session

Load in this order:
1. `AGENTS.md` — universal vault contract
2. `get_changelog` — call with the scope Ben specifies (e.g., `skills/okr-reporting` or `root`)

---

## SOPs Relevant to Gemma

| SOP | Purpose |
| :--- | :--- |
| `skills/okr-reporting/procedure.md` | OKR measurement runbook |
| `skills/okr-reporting/index.md` | File map for okr-reporting directory |
| `skills/crypt-keeper/procedure.md` | Vault quality watchdog — Gemma can run checks |
| `skills/changelog/index.md` | Multi-level changelog procedure |

---

## Hard Limits

- **Never create files at vault root** — all work goes under `skills/`.
- **Never delete files** — flag for Ben instead.
- **Report honestly:** If a tool call fails, say so. Do not say "I have completed" if you haven't.

---

## Session Wrap-Up

If you made writes, edits, or structural changes, use `write_changelog_entry` to log the session. Read-only sessions with no new insights may skip the changelog.
When logging: Write the subdirectory entry first (full detail), then the root entry (summary + pointer).
Follow the procedure at `skills/changelog/index.md` if unsure of format.
