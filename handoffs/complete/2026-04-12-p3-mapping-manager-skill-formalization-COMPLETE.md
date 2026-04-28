---
title: 'Implementation Plan: Mapping Manager Skill Formalization'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: Mapping Manager Skill Formalization

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Ben
> **Repo root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P3
> **v1.0**
> **STATUS**: ✅ COMPLETE — 2026-04-26

Converted to task: mapping-manager-skill-formalization. Design conversation needed before agent execution — parked as a Ben task until direction is set.

---

## Context

With the consolidation of mapping logic into `skills/memory/mapping/`, there is now a centralized source of truth for interpretive logic (like OKR status health). However, these files are currently static. A "Mapping Manager" skill is needed to oversee consistency — defining how mappings get updated and validated as the repo evolves.

## Tasks

1. **Define `mapping/SKILL.md`**: Create a formal procedure for updating and validating mappings.
2. **Schema Integration**: Ensure all mapping files (e.g., `status_mapping.md`) follow a consistent JSON or Markdown schema.
3. **Cross-skill Verification**: Whenever a major skill is added (e.g., Finance or Legal), the Mapping Manager should ensure its interpretation logic is registered in the Memory Store.
4. **Draft 'Mapping Update' Procedure**: Define how an agent requests a change to a global mapping — what triggers a change, who reviews it, and how it gets logged.

## Success Criteria

Any agent can confidently reference `skills/memory/mapping/` to determine the correct way to transform raw data into a status or interpretation, and the procedure for proposing a change is documented and followable.

## Note for Ben

This is a design task before it's an execution task — the key decision is what the "Mapping Update" procedure should look like. Once that's settled, the SKILL.md writes itself. Worth a quick conversation before an agent dives in.
