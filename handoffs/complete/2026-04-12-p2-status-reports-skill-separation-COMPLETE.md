---
title: 'Implementation Plan: status-reports-skill-separation'
type: handoff
domain: handoffs/complete
---


# Implementation Plan: status-reports-skill-separation

> **Prepared by:** Antigravity (Gemini) (2026-04-12)
> **Assigned to:** Claude Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **v1.0**
> **STATUS**: ✅ COMPLETE

Migrated skills/product/status-reports/ from a three-layer mixed directory to a clean two-file skill stub. All execution tooling moved to tools/status-reports/ (scripts, run_pipeline.sh, tests). All live data moved to inputs/status-reports/ (raw/, processed/, archive/, manifest.json). Generated log moved to outputs/status-reports/. Updated all path constants in 8 Python scripts + shell wrapper to compute REPO_ROOT from __file__ and resolve all data paths from repo root. Updated manifest.json config and step file paths. Updated index.md kickstart commands. Wrote READMEs for tools/ and inputs/ layers. Smoke tested — all paths resolve correctly. Note: files were untracked (never committed), so filesystem mv was used rather than git mv; no git history existed to preserve.

**Changelog:** (see root changelog.md)


---

## Context

`skills/product/status-reports/` is the primary violation of the repo's skill separation policy (see companion handoff `2026-04-12-p2-skill-separation-architecture-policy.md`, which must be completed first). It currently mixes three layers in one directory:

- **Skill logic** (correct): `index.md`, `SKILL.md`, `changelog.md`
- **Execution tooling** (wrong location): `scripts/full_run.py`, `step_*.py`, `render_html.py`, `platform_report.py`, `update_manifest.py`, `run_pipeline.sh`
- **Live data** (wrong location): `inputs/raw/asana.json`, `inputs/raw/jira_issues.json`, `inputs/processed/asana_active.json`, `manifest.json`, and an entire `inputs/archive/` tree of 20+ dated HTML and JSON files

**After this migration:**
- `skills/product/status-reports/` contains only: `SKILL.md`, `index.md`, `changelog.md`
- `tools/status-reports/` contains: all scripts
- `inputs/status-reports/` contains: `manifest.json`, `raw/`, `processed/`, `archive/`
- `outputs/status-reports/` contains: generated HTML reports (ongoing)

The scripts use relative path resolution anchored to `manifest.json` location. All path constants in the scripts must be updated to reflect the new layout.

---

## Prerequisites

- `2026-04-12-p2-skill-separation-architecture-policy.md` must be COMPLETE before this runs
- Read `skills/product/status-reports/SKILL.md` and `scripts/full_run.py` in full before touching any files — the path logic is non-trivial

---

## Execution Order

1. **Read and map current paths** — understand all hardcoded and manifest-driven path resolution in the scripts
2. **Create new directory structure** — `tools/status-reports/`, `inputs/status-reports/`, `outputs/status-reports/`
3. **Move scripts** — git mv all `.py` and `.sh` files to `tools/status-reports/scripts/`
4. **Move input data** — git mv `inputs/` tree to `inputs/status-reports/`
5. **Move manifest** — git mv `manifest.json` to `inputs/status-reports/manifest.json`
6. **Update path constants in scripts** — fix all path resolution to point to new locations
7. **Update `SKILL.md`** — replace all path references to scripts and inputs with new locations
8. **Update `manifest.json`** — update the `config` block's `processed_dir` and `archive_dir` values
9. **Smoke test** — verify `full_run.py --help` or a dry run resolves paths without error
10. **Changelog + completion**

---

## Task 1: Read and Map Paths

Before moving anything, read `scripts/full_run.py` in full and document every path constant:

Key path vars to track:
- `MANIFEST_PATH` — currently anchored relative to `__file__` (the script), navigating up to `../manifest.json`
- `REPO_ROOT` — derived from `MANIFEST_PATH`'s parent
- `ASANA_RAW`, `JIRA_RAW_DIR`, `ASANA_FILTERED`, `JIRA_HARVESTED`, `OUTPUT_PATH` — all derived from `REPO_ROOT` + manifest step `file` values
- `.env` loader: navigates two levels up from `REPO_ROOT` to find the `.env` at repo root

After the move:
- Scripts live at `tools/status-reports/scripts/full_run.py`
- `MANIFEST_PATH` must navigate from the script to `inputs/status-reports/manifest.json`
- `REPO_ROOT` will change meaning — it should now point to the repo root (`ben-cp/`), not `skills/project-status-reports/`
- `.env` loader: navigate from repo root to repo root (one level up, not two)

---

## Task 2: Create Directory Structure

