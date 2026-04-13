# Concept: Unified Task Aggregation Pipeline

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P3
> **STATUS: 🔲 READY — pick up when P1/P2 queue is clear**

---

## Goal

Pull "assigned to Ben" work from Asana and Jira into a single vault-side task list so agents can help prioritize, draft deliverables, and codify results — without Ben having to manually bridge the two systems.

## Proposed Architecture

- **Pipeline Home:** `orchestration/pipelines/tasks/unified/`
- **Standard Structure:**
  - `pipeline/` — Python harvesting logic (multi-service)
  - `inputs/` — raw API seeds (task GIDs, issue keys)
  - `outputs/` — staged `.md` task files mapped to `tasks/incoming/`
  - `schemas/` — Unified Task Schema

**Unified Task Schema (draft):**
```
Title, Source System, Source ID, URL, Due Date, Priority, Status, Context/Notes
```

**Execution modes:**
- "New" tasks → create a new `.md` in `tasks/incoming/`
- "Updated" tasks → diff against existing file, patch in place
- Agents can then use `get_task` / `edit_task` to help work the backlog

---

## Concrete First Steps

1. **Scaffold the pipeline directory**: Create `orchestration/pipelines/tasks/unified/` with a `README.md` describing the architecture above and a `schemas/unified-task-schema.md` with the field definitions.
2. **Build Asana MVP harvester**: Write `pipeline/harvest_asana.py` that calls `mcp__300a198f__get_my_tasks` and writes one `.md` file per task to `outputs/`. Asana is the simpler starting point — Jira can be layered in after.
3. **Validate with a smoke test**: Run the harvester, confirm at least 3 tasks land in `outputs/` with correct fields, and spot-check against what Ben actually sees in Asana.
4. **Wire Jira**: Add `pipeline/harvest_jira.py` using `searchJiraIssuesUsingJql` with `assignee = currentUser() AND resolution = Unresolved`. Merge output into the same `tasks/incoming/` format.
5. **Create `tasks/incoming/index.md`**: Auto-generated index of all staged tasks, sorted by due date.

## Open Questions for Ben

- Should tasks from both systems land in a single flat list, or stay separated by source (Asana vs. Jira sections)?
- What's the right cadence for the harvester to run — daily at a set time, or on demand?
- Should completed/closed tasks be automatically archived out of `tasks/incoming/`?
