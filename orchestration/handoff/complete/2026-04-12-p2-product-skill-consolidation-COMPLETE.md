# Implementation Plan: product-skill-consolidation

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-12**

Created skills/product/ as a new peer-level domain. Moved project-status-reports/ (renamed to status-reports/) and okr-reporting/ under it. Created a shared/ directory with merged data_sources.md covering sources common to both skills. Created master index.md as the PM-facing entry point.

**Changelog:** (see root changelog.md)


---

# Implementation Plan: product-skill-consolidation

> **Prepared by:** Claude via Cowork/Dispatch (2026-04-11)
> **Assigned to:** Claude (desktop)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2 — vault reorganization, no urgency but improves agent navigation
> **v1.0**
> **STATUS: 🔲 READY — pick up on desktop**

---

## Context

Human user's two most active PM skills — `project-status-reports/` and `okr-reporting/` — are currently stored as sibling directories at the vault root. They share significant overlap: both are about measuring and communicating platform delivery health, both draw from the same Asana and Jira data sources, and both serve human user's primary duties as a Product Manager.

The goal is to consolidate them under a new `product/` skill directory that serves as the canonical home for PM-facing knowledge and tooling. This makes the vault easier to navigate for both agents and Ben, and reduces duplication in data source references and shared conventions.

---

## Execution Order

1. **Load context** — Read `AGENTS.md`, `project-status-reports/index.md`, `okr-reporting/index.md`, and `index.md` (vault root)
2. **Design the new structure** — Confirm proposed layout before touching anything (see Task 2)
3. **Create `product/` directory** — New index, move sub-skills, update all internal cross-references
4. **Update vault root `index.md`** — Replace the two old entries with one `product/` entry
5. **Update `AGENTS.md`** — Reflect the new skill location for any agent that references these skills
6. **Changelog + completion** — Write changelogs and mark complete

---

## Task 1: Load Context

Before starting, read:
- `AGENTS.md` — check which agents reference `project-status-reports/` or `okr-reporting/` by name
- `project-status-reports/index.md` — understand the pipeline structure
- `okr-reporting/index.md` — understand the KR reporting structure
- `index.md` at vault root — understand the current skill directory listing

---

## Task 2: Proposed New Structure

```
skills/
  product/
    index.md                        ← new: master index for all PM-facing skills
    status-reports/                 ← renamed from project-status-reports/
      index.md                      ← updated paths and references
      [all existing files]
    okr-reporting/                  ← moved as-is from root
      index.md                      ← update cross-references only
      [all existing files]
    shared/
      data_sources.md               ← merged from okr-reporting/data_sources.md
                                       (status reports currently have no equivalent — combine here)
```

Before executing, confirm this structure with human user if anything looks wrong. Do not rename or move files until he approves the layout.

Key decisions baked in:
- `project-status-reports/` becomes `product/status-reports/` (shorter, cleaner name)
- `okr-reporting/` moves to `product/okr-reporting/` (no rename — the name is fine)
- A `product/shared/data_sources.md` is created by merging the existing `okr-reporting/data_sources.md` with any data source references found in the status reports skill. This prevents duplication as both skills grow.
- A `product/index.md` serves as the PM-facing entry point for all agents

---

## Task 3: Create the New Structure

Steps:
1. Create `skills/product/index.md` with a clear purpose statement and table of contents pointing to both sub-skills
2. Use `git mv` to move `skills/project-status-reports/` → `skills/product/status-reports/`
3. Use `git mv` to move `skills/okr-reporting/` → `skills/product/okr-reporting/`
4. Create `skills/product/shared/data_sources.md` by merging content from `okr-reporting/data_sources.md` and any inline data source references in status reports scripts/SOPs
5. Update all internal cross-references (any path that pointed to old locations)

---

## Task 4: Update Vault Root `index.md`

Replace the two existing entries:
- `project-status-reports/` → remove
- `okr-reporting/` → remove

Add one new entry:
- `product/` — PM-facing skills: weekly status reports and OKR reporting

---

## Task 5: Update `AGENTS.md`

Check for any agent definitions that reference the old skill paths and update them to the new locations. Also add a note in the `product/` section about the shared data sources file to prevent future duplication.

---

## Task 6: Changelog + Completion

Write changelog entries:
- Subdirectory level: `product/changelog.md` (new), `okr-reporting/changelog.md`, status-reports changelog
- Root level: one-line summary

Mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent

- Use `git mv` for all moves to preserve git history — do not copy and delete
- Do not touch the contents of any script files in `project-status-reports/scripts/` — only update path references in documentation and index files
- The `product/shared/data_sources.md` is a new file — create it, don't just move the existing one. Merge content from both skills.
- Cross-reference this handoff with `handoff/2026-04-11-p1-dream-cycles.md` — dream cycles will depend on the new `product/` structure
