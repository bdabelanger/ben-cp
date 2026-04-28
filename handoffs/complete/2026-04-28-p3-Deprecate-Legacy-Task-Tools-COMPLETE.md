# Implementation Plan: Deprecate Legacy Task Tools

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Any
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-28

Removed legacy task tools (add_task, edit_task, list_tasks, get_task) from the MCP server source code and rebuilt the server. Updated AGENTS.md and the root changelog to reflect the new sync-first task management policy. Agents should now use generate_report(skill='tasks') for reading and capture_task for intake.

---

# Implementation Plan: Deprecate Legacy Task Tools

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-28

---

# Context
The repo has moved to a sync-first model for tasks (from Asana/Jira). The legacy tools for manual task management (`add_task`, `edit_task`) are already logically deprecated in `AGENTS.md` and are causing confusion. Furthermore, the specialized `list_tasks` and `get_task` tools are redundant as the `tasks/` directory can be treated as a standard read-only directory.

# Logic
1.  **Remove Write Tools**: Physically remove the `add_task` and `edit_task` tools from `src/ben-cp.ts`.
2.  **Remove Read Tools**: Remove `list_tasks` and `get_task`. Agents should use the `tasks` skill report or standard filesystem tools to read synced tasks if necessary.
3.  **Governance Cleanup**: Update `AGENTS.md` to remove these tools from the tool list and update the "Tasks" terminology section to reflect the removal of specialized tools.

# Execution Steps
1.  **Modify `src/ben-cp.ts`**:
    *   Remove `add_task`, `edit_task`, `list_tasks`, and `get_task` from `ListToolsRequestSchema`.
    *   Remove their respective handlers from `CallToolRequestSchema`.
2.  **Build**: Run `npm run build` to apply changes.
3.  **Update `AGENTS.md`**:
    *   Remove the deprecated tools from the MCP Tools table.
    *   Ensure the "Tasks" section clearly states that tasks are read-only and managed via Asana/Jira.
4.  **Verification**: Confirm the tools are no longer listed in the MCP server.

# Verification
- [ ] `add_task`, `edit_task`, `list_tasks`, and `get_task` are gone from the tool list.
- [ ] `AGENTS.md` is updated and consistent.
- [ ] `capture_task` and `generate_report(skill='tasks')` remain functional.
