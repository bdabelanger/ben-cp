# Implementation Plan: interpretation-skill-grouping

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Consolidated the synthesis and predict skills into a new interpretation/ domain, cleaned up root-level junk (project-status-reports/), and normalized all vault-wide references in AGENTS.md and the dream orchestrator. The collaboration group and unified notes system are also fully documented and synced.

**Changelog:** (see root changelog.md)


---

## Context
Currently, the `synthesis` (Robert) and `predict` (Bryan) agents operate inside standalone logic domains. Strategically, these abilities are highly interrelated facets of vault analysis. Grouping these under a unified functional capability will tighten context loading and reduce root-level vault sprawl.

## Execution Plan
1. Create a new `skills/interpretation/` domain directory.
2. Natively migrate both the `skills/synthesis/` and `skills/predict/` directories underneath this new `interpretation` umbrella (`skills/interpretation/synthesis/` and `skills/interpretation/predict/`).
3. Ensure their individual outputs directories map correctly.
4. Execute string-replacement queries across `AGENTS.md` and the individual agent files (e.g. `agents/robert.md`, `agents/bryan.md`) to re-route their skill procedures and character config pointers to the nested `skills/interpretation/` paths.