# Tasks Changelog

## [Unreleased]

## 2026-04-28 — Deprecate legacy task tools in favor of sync-first model.

**Files changed:**
- `src/ben-cp.ts` — Removed legacy task tools (add_task, edit_task, list_tasks, get_task) from ben-cp MCP server. done
- `AGENTS.md` — Updated AGENTS.md to remove deprecated task tools and clarify task management policy. done

**Next:** Confirm tool removal with user.


## 2026-04-28 — Improve Transcripts Skill — Rich Meeting Support + capture_task Clarification

**Files changed:**
- `skills/tasks/SKILL.md` — Created SKILL.md to document the capture_task MCP tool and its routing logic. done
- `src/ben-cp.ts` — Updated capture_task schema to support optional fields (ACs, Figma, project override) and updated getPopulatedTemplate to make fields conditional. done
- `skills/transcripts/scripts/run.py` — Added --mode rich flag, heuristic context extraction, and improved routing hints based on description content. done
- `skills/transcripts/SKILL.md` — Updated to reflect rich mode and context extraction capabilities. done

**Next:** Run harvester on a real meeting transcript to verify context extraction quality.


## 2026-04-27 — Re-run tasks report and fix stale path bugs in tasks domain.

**Files changed:**
- `reports/tasks/report.md` — Re-run tasks report to update Asana and Jira status. COMPLETED
- `src/ben-cp.ts` — Fixed stale orchestration/tasks path references in tool definitions. COMPLETED
- `src/ben-cp.ts (list_skills)` — Added try/catch to readdir call for non-existent domains. COMPLETED
- `skills/tasks/SKILL.md` — Updated hierarchy documentation to reflect root tasks/ directory. COMPLETED

**Next:** Restart the ben-cp MCP server to pick up the fixes for list_tasks and list_skills.

