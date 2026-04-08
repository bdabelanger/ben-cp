# Project Status Reports Changelog

> Detail log for `skills/project-status-reports/`. See root `changelog.md` for version history.
> Use `write_changelog_entry` to append — never overwrite this file.

---

## [Unreleased]

---

## [1.1.0] - Pipeline Consolidation (2026-04-09)

**Changes:**
- Pipeline moved from `project-status-reports/` (vault root) into this directory
- `scripts/`, `inputs/`, `outputs/`, `logs/`, `tests/`, `manifest.json`,
  `run_pipeline.sh` all now live under `skills/project-status-reports/`
- Run path updated in `index.md`: `skills/project-status-reports/scripts/full_run.py`
- Root `project-status-reports/` directory removed

**Rationale:** Skill is now self-contained — runbook, code, and changelog in one place.

**⚠️ Flag for Ben:** `full_run.py` derives the `.env` path as `dirname(REPO_ROOT)`.
Before consolidation: `project-status-reports/ → ben-cp/.env` ✓
After consolidation: `skills/project-status-reports/ → skills/.env` ✗
Fix: change `os.path.dirname(REPO_ROOT)` to `os.path.dirname(os.path.dirname(REPO_ROOT))`
in `full_run.py` line 17. One-line change — awaiting Ben's approval before editing script.

---

## [0.1.0] - Stub (2026-04-08)

**Current state:** Directory exists with `outputs/` and `scripts/` subdirectories. No changelog history prior to this entry.

**TODOs:**
- None known — add when project-status-reports work resumes
