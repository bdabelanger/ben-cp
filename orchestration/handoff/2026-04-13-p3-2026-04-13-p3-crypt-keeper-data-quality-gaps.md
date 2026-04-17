# Implementation Plan: Crypt-Keeper — Data Quality Gaps

> **Prepared by:** Gemma (Local)
> **Assigned to:** Cowork (For Guidance)
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P3 — Data quality gaps (missing KR SOP files, data_sources.md sync, stale migration debt flags)
> **Source report:** `skills/knowledge/outputs/reports/knowledge-report-2026-04-13.md`
> **v1.0**
> **STATUS**: 🔲 READY — pick up 2026-04-13

---

## Context
The 2026-04-13 Intelligence (Memory) run found that `product/projects/data_sources.md` references 6 KR SOP files that do not exist on disk. It also found migration debt items from 2026-04-12.

## Findings & Blockers

### Task 1: Missing KR SOP Files (BLOCKED)
- **Result**: Directory `product/projects/q2-2026` does not exist in the vault structure. Attempts to check git history were inconclusive regarding creation or removal of the 6 referenced files.
- **Action Required from Cowork**: Please advise if these files should be flagged as Q2 OKR documentation debt (do not fabricate content) or if they need restoration from a previous state.

### Task 2: Migration Debt — intelligence/report/run.py (UNCLEAR)
- **Result**: The expected script path `skills/intelligence/report/run.py` does not exist in the vault structure, though related tasks exist in `tools/intelligence-report/`.
- **Action Required from Cowork**: Confirm if this migration is complete or if a different agent should handle the cleanup of the debt flag in `shared/separation-policy.md`.

### Task 3: Update Portal KR Blocker Status (UNCLEAR)
- **Result**: Recent notes confirm ongoing work on JIRA/Visualization but do not provide a definitive status update or resolution date for the Portal data model blocker.
- **Action Required from Cowork**: Please advise if I should stamp the current date onto `product/projects/data_sources.md` to track age, or wait for confirmation.

## Next Steps (Awaiting Guidance)
I am pausing execution until guidance is received on how to resolve documentation debt and status ambiguity.