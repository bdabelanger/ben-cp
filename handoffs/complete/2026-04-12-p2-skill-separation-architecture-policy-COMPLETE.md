---
title: 'Implementation Plan: skill-separation-architecture-policy'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: skill-separation-architecture-policy

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Established the vault's four-layer separation policy. Created skills/shared/separation-policy.md documenting what belongs in skills/ vs tools/ vs inputs/ vs outputs/, including the character.md contract. Updated AGENTS.md with a Directory Boundaries section (hard constraint rule + four-layer table). Updated skills/index.md to register tools/ and inputs/ as Central Stores. Ran a full violation scan and documented 13 script violations, 6 live data paths, 1 structural double-nesting bug, and 7 stale notes.md files as Known Migration Debt in the policy doc.

**Changelog:** (see root changelog.md)


---

## Context

A structural audit (2026-04-12) identified that several skills — most visibly `product/status-reports/` — are doing three jobs at once: defining skill logic, storing live pipeline inputs/outputs, and housing execution scripts. This violates the principle that `skills/` should be a generic, version-controlled toolset that can be iterated and improved independently of any particular run's data.

The vault currently has no explicit policy documenting what belongs where. This handoff establishes that policy as a governance record and updates `AGENTS.md` and vault `index.md` to enforce it.

**The rule:**

| Layer | Lives in | Contents |
|---|---|---|
| Skill logic | `skills/` | `SKILL.md`, `character.md`, `index.md`, `changelog.md`, templates, report specs — anything defining *how* the skill works |
| Execution tooling | `tools/` | Scripts, pipeline runners, automation harnesses that *execute* a skill's procedure |
| Live data / WIP | `inputs/` | Raw API responses, processed JSON, `manifest.json`, session `notes.md` — anything produced *during* a run |
| Outputs | `outputs/` | Final reports, HTML, archives — anything *produced by* a run |

`skills/` must never contain: raw data files, processed JSON, archived reports, `manifest.json`, Python/shell scripts, or transient `notes.md` session files.

`character.md` files are the user-customization surface for voice and output structure. They belong exclusively inside their skill directory. `SKILL.md` never embeds character content — it only invokes `character.md` by reference.

---

## Execution Order

1. **Draft the separation policy doc** — write `skills/shared/separation-policy.md`
2. **Update `AGENTS.md`** — add a "Directory Boundaries" section with the four-layer table and cross-reference to `separation-policy.md`
3. **Update vault root `index.md`** — add `tools/` and `inputs/` to the Central Stores table with descriptions
4. **Flag existing violations** — scan `skills/` for any `inputs/`, `outputs/`, `scripts/`, `manifest.json`, or `notes.md` at rest; list them in a brief audit section at the bottom of `separation-policy.md` as "Known Migration Debt" (do not fix here — fixes are scoped to the companion migration handoff)
5. **Changelog + completion**

---

## Task 1: Create `skills/shared/separation-policy.md`

Write a clean policy doc. Sections:

```markdown
# Vault Separation Policy

> Effective: 2026-04-12
> Authority: AGENTS.md § Directory Boundaries

## The Four Layers
[four-layer table]

## What Belongs in `skills/`
[explicit list of allowed file types]

## What Does Not Belong in `skills/`
[explicit exclusion list with rationale]

## The `character.md` Contract
[character.md is the user-customization surface; it controls voice, output structure, persona.
SKILL.md invokes it by reference. Neither embeds the other's content.]

## Known Migration Debt
[auto-populated during Task 4 scan — list violations found]
```

---

## Task 2: Update `AGENTS.md`

Add a **Directory Boundaries** section (after the skill registry table, before agent role definitions). Content:

- Reference `skills/shared/separation-policy.md` as the authoritative doc
- State the four-layer rule as a hard constraint: any agent writing data files into `skills/` is in violation
- Note that `tools/` houses execution scripts; `inputs/` houses live run data; `outputs/` is already the established central store

---

## Task 3: Update vault root `index.md`

In the Central Stores table, add or update:

| Store | Purpose |
|---|---|
| `tools/` | Execution scripts and pipeline runners for all skills |
| `inputs/` | Live run data: raw API responses, processed JSON, manifest state |
| `outputs/` | Centralized final reports and session artifacts (already present — confirm entry) |

---

## Task 4: Violation Scan

Read the `list_vault` index and identify every file under `skills/` that matches:
- `inputs/` directories or files
- `outputs/` directories (within skill subdirs, not the root)
- `scripts/` directories
- `manifest.json`
- `notes.md` (session WIP files — distinguish from structural `index.md`)
- `*.py`, `*.sh` files

List each as a Known Migration Debt entry in `separation-policy.md`. Format:

```
- `skills/product/status-reports/inputs/` — live pipeline data (→ migrate to `inputs/status-reports/`)
- `skills/product/status-reports/scripts/` — pipeline runner scripts (→ migrate to `tools/status-reports/`)
- `skills/product/status-reports/manifest.json` — pipeline state (→ migrate to `inputs/status-reports/manifest.json`)
- `skills/product/notes.md` — session WIP (→ ephemeral, use `wip/` or delete post-session)
```

---

## Task 5: Changelog + Completion

- Write subdirectory changelog entry in `skills/shared/changelog.md` (create if absent)
- Write root changelog entry: one-line summary + pointer
- Move this handoff to `handoff/complete/`

---

## Notes for This Agent

- This is a **policy-only** handoff. Do not move or delete any files. The companion handoff `2026-04-12-p2-status-reports-skill-separation.md` handles the first concrete migration.
- `shared/` may not exist yet — create it if needed. It is the right home for cross-cutting vault governance docs.
- The `product/shared/shared/` double-nesting found in the vault index is a separate bug — flag it in Known Migration Debt but do not fix here.
- Keep the policy doc terse. It is a reference doc, not a manifesto.
