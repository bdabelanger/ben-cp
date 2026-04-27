# Implementation Plan: Review Flattened Vault Orchestration

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Cowork
> **Vault root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-27

Audited all run.py files in skills/. Standardized REPO_ROOT paths. Fixed status pipeline imports and legacy path references. Smoke tested pipelines.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/handoffs/2026-04-27-p1-Review-Flattened-Vault-Orchestration.mdScan

---

# Review Flattened Vault Orchestration

## Context
The vault has been flattened to remove redundant nesting:
- `skills/pipelines/[skill]` -> `skills/[skill]`
- `skills/skills/dream` -> `skills/dream`
- `skills/intelligence/governance` -> `intelligence/governance`

During this process, the Intelligence Pipeline scripts were accidentally deleted and have been reconstructed in their new home at `skills/intelligence/`.

## Logic
All pipeline orchestrators (`run.py` files) in the `skills/` domain must now use exactly **two** parent joins (`..`, `..`) to reach the `REPO_ROOT`. 

## Execution Steps
1. [ ] **Verify `run.py` Paths**: Audit `skills/asana/run.py`, `skills/tasks/run.py`, `skills/status/run.py`, and `skills/intelligence/run.py` to ensure `REPO_ROOT` is correctly calculated.
2. [ ] **Smoke Test Pipelines**: Run each pipeline via the `npx` platform command or direct `python3` calls to verify they produce reports in the `reports/` directory correctly.
3. [ ] **Update TS SDK**: Ensure `src/ben-cp.ts` is fully updated with the new paths for all report generation commands.
4. [ ] **Final Integrity Check**: Ensure no remaining references to `pipelines/` or `skills/skills/` exist in any `SKILL.md` or SOP.
