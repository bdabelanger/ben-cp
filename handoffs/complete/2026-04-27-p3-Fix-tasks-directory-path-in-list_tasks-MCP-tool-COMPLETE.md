# Implementation Plan: Fix Stale Path References in MCP Tools (list_tasks + list_skills)

> **Prepared by:** Cowork (Sonnet 4.6) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: ✅ COMPLETE — 2026-04-27

Updated src/ben-cp.ts to point to root tasks/ directory instead of orchestration/tasks/. Added try/catch to list_skills to prevent ENOENT errors on non-existent domains. Created root tasks/ directory. Rebuilt MCP server. Updated skills/tasks/SKILL.md. Note: MCP server needs a restart to pick up changes.

---

## Context

During a smoke test session on 2026-04-27, Cowork (Sonnet 4.6) identified **two MCP tool path errors** both caused by stale directory references surviving the repo's structural normalization (1.18.x era).

### Bug 1 — `list_tasks` ENOENT

Calling `list_tasks` throws:

```
Error: ENOENT: no such file or directory, scandir '/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/orchestration/tasks'
```

The tool is resolving to `orchestration/tasks` — a path that existed before the repo's directory restructure. Per AGENTS.md, the tasks directory now lives at repo root:

```
├── tasks/  ← (Symlink to tasks/)
```

### Bug 2 — `list_skills` ENOENT on domain param

Calling `list_skills` with `domain: "product"` throws:

```
Error: ENOENT: no such file or directory, scandir '...ben-cp/skills/product'
```

The `skills/product/` subdomain was dissolved during the Unified Repo Architecture normalization (changelog v1.18.0). The current `skills/` root now contains: `asana`, `changelog.md`, `dream`, `handoff`, `index.md`, `intelligence`, `releasinator`, `rovo`, `standup`, `status`, `styles`, `tasks`. There is no `product/` subdirectory.

This means either:
- The `list_skills` tool is not validating domain existence before scanning, OR
- Callers referencing the old `product` domain path need to be updated in repo documentation

Both bugs share a common root cause: path references not updated after the 1.18.x structural normalization.

---

## Logic

For **Bug 1**: Update `list_tasks` path from `orchestration/tasks` → the correct resolved tasks path at repo root.

For **Bug 2**: Two possible fixes — Code should determine which is appropriate:
- **Option A (preferred):** Add a graceful error or "domain not found" response in `list_skills` when the subdomain doesn't exist, rather than throwing ENOENT. This prevents misleading errors for any caller using stale domain names.
- **Option B:** If the tool already handles this correctly and the issue is documentation, update any repo docs still referencing `skills/product/` as a valid domain.

Both fixes are in `src/ben-cp.ts` and require a rebuild (`npm run build`).

---

## Execution Steps

- [ ] Open `src/ben-cp.ts` and locate the `list_tasks` tool definition — find the `scandir` path
- [ ] Confirm the correct resolved path for the tasks directory (`ls` at repo root or check AGENTS.md repo tree)
- [ ] Update `list_tasks` path reference to the correct location
- [ ] Locate the `list_skills` tool definition — review how the `domain` param is resolved and whether ENOENT is caught
- [ ] Implement Option A: wrap the `scandir` call for `list_skills` in a try/catch and return a clear "domain not found" message instead of throwing
- [ ] Run `npm run build` to rebuild `dist/ben-cp.js`
- [ ] Restart the MCP server
- [ ] Re-run `list_tasks` — confirm no ENOENT, returns task list or empty array
- [ ] Re-run `list_skills` with a valid domain (e.g. `"intelligence"`) — confirm works
- [ ] Re-run `list_skills` with a non-existent domain (e.g. `"product"`) — confirm graceful response, not ENOENT
- [ ] Write a changelog entry scoped to `src/`

## Acceptance Criteria

- `list_tasks` returns a task list (or empty array) without ENOENT
- `list_skills` with a non-existent domain returns a graceful message, not an unhandled ENOENT error
- `npm run build` passes cleanly
