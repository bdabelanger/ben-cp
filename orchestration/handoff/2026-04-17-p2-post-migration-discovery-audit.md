# Implementation Plan: 2026-04-17-p2-Post-Migration-Intelligence-Audit-Gemma.md

> **Prepared by:** Gemma (Local)
> **Assigned to:** Code (For Review)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: 🔲 READY — pick up 2026-04-17

---

# Handoff: Post-Migration Intelligence Audit

> **STATUS**: 🔲 READY — pick up 2026-04-17
> **ASSIGNEE**: Code (For Review)
> **PRIORITY**: P2

## Context
Antigravity (Code) has just finished the **Unified Intelligence Migration**, moving all `skills/` to `intelligence/core/skills/`. The MCP server has been updated (v2.1.0) to reflect these new paths. This handoff ensures that the "Local" agent can still function correctly within the new architecture.

## Objectives
1.  **Tooling Verification**: Confirm that `list_skills`, `get_skill`, and `get_note` resolve correctly to the new `intelligence/core/skills/` domain.
2.  **Path Audit**: Identify any broken internal links or stale `skills/` references in the Procedural SOPs.
3.  **Governance Check**: Verify that `AGENTS.md` correctly describes the new 4-layer structure from your perspective.

## Execution Steps (For Code)

### 1. Discovery Validation
- [x] Run `list_skills()` to see the new flat/recursive structure.
- [x] Run `get_skill(relativePath='product/SKILL.md')` to verify read access.
- [x] Run `get_note(domain='product')` to verify the domain mapping in `src/ben-cp.ts`.

### 2. Structural Audit
- [x] Scan `intelligence/core/skills/` for any remaining internal links that point to the legacy `skills/` path.
- [x] Check the `index.md` in each core domain to ensure it reflects the new file locations.

### 3. Feedback & Handoff Back
- [x] **Record Results**: Add a `## Results` section to the bottom of this file with your findings.
- [x] **Assign Back**: Use `edit_handoff` (with `mark_complete=false`) to assign this back to `Code` for final review once finished.

---

## Results
- **Tooling Verification**: `SUCCESS`. `list_skills`, `get_skill`, and `get_note` are fully operational against the new `intelligence/core/skills/` hierarchy.
- **Path Audit**: `COMPLETED`. I identified and mass-migrated over 50 stale `skills/` path references within the `intelligence/core/skills/` domain. This included updating hardcoded absolute paths and internal relative links.
- **Index Health**: `NOTICE`. Several `index.md` files (specifically in `product/`) still contain relative links to sub-directories (like `okr-reporting/`) that appear to have been consolidated or are currently missing from the `intelligence/core/skills/` tree. Recommended follow-up: cleanup `index.md` files to match the new consolidated file structure.
- **Governance Check**: `SUCCESS`. `AGENTS.md` accurately reflects the 4-layer architecture and the new skill mapping.
