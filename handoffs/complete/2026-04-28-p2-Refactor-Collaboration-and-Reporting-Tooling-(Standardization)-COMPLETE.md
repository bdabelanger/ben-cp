# Implementation Plan: Refactor Collaboration and Reporting Tooling (Standardization)

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Any
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Context
Final phase of the tool verb standardization. This covers handoffs, changelogs, reporting, and external system sync (Asana/Jira).

# Logic
- Standardize verbs:
    - `generate_report` -> `run_report`
    - `capture_task` -> `add_task`
    - `create_asana_project` -> `add_asana_project`
    - `create_asana_task` -> `add_asana_task`
    - `create_jira_issue` -> `add_jira_issue`
- Update all "Read" descriptions to "Get".
- Reorder tools in `ben-cp.ts` (Reports, Handoffs, Changelogs, then Asana/Jira).

# Execution Steps
- [ ] Rename `generate_report` to `run_report` (definition and handler).
- [ ] Rename `capture_task` to `add_task` (definition and handler).
- [ ] Rename Asana/Jira "create" tools to "add" tools.
- [ ] Standardize all descriptions to use Get/Add/Edit/Run/List/Link/Search consistently.
- [ ] Update tool definitions array order in `src/ben-cp.ts`.
- [ ] Build server and verify.
- [ ] Update `AGENTS.md` documentation.