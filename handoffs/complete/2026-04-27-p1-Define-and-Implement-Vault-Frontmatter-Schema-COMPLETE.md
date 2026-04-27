---
title: Implementation Plan Define and Implement Vault Frontmatter Schema
type: handoff
domain: handoffs
---

# Implementation Plan: Define and Implement Vault Frontmatter Schema

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully standardized the vault metadata by implementing a YAML frontmatter schema across 363 files. This involved updating the frontmatter sensor, executing a bulk migration, and resolving structural inconsistencies like multiple H1 headers. The frontmatter sensor now reports 0 issues.

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P1
> **STATUS**: 🔲 READY

---

## Context

The vault has no consistent frontmatter standard. Files currently use blockquotes (`> **Purpose:** ...`) as a substitute, or have no metadata at all. The frontmatter sensor is flagging 214 issues across 167 files as a result.

## Goal

Define a standard frontmatter schema, apply it across the vault, and update the frontmatter sensor to validate against it.

---

## Schema

All `.md` files in the vault should have YAML frontmatter. Only include `links` sources that are actually present — omit empty sources.

```yaml
---
title: 
type: 
domain: 
links:
  asana:
    - 
  confluence:
    - 
  jira:
    - 
  google-drive:
    - 
  github:
    - 
  figma:
    - 
---
```

### Field definitions

| Field | Required | Description |
| :---- | :------- | :---------- |
| `title` | Yes | Human-readable title. Should match the `# H1` heading. |
| `type` | Yes | File type. See valid values below. |
| `domain` | Yes | Vault domain path (e.g. `skills/dream`, `intelligence/product/projects/q2`). |
| `links` | No | External source links, grouped by system. Only include systems with actual links. |

### Valid `type` values

| Type | Used for |
| :--- | :------- |
| `index` | Directory index files (`index.md`) |
| `skill` | Skill definition files (`SKILL.md`) |
| `intelligence` | Intelligence records |
| `handoff` | Handoff files |
| `changelog` | Changelog files |
| `release` | Release notes |
| `prd` | Product requirement docs |
| `agent` | Agent definition files |
| `task` | Task files |
| `report` | Report files |

---

## Execution Steps

1. Update the frontmatter sensor (`src/`) to validate:
   - `title` present and non-empty
   - `type` present and one of the valid values above
   - `domain` present and non-empty
   - `links` is optional but if present, must be a map with at least one source key
   - Flag `multiple_h1` and `no_h1` as before

2. Write a migration script (`orchestration/pipelines/intelligence/scripts/migrate_frontmatter.py` or similar) that:
   - Walks all `.md` files in the vault (excluding `node_modules`, `dist`, `src`, `reports`)
   - For files with no frontmatter: infers `title` from `# H1`, infers `type` from file path/name, infers `domain` from directory path, leaves `links` empty
   - For files with existing blockquote metadata (`> **Purpose:**` etc.): preserves the blockquote in the body (do not remove) and adds frontmatter above it
   - Logs any files it couldn't auto-migrate

3. Run the migration script

4. Spot-check 10 files across different domains to confirm frontmatter looks correct

5. Re-run `generate_report(skill='dream')` and confirm frontmatter sensor issue count drops significantly

## Verification

- Frontmatter sensor shows green or yellow (not red)
- `title`, `type`, and `domain` present on all migrated files
- `links` blocks use the correct source keys where applicable
- No files have frontmatter that conflicts with their `# H1` heading
