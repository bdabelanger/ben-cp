# gemma-rules.md — Gemma Simplified Rules

> **Load order:** `AGENTS.md` → `agents/gemma.md` → this file
> These rules are a simplified, reinforced subset of the universal contract.
> Last updated: 2026-04-08

---

## Core Rules (Simple Version)

### Rule 1: Always Read Before Writing
- ALWAYS call `read_text_file` before `edit_file` or `write_file`
- If you skip this step, your write will be wrong
- No exceptions — even if you think you know the file contents

### Rule 2: Use the Right Tool
- `read_text_file` → to read any file
- `edit_file` → to change part of an existing file
- `write_file` → ONLY for brand new files that do not exist yet
- NEVER use `write_file` on a file that already exists

### Rule 3: Check the Path First
- All SOP files go in `sop/`
- OKR KR files go in `sop/okr-reporting/`
- When unsure, call `list_directory` to check what's already there
- NEVER create a file at the vault root

### Rule 4: Update index.md After Every New File
- After creating a new file, find `index.md` in the same folder
- Read `index.md`, then add an entry for your new file
- If `index.md` doesn't exist, create it

### Rule 5: File Names Use Underscores
- Correct: `notes_quick_entry.md`
- Wrong: `notes-quick-entry.md`, `NotesQuickEntry.md`, `notes_quick_entry_outside_uow_sop.md`
- Keep names short — feature + metric type only

### Rule 6: Report Honestly
- If a tool call fails, say so — do not say "I have completed" if you haven't
- If you are unsure where a file belongs, ask Ben before creating it

### Rule 7: Wrap Up Every Session
- At the end of every session, list every file you created or changed
- Use full absolute paths
- List any steps you could not complete and why
- Write the wrap-up to: `sop/gemma-wrap-up-latest.md`
