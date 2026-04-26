# Implementation Plan: task-capture-skill-migration

> **Prepared by:** Claude via Dispatch (2026-04-12)
> **Assigned to:** Claude
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2 — skill migration, no urgency but improves vault completeness
> **v1.0**
> **STATUS**: ✅ COMPLETE

Migrated task-capture skill into the vault at skills/product/task-capture/. Source content taken from the Cowork plugin definition shared in-session (files were not on disk). Created index.md (purpose, scope, companion skills, source-of-truth note), procedure.md (classification system, workspace config, Asana custom field GIDs, Jira issue type mapping, execution steps, confirmation format, known limitations), changelog.md, and a references/ directory stub. Updated skills/product/index.md and skills/index.md to register the new skill. Cowork plugin remains the runtime version; vault is now the canonical reference and edit target.

**Changelog:** (see root changelog.md)


---

## Context

The `task-capture` skill currently lives only in human user's Cowork plugin (`.claude/skills/task-capture/`). It captures work items from raw notes and routes them into Asana or Jira with the correct metadata, issue types, and templates.

The goal is to port this skill into the ben-cp vault so it:
- Lives alongside other product skills (under `skills/product/` once that consolidation is complete)
- Is versioned, auditable, and improvable through the standard vault workflow
- Can be referenced and updated by meta-agents (Changelog Auditor, Vault Auditor, etc.)
- Becomes the source of truth — the Cowork plugin version should eventually be replaced by a symlink or thin wrapper pointing back to the vault copy

---

## Source Files

The Cowork plugin version lives at:
```
.claude/skills/task-capture/
  SKILL.md                          ← main routing logic
  references/
    asana-custom-fields.md          ← all Asana field and value GIDs
    user-story-template.md          ← Jira User Story template
    task-template.md                ← Jira Task template
    bug-template.md                 ← Jira Bug template
    cx-bug-template.md              ← Jira CX Bug template
    research-template.md            ← Jira Research/Spike template
```

Read all of these before beginning. They are the authoritative content to migrate.

---

## Execution Order

1. **Load context** — Read `AGENTS.md`, `skills/product/index.md` (if it exists), vault root `index.md`
2. **Decide placement** — See Task 2
3. **Create skill directory** — Migrate all content with vault-native formatting
4. **Update vault root `index.md`** — Register the new skill
5. **Update Cowork plugin** — Replace or note the plugin version (see Task 4)
6. **Changelog + completion**

---

## Task 1: Load Context

Before starting, read:
- `AGENTS.md` — understand the current skill registry and any agent that may reference task capture
- Vault root `index.md` — understand where skills currently live
- `skills/product/index.md` — if the product-skill-consolidation handoff has already been executed, task-capture should land under `skills/product/`; if not, create it as `skills/task-capture/` for now with a note to relocate later

---

## Task 2: Decide Placement

**If `skills/product/` exists** (consolidation handoff already executed):
- Create `skills/product/task-capture/`
- Add it to `skills/product/index.md`

**If `skills/product/` does not exist yet**:
- Create `skills/task-capture/` at the vault skill root
- Add a note in `index.md` and in this skill's own `index.md` that it should be relocated to `skills/product/task-capture/` once consolidation runs
- Cross-reference `handoff/2026-04-12-p2-product-skill-consolidation.md`

---

## Task 3: Create the Vault Skill

Create the following structure (adjust path based on Task 2):

```
skills/[product/]task-capture/
  index.md              ← purpose, scope, usage, cross-references
  procedure.md          ← adapted from SKILL.md: classification, routing, metadata, confirmation steps
  references/
    asana-custom-fields.md
    user-story-template.md
    task-template.md
    bug-template.md
    cx-bug-template.md
    research-template.md
  changelog.md
```

**Formatting notes:**
- `index.md` should follow the vault's standard skill index format (see any existing `skills/*/index.md` for the convention)
- `procedure.md` is the main content — adapt the SKILL.md content into vault-native prose/steps rather than keeping the Cowork agent-instruction framing. The vault version is documentation; the Cowork version is a runtime prompt.
- All reference files should be copied verbatim from the Cowork plugin versions
- Do not add an `index.md` inside `references/` — it's a flat reference folder

**Key content to preserve exactly:**
- All GIDs (Asana workspace, project, field, value GIDs; Jira cloud ID, project key, assignee ID)
- Issue type IDs and mappings
- The known limitations section — these are live operational quirks
- The Asana ↔ Jira linking protocol (this is easy to get wrong)

---

## Task 4: Cowork Plugin Relationship

After the vault version exists, update the Cowork plugin `SKILL.md` to add a note at the top:

```
> **Source of truth:** This skill is mirrored from the ben-cp vault at
> `skills/[product/]task-capture/procedure.md`. Update the vault version first;
> keep this file in sync manually until a symlink or auto-sync is in place.
```

Do not delete or replace the Cowork plugin version — it must remain functional for runtime use. The vault version is the canonical reference and edit target.

---

## Task 5: Update Registry Files

- Vault root `index.md`: add `task-capture` entry (or `product/task-capture` if under product/)
- `AGENTS.md`: check if any agent should reference task-capture and add if appropriate

---

## Task 6: Changelog + Completion

Write changelog entries:
- Skill-level `changelog.md` (new file)
- Root changelog: one-line summary

Mark this handoff complete and move to `handoff/complete/`.

---

## Notes for This Agent

- The Cowork plugin SKILL.md is written as an agent-instruction prompt (imperative, "you are..."). The vault `procedure.md` should be written as documentation — the same information but in third-person reference format. Both are valid, just for different audiences.
- The GIDs in the Cowork version are the live production values. Copy them exactly. Do not normalize or reformat.
- Cross-reference `handoff/2026-04-12-p2-product-skill-consolidation.md` — if that handoff runs first, coordinate placement. If this handoff runs first, leave a relocation note.
- The task-dod-helper skill may also be a candidate for the same migration. Do not do that work here — note it as a follow-up for human user.
