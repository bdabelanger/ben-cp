---
title: Code Implementation Plan Consolidating Skills into Intelligence
type: handoff
domain: handoffs/complete
---

# Code Implementation Plan: Consolidating Skills into Intelligence

> **Prepared by:** Human User / Cowork (Unified Intelligence Migration, 2026-04-15)
> **Assigned to:** Code
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — Major structural consolidation
> **STATUS**: ✅ COMPLETE

Successfully migrated procedural Skills into the Intelligence domain. Repointed all MCP tools, updated reporting pipelines, and overhauled AGENTS.md governance to reflect the new 4-layer architecture. Validated build and sync status.

---

## Context
The project is moving toward a **NotebookLM-centric** intelligence model. In this model, the distinction between "Skill Logic" (SOPs) and "Vault Truth" (Data) is an artificial barrier to synthesis. By consolidating `skills/` into the `intelligence/` domain, we enable unified search, cross-domain discovery, and automated indexing for our procedural knowledge.

This migration addresses structural debt where tools (like `sync.py`) and agents have to hunt across multiple top-level directories to find "what to do" vs "how to do it."

---

## Logic
Shift from a 5-layer model to a simplified 4-layer model where **Intelligence** encompasses both **Execution SOPs** and **Domain Facts**.
- **New Home**: `skills/`
- **System Domain**: Establish `intelligence/` for all system-level logic (policies, agents, skills).
- **Identity Maintenance**: Retain the `character.md` and `SKILL.md` file naming within the new domain to satisfy existing agent personas.
- **Tooling Consolidation**: Repoint or merge `get_skill` and `get_intelligence` to allow for a single "Knowledge Retrieval" surface.

---

## Execution Order
1. **Task 1** — Tooling & Pipeline Audit (Pre-migration)
2. **Task 2** — Governance Refactoring
3. **Task 3** — Physical Migration
4. **Task 4** — Automated Indexing & Promotion
5. **Task 5** — Cleanup
6. **Task 6** — Write changelog and mark complete

---

## Task 1: Tooling & Pipeline Audit (Pre-migration)
- **MCP Server**: Update `src/ben-cp.ts` constants (`skillsPath`) to point to the new `skills/` location.
- **Python Scripts**: Audit and refactor `tools/` (specifically `sync.py` and `report.py`) which contain hardcoded `skills/` path references for report generation and git-drift detection ("Snowed In" logic).

---

## Task 2: Governance Refactoring
- **AGENTS.md**: Overhaul the "Directory Boundaries" section.
- **Separation Policy**: Move `skills/orchestration/separation-policy.md` to `intelligence/governance/policy.md` and update its definitions.
- **Index Updates**: Add a new first-class domain to `intelligence/index.md`: `4. [Core Logic & Skills](core/index.md)`.

---

## Task 3: Physical Migration
- **Mkdir**: Create the new core hierarchy: `intelligence/{skills,governance,mapping}`.
- **Move**: `git mv skills/* skills/`.
- **Relink**: Update internal cross-links within moved SOPs.

---

## Task 4: Automated Indexing & Promotion
- Run the equivalent of `add_intelligence` on each moved skill. This "promotes" the SOPs to tracked intelligence records, ensuring they are included in the master domain indices.

---

## Task 5: Cleanup
- Remove the empty `skills/` root directory.
- Verify existing handoffs still resolve (the tools should handle the path re-pointing transparently).

---

## Task 6: Changelog + Completion

Write changelog entries (subdirectory first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Acceptance Criteria
- [ ] `skills/` directory is empty/removed.
- [ ] `get_skill(relativePath: 'orchestration/handoff/SKILL.md')` resolves correctly to `skills/handoff/SKILL.md`.
- [ ] NotebookLM-optimized header levels (H1/H2) are preserved across all moved SOPs.
- [ ] `sync.py` runs successfully against the new paths.
- [ ] `intelligence/index.md` links to the new `core/` domain.

---

## Notes for This Agent
- This is a structural P2 change. Ensure that `AGENTS.md` boundaries are thoroughly checked and that index changes reflect the logic.
- Execute tasks in the explicit order via git and file operations. Execute carefully and verify tools afterward.