```
tools/
  status-reports/
    scripts/         ← destination for all .py and .sh files

inputs/
  status-reports/
    raw/             ← asana_all_projects.json, jira/, etc.
    processed/       ← asana_active.json, jira_issues.json, etc.
    archive/         ← dated HTML and JSON archives

outputs/
  status-reports/    ← generated HTML reports land here going forward
```

Create `tools/status-reports/README.md` and `inputs/status-reports/README.md` as minimal orientation files (one paragraph each — purpose, what lives here, how to invoke).

---

## Task 3: Move Scripts

```bash
git mv skills/product/status-reports/scripts/ tools/status-reports/scripts/
git mv skills/product/status-reports/run_pipeline.sh tools/status-reports/run_pipeline.sh
```

Also move `tests/` if present:
```bash
git mv skills/product/status-reports/tests/ tools/status-reports/tests/
```

Do not move `__pycache__/` — delete it:
```bash
rm -rf skills/product/status-reports/scripts/__pycache__
```

---

## Task 4: Move Input Data

```bash
git mv skills/product/status-reports/inputs/ inputs/status-reports/
```

This moves the entire tree: `raw/`, `processed/`, `archive/`.

---

## Task 5: Move Manifest

If `manifest.json` is at `skills/product/status-reports/manifest.json`:
```bash
git mv skills/product/status-reports/manifest.json inputs/status-reports/manifest.json
```

---

## Task 6: Update Path Constants in Scripts

In `tools/status-reports/scripts/full_run.py`, update:

```python
# OLD — navigated up from script to sibling manifest.json
MANIFEST_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../manifest.json")
REPO_ROOT = os.path.dirname(os.path.abspath(MANIFEST_PATH))

# NEW — navigate from tools/status-reports/scripts/ up to repo root, then into inputs/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))   # tools/status-reports/scripts/ → repo root
MANIFEST_PATH = os.path.join(REPO_ROOT, "inputs/status-reports/manifest.json")
```

Update the `.env` loader to walk one level up from `REPO_ROOT` (to repo root), not two.

Update `OUTPUT_PATH` default target — report output should resolve to `outputs/status-reports/`.

Check `step_0_asana_refresh.py`, `step_1_asana_ingest.py`, `step_2_atlassian_fetch.py`, `step_3_jira_harvest.py`, `step_4_report_generator.py`, and `update_manifest.py` for any independent path constants that also need updating. Any script that computes its own `REPO_ROOT` or data paths must be updated consistently.

---

## Task 7: Update `SKILL.md`

In `skills/product/status-reports/SKILL.md` (formerly `index.md`), update all path references:

- Kickstart command: `python3 tools/status-reports/scripts/full_run.py --force`
- Any references to `inputs/raw/`, `inputs/processed/`, `inputs/archive/` → `inputs/status-reports/raw/` etc.
- Any references to `scripts/` → `tools/status-reports/scripts/`
- Any references to `manifest.json` → `inputs/status-reports/manifest.json`
- Output path references → `outputs/status-reports/`

---

## Task 8: Update `manifest.json`

Open `inputs/status-reports/manifest.json` and update the `config` block:

```json
"config": {
    "processed_dir": "inputs/status-reports/processed",
    "archive_dir": "inputs/status-reports/archive"
}
```

Also update any `file` values in the `steps` array that reference relative paths — they should now be relative to repo root.

---

## Task 9: Smoke Test

Run from repo root:
```bash
python3 tools/status-reports/scripts/full_run.py
```

Expected: path resolution works, no `FileNotFoundError` on manifest or input files. A full re-run is not required — just confirm the path logic resolves cleanly (can abort after manifest loads successfully).

If any `import` fails because scripts previously imported from sibling files (e.g. `from platform_report import ...`), add the scripts directory to `sys.path` at the top of `full_run.py`:
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

---

## Task 10: Changelog + Completion

- Subdirectory changelogs: `skills/product/status-reports/changelog.md`, `tools/status-reports/` (new), `inputs/status-reports/` (new)
- Root changelog: one-line summary
- Move this handoff to `handoff/complete/`

---

## Notes for This Agent

- Use `git mv` for all file moves — not `cp` or filesystem moves. Preserving git history on scripts matters.
- The `__pycache__` directories should be deleted, not moved. They are build artifacts.
- Do not touch `skills/product/status-reports/SKILL.md`, `index.md`, or `changelog.md` — these stay in the skill directory. That is the correct residue after migration.
- The `product/shared/shared/` double-nesting is a separate bug — do not fix here, but note it in your changelog if you encounter it.
- After migration, `skills/product/status-reports/` should contain exactly 3 files: `SKILL.md`, `index.md`, `changelog.md`. If anything else remains, it is a violation.
- The `inputs/archive/` tree has 20+ dated files. Move the whole tree wholesale — do not curate or delete anything.
