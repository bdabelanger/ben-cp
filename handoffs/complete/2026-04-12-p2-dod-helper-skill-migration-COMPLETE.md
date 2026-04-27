---
title: Implementation Plan dod-helper-skill-migration
type: handoff
domain: handoffs/complete
---

# Implementation Plan: dod-helper-skill-migration

> **Prepared by:** Claude via Dispatch (2026-04-12)
> **Assigned to:** Claude
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2 — skill migration, companion to task-capture-skill-migration
> **v1.0**
> **STATUS**: ✅ COMPLETE

Migrated dod-helper skill into the vault at skills/product/dod-helper/. Source content taken from the Cowork plugin definition (task-dod-helper) shared in-session. Created index.md (purpose, modes, companion skills, source-of-truth note), procedure.md (mode detection, single-task flow, question sets by task type, DoD format rules with rationale, posting behavior for Asana vs Jira, batch mode flow), and changelog.md. The DoD quality bar rules — plain dashes, no markdown headers, 3–7 criteria — are preserved verbatim with rationale in procedure.md. Cowork plugin remains the runtime version; vault is now the canonical reference and edit target.

**Changelog:** (see root changelog.md)


---

## Context

The `task-dod-helper` skill currently lives only in human user's Cowork plugin (`.claude/skills/task-dod-helper/SKILL.md`). It interviews human user about a specific task (Asana or Jira) and writes a Definition of Done back to it. It also supports a batch mode that sweeps all of human user's open Asana tasks.

This handoff mirrors the pattern established in `2026-04-12-p2-task-capture-skill-migration.md`. Execute these two together if possible — they are both product PM tools and should land in the same destination directory.

---

## Source File

```
.claude/skills/task-dod-helper/
  SKILL.md       ← all content (no sub-references)
```

The SKILL.md covers: mode detection, single-task flow (fetch → detect type → check existing DoD → subtask check → question set → draft → post), and batch mode flow.

---

## Execution Order

1. **Load context** — Read `AGENTS.md`, vault root `index.md`, `skills/product/index.md` if it exists
2. **Coordinate with task-capture** — Both skills should land in the same destination. Confirm placement before creating anything.
3. **Create skill directory** — Migrate content with vault-native formatting
4. **Update vault root `index.md`**
5. **Update Cowork plugin** — Add source-of-truth note
6. **Changelog + completion**

---

## Task 1: Load Context

Read:
- `AGENTS.md` — check for any agent that references task-dod-helper
- Vault root `index.md` — understand current skill registry
- `skills/product/index.md` — if product-skill-consolidation has run, both PM skills land here

---

## Task 2: Placement (coordinate with task-capture)

**If `skills/product/` exists:**
- Create `skills/product/dod-helper/`
- Add to `skills/product/index.md`

**If not:**
- Create `skills/dod-helper/` at vault skill root
- Add relocation note pointing to `2026-04-12-p2-product-skill-consolidation.md`

Use the same placement logic as `task-capture`. Both should land together.

---

## Task 3: Create the Vault Skill

```
skills/[product/]dod-helper/
  index.md          ← purpose, scope, mode overview, cross-reference to task-capture
  procedure.md      ← adapted from SKILL.md content (vault-native doc format)
  changelog.md
```

**Formatting notes:**
- `procedure.md` should document both modes (single-task and batch) clearly
- Preserve the question sets per task type verbatim — these are the calibrated interview logic
- Preserve the quality bar criteria (plain dashes, no checkboxes, 3–7 criteria, plain label not markdown header) — these are non-obvious operational rules
- Preserve the Asana vs. Jira posting behavior (Asana: update notes; Jira: add comment, not description edit)
- `index.md` should cross-reference `dod-helper` and `task-capture` as companion skills under the product umbrella

---

## Task 4: Cowork Plugin Note

Add at the top of `.claude/skills/task-dod-helper/SKILL.md`:

```
> **Source of truth:** This skill is mirrored from the ben-cp vault at
> `skills/[product/]dod-helper/procedure.md`. Update the vault version first;
> keep this file in sync manually until a symlink or auto-sync is in place.
```

Do not delete or replace the plugin version — it must remain functional for runtime use.

---

## Task 5: Update Registry Files

- Vault root `index.md`: add `dod-helper` entry
- `AGENTS.md`: check if any agent should reference dod-helper

---

## Task 6: Changelog + Completion

- New `changelog.md` in the skill directory
- Root changelog: one-line summary
- Move this handoff to `handoff/complete/`

---

## Notes for This Agent

- Run this alongside `2026-04-12-p2-task-capture-skill-migration.md` — they are companion tasks.
- The DoD quality bar (plain dashes, no markdown headers, 3–7 criteria) is an operational rule that emerged from real Asana/Jira rendering issues. Preserve it exactly in `procedure.md` with the rationale.
- The batch mode is a meaningful feature — document it as a first-class flow, not a footnote.
- No reference sub-files in this skill (unlike task-capture). Single SKILL.md → single `procedure.md`.
