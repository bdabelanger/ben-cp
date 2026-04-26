# Design: Mapping Manager Skill Formalization

- **priority:** P3
- **assigned_to:** Ben
- **source_handoff:** 2026-04-12-p3-mapping-manager-skill-formalization.md
- **created:** 2026-04-25

# Design: Mapping Manager Skill Formalization

> **Priority:** P3
> **Assigned to:** Ben
> **Source handoff:** 2026-04-12-p3-mapping-manager-skill-formalization.md
> **Created:** 2026-04-25

## Context

Mapping logic is now centralized in `skills/memory/mapping/` but files are static. A Mapping Manager skill is needed to define how mappings get updated and validated as the vault evolves.

## This is a design task first

The key decision is what the "Mapping Update" procedure should look like — once that's settled, the SKILL.md writes itself. Have the design conversation before handing to an agent for execution.

## Scope (once design is settled)

1. Define `mapping/SKILL.md` — procedure for updating and validating mappings
2. Ensure all mapping files follow a consistent schema
3. Cross-skill verification rule: new skills must register interpretation logic in the Memory Store
4. Draft "Mapping Update" procedure — what triggers a change, who reviews, how it gets logged

## Success Criteria

Any agent can reference `skills/memory/mapping/` to determine the correct way to transform raw data into a status or interpretation, and the procedure for proposing changes is documented and followable.

