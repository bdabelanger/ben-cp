---
title: Orchestration Changelog
type: changelog
domain: skills
---

# Orchestration Changelog

> Detail log for `skills/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-16 — Implement Jira Fix Version Alignment Audit logic in project reporting pipeline

**Files changed:**
- `orchestration/pipelines/product/projects/pipeline/platform_report.py` — Implemented 4-bucket logic for Jira fix version alignment (Aligned, Stalled, Lagging, Unmapped) Complete
- `orchestration/pipelines/product/projects/pipeline/step_3_jira_harvest.py` — Added retrieval of missing release date and raw ticket status for use in pipeline logic Complete
- `orchestration/pipelines/product/projects/pipeline/platform_report.py` — Normalized visual emoji alignment to left-side usage across issues and metadata flags Complete

**Next:** Validate the alignment data mapping against Asana Push corrections


## 2026-04-12 — Build repo-native CRU tools for notes.md so agents never need shell or filesystem access to read, write, or correct notes.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/src/ben-cp.ts` — Added read_notes, append_note, edit_note tools with NOTES_DOMAIN_MAP and server-side ownership enforcement ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/dist/` — Rebuilt — tsc compile clean ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/notes/SKILL.md` — Rewrote to document new tools with copy-paste examples, removed all shell_exec patterns ✅ Complete

**Next:** Restart ben-cp MCP server so new tools are live (read_notes, append_note, edit_note)


## 2026-04-12 — Give agents concrete, low-ambiguity CRU tool patterns for notes.md so they stop relying on absolute path guessing or fabricating non-existent tool names.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/notes/SKILL.md` — Rewrote as Notes & Context skill with explicit CRU tool patterns, Notes Map table, and ownership rule ✅ Complete

**Handoff:** `handoff/complete/2026-04-12-p2-refactor-communication-to-notes-skill-COMPLETE.md`

**Next:** Update the 3 hardcoded skills/notes/ path references in predict/SKILL.md, synthesize/audit.md, and shared/separation-policy.md if naming ever changes


## 2026-04-12 — Verify structural integrity of intelligence/ and orchestration/ domains post-refactor, and clean up side-effects from prior agent session.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/orchestration/notes/` — Deleted rogue directory created at repo root by prior agent (Gemma) — was not in repo path ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/index.md` — Fixed broken link: collaboration/index.md → communication/index.md ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/intelligence/index.md` — Verified clean — no corruption from prior agent's failed shell commands ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/notes/notes.md` — Verified readable at correct repo-relative path (smoke test step 3 had wrong path in handoff) ✅ Complete

**Handoff:** `handoff/complete/2026-04-12-p4-intelligence-smoke-test-fresh-chat-COMPLETE.md`

**Next:** Pick up p2-refactor-communication-to-notes-skill handoff — the real, staged refactor. communication/ skill is solid, just needs naming decision and cross-ref audit.


## 2026-04-12 — Refactor the orchestration/communication skill into a dedicated, standardized orchestration/notes structure to improve path independence.

**Files changed:**
- `orchestration/notes/SKILL.md` — Migrated content from old communication skill to new notes skill definition. ✅ Complete
- `intelligence/index.md` — Updated description to reference the new standardized notes system for reporting context. 🟡 Partial

**Handoff:** `handoff/complete/2026-04-12-p2-migrate-communication-to-notes-skill-COMPLETE.md`

**Next:** Perform a final audit pass on all domain indexes (e.g., orchestration/index.md) to ensure all references point to `orchestration/notes/SKILL.md` and not old paths.

