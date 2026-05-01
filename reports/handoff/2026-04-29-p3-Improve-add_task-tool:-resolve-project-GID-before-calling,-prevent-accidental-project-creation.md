---
title: "Improve add_task tool: resolve project GID before calling, prevent accidental project creation"
priority: P3
assigned_to: Code
status: READY
date: 2026-04-29
---
# Implementation Plan: Improve add_task tool: resolve project GID before calling, prevent accidental project creation

> **Prepared by:** Code (Gemini) (2026-04-29)
> **Assigned to:** ben
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3
> **STATUS**: 🔲 READY — pick up 2026-04-29

---

## Problem

When Claude calls `ben-cp:add_task` without an `asana_project_gid`, the tool silently creates a **new Asana project** instead of failing or prompting for clarification. This is surprising and destructive behavior — the user has to manually find and delete the errant project.

This happened in a real interaction: a user asked Claude to log a task in the "Bulk Service Notes" project. Claude called `add_task` without first resolving the GID, and a new project was created. Claude had to then call `asana_typeahead_search` to find the correct GID and re-submit.

## Root Cause

Two issues:
1. **Tool fallback behavior**: `add_task` should not silently create a project when no `asana_project_gid` is provided. It should either error or require the field.
2. **No GID resolution prompt**: The tool description doesn't signal to Claude that it must resolve the project GID first. Claude treated `asana_project_gid` as optional and skipped it.

## Recommended Fix

**Option A — Enforce GID in the tool:**
Make `asana_project_gid` a required field in `add_task`. This forces Claude (or any caller) to look it up first. If the caller doesn't know it, they must search before proceeding.

**Option B — Add a project name field with auto-resolution:**
Accept a `asana_project_name` string as an alternative, and have the tool itself call `asana_typeahead_search` internally to resolve it before creating the task. This is more ergonomic but adds complexity server-side.

**Option C — Fail loudly with a helpful error:**
If `asana_project_gid` is absent, return an error like: `"No project GID provided. Please search for the project first using asana_typeahead_search and pass the GID."` This preserves optionality but prevents silent misbehavior.

**Recommended:** Option C short-term (quick fix), Option B long-term (best UX).

## Also Consider

Update the `add_task` tool description to include a note like:
> "If adding to an existing project, you MUST resolve the project GID first via `asana_typeahead_search` before calling this tool."

This primes Claude to do the right thing without code changes.

## Execution Steps

- [🔲] **Tool Description Update**: Update `add_task` description in `src/ben-cp.ts` to mandate GID resolution.
- [🔲] **Validation Logic**: Implement Option C (fail loudly if GID is missing).
- [🔲] **Build & Deploy**: Run `npm run build` and `refresh_mcp`.
- [🔲] **Verification**: Test `add_task` without GID and confirm error message.

