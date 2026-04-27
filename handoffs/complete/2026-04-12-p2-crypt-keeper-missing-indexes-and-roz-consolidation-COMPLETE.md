---
title: Claude Code Implementation Plan Missing index.md Files  Roz Consolidation
type: handoff
domain: handoffs/complete
---

# Claude Code Implementation Plan: Missing index.md Files + Roz Consolidation

> **Prepared by:** Claude (Cowork) via knowledge skill run (2026-04-12)
> **Assigned to:** Claude Code
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — structural violations
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-12.md`
> **v1.0**
> **STATUS**: ✅ COMPLETE

---

## Context
The knowledge skill run on 2026-04-12 identified three skill directories missing `index.md` files, and confirmed that `agents/roz.md` is redundant with `skills/access/` now that the access skill has a full `SKILL.md` and `character.md`. Consolidating removes a maintenance split.

---

## Execution Order

1. Add `index.md` to `skills/dream/`
2. Add `index.md` to `skills/predict/`
3. Add `index.md` to `skills/changelog/lumberjack/`
4. Archive `agents/roz.md` — consolidate access auditor into `skills/access/`
5. Write changelog and mark complete

---

## Task 1: Add index.md to skills/dream/

Create `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/dream/index.md`:

```markdown
# Skill: Dream (Orchestrator)

> **Purpose:** Nightly Digest orchestration — runs all skill agents in sequence and compiles daily output.
> **Preferred Agent:** Digest Editor
> **Cadence:** Daily
> Last updated: 2026-04-12

---

## Overview

The dream skill is the Editor-in-Chief of the nightly Digest cycle. It reads each skill's `report_spec.json`, invokes the preferred agent for each, collects structured output envelopes, and compiles the Digest (HTML + MD) for the next day's agents to read on startup.

## Files

- [character.md](./character.md) — Voice and persona definition
- [run.py](./run.py) — Orchestrator script (Digest Editor)
- [outputs/](./outputs/) — Digest outputs archive
```

---

## Task 2: Add index.md to skills/predict/

Create `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/predict/index.md`:

```markdown
# Skill: Predict

> **Purpose:** Forward-looking analysis skill — in development.
> Last updated: 2026-04-12

---

## Files

- [character.md](./character.md) — Voice and persona definition
- [report_spec.json](./report_spec.json) — Report spec for Digest Editor integration
- [outputs/](./outputs/) — Skill outputs
```

---

## Task 3: Add index.md to skills/changelog/lumberjack/

Create `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/changelog/lumberjack/index.md`:

```markdown
# Skill: Changelog / Changelog Auditor (Character)

> **Purpose:** Character definition subdirectory for the changelog skill.
> Last updated: 2026-04-12

---

## Files

- [character.md](./character.md) — Voice and persona definition for the changelog skill agent
```

Also add a reference to the `lumberjack/` subdirectory in `skills/changelog/index.md` if not already present.

---

## Task 4: Archive agents/roz.md

The access auditor role is fully defined in `skills/access/SKILL.md` and `skills/access/character.md`. `agents/roz.md` is now redundant.

1. Read `agents/roz.md` — confirm no unique content exists that isn't already in `skills/access/`
2. If clean: `git mv agents/roz.md agents/archive/roz-archived-2026-04-12.md` (create `agents/archive/` if it doesn't exist)
3. Update `agents/index.md` (if it exists) to reflect the removal
4. Note: `AGENTS.md` role dispatch table update is handled in the P1 handoff — do not edit `AGENTS.md` here

---

## Task 5: Changelog + Completion

Write changelog entries (subdirectory first at `skills/knowledge/changelog.md`, then root `changelog.md`), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Do not edit `AGENTS.md` in this task — that is fully covered by the P1 handoff.
- Character names are not used in skill references outside of `character.md` files.
- Read each target directory before creating any new files.
