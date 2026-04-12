# Handoff: Resolve Gemini Root Edit Block and MCP Traversal

> **Assigned to:** Claude Code / Roz (Access Auditor)
> **Priority:** P1 — Agent Environment Blocker
> **Status:** 🔲 READY
> **Reference Plan:** [outputs/access/resolution/implementation_plan.md](../../outputs/access/resolution/implementation_plan.md)

---

## Context
During the Documentation Triad refactoring (Session 17-2), Antigravity encountered a persistent permission block in the App Data Root (`/Users/benbelanger/.gemini/antigravity/`). While `write_to_file` (Overwrite) is functional, `replace_file_content` (Edit) consistently fails with `context canceled`. 

Additionally, the Access Auditor (Roz) is currently blocked from auditing other agents because the `filesystem` MCP tool security policy denies symlink traversal to directories outside the allowed list (e.g., `~/.claude`).

## Execution Boundary
1. **MCP Configuration**: Update the `filesystem` MCP server arguments to include mandatory agent roots (`/Users/benbelanger/.claude/`, etc.) to enable cross-agent auditing for Roz.
2. **Environment Repair**: Investigate the native MacOS TCC/Sandbox restriction on the `~/.gemini` folder. Verify if the AI client requires Full Disk Access or a specific `chmod` reset.
3. **Artifact Recovery**: Once unblocked, migrate the temporary artifacts from `/outputs/access/resolution/` back into the standard Gemini brain artifact directory.

## Next Steps
- [ ] Read the detailed research brief in [the implementation plan](../../outputs/access/resolution/implementation_plan.md).
- [ ] Attempt a targeted `mcp_filesystem_list_directory` on `agent-roots/claude` after updating the config.
- [ ] Test the `edit_file` tool against a test artifact in the Gemini root.

---
*"Access is the skeleton of governance; currently, the bones are locked."*
