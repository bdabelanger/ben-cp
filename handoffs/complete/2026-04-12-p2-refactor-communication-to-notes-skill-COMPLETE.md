---
title: 'Implementation Plan: refactor-communication-to-notes-skill'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: refactor-communication-to-notes-skill

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Gemma
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Refactored orchestration/communication/SKILL.md from abstract principles to concrete CRU tool patterns. Renamed the skill internally from 'Communication' to 'Notes & Context'. Added an explicit Notes Map table with absolute paths for every active notes.md in the repo, plus copy-paste-ready shell_exec patterns for Create (signed append), Read (get_skill or grep), and Update (own entries only, with correction-append as preferred pattern over direct sed edit). Directory kept as communication/ — no path changes needed, no cross-ref breakage. The ownership rule (agents may only edit their own signed entries) is now an explicit constraint in the U section rather than buried in general constraints.

**Changelog:** (see root changelog.md)


---

**Goal:** Refine the scope of `orchestration/communication` to explicitly center on collaborative note-taking, aligning its name and documentation with the repo's primary use case for shared context.

**Execution Plan:**
1. **Update SKILL Definition:** Modify `orchestration/communication/SKILL.md` to change its internal focus from general 'Communication' to 'Collaborative Notes & Context'. The core rules (Sign, Append only) must remain intact.
2. **Review Cross-References:** Scan other domain indexes (`intelligence/index.md`, etc.) for any hardcoded references to `communication/` and update them to point toward the refined skill or a new dedicated notes endpoint if necessary.
3. **Address Collaboration Layer:** Determine how this 'Notes' function integrates with the broader 'Collaboration' layer mentioned in `orchestration/index.md`. If they are distinct, we must define the boundary; if they overlap, we consolidate.
4. **Finalize Naming:** Propose a final name change (e.g., from `communication` to `notes`) only after step 2 and 3 confirm no breaking changes exist in other skills.

**Deliverables:** Updated `orchestration/communication/SKILL.md`, updated cross-references, and a decision on the final directory structure.