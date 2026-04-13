# Implementation Plan: Vault Intelligence Re-Indexing Audit

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Gemma
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P1
> **Constraint:** DO NOT create new intelligence records. FOCUS on updating `index.md` files and link integrity.
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

## Context

The `intelligence/product/` domain has been reorganized to align with a strategic roadmap hierarchy. `projects` have been moved underneath `roadmap/` to create a tiered Strategic → Tactical mapping. Many links in existing `index.md` files are now broken or pointing to ghost directories.

## Objectives

1. **Audit All Indices**: Traverse the `intelligence/` domain and locate every `index.md` file.
2. **Path Correction**:
    - `intelligence/product/projects/` → `intelligence/product/roadmap/projects/`
    - `intelligence/product/shareout/` → `intelligence/product/roadmap/shareout/`
3. **Link Verification**: Ensure all `file:///` and relative links in indices point to files that actually exist in the current vault structure.
4. **Link Consistency**: Prefer relative links within the `intelligence/` domain where possible.

## Execution Steps

1. **Root Audit**: Start at `intelligence/` root. If an index is missing, create one that points to the major sub-domains (product, mapping, casebook).
2. **Product Domain**: Deep-dive into `intelligence/product/`.
    - Verify `roadmap/index.md` points correctly to `roadmap/projects/index.md` and `roadmap/shareout/q2/index.md`.
    - Fix the `projects/index.md` (now at `roadmap/projects/index.md`) so its back-links to "Roadmap Root" are correct.
3. **Cross-Domain Audit**: Check `intelligence/mapping` and other folders for links that may be breaking due to the `product` move.
4. **No New Source Data**: If you find files that seem mislocated, DO NOT move them — simply update the indices to point to their current location or flag them in your session notes.

## Success Criteria

- [ ] No `404` or "No such file" errors when clicking links in `intelligence/product/index.md`.
- [ ] The `roadmap` index and `projects` index are correctly nested and interlinked.
- [ ] The `intelligence/product/` hierarchy is fully navigable for other agents.
