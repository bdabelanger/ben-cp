# Implementation Plan: Flatten skills pipelines into skills

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully flattened the skills directory by removing the redundant `pipelines/` wrapper. All core pipelines (Asana, Intelligence, Status, Tasks) now live directly under `skills/`. Updated the TS SDK, AGENTS.md governance, and all internal script/index references to ensure zero breakage in the orchestration layer. Scan

---

> **Prepared by:** Cowork (Claude) (2026-04-26)
> **Assigned to:** Code
> **Priority:** P2
> **STATUS**: 🔲 READY

---

## Context

`skills/pipelines/` is an unnecessary wrapper directory. The four skills inside it — `asana`, `intelligence`, `status`, and `tasks` — should live directly under `skills/` for easier navigation. Scripts are a valid optional component of any skill and don't need a `pipelines/` grouping to justify their existence.

Note: The legacy `skills/intelligence/` has already been archived, so there is no conflict with moving `skills/pipelines/intelligence/`.

## Goal

Move all four pipeline skills up one level and remove the `skills/pipelines/` wrapper.

## Execution Steps

1. Move `skills/pipelines/asana/` → `skills/asana/`
2. Move `skills/pipelines/intelligence/` → `skills/intelligence/`
3. Move `skills/pipelines/status/` → `skills/status/`
4. Move `skills/pipelines/tasks/` → `skills/tasks/`
5. Delete `skills/pipelines/` (including its `index.md` and `changelog.md`)
6. Update any references to `skills/pipelines/` across the repo (`AGENTS.md`, `skills/index.md`, any handoffs or intelligence records)

## Verification

- `skills/pipelines/` no longer exists
- `skills/asana/`, `skills/intelligence/`, `skills/status/`, `skills/tasks/` all exist with full contents intact
- No broken links pointing to `skills/pipelines/` (grep or run links sensor)
