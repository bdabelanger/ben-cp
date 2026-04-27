---
title: 'Implementation Plan: Mutual Exclusion Audit — Roadmap Intelligence'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Mutual Exclusion Audit — Roadmap Intelligence

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P1
> **STATUS**: ✅ COMPLETE

Audited 18+ project files and 10+ OKR/KR files in the Q2 roadmap. Implemented 'OKR Mapping' in tactical project files and 'Constituent Projects' lists in strategic OKR/KR files using vault-relative paths. Verified the separation of concerns, ensuring project files focus on technical status while OKR files handle governance and measurement methodology.

---

## Context

The `product` intelligence domain has been consolidated under `roadmap/` with three distinct layers:
1. `shareout/`: Strategic messaging, slide content, and presentation narrative.
2. `projects/`: Tactical execution, technical status (Asana/Jira), and project-specific metadata.
3. `okrs/`: Governance layer, objectives, and key results (cross-project metrics).

## The Principle of Mutual Exclusion

To prevent data duplication and agent confusion, we are enforcing a strict separation of concerns:

### 1. Projects (Tactical)
- **Content:** Technical status, GIDs, Permalinks, Engineering leads, and per-project updates.
- **Linkage:** Each project file should link to its parent OKR(s) in the `okrs/` domain.
- **Mutual Exclusion:** DO NOT maintain KR baseline data or cross-project outcome tracking within a project file.

### 2. OKRs (Governance)
- **Content:** Objectives (e.g., "Elevate Notes Experience") and KRs that may span multiple projects. Maintained metrics and high-level results live here.
- **Linkage:** OKR files should link to the individual projects contributing to them in the `projects/` domain.
- **Mutual Exclusion:** DO NOT maintain per-project status updates or Jira ticket lists inside an OKR file.

## Execution Steps

1. **Audit `projects/q2/`**: Review all 18+ project files. Ensure they have a link to their corresponding OKR in `roadmap/okrs/q2/`.
2. **Audit `okrs/q2/`**: Ensure each KR/Objective file properly links to its constituent projects in `roadmap/projects/q2/`.
3. **Data Cleanup**:
    - If you find a Project file containing deep KR methodology/baselines, move that data to the OKR file.
    - If you find an OKR file containing tactical Jira updates, move that data to the Project file.
4. **Link Integrity**: Use vault-relative paths for all links.

## Success Criteria
- [ ] Every project in `roadmap/projects/q2/` has an "OKR Mapping" field or link.
- [ ] Every OKR in `roadmap/okrs/q2/` has a "Constituent Projects" list.
- [ ] No duplicative technical status exists in the `okrs/` domain.
