# Implementation Plan: Fix Frontmatter Sensor Dependency and Add Requirements File

> **Prepared by:** Code (Gemini) (2026-04-27)
> **Assigned to:** Code
> **Repo root:** /Users/benbelanger/My Drive (ben.belanger@casebook.net)/ben-cp
> **Priority:** P2
> **STATUS**: ✅ COMPLETE — 2026-04-27

Explicitly declared Python dependencies in requirements.txt and updated README.md with setup instructions and corrected runner paths. Verified frontmatter sensor is operational.

---

## Context

The frontmatter sensor failed tonight with `ModuleNotFoundError: No module named 'yaml'`. The same error also caused the intelligence harvest and scan pipelines to fail initially.

During this Dream run, Cowork installed `pyyaml` and `requests` via pip (`pip3 install pyyaml requests --break-system-packages`) to unblock the intelligence pipelines. Those are now installed on Ben's machine. However, the repo has no `requirements.txt` or dependency manifest, so this will silently re-break on any new environment or after a Python upgrade.

## Goal

Make the repo's Python dependencies explicit and ensure the frontmatter sensor and all skill scripts declare their requirements so they can be reliably installed.

## Execution Steps

1. Audit all Python scripts under `skills/` for `import` statements — collect all third-party deps (not stdlib).
2. Create a `requirements.txt` at the repo root listing all third-party deps with pinned or minimum versions. At minimum: `pyyaml>=6.0`, `requests>=2.28`.
3. Add a `## Setup` section to the repo `README.md` (or create one) with: `pip3 install -r requirements.txt --break-system-packages`.
4. Verify the frontmatter sensor runs clean after the install: `generate_report(skill='dream')` → frontmatter sensor should show 🟢 or 🟡 (not 🔴 FAILED).

## Verification

- `generate_report(skill='dream')` → frontmatter sensor no longer errors
- `requirements.txt` exists at repo root with all required deps
- Intelligence pipelines run without import errors
