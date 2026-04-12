# Shared Changelog

> Detail log for `skills/shared/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-12 — Consolidate all stale/duplicate skill directories into intelligence domain, rename knowledge/ to intelligence/ at vault root, and establish the five-layer vault architecture.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/intelligence/` — Renamed from knowledge/ — vault source-of-truth store. Contains mapping/ and casebook/. Gitignored optional. ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/.gitignore` — Updated knowledge/ comment to intelligence/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/intelligence/dream/` — Moved from skills/dream/ — now canonically housed under intelligence domain ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/` — Deleted 9 stale duplicate dirs: interpretation/, memory/, changelog/, handoff/, access/, collaboration/, synthesize/, status-reports/, project-status-reports/ — all confirmed identical to canonical locations or already migrated ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Updated vault tree (five-layer arch), Directory Boundaries table (added intelligence/ layer), File Placement table (knowledge/ → intelligence/mapping/, stale dirs updated), notes.md policy path updated to orchestration/communication/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/index.md` — Removed casebook/ row (no longer in skills/), added shared/ row, updated Central Stores: knowledge/ → intelligence/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/shared/separation-policy.md` — Four Layers → Five Layers (added intelligence/ row), Known Migration Debt updated: status-reports items marked resolved, knowledge/ ref removed ✅ Complete

**Next:** Migrate skills/intelligence/report/run.py → tools/intelligence-report/


## 2026-04-12 — Establish vault separation policy as governance record and update AGENTS.md and skills/index.md to enforce the four-layer architecture rule.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/shared/separation-policy.md` — Created separation policy with four-layer table, allowed/excluded file lists, character.md contract, and Known Migration Debt audit ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Added Directory Boundaries section after Who Are You? table ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/index.md` — Added tools/ and inputs/ to Central Stores table ✅ Complete

**Handoff:** `handoff/complete/2026-04-12-p2-skill-separation-architecture-policy-COMPLETE.md`

**Next:** Execute 2026-04-12-p2-status-reports-skill-separation.md — migrate scripts, inputs, and manifest out of skills/product/status-reports/


## 2026-04-12 — Establish vault separation policy: document the four-layer architecture rule, update AGENTS.md and skills/index.md, and audit skills/ for existing violations.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/shared/separation-policy.md` — Created — four-layer separation policy with Known Migration Debt audit (13 scripts, 6 live data paths, 1 structural bug, 7 stale notes.md) ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Added Directory Boundaries section with four-layer table and hard constraint rule, cross-referencing separation-policy.md ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/index.md` — Added tools/ and inputs/ to Central Stores table ✅ Complete

**Handoff:** `handoff/2026-04-12-p2-skill-separation-architecture-policy.md`

**Next:** Execute companion migration handoff: 2026-04-12-p2-status-reports-skill-separation.md — move scripts, inputs, and manifest out of skills/product/status-reports/

