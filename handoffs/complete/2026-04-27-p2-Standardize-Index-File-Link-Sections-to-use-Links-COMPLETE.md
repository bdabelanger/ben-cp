---
title: 'Implementation Plan: Standardize Index File Link Sections to use Links'
type: handoff
domain: handoffs
---


# Implementation Plan: Standardize Index File Link Sections to use Links

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully replaced non-standard link headers (Navigation, Documentation, Core Logic, Components, Resources) with `## Links` across all index files in the vault. Verified with `grep_search` that no legacy headers remain.Scan

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

Index files across the vault use inconsistent section headers for links — both internal and external. Observed variants include:

- `## Documentation`
- `## Components`
- `## Core Logic`
- `## Records (Vault Shadow Files)`
- `## Constituent Projects`
- `## References`
- `## Resources`

These all serve the same purpose: a list of links relevant to that index. The standard going forward is `## Links`.

## Goal

Replace all link-section headers in `index.md` files across the vault with `## Links`.

## Execution Steps

1. Find all `index.md` files in the vault (excluding `node_modules`, `dist`, `reports`, `src`)
2. For each file, identify any heading that is used purely as a link list section — i.e. the section body contains only bullet-point links
3. Replace those headings with `## Links`
4. Where a file has multiple link sections with different groupings (e.g. internal vs. external), collapse into a single `## Links` section where sensible, or use `## Links` with sub-groupings if distinction is meaningful
5. Update `skills/dream/index.md` specifically — it currently uses `## Core Logic` and `## Components`

## Verification

- Grep for `## Documentation`, `## Components`, `## Core Logic`, `## Records`, `## Constituent Projects`, `## Resources`, `## References` across all `index.md` files — result should be zero
- Spot-check 5 index files to confirm `## Links` section is present and correct
