# Tasks Changelog

## [Unreleased]

## 2026-04-27 — Re-run tasks report and fix stale path bugs in tasks domain.

**Files changed:**
- `reports/tasks/report.md` — Re-run tasks report to update Asana and Jira status. COMPLETED
- `src/ben-cp.ts` — Fixed stale orchestration/tasks path references in tool definitions. COMPLETED
- `src/ben-cp.ts (list_skills)` — Added try/catch to readdir call for non-existent domains. COMPLETED
- `skills/tasks/SKILL.md` — Updated hierarchy documentation to reflect root tasks/ directory. COMPLETED

**Next:** Restart the ben-cp MCP server to pick up the fixes for list_tasks and list_skills.

