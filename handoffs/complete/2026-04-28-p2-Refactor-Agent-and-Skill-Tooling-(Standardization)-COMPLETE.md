# Implementation Plan: Refactor Agent and Skill Tooling (Standardization)

> **Prepared by:** Code (Gemini) (2026-04-28)
> **Assigned to:** Any
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Context
The repo is undergoing a major standardization of tool verbs (LIST, GET, ADD, EDIT, LINK, SEARCH, RUN) to ensure consistency across the MCP server and documentation. This handoff focuses on the **Agent and Skill Governance** tools.

# Logic
- Rename `get_agent_info` to `get_agent`.
- Implement new `list_agents` tool which returns `agents/index.md` and `AGENTS.md`.
- Standardize descriptions for `list_skills` and `get_skill`.
- Reorder these tools to the top of the `ben-cp.ts` list.

# Execution Steps
- [ ] Implement `list_agents` handler in `src/ben-cp.ts`.
- [ ] Rename `get_agent_info` handler to `get_agent` and update its definition.
- [ ] Standardize descriptions for `list_skills` and `get_skill` (use "Get" instead of "Read").
- [ ] Update tool definitions array order in `src/ben-cp.ts`.
- [ ] Build server and verify.
- [ ] Update `AGENTS.md` documentation.