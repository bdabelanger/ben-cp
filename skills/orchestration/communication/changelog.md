# Input Changelog

> Detail log for `skills/input/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-12 — Vault Path Normalization: Flattened Orchestration Domain

**Files changed:**
- `skills/orchestration/communication/SKILL.md` — Renamed domain to **Communication**, updated functional summary, and deployed global `notes.md` map for the new intelligence/orchestration hierarchy. ✅ Complete
- `skills/orchestration/communication/notes.md` — Signed final normalization mission summary. ✅ Complete

## 2026-04-12 — Deploy unified notes system across all agent skill domains

**Files changed:**
- `skills/collaboration/SKILL.md` — Rewrote to unified notes model — no human user notes distinction, single notes.md per skill, write/read/edit-own rules ✅ Complete
- `skills/access/notes.md` — Empty stub created — collaboration notes system deployed ✅ Complete
- `skills/changelog/notes.md` — Empty stub created ✅ Complete
- `skills/dream/notes.md` — Empty stub created ✅ Complete
- `skills/knowledge/notes.md` — Empty stub created ✅ Complete
- `skills/predict/notes.md` — Empty stub created ✅ Complete
- `skills/synthesis/notes.md` — Empty stub created ✅ Complete
- `skills/product/notes.md` — Empty stub created ✅ Complete

**Next:** Update AGENTS.md notes.md policy to remove human user notes distinction


## 2026-04-12 — Correct notes.md write policy — any agent may write to any notes.md vault-wide, entries must be signed with agent name and timestamp.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Updated notes.md write policy — any agent may write to any notes.md, append-only, signed entries required, agents own their followups ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/input/SKILL.md` — Rewrote to match corrected policy — collaborative scratchpad, signed entries, append-only, agents own followups ✅ Complete

**Next:** Execute P2 handoff: add missing index.md to dream/, predict/, changelog/lumberjack/ and archive agents/roz.md


## 2026-04-12 — Rename skills/input/captains-log.md to notes.md and establish universal notes.md write policy across the vault.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/input/notes.md` — Renamed from captains-log.md — content preserved, header updated to remove character name reference ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/input/SKILL.md` — Rewrote to define universal notes.md write policy: any agent may append to their own skill's notes.md, no agent may write to another skill's notes.md, skills/input/notes.md is persistent ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/input/index.md` — Updated to reference notes.md (was captains-log.md) ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Major update: added notes.md write policy section, fixed Session Pattern (notes.md + skills/pmm/report.md), updated vault structure diagram, fixed Roz dispatch to skills/access/SKILL.md, removed character name references ✅ Complete

**Next:** Execute P1 handoff: remaining AGENTS.md and skills/index.md fixes (skills/index.md rewrite)

