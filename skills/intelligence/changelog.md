---
title: Intelligence Skill Changelog
type: changelog
domain: skills/intelligence
---

# Intelligence Changelog

## [Unreleased]

## 2026-04-28 — Deprecate legacy intelligence tools.

**Files changed:**
- `src/ben-cp.ts` — Removed legacy intelligence tools (synthesize_intelligence, predict_intelligence, audit_intelligence) from ben-cp MCP server. done
- `src/ben-cp.ts` — Restored accidentally removed search_intelligence and connect_intelligence tool definitions. done

**Next:** Confirm tool removal with user.


## 2026-04-27 — Fix ghost links across the repo

**Files changed:**
- `intelligence/product/projects/asana_field_definitions.md` — Fixed broken source_file link.
- `intelligence/governance/policy.md` — Fixed broken example link.
- `skills/index.md`, `intelligence/casebook/reporting/schema_joins.md` — Removed stale/broken links.

## 2026-04-27 — Implement the intelligence harvest script

**Files changed:**
- `skills/intelligence/01_harvest.py` — Implemented with support for Asana projects and Jira epics.
- `skills/asana/scripts/01_fetch_projects.py` — Added .env loading and corrected REPO_ROOT path.
- `intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md` — Instrumented with sources frontmatter.

**Next:** Implement Confluence URL fetching in 01_harvest.py (Step 4 of spec)
