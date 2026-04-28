# Implementation Plan: Fix Structural Issues in Triage Overdue Tasks Handoff

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Added YAML frontmatter to Triage-Overdue-Tasks handoff, removed duplicate header block, and updated handoffs/index.md to register the file.

---

## Context

The handoffs sensor and frontmatter sensor both flagged `handoffs/2026-04-27-p2-Triage-Overdue-Tasks.md`. Three distinct issues were found:

1. **Missing frontmatter** — file has no YAML frontmatter block
2. **Duplicate H1** — the header block (title + metadata callout + STATUS line + divider) appears twice, verbatim
3. **ready_no_checkboxes** — the handoff has STATUS: READY but contains no checkboxes (verification items). The file does have a Verification section with checkboxes, but the sensor may be parsing before the duplicate content confuses it.
4. **Shadow in index** — the file exists in `handoffs/` but is not registered in `handoffs/index.md`

## Goal

Fix the handoff file structure and register it in the index.

## Execution Steps

1. Read `handoffs/2026-04-27-p2-Triage-Overdue-Tasks.md`
2. Remove the duplicate header block — keep one clean instance of the title, metadata, STATUS line, and divider
3. Add a valid YAML frontmatter block at the top with fields: `title`, `priority`, `assigned_to`, `status`, `date`
4. Verify the Verification section checkboxes are intact and parseable
5. Read `handoffs/index.md` and add an entry for this handoff in the appropriate section
6. Re-run handoffs sensor to confirm 0 issues

## Verification

- [ ] Handoffs sensor shows 0 issues for this file
- [ ] Frontmatter sensor shows 0 issues for this file
- [ ] Index sensor shows 0 shadow files in `handoffs/`
- [ ] File has exactly one H1
