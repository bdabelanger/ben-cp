---
title: 'Implementation Plan: universal-skill-md-consolidation'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: universal-skill-md-consolidation

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code / Antigravity
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Audited the vault for the dual `procedure.md` / `SKILL.md` paradigm. Successfully identified the two domains (Knowledge and Access) containing structural duplicates. Rewrote both central `SKILL.md` files to natively incorporate exact procedural mechanisms, checklists, priorities, and workflow loops. Safely deleted the deprecated `procedure.md` files and routed all index pointers straight to `SKILL.md`.

**Changelog:** (see root changelog.md)


---

## Context
Currently, many functional domains within the vault (e.g. `skills/knowledge/`) suffer from mechanical redundancy by possessing both a `procedure.md` and a `SKILL.md` file. Claude's MCP conventions rely natively on parsing a defined `SKILL.md` file within a tool directory to understand its constraints and actions.

## Execution Plan
1. Audit the entire `skills/` directory tree.
2. For any skill that possesses both a `procedure.md` and a `SKILL.md`, consolidate all procedural steps, checks, formatting headers, and output templates natively into `SKILL.md`.
3. Delete the redundant `procedure.md` files (and any other redundant instructional splits like `diff_checker.md` if applicable, merging them up to `SKILL.md`).
4. Update their parent `index.md` files and any `AGENTS.md` pointing references to ensure nothing breaks during execution.