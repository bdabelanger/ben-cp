# Implementation Plan: 2026-04-13-p1-crypt-keeper-agent-navigation-broken

> **Prepared by:** Antigravity (Gemini) (2026-04-13)
> **Assigned to:** Any
> **Vault root:** /Users/benbelanger/GitHub/ben-cp
> **Priority:** P1
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

# Any Agent Implementation Plan: P1 Crypt-Keeper — Agent Navigation Broken

> **Prepared by:** Claude (Cowork) (Crypt-Keeper scheduled run, 2026-04-13)
> **Assigned to:** Any
> **Vault root:** `/Users/benbelanger/GitHub/ben-cp`
> **Priority:** P1 — Agent navigation broken (missing AGENTS.md, missing index.md files, orphaned files)
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-13.md`
> **v1.0**
> **STATUS: 🔲 READY — pick up 2026-04-13**

---

## Context

The 2026-04-13 Crypt-Keeper run identified critical P1 structural issues that break agent navigation. Most critically, `AGENTS.md` does not exist at the vault root — this is a hard blocker for any agent attempting to orient itself. Several subdirectories also lack `index.md` files, and orphaned files exist with no index entries. These must be resolved before agents can reliably navigate the vault.

---

## Execution Order

1. **Task 1** — Recreate or restore `AGENTS.md` at vault root
2. **Task 2** — Create missing `index.md` for `intelligence/report/`
3. **Task 3** — Create missing `index.md` for `intelligence/memory/retrieval/`
4. **Task 4** — Create missing `index.md` for `intelligence/memory/intake/`
5. **Task 5** — Create missing `index.md` for `intelligence/memory/audit/`
6. **Task 6** — Create missing `index.md` for `styles/`
7. **Task 7** — Create missing `index.md` for `shared/`
8. **Task 8** — Resolve orphaned `intelligence/report/report_spec.json` (add to index once Task 2 complete)
9. **Task 9** — Reconcile memory index naming mismatch (index references `learn/`, `recall/`, `mapping/`, `watchdog/` but vault dirs are `retrieval/`, `intake/`, `audit/`)
10. **Task 10** — Write changelog and mark complete

---

## Task 1: Restore AGENTS.md

AGENTS.md is referenced throughout the vault as the authoritative governance document — agent dispatch table, directory boundaries, universal rules, the Agent's Creed. It does not exist at `/Users/benbelanger/GitHub/ben-cp/AGENTS.md`. Check git history to see if it was accidentally deleted:

```
git log --oneline --all -- AGENTS.md
git show <commit>:AGENTS.md
```

If recoverable from git: restore it. If not: reconstruct from references in `shared/separation-policy.md`, `orchestration/handoff/index.md`, `intelligence/analyze/synthesize/diff_checker.md`, and skill SKILL.md files. The file must include at minimum: Agent's Creed, Agent Dispatch Table, Directory Boundaries (matching `shared/separation-policy.md`), Universal Rules, and notes.md Write Policy.

---

## Task 2: Create `intelligence/report/index.md`

`intelligence/report/` contains only `report_spec.json` with no index.md. Draft a starter:

```markdown
# Report Domain Index

> **Purpose:** Daily Progress Summary (Dream Cycle) orchestration and output spec.
> **Last updated:** 2026-04-13

## Contents

| File | Purpose |
| :--- | :--- |
| `report_spec.json` | Digest Editor routing spec — preferred agent: Antigravity, cadence: daily |

## Notes
- Execution script `run.py` is pending migration to `tools/intelligence-report/` per separation-policy.md
```

---

## Task 3–5: Create missing `index.md` for memory sub-skills

For each of `intelligence/memory/retrieval/`, `intelligence/memory/intake/`, `intelligence/memory/audit/` — draft a minimal index.md listing the files present (SKILL.md, audit.md, report.md) and their purpose. Use the existing SKILL.md for each as the source of purpose/description.

---

## Task 6: Create `styles/index.md`

`styles/` contains `SKILL.md`, `audit.md`, `report.md`, `vault.css` but no index.md. Starter:

```markdown
# Styles Index

> **Purpose:** Visual syntax authority — emoji glossary, vault nomenclature, and global CSS.
> **Last updated:** 2026-04-13

## Contents

| File | Purpose |
| :--- | :--- |
| `SKILL.md` | Skill descriptor |
| `audit.md` | Audit procedure |
| `report.md` | Visual glossary and report template |
| `vault.css` | Global CSS tokens for HTML-rendered reports |
```

---

## Task 7: Create `shared/index.md`

`shared/` contains `changelog.md` and `separation-policy.md` but no index.md. Starter:

```markdown
# Shared Index

> **Purpose:** Cross-cutting vault governance documents.
> **Last updated:** 2026-04-13

## Contents

| File | Purpose |
| :--- | :--- |
| `separation-policy.md` | Vault layer separation rules — what belongs where |
| `changelog.md` | Shared domain change history |
```

---

## Task 9: Reconcile Memory Index Naming

`intelligence/memory/index.md` references sub-skills as `learn/`, `recall/`, `mapping/`, `watchdog/` but the actual vault directories (per list_vault) are `retrieval/`, `intake/`, `audit/`. Either:
- The index is outdated and the dirs were renamed — update the index to match physical dirs
- The index is correct and the dirs were incorrectly renamed — restore correct names

Read git history for `intelligence/memory/` to determine which names are authoritative before editing.

---

## Task 10: Changelog + Completion

Write changelog entries (subdirectory `knowledge` first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Read before every write — no exceptions
- Never delete vault files — create or edit only
- AGENTS.md restoration is the highest priority in this list; do it first
- Do not guess at AGENTS.md content — recover from git or reconstruct conservatively from references
- Character names are not used in any outputs — use generic skill names only
