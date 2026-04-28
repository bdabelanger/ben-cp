# Implementation Plan: Refactor Intelligence and Art Tooling (Standardization)

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Any
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Context
As part of the tool verb standardization, the **Intelligence and Art** domains need to be updated. Specifically, linking logic is being merged into the editing tool to reduce tool sprawl.

# Logic
- Merge `connect_intelligence` functionality into `edit_intelligence`.
- Standardize verbs:
    - `get_intelligence` (Get instead of Read)
    - `add_art` (Add instead of Contribute)
    - `get_art` (Get instead of Read)
- Standardize descriptions for `search_intelligence` and `list_intelligence`.
- Reorder tools in `ben-cp.ts` as per the new schema.

# Execution Steps
- [ ] Update `edit_intelligence` handler to support optional linking arguments (`relationship`, `targetPath`).
- [ ] Remove `connect_intelligence` tool and handler.
- [ ] Update definitions and handlers for `add_art`, `get_art`, `get_intelligence` with standardized verbs and descriptions.
- [ ] Update tool definitions array order in `src/ben-cp.ts`.
- [ ] Build server and verify.
- [ ] Update `AGENTS.md` documentation.