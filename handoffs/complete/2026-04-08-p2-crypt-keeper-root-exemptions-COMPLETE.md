---
title: 'Claude Code Implementation Plan: Document Root-Level File Exemptions in AGENTS.md'
type: handoff
domain: handoffs/complete
---


# Claude Code Implementation Plan: Document Root-Level File Exemptions in AGENTS.md

> **Prepared by:** Repo Auditor (scheduled run, 2026-04-08)
> **Repo root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — structural violation (AGENTS.md compliance)
> **Source report:** `skills/knowledge/reports/knowledge-report-2026-04-08.md`
> **v1.0**
> **STATUS**: ✅ COMPLETE

On reading `AGENTS.md`, the exemption list already contained `CLAUDE.md` and `README.md` — the update was applied in a prior session. `CLAUDE.md` contains unique Claude Code–specific guidance (handoff check protocol), so it is retained and correctly listed in exemptions. No file edits or deletions were needed; handoff is complete as found.

**Changelog:** 1.6.0 — 2026-04-09 (see root `changelog.md`)

---

## Context

Repo Auditor Check 2 flagged two files at repo root that are not listed in
AGENTS.md's explicit exemptions: `CLAUDE.md` and `README.md`. The current rule
reads: "Never create files at repo root (except `AGENTS.md`, `GEMMA.md`,
`changelog.md`)."

- `README.md` is standard GitHub convention — it belongs at root and should be
  permanently exempted in AGENTS.md.
- `CLAUDE.md` appears to be a Claude Code agent directive stub (parallel to
  `GEMMA.md` for Gemma). Human user needs to confirm intent: if it's intentional,
  add it to the exemption list; if it duplicates `AGENTS.md`, delete it.

No file moves or deletions here — this is purely an AGENTS.md documentation
update (plus one conditional deletion).

---

## Execution Order

1. **Task 1** — Read `CLAUDE.md` and confirm intent with context
2. **Task 2** — Update AGENTS.md exemption list
3. **Task 3** — (Conditional) Delete `CLAUDE.md` if redundant
4. **Task 4** — Write changelog and mark complete

---

## Task 1: Read CLAUDE.md

**Read:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/CLAUDE.md`

Assess:
- If it contains unique Claude Code–specific guidance not in `AGENTS.md` → retain, add to exemptions
- If it is a pure redirect/stub duplicating `AGENTS.md` content → flag for deletion in Task 3

---

## Task 2: Update AGENTS.md — Root Exemption List

**Read first:** `AGENTS.md`

Find the line:
```
**Never create files at repo root** (except `AGENTS.md`, `GEMMA.md`, `changelog.md`).
```

Replace with:
```
**Never create files at repo root** (except `AGENTS.md`, `CLAUDE.md`, `GEMMA.md`, `README.md`, `changelog.md`).
```

If Task 1 determined `CLAUDE.md` should be deleted, omit it from the exemption list and use:
```
**Never create files at repo root** (except `AGENTS.md`, `GEMMA.md`, `README.md`, `changelog.md`).
```

Use `edit_file` — do not `write_file` on AGENTS.md.

---

## Task 3: (Conditional) Delete CLAUDE.md

Only execute if Task 1 confirmed `CLAUDE.md` is a redundant stub.

```
git rm /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/CLAUDE.md
```

If retaining, skip this task.

---

## Task 4: Changelog + Completion

Write changelog entries using `write_changelog_entry`:

**Subdirectory level** (`skills/knowledge/changelog.md`):
- Note: AGENTS.md root exemption list updated per Repo Auditor flag 2.2–2.3
- Include disposition of CLAUDE.md (retained or deleted)

**Root level** (`changelog.md`):
- One-liner: `AGENTS.md root exemptions updated — README.md and CLAUDE.md clarified`
- Pointer: `See skills/knowledge/changelog.md`

Then mark this file complete:
1. Update STATUS line to `✅ COMPLETE — [date]`
2. Add one-paragraph summary
3. Move to `handoff/complete/2026-04-08-p2-crypt-keeper-root-exemptions-COMPLETE.md`

---

## Notes for This Agent

- Read before every write — no exceptions
- Do not modify `CLAUDE.md` content — only assess and optionally delete
- The exemption list update is a targeted `edit_file` on one line in AGENTS.md
- If unsure about CLAUDE.md intent, retain it and add to exemptions — human user can
  decide to delete later
