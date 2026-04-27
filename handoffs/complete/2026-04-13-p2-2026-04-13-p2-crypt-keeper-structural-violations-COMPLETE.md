---
title: Implementation Plan Crypt-Keeper  Structural Violations
type: handoff
domain: handoffs/complete
---

# Implementation Plan: Crypt-Keeper — Structural Violations

> **Prepared by:** Claude (Cowork) (Intelligence (Memory) scheduled run, 2026-04-13)
> **Assigned to:** Claude
> **Vault root:** `/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp`
> **Priority:** P2 — Structural violations (duplicates, misplaced files, lingering notes.md, AGENTS.md compliance gaps)
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-13.md`
> **v1.0**
> **STATUS**: ✅ COMPLETE

Executed a full structural cleanup based on the Crypt-Keeper audit. Resolved data source duplication, purged stale session artifacts, and verified directory boundary compliance. Updated the vault separation policy to mark identified debt as resolved.

---

## Context

The 2026-04-13 Intelligence (Memory) run identified several P2 structural violations: two data_sources.md files in the product domain (likely duplicate coverage), a double-nested `product/shared/shared/` directory with a spurious `vault.css` copy, and 7 lingering ephemeral `notes.md` files that should have been deleted after their respective sessions. These are known in `shared/separation-policy.md` but remain unresolved.

---

## Execution Order

1. **Task 1** — Resolve duplicate data_sources.md in product domain
2. **Task 2** — Remove double-nested `product/shared/shared/vault.css`
3. **Task 3** — Delete lingering ephemeral notes.md files (5 confirmed empty, 1 confirmed stale)
4. **Task 4** — AGENTS.md compliance spot-check (defer to P1 handoff if AGENTS.md not yet restored)
5. **Task 5** — Write changelog and mark complete

---

## Task 1: Resolve Duplicate data_sources.md

Two files cover overlapping territory:
- `product/shared/data_sources.md` — covers GA4, Casebook Admin, Asana, ChurnZero; shared across status-reports and okr-reporting
- `product/projects/data_sources.md` — covers KR-level metric mapping for OKR reporting (Notes Quick Entry, Service Notes, Enrollments, Locked Notes, Datagrid Shortcuts)

**Recommendation:** These serve distinct purposes and should both be kept, but `product/projects/data_sources.md` should be renamed to `product/projects/okr-data-sources.md` or moved to `product/okr-reporting/data_sources.md` to reduce confusion. Read both files in full, compare coverage, and update cross-references accordingly. Do not delete either without confirming no unique content is lost.

---

## Task 2: Remove Spurious `product/shared/shared/` Directory

`product/shared/shared/vault.css` is a double-nesting artifact from a migration. The canonical `vault.css` lives at `styles/vault.css`. Per `shared/separation-policy.md` § Known Migration Debt:

> `skills/product/shared/shared/vault.css` — double-nesting artifact; `product/shared/shared/` is a spurious extra directory layer (→ remove duplicate; `vault.css` canonical copy lives at `skills/styles/vault.css`)

Steps:
1. Read `product/shared/shared/vault.css` and `styles/vault.css` — confirm they are identical
2. If identical: delete `product/shared/shared/vault.css` and the empty `product/shared/shared/` directory
3. If different: flag the diff for Ben's review before deleting
4. Update `product/shared/separation-policy.md` to mark this item ✅

---

## Task 3: Delete Lingering Ephemeral notes.md Files

Per `shared/separation-policy.md` § Stale Ephemeral Session Files, these files must be deleted:

- `orchestration/changelog/notes.md` — confirmed empty, stale
- `orchestration/access/notes.md` — confirmed empty, stale
- `intelligence/memory/notes.md` — confirmed empty, stale
- `intelligence/analyze/synthesize/notes.md` — confirmed empty, stale
- `intelligence/analyze/predict/notes.md` — confirmed empty, stale

**Do NOT delete:**
- `orchestration/notes/notes.md` — this is the PRIMARY vault notes file (confirmed active with entries dated 2026-04-12 and 2026-04-13). This is intentional, not ephemeral.

For each file to delete: read it first to confirm it is empty/stale, then delete. Log each deletion in changelog.

Note: `shared/separation-policy.md` also lists `skills/product/notes.md` — verify whether this path resolves in the current vault structure before acting.

---

## Task 4: AGENTS.md Compliance Spot-Check

This task depends on the P1 handoff (AGENTS.md restoration) being complete first. Once AGENTS.md exists:

Identify the 3 most recently modified files in the vault (excluding knowledge outputs/reports). For each verify:
- Correct path per AGENTS.md directory boundaries
- Referenced in parent index.md
- Filename uses hyphens or underscores (no camelCase)

The most recently active files based on this scan are likely in `orchestration/notes/` and `product/` domains given the 2026-04-13 activity noted in notes.md.

---

## Task 5: Changelog + Completion

Write changelog entries (subdirectory `knowledge` first, then root), then mark this file complete and move to `handoff/complete/`.

---

## Notes for This Agent
- Read before every write — no exceptions
- Do NOT delete `orchestration/notes/notes.md` — it is the active primary notes file, not a stale ephemeral
- AGENTS.md compliance check (Task 4) must wait for P1 handoff to complete first
- Update `shared/separation-policy.md` migration debt items to ✅ as each is resolved
