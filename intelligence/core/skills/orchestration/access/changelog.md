# Access Changelog

> Detail log for `skills/access/`. See root `changelog.md` for version history.

---

## [Unreleased]

## 2026-04-12 — Codify the separation policy as a standing enforcement check: add Separation Policy Scan to Roz's nightly audit procedure, and extend Robert's diff_checker to watch Directory Boundaries consistency.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/orchestration/access/SKILL.md` — Added Step 2 — Separation Policy Scan (ALWAYS RUN): walks skills/ for scripts, manifests, data files, logs; flags new violations as P1 handoff; known debt items as P2 after 7+ days ✅ Complete
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/intelligence/analysis/synthesize/diff_checker.md` — Extended Step 3 to read separation-policy.md and Step 4 to watch for Directory Boundaries drift between AGENTS.md and separation-policy.md ✅ Complete

**Next:** Execute migration handoff 2026-04-12-p2-status-reports-skill-separation.md — move scripts, inputs, manifest out of skills/product/status-reports/


## 2026-04-12 — Add deletion and overwrite watch to access audit skill — any agent/skill/tool advocating destructive operations is an automatic P1 violation.

**Files changed:**
- `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/skills/access/SKILL.md` — Added Step 2 — Deletion & Overwrite Watch: scans all agent outputs, skills, handoffs, and changelogs for any language advocating deletion or overwrite; flags as P1 violation. Defined approved exceptions (notes.md cleanup, git mv for archiving). ✅ Complete

**Next:** Execute P2 handoff: add missing index.md to dream/, predict/, changelog/lumberjack/ and archive agents/roz.md

