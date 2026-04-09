# Changelog for Skill Documentation Guide

This log tracks all significant structural, philosophical, or content changes made to the Skill documentation standards.

## [Unreleased]

## 2026-04-09 — Execute all 7 outstanding handoffs from 2026-04-08: fix orphaned index entries, fix casebook/reporting/index.md, create skill-builder subdirectory indexes, add Portal data sources + SKILL.md naming exemption, move reports/ into crypt-keeper, document root-level exemptions, and fix changelog fact-check issues.

**Files changed:**
- `/Users/benbelanger/GitHub/ben-cp/skills/crypt-keeper/index.md` — Added SKILL.md, changelog.md, and reports/ entries to contents table; fixed stale reports path reference ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/okr-reporting/index.md` — Added changelog.md entry to contents table ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/crypt-keeper.md` — Deleted root redirect stub via git rm ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/casebook/reporting/schema_joins.md` — Created — moved schema joins content from index.md with fixed paths (casebook-reporting/ → casebook/reporting/) ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/casebook/reporting/index.md` — Replaced schema joins doc with proper directory TOC listing all 9 files ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/skill-builder/mappings/index.md` — Created — new directory TOC for mappings/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/skill-builder/styles/index.md` — Created — new directory TOC for styles/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/skill-builder/rules/` — Removed empty directory ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/okr-reporting/data_sources.md` — Added Database (Direct) — Portal KRs section + /portal GA proxy row with engineering note ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/AGENTS.md` — Added SKILL.md/AGENTS.md naming exemption; updated vault tree (removed root reports/, added crypt-keeper/reports/); updated File Placement table; root exemptions already had CLAUDE.md and README.md ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/reports/` — Removed root reports/ directory (git rm -r); content already existed in skills/crypt-keeper/reports/ ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/crypt-keeper/procedure.md` — Updated output path from reports/ to skills/crypt-keeper/reports/; added archive step to Pre-Flight ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/handoff/complete/2026-04-08-changelog-refactor-COMPLETE.md` — Renamed from 2026-04-08-changelog-refactor.md (added -COMPLETE suffix) ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/handoff/complete/2026-04-09-consolidate-project-status-reports-COMPLETE.md` — Renamed from 2026-04-09-consolidate-project-status-reports.md (added -COMPLETE suffix) ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/changelog.md` — Fixed 1.4.1 phantom reports/archive/ path; expanded 1.5.0 with missing infrastructure changes; annotated stale Next Tasks in 1.2.0 and 1.3.0 ✅ Complete
- `/Users/benbelanger/GitHub/ben-cp/skills/casebook/changelog.md` — Fixed 1.1.0 wrong count: 4 unexposed → 3 unexposed API functions for subscriptions ✅ Complete

**Handoff:** `handoff/2026-04-08-p2-changelog-factcheck-COMPLETE.md`

**Next:** Run Crypt-Keeper to verify all P1/P2 flags from 2026-04-08 report are resolved


## [1.0.0] - Initial Release (YYYY-MM-DD)
*   Established the modular structure: Index, Workflow, Styling, Data Sources, and Changelog.
*   Defined the core philosophy of documenting processes as 'Contracts'.
*   Renamed documentation artifacts from 'SOP' to 'Skill' for broader applicability.