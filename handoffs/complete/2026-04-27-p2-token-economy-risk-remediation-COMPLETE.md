# Implementation Plan: 2026-04-27-p2-token-economy-risk-remediation

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Cowork
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-28

undefined

---

# Context
The Dream cycle context sensor (2026-04-26) flagged several files as token economy risks due to size or accumulation. The user prefers to handle these via repo handoffs rather than Asana tasks.

# Risks Identified

## RED FLAGS (>750KB - action required)
- `intelligence/product/shareout/q2/source/Q2 2026 Product Shareout.pdf` — 7,410 KB (7.2 MB)
  - **Question**: Should this large PDF live in the repo or be archived/offloaded?
- `reports/projects/data/raw/asana.json` — 1,441 KB
  - **Question**: Is this raw pipeline data needed long-term or should it be auto-purged?
- `reports/projects/data/raw/asana_all_projects.json` — 1,037 KB
  - **Question**: Same as above — raw pipeline artifact.

## YELLOW FLAGS (>500KB - monitor)
- `reports/projects/data/archive/archived_2026_04_11_jira_issues.json` — 644 KB
- `reports/projects/data/archive/archived_2026_04_10_jira_issues.json` — 641 KB
- `reports/projects/data/archive/archived_2026_04_09_jira_issues.json` — 636 KB
- `reports/projects/data/archive/archived_2026_04_06_jira_issues.json` — 633 KB
- `reports/projects/data/archive/archived_2026_04_05_jira_issues.json` — 597 KB
- `reports/projects/data/processed/jira_issues.json` — 536 KB

# Finalized Policy (Decisions)

1. **Q2 Shareout PDF**: Large binary PDF moved to `source/archive/`.
   - **Decision**: Keep in archive for Drive reference, but exclude from repo health scans (which ignore `archive/` paths).
2. **Raw Data Purge**: 
   - **Decision**: Purge `reports/**/data/raw/*.json` files automatically at the end of every successful pipeline run.
3. **Retention Policy (Snapshots)**:
   - **Decision**: Implement a rolling retention of **3 snapshots** for `archive/` directories.

# Execution Steps
- [x] Move `Q2 2026 Product Shareout.pdf` to `source/archive/`.
- [ ] Implement `prune_archive()` function in `skills/status/scripts/run.py` and `skills/intelligence/run.py`.
- [ ] Add `os.remove()` calls for raw JSON snapshots at the end of pipeline runners.
- [ ] Run `generate_report(skill='dream')` to verify "Red Flags" are cleared.
