# Implementation Plan: weekly-status-skill-migration

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Claude
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS: ✅ COMPLETE — 2026-04-13**

Migrated weekly-status-update skill into the vault at skills/product/weekly-status/. Source content taken from the Cowork plugin spec shared in-session. Created index.md, procedure.md (full four-step spec: Asana fetch + bucketing, Jira fetch + status overrides + batching, card format with all emoji/flag/time bar rules, report structure with data quality and summary sections), and changelog.md. Updated product/index.md and skills/index.md. Cowork plugin remains the runtime version; vault is now the canonical reference.

**Changelog:** (see root changelog.md)


---

## Context

The `weekly-status-update` skill lives in Ben's Cowork plugin. It generates the Platform weekly status report from Asana project data and linked Jira child issues. This handoff tracks its migration into the vault.

**Status:** ✅ Already executed this session (2026-04-12). Closing for record-keeping.

## What Was Done

- Created `skills/product/weekly-status/index.md` — purpose, modes, key config table, companion skills, source-of-truth note
- Created `skills/product/weekly-status/procedure.md` — full spec: mode detection, Step 1 (Asana fetch + bucketing + sort), Step 2 (Jira fetch + status overrides + batching), Step 3 (card format with all rules), Step 4 (report structure, data quality, summary narrative)
- Created `skills/product/weekly-status/changelog.md`
- Updated `skills/product/index.md` to register the new skill
- Updated `skills/index.md` to reflect expanded product/ scope

## Next Tasks

1. Keep vault procedure.md in sync when plugin SKILL.md is updated
2. Consider whether weekly-status and status-reports/ should be consolidated — they cover similar ground from different angles
