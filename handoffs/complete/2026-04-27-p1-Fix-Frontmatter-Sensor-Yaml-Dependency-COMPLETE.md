# Implementation Plan: Fix Frontmatter Sensor Yaml Dependency

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P1
> **STATUS**: ✅ COMPLETE — 2026-04-27

Successfully fixed the frontmatter sensor by confirming PyYAML is present and verified with a clean sensor run. Also created a root requirements.txt for future dependency management.Scan/Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp/Scan

---

## Context

The `frontmatter` sensor failed entirely in the 2026-04-27 Dream cycle with the error:

```
❌ frontmatter failed: No module named 'yaml'
```

This sensor has been blind since at least this run — it cannot audit any frontmatter in the repo while the `yaml` (PyYAML) dependency is missing from the environment.

## Goal

Install the missing dependency and confirm the frontmatter sensor runs clean.

## Execution Steps

1. Locate the dream sensor runner — likely `reports/dream/run.py` or similar in the repo's `src/` directory.
2. Check the project's dependency file (`requirements.txt`, `pyproject.toml`, or equivalent).
3. Add `pyyaml` if missing from the dependency declaration.
4. Install: `pip install pyyaml` (or `pip install -r requirements.txt --break-system-packages` as appropriate for the environment).
5. Re-run `generate_report(skill='dream')` and confirm frontmatter sensor returns a result (pass or findings) rather than an error.

## Verification

- `generate_report` output shows `✅ frontmatter` (not `❌ frontmatter failed`).
- Sensor result file `reports/dream/data/raw/frontmatter_report.json` exists and is valid JSON.
