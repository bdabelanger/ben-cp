---
title: 'Implementation Plan: universal-skill-deployment'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: universal-skill-deployment

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code / Antigravity
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.2**
> **STATUS**: ✅ COMPLETE

---

## Context
While the Knowledge and Access domains had their `procedure.md` files merged into their `SKILL.md` wrappers, a vault audit revealed that several domains (such as `okr-reporting` and `rovo`) still rely on divergent instruction files like `procedure.md` or `rovo-sop.md` because they entirely lack a formal `SKILL.md` definition.

## The Claude Perspective
> **Injected by:** Claude (Cowork) (2026-04-12)

This is the most foundational handoff in the current batch — everything else (Digest Editor routing, `character.md` fallbacks, `report_spec.json`, python wrappers) assumes every skill has a well-formed `SKILL.md`. Getting this right unblocks the rest.

Character names belong exclusively in `character.md` files. `SKILL.md` files and all routing/index references use the generic skill name only.

**On the standard `SKILL.md` structure:**
When drafting new `SKILL.md` files, each should follow a consistent header block so agents can load them predictably. Recommended standard sections:

```
# Skill: <name>
> Preferred Agent: <agent name>
> Cadence: daily | weekly | on-change | on-demand
> Report: yes | no

## Purpose
## Procedure
## Output Format
## Notes / Edge Cases
```

Note: `character.md` lives separately in the same skill directory and is loaded alongside `SKILL.md` at invocation time — it is not referenced or embedded in `SKILL.md` itself.

The `Preferred Agent`, `Cadence`, and `Report` frontmatter fields feed directly into `report_spec.json` generation — if Digest Editor can read them from `SKILL.md`, a separate `report_spec.json` may not be needed as a standalone file. Consider collapsing the two.

**On priority order for drafting missing `SKILL.md` files:**
Not all missing skills are equal. Tackle in this order:
1. Skills already referenced in Digest Editor's run order (changelog, handoff, knowledge, access) — these are blocking the Digest.
2. Skills with active `run.py` work in progress (changelog, knowledge from the python-wrappers handoff).
3. Remaining skills (okr-reporting, rovo, etc.) — lower urgency, rename/migrate is sufficient.

**On `AGENTS.md` path reference tables:**
When updating these, add a `preferred_agent` column to the skill registry table. This gives any agent a single place to look up routing intent without opening individual `SKILL.md` files.

## Execution Plan
1. Scan the entire `skills/` directory tree to identify every skill currently lacking a `SKILL.md`.
2. For `okr-reporting`, rename `procedure.md` to `SKILL.md` and update its header block to match standard skill loading.
3. For `rovo`, rename `rovo-sop.md` to `SKILL.md` and update its header block.
4. For all other skills found lacking a `SKILL.md` (changelog, handoff, etc.), draft a cohesive `SKILL.md` using the standard structure above — prioritizing skills in Digest Editor's run order first.
5. Evaluate whether `report_spec.json` can be eliminated in favor of frontmatter fields in `SKILL.md`. Consolidate if viable.
6. Update `AGENTS.md` path reference tables to reflect universal `SKILL.md` naming, and add a `preferred_agent` column to the skill registry.
